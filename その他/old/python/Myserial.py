# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:05:36 2016

@author: p000495138
"""
from __future__ import unicode_literals,print_function
from serial import Serial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import ctypes

#前回のグラフを消す
plt.close()

#キーボード待ち
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B          # ESCキーの仮想キーコード
plt.ion()           # 対話モードオン

#ファイル名
savename = "test.txt"

#シリアルポート設定
com.close()
plt.close()

com = Serial(
  port=29,
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

#データ処理関数定義
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

###f22初期値生成
t_f22sen1 = np.array([0])
t_f22sen3 = np.array([0])
y1 = t_f22sen1*0
y2 = t_f22sen1*0
y3 = t_f22sen3*0

t_f22sen1=t_f22sen1.reshape(t_f22sen1.size,1)
t_f22sen3=t_f22sen3.reshape(t_f22sen3.size,1)
y1=y1.reshape(t_f22sen1.size,1)
y2=y2.reshape(t_f22sen1.size,1)
y3=y2.reshape(t_f22sen3.size,1)

###f26初期値生成
t_f26 = np.array([0])
y261 = t_f26*0
y262 = t_f26*0
y263 = t_f26*0

t_f26=t_f26.reshape(t_f26.size,1)
y261=y261.reshape(t_f26.size,1)
y262=y262.reshape(t_f26.size,1)
y263=y263.reshape(t_f26.size,1)


#プロット
dt = 0.5

#figureインスタンス生成
#fig = plt.figure()

#Axesインスタンス生成
fig = plt.figure(2)

ax1 = fig.add_subplot(211)
ax1.hold(True)
lines2, = ax1.plot(t_f22sen1,y2,'r-*')
lines1, = ax1.plot(t_f22sen1,y1,'b-*')
lines3, = ax1.plot(t_f22sen1,y3,'g-*')
plt.xlabel('sec')
plt.ylabel('deg')
plt.legend(['Tar','Sen1','Sen3'],bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.subplots_adjust(right=0.7)
plt.grid()

ax2 = fig.add_subplot(212)
ax2.hold(True)
lines261, = ax2.plot(t_f26,y261,'b-*')
lines262, = ax2.plot(t_f26,y262,'r-*')
lines263, = ax2.plot(t_f26,y263,'g-*')
plt.xlabel('sec')
plt.ylabel('%')
plt.legend(['Duty','FF_Duty','none'],bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.subplots_adjust(right=0.7)
plt.grid()

#保存用
mysave1=[]
mysave2=[]

for i in range(999999999):
    #データ取得
    line1=com.readline()
    line2=line1.strip().decode('shift-jis') #改行文字を除外し文字列変換
    print(line2)        
    mysave1.append(line1) #加える
    mysave2.append(line2) #加える

    
    ###f22の処理
    if line2[1:4] == 'f22':
        [time,Tar,Cur,Sen] = Func_f22(line2)
        
        #初回の時刻を取得
        if i==0:
            time0 = time
        else:
            pass
            
        ###プロット
        #Sensor1プロット
        if Sen=='[Sensor1]':
            t_f22sen1 = np.append(t_f22sen1,time-time0) 
            y1 = np.append(y1,Cur)
            y2 = np.append(y2,Tar)            
            #t = t0[1:]
            #y = y0[1:]
            lines1.set_data(t_f22sen1,y1)
            lines2.set_data(t_f22sen1,y2)
            if t_f22sen1.max()>50:
                ax1.set_xlim((t_f22sen1.max()-50,t_f22sen1.max()))                    
            else:
                ax1.set_xlim((t_f22sen1.min(),t_f22sen1.max()))                    
            ax1.set_ylim(0,180)     
            plt.pause(0.01)
        #Sensor3プロット
        elif Sen=='[Sensor3]':
            t_f22sen3 = np.append(t_f22sen3,time-time0) 
            y3 = np.append(y3,Cur)
            #t = t0[1:]
            #y = y0[1:]
            lines1.set_data(t_f22sen1,y1)
            lines2.set_data(t_f22sen1,y2)
            lines3.set_data(t_f22sen3,y3)
            if t_f22sen3.max()>50:
                ax1.set_xlim((t_f22sen3.max()-50,t_f22sen3.max()))                    
            else:
                ax1.set_xlim((t_f22sen3.min(),t_f22sen3.max()))                                        
            ax1.set_ylim(0,180)     
            plt.pause(0.01)
            
        else:
            pass
            
    ###f26の処理
    elif line2[1:4] == 'f26':
        [time,MVn,FF_Duty,Max_Duty,Duty,Heater] = Func_f26(line2)

        ###プロット
        #Sensor1プロット
        if Heater=='[Heat1]':
            t_f26 = np.append(t_f26,time-time0) 
            
            y261 = np.append(y261,Duty)
            y262 = np.append(y262,FF_Duty)            
            
            lines261.set_data(t_f26,y261)
            lines262.set_data(t_f26,y262)

            if t_f26.max()>50:
                ax2.set_xlim((t_f26.max()-50,t_f26.max()))                    
            else:
                ax2.set_xlim((t_f26.min(),t_f26.max()))                    
                
            ax2.set_ylim(0,100)     
            plt.pause(0.01)

        else:
            pass
    else: 
        pass
    
    if getkey(ESC):     # ESCキーが押されたら終了
        s=pd.Series(mysave2)
        s.to_csv(savename,index=False)    
        break

com.close()