#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 14. des. 2016

@author: E.Protsenko
'''

import os,sys
import numpy as np
from netCDF4 import Dataset 
from PyQt4 import QtGui, QtCore

from matplotlib import rc
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt4agg import (
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

import readdata
import time_plot 
import dist_plot
import fluxes_plot
import all_year_1d
import help_dialog

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)
class Window(QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # function to display the names of the window flags        
        # Qt.Window Indicates that the widget is a window, 
        # usually with a window system frame and a title bar
        # ! it is not possible to unset this flag if the widget 
        # does not have a parent.
        
        self.setWindowFlags(QtCore.Qt.Window)   
        
        self.setWindowIcon(QtGui.QIcon('bromlogo2.png'))       
        self.figure = plt.figure(figsize=(8.69 , 10.27),
                        facecolor='None',edgecolor='None') 
        self.figure.patch.set_alpha(0)        
        # open file system to choose needed nc file 
        self.fname = str(QtGui.QFileDialog.getOpenFileName(self,
        'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)")) 

        totitle = os.path.split(self.fname)[1]
        self.setWindowTitle("BROM Pictures ("+str(totitle)+')') 
        #self.totitle = totitle[16:-3]           
        readdata.readdata_brom(self,self.fname)    
         
        # Add group Boxes - boxes of widgets
        createOptionsGroup(self)
        createTimeGroup(self)
        createDistGroup(self) 
                
        # Create widgets
        self.label_choose_var = QtGui.QLabel('Choose variable:')                   
        self.qlistwidget = QtGui.QListWidget() 

        self.qlistwidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        
        self.all_year_box = QtGui.QComboBox()                                      
        self.dist_prof_button = QtGui.QPushButton()           
        #self.injlines_checkbox = QtGui.QCheckBox(
        #    'Draw inject lines')                     
        self.time_prof_last_year =  QtGui.QPushButton()    
        self.time_prof_all =  QtGui.QPushButton()  
        
        #self.time_prof_box = QtGui.QComboBox()                                   
        self.all_year_button =  QtGui.QPushButton()                                  
        self.fick_box = QtGui.QPushButton() 
        self.help_button = QtGui.QPushButton(' ')
        
        self.fh =  Dataset(self.fname)        
        #def testvar(self):                    
        readdata.read_num_col(self,self.fname)
            #max_num_col = self.testvar.shape[0]
            #return (self.testvar)
            
        # Add group Boxes - boxes of widgets       
        createOptionsGroup(self)
        createTimeGroup(self)
        createDistGroup(self)        
        createCmapLimitsGroup(self)
                              
        if 'i' in self.names_vars:
            self.dist = np.array(self.fh.variables['i'])                          
            self.numcol_2d.setRange(0, int(self.testvar.shape[0]-1))               
            self.numday_box.setRange(0, self.lentime-1)              
            self.numday_stop_box.setRange(0, self.lentime-1)             
            self.numday_stop_box.setValue(self.lentime-1)
        
        self.fh.close()
        
        # Add titles to buttons 
        self.time_prof_all.setText('Time: all year')
        self.fick_box.setText('Fluxes SWI')
        self.all_year_button.setText('1D plot')
        self.time_prof_last_year.setText('Time: last year')               
        self.dist_prof_button.setText('Show Dist Profile')  
           
        ### Define connection between clicking the button and 
        ### calling the function to plot figures         
                                 
        self.time_prof_last_year.released.connect(self.call_print_lyr)
        self.all_year_button.released.connect(self.call_all_year)
        self.time_prof_all.released.connect(self.call_print_allyr)        
        self.fick_box.released.connect(self.call_fluxes)        
        self.dist_prof_button.released.connect(self.call_print_dist)                             
        self.help_button.released.connect(self.call_help)
                  
        self.canvas = FigureCanvas(self.figure)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)  
        self.canvas.setSizePolicy(sizePolicy)         
        self.toolbar = NavigationToolbar(self.canvas, self)
        #self.canvas.setMinimumSize(self.canvas.size())
        
        ## The QGridLayout class lays out widgets in a grid          
        self.grid = QtGui.QGridLayout(self)
        
        readdata.widget_layout(self)        
        readdata.readdata2_brom(self,self.fname)   
                 
        if 'Kz'  in self.names_vars :
            readdata.calculate_ywat(self)
            readdata.calculate_ybbl(self)   
            readdata.y2max_fill_water(self)
            readdata.depth_sed(self)
            readdata.calculate_ysed(self)
            readdata.calculate_ysed(self)
            readdata.calc_nysedmin(self)  
            readdata.y_coords(self)        
        else: 
            self.sediment = False
           
        readdata.colors(self)
        readdata.set_widget_styles(self) 
        
        self.num = 50. 

        self.qlistwidget.addItems(self.sorted_names)
        self.qlistwidget.setFixedSize(
        self.qlistwidget.sizeHintForColumn(0)+ 2 * self.qlistwidget.frameWidth()+50,
              self.canvas.height())
        
    def call_all_year(self):    
        all_year_1d.plot(self)
        
    def call_fluxes(self):    
        fluxes_plot.fluxes(self)
        
    def call_print_dist(self): 
        dist_plot.dist_profile(self)
            
    def call_print_lyr(self): #last year
        stop = len(self.time)
        start = stop - 365
        time_plot.time_profile(self,start,stop)
        #self.time_profile(start,stop) 
            
    def call_print_allyr(self):  
        start = self.numday_box.value() 
        stop = self.numday_stop_box.value()  
        #stop = len(self.time)
        #start = 0
        time_plot.time_profile(self,start,stop)
        #self.time_profile(start,stop)   
                       
    def save_figure(self): 
        #does not work 
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setPageSize(QtGui.QPrinter.A9)
        printer.setColorMode(QtGui.QPrinter.Color)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(self.edit.text())
        self.render(printer)
        #plt.savefig('pdf_fig.pdf',format = 'pdf')    
        #self.figure.savefig('pic.png', format='png')
   
   
    def call_help(self):
        help_dialog.show(self) 

        
def createDistGroup(self):  
        
    self.dist_groupBox = QtGui.QGroupBox("Distance axis")  
         
    self.dist_grid = QtGui.QGridLayout(self.dist_groupBox)
    
    self.col_label = QtGui.QLabel('Column: ')
    self.numcol_2d = QtGui.QSpinBox() 
    readdata.read_num_col(self,self.fname)
    self.label_maxcol = QtGui.QLabel(
        'max\ncolumn: '+ str(self.testvar.shape[0]-1)) 

    #max_col = readdata.read_num_col(self,self.fname)
    #self.label_maxcol_n =
    # QtGui.QLabel('max\ncolumn: ') #+ str(testvar.shape[0]-1))      
    
    self.dist_grid.addWidget(self.col_label,0,0,1,1) 
    self.dist_grid.addWidget(self.numcol_2d,1,0,1,1) 
    self.dist_grid.addWidget(self.label_maxcol,1,1,1,1) 
    
       
def createTimeGroup(self):  
     
    self.last_year_button = QtGui.QPushButton('last year')    
    self.time_groupBox = QtGui.QGroupBox(" Time axis")        
    self.label_maxday_label = QtGui.QLabel('max day: ')
    self.label_maxday = QtGui.QLabel(str(self.lentime-1))    
    self.numday_start_label = QtGui.QLabel('start: ') 
    self.numday_box = QtGui.QSpinBox()     
    self.numday_stop_label = QtGui.QLabel('stop: ') 
    self.numday_stop_box = QtGui.QSpinBox()    

    
    self.time_grid = QtGui.QGridLayout(self.time_groupBox)   
 

    self.time_grid.addWidget(self.numday_start_label,1,0,1,1)
    
      
    self.time_grid.addWidget(self.numday_start_label,1,0,1,1)
    self.time_grid.addWidget(self.numday_stop_label,1,1,1,1)
    self.time_grid.addWidget(self.label_maxday_label,1,2,1,1) 
    
    self.time_grid.addWidget(self.label_maxday,2,2,1,1)                    
    self.time_grid.addWidget(self.numday_box,2,0,1,1) 
    self.time_grid.addWidget(self.numday_stop_box,2,1,1,1)      

   
def createOptionsGroup(self):
        self.options_groupBox = QtGui.QGroupBox(" Properties ")  
        
        self.scale_all_axes = QtGui.QCheckBox(
            "Scale:all columns, all time")                 
        self.yearlines_checkbox = QtGui.QCheckBox(
            'Draw year lines')           
        self.datescale_checkbox = QtGui.QCheckBox(
            'Format time axis')         
        self.fielddata_checkbox = QtGui.QCheckBox(
            'Add field data (1D)') 
        self.interpolate_checkbox = QtGui.QCheckBox(
            'Interpolate')       
                     
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.scale_all_axes)
        vbox.addWidget(self.yearlines_checkbox)
        vbox.addWidget(self.datescale_checkbox)
        vbox.addWidget(self.fielddata_checkbox) 
        vbox.addWidget(self.interpolate_checkbox)       
        vbox.addStretch(1)
        self.options_groupBox.setLayout(vbox)     

def createCmapLimitsGroup(self):
        self.cmap_groupBox = QtGui.QGroupBox("colour map limits ")  
        self.label_maxwater = QtGui.QLabel('cmap max water: ')
        self.label_minwater = QtGui.QLabel('min water: ')   
        self.label_maxsed = QtGui.QLabel('cmap max sediment: ')
        self.label_minsed = QtGui.QLabel('min sediment: ')  
        self.box_minwater = QtGui.QSpinBox()
        self.box_maxwater = QtGui.QSpinBox()
        self.box_minsed = QtGui.QSpinBox()
        self.box_maxsed = QtGui.QSpinBox()        
               
        cmap_grid = QtGui.QGridLayout(self.cmap_groupBox) 
         
        cmap_grid.addWidget(self.label_minwater,0,0,1,1)
        cmap_grid.addWidget(self.label_maxwater,0,1,1,1)
        cmap_grid.addWidget(self.box_minwater,1,0,1,1)
        cmap_grid.addWidget(self.box_maxwater,1,1,1,1)           
        cmap_grid.addWidget(self.label_minsed,2,0,1,1)        
        cmap_grid.addWidget(self.label_maxsed,2,1,1,1)
        cmap_grid.addWidget(self.box_minsed,3,0,1,1)
        cmap_grid.addWidget(self.box_maxsed,3,1,1,1)       
                                
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()
    main.setStyleSheet("background-color:#dceaed;")
    main.show()
    sys.exit(app.exec_()) 
