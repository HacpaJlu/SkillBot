import importlib, traceback, sys, os
# Ensure project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

modules = ['core.bot','core.autopot','ui.tabs.settings_tab','ui.widgets.click_overlay','ui.main_window']
for m in modules:
    try:
        importlib.import_module(m)
        print(f'IMPORTED: {m}')
    except Exception as e:
        print(f'ERROR importing {m}: {e}')
        traceback.print_exc()
