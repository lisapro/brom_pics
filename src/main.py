#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 14. des. 2016

@author: Elizaveta Protsenko
'''

import os,sys
import numpy as np
from netCDF4 import Dataset 
from PyQt5 import QtGui, QtCore,QtWidgets
from PyQt5.QtWidgets import (QLineEdit,QComboBox,
            QLabel,QListWidget,QPushButton,QGroupBox,
            QGridLayout,QCheckBox,QVBoxLayout,QSpinBox) 
from matplotlib import rc
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

import readdata, time_plot
import dist_plot, fluxes_plot
import all_year_1d
#import help_dialog
import matplotlib.pylab as pylab
from messages import Messages

params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        self.setWindowFlags(QtCore.Qt.Window)          
        self.setWindowIcon(QtGui.QIcon('img/logo.png'))       
        self.figure = plt.figure(figsize=(5.9 , 6.27),
                        facecolor='None',edgecolor='None') 
        self.figure.patch.set_alpha(0)    
                  
        self.fname ,_  = (QtWidgets.QFileDialog.getOpenFileName(self,
        'Open netcdf ', os.getcwd(), "netcdf (*.nc) "))  
        
        totitle = os.path.split(self.fname)[1]
        self.setWindowTitle("BROM Pictures ("+str(totitle)+')')           
        readdata.readdata_brom(self,self.fname)    
         
        # Add group Boxes - boxes of widgets
        createOptionsGroup(self)
        createTimeGroup(self)
        createDistGroup(self) 
                
        # Create widgets
        self.lbl_choose_var = QLabel('Choose variable:')                   
        self.qlistwidget = QListWidget() 

        self.qlistwidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.all_year_box =     QComboBox()                                      
        self.dist_prof_button = QPushButton()                               
        self.time_prof_lyr =    QPushButton()    
        self.time_prof_all =    QPushButton()  
                                        
        self.all_year_button =  QPushButton()                                  
        self.fick_box =         QPushButton() 
        self.help_button =      QPushButton(' ')
                                          
        readdata.read_num_col(self,self.fname)
                    
        # Add group Boxes - boxes of widgets       
        createOptionsGroup(self)
        createTimeGroup(self)
        createDistGroup(self)        
        createCmapLimitsGroup(self)
        createFluxGroup(self) 
                             
        if 'i' in self.names_vars:                     
            self.numcol_2d.setRange(0, int(self.testvar.shape[0]-1))               
            self.numday_box.setRange(0, self.lentime-1)              
            self.numday_stop_box.setRange(0, self.lentime-1)             
            self.numday_stop_box.setValue(self.lentime-1)
                
        # Add titles to buttons 
        self.time_prof_all.setText('Time: all year')
        self.fick_box.setText('Fluxes SWI')
        self.all_year_button.setText('1D plot')
        self.time_prof_lyr.setText('Time: last year')               
        self.dist_prof_button.setText('Transect 1 day')  
           
        ### Define connection                                   
        self.time_prof_lyr.released.connect(self.call_print_lyr)
        self.all_year_button.released.connect(self.call_1d)
        self.time_prof_all.released.connect(self.call_print_allyr)        
        self.fick_box.released.connect(self.call_fluxes)        
        self.dist_prof_button.released.connect(self.call_print_dist)                             
                  
        self.canvas = FigureCanvas(self.figure)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
                        QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)  
        self.canvas.setSizePolicy(sizePolicy)         
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        ## The QGridLayout class lays out widgets in a grid          
        self.grid = QGridLayout(self)
        
        readdata.widget_layout(self)        
        readdata.readdata2_brom(self,self.fname)   
                 
        if 'Kz'  in self.names_vars :
            readdata.calculate_ywat(self)
            readdata.calculate_ybbl(self)   
            readdata.y2max_fill_water(self)
            readdata.depth_sed(self)
            readdata.calculate_ysed(self)
            readdata.calc_nysedmin(self)  
            readdata.y_coords(self)        
        else: 
            self.sediment = False
            self.ny1max = len(self.depth)-1
            self.y1max = self.depth[self.ny1max]

        readdata.colors(self)
        readdata.set_widget_styles(self) 
        
        
        self.qlistwidget.addItems(self.sorted_names)
        self.qlistwidget.setFixedSize(
        self.qlistwidget.sizeHintForColumn(0)+ 2 * self.qlistwidget.frameWidth()+50,
              self.canvas.height())
        
    def call_1d(self):  
        start = self.numday_box.value() 
        stop = self.numday_stop_box.value() 

        all_year_1d.plot(self,start,stop)
        
    def call_fluxes(self): 
        start,stop = readdata.get_startstop(self)        
        fluxes_plot.fluxes(self,start,stop)
        
    def call_print_dist(self):         
        dist_plot.dist_profile(self)
            
    def call_print_lyr(self): #last year
        stop = len(self.time)
        start = stop - 365
        time_plot.time_profile(self,start,stop)
            
    def call_print_allyr(self):  
        start,stop = readdata.get_startstop(self)                 
        time_plot.time_profile(self,start,stop)  
                         
    def call_help(self):
        help_dialog.show(self) 

    def closeEvent(self, event):
            event.accept()
    
def createFluxGroup(self):
    self.flux_groupBox = QGroupBox("Fluxes properties")  
    self.minflux_lbl = QLabel('Min flux axis')
    self.maxflux_lbl = QLabel('Max flux axis')
    self.flux_min_box =  QLineEdit() 
    self.flux_max_box = QLineEdit()    
    self.manual_limits_flux =  QCheckBox(
    'Use manual limits for flux axis')  
    self.reverse_flux = QCheckBox(
    'Reverse flux axis')  
              
    self.flux_grid = QGridLayout(self.flux_groupBox)
    
    self.flux_grid.addWidget(self.reverse_flux,0,0,1,1)
    self.flux_grid.addWidget(self.manual_limits_flux,1,0,1,2) 
    self.flux_grid.addWidget(self.minflux_lbl,2,0,1,1) 
    self.flux_grid.addWidget(self.maxflux_lbl,2,1,1,1) 
    
    self.flux_grid.addWidget(self.flux_min_box,3,0,1,1) 
    self.flux_grid.addWidget(self.flux_max_box,3,1,1,1) 
☻  
def createDistGroup(self):  
        
    self.dist_groupBox = QGroupBox("Distance axis")           
    self.dist_grid = QGridLayout(self.dist_groupBox)   
    self.col_lbl = QLabel('Column: ')
    self.numcol_2d = QSpinBox() 

    try:
        self.lbl_maxcol = QLabel(
        'max\ncolumn: '+ str(self.testvar.shape[0]-1)) 
    except AttributeError: 
        pass
      
    self.dist_grid.addWidget(self.col_lbl,0,0,1,1) 
    self.dist_grid.addWidget(self.numcol_2d,1,0,1,1) 
    try:
        self.dist_grid.addWidget(self.lbl_maxcol,1,1,1,1) 
    except AttributeError: 
        pass    
       
def createTimeGroup(self):  
     
    self.last_year_button = QPushButton('last year')    
    self.time_groupBox = QGroupBox("Time axis")        

    self.numday_start_lbl = QLabel('start: ') 
    self.numday_stop_lbl =  QLabel('stop: ')  
    self.maxday_lbl =       QLabel('max day: ')
                    
    self.numday_box =       QSpinBox()   
    self.numday_stop_box =  QSpinBox()  
    self.value_maxday = QLabel(str(self.lentime-1))  
          
    self.cmap_water_box = QComboBox() 
    self.cmap_water_lbl = QLabel('cmap water: ') 
    self.cmap_water_box.addItems(readdata.cmap_list(self))  
    
    self.cmap_sed_box = QComboBox()
    self.cmap_sed_lbl = QLabel('cmap sed: ')
    self.cmap_sed_box.addItems(readdata.cmap_list(self)) 
                
    self.time_grid = QGridLayout(self.time_groupBox)   
    #line 0
    self.time_grid.addWidget(self.cmap_water_lbl,0,0,1,1)
    self.time_grid.addWidget( self.cmap_sed_lbl,0,1,1,1) 
        
    #line 1
    self.time_grid.addWidget(self.cmap_water_box,1,0,1,1)
    self.time_grid.addWidget( self.cmap_sed_box,1,1,1,1)    
    
    #line 2 
    self.time_grid.addWidget(self.numday_start_lbl,2,0,1,1)
    self.time_grid.addWidget( self.numday_stop_lbl,2,1,1,1) 
    self.time_grid.addWidget(      self.maxday_lbl,2,2,1,1)            
   
    #line 3             
    self.time_grid.addWidget(     self.numday_box,3,0,1,1) 
    self.time_grid.addWidget(self.numday_stop_box,3,1,1,1)      
    self.time_grid.addWidget(   self.value_maxday,3,2,1,1)   
   
def createOptionsGroup(self):
        self.options_groupBox = QGroupBox(" Properties ")  
        
        self.scale_all_axes = QCheckBox(
            "Scale:all columns, all time")                 
        self.yearlines = QCheckBox(
            'Draw year lines')           
        self.datescale_checkbox = QCheckBox(
            'Format time axis')         
        self.interpolate_checkbox = QCheckBox(
            'Interpolate')       
                    
        vbox = QVBoxLayout()
        vbox.addWidget(self.scale_all_axes)
        vbox.addWidget(self.yearlines)
        vbox.addWidget(self.datescale_checkbox)
        vbox.addWidget(self.interpolate_checkbox)    
        vbox.addStretch(1)
        self.options_groupBox.setLayout(vbox)     

def createCmapLimitsGroup(self):
        
        self.cmap_groupBox = QGroupBox("colour map limits ")  
        self.change_limits = QCheckBox('Change limits')
        self.exact_limits = QCheckBox('Exact limits')
        self.lbl_maxw = QLabel('max water: ')
        
        self.lbl_minw = QLabel('min water: ')   
        self.lbl_maxsed = QLabel('max sediment: ')
        self.lbl_minsed = QLabel('min sediment: ')  
        
        self.box_minw = QLineEdit()     
        self.box_maxw = QLineEdit() 
        self.box_minsed = QLineEdit()
        self.box_maxsed = QLineEdit() 
         
        cmap_grid = QGridLayout(self.cmap_groupBox) 

        cmap_grid.addWidget(self.change_limits,0,0,1,1) 
        cmap_grid.addWidget(self.exact_limits,0,1,1,1)
        cmap_grid.addWidget(self.lbl_minw,1,0,1,1)
        cmap_grid.addWidget(self.lbl_maxw,1,1,1,1)
        cmap_grid.addWidget(self.box_minw,2,0,1,1)
        cmap_grid.addWidget(self.box_maxw,2,1,1,1)  
                 
        cmap_grid.addWidget(self.lbl_minsed,3,0,1,1)        
        cmap_grid.addWidget(self.lbl_maxsed,3,1,1,1)
        cmap_grid.addWidget(self.box_minsed,4,0,1,1)
        cmap_grid.addWidget(self.box_maxsed,4,1,1,1)  

                          
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()
    main.setStyleSheet("background-color:#dceaed;")
    main.show()
    sys.exit(app.exec_()) 
