import sys
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.uic import loadUi
from time import sleep
from DataProcessor import DataProcessor


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui/MainWindow.ui", self)
        self.browser_button.clicked.connect(self.file_browser)
        self.start_button.clicked.connect(self.start_calc)
        self.dp = DataProcessor()

    def file_browser(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", filter="CSV files (*.csv)")
        self.file_path.setText(fname[0])

    def start_calc(self):
        self.dp.start_processing(self.file_path.text(), self.text_area.toPlainText().split(","))
        result = self.dp.get_result()
        self._set_response("spam" if result["ham"] < result["spam"] else "ham")

    def _set_response(self, rs: str):
        self.response.setText(rs)

