# main.py
import sys
import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.styles import apply_modern_style

if __name__ == "__main__":
    try:
        print("DEBUG: Starting application...")
        # Note: qRegisterMetaType is not available in some PyQt builds.
        # GUI updates from background threads are scheduled on the Qt main
        # thread (via QTimer.singleShot) elsewhere in the code to avoid
        # queued-argument warnings for complex Qt types.
        # HighDPI scaling is enabled by default in PyQt6, no need to set it explicitly
        # For PyQt5 compatibility, we could set AA_EnableHighDpiScaling, but it's not necessary
        # since PyQt6 handles this automatically
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        
        # Set application icon for taskbar
        from PyQt6.QtGui import QIcon
        app_icon = QIcon("icon.png")
        app.setWindowIcon(app_icon)
        
        print("DEBUG: Creating MainWindow...")
        win = MainWindow()
        # Применяем современные стили к главному окну
        apply_modern_style(win)
        print("DEBUG: Showing window...")
        win.show()
        print("DEBUG: Application started successfully, entering event loop...")
        sys.exit(app.exec())
    except Exception as e:
        print(f"DEBUG: Exception occurred: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")
