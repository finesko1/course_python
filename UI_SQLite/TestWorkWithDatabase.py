import sqlite3
import unittest
import tempfile
import shutil
import os
from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMessageBox, QTableWidgetItem
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
from CreateDatabaseDialog import CreateDbDialog
from main import MainWindow


# Обновление БД
class TestWorkWithDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем экземпляр приложения Qt
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self):
        # Создаем временную рабочую директорию
        self.test_dir = tempfile.mkdtemp()
        # Создаем несколько файлов базы данных и файлы, не являющиеся базами данных
        self.db_files = ['test1.db', 'test2.sqlite', 'notadb.txt', 'test3.DB']
        for file_name in self.db_files:
            file_path = os.path.join(self.test_dir, file_name)
            with open(file_path, 'w') as f:
                f.write('')  # создаем пустой файл

        # Создаем экземпляр MainWindow
        self.main_window = MainWindow()
        self.main_window.work_directory = self.test_dir

    def tearDown(self):
        # Удаляем временную рабочую директорию после тестов
        shutil.rmtree(self.test_dir)
        self.main_window = None

    def test_refresh_databases(self):
        """
        Тестирует метод refresh_databases на корректное обновление списка баз данных.
        """
        # Вызываем метод
        self.main_window.refresh_databases()

        # Ожидаемый список баз данных (файлы с расширениями .db и .sqlite)
        expected_databases = [file_name for file_name in self.db_files if file_name.lower().endswith(('.db', '.sqlite'))]
        expected_count = len(expected_databases)

        # Получаем фактический список баз данных из интерфейса
        layout = self.main_window.ui.DatabasesVBoxLayoutForWidget
        actual_databases = []

        # Проходим по всем элементам в layout, начиная с индекса 1, так как первый элемент — кнопка создания БД
        for i in range(1, layout.count()):
            item = layout.itemAt(i)
            if isinstance(item, QHBoxLayout):
                label = item.itemAt(0).widget()
                if isinstance(label, QLabel):
                    text = label.text()
                    actual_databases.append(text)

        # Сравниваем ожидаемые и фактические базы данных
        self.assertEqual(sorted(actual_databases), sorted(expected_databases), "Списки баз данных не совпадают.")

        # Проверяем, что количество отображаемых баз данных соответствует ожидаемому
        actual_count = len(actual_databases)
        self.assertEqual(actual_count, expected_count, "Количество отображаемых баз данных не соответствует ожидаемому.")

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

