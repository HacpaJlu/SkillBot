# utils.py — ФИНАЛЬНАЯ ВЕРСИЯ:
# • Можно менять клавишу сколько угодно
# • Клавиша НЕ пробрасывается в другие кнопки
# • НЕ ломает горячие клавиши бота и автопота
# • Работает идеально везде

import keyboard
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QLineEdit, QPushButton


class KeyCaptureButton(QPushButton):
    key_captured = pyqtSignal(str)

    def __init__(self, text="Нажми", parent=None):
        super().__init__(text, parent)
        self.setFixedSize(90, 36)
        from ui.styles import PANEL_COLOR, TEXT_COLOR, PRIMARY_COLOR, SUCCESS_COLOR
        self.setStyleSheet(
            f"background:{PANEL_COLOR};color:{TEXT_COLOR};border-radius:8px;font-weight:bold;"
        )
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.is_capturing = False
        self.hook = None
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
        from ui.styles import PRIMARY_COLOR, TEXT_COLOR
        self.setStyleSheet(
            f"background:{PRIMARY_COLOR};color:{TEXT_COLOR};border-radius:8px;font-weight:bold;"
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
                from ui.styles import SUCCESS_COLOR, TEXT_COLOR, PANEL_COLOR
                self.setStyleSheet(
                    f"background:{SUCCESS_COLOR};color:#00ff80;border-radius:8px;font-weight:bold;"
                )
                QTimer.singleShot(
                    300,
                    lambda: self.setStyleSheet(
                        f"background:{PANEL_COLOR};color:{TEXT_COLOR};border-radius:8px;font-weight:bold;"
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
            from ui.styles import PANEL_COLOR, TEXT_COLOR
            self.setStyleSheet(
                f"background:{PANEL_COLOR};color:{TEXT_COLOR};border-radius:8px;font-weight:bold;"
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


class SelectAllLineEdit(QLineEdit):
    def focusInEvent(self, event):
        super().focusInEvent(event)
        QTimer.singleShot(0, self.selectAll)

    def focusOutEvent(self, event):
        """Normalize numeric input: '05' -> '0.5', '5' -> '5', etc."""
        super().focusOutEvent(event)
        try:
            txt = self.text().strip()
            if txt:
                # Replace comma with dot
                txt = txt.replace(',', '.')
                # Try to parse as float
                try:
                    val = float(txt)
                    # If input was like "05", convert to "0.5"
                    # Check if the original text has more leading zeros than typical (e.g., "05", "005")
                    # and interpret it as fractional if all digits were 0-9 without decimal point originally
                    original_clean = self.text().strip().replace(',', '.')
                    if '.' not in self.text() and original_clean.isdigit():
                        # Pure digit string like "5" or "05" or "005"
                        # Check if it starts with 0 and has length > 1
                        if self.text().strip()[0] == '0' and len(self.text().strip()) > 1:
                            # Treat "05" as "0.5", "005" as "0.05", etc.
                            # Count leading zeros
                            digit_part = self.text().strip()
                            # Convert "05" -> 5 -> "5" then prepend "0."
                            # Better: interpret "05" as 5 * 10^(-(len-1)) = 5 * 0.1 = 0.5
                            val = float(digit_part)
                            # Shift decimal point: if we had N digits total, 
                            # we want (N-1) decimal places
                            num_digits = len(digit_part)
                            val = val / (10 ** (num_digits - 1))
                    # Format with appropriate decimal places
                    self.setText(str(val))
                except ValueError:
                    # If not a valid float, leave as is
                    pass
        except Exception:
            pass

    def keyPressEvent(self, event):
        """Auto-replace comma with dot for numeric input."""
        if event.text() == ',':
            # Replace comma with dot
            try:
                cursor_pos = self.cursorPosition()
                text = self.text()
                new_text = text[:cursor_pos] + '.' + text[cursor_pos + 1:]
                self.setText(new_text)
                self.setCursorPosition(cursor_pos + 1)
                return
            except Exception:
                pass
        super().keyPressEvent(event)
