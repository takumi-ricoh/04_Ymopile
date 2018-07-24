# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 14:10:30 2017

@author: p000495138

***** 概要 *****

・シリアル通信をして1行読み出す
・中身を判定して、リストにappendする

*****************

"""
import random

from . import base_mdl
import pandas as pd
import numpy as np
import threading
import time
import itertools

#%% センサ値のロギング
class SensorLog(base_mdl.SerialThread):

    def __init__(self,t0,cfg):
        #センサパラメータセット
        self.port       = cfg["COM"]["PORT"]
        self.baudrate   = cfg["COM"]["BAUDRATE"]
        self.samplerate = cfg["COM"]["SAMPLERATE"]
        self.senNum     = cfg["SENSOR"]["NUM"]        #センサ数
        self.senPos     = cfg["SENSOR"]["POS"]
        self.t0         = t0

        self.ser        = base_mdl.SerialCom(self.port, self.baudrate) 
        
        super().__init__(self.ser)

        #データ格納用の空データフレームを準備
        self.couple = pd.DataFrame([],columns=["sec","couple1","couple2"])
        self.num    = pd.DataFrame([],columns=["sec"]+["num"+str(i) for i in range(self.senNum)])
        self.obj    = pd.DataFrame([],columns=["sec"]+["obj"+str(i) for i in range(self.senNum)])
        self.amb    = pd.DataFrame([],columns=["sec"]+["amb"+str(i) for i in range(self.senNum)])


    def get_value(self):
        return {"couple":{"obj":self.couple}, "thermopile":{"num":self.num, "obj":self.obj, "amb":self.amb}}
        
    #オーバーライド
    def _worker(self):
        print("sensorworker start")
        
        #インデックス用のカウンタ
        it = itertools.count()
        
        while not self.stop_event.is_set():
            #データ読み
            self.data = self.ser.serial_read("cp932").split(",")
            
            #print(self.data)
            #カウンタ
            self.count  = next(it)

            if len(self.data)>1: #データが少なくとも取得されたあとから～
                
                #正常データかどうかの判定
                num_check    = [float(i.split(":")[0]) for i in self.data[3:-1]]
                
                if num_check == [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:

                    #ある時刻でのデータ列取得(リスト)
                    time_now    = [time.time() - self.t0]
                    couples_now = time_now + [float(self.data[1]), float(self.data[2])] 
                    nums_now    = time_now + [float(i.split(":")[0]) for i in self.data[3:-1]]
                    objs_now    = time_now + [float(i.split(":")[1]) for i in self.data[3:-1]]
                    ambs_now    = time_now + [float(i.split(":")[2]) for i in self.data[3:-1]]
            
                    #データフレームに追加
                    self.couple.loc[self.count] = couples_now
                    self.num.loc[self.count]    = nums_now
                    self.obj.loc[self.count]    = objs_now
                    self.amb.loc[self.count]    = ambs_now
                    
                    #センサ数取得
                    self.sensor_number = len(objs_now)

            #ワーカー
            time.sleep(.05)