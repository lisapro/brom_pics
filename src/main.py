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

        self.fh =  Dataset(self.fname)
        readdata.readdata_brom(self)   
        
        # Create widgets
                            
        self.time_prof_box = QtGui.QComboBox()        
        self.all_year_1d_box = QtGui.QComboBox()    
                           
        self.dist_prof_button = QtGui.QPushButton()       
        self.time_prof_last_year =  QtGui.QPushButton()    
        self.time_prof_all =  QtGui.QPushButton()           
              
        self.numcol_2d = QtGui.QSpinBox()        
        self.varname_box = QtGui.QSpinBox()     
        self.numday_box = QtGui.QSpinBox() 
        self.textbox = QtGui.QLineEdit()  
        self.textbox2 = QtGui.QLineEdit()          
  
        # add items to Combobox        
        for i in self.var_names_charts_year:
            self.all_year_1d_box.addItem(str(i))
                 
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
        ##print (self.lentime)
        self.fh.close()    
        ##print ('testvar', testvar.shape[2])
        self.textbox.setText(
            'Number of columns = {}'.format(str(testvar.shape[0])))
        self.textbox2.setText(
            'Number of days = {}'.format(lentime))                
        self.numcol_2d.setRange(0, int(testvar.shape[0]-1))   
        self.numday_box.setRange(0, lentime-1)               
        #self.varname_box = QtGui.QSpinBox()        
                
                
            #varnames_list.append(names)    
        #for names in self.fh.variables.items():
        #    #print str(names)
        #    break
        #    self.time_prof_box.addItem(str(names))   
            
        # Define connection between clicking the button and 
        # calling the function to plot figures                           
        self.all_year_1d_box.currentIndexChanged.connect(
            self.all_year_charts)                   
        #self.numcol_2d.valueChanged.connect(
        #    self.time_profile) 
        self.time_prof_last_year.released.connect(self.call_print_lyr)
        self.time_prof_all.released.connect(self.call_print_allyr)        

        #:(self.time_profile)   
        self.dist_prof_button.released.connect(self.dist_profile)           
        # Create widget 2         
        self.all_year_box = QtGui.QComboBox()
        # add items to Combobox 
               
        self.time_prof_all.setText('Time Prof all')
        self.time_prof_last_year.setText('Time Prof last year')               
        self.dist_prof_button.setText('Show Dist Profile')       
                         
        self.canvas = FigureCanvas(self.figure)    
        self.toolbar = NavigationToolbar(self.canvas, self) #, self.qfigWidget
        #self.canvas.setMinimumSize(self.canvas.size())
        #The QGridLayout class lays out widgets in a grid          
        self.grid = QtGui.QGridLayout(self)
        readdata.widget_layout(self)
        
        readdata.readdata2_brom(self,self.fname)            
        readdata.calculate_ywat(self)
        readdata.calculate_ybbl(self)   
        readdata.y2max_fill_water(self)        
        readdata.depth_sed(self)
        readdata.calculate_ysed(self)
        readdata.colors(self)
        readdata.set_widget_styles(self) 
        readdata.y_coords(self)
        readdata.calc_nysedmin(self)  
        
    def time_profile(self,start,stop):
        
        plt.clf()
        index = str(self.time_prof_box.currentText())
        # read chosen variable 
        z = np.array(self.fh.variables[index]) 
        z = z[start:stop] 
        ylen1 = len(self.depth) #95  

        x = np.array(self.time[start:stop]) #np.arange(6)
        xlen = len(x) #365    
         
        # check if the variable is defined of middlepoints  
        if (z.shape[1])> ylen1: 
            y = self.depth2
        elif (z.shape[1]) == ylen1:
            y = self.depth #pass
        else :
            print ("wrong depth array size") 

        ylen = len(y)           

        z2d = []
        numcol = self.numcol_2d.value() # 
        ##print ('number of column', numcol) # QSpinBox.value()  #1 
        if z.shape[2] > 1:
            ##print (z.shape)
            for n in range(start,stop): #xlen
                for m in range(0,ylen):                
                    z2d.append(z[n][m][numcol]) # take only n's column for brom
        #zz = np.array(zz).reshape(ylen,xlen)        
            z = np.array(z2d)
        ##print ('z.shape',z.shape,xlen,ylen)                      
        z = z.flatten()   
        ##print ('z',z)
        z = z.reshape(xlen,ylen)       
        zz = z.T      
      

        #self.fh.close()                        
 
                                 
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
          
        watmin = readdata.varmin(self,zz,0,start,stop) #0 - water 
        watmax = readdata.varmax(self,zz,0,start,stop)
        sed_min = readdata.varmin(self,zz,1,start,stop)
        sed_max = readdata.varmax(self,zz,1,start,stop) 
       #print (watmin,watmax,sed_min,sed_max)
        '''watmin = math.floor(zz[0:self.ny1max,0:].min())# np.floor()
        watmax = math.ceil(zz[0:self.ny1max, 0:].max()) #np.round() 
        
        sed_min = math.floor(zz[self.ny2min:, 0:].min()) 
        sed_max = math.ceil(zz[self.ny2min:, 0:].max()) '''
        
        if watmin == watmax :
            if watmax == 0: 
                watmajprintx = 0.1
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
        ax.set_ylim(self.y1max,0)       
        ax2.set_ylim(self.ysedmax,self.ysedmin) #ysedmin
        #xlen = len(x)
        ax.set_xlim(start,stop)
        ax2.set_xlim(start,stop)

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
        #for n in sed_levs:
        #    n = readdata.int_value(self,n,sed_min,
        #                           sed_max)
        #    int_sed_levs.append(n)            
                      
        

        ## contourf() draw contour lines and filled contours
        # levels = A list of floating point numbers indicating 
        # the level curves to draw, in increasing order    
        # If None, the first value of Z will correspond to the lower
        # left corner, location (0,0).  
        # If â€˜imageâ€™, the rc value for image.origin will be used.
          
        CS = ax.contourf(X,Y, zz, levels= wat_levs, #int_
                              cmap= self.cmap)

        CS1 = ax2.contourf(X_sed,Y_sed, zz, levels = sed_levs, #int_
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
        #def test():   
        #    print ("test")
        self.canvas.draw()
        
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.call_print_allyr)
        timer.start(200) 
        
        #timer.timeout.connect(test) #(self.call_print_allyr)
        #timer.start(1)
        #QtCore.QTimer.connect(timer, QtCore.SIGNAL("timeout()"), self, QtCore.SLOT("func()"))
        
        #QtCore.QTimer.singleShot(1000, self.updateCost())        

    def dist_profile(self): 
        plt.clf()
        
        index = str(self.time_prof_box.currentText())
        numday = self.numday_box.value()  
        z = np.array(self.fh.variables[index]) 

        #y = self.depth 
        ylen = len(self.depth)        
        xlen = len(self.dist)  
         
        # for some variables defined at grid middlepoints
        if (z.shape[1])> ylen:
            y = self.depth2 # = np.array(self.fh.variables['z2'][:])    
        elif (z.shape[1]) == ylen :
            y = self.depth 
        else :
            print ("wrong depth array size") 
         
        
        z2d = []
        if z.shape[2] > 1: 
            ##print ('zshape', z.shape)
            for n in range(0,xlen): # distance 
                for m in range(0,ylen):  # depth              
                    z2d.append(z[numday][m][n]) # take only n's column for brom
                ##print ('1iteration', z2d)    
                #break                
        else:
            messagebox = QtGui.QMessageBox.about(self, "Retry",'it is 1D BROM')
            #self.setWindowIcon(QtGui.QIcon('bromlogo.png')) 
            #messagebox.setIcon(QtGui.QIcon("monitor.png"))
            #print ('it is 1D BROM')  y
                      
        #zz = np.array(zz).reshape(ylen,xlen)        
        z2 = np.array(z2d)
        ##print ('z2d shape',z2.shape)
        z = z2.flatten()   

        z = z.reshape(xlen,ylen)       
        zz = z.T 
        ##print (self.depth2)    
        for n in range(0,(len(self.depth2)-1)):
            ##print ('depth2',len(self.depth2),n)
            if self.depth2[n+1] - self.depth2[n] >= 0.5:
                pass
            elif self.depth2[n+1] - self.depth2[n] < 0.50:    
                y1max = (self.depth2[n])
                ##print (y1max)
                y1max = y1max                                                      
                ny1max = n
                ##print ('distance ny1max', self.ny1max)
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
        
        ##print ('maxmin', watmin,watmax)
        self.num = 50.            
        wat_levs = np.linspace(watmin,watmax, num= self.num)
        #sed_levs = np.linspace(sed_min,sed_max,
        #                     num = self.num)
        ##print (watmin,watmax)       
        ##print (zz)
        int_wat_levs = []
        int_sed_levs= []
                
        for n in wat_levs:
            n = readdata.int_value(self,n,watmin,watmax)
            int_wat_levs.append(n)            

              
        CS = ax.contourf(X,Y, zz, levels= int_wat_levs,
                              cmap=self.cmap)
        
        CS1 = ax2.contourf(X,Y, zz, levels= int_wat_levs,
                              cmap=self.cmap1)      
          
        ax.scatter(X,Y, c = zz)  
        ax.set_ylim(self.y1max,0)  
        ax2.set_ylim(self.ysedmax,self.y3min) 
                        
        cax = self.figure.add_axes([0.92, 0.53, 0.02, 0.35])                
        cax1 = self.figure.add_axes([0.92, 0.1, 0.02, 0.35])
        
        wat_ticks = readdata.ticks(watmin,watmax) 
        
        cb = plt.colorbar(CS,cax = cax,ticks = wat_ticks)   
        cb1 = plt.colorbar(CS1,cax = cax,ticks = wat_ticks)         
        cb.set_ticks(wat_ticks)       
     
        self.canvas.draw() 
        
    def call_print_lyr(self): 
        stop = len(self.time) #175
        start = stop - 365
        self.time_profile(start,stop) 
            
    def call_print_allyr(self): 
        stop = len(self.time)
        start = 0
        print ("test")
        self.time_profile(start,stop)             
    
        
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
                #print('shape', z0.shape, z1.shape,z2.shape)   
       
                   
                #z0 = np.array(self.var1) #self.start_last_year
                #z1 = np.array(self.var1) #self.start_last_year
                #z2 = np.array(self.var1) #self.start_last_year                                
                #print (varname1,varname2,varname3)
                #print (z1[0])
                #z0 = np.array(self.vars_year[n][0][0][self.start_last_year:])
                #z1 = np.array(self.vars_year[n][1][0][:]) #self.start_last_year
                #z2 = np.array(self.vars_year[n][2][0][:]) #self.start_last_year
                ax00.set_title(str(self.titles_all_year[n][0]), 
                fontsize=self.xlabel_fontsize, fontweight='bold') 
                ax10.set_title(str(self.titles_all_year[n][1]), 
                fontsize=self.xlabel_fontsize, fontweight='bold') 
                ax20.set_title(str(self.titles_all_year[n][2]), 
                fontsize=self.xlabel_fontsize, fontweight='bold')                                 
                self.num_var = n #title0 = self.var_titles_charts_year[n][0] 
                #title1 = self.var_titles_charts_year[n][1] 
                #title2 = self.var_titles_charts_year[n][2]
              
        #ax00.set_title(title0) 
        #ax10.set_title(title1)
        #ax20.set_title(title2)

        #self.ax10.set_xlabel(r'$\rm Fe $',fontsize=14)   
        #self.ax20.set_xlabel(r'$\rm H _2 S $',fontsize=14) 




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
        
        
        watmin0 = readdata.varmin(self,z0,0,start,stop) #0 - water 
        watmin1 = readdata.varmin(self,z1,0,start,stop) #0 - water 
        watmin2 = readdata.varmin(self,z2,0,start,stop) #0 - water          

        watmax0 = readdata.varmax(self,z0,0,start,stop) #
        # z0[0:self.ny2max-4,:].max() # readdata.varmax(self,z0,0)
        watmax1 = readdata.varmax(self,z1,0,start,stop)
        watmax2 = readdata.varmax(self,z2,0,start,stop)  
         
         
        sed_min0 = readdata.varmin(self,z0,1,start,stop) #0 - water 
        sed_min1 = readdata.varmin(self,z1,1,start,stop) #0 - water 
        sed_min2 = readdata.varmin(self,z2,1,start,stop) #0 - water    

        sed_max0 = readdata.varmax(self,z0,1,start,stop) #z0[:,self.ny2min:].max() 
        sed_max1 = readdata.varmax(self,z1,1,start,stop) #z1[:,self.ny2min:].max()         
        sed_max2 = readdata.varmax(self,z2,1,start,stop) #z2[:,self.ny2min:].max()         
        
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
                            

        
                
        for n in range(0,365):
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
