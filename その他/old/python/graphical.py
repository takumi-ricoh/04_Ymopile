# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 17:10:24 2017

@author: p000495138
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 16:34:03 2017

@author: p000495138
"""
from serial import Serial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ctypes
import time

#前回のグラフを消す
plt.close()

#キーボード待ち
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B          # ESCキーの仮想キーコード
plt.ion()           # 対話モードオン

#グラフ初期化
t0=time.time()
t=[]
fig,ax=plt.subplots()
line, = ax.plot(0,0,".-")

#高速描画
ax.lines.remove(line)
ax.grid(True)
ax.set_ylim(10,200)
ax.set_xlabel("time")
fig.show()
ax.set_ylabel("temperature")
fig.canvas.draw()
bg = fig.canvas.copy_from_bbox(ax.bbox)

#シリアルポート設定
#com.close()
com = Serial(
  port="COM24",
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

tobj=[]
tamb=[]
millis=[]
old_mil=-1

for i in range(999999999):
    if getkey(ESC):     # ESCキーが押されたら終了
        break    
    #データ取得
    data=com.readline()
    data=data.strip().decode("shift-jis") #先頭/末を消す
    data=data.split(" ")
    cur_mil=np.float64(data[0])
    
    #時刻a
    if cur_mil < old_mil:
        millis=[]
        tobj=[]
        tamb=[]
    old_mil=cur_mil
    millis.append(np.float64(data[0]))
    tobj.append(np.float64(data[2]))
    tamb.append(np.float64(data[3]))
    millis_array=np.array(millis)
    millis_array = millis_array - millis_array[0] 
    cur = millis_array[-1]/1000
    t=millis_array/1000
    #データ取得
    print(np.round(cur,3),"/",data[2])
    #グラフ更新(速い)
    line.set_data(t,tobj)
    fig.canvas.restore_region(bg)
    plt.legend("test")
    fig.canvas.draw()
    ax.draw_artist(line)
    num=30
    if cur<num:
        ax.set_xlim(0,num)
    else:
        ax.set_xlim(cur-num,cur)
    fig.canvas.update()
    fig.canvas.flush_events()
    
ax.plot(t,tobj,".-")
com.close()
datas=np.array([t,tobj,tamb])    
savedata=pd.DataFrame(datas.T,columns=["t","tobj","tamb"])
savedata.to_csv("save.csv")

