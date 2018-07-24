# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 13:15:33 2018

@author: p000495138
"""


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QMessageBox,QDesktopWidget
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.resize(250, 150)
        self.center()
        
        self.setWindowTitle('Center')
        self.show()

    def center(self):
        
        qr = self.frameGeometry()
        #メインウィンドウの座標を特定するような長方形の情報(PyQt5.QtCore.QRectクラスのオブジェクト)を取得します。
        #これにはウィンドウフレームの情報も入っています。
        cp = QDesktopWidget().availableGeometry().center()
        #プログラム実行者のモニタの解像度、それから中央のポイントを取得します。
        qr.moveCenter(cp)
        #qrオブジェクトは既にウィンドウの幅と高さの情報を持っており、中央座標の情報も持っています。
        #その中央座標をcp、つまり先ほど求めたプログラム実行者のモニタの中央に移動します。
        #サイズは変わりません。
        self.move(qr.topLeft())

if __name__ == '__main__':

    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())