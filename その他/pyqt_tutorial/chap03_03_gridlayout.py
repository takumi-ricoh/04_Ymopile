# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 19:06:58 2018

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
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout,
                             QGridLayout,
                             )
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        
        grid = QGridLayout()
        self.setLayout(grid)
        
        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']
        
        positions = [(i,j) for i in range(5) for j in range(4)]
        
        for position, name in zip(positions, names):
            
            if name == "":
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)
        
        self.move(300,150)        
        self.setWindowTitle("Calculator")
        self.show()

if __name__ == '__main__':

    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())