# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 23:08:49 2022

@author: Yigan
"""
from scipy import signal
import numpy as np

arr = np.array([[0,0,1,0,0],[0,1,1,1,0],[0,0,1,1,0],[0,0,0,1,0],[0,0,0,0,0]])
filt = np.array([[1,1],[1,1]])

c = signal.convolve2d(arr, filt, mode='same')

tf = c >= 4
edge = np.array(c)

edge[tf] = 0

indices = np.where(edge > 0)
idcomp = np.transpose(np.array([indices[0],indices[1]]))

print(arr)
print()
print(c)
print()
print(edge)
print()
print(idcomp)
print()
print(idcomp - [0.5,0.5])



