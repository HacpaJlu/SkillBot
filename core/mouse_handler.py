import pyautogui
import math
from typing import Tuple


class MouseHandler:
    """Класс для обработки мышиных действий, таких как клики по координатам."""
    
    def __init__(self):
        # Убедимся, что pyautogui настроен безопасно
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01  # Небольшая задержка между действиями
    
    def click_at_coordinates(self, x: int, y: int, button: str = 'left') -> bool:
        """
        Выполняет клик по указанным координатам.
        
        Args:
            x (int): Координата X
            y (int): Координата Y
            button (str): Кнопка мыши ('left', 'right', 'middle')
            
        Returns:
            bool: True если клик был успешно выполнен, иначе False
        """
        try:
            # Проверяем, что координаты в пределах экрана
            screen_width, screen_height = pyautogui.size()
            if 0 <= x <= screen_width and 0 <= y <= screen_height:
                pyautogui.click(x, y, button=button)
                return True
            else:
                print(f"Координаты ({x}, {y}) вне пределов экрана ({screen_width}x{screen_height})")
                return False
        except Exception as e:
            print(f"Ошибка при клике по координатам ({x}, {y}): {e}")
            return False
    
    def click_aoe_at_coordinates(self, center_x: int, center_y: int, radius: int = 50, button: str = 'left') -> bool:
        """
        Выполняет AOE (Area of Effect) клик вокруг указанных координат.
        Кликает в центр и в несколько точек по кругу для AOE эффекта.
        
        Args:
            center_x (int): Центральная координата X
            center_y (int): Центральная координата Y
            radius (int): Радиус области AOE
            button (str): Кнопка мыши ('left', 'right', 'middle')
            
        Returns:
            bool: True если клики были успешно выполнены, иначе False
        """
        try:
            # Кликаем в центр
            if not self.click_at_coordinates(center_x, center_y, button):
                return False
            
            # Кликаем в точки по кругу для AOE эффекта
            num_points = 6  # Количество точек по кругу
            for i in range(num_points):
                angle = 2 * math.pi * i / num_points
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                
                # Проверяем, что координаты в пределах экрана
                screen_width, screen_height = pyautogui.size()
                if 0 <= x <= screen_width and 0 <= y <= screen_height:
                    pyautogui.click(x, y, button=button)
            
            return True
        except Exception as e:
            print(f"Ошибка при AOE клике: {e}")
            return False
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """
        Возвращает текущую позицию мыши.
        
        Returns:
            Tuple[int, int]: Координаты (x, y) мыши
        """
        return pyautogui.position()
    
    def move_mouse_to(self, x: int, y: int) -> bool:
        """
        Перемещает мышь к указанным координатам.
        
        Args:
            x (int): Координата X
            y (int): Координата Y
            
        Returns:
            bool: True если перемещение было успешно, иначе False
        """
        try:
            screen_width, screen_height = pyautogui.size()
            if 0 <= x <= screen_width and 0 <= y <= screen_height:
                pyautogui.moveTo(x, y)
                return True
            else:
                print(f"Координаты ({x}, {y}) вне пределов экрана ({screen_width}x{screen_height})")
                return False
        except Exception as e:
            print(f"Ошибка при перемещении мыши к ({x}, {y}): {e}")
            return False