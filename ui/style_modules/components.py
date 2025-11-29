"""
Component-specific styles for SkillBot application
This module contains styles for specific UI components (skills, autopot, etc.)
"""
from .colors import *

# Стили для вкладки Main
MAIN_TAB_STYLES = f"""
    QLabel#status_label {{
        font-size: 32px;
        font-weight: bold;
        color: {TEXT_SECONDARY};
        qproperty-alignment: AlignCenter;
    }}
    
    QLabel#status_label[status="active"] {{
        color: {SUCCESS_COLOR};
    }}
    
    QLabel#status_label[status="paused"] {{
        color: {WARNING_COLOR};
    }}
    
    QLabel#casting_label {{
        font-size: 22px;
        color: {WARNING_COLOR};
        font-weight: bold;
        qproperty-alignment: AlignCenter;
    }}
    
    QLabel#urgent_label {{
        font-size: 20px;
        color: {SECONDARY_COLOR};
        font-weight: bold;
        qproperty-alignment: AlignCenter;
    }}
    
    QLabel#queue_label {{
        font-size: 20px;
        color: {SUCCESS_COLOR};
        qproperty-alignment: AlignCenter;
    }}
    
    QLabel#skills_count_label {{
        font-size: 24px;
        color: {HIGHLIGHT_COLOR};
        qproperty-alignment: AlignCenter;
    }}
    
    QLabel#autopot_status_label {{
        font-size: 18px;
        color: {DANGER_COLOR};
        font-weight: bold;
        qproperty-alignment: AlignCenter;
    }}
    
    QLabel#autopot_status_label[status="active"] {{
        color: {SUCCESS_COLOR};
    }}
    
    QScrollArea#cooldowns_scroll {{
        background-color: {PANEL_COLOR};
        border: 1px solid #444;
        border-radius: 6px;
    }}
"""

# Стили для вкладки Settings
SETTINGS_TAB_STYLES = f"""
    QFormLayout {{
        margin: 4px;
    }}
    
    QGroupBox {{
        background-color: {PANEL_COLOR};
        border: 1px solid #444;
        border-radius: 6px;
        margin-top: 0.5ex;
        padding-top: 4px;
        padding-bottom: 4px;
        padding-left: 4px;
        padding-right: 4px;
        font-weight: bold;
        color: {HIGHLIGHT_COLOR};
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }}
    
    /* Стили для вкладки автопота */
    QWidget#autopot_tab {{
        background-color: {BACKGROUND_COLOR};
        padding: 10px;
    }}
    
    QPushButton#autopot_delete {{
        background-color: {DANGER_COLOR};
        color: white;
        border: none;
        border-radius: 3px;
        padding: 3px 6px;
        font-weight: bold;
        font-size: 12px;
        min-width: 20px;
        min-height: 20px;
    }}
    
    QPushButton#autopot_delete:hover {{
        background-color: #d32f2f;
    }}
    
    QPushButton#autopot_delete:pressed {{
        background-color: #b71c1c;
    }}
"""

# Стили для элементов навыков
SKILL_ITEM_STYLES = f"""
    QWidget#skill_row {{
        background-color: {PANEL_COLOR};
        border-radius: 6px;
        margin: 1px;
        padding: 4px;
    }}
    
    QLineEdit#skill_input {{
        background-color: {PANEL_COLOR};
        border: 1px solid #444;
        border-radius: 4px;
        padding: 4px;
    }}
    
    QPushButton#skill_delete {{
        background-color: {DANGER_COLOR};
        color: white;
        border: none;
        border-radius: 3px;
        padding: 3px 6px;
        font-weight: bold;
        font-size: 12px;
    }}
"""