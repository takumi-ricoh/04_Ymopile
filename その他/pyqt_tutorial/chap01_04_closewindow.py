# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 13:30:00 2018

@author: p000495138
"""


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def closing(self):
        self.close()

    def initUI(self):

        qbtn = QPushButton("Quit", self)
        #qbtn.clicked.connect(QCoreApplication.instance().quit) #NG
        qbtn.clicked.connect(self.closing) #OK
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50,50)

        self.setGeometry(300,300,300,220)#位置、位置、幅、高さ
        self.setWindowTitle("Quit button")
        self.show()


if __name__ == '__main__':

    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())