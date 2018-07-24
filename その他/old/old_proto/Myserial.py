3# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:05:36 2016

@author: p000495138
"""
#from __future__ import unicode_literals,print_function
from serial import Serial
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
import scipy.interpolate as si

import ctypes

#前回のグラフを消す
plt.close()
x=np.arange(0,23)

#キーボード待ち
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B          # ESCキーの仮想キーコード

def calc_bspline(x,y):
    
    t = range(len(x))
    ipl_t = np.linspace(0.0, len(x) - 1, 20)
    
    x_tup = si.splrep(t, x, k=3)
    y_tup = si.splrep(t, y, k=3)
    
    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]
    
    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]
    
    x_i = np.array(si.splev(ipl_t, x_list))
    y_i = np.array(si.splev(ipl_t, y_list))
    
    return x_i,y_i

#ファイル名
savename = "test.txt"

#シリアルポート設定
com.close()
plt.close()

com = Serial(
  port="COM11",
  baudrate=57600,
  bytesize=8,
  parity='N',
  stopbits=1,
  timeout=None,
  xonxoff=0,
  rtscts=0,
  writeTimeout=None,
  dsrdtr=None)
print(com.portstr)


#初期グラフ
fig, ax = plt.subplots(2,1)
line1, = ax[0].plot(np.zeros(23),"r.-")
line2, = ax[1].plot(np.zeros(23),"g.-")
fig.show()
fig.canvas.draw()
bg0 = fig.canvas.copy_from_bbox(ax[0].bbox)
bg1 = fig.canvas.copy_from_bbox(ax[0].bbox)
ax[0].set_xlim(0,25)
ax[1].set_xlim(0,25)
ax[0].set_ylim(20,40)
ax[1].set_ylim(20,40)

#保存用
mysave=[]
tmp = []
res=[]

while True:
    time=[]
    sen=[]
    obj=[]
    amb=[]
        
    #データ取得
    data1=com.readline()
    data2=data1.strip().decode('shift-jis') #改行文字を除外し文字列変換
    
    #大きく分割
    data3 = data2.split(",")
    
    #内容で分割
    time.append(data3[0])
    for i in data3[1:-1]:
        sen.append(i.split(":")[0])
        obj.append(i.split(":")[1])
        amb.append(i.split(":")[2])    
    
    sen_np = np.array(sen,dtype=np.float32)
    obj_np = np.array(obj,dtype=np.float32)
    amb_np = np.array(amb,dtype=np.float32)    

    res.append([sen_np,obj_np,amb_np])
    
    #%%グラフ化

    #値の更新
    x=sen_np 
    line1.set_data(x,obj_np)
    line2.set_data(x,amb_np)


    #描画設定
    ax[0].set_title("Tobj")  
    ax[1].set_title("Tamb")
    ax[0].grid(True)
    ax[1].grid(True)
    ax[0].set_xlabel("sample")
    ax[1].set_xlabel("sample")
    ax[0].set_ylabel("deg")
    ax[1].set_ylabel("deg")    
    
    #おまじない
    fig.canvas.restore_region(bg0)
    fig.canvas.restore_region(bg1)
    fig.canvas.draw()
    ax[0].draw_artist(line1)
    ax[1].draw_artist(line2)
    fig.canvas.update()
    fig.canvas.flush_events()    
    fig.tight_layout()
        
    if getkey(ESC):     # ESCキーが押されたら終了
        break
    
com.close()