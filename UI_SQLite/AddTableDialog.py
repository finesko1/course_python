import logging
import os
import sqlite3

from PySide6.QtCore import QSize, Qt, QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QVBoxLayout, QTextEdit, QMessageBox, \
    QTableWidgetItem, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QLayout, QDialog, QLineEdit, \
    QComboBox, QCheckBox, QHeaderView
import uuid

from SQLite2 import Ui_Dialog
from SQLite_connect import SQLiteConnection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AddTableDialog(QDialog):
    def __init__(self, db_name, db_path):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Настройка данных
        # строки виджетов
        self.rows = {}
        # имя бд, настройка title
        self.db_name = db_name
        self.db_path = db_path
        self.ui.WindowHeaderLabel.setText(f"Добавление таблицы в базу данных: {self.db_name}")

        # Иконки элементов
        self.add_icon = QIcon()
        self.add_icon.addFile(u":/icons/icons/add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.del_icon = QIcon()
        self.del_icon.addFile(u":/icons/icons/delete.svg", QSize(), QIcon.Normal, QIcon.Off)

        # Настраиваем первую строку как поле 'id'
        self.setup_id_row()

        # Управление кнопками
        self.ui.AddRowButton_0.clicked.connect(self.add_row)
        self.ui.SaveButton.clicked.connect(lambda: self.save(self.db_name, self.db_path))
        # Привязка сигналов к обновлению состояний
        self.ui.TypeDataComboBox_0.currentIndexChanged.connect(lambda: self.update_widget_states())
        self.ui.PKcheckBox_0.stateChanged.connect(lambda: self.update_widget_states())
        self.ui.NNcheckBox_0.stateChanged.connect(lambda: self.update_widget_states())
        self.ui.BcheckBox_0.stateChanged.connect(lambda: self.update_widget_states())
        self.ui.UNcheckBox_0.stateChanged.connect(lambda: self.update_widget_states())

        # Инициализация состояния
        self.update_widget_states()

    def setup_id_row(self):
        """Настраивает первую строку как поле 'id'."""
        # Настраиваем lineEdit_0
        self.ui.lineEdit_0.setText('id')
        self.ui.lineEdit_0.setReadOnly(True)

        # Настраиваем TypeDataComboBox_0
        self.ui.TypeDataComboBox_0.setCurrentText('INTEGER')
        self.ui.TypeDataComboBox_0.setEnabled(False)

        # Настраиваем PKcheckBox_0
        self.ui.PKcheckBox_0.setChecked(True)
        self.ui.PKcheckBox_0.setEnabled(False)
        self.ui.UQcheckBox_0.setEnabled(False)
        self.ui.UNcheckBox_0.setEnabled(False)
        self.ui.BcheckBox_0.setEnabled(False)
        self.ui.NNcheckBox_0.setEnabled(False)

        # Отключаем DelRowButton_0
        self.ui.DelRowButton_0.setEnabled(False)

    # Добавление строки для ввода ограничений аттрибута
    def add_row(self, disable_delete=False):
        row_id = str(uuid.uuid4())  # Уникальный идентификатор для строки

        # Создаем виджеты для новой строки
        line_edit = QLineEdit(self)
        type_data_combo_box = QComboBox(self)
        type_data_combo_box.addItems([
            "Выберите...", "TEXT", "INTEGER", "REAL", "DATE", "DATETIME", "BOOLEAN"
        ])

        pk_checkbox = QCheckBox("", self)
        nn_checkbox = QCheckBox("", self)
        uq_checkbox = QCheckBox("", self)
        b_checkbox = QCheckBox("", self)
        un_checkbox = QCheckBox("", self)
        add_button = QPushButton()
        add_button.setIcon(self.add_icon)
        delete_button = QPushButton()
        delete_button.setIcon(self.del_icon)

        # Устанавливаем имена объектов
        line_edit.setObjectName(f"lineEdit_{row_id}")
        type_data_combo_box.setObjectName(f"TypeDataComboBox_{row_id}")
        add_button.setObjectName(f"AddRowButton_{row_id}")
        delete_button.setObjectName(f"DelRowButton_{row_id}")

        # Подключаем кнопки
        add_button.clicked.connect(lambda: self.add_row())
        delete_button.clicked.connect(lambda: self.remove_row(row_id))

        # Создаем виджеты для чекбоксов
        pk_widget = QWidget(self)
        pk_layout = QVBoxLayout(pk_widget)
        pk_layout.addWidget(pk_checkbox)

        nn_widget = QWidget(self)
        nn_layout = QVBoxLayout(nn_widget)
        nn_layout.addWidget(nn_checkbox)

        uq_widget = QWidget(self)
        uq_layout = QVBoxLayout(uq_widget)
        uq_layout.addWidget(uq_checkbox)

        b_widget = QWidget(self)
        b_layout = QVBoxLayout(b_widget)
        b_layout.addWidget(b_checkbox)

        un_widget = QWidget(self)
        un_layout = QVBoxLayout(un_widget)
        un_layout.addWidget(un_checkbox)

        # Добавляем виджеты в сетку
        row_index = self.ui.gridLayout.rowCount()
        widgets = [
            line_edit,
            type_data_combo_box,
            pk_widget,
            nn_widget,
            uq_widget,
            b_widget,
            un_widget,
            add_button,
            delete_button,
        ]
        for col, widget in enumerate(widgets):
            self.ui.gridLayout.addWidget(widget, row_index, col)

        # Сохраняем виджеты строки в словаре
        self.rows[row_id] = widgets

        # Подключаем сигналы для обновления состояний виджетов
        type_data_combo_box.currentIndexChanged.connect(lambda: self.update_widget_states())
        pk_checkbox.stateChanged.connect(lambda: self.update_widget_states())
        nn_checkbox.stateChanged.connect(lambda: self.update_widget_states())
        b_checkbox.stateChanged.connect(lambda: self.update_widget_states())
        un_checkbox.stateChanged.connect(lambda: self.update_widget_states())

        self.update_widget_states()

    # Удаление строки управления
    def remove_row(self, row_id):
        """Удаление строки компонентов по уникальному ID"""
        if row_id in self.rows:
            # Удаление виджетов из слоев
            widgets = self.rows.pop(row_id)
            for widget in widgets:
                self.ui.gridLayout.removeWidget(widget)
                widget.deleteLater()
        else:
            # Ссылка на виджет утеряна
            #print(f"Row with ID {row_id} not found.")
            pass

    # Актуальные значения в полях виджетов, обновление массива
    def refresh_data(self):
        updated_rows = {}
        row_count = self.ui.gridLayout.rowCount()  # Количество строк в сетке

        for row_index in range(row_count):
            try:
                # Получение виджетов в строке
                widgets = []
                for col_index in range(self.ui.gridLayout.columnCount()):
                    widget_item = self.ui.gridLayout.itemAtPosition(row_index, col_index)
                    if widget_item:
                        widgets.append(widget_item.widget())
                # Сбор данных из виджетов
                if widgets:
                    row_id = widgets[0].objectName().split("_")[1]  # Получаем ID строки из имени виджета
                    updated_rows[row_id] = widgets
            except Exception as e:
                pass
        self.rows = updated_rows

    # Обновление состояний (disable) при включении чекбоксов
    def update_widget_states(self):
        for row_id, widgets in self.rows.items():  # Проходим по всем строкам в self.rows
            if row_id == '0':
                continue  # Пропускаем строку 'id'
            if widgets is None or len(widgets) < 7:
                continue  # Пропускаем строки, если они пустые или не содержат необходимых виджетов

            # Получаем виджеты для текущей строки
            type_data_combo_box = widgets[1]
            pk_checkbox = widgets[2].layout().itemAt(0).widget() if widgets[2].layout() else None
            nn_checkbox = widgets[3].layout().itemAt(0).widget() if widgets[3].layout() else None
            uq_checkbox = widgets[4].layout().itemAt(0).widget() if widgets[4].layout() else None
            blob_checkbox = widgets[5].layout().itemAt(0).widget() if widgets[5].layout() else None
            unsigned_checkbox = widgets[6].layout().itemAt(0).widget() if widgets[6].layout() else None

            # Проверяем, все ли виджеты корректно получены
            if not all([type_data_combo_box, pk_checkbox, nn_checkbox, uq_checkbox, blob_checkbox, unsigned_checkbox]):
                continue  # Пропускаем строки, если какие-то виджеты отсутствуют

            # Значения текущих виджетов
            type_data = type_data_combo_box.currentText().strip()
            pk = pk_checkbox.isChecked()
            blob = blob_checkbox.isChecked()
            unsigned = unsigned_checkbox.isChecked()

            # Обновление состояний виджетов на основе состояния PRIMARY KEY
            if pk:
                nn_checkbox.setEnabled(False)
                uq_checkbox.setEnabled(False)
                nn_checkbox.setChecked(False)
                uq_checkbox.setChecked(False)
            else:
                nn_checkbox.setEnabled(True)
                uq_checkbox.setEnabled(True)

            # Обновление состояния для BLOB
            if blob:
                # Если выбран BLOB, нельзя выбрать тип данных, изменим состояние
                #type_data_combo_box.setCurrentText("BLOB")
                type_data_combo_box.setCurrentIndex(0)
                type_data_combo_box.setEnabled(False)
                for i in range(type_data_combo_box.count()):
                    if type_data_combo_box.itemText(i) != "BLOB":
                        type_data_combo_box.model().item(i).setEnabled(False)
            else:
                # Если BLOB не выбран, разрешаем редактирование других типов данных
                type_data_combo_box.setEnabled(True)
                for i in range(type_data_combo_box.count()):
                    type_data_combo_box.model().item(i).setEnabled(True)

            # Обновление состояния для UNSIGNED
            if unsigned:
                for i in range(type_data_combo_box.count()):
                    if type_data_combo_box.itemText(i) not in ["INTEGER", "REAL"]:
                        type_data_combo_box.model().item(i).setEnabled(False)
                    else:
                        type_data_combo_box.model().item(i).setEnabled(True)
            else:
                for i in range(type_data_combo_box.count()):
                    type_data_combo_box.model().item(i).setEnabled(True)

            # Если выбран тип данных INTEGER или REAL, включаем поддержку UNSIGNED
            if type_data in ["INTEGER", "REAL"]:
                unsigned_checkbox.setEnabled(True)
            else:
                unsigned_checkbox.setEnabled(False)
                unsigned_checkbox.setChecked(False)

            # Если тип данных DATE или DATETIME, выключаем поддержку BLOB
            if type_data in ["DATE", "DATETIME"]:
                blob_checkbox.setEnabled(False)
                blob_checkbox.setChecked(False)
            else:
                blob_checkbox.setEnabled(True)
        self.refresh_data()

    # Сохранить новую таблицу. Выполнение SQL-запроса к базе
    def save(self, db_name, db_path):
        self.refresh_data()  # Обновляем данные строк
        table_name = self.ui.TableName.text().strip()

        if not table_name:
            self.show_message("Ошибка", "Укажите имя таблицы.", QMessageBox.Warning)
            logging.warning("Не указано имя таблицы.")
            return

        # Подключение к базе данных
        full_db_path = os.path.join(db_path, db_name)
        db_connection = SQLiteConnection(full_db_path)
        db_connection.connect()

        if not db_connection.connection:
            self.show_message("Ошибка", f"Не удалось подключиться к базе данных: {db_name}.", QMessageBox.Critical)
            logging.error(f"Не удалось подключиться к базе данных {db_name}.")
            return

        # Проверка на существование таблицы
        existing_tables = db_connection.get_tables()
        if table_name in existing_tables:
            self.show_message(
                "Ошибка",
                f"Таблица с именем '{table_name}' уже существует в базе данных.",
                QMessageBox.Warning
            )
            logging.warning(f"Таблица '{table_name}' уже существует. Создание таблицы отменено.")
            db_connection.close()
            return

        # Список столбцов для создания таблицы
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]  # Добавляем автоинкрементный ID
        additional_columns = []  # Список для хранения дополнительных столбцов

        for row_id, widgets in self.rows.items():
            if row_id == '0':
                continue  # Пропускаем строку 'id'

            name = widgets[0].text().strip()
            type_data = widgets[1].currentText().strip()
            pk = widgets[2].layout().itemAt(0).widget().isChecked()
            nn = widgets[3].layout().itemAt(0).widget().isChecked()
            uq = widgets[4].layout().itemAt(0).widget().isChecked()
            blob = widgets[5].layout().itemAt(0).widget().isChecked()
            unsigned = widgets[6].layout().itemAt(0).widget().isChecked()

            if not name or type_data == "Выберите...":
                self.show_message("Ошибка", f"Укажите имя и тип данных для атрибута '{name}'.", QMessageBox.Warning)
                logging.warning(f"Для атрибута '{name}' не указаны имя или тип данных.")
                db_connection.close()
                return  # Прерываем сохранение, так как есть незаполненные поля

            constraints = []
            if pk:
                self.show_message("Ошибка", "Только поле 'id' может быть PRIMARY KEY.", QMessageBox.Warning)
                logging.warning("Попытка назначить PRIMARY KEY для другого поля.")
                db_connection.close()
                return  # Прерываем сохранение
            if nn:
                constraints.append("NOT NULL")
                # **Добавляем CHECK-ограничение для предотвращения вставки пустых строк**
                constraints.append(f"CHECK({name} <> '')")
            if uq:
                constraints.append("UNIQUE")
            if unsigned and type_data in ["INTEGER", "REAL"]:
                constraints.append(f"CHECK ({name} >= 0)")
            if blob and type_data == "BLOB":
                constraints.append("BLOB")

            column_definition = f"{name} {type_data} {' '.join(constraints)}"
            additional_columns.append(column_definition)

        if not additional_columns:
            self.show_message("Ошибка", "Необходимо добавить хотя бы одно поле помимо 'id'.", QMessageBox.Warning)
            logging.warning("Попытка создать таблицу без дополнительных полей.")
            db_connection.close()
            return

        # Объединяем колонки
        columns.extend(additional_columns)

        create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)});"
        logging.info(f"Созданный запрос: {create_table_query}")

        try:
            # Выполнение запроса с использованием execute_query
            db_connection.execute_query(create_table_query)
            logging.info(f"Таблица {table_name} успешно создана.")

            # Фиксация изменений
            db_connection.connection.commit()

            # Уведомление об успешном создании
            self.show_message("Успех", f"Таблица {table_name} успешно создана.", QMessageBox.Information)
        except sqlite3.Error as e:
            self.show_message("Ошибка", f"Ошибка при создании таблицы: {e}", QMessageBox.Critical)
            logging.error(f"Ошибка при создании таблицы {table_name}: {e}")
        finally:
            db_connection.close()
            logging.info(f"Соединение с базой данных {db_name} закрыто.")

    def show_message(self, title, text, icon):
        """Показывает сообщение с указанным текстом."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setIcon(icon)
        msg_box.exec()