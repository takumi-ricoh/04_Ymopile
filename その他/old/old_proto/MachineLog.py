# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 12:52:27 2017

@author: p000495138

***** 概要 *****

・シリアル通信をして1行読み出す
・中身を判定して、リストにappendする

*****************

"""

import Sensor.SerialCom as serial
import numpy as np

#%%　f22        
def Func_f22(data):
    #分ける
    temp1 = data
    temp2 = temp1.split('|')
    temp3 = temp2[-1].split(',')
    #時刻を計算
    time_str = temp2[2].split(':')
    time = float(time_str[0])*60 + float(time_str[1]) #秒単位換算
    #数値に変換
    TargetTemp = np.float64(temp3[1])
    CurentTemp = np.float64(temp3[3])
    #センサ種類
    Sensor = temp2[1]
    #print(Sensor)
    return [time,TargetTemp,CurentTemp,Sensor]

#%%　f26    
def Func_f26(data):
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

#%% データの中身を判定してリスト保存
class MachineLog():

    def __init__(self):
        self.f22 = {"Sen1":[],"Sen3":[],}
        self.f26 = {"Heater1":[],"Heater2":[],}
        self.temp=[]

    def set_ch(self,port):
        self.machine = serial.SerialCom(port)

    def update(self):
        try:
            data = self.machine.read() #リスト
            print(data)
            self.temp.append(data)
            if data[1:4] == "f22":
                [time,Tar,Cur,Sen] = Func_f22(data)
                if   Sen == '[Sensor1]':
                        self.f22["Sen1"].append([time,Tar,Cur,Sen])
                elif Sen == '[Sensor3]':
                        self.f22["Sen3"].append([time,Tar,Cur,Sen])
            elif data[1:4] == "f26":  
                [time,MVn,FF_Duty,Max_Duty,Duty,Heater] = Func_f26(data)
                if   Heater == '[Heat1]':
                        self.f26["Heater1"].append([time,MVn,FF_Duty,Max_Duty,Duty,Heater])
                elif Heater == '[Heat2]':
                        self.f26["Heater2"].append([time,MVn,FF_Duty,Max_Duty,Duty,Heater])
        except:
            pass
