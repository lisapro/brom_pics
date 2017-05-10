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
from PyQt4.QtGui import QSpinBox,QLabel,QComboBox,QCheckBox

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
        # Qt.Window Indicates that the widget is a window, 
        # usually with a window system frame and a title bar
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
                
        # open file system to choose needed nc file 
        self.fname = str(QtGui.QFileDialog.getOpenFileName(self,
        'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)"))   

        #filename = self.fname
        self.fh =  Dataset(self.fname)
        readdata.readdata_brom(self)   
        
        # Create widgets
                            
        self.time_prof_box = QtGui.QComboBox()  
        self.qtreewidget = QtGui.QListWidget()      
        self.all_year_1d_box = QtGui.QComboBox()    
                           
        self.dist_prof_button = QtGui.QPushButton() 
        self.dist_prof_checkbox = QtGui.QCheckBox("Fit scale to data")      
        self.time_prof_last_year =  QtGui.QPushButton()    
        self.time_prof_all =  QtGui.QPushButton()           
        self.all_year_test_button =  QtGui.QPushButton() 
              
        self.numcol_2d = QtGui.QSpinBox()        
        self.varname_box = QtGui.QSpinBox()     
        self.numday_box = QtGui.QSpinBox() 
        
        self.textbox = QtGui.QLineEdit()  
        self.textbox2 = QtGui.QLineEdit()          
  
        # add items to Combobox        
        for i in self.var_names_charts_year:
            self.all_year_1d_box.addItem(str(i))

        ## self.time_prof_box.addItem('plot 1D')  
        ## add only 2d arrays to variables list       
        ## We skip z and time since they are 1d array, 
        ## we need to know the shape of other arrays
        ## If the file includes other 1d var, it 
        ## could raise an err, such var should be skipped also
        
        self.names_vars = [] 
        for names,vars in self.fh.variables.items():
            if names == 'z' or names == 'z2' : 
                self.names_vars.append(names)
            elif names == 'time' or names == 'i' : 
                self.names_vars.append(names) 
            else :
                self.time_prof_box.addItem(names)
                #names = QTreeWidgetItem(i)
                self.qtreewidget.addItem(names)
                self.names_vars.append(names)  
                      
        #read i variable to know number of columns 
        for names,vars in self.fh.variables.items():
            if names == 'z' or names == 'z2' : 
                pass
            elif names == 'time': # or names == 'i' : 
                pass 
            else :
                if 'i' in self.names_vars:
                    #print ("we try")
                    testvar = np.array(self.fh['i'][:])      
                    break  
                #except AttributeError:
                #    print ('var  i not found' )                
        #try:
        #    self.kz =  self.fh.variables['Kz'][:,:]  
        #except AttributeError:
        #    print ('var not found')      

                
        lentime = len(self.fh['time'][:])
        self.fh.close()    
        
        self.textbox2.setText(
            'Number of days = {}'.format(lentime))  
        if 'i' in self.names_vars:  
            self.textbox.setText(
                'Number of columns = {}'.format(str(
                testvar.shape[0])))                        
            self.numcol_2d.setRange(0, int(testvar.shape[0]-1))   
            self.numday_box.setRange(0, lentime-1)               

            
        # Define connection between clicking the button and 
        # calling the function to plot figures                           
        self.all_year_1d_box.currentIndexChanged.connect(
            self.all_year_charts)                   
        #self.numcol_2d.valueChanged.connect(
        #    self.time_profile) 
        self.time_prof_last_year.released.connect(self.call_print_lyr)
        self.all_year_test_button.released.connect(self.all_year_test)
        self.time_prof_all.released.connect(self.call_print_allyr)        

        #:(self.time_profile)   
        self.dist_prof_button.released.connect(self.dist_profile)           
        # Create widget 2         
        self.all_year_box = QtGui.QComboBox()
        # add items to Combobox 
               
        self.time_prof_all.setText('Time: all year')
        self.all_year_test_button.setText('1D plot')
        self.time_prof_last_year.setText('Time: last year')               
        self.dist_prof_button.setText('Show Dist Profile')       
                         
        self.canvas = FigureCanvas(self.figure)    
        self.toolbar = NavigationToolbar(self.canvas, self) #, self.qfigWidget
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
            print ("we do not have kz")      
        
        readdata.colors(self)
        readdata.set_widget_styles(self) 
        
  
        self.num = 50. 
        
    def time_profile(self,start,stop):
        
        plt.clf()
        index = str(self.qtreewidget.currentItem().text())
        #str(self.time_prof_box.currentText())
        #print (index)
        ## read chosen variable 
        z = np.array(self.fh.variables[index]) 

        z = z[start:stop] 
        ylen1 = len(self.depth) #95  

        x = np.array(self.time[start:stop]) #np.arange(6)
        xlen = len(x) #365    

        # check if the variable is defined of middlepoints  
        if (z.shape[1])> ylen1: 
            y = self.depth2
            if self.sediment != False:
                #print ('in sed1')                
                y_sed = np.array(self.depth_sed2) 
        elif (z.shape[1]) == ylen1:
            y = self.depth #pass
            if self.sediment != False:
                #print ('in sed1')                
                y_sed = np.array(self.depth_sed) 
        else :
            print ("wrong depth array size") 

        ylen = len(y)           

        z2d = []
        numcol = self.numcol_2d.value() # 
        #print ('number of column', numcol) # QSpinBox.value()  #1 
        if 'i' in self.names_vars:
            print ("in i")
            if z.shape[2] > 1:
                #print (z.shape)
                for n in range(0,xlen): #xlen
                    #print (n)
                    for m in range(0,ylen):  
                        # take only n's column for brom             
                        z2d.append(z[n][m][numcol]) 
            #zz = np.array(zz).reshape(ylen,xlen)        
                z = np.array(z2d)                     
        z = z.flatten()   
        z = z.reshape(xlen,ylen)       
        zz = z.T  
            
        #varmin(self,variable,vartype,start,stop)
        if 'Kz' in self.names_vars:
            watmin = readdata.varmin(self,zz,'wattime',start,stop) #0 - water 
            watmax = readdata.varmax(self,zz,'wattime',start,stop)
        else:  
            self.ny1max = len(self.depth-1)
            self.y1max = max(self.depth)    
            #print ('no kz',self.ny1max)
            watmin = readdata.varmin(self,zz,'wattime',start,stop) #0 - water 
            watmax = readdata.varmax(self,zz,'wattime',start,stop)
                      
 
        if self.sediment == False: 
            gs = gridspec.GridSpec(1, 1) 
            cax = self.figure.add_axes([0.92, 0.1, 0.02, 0.8])  
        else : 
                             
            gs = gridspec.GridSpec(2, 1) 
            #y_sed = np.array(self.depth_sed)
            X_sed,Y_sed = np.meshgrid(x,y_sed)
            ax2 = self.figure.add_subplot(gs[1])  
            sed_min = readdata.varmin(self,zz,'sedtime',start,stop)
            sed_max = readdata.varmax(self,zz,'sedtime',start,stop)             
            ax2.set_ylim(self.ysedmax,self.ysedmin) #ysedmin
            ax2.set_xlim(start,stop)
            ax2.set_ylabel('Depth (cm)',fontsize= self.font_txt) 
            ax2.set_xlabel('Number of day',fontsize= self.font_txt) 
            
            sed_levs = np.linspace(sed_min,sed_max,
                                 num = self.num) 
             
            CS1 = ax2.contourf(X_sed,Y_sed, zz, levels = sed_levs, #int_
                              cmap= self.cmap1) #, origin='lower' 
            # Add an axes at position rect [left, bottom, width, height]                    
            cax1 = self.figure.add_axes([0.92, 0.1, 0.02, 0.35])
            sed_ticks = readdata.ticks(sed_min,sed_max) 

            ax2.axhline(0, color='white', linestyle = '--',linewidth = 1 )        
            cb_sed = plt.colorbar(CS1,cax = cax1 )
            cb_sed.set_ticks(sed_ticks)              
            #cb.set_label('Water')   
            cax = self.figure.add_axes([0.92, 0.53, 0.02, 0.35])           
                
            
        X,Y = np.meshgrid(x,y)             
        ax = self.figure.add_subplot(gs[0])
         

        if watmin == watmax :
            if watmax == 0: 
                watmax = 0.1
                watmin = 0
            else:      
                watmax = watmax + watmax/10.
                 
        if self.sediment != False:        
            if sed_min == sed_max: 
                if sed_max == 0: 
                    sed_max = 0.1
                    sed_min = 0
                else:     
                    sed_max = sed_max + sed_max/10.   
             

        self.ny1min = min(self.depth)
        ax.set_title(index)
        ax.set_ylim(self.y1max,self.ny1min)   

        ax.set_xlim(start,stop)
        ax.set_ylabel('Depth (m)',fontsize= self.font_txt)
         
        wat_levs = np.linspace(watmin,watmax,num= self.num)

                
        int_wat_levs = []
        int_sed_levs= []
                
        for n in wat_levs:
            n = readdata.int_value(self,n,watmin,watmax)
            int_wat_levs.append(n)  
                      

        ## contourf() draws contour lines and filled contours
        ## levels = A list of floating point numbers indicating 
        ## the level curves to draw, in increasing order    
        ## If None, the first value of Z will correspond to the lower
        ## left corner, location (0,0).  
        ## If â€˜imageâ€™, the rc value for image.origin will be used.
          
        CS = ax.contourf(X,Y, zz, levels= wat_levs, #int_
                              cmap= self.cmap)

        wat_ticks = readdata.ticks(watmin,watmax)        
       
        cb = plt.colorbar(CS,cax = cax,ticks = wat_ticks)
        cb.set_ticks(wat_ticks)
  
        self.canvas.draw()
        
        # Attempt to make timer for updating 
        # the datafile, while model is running 
        # still does not work 
        
        #timer = QtCore.QTimer(self)
        #timer.timeout.connect(self.update_all_year)
        #timer.start(20000) 
        
        #timer.timeout.connect(test) #(self.call_print_allyr)
        #timer.start(1)
        #QtCore.QTimer.connect(timer, QtCore.SIGNAL("timeout()"), self, QtCore.SLOT("func()"))
        
        #QtCore.QTimer.singleShot(1000, self.updateCost())   
     
             
    ## function to plot figure where 
    ## xaxis - is horizontal distance between columns
    ## yaxis is depth 
    
    def dist_profile(self): 
        plt.clf()
        index = str(self.qtreewidget.currentItem().text())
        #index = str(self.time_prof_box.currentText())
        numday = self.numday_box.value()  
        z = np.array(self.fh.variables[index]) 

        ylen = len(self.depth)        
        xlen = len(self.dist)  

        # for some variables defined at grid middlepoints
        # kz and fluxes 
        if (z.shape[1])> ylen:
            y = self.depth2 # = np.array(self.fh.variables['z2'][:])   
            if self.sediment != False:
                #print ('in sed2')
                y_sed = np.array(self.depth_sed2) 
        elif (z.shape[1]) == ylen :
            y = self.depth 
            if self.sediment != False:
                #print ('in sed1')                
                y_sed = np.array(self.depth_sed)            
        else :
            print ("wrong depth array size") 
        
        ylen = len(y) 

            
        z2d = []
        if z.shape[2] > 1: 
            for n in range(0,xlen): # distance 
                for m in range(0,ylen):  # depth 
                    # take only n's column for brom             
                    z2d.append(z[numday][m][n])                     
            
            z2 = np.array(z2d)
            z = z2.flatten()   
            z = z.reshape(xlen,ylen)       
            zz = z.T   
                        
            data = np.array(self.fh.variables[index])
            if self.dist_prof_checkbox.isChecked() == True:
                #print ('is checked')
                start = numday
                stop = numday+1
            else:     
                start = 0
                stop = len(self.time)    
                    
            watmin = readdata.varmin(self,data,'watdist',start,stop) 
            watmax = readdata.varmax(self,data,'watdist',start,stop)             
            wat_ticks = readdata.ticks(watmin,watmax) 
            
            if self.sediment == False:                                 
                gs = gridspec.GridSpec(1, 1)                        
                cax = self.figure.add_axes([0.92, 0.1, 0.02, 0.8])                  
                cb = plt.colorbar(CS,cax = cax,ticks = wat_ticks)        
                cb.set_ticks(wat_ticks)       
                              
            else :  
                gs = gridspec.GridSpec(2, 1)         
                
                X_sed,Y_sed = np.meshgrid(self.dist,y_sed)                       
                ax2 = self.figure.add_subplot(gs[1])
                               

                sed_min = readdata.varmin(self,data,'seddist',start,stop)
                sed_max = readdata.varmax(self,data,'seddist',start,stop)
          
                sed_levs = np.linspace(sed_min,sed_max,
                                     num = self.num)
        
                #int_wat_levs = []
                #int_sed_levs= []
                                        
                CS1 = ax2.contourf(X_sed,Y_sed, zz, levels = sed_levs,
                                      cmap=self.cmap1)      
                ax2.axhline(0, color='white', linestyle = '--',
                            linewidth = 1 )                   

                ax2.set_ylim(self.ysedmax,self.ysedmin) 
                                 
                cax1 = self.figure.add_axes([0.92, 0.1, 0.02, 0.35])
                cax = self.figure.add_axes([0.92, 0.53, 0.02, 0.35])   
                               
                sed_ticks = readdata.ticks(sed_min,sed_max)                 
                cb1 = plt.colorbar(CS1,cax = cax1,ticks = sed_ticks)     
                cb1.set_ticks(sed_ticks)
            

            
            X,Y = np.meshgrid(self.dist,y)
            ax = self.figure.add_subplot(gs[0])  
            ax.set_title(index) 

            wat_levs = np.linspace(watmin,watmax, num = self.num)        
            int_wat_levs = []
                    
            for n in wat_levs:
                n = readdata.int_value(self,n,watmin,watmax)
                int_wat_levs.append(n)            
    
                  
            CS = ax.contourf(X,Y, zz, levels= wat_levs,#int_
                                  cmap=self.cmap)
            wat_ticks = readdata.ticks(watmin,watmax) 
            cb = plt.colorbar(CS,cax = cax,ticks = wat_ticks)            
            cb.set_ticks(wat_ticks)                 
            ax.set_ylim(self.y1max,0)
              
            self.canvas.draw()
                                
                
                                                 
        else:
            messagebox = QtGui.QMessageBox.about(self, "Retry,please",
                                                 'it is 1D BROM')
            pass

        
    def call_print_lyr(self): 
        stop = len(self.time) #175
        start = stop - 365
        print (start,stop)
        self.time_profile(start,stop) 
            
    def call_print_allyr(self): 
        stop = len(self.time)
        start = 0
        self.time_profile(start,stop)   
     
    def all_year_test(self):  
        plt.clf()
        self.figure.patch.set_facecolor('white') 
        gs = gridspec.GridSpec(3,1) 
        gs.update(left=0.3, right=0.7,top = 0.94,bottom = 0.04,
                   wspace=0.2,hspace=0.3) 
        
        ax00 = self.figure.add_subplot(gs[0]) # water         
        ax10 = self.figure.add_subplot(gs[1]) # bbl
        ax20 = self.figure.add_subplot(gs[2]) # sediment 
        
        for axis in (ax00,ax10,ax20):
            axis.yaxis.grid(True,'minor')
            axis.xaxis.grid(True,'major')                
            axis.yaxis.grid(True,'major')    
                         
        index = str(self.time_prof_box.currentText())
        numcol = self.numcol_2d.value() # 
        # read chosen variable 
        z = np.array(self.fh.variables[index])
        z = np.array(z[:,:,numcol]) 
        #print (z.shape)
        
        ax00.set_title(index) 
        #Label y axis        
        ax00.set_ylabel('Depth (m)',
                        fontsize= self.font_txt) 
        ax10.set_ylabel('Depth (m)',
                        fontsize= self.font_txt)   
        ax20.set_ylabel('Depth (cm)',
                        fontsize= self.font_txt)
        
        ax00.set_ylim(self.y1max,0)  
        ax10.set_ylim(self.y2max, self.y1max)   
        ax20.set_ylim(self.ysedmax, self.ysedmin) 
         
        for n in range(0,365):#365
            if (n>0 and n <60) or (n>=335 and n<365) : #"winter"
            #if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter"                               
                ax00.plot(z[n][0:self.ny2max],
                      self.depth[0:self.ny2max],
                      self.wint,alpha = self.a_w, 
                      linewidth = self.linewidth , zorder = 10) 
             
                ax10.plot(z[n][0:self.ny2max],
                      self.depth[0:self.ny2max],
                      self.wint,alpha = self.a_w, 
                      linewidth = self.linewidth , zorder = 10) 
            
                ax20.plot(z[n][self.nysedmin-1:],
                      self.depth_sed[self.nysedmin-1:],
                      self.wint, alpha = self.a_w,
                      linewidth = self.linewidth, zorder = 10)   
            else: 
                ax00.plot(z[n][0:self.ny2max],
                      self.depth[0:self.ny2max],
                      self.spr_aut,alpha = self.a_w, 
                      linewidth = self.linewidth , zorder = 10) 
             
                ax10.plot(z[n][0:self.ny2max],
                      self.depth[0:self.ny2max],
                      self.spr_aut,alpha = self.a_w, 
                      linewidth = self.linewidth , zorder = 10) 
            
                ax20.plot(z[n][self.nysedmin-1:],
                      self.depth_sed[self.nysedmin-1:],
                      self.spr_aut, alpha = self.a_w,
                      linewidth = self.linewidth, zorder = 10)                          
                           
        self.canvas.draw()     
    def all_year_charts(self): 
        #messagebox = QtGui.QMessageBox.about(self, "Next time",
        #                                     'it does not work yet =(')           
        plt.clf()
        gs = gridspec.GridSpec(3,3) 
        gs.update(left=0.06, right=0.93,top = 0.94,bottom = 0.04,
                   wspace=0.2,hspace=0.1)   
        self.figure.patch.set_facecolor('white') 
        #self.figure.patch.set_facecolor(self.background) 
        #Set the background color  
        ax00 = self.figure.add_subplot(gs[0]) # water         
        ax10 = self.figure.add_subplot(gs[1]) # water
        ax20 = self.figure.add_subplot(gs[2]) # water 
 
        ax01 = self.figure.add_subplot(gs[3])          
        ax11 = self.figure.add_subplot(gs[4])
        ax21 = self.figure.add_subplot(gs[5])

        ax02 = self.figure.add_subplot(gs[6])    
        ax12 = self.figure.add_subplot(gs[7])
        ax22 = self.figure.add_subplot(gs[8])
   
        ax00.set_ylabel('Depth (m)',fontsize= self.font_txt) #Label y axis
        ax01.set_ylabel('Depth (m)',fontsize= self.font_txt)   
        ax02.set_ylabel('Depth (cm)',fontsize= self.font_txt) 
                                     
        for n in range(1,len(self.vars)):
            if (self.all_year_1d_box.currentIndex() == n) :
                
                varname1 = self.vars[n][0] 
                varname2 = self.vars[n][1] 
                varname3 = self.vars[n][2] 
                #print (n)
                z123 = readdata.read_all_year_var(self,
                            self.fname,varname1,varname2,varname3)

                z0 = np.array(z123[0])
                z1 = np.array(z123[1])
                z2 = np.array(z123[2])
                
                ax00.set_title(str(self.titles_all_year[n][0]), 
                fontsize=self.xlabel_fontsize, fontweight='bold') 
                
                ax10.set_title(str(self.titles_all_year[n][1]), 
                fontsize=self.xlabel_fontsize, fontweight='bold') 
                
                ax20.set_title(str(self.titles_all_year[n][2]), 
                fontsize=self.xlabel_fontsize, fontweight='bold')                                 
                self.num_var = n  

        for axis in (ax00,ax10,ax20,ax01,ax11,ax21,ax02,ax12,ax22):
            #water          
            axis.yaxis.grid(True,'minor')
            axis.xaxis.grid(True,'major')                
            axis.yaxis.grid(True,'major') 
                    
        ax00.set_ylim(self.y1max,0)   
        ax10.set_ylim(self.y1max,0)  
        ax20.set_ylim(self.y1max,0) 
        
        ax01.set_ylim(self.y2max, self.y2min)   
        ax11.set_ylim(self.y2max, self.y2min)  
        ax21.set_ylim(self.y2max, self.y2min) 

        ax02.set_ylim(self.ysedmax, self.ysedmin)   
        ax12.set_ylim(self.ysedmax, self.ysedmin)  
        ax22.set_ylim(self.ysedmax, self.ysedmin) 
        #
        #n0 = self.varmax(self,z0,1) #[0:self.y2max_fill_water,:].max() 
        start = 0
        stop = 365 
        #### to change""!!!!
        
        
        watmin0 = readdata.varmin(self,z0,"wattime",start,stop) 
        watmin1 = readdata.varmin(self,z1,"wattime",start,stop) 
        watmin2 = readdata.varmin(self,z2,"wattime",start,stop)          

        watmax0 = readdata.varmax(self,z0,"wattime",start,stop) 
        watmax1 = readdata.varmax(self,z1,"wattime",start,stop)
        watmax2 = readdata.varmax(self,z2,"wattime",start,stop)  
                 
        sed_min0 = readdata.varmin(self,z0,"sedtime",start,stop) 
        sed_min1 = readdata.varmin(self,z1,"sedtime",start,stop) 
        sed_min2 = readdata.varmin(self,z2,"sedtime",start,stop)    

        sed_max0 = readdata.varmax(self,z0,"sedtime",start,stop) 
        sed_max1 = readdata.varmax(self,z1,"sedtime",start,stop)         
        sed_max2 = readdata.varmax(self,z2,"sedtime",start,stop)         
        
        if self.num_var == 5: #pH 
            watmax1 = 9
            watmin1 = 6.5
        elif self.num_var == 2: #po4, so4
            watmax0 = 3  
            #watmax1 = 7000.          
            #watmin1 = 4000.            
        else:
            pass
                    
        
        self.m0ticks = readdata.ticks(watmin0,watmax0)
        self.m1ticks = readdata.ticks(watmin1,watmax1)
        self.m2ticks = readdata.ticks(watmin2,watmax2)  
        
        self.sed_m0ticks = readdata.ticks(sed_min0,sed_max0)
        self.sed_m1ticks = readdata.ticks(sed_min1,sed_max1)
        self.sed_m2ticks = readdata.ticks(sed_min2,sed_max2)                 
        #for axis in (ax00,ax10,ax20):             
        
        ax00.set_xlim(watmin0,watmax0)   
        ax01.set_xlim(watmin0,watmax0)         
        ax02.set_xlim(sed_min0,sed_max0)
        
        ax10.set_xlim(watmin1,watmax1)   
        ax11.set_xlim(watmin1,watmax1)         
        ax12.set_xlim(sed_min1,sed_max1)         
         
        ax20.set_xlim(watmin2,watmax2)   
        ax21.set_xlim(watmin2,watmax2)         
        ax22.set_xlim(sed_min2,sed_max2) 
                
        ax10.set_xlim(watmin1,watmax1)   
        ax11.set_xlim(watmin1,watmax1)         
        #ax12.set_xlim(sed_min1,sed_max1) 
                     
        ax20.set_xlim(watmin2,watmax2)   
        ax21.set_xlim(watmin2,watmax2)         
        #ax22.set_xlim(sed_min2,sed_max2)                  
        #water

                     
        ax00.fill_between(
                        self.m0ticks, self.y1max, 0,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w
        ax01.fill_between(
                        self.m0ticks, self.y2min_fill_bbl ,self.y2min,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w    
        ax01.fill_between(self.m0ticks, self.y2max, self.y2min_fill_bbl,
                               facecolor= self.bbl_col1, alpha=self.a_bbl) 
            
        ax02.fill_between(self.sed_m0ticks,self.ysedmin_fill_sed,-10,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)          
        ax02.fill_between(self.sed_m0ticks, self.ysedmax, self.ysedmin_fill_sed,
                               facecolor= self.sed_col1, alpha=self.a_s)          
        
            #axis.fill_between(self.xticks, self.y2max, self.y2min_fill_bbl,
            #                   facecolor= self.bbl_color, alpha=self.alpha_bbl)        
            
        ax10.fill_between(
                        self.m1ticks, self.y1max, 0,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w
        
        ax11.fill_between(
                        self.m1ticks, self.y2min_fill_bbl ,self.y2min,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w    
        ax11.fill_between(self.m1ticks, self.y2max, self.y2min_fill_bbl,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)      
        ax12.fill_between(self.sed_m1ticks,self.ysedmin_fill_sed,-10,
                               facecolor= self.bbl_col1, alpha=self.a_bbl) 
        ax12.fill_between(self.sed_m1ticks, self.ysedmax, self.ysedmin_fill_sed,
                              facecolor= self.sed_col1, alpha=self.a_s)        
        ax20.fill_between(
                        self.m2ticks, self.y1max, 0,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w
        
        ax21.fill_between(
                        self.m2ticks, self.y2min_fill_bbl ,self.y2min,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w    
        ax21.fill_between(self.m2ticks, self.y2max, self.y2min_fill_bbl,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)     
        ax22.fill_between(self.sed_m2ticks,self.ysedmin_fill_sed,-10,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)                         
        ax22.fill_between(self.sed_m2ticks, self.ysedmax, self.ysedmin_fill_sed,
                               facecolor= self.sed_col1, alpha=self.a_s) 
                            

        
                
        for n in range(0,3): #365
            if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter" 
                linewidth = self.linewidth
                                  
                ax00.plot(z0[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth , zorder = 10) 
                ax10.plot(z1[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth , zorder = 10)
                ax20.plot(z2[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 )  
                
                ax01.plot(z0[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
                ax11.plot(z1[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth , zorder = 10)
                ax21.plot(z2[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
    
                ax02.plot(z0[n],self.depth_sed,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
                ax12.plot(z1[n],self.depth_sed,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 )
                ax22.plot(z2[n],self.depth_sed,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
            elif n >= 150 and n < 249: #"summer"
                ax00.plot(z0[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
                ax10.plot(z1[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )
                ax20.plot(z2[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )  
                
                ax01.plot(z0[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
                ax11.plot(z1[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )
                ax21.plot(z2[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
    
                ax02.plot(z0[n],self.depth_sed,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
                ax12.plot(z1[n],self.depth_sed,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )
                ax22.plot(z2[n],self.depth_sed,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
            else : #"autumn and spring"
                ax00.plot(z0[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 ) 
                ax10.plot(z1[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 )
                ax20.plot(z2[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 )  
                
                ax01.plot(z0[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 ) 
                ax11.plot(z1[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 )
                ax21.plot(z2[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 ) 
    
                ax02.plot(z0[n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut, zorder = 10) 
                ax12.plot(z1[n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut, zorder = 10)
                ax22.plot(z2[n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut, zorder = 10)      


           
            
                          
        self.canvas.draw()     
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()
    main.setStyleSheet("background-color:#d8c9c2;")

    main.show()
    #PySide.QtCore.Qt.WindowFlags
    sys.exit(app.exec_()) 
