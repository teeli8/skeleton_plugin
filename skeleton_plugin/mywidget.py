# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 15:32:30 2022

@author: Yigan
"""
import napari
#import sys
from qtpy.QtWidgets import QWidget, QCheckBox, QPushButton,QSlider,QLabel,QLineEdit
from PyQt5.QtCore import Qt
from .display import Display
from . import mainalgo

main_widget = "main"
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
        self.name = main_widget
        
        left = 10
        
        s,t = self.__make_slider_label()
        self.thSlider = s
        self.thSText = t
        self.thSlider.valueChanged.connect(self.set_bi_thr)
        self.thSlider.sliderReleased.connect(self.set_bithr_lift)
        self.thSlider.move(left,10)
        self.thSText.move(left,30)
        
        self.etValue = 0
        s,t = self.__make_slider_label()
        self.etSlider = s
        self.etSText = t
        self.etSlider.valueChanged.connect(self.set_thr)
        self.etSlider.sliderReleased.connect(self.set_thr_lift)
        self.etSlider.move(left,70)
        self.etSText.move(left,90)
        
        self.etInput = QLineEdit(self)
        self.etInput.move(left+110,90)
        self.etInput.resize(40,20)
        self.etInput.returnPressed.connect(self.widget_changed)
        
        self.runButton = QPushButton(self)
        self.runButton.setText("Find Skeleton")
        self.runButton.clicked.connect(MainWidget.run)
        self.runButton.move(left, 120)
        
        self.saveButton = QPushButton(self)
        self.saveButton.setText("Save To File")
        self.saveButton.clicked.connect(self.save_to_file)
        self.saveButton.move(left, 150)
        
        self.resetButton = QPushButton(self)
        self.resetButton.setText("Reset")
        self.resetButton.clicked.connect(MainWidget.reset)
        self.resetButton.move(left, 170)
        
        self.set_bi_thr()
        self.set_thr()
        
        WidgetManager.inst().add(self)
    
    def sync(self):
        '''
        c = self.modeBox.isChecked()
        mainalgo.SkeletonApp.inst().reset_method(1 if c else 0)
        '''
        pass
    
    def run():
        WidgetManager.inst().start()
        mainalgo.SkeletonApp.inst().run()
        
    def set_bi_thr(self):
        self.thSText.setText("segmentation parameter : " + str(self.thSlider.value()) + "%")
    
    def set_bithr_lift(self):
        mainalgo.SkeletonApp.inst().reset_bithresh(self.thSlider.value())
    
    def set_thr(self):  
        self.etValue = self.etSlider.value()
        self.etSText.setText("pruning parameter : " + str(self.etValue) + "%")
        self.etInput.setText(str(self.etValue))
    
    def set_thr_lift(self):
        mainalgo.SkeletonApp.inst().reset_etthresh(self.etValue)
    
    def save_to_file(self):
        mainalgo.SkeletonApp.inst().save_to_file()
     
    def widget_changed(self):
        txt = self.etInput.text()
        if txt == "":
            self.etSlider.setValue(0)
            return
        try:
           num = float(txt)
           if num >= 0 and num <= 100:
               self.etSlider.setValue(num)
               self.etValue = num
               self.set_thr_lift()
           else:
               self.etInput.undo()
        except ValueError:
            self.etInput.undo()
            
        
        
    
    def reset():
        mainalgo.SkeletonApp.inst().reset_algo()
        Display.current().removeall()
    
    def __make_slider_label(self):
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(0,100)
        slider.resize(150,20)
        sText = QLabel('0', self)
        sText.setMinimumWidth(80)
        return slider,sText
    
    
            
    

class DebugWidget(QWidget):
    """Any QtWidgets.QWidget or magicgui.widgets.Widget subclass can be used."""


    def __init__(self, viewer : napari.Viewer, parent=None):
        super().__init__(parent)
        
        self.name = debug_widget
        
        
        self.show_edge_box = self.__make_box("show boundary", 0)       
        self.show_vor_box = self.__make_box("show full voronoi", 40)        
        self.show_intvor_box = self.__make_box("show internal voronoi", 80)        
        self.show_hm_box = self.__make_box("show heatmap", 120)       
        self.show_bt_box = self.__make_box("show burn time", 160)
        self.show_et_box = self.__make_box("show et", 200)
        self.show_final_box = self.__make_box("show final", 240)
        self.show_angle_box = self.__make_box("show angle", 280)
        
        WidgetManager.inst().add(self)
    
    def sync(self):
        config = Display.current().config
        config.show_edgepoints = self.show_edge_box.isChecked()
        config.show_voronoi = self.show_vor_box.isChecked()
        config.show_internal_voronoi = self.show_intvor_box.isChecked()
        config.show_heatmap = self.show_hm_box.isChecked()
        config.show_bt = self.show_bt_box.isChecked()
        config.show_et = self.show_et_box.isChecked()
        config.show_final = self.show_final_box.isChecked()
        config.show_angle = self.show_angle_box.isChecked()
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