# -*- coding: utf-8 -*-
from . import graph
#import graph
import numpy as np
from tkinter import Tk,filedialog 
#from tabulate import tabulate
from plyfile import PlyData, PlyElement

class GraphFormatString:
    
    def __init__(self, g : graph.Graph, et:list):
        #vertices (id, position, et)
        self.vertices = np.array([(np.round(g.points[i],2),round(et[i],2)) for i in range(len(g.points))],dtype=[('coordinates','f4', (2,)),('thickness', 'f4')])
        #print(self.vertices)
        #edges (id, vertices)
        #self.edges = np.array([(g.edgeIndex[i][0],g.edgeIndex[i][1]) for i in range(len(g.edgeIndex))],dtype = [('vertex 1','i4'),('vertex 2','i4')])
        self.edges = np.array([tuple(e) for e in g.edgeIndex],dtype = [('vertex1','i4'),('vertex2','i4')])
        #self.edges = np.array(g.edgeIndex)
        
    def toPly(self) -> PlyData:
        vertexEle = PlyElement.describe(self.vertices,'Vertices')
        edgeEle = PlyElement.describe(self.edges, 'Edges')
        return PlyData([vertexEle,edgeEle],text=True)
'''    
    def toLines(self) -> str :
        lines = list()

        lines.append("<---------- vertices ---------->\n")
        lines.append(tabulate(self.vertices,headers = ["Id","Position","Thickness"]))
        lines.append("\n")
        
        lines.append("<---------- edges ---------->\n")
        lines.append(tabulate(self.edges,headers = ["Id","Vertices"]))
        lines.append("\n")
        string = ""
        string = string.join(lines)
        
        return string
'''    
    

class GraphPrinter:
    
    def __init__(self):
        self.graph = None
        self.et = None
    
    def set_graph(self, g : graph.Graph):
        self.graph = g
    
    def set_et(self, e):
        self.et = e
        
    
    def write(self):
        fs = GraphFormatString(self.graph, self.et)
        #lines = fs.toLines()
        
        ply = fs.toPly()
        root = Tk()
        root.withdraw()
        root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = [("PLY","*.ply")])
        try:
            f = open(root.filename,"wb")
            #f.write(lines)
            ply.write(f)
            f.close()
            return True
        except:
            return False
        
        
'''
points = [[0.010101,1.1010011],[1.121212,2.123232],[2.00101,3.11010],[3.00000,4.00300]]
edges = [[0,1],[0,2],[0,3],[1,3],[2,3],[1,2]]
flags = [0,1,1,0]


gr = graph.Graph(points, edges)
printer = GraphPrinter()
printer.set_graph(gr)
printer.set_et(flags)
printer.write()
'''

'''
root = Tk()
root.withdraw()
root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = [("graph","*.grp")])
print (root.filename)
'''

