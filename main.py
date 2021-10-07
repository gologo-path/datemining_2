import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from gui.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_window)
    widget.setFixedWidth(555)
    widget.setFixedHeight(300)
    widget.show()
    app.exec()
