# help_tab.py — новая файл для вкладки "Помощь"
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from ui.tooltip import TooltipManager
from ui.widgets.changelog_viewer import ChangelogViewer


class HelpTab(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        # Инициализируем менеджер подсказок
        self.tooltip_manager = TooltipManager()
        # Сохраняем ссылку на главное окно
        self.main_window = main_window
        # Создаем layout для виджета
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Создаем вкладки для справки и changelog
        self.tabs = QTabWidget()
        
        # Вкладка с основной справкой
        self.help_web_view = QWebEngineView()
        self.tooltip_manager.register_widget(self.help_web_view, "Панель справки и инструкций по использованию бота")
        
        # Загружаем HTML-файл
        help_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "help.html")
        if os.path.exists(help_path):
            from PyQt6.QtCore import QUrl
            self.help_web_view.load(QUrl.fromLocalFile(help_path))
        else:
            self.help_web_view.setHtml("""
                <html>
                <body style="background: #2d2d2d; color: #ffffff; font-size: 15px; padding: 30px;">
                    Инструкция не найдена. Пожалуйста, добавьте файл assets/help.html.
                </body>
                </html>
            """)
        
        self.tabs.addTab(self.help_web_view, "Справка")
        
        # Вкладка с changelog
        self.changelog_viewer = ChangelogViewer()
        self.tabs.addTab(self.changelog_viewer, "Список изменений")
        
        layout.addWidget(self.tabs)
        
        # Подключаем обработчик смены URL для перехвата специальных сообщений
        self.help_web_view.urlChanged.connect(self.on_url_changed)
    
    def on_url_changed(self, url):
        """Обработчик смены URL для перехвата специальных сообщений"""
        url_string = url.toString()
        if url_string.startswith('switch:changelog'):
            # Переключаемся на вкладку changelog
            self.tabs.setCurrentIndex(1)  # Индекс вкладки changelog
            # Возвращаемся к предыдущему URL
            help_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "help.html")
            from PyQt6.QtCore import QUrl
            self.help_web_view.load(QUrl.fromLocalFile(help_path))
            return True
        return False