# Добавление БД
class TestCreateDbDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем экземпляр приложения Qt
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self):
        # Создаем временную рабочую директорию
        self.test_dir = tempfile.mkdtemp()
        # Создаем экземпляр диалога создания базы данных
        self.create_db_dialog = CreateDbDialog(work_directory=self.test_dir)
        # Показываем диалоговое окно
        # self.create_db_dialog.show()

    def tearDown(self):
        # Закрываем диалоговое окно
        #self.create_db_dialog.close()
        # Удаляем временную рабочую директорию после тестов
        shutil.rmtree(self.test_dir)

    @classmethod
    def tearDownClass(cls):
        # Закрываем приложение Qt
        cls.app.quit()

    def test_add_database_success(self):
        """
        Тестирует успешное создание базы данных через диалоговое окно.
        """
        # Устанавливаем имя базы данных
        db_name = 'test_database'
        self.create_db_dialog.ui.DatabaseName.setText(db_name)

        # Симулируем нажатие на кнопку "Создать"
        QTest.mouseClick(self.create_db_dialog.ui.AddDatabaseButton, Qt.LeftButton)

        # Проверяем, что файл базы данных создан
        expected_db_path = os.path.join(self.test_dir, db_name + '.sqlite')
        self.assertTrue(os.path.exists(expected_db_path), "База данных не была создана.")

    def test_add_database_existing(self):
        """
        Тестирует поведение при попытке создать базу данных, которая уже существует.
        """
        # Создаем файл базы данных с тем же именем
        db_name = 'existing_database'
        existing_db_path = os.path.join(self.test_dir, db_name + '.sqlite')
        open(existing_db_path, 'w').close()  # Создаем пустой файл

        # Устанавливаем имя базы данных
        self.create_db_dialog.ui.DatabaseName.setText(db_name)

        # Симулируем нажатие на кнопку "Создать"
        QTest.mouseClick(self.create_db_dialog.ui.AddDatabaseButton, Qt.LeftButton)

        # Проверяем, что существующий файл не был изменен
        self.assertTrue(os.path.exists(existing_db_path), "Существующий файл базы данных был изменен или удален.")

    def test_add_database_no_name(self):
        """
        Тестирует поведение при попытке создать базу данных без указания имени.
        """
        # Оставляем поле имени базы данных пустым
        self.create_db_dialog.ui.DatabaseName.setText('')

        # Симулируем нажатие на кнопку "Создать"
        QTest.mouseClick(self.create_db_dialog.ui.AddDatabaseButton, Qt.LeftButton)

        # Проверяем, что база данных не создана
        files_in_test_dir = os.listdir(self.test_dir)
        self.assertEqual(len(files_in_test_dir), 0, "Неожиданно был создан файл базы данных.")

    def test_add_database_invalid_directory(self):
        """
        Тестирует поведение при указании несуществующей рабочей директории.
        """
        # Устанавливаем несуществующую рабочую директорию
        self.create_db_dialog.work_directory = '/non/existent/directory'

        # Устанавливаем имя базы данных
        db_name = 'test_invalid_dir'
        self.create_db_dialog.ui.DatabaseName.setText(db_name)

        # Симулируем нажатие на кнопку "Создать"
        QTest.mouseClick(self.create_db_dialog.ui.AddDatabaseButton, Qt.LeftButton)

        # Проверяем, что база данных не создана
        expected_db_path = os.path.join('/non/existent/directory', db_name + '.sqlite')
        self.assertFalse(os.path.exists(expected_db_path),
                         "База данных не должна быть создана в несуществующей директории.")

