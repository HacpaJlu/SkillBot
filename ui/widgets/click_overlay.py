from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtGui import QFont, QPainter, QColor


class ClickOverlay(QWidget):
    clicked = pyqtSignal(int, int)

    def __init__(self, parent=None, message="Кликните левой кнопкой мыши для выбора точки"):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.message = message

        self.label = QLabel(self.message, self)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet('color: white; background: rgba(0,0,0,0);')
        self.label.adjustSize()

    def showFullScreenWithMessage(self, message=None):
        if message:
            self.message = message
            self.label.setText(self.message)
            self.label.adjustSize()
        # Compute union of all screens to support multi-monitor setups
        try:
            screens = QApplication.screens()
            if screens:
                union_rect = QRect()
                for s in screens:
                    geo = s.geometry()
                    if union_rect.isNull():
                        union_rect = QRect(geo)
                    else:
                        union_rect = union_rect.united(geo)
                # position and size to cover all monitors
                self.setGeometry(union_rect)
            else:
                # fallback to primary screen
                # PyQt6: screen() may return None, use QApplication.primaryScreen()
                screen = QApplication.primaryScreen()
                if screen:
                    self.resize(screen.size())
        except Exception:
            try:
                # Fallback to primary screen
                screen = QApplication.primaryScreen()
                if screen:
                    self.resize(screen.size())
            except Exception:
                pass

        # center label near top center of the combined area
        try:
            self.label.move((self.width() - self.label.width()) // 2, 40)
        except Exception:
            pass
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # PyQt6: globalX()/globalY() replaced with globalPosition()
            pos = event.globalPosition()
            x = int(pos.x())
            y = int(pos.y())
            self.clicked.emit(x, y)
            self.hide()
        elif event.button() == Qt.MouseButton.RightButton:
            # allow cancel with right click
            self.hide()

    def keyPressEvent(self, event):
        # allow Esc to cancel
        if event.key() == Qt.Key.Key_Escape:
            self.hide()


class WindowSelectOverlay(QWidget):
    window_selected = pyqtSignal(str)  # Emits window process name

    def __init__(self, parent=None, message="Кликни на окно для выбора"):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.message = message

        self.label = QLabel(self.message, self)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet('color: white; background: rgba(0,0,0,0);')
        self.label.adjustSize()

    def showFullScreenWithMessage(self, message=None):
        if message:
            self.message = message
            self.label.setText(self.message)
            self.label.adjustSize()
        # Compute union of all screens to support multi-monitor setups
        try:
            screens = QApplication.screens()
            if screens:
                union_rect = QRect()
                for s in screens:
                    geo = s.geometry()
                    if union_rect.isNull():
                        union_rect = QRect(geo)
                    else:
                        union_rect = union_rect.united(geo)
                # position and size to cover all monitors
                self.setGeometry(union_rect)
            else:
                # fallback to primary screen
                # PyQt6: screen() may return None, use QApplication.primaryScreen()
                screen = QApplication.primaryScreen()
                if screen:
                    self.resize(screen.size())
        except Exception:
            try:
                # Fallback to primary screen
                screen = QApplication.primaryScreen()
                if screen:
                    self.resize(screen.size())
            except Exception:
                pass

        # center label near top center of the combined area
        try:
            self.label.move((self.width() - self.label.width()) // 2, 40)
        except Exception:
            pass
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            try:
                import win32gui
                import win32process
                import win32con
                import psutil
                import os
                from PyQt6.QtCore import QTimer

                # PyQt6: globalPos() replaced with globalPosition()
                pos = event.globalPosition()

                # Hide overlay first so WindowFromPoint returns the underlying window
                self.hide()

                def lookup():
                    try:
                        hwnd = win32gui.WindowFromPoint((int(pos.x()), int(pos.y())))
                        # If hwnd belongs to this python process (our overlay), skip to next
                        mypid = os.getpid()
                        attempts = 0
                        while hwnd and attempts < 10:
                            try:
                                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                                if pid == mypid:
                                    # try next window in Z-order
                                    hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
                                    attempts += 1
                                    continue
                                break
                            except Exception:
                                break

                        if hwnd:
                            try:
                                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                                proc = psutil.Process(pid)
                                window_name = proc.name()
                                if window_name.endswith('.exe'):
                                    window_name = window_name[:-4]
                                self.window_selected.emit(window_name)
                            except Exception as e:
                                print(f"Error getting process info: {e}")
                    except Exception as e:
                        print(f"Error selecting window: {e}")
                    finally:
                        try:
                            self.close()
                        except Exception:
                            pass

                # small delay to allow the overlay to hide and OS to update
                QTimer.singleShot(60, lookup)
            except Exception as e:
                print(f"Error selecting window (setup): {e}")
        elif event.button() == Qt.MouseButton.RightButton:
            # allow cancel with right click
            self.hide()

    def keyPressEvent(self, event):
        # allow Esc to cancel
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
