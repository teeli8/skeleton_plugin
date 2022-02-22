# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 15:46:23 2022

@author: Yigan
"""

import napari
from . import graph
from . import drawing

boundary = "boundary"
voronoi = "voronoi"
internalVoronoi = "internal voronoi"
heatmap = "heatmap"



class DisplayConfig:
    
    def __init__(self):
        self.show_edgepoints = False
        self.show_voronoi = False
        self.show_internal_voronoi = False
        self.show_heatmap = False
        self.show_final = True


class Display:
    
    current_display = None
    
    def current(): 
        if Display.current_display is None:
            Display.current_display = Display(napari.current_viewer())
        return Display.current_display
    
    def __init__(self, viewer : napari.Viewer):
        self.viewer = viewer
        self.layers = list()
        self.config = DisplayConfig()
    
    def set_config(self, con : DisplayConfig):
        self.config = con

    def draw_layer(self, g : graph.Graph, config : drawing.PointEdgeConfig, name : str) :
        graph_layer = GraphLayer.create(g = g, config = config, name = name)
        self.layers.append(graph_layer)
    
    def show_layer(self, isShow : bool, layer : str):
        for l in self.layers:
            if l.name == layer:
                l.show(isShow)
    
    def reset(self):
        self.show_layer(isShow = self.config.show_edgepoints, layer = boundary)
        self.show_layer(isShow = self.config.show_voronoi, layer = voronoi)
        self.show_layer(isShow = self.config.show_internal_voronoi, layer = internalVoronoi)
        self.show_layer(isShow = self.config.show_heatmap, layer = heatmap)

    def removeall(self):
        # todo : remove all layers
        self.layers.clear()
    

class GraphLayer:
    
    def __init__(self, name : str, pl : napari.layers.Points, el : napari.layers.Shapes):
        self.name = name
        self.pointLayer = pl
        self.edgeLayer = el
    
    def show(self, isShow : bool):
        self.pointLayer.visible = isShow
        self.edgeLayer.visible = isShow
        pass
    
    def create(g : graph.Graph, config : drawing.PointEdgeConfig, name : str):
        viewer = Display.current().viewer
        
        pc = config.pointConfig
        pname = name + " : " + "points"
        pointLayer = viewer.add_points(g.points, name = pname, size = pc.size, opacity = pc.opacity, face_color = pc.face_color, edge_color = pc.edge_color)
    
        ec = config.edgeConfig
        ename = name + " : " + "edges"
        
        shapeLayer = napari.layers.Shapes(name = ename)
        shapeLayer.add_lines(g.get_edge_cord(), edge_width = ec.size, face_color = ec.face_color, edge_color = ec.edge_color)
        viewer.add_layer(shapeLayer)
        
        return GraphLayer(name = name, pl = pointLayer, el = shapeLayer)


