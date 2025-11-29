# Code Index

Repository root: `c:\Users\Admin\Documents\skillbot\SkillBot`

_Automatically generated. Click file links to open in VSCode._

## `__version__.py`
- Path: [__version__.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\__version__.py:1)
- Variables: __version__ (L2), __author__ (L3), __date__ (L4)

## `config/__init__.py`
- Path: [config/__init__.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\config\__init__.py:1)
- Doc: Config package.

## `core/__init__.py`
- Path: [core/__init__.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\core\__init__.py:1)
- Doc: Core package for SkillBot.

Central constants for the application (name and version) live here so
the UI, README and other modules can reference a single source of truth.
- Variables: APP_NAME (L8), __version__ (L9), __all__ (L11)

## `core/autopot.py`
- Path: [core/autopot.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\core\autopot.py:21)
- Imports: `PyQt6.QtCore.QLocale, PyQt6.QtCore.QThread, PyQt6.QtCore.QTimer, PyQt6.QtCore.Qt, PyQt6.QtCore.pyqtSignal, PyQt6.QtGui.QDoubleValidator, PyQt6.QtGui.QIntValidator, PyQt6.QtWidgets.QGridLayout, PyQt6.QtWidgets.QHBoxLayout, PyQt6.QtWidgets.QLabel, PyQt6.QtWidgets.QLineEdit, PyQt6.QtWidgets.QPushButton, PyQt6.QtWidgets.QVBoxLayout, PyQt6.QtWidgets.QWidget, keyboard, mss.mss, numpy, pynput.keyboard.Controller, pynput.mouse, threading, time, utils.KeyCaptureButton, win32gui`
- Classes:
  - [AutopotThread (L21)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\core\autopot.py:21)
  - [AutopotTab (L106)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\core\autopot.py:106)

## `core/bot.py`
- Path: [core/bot.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\core\bot.py:11)
- Imports: `PyQt6.QtCore.QThread, PyQt6.QtCore.pyqtSignal, keyboard, threading, time, win32gui`
- Classes:
  - [SkillBot (L11)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\core\bot.py:11)

## `core/keyboard_handler.py`
- Path: [core/keyboard_handler.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\core\keyboard_handler.py:3)
- Doc: Placeholder for keyboard handler (to be implemented later).
- Functions:
  - [register_hotkeys (L3)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\core\keyboard_handler.py:3)

## `main.py`
- Path: [main.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\main.py:1)
- Imports: `PyQt6.QtCore.Qt, PyQt6.QtWidgets.QApplication, sys, traceback, ui.main_window.MainWindow, ui.styles.apply_modern_style`

## `models/__init__.py`
- Path: [models/__init__.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\models\__init__.py:1)
- Doc: Models package for SkillBot.

## `models/profile.py`
- Path: [models/profile.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\models\profile.py:3)
- Doc: Simple profile model (placeholder).
- Classes:
  - [Profile (L3)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\models\profile.py:3)

## `models/skill.py`
- Path: [models/skill.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\models\skill.py:3)
- Doc: Simple skill model (placeholder).
- Classes:
  - [Skill (L3)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\models\skill.py:3)

## `scripts/build_index.py`
- Path: [scripts/build_index.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\scripts\build_index.py:18)
- Doc: Build a code index (JSON + Markdown) for the repository.

Usage:
  python scripts/build_index.py [--root PATH] [--out-json PATH] [--out-md PATH]

Produces `code_index.json` and `CODE_INDEX.md` by def…
- Imports: `argparse.ArgumentParser, ast, json, os, sys`
- Functions:
  - [is_simple_value (L18)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\scripts\build_index.py:18)
  - [short (L22)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\scripts\build_index.py:22)
  - [get_params (L30)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\scripts\build_index.py:30): Return a list of parameter descriptors for a FunctionDef node.
  - [parse_file (L56)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\scripts\build_index.py:56)
  - [build_index (L121)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\scripts\build_index.py:121)
  - [make_markdown (L147)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\scripts\build_index.py:147)
  - [main (L189)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\scripts\build_index.py:189)

## `scripts/import_check.py`
- Path: [scripts/import_check.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\scripts\import_check.py:1)
- Imports: `importlib, os, sys, traceback`
- Variables: modules (L7)

