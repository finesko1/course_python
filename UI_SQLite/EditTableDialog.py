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



# Окно удаления таблицы
class EditTableDialog(QDialog):
    def __init__(self, db_name, db_path, table_name):
        super().__init__()
        # Инициализация UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.db_name = db_name
        self.db_path = db_path
        self.table_name = table_name

        # Устанавливаем имя таблицы
        self.ui.TableName.setText(self.table_name)
        self.ui.TableName.setReadOnly(False)

        self.ui.WindowHeaderLabel.setText(f"Редактирование таблицы: {self.table_name} в базе данных: {self.db_name}")

        # Иконки для кнопок
        self.add_icon = QIcon()
        self.add_icon.addFile(u":/icons/icons/add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.del_icon = QIcon()
        self.del_icon.addFile(u":/icons/icons/delete.svg", QSize(), QIcon.Normal, QIcon.Off)

        # Словарь для хранения строк
        self.rows = {}

        # Подключение к базе данных
        self.full_db_path = os.path.join(self.db_path, self.db_name)
        self.db_connection = SQLiteConnection(self.full_db_path)
        self.db_connection.connect()

        # Очищаем gridLayout перед добавлением новых виджетов
        self.clear_grid_layout()

        # Добавляем заголовки
        self.add_header_labels()

        # Загрузка структуры таблицы
        self.load_table_structure()

        # Подключаем кнопку "Сохранить"
        self.ui.SaveButton.clicked.connect(lambda: self.save_changes())

        # Инициализация состояния виджетов
        self.update_widget_states()

    def add_header_labels(self):
        """Добавляет заголовки в gridLayout."""
        headers = [
            ("AttributeLabel", "Атрибут", 0),
            ("TypeLabel", "Тип", 1),
            ("PKLabel", "PK", 2),
            ("NNLabel", "NN", 3),
            ("UQLabel", "UQ", 4),
            ("BLabel", "B", 5),
            ("UNLabel", "UN", 6),
            ("EmptyLabel1", "", 7),
            ("EmptyLabel2", "", 8),
        ]

        for obj_name, text, col in headers:
            label = QLabel(text, self.ui.scrollAreaWidgetContents)
            label.setObjectName(obj_name)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setMargin(4)
            self.ui.gridLayout.addWidget(label, 0, col, 1, 1)

    def get_unique_columns(self, table_name):
        """Возвращает список имен столбцов с уникальными ограничениями."""
        unique_columns = set()
        cursor = self.db_connection.connection.cursor()
        try:
            # Получаем список индексов с уникальными ограничениями
            cursor.execute(f"PRAGMA index_list(`{table_name}`);")
            indexes = cursor.fetchall()
            for index in indexes:
                index_name = index[1]
                is_unique = index[2]
                if is_unique:
                    # Получаем список столбцов в индексе
                    cursor.execute(f"PRAGMA index_info(`{index_name}`);")
                    index_info = cursor.fetchall()
                    for info in index_info:
                        column_name = info[2]
                        unique_columns.add(column_name)
        except sqlite3.Error as e:
            logging.error(f"Ошибка при получении уникальных ограничений для таблицы '{table_name}': {e}")
        finally:
            cursor.close()
        return list(unique_columns)

    def load_table_structure(self):
        """Загружает текущую структуру таблицы и отображает ее в интерфейсе."""
        # Получаем информацию о столбцах таблицы
        pragma_query = f"PRAGMA table_info(`{self.table_name}`);"
        columns_info = self.db_connection.execute_query(pragma_query, is_select=True)
        if not columns_info:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить структуру таблицы {self.table_name}.")
            self.close()
            return

        # Получаем столбцы с уникальными ограничениями
        unique_columns = self.get_unique_columns(self.table_name)

        # Начинаем добавлять строки с индекса 1, так как 0 занят заголовками
        current_row = 1

        # Добавляем строки в gridLayout на основе columns_info
        for col_info in columns_info:
            cid, name, type_data, notnull, dflt_value, pk = col_info

            row_id = str(uuid.uuid4())

            # Создаем виджеты для строки
            line_edit = QLineEdit(self)
            line_edit.setText(name)
            line_edit.old_name = name

            type_data_combo_box = QComboBox(self)
            type_data_combo_box.addItems(
                ["Выберите...", "TEXT", "INTEGER", "REAL", "DATE", "DATETIME", "BOOLEAN", "BLOB"])
            index = type_data_combo_box.findText(type_data.upper())
            if index != -1:
                type_data_combo_box.setCurrentIndex(index)
            else:
                type_data_combo_box.setCurrentIndex(0)

            # Создаём чекбоксы
            pk_checkbox = QCheckBox("", self)
            pk_checkbox.setChecked(pk == 1)
            pk_checkbox.setEnabled(False)  # Делаем невозможным редактирование чекбокса PK

            nn_checkbox = QCheckBox("", self)
            nn_checkbox.setChecked(notnull == 1)

            uq_checkbox = QCheckBox("", self)
            uq_checkbox.setChecked(name in unique_columns)  # Отмечаем, если столбец имеет уникальное ограничение
            uq_checkbox.setEnabled(False)  # Делаем невозможным редактирование чекбокса UQ для существующих полей

            b_checkbox = QCheckBox("", self)
            # Если тип данных столбца BLOB, отмечаем чекбокс B
            is_blob = type_data.upper() == "BLOB"
            b_checkbox.setChecked(is_blob)
            if is_blob:
                # Отключаем возможность выбора других типов данных
                type_data_combo_box.setEnabled(False)
                # Блокируем изменение чекбокса B для столбцов типа BLOB
                b_checkbox.setEnabled(False)

            un_checkbox = QCheckBox("", self)
            # Пока нет информации об использовании UNSIGNED, осталяем его неотмеченным и активным

            add_button = QPushButton()
            add_button.setIcon(self.add_icon)
            add_button.clicked.connect(self.add_row)

            delete_button = QPushButton()
            delete_button.setIcon(self.del_icon)
            delete_button.clicked.connect(lambda checked, rid=row_id: self.remove_row(rid))

            # Оборачиваем чекбоксы в QWidget с QVBoxLayout
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

            # Если это столбец 'id', делаем его только для чтения
            if name == 'id':
                line_edit.setReadOnly(True)
                type_data_combo_box.setEnabled(False)
                nn_checkbox.setEnabled(False)
                uq_checkbox.setEnabled(False)
                b_checkbox.setEnabled(False)
                un_checkbox.setEnabled(False)
                delete_button.setEnabled(False)

            # Собираем виджеты в список
            widgets = [
                line_edit,
                type_data_combo_box,
                pk_widget,  # Используем обернутый виджет
                nn_widget,  # Используем обернутый виджет
                uq_widget,  # Используем обернутый виджет
                b_widget,  # Используем обернутый виджет
                un_widget,  # Используем обернутый виджет
                add_button,
                delete_button,
            ]

            # Добавляем виджеты в gridLayout в правильную строку
            for col_index, widget in enumerate(widgets):
                self.ui.gridLayout.addWidget(widget, current_row, col_index)

            # Сохраняем виджеты строки в словаре
            self.rows[row_id] = widgets

            # Подключаем сигналы для обновления состояний виджетов
            type_data_combo_box.currentIndexChanged.connect(self.update_widget_states)
            nn_checkbox.stateChanged.connect(self.update_widget_states)
            b_checkbox.stateChanged.connect(self.update_widget_states)
            un_checkbox.stateChanged.connect(self.update_widget_states)

            # Переходим к следующей строке
            current_row += 1

        # Инициализируем состояние виджетов после загрузки структуры
        self.update_widget_states()


    def add_row(self):
        """Добавляет новую строку для столбца."""
        row_id = str(uuid.uuid4())

        # Создаем виджеты для новой строки
        line_edit = QLineEdit(self)
        line_edit.old_name = None
        type_data_combo_box = QComboBox(self)
        type_data_combo_box.addItems(["Выберите...", "TEXT", "INTEGER", "REAL", "DATE", "DATETIME", "BOOLEAN"])

        pk_checkbox = QCheckBox("", self)
        pk_checkbox.setEnabled(False)
        nn_checkbox = QCheckBox("", self)
        uq_checkbox = QCheckBox("", self)
        b_checkbox = QCheckBox("", self)
        un_checkbox = QCheckBox("", self)

        add_button = QPushButton()
        add_button.setIcon(self.add_icon)
        add_button.clicked.connect(self.add_row)

        delete_button = QPushButton()
        delete_button.setIcon(self.del_icon)
        delete_button.clicked.connect(lambda checked, rid=row_id: self.remove_row(rid))

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

        # Обновляем состояния виджетов
        self.update_widget_states()

    def get_column_names(self, table_name):
        """Получает имена столбцов указанной таблицы."""
        query = f"PRAGMA table_info({table_name});"
        columns_info = self.db_connection.execute_query(query)
        return [col[1] for col in columns_info]

    def remove_row(self, row_id):
        """Удаляет строку с указанным row_id."""
        if row_id in self.rows:
            widgets = self.rows.pop(row_id)
            for widget in widgets:
                self.ui.gridLayout.removeWidget(widget)
                widget.setParent(None)

    def save_changes(self):
        """Сохраняет изменения структуры таблицы, включая изменение названий атрибутов."""
        new_table_name = self.ui.TableName.text().strip()
        if not new_table_name:
            QMessageBox.warning(self, "Ошибка", "Имя таблицы не может быть пустым.")
            logging.warning("Не указано имя таблицы.")
            return

        # Проверяем, изменилось ли имя таблицы
        table_name_changed = new_table_name != self.table_name

        # Проверяем, если новое имя таблицы уже существует
        existing_tables = self.db_connection.get_tables()
        if table_name_changed and new_table_name in existing_tables:
            QMessageBox.warning(self, "Ошибка", f"Таблица с именем '{new_table_name}' уже существует.")
            logging.warning(f"Таблица '{new_table_name}' уже существует. Создание таблицы отменено.")
            return

        # Предупреждаем пользователя о потенциальной потере данных
        reply = QMessageBox.question(
            self,
            "Подтверждение изменений",
            f"Вы уверены, что хотите сохранить изменения структуры таблицы '{self.table_name}'? Это может привести к потере данных.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        # Собираем новые определения столбцов и соответствие старых и новых имен
        columns = []
        column_names = []
        old_to_new_column_names = {}
        notnull_columns = []

        for row_id, widgets in self.rows.items():
            line_edit = widgets[0]
            name = line_edit.text().strip()
            old_name = getattr(line_edit, 'old_name', None)
            type_data = widgets[1].currentText().strip()

            if not name or type_data == "Выберите...":
                QMessageBox.warning(self, "Ошибка", f"Укажите имя и тип данных для атрибута '{name}'.")
                logging.warning(f"Для атрибута '{name}' не указаны имя или тип данных.")
                return  # Прерываем сохранение, так как есть незаполненные поля

            # Получаем чекбоксы из контейнера QWidget
            pk_widget = widgets[2]
            nn_widget = widgets[3]
            uq_widget = widgets[4]
            blob_widget = widgets[5]
            unsigned_widget = widgets[6]

            pk_checkbox = pk_widget.layout().itemAt(0).widget() if pk_widget.layout() else None
            nn_checkbox = nn_widget.layout().itemAt(0).widget() if nn_widget.layout() else None
            uq_checkbox = uq_widget.layout().itemAt(0).widget() if uq_widget.layout() else None
            blob_checkbox = blob_widget.layout().itemAt(0).widget() if blob_widget.layout() else None
            unsigned_checkbox = unsigned_widget.layout().itemAt(0).widget() if unsigned_widget.layout() else None

            pk = pk_checkbox.isChecked()
            nn = nn_checkbox.isChecked()
            uq = uq_checkbox.isChecked()
            blob = blob_checkbox.isChecked()
            unsigned = unsigned_checkbox.isChecked()

            constraints = []
            if pk:
                if name != 'id':
                    QMessageBox.warning(self, "Ошибка", "Только поле 'id' может быть PRIMARY KEY.")
                    logging.warning("Попытка назначить PRIMARY KEY для другого поля.")
                    return  # Прерываем сохранение
                else:
                    constraints.append("PRIMARY KEY AUTOINCREMENT")
            if nn:
                constraints.append("NOT NULL")
                notnull_columns.append(name)
            if uq:
                constraints.append("UNIQUE")
            if unsigned and type_data in ["INTEGER", "REAL"]:
                constraints.append(f"CHECK ({name} >= 0)")
            if blob and type_data == "BLOB":
                type_data = "BLOB"

            column_definition = f"`{name}` {type_data} {' '.join(constraints)}"
            columns.append(column_definition)
            column_names.append(name)

            # Проверяем, является ли это изменение имени существующего столбца
            if old_name and old_name != name:
                old_to_new_column_names[old_name] = name

        if not columns:
            QMessageBox.warning(self, "Ошибка", "Необходимо добавить хотя бы одно поле помимо 'id'.")
            logging.warning("Попытка создать таблицу без дополнительных полей.")
            return

        create_table_query = f"CREATE TABLE `{new_table_name}` ({', '.join(columns)});"
        logging.info(f"Созданный запрос: {create_table_query}")

        temp_table_name = f"{self.table_name}_old"

        try:
            # Начинаем транзакцию
            self.db_connection.execute_query('BEGIN TRANSACTION;', commit=False)

            # 1. Переименовываем старую таблицу
            self.db_connection.execute_query(f"ALTER TABLE `{self.table_name}` RENAME TO `{temp_table_name}`;",
                                             commit=False)

            # 2. Создаем новую таблицу
            self.db_connection.execute_query(create_table_query, commit=False)

            # 3. Переносим данные с учетом переименования столбцов
            old_columns_info = self.db_connection.get_table_structure(temp_table_name)
            old_column_names = [col['name'] for col in old_columns_info]

            common_columns = []
            for old_name in old_column_names:
                new_name = old_to_new_column_names.get(old_name, old_name)
                if new_name in column_names:
                    common_columns.append((old_name, new_name))

            if common_columns:
                columns_for_insert = ', '.join([f'`{col[1]}`' for col in common_columns])
                columns_for_select = ', '.join([f'`{col[0]}`' for col in common_columns])
                insert_data_query = f"INSERT INTO `{new_table_name}` ({columns_for_insert}) SELECT {columns_for_select} FROM `{temp_table_name}`;"
                self.db_connection.execute_query(insert_data_query, commit=False)

            # 4. Удаляем временную таблицу
            self.db_connection.execute_query(f"DROP TABLE `{temp_table_name}`;", commit=False)

            # Фиксируем транзакцию
            self.db_connection.execute_query('COMMIT;', commit=False)

            QMessageBox.information(self, "Успех", f"Таблица '{new_table_name}' успешно обновлена.")
            self.table_name = new_table_name
        except Exception as e:
            # Откатываем транзакцию
            self.db_connection.execute_query('ROLLBACK;', commit=False)
            logging.error(f"Ошибка при обновлении таблицы {new_table_name}: {e}")

            # Проверяем, существует ли временная таблица, и удаляем ее
            try:
                self.db_connection.execute_query(f"DROP TABLE IF EXISTS `{temp_table_name}`;", commit=True)
                logging.info(f"Временная таблица `{temp_table_name}` удалена.")
            except Exception as drop_ex:
                logging.error(f"Ошибка при удалении временной таблицы `{temp_table_name}`: {drop_ex}")

            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении таблицы: {e}")
        finally:
            pass

    def clear_grid_layout(self):
        """Очищает все виджеты из gridLayout."""
        layout = self.ui.gridLayout
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item.widget():
                widget = item.widget()
                layout.removeWidget(widget)
                widget.setParent(None)

    def closeEvent(self, event):
        # Закрываем соединение с базой данных
        if self.db_connection:
            self.db_connection.close()
        event.accept()

    def update_widget_states(self):
        """Обновляет состояния виджетов в строках в зависимости от выбранных значений."""
        for row_id, widgets in self.rows.items():
            if widgets is None or len(widgets) < 9:
                continue  # Пропускаем строки, если они пустые или не содержат необходимых виджетов

            # Получаем виджеты для текущей строки
            line_edit = widgets[0]
            type_data_combo_box = widgets[1]
            pk_checkbox = widgets[2].layout().itemAt(0).widget() if widgets[2].layout() else None
            nn_checkbox = widgets[3].layout().itemAt(0).widget() if widgets[3].layout() else None
            uq_checkbox = widgets[4].layout().itemAt(0).widget() if widgets[4].layout() else None
            b_checkbox = widgets[5].layout().itemAt(0).widget() if widgets[5].layout() else None
            un_checkbox = widgets[6].layout().itemAt(0).widget() if widgets[6].layout() else None
            add_button = widgets[7]
            delete_button = widgets[8]

            # Проверяем, все ли виджеты корректно получены
            if not all(
                    [line_edit, type_data_combo_box, pk_checkbox, nn_checkbox, uq_checkbox, b_checkbox, un_checkbox]):
                continue  # Пропускаем строки, если какие-то виджеты отсутствуют

            # Значения текущих виджетов
            type_data = type_data_combo_box.currentText().strip()
            pk = pk_checkbox.isChecked()
            nn = nn_checkbox.isChecked()
            uq = uq_checkbox.isChecked()
            blob = b_checkbox.isChecked()
            unsigned = un_checkbox.isChecked()
            if type_data == "BLOB":
                b_checkbox.setChecked(True)
                b_checkbox.setEnabled(False)
                # Отключаем возможность выбора других типов данных
                type_data_combo_box.setEnabled(False)
                for i in range(type_data_combo_box.count()):
                    if type_data_combo_box.itemText(i) != "BLOB":
                        type_data_combo_box.model().item(i).setEnabled(False)
            else:
                b_checkbox.setEnabled(True)
                # Включаем выбор типов данных, кроме BLOB, если чекбокс не отмечен
                if not blob:
                    type_data_combo_box.setEnabled(True)
                    for i in range(type_data_combo_box.count()):
                        type_data_combo_box.model().item(i).setEnabled(True)
                    # Исключаем BLOB, если чекбокс не отмечен
                    index = type_data_combo_box.findText("BLOB")
                    if index != -1:
                        type_data_combo_box.model().item(index).setEnabled(False)
                else:
                    # Если чекбокс B отмечен, устанавливаем тип данных BLOB
                    type_data_combo_box.setCurrentText("BLOB")
                    type_data_combo_box.setEnabled(False)
                    for i in range(type_data_combo_box.count()):
                        if type_data_combo_box.itemText(i) != "BLOB":
                            type_data_combo_box.model().item(i).setEnabled(False)

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
                type_data_combo_box.setCurrentText("BLOB")
                type_data_combo_box.setEnabled(False)
                # Отключаем другие типы данных
                for i in range(type_data_combo_box.count()):
                    if type_data_combo_box.itemText(i) != "BLOB":
                        type_data_combo_box.model().item(i).setEnabled(False)
            else:
                # Если тип данных был BLOB и флажок снят, сбрасываем тип данных
                if type_data == "BLOB":
                    type_data_combo_box.setCurrentIndex(0)
                type_data_combo_box.setEnabled(True)
                # Включаем все типы данных
                for i in range(type_data_combo_box.count()):
                    type_data_combo_box.model().item(i).setEnabled(True)

            # Обновление состояния для UNSIGNED
            if unsigned:
                # Проверяем, выбран ли корректный тип данных
                if type_data not in ["INTEGER", "REAL"]:
                    type_data_combo_box.setCurrentText("INTEGER")
                # Отключаем недопустимые типы данных
                for i in range(type_data_combo_box.count()):
                    if type_data_combo_box.itemText(i) not in ["INTEGER", "REAL"]:
                        type_data_combo_box.model().item(i).setEnabled(False)
                    else:
                        type_data_combo_box.model().item(i).setEnabled(True)
            else:
                # Включаем все типы данных
                for i in range(type_data_combo_box.count()):
                    type_data_combo_box.model().item(i).setEnabled(True)

            # Если выбран тип данных INTEGER или REAL, включаем поддержку UNSIGNED
            if type_data in ["INTEGER", "REAL"]:
                un_checkbox.setEnabled(True)
            else:
                un_checkbox.setEnabled(False)
                un_checkbox.setChecked(False)

            # Если тип данных DATE или DATETIME, выключаем поддержку BLOB
            if type_data in ["DATE", "DATETIME"]:
                b_checkbox.setEnabled(False)
                b_checkbox.setChecked(False)
            else:
                b_checkbox.setEnabled(True)

            # Особая обработка для столбца 'id'
            if line_edit.text().strip() == 'id':
                line_edit.setReadOnly(True)
                type_data_combo_box.setEnabled(False)
                pk_checkbox.setEnabled(False)
                nn_checkbox.setEnabled(False)
                uq_checkbox.setEnabled(False)
                b_checkbox.setEnabled(False)
                un_checkbox.setEnabled(False)
                delete_button.setEnabled(False)