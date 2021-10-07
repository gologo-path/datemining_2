import sys
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.uic import loadUi
from time import sleep


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui/MainWindow.ui", self)
        self.browser_button.clicked.connect(self.file_browser)
        self.start_button.clicked.connect(self.start_calc)

    def file_browser(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", filter="CSV files (*.csv)")
        self.file_path.setText(fname[0])

    def start_calc(self):
        self.path = self.file_path.text()
        self.phrase = self.text_area.toPlainText()
        self._do_work()

    def _do_work(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def _set_response(self, rs: str):
        self.response.setText(rs)


class Worker(QObject):
    finished = pyqtSignal()

    def run(self):
        """Paste long-time task here"""
        self.finished.emit()
