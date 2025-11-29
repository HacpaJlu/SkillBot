# main_tab.py — новая файл для вкладки "Главная"
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QSizePolicy
)


class MainTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Примение стилей через объекты
        self.status_label = QLabel("ОЖИДАНИЕ...")
        self.status_label.setObjectName("status_label")
        self.status_label.setProperty("status", "inactive")  # Для стилей
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.status_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #b0b0b0;")
        layout.addWidget(self.status_label)

        self.casting_label = QLabel("")
        self.casting_label.setObjectName("casting_label")
        self.casting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.casting_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.casting_label.setStyleSheet("font-size: 22px; color: #ffc107; font-weight: bold;")
        layout.addWidget(self.casting_label)

        self.urgent_label = QLabel("")
        self.urgent_label.setObjectName("urgent_label")
        self.urgent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.urgent_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.urgent_label.setStyleSheet("font-size: 20px; color: #ff0066; font-weight: bold;")
        layout.addWidget(self.urgent_label)

        self.queue_label = QLabel("Очередь пуста")
        self.queue_label.setObjectName("queue_label")
        self.queue_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.queue_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.queue_label.setStyleSheet("font-size: 20px; color: #4caf50;")
        layout.addWidget(self.queue_label)
        
        self.skills_count_label = QLabel("Скиллов: 0")
        self.skills_count_label.setObjectName("skills_count_label")
        self.skills_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.skills_count_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.skills_count_label.setStyleSheet("font-size: 24px; color: #00d4ff;")
        layout.addWidget(self.skills_count_label)

        self.autopot_status_label = QLabel("АВТОПОТ: ВЫКЛЮЧЕН")
        self.autopot_status_label.setObjectName("autopot_status_label")
        self.autopot_status_label.setProperty("status", "inactive")  # Для стилей
        self.autopot_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.autopot_status_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.autopot_status_label.setStyleSheet("font-size: 18px; color: #f44336; font-weight: bold;")
        layout.addWidget(self.autopot_status_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("cooldowns_scroll")
        scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #444444;
                border-radius: 6px;
                background-color: #2d2d2d;
            }
        """)
        self.cooldowns_widget = QWidget()
        self.cooldowns_layout = QVBoxLayout(self.cooldowns_widget)
        self.cooldowns_layout.setSpacing(8)
        self.cooldowns_layout.setContentsMargins(10, 10, 10, 10)
        scroll.setWidget(self.cooldowns_widget)
        layout.addWidget(scroll, 1)
