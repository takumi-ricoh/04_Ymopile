# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 12:24:16 2017

@author: p000495138
"""

import Ploter as gr
import numpy as np
import time
import ctypes

b=gr.Ploter()

def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B  

x=[]
for i in range(10,99999999999):
    if getkey(ESC):     # ESCキーが押されたら終了
       break
    x=np.random.randn(i)
    y=np.random.randn(i)
    b.update(x,y,0,0)
    time.sleep(0.01)
    
#x=[1,2,3,4,5,6,7,8,9,10]
#y=np.random.randn(10)
#b.update(x,y)