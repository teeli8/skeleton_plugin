# -*- coding: utf-8 -*-
from . import graph
#import graph
from tkinter import Tk,filedialog 
from tabulate import tabulate

class GraphFormatString:
    
    def __init__(self, g : graph.Graph, et:list):
        #vertices (id, position, et)
        self.vertices = [[i,g.points[i],et[i]] for i in range(len(g.points))]
        #edges (id, vertices)
        self.edges = [[i,g.edgeIndex[i]] for i in range(len(g.edgeIndex))]
    
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

class GraphPrinter:
    
    def __init__(self):
        self.graph = None
        self.et = None
    
    def set_graph(self, g : graph.Graph):
        self.graph = g
    
    def set_et(self, e : list):
        self.et = e
        
    
    def write(self):
        fs = GraphFormatString(self.graph, self.et)
        lines = fs.toLines()
        root = Tk()
        root.withdraw()
        root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = [("text","*.txt")])
        f = open(root.filename,"w")
        f.write(lines)
        f.close()
        
'''
points = [[0,1],[1,2],[2,3],[3,4]]
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

