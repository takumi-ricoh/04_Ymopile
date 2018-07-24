# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 11:46:15 2018

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

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')
        
        menubar = self.menuBar()
        viewMenu = menubar.addMenu('View')
        
        viewStatAct = QAction('View statusbar',self, checkable = True)
        viewStatAct.setStatusTip('View statusbar')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)
        
        viewMenu.addAction(viewStatAct)
                
        self.setGeometry(300,300,300,150)#位置、位置、幅、高さ
        self.setWindowTitle("Check menu")
        self.show()

    def toggleMenu(self,state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

if __name__ == '__main__':

    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())