from PySide6.QtWidgets import QTextEdit, QCompleter
from PySide6.QtCore import Qt, QStringListModel
from PySide6.QtGui import QTextCursor

class AutoCompleteTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.completer = None
        self.keywords = [
            "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES", "UPDATE",
            "SET", "DELETE", "CREATE", "TABLE", "ALTER", "DROP", "JOIN",
            "ON", "AS", "AND", "OR", "NOT", "NULL", "PRIMARY", "KEY",
            "FOREIGN", "REFERENCES", "INDEX", "VIEW", "TRIGGER", "BEGIN",
            "END", "TRANSACTION", "COMMIT", "ROLLBACK", "UNION", "ALL",
            "DISTINCT", "GROUP", "BY", "ORDER", "HAVING", "LIMIT", "OFFSET"
        ]
        self.hints = {
            "SELECT": "Укажите поля или *",
            "FROM": "имя таблицы",
            "WHERE": "условие",
            "INSERT": "INTO таблица (поля)",
            "UPDATE": "таблица SET поле = значение",
            # Добавьте другие подсказки по необходимости
        }
        self.create_completer()

    def create_completer(self):
        self.model = QStringListModel(self.keywords)
        self.completer = QCompleter(self.model, self)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)

    def insert_completion(self, completion):
        cursor = self.textCursor()
        cursor_position = cursor.position()

        cursor.beginEditBlock()

        # Перемещаем курсор к началу текущего слова и выделяем текст до исходной позиции
        cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)

        # Удаляем выделенный текст (введённую часть слова)
        cursor.removeSelectedText()

        # Вставляем выбранное автодополнение
        cursor.insertText(completion + " ")

        cursor.endEditBlock()

        self.setTextCursor(cursor)

        # Добавление и выделение подсказки, если есть
        hint_text = self.get_hint_for_completion(completion)
        if hint_text:
            cursor.insertText(hint_text)
            # Выделяем текст подсказки
            cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor, len(hint_text))
            self.setTextCursor(cursor)

    def get_hint_for_completion(self, completion):
        return self.hints.get(completion.upper(), "")

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape,
                               Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return

        super().keyPressEvent(event)

        completion_prefix = self.textUnderCursor()
        if len(completion_prefix) >= 2:
            self.completer.setCompletionPrefix(completion_prefix)
            if self.completer.completionCount() > 0:
                self.completer.popup().setCurrentIndex(
                    self.completer.completionModel().index(0, 0)
                )
                cr = self.cursorRect()
                cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                            + self.completer.popup().verticalScrollBar().sizeHint().width())
                self.completer.complete(cr)
            else:
                self.completer.popup().hide()
        else:
            self.completer.popup().hide()

    def textUnderCursor(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        return cursor.selectedText()