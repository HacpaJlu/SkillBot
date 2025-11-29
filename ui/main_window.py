# gui.py — Полная финальная версия (все функции есть, всё работает)
import json
import os
import warnings

import keyboard
from core import APP_NAME, __version__
from PyQt6.QtCore import QEvent, QTimer, QCoreApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QLabel, QTextEdit,
    QSystemTrayIcon, QMessageBox, QInputDialog, QLineEdit, QSizePolicy
)
warnings.filterwarnings("ignore", category=UserWarning, module="PyQt6")
from core.autopot import AutopotTab
from core.bot import SkillBot
from ui.tabs.help_tab import HelpTab
from ui.tabs.main_tab import MainTab
from ui.tabs.settings_tab import SettingsTab
from ui.tabs.overlay_tab import OverlayTab
from ui.widgets.overlay_window import OverlayWindow
PROFILES_DIR = "profiles"
CONFIG_DIR = "config"
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")
os.makedirs(PROFILES_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Title uses central APP_NAME and __version__ constants
        try:
            self.setWindowTitle(f"{APP_NAME} {__version__}")
        except Exception:
            self.setWindowTitle("SkillBot")
        
        # Set application icon
        try:
            icon_path = "icon.png"
            app_icon = QIcon(icon_path)
            self.setWindowIcon(app_icon)
        except Exception:
            pass
        self.resize(900, 650)
        self.setMinimumSize(600, 450)  # Уменьшаем минимальный размер для лучшей адаптивности
        
        # Применение современных стилей
        from ui.styles import apply_modern_style
        apply_modern_style(self)
        
        # Устанавливаем политику размера для адаптивности
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.bot = SkillBot()
        self.bot.update_signal.connect(self.update_status)
        self.bot.log_signal.connect(self.update_log)

        self.current_profile = "default"
        self.hotkey = "f8"
        self.autopot_tab = None
        self.debug_page = None
        self.overlay_tab = None
        self.overlay_window = None

        self.load_settings()  # ← теперь функция есть!
        # Create a system tray icon for toast/balloon notifications
        try:
            # Use the application icon from the main directory
            icon_path = "icon.png"
            icon = QIcon(icon_path)
            
            self.tray = QSystemTrayIcon(self)
            self.tray.setIcon(icon)
            
            # Some platforms require showing the icon before messages
            try:
                self.tray.setVisible(True)
            except Exception:
                pass
        except Exception:
            self.tray = None
        self.load_window_size()

        self.init_ui()
        self.load_profiles()
        
    def resizeEvent(self, event):
        """
        Обработчик изменения размера окна для адаптивности
        """
        # Обновляем свойство размера экрана для стилей
        screen_size = "large"
        if self.width() < 1000:
            screen_size = "medium"
        if self.width() < 768:
            screen_size = "small"
        
        self.setProperty("screen", screen_size)
        try:
            style = self.style()
            if style:
                style.unpolish(self)
                style.polish(self)
        except:
            pass  # Игнорируем ошибки стиля
        
        # Вызываем базовый обработчик
        super().resizeEvent(event)

        # Install global event filter to clear focus from QLineEdit when clicking elsewhere
        try:
            app_instance = QApplication.instance()
            if app_instance:
                app_instance.installEventFilter(self)
        except Exception:
            pass

        self.bot.running = True
        self.bot.start()

        last = self.load_last_profile()
        if last and self.settings_tab.profile_combo.findText(last) != -1:
            self.settings_tab.profile_combo.setCurrentText(last)

        self.safe_load_profile(self.settings_tab.profile_combo.currentText())
        self.setup_main_hotkey()
        self.setup_panic_hotkey()

        # QTimer.singleShot(100, lambda: self.tabs.setCurrentIndex(0))  # Временно отключено

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.main_tab = MainTab(self)
        self.tabs.addTab(self.main_tab, "Главная")

        self.settings_tab = SettingsTab(self)
        self.tabs.addTab(self.settings_tab, "Настройки")
        # self.settings_tab.overlay_tab_cb.stateChanged.connect(self.toggle_overlay_tab)  # Временно отключено

        self.debug_page = QTextEdit()
        self.debug_page.setReadOnly(True)
        self.debug_page.setStyleSheet(
            "background:#111;color:#00ff00;font-family:Consolas;font-size:15px;"
        )

        self.help_tab = HelpTab()
        self.tabs.addTab(self.help_tab, "Помощь")
        tab_bar = self.tabs.tabBar()
        if tab_bar:
            tab_bar.moveTab(
                self.tabs.indexOf(self.help_tab), self.tabs.count() - 1
            )

    def show_toast(self, title: str, message: str, timeout: int = 5000):
        """Show unobtrusive toast/balloon notification via system tray if available.

        Falls back to writing to the main log if tray is unavailable.
        """
        # Schedule display on the Qt event loop to be thread-safe
        def _show():
            try:
                if hasattr(self, "tray") and self.tray:
                    # Создаем простую иконку для совместимости
                    self.tray.showMessage(title, message, QIcon(), timeout)
                else:
                    self.update_log(f"{title}: {message}")
            except Exception:
                try:
                    self.update_log(f"{title}: {message}")
                except Exception:
                    pass

        try:
            QTimer.singleShot(0, _show)
        except Exception:
            _show()

    def toggle_debug_tab(self):
        show = self.settings_tab.debug_cb.isChecked()
        self.bot.debug = show
        idx = self.tabs.indexOf(self.debug_page)
        if show and idx == -1:
            self.tabs.insertTab(self.tabs.count() - 1, self.debug_page, "Отладка")
        elif not show and idx != -1:
            self.tabs.removeTab(idx)

    def toggle_overlay_tab(self):
        show = self.settings_tab.overlay_tab_cb.isChecked()
        if show and not self.overlay_tab:
            if not self.overlay_window:
                self.overlay_window = OverlayWindow(self)
                self.overlay_window.show()
                # Сразу применяем настройки из текущего профиля
                if hasattr(self, "current_profile"):
                    path = os.path.join(PROFILES_DIR, f"{self.current_profile}.json")
                    if os.path.exists(path):
                        try:
                            with open(path, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                overlay_cfg = data.get("overlay", {})
                                clean = {k: v for k, v in overlay_cfg.items() if k != "show_tab"}
                                self.overlay_window.load_settings(clean)
                        except Exception as e:
                            self.bot.log_signal.emit(f"Ошибка загрузки настроек оверлея: {e}")
            self.overlay_tab = OverlayTab(self)
            self.tabs.insertTab(self.tabs.count() - 1, self.overlay_tab, "Оверлей")
            if self.overlay_window and hasattr(self, "current_profile"):
                # Повторно загружаем настройки для вкладки после её создания
                path = os.path.join(PROFILES_DIR, f"{self.current_profile}.json")
                if os.path.exists(path):
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            overlay_cfg = data.get("overlay", {})
                            clean = {k: v for k, v in overlay_cfg.items() if k != "show_tab"}
                            self.overlay_tab.load_from_dict(clean)
                    except Exception as e:
                        self.bot.log_signal.emit(f"Ошибка загрузки настроек оверлея: {e}")
        elif not show and self.overlay_tab:
            self.tabs.removeTab(self.tabs.indexOf(self.overlay_tab))
            self.overlay_tab = None
            if self.overlay_window:
                self.overlay_window.close()
                self.overlay_window = None

    def toggle_autopot_tab(self):
        show = self.settings_tab.autopot_tab_cb.isChecked()
        if show and not self.autopot_tab:
            self.autopot_tab = AutopotTab(self)
            self.tabs.insertTab(self.tabs.count() - 1, self.autopot_tab, "Автопот")
        elif not show and self.autopot_tab:
            if self.autopot_tab.thread.isRunning():
                self.autopot_tab.stop()
            self.tabs.removeTab(self.tabs.indexOf(self.autopot_tab))
            self.autopot_tab = None
# (Existing toggle_autopot_tab, no changes)

    def toggle_pause_on_input(self):
        self.bot.pause_on_input = self.settings_tab.pause_on_input_cb.isChecked()
        self.bot.setup_user_input_hook()

    def update_status(self, status, cooldowns, casting_info, queue_info, urgent_skill):
        self.main_tab.status_label.setText(status)
        color = (
            "#00ff00"
            if "РАБОТАЕТ" in status
            else "#888" if status == "ОЖИДАНИЕ..." else "#ffaa00"
        )
        self.main_tab.status_label.setStyleSheet(
            f"font-size:52px;font-weight:bold;color:{color};"
        )

        self.main_tab.casting_label.setText(casting_info)
        self.main_tab.urgent_label.setText(urgent_skill)
        self.main_tab.queue_label.setText(queue_info)
        # Обновляем количество скиллов
        skills_count = len(self.bot.skills)
        self.main_tab.skills_count_label.setText(f"Скилов: {skills_count}")

        for i in reversed(range(self.main_tab.cooldowns_layout.count())):
            layout_item = self.main_tab.cooldowns_layout.itemAt(i)
            if layout_item:
                w = layout_item.widget()
                if w:
                    w.deleteLater()

        for key, cd in sorted(cooldowns.items(), key=lambda x: x[1], reverse=True):
            text = f"{key}: ГОТОВО" if cd <= 0.05 else f"{key}: {cd:.1f}с"
            color = "#00ff80" if cd <= 0.05 else "#ff6666"
            lbl = QLabel(text)
            lbl.setStyleSheet(f"font-size:24px;color:{color};")
            self.main_tab.cooldowns_layout.addWidget(lbl)

        ap_running = (
            self.autopot_tab and self.autopot_tab.thread.isRunning()
            if self.autopot_tab
            else False
        )
        ap_text = "РАБОТАЕТ" if ap_running else "ВЫКЛЮЧЕН"
        ap_color = "#00ff00" if ap_running else "#ff4444"
        self.main_tab.autopot_status_label.setText(f"АВТОПОТ: {ap_text}")
        self.main_tab.autopot_status_label.setStyleSheet(
            f"font-size:28px;color:{ap_color};font-weight:bold;"
        )

    def update_log(self, text):
        # Always schedule GUI update on the Qt main loop to avoid cross-thread calls
        if not self.debug_page:
            return
        
        def _update_debug_page():
            if self.debug_page:
                self.debug_page.append(text)
                self.debug_page.ensureCursorVisible()
        
        try:
            QTimer.singleShot(0, _update_debug_page)
        except Exception:
            try:
                # Fallback synchronous append
                _update_debug_page()
            except Exception:
                pass

    def eventFilter(self, obj, event):
        # Clear focus from QLineEdit when clicking outside it
        try:
            if event.type() == QEvent.Type.MouseButtonPress:
                focused = QApplication.focusWidget()
                if focused and isinstance(focused, QLineEdit):
                    # find widget under cursor
                    try:
                        # PyQt6: globalPos() replaced with globalPosition()
                        pos = event.globalPosition()
                        w = QApplication.widgetAt(int(pos.x()), int(pos.y()))
                    except Exception:
                        w = None

                    def is_descendant(child, ancestor):
                        while child:
                            if child == ancestor:
                                return True
                            try:
                                child = child.parentWidget()
                            except Exception:
                                return False
                        return False

                    if not w or not is_descendant(w, focused):
                        try:
                            focused.clearFocus()
                        except Exception:
                            try:
                                focused.clearFocus()
                            except Exception:
                                pass
        except Exception:
            pass
        return super().eventFilter(obj, event)

    def toggle_bot(self):
        self.bot.enabled = self.settings_tab.enable_cb.isChecked()

    def toggle_bot_hotkey(self):
        self.settings_tab.enable_cb.setChecked(
            not self.settings_tab.enable_cb.isChecked()
        )
        self.toggle_bot()

    def setup_main_hotkey(self):
        # Полностью пересоздаём хоткей — теперь работает всегда!
        try:
            keyboard.remove_hotkey(self.hotkey)
        except KeyError:
            # Исключение KeyError выбрасывается, когда хоткей не был зарегистрирован ранее
            # Это нормальное поведение при первом запуске, не нужно логировать
            pass
        except Exception as e:
            # Логируем только другие типы исключений
            self.bot.log_signal.emit(f"Ошибка при удалении хоткея: {e}")
        keyboard.add_hotkey(self.hotkey, self.toggle_bot_hotkey, suppress=False)

    def setup_panic_hotkey(self):
        """Register the emergency panic hotkey which immediately stops bots and exits."""
        # Remove previous registration if present
        try:
            keyboard.remove_hotkey(self.panic_key)
        except KeyError:
            # Исключение KeyError выбрасывается, когда хоткей не был зарегистрирован ранее
            # Это нормальное поведение при первом запуске, не нужно логировать
            pass
        except Exception as e:
            # Логируем только другие типы исключений
            self.bot.log_signal.emit(f"Ошибка при удалении panic хоткея: {e}")
        try:
            # Используем lambda для вызова через сигнал, чтобы избежать проблем с потоками
            keyboard.add_hotkey(self.panic_key, lambda: self.emergency_stop(), suppress=False)
        except Exception as e:
            self.bot.log_signal.emit(f"Не удалось зарегистрировать panic hotkey {self.panic_key}: {e}")

    def change_panic_key(self, key):
        try:
            keyboard.remove_hotkey(self.panic_key)
        except KeyError:
            # Исключение KeyError выбрасывается, когда хоткей не был зарегистрирован ранее
            # Это нормальное поведение, не нужно логировать
            pass
        except Exception as e:
            # Логируем только другие типы исключений
            self.bot.log_signal.emit(f"Ошибка при удалении panic хоткея: {e}")
        self.panic_key = key.lower()
        try:
            self.settings_tab.panic_btn.setText(key.upper())
        except Exception:
            pass
        self.setup_panic_hotkey()
        self.save_settings()

    def emergency_stop(self):
        """Immediate emergency stop: force exit application immediately."""
        # Простое и надежное завершение
        # Используем QTimer для выполнения в основном потоке
        try:
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(0, self._simple_emergency_stop)
        except Exception:
            # В крайнем случае вызываем напрямую
            self._simple_emergency_stop()
    
    def _simple_emergency_stop(self):
        """Simple emergency stop implementation."""
        try:
            # Завершаем все потоки
            self.bot.running = False
            if hasattr(self.bot, 'quit'):
                self.bot.quit()
                
            if self.autopot_tab and hasattr(self.autopot_tab, 'thread'):
                th = self.autopot_tab.thread
                if hasattr(th, 'quit'):
                    th.quit()
            
            # Останавливаем все горячие клавиши
            try:
                keyboard.unhook_all()
            except Exception:
                pass
                
            # Закрываем окна
            try:
                if self.overlay_window:
                    self.overlay_window.close()
                    self.overlay_window = None
                if self.autopot_tab:
                    self.autopot_tab.stop()
            except Exception:
                pass
                
            # Принудительное завершение
            import os
            os._exit(0)
        except Exception:
            # Последний вариант - через sys.exit
            try:
                import sys
                sys.exit(0)
            except Exception:
                # Если ничего не помогает, используем QApplication.quit()
                try:
                    QCoreApplication.quit()
                except Exception:
                    pass

    def change_hotkey(self, key):
        try:
            keyboard.remove_hotkey(self.hotkey)
        except KeyError:
            # Исключение KeyError выбрасывается, когда хоткей не был зарегистрирован ранее
            # Это нормальное поведение, не нужно логировать
            pass
        except Exception as e:
            # Логируем только другие типы исключений
            self.bot.log_signal.emit(f"Ошибка при удалении хоткея: {e}")
        self.hotkey = key.lower()
        self.settings_tab.hotkey_btn.setText(key.upper())
        self.setup_main_hotkey()

    # ────────────────────── Сохранение/загрузка настроек ──────────────────────
    def save_settings(self):
        data = {
            "last_profile": self.current_profile,
            "window_width": self.width(),
            "window_height": self.height(),
        }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.bot.log_signal.emit(f"Ошибка сохранения настроек: {e}")

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    # Load defaults for hotkey and panic_key (will be overridden by profile)
                    self.hotkey = "f8"
                    self.panic_key = "f12"
                    self.pause_on_input_duration = 1.0
            except Exception as e:
                self.bot.log_signal.emit(f"Ошибка загрузки настроек: {e}")
                self.hotkey = "f8"
                self.panic_key = "f12"
                self.pause_on_input_duration = 1.0
        else:
            self.hotkey = "f8"
            self.panic_key = "f12"
            self.pause_on_input_duration = 1.0

    def load_last_profile(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("last_profile", "default")
            except Exception as e:
                self.bot.log_signal.emit(f"Ошибка: {e}")
        return "default"

    def load_window_size(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    self.resize(
                        d.get("window_width", 1150), d.get("window_height", 980)
                    )
            except Exception as e:
                self.bot.log_signal.emit(f"Ошибка: {e}")

    # ────────────────────── Профили ──────────────────────
    def load_profiles(self):
        self.settings_tab.profile_combo.blockSignals(True)
        self.settings_tab.profile_combo.clear()
        for f in sorted(os.listdir(PROFILES_DIR)):
            if f.endswith(".json"):
                self.settings_tab.profile_combo.addItem(f[:-5])
        if self.settings_tab.profile_combo.count() == 0:
            self.settings_tab.profile_combo.addItem("default")
            path = os.path.join(PROFILES_DIR, "default.json")
            default_data = {
                "target_window": "",
                "debug": False,
                "skills": [],
                "autopot": {"show_tab": False},
                "pause_on_input": False,
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
        self.settings_tab.profile_combo.blockSignals(False)

    def new_profile(self):
        name, ok = QInputDialog.getText(self, "Новый профиль", "Название:")
        if ok and name.strip():
            path = os.path.join(PROFILES_DIR, f"{name.strip()}.json")
            if os.path.exists(path):
                QMessageBox.warning(self, "Ошибка", "Профиль уже существует")
                return
            with open(path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "target_window": "",
                        "debug": False,
                        "skills": [],
                        "autopot": {"show_tab": False},
                        "pause_on_input": False,
                    },
                    f,
                    indent=2,
                )
            self.load_profiles()
            self.settings_tab.profile_combo.setCurrentText(name.strip())
            self.safe_load_profile(name.strip())

    def delete_profile(self):
        name = self.settings_tab.profile_combo.currentText()
        if name == "default":
            QMessageBox.information(self, "", "default нельзя удалить")
            return
        if (
            QMessageBox.question(
                self, "", f"Удалить '{name}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            == QMessageBox.StandardButton.Yes
        ):
            os.remove(os.path.join(PROFILES_DIR, f"{name}.json"))
            self.load_profiles()
            self.safe_load_profile("default")

    def save_profile(self):
        self.settings_tab.apply_skills_now()
        autopot_data = {"show_tab": self.settings_tab.autopot_tab_cb.isChecked()}
        if self.autopot_tab:
            autopot_data.update(self.autopot_tab.save_to_dict())
        else:
            autopot_data = {"show_tab": self.settings_tab.autopot_tab_cb.isChecked(), "hotkey": "f9"}

        data = {
            "target_window": self.bot.target_window,
            "debug": self.settings_tab.debug_cb.isChecked(),
            "pause_on_input": self.settings_tab.pause_on_input_cb.isChecked(),
            "pause_on_input_duration": self.pause_on_input_duration,
            "skills": [
                {k: v for k, v in s.items() if k not in ["last_used", "in_cast"]}
                for s in self.bot.skills
            ],
            "autopot": autopot_data,
            "overlay": {
                "show_tab": self.settings_tab.overlay_tab_cb.isChecked(),
                **(self.overlay_tab.save_to_dict() if self.overlay_tab else {}),
            },
            # Save all settings in profile
            "hotkey": self.hotkey,
            "panic_key": self.panic_key,
        }
        path = os.path.join(PROFILES_DIR, f"{self.current_profile}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        QMessageBox.information(self, "Готово", "Профиль сохранён!")
        # Обновляем отображение количества скиллов в интерфейсе после сохранения
        if hasattr(self.main_tab, 'skills_count_label'):
            skills_count = len(self.bot.skills)
            self.main_tab.skills_count_label.setText(f"Скилов: {skills_count}")
        # Обновляем количество скиллов в логе бота
        # Не нужно вызывать update_skills, так как скиллы уже обновлены, просто обновим лог
        if self.bot.debug:
            from core.bot import time
            self.bot.log_signal.emit(f"[{time.strftime('%H:%M:%S')}] Количество скиллов: {len(self.bot.skills)} (после сохранения профиля)")

    def safe_load_profile(self, name):
        if not name or name == self.current_profile:
            return
        self.current_profile = name
        path = os.path.join(PROFILES_DIR, f"{name}.json")
        self.settings_tab.clear_skills_ui_fast()
        self.bot.skills.clear()
        self.bot.target_window = ""

        if not os.path.exists(path):
            self.settings_tab.window_input.setText("")
            self.settings_tab.autopot_tab_cb.setChecked(False)
            self.settings_tab.debug_cb.setChecked(False)
            self.settings_tab.pause_on_input_cb.setChecked(False)
            # Load defaults for settings not in profile
            self.hotkey = "f8"
            self.panic_key = "f12"
            self.pause_on_input_duration = 1.0
            try:
                self.settings_tab.hotkey_btn.setText(self.hotkey.upper())
                self.settings_tab.panic_btn.setText(self.panic_key.upper())
                self.settings_tab.pause_duration_edit.setText(str(self.pause_on_input_duration))
            except Exception:
                pass
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.bot.target_window = data.get("target_window", "")
            self.settings_tab.window_input.setText(self.bot.target_window)

            self.settings_tab.debug_cb.setChecked(data.get("debug", False))
            self.toggle_debug_tab()

            self.settings_tab.pause_on_input_cb.setChecked(
                data.get("pause_on_input", False)
            )
            self.toggle_pause_on_input()
            
            # Load pause duration from profile
            self.pause_on_input_duration = float(data.get("pause_on_input_duration", 1.0))
            try:
                self.bot.pause_duration = float(self.pause_on_input_duration)
            except Exception:
                pass
            try:
                self.settings_tab.pause_duration_edit.setText(str(self.pause_on_input_duration))
            except Exception:
                pass

            for s in data.get("skills", []):
                self.settings_tab.add_skill_row(
                    key=s.get("key", ""),
                    cd=s.get("cooldown", 1.0),
                    cast=s.get("cast_time", 0.3),
                    priority=s.get("priority", 5),
                )

            cfg = data.get("autopot", {})
            show = cfg.get("show_tab", False)
            self.settings_tab.autopot_tab_cb.setChecked(show)
            self.toggle_autopot_tab()
            if self.autopot_tab and show:
                clean_cfg = {k: v for k, v in cfg.items() if k != "show_tab"}
                self.autopot_tab.load_from_dict(clean_cfg)

            cfg = data.get("overlay", {})
            show = cfg.get("show_tab", False)
            self.settings_tab.overlay_tab_cb.setChecked(show)
            self.toggle_overlay_tab()
            if self.overlay_tab and show:
                clean_cfg = {k: v for k, v in cfg.items() if k != "show_tab"}
                self.overlay_tab.load_from_dict(clean_cfg)

                # Принудительно применим настройки к окну
                if self.overlay_window:
                    self.overlay_window.load_settings(clean_cfg)

            # Load hotkey and panic_key from profile
            self.hotkey = data.get("hotkey", "f8")
            self.panic_key = data.get("panic_key", "f12")
            try:
                self.settings_tab.hotkey_btn.setText(self.hotkey.upper())
                self.settings_tab.panic_btn.setText(self.panic_key.upper())
            except Exception:
                pass
            # Register hotkeys after loading from profile
            self.setup_main_hotkey()
            self.setup_panic_hotkey()

            self.settings_tab.apply_skills_now()
            # Обновляем отображение количества скиллов в интерфейсе
            if hasattr(self.main_tab, 'skills_count_label'):
                skills_count = len(self.bot.skills)
                self.main_tab.skills_count_label.setText(f"Скилов: {skills_count}")
            # Отправляем сообщение о количестве скиллов в лог с небольшой задержкой, чтобы обеспечить правильный порядок
            from PyQt6.QtCore import QTimer
            def send_skills_count_update():
                if self.bot.debug:
                    import time
                    self.bot.log_signal.emit(f"[{time.strftime('%H:%M:%S')}] Количество скилов: {len(self.bot.skills)} (обновлено из профиля)")
            QTimer.singleShot(100, send_skills_count_update) # Задержка 100мс для правильного порядка
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить профиль:\n{e}")

    def closeEvent(self, e):
        try:
            keyboard.unhook_all()
        except Exception as ex:
            self.bot.log_signal.emit(f"Ошибка при отключении хуков: {ex}")
        # ДОБАВЛЕНО: чистим хуки keyboard от автопота
        if self.autopot_tab and hasattr(self.autopot_tab, '_registered_hotkey'):
            try:
                import keyboard as kb_lib
                if self.autopot_tab._registered_hotkey:
                    kb_lib.remove_hotkey(self.autopot_tab._registered_hotkey)
            except KeyError:
                # Исключение KeyError выбрасывается, когда хоткей не был зарегистрирован
                # Это нормальное поведение, не нужно логировать
                pass
            except Exception as ex:
                # Логируем только другие типы исключений
                self.bot.log_signal.emit(f"Ошибка при удалении автопот хоткея: {ex}")
        if self.autopot_tab:
            self.autopot_tab.stop()
        if self.overlay_window:
            self.overlay_window.close()
            self.overlay_window.deleteLater()
            self.bot.log_signal.emit("Overlay window закрыт и удалён.")
            self.overlay_window = None
        if hasattr(self, 'overlay_tab'):
            self.overlay_tab = None
        self.bot.running = False
        try:
            self.bot.quit()
            self.bot.wait(1000)  # Ждем до 1 секунды для корректного завершения
        except Exception:
            pass
        self.save_settings()
        e.accept()
