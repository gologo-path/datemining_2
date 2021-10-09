import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from gui.MainWindow import MainWindow
from DataProcessor import DataProcessor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_window)
    widget.setFixedWidth(555)
    widget.setFixedHeight(300)
    widget.show()
    app.exec()

    # dp = DataProcessor()
    # dp.start_processing("input/sms-spam-corpus.csv", "prize, price".split(","))
    # result = dp.get_result()
    #
    # print("spam" if result["ham"] < result["spam"] else "ham")

