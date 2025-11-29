import keyboard
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QPushButton
from ui.tooltip import TooltipManager


class KeyCaptureButton(QPushButton):
    key_captured = pyqtSignal(str)

    def __init__(self, text="Нажми", parent=None):
        super().__init__(text, parent)
        self.setFixedSize(90, 36)
        self.setStyleSheet(
            "background:#333;color:white;border-radius:8px;font-weight:bold;"
        )
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.is_capturing = False
        self.hook = None
        # Инициализируем менеджер подсказок
        self.tooltip_manager = TooltipManager()
        # Добавляем подсказку
        self.tooltip_manager.register_widget(self, "Кнопка для захвата клавиши - нажмите для назначения")
        self.clicked.connect(self.toggle_capture)

    def toggle_capture(self):
        if self.is_capturing:
            self.cancel_capture()
        else:
            self.start_capture()

    def start_capture(self):
        if self.is_capturing:
            return

        self.is_capturing = True
        self.setText("Жду...")
        self.setStyleSheet(
            "background:#0066cc;color:white;border-radius:6px;font-weight:bold;font-size:12px;"
        )

        # Очищаем только наш хук — НЕ трогаем глобальные горячие клавиши!
        if self.hook:
            try:
                keyboard.unhook(self.hook)
            except Exception as e:
                print(f"Ошибка unhook в KeyCaptureButton: {e}")

        def on_press(key):
            if not self.is_capturing:
                return False

            try:
                name = getattr(key, "name", str(key))
                if not name:
                    return True

                # Нормализуем имя
                if len(name) == 1:
                    name = name.lower()
                elif "left" in name or "right" in name:
                    name = name.split()[-1]
                else:
                    name = name.lower()

                # Принимаем клавишу
                self.setText(name.upper())
                self.key_captured.emit(name)

                # Краткая зелёная вспышка — подтверждение
                self.setStyleSheet(
                    "background:#004400;color:#00ff80;border-radius:8px;font-weight:bold;"
                )
                QTimer.singleShot(
                    300,
                    lambda: self.setStyleSheet(
                        "background:#333;color:white;border-radius:6px;font-weight:bold;font-size:12px;"
                    ),
                )

                self.stop_capture()
                return False  # ← Клавиша поглощена — не уходит дальше
            except Exception as e:
                print(f"Ошибка захвата клавиши: {e}")
                self.stop_capture()
                return False

        # suppress=True — клавиша НЕ доходит до других кнопок и НЕ мешает боту!
        self.hook = keyboard.on_press(on_press, suppress=True)
        QTimer.singleShot(8000, self.cancel_capture)

    def stop_capture(self):
        if not self.is_capturing:
            return
        self.is_capturing = False
        if self.hook:
            try:
                keyboard.unhook(self.hook)
            except Exception as e:
                print(f"Ошибка unhook в KeyCaptureButton: {e}")
            self.hook = None
        if self.text() == "Жду...":
            self.setText("Нажми")
            self.setStyleSheet(
                "background:#333;color:white;border-radius:6px;font-weight:bold;font-size:12px;"
            )

    def cancel_capture(self):
        self.stop_capture()

    def mousePressEvent(self, event):
        # Клик по кнопке = начать/отменить захват
        self.toggle_capture()
        event.accept()

    def keyPressEvent(self, event):
        # Любая клавиша во время захвата — отмена
        if self.is_capturing:
            self.cancel_capture()
        super().keyPressEvent(event)
