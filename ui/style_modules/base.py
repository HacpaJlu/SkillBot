"""
Base styles for SkillBot application
This module contains basic component styles (buttons, checkboxes, inputs, etc.)
"""
from .colors import *

# Стили для кнопок
BUTTON_STYLES = f"""
    QPushButton {{
        background-color: {PANEL_COLOR};
        color: {TEXT_COLOR};
        border: 1px solid #444;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 13px;
        font-weight: 500;
        min-height: 32px;
    }}
    
    QPushButton:hover {{
        background-color: {PANEL_COLOR};
        border-color: {HIGHLIGHT_COLOR};
    }}
    
    QPushButton:pressed {{
        background-color: {PANEL_COLOR};
    }}
    
    QPushButton:checked {{
        background-color: {PRIMARY_COLOR};
        border-color: {PRIMARY_COLOR};
    }}
    
    QPushButton#primary {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border-color: {PRIMARY_COLOR};
    }}
    
    QPushButton#primary:hover {{
        background-color: {PRIMARY_COLOR};
        border-color: {PRIMARY_COLOR};
    }}
    
    QPushButton#danger {{
        background-color: {DANGER_COLOR};
        color: white;
        border-color: {DANGER_COLOR};
    }}
    
    QPushButton#danger:hover {{
        background-color: {DANGER_COLOR};
        border-color: {DANGER_COLOR};
    }}
    
    QPushButton#success {{
        background-color: {SUCCESS_COLOR};
        color: white;
        border-color: {SUCCESS_COLOR};
    }}
    
    QPushButton#success:hover {{
        background-color: {SUCCESS_COLOR};
        border-color: {SUCCESS_COLOR};
    }}
"""

# Стили для чекбоксов и переключателей
CHECKBOX_STYLES = f"""
    QCheckBox {{
        spacing: 4px;
        padding: 4px;
        color: {TEXT_COLOR};
    }}
    
    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 2px solid {TEXT_DISABLED};
        border-radius: 4px;
        background-color: {PANEL_COLOR};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {PRIMARY_COLOR};
        border-color: {PRIMARY_COLOR};
        image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTExLjY5NjcgNS42OTY3MUw2LjUgMTAuODkzNCIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+Cg==);
    }}
    
    QCheckBox::indicator:unchecked:hover {{
        border-color: {HIGHLIGHT_COLOR};
    }}
    
    QCheckBox::indicator:checked:hover {{
        background-color: {PRIMARY_COLOR};
    }}
"""

# Стили для полей ввода
INPUT_STYLES = f"""
    QLineEdit {{
        background-color: {PANEL_COLOR};
        color: {TEXT_COLOR};
        border: 1px solid #444;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 13px;
        min-height: 32px;
    }}
    
    QLineEdit:focus {{
        border-color: {PRIMARY_COLOR};
        outline: none;
    }}
    
    QLineEdit:hover {{
        border-color: {HIGHLIGHT_COLOR};
    }}
    
    QComboBox {{
        background-color: {PANEL_COLOR};
        color: {TEXT_COLOR};
        border: 1px solid #444;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 13px;
        min-height: 32px;
    }}
    
    QComboBox:focus {{
        border-color: {PRIMARY_COLOR};
        outline: none;
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    
    QComboBox::down-arrow {{
        image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xLjQxNDE0IDEuNDE0MTRMNS45OTk5OSA2TDEwLjU4NTggMS40MTQxNCIgc3Ryb2tlPSIjZTBlMGUwIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
        width: 10px;
        height: 7px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {PANEL_COLOR};
        color: {TEXT_COLOR};
        selection-background-color: {PRIMARY_COLOR};
        selection-color: white;
        border: 1px solid #444;
        border-radius: 4px;
    }}
"""

# Стили для прокрутки
SCROLLBAR_STYLES = f"""
    QScrollBar:vertical {{
        background-color: {PANEL_COLOR};
        width: 8px;
        border-radius: 5px;
        margin: 0px 0px 0px 0px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {BACKGROUND_COLOR};
        border-radius: 5px;
        min-height: 16px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {HIGHLIGHT_COLOR};
    }}
    
    QScrollBar::handle:vertical:pressed {{
        background-color: {PRIMARY_COLOR};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
        subcontrol-origin: margin;
    }}
    
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}
"""