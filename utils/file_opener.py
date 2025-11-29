# file_opener.py — вспомогательные функции для открытия файлов
import os
import webbrowser
import subprocess
import platform
from PyQt6.QtWidgets import QMessageBox


def open_file(file_path):
    """
    Открывает указанный файл в системном редакторе по умолчанию
    """
    try:
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            return False
            
        system = platform.system()
        try:
            if system == "Windows":
                os.startfile(abs_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", abs_path])
            else:  # Linux и другие Unix-подобные системы
                subprocess.run(["xdg-open", abs_path])
            return True
        except Exception:
            # Если стандартные методы не работают, пробуем через webbrowser
            webbrowser.open(f"file://{abs_path}")
            return True
    except Exception as e:
        print(f"Ошибка при открытии файла {file_path}: {e}")
        return False