## `scripts/prune_root.py`
- Path: [scripts/prune_root.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\scripts\prune_root.py:1)
- Doc: Prune root files script

Usage:
  - Review the script, then run in project root (PowerShell):
      python .\scripts\prune_root.py

Behavior:
  - Creates/uses `archive/root_backup/` to store copies o…
- Imports: `os, pathlib.Path, shutil`
- Variables: WHITELIST (L22), archived (L46), deleted (L47), errors (L48)

## `ui/__init__.py`
- Path: [ui/__init__.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\__init__.py:1)
- Doc: UI package for SkillBot (auto-created).

## `ui/main_window.py`
- Path: [ui/main_window.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\main_window.py:29)
- Imports: `PyQt6.QtCore.QCoreApplication, PyQt6.QtCore.QEvent, PyQt6.QtCore.QTimer, PyQt6.QtGui.QIcon, PyQt6.QtWidgets.QApplication, PyQt6.QtWidgets.QInputDialog, PyQt6.QtWidgets.QLabel, PyQt6.QtWidgets.QLineEdit, PyQt6.QtWidgets.QMainWindow, PyQt6.QtWidgets.QMessageBox, PyQt6.QtWidgets.QSizePolicy, PyQt6.QtWidgets.QSystemTrayIcon, PyQt6.QtWidgets.QTabWidget, PyQt6.QtWidgets.QTextEdit, core.APP_NAME, core.__version__, core.autopot.AutopotTab, core.bot.SkillBot, json, keyboard, os, ui.tabs.help_tab.HelpTab, ui.tabs.main_tab.MainTab, ui.tabs.overlay_tab.OverlayTab, ui.tabs.settings_tab.SettingsTab, ui.widgets.overlay_window.OverlayWindow, warnings`
- Variables: PROFILES_DIR (L22), CONFIG_DIR (L23)
- Classes:
  - [MainWindow (L29)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\main_window.py:29)

## `ui/style_modules/__init__.py`
- Path: [ui/style_modules/__init__.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\style_modules\__init__.py:1)
- Doc: Style modules package for SkillBot application
This package contains modularized styles for better maintainability

## `ui/style_modules/base.py`
- Path: [ui/style_modules/base.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\style_modules\base.py:1)
- Doc: Base styles for SkillBot application
This module contains basic component styles (buttons, checkboxes, inputs, etc.)
- Imports: `colors.*`

## `ui/style_modules/colors.py`
- Path: [ui/style_modules/colors.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\style_modules\colors.py:1)
- Doc: Color definitions for SkillBot application
This module contains color variables used throughout the application
- Variables: PRIMARY_COLOR (L7), SECONDARY_COLOR (L8), BACKGROUND_COLOR (L9), PANEL_COLOR (L10), HIGHLIGHT_COLOR (L11), SUCCESS_COLOR (L12), WARNING_COLOR (L13), DANGER_COLOR (L14), TEXT_COLOR (L17), TEXT_SECONDARY (L18), TEXT_DISABLED (L19)

## `ui/style_modules/components.py`
- Path: [ui/style_modules/components.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\style_modules\components.py:1)
- Doc: Component-specific styles for SkillBot application
This module contains styles for specific UI components (skills, autopot, etc.)
- Imports: `colors.*`

## `ui/style_modules/responsive.py`
- Path: [ui/style_modules/responsive.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\style_modules\responsive.py:6)
- Doc: Responsive styles for SkillBot application
This module contains responsive and adaptive styles
- Functions:
  - [get_responsive_style (L6)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\style_modules\responsive.py:6): Возвращает стили, адаптированные для разных размеров экрана

## `ui/style_modules/window.py`
- Path: [ui/style_modules/window.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\style_modules\window.py:1)
- Doc: Window and tab styles for SkillBot application
This module contains styles for main window and tabs
- Imports: `colors.*`

