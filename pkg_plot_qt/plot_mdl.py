# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:04:01 2017

@author: p000495138


"""
from PyQt5.QtGui import QFont
from pyqtgraph.Qt import QtCore, QtGui
from . import plot_base_mdl as base_p
#%%プロッタ
class Plotter():

    def __init__(self, pltcanvas, pool, cfgs):
        self.canvas   = pltcanvas
        self.pool = pool
        self.cfgs = cfgs
        self.plots = {}
        self.InitPlot()
        
    
    #初期化
    def InitPlot(self):
        
        #プロットアイテムの登録
        for key,cfg in self.cfgs.items():
            
            #レイアウト
            row     = cfg['pos'][0]
            column  = cfg['pos'][1]            
            self.layout = self.canvas.addPlot(row,column)

            #プロットの種類を指定して、プロット生成
            if cfg['kind'] == 'timeseries':
                self.plt = TimePlots(self.layout, cfg, self.pool)
            if cfg['kind'] == 'distribution':
                self.plt = DistPlots(self.layout, cfg, self.pool)

            #登録
            self.plots[key] = self.plt

    def one_shot(self):
        self.plots["PLOT1"].update()
        self.plots["PLOT2"].update()
        self.plots["PLOT3"].update()
        self.plots["PLOT4"].update()

    #スタート
    def start(self):
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.plots["PLOT1"].update)
        self.timer.timeout.connect(self.plots["PLOT2"].update)
        self.timer.timeout.connect(self.plots["PLOT3"].update)
        self.timer.timeout.connect(self.plots["PLOT4"].update)
        self.timer.start(200)    #10msごとにupdateを呼び出し

    #ストップ
    def stop(self):
        self.timer.stop()

#%%センサ時系列    
class TimePlots(base_p.Time_Plot):
        
    def __init__(self, plt, cfg, pool):
        
        
        #共通部分
        super().__init__(plt, pool)

        #初期設定
        self.plt.setTitle(cfg["title"])
        self.plt.setLabel("bottom",text="time")
        self.plt.setLabel("left",text="temperature")        
        self.plt.showGrid(x=True,y=True)
        self.plt.setYRange(0,300) 
        self.plt.addLegend() 

        #グラフの初期化
        self.init_line(cfg['keys'], cfg['legend'])

#%%センサ温度分布    
class DistPlots(base_p.Dist_Plot):
        
    def __init__(self, plt, cfg, pool):

        super().__init__(plt, pool)

        #初期設定
        self.plt.setTitle(cfg["title"])
        self.plt.setLabel("bottom",text="x[mm]")
        self.plt.setLabel("left",text="temperature")        
        self.plt.showGrid(x=True,y=True)
        self.plt.setYRange(0,300) 
        self.plt.addLegend() 

        #グラフの初期化
        self.init_line(cfg['keys'], cfg['xx'], cfg['legend'])       