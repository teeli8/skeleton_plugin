# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 13:28:18 2022

@author: Yigan
"""

from .graph import Graph, dist2D, prune_graph
from queue import PriorityQueue

class Node:   
    
    def __init__(self, p, r : float, ma : float):
        self.point = p
        self.radius = r
        self.bt = ma
        self.paths = set()
    
    def et(self):
        return self.bt - self.radius
    
    def get_one_path(self):
        for p in self.paths:
            return p
        return None
    
    def add_path(self, path):
        if path not in self.paths:
            self.paths.add(path)        
    
    def remove_path(self, path):
        self.paths.remove(path)
    
        
    def is_iso(self):
        return len(self.paths) == 1

    def get_next(self, path):
        return path.other if path.one == self else path.one
    

class Path:
    
    def __init__(self, one:Node, other:Node, l:float):
        self.one = one
        self.other = other
        self.length = l


class NodePathGraph:  
    
    def __init__(self, points, edges, radi, ma):
        self.nodes = list()
        self.paths = list()
        for pi in range(len(points)):
            self.nodes.append(Node(p = points[pi], r = radi[pi], ma=ma))
        
        for e in edges:
            pid1 = e[0]
            pid2 = e[1]
            l = dist2D(points[pid1],points[pid2])
            node1 = self.nodes[pid1]
            node2 = self.nodes[pid2]
            path = Path(node1, node2, l)
            node1.add_path(path)
            node2.add_path(path)
            self.paths.append(path)
    
    def get_degree_ones(self) -> list():
        ans = list()
        for node in self.nodes:
            if node.is_iso():
                ans.append(node)
        return ans
    
    def get_ets(self) -> list():
        return [n.et() for n in self.nodes]

    def get_bts(self) -> list():
        return [n.bt for n in self.nodes]
    
    def reset_paths(self):
        for path in self.paths:
            path.one.add_path(path)
            path.other.add_path(path)

class PItem:
    
    def __init__(self, p : float, i):
        self.pri = p
        self.item = i
    
    def __lt__(self, other):
        return self.pri < other.pri

class ETPruningAlgo:
    
    def __init__(self, g : Graph, radi : list(), ma : float):
        self.graph = g
        self.npGraph = NodePathGraph(g.points, g.edgeIndex, radi, ma)
        
    def burn(self):
        #todo
        d_ones = self.npGraph.get_degree_ones()
        pq = PriorityQueue()
        for n in d_ones:
            n.bt = n.radius
            pq.put(PItem(n.bt,n))
        
        while not pq.empty():
            targetN = pq.get().item
            path = targetN.get_one_path()
            if path is None:
                continue
            nextN = targetN.get_next(path)
            nextN.remove_path(path)
            if nextN.is_iso():
                nextN.bt = targetN.bt + path.length
                pq.put(PItem(nextN.bt, nextN))
        
        self.npGraph.reset_paths()
    
    def prune(self, thresh : float) -> Graph:
        #todo
        removed = set()
        d_ones = self.npGraph.get_degree_ones()
        pq = PriorityQueue()
        for n in d_ones:
            pq.put(PItem(n.et(),n))
        
        while not pq.empty():
            targetN = pq.get().item
            if targetN.et() > thresh:
                break;
            removed.add(targetN)
            path = targetN.get_one_path()
            if path is None:
                continue;
            nextN = targetN.get_next(path)
            nextN.remove_path(path)
            if nextN.is_iso():
                pq.put(PItem(nextN.et(), nextN))
        
        self.npGraph.reset_paths()
        
        flags = [0 if node in removed else 1 for node in self.npGraph.nodes]
        return prune_graph(self.graph, flags)
  
'''
points = [[0,1],[1,2],[2,3],[3,4]]
edges = [[0,1],[1,2],[2,3]]
#flags = [0,1,1,0]
radi = [1,2,2,1]

g = Graph(points, edges, None)
algo = ETPruningAlgo(g, radi)
algo.burn()
print(algo.npGraph.get_bts())
'''
