from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPoint
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtGui import QFont, QPainter, QColor, QPen


class ROIOverlay(QWidget):
    """
    Оверлей для выделения прямоугольной области ROI (Region of Interest)
    """
    roi_selected = pyqtSignal(int, int, int, int)  # x, y, width, height
    roi_canceled = pyqtSignal()

    def __init__(self, parent=None, message="Выделите прямоугольную область для ROI (Esc — отмена)"):
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

        self.drawing = False
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.current_rect = QRect()

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
        
        # Draw the current selection rectangle if we're drawing
        if self.drawing:
            pen = QPen(QColor(255, 255, 0), 2)
            pen.setStyle(Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.drawRect(self.current_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.start_point = event.position().toPoint()
            self.end_point = self.start_point
            self.current_rect = QRect(self.start_point, self.end_point)
            self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            # allow cancel with right click
            self.drawing = False
            self.hide()
            self.roi_canceled.emit()

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = event.position().toPoint()
            # Calculate the rectangle from start to end points
            left = min(self.start_point.x(), self.end_point.x())
            top = min(self.start_point.y(), self.end_point.y())
            right = max(self.start_point.x(), self.end_point.x())
            bottom = max(self.start_point.y(), self.end_point.y())
            
            self.current_rect = QRect(left, top, right - left, bottom - top)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            if self.current_rect.width() > 0 and self.current_rect.height() > 0:
                # Emit the ROI coordinates: center_x, center_y, width, height
                center_x = self.current_rect.x() + self.current_rect.width() // 2
                center_y = self.current_rect.y() + self.current_rect.height() // 2
                width = self.current_rect.width()
                height = self.current_rect.height()
                
                self.roi_selected.emit(center_x, center_y, width, height)
            self.hide()

    def keyPressEvent(self, event):
        # allow Esc to cancel
        if event.key() == Qt.Key.Key_Escape:
            self.drawing = False
            self.hide()
            self.roi_canceled.emit()