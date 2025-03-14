from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QTextCursor
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtWidgets import QCompleter
from PySide6.QtCore import QStringListModel

class SQLSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Определяем формат для ключевых слов
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        # Определяем формат для функций
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("darkMagenta"))
        function_format.setFontWeight(QFont.Weight.Bold)

        # Определяем формат для типов данных
        type_format = QTextCharFormat()
        type_format.setForeground(QColor("darkCyan"))
        type_format.setFontWeight(QFont.Weight.Bold)

        # Список ключевых слов SQL
        self.keywords = [
            "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE",
            "CREATE", "TABLE", "ALTER", "DROP", "JOIN", "ON", "AS", "AND", "OR", "NOT", "NULL",
            "PRIMARY", "KEY", "FOREIGN", "REFERENCES", "INDEX", "VIEW", "TRIGGER", "BEGIN", "END",
            "TRANSACTION", "COMMIT", "ROLLBACK", "UNION", "ALL", "DISTINCT", "GROUP", "BY", "ORDER",
            "HAVING", "LIMIT", "OFFSET"
        ]

        # Список функций SQL
        self.functions = [
            "AVG", "COUNT", "MIN", "MAX", "SUM"
        ]

        # Список типов данных SQL
        self.types = [
            "INTEGER", "TEXT", "REAL", "BLOB", "NULL"
        ]

        # Создаем правила подсветки для каждого ключевого слова
        for keyword in self.keywords:
            pattern = QRegularExpression(f"\\b{keyword}\\b", QRegularExpression.CaseInsensitiveOption)
            self.highlighting_rules.append((pattern, keyword_format))

        # Создаем правила подсветки для каждой функции
        for function in self.functions:
            pattern = QRegularExpression(f"\\b{function}\\b", QRegularExpression.CaseInsensitiveOption)
            self.highlighting_rules.append((pattern, function_format))

        # Создаем правила подсветки для каждого типа данных
        for type_ in self.types:
            pattern = QRegularExpression(f"\\b{type_}\\b", QRegularExpression.CaseInsensitiveOption)
            self.highlighting_rules.append((pattern, type_format))

        # Настройка автодополнения
        self.completer = QCompleter()
        self.model = QStringListModel()
        self.completer.setModel(self.model)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

    def highlightBlock(self, text):
        # Анализ слов и применение форматов
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)

        # Обновление подсказок на основе последнего ключевого слова
        words = text[:self.currentBlock().position() + self.currentBlock().length()].split()
        if words:
            last_word = words[-1].upper()
            suggestions = self.get_suggestions(last_word)
            if suggestions:
                self.model.setStringList(suggestions)
                self.completer.setCompletionPrefix(last_word)
                cursor_rect = self.parent().cursorRect()
                cursor_rect.setWidth(self.completer.popup().sizeHintForColumn(0)
                                     + self.completer.popup().verticalScrollBar().sizeHint().width())
                self.completer.complete(cursor_rect)
            else:
                self.completer.popup().hide()
        else:
            self.completer.popup().hide()

    def get_suggestions(self, last_word):
        # Определяем подсказки для ключевых слов
        suggestions = {
            "SELECT": ["FROM", "WHERE", "GROUP BY", "ORDER BY"],
            "INSERT": ["INTO", "VALUES"],
            "UPDATE": ["SET", "WHERE"],
            "DELETE": ["FROM", "WHERE"],
            "CREATE": ["TABLE", "INDEX", "VIEW"],
            "DROP": ["TABLE", "INDEX", "VIEW"],
            "ALTER": ["TABLE", "ADD", "DROP", "MODIFY"],
        }
        return suggestions.get(last_word, [])

    def insert_completion(self, completion):
        cursor = self.parent().textCursor()
        cursor_position = cursor.position()

        # Начинаем редактирование блока
        cursor.beginEditBlock()

        # Перемещаем курсор к началу текущего слова
        cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.MoveAnchor)

        # Удаляем введенную часть слова
        cursor.setPosition(cursor_position, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()

        # Вставляем выбранное слово
        cursor.insertText(completion + " ")

        # Завершаем редактирование блока
        cursor.endEditBlock()

        self.parent().setTextCursor(cursor)