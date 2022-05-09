# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 23:08:49 2022

@author: Yigan
"""
from scipy import signal
import numpy as np
import graph
from matplotlib import cm

'''
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
'''
'''
arr = np.array([1.176005207095135, 1.038292228493046, 0.9272952180016123, 1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 0.7610127542247298, 2.4229664938452533, 0.6987001684571055, 1.5707963267948966, 1.3494818844471053, 1.176005207095135, 1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 1.5707963267948966, 0.7610127542247298, 0.8364486591584582, 1.3494818844471053, 1.5707963267948966])
colors = graph.get_color_list(arr)
print(colors)
'''
'''
print(np.linalg.norm(2))
'''
'''
arr = np.array([[0,1],[1,2],[2,3],[3,4]])
print(np.count_nonzero(arr == 1))
'''
'''
arr = np.array([[0,1],[1,0],[0,1],[1,0]])
white = np.ones((arr.shape[0],arr.shape[1],4))
white[arr>0] = [255,255,255,255]
white[arr<=0] = [0,0,0,0]
print(white)
'''
arr = np.array([[2,1],[1,0],[1,3],[1,0]])
unique, counts = np.unique(arr, return_counts=True)
d = dict(zip(unique, counts))
print(d)




