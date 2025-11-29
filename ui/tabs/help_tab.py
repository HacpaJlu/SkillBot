# help_tab.py — новая файл для вкладки "Помощь"
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from ui.tooltip import TooltipManager

class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        from PyQt6.QtWidgets import QSizePolicy
        # Инициализируем менеджер подсказок
        self.tooltip_manager = TooltipManager()
        # Создаем layout для виджета
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Создаем QWebEngineView для отображения HTML с поддержкой JavaScript
        self.web_view = QWebEngineView()
        # Добавляем подсказку
        self.tooltip_manager.register_widget(self.web_view, "Панель справки и инструкций по использованию бота")
        # Устанавливаем политику размера
        self.web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Загружаем HTML-файл
        help_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "help.html")
        if os.path.exists(help_path):
            from PyQt6.QtCore import QUrl
            self.web_view.load(QUrl.fromLocalFile(help_path))
        else:
            self.web_view.setHtml("""
                <html>
                <body style="background: #2d2d2d; color: #ffffff; font-size: 15px; padding: 30px;">
                    Инструкция не найдена. Пожалуйста, добавьте файл assets/help.html.
                </body>
                </html>
            """)
        
        layout.addWidget(self.web_view)
