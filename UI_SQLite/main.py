import logging
import os
import sqlite3
import sys
import time

from PySide6.QtCore import QSize, Qt, QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QVBoxLayout, QTextEdit, QMessageBox, \
    QTableWidgetItem, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QLayout, QDialog, QLineEdit, \
    QComboBox, QCheckBox, QHeaderView
import uuid

from AutoCompleter import AutoCompleteTextEdit
from EditTableDialog import EditTableDialog
from SQLHighlighter import SQLSyntaxHighlighter
from SQLite import Ui_MainWindow  # Импорт вашего файла с UI-классом
# Управление подключением к БД
from SQLite_connect import SQLiteConnection

# Диалоговое окно добавления таблицы в БД
from AddTableDialog import AddTableDialog
# Окно с информацией о разработчике
from DevInfoDialog import DevInfoDialog
# О программе
from ProgInfoDialog import ProgInfoDialog
# Создание БД
from CreateDatabaseDialog import CreateDbDialog
# Настройки программы
from SettingsDialog import SettingsDialog

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.last_db = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Начальные данные
        self.work_directory = None
        self.current_database = None
        self.connection = None
        self.cursor = None
        # tabs
        self.last_tab_number = 0  # Хранит индекс вкладки

        # Начальные параметры окон
        self.ui.TabWidget.setMinimumHeight(250)
        # Создаём макет для вкладки tab
        self.tab_layout = QVBoxLayout(self.ui.tab)  # Макет для размещения виджетов внутри tab
        # Добавляем QTextEdit в вкладку tab
        self.query_editor = AutoCompleteTextEdit(self.ui.tab)
        self.query_editor.setPlaceholderText("Введите SQL-запрос...")
        self.tab_layout.addWidget(self.query_editor)  # Растянуть текстовое поле по вкладке, вертикальный компоновщик

        # Инициализация иконок
        # Добавление
        self.icon1 = QIcon()
        self.icon1.addFile(u":/icons/icons/add.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        # Удаление
        self.icon2 = QIcon()
        self.icon2.addFile(u":/icons/icons/delete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        # Кнопка для показа таблиц
        self.icon3 = QIcon()
        self.icon3.addFile(u":/icons/icons/arrow_forward.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        # Изменить
        self.icon4 = QIcon()
        self.icon4.addFile(u":/icons/icons/edit.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        # Развернуть
        self.icon5 = QIcon()
        self.icon5.addFile(u":/icons/icons/forward.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        # Свернуть
        self.icon6 = QIcon()
        self.icon6.addFile(u":/icons/icons/drop_down.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        # Инициализация списка БД
        self.clear_layout(self.ui.DatabasesVBoxLayoutForWidget)

        # Начальные данные
        self.work_directory = None
        self.current_database = None
        self.connection = None
        self.cursor = None
        # Словарь для хранения соответствия индекс -> UUID (QTableWidget)
        self.row_data_map = {}
        # Текущая бд и таблица
        self.curr_db_name = None
        self.curr_table_name = None
        # Список для id
        self.new_ids_in_use = set()
        # Для выполнения запроса
        self.current_database = None

        # Настройки программы
        # Отображать все таблицы баз данных
        self.show_all_tables = False
        # Подключаем подсветку синтаксиса
        self.highlighter = SQLSyntaxHighlighter(self.query_editor)
        self.highlighter.completer.activated.connect(self.highlighter.insert_completion)

        # Инициализация политик выравниваний
        # Главное окно
        self.sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(self.ui.centralwidget.sizePolicy().hasHeightForWidth())
        # Для строки с выбором директории
        self.sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.sizePolicy1.setHorizontalStretch(0)
        self.sizePolicy1.setVerticalStretch(0)
        self.sizePolicy1.setHeightForWidth(self.ui.WorkDirectoryLabel.sizePolicy().hasHeightForWidth())
        # Выбор БД, кнопка
        self.sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.sizePolicy2.setHorizontalStretch(0)
        self.sizePolicy2.setVerticalStretch(0)
        self.sizePolicy2.setHeightForWidth(self.ui.SelectFolderButton.sizePolicy().hasHeightForWidth())

        # Подключение сигналов к кнопкам
        # Выбор директории
        self.ui.SelectFolderButton.clicked.connect(self.read_work_directory)
        # Управление SQL вкладками
        self.ui.AddQueryButton.clicked.connect(self.add_query_tab)
        self.ui.DelQueryButton.clicked.connect(self.del_current_tab)
        # Выполнение запроса
        self.ui.ExecuteQueryButton.clicked.connect(self.execute_query)
        #self.ui.SaveChangesButton.clicked.connect(lambda checked, db_name = self.curr_db_name, table_name = self.curr_table_name: self.save_changes(db_name, table_name))
        # Кнопки меню
        self.ui.DeveloperInfoAction.triggered.connect(self.developer_info)
        self.ui.ProgrammInfoAction.triggered.connect(self.program_info)
        self.ui.SettingsAction.triggered.connect(self.settings_action)
        self.ui.SaveChangesButton.clicked.connect(lambda checked, db = self.curr_db_name, table = self.curr_table_name:self.save_changes(db, table))
        # Изменения в таблице
        self.ui.tableWidget.itemChanged.connect(self.on_item_changed)

    def closeEvent(self, event):
        # Закрываем все соединения с базой данных
        if self.connection:
            self.connection.close()
            self.connection = None
        event.accept()

    def close_resources(self):
        # Закрываем все соединения с базой данных
        if self.connection:
            self.connection.close()
            self.connection = None

    # Анализ рабочей директории (считывание файлов БД sqlite и db)
    def read_work_directory(self):
        selected_directory = QFileDialog.getExistingDirectory(self, "Выбрать рабочую директорию")
        if selected_directory:
            self.work_directory = os.path.normpath(selected_directory)
            self.ui.SelectWorkDirectoryLabel.setText(self.work_directory)
            self.refresh_databases()

    # Обновляет список баз данных в указанной рабочей директории + отображение списка БД
    def refresh_databases(self):
        # Очистка текущего списка баз данных в интерфейсе
        self.clear_layout(self.ui.DatabasesVBoxLayoutForWidget)
        if not self.work_directory:
            return

        databases = []  # Список баз данных в директории

        # Поиск файлов с расширениями .db и .sqlite
        for root, dirs, files in os.walk(self.work_directory):
            for file in files:
                if file.lower().endswith('.db') or file.endswith('.sqlite'):
                    databases.append(file)

        # Если базы данных найдены, отображаем их
        if databases:
            # Создаем горизонтальный layout
            db_hs_layout = QHBoxLayout()
            db_hs_layout.setContentsMargins(0, 0, 0, 5)

            db_label = QLabel("Создать базу данных")
            db_label.setObjectName("AddDatabasesLabel")
            db_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            db_label.setSizePolicy(QSizePolicy.Policy.Expanding,
                                   QSizePolicy.Policy.Preferred)
            db_hs_layout.addWidget(db_label)

            # Кнопка "Добавить базу данных"
            add_database_button = QPushButton()
            add_database_button.setIcon(self.icon1)
            add_database_button.setObjectName("AddDatabaseButton")
            add_database_button.setToolTip("Создать базу данных")
            add_database_button.setSizePolicy(QSizePolicy.Policy.Expanding,
                                              QSizePolicy.Policy.Preferred)  # Устанавливаем политику размера
            add_database_button.clicked.connect(lambda checked, work_directory=self.work_directory: self.on_add_database_clicked(work_directory))  # Привязываем обработчик
            db_hs_layout.addWidget(add_database_button)

            # Добавляем горизонтальный layout в основной VBoxLayout
            self.ui.DatabasesVBoxLayoutForWidget.addLayout(db_hs_layout)

            # Отображаем каждую базу данных
            for db_name in databases:
                db_hs = QHBoxLayout()
                db_hs.setObjectName(f"DB_HS_{db_name}")
                db_hs.setContentsMargins(-1, -1, -1, 5)

                db_label = QLabel(db_name)
                db_label.setObjectName(f"Label_{db_name}")
                db_hs.addWidget(db_label)

                spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
                db_hs.addItem(spacer)

                delete_database_button = QPushButton()
                delete_database_button.setObjectName(f"DeleteDatabaseButton_{db_name}")
                delete_database_button.setToolTip("Удалить базу данных")
                delete_database_button.setIcon(self.icon2)
                delete_database_button.setIconSize(QSize(16, 20))
                db_hs.addWidget(delete_database_button)
                db_hs.addSpacing(2)

                add_table_button = QPushButton("Таблица")
                add_table_button.setObjectName(f"AddTableButton_{db_name}")
                add_table_button.setToolTip("Добавить таблицу в базу данных")
                add_table_button.setIcon(self.icon1)
                add_table_button.setIconSize(QSize(16, 20))
                db_hs.addWidget(add_table_button)
                db_hs.addSpacing(2)


                # Переключение иконок при нажатии на кнопку
                toggle_button = QPushButton()
                toggle_button.setObjectName(f"ToggleDatabaseButton_{db_name}")
                toggle_button.setToolTip("Показать содержимое базы данных")
                toggle_button.setIcon(self.icon3)
                toggle_button.setIconSize(QSize(16, 20))
                toggle_button.state = False
                db_hs.addWidget(toggle_button)

                # обработчики
                delete_database_button.clicked.connect(lambda checked, db=db_name: self.on_del_database_clicked(db))
                add_table_button.clicked.connect(lambda checked, db=db_name, db_path=self.work_directory, button=toggle_button: self.on_add_table_clicked(db, db_path, button))
                toggle_button.clicked.connect(lambda checked, db=db_name, button=toggle_button: self.on_read_db_clicked(db, button))
                self.ui.DatabasesVBoxLayoutForWidget.addLayout(db_hs)
        else:
            # Создаем горизонтальный layout
            db_hs_layout = QHBoxLayout()
            db_hs_layout.setContentsMargins(0, 0, 0, 5)

            # Надпись "Нет баз данных"
            db_label = QLabel("Создать базу данных")
            db_label.setObjectName("AddDatabasesLabel")
            db_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            db_label.setSizePolicy(QSizePolicy.Policy.Expanding,
                                   QSizePolicy.Policy.Preferred)  # Устанавливаем политику размера
            db_hs_layout.addWidget(db_label)

            # Кнопка "Добавить базу данных"
            add_database_button = QPushButton()
            add_database_button.setIcon(self.icon1)
            add_database_button.setObjectName("AddDatabaseButton")
            add_database_button.setSizePolicy(QSizePolicy.Policy.Expanding,
                                              QSizePolicy.Policy.Preferred)  # Устанавливаем политику размера
            add_database_button.clicked.connect(
                lambda checked, work_directory=self.work_directory: self.on_add_database_clicked(work_directory))
            db_hs_layout.addWidget(add_database_button)

            # Добавляем горизонтальный layout в основной VBoxLayout
            self.ui.DatabasesVBoxLayoutForWidget.addLayout(db_hs_layout)
            return

    # Вызов окна с созданием таблицы БД
    def on_add_table_clicked(self, db_name, db_path, button):
        #print(f"Добавление таблицы для базы данных: {db_name}")
        dialog = AddTableDialog(db_name, db_path)
        dialog.exec()
        # Обновление списка
        self.on_read_db_clicked(db_name, button)
        time.sleep(0.1)
        self.on_read_db_clicked(db_name, button)
        time.sleep(0.1)

    # Логика добавления базы данных
    def on_add_database_clicked(self, work_directory):
        dialog = CreateDbDialog(work_directory)
        dialog.exec()
        self.refresh_databases()

    # Логика удаления базы данных
    def on_del_database_clicked(self, db_name):
        # Формируем полный путь к базе данных
        full_db_path = os.path.join(self.work_directory, db_name)

        # Проверяем, существует ли база данных
        if os.path.exists(full_db_path):
            # Создаем окно с подтверждением
            reply = QMessageBox.question(self, 'Подтверждение',
                                         f"Вы уверены, что хотите удалить базу данных '{db_name}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # Если пользователь нажал "Да"
            if reply == QMessageBox.Yes:
                try:
                    # Удаляем файл базы данных
                    os.remove(full_db_path)
                    # Сообщаем об успешном удалении
                    QMessageBox.information(self, "Успех", f"База данных '{db_name}' успешно удалена.")
                except Exception as e:
                    # Если возникла ошибка при удалении
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении базы данных: {str(e)}")
            else:
                # Если пользователь нажал "Нет"
                QMessageBox.information(self, "Отмена", "Удаление базы данных отменено.")
        else:
            # Если база данных не найдена
            QMessageBox.warning(self, "Ошибка", f"База данных '{db_name}' не найдена.")
        self.refresh_databases()

    # Считывание таблиц базы данных, обновление полей
    def on_read_db_clicked(self, db_name, button=None):
        # Если текущая база данных не равна последней, очищаем таблицы последней базы
        if self.show_all_tables:
            if self.last_db and self.last_db != db_name:
                self.clear_finded_table_layout(self.last_db)
        self.current_database = db_name

        # Скрыть таблицы
        if button.state:
            button.setIcon(self.icon3)  # Устанавливаем значок для скрытия
            self.clear_finded_table_layout(db_name)
            button.state = False
        # Отобразить таблицы
        else:
            button.setIcon(self.icon6)  # Устанавливаем значок для отображения

            # Создаем экземпляр подключения к SQLite
            full_db_path = os.path.join(self.work_directory, db_name)
            db_connection = SQLiteConnection(full_db_path)
            # Подключаемся к базе данных
            db_connection.connect()
            # Получаем список таблиц из базы данных
            tables = db_connection.get_tables()
            tables.reverse()
            # Отображаем таблицы под элементом с названием базы данных
            self.display_tables(db_name, tables, button)
            # Закрываем подключение
            db_connection.close()

            if self.show_all_tables:
                # Скрываем остальные таблицы БД
                part_name_buttons = f'ToggleDatabaseButton_'
                # Обновляем состояние кнопок
                for current_button in self.findChildren(QPushButton):
                    if part_name_buttons.lower() in current_button.objectName().lower():
                        if (part_name_buttons.lower() + db_name) in current_button.objectName().lower():
                            current_button.setIcon(self.icon6)  # Значок для текущей базы данных
                            current_button.state = True
                        else:
                            current_button.setIcon(self.icon3)  # Значок для остальных кнопок
                            current_button.state = False
            button.state = True

            # Обновляем last_db на текущую базу данных
            self.last_db = db_name

    # Отображение таблиц базы данных, создание виджетов
    def display_tables(self, db_name, tables, button):
        # Ищем уже существующий блок для базы данных
        index = -1
        for i in range(self.ui.DatabasesVBoxLayoutForWidget.count()):
            item = self.ui.DatabasesVBoxLayoutForWidget.itemAt(i)
            if isinstance(item, QLayout) and item.objectName() == f"DB_HS_{db_name}":
                index = i

        if index != -1:  # Если блок найден
            # Очищаем старые элементы с таблицами
            self.clear_finded_table_layout(db_name)

            # Если таблиц нет, добавляем метку "Нет таблиц"
            if not tables:
                table_hs_all = QHBoxLayout()
                table_hs_all.setObjectName(f"Table_{db_name}_HS_ALL")
                table_hs_all.setContentsMargins(0, 0, 0, 5)

                spacer_item = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
                table_hs_all.addItem(spacer_item)

                no_tables_label = QLabel("Нет таблиц")
                no_tables_label.setObjectName(f"NoTablesLabel_{db_name}")
                no_tables_label.setStyleSheet("color: gray; font-style: italic;")
                table_hs_all.addWidget(no_tables_label)

                self.ui.DatabasesVBoxLayoutForWidget.insertLayout(index + 1, table_hs_all)
            else:
                # Если таблицы есть, добавляем их
                for table in tables:
                    try:
                        table_name = table
                        # Основной горизонтальный layout для таблицы
                        table_hs_all = QHBoxLayout()
                        table_hs_all.setObjectName(f"Table_{db_name}_{table_name}_HS_ALL")
                        table_hs_all.setContentsMargins(-1, -1, -1, 5)

                        # Отступ слева
                        table_hs_spacer_left = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum,
                                                           QSizePolicy.Policy.Minimum)
                        table_hs_all.addItem(table_hs_spacer_left)

                        # Метка с именем таблицы
                        table_label = QLabel(table_name)
                        table_label.setObjectName(f"Label_{db_name}_{table_name}")
                        table_hs_all.addWidget(table_label)

                        # Второй отступ (расширяющийся)
                        table_hs_spacer_right = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding,
                                                            QSizePolicy.Policy.Minimum)
                        table_hs_all.addItem(table_hs_spacer_right)

                        # Кнопка "Удалить таблицу"
                        delete_table_button = QPushButton()
                        delete_table_button.setObjectName(f"DeleteTableButton_{db_name}_{table_name}")
                        delete_table_button.setToolTip("Удалить таблицу из базы данных")
                        delete_table_button.setIcon(self.icon2)

                        # Установка политики размера для кнопки
                        delete_table_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                        table_hs_all.addSpacing(2)
                        delete_table_button.setIconSize(QSize(16, 20))
                        table_hs_all.addWidget(delete_table_button)

                        # Кнопка "Редактировать"
                        edit_table_button = QPushButton()
                        edit_table_button.setObjectName(f"EditTableButton_{db_name}_{table_name}")
                        edit_table_button.setToolTip("Изменить таблицу")
                        edit_table_button.setIcon(self.icon4)

                        # Установка политики размера для кнопки
                        edit_table_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                        table_hs_all.addSpacing(2)
                        edit_table_button.setIconSize(QSize(16, 20))
                        table_hs_all.addWidget(edit_table_button)

                        # Кнопка "Показать таблицу"
                        show_table_button = QPushButton()
                        show_table_button.setObjectName(f"ShowTableButton_{db_name}_{table_name}")
                        show_table_button.setToolTip("Показать содержимое таблицы")
                        show_table_button.setIcon(self.icon5)

                        # Установка политики размера для кнопки
                        show_table_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                        table_hs_all.addSpacing(2)
                        show_table_button.setIconSize(QSize(16, 20))
                        table_hs_all.addWidget(show_table_button)


                        # Привязка обработки кнопок
                        delete_table_button.clicked.connect(
                            lambda checked, db=db_name, curr_table=table_name: self.on_del_table_clicked(db, curr_table, button))
                        edit_table_button.clicked.connect(
                            lambda checked, db=db_name, curr_table=table_name: self.on_edit_table_clicked(db, curr_table, button))
                        show_table_button.clicked.connect(
                            lambda checked, db=db_name, curr_table=table_name: self.on_show_table_clicked(db, curr_table, button))

                        # Вставляем layout для таблицы после блока базы данных
                        self.ui.DatabasesVBoxLayoutForWidget.insertLayout(index + 1, table_hs_all)
                    except Exception as e:
                        print(f"Ошибка при добавлении таблицы {table}: {e}")

    # Очистка слоя с содержимым (таблицами) базы данных
    def clear_finded_table_layout(self, db_name):
        for i in reversed(range(self.ui.DatabasesVBoxLayoutForWidget.count())):
            item = self.ui.DatabasesVBoxLayoutForWidget.itemAt(i)
            if isinstance(item, QLayout) and item.objectName().startswith(f"Table_{db_name}_"):
                self.clear_layout(item)  # Очищаем вложенные элементы
                self.ui.DatabasesVBoxLayoutForWidget.removeItem(item)  # Удаляем сам layout

    # Удаление таблицы базы данных
    def on_del_table_clicked(self, db, table, button):
        # Формируем полный путь к базе данных
        full_db_path = os.path.join(self.work_directory, db)

        # Проверяем, существует ли база данных
        if os.path.exists(full_db_path):
            # Создаем окно с подтверждением
            reply = QMessageBox.question(self, 'Подтверждение удаления',
                                         f"Вы уверены, что хотите удалить таблицу '{table}' из базы данных '{db}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    conn = sqlite3.connect(full_db_path) # Подключаемся к БД
                    cursor = conn.cursor() # Создаем обработчик
                    drop_table_query = f"DROP TABLE IF EXISTS {table};" # Создаем запрос
                    cursor.execute(drop_table_query) # Выполняем запрос
                    conn.commit()  # Сохраняем изменения
                    conn.close() # Закрываем соединение
                    # Сообщаем об успешном удалении таблицы
                    QMessageBox.information(self, "Успех", f"Таблица '{table}' успешно удалена из базы данных '{db}'.")
                except sqlite3.Error as e:
                    # Если возникла ошибка при удалении
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении таблицы: {str(e)}")
                except Exception as e:
                    # Обработка других ошибок
                    QMessageBox.critical(self, "Ошибка", f"Непредвиденная ошибка: {str(e)}")
            else:
                QMessageBox.information(self, "Отмена", "Удаление таблицы отменено.")
        else:
            # Если база данных не найдена
            QMessageBox.warning(self, "Ошибка", f"База данных '{db}' не найдена.")
        # Обновление списка
        self.on_read_db_clicked(db, button)
        time.sleep(0.1)
        self.on_read_db_clicked(db, button)
        time.sleep(0.1)

    # Изменение таблицы базы данных
    def on_edit_table_clicked(self, db_name, table_name, button):
        dialog = EditTableDialog(db_name, self.work_directory, table_name)
        dialog.exec()
        # После закрытия диалога обновляем отображение таблиц
        self.on_read_db_clicked(db_name, button)
        time.sleep(0.1)
        self.on_read_db_clicked(db_name, button)
        time.sleep(0.1)

    # Отображение содержимого таблицы базы данных
    def on_show_table_clicked(self, db_name, table_name, button):
        full_db_path = os.path.normpath(os.path.join(self.work_directory, db_name))
        self.curr_db_name = db_name
        self.curr_table_name = table_name
        db_connection = None
        if not os.path.exists(full_db_path):
            QMessageBox.warning(self, "Ошибка", f"База данных '{db_name}' не найдена.")
            return

        is_read_only = False  # По умолчанию таблица редактируемая
        is_system_table = False  # Флаг для определения служебной таблицы

        # Проверяем, является ли таблица служебной (например, 'sqlite_sequence')
        if table_name.startswith('sqlite_'):
            QMessageBox.information(self, "Информация",
                                    f"Таблица '{table_name}' является системной и доступна только для чтения.")
            is_read_only = True
            is_system_table = True

        try:
            # Подключение к базе данных
            db_connection = SQLiteConnection(full_db_path)
            db_connection.connect()
            # Избегаем пометки isChanged при первоначальном заполнении
            self.ui.tableWidget.blockSignals(True)  # Блокируем сигналы перед заполнением таблицы
            # Проверяем наличие таблицы
            table_exists_query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
            table_exists = db_connection.execute_query(table_exists_query, (table_name,), is_select=True)
            if not table_exists:
                QMessageBox.warning(self, "Ошибка", f"Таблица '{table_name}' не найдена в базе данных.")
                return

            # Получаем заголовки столбцов
            headers_query = f"PRAGMA table_info({table_name});"
            headers_info = db_connection.execute_query(headers_query, is_select=True)
            headers = [column[1] for column in headers_info]

            # Проверяем, есть ли столбец 'id' в таблице
            if 'id' in headers:
                # Получаем максимальный `id` из существующих записей
                max_id_query = f"SELECT MAX(id) FROM {table_name};"
                max_id_result = db_connection.execute_query(max_id_query, is_select=True)
                self.last_id_in_db = max_id_result[0][0] if max_id_result[0][0] is not None else 0
                has_id_column = True
            else:
                self.last_id_in_db = 0
                has_id_column = False

            # Получаем данные таблицы
            data_query = f"SELECT * FROM {table_name};"
            table_data = db_connection.execute_query(data_query, is_select=True)

            # Очищаем QTableWidget и row_data_map
            self.ui.tableWidget.clear()
            self.row_data_map.clear()

            if is_system_table:
                # Для служебных таблиц отображаем только данные без '#' и 'Управление'
                self.ui.tableWidget.setColumnCount(len(headers))
                self.ui.tableWidget.setHorizontalHeaderLabels(headers)
                self.ui.tableWidget.setRowCount(len(table_data))

                for row_index, row in enumerate(table_data):
                    for col_index, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)  # Ячейки только для чтения
                        self.ui.tableWidget.setItem(row_index, col_index, item)

                self.ui.SaveChangesButton.setEnabled(False)  # Отключаем кнопку 'Сохранить'
                # Автоматическое изменение размеров
                self.ui.tableWidget.resizeColumnsToContents()
            else:
                # Для обычных таблиц отображаем с колонками '#' и 'Управление'
                self.ui.tableWidget.setColumnCount(len(headers) + 2)  # +2 для UUID и 'Управление'
                self.ui.tableWidget.setHorizontalHeaderLabels(["#"] + headers + ["Управление"])
                self.ui.tableWidget.setRowCount(len(table_data))

                # Заполняем таблицу данными из базы данных
                for row_index, row in enumerate(table_data):
                    # Генерация UUID
                    row_uuid = str(uuid.uuid4())
                    self.row_data_map[row_uuid] = {
                        'row_index': row_index,
                        'row_data': row,  # 'row' содержит данные строки
                        'isDeleted': False,
                        'isChanged': False,
                        'isNew': False
                    }
                    # Добавляем UUID в ячейку
                    uuid_item = QTableWidgetItem()
                    uuid_item.setData(Qt.UserRole, row_uuid)
                    uuid_item.setText(row_uuid)
                    uuid_item.setFlags(Qt.ItemIsEnabled)
                    self.ui.tableWidget.setItem(row_index, 0, uuid_item)

                    # Добавляем данные в колонки
                    for col_index, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        if headers[col_index] == 'id':
                            item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemIsEnabled)  # Делаем 'id' не редактируемым
                        else:
                            item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemIsEnabled)
                        self.ui.tableWidget.setItem(row_index, col_index + 1, item)

                    # Добавляем кнопку управления
                    self.add_del_row_button(row_index, row_uuid)

                # Добавление кнопки 'Добавить' для обычных таблиц
                if not is_read_only:
                    self.add_new_row(has_id_column)
                # Автоматическое изменение размеров
                self.ui.tableWidget.resizeColumnsToContents()
                # Скрываем поле '#'
                self.ui.tableWidget.setColumnWidth(0, 5)
                # Запрет увеличения ширины 1 столбца
                self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
                self.ui.SaveChangesButton.setEnabled(True)  # Включаем кнопку 'Сохранить'
                self.ui.SaveChangesButton.clicked.disconnect()
                self.ui.SaveChangesButton.clicked.connect(
                    lambda checked, db=self.curr_db_name, table=self.curr_table_name: self.save_changes(db, table))
                # После заполнения таблицы
                self.ui.tableWidget.blockSignals(False)  # Разблокируем сигналы после заполнения
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при работе с базой данных: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Непредвиденная ошибка: {str(e)}")
        finally:
            if db_connection:
                db_connection.close()
            # Очищаем `new_ids_in_use` и устанавливаем `last_id_in_db`
            self.new_ids_in_use.clear()

    # Добавление строки, инициализация таблицы
    def add_new_row(self, has_id_column):
        """Adds a new row to the QTableWidget with an 'Add' button."""
        row_count = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row_count)
        for col_index in range(1, self.ui.tableWidget.columnCount() - 1):
            item = QTableWidgetItem("")
            if self.ui.tableWidget.horizontalHeaderItem(col_index).text() == 'id':
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemIsEnabled)  # Make 'id' column not editable
            else:
                item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(row_count, col_index, item)

        # Insert a placeholder for the UUID
        uuid_item = QTableWidgetItem()
        uuid_item.setFlags(Qt.ItemIsEnabled)
        self.ui.tableWidget.setItem(row_count, 0, uuid_item)

        # Add the 'Add' button
        self.add_add_row_button()

    def add_row(self):
        """Adds a new row to the QTableWidget when the 'Add' button is pressed."""
        row_count = self.ui.tableWidget.rowCount()
        last_row_index = row_count - 1  # Index of the last row with the 'Add' button

        # Make the last row editable
        for col_index in range(1, self.ui.tableWidget.columnCount() - 1):
            item = self.ui.tableWidget.item(last_row_index, col_index)
            if not item:
                item = QTableWidgetItem("")
                self.ui.tableWidget.setItem(last_row_index, col_index, item)
            if self.ui.tableWidget.horizontalHeaderItem(col_index).text() == 'id':
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemIsEnabled)  # Make 'id' column not editable
            else:
                item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemIsEnabled)

        # Generate UUID for the new row
        row_uuid = str(uuid.uuid4())

        # Initialize `row_data`
        column_count = self.ui.tableWidget.columnCount() - 2  # Exclude '#' and 'Управление' columns
        initial_data = [self.ui.tableWidget.item(last_row_index, col_index + 1).text()
                        for col_index in range(column_count)]

        self.row_data_map[row_uuid] = {
            'row_index': last_row_index,
            'row_data': tuple(initial_data),
            'isDeleted': False,
            'isChanged': False,
            'isNew': True
        }

        # Set UUID in the first cell of the row
        uuid_item = QTableWidgetItem()
        uuid_item.setData(Qt.UserRole, row_uuid)
        uuid_item.setText(row_uuid)
        uuid_item.setFlags(Qt.ItemIsEnabled)
        self.ui.tableWidget.setItem(last_row_index, 0, uuid_item)

        # Replace the 'Add' button with a 'Delete' button
        self.add_del_row_button(last_row_index, row_uuid)

        # Update row indices
        self.reindex_row_data_map()

        # Add a new row with the 'Add' button
        self.add_new_row('id' in self.get_column_names(self.curr_table_name))

    def get_next_available_id(self):
        """Возвращает наименьший доступный `id` для новой записи, начиная с `last_id_in_db + 1`."""
        used_ids = set()

        # Собираем `id` существующих записей из базы данных
        for row_data in self.row_data_map.values():
            if not row_data['isDeleted']:
                record_id = row_data['row_data'][0]
                if record_id is not None:
                    used_ids.add(int(record_id))

        # Начальное значение для нового `id`
        candidate_id = self.last_id_in_db + 1

        # Ищем наименьший доступный `id`
        while True:
            if candidate_id not in used_ids:
                return candidate_id
            candidate_id += 1

    # Добавить кнопки удаления
    def add_del_row_button(self, row_index, row_uuid):
        """Добавляет кнопку удаления в строку таблицы."""
        del_button = QPushButton()
        del_button.setIcon(self.icon2)
        del_button.clicked.connect(lambda checked, uuid=row_uuid: self.on_delete_row(uuid))
        self.ui.tableWidget.setCellWidget(row_index, self.ui.tableWidget.columnCount() - 1, del_button)

    # Добавление кнопки "Добавить"
    def add_add_row_button(self):
        """Добавляет кнопку добавления в строку таблицы."""
        row_count = self.ui.tableWidget.rowCount()
        add_button = QPushButton()
        add_button.setIcon(self.icon1)
        add_button.clicked.connect(lambda: self.add_row())
        self.ui.tableWidget.setCellWidget(row_count-1, self.ui.tableWidget.columnCount() - 1, add_button)

    # Удаление строки
    def on_delete_row(self, row_uuid):
        """Обработка удаления строки по UUID."""
        if row_uuid not in self.row_data_map:
            QMessageBox.warning(self, "Ошибка", f"Строка с UUID {row_uuid} не найдена.")
            return
        # Получаем информацию о строке
        row_data = self.row_data_map[row_uuid]
        row_index = row_data['row_index']

        # Помечаем строку как удаленную
        row_data['isDeleted'] = True
        # Обновляем в `row_data_map`
        self.row_data_map[row_uuid] = row_data

        # Удаляем строку из таблицы
        self.ui.tableWidget.removeRow(row_index)
        # Обновляем индексы
        self.reindex_row_data_map()

    # Обновление row_data_map
    def reindex_row_data_map(self):
        """Обновляет индексы строк в `row_data_map` и переопределяет `id` для новых строк, обеспечивая их непрерывность."""
        uuid_to_row_index = {}
        new_row_uuids = []

        # Сначала собираем соответствие UUID и индексов строк из таблицы
        for row_index in range(self.ui.tableWidget.rowCount()):
            uuid_item = self.ui.tableWidget.item(row_index, 0)
            if uuid_item:
                row_uuid = uuid_item.data(Qt.UserRole)
                uuid_to_row_index[row_uuid] = row_index

        # Проходим по всему `row_data_map` и обновляем `row_index`
        for row_uuid, row_data in self.row_data_map.items():
            if row_uuid in uuid_to_row_index:
                new_index = uuid_to_row_index[row_uuid]
                row_data['row_index'] = new_index
                # Если строка является новой и не удаленной, добавляем ее UUID в список для переопределения `id`
                if row_data['isNew'] and not row_data['isDeleted']:
                    new_row_uuids.append((new_index, row_uuid))
            else:
                row_data['row_index'] = None  # Строка удалена из таблицы

        # Сортируем новые строки по `row_index` для последовательного присвоения `id`
        new_row_uuids.sort(key=lambda x: x[0])  # Сортируем по индексу строки в таблице

        # Переопределяем `id` для новых строк
        next_id = self.last_id_in_db + 1
        for _, row_uuid in new_row_uuids:
            row_data = self.row_data_map[row_uuid]
            row_data_list = list(row_data['row_data'])
            row_data_list[0] = next_id  # Устанавливаем новый `id`
            row_data['row_data'] = tuple(row_data_list)

            # Обновляем отображение `id` в таблице
            row_index = row_data['row_index']
            id_item = self.ui.tableWidget.item(row_index, 1)  # Предполагается, что столбец 'id' имеет индекс 1
            if id_item:
                id_item.setText(str(next_id))
            else:
                # Если элемент отсутствует, создаем его
                id_item = QTableWidgetItem(str(next_id))
                id_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Делаем 'id' не редактируемым
                self.ui.tableWidget.setItem(row_index, 1, id_item)
            next_id += 1

    # Изменения в таблице
    def on_item_changed(self, item):
        """Обрабатывает изменения в ячейках таблицы и ставит флаг isChanged в row_data_map."""
        row_index = item.row()  # Индекс строки
        col_index = item.column()  # Индекс столбца

        # Игнорируем изменения в не редактируемых ячейках (например, 'id' и UUID)
        if col_index == 0 or self.ui.tableWidget.horizontalHeaderItem(col_index).text() == 'id':
            return

        # Получаем UUID строки, которая была изменена
        uuid_item = self.ui.tableWidget.item(row_index, 0)  # Столбец с UUID
        if uuid_item:
            row_uuid = uuid_item.data(Qt.UserRole)
            if row_uuid in self.row_data_map:
                # Получаем данные строки из row_data_map
                row_data = self.row_data_map[row_uuid]

                # Обновляем флаг isChanged, если это не новая строка
                if not row_data['isNew']:
                    row_data['isChanged'] = True

                # Обновляем данные строки
                row_data_list = list(row_data['row_data'])
                # Обновляем значение в `row_data_list`, смещение на -1, так как первая колонка — UUID
                row_data_list[col_index - 1] = item.text()
                row_data['row_data'] = tuple(row_data_list)
                # Обновляем `row_data_map`
                self.row_data_map[row_uuid] = row_data

    # Добавление страницы в TabWidget
    def add_query_tab(self):
        """Добавление новой вкладки с правильным номером."""
        # Создание новой вкладки
        new_tab = QWidget()
        new_tab_layout = QVBoxLayout(new_tab)

        query_editor = AutoCompleteTextEdit()
        query_editor.setPlaceholderText("Введите SQL-запрос...")
        # Для нового QTextEdit подключаем SQLHighlighter. (переопределение привязки обработчика событий. обновление информации о QTabWidget)
        # Подключаем подсветку синтаксиса
        self.highlighter = SQLSyntaxHighlighter(query_editor)
        self.highlighter.completer.activated.connect(self.highlighter.insert_completion)

        new_tab_layout.addWidget(query_editor)

        if self.ui.TabWidget.count() == 1:
            self.last_tab_number = 2
        else:
            self.last_tab_number += 1
        # Создание вкладки
        tab_index = self.ui.TabWidget.addTab(new_tab, f"Запрос {self.last_tab_number}")
        self.ui.TabWidget.setCurrentIndex(tab_index)

    # Удаление страницы из TabWidget
    def del_current_tab(self):
        """Удаление текущей вкладки."""
        current_index = self.ui.TabWidget.currentIndex()

        if current_index != -1 and current_index != 0:
            reply = QMessageBox.question(
                self,
                "Подтверждение",
                "Вы уверены, что хотите удалить текущий запрос?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Удаляем вкладку
                if current_index == self.ui.TabWidget.count() - 1:
                    self.last_tab_number -= 1
                self.ui.TabWidget.removeTab(current_index)

    # Выполнение запроса из LineEdit в CurrentTabWidget
    def execute_query(self):
        """Обработчик кнопки выполнения SQL-запроса."""
        if not self.current_database:
            QMessageBox.warning(self, "Ошибка", "Не выбрана база данных.")
            return

        current_tab = self.ui.TabWidget.currentWidget()
        if not current_tab:
            QMessageBox.warning(self, "Ошибка", "Нет активного SQL-запроса.")
            return

        # Получаем редактор запроса из текущей вкладки
        query_editor = current_tab.findChild(QTextEdit)
        if not query_editor:
            QMessageBox.warning(self, "Ошибка", "Невозможно найти редактор запроса.")
            return
        query = query_editor.toPlainText().strip()
        if not query:
            QMessageBox.warning(self, "Ошибка", "Запрос пуст.")
            return

        # Формируем полный путь к базе данных
        full_db_path = os.path.normpath(os.path.join(self.work_directory, self.current_database))

        if not os.path.exists(full_db_path):
            QMessageBox.warning(self, "Ошибка", f"База данных '{self.current_database}' не найдена.")
            return

        db_connection = SQLiteConnection(full_db_path)
        db_connection.connect()

        start_time = time.time()  # Запускаем таймер

        try:
            # Определяем, является ли запрос запросом на выборку данных
            is_select_query = query.strip().upper().startswith(("SELECT", "PRAGMA", "EXPLAIN", "WITH"))

            # Выполняем запрос с использованием метода из SQLiteConnection
            results = db_connection.execute_query(query, is_select=is_select_query)

            if is_select_query and results is not None:
                # Получаем заголовки столбцов
                cursor = db_connection.connection.cursor()
                cursor.execute(query)
                headers = [description[0] for description in cursor.description]
                cursor.close()

                # Очищаем таблицу и заполняем новыми данными
                self.ui.tableWidget.clear()
                self.ui.tableWidget.setRowCount(0)
                self.ui.tableWidget.setColumnCount(len(headers))
                self.ui.tableWidget.setHorizontalHeaderLabels(headers)

                for row_index, row in enumerate(results):
                    self.ui.tableWidget.insertRow(row_index)
                    for col_index, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.ui.tableWidget.setItem(row_index, col_index, item)

                self.ui.tableWidget.resizeColumnsToContents()

                end_time = time.time()  # Останавливаем таймер
                execution_time = end_time - start_time

                self.ui.ResutlText.setPlainText(f"Запрос выполнен успешно за {execution_time:.4f} секунд.")
            else:
                # Если данные не возвращены, отображаем количество затронутых строк
                affected_rows = db_connection.connection.total_changes
                end_time = time.time()  # Останавливаем таймер
                execution_time = end_time - start_time

                self.ui.tableWidget.clear()
                self.ui.ResutlText.setPlainText(
                    f"Запрос выполнен успешно за {execution_time:.4f} секунд.\nЗатронуто строк: {affected_rows}")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка SQL", f"Не удалось выполнить запрос: {e}")
            self.ui.ResutlText.setPlainText(f"Ошибка SQL: {e}")

        finally:
            db_connection.close()

    # Сохранение изменений
    def save_changes(self, db_name, table_name):
        """Сохранение изменений таблицы в базу данных sqlite. Обработка isNew, isChanged, isDeleted"""
        self.curr_db_name = db_name
        #self.curr_table_name = table_name
        if not table_name:
            QMessageBox.warning(self, "Ошибка", "Нет текущей таблицы")
            return

        full_db_path = os.path.normpath(os.path.join(self.work_directory, db_name))

        # Проверяем, существует ли база данных
        if not os.path.exists(full_db_path):
            QMessageBox.warning(self, "Ошибка", f"База данных '{db_name}' не найдена.")
            return

        db_connection = SQLiteConnection(full_db_path)
        db_connection.connect()

        # Получаем информацию о столбцах таблицы и их типах
        column_info = db_connection.execute_query(f"PRAGMA table_info({table_name});", is_select=True)
        column_names = [col[1] for col in column_info]  # Имена столбцов
        not_null_columns = [col[1] for col in column_info if col[3] == 1]  # Столбцы с NOT NULL
        integer_columns = [col[1] for col in column_info if col[2].upper() == 'INTEGER']  # Столбцы типа INTEGER

        if not column_names:
            QMessageBox.warning(self, "Ошибка", f"Не удалось получить столбцы таблицы '{table_name}'.")
            return

        # Проверяем, есть ли столбец 'id' в таблице
        if 'id' in column_names:
            id_column_exists = True
        else:
            id_column_exists = False

        # Проходим по всем строкам и обрабатываем изменения
        for row_uuid, row_data in self.row_data_map.items():
            if row_data['isDeleted']:
                if not row_data['isNew'] and id_column_exists:
                    # Удаление существующей строки из БД по 'id'
                    row_id = row_data['row_data'][column_names.index('id')]
                    delete_query = f"DELETE FROM {table_name} WHERE id = ?"
                    logging.info(f"Удаление строки с id = {row_id} из таблицы {table_name}")
                    db_connection.execute_query(delete_query, (row_id,))
                elif not row_data['isNew']:
                    # Удаление существующей строки без 'id' (по первичному ключу)
                    primary_keys = [col[1] for col in column_info if col[5] == 1]  # Столбцы, которые являются PK
                    if primary_keys:
                        # Составляем условие WHERE на основе первичного ключа
                        where_clause = " AND ".join([f"{pk} = ?" for pk in primary_keys])
                        values = [row_data['row_data'][column_names.index(pk)] for pk in primary_keys]
                        delete_query = f"DELETE FROM {table_name} WHERE {where_clause}"
                        db_connection.execute_query(delete_query, values)
                    else:
                        QMessageBox.warning(self, "Ошибка",
                                            f"Невозможно удалить строку из таблицы '{table_name}' без 'id' или первичного ключа.")
                continue

            if row_data['isNew']:
                # Вставка новой строки в БД
                row_index = row_data['row_index']
                values = []
                for col_index in range(1, len(column_names) + 1):
                    item = self.ui.tableWidget.item(row_index, col_index)
                    value = item.text() if item else None
                    if self.ui.tableWidget.horizontalHeaderItem(col_index).text() == 'id' and not id_column_exists:
                        continue  # Пропускаем столбец 'id' если его нет в таблице
                    values.append(value)

                # **Проверка обязательных полей перед вставкой**
                for col_name, value in zip(column_names, values):
                    if col_name in not_null_columns:
                        if value is None or value.strip() == '':
                            logging.warning(
                                f"Строка с индексом {row_index} содержит пустые значения в обязательном поле '{col_name}'. Вставка пропущена.")
                            QMessageBox.warning(self, "Ошибка",
                                                f"Строка {row_index + 1}: поле '{col_name}' является обязательным и не может быть пустым. Вставка отменена.")
                            return  # Прерываем сохранение из-за пустого обязательного поля

                    # **Проверка типа данных INTEGER**
                    if col_name in integer_columns:
                        if value is not None and value.strip() != '':
                            try:
                                int(value)
                            except ValueError:
                                logging.warning(
                                    f"Строка с индексом {row_index}: значение '{value}' в поле '{col_name}' должно быть целым числом.")
                                QMessageBox.warning(self, "Ошибка",
                                                    f"Строка {row_index + 1}: значение '{value}' в поле '{col_name}' должно быть целым числом. Вставка отменена.")
                                return  # Прерываем сохранение из-за несоответствия типов данных

                # Формируем запрос INSERT
                columns_to_insert = [col for col in column_names if col != 'id' or id_column_exists]
                placeholders = ", ".join(["?"] * len(columns_to_insert))
                formatted_columns = ", ".join([f'`{col}`' for col in columns_to_insert])
                insert_query = f"INSERT INTO `{table_name}` ({formatted_columns}) VALUES ({placeholders})"

                try:
                    db_connection.execute_query(insert_query, tuple(values))
                    row_data['isNew'] = False  # Очищаем флаг после успешной вставки
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось вставить новую строку: {e}")
                continue

            elif row_data['isChanged']:
                # Обновление существующей строки в БД
                row_index = row_data['row_index']
                set_clauses = []
                values = []
                for col_index in range(1, len(column_names) + 1):
                    item = self.ui.tableWidget.item(row_index, col_index)
                    value = item.text() if item else None
                    column_name = column_names[col_index - 1]
                    if column_name == 'id' and not id_column_exists:
                        continue  # Пропускаем столбец 'id' если его нет в таблице
                    set_clauses.append(f"{column_name} = ?")
                    values.append(value)

                # **Проверка обязательных полей перед обновлением**
                for col_name, value in zip(column_names, values):
                    if col_name in not_null_columns:
                        if value is None or value.strip() == '':
                            logging.warning(
                                f"Строка с индексом {row_index} содержит пустые значения в обязательном поле '{col_name}'. Обновление пропущено.")
                            QMessageBox.warning(self, "Ошибка",
                                                f"Строка {row_index + 1}: поле '{col_name}' является обязательным и не может быть пустым. Обновление пропущено.")
                            break  # Переходим к следующей строке

                    # **Проверка типа данных INTEGER**
                    if col_name in integer_columns:
                        if value is not None and value.strip() != '':
                            try:
                                int(value)
                            except ValueError:
                                logging.warning(
                                    f"Строка с индексом {row_index}: значение '{value}' в поле '{col_name}' должно быть целым числом.")
                                QMessageBox.warning(self, "Ошибка",
                                                    f"Строка {row_index + 1}: значение '{value}' в поле '{col_name}' должно быть целым числом. Обновление пропущено.")
                                break  # Пропускаем обновление этой строки из-за несоответствия типов данных

                else:
                    if id_column_exists:
                        # Обновление по 'id'
                        row_id = row_data['row_data'][column_names.index('id')]
                        update_query = f"UPDATE {table_name} SET {', '.join(set_clauses)} WHERE id = ?"
                        db_connection.execute_query(update_query, (*values, row_id))
                    else:
                        # Обновление по первичному ключу
                        primary_keys = [col[1] for col in column_info if col[5] == 1]  # Столбцы, которые являются PK
                        if primary_keys:
                            where_clause = " AND ".join([f"{pk} = ?" for pk in primary_keys])
                            pk_values = [row_data['row_data'][column_names.index(pk)] for pk in primary_keys]
                            update_query = f"UPDATE {table_name} SET {', '.join(set_clauses)} WHERE {where_clause}"
                            db_connection.execute_query(update_query, (*values, *pk_values))
                        else:
                            QMessageBox.warning(self, "Ошибка",
                                                f"Невозможно обновить строку без 'id' или первичного ключа.")
                            continue  # Переходим к следующей строке
                    row_data['isChanged'] = False  # Сбрасываем флаг после успешного обновления

        # После успешного сохранения обновляем `last_id_in_db`
        if id_column_exists:
            max_id_query = f"SELECT MAX(id) FROM {table_name};"
            max_id_result = db_connection.execute_query(max_id_query, is_select=True)
            self.last_id_in_db = max_id_result[0][0] if max_id_result[0][0] is not None else 0

        # Очищаем `new_ids_in_use` после сохранения
        self.new_ids_in_use.clear()

        QMessageBox.information(self, "Сохранено", "Изменения успешно сохранены.")
        db_connection.close()

    def get_column_names(self, table_name):
        """Получает имена колонок таблицы."""
        full_db_path = os.path.normpath(os.path.join(self.work_directory, self.current_database))
        db_connection = SQLiteConnection(full_db_path)
        db_connection.connect()
        query = f"PRAGMA table_info({table_name});"
        columns = db_connection.execute_query(query, is_select=True)
        db_connection.close()

        return [column[1] for column in columns]

    # Очистка слоя. В частности, для содержимого scrollArea
    def clear_layout(self, layout):
        """Рекурсивно очищает указанный QLayout от всех элементов."""
        while layout.count():
            item = layout.takeAt(0)
            if widget := item.widget():
                widget.deleteLater()  # Удаляем виджет
            elif sub_layout := item.layout():
                self.clear_layout(sub_layout)  # Рекурсивно очищаем вложенные макеты
            del item  # Удаляем сам объект item из памяти

    # Информация о разработчике
    def developer_info(self):
        # print(f"Добавление таблицы для базы данных: {db_name}")
        dialog = DevInfoDialog()
        dialog.exec()  # Открываем диалог модально

    # Информация о программе
    def program_info(self):
        dialog = ProgInfoDialog()
        dialog.exec()

    # Окно с настройками приложение
    def settings_action(self):
        dialog = SettingsDialog(self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())