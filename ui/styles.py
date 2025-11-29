"""
Modern CSS-like styles for SkillBot application
This module contains QSS (Qt Style Sheets) styles for modern UI design
"""
from .style_modules.window import MAIN_WINDOW_STYLE
from .style_modules.base import BUTTON_STYLES, CHECKBOX_STYLES, INPUT_STYLES, SCROLLBAR_STYLES
from .style_modules.components import MAIN_TAB_STYLES, SETTINGS_TAB_STYLES, SKILL_ITEM_STYLES
from .style_modules.responsive import get_responsive_style
from .style_modules.colors import *

# Комбинированный стиль
COMBINED_STYLE = f"""
{MAIN_WINDOW_STYLE}
{BUTTON_STYLES}
{CHECKBOX_STYLES}
{INPUT_STYLES}
{SCROLLBAR_STYLES}
{MAIN_TAB_STYLES}
{SETTINGS_TAB_STYLES}
{SKILL_ITEM_STYLES}
/* Анимации - не поддерживаются в QSS */
"""


def get_modern_style():
    """
    Возвращает комбинированный современный стиль для приложения
    """
    return COMBINED_STYLE


def apply_modern_style(widget):
    """
    Применяет современный стиль к виджету
    """
    # Определяем размер экрана для адаптивности
    screen_size = "large"
    if widget.width() < 1000:
        screen_size = "medium"
    if widget.width() < 768:
        screen_size = "small"
    
    widget.setProperty("screen", screen_size)
    try:
        style = widget.style()
        if style:
            style.unpolish(widget)
            style.polish(widget)
    except:
        pass  # Игнорируем ошибки стиля
    
    widget.setStyleSheet(get_modern_style() + get_responsive_style())