# Удаление БД
class TestDeleteDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем экземпляр приложения Qt
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self):
        # Создаем временную рабочую директорию
        self.test_dir = tempfile.mkdtemp()
        # Создаем тестовую базу данных
        self.db_name = 'test_delete.db'
        self.full_db_path = os.path.join(self.test_dir, self.db_name)
        with open(self.full_db_path, 'w') as f:
            f.write('')  # Создаем пустой файл базы данных

        # Создаем экземпляр MainWindow
        self.main_window = MainWindow()
        self.main_window.work_directory = self.test_dir
        self.main_window.refresh_databases()

    def tearDown(self):
        # Закрываем главное окно и удаляем временную директорию
        self.main_window.close()
        shutil.rmtree(self.test_dir)

    @classmethod
    def tearDownClass(cls):
        # Закрываем приложение Qt
        cls.app.quit()

    @patch('PySide6.QtWidgets.QMessageBox.question')
    def test_on_del_database_clicked_confirm_yes(self, mock_question):
        """
        Тестирует успешное удаление базы данных при подтверждении удаления.
        """
        # Настраиваем mock для QMessageBox.question, чтобы он возвращал Yes
        mock_question.return_value = QMessageBox.Yes

        # Вызываем метод удаления базы данных
        self.main_window.on_del_database_clicked(self.db_name)

        # Проверяем, что файл базы данных был удален
        self.assertFalse(os.path.exists(self.full_db_path), "База данных не была удалена.")

    @patch('PySide6.QtWidgets.QMessageBox.question')
    def test_on_del_database_clicked_confirm_no(self, mock_question):
        """
        Тестирует отмену удаления базы данных при выборе 'Нет' в диалоговом окне.
        """
        # Настраиваем mock для QMessageBox.question, чтобы он возвращал No
        mock_question.return_value = QMessageBox.No

        # Вызываем метод удаления базы данных
        self.main_window.on_del_database_clicked(self.db_name)

        # Проверяем, что файл базы данных все еще существует
        self.assertTrue(os.path.exists(self.full_db_path), "База данных была удалена, хотя не должна была.")

    def test_on_del_database_clicked_nonexistent(self):
        """
        Тестирует поведение при попытке удалить несуществующую базу данных.
        """
        # Удаляем файл базы данных
        os.remove(self.full_db_path)

        # Сохраняем имя для несуществующей базы данных
        nonexistent_db_name = self.db_name

        # Проверяем, что файла базы данных не существует
        self.assertFalse(os.path.exists(self.full_db_path), "Файл базы данных должен быть отсутствовать для этого теста.")

        # Патчим QMessageBox.warning, чтобы подавить диалоговое окно
        with patch('PySide6.QtWidgets.QMessageBox.warning') as mock_warning:
            # Вызываем метод удаления базы данных
            self.main_window.on_del_database_clicked(nonexistent_db_name)

            # Проверяем, что QMessageBox.warning был вызван
            mock_warning.assert_called_once()

    @patch('PySide6.QtWidgets.QMessageBox.question')
    def test_refresh_databases_called(self, mock_question):
        """
        Тестирует, что метод refresh_databases вызывается после удаления базы данных.
        """
        # Настраиваем mock для QMessageBox.question, чтобы он возвращал Yes
        mock_question.return_value = QMessageBox.Yes

        # Патчим метод refresh_databases
        with patch.object(self.main_window, 'refresh_databases') as mock_refresh:
            # Вызываем метод удаления базы данных
            self.main_window.on_del_database_clicked(self.db_name)

            # Проверяем, что refresh_databases был вызван
            mock_refresh.assert_called_once()

    @patch('PySide6.QtWidgets.QMessageBox.question')
    def test_on_del_database_error_handling(self, mock_question):
        """
        Тестирует обработку исключений при удалении базы данных.
        """
        # Настраиваем mock для QMessageBox.question, чтобы он возвращал Yes
        mock_question.return_value = QMessageBox.Yes

        # Создаем mock для os.remove, чтобы вызвать исключение
        with patch('os.remove', side_effect=Exception("Ошибка удаления")):
            # Патчим QMessageBox.critical, чтобы проверить его вызов
            with patch('PySide6.QtWidgets.QMessageBox.critical') as mock_critical:
                # Вызываем метод удаления базы данных
                self.main_window.on_del_database_clicked(self.db_name)

                # Проверяем, что QMessageBox.critical был вызван с сообщением об ошибке
                mock_critical.assert_called_once()
                args, kwargs = mock_critical.call_args
                # Проверяем текст сообщения в args[2]
                self.assertIn("Ошибка при удалении базы данных", args[2])