## `ui/styles.py`
- Path: [ui/styles.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\styles.py:25)
- Doc: Modern CSS-like styles for SkillBot application
This module contains QSS (Qt Style Sheets) styles for modern UI design
- Imports: `style_modules.base.BUTTON_STYLES, style_modules.base.CHECKBOX_STYLES, style_modules.base.INPUT_STYLES, style_modules.base.SCROLLBAR_STYLES, style_modules.colors.*, style_modules.components.MAIN_TAB_STYLES, style_modules.components.SETTINGS_TAB_STYLES, style_modules.components.SKILL_ITEM_STYLES, style_modules.responsive.get_responsive_style, style_modules.window.MAIN_WINDOW_STYLE`
- Functions:
  - [get_modern_style (L25)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\styles.py:25): Возвращает комбинированный современный стиль для приложения
  - [apply_modern_style (L32)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\styles.py:32): Применяет современный стиль к виджету

## `ui/tabs/__init__.py`
- Path: [ui/tabs/__init__.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\tabs\__init__.py:1)
- Doc: UI tabs package.

## `ui/tabs/autopot_tab.py`
- Path: [ui/tabs/autopot_tab.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\tabs\autopot_tab.py:1)
- Imports: `core.autopot.AutopotTab, core.autopot.AutopotThread`
- Variables: __all__ (L5)

## `ui/tabs/help_tab.py`
- Path: [ui/tabs/help_tab.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\tabs\help_tab.py:7)
- Imports: `PyQt6.QtWidgets.QTextEdit, os`
- Classes:
  - [HelpTab (L7)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\tabs\help_tab.py:7)

## `ui/tabs/main_tab.py`
- Path: [ui/tabs/main_tab.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\tabs\main_tab.py:8)
- Imports: `PyQt6.QtCore.Qt, PyQt6.QtWidgets.QLabel, PyQt6.QtWidgets.QScrollArea, PyQt6.QtWidgets.QSizePolicy, PyQt6.QtWidgets.QVBoxLayout, PyQt6.QtWidgets.QWidget`
- Classes:
  - [MainTab (L8)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\tabs\main_tab.py:8)

## `ui/tabs/overlay_tab.py`
- Path: [ui/tabs/overlay_tab.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\tabs\overlay_tab.py:9)
- Imports: `PyQt6.QtCore.Qt, PyQt6.QtGui.QColor, PyQt6.QtWidgets.QCheckBox, PyQt6.QtWidgets.QColorDialog, PyQt6.QtWidgets.QFormLayout, PyQt6.QtWidgets.QPushButton, PyQt6.QtWidgets.QSizePolicy, PyQt6.QtWidgets.QVBoxLayout, PyQt6.QtWidgets.QWidget`
- Classes:
  - [OverlayTab (L9)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\tabs\overlay_tab.py:9)

## `ui/tabs/settings_tab.py`
- Path: [ui/tabs/settings_tab.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\tabs\settings_tab.py:15)
- Imports: `PyQt6.QtCore.QLocale, PyQt6.QtCore.Qt, PyQt6.QtCore.pyqtSignal, PyQt6.QtGui.QAction, PyQt6.QtGui.QBrush, PyQt6.QtGui.QConicalGradient, PyQt6.QtGui.QCursor, PyQt6.QtGui.QDoubleValidator, PyQt6.QtGui.QFont, PyQt6.QtGui.QIcon, PyQt6.QtGui.QIntValidator, PyQt6.QtGui.QKeySequence, PyQt6.QtGui.QLinearGradient, PyQt6.QtGui.QMovie, PyQt6.QtGui.QPainter, PyQt6.QtGui.QPalette, PyQt6.QtGui.QPen, PyQt6.QtGui.QPicture, PyQt6.QtGui.QPixmap, PyQt6.QtGui.QPolygon, PyQt6.QtGui.QRadialGradient, PyQt6.QtGui.QRegion, PyQt6.QtGui.QRegularExpressionValidator, PyQt6.QtGui.QTransform, PyQt6.QtGui.QValidator, PyQt6.QtWidgets.QApplication, PyQt6.QtWidgets.QCheckBox, PyQt6.QtWidgets.QComboBox, PyQt6.QtWidgets.QDialog, PyQt6.QtWidgets.QFormLayout, PyQt6.QtWidgets.QHBoxLayout, PyQt6.QtWidgets.QInputDialog, PyQt6.QtWidgets.QLabel, PyQt6.QtWidgets.QLineEdit, PyQt6.QtWidgets.QPushButton, PyQt6.QtWidgets.QScrollArea, PyQt6.QtWidgets.QSizePolicy, PyQt6.QtWidgets.QSpinBox, PyQt6.QtWidgets.QTabWidget, PyQt6.QtWidgets.QVBoxLayout, PyQt6.QtWidgets.QWidget, os, psutil, utils.KeyCaptureButton, utils.SelectAllLineEdit, win32gui, win32process`
- Classes:
  - [SettingsTab (L15)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\tabs\settings_tab.py:15)

