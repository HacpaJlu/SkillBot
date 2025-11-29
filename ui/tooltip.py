"""
Tooltip component for SkillBot UI
"""
import time
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, QEvent
from PyQt6.QtGui import QFont



class TooltipWidget(QWidget):
    """
    Виджет всплывающей подсказки
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Используем правильные флаги окна для PyQt6
        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Устанавливаем атрибут, чтобы подсказка не перехватывала события мыши
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        # Убираем любые стандартные подсказки у самого виджета подсказки
        self.setToolTip("")
        
        # Создаем метку для текста подсказки
        self.label = QLabel(self)
        # Используем правильные флаги выравнивания для PyQt6
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.label.setWordWrap(True)
        
        # Применяем стили
        self._apply_styles()
        
        self.text = ""
        self.max_width = 300
        
        # Создаем анимации для прозрачности и масштаба
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(300)  # 300мс длительность (в диапазоне 300-500мс)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)  # easing кривая
        
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(300)  # 300мс длительность (в диапазоне 300-500мс)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)  # easing кривая

    def _apply_styles(self):
        """Применение стилей к подсказке"""
        # Используем цвета из модуля стилей
        try:
            from ui.style_modules.colors import BACKGROUND_COLOR, TEXT_COLOR, PANEL_COLOR
            # Создаем стиль подсказки с использованием цветов из темы
            style = f"""
                QWidget {{
                    background-color: {PANEL_COLOR};
                    color: {TEXT_COLOR};
                    border: 1px solid rgba(68, 68, 68, 0.267);
                    border-radius: 6px;
                    padding: 8px;
                    font-size: 10px;
                }}
            """
            self.setStyleSheet(style)
        except ImportError:
            # Если стили недоступны, используем базовые стили
            self.setStyleSheet("""
                QWidget {
                    background-color: rgba(45, 45, 45, 0.2);
                    color: #ffffff;
                    border: 1px solid rgba(68, 68, 68, 0.267);
                    border-radius: 6px;
                    padding: 8px;
                    font-size: 10px;
                }
            """)
        
        # Настраиваем шрифт
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        
    def set_text(self, text):
        """Установка текста подсказки"""
        self.text = text
        self.label.setText(text)
        
        # Ограничиваем ширину и переносим текст
        self.label.setFixedWidth(min(self.max_width, self.label.sizeHint().width()))
        self.label.resize(self.label.sizeHint())
        
        # Обновляем размеры виджета
        label_size = self.label.size()
        margin = 8  # значение отступа
        self.resize(label_size.width() + margin * 2, label_size.height() + margin * 2)
        
    def show_at(self, pos, screen_rect=None):
        """Отображение подсказки в заданной позиции"""
        if screen_rect is None:
            # Получаем доступную область экрана
            # В PyQt6 QDesktopWidget больше не доступен, используем QGuiApplication.screens()
            from PyQt6.QtGui import QGuiApplication
            from typing import cast
            app = QGuiApplication.instance()
            if app is not None:
                # Приведение к QGuiApplication для доступа к методам экрана
                gui_app = cast(QGuiApplication, app)
                # Находим экран, на котором находится позиция
                screens = gui_app.screens()
                screen = None
                for s in screens:
                    if s.geometry().contains(pos):
                        screen = s
                        break
                
                if screen is not None:
                    screen_rect = screen.availableGeometry()
                else:
                    # Если не удается найти конкретный экран, используем основной экран
                    primary_screen = gui_app.primaryScreen()
                    if primary_screen:
                        screen_rect = primary_screen.availableGeometry()
                    else:
                        # Резервный вариант: используем размеры по умолчанию
                        from PyQt6.QtCore import QRect
                        screen_rect = QRect(0, 0, 1920, 1080)  # стандартный размер экрана
            else:
                # Если не удается получить информацию об экране, используем стандартные значения
                from PyQt6.QtCore import QRect
                screen_rect = QRect(0, 0, 1920, 1080)  # стандартный размер экрана
        
        # Смещаем позицию подсказки чуть ниже курсора, чтобы избежать конфликта с событиями мыши
        adjusted_pos = QPoint(pos.x(), pos.y() + 20)
        
        # Определяем оптимальное положение
        tooltip_pos = self._calculate_position(adjusted_pos, screen_rect)
        self.move(tooltip_pos)
        
        # Устанавливаем начальное состояние для анимации (прозрачность и масштаб)
        self.setWindowOpacity(0)
        original_geometry = self.geometry()
        # Уменьшаем размеры для анимации появления (эффект масштабирования)
        scaled_geometry = original_geometry.adjusted(
            original_geometry.width() // 4,  # уменьшаем на 25% от ширины
            original_geometry.height() // 4,  # уменьшаем на 25% от высоты
            -original_geometry.width() // 4,  # уменьшаем на 25% от ширины
            -original_geometry.height() // 4  # уменьшаем на 25% от высоты
        )
        self.setGeometry(scaled_geometry)
        self.show()
        
        # Запускаем анимации появления
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.setDuration(400)  # 400мс длительность (в диапазоне 300-500мс)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)  # easing кривая
        self.opacity_animation.start()
        
        self.scale_animation.setStartValue(scaled_geometry)
        self.scale_animation.setEndValue(original_geometry)
        self.scale_animation.setDuration(400)  # 400мс длительность (в диапазоне 300-500мс)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)  # easing кривая
        self.scale_animation.start()

    def _calculate_position(self, pos, screen_rect):
        """Расчет оптимальной позиции подсказки с учетом границ экрана"""
        tooltip_size = self.size()
        
        # Рассчитываем доступные пространства в каждом направлении
        space_above = pos.y() - screen_rect.top()
        space_below = screen_rect.bottom() - pos.y()
        space_left = pos.x() - screen_rect.left()
        space_right = screen_rect.right() - pos.x()
        
        # Выбираем оптимальное положение исходя из доступного пространства
        # Приоритет: снизу, сверху, справа, слева
        if tooltip_size.height() <= space_below:
            # Помещаем снизу
            y = pos.y()
        elif tooltip_size.height() <= space_above:
            # Помещаем сверху
            y = pos.y() - tooltip_size.height()
        elif tooltip_size.width() <= space_right:
            # Помещаем справа
            x = pos.x()
            y = pos.y() - tooltip_size.height() // 2
        else:
            # Помещаем слева
            x = pos.x() - tooltip_size.width()
            y = pos.y() - tooltip_size.height() // 2
        
        # Также учитываем ширину
        if tooltip_size.width() <= space_right and tooltip_size.height() <= space_below:
            # Помещаем справа снизу
            x = pos.x()
        elif tooltip_size.width() <= space_left and tooltip_size.height() <= space_below:
            # Помещаем слева снизу
            x = pos.x() - tooltip_size.width()
        elif tooltip_size.width() <= space_right and tooltip_size.height() <= space_above:
            # Помещаем справа сверху
            x = pos.x()
            y = pos.y() - tooltip_size.height()
        elif tooltip_size.width() <= space_left and tooltip_size.height() <= space_above:
            # Помещаем слева сверху
            x = pos.x() - tooltip_size.width()
            y = pos.y() - tooltip_size.height()
        else:
            # Если нигде не помещается идеально, выбираем наилучший вариант
            max_space_direction = max(space_above, space_below, space_left, space_right)
            if max_space_direction == space_below:
                x = pos.x()
                y = pos.y()
            elif max_space_direction == space_above:
                x = pos.x()
                y = pos.y() - tooltip_size.height()
            elif max_space_direction == space_right:
                x = pos.x()
                y = pos.y() - tooltip_size.height() // 2
            else:  # space_left
                x = pos.x() - tooltip_size.width()
                y = pos.y() - tooltip_size.height() // 2
        
        # Ограничиваем координаты в пределах экрана
        x = max(screen_rect.left(), min(x, screen_rect.right() - tooltip_size.width()))
        y = max(screen_rect.top(), min(y, screen_rect.bottom() - tooltip_size.height()))
        return QPoint(x, y)

    def fade_out(self, on_complete_callback=None):
        """Плавное скрытие подсказки с анимацией"""
        # Запускаем анимации исчезновения
        self.opacity_animation.setStartValue(1)
        self.opacity_animation.setEndValue(0)
        self.opacity_animation.setDuration(350)  # 350мс длительность (в диапазоне 300-500мс)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)  # easing кривая
        self.opacity_animation.start()
        
        original_geometry = self.geometry()
        # Уменьшаем размеры для анимации исчезновения (эффект масштабирования)
        scaled_geometry = original_geometry.adjusted(
            original_geometry.width() // 4,  # уменьшаем на 25% от ширины
            original_geometry.height() // 4,  # уменьшаем на 25% от высоты
            -original_geometry.width() // 4,  # уменьшаем на 25% от ширины
            -original_geometry.height() // 4  # уменьшаем на 25% от высоты
        )
        self.scale_animation.setStartValue(original_geometry)
        self.scale_animation.setEndValue(scaled_geometry)
        self.scale_animation.setDuration(350)  # 350мс длительность (в диапазоне 300-500мс)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)  # easing кривая
        self.scale_animation.start()
        
        # Создаем замыкание для вызова hide и уведомления о завершении
        def on_animation_finished():
            self.hide()
            if on_complete_callback:
                on_complete_callback()
        
        # Отключаем все предыдущие соединения анимации, чтобы избежать дублирования
        try:
            self.opacity_animation.finished.disconnect()
        except:
            pass  # Сигнал не был подключен ранее
        
        # Скрываем виджет после завершения анимации
        self.opacity_animation.finished.connect(on_animation_finished)
    
    def on_fade_out_finished(self):
        """Метод, вызываемый менеджером при завершении анимации скрытия"""
        # Останавливаем таймер принудительного скрытия, если он запущен
        # (этот метод будет вызываться из менеджера, если у него есть ссылка)



class TooltipManager:
    """
    Менеджер управления всплывающими подсказками
    """
    def __init__(self):
        self.tooltip_widget = TooltipWidget()
        self.current_widget = None
        self.current_text = ""
        
        # Таймеры для задержек
        self.show_timer = QTimer()
        self.show_timer.setSingleShot(True)
        self.show_timer.timeout.connect(self._show_tooltip)
        
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self._hide_tooltip)
        
        # Таймер для принудительного скрытия подсказки в случае зависания
        self.force_hide_timer = QTimer()
        self.force_hide_timer.setSingleShot(True)
        self.force_hide_timer.timeout.connect(self._force_hide_tooltip)
        
        # Флаг, показывающий, что подсказка сейчас отображается
        self.is_tooltip_visible = False
        
        # Флаг, отслеживающий, находится ли курсор над виджетом
        self.is_cursor_over_widget = False
        
        # Флаг, отслеживающий, запланировано ли отображение подсказки
        self.is_show_scheduled = False
        
        # Таймер для предотвращения дребезга (anti-jitter)
        self.anti_jitter_timer = QTimer()
        self.anti_jitter_timer.setSingleShot(True)
        self.anti_jitter_timer.setInterval(50) # 50мс задержка для предотвращения дребезга
        
        
    def register_widget(self, widget, text):
        """Регистрация виджета для отображения подсказки"""
        # Убираем стандартную подсказку у виджета, чтобы избежать дублирования
        widget.setToolTip("")
        # Сохраняем оригинальные методы, если они существуют
        if hasattr(widget, 'enterEvent'):
            original_enter = widget.enterEvent
        else:
            original_enter = None
            
        if hasattr(widget, 'leaveEvent'):
            original_leave = widget.leaveEvent
        else:
            original_leave = None
        
        # Переопределяем методы
        def enter_event(event):
            # Отключаем стандартную подсказку, чтобы избежать дублирования
            widget.setToolTip("")  # Убираем стандартную подсказку
            self._on_enter(widget, text)
            if original_enter:
                original_enter(event)
                
        def leave_event(event):
            self._on_leave()
            if original_leave:
                original_leave(event)
        
        widget.enterEvent = enter_event
        widget.leaveEvent = leave_event
        
    def _on_enter(self, widget, text):
        """Обработка события наведения курсора"""
        self.current_widget = widget
        self.current_text = text
        
        # Устанавливаем флаг, что курсор над виджетом
        self.is_cursor_over_widget = True
        self.is_show_scheduled = True # Помечаем, что показ запланирован
        
        # Отменяем таймер скрытия, если он запущен
        if self.hide_timer.isActive():
            self.hide_timer.stop()
        
        # Отменяем предыдущий таймер показа, если был
        if self.show_timer.isActive():
            self.show_timer.stop()
        
        # Если подсказка уже видна, нужно сначала скрыть текущую подсказку
        if self.is_tooltip_visible:
            # Сбрасываем флаги и скрываем текущую подсказку
            self.is_tooltip_visible = False
            self.is_show_scheduled = False
            # Прячем виджет напрямую
            self.tooltip_widget.hide()
            # Отменяем таймер скрытия, если он запущен
            if self.hide_timer.isActive():
                self.hide_timer.stop()
            # Отменяем таймер принудительного скрытия, если он запущен
            if self.force_hide_timer.isActive():
                self.force_hide_timer.stop()
        
        # Обновляем текущий виджет и текст
        self.current_widget = widget
        self.current_text = text
        
        # Отменяем предыдущий таймер показа, если был
        if self.show_timer.isActive():
            self.show_timer.stop()
        
        # Запускаем таймер для отображения подсказки с задержкой 750мс (увеличил для стабильности)
        self.show_timer.start(750)
        
    def _on_leave(self):
        """Обработка события ухода курсора"""
        # Сбрасываем флаг, что курсор над виджетом
        self.is_cursor_over_widget = False
        self.is_show_scheduled = False # Сбрасываем флаг запланированного показа
        
        # Отменяем таймер отображения, если курсор ушел до отображения
        if self.show_timer.isActive():
            self.show_timer.stop()
        
        # Если подсказка не отображается, не нужно запускать таймер скрытия
        if not self.is_tooltip_visible:
            return
            
        # Запускаем таймер скрытия с задержкой 500мс (увеличили время для стабильности)
        self.hide_timer.start(500)
        
    def _show_tooltip(self):
        """Отображение подсказки"""
        # Проверяем, что курсор все еще над виджетом и показ запланирован перед показом подсказки
        if self.current_widget and self.current_text and self.is_cursor_over_widget and self.is_show_scheduled:
            # Получаем глобальную позицию виджета
            pos = self.current_widget.mapToGlobal(
                QPoint(self.current_widget.width() // 2, self.current_widget.height())
            )
            
            # Устанавливаем текст и показываем подсказку
            self.tooltip_widget.set_text(self.current_text)
            self.tooltip_widget.show_at(pos)
            
            # Устанавливаем флаг, что подсказка видна
            self.is_tooltip_visible = True
            
    def _hide_tooltip(self):
        """Скрытие подсказки"""
        # Проверяем, не вернулся ли курсор над виджетом до истечения таймера скрытия
        if self.is_cursor_over_widget:
            return
            
        # Устанавливаем флаг, что подсказка больше не видна
        self.is_tooltip_visible = False
        # Сбрасываем флаг запланированного показа, так как подсказка скрывается
        self.is_show_scheduled = False
        # Для плавного скрытия нужно создать анимацию в классе TooltipWidget
        # Обновляем метод hide в TooltipWidget для плавного скрытия
        # Передаем callback для остановки таймера принудительного скрытия при успешном завершении анимации
        self.tooltip_widget.fade_out(self._on_fade_out_complete)
        # Запускаем таймер принудительного скрытия на случай, если анимация зависнет
        self.force_hide_timer.start(1000)  # 1 секунда таймаут

    def _on_fade_out_complete(self):
        """Вызывается при успешном завершении анимации скрытия"""
        # Убедимся, что флаг видимости установлен в False
        self.is_tooltip_visible = False
        # Сбрасываем флаг запланированного показа
        self.is_show_scheduled = False
        # Останавливаем таймер принудительного скрытия, так как анимация завершена успешно
        if self.force_hide_timer.isActive():
            self.force_hide_timer.stop()
        # Также останавливаем основной таймер скрытия
        if self.hide_timer.isActive():
            self.hide_timer.stop()

    def _force_hide_tooltip(self):
        """Принудительное скрытие подсказки в случае зависания"""
        # Прячем виджет напрямую
        self.tooltip_widget.hide()
        # Сбрасываем все флаги
        self.is_tooltip_visible = False
        self.is_show_scheduled = False
        # Останавливаем таймер принудительного скрытия
        if self.force_hide_timer.isActive():
            self.force_hide_timer.stop()
        # Также останавливаем основной таймер скрытия
        if self.hide_timer.isActive():
            self.hide_timer.stop()
    
    def set_tooltip_text(self, widget, text):
        """Установка текста подсказки для виджета"""
        self.register_widget(widget, text)

    def disable_standard_tooltips(self, widget):
        """Отключает стандартные подсказки для виджета и всех его дочерних элементов"""
        # Отключаем стандартную подсказку для текущего виджета
        widget.setToolTip("")
        # Рекурсивно отключаем для всех дочерних элементов
        for child in widget.findChildren(QWidget):
            child.setToolTip("")