# Сохранение изменений в БД sqlite
class TestSaveChanges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем экземпляр приложения Qt
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self):
        # Создаем временную рабочую директорию
        self.test_dir = tempfile.mkdtemp()
        # Создаем тестовую базу данных
        self.db_name = 'test_save_changes.db'
        self.full_db_path = os.path.join(self.test_dir, self.db_name)

        # Создаем экземпляр MainWindow
        self.main_window = MainWindow()
        self.main_window.work_directory = self.test_dir
        self.main_window.current_database = self.db_name

        # Подключаемся к базе данных и создаем таблицу для тестирования
        self.connection = sqlite3.connect(self.full_db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER
            )
        """)
        self.connection.commit()

        # Вставляем тестовые данные
        self.cursor.executemany("INSERT INTO test_table (name, age) VALUES (?, ?)", [
            ('Alice', 30),
            ('Bob', 25),
            ('Charlie', 35)
        ])
        self.connection.commit()
        self.connection.close()

        # Устанавливаем текущую таблицу и обновляем интерфейс
        self.main_window.curr_db_name = self.db_name
        self.main_window.curr_table_name = 'test_table'

        # Отображаем таблицу
        self.main_window.on_show_table_clicked(self.db_name, 'test_table', None)

    def tearDown(self):
        # Закрываем главное окно и удаляем ссылку на него
        self.main_window.close()
        self.main_window = None

        # Обрабатываем оставшиеся события в цикле событий Qt
        QApplication.processEvents()

        # Принудительно запускаем сборщик мусора
        import gc
        gc.collect()

        # Теперь можем безопасно удалить временную директорию
        shutil.rmtree(self.test_dir)

    @classmethod
    def tearDownClass(cls):
        # Закрываем приложение Qt
        cls.app.quit()

    def test_add_new_row(self):
        """
        Тест добавления новой строки и сохранения изменений.
        """
        # Добавляем новую строку через метод add_row
        self.main_window.add_row()

        # Получаем индекс последней строки
        row_count = self.main_window.ui.tableWidget.rowCount()
        last_row_index = row_count - 2  # Последний индекс с реальными данными

        # Заполняем данные в новой строке
        name_item = QTableWidgetItem('David')
        age_item = QTableWidgetItem('28')

        self.main_window.ui.tableWidget.setItem(last_row_index, 2, name_item)  # Столбец 'name'
        self.main_window.ui.tableWidget.setItem(last_row_index, 3, age_item)   # Столбец 'age'

        # Симулируем изменение ячейки
        self.main_window.on_item_changed(name_item)
        self.main_window.on_item_changed(age_item)

        # Вызываем метод сохранения изменений
        self.main_window.save_changes(self.db_name, 'test_table')

        # Проверяем, что запись добавлена в базу данных
        conn = sqlite3.connect(self.full_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, age FROM test_table WHERE name = 'David'")
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result, "Новая запись не была добавлена в базу данных.")
        self.assertEqual(result, ('David', 28), "Данные новой записи не соответствуют ожидаемым.")

    def test_update_existing_row(self):
        """
        Тест обновления существующей строки и сохранения изменений.
        """
        # Изменяем возраст пользователя 'Alice' на 31
        # Находим индекс строки с 'Alice'
        row_index = None
        for i in range(self.main_window.ui.tableWidget.rowCount()):
            item = self.main_window.ui.tableWidget.item(i, 2)  # Столбец 'name'
            if item and item.text() == 'Alice':
                row_index = i
                break

        self.assertIsNotNone(row_index, "Не удалось найти строку с именем 'Alice'.")

        # Обновляем возраст
        age_item = self.main_window.ui.tableWidget.item(row_index, 3)  # Столбец 'age'
        age_item.setText('31')
        self.main_window.on_item_changed(age_item)

        # Вызываем метод сохранения изменений
        self.main_window.save_changes(self.db_name, 'test_table')

        # Проверяем, что изменения сохранены в базе данных
        conn = sqlite3.connect(self.full_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM test_table WHERE name = 'Alice'")
        result = cursor.fetchone()
        conn.close()

        self.assertEqual(result[0], 31, "Возраст пользователя 'Alice' не был обновлен в базе данных.")

    def test_delete_row(self):
        """
        Тест удаления строки и сохранения изменений.
        """
        # Находим индекс строки с 'Bob'
        row_index = None
        for i in range(self.main_window.ui.tableWidget.rowCount()):
            item = self.main_window.ui.tableWidget.item(i, 2)  # Столбец 'name'
            if item and item.text() == 'Bob':
                row_index = i
                break

        self.assertIsNotNone(row_index, "Не удалось найти строку с именем 'Bob'.")

        # Получаем UUID строки
        uuid_item = self.main_window.ui.tableWidget.item(row_index, 0)
        row_uuid = uuid_item.data(Qt.UserRole)

        # Вызываем метод удаления строки
        self.main_window.on_delete_row(row_uuid)

        # Вызываем метод сохранения изменений
        self.main_window.save_changes(self.db_name, 'test_table')

        # Проверяем, что запись удалена из базы данных
        conn = sqlite3.connect(self.full_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_table WHERE name = 'Bob'")
        result = cursor.fetchone()
        conn.close()

        self.assertIsNone(result, "Запись пользователя 'Bob' не была удалена из базы данных.")

    def test_add_update_delete_combination(self):
        """
        Тест комбинации операций: добавление, обновление и удаление, затем сохранение.
        """
        # Добавляем новую строку
        self.main_window.add_row()
        row_count = self.main_window.ui.tableWidget.rowCount()
        new_row_index = row_count - 2

        name_item_new = QTableWidgetItem('Eve')
        age_item_new = QTableWidgetItem('26')

        self.main_window.ui.tableWidget.setItem(new_row_index, 2, name_item_new)  # 'name'
        self.main_window.ui.tableWidget.setItem(new_row_index, 3, age_item_new)   # 'age'

        self.main_window.on_item_changed(name_item_new)
        self.main_window.on_item_changed(age_item_new)

        # Изменяем запись 'Charlie'
        # Находим индекс строки с 'Charlie'
        row_index_charlie = None
        for i in range(self.main_window.ui.tableWidget.rowCount()):
            item = self.main_window.ui.tableWidget.item(i, 2)  # 'name'
            if item and item.text() == 'Charlie':
                row_index_charlie = i
                break

        self.assertIsNotNone(row_index_charlie, "Не удалось найти строку с именем 'Charlie'.")

        age_item_charlie = self.main_window.ui.tableWidget.item(row_index_charlie, 3)  # 'age'
        age_item_charlie.setText('36')
        self.main_window.on_item_changed(age_item_charlie)

        # Удаляем запись 'Alice'
        # Находим индекс строки с 'Alice'
        row_index_alice = None
        for i in range(self.main_window.ui.tableWidget.rowCount()):
            item = self.main_window.ui.tableWidget.item(i, 2)  # 'name'
            if item and item.text() == 'Alice':
                row_index_alice = i
                break

        self.assertIsNotNone(row_index_alice, "Не удалось найти строку с именем 'Alice'.")

        uuid_item_alice = self.main_window.ui.tableWidget.item(row_index_alice, 0)
        row_uuid_alice = uuid_item_alice.data(Qt.UserRole)
        self.main_window.on_delete_row(row_uuid_alice)

        # Сохраняем изменения
        self.main_window.save_changes(self.db_name, 'test_table')

        # Проверяем результаты в базе данных
        conn = sqlite3.connect(self.full_db_path)
        cursor = conn.cursor()
        # Проверяем, что 'Eve' добавлена
        cursor.execute("SELECT age FROM test_table WHERE name = 'Eve'")
        result_eve = cursor.fetchone()
        self.assertIsNotNone(result_eve, "Запись 'Eve' не добавлена в базу данных.")
        self.assertEqual(result_eve[0], 26, "Возраст 'Eve' не соответствует ожидаемому.")

        # Проверяем, что 'Charlie' обновлен
        cursor.execute("SELECT age FROM test_table WHERE name = 'Charlie'")
        result_charlie = cursor.fetchone()
        self.assertEqual(result_charlie[0], 36, "Возраст 'Charlie' не был обновлен в базе данных.")

        # Проверяем, что 'Alice' удалена
        cursor.execute("SELECT * FROM test_table WHERE name = 'Alice'")
        result_alice = cursor.fetchone()
        self.assertIsNone(result_alice, "Запись 'Alice' не была удалена из базы данных.")

        conn.close()

    def test_save_changes_without_modifications(self):
        """
        Тест сохранения без каких-либо изменений.
        """
        # Проверяем, что self.row_data_map существует и не пуст
        self.assertTrue(hasattr(self.main_window, 'row_data_map'), "MainWindow должен иметь атрибут 'row_data_map'.")
        self.assertGreater(len(self.main_window.row_data_map), 0, "row_data_map не должен быть пустым.")

        # Проверяем, что ни одна строка не помечена как измененная, удаленная или новая
        for row_uuid, row_data in self.main_window.row_data_map.items():
            self.assertFalse(row_data['isChanged'], f"Строка {row_uuid} не должна быть помечена как измененная.")
            self.assertFalse(row_data['isDeleted'], f"Строка {row_uuid} не должна быть помечена как удаленная.")
            self.assertFalse(row_data['isNew'], f"Строка {row_uuid} не должна быть помечена как новая.")

        # Получаем данные из базы данных перед вызовом save_changes
        conn = sqlite3.connect(self.full_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_table")
        data_before = cursor.fetchall()
        conn.close()

        # Вызываем метод сохранения изменений
        try:
            self.main_window.save_changes(self.db_name, 'test_table')
        except Exception as e:
            self.fail(f"Метод save_changes вызвал исключение при отсутствии изменений: {e}")

        # Получаем данные из базы данных после вызова save_changes
        conn = sqlite3.connect(self.full_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_table")
        data_after = cursor.fetchall()
        conn.close()

        # Проверяем, что данные в базе данных не изменились
        self.assertEqual(data_before, data_after,
                         "Данные в базе данных не должны измениться при отсутствии модификаций.")

    def test_mandatory_field_validation(self):
        """
        Тест проверки обязательных полей при сохранении.
        """
        # Добавляем новую строку
        self.main_window.add_row()
        row_count = self.main_window.ui.tableWidget.rowCount()
        new_row_index = row_count - 2

        # Оставляем поле 'name' пустым (обязательное поле)
        age_item_new = QTableWidgetItem('29')

        self.main_window.ui.tableWidget.setItem(new_row_index, 3, age_item_new)  # 'age'

        self.main_window.on_item_changed(age_item_new)

        # Патчим QMessageBox.warning, чтобы перехватить предупреждение
        with patch('PySide6.QtWidgets.QMessageBox.warning') as mock_warning:
            self.main_window.save_changes(self.db_name, 'test_table')

            # Проверяем, что предупреждение было показано
            mock_warning.assert_called_once()
            args, kwargs = mock_warning.call_args
            # Изменение здесь: проверяем args[2] вместо args[1]
            self.assertIn("является обязательным и не может быть пустым", args[2])

        # Проверяем, что запись не была добавлена в базу данных
        conn = sqlite3.connect(self.full_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_table WHERE age = 29")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 0, "Запись с незаполненным обязательным полем не должна быть добавлена.")

    def test_type_validation(self):
        """
        Тест проверки типа данных при сохранении.
        """
        # Добавляем новую строку с некорректным типом данных для 'age'
        self.main_window.add_row()
        row_count = self.main_window.ui.tableWidget.rowCount()
        new_row_index = row_count - 2

        name_item_new = QTableWidgetItem('Frank')
        age_item_new = QTableWidgetItem('twenty')  # Некорректное значение для INTEGER

        self.main_window.ui.tableWidget.setItem(new_row_index, 2, name_item_new)  # 'name'
        self.main_window.ui.tableWidget.setItem(new_row_index, 3, age_item_new)  # 'age'

        self.main_window.on_item_changed(name_item_new)
        self.main_window.on_item_changed(age_item_new)

        # Мокируем QMessageBox.warning, чтобы перехватить предупреждение
        with patch('PySide6.QtWidgets.QMessageBox.warning') as mock_warning:
            self.main_window.save_changes(self.db_name, 'test_table')

            # Проверяем, что предупреждение было показано
            mock_warning.assert_called_once()
            args, kwargs = mock_warning.call_args
            # Изменение здесь: проверяем args[2] вместо args[1]
            self.assertIn("должно быть целым числом", args[2])

        # Проверяем, что запись не была добавлена в базу данных
        conn = sqlite3.connect(self.full_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_table WHERE name = 'Frank'")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 0, "Запись с некорректным типом данных не должна быть добавлена.")

if __name__ == '__main__':
    unittest.main()