# overlay_tab.py — copied for refactor compatibility (contains OverlayTab)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QCheckBox, QPushButton, QSizePolicy, QColorDialog
)
from PyQt6.QtGui import QColor


class OverlayTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.setStyleSheet("QFormLayout { margin: 20px; }")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.cbs = []
        cbs_text = ["Статус бота", "Статус автопота", "Текущий каст", "Срочный скилл", "Очередь"]
        attrs = ["show_bot_status", "show_autopot", "show_casting", "show_urgent", "show_queue"]
        for i, text in enumerate(cbs_text):
            cb = QCheckBox(text)
            cb.setChecked(getattr(self.main.overlay_window, attrs[i]))
            def make_lambda(idx_val):
                return lambda state: self.update_visibility(idx_val, state == Qt.CheckState.Checked)
            cb.stateChanged.connect(make_lambda(i))
            self.cbs.append(cb)
            form.addRow(cb)

        self.bg_btn = QPushButton("Цвет фона (с прозрачностью)")
        self.bg_btn.clicked.connect(self.pick_bg_color)
        form.addRow(self.bg_btn)

        self.text_btn = QPushButton("Цвет текста")
        self.text_btn.clicked.connect(self.pick_text_color)
        form.addRow(self.text_btn)

        self.click_through_cb = QCheckBox("Пропускать клики мыши")
        self.click_through_cb.setChecked(self.main.overlay_window.click_through)
        self.click_through_cb.stateChanged.connect(self.update_click_through)
        form.addRow(self.click_through_cb)

        layout.addLayout(form)
        layout.addStretch()

    def update_visibility(self, idx, checked):
        attrs = ["show_bot_status", "show_autopot", "show_casting", "show_urgent", "show_queue"]
        setattr(self.main.overlay_window, attrs[idx], checked)
        self.main.overlay_window.labels[idx].setVisible(checked)
        self.main.overlay_window.update()

    def pick_bg_color(self):
        dialog = QColorDialog(self.main.overlay_window.bg_color, self)
        dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, True)
        dialog.setWindowTitle("Выберите цвет фона оверлея")
        
        if dialog.exec() == QColorDialog.DialogCode.Accepted:
            color = dialog.currentColor()
            if color.isValid():
                self.main.overlay_window.bg_color = color
                self.main.overlay_window.update()

    def pick_text_color(self):
        color = QColorDialog.getColor(self.main.overlay_window.text_color, self)
        if color.isValid():
            self.main.overlay_window.text_color = color
            for label in self.main.overlay_window.labels:
                label.setStyleSheet(f"color: {color.name()};")
            self.main.overlay_window.update()

    def update_click_through(self):
        self.main.overlay_window.set_click_through(self.click_through_cb.isChecked())

    def save_to_dict(self):
        return self.main.overlay_window.save_settings()

    def load_from_dict(self, data):
        self.main.overlay_window.load_settings(data)
        self.click_through_cb.setChecked(self.main.overlay_window.click_through)
        attrs = ["show_bot_status", "show_autopot", "show_casting", "show_urgent", "show_queue"]
        for i, cb in enumerate(self.cbs):
            cb.setChecked(getattr(self.main.overlay_window, attrs[i]))
