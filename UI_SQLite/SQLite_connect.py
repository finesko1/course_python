import logging
import sqlite3

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SQLiteConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def connect(self):
        """Устанавливает соединение с базой данных."""
        try:
            self.connection = sqlite3.connect(self.db_file)
            #logging.info(f"Подключено к базе данных {self.db_file}")
        except sqlite3.Error as e:
            logging.error(f"Ошибка подключения к базе данных {self.db_file}: {e}")

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            try:
                self.connection.close()
                logging.info(f"Соединение с базой данных {self.db_file} закрыто.")
            except sqlite3.Error as e:
                logging.error(f"Ошибка при закрытии соединения с базой данных {self.db_file}: {e}")

    def execute_query(self, query, params=None, is_select=False, commit=True):
        """Выполняет SQL-запрос и отслеживает его выполнение."""
        if self.connection:
            cursor = self.connection.cursor()
            try:
                if params:
                    logging.info(f"Выполняется запрос: {query} с параметрами {params}")
                    cursor.execute(query, params)
                else:
                    logging.info(f"Выполняется запрос: {query}")
                    cursor.execute(query)

                if not is_select and commit:
                    self.connection.commit()

                if is_select:
                    results = cursor.fetchall()
                    return results
            except sqlite3.Error as e:
                logging.error(f"Ошибка выполнения запроса '{query}': {e}")
                raise
            finally:
                cursor.close()
        else:
            logging.error("Соединение с базой данных не установлено.")
            raise sqlite3.Error("Соединение с базой данных не установлено.")

    def get_tables(self):
        """Возвращает список имен таблиц в базе данных."""
        if not self.connection:
            logging.error("Соединение с базой данных не установлено.")
            return []

        try:
            # Создаем курсор для выполнения запроса
            cursor = self.connection.cursor()
            # Выполняем запрос для получения имен таблиц
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            # Закрываем курсор вручную
            cursor.close()
            # Преобразуем список кортежей в список строк с именами таблиц
            table_names = [table[0] for table in tables]
            sorted_table_names = sorted(table_names, key=lambda x: (1 if x[0].isascii() else 0, x.lower()))
            logging.info(f"Таблицы в базе данных {self.db_file}: {sorted_table_names}")
            return sorted_table_names

        except sqlite3.Error as e:
            logging.error(f"Ошибка при получении таблиц из базы данных {self.db_file}: {e}")
            return []

    def get_column_names(self, table_name):
        """Возвращает список имен столбцов для заданной таблицы."""
        if not self.connection:
            logging.error("Соединение с базой данных не установлено.")
            return []

        try:
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info('{table_name}');")
            columns_info = cursor.fetchall()
            cursor.close()
            column_names = [column[1] for column in columns_info]
            logging.info(f"Столбцы таблицы '{table_name}': {column_names}")
            return column_names

        except sqlite3.Error as e:
            logging.error(f"Ошибка при получении столбцов таблицы '{table_name}': {e}")
            return []

    def init_test_table(self):
        """Пример создания тестовой таблицы."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                create_table_query = """
                    CREATE TABLE IF NOT EXISTS test_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER
                    );
                """
                cursor.execute(create_table_query)
                logging.info("Таблица test_table создана или уже существует.")
            except sqlite3.Error as e:
                logging.error(f"Ошибка при создании таблицы test_table: {e}")
        else:
            logging.error("Соединение с базой данных не установлено.")

    def get_table_structure(self, table_name):
        """Возвращает информацию о столбцах таблицы."""
        if not self.connection:
            logging.error("Соединение с базой данных не установлено.")
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info('{table_name}');")
            columns_info = cursor.fetchall()
            cursor.close()
            # Возвращаем список словарей с информацией о каждом столбце
            columns = []
            for column in columns_info:
                col_dict = {
                    'cid': column[0],
                    'name': column[1],
                    'type': column[2],
                    'notnull': bool(column[3]),
                    'dflt_value': column[4],
                    'pk': bool(column[5])
                }
                columns.append(col_dict)
            logging.info(f"Структура таблицы '{table_name}': {columns}")
            return columns
        except sqlite3.Error as e:
            logging.error(f"Ошибка при получении структуры таблицы '{table_name}': {e}")
            return []