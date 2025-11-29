"""
Responsive styles for SkillBot application
This module contains responsive and adaptive styles
"""

def get_responsive_style():
    """
    Возвращает стили, адаптированные для разных размеров экрана
    """
    return """
    /* Адаптивные стили для различных размеров экрана */
    
    /* Для больших экранов */
    QMainWindow[screen="large"] QLabel#status_label {
        font-size: 36px;
    }
     
    QMainWindow[screen="large"] QLabel#casting_label {
        font-size: 24px;
    }
     
    QMainWindow[screen="large"] QLabel#urgent_label {
        font-size: 22px;
    }
     
    QMainWindow[screen="large"] QLabel#queue_label {
        font-size: 18px;
    }
     
    QMainWindow[screen="large"] QLabel#autopot_status_label {
        font-size: 18px;
    }
     
    /* Для средних экранов */
    QMainWindow[screen="medium"] QLabel#status_label {
        font-size: 30px;
    }
     
    QMainWindow[screen="medium"] QLabel#casting_label {
        font-size: 20px;
    }
     
    QMainWindow[screen="medium"] QLabel#urgent_label {
        font-size: 18px;
    }
     
    QMainWindow[screen="medium"] QLabel#queue_label {
        font-size: 14px;
    }
     
    QMainWindow[screen="medium"] QLabel#autopot_status_label {
        font-size: 14px;
    }
     
    /* Для маленьких экранов */
    QMainWindow[screen="small"] QLabel#status_label {
        font-size: 28px;
    }
     
    QMainWindow[screen="small"] QLabel#casting_label {
        font-size: 18px;
    }
     
    QMainWindow[screen="small"] QLabel#urgent_label {
        font-size: 16px;
    }
     
    QMainWindow[screen="small"] QLabel#queue_label {
        font-size: 14px;
    }
     
    QMainWindow[screen="small"] QLabel#autopot_status_label {
        font-size: 14px;
    }
     
    QMainWindow[screen="small"] QPushButton {
        padding: 4px 8px;
        font-size: 11px;
        min-height: 24px;
    }
     
    QMainWindow[screen="small"] QLineEdit, QMainWindow[screen="small"] QComboBox {
        padding: 4px 6px;
        font-size: 11px;
        min-height: 24px;
    }
     
    QMainWindow[screen="small"] QTabBar::tab {
        padding: 4px 8px;
        font-size: 11px;
        min-width: 50px;
    }
     
    /* Адаптивные стили прокрутки */
    QMainWindow[screen="small"] QScrollArea {
        min-height: 120px;
    }
    """