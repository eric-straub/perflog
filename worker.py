# import time
# import perflog
# from PyQt5.QtCore import QThread, pyqtSignal

# class Worker(QThread):
#     update_label = pyqtSignal(str)

#     def __init__(self, period_box, log_to_file_checkbox):
#         super().__init__()
#         self.period_box = period_box
#         self.log_to_file_checkbox = log_to_file_checkbox
#         self._running = True

#     def run(self):
#         period = int(self.period_box.text())
#         while self._running:
#             # Gather performance information
#             log_and_label = perflog.gen_perf_stats()

#             # Write message to file if checkbox is checked
#             if self.log_to_file_checkbox.isChecked():
#                 with open("system_performance_log.txt", "a") as file:
#                     file.write(log_and_label[0])

#             # Emit the message to update the label
#             self.update_label.emit(log_and_label[1])
            
#             # Wait for specified time
#             time.sleep(period)

#     def stop(self):
#         self._running = False

import time
import perflog
from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    update_label = pyqtSignal(str)

    def __init__(self, period_box, log_to_file_checkbox, file_path_box):
        super().__init__()
        self.period_box = period_box
        self.log_to_file_checkbox = log_to_file_checkbox
        self.file_path_box = file_path_box
        self._running = True

    def run(self):
        period = int(self.period_box.text())
        file_path = self.file_path_box.text()
        while self._running:
            # Gather performance information
            log_and_label = perflog.gen_perf_stats()

            # Write message to file if checkbox is checked
            if self.log_to_file_checkbox.isChecked():
                with open(file_path, "a") as file:
                    file.write(log_and_label[0])

            # Emit the message to update the label
            self.update_label.emit(log_and_label[1])
            
            # Wait for specified time
            time.sleep(period)

    def stop(self):
        self._running = False
