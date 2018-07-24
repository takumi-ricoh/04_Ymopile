# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:04:01 2017

@author: p000495138


***** 概要 *****
・グラフを初期化
・外部から、update()メソッドでlineを更新する。
  ・同じグラフ中のlineの数はNumOfLine
  ・set_dataは、1つのlineに対して行う

    fig ─┬───ax[0]─┬── line[0][0]
         │         │
         │         │
         │         ├── line[0][1]
         │         │
         │         │
         │         └── line[0][2]
         │
         └───ax[1]  

*****************

"""


import matplotlib.pyplot as plt
import numpy as np

class Ploter():
    
    plt.close()
    
    def __init__(self):
        #グラフは2つ作る
        self.fig, self.ax = plt.subplots(2,1)
        plt.tight_layout()
        self.line=[[],[]]
        self.bg=[0,0]

    #%% 温度グラフ 
    def init_ax0(self,NumOfLine=1): 
        for i in range(NumOfLine):
            self.line[0].append(self.ax[0].plot(0,0,".-")[0])
            plt.hold(True)
        self.ax[0].grid(True)
        self.ax[0].set_xlabel("time")
        self.ax[0].set_ylabel("temperature")
        self.fig.canvas.draw()
        self.bg[0] = self.fig.canvas.copy_from_bbox(self.ax[0].bbox)
            
    #%% dutyグラフ
    def init_ax1(self,NumOfLine=1):
        for i in range(NumOfLine):
            self.line[1].append(self.ax[1].plot(0,0,".-")[0])
            plt.hold(True)
        self.ax[1].grid(True)
        self.ax[1].set_xlabel("time")
        self.ax[1].set_ylabel("Duty")
        self.fig.canvas.draw()
        self.bg[1] = self.fig.canvas.copy_from_bbox(self.ax[1].bbox)

    #%% 更新：line1本ごと
    def update(self,x,y,n,i): #line[n][i]への更新
        if type(self.line[n]) == list:
            self.line[n][i].set_data(x,y)
            self.ax[n].draw_artist(self.line[n][i])
        else:
            self.line[n].set_data(x,y)
            self.ax[n].draw_artist(self.line[n])
        #ライン更新
        self.fig.canvas.restore_region(self.bg[n])
        self.fig.canvas.draw()
        #画面の更新
        self.fig.canvas.update()
        self.fig.canvas.flush_events()
    
    #%% limit設定    
    def set_limit(self,xmin,xmax,ymin,ymax,n):
        self.ax[n].set_xlim(xmin,xmax)
        self.ax[n].set_ylim(ymin,ymax)