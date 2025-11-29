# bot.py — финальная 100% рабочая версия
import threading
# (No changes, but ensure signals are accessible for overlay)
import time
import random

import keyboard
import win32gui
from PyQt6.QtCore import QThread, pyqtSignal


class SkillBot(QThread):
    update_signal = pyqtSignal(str, dict, str, str, str)
    # Existing signals are sufficient; overlay will connect to update_signal
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.skills = []
        self.enabled = False
        self.running = True
        self.target_window = ""
        self.debug = False

        self.pause_on_input = False
        self.last_user_input = 0
        # Duration (seconds) to consider recent user input for pausing the bot
        # Default 1.0 second; can be updated from UI settings
        self.pause_duration = 1.0
        self._user_input_hook = None
        self._pressing_keys = set()
        self.state_lock = threading.Lock()

        self.current_cast = None
        self.cast_end_time = 0
        self.queue = []

    def log(self, text):
        if self.debug:
            self.log_signal.emit(f"[{time.strftime('%H:%M:%S')}] {text}")
    
    def press_skill(self, key):
        """Нажатие клавиши с рандомизированной задержкой для имитации реального пользователя"""
        # Задержка перед нажатием (0.1-0.3 секунды)
        time.sleep(random.uniform(0.1, 0.3))
        keyboard.press_and_release(key)
        # Небольшая задержка после нажатия для более реалистичного поведения
        time.sleep(random.uniform(0.05, 0.15))
    
    def update_skills_count_log(self):
        """Обновляет сообщение о количестве скиллов в логе"""
        if self.debug:
            self.log_signal.emit(f"[{time.strftime('%H:%M:%S')}] Количество скиллов: {len(self.skills)} (после загрузки профиля)")
    

    def setup_user_input_hook(self):
        if self._user_input_hook:
            try:
                keyboard.unhook(self._user_input_hook)
            except Exception as e:
                if self.debug:
                    self.log_signal.emit(f"Ошибка: {e}")

        def on_press(key):
            try:
                key_name = (
                    key.name.lower() if hasattr(key, "name") else str(key).lower()
                )
            except Exception as e:
                if self.debug:
                    self.log_signal.emit(f"Ошибка получения имени клавиши: {e}")
                key_name = "unknown"

            # ← НОВОЕ ПОВЕДЕНИЕ:
            # 1. Если бот ВЫКЛЮЧЕН — вообще не реагируем на ввод (и не спамим в лог!)
            # 2. Если бот ВКЛЮЧЕН и пауза включена — только тогда сбрасываем очередь
            if not self.enabled:
                return True  # просто пропускаем, ничего не делаем и не пишем в лог

            if self.pause_on_input:
                self.last_user_input = time.time()
                if self.queue:
                    self.queue.clear()
                    self.log(f"Очередь сброшена из-за ввода пользователя (очередь содержала {len(self.queue)} скиллов)")
            return True

        self._user_input_hook = keyboard.on_press(on_press)

    def run(self):
        from core import __version__
        self.log(f"=== Skill Bot v{__version__} запущен ===")
        self.log(f"Целевое окно: {self.target_window if self.target_window else 'не задано'}")
        # self.log(f"Количество скиллов: {len(self.skills)} (обновится после загрузки профиля)")
        self.log(f"Состояние бота: {'включен' if self.enabled else 'выключен'}")
        self.setup_user_input_hook()

        while True:
            with self.state_lock:
                if not self.running:
                    break
            time.sleep(0.01)
            t = time.time()

            # Проверка активного окна
            if self.target_window:
                try:
                    fg = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                    if self.target_window.lower() not in fg.lower():
                        # Окно неактивно, пропускаем действия
                        if self.debug:
                            self.log(f"Окно неактивно: '{fg}' (ожидалось: '{self.target_window}')")
                        status = "ОКНО НЕАКТИВНО"
                        cooldowns = {}
                        for s in self.skills:
                            cd_left = max(0.0, s["last_used"] + s["cooldown"] - t)
                            cooldowns[s["key"].upper()] = cd_left
                        casting_info = (
                            f"Кастую {self.current_cast['key'].upper()}..."
                            if self.current_cast
                            else ""
                        )
                        queue_info = (
                            " → ".join([s["key"].upper() for s in self.queue])
                            if self.queue
                            else "Очередь пуста"
                        )
                        urgent_skill = ""
                        self.update_signal.emit(
                            status, cooldowns, casting_info, queue_info, urgent_skill
                        )
                        time.sleep(0.1)
                        continue
                except Exception as e:
                    if self.debug:
                        self.log_signal.emit(f"Ошибка проверки окна: {e}")

            # Кулдауны
            cooldowns = {}
            for s in self.skills:
                cd_left = max(0.0, s["last_used"] + s["cooldown"] - t)
                cooldowns[s["key"].upper()] = cd_left

            # Завершение каста
            if self.current_cast and t >= self.cast_end_time:
                self.current_cast = None

            casting_info = (
                f"Кастую {self.current_cast['key'].upper()}..."
                if self.current_cast
                else ""
            )
            queue_info = (
                " → ".join([s["key"].upper() for s in self.queue])
                if self.queue
                else "Очередь пуста"
            )
            urgent_skill = ""

            status = "РАБОТАЕТ" if self.enabled else "ОЖИДАНИЕ..."

            # ПОЛНАЯ ПАУЗА ПРИ ДВИЖЕНИИ — учитываем настраиваемую длительность
            if self.pause_on_input and (t - self.last_user_input < getattr(self, 'pause_duration', 1.0)):
                status = "ПАУЗА (ввод)"
                if self.debug:
                    self.log(f"Пауза из-за ввода пользователя (осталось: {(getattr(self, 'pause_duration', 1.0) - (t - self.last_user_input)):.1f}с)")
                self.update_signal.emit(
                    status, cooldowns, casting_info, queue_info, urgent_skill
                )
                continue  # ← ничего не нажимаем

            # Основная логика только если нет ввода пользователя
            if self.enabled and not self.current_cast:
                # Срочные скиллы (>10)
                urgent = [
                    s
                    for s in self.skills
                    if s["priority"] > 10 and cooldowns[s["key"].upper()] <= 0.05
                ]
                if urgent:
                    skill = max(urgent, key=lambda x: x["priority"])
                    self.current_cast = skill
                    self.cast_end_time = t + skill["cast_time"]
                    skill["last_used"] = t
                    self.press_skill(skill["key"])
                    self.log(f"СРОЧНО → {skill['key'].upper()} (приоритет: {skill['priority']}, кулдаун: {skill['cooldown']}, каст: {skill['cast_time']})")
                    urgent_skill = skill["key"].upper() + "!"
                else:
                    # Обычные скиллы
                    ready = [
                        s
                        for s in self.skills
                        if s["priority"] <= 10 and cooldowns[s["key"].upper()] <= 0.05
                    ]
                    if ready and not self.queue:
                        ready.sort(key=lambda x: x["priority"], reverse=True)
                        self.queue = ready.copy()
                        if self.debug:
                            self.log(f"Формирование очереди: {len(ready)} доступных скилов отсортировано по приоритету")

                    if self.queue:
                        skill = self.queue.pop(0)
                        self.current_cast = skill
                        self.cast_end_time = t + skill["cast_time"]
                        skill["last_used"] = t
                        self.press_skill(skill["key"])
                        self.log(f"→ {skill['key'].upper()} (приоритет: {skill['priority']}, кулдаун: {skill['cooldown']}, каст: {skill['cast_time']})")
                        if self.debug and self.queue:
                            self.log(f"Очередь: {len(self.queue)} скиллов осталось после выполнения {skill['key'].upper()}")

            self.update_signal.emit(
                status, cooldowns, casting_info, queue_info, urgent_skill
            )

    def quit(self):
        self.running = False
        if self._user_input_hook:
            try:
                keyboard.unhook(self._user_input_hook)
            except Exception as e:
                if self.debug:
                    self.log_signal.emit(f"Ошибка: {e}")
