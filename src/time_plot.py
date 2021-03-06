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
#import matplotlib.gridspec as gridspec
import numpy.ma as ma
#from PyQt5 import QtGui,QtWidgets
from netCDF4 import num2date, Dataset
import xarray as xr
import datetime
from datetime import timedelta

def fmt(x, pos):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return r'${} \times 10^{{{}}}$'.format(a, b)  

def get_years(var):
    len_years = var.time[-1].dt.year.values  - var.time[0].dt.year.values + 1
    start_date = datetime.date(year = var.time[0].dt.year.values,month = 1, day = 1)
    years = [start_date + timedelta(days=365*n) for n in range(len_years)]
    return years 

def add_lines(axis,years):
    [axis.axvline(y, color='white', linestyle = '--', linewidth=0.5) for y in years]

def time_profile(self,index,start,stop):   
     
    plt.clf()
    self.changing_depth = False               
    readdata.get_cmap(self)           
    ## read chosen variable and data units
    da = xr.open_dataset(self.fname)[index].copy()     
    data_units = da.units
    var = da[start:stop+1]
    if 'i' in var.coords:
        numcol = self.numcol_2d.value() 
        i = da.i.values[numcol]
        var = var.where(var.i == i,drop = True)     
    else:
        var = da[start:stop+1,:]

    x = var.time
    xlen = x.shape[0]   

    if 'z' in var.coords:d = 'z'
    elif 'z2' in var.coords: d = 'z2'          
    y = var[d]

    var['z_sed'] = (y - self.y2max)*100 
    ylen = y.shape[0]                                                     
    X,Y = np.meshgrid(var.time,var.z)

    self.ny1min = min(self.depth)
    zz = var.values.T[0]   

    if self.yearlines.isChecked()==True: 
        years = get_years(var.time)

    if (self.sediment == False and 
        'V_air' not in self.names_vars) : 
        readdata.grid_plot(self,1)              

    elif self.sediment == True:                                  
        readdata.grid_plot(self,2)
                              
        self.ax2.set_ylabel('Depth, cm',    
                            fontsize= self.font_txt) 

        var_sed = var.where(var['z_sed']> - 20,drop = True)   
        zz_sed = var_sed.T.values[0]                 
        X_sed,Y_sed = np.meshgrid(var_sed.time,var_sed.z_sed)  
                       
        sedmin = var_sed.values.min()
        sedmax =  var_sed.values.max() 
                  
        sed_ticks = readdata.ticks_2(sedmin,sedmax)
        sed_levs = np.linspace(sedmin,sedmax,
                            num = self.num)
                  
        if self.interpolate_checkbox.isChecked():
            CS1 = self.ax2.contourf(
                X_sed,Y_sed, zz_sed, levels = sed_levs,        
                extend="both", cmap= self.cmap1)                  
        else: 
            CS1 = self.ax2.pcolormesh(X_sed,Y_sed, zz_sed,                                      
                                 vmin = sedmin, vmax = sedmax,    
                             cmap= self.cmap1) 

        if self.yearlines.isChecked()==True:
            add_lines(self.ax2, years) 

        self.ax2.set_xlim(np.min(X_sed),np.max(X_sed))
        self.ax2.set_ylim(self.ysedmax,self.ysedmin)                                                               
        self.ax2.axhline(0, color='white', linestyle = '--',
                         linewidth = 0.5)        
                                          
        if sedmax > self.e_crit_max or sedmax < self.e_crit_min:
            format = mtick.FuncFormatter(fmt)
            cb_sed = plt.colorbar(CS1,cax = self.cax1,format = format)            
        else: 
            format = None                  
            cb_sed = plt.colorbar(CS1,cax = self.cax1,
                ticks = sed_ticks,format = format)
                                                      
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
       
    if self.yearlines.isChecked()==True:
        add_lines(self.ax, years)

    if (watmax > self.e_crit_max):
        format = mtick.FuncFormatter(fmt)
    elif ((self.sediment == True) & (sedmax < self.e_crit_min)): 
        #if sedmax < self.e_crit_min:
        format = mtick.FuncFormatter(fmt)
    else: 
        format = None  
    cb = plt.colorbar(CS, self.cax,ticks = wat_ticks, 
                          format = format)
    da.close()  


    self.canvas.draw()
