#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функциональности вкладки "Помощь"
"""
import sys
import os
# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from ui.tabs.help_tab import HelpTab

class TestMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Тест вкладки Помощь")
        self.setGeometry(100, 100, 1200, 800)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Создаем layout
        layout = QVBoxLayout(central_widget)
        
        # Создаем вкладку помощи
        self.help_tab = HelpTab()
        layout.addWidget(self.help_tab)

def main():
    app = QApplication(sys.argv)
    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()