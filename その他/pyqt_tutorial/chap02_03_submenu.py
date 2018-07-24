# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 11:38:18 2018

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

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        
        impMenu = QMenu('Import',self)
        impAct = QAction('Import mail',self)
        impMenu.addAction(impAct)
        
        newAct = QAction('New',self)
        
        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)
        
                
        self.setGeometry(300,300,300,150)#位置、位置、幅、高さ
        self.setWindowTitle("Sub menu")
        self.show()

if __name__ == '__main__':

    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())