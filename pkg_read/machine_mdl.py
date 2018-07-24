# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 12:52:27 2017

@author: p000495138

***** 概要 *****

・シリアル通信をして1行読み出す
・中身を判定して、リストにappendする

*****************

"""
from . import base_mdl
from . import functions as f
import time
import pandas as pd
import threading
import itertools
import copy

#%% データの中身を判定してリスト保存
class MachineLog(base_mdl.SerialThread):
    
    def __init__(self, t0, cfg):
        self.port       = cfg["COM"]["PORT"]
        self.baudrate   = cfg["COM"]["BAUDRATE"]
        self.samplerate = cfg["COM"]["SAMPLERATE"]
        self.t0         = t0
        
        self.ser        = base_mdl.SerialCom(self.port, self.baudrate)     
        
        super().__init__(self.ser)
        
        #初期化(データフレーム)
        f22_init = pd.DataFrame([],columns=["sec","time","Tar","Cur","Sen"])
        f26_init = pd.DataFrame([],columns=["sec","time","MVn","FF_Duty","Max_Duty","Duty","Heater"])
        
        self.f22 = {"Sen1":f22_init, "Sen3":copy.copy(f22_init)}
        self.f26 = {"Heater1":f26_init, "Heater2":copy.copy(f26_init)}


        #生データ
        self.raw_data = []

    def get_value(self):        
        return {"f22":self.f22,"f26":self.f26}
    
    #オーバーライド
    def _worker(self):
        #self.datasen = self.ser.serial_read("shift-jis"
        #self.data = []

        #インデックス用のカウンタ
        it = itertools.count()
        
        while not self.stop_event.is_set():

            #読み出し失敗の場合
            try:
                #self.data = "@f22@|[Sensor1]|061:59.550 |Tar=,150,Cur=,120,Sen=,100,Air=,000,"
                
                self.data = self.ser.serial_read("utf-8")
                
                self.raw_data.append(self.data)
                
                #時刻
                time_now    = [time.time() - self.t0]
                #カウンタ
                self.count       = next(it)
                            
                #f22
                if   "f22" in self.data:
                    [sec,Tar,Cur,Sen] = f.f22(self.data)
                    f22_tmp = time_now + [sec,Tar,Cur,Sen]
                    #print(f22_tmp)
                    
                    if Sen == '[Sensor1]':
                        self.f22["Sen1"].loc[self.count] = f22_tmp
                    elif Sen == '[Sensor3]':
                        self.f22["Sen3"].loc[self.count] = f22_tmp
                
                #f26
                elif "f26" in self.data:
                    [sec,MVn,FF_Duty,Max_Duty,Duty,Heater] = f.f26(self.data)
                    f26_tmp = time_now + [sec,MVn,FF_Duty,Max_Duty,Duty,Heater]
        
                    if   Heater == '[Heat1]':
                            self.f26["Heater1"].loc[self.count] = f26_tmp
                    elif Heater == '[Heat2]':
                            self.f26["Heater2"].loc[self.count] = f26_tmp
            except:
                pass
    
            time.sleep(.01)