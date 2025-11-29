from PyQt6.QtCore import Qt, QPoint, QSize, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QCheckBox, QPushButton, QColorDialog, QLabel
from ui.tooltip import TooltipManager

class OverlayWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        # Инициализируем менеджер подсказок
        self.tooltip_manager = TooltipManager()

        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.click_through = True
        self.old_pos = None
        self.resizing = False

        self.bg_color = QColor(20, 30, 60, 10)
        self.text_color = QColor(0, 255, 200)
        self.show_bot_status = True
        self.show_autopot = True
        self.show_casting = True
        self.show_urgent = True
        self.show_queue = True

        self.setMinimumSize(240, 130)

        self.status_text = "БОТ: ОЖИДАНИЕ..."
        self.autopot_text = "АВТОПОТ: ВЫКЛЮЧЕН"
        self.casting_text = ""
        self.urgent_text = ""
        self.queue_text = "Очередь пуста"

        try:
            # PyQt6: QFont.Weight.Bold
            weight = QFont.Weight.Bold
        except Exception:
            # Fallback for older/newer bindings
            weight = 75
        self.font_obj = QFont()
        self.font_obj.setFamily("Segoe UI")
        self.font_obj.setPointSize(11)
        try:
            self.font_obj.setWeight(weight)
        except Exception:
            self.font_obj.setBold(True)

        self.layout_obj = QVBoxLayout(self)
        self.layout_obj.setContentsMargins(15, 10, 15, 10)
        self.labels = []
        texts = [self.status_text, self.autopot_text, self.casting_text, self.urgent_text, self.queue_text]
        visibles = [self.show_bot_status, self.show_autopot, self.show_casting, self.show_urgent, self.show_queue]
        for text, visible in zip(texts, visibles):
            label = QLabel(text)
            label.setFont(self.font_obj)
            label.setStyleSheet(f"color: {self.text_color.name()};")
            label.setVisible(visible)
            # Добавляем подсказку
            self.tooltip_manager.register_widget(label, f"Элемент оверлея: {text}")
            self.layout_obj.addWidget(label)
            self.labels.append(label)

        self.main.bot.update_signal.connect(self.update_overlay)

        self.update_overlay("", {}, "", "", "")

    def paintEvent(self, event):
        if self.bg_color.alpha() == 0:
            return

        painter = QPainter(self)
        try:
            # PyQt6: Antialiasing might be in different enum, try without render hints first
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        except Exception:
            pass  # Skip antialiasing if not available
        painter.setBrush(self.bg_color)
        painter.drawRoundedRect(self.rect(), 20, 20)

    def update_overlay(self, status, cooldowns, casting_info, queue_info, urgent_skill):
        self.status_text = status
        ap_running = self.main.autopot_tab and self.main.autopot_tab.thread.isRunning() if self.main.autopot_tab else False
        ap_text = "РАБОТАЕТ" if ap_running else "ВЫКЛЮЧЕН"
        self.autopot_text = f"АВТОПОТ: {ap_text}"
        self.casting_text = casting_info or ""
        self.urgent_text = urgent_skill or ""
        self.queue_text = queue_info or "Очередь пуста"
        for i, (visible, text) in enumerate([(self.show_bot_status, self.status_text), (self.show_autopot, self.autopot_text), (self.show_casting, self.casting_text), (self.show_urgent, self.urgent_text), (self.show_queue, self.queue_text)]):
            if visible:
                self.labels[i].setText(text)
                self.labels[i].show()
            else:
                self.labels[i].hide()
        self.setVisible(self.bg_color.alpha() != 0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.click_through:
            # PyQt6: globalPos() replaced with globalPosition()
            self.old_pos = event.globalPosition()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            if (self.width() - event.pos().x() <= 40 and self.height() - event.pos().y() <= 40):
                self.resizing = True
            else:
                self.resizing = False

    def mouseMoveEvent(self, event):
        if not self.old_pos or self.click_through: return
        # PyQt6: globalPos() replaced with globalPosition()
        delta_pos = event.globalPosition() - self.old_pos
        if self.resizing:
            new_size = self.size() + QSize(int(delta_pos.x()), int(delta_pos.y()))
            new_size = new_size.expandedTo(QSize(200, 100))
            self.resize(new_size)
        else:
            self.move(self.pos() + QPoint(int(delta_pos.x()), int(delta_pos.y())))
        self.old_pos = event.globalPosition()

    def mouseReleaseEvent(self, event):
        self.old_pos = None
        self.resizing = False

    def set_click_through(self, enabled):
        self.click_through = enabled
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, enabled)
        self.show()

    def save_settings(self):
        return {
            "position": (self.pos().x(), self.pos().y()),
            "size": (self.width(), self.height()),
            "bg_color": self.bg_color.name(),
            "text_color": self.text_color.name(),
            "show_bot_status": self.show_bot_status,
            "show_autopot": self.show_autopot,
            "show_casting": self.show_casting,
            "show_urgent": self.show_urgent,
            "show_queue": self.show_queue,
            "click_through": self.click_through,
        }

    def load_settings(self, data):
        if "position" in data: self.move(QPoint(*data["position"]))
        if "size" in data: self.resize(QSize(*data["size"]))
        if "bg_color" in data: self.bg_color = QColor(data["bg_color"]) 
        if "text_color" in data: self.text_color = QColor(data["text_color"]) 
        if "show_bot_status" in data: self.show_bot_status = data["show_bot_status"]
        if "show_autopot" in data: self.show_autopot = data["show_autopot"]
        if "show_casting" in data: self.show_casting = data["show_casting"]
        if "show_urgent" in data: self.show_urgent = data["show_urgent"]
        if "show_queue" in data: self.show_queue = data["show_queue"]
        if "click_through" in data: self.set_click_through(data["click_through"])
        for label in self.labels:
            label.setStyleSheet(f"color: {self.text_color.name()};")
        self.update()
