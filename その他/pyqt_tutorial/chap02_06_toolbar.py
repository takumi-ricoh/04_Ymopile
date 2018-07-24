# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 12:09:08 2018

@author: p000495138
"""


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QMessageBox,QDesktopWidget,QMainWindow,QAction,qApp,QMenu
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
                
        exitAct = QAction(QIcon('exit24.png'),'Exit',self)
        #exitAct = QAction('Exit',self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.close)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)
        
        
        self.setGeometry(300,300,300,150)#位置、位置、幅、高さ
        self.setWindowTitle("Toolbar")
        self.show()

if __name__ == '__main__':

    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())