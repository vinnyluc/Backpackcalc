import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QListWidget, QMessageBox, QSpinBox, QComboBox,
                            QMenuBar, QMenu, QFileDialog, QDialog, QGridLayout,
                            QButtonGroup, QFrame, QDoubleSpinBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QKeySequence, QIcon, QPixmap, QPainter, QColor, QPen
import os

class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F2:
            self.parent.edit_item()
        elif event.key() == Qt.Key.Key_Delete:
            self.parent.delete_item()
        else:
            super().keyPressEvent(event)

class EditItemDialog(QDialog):
    def __init__(self, parent=None, item_name="", item_weight=0, item_volume=0):
        super().__init__(parent)
        self.setWindowTitle("Изменить предмет")
        layout = QGridLayout(self)
        
        # Название
        layout.addWidget(QLabel("Название:"), 0, 0)
        self.name_edit = QLineEdit(item_name)
        layout.addWidget(self.name_edit, 0, 1)
        
        # Вес
        layout.addWidget(QLabel("Вес (гр.):"), 1, 0)
        self.weight_spin = QSpinBox()
        self.weight_spin.setRange(1, 10000)
        self.weight_spin.setValue(item_weight)
        layout.addWidget(self.weight_spin, 1, 1)
        
        # Объем
        layout.addWidget(QLabel("Объем (л):"), 2, 0)
        self.volume_spin = QDoubleSpinBox()
        self.volume_spin.setRange(0, 100)
        self.volume_spin.setDecimals(1)
        self.volume_spin.setSingleStep(0.1)
        self.volume_spin.setValue(item_volume)
        layout.addWidget(self.volume_spin, 2, 1)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout, 3, 0, 1, 2)

    def get_data(self):
        return self.name_edit.text().strip(), self.weight_spin.value(), self.volume_spin.value()

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        
        # Создаем горизонтальный layout для иконки и текста
        header_layout = QHBoxLayout()
        
        # Добавляем иконку
        icon_label = QLabel()
        icon_path = os.path.join(os.path.dirname(__file__), "icon_calc_2.png")
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            icon_label.setPixmap(pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio))
        header_layout.addWidget(icon_label)
        
        # Добавляем текст
        text_label = QLabel(
            "Калькулятор рюкзака v1.0\n\n"
            "Программа для расчета веса снаряжения в рюкзаке.\n"
            "Позволяет добавлять предметы вручную или использовать "
            "готовые наборы снаряжения.\n\n"
            "© 2025 Himaltrex"
        )
        header_layout.addWidget(text_label)
        layout.addLayout(header_layout)
        
        # Добавляем ссылку на сайт
        link_label = QLabel()
        link_label.setText('<a href="http://www.himaltrex.ru">www.himaltrex.ru</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(link_label)
        
        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

class BackpackVisualizer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(120)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.current_weight = 0
        self.max_weight = 20000  # По умолчанию 20 кг в граммах
        self.current_volume = 0
        self.max_volume = 40  # По умолчанию 40 литров
        
    def set_weights(self, current_weight, max_weight, current_volume, max_volume):
        self.current_weight = current_weight
        self.max_weight = max_weight
        self.current_volume = current_volume
        self.max_volume = max_volume
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        
        # Делим область на две части
        weight_rect = rect.adjusted(1, 1, -rect.width()//2, -1)
        volume_rect = rect.adjusted(rect.width()//2, 1, -1, -1)
        
        # Определяем цвета для рамок в зависимости от состояния
        weight_frame_color = QColor(255, 0, 0) if self.current_weight > self.max_weight else QColor(0, 150, 0)
        volume_frame_color = QColor(255, 0, 0) if self.current_volume > self.max_volume else QColor(0, 150, 0)
        
        # Рисуем рамки с соответствующими цветами
        pen = QPen(weight_frame_color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(weight_rect)
        
        pen.setColor(volume_frame_color)
        painter.setPen(pen)
        painter.drawRect(volume_rect)
        
        # Вычисляем высоту заполнения для веса
        if self.max_weight > 0:
            weight_height = int((self.current_weight / self.max_weight) * weight_rect.height())
            weight_height = min(weight_height, weight_rect.height())
            
            # Определяем цвет заполнения для веса
            if self.current_weight > self.max_weight:
                weight_color = QColor(255, 200, 200)  # Светло-красный при перевесе
            else:
                weight_color = QColor(200, 255, 200)  # Светло-зеленый при нормальном весе
            
            # Рисуем заполнение для веса
            painter.fillRect(
                weight_rect.x() + 2,
                weight_rect.bottom() - weight_height + 2,
                weight_rect.width() - 3,
                weight_height - 3,
                weight_color
            )
        
        # Вычисляем высоту заполнения для объема
        if self.max_volume > 0:
            volume_height = int((self.current_volume / self.max_volume) * volume_rect.height())
            volume_height = min(volume_height, volume_rect.height())
            
            # Определяем цвет заполнения для объема
            if self.current_volume > self.max_volume:
                volume_color = QColor(255, 200, 200)  # Светло-красный при переполнении
            else:
                volume_color = QColor(200, 255, 200)  # Светло-зеленый при нормальном объеме
            
            # Рисуем заполнение для объема
            painter.fillRect(
                volume_rect.x() + 2,
                volume_rect.bottom() - volume_height + 2,
                volume_rect.width() - 3,
                volume_height - 3,
                volume_color
            )
        
        # Добавляем подписи
        painter.setPen(QColor(0, 0, 0))  # Черный цвет для текста
        painter.drawText(weight_rect, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, "Вес")
        painter.drawText(volume_rect, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, "Объем")
        
        # Устанавливаем жирный шрифт для предупреждений
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        
        # Если есть перевес или переполнение, пишем предупреждения по центру
        if self.current_weight > self.max_weight:
            painter.save()
            painter.translate(weight_rect.center())
            painter.rotate(-90)
            text_rect = painter.fontMetrics().boundingRect("Перевес")
            painter.drawText(-text_rect.width()//2, 0, "Перевес")
            painter.restore()
            
        if self.current_volume > self.max_volume:
            painter.save()
            painter.translate(volume_rect.center())
            painter.rotate(-90)
            text_rect = painter.fontMetrics().boundingRect("Переполнен")
            painter.drawText(-text_rect.width()//2, 0, "Переполнен")
            painter.restore()

class BackpackCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None  # Добавляем отслеживание текущего файла
        self.update_window_title()
        self.setMinimumSize(700, 500)  # Увеличиваем минимальный размер окна
        
        # Устанавливаем иконку программы
        icon_path = os.path.join(os.path.dirname(__file__), "icon_calc.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Создание меню
        self.create_menu()
        
        # Предустановленные наборы снаряжения
        self.preset_items = {
            "Базовое снаряжение": {
                "Документы, билеты, деньги": {"вес": 100, "объем": 0.2},
                "Чехол от дождя для рюкзака": {"вес": 200, "объем": 0.3},
                "Спальный мешок -10°C": {"вес": 1800, "объем": 8.0},
                "Средства личной гигиены": {"вес": 400, "объем": 1.5},
                "Крем от солнца SF 70-110": {"вес": 150, "объем": 0.2},
                "Гигиеническая помада SF": {"вес": 20, "объем": 0.1},
                "Фонарик налобный": {"вес": 150, "объем": 0.3},
                "Очки солнцезащитные": {"вес": 150, "объем": 0.5},
                "Треккинговые палки": {"вес": 500, "объем": 1.0}
            },
            "Одежда": {
                "Треккинговые ботинки": {"вес": 1200, "объем": 4.0},
                "Кроссовки легкие": {"вес": 800, "объем": 3.0},
                "Пуховка": {"вес": 800, "объем": 4.0},
                "Штормовка": {"вес": 400, "объем": 2.0},
                "Футболка": {"вес": 150, "объем": 0.5},
                "Носки треккинговые (2 пары)": {"вес": 200, "объем": 0.4},
                "Носки обычные (2 пары)": {"вес": 150, "объем": 0.3},
                "Нижнее бельё (комплект)": {"вес": 200, "объем": 0.5},
                "Флисовая кофта": {"вес": 400, "объем": 2.0},
                "Термобелье верх": {"вес": 250, "объем": 0.8},
                "Термобелье низ": {"вес": 250, "объем": 0.8},
                "Штаны ходовые": {"вес": 400, "объем": 1.5},
                "Шорты": {"вес": 200, "объем": 0.7},
                "Шапка тёплая": {"вес": 100, "объем": 0.3},
                "Панамка": {"вес": 100, "объем": 0.3},
                "Перчатки флисовые": {"вес": 150, "объем": 0.3},
                "Перчатки виндстопер": {"вес": 100, "объем": 0.3},
                "Баф": {"вес": 50, "объем": 0.2},
                "Дождевик": {"вес": 300, "объем": 1.0}
            },
            "Электроника": {
                "Телефон": {"вес": 200, "объем": 0.3},
                "Зарядное устройство": {"вес": 150, "объем": 0.2},
                "Повербанк": {"вес": 350, "объем": 0.4},
                "GPS навигатор": {"вес": 250, "объем": 0.3},
                "Рация": {"вес": 300, "объем": 0.4},
                "Запасные батарейки": {"вес": 100, "объем": 0.2}
            }
        }
        
        # Словарь для хранения предметов, их веса и объема
        self.items = {}
        
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Создание кнопок категорий
        categories_layout = QHBoxLayout()
        self.category_buttons = QButtonGroup(self)
        self.category_buttons.setExclusive(True)
        
        for category in self.preset_items.keys():
            button = QPushButton(category)
            button.setCheckable(True)
            self.category_buttons.addButton(button)
            categories_layout.addWidget(button)
            if category == "Базовое снаряжение":  # По умолчанию выбираем первую категорию
                button.setChecked(True)
        
        self.category_buttons.buttonClicked.connect(self.update_items_list)
        layout.addLayout(categories_layout)
        
        # Создание трехколоночного layout
        main_content_layout = QHBoxLayout()
        
        # Левая колонка - список доступных предметов
        left_panel = QVBoxLayout()
        self.available_items_list = QListWidget()
        self.available_items_list.setMinimumWidth(250)
        self.update_items_list()  # Заполняем список предметами первой категории
        left_panel.addWidget(self.available_items_list)
        
        add_selected_button = QPushButton("Добавить выбранный предмет")
        add_selected_button.clicked.connect(self.add_selected_item)
        left_panel.addWidget(add_selected_button)
        
        # Добавление своего предмета
        left_panel.addWidget(QLabel("Добавить свой предмет:"))
        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText("Название предмета")
        left_panel.addWidget(self.item_name)
        
        weight_layout = QHBoxLayout()
        weight_layout.addWidget(QLabel("Вес:"))
        self.item_weight = QSpinBox()
        self.item_weight.setRange(1, 10000)
        self.item_weight.setSuffix(" гр.")
        self.item_weight.setValue(100)
        weight_layout.addWidget(self.item_weight)
        left_panel.addLayout(weight_layout)
        
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Объем:"))
        self.item_volume = QDoubleSpinBox()
        self.item_volume.setRange(0, 100)
        self.item_volume.setSuffix(" л")
        self.item_volume.setDecimals(1)
        self.item_volume.setSingleStep(0.1)
        self.item_volume.setValue(0.5)
        volume_layout.addWidget(self.item_volume)
        left_panel.addLayout(volume_layout)
        
        add_custom_button = QPushButton("Добавить свой предмет")
        add_custom_button.clicked.connect(self.add_item)
        left_panel.addWidget(add_custom_button)
        
        main_content_layout.addLayout(left_panel)
        
        # Центральная колонка - список добавленных предметов
        center_panel = QVBoxLayout()
        center_panel.addWidget(QLabel("Добавленные предметы:"))
        self.items_list = CustomListWidget(self)
        self.items_list.setMinimumWidth(300)
        self.setup_context_menu()
        center_panel.addWidget(self.items_list)
        
        buttons_layout = QHBoxLayout()
        delete_button = QPushButton("Удалить предмет")
        delete_button.clicked.connect(self.delete_item)
        buttons_layout.addWidget(delete_button)
        
        clear_button = QPushButton("Очистить список")
        clear_button.clicked.connect(self.clear_items)
        buttons_layout.addWidget(clear_button)
        center_panel.addLayout(buttons_layout)
        
        main_content_layout.addLayout(center_panel)
        
        # Правая колонка - визуализатор
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Визуализация заполнения:"))
        self.backpack_viz = BackpackVisualizer()
        self.backpack_viz.setMinimumHeight(300)
        self.backpack_viz.setMinimumWidth(150)
        right_panel.addWidget(self.backpack_viz)
        right_panel.addStretch()
        
        main_content_layout.addLayout(right_panel)
        
        layout.addLayout(main_content_layout)
        
        # Установка веса и объема рюкзака
        params_layout = QHBoxLayout()
        
        # Вес рюкзака
        weight_layout = QHBoxLayout()
        weight_layout.addWidget(QLabel("Вес рюкзака (кг):"))
        
        self.weight_input = QSpinBox()
        self.weight_input.setRange(5, 25)
        self.weight_input.setValue(12)
        self.weight_input.setSuffix(" кг")
        weight_layout.addWidget(self.weight_input)
        
        set_weight_button = QPushButton("Подтвердить")
        set_weight_button.clicked.connect(self.update_max_weight)
        weight_layout.addWidget(set_weight_button)
        
        params_layout.addLayout(weight_layout)
        params_layout.addSpacing(20)  # Добавляем промежуток между полями
        
        # Объем рюкзака
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Объем рюкзака (л):"))
        
        self.volume_spin = QSpinBox()
        self.volume_spin.setRange(20, 80)
        self.volume_spin.setValue(40)
        self.volume_spin.setSuffix(" л")
        volume_layout.addWidget(self.volume_spin)
        
        set_volume_button = QPushButton("Подтвердить")
        set_volume_button.clicked.connect(self.update_max_weight)  # Используем тот же метод
        volume_layout.addWidget(set_volume_button)
        
        params_layout.addLayout(volume_layout)
        params_layout.addStretch()
        layout.addLayout(params_layout)
        
        # Результаты
        self.result_list = QListWidget()
        self.result_list.setFixedHeight(75)  # Устанавливаем фиксированную высоту для трех строк
        self.result_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Отключаем полосу прокрутки
        layout.addWidget(self.result_list)

    def update_window_title(self):
        """Обновляет заголовок окна с учетом текущего файла"""
        base_title = "Калькулятор рюкзака"
        if self.current_file:
            self.setWindowTitle(f"{base_title} - {os.path.basename(self.current_file)}")
        else:
            self.setWindowTitle(base_title)

    def create_menu(self):
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("Файл")
        
        open_action = QAction("Открыть", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Сохранить как...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню Справка
        help_menu = menubar.addMenu("Справка")
        
        about_action = QAction("О программе", self)
        about_action.setShortcut("F1")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть файл",
            "",
            "Файлы рюкзака (*.bpc);;Все файлы (*.*)"
        )
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    # Загружаем максимальный вес и объем, если они есть в файле
                    if isinstance(data, dict) and "max_weight" in data and "max_volume" in data:
                        self.weight_input.setValue(data["max_weight"])
                        self.volume_spin.setValue(data["max_volume"])
                        items_data = data["items"]
                    else:
                        # Для обратной совместимости со старым форматом
                        items_data = data
                    
                    self.items.clear()
                    self.items_list.clear()
                    for item_name, item_data in items_data.items():
                        self.items[item_name] = item_data
                        self.items_list.addItem(f"{item_name} = {item_data['вес']} гр., {item_data['объем']} л")
                    self.current_file = file_name
                    self.update_window_title()
                    self.update_backpack_state()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл: {str(e)}")

    def save_file(self):
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        default_name = "Backpack_calculation.bpc"
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            default_name,
            "Файлы рюкзака (*.bpc);;Все файлы (*.*)"
        )
        if file_name:
            # Добавляем расширение .bpc, если его нет
            if not file_name.lower().endswith('.bpc'):
                file_name += '.bpc'
            self._save_to_file(file_name)

    def _save_to_file(self, file_name):
        """Сохраняет данные в файл"""
        try:
            data = {
                "max_weight": self.weight_input.value(),
                "max_volume": self.volume_spin.value(),
                "items": self.items
            }
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            self.current_file = file_name
            self.update_window_title()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def update_items_list(self, button=None):
        # Если кнопка не указана, берем текущую выбранную
        if button is None:
            button = self.category_buttons.checkedButton()
        
        category = button.text()
        self.available_items_list.clear()
        
        # Добавляем предметы из выбранной категории
        items = self.preset_items[category]
        for item_name, item_data in items.items():
            self.available_items_list.addItem(f"{item_name} ({item_data['вес']} гр., {item_data['объем']} л)")

    def add_selected_item(self):
        current_item = self.available_items_list.currentItem()
        if current_item:
            text = current_item.text()
            item_name = text[:text.rfind('(')].strip()
            category = self.category_buttons.checkedButton().text()
            item_data = self.preset_items[category][item_name]
            
            if item_name not in self.items:
                self.items[item_name] = item_data
                self.items_list.addItem(f"{item_name} = {item_data['вес']} гр., {item_data['объем']} л")
                self.update_backpack_state()

    def add_item(self):
        name = self.item_name.text().strip()
        weight = self.item_weight.value()
        volume = self.item_volume.value()
        
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название предмета!")
            return
            
        if name in self.items:
            QMessageBox.warning(self, "Ошибка", "Такой предмет уже существует!")
            return
            
        self.items[name] = {"вес": weight, "объем": volume}
        self.items_list.addItem(f"{name} = {weight} гр., {volume} л")
        self.item_name.clear()
        self.item_weight.setValue(100)
        self.item_volume.setValue(0.5)
        self.update_backpack_state()

    def delete_item(self):
        current_item = self.items_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Ошибка", "Выберите предмет для удаления!")
            return
            
        item_text = current_item.text()
        item_name = item_text.split(" = ")[0]
        
        del self.items[item_name]
        self.items_list.takeItem(self.items_list.row(current_item))
        self.update_backpack_state()

    def clear_items(self):
        self.items.clear()
        self.items_list.clear()
        self.result_list.clear()
        self.update_backpack_state()

    def update_backpack_state(self):
        """Обновляет состояние рюкзака и результаты при любых изменениях"""
        if not self.items:
            self.result_list.clear()
            self.backpack_viz.set_weights(0, self.weight_input.value() * 1000, 0, self.volume_spin.value())
            return
            
        max_weight = self.weight_input.value() * 1000  # Перевод в граммы
        max_volume = self.volume_spin.value()  # Объем в литрах
        remaining_weight = max_weight
        remaining_volume = max_volume
        sorted_items = dict(sorted(self.items.items(), key=lambda x: -x[1]['вес']))
        
        self.result_list.clear()
        
        # Первая строка: максимальные значения
        self.result_list.addItem(f"Максимальный вес: {max_weight} гр. ({max_weight/1000:.1f} кг)     Максимальный объем: {max_volume} л")
        
        # Подсчет общих значений
        total_weight = sum(data['вес'] for data in self.items.values())
        total_volume = sum(data['объем'] for data in self.items.values())
        items_count = len(self.items)
        
        # Вторая строка: количество предметов
        items_word = self.get_items_word(items_count)
        self.result_list.addItem(f"В рюкзаке {items_count} {items_word}")
        
        # Третья строка: занято/осталось
        self.result_list.addItem(
            f"Занято: {total_weight} гр. ({total_weight/1000:.1f} кг), осталось {max_weight - total_weight} гр. ({(max_weight - total_weight)/1000:.1f} кг)"
            f"     Занято: {total_volume:.1f} л, осталось {max_volume - total_volume:.1f} л"
        )
        
        # Обновляем визуализацию
        self.backpack_viz.set_weights(
            total_weight,
            max_weight,
            total_volume,
            max_volume
        )

    def update_max_weight(self):
        """Обновляет максимальный вес и объем рюкзака"""
        self.update_backpack_state()

    def edit_item(self):
        current_item = self.items_list.currentItem()
        if current_item is None:
            return
            
        item_text = current_item.text()
        item_name = item_text.split(" = ")[0]
        item_data = self.items[item_name]
        
        dialog = EditItemDialog(self, item_name, item_data['вес'], item_data['объем'])
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_name, new_weight, new_volume = dialog.get_data()
            
            if not new_name:
                QMessageBox.warning(self, "Ошибка", "Название не может быть пустым!")
                return
                
            if new_name != item_name and new_name in self.items:
                QMessageBox.warning(self, "Ошибка", "Предмет с таким названием уже существует!")
                return
            
            # Удаляем старый предмет
            del self.items[item_name]
            
            # Добавляем обновленный предмет
            self.items[new_name] = {"вес": new_weight, "объем": new_volume}
            current_item.setText(f"{new_name} = {new_weight} гр., {new_volume} л")
            self.update_backpack_state()

    def get_items_word(self, count):
        """Возвращает правильное склонение слова 'предмет' в зависимости от числа"""
        last_digit = count % 10
        last_two_digits = count % 100
        
        if last_two_digits in [11, 12, 13, 14]:
            return "предметов"
        elif last_digit == 1:
            return "предмет"
        elif last_digit in [2, 3, 4]:
            return "предмета"
        else:
            return "предметов"

    def calculate_total_weight(self):
        """Подсчитывает общий текущий вес всех предметов"""
        return sum(item['вес'] for item in self.items.values())

    def calculate_total_volume(self):
        """Подсчитывает общий текущий объем всех предметов"""
        return sum(item['объем'] for item in self.items.values())

    def setup_context_menu(self):
        self.items_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.items_list.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        current_item = self.items_list.currentItem()
        if current_item is None:
            return
            
        context_menu = QMenu(self)
        
        edit_action = context_menu.addAction("Изменить")
        edit_action.setShortcut("F2")
        delete_action = context_menu.addAction("Удалить")
        delete_action.setShortcut("Del")
        
        action = context_menu.exec(self.items_list.mapToGlobal(position))
        
        if action == edit_action:
            self.edit_item()
        elif action == delete_action:
            self.delete_item()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BackpackCalculator()
    window.show()
    sys.exit(app.exec()) 