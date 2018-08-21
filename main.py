# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 17:48:26 2018

*******   Matplotlibを使うパターン   ********

@author: p000495138
"""
from PyQt5.QtWidgets import QApplication
import sys
import ctypes
import time
from pkg_read import sensor_mdl
from pkg_read import machine_mdl
from pkg_plot_qt import plot_mdl
from pkg_config import get_cfg_mdl #グローバル変数
from pkg_save import save_mdl
import gui
import pickle
import pandas as pd
#%%キーボード待ち
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B          


#%% 仲介クラス
class GUI_Adapter():
    def __init__(self, sensor, machine, plotter, pool):
        self.sensor = sensor
        self.machine = machine
        self.plotter = plotter
        self.pool = pool

    #スタート
    def start(self):
        print("start clicked")
        self.sensor.start()
        self.machine.start()
        self.plotter.start()
        print("start success")

    #ストップ
    def stop(self):
        print("stop clicked")
        #読み込みスレッド停止
        self.sensor.stop()
        self.machine.stop()
        #プロット停止
        self.plotter.stop()
        print("stop success")

    def save_sensor(self,savename):
        data = pd.concat([sensor.couple,sensor.obj,sensor.amb],axis=1)
        data.to_csv(savename)

    def save_log(self,savename):
        data = machine.raw_data
        with open(savename, mode='w') as f:
            for word in data:
                f.writelines(word+"\n")

    def fopen(self,openname):
        with open(openname, mode='rb') as f:
            self.opendata = pickle.load(f)
        pool.pool = self.opendata
        plotter.one_shot()

#%% データプールクラス
class DataPool():
    def __init__(self,sensor,machine):
        self.sensor = sensor
        self.machine = machine    
        self.pool = {}

    def get_value(self):
        self.pool["sensor"]  = sensor.get_value()
        self.pool["machine"] = machine.get_value()
        return self.pool

#%% メイン処理
if __name__ == '__main__':
    
    # GUI
    #インスタンスが無い場合のみ新たに作成
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # 基準時刻を取得する
    t0 = time.time()
    #%% パラメータ取得
    gui_conf, plot_conf, sen_conf, log_conf = get_cfg_mdl.read_config()
 
    #%% オブジェクト生成    

    #GUI
    gui = gui.GUI()

    #データソース
    sensor = sensor_mdl.SensorLog(t0, sen_conf)
    machine = machine_mdl.MachineLog(t0, log_conf)
    pool = DataPool(sensor, machine)    

    #プロッタ 
    #センサ、fuserのまぜこぜにも対応するため、poolという一つの辞書で管理する
    plotter = plot_mdl.Plotter(gui.pltcanvas, pool,  plot_conf)


    #セーブモジュール
    #saver = save_mdl.saver

    #GUIのアクションを設定
    #いろいろあるので、GUI_Adapterクラスにまとめる
    adapter = GUI_Adapter(sensor, machine, plotter, pool)
    print(type(adapter))
    gui.set_action(adapter)
    sys.exit(app.exec_())