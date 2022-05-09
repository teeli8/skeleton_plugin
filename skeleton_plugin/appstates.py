# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:35:25 2022

@author: Yigan
"""
from . import graph
from . import statemachine as st
from . import mainalgo as ma
from . import display as ds
from .pruning import BurningAlgo,ETPruningAlgo,AnglePruningAlgo
import numpy as np

debug = False

def algo_st():
    return ma.SkeletonApp.inst().algoStatus

def app_st():
    return ma.SkeletonApp.inst().appStatus

def tRec():
    return ma.SkeletonApp.inst().timer

def get_size() -> float:
    refer = 256
    x, y, c = app_st().shape
    m = float(max([x,y,c]))
    return m / refer


class ReadState(st.State):
    
    def execute(self):
        algo_st().raw_data = self.__read_data()
        if len(algo_st().raw_data) == 0:
            #ds.Display.current().toast("Read Fail")
            return
        app_st().shape = algo_st().raw_data.shape
        tRec().stamp("Read Data")
        
    
    def get_next(self):
        if len(algo_st().raw_data) == 0:
            return None
        return ThreshState()

    def __read_data(self):
        viewer = ds.Display.current().viewer
        sl = viewer.layers.selection
        if len(sl) != 1:
            ds.Display.current().toast("Please select one image layer")
            return []
        layer = sl.pop()
        return layer.data_raw

class ThreshState(st.State):
    
    def execute(self):
        if algo_st().raw_data is None:
            return
        algo_st().biimg = graph.BinaryImage(algo_st().raw_data, int(app_st().biThresh/100.0*255))
        tRec().stamp("Threshold")
        ds.Display.current().draw_image_layer(algo_st().biimg.get_drawable())
    
    def get_next(self):
        if algo_st().raw_data is None: 
            return None
        if algo_st().run:
            return BoundaryState()
        else:
            return None
        #return None

class BoundaryState(st.State):
    
    def execute(self):
        algo_st().boundary = graph.get_edge_vertices(algo_st().biimg)
        tRec().stamp("Find Edge")
        
        if debug:
            peConfig = ma.get_vorgraph_config(get_size())
            peConfig.pointConfig.edge_color = "red"
            ds.Display.current().draw_layer(graph.Graph(algo_st().boundary,[],[]), peConfig, ds.boundary)
            tRec().stamp("Draw Boundary")

    def get_next(self):
        return VorState()
    
class VorState(st.State):
    
    def execute(self):
        algo_st().vor = graph.get_voronoi(algo_st().boundary)
        tRec().stamp("Voronoi")
    
    def get_next(self):
        return PruneState()

class PruneState(st.State):
    
    def execute(self):
        algo_st().graph = graph.graph_in_image(algo_st().vor.graph, algo_st().biimg)
        tRec().stamp("Prune Voronoi")
        
        if debug:
            peConfig = ma.get_vorgraph_config(get_size())
            ds.Display.current().draw_layer(algo_st().vor.graph, peConfig, ds.internalVoronoi)
            tRec().stamp("Draw Prune Voronoi")
    
    def get_next(self):
        return BTState()

class BTState(st.State):
    
    def execute(self):
        closestDist = graph.get_closest_dists(algo_st().graph.point_ids, algo_st().vor) 
        tRec().stamp("Calc Radius")
        
        algo_st().algo = BurningAlgo(algo_st().graph, closestDist, max(app_st().shape))
        algo_st().algo.burn()
        tRec().stamp("Burn")
        
        if debug:
            bts = algo_st().algo.npGraph.get_bts()
            ets = algo_st().algo.npGraph.get_ets()
            self.__draw(bts, ds.burnTime)
            self.__draw(ets, ds.erosionT)
            tRec().stamp("Draw Burn Graph")
        
    
    def get_next(self):
        #return PruneChoosingState()
        return ETPruneState()
    
    def __draw(self, radi, layerName):
        peConfig = ma.get_vorgraph_config(get_size())
        colors = graph.get_color_list(radi)
        peConfig.pointConfig.edge_color = colors
        peConfig.edgeConfig.edge_color = graph.get_edge_color_list(colors, algo_st().graph.edgeIndex)
        ds.Display.current().draw_layer(algo_st().graph, peConfig, layerName)

class PruneChoosingState(st.State):
    
    def get_next(self):
        return ETPruneState() if app_st().method == 0 else AngleState()


class AngleState(st.State):
    
    def execute(self): 
        
        if algo_st().algo is None:
            return
        
        angles = graph.get_angle(algo_st().graph.edge_ids, algo_st().vor)
        #print(angles)
        algo_st().algo.npGraph.set_angles(angles) 
        tRec().stamp("calc angles")           
       
        
    def get_next(self):
        return AnglePruneState()
        


class ETPruneState(st.State):
    
    def execute(self):
        if algo_st().algo is None:
            return
        
        prune_algo = ETPruningAlgo(algo_st().algo.graph, algo_st().algo.npGraph)
        pruneT = app_st().etThresh / 100.0 * max(app_st().shape)
        algo_st().final = prune_algo.prune(pruneT)
        tRec().stamp("ET Prune")
        algo_st().finalEts = prune_algo.pruned_et
        
        joints = algo_st().final.get_joints()
        jointG = graph.Graph(joints,[])
        tRec().stamp("find joints")
        
        peConfig = ma.get_vorgraph_config(get_size())
        '''
        peConfig.pointConfig.face_color = "red"
        peConfig.pointConfig.edge_color = "red"
        '''
        rds = algo_st().algo.npGraph.get_rad()
        colors = np.array(graph.get_color_list(rds))
        prune_colors = colors[prune_algo.pruned_flag>0]
        edge_colors = graph.get_edge_color_list(prune_colors,algo_st().final.edgeIndex)
        
        peConfig.edgeConfig.face_color = edge_colors
        peConfig.edgeConfig.edge_color = edge_colors
        peConfig.drawpoint = False
        peConfig.drawedge = True      
        ds.Display.current().draw_layer(algo_st().final, peConfig, ds.final)
        
        peConfig.pointConfig.face_color = "white"
        peConfig.pointConfig.edge_color = "black"
        peConfig.pointConfig.size = peConfig.pointConfig.size * 2
        peConfig.drawpoint = True
        peConfig.drawedge = False
        ds.Display.current().draw_layer(jointG, peConfig, ds.joint)
        
        
        tRec().stamp("Draw Final")

class AnglePruneState(st.State):
    
    def execute(self):
        if algo_st().algo is None:
            return
        
        pruneT = np.pi * app_st().etThresh / 100.0
        prune_algo = AnglePruningAlgo(algo_st().algo.graph, algo_st().algo.npGraph)
        prune_algo.prune(pruneT)
        
        peConfig = ma.get_vorgraph_config(get_size())
        #print(algo_st().algo.npGraph.get_segval())
        seg_val = algo_st().algo.npGraph.get_segval()
        colors = graph.get_three_color_list(seg_val)
        #print(colors)
        peConfig.pointConfig.edge_color = "blue"
        peConfig.edgeConfig.edge_color = colors
        ds.Display.current().draw_layer(algo_st().graph, peConfig, ds.angle)
        tRec().stamp("draw angles")
        


        
        