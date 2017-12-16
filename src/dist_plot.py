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
    data = np.array(self.fh.variables[index])
    data_units = self.fh.variables[index].units
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
        
    z2d = []
    if data.shape[2] > 1: 
        for n in range(0,xlen): # distance 
            for m in range(0,ylen):  # depth 
                # take only n's column for brom             
                z2d.append(data[numday][m][n])                     
        
        z2 = np.array(z2d).flatten() 
        z2 = z2.reshape(xlen,ylen)       
        zz = z2.T   

        if self.scale_all_axes.isChecked():                      
            start = self.numday_box.value() 
            stop = self.numday_stop_box.value() 
            print (start,stop)  
        else : 
            start = numday
            stop = numday+1 
            
            #(self,var,start,stop,index,type)
        maxmin = readdata.make_maxmin(
            self,data,start,stop,index,'water_dist')    
        watmin = maxmin[0]     
        watmax = maxmin[1]            
            
        '''                
        #if index == 'pH':
        watmin = round(
            data[start:stop,0:self.ny1max].min(),2)
        watmax = round(
            data[start:stop,0:self.ny1max].max(),2) '''
        #wat_ticks = np.linspace(watmin,watmax,5)
        #wat_ticks = (np.floor(wat_ticks*100)/100.)
        def fmt(x, pos):
            a, b = '{:.2e}'.format(x).split('e')
            b = int(b)
            return r'${} \times 10^{{{}}}$'.format(a, b) 
    
        if self.sediment == False:   
            readdata.grid_plot(self,1)                              
            #gs = gridspec.GridSpec(1, 1)                        
            #cax = self.figure.add_axes([0.92, 0.1, 0.02, 0.8])                  
                             
        elif self.sediment == True : 
            readdata.grid_plot(self,2)
            #gs = gridspec.GridSpec(2, 1)         
    
            X_sed,Y_sed = np.meshgrid(self.dist,y_sed)
                                   
            #ax2 = self.figure.add_subplot(gs[1])
            '''
            #if  self.change_limits_checkbox.isChecked():
                #readdata.make_maxmin(
                #    self,var,start,stop,index,type)                
            if index == 'pH':
                sed_min = round(
                    data[start:stop,self.nysedmin:].min(),2)
                sed_max = round(
                    data[start:stop,self.nysedmin:].max(),2)
                #sed_ticks = np.linspace(sed_min,sed_max,5)
                #sed_ticks = (np.floor(sed_ticks*100)/100.)             
                
            else: 
                sed_min = readdata.varmin(
                    self,data,'seddist',start,stop)
                sed_max = readdata.varmax(
                    self,data,'seddist',start,stop)'''
                
            sed_maxmin = readdata.make_maxmin(self,
                    data,start,stop,index,'sed_dist')    
            sed_min = sed_maxmin[0]     
            sed_max = sed_maxmin[1]                 
            sed_ticks = readdata.ticks(sed_min,sed_max) 
            #sed_levels = linspace(sed_min,sed_max,50)                                    
            sed_levs = np.linspace(sed_min,sed_max,
                            num = self.num) 
             
            if self.interpolate_checkbox.isChecked():                       
                CS1 = self.ax2.contourf(X_sed,Y_sed, zz,
                        levels = sed_levs,
                        #vmin = sed_min, vmax = sed_max,
                        extend="both", cmap=self.cmap)   
            else:        
                CS1 = self.ax2.pcolormesh(X_sed,Y_sed, zz, 
                    vmin = sed_min, vmax = sed_max, #levels = sed_levs,
                                 cmap=self.cmap)  
                           
            self.ax2.axhline(0, color='white', linestyle = '--',
                        linewidth = 1 )                   

            self.ax2.set_ylim(self.ysedmax,self.ysedmin) 
            self.ax2.set_ylabel('h, cm',fontsize= self.font_txt)  #Depth (cm)
            self.ax2.set_xlabel('distance, m',fontsize= self.font_txt)   #Distance (km)  
                         
            #cax1 = self.figure.add_axes([0.92, 0.1, 0.02, 0.35])
            #cax = self.figure.add_axes([0.92, 0.53, 0.02, 0.35])   
                           
            from matplotlib import colors
            
            if sed_max > self.e_crit_max or sed_max < self.e_crit_min:
                format = mtick.FuncFormatter(fmt)
                cb1 = plt.colorbar(CS1,cax = self.cax,format= format)
            else: 
                format = None 
                cb1 = plt.colorbar(CS1,cax = self.cax1,
                               ticks = sed_ticks)
        
        X,Y = np.meshgrid(self.dist,y)
        self.ax.set_title(index + ', ' + data_units) 
        self.ax.set_ylabel('h, m',fontsize= self.font_txt) #Depth (m)
        
        wat_ticks = readdata.ticks(watmin,watmax)  
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
        from matplotlib import colors
        
        if watmax > self.e_crit_max or watmax < self.e_crit_min:
            format = mtick.FuncFormatter(fmt)
            cb = plt.colorbar(CS,cax = self.cax,format= format)
        else: 
            format = None 
            cb = plt.colorbar(CS,cax = self.cax,ticks = wat_ticks)            
                       
        self.ax.set_ylim(self.y1max,0)
          
        self.canvas.draw()
                            
            
                                             
    else:
        messagebox = QtWidgets.QMessageBox.about(self, "Retry,please",
                                             'it is 1D BROM')
        pass