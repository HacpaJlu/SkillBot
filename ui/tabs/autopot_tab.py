# AutopotTab — Import from core.autopot (actual implementation)
# Re-export classes so that ui.main_window and other modules can import from here
from core.autopot import AutopotTab, AutopotThread
from ui.widgets.roi_overlay import ROIOverlay

__all__ = ['AutopotTab', 'AutopotThread']

