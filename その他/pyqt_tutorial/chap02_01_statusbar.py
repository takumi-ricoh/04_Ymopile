# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 13:20:20 2018

@author: p000495138
"""


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QMessageBox,QDesktopWidget,QMainWindow
from PyQt5.QtCore import QCoreApplication

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.statusBar().showMessage("Ready")
        
        self.setGeometry(300,300,300,150)#位置、位置、幅、高さ
        self.setWindowTitle("Statusbar")
        self.show()

if __name__ == '__main__':

    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())