#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 29. jun. 2017

@author: Elizaveta Protsenko
'''
import matplotlib.pyplot as plt
from PyQt5 import QtGui,QtWidgets
import numpy as np
import readdata
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mtick 
from matplotlib import colors
from netCDF4 import Dataset 

def dist_profile(self): 
    plt.clf()
    try:
        index = str(self.qlistwidget.currentItem().text())
    except AttributeError: 
        print ("Choose the variable to print ")        
        messagebox = QtWidgets.QMessageBox.about(
            self, "Retry", 'Choose variable,please') 
        return None            
    readdata.get_cmap(self)
    numday = self.numday_box.value()  
    fh =  Dataset(self.fname)
    data = np.array(fh.variables[index])
    data_units = fh.variables[index].units
    ylen = len(self.depth)        
    xlen = len(self.dist)  

    # for some variables defined at grid middlepoints
    # kz and fluxes 
    if (data.shape[1])> ylen:
        y = self.depth2 
        if self.sediment != False:
            y_sed = np.array(self.depth_sed2) 
    elif (data.shape[1]) == ylen :
        y = self.depth 
        if self.sediment != False:              
            y_sed = np.array(self.depth_sed)            
    else :
        print ("wrong depth array size") 
    
    ylen = len(y)         


    if data.shape[2] > 1: 
        z2d = [data[numday][m][n]  for n in range(0,xlen) for m in range(0,ylen) ]                         
        zz = np.array(z2d).flatten().reshape(xlen,ylen).T 
      
        if self.scale_all_axes.isChecked():                      
            start = self.numday_box.value() 
            stop = self.numday_stop_box.value() 
        else : 
            start = numday
            stop = numday+1 
            
        watmin,watmax  = readdata.make_maxmin(
            self,data,start,stop,index,'wat_dist')    

        def fmt(x, pos):
            a, b = '{:.2e}'.format(x).split('e')
            return r'${} \times 10^{{{}}}$'.format(a, int(b)) 
    
        if self.sediment == False:   
            readdata.grid_plot(self,1)  

        elif self.sediment == True : 
            readdata.grid_plot(self,2)
           
            X_sed,Y_sed = np.meshgrid(self.dist,y_sed)
                                                   
            sed_min,sed_max = readdata.make_maxmin(self,
                    data,start,stop,index,'sed_dist') 

            sed_ticks = readdata.ticks_2(sed_min,sed_max)                                    
            sed_levs = np.linspace(sed_min,sed_max,
                            num = self.num) 
             
            if self.interpolate_checkbox.isChecked():                       
                CS1 = self.ax2.contourf(X_sed,Y_sed, zz,
                        levels = sed_levs,
                        extend="both", cmap=self.cmap)   
            else:        
                CS1 = self.ax2.pcolormesh(X_sed,Y_sed, zz, 
                    vmin = sed_min, vmax = sed_max, 
                                 cmap=self.cmap)  
                           
            self.ax2.axhline(0, color='white', linestyle = '--',
                        linewidth = 1 )                   

            self.ax2.set_ylim(self.ysedmax,self.ysedmin) 
            self.ax2.set_ylabel('Depth, cm',fontsize= self.font_txt)
            self.ax2.set_xlabel('distance, m',fontsize= self.font_txt)
                                                      
            from matplotlib import colors
            
            if sed_max > self.e_crit_max or sed_max < self.e_crit_min:
                format = mtick.FuncFormatter(fmt)
            else: 
                format = None 
            cb1 = plt.colorbar(CS1,cax = self.cax1, ticks = sed_ticks,format= format)
        
        X,Y = np.meshgrid(self.dist,y)
        self.ax.set_title(index + ', ' + data_units) 
        self.ax.set_ylabel('Depth, m',fontsize= self.font_txt)
        wat_ticks = readdata.ticks_2(watmin,watmax)  
        wat_levs = np.linspace(watmin,watmax,
                            num = self.num)            

        if self.interpolate_checkbox.isChecked():                                   
            CS = self.ax.contourf(X,Y, zz,
                extend="both", levels = wat_levs,  
                cmap=self.cmap1)           
        else:            
            CS = self.ax.pcolormesh(X,Y, zz, 
                 vmin = watmin,vmax = watmax,  
                 cmap=self.cmap1)
       
        if watmax > self.e_crit_max or watmax < self.e_crit_min:
            format = mtick.FuncFormatter(fmt)
            cb = plt.colorbar(CS,cax = self.cax,format= format)
        else: 
            format = None 
            cb = plt.colorbar(CS,cax = self.cax,ticks = wat_ticks)            
                       
        self.ax.set_ylim(self.y1max,0)
        fh.close()  
        self.canvas.draw()
                             
    else:
        messagebox = QtWidgets.QMessageBox.about(self, "Retry,please",
                                             'it is 1D BROM')
        pass