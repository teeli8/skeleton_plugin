# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 15:36:07 2022

@author: Yigan
"""
import math
import numpy as np
from scipy.spatial import Voronoi
from matplotlib import cm
from matplotlib import colors as cl

def get_color_value(color):
    return np.average(color[0:2])

def dist2D(p1,p2):
    return math.sqrt(math.pow(p1[0]-p2[0],2) + math.pow(p1[1]-p2[1],2))



class BinaryImage:
    
    """
    rawData : in the form of a matrix of [r,g,b,a] value
    """
    def __init__(self, rawData : np.ndarray, thresh : int):
        
        numRow,numCol,colorSize = rawData.shape;
        
        self.data = np.zeros((numRow,numCol))
        flags = rawData[:,:,0] > thresh
        self.data[flags] = 1
        '''
        for r in range(numRow):
            for c in range(numCol):
                color_value = get_color_value(rawData[r,c])
                self.data[r,c] = 0 if color_value < thresh else 1
        '''
    
    def position_is_bright(self, x : float, y : float) -> bool:
        xint = int(x)
        yint = int(y)
        numRow,numCol = self.data.shape;
        return xint >= 0 and yint >= 0 and xint < numRow and y < numCol and self.data[xint,yint] == 1



           

class Graph:
    
    def __init__(self, point_list : list, edge : list, point_ids : list = None):
        self.points = point_list
        self.edgeIndex = edge
        self.point_ids = self.__build_point_ids(point_ids)
    
    def get_edge_cord(self) -> np.ndarray:
        edges = list()
        for e in self.edgeIndex:
            x = e[0]
            y = e[1]
            if x >= 0 and y >= 0:
                edges.append([self.points[x],self.points[y]])
        return np.array(edges)

    def __build_point_ids(self, ids : list):
        if ids is None or len(ids) != len(self.points):
            return list(range(0,len(self.points)))
        else:
            return ids


class VoronoiDiagram:
    
    def __init__(self, point_list : list):
        self.vor = Voronoi(point_list)
        self.vert_to_regions = self.__build_vert_to_region()
        self.region_to_site = self.__build_region_to_site()
        self.graph = Graph(self.vor.vertices, self.vor.ridge_vertices)
        
    
    def closest_site(self, vertex_id : int) -> (int, float):
        if vertex_id < 0 or vertex_id >= len(self.vor.vertices):
            return ([],-1)
        
        vertex = self.vor.vertices[vertex_id]       
        regions = self.vert_to_regions[vertex_id]
        
        dist = float("inf")
        cursite = 0
        for r in regions:
            siteid = self.region_to_site[r]
            site = self.vor.points[siteid]
            curdist = dist2D(site, vertex)
            if curdist < dist:
                dist = curdist
                cursite = siteid
        
        return (cursite,dist) 
    
    
    def __build_vert_to_region(self):
        
        dic = dict()
        for rid in range(len(self.vor.regions)):
            region = self.vor.regions[rid]
            for vid in region:
                if vid >= 0:
                    if vid not in dic:
                        dic[vid] = list()
                    dic[vid].append(rid)
        return dic
    
    def __build_region_to_site(self):
        
        dic = dict()
        for pid in range(len(self.vor.point_region)):
            rid = self.vor.point_region[pid]
            if rid >= 0:
                dic[rid] = pid
        return dic
   


    

def get_edge_vertices(img : BinaryImage) -> list:
    s = set()
    numRow, numCol = img.data.shape
    for r in range(numRow):
        for c in range(numCol):
            if(img.data[r,c] == 1):
                neighbors = [(r-1,c),(r+1,c), (r,c+1), (r,c-1)]
                for nr,nc in neighbors:
                    if(nr < 0 or nr >= numRow or nc < 0 or nc >= numCol or img.data[nr,nc] == 0):
                         if(r == nr):
                            vc = float(abs(c+nc))/2
                            s.add((r-0.5,vc))
                            s.add((r+0.5,vc))
                         else:
                            vr = float(abs(r+nr))/2
                            s.add((vr,c-0.5))
                            s.add((vr,c+0.5)) 
                
    return list(s)      

def get_voronoi(points : list) -> VoronoiDiagram:
    return VoronoiDiagram(points)


def prune_graph(graph : Graph, flags : list) -> Graph:
    new_points = list()
    new_ids = list()
    prune_index = [-1] * len(graph.points)
    numPruned = 0
    for i in range(len(flags)):
        if flags[i] == 1 :
            prune_index[i] = numPruned
            new_points.append(graph.points[i])
            new_ids.append(i)
        else:
            numPruned += 1
    
    new_edges = list()
    for e in graph.edgeIndex:
        ex = e[0]
        ey = e[1]
        if ex >= 0 and ey >= 0:            
            if prune_index[ex] >= 0 and prune_index[ey] >= 0: 
                ex -= prune_index[ex]
                ey -= prune_index[ey]
                new_edges.append([ex,ey])
                
    return Graph(new_points, new_edges, new_ids)

'''
pruned graph
'''
def graph_in_image(vor : Graph, img : BinaryImage) -> Graph:
    flags = [0]*len(vor.points)
    for i in range(len(vor.points)):
        p = vor.points[i]
        if img.position_is_bright(p[0],p[1]):
            flags[i] = 1
    return prune_graph(vor, flags)





"""Closest Site Graph"""
def closest_site_graph(vor : VoronoiDiagram) -> Graph:
    
    points = list()
    edges = list()
    
    index = 0
    for vid in range(len(vor.vor.vertices)):
        siteid,dist = vor.closest_site(vid)
        points.append(vor.vor.vertices[vid])
        points.append(vor.vor.points[siteid])
        edges.append([index,index+1])
        index += 2
    return Graph(points,edges)

def get_closest_dists(pids : list(), vor : VoronoiDiagram) -> list():
    result = list()
    for pid in pids:
        site, dist = vor.closest_site(pid)
        result.append(dist)
    return result


def get_color_list(dist : list()) -> list:
    colors = list()    
    data = np.array(dist)
    norm = (data - np.min(data)) / (np.max(data) - np.min(data))
    clist = cm.rainbow(norm)
    for c in clist:
        colors.append(cl.to_hex(c))
    return colors

def get_edge_color_list(colors : list(), edges:list()) -> list:
    col = list()
    for e in edges:
        x = e[0]
        y = e[1]
        col1 = cl.to_rgb(colors[x])
        col2 = cl.to_rgb(colors[y])
        col.append(cl.to_hex((np.array(col1)+np.array(col2))/2))
    return col  

'''
colors = ["#FFFFFF","#FFFF00","#FF0000", "#000000"] 
edges = [[0,1],[0,2],[0,3],[1,2]]
print(get_edge_color_list(colors, edges))
'''
"""Binary Image Test"""
'''
rawData = np.array([
        [[0,0,0,1],[255,255,255,1],[0,0,0,1]],
    [[0,0,0,1],[255,255,255,1],[255,255,255,1]],
    [[0,0,0,1],[0,0,0,1],[0,0,0,1]]])

image = BinaryImage(rawData, 200)


vertices = get_edge_vertices(image)

vor = VoronoiDiagram(vertices)
print(vor.vor.points)
'''
'''
print(vor.region_to_site)

print(vor.vert_to_regions)
print(vor.closest_site(0))
'''
'''
vor = get_voronoi(vertices)


points = [[0,1],[1,2],[2,3],[3,4]]
edges = [[0,1],[0,2],[0,3],[1,3],[2,3],[1,2]]
flags = [0,1,1,0]

graph = Graph(points, edges)

new_graph = graph_in_image(vor, image)
print(new_graph.points)
print(new_graph.edgeIndex)
'''
'''
dist = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7]
rainbow = cm.rainbow(dist)
print(rainbow)
'''
#print(cl.to_hex(rainbow))
