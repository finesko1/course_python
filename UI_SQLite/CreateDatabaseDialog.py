import os
import sqlite3

from PySide6.QtWidgets import QDialog, QMessageBox

from CreateDatabase import Ui_Dialog as CreateDB_Dialog

# Окно с созданием БД
class CreateDbDialog(QDialog):
    def __init__(self, work_directory):
        super().__init__()
        self.ui = CreateDB_Dialog()
        self.ui.setupUi(self)
        self.work_directory = work_directory
        self.info = self.ui.label.text() + " в " + work_directory
        self.ui.label.setText(self.info)

        # Обработка кнопки создания БД
        self.ui.AddDatabaseButton.clicked.connect(lambda: self.add_database(self.work_directory))

    def add_database(self, work_directory):
        # Проверка существования директории
        if os.path.exists(work_directory):
            # Преобразование пути в нормальный формат
            work_directory = os.path.normpath(work_directory)
            # Имя БД
            db_name = self.ui.DatabaseName.text().strip()  # Убираем пробелы
            if db_name:  # Проверка, что имя базы данных введено
                try:
                    # Проверка расширения
                    if not db_name.endswith(('.sqlite', '.db')):
                        db_name += '.sqlite'
                    db_path = os.path.normpath(os.path.join(work_directory, db_name))
                    # Проверка существования БД в списке директории
                    if os.path.exists(db_path):
                        QMessageBox.warning(self, "Ошибка",
                                            f"База данных '{db_name}' уже существует в {work_directory}.")
                        return
                    # Создание подключения (создаст файл БД, если его нет)
                    connect = sqlite3.connect(db_path)
                    connect.close()

                    # Уведомление об успешном создании базы
                    QMessageBox.information(self, "Успех",
                                            f"База данных '{db_name}' успешно создана в {work_directory}.")
                except sqlite3.Error as e:
                    # Обработка ошибок SQLite
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при создании базы данных: {str(e)}")
                except Exception as e:
                    # Обработка других ошибок
                    QMessageBox.critical(self, "Ошибка", f"Непредвиденная ошибка: {str(e)}")
            else:
                QMessageBox.warning(self, "Ошибка", "Введите имя базы данных.")
        else:
            QMessageBox.warning(self, "Ошибка", "Не выбрана рабочая директория.")