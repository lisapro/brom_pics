#!/usr/bin/python
# -*- coding: utf-8 -*-

# this ↑ comment is important to have 
# at the very first line 
# to define using unicode 

'''
Created on 29. jun. 2017

@author: ELP
'''

import matplotlib.pyplot as plt
from PyQt4 import QtGui
import numpy as np
import readdata
import matplotlib.gridspec as gridspec
from netCDF4 import num2date 
import matplotlib.dates as mdates


def time_profile(self,start,stop):
    
    plt.clf()
        
    try:
        index = str(self.qlistwidget.currentItem().text())
    except AttributeError:   
        messagebox = QtGui.QMessageBox.about(self, "Retry",
                                             'Choose variable,please') 
        return None           
    
    ## read chosen variable     
    z = np.array(self.fh.variables[index]) 
    
    # take the value of data units for the title
    data_units = self.fh.variables[index].units
    
    z = z[start:stop] 
    ylen1 = len(self.depth) #95  

    x = np.array(self.time[start:stop]) 
    xlen = len(x)     

    # check if the variable is defined on middlepoints  
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
    
    # check wich column to plot 
    numcol = self.numcol_2d.value() # 

    
    if 'i' in self.names_vars:
        # check if we have 2D array 
        if z.shape[2] > 1:
            for n in range(0,xlen): #xlen
                for m in range(0,ylen):  
                    # take only n's column for brom             
                    z2d.append(z[n][m][numcol]) 
  
            z = np.array(z2d)                     
    z = z.flatten()   
    z = z.reshape(xlen,ylen)       
    zz = z.T  
        
    if 'Kz' in self.names_vars and index != 'pH':
        watmin = readdata.varmin(self,zz,'wattime',start,stop) 
        watmax = readdata.varmax(self,zz,'wattime',start,stop)
        #wat_ticks = readdata.ticks(watmin,watmax) 
       
    elif 'Kz'in self.names_vars and index == 'pH':
        
        # take the value with two decimal places 
        watmin = round(zz[0:self.ny1max,:].min(),2) 
        watmax = round(zz[0:self.ny1max,:].max(),2) 
        wat_ticks = np.linspace(watmin,watmax,5)    
        wat_ticks = (np.floor(wat_ticks*100)/100.)   
        
    # if we do not have kz     
    else:  
        self.ny1max = len(self.depth-1)
        self.y1max = max(self.depth)    
        watmin = readdata.varmin(self,zz,'wattime',start,stop) #0 - water 
        watmax = readdata.varmax(self,zz,'wattime',start,stop)
        

    if self.scale_all_axes.isChecked(): 
        z_all_columns = np.array(self.fh.variables[index])  
        watmin = round((z_all_columns[start:stop,0:self.ny1max,:].min()),0) 
        watmax = round((z_all_columns[start:stop,0:self.ny1max,:].max()),2) 
        
    #wat_ticks = np.linspace(watmin,watmax,5)         
    wat_ticks = readdata.ticks(watmin,watmax)   
    #wat_ticks = (np.floor(wat_ticks*100)/100.)               
    
    if self.sediment == False: 
        gs = gridspec.GridSpec(1, 1) 
        gs.update(left = 0.07,right = 0.9 )
        cax = self.figure.add_axes([0.92, 0.1, 0.02, 0.8])  
    else : 
                         
        gs = gridspec.GridSpec(2, 1) 
        gs.update(left = 0.07,right = 0.9 )
         

        X_sed,Y_sed = np.meshgrid(x,y_sed)
        
        if self.datescale_checkbox.isChecked() == True:
            
            self.format_time = num2date(X_sed,
                                         units= self.time_units)   
            X_sed = self.format_time
        
        ax2 = self.figure.add_subplot(gs[1])  


        if self.scale_all_axes.isChecked(): 
            #z_all_columns = np.array(self.fh.variables[index])  
            #print(z_all_columns.shape)
            sed_min  = round((
                z_all_columns[start:stop,self.nysedmin-2:,:].min()),2) 
            sed_max = round((
                z_all_columns[start:stop,self.nysedmin-2:,:].max()),2) 
            sed_ticks = readdata.ticks(sed_min,sed_max)
            
        else :
            sed_min = readdata.varmin(self,zz,'sedtime',start,stop)
            sed_max = readdata.varmax(self,zz,'sedtime',start,stop)     
            sed_ticks = readdata.ticks(sed_min,sed_max)
                        
        if index == 'pH': 
            sed_min  = (zz[self.nysedmin-2:,:].min()) 
            sed_max  = (zz[self.nysedmin-2:,:].max())                 
            sed_ticks = readdata.ticks(sed_min,sed_max) 
            sed_ticks = (np.floor(sed_ticks*100)/100.)                

               
        ax2.set_ylabel('h, cm',fontsize= self.font_txt) 
        ax2.set_xlabel('Number of day',fontsize= self.font_txt)  
                           
        sed_levs = np.linspace(sed_min,sed_max,
                             num = self.num) 
        ax2.set_ylim(self.ysedmax,self.ysedmin) #ysedmin
        #ax2.set_xlim(start,stop)


        
                   
        #print (self.dates)
        #x = self.dates

        #   x = self.dates
        #print (self.dates, x )
        #calendar= time_calendar)
        #self.time = self.dates 

        #print (X_sed[0])
        
        #CS1 = ax2.contourf(X_sed,Y_sed, zz, levels = sed_levs, #int_        
        #                  extend="both", cmap= self.cmap1)
        
        CS1 = ax2.pcolormesh(X_sed,Y_sed, zz,    
                         cmap= self.cmap1)       
        
        if self.datescale_checkbox.isChecked() == True: 
            if len(x) > 365:
                ax2.xaxis_date()
                ax2.xaxis.set_major_formatter(
                    mdates.DateFormatter('%m/%Y'))  
            else : 
                ax2.xaxis_date()
                ax2.xaxis.set_major_formatter(
                    mdates.DateFormatter('%d/%m'))                                 
        
        # Add an axes at position rect [left, bottom, width, height]                    
        cax1 = self.figure.add_axes([0.92, 0.1, 0.02, 0.35])
        

        ax2.axhline(0, color='white', linestyle = '--',linewidth = 1 )        
        cb_sed = plt.colorbar(CS1,cax = cax1)
        cb_sed.set_ticks(sed_ticks)   
          
        #cb.set_label('Water')   
        cax = self.figure.add_axes([0.92, 0.53, 0.02, 0.35])      
             
        if self.yearlines_checkbox.isChecked()==True and \
           self.datescale_checkbox.isChecked()== False:
            for n in range(start,stop):
                if n%365 == 0: 
                    ax2.axvline(n, color='white', linestyle = '--') 
                    
                  
                    
        #if self.injlines_checkbox.isChecked()== True:             
        #    ax2.axvline(365,color='red', linewidth = 2,
        #            linestyle = '--',zorder = 10) 
        #    ax2.axvline(730,color='red',linewidth = 2,
        #            linestyle = '--',zorder = 10)                       
                                                               
    X,Y = np.meshgrid(x,y)  
    ax = self.figure.add_subplot(gs[0])
    
    if self.datescale_checkbox.isChecked() == True: 
        X = self.format_time     
                      
    
     

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
    #ax.set_title(index)
    
    ax.set_title(index + ', ' + data_units) 
    ax.set_ylim(self.y1max,self.ny1min)   

    ax.set_ylabel('h, m',fontsize= self.font_txt)
     
    wat_levs = np.linspace(watmin,watmax,num= self.num)
                            
    ## contourf() draws contour lines and filled contours
    ## levels = A list of floating point numbers indicating 
    ## the level curves to draw, in increasing order    
    ## If None, the first value of Z will correspond to the lower
    ## left corner, location (0,0).  
    ## If â€˜imageâ€™, the rc value for image.origin will be used.
      
    #CS = ax.contourf(X,Y, zz, levels = wat_levs, extend="both", #int_
    #                      cmap= self.cmap)
    CS = ax.pcolormesh(X,Y, zz,    
                         cmap= self.cmap) 
        
    if self.yearlines_checkbox.isChecked()==True and \
       self.datescale_checkbox.isChecked()== False:
        for n in range(start,stop):
            if n%365 == 0: 
                ax.axvline(n, color='white', linestyle = '--')     
                
    if self.datescale_checkbox.isChecked() == True: 
        if len(x) > 365:
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(
                mdates.DateFormatter('%m/%Y'))  
             
        else : 
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(
                mdates.DateFormatter('%d/%m'))     
                  
    cb = plt.colorbar(CS,cax = cax)   #, ticks = wat_ticks   
    cb.set_ticks(wat_ticks)

  
    '''def format_coord():
        
        col = int(x)
        row = int(y)
        #if col>=0 and col<numcols and row>=0 and row<numrows:
        z = zz[x,y]
        return 'z=%1.4f'%(z)

    ax.format_coord = format_coord()'''     
    
    
    
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