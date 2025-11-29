# settings_tab.py — ПОЛНЫЙ РАБОЧИЙ ФАЙЛ (все методы на месте)
import os  # (Existing)
import win32gui
import win32process

import psutil
from PyQt6.QtCore import Qt, pyqtSignal, QLocale
from PyQt6.QtGui import QAction, QBrush, QConicalGradient, QCursor, QFont, QIcon, QKeySequence, QLinearGradient, QMovie, QPainter, QPalette, QPen, QPicture, QPixmap, QPolygon, QRegion, QRegularExpressionValidator, QRadialGradient, QTransform, QValidator, QIntValidator, QDoubleValidator
from PyQt6.QtWidgets import QApplication, QCheckBox, QComboBox, QDialog, QFormLayout, QHBoxLayout, QInputDialog, QLabel, QLineEdit, QPushButton, QScrollArea, QSizePolicy, QSpinBox, QTabWidget, QVBoxLayout, QWidget

from utils import KeyCaptureButton, SelectAllLineEdit
# legacy imports removed (migrated to PyQt6 above)


class SettingsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # === Профили ===
        top = QHBoxLayout()
        top.addWidget(QLabel("Профиль:"))
        self.profile_combo = QComboBox()
        self.profile_combo.setMinimumWidth(300)
        top.addWidget(self.profile_combo)
        new_btn = QPushButton("Новый")
        new_btn.clicked.connect(self.main.new_profile)
        top.addWidget(new_btn)
        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(self.main.delete_profile)
        top.addWidget(delete_btn)
        save_btn = QPushButton("Сохранить")
        save_btn.setObjectName("success")
        save_btn.clicked.connect(self.main.save_profile)
        top.addWidget(save_btn)
        top.addStretch()
        layout.addLayout(top)
        self.profile_combo.currentTextChanged.connect(self.main.safe_load_profile)

        form = QFormLayout()
        form.setSpacing(8)

        # Включить бота + горячая клавиша
        row1 = QHBoxLayout()
        self.enable_cb = QCheckBox("Включить бота")
        self.enable_cb.stateChanged.connect(self.main.toggle_bot)
        row1.addWidget(self.enable_cb)
        self.hotkey_btn = KeyCaptureButton(self.main.hotkey.upper())
        self.hotkey_btn.key_captured.connect(self.main.change_hotkey)
        row1.addWidget(QLabel("   Горячая:"))
        row1.addWidget(self.hotkey_btn)
        # Panic key (emergency stop)
        self.panic_btn = KeyCaptureButton(getattr(self.main, 'panic_key', 'f12').upper())
        self.panic_btn.key_captured.connect(self.main.change_panic_key)
        row1.addWidget(QLabel("   Клавиша паники:"))
        row1.addWidget(self.panic_btn)
        row1.addStretch()
        form.addRow(row1)

        # Автопот
        # ← ОДНА ЕДИНСТВЕННАЯ ГАЛОЧКА АВТОПОТА (дубликат удалён)
        # (если чекбокс уже есть — удаляем старую строку выше и оставляем только эту)
        if not hasattr(self, "autopot_tab_cb"):
            self.autopot_tab_cb = QCheckBox("Показать вкладку настроек автопота")
            self.autopot_tab_cb.stateChanged.connect(self.main.toggle_autopot_tab)
            form.addRow(self.autopot_tab_cb)

        self.overlay_tab_cb = QCheckBox("Показать вкладку оверлея")
        self.overlay_tab_cb.stateChanged.connect(self.main.toggle_overlay_tab)
        form.addRow(self.overlay_tab_cb)

        # ПАУЗА ПРИ ДВИЖЕНИИ — НОВАЯ ФУНКЦИЯ
        self.pause_on_input_cb = QCheckBox("Пауза бота при движении (полный стоп)")
        self.pause_on_input_cb.setToolTip(
            "Бот не будет нажимать НИ ОДНУ клавишу, пока вы двигаетесь"
        )
        self.pause_on_input_cb.stateChanged.connect(self.main.toggle_pause_on_input)
        # Duration control (seconds) — manual entry only (no spinbox)
        pause_h = QHBoxLayout()
        pause_h.addWidget(self.pause_on_input_cb)
        self.pause_duration_edit = SelectAllLineEdit()
        # Validator: allow dot/comma, up to 3 decimals
        pd_validator = QDoubleValidator(0.0, 10.0, 3)
        try:
            pd_validator.setLocale(QLocale(QLocale.Language.English))
        except Exception:
            pass
        self.pause_duration_edit.setValidator(pd_validator)
        # Initialize from main window settings (load_settings called before init_ui)
        try:
            val = getattr(self.main, 'pause_on_input_duration', getattr(self.main.bot, 'pause_duration', 1.0))
            self.pause_duration_edit.setText(str(val))
        except Exception:
            self.pause_duration_edit.setText('1.0')
        self.pause_duration_edit.setToolTip('Длительность паузы после ввода пользователя (в секундах). Ввод вручную.')
        self.pause_duration_edit.editingFinished.connect(self._on_pause_duration_changed)
        pause_h.addWidget(QLabel('Длительность (с):'))
        pause_h.addWidget(self.pause_duration_edit)
        pause_h.addStretch()
        form.addRow(pause_h)

        # Окно
        win_h = QHBoxLayout()
        self.window_input = QLineEdit()
        self.window_input.setPlaceholderText("Например: Dota 2 или Client")
        self.window_input.textChanged.connect(
            self.apply_window_now
        )  # ← теперь метод есть!
        win_h.addWidget(self.window_input)
        select_from_list_btn = QPushButton("Из списка")
        select_from_list_btn.clicked.connect(self.select_window)
        win_h.addWidget(select_from_list_btn)
        select_by_click_btn = QPushButton("Кликом")
        select_by_click_btn.clicked.connect(self.select_window_by_click)
        win_h.addWidget(select_by_click_btn)
        form.addRow("Работать только в окне:", win_h)

        # Отладка
        self.debug_cb = QCheckBox("Отладка")
        self.debug_cb.stateChanged.connect(self.main.toggle_debug_tab)
        form.addRow(self.debug_cb)

        layout.addLayout(form)

        layout.addWidget(QLabel("<b>Скиллы (приоритет >10 = срочный):</b>"))

        # Список скиллов
        skills_scroll = QScrollArea()
        skills_scroll.setWidgetResizable(True)
        self.skills_widget = QWidget()
        self.skills_layout = QVBoxLayout(self.skills_widget)
        self.skills_layout.addStretch()
        skills_scroll.setWidget(self.skills_widget)
        layout.addWidget(skills_scroll, 1)

        add_btn = QPushButton("＋ Добавить скилл")
        add_btn.clicked.connect(self.add_skill_row)
        add_btn.setObjectName("primary")
        layout.addWidget(add_btn)

    def apply_window_now(self):
        text = self.window_input.text().strip()
        self.main.bot.target_window = text
        self.main.bot.setup_user_input_hook()  # обновляем хук при смене окна

    def _on_pause_duration_changed(self):
        try:
            txt = self.pause_duration_edit.text().strip()
            val = float(txt) if txt else 1.0
            # clamp to allowed range
            if val < 0.0:
                val = 0.0
            if val > 10.0:
                val = 10.0
            self.main.pause_on_input_duration = float(val)
            # update bot instance immediately
            try:
                self.main.bot.pause_duration = float(val)
            except Exception:
                pass
            # Note: settings are saved to profile on click "Сохранить профиль", not here
        except Exception:
            pass

    def select_window(self):
        windows = []
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if proc.info["name"]:
                    windows.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
            except Exception as e:
                self.main.bot.log_signal.emit(f"Ошибка: {e}")
        item, ok = QInputDialog.getItem(
            self, "Выбрать окно", "Активные процессы:", windows, 0, False
        )
        if ok and item:
            name = item.split(" (PID:")[0]
            self.window_input.setText(name)
            self.apply_window_now()

    def select_window_by_click(self):
        """Show fullscreen overlay and wait for user to click on a window to select it."""
        try:
            from ui.widgets.click_overlay import WindowSelectOverlay
            
            overlay = WindowSelectOverlay(self.main, message="Кликни на окно для выбора (Esc — отмена)")
            
            def handle_window_select(window_name):
                try:
                    self.window_input.setText(window_name)
                    self.apply_window_now()
                    self.main.bot.log_signal.emit(f"[Настройки] Окно выбрано: {window_name}")
                except Exception as e:
                    self.main.bot.log_signal.emit(f"Ошибка при установке окна: {e}")
            
            overlay.window_selected.connect(handle_window_select)
            overlay.showFullScreenWithMessage()
        except Exception as e:
            self.main.bot.log_signal.emit(f"Ошибка в select_window_by_click: {e}")

    def add_skill_row(self, key="", cd=1.0, cast=0.3, priority=5):
        row = QHBoxLayout()
        row.setContentsMargins(3, 3, 3, 3)

        key_btn = KeyCaptureButton(key.upper() if key else "Нажми")
        # Обычные поля вместо спинбоксов — всё выделяется при клике
        cd_edit = SelectAllLineEdit()
        # Allow up to 3 decimals and minimum 5 ms
        cd_validator = QDoubleValidator(0.005, 60.0, 3)
        try:
            cd_validator.setLocale(QLocale(QLocale.Language.English))
        except Exception:
            pass
        cd_edit.setValidator(cd_validator)
        cd_edit.setText(str(cd))
        cast_edit = SelectAllLineEdit()
        cast_validator = QDoubleValidator(0.0, 5.0, 3)
        try:
            cast_validator.setLocale(QLocale(QLocale.Language.English))
        except Exception:
            pass
        cast_edit.setValidator(cast_validator)
        cast_edit.setText(str(cast))
        prio_edit = SelectAllLineEdit()
        prio_edit.setValidator(QIntValidator(1, 100))
        prio_edit.setText(str(priority))

        row.addWidget(QLabel("Клавиша:"))
        row.addWidget(key_btn)
        row.addWidget(QLabel("Кулдаун:"))
        row.addWidget(cd_edit)
        row.addWidget(QLabel("Каст:"))
        row.addWidget(cast_edit)
        row.addWidget(QLabel("Приоритет:"))
        row.addWidget(prio_edit)

        # Создаем виджет строки перед тем, как добавить кнопку удаления
        row_widget = QWidget()
        row_widget.setLayout(row)
        row_widget.setStyleSheet("background:#2d2d2d;border-radius:8px;margin:2px;")

        # Кнопка удаления — БЕЗ ОШИБОК!
        delete_btn = QPushButton("Удалить ×")
        delete_btn.clicked.connect(lambda: self.remove_skill_row(row_widget))
        row.addWidget(delete_btn)

        row.addStretch()

        # === КЛЮЧЕВАЯ ЧАСТЬ: сохраняем всё в row_widget, чтобы потом читать ===
        setattr(row_widget, '_key_btn', key_btn)
        setattr(row_widget, '_cd_edit', cd_edit)
        setattr(row_widget, '_cast_edit', cast_edit)
        setattr(row_widget, '_prio_edit', prio_edit)

        self.skills_layout.insertWidget(self.skills_layout.count() - 1, row_widget)

        # ← БОЛЬШЕ НИЧЕГО НЕ НАДО! Кнопка сама себя блокирует в utils.py
        # key_btn сама станет зелёной и отключится навсегда после назначения

    def remove_skill_row(self, widget):
        self.skills_layout.removeWidget(widget)
        widget.deleteLater()

    def clear_skills_ui_fast(self):
        for i in reversed(range(self.skills_layout.count() - 1)):
            item = self.skills_layout.itemAt(i)
            if item:
                w = item.widget()
                if w:
                    w.deleteLater()

    def apply_skills_now(self):
        skills = []
        for i in range(self.skills_layout.count() - 1):
            item = self.skills_layout.itemAt(i)
            if item is None:
                continue
            row = item.widget()
            if not row:
                continue

            # Теперь всё надёжно берём из сохранённых ссылок
            # Теперь всё надёжно берём из сохранённых ссылок
            key_btn = getattr(row, '_key_btn', None)
            cd_edit = getattr(row, '_cd_edit', None)
            cast_edit = getattr(row, '_cast_edit', None)
            prio_edit = getattr(row, '_prio_edit', None)
            
            # Проверяем, что все элементы существуют
            if not all([key_btn, cd_edit, cast_edit, prio_edit]):
                continue

            try:
                if key_btn is None:
                    continue
                key_text = key_btn.text().strip().lower()
            except:
                continue
            if not key_text or key_text in ["нажми", "жд..."]:
                continue

            try:
                if cd_edit is None:
                    cd = 1.0
                else:
                    cd_text_val = cd_edit.text()
                    cd_text = cd_text_val.strip().strip('сС').replace(',', '.')
                    cd = float(cd_text)
            except Exception as e:
                try:
                    self.main.bot.log_signal.emit(f"Ошибка парсинга CD '{cd_text_val}': {e}")
                except:
                    self.main.bot.log_signal.emit(f"Ошибка парсинга CD: {e}")
                cd = 1.0

            try:
                if cast_edit is None:
                    cast = 0.3
                else:
                    cast_text_val = cast_edit.text()
                    cast_text = cast_text_val.strip().strip('сС').replace(',', '.')
                    cast = float(cast_text)
            except Exception as e:
                try:
                    self.main.bot.log_signal.emit(f"Ошибка парсинга Cast '{cast_text_val}': {e}")
                except:
                    self.main.bot.log_signal.emit(f"Ошибка парсинга Cast: {e}")
                cast = 0.3

            try:
                if prio_edit is None:
                    prio = 5
                else:
                    prio_text_val = prio_edit.text()
                    prio_text = prio_text_val.strip()
                    prio = int(prio_text)
            except Exception as e:
                try:
                    self.main.bot.log_signal.emit(f"Ошибка парсинга Priority '{prio_text_val}': {e}")
                except:
                    self.main.bot.log_signal.emit(f"Ошибка парсинга Priority: {e}")
                prio = 5

            skills.append(
                {
                    "key": key_text,
                    "cooldown": cd,
                    "cast_time": cast,
                    "priority": prio,
                    "last_used": 0.0,
                }
            )

        self.main.bot.skills = skills
