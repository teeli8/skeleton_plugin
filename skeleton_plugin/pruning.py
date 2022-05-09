# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 13:28:18 2022

@author: Yigan
"""
import numpy as np
from .graph import Graph, dist2D, prune_graph
from queue import PriorityQueue

class Node:   
    
    def __init__(self, p, r : float, ma : float):
        self.point = p
        self.radius = r
        self.bt = ma
        self.isCore = True
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
    
    def path_count(self):
        return len(self.paths)
    

class Path:
    
    def __init__(self, one:Node, other:Node, l:float):
        self.one = one
        self.other = other
        self.length = l
        
        self.theta = 0
        self.segval = 0
        self.isCore = True
        


class NodePathGraph:  
    
    def __init__(self, points, edges, radi, ma):
        self.max = ma
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
    
    def get_rad(self) -> list:
        return [n.radius for n in self.nodes]
    
    def get_ets(self) -> list:
        return [n.et() for n in self.nodes]

    def get_bts(self) -> list:
        return [n.bt for n in self.nodes]
    
    def get_segval(self) -> list:
        return [p.segval for p in self.paths]
    
    def reset_paths(self):
        for path in self.paths:
            path.one.add_path(path)
            path.other.add_path(path)
    
    def set_angles(self, angles:list):
        for pi in range(len(self.paths)):
            self.paths[pi].theta = angles[pi];
    

class PItem:
    
    def __init__(self, p : float, i):
        self.pri = p
        self.item = i
    
    def __lt__(self, other):
        return self.pri < other.pri
    

class BurningAlgo:
    
    def __init__(self, g : Graph, radi : list, ma : float):
        self.graph = g
        self.npGraph = NodePathGraph(g.points, g.edgeIndex, radi, ma)
    
    def burn(self):
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
            path.isCore = False
            nextN = targetN.get_next(path)
            nextN.remove_path(path)
            if nextN.is_iso():
                nextN.bt = targetN.bt + path.length
                pq.put(PItem(nextN.bt, nextN))
        
        self.npGraph.reset_paths()
        

class PruningAlgo:
    
    def __init__(self, g : Graph, npg : NodePathGraph):
        self.graph = g
        self.npGraph = npg
    
    def prune(self, thresh:float)->Graph:
        #virtual
        pass
    
    

class ETPruningAlgo(PruningAlgo):
    
    def __init__(self, g : Graph, npg : NodePathGraph):
        super().__init__(g, npg)
        self.pruned_et = None
        self.pruned_flag = None
        '''
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
                nextN.isCore = False
                pq.put(PItem(nextN.bt, nextN))
        
        self.npGraph.reset_paths()
    '''
    
    def prune(self, thresh : float) -> Graph:
        #todo
        removed = set()
        d_ones = self.npGraph.get_degree_ones()
        pq = PriorityQueue()
        for n in d_ones:
            pq.put(PItem(n.et(),n))
        
        while not pq.empty():
            targetN = pq.get().item
            if targetN.et() >= thresh:
                break;
            if not targetN.is_iso():
                continue;
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
        ets = np.array(self.npGraph.get_ets())
        self.pruned_flag = np.array(flags)
        self.pruned_et = ets[self.pruned_flag>0]
        return prune_graph(self.graph, flags)


class AnglePruningAlgo(PruningAlgo):
    
    def __init__(self, g : Graph, npg : NodePathGraph):
        super().__init__(g, npg)
        
    def prune(self, thresh:float)->Graph:
        #todo
        self.__angle_thresh(thresh)
        pass
    
    def __angle_thresh(self, thresh:float):
        pos = set()
        neg = set()
        core = set()
        for p in self.npGraph.paths:
            if p.isCore:
                p.segval = 10
                core.add(p)
            else:
                p.segval = p.theta - thresh
                if p.segval >= 0:
                    pos.add(p)
                else:
                    p.segval = 0
                    neg.add(p)
        return (pos,neg,core)
        
  
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
