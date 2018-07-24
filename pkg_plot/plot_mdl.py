# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:04:01 2017

@author: p000495138


"""


import matplotlib.pyplot as plt
from pkg_plot import plot_base_mdl as base_p

#%%プロッタ
class Plotter():
    """
    グラフを配置する
    """
    def __init__(self, cfg):
        self.pos = cfg.SENPOS
        plt.close()
    
        #グラフ生成
        self.fig, self.ax = plt.subplots(2,2, figsize=(13, 6))
        self.fig.show()
        
        #グラフ初期化
        self.sensor  = SensorPlots (self.fig, self.ax[0,0])
        self.machine = MachinePlots(self.fig, self.ax[0,1]) 
        self.dist    = DistPlots   (self.fig, self.ax[1,0])     
    
        #self.fig.tight_layout()
    
#%%センサ時系列    
class SensorPlots(base_p.Time_Plot):
        
    def __init__(self, fig, ax):

        super().__init__(fig, ax)

        self.ax.set_title("sensor")
        

#%%マシンログ時系列    
class MachinePlots(base_p.Time_Plot):
        
    def __init__(self, fig, ax,):
        
        super().__init__(fig, ax,)
        
        self.ax.set_title("machineLog")

        
#%%センサ温度分布    
class DistPlots(base_p.Dist_Plot):
        
    def __init__(self, fig, ax):
        self.fig    = fig
        self.ax     = ax
        self.ax.set_title("DistPlot")

        super().__init__(self.fig, self.ax)
        