"""
Window and tab styles for SkillBot application
This module contains styles for main window and tabs
"""
from .colors import *

# Стили для основного окна
MAIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    QTabWidget {{
        background-color: {BACKGROUND_COLOR};
        border: none;
    }}
    
    QTabWidget::pane {{
        border: none;
        background-color: {BACKGROUND_COLOR};
    }}
    
    QTabBar {{
        height: 50px;
        alignment: center;
    }}
    
    QTabWidget::tab-bar {{
        alignment: center;
    }}
    
    QTabBar::tab {{
    }}
    
    QTabBar::tab {{
        background-color: {PANEL_COLOR};
        color: {TEXT_SECONDARY};
        padding: 12px 20px;
        margin: 1px;
        border-top-left-radius: 0px;
        border-top-right-radius: 0px;
        font-size: 20px;
        font-weight: 600;
        min-width: 0px;
        width: 100%;
        min-height: 40px;
        border: 1px solid #444;
    }}
    
    QTabBar::tab:selected {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border-bottom: 4px solid {HIGHLIGHT_COLOR};
    }}
    
    QTabBar::tab:hover {{
        background-color: {HIGHLIGHT_COLOR};
        color: white;
    }}
    
    QTabBar::tab:!selected {{
        border-bottom: 2px solid #555;
    }}
    
    QWidget {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
    }}
"""