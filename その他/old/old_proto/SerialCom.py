# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 10:43:05 2017

@author: p000495138
"""


"""
#input
 comチャンネル

#output
 毎時取得した文字列
"""
from serial import Serial

class SerialCom():
    
    def __init__(self,port):
        self._set_com(port)
        
    def _set_com(self,port):  
        self.com = Serial(
        port=port,
        baudrate=57600,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1,
        xonxoff=0,
        rtscts=0,
        writeTimeout=None,
        dsrdtr=None)    
    
    def read(self):
        #データ取得
        data = self.com.readline()
        data = data.strip().decode("shift-jis") #先頭/末を消す
        return data