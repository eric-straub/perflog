# Perflog GUI v0.3
# Eric Straub
# 6/18/2024

import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QCheckBox
from PyQt5.QtGui import QIntValidator
from worker import Worker
from options_window import OptionsWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
        self.load_options()
        
    def init_ui(self):
        self.setWindowTitle("Perflog GUI v0.2")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Label for displaying info
        self.body_label = QLabel("Created by\nEric Straub")
        layout.addWidget(self.body_label)

        # Label for the text box
        period_label = QLabel("Logging Period (seconds):")
        layout.addWidget(period_label)

        # Text box to set logging period
        self.period_box = QLineEdit()
        self.period_box.setText("5")
        int_validator = QIntValidator()
        self.period_box.setValidator(int_validator)
        layout.addWidget(self.period_box)

        # Checkbox to choose whether to log to file
        self.log_to_file_checkbox = QCheckBox("Log to file")
        layout.addWidget(self.log_to_file_checkbox)

        # File path for logging
        self.file_path_box = QLineEdit()
        layout.addWidget(self.file_path_box)

        # Create a start button
        start_button = QPushButton("START")
        start_button.clicked.connect(self.start_worker)
        layout.addWidget(start_button)

        # Create a stop button
        stop_button = QPushButton("STOP")
        stop_button.clicked.connect(self.stop_worker)
        layout.addWidget(stop_button)

        # Create an options button
        options_button = QPushButton("OPTIONS")
        options_button.clicked.connect(self.open_options_window)
        layout.addWidget(options_button)

        # Adjust window size to fit content
        self.adjustSize()

    def start_worker(self):
        if self.worker is None or not self.worker.isRunning():
            self.worker = Worker(self.period_box, self.log_to_file_checkbox, self.file_path_box)
            self.worker.update_label.connect(self.body_label.setText)
            self.worker.start()

    def stop_worker(self):
        if self.worker is not None and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
            self.worker = None

    def open_options_window(self):
        options_window = OptionsWindow()
        options_window.exec_()
        self.load_options()

    def load_options(self):
        try:
            with open("options.json", "r") as file:
                options = json.load(file)
                self.period_box.setText(options.get('default_period', '5'))
                self.log_to_file_checkbox.setChecked(options.get('log_to_file', False))
                self.file_path_box.setText(options.get('file_path', 'system_performance_log.txt'))
        except FileNotFoundError:
            pass

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
