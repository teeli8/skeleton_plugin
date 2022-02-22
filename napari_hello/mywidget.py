# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 15:32:30 2022

@author: Yigan
"""
import napari
import sys
from qtpy.QtWidgets import QWidget, QApplication, QCheckBox
from .display import Display


debug_widget = "debug"

class WidgetManager:
    
    __instance = None
    
    def inst():
        if WidgetManager.__instance is None:
            WidgetManager.__instance = WidgetManager()
        return WidgetManager.__instance
    
    def __init__(self):
        self.widgets = list()
    
    def start(self):
        for w in self.widgets:
            w.sync()
    
    def add(self, widget : QWidget):
        self.widgets.append(widget)
    
    def find(self, name : str) -> QWidget:
        for w in self.widgets:
            if w.name == name:
                return w
        return None


class MainWidget(QWidget):

    def __init__(self, viewer : napari.Viewer, parent=None):
        super().__init__(parent)
            
    

class DebugWidget(QWidget):
    """Any QtWidgets.QWidget or magicgui.widgets.Widget subclass can be used."""


    def __init__(self, viewer : napari.Viewer, parent=None):
        super().__init__(parent)
        
        self.name = debug_widget
        
        
        self.show_edge_box = self.__make_box("show boundary", 0)       
        self.show_vor_box = self.__make_box("show full voronoi", 40)        
        self.show_intvor_box = self.__make_box("show internal voronoi", 80)        
        self.show_hm_box = self.__make_box("show heatmap", 120)       
        self.show_final_box = self.__make_box("show final", 160)
        
        WidgetManager.inst().add(self)
    
    def sync(self):
        config = Display.current().config
        config.show_edgepoints = self.show_edge_box.isChecked()
        config.show_voronoi = self.show_vor_box.isChecked()
        config.show_internal_voronoi = self.show_intvor_box.isChecked()
        config.show_heatmap = self.show_hm_box.isChecked()
        config.show_final = self.show_final_box.isChecked()
        Display.current().set_config(config)
    
    def __make_box(self, text, position):
        box = QCheckBox(self)
        box.setText(text)
        box.move(0, position)
        return box
        

'''
app = QApplication(sys.argv)
w = QWidget()
w.resize(300,300)
w.setWindowTitle("HA")

label.setText("Behold the Guru, Guru99")
label = QLabel(w)

label.move(100,130)
label.show()

w.show()

sys.exit(app.exec_())
'''