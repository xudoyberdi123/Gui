from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys


def salom():
    print("salom")


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Salom dunyo")
        label = QLabel("salom olam")
        label2 = QLabel("salom olam2")


        btn = QPushButton()
        btn.setText("Click me")
        btn.clicked.connect(salom)


        self.setMenuWidget(label)
        self.setMenuWidget(label2)
        self.setCentralWidget(btn)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
