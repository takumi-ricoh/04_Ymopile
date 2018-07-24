# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 17:48:26 2018

*******   Matplotlibを使うパターン   ********

@author: p000495138
"""
import ctypes
import time
import itertools
from pkg_read import sensor_mdl
from pkg_read import machine_mdl
from pkg_plot import plot_mdl
from pkg_config import sensor_cfg_mdl 
from pkg_config import machine_cfg_mdl
from pkg_config import plotter_cfg_mdl
from pkg_save import save_mdl

#%%キーボード待ち
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B          

#%%パラメータ
sensor_cfg     = sensor_cfg_mdl.Cfg()

machine_cfg    = machine_cfg_mdl.Cfg()

plotter_cfg    = plotter_cfg_mdl.Cfg(sensor_cfg)

#%% 基準時刻を取得する
t0 = time.time()

#%%オブジェクト生成
#サーモパイル
sensor = sensor_mdl.SensorLog(sensor_cfg,t0)
#マシンログ
machine = machine_mdl.MachineLog(machine_cfg,t0)
#プロット
plotter = plot_mdl.Plotter(plotter_cfg)

#セーブ用
#saver   = save_mdl.Saver()

#%%データ取得スタート
sensor.start()
machine.start()

#センサ数取得
sensor_number = sensor.senNum

#%%グラフの初期化

#描画条件指定
machine_key = plotter_cfg.MACHINE_KEY
sensor_key  = plotter_cfg.SENSOR_KEY
dist_key  = plotter_cfg.DIST_KEY

#グラフの初期化
plotter.sensor.init_line(sensor_key)
plotter.machine.init_line(machine_key)
plotter.dist.init_line(dist_key,plotter_cfg.SENPOS)

#%%繰り返し処理

sta = time.time()
while True:
    #データ取得
    sensor_data   = sensor.get_value()
    machine_data  = machine.get_value()

    #プロットの更新
    plotter.sensor.update(sensor_data)
    plotter.machine.update(machine_data)
    plotter.dist.update(sensor_data)
    
    print(time.time()-sta)
    sta = time.time()
    # ESCキーが押されたら終了
    if getkey(ESC):   
        break

#%%終了処理
sensor.stop()
machine.stop()