## `ui/widgets/__init__.py`
- Path: [ui/widgets/__init__.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\widgets\__init__.py:1)
- Doc: UI widgets package.

## `ui/widgets/click_overlay.py`
- Path: [ui/widgets/click_overlay.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\widgets\click_overlay.py:6)
- Imports: `PyQt6.QtCore.QRect, PyQt6.QtCore.Qt, PyQt6.QtCore.pyqtSignal, PyQt6.QtGui.QColor, PyQt6.QtGui.QFont, PyQt6.QtGui.QPainter, PyQt6.QtWidgets.QApplication, PyQt6.QtWidgets.QLabel, PyQt6.QtWidgets.QWidget`
- Classes:
  - [ClickOverlay (L6)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\widgets\click_overlay.py:6)
  - [WindowSelectOverlay (L87)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\widgets\click_overlay.py:87)

## `ui/widgets/key_capture_button.py`
- Path: [ui/widgets/key_capture_button.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\widgets\key_capture_button.py:6)
- Imports: `PyQt6.QtCore.QTimer, PyQt6.QtCore.Qt, PyQt6.QtCore.pyqtSignal, PyQt6.QtWidgets.QPushButton, keyboard`
- Classes:
  - [KeyCaptureButton (L6)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\widgets\key_capture_button.py:6)

## `ui/widgets/overlay_window.py`
- Path: [ui/widgets/overlay_window.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\widgets\overlay_window.py:5)
- Imports: `PyQt6.QtCore.QPoint, PyQt6.QtCore.QSize, PyQt6.QtCore.Qt, PyQt6.QtCore.pyqtSignal, PyQt6.QtGui.QColor, PyQt6.QtGui.QFont, PyQt6.QtGui.QPainter, PyQt6.QtGui.QPainterPath, PyQt6.QtWidgets.QCheckBox, PyQt6.QtWidgets.QColorDialog, PyQt6.QtWidgets.QFormLayout, PyQt6.QtWidgets.QLabel, PyQt6.QtWidgets.QPushButton, PyQt6.QtWidgets.QVBoxLayout, PyQt6.QtWidgets.QWidget`
- Classes:
  - [OverlayWindow (L5)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\widgets\overlay_window.py:5)

## `ui/widgets/select_all_lineedit.py`
- Path: [ui/widgets/select_all_lineedit.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\widgets\select_all_lineedit.py:5)
- Imports: `PyQt6.QtCore.QTimer, PyQt6.QtWidgets.QLineEdit`
- Classes:
  - [SelectAllLineEdit (L5)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\ui\widgets\select_all_lineedit.py:5)

## `utils/__init__.py`
- Path: [utils/__init__.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\utils\__init__.py:12)
- Imports: `PyQt6.QtCore.QTimer, PyQt6.QtCore.Qt, PyQt6.QtCore.pyqtSignal, PyQt6.QtWidgets.QLineEdit, PyQt6.QtWidgets.QPushButton, keyboard`
- Classes:
  - [KeyCaptureButton (L12)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\utils\__init__.py:12)
  - [SelectAllLineEdit (L127)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\utils\__init__.py:127)

## `utils/json_helper.py`
- Path: [utils/json_helper.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\utils\json_helper.py:3)
- Imports: `json`
- Functions:
  - [load_json (L3)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\utils\json_helper.py:3)
  - [save_json (L10)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\utils\json_helper.py:10)

## `utils/logger.py`
- Path: [utils/logger.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\utils\logger.py:3)
- Imports: `sys`
- Functions:
  - [log (L3)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\utils\logger.py:3)

## `utils/profile_manager.py`
- Path: [utils/profile_manager.py](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\utils\profile_manager.py:6)
- Imports: `json_helper.load_json, json_helper.save_json, os`
- Functions:
  - [list_profiles (L6)](vscode://file/c:\Users\Admin\Documents\skillbot\SkillBot\utils\profile_manager.py:6)

---
Generated by `scripts/build_index.py`.