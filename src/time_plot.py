#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 29. jun. 2017

@author: Elizaveta Protsenko
'''
import numpy as np
import readdata
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick 
import matplotlib.gridspec as gridspec
import numpy.ma as ma
from PyQt5 import QtGui,QtWidgets
from netCDF4 import num2date, Dataset


def time_profile(self,index,start,stop):    
    plt.clf()
    self.changing_depth = False    
            
    readdata.get_cmap(self)           
    ## read chosen variable and data units
    self.fh =  Dataset(self.fname)      
    z = np.array(self.fh.variables[index]) 
    data_units = self.fh.variables[index].units
    
    z = z[start:stop+1] # read only part 
    ylen1 = len(self.depth) 
    x = np.array(self.time[start:stop+1]) 
    xlen = len(x)     

    # check if the variable is defined on middlepoints  
    if (z.shape[1])> ylen1: 
        y = self.depth2
        if self.sediment != False:               
            y_sed = np.array(self.depth_sed2) 
    elif (z.shape[1]) == ylen1:
        y = self.depth 
        if self.sediment != False:         
            y_sed = np.array(self.depth_sed) 
    else :
        print ("wrong depth array size") 

    ylen = len(y)           
    
    if ('i' in self.names_vars and z.shape[2] > 1):
        numcol = self.numcol_2d.value() 
        z = ma.array(
        [z[n][m][numcol] for n in range(
                 0,xlen) for m in range(
                     0,ylen)])
                            
    zz = ma.masked_invalid(z.flatten().reshape(xlen,ylen).T) #mask NaNs 
                                                                  
    X,Y = np.meshgrid(x,y)        
    self.ny1min = min(self.depth)
 
    def fmt(x, pos):
        a, b = '{:.2e}'.format(x).split('e')
        b = int(b)
        return r'${} \times 10^{{{}}}$'.format(a, b)          
                   
    if (self.sediment == False and 
        'V_air' not in self.names_vars) : 
        readdata.grid_plot(self,1)              
           
    elif self.sediment == True:                                  
        readdata.grid_plot(self,2)
                              
        self.ax2.set_ylabel('Depth, cm',    
                            fontsize= self.font_txt) 
        self.ax2.set_xlabel('Number of day',
                            fontsize= self.font_txt)
                        
        X_sed,Y_sed = np.meshgrid(x,y_sed)  
                    
        sedmin,sedmax = readdata.make_maxmin(self,
                    zz,start,stop,index,'sed_time')    
                   
        sed_ticks = readdata.ticks_2(sedmin,sedmax)
        sed_levs = np.linspace(sedmin,sedmax,
                            num = self.num)
                  
        if self.datescale_checkbox.isChecked() == True:  
            X_sed = readdata.use_num2date(
                self,self.time_units,X_sed)     
            readdata.format_time_axis2(
                self,self.ax2,xlen)        
            self.ax2.set_xlabel(' ',fontsize= self.font_txt)   
        if self.interpolate_checkbox.isChecked():
            CS1 = self.ax2.contourf(
                X_sed,Y_sed, zz, levels = sed_levs,        
                extend="both", cmap= self.cmap1)                  
        else: 
            CS1 = self.ax2.pcolormesh(X_sed,Y_sed, zz,                                      
                                 vmin = sedmin, vmax = sedmax,    
                             cmap= self.cmap1) 
                                    
        if self.yearlines.isChecked()==True and \
           self.datescale_checkbox.isChecked()== False:
            for n in range(start,stop):
                if n%365 == 0: 
                    self.ax2.axvline(n, color='white',
                                      linestyle = '--') 
        self.ax2.set_xlim(np.min(X_sed),np.max(X_sed))
        self.ax2.set_ylim(self.ysedmax,self.ysedmin)                                                               
        self.ax2.axhline(0, color='white', linestyle = '--',
                         linewidth = 1)        
                                          
        if sedmax > self.e_crit_max or sedmax < self.e_crit_min:
            format = mtick.FuncFormatter(fmt)
            cb_sed = plt.colorbar(CS1,cax = self.cax1,format = format)            
        else: 
            format = None                  
            cb_sed = plt.colorbar(CS1,cax = self.cax1,
                ticks = sed_ticks,format = format)
                          
    if self.datescale_checkbox.isChecked() == True:          
        X = readdata.use_num2date(self,self.time_units,X)     
        readdata.format_time_axis2(self,self.ax,xlen)   
                             
    watmin,watmax  = readdata.water_make_maxmin(
        self,zz,start,stop,index,'wat_time')    
    wat_ticks = readdata.ticks_2(watmin,watmax)
    wat_levs = np.linspace(watmin,watmax,num = self.num)  
         
    self.ax.set_title(index + ', ' + data_units) 
    self.ax.set_ylim(self.y1max,self.ny1min)   
    self.ax.set_ylabel('Depth, m',fontsize= self.font_txt)
                                         
    if self.interpolate_checkbox.isChecked():
        CS = self.ax.contourf(X,Y, zz, 
                         levels = wat_levs, extend="both", 
                              cmap= self.cmap)        
    else:       
        CS = self.ax.pcolormesh(X,Y, zz, 
            vmin = watmin, vmax = watmax,    
                        cmap= self.cmap) 
         
    self.ax.set_xlim(np.min(X),np.max(X))
       
    if self.yearlines.isChecked()==True  and \
       self.datescale_checkbox.isChecked()== False:
        for n in range(start,stop):
            if n%365 == 0: 
                self.ax.axvline(n, color='white', linestyle = '--')     

    if (watmax > self.e_crit_max):
        format = mtick.FuncFormatter(fmt)
  
    elif self.sediment == True: 
        if sedmax < self.e_crit_min:
            format = mtick.FuncFormatter(fmt)

    else: 
        format = None  
    cb = plt.colorbar(CS, self.cax,ticks = wat_ticks, 
                          format = format)
    self.fh.close()    
    self.canvas.draw()
