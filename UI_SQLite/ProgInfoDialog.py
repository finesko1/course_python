from PySide6.QtWidgets import QDialog
from ProgInfo import Ui_dialog as Prog_Dialog

# Окно с информацией о программе
class ProgInfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Prog_Dialog()  # Ваш UI класс
        self.ui.setupUi(self)
        self.center_element()

    def center_element(self):
        # Получаем размеры экрана
        window = self.geometry()

        # Рассчитываем координаты для центрирования окна
        x = (window.width() - window.width()) // 2
        y = (window.height() - window.height()) // 2

        # Дополнительно сдвигаем на половину размера виджета, чтобы его центр совпал с центром окна
        x += (window.width() - self.ui.info.geometry().width()) // 2
        y += (window.height() - self.ui.info.geometry().height()) // 2

        #self.ui.info.move(x, y)
        self.ui.info.setGeometry(0, 0, window.width(), window.height())
        self.ui.background.setGeometry(0, 0, window.width(), window.height())

    def resizeEvent(self, event):
        self.center_element()  # Центрируем элемент при изменении размера окна
        super().resizeEvent(event)  # Важно вызвать базовый обработчик события