# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:46:40 2018

@author: p000495138
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.setGeometry(300,300,300,220)#位置、位置、幅、高さ
        self.setWindowTitle("Icon")
        self.setWindowIcon(QIcon("web.png"))

        self.show()

if __name__ == '__main__':
    
    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)

    ex = Example()
    
    sys.exit(app.exec_())