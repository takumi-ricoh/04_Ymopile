# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 22:45:23 2018

@author: takumi
"""

import yaml
import os

#%%読み出し関数
def _read_yaml(filename):
    with open(filename,'r',encoding='utf-8') as f:
        data = yaml.load(f)
        
    return data

#%%読み出し関数
def read_config():
    #現在のディレクトリ取得
    cur = os.getcwd()
    ##移動先
    newcur = cur + "//pkg_config"
    ##移動
    os.chdir(newcur)
    
    
    gui_conf = _read_yaml('config_gui.yaml')
    #プロット
    plot_conf = _read_yaml('config_plot.yaml')
    #温度センサ
    sen_conf = _read_yaml('config_sensor.yaml')
    #マシンログ
    log_conf = _read_yaml('config_log.yaml')
    #戻す
    os.chdir(cur)

    return gui_conf, plot_conf, sen_conf, log_conf


#%%読み出す


