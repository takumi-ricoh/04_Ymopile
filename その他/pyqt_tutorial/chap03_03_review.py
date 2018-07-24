# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 19:14:08 2018

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
                             QLineEdit,
                             )
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        
        title = QLabel("Title")
        author = QLabel("Author")
        review = QLabel("Review")
        
        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()
        
        grid = QGridLayout()
        grid.setSpacing(10)        
        
        grid.addWidget(title,1,0)
        grid.addWidget(titleEdit,1,1)

        grid.addWidget(author,2,0)
        grid.addWidget(authorEdit,2,1)

        grid.addWidget(review,3,0)
        grid.addWidget(reviewEdit,3,1,5,1)        
        
        self.setLayout(grid)

        self.setGeometry(300,300,300,150)#位置、位置、幅、高さ   
        self.setWindowTitle("Review")
        self.show()

if __name__ == '__main__':

    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())