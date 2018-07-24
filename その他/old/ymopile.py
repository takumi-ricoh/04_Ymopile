# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 18:21:33 2018

@author: p000495138
"""

#別プロセスで
#https://stackoverflow.com/questions/36181316/python-matplotlib-plotting-in-another-process

#別プロセスでのプロットはうまくいかないのでやらない

import serial
import time
import threading
import matplotlib.pyplot as plt
import multiprocessing as mp
import numpy as np
import random

#%% シリアルクラス
class SerialThread():

    def __init__(self, param):
        
        #停止用の初期化
        self.stop_event = threading.Event() #停止させるかのフラグ
        #シリアル通信開始
        self.ser = self._serInit(param["com"],param["rate"])
        #保存用データの初期化
        self.return_value = []

        #スレッドの作成と開始
        self.thread = threading.Thread(target = self._serial_worker)
        self.thread.start()

    def stop(self):
        """スレッドを停止させる"""
        self.stop_event.set()
        self.thread.join()    #スレッドが停止するのを待つ
        self.ser.close()      #終わったら通信をきる

    def get_value(self):
        return self.return_value

    def _serial_worker(self):
        #stop_event がセットされるまでは、、」
        while not self.stop_event.is_set():
            line = self.ser.readline().decode("utf-8").strip()
            #データ保存
            self.return_value.append(line)
            time.sleep(.1)
    
    def _serInit(self,com,rate):
        #異常がある場合に自動で、シリアル通史を閉じる
        ser = serial.Serial(
            port=com,
            baudrate=rate,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            rtscts=True)
        return ser

#%% シリアルクラス
class PlotProcess():
    def __init__(self):
        #停止用の初期化
        self.stop_event = mp.Event() #停止させるかのフラグ        
        #データl更新プロセスの作成と初期化
        self.queue = mp.Queue()
        self.process = mp.Process(target = self._plot_worker, args=(self.queue,))
        self.process.start()
        
    def stop(self):
        self.stop_event.set()
        self.process.join()    #スレッドが停止するのを待つ

    def set_data(self,data):
        self.queue.put(data)

    def _init_plot(self):
        #共通データ
        fig, ax = plt.subplots(2,1)
        line1, = self.ax[0].plot(np.zeros(1),"r.-")
        line2, = self.ax[1].plot(np.zeros(1),"g.-")
        fig.show()
        fig.canvas.draw()
        bg0 = self.fig.canvas.copy_from_bbox(self.ax[0].bbox)
        bg1 = self.fig.canvas.copy_from_bbox(self.ax[1].bbox)
        fig.show()
        
        return {"fig":fig, "ax":ax, "line1":line1, "line2":line2, "bg0":bg0, "bg1":bg1}

    def _plot_worker(self,q):
        plot = self._init_plot()
        
        #stop_event がセットされるまでは、、」
        while not self.stop_event.is_set():
            obj = q.get()
            print(obj)
            
            #データ更新
#            x=np.arange(0,len(self.plot_data))
            self.line1.set_data(obj[0], obj[1])
            self.line2.set_data(obj[0], obj[1])
            #おまじない           
            plot["fig"].canvas.restore_region(plot["bg0"])
            plot["fig"].canvas.restore_region(plot["bg1"])
            plot["fig"].canvas.draw()
            plot["ax"][0].draw_artist(plot["line1"])
            plot["ax"][1].draw_artist(plot["line2"])
            plot["fig"].canvas.update()
            plot["fig"].canvas.flush_events()    
            plot["fig"].tight_layout()      
            time.sleep(.1)

#%%メイン処理
if __name__ == "__main__":

    #シリアル通信スレッド開始
    param1 = {"com":"COM13", "rate":9600}
    param2 = {"com":"COM5",  "rate":9600}

    #th1 = SerialThread(param1)
    #th2 = SerialThread(param2)
    
    #プロットプロセス実行
    pro1 = PlotProcess()
    
    #%%実行    
    start = time.time()

    count=0
    
    while True:
        #a=th1.get_value()
        #b=th2.get_value()

        count+=1               
        if count < 100: 
            pro1.set_data([random.random(), random.random()])
    
        elif time.time()-start > 5:
            #th1.stop()
            #th2.stop()
            pro1.stop()
            print("finish")
            time.sleep(.1)
            break
        time.sleep(.1)
