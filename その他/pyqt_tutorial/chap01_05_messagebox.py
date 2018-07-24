# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 09:30:40 2018

@author: p000495138
"""


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QMessageBox
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setGeometry(300,300,300,220)#位置、位置、幅、高さ
        self.setWindowTitle("Quit button")
        self.show()

    def closeEvent(self, event):
        #QWidgetを閉じようとすると、QCloseEventが発生します。
        #ウィジェットの振る舞いを修正するため、closeEvent()というイベントハンドラを実装し直す必要があります。
        
        reply = QMessageBox.question(self, 'Message',
                                     'Are you sure to quit?',QMessageBox.Yes | 
                                     QMessageBox.No, QMessageBox.No)
        #Yes/Noボタンとともにメッセージボックスを表示します。
        #最初の文字列(第2引数)はタイトルバーに表示され、続く文字列(第3引数)はダイアログ本体に表示されます。
        #第4引数はダイアログの中で表示されるボタンを指定しています(他にもQMessageBox.YesAllなどの選択肢有り)。
        #最後の引数はデフォルトでフォーカスの当たっているボタンを指定します。つまり、そのままエンターキーを押下した場合はNoボタンが押されることになります。
        if reply == QMessageBox.Yes:
            event.accept()
            
        else:
            event.ignore()

if __name__ == '__main__':

    app = QApplication.instance()

    #インスタンスが無い場合のみ新たに作成
    if app is None:
        app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())