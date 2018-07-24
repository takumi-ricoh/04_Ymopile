# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 17:30:19 2017

@author: p000495138
"""

import Sensor.MachineLog
import Sensor.SensorLog
import Sensor.Ploter
import pandas as pd
import numpy as np
import ctypes

#%%
""" 初期化 """
mlog    = Sensor.MachineLog.MachineLog()
slog    = Sensor.SensorLog.SensorLog()
ploter  = Sensor.Ploter.Ploter()
ploter.init_ax0(2) #2本
ploter.init_ax1(2) #2本

mlog.set_ch("COM26")
slog.set_ch("COM24")

#キーボード待ち
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B      


#%%
""" 実行 """ 
for i in range(99999):
    if getkey(ESC):     # ESCキーが押されたら終了
       break    
    
    mlog.update() #値の読み出し
    slog.update() #値の読み出し
    
    if i%20==0:
        #データｆフレームとして読み出す
        f22_sen1    = pd.DataFrame(mlog.f22["Sen1"],columns=["time","Tar","Cur","Sen"])
        f22_sen3    = pd.DataFrame(mlog.f22["Sen3"],columns=["time","Tar","Cur","Sen"])
        f26_heater1 = pd.DataFrame(mlog.f26["Heater1"],columns=["time","MVn","FF_Duty","Max_Duty","Duty","Heater"])
        f26_heater2 = pd.DataFrame(mlog.f26["Heater2"],columns=["time","MVn","FF_Duty","Max_Duty","Duty","Heater"])
    
        #%% マシンログ時刻補正    
        if len(f22_sen1)>0:
            f22_t0 = f22_sen1["time"][0]
            f22_sen1["time2"] = f22_sen1["time"] - f22_t0
            f22_sen3["time2"] = f22_sen3["time"] - f22_t0
        if len(f26_heater1)>0:
            f26_t0 = f26_heater1["time"][0]
            f26_heater1["time2"] = f26_heater1["time"] - f26_t0
            f26_heater2["time2"] = f26_heater2["time"] - f26_t0    
        sensor = pd.DataFrame(slog.sensor["Sen1"],columns=["millis","vobj","tobj","tamb"])
        
        #%% プロット
#        if len(f22_sen1)>0:
#            ploter.update(f22_sen1["time2"],f22_sen1["Cur"],0,0)
#            ploter.update(f22_sen3["time2"],f22_sen3["Cur"],0,1)
#            xmin = min(f22_sen1["time2"]) - 10
#            xmax = max(f22_sen1["time2"]) + 10
#            ymin = 0
#            ymax = 200
#            ploter.set_limit(xmin,xmax,ymin,ymax,0)
#        if len(f26_heater1)>0:
#            ploter.update(f26_heater1["time2"],f26_heater1["Duty"],1,0)
#            ploter.update(f26_heater2["time2"],f26_heater2["Duty"],1,1)
#            xmin = min(f26_heater1["time2"]) - 10
#            xmax = max(f26_heater1["time2"]) + 10
#            ymin = -10
#            ymax = 120
#            ploter.set_limit(xmin,xmax,ymin,ymax,1)
