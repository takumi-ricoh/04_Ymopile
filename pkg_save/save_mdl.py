# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:04:01 2017

@author: p000495138

"""

import pickle

def saver(name,data): 

    with open(name, mode='wb') as f:
         print("kita1")
         pickle.dump(data, f)
