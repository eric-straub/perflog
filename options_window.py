import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QFileDialog

class OptionsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Options")
        self.setGeometry(100, 100, 400, 200)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.period_label = QLabel("Default Logging Period (seconds):")
        layout.addWidget(self.period_label)

        self.period_box = QLineEdit()
        layout.addWidget(self.period_box)

        self.log_to_file_checkbox = QCheckBox("Log to file by default")
        layout.addWidget(self.log_to_file_checkbox)

        self.file_path_label = QLabel("Log File Path:")
        layout.addWidget(self.file_path_label)

        self.file_path_box = QLineEdit()
        layout.addWidget(self.file_path_box)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file_path)
        layout.addWidget(self.browse_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_options)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)
        self.load_options()

    def browse_file_path(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select Log File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.file_path_box.setText(file_path)

    def save_options(self):
        options = {
            'default_period': self.period_box.text(),
            'log_to_file': self.log_to_file_checkbox.isChecked(),
            'file_path': self.file_path_box.text()
        }
        with open("options.json", "w") as file:
            json.dump(options, file)
        self.accept()  # Close the dialog

    def load_options(self):
        try:
            with open("options.json", "r") as file:
                options = json.load(file)
                self.period_box.setText(options.get('default_period', ''))
                self.log_to_file_checkbox.setChecked(options.get('log_to_file', False))
                self.file_path_box.setText(options.get('file_path', 'system_performance_log.txt'))
        except FileNotFoundError:
            pass
