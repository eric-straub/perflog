# # Perflog GUI v0.2
# # Eric Straub
# # 6/18/2024

# import sys
# import time
# import perflog
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit
# from PyQt5.QtGui import QIntValidator
# from PyQt5.QtCore import QThread, pyqtSignal

# class Worker(QThread):
#     update_label = pyqtSignal(str)

#     def __init__(self, period_box):
#         super().__init__()
#         self.period_box = period_box
#         self._running = True

#     def run(self):
#         with open("system_performance_log.txt", "a") as file:
#             period = int(self.period_box.text())
#             while self._running:
#                 # Gather performance information
#                 log_and_label = perflog.gen_perf_stats()

#                 # Write message to file
#                 file.write(log_and_label[0])
                
#                 # Emit the message to update the label
#                 self.update_label.emit(log_and_label[1])
                
#                 # Wait for specified time
#                 time.sleep(period)

#     def stop(self):
#         self._running = False

# def start_worker():
#     global worker
#     if worker is None or not worker.isRunning():
#         worker = Worker(period_box)
#         worker.update_label.connect(body_label.setText)
#         worker.start()

# def stop_worker():
#     global worker
#     if worker is not None and worker.isRunning():
#         worker.stop()
#         worker.wait()
#         worker = None

# def main():
#     global worker, period_box, body_label

#     worker = None

#     app = QApplication(sys.argv)
#     window = QMainWindow()
#     window.setWindowTitle("Perflog GUI v0.2")

#     central_widget = QWidget()
#     window.setCentralWidget(central_widget)
    
#     layout = QVBoxLayout()
#     central_widget.setLayout(layout)

#     # Label for displaying info
#     body_label = QLabel("Created by\nEric Straub")
#     layout.addWidget(body_label)

#     # Label for the text box
#     period_label = QLabel("Logging Period (seconds):")
#     layout.addWidget(period_label)

#     # Text box to set logging period
#     period_box = QLineEdit()
#     period_box.setText("5")
#     int_validator = QIntValidator()
#     period_box.setValidator(int_validator)
#     layout.addWidget(period_box)

#     # Create a button
#     start_button = QPushButton("START")
#     start_button.clicked.connect(start_worker)
#     layout.addWidget(start_button)

#     # Create a stop button
#     stop_button = QPushButton("STOP")
#     stop_button.clicked.connect(stop_worker)
#     layout.addWidget(stop_button)

#     # Adjust window size to fit content
#     window.adjustSize()

#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()

import sys
import time
import perflog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QCheckBox
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    update_label = pyqtSignal(str)

    def __init__(self, period_box, log_to_file_checkbox):
        super().__init__()
        self.period_box = period_box
        self.log_to_file_checkbox = log_to_file_checkbox
        self._running = True

    def run(self):
        period = int(self.period_box.text())
        while self._running:
            # Gather performance information
            log_and_label = perflog.gen_perf_stats()

            # Write message to file if checkbox is checked
            if self.log_to_file_checkbox.isChecked():
                with open("system_performance_log.txt", "a") as file:
                    file.write(log_and_label[0])

            # Emit the message to update the label
            self.update_label.emit(log_and_label[1])
            
            # Wait for specified time
            time.sleep(period)

    def stop(self):
        self._running = False

def start_worker():
    global worker
    if worker is None or not worker.isRunning():
        worker = Worker(period_box, log_to_file_checkbox)
        worker.update_label.connect(body_label.setText)
        worker.start()

def stop_worker():
    global worker
    if worker is not None and worker.isRunning():
        worker.stop()
        worker.wait()
        worker = None

def main():
    global worker, period_box, body_label, log_to_file_checkbox

    worker = None

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Perflog GUI v0.2")

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    # Label for displaying info
    body_label = QLabel("Created by\nEric Straub")
    layout.addWidget(body_label)

    # Label for the text box
    period_label = QLabel("Logging Period (seconds):")
    layout.addWidget(period_label)

    # Text box to set logging period
    period_box = QLineEdit()
    period_box.setText("5")
    int_validator = QIntValidator()
    period_box.setValidator(int_validator)
    layout.addWidget(period_box)

    # Checkbox to choose whether to log to file
    log_to_file_checkbox = QCheckBox("Log to file")
    layout.addWidget(log_to_file_checkbox)

    # Create a start button
    start_button = QPushButton("START")
    start_button.clicked.connect(start_worker)
    layout.addWidget(start_button)

    # Create a stop button
    stop_button = QPushButton("STOP")
    stop_button.clicked.connect(stop_worker)
    layout.addWidget(stop_button)

    # Adjust window size to fit content
    window.adjustSize()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
