from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QTimer
from ui.tooltip import TooltipManager


class SelectAllLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Инициализируем менеджер подсказок
        self.tooltip_manager = TooltipManager()
        # Добавляем подсказку
        self.tooltip_manager.register_widget(self, "Поле ввода, в котором весь текст выделяется при фокусе")
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        QTimer.singleShot(0, self.selectAll)
