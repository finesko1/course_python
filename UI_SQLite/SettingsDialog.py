from PySide6.QtWidgets import QDialog

from Settings import Ui_Dialog as Settings_Dialog

# Окно с настройками программы
class SettingsDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Settings_Dialog()
        self.ui.setupUi(self)

        self.main_window = main_window
        # Параметры программы
        self.ui.AllTablesCheckBox.setChecked(self.main_window.show_all_tables)

        self.ui.SaveChangesButton.clicked.connect(self.save_changes)

    def save_changes(self):
        self.main_window.show_all_tables = self.ui.AllTablesCheckBox.isChecked()
        self.close()