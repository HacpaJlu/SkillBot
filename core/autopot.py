# autopot.py — Skill Bot v23.5 (исправлено: лишняя скобка + стабильность)
import threading
import time

import cv2
import keyboard as kb_lib
import numpy as np
import win32gui
from mss import mss
from pynput.keyboard import Controller
from pynput import mouse as pynput_mouse
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QLocale
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout,
    QPushButton, QLineEdit, QHBoxLayout, QCheckBox
)
from PyQt6.QtGui import QDoubleValidator, QIntValidator

from utils import KeyCaptureButton
from ui.widgets.roi_overlay import ROIOverlay


class AutopotThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, parent_tab):
        super().__init__()
        self.parent_tab = parent_tab  # Переименовано для избежания конфликта с QThread.parent
        self.running = False
        self.coords = None
        self.base_color = None
        self.press_key = "f"
        self.cd = 0.25
        self.thresh = 15
        self.target_window = ""
        self.state_lock = threading.Lock()
        self.use_roi = False
        self.roi_width = 100
        self.roi_height = 20
        self.hp_threshold_percent = 30

    def set_params(self, coords, color, key, cd, thresh, window, use_roi=False, roi_width=100, roi_height=20, hp_threshold_percent=30.0):
        self.coords = coords
        self.base_color = color
        self.press_key = key.lower()
        self.cd = cd
        self.thresh = thresh
        self.target_window = window
        self.use_roi = use_roi
        self.roi_width = roi_width
        self.roi_height = roi_height
        self.hp_threshold_percent = hp_threshold_percent

    def run(self):
        self.running = True
        self.parent_tab.update_main_status()
        self.log_signal.emit("[Автопот] ЗАПУЩЕН")

        kb = Controller()
        last_press = 0

        with mss() as sct:
            while True:
                with self.state_lock:
                    if not self.running:
                        break
                # проверка окна
                if self.target_window:
                    try:
                        fg = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                        if self.target_window.lower() not in fg.lower():
                            time.sleep(0.1)
                            continue
                    except Exception as e:
                        self.log_signal.emit(f"Ошибка проверки окна: {e}")

                if not self.coords or not self.base_color:
                    time.sleep(0.05)
                    continue

                x, y = self.coords
                try:
                    if self.use_roi:
                        # Захватываем область ROI для анализа HP-бара
                        left = x - self.roi_width // 2
                        top = y - self.roi_height // 2
                        width = self.roi_width
                        height = self.roi_height
                        
                        img = sct.grab({"left": left, "top": top, "width": width, "height": height})
                        frame = np.array(img)
                        
                        # Преобразуем изображение в формат BGR (OpenCV)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                        
                        # Сравниваем с базовым цветом для определения HP
                        lower_bound = np.array([max(0, c - self.thresh) for c in self.base_color[::-1]], dtype=np.uint8)
                        upper_bound = np.array([min(255, c + self.thresh) for c in self.base_color[::-1]], dtype=np.uint8)
                        
                        # Создаем маску для области с цветом HP-бара
                        mask = cv2.inRange(frame, lower_bound, upper_bound)
                        
                        # Вычисляем процент заполнения HP-бара
                        total_pixels = mask.size
                        filled_pixels = cv2.countNonZero(mask)
                        hp_percentage = (filled_pixels / total_pixels) * 100
                        
                        # Если HP ниже порога, используем зелье
                        if hp_percentage < self.hp_threshold_percent:
                            now = time.time()
                            if now - last_press >= self.cd:
                                kb.press(self.press_key)
                                kb.release(self.press_key)
                                last_press = now
                                self.log_signal.emit(
                                    f"[Автопот] Нажал {self.press_key.upper()} | HP: {hp_percentage:.1f}%"
                                )
                    else:
                        # Стандартное поведение - анализ отдельного пикселя
                        img = sct.grab(
                            {"left": x - 3, "top": y - 3, "width": 7, "height": 7}
                        )
                        # ← ИСПРАВЛЕНО: убрана лишняя закрывающая скобка
                        current = tuple(
                            map(
                                int,
                                np.mean(
                                    np.frombuffer(img.rgb, np.uint8).reshape(7, 7, 3),
                                    axis=(0, 1),
                                ),
                            )
                        )
                        diff = sum(abs(a - b) for a, b in zip(current, self.base_color))

                        if diff > self.thresh:
                            now = time.time()
                            if now - last_press >= self.cd:
                                kb.press(self.press_key)
                                kb.release(self.press_key)
                                last_press = now
                                self.log_signal.emit(
                                    f"[Автопот] Нажал {self.press_key.upper()} | Δ={diff:.0f}"
                                )
                except Exception as e:
                    self.log_signal.emit(f"[Автопот] Ошибка скриншота: {e}")

                time.sleep(0.02)

        self.parent_tab.update_main_status()
        self.log_signal.emit("[Автопот] Остановлен")


class AutopotTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.thread: AutopotThread = AutopotThread(self)  # Явно указываем тип
        self.thread.log_signal.connect(self.main.update_log)

        self.coords = None
        self.base_color = None
        self.hotkey = "f9"
        self.profile_hotkey = "f9"
        self._registered_hotkey = None
        self.roi_width = 100  # Добавляем атрибуты для ROI
        self.roi_height = 20

        self.build_ui()
        self.setup_hotkey()

    def build_ui(self):
        # Устанавливаем стиль для всей вкладки
        self.setObjectName("autopot_tab")
        
        layout = QVBoxLayout(self)
        
        # Добавляем заголовок с кнопкой удаления
        title_container = QHBoxLayout()
        title = QLabel("<b style='font-size:28px;color:#ff0066;'>АВТОПОТ</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Кнопка удаления (для примера стилизации, как в настройках скиллов)
        # Эта кнопка будет скрыта по умолчанию, но стилизуется как "красный крестик"
        delete_btn = QPushButton("×")
        delete_btn.setObjectName("autopot_delete")  # Используем новый стиль из ui/styles.py
        delete_btn.setFixedSize(30, 30)
        delete_btn.setToolTip("Удалить автопот")
        # Пока скрываем кнопку, так как функционал удаления автопота не реализован
        delete_btn.hide()
        
        title_container.addStretch()
        title_container.addWidget(title)
        title_container.addStretch()
        title_container.addWidget(delete_btn)
        
        layout.addLayout(title_container)

        grid = QGridLayout()

        grid.addWidget(QLabel("Горячая клавиша:"), 0, 0)
        self.hotkey_btn = KeyCaptureButton(self.hotkey.upper())
        self.hotkey_btn.key_captured.connect(self.change_hotkey)
        grid.addWidget(self.hotkey_btn, 0, 1)

        grid.addWidget(QLabel("Точка:"), 1, 0)
        self.coord_lbl = QLabel("Не выбрана")
        self.coord_lbl.setStyleSheet("color:red;font-weight:bold")
        grid.addWidget(self.coord_lbl, 1, 1)

        grid.addWidget(QLabel("Цвет:"), 2, 0)
        self.color_lbl = QLabel("Не выбран")
        self.color_lbl.setStyleSheet("color:red;font-weight:bold")
        grid.addWidget(self.color_lbl, 2, 1)

        grid.addWidget(QLabel("Клавиша нажатия:"), 3, 0)
        self.key_btn = KeyCaptureButton("F")
        grid.addWidget(self.key_btn, 3, 1)

        grid.addWidget(QLabel("Кулдаун:"), 4, 0)
        self.cd_edit = QLineEdit("0.25")
        # Allow up to 3 decimal places and minimum 0.005s (5 ms)
        cd_validator = QDoubleValidator(0.005, 10, 3)
        # Use English locale so dot (.) is accepted as decimal separator
        try:
            cd_validator.setLocale(QLocale(QLocale.Language.English))
        except Exception:
            pass
        self.cd_edit.setValidator(cd_validator)
        grid.addWidget(self.cd_edit, 4, 1)

        grid.addWidget(QLabel("Чувствительность:"), 5, 0)
        self.thresh_edit = QLineEdit("15")
        self.thresh_edit.setValidator(QIntValidator(1, 255))
        grid.addWidget(self.thresh_edit, 5, 1)

        # Добавляем чекбокс для включения ROI анализа
        self.use_roi_checkbox = QCheckBox("Использовать анализ области (ROI)")
        self.use_roi_checkbox.stateChanged.connect(self.toggle_roi_options)
        layout.addWidget(self.use_roi_checkbox)

        # Создаем контейнер для опций ROI
        self.roi_options_widget = QWidget()
        self.roi_options_widget.setVisible(False)
        roi_layout = QGridLayout(self.roi_options_widget)

        roi_layout.addWidget(QLabel("Ширина ROI:"), 0, 0)
        self.roi_width_edit = QLineEdit("100")
        self.roi_width_edit.setValidator(QIntValidator(1, 1000))
        roi_layout.addWidget(self.roi_width_edit, 0, 1)

        roi_layout.addWidget(QLabel("Высота ROI:"), 1, 0)
        self.roi_height_edit = QLineEdit("20")
        self.roi_height_edit.setValidator(QIntValidator(1, 1000))
        roi_layout.addWidget(self.roi_height_edit, 1, 1)

        roi_layout.addWidget(QLabel("Порог HP (%):"), 2, 0)
        self.hp_threshold_edit = QLineEdit("30.0")
        self.hp_threshold_edit.setValidator(QDoubleValidator(0.0, 100.0, 1))
        roi_layout.addWidget(self.hp_threshold_edit, 2, 1)

        layout.addWidget(self.roi_options_widget)

        self.status = QLabel("ВЫКЛЮЧЕН")
        self.status.setStyleSheet("font-size:22px;color:#ff4444;font-weight:bold")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)

        layout.addLayout(grid)

        # Кнопки выбора точки и ROI
        button_layout = QHBoxLayout()
        
        btn = QPushButton("Выбрать точку (ЛКМ при полном ХП)")
        btn.clicked.connect(self.pick_color)
        btn.setObjectName("primary") # Используем существующий стиль кнопки из стилей
        button_layout.addWidget(btn)
        
        btn_roi = QPushButton("Выбрать ROI")
        btn_roi.clicked.connect(self.pick_roi)
        btn_roi.setObjectName("primary") # Используем существующий стиль кнопки из стилей
        button_layout.addWidget(btn_roi)
        
        layout.addLayout(button_layout)

        layout.addStretch()

    def setup_hotkey(self):
        old_hotkey = getattr(self, '_registered_hotkey', None)
        if old_hotkey:
            try:
                kb_lib.remove_hotkey(old_hotkey)
            except:
                pass
        if self.hotkey:
            try:
                # ИСПРАВЛЕНИЕ: suppress=True ломает глобальные клавиши!
                # Убираем suppress — теперь горячие клавиши бота НЕ ломаются!
                kb_lib.add_hotkey(self.hotkey, self.toggle, suppress=False)
                self._registered_hotkey = self.hotkey
            except Exception as e:
                print(f"[Автопот] Не удалось зарегать горячую клавишу {self.hotkey}: {e}")
                self._registered_hotkey = None
        else:
            self._registered_hotkey = None

    def is_valid_hotkey(self, key):
        return key and key not in ["", "none"] and len(key) > 0  # simple check, keyboard.add_hotkey will fail anyway but for fallback

    def change_hotkey(self, key):
        self.profile_hotkey = key.lower()
        self.hotkey = key.lower()
        self.hotkey_btn.setText(key.upper())
        self.setup_hotkey()

    def toggle(self):
        if not self.coords or not self.base_color:
            # unobtrusive notification instead of blocking MessageBox
            try:
                # Use main's toast (thread-safe) to notify user
                self.main.show_toast("Автопот", "Сначала выбери точку и цвет! Нажми 'Выбрать точку' и кликни ЛКМ на полный индикатор.")
            except Exception:
                try:
                    QTimer.singleShot(0, lambda: self.main.update_log("[Автопот] ОШИБКА: Сначала выбери точку и цвет!"))
                except Exception:
                    try:
                        self.main.update_log("[Автопот] ОШИБКА: Сначала выбери точку и цвет!")
                    except Exception:
                        pass
            return

        if self.thread.isRunning():
            self.stop()
        else:
            self.start()

    def toggle_roi_options(self, state):
        self.roi_options_widget.setVisible(state == Qt.CheckState.Checked.value)

    def start(self):
        try:
            key = self.key_btn.text().strip() or "f"
            # Accept both comma and dot as decimal separator
            cd_text = self.cd_edit.text().strip().replace(",", ".")
            cd = float(cd_text)
            # Enforce minimum 5 ms
            if cd < 0.005:
                cd = 0.005
            thr = int(self.thresh_edit.text())
            
            # Получаем значения для ROI анализа
            use_roi = getattr(self, 'use_roi_checkbox', None) and self.use_roi_checkbox.isChecked() or False
            roi_width = getattr(self, 'roi_width_edit', None) and int(self.roi_width_edit.text()) or 100
            roi_height = getattr(self, 'roi_height_edit', None) and int(self.roi_height_edit.text()) or 20
            hp_threshold_percent = getattr(self, 'hp_threshold_edit', None) and float(self.hp_threshold_edit.text()) or 30.0

            self.thread.set_params(
                self.coords, self.base_color, key, cd, thr, self.main.bot.target_window,
                use_roi=use_roi, roi_width=roi_width, roi_height=roi_height,
                hp_threshold_percent=hp_threshold_percent
            )
            self.thread.start()

            self.status.setText("РАБОТАЕТ")
            self.status.setStyleSheet("font-size:22px;color:#00ff00;font-weight:bold")
            self.update_main_status()
        except Exception as e:
            try:
                QTimer.singleShot(0, lambda: self.main.update_log(f"[Автопот] Ошибка запуска: {e}"))
            except Exception:
                try:
                    self.main.update_log(f"[Автопот] Ошибка запуска: {e}")
                except Exception:
                    pass

    def stop(self):
        self.thread.running = False
        if self.thread.isRunning():
            self.thread.wait(100)
        self.status.setText("ВЫКЛЮЧЕН")
        self.status.setStyleSheet("font-size:22px;color:#ff4444;font-weight:bold")
        self.update_main_status()

    def update_main_status(self):
        if self.thread.isRunning():
            self.main.main_tab.autopot_status_label.setText("АВТОПОТ: РАБОТАЕТ")
            self.main.main_tab.autopot_status_label.setStyleSheet(
                "font-size: 28px; color: #00ff00; font-weight: bold;"
            )
        else:
            self.main.main_tab.autopot_status_label.setText("АВТОПОТ: ВЫКЛЮЧЕН")
            self.main.main_tab.autopot_status_label.setStyleSheet(
                "font-size: 28px; color: #ff4444; font-weight: bold;"
            )

    def pick_color(self):
        # Показываем полноэкранный полупрозрачный оверлей с подсказкой
        try:
            # import here to avoid circular imports at module load
            from ui.widgets.click_overlay import ClickOverlay

            overlay = ClickOverlay(self.main, message="Кликни ЛКМ на полный индикатор для выбора точки (Esc — отмена)")

            def handle_click(x, y):
                try:
                    with mss() as sct:
                        img = sct.grab({"left": x - 3, "top": y - 3, "width": 7, "height": 7})
                        color = tuple(
                            map(
                                int,
                                np.mean(
                                    np.frombuffer(img.rgb, np.uint8).reshape(7, 7, 3),
                                    axis=(0, 1),
                                ),
                            )
                        )
                    self.coords = (x, y)
                    self.base_color = color
                    self.coord_lbl.setText(f"{x}, {y}")
                    self.color_lbl.setText(str(color))
                    self.coord_lbl.setStyleSheet("color:#00ff00;font-weight:bold")
                    self.color_lbl.setStyleSheet("color:#00ff00;font-weight:bold")
                    # Schedule GUI updates on the main Qt thread
                    try:
                        QTimer.singleShot(0, lambda: self.main.update_log(f"[Автопот] Точка зафиксирована: {x},{y} | Цвет: {color}"))
                        QTimer.singleShot(0, lambda: self.main.showNormal())
                    except Exception:
                        try:
                            self.main.update_log(f"[Автопот] Точка зафиксирована: {x},{y} | Цвет: {color}")
                        except Exception:
                            pass
                except Exception as e:
                    try:
                        QTimer.singleShot(0, lambda: self.main.update_log(f"[Автопот] Ошибка при захвате цвета: {e}"))
                    except Exception:
                        pass

            overlay.clicked.connect(handle_click)
            overlay.showFullScreenWithMessage()
        except Exception as e:
            # Fallback to previous behavior: minimize and use background listener
            try:
                self.main.showMinimized()
            except Exception:
                try:
                    self.main.setWindowState(Qt.WindowState.WindowMinimized)
                except Exception:
                    pass

            def on_click(x, y, button, pressed):
                if pressed and button == pynput_mouse.Button.left:
                    with mss() as sct:
                        img = sct.grab({"left": x - 3, "top": y - 3, "width": 7, "height": 7})
                        color = tuple(
                            map(
                                int,
                                np.mean(
                                    np.frombuffer(img.rgb, np.uint8).reshape(7, 7, 3),
                                    axis=(0, 1),
                                ),
                            )
                        )
                    self.coords = (x, y)
                    self.base_color = color
                    self.coord_lbl.setText(f"{x}, {y}")
                    self.color_lbl.setText(str(color))
                    self.coord_lbl.setStyleSheet("color:#00ff00;font-weight:bold")
                    self.color_lbl.setStyleSheet("color:#00ff00;font-weight:bold")
                    listener.stop()
                    try:
                        QTimer.singleShot(0, lambda: self.main.update_log(f"[Автопот] Точка зафиксирована: {x},{y} | Цвет: {color}"))
                        QTimer.singleShot(0, lambda: self.main.showNormal())
                    except Exception:
                        try:
                            self.main.update_log(f"[Автопот] Точка зафиксирована: {x},{y} | Цвет: {color}")
                        except Exception:
                            pass
                    return False

            listener = pynput_mouse.Listener(on_click=on_click, daemon=True)
            listener.start()

    def pick_roi(self):
        # Показываем оверлей для выбора ROI
        try:
            overlay = ROIOverlay(self.main, message="Выделите прямоугольную область для ROI (Esc — отмена)")
            
            def handle_roi_selection(center_x, center_y, width, height):
                try:
                    # Сохраняем параметры ROI
                    self.coords = (center_x, center_y)
                    self.roi_width = width
                    self.roi_height = height
                    
                    # Обновляем соответствующие поля в интерфейсе
                    self.coord_lbl.setText(f"{center_x}, {center_y}")  # Показываем центр ROI как координаты
                    self.roi_width_edit.setText(str(width))
                    self.roi_height_edit.setText(str(height))
                    
                    # Включаем чекбокс использования ROI
                    self.use_roi_checkbox.setChecked(True)
                    self.toggle_roi_options(Qt.CheckState.Checked.value)
                    
                    # Обновляем стили
                    self.coord_lbl.setStyleSheet("color:#00ff00;font-weight:bold")
                    
                    # Логируем результат
                    try:
                        QTimer.singleShot(0, lambda: self.main.update_log(f"[Автопот] ROI зафиксирован: центр({center_x},{center_y}), ширина={width}, высота={height}"))
                        QTimer.singleShot(0, lambda: self.main.showNormal())
                    except Exception:
                        try:
                            self.main.update_log(f"[Автопот] ROI зафиксирован: центр({center_x},{center_y}), ширина={width}, высота={height}")
                        except Exception:
                            pass
                except Exception as e:
                    try:
                        QTimer.singleShot(0, lambda: self.main.update_log(f"[Автопот] Ошибка при обработке ROI: {e}"))
                    except Exception:
                        pass

            overlay.roi_selected.connect(handle_roi_selection)
            overlay.showFullScreenWithMessage()
        except Exception as e:
            # Fallback
            try:
                self.main.update_log(f"[Автопот] Ошибка при открытии оверлея ROI: {e}")
            except Exception:
                pass

    def save_to_dict(self):
        return {
            "coords": self.coords,
            "color": self.base_color,
            "press_key": self.key_btn.text().strip() or "f",
            "cd": self.cd_edit.text(),
            "thresh": self.thresh_edit.text(),
            "hotkey": self.profile_hotkey,
            "roi_width": self.roi_width,
            "roi_height": self.roi_height,
            "use_roi": self.use_roi_checkbox.isChecked() if hasattr(self, 'use_roi_checkbox') else False,
        }

    def load_from_dict(self, data):
        if not data:
            return
        self.coords = data.get("coords")
        self.base_color = data.get("color")
        if self.coords and self.base_color:
            x, y = self.coords
            self.coord_lbl.setText(f"{x}, {y}")
            self.color_lbl.setText(str(self.base_color))
            self.coord_lbl.setStyleSheet("color:#00ff00;font-weight:bold")
            self.color_lbl.setStyleSheet("color:#00ff00;font-weight:bold")
        self.key_btn.setText(data.get("press_key", "F"))
        self.cd_edit.setText(str(data.get("cd", "0.25")))
        self.thresh_edit.setText(str(data.get("thresh", "15")))
        self.profile_hotkey = data.get("hotkey", "f9")
        self.hotkey = self.profile_hotkey if self.is_valid_hotkey(self.profile_hotkey) else "f9"
        self.hotkey_btn.setText(self.hotkey.upper())
        self.setup_hotkey()
        
        # Загружаем параметры ROI
        self.roi_width = data.get("roi_width", 100)
        self.roi_height = data.get("roi_height", 20)
        use_roi = data.get("use_roi", False)
        if hasattr(self, 'use_roi_checkbox'):
            self.use_roi_checkbox.setChecked(use_roi)
            self.toggle_roi_options(use_roi)
        if hasattr(self, 'roi_width_edit'):
            self.roi_width_edit.setText(str(self.roi_width))
        if hasattr(self, 'roi_height_edit'):
            self.roi_height_edit.setText(str(self.roi_height))
