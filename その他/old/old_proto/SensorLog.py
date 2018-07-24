# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 14:10:30 2017

@author: p000495138

***** 概要 *****

・シリアル通信をして1行読み出す
・中身を判定して、リストにappendする

*****************

"""


import Sensor.SerialCom as serial
import numpy as np

#%% 値変換クラス
def Func_Arduino(data):
    millis = np.float64(data[0])
    vobj   = np.float64(data[1])
    tobj   = np.float64(data[2]) 
    tamb   = np.float64(data[3])
    return [millis,vobj,tobj,tamb]

#%% センサ値のロギング
class SensorLog():

    def __init__(self):
        self.sensor = {"Sen1":[],}
        pass
        
    def set_ch(self,port):
        self.arduino = serial.SerialCom(port)   
    
    def update(self):
        self.data = self.arduino.read() #リスト
        self.data = self.data.split(" ")
        [millis,vobj,tobj,tamb] = Func_Arduino(self.data)
        self.sensor["Sen1"].append([millis,vobj,tobj,tamb])
