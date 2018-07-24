# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 12:52:27 2017

@author: p000495138

***** 概要 *****

・シリアル通信をして1行読み出す
・中身を判定して、リストにappendする

*****************

"""

import numpy as np

#%%　f22        
def f22(data):
    #分ける
    temp1 = data
    temp2 = temp1.split('|')
    temp3 = temp2[-1].split(',')
    #時刻を計算
    time_str = temp2[2].split(':')
    time = float(time_str[0])*60 + float(time_str[1]) #秒単位換算
    #数値に変換
    Tar = np.float64(temp3[1])
    Cur = np.float64(temp3[3])
    #センサ種類
    Sen = temp2[1]
    #print(Sensor)
    return [time,Tar,Cur,Sen]

#%%　f26    
def f26(data):
    #分ける
    temp1 = data
    temp2 = temp1.split('|')
    temp3 = temp2[-1].split(',')
    #時刻を計算
    time_str = temp2[2].split(':')
    time = float(time_str[0])*60 + float(time_str[1]) #秒単位換算
    #Dutyの部分を分ける
    moji,MVn      = temp3[0].split('=')    
    moji,FF_Duty  = temp3[1].split('=')
    moji,Max_Duty = temp3[2].split('=')
    moji,Duty     = temp3[3].split('=')    
    #数値に変換
    MVn         = np.float64(MVn)
    FF_Duty     = np.float64(FF_Duty)    
    Max_Duty    = np.float64(Max_Duty) 
    Duty        = np.float64(Duty)    
    
    #センサ種類
    Heater = temp2[1]
    #print(Sensor)
    return [time,MVn,FF_Duty,Max_Duty,Duty,Heater]