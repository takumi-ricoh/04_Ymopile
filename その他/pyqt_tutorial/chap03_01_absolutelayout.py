# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 18:46:08 2018

@author: p000495138
"""


import sys
from PyQt5.QtWidgets import (QApplication, 
                             QWidget, 
                             QToolTip, 
                             QPushButton, 
                             QMessageBox,
                             QDesktopWidget,
                             QMainWindow,
                             QAction,qApp,
                             QMenu,
                             QTextEdit,
                             QLabel
                             )
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        lbl1 = QLabel("Zetcode",self)
        lbl1.move(15,10)
        
        lbl2 = QLabel("tutorials",self)
        lbl2.move(35,40)

        lbl3 = QLabel("for programmers",self)
        lbl3.move(55,70)        
        
        self.setGeometry(300,300,300,150)#位置、位置、幅、高さ
        self.setWindowTitle("Main Window")
        self.show()

if __name__ == '__main__':

    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())