# changelog_viewer.py — виджет для просмотра changelog.md
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ui.tooltip import TooltipManager
# Попробуем импортировать markdown, и если он недоступен, покажем сообщение об ошибке
try:
    import markdown
except ImportError:
    markdown = None


class ChangelogViewer(QWidget):
    def __init__(self):
        super().__init__()
        # Инициализируем менеджер подсказок
        self.tooltip_manager = TooltipManager()
        
        # Создаем layout для виджета
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Создаем QTextBrowser для отображения HTML-контента
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)  # Открывать внешние ссылки в браузере
        self.text_browser.setOpenLinks(False)  # Не открывать внутренние ссылки автоматически
        
        # Устанавливаем стили для просмотра markdown
        self.text_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 12pt;
            }
        """)
        
        # Загружаем и отображаем changelog
        self.load_changelog()
        
        layout.addWidget(self.text_browser)
        
    def load_changelog(self):
        """Загружает и отображает содержимое changelog.md"""
        try:
            changelog_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "changelog.md")
            
            if os.path.exists(changelog_path):
                with open(changelog_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Конвертируем markdown в HTML
                if markdown is not None:
                    html_content = markdown.markdown(content, extensions=['extra', 'codehilite', 'toc'])
                else:
                    # Если markdown недоступен, отображаем содержимое как обычный текст
                    html_content = f"<pre>{content}</pre>"
                
                # Добавляем стили для лучшего отображения
                styled_html = f"""
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        color: #e0e0e0;
                        background-color: #2d2d2d;
                        line-height: 1.6;
                        padding: 20px;
                    }}
                    h1, h2, h3, h4, h5, h6 {{
                        color: #0078d4;
                        border-bottom: 1px solid #444444;
                        padding-bottom: 5px;
                        margin-top: 20px;
                        margin-bottom: 15px;
                    }}
                    h1 {{
                        color: #ff0066;
                        font-size: 2em;
                    }}
                    h2 {{
                        color: #0078d4;
                        font-size: 1.6em;
                    }}
                    h3 {{
                        color: #1dd1a1;
                        font-size: 1.4em;
                    }}
                    a {{
                        color: #0078d4;
                        text-decoration: none;
                    }}
                    a:hover {{
                        color: #00d4ff;
                    }}
                    code {{
                        background-color: #3a3a3a;
                        padding: 2px 6px;
                        border-radius: 3px;
                        font-family: 'Courier New', monospace;
                    }}
                    pre {{
                        background-color: #3a3a3a;
                        padding: 10px;
                        border-radius: 5px;
                        overflow: auto;
                    }}
                    pre code {{
                        background: none;
                        padding: 0;
                    }}
                    blockquote {{
                        border-left: 4px solid #0078d4;
                        padding-left: 15px;
                        margin-left: 0;
                        color: #ccc;
                    }}
                    ul, ol {{
                        padding-left: 25px;
                    }}
                    li {{
                        margin: 5px 0;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin: 15px 0;
                    }}
                    th, td {{
                        border: 1px solid #444444;
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #3a3a3a;
                    }}
                </style>
                <div style="max-width: 900px; margin: 0 auto;">
                    {html_content}
                </div>
                """
                
                self.text_browser.setHtml(styled_html)
            else:
                self.text_browser.setHtml("""
                    <div style="color: #ff6666; text-align: center; padding: 50px;">
                        <h2>Файл changelog.md не найден</h2>
                        <p>Файл changelog.md должен находиться в корне проекта</p>
                    </div>
                """)
        except Exception as e:
            self.text_browser.setHtml(f"""
                <div style="color: #ff6666; padding: 20px;">
                    <h3>Ошибка загрузки changelog.md:</h3>
                    <p>{str(e)}</p>
                </div>
            """)

    def check_markdown_available(self):
        """Проверяет, доступен ли модуль markdown"""
        return markdown is not None
    
    def refresh(self):
        """Обновляет отображение changelog"""
        self.load_changelog()