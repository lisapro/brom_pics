#!/usr/bin/python
# -*- coding: utf-8 -*-
# this â†‘ comment is important to have 
# at the very first line 
# to define using unicode 
'''
Created on 14. des. 2016

@author: E.Protsenko
'''
import math
import os,sys
import numpy as np
from netCDF4 import Dataset
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSpinBox,QLabel,QComboBox

from matplotlib import rc
from matplotlib import style
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt4agg import (
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec

import readdata

class Window(QtGui.QDialog):
    #QDialog - the base class of dialog windows.Inherits QWidget.
    #QMainWindow - 
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # function to display the names of the window flags        
        # Qt.Window Indicates that the widget is a window, usually with a window
        # system frame and a title bar
        # ! it is not possible to unset this flag if the widget 
        # does not have a parent.
        
        self.setWindowFlags(QtCore.Qt.Window)   
        self.setWindowTitle("BROM Pictures")
        self.setWindowIcon(QtGui.QIcon('bromlogo.png'))
        
        #app1 = QtGui.QApplication(sys.argv)
        #screen_rect = app1.desktop().screenGeometry()
        #width, height = screen_rect.width(), screen_rect.height()
             
        self.xsize = 8.27 
        self.figure = plt.figure(figsize=(11.69 ,self.xsize), dpi=100,
                                  facecolor='white') 
        #for unicode text     
        rc('font', **{'sans-serif' : 'Arial', 
                           'family' : 'sans-serif'})  
                
        # Set to make the inner widget resize with scroll area
        ##scrollArea = QtGui.QScrollArea()
        ##scrollwidget = QtGui.QWidget()  #central widget   
                
        # open file system to choose needed nc file 
        self.fname = str(QtGui.QFileDialog.getOpenFileName(self,
        'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)"))   

        # Create widget 1                    
        self.time_prof_box = QtGui.QComboBox()
        self.dist_prof_button = QtGui.QPushButton()
        self.time_prof_button =  QtGui.QPushButton()         
        # add items to Combobox
        self.numcol_2d = QtGui.QSpinBox()        
        self.varname_box = QtGui.QSpinBox()     
        self.numday_box = QtGui.QSpinBox() 
        self.textbox = QtGui.QLineEdit()  
        self.textbox2 = QtGui.QLineEdit()          
        '''for i in self.var_names_profile:
            self.time_prof_box.addItem(str(i))'''
            
        #varnames_list = []    
        self.fh =  Dataset(self.fname)
                
        #self.time_prof_box.addItem('plot 1D')  
        # add only 2d arrays to variables list       
        for names,vars in self.fh.variables.items():
            if names == 'z' or names == 'z2' : 
                pass
            elif names == 'time' or names == 'i' : 
                pass 
            else :
                self.time_prof_box.addItem(names)
        
        #read i variable to know number of columns 
        for names,vars in self.fh.variables.items():
            if names == 'z' or names == 'z2' : 
                pass
            elif names == 'time': # or names == 'i' : 
                pass 
            else :
                testvar = np.array(self.fh['i'][:])      
                break  
        
        lentime = len(self.fh['time'][:])
        #print (self.lentime)
        self.fh.close()    
        #print ('testvar', testvar.shape[2])
        self.textbox.setText(
            'Number of columns = {}'.format(str(testvar.shape[0])))
        self.textbox2.setText(
            'Number of days = {}'.format(lentime))                
        self.numcol_2d.setRange(0, int(testvar.shape[0]-1))   
        self.numday_box.setRange(0, lentime-1)               
        #self.varname_box = QtGui.QSpinBox()        
                
                
            #varnames_list.append(names)    
        #for names in self.fh.variables.items():
        #    print str(names)
        #    break
        #    self.time_prof_box.addItem(str(names))   
            
            
        # Define connection between clicking the button and 
        # calling the function to plot figures        
        ######3self.time_prof_box.currentIndexChanged.connect(
        ######    self.time_profile)    
        #self.numcol_2d.valueChanged.connect(
        #    self.time_profile) 
        self.time_prof_button.released.connect(self.time_profile)   
        self.dist_prof_button.released.connect(self.dist_profile)           
        # Create widget 2         
        self.all_year_box = QtGui.QComboBox()
        # add items to Combobox        
        self.time_prof_button.setText('Show Time Profile')
        self.dist_prof_button.setText('Show Dist Profile')        
        #for i in self.var_names_charts_year:
        #    self.all_year_box.addItem(str(i))
        # Define connection between clicking the button and 
        # calling the function to plot figures                   
        #self.all_year_box.currentIndexChanged.connect(
        #    self.all_year_charts) 

 
                     
        # Here I change the size and style of buttons
        self.time_prof_box.setStyleSheet(
        'QComboBox {background-color: #c2b4ae;padding: 2px;border-width: 5px;'
         'font: bold 15px;}') 
        
        
        self.time_prof_button.setStyleSheet(
        'QPushButton {background-color: #c2b4ae; border-width: 5px;'
        '  padding: 2px; font: bold 15px; }') 
         
        self.dist_prof_button.setStyleSheet(
        'QPushButton {background-color: #c2b4ae; border-width: 5px;'
        '  padding: 2px; font: bold 15px; }')
        
        self.varname_box.setStyleSheet(
        'QSpinBox {background-color: #c2b4ae; border-width: 5px;'
        '  padding: 2px; font: bold 15px; }')
                
        '''     
        self.all_year_box.setStyleSheet(
        'QComboBox {background-color: #c2b4ae;padding: 6px;border-width: 10px;'
         'font: bold 25px;}')           
           
        self.fick_box.setStyleSheet(
        'QComboBox {background-color: #c2b4ae;padding: 6px;border-width: 10px;'
         'font: bold 25px;}')          
         ''' 


         
        ##self.qwidget = QtGui.QWidget()
                
        self.canvas = FigureCanvas(self.figure)
    
        self.toolbar = NavigationToolbar(self.canvas, self) #, self.qfigWidget
        #self.canvas.setMinimumSize(self.canvas.size())
        #The QGridLayout class lays out widgets in a grid  
        
        self.grid = QtGui.QGridLayout(self)
        
        #Places the layout at position
        ##self.grid.addLayout(layout, 0, 0)
        
        self.grid.addWidget(self.canvas, 3, 0,1,6) 
        #self.grid.addWidget(scrollwidget, 2, 0,1,5)                    
        self.grid.addWidget(self.toolbar,1,0,1,1)   
         

        self.grid.addWidget(self.time_prof_button,1,1,1,1)  
        self.grid.addWidget(self.dist_prof_button,1,2,1,1) 
        
        self.grid.addWidget(self.time_prof_box,1,3,1,1) 
        self.grid.addWidget(self.numcol_2d ,1,4,1,1)              
        self.grid.addWidget(self.textbox,1,5,1,1)     
        self.grid.addWidget(self.numday_box,2,4,1,1)  
        self.grid.addWidget(self.textbox2,2,5,1,1)
        
        readdata.readdata2_brom(self,self.fname)     
        readdata.calculate_ywat(self)
        readdata.calculate_ybbl(self)          
        readdata.depth_sed(self)
        readdata.colors(self)
        
    def time_profile(self):
        
        plt.clf()
        index = str(self.time_prof_box.currentText())
        # read chosen variable 
        z = np.array(self.fh.variables[index]) 
         
        ylen = len(self.depth) #95  

        x = np.array(self.time) #np.arange(6)
        xlen = len(x) #365    
         
        # check if the variable is defined of middlepoints  
        if (z.shape[1])> ylen: 
            y = self.depth2
        elif (z.shape[1]) == ylen :
            y = self.depth #pass
        else :
            print ("wrong depth array size") 

        ylen = len(y)           

        z2d = []
        numcol = self.numcol_2d.value() # 
        print ('number of column', numcol) # QSpinBox.value()  #1 
        if z.shape[2] > 1:
            print (z.shape)
            for n in range(0,xlen):
                for m in range(0,ylen):                
                    z2d.append(z[n][m][numcol]) # take only n's column for brom
        #zz = np.array(zz).reshape(ylen,xlen)        
            z = np.array(z2d)
                              
        z = z.flatten()   
        z = z.reshape(len(self.time),len(self.depth))       
        zz = z.T      
      

        #self.fh.close()


        #def calculate_ybbl(self):
        for n in range(0,(len(self.depth2)-1)):
            if self.kz[0,n,0] == 0:
                self.y2max = self.depth2[n]         
                self.ny2max = n 
            elif self.kz[0,n,0] != 0 and n == (len(self.depth2)-1)-1 :  
                self.ny2max = n  
                self.y2max = self.depth2[n]    
                print (self.ny2max)
                break 
        print ('y2max', self.y2max)
        
        #def depth_sed(self):
        '''
        to_float = []
        for item in self.depth:
            to_float.append(float(item)) #make a list of floats from tuple 
        depth_sed = [] # list for storing final depth data for sediment 
        v=0  
        
        for i in to_float:
            v = (i- self.y2max)*100  #convert depth from m to cm
            depth_sed.append(v)
            self.depth_sed = depth_sed'''
         
        lendepth2 = len(self.depth2)   
         
                   
        #def y2max_fill_water(self):
        for n in range(0,(len(self.depth2)-1)):
    #        if depth[_]-depth[_?]
            if self.depth2[n+1] - self.depth2[n] >= 0.5:
                pass
            elif self.depth2[n+1] - self.depth2[n] < 0.50:
    #            watmax =  depth[n],depth[n]-depth[n+1],n
                self.y2max_fill_water = self.depth2[n] 
                self.nbblmin = n            
                break 
            elif n == (len(self.depth2)-2) and self.depth2[n+1] - self.depth2[n] >= 0.5 :
                self.y2max_fill_water = self.depth2[n] 
                self.nbblmin = n              
            
             
        #def calculate_ysed(self):
        for n in range(0,(len(self.depth_sed))):
            if self.kz[1,n,0] == 0:
                ysed = self.depth_sed[n]  
                self.ysedmin =  ysed - 10
                self.ysedmax =  self.depth_sed[len(self.depth_sed)-1] 
                self.y3min = self.depth_sed[self.nbblmin+2]
                self.nysedmin = n 
                #here we cach part of BBL to add to 
                #the sediment image                
                break            
        #def y_coords(self):       
        #self.y2min = self.y2max - 2*(self.y2max - self.y1max)
        #calculate the position of y2min, for catching part of BBL 
        self.ny2min = self.ny2max - 2*(self.ny2max - self.ny1max) 
        self.y2min_fill_bbl = self.y2max_fill_water = self.y1max 
        #y2max_fill_water()
        #109.5 #BBL-water interface
        self.ysedmax_fill_bbl = 0
        self.ysedmin_fill_sed = 0
        self.y1min = 0
        self.y2min = self.y2max - 2*(self.y2max - self.y1max)   
                  
        #calculate the position of y2min, for catching part of BBL 
        #def depth_sed2(self):
        to_float = []
        for item in self.depth2:
            to_float.append(float(item)) #make a list of floats from tuple 
        depth_sed2 = [] # list for storing final depth data for sediment 
        v=0  
        for i in to_float:
            v = (i- self.y2max)*100  #convert depth from m to cm
            depth_sed2.append(v)
            self.depth_sed2 = depth_sed2  
                           
 
                                 
        gs = gridspec.GridSpec(2, 1) 
        
        self.spr_aut ='#998970'#'#cecebd'#'#ffffd1'#'#e5e5d2'  
        self.wint =  '#8dc0e7'
        self.summ = '#d0576f' 
        self.a_w = 0.4 #alpha_wat alpha (transparency) for winter
        self.a_bbl = 0.3 
        
        self.a_s = 0.4 #alpha (transparency) for summer
        self.a_aut = 0.4 #alpha (transparency) for autumn and spring    
        self.wat_col = '#c9ecfd' # calc_resolution for filling water,bbl and sediment 
        self.bbl_col = '#2873b8' # for plot 1,2,3,4,5,1_1,2_2,etc.
        self.sed_col= '#916012'
        self.wat_col1 = '#c9ecfd' # calc_resolution for filling water,bbl and sediment 
        self.bbl_col1 = '#ccd6de' # for plot 1,2,3,4,5,1_1,2_2,etc.
        self.sed_col1 = '#a3abb1'
    
    
        
        # disctances between x axes
        dx = 0.1 #(height / 30000.) #0.1
        dy = 14 #height/96
        
        #x and y positions of axes labels 
        self.labelaxis_x =  1.10         
        self.labelaxis1_y = 1.02    
        self.labelaxis2_y = 1.02 + dx
        self.labelaxis3_y = 1.02 + dx * 2.
        self.labelaxis4_y = 1.02 + dx * 3.
        self.labelaxis5_y = 1.02 + dx * 4.
    
        # positions of xaxes
        self.axis1 = 0
        self.axis2 = 0 + dy 
        self.axis3 = 0 + dy * 2
        self.axis4 = 0 + dy * 3
        self.axis5 = 0 + dy * 4  
    
        self.font_txt = 15 #(height / 190.)  # text on figure 2 (Water; BBL, Sed) 
        self.xlabel_fontsize = 10 #(height / 170.) #14 #axis labels      
        self.ticklabel_fontsize = 10 #(height / 190.) #14 #axis labels   
        self.linewidth = 0.7                 
      
        y_sed = np.array(self.depth_sed)
          
        watmin = readdata.varmin(self,zz,0) #0 - water 
        watmax = readdata.varmax(self,zz,0)
        sed_min = readdata.varmin(self,zz,1)
        sed_max = readdata.varmax(self,zz,1) 

        '''watmin = math.floor(zz[0:self.ny1max,0:].min())# np.floor()
        watmax = math.ceil(zz[0:self.ny1max, 0:].max()) #np.round() 
        
        sed_min = math.floor(zz[self.ny2min:, 0:].min()) 
        sed_max = math.ceil(zz[self.ny2min:, 0:].max()) '''
        
        if watmin == watmax :
            if watmax == 0: 
                watmax = 0.1
                watmix = - 0.1
            else:      
                watmax = watmax + watmax/10. 
        elif sed_min == sed_max: 
            if sed_max == 0: 
                sed_max = 0.1
                sed_min = - 0.1
            else:     
                sed_max = sed_max + sed_max/10.   
             
        '''if self.num_var == 34: 
            watmax = 9
            watmin = 6.8
            sed_max = 10
            sed_min = 6 '''

        X,Y = np.meshgrid(x,y)
        X_sed,Y_sed = np.meshgrid(x,y_sed)
        
        ax = self.figure.add_subplot(gs[0])
        ax2 = self.figure.add_subplot(gs[1])        
        #self.figure, (ax, ax2) = plt.subplots(2, 1, sharex=True)
        #f.set_size_inches(11.69,8.27)

        ax.set_title(index)
        ax.set_ylim(self.y1max-1,0)       
        ax2.set_ylim(self.ysedmax,self.y3min) #ysedmin
        #xlen = len(x)
        ax.set_xlim(0,xlen)


        ax.set_ylabel('Depth (m)',fontsize= self.font_txt) #Label y axis 
        ax2.set_ylabel('Depth (cm)',fontsize= self.font_txt) 
        ax2.set_xlabel('Number of day',fontsize= self.font_txt) 
                          
        self.num = 50.            
        wat_levs = np.linspace(watmin,watmax,num= self.num)
        sed_levs = np.linspace(sed_min,sed_max,
                             num = self.num)
                
        int_wat_levs = []
        int_sed_levs= []
                
        for n in wat_levs:
            n = readdata.int_value(self,n,watmin,watmax)
            int_wat_levs.append(n)            
        for n in sed_levs:
            n = readdata.int_value(self,n,sed_min,
                                   sed_max)
            int_sed_levs.append(n)            
                      
        

        ## contourf() draw contour lines and filled contours
        # levels = A list of floating point numbers indicating 
        # the level curves to draw, in increasing order    
        # If None, the first value of Z will correspond to the lower
        # left corner, location (0,0).  
        # If â€˜imageâ€™, the rc value for image.origin will be used.
            
        CS = ax.contourf(X,Y, zz, levels= int_wat_levs,
                              cmap= self.cmap)

        CS1 = ax2.contourf(X_sed,Y_sed, zz, levels = int_sed_levs,
                              cmap= self.cmap1) #, origin='lower'
       
        # Add an axes at position rect [left, bottom, width, height]
        cax = self.figure.add_axes([0.92, 0.53, 0.02, 0.35])                
        cax1 = self.figure.add_axes([0.92, 0.1, 0.02, 0.35])
        
        wat_ticks = readdata.ticks(watmin,watmax)        
        sed_ticks = readdata.ticks(sed_min,sed_max)
        
        cb = plt.colorbar(CS,cax = cax,ticks = wat_ticks)
        cb_sed = plt.colorbar(CS1,cax = cax1 )
        #cb.set_label('Water')
        

        cb.set_ticks(wat_ticks)
        cb_sed.set_ticks(sed_ticks)  
        ax2.axhline(0, color='white', linestyle = '--',linewidth = 1 )     
  
        self.canvas.draw() 
        

    def dist_profile(self): 
        plt.clf()
        
        index = str(self.time_prof_box.currentText())
        numday = self.numday_box.value()  
        z = np.array(self.fh.variables[index]) 

       
        #self.depth2 = self.fh.variables['z2'][:] #middle points
        #dist = np.array(self.fh.variables['i'])                
        #self.depth = np.array(self.fh.variables['z'][:])    

        y = self.depth 
        ylen = len(self.depth)        
        xlen = len(self.dist)  
         
        # for some variables defined at grid middlepoints
        if (z.shape[1])> ylen:
            self.depth = np.array(self.fh.variables['z2'][:])    
        elif (z.shape[1]) == ylen :
            pass
        else :
            print ("wrong depth array size") 
         
        
        z2d = []
        if z.shape[2] > 1: 
            print ('zshape', z.shape)
            for n in range(0,xlen): # distance 
                for m in range(0,ylen):  # depth              
                    z2d.append(z[numday][m][n]) # take only n's column for brom
                #print ('1iteration', z2d)    
                #break                
        else:
            print ('it is 1D BROM')  
                      
        #zz = np.array(zz).reshape(ylen,xlen)        
        z2 = np.array(z2d)
        print ('z2d shape',z2.shape)
        z = z2.flatten()   

        z = z.reshape(xlen,ylen)       
        zz = z.T 
        print (self.depth2)    
        for n in range(0,(len(self.depth2)-1)):
            #print ('depth2',len(self.depth2),n)
            if self.depth2[n+1] - self.depth2[n] >= 0.5:
                pass
            elif self.depth2[n+1] - self.depth2[n] < 0.50:    
                y1max = (self.depth2[n])
                print (y1max)
                y1max = y1max                                                      
                ny1max = n
                print ('distance ny1max', self.ny1max)
                break     
                    

        
        
        gs = gridspec.GridSpec(2, 1) 
        
        X,Y = np.meshgrid(self.dist,y)

        
        ax = self.figure.add_subplot(gs[0])
        ax2 = self.figure.add_subplot(gs[1])
        ax.set_title(index)
        
        data = np.array(self.fh.variables[index])
       
        #watmin = readdata.varmin(self,np.array(self.fh.variables[index]) ,0) #0 - water 
        watmin = data[:].min() #-(data[0:xlen, 0:, :].min()) #/3. #self.ny1max-1
        watmax = data[:].max() #+(data[0:xlen, 0:, :].min()) #/3. #self.ny1max-1
        #watmax = readdata.varmax(self,np.array(self.fh.variables[index]) ,0)
        
        print ('maxmin', watmin,watmax)
        self.num = 50.            
        wat_levs = np.linspace(watmin,watmax, num= self.num)
        #sed_levs = np.linspace(sed_min,sed_max,
        #                     num = self.num)
        print (watmin,watmax)       
        print (zz)
        int_wat_levs = []
        int_sed_levs= []
                
        for n in wat_levs:
            n = readdata.int_value(self,n,watmin,watmax)
            int_wat_levs.append(n)            
            
        '''for n in sed_levs:
            n = readdata.int_value(self,n,sed_min,
                                   sed_max)
            int_sed_levs.append(n)        '''    
                      
        #define color maps 
        #cmap = plt.cm.jet #gnuplot#jet#gist_rainbow
        #cmap1 = plt.cm.rainbow  
        
              
        CS = ax.contourf(X,Y, zz, levels= int_wat_levs,
                              cmap=self.cmap)
        
        CS1 = ax2.contourf(X,Y, zz, levels= int_wat_levs,
                              cmap=self.cmap1)      
          
        ax.scatter(X,Y, c = zz)  
        ax.set_ylim(self.y1max,0)  
        ax2.set_ylim(self.y3max, self.y1max) 
        
        cax = self.figure.add_axes([0.92, 0.53, 0.02, 0.35])                
        cax1 = self.figure.add_axes([0.92, 0.1, 0.02, 0.35])
        
        wat_ticks = readdata.ticks(watmin,watmax) 
        
        cb = plt.colorbar(CS,cax = cax,ticks = wat_ticks)   
        cb1 = plt.colorbar(CS1,cax = cax,ticks = wat_ticks)         
        cb.set_ticks(wat_ticks)       
        #print (numday,dist)      
        self.canvas.draw() 
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()
    main.setStyleSheet("background-color:#d8c9c2;")

    main.show()
    #PySide.QtCore.Qt.WindowFlags
    sys.exit(app.exec_()) 
