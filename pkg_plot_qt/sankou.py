# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 20:41:41 2018

@author: p000495138
"""

# -*- coding:utf-8 -*-

#プロット関係のライブラリ
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import sys
import time

#音声関係のライブラリ
#import pyaudio
#import struct


pg.setConfigOption('background', 'w')
pg.setConfigOptions(antialias=True)

class PlotWindow:
    def __init__(self):
        #プロット初期設定

        self.win=pg.GraphicsWindow()
        self.win.setWindowTitle(u"リアルタイムプロット")
        self.plt=self.win.addPlot(0,1) #プロットのビジュアル関係
        self.plt=self.win.addPlot(1,1) #プロットのビジュアル関係
        self.plt.setYRange(-1,1)    #y軸の上限、下限の設定
        self.plt.setTitle("title")    #y軸の上限、下限の設定
        self.plt.showGrid(x=True,y=True)
        
        self.curves=[]
        for i in range(10):
            color = np.random.randint(0,255,3)
            curve = self.plt.plot(pen=pg.mkPen(color))
            self.curves.append(curve)

        self.start = time.time()

#        #マイクインプット設定
#        self.CHUNK=1024             #1度に読み取る音声のデータ幅
#        self.RATE=44100             #サンプリング周波数
#        self.audio=pyaudio.PyAudio()
#        self.stream=self.audio.open(format=pyaudio.paInt16,
#                                    channels=1,
#                                    rate=self.RATE,
#                                    input=True,
#                                    frames_per_buffer=self.CHUNK)

        #アップデート時間設定
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)    #10msごとにupdateを呼び出し

        #音声データの格納場所(プロットデータ)
        #self.data=np.zeros(self.CHUNK)

    def update(self):
        #self.data=self.AudioInput()
        for curve in self.curves:
            datax = np.random.randn(100)
            datay = np.random.randn(100)
            curve.setData(datax,datay)   #プロットデータを格納
        self.dt   = time.time() - self.start
        self.start = time.time()
        self.fps  = 1/self.dt
        print(self.fps)

#    def AudioInput(self):
#        ret=self.stream.read(self.CHUNK)    #音声の読み取り(バイナリ)
#        #バイナリ → 数値(int16)に変換
#        #32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)
#        ret=np.frombuffer(ret, dtype="int16")/32768.0
#        return ret

#plotwin=PlotWindow()

if __name__=="__main__":
    plotwin=PlotWindow()

    if (sys.flags.interactive!=1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        


