# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:40:29 2018

@author: p000495138
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    
    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)
    
    #ウィンドウ生成
    w = QWidget()
    
    w.resize(250,250)
    
    w.move(300,300)
    
    w.setWindowTitle('simple')
    
    w.show()
    
    sys.exit(app.exec_())
    
    