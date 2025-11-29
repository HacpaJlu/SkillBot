from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QTimer


class SelectAllLineEdit(QLineEdit):
    def focusInEvent(self, event):
        super().focusInEvent(event)
        QTimer.singleShot(0, self.selectAll)
