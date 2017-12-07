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
from PyQt5 import QtGui,QtWidgets
import numpy as np
import readdata
import matplotlib.gridspec as gridspec
from netCDF4 import num2date 
import matplotlib.dates as mdates
import numpy.ma as ma
import matplotlib.ticker as mtick 

def time_profile(self,start,stop):
    
    plt.clf()
    self.changing_depth = False    
    try:
        index = str(self.qlistwidget.currentItem().text())
    except AttributeError:   
        messagebox = QtWidgets.QMessageBox.about(self, "Retry",
                                             'Choose variable,please') 
        return None     
          
    readdata.get_cmap(self)           
    ## read chosen variable and data units     
    z = np.array(self.fh.variables[index]) 
    data_units = self.fh.variables[index].units
    # read only part 
    z = z[start:stop+1] 
    ylen1 = len(self.depth) 
    x = np.array(self.time[start:stop+1]) 
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
    
    # check the column to plot 
    numcol = self.numcol_2d.value() # 

    if 'i' in self.names_vars:
        # check if we have 2D array 
        if z.shape[2] > 1:
            for n in range(0,xlen): #xlen
                for m in range(0,ylen):  
                    # take only n's column for brom             
                    z2d.append(z[n][m][numcol]) 
            z = ma.array(z2d)
                            
    z = z.flatten()   
    z = z.reshape(xlen,ylen)       
    tomask_zz = z.T  
    zz = ma.masked_invalid(tomask_zz) #mask NaNs 
                                                                  
    X,Y = np.meshgrid(x,y)        
    self.ny1min = min(self.depth)
 
    def fmt(x, pos):
        a, b = '{:.2e}'.format(x).split('e')
        b = int(b)
        return r'${} \times 10^{{{}}}$'.format(a, b)          
                   
    if self.sediment == False and 'V_air' not in self.names_vars : 
        readdata.grid_plot(self,1)              
 
    elif 'V_air' in self.names_vars:
        #elif self.changing_depth == True:     
        #Urmia or any other file with changing depth 
        readdata.grid_plot(self,2)  
        
        self.ax2.set_ylim(self.y1max,self.ny1min)   
        self.ax2.set_ylabel('h, m',fontsize= self.font_txt) 
               
        air = np.array(self.fh.variables['V_air'][start:stop+1,:,0]).T
        v_sed = np.array(self.fh.variables['V_sed'][start:stop+1,:,0]).T
        v_wat = np.array(self.fh.variables['V_wat'][start:stop+1,:,0]).T            
               
        zz_sed = zz     
        zz =  ma.masked_where(air >= 90, zz)
        zz =  ma.masked_where(v_sed > 30, zz)
        zz =  ma.masked_where(v_wat < 40, zz )   
        zz_sed =  ma.masked_where(air >= 90, zz_sed) 
        zz_sed =  ma.masked_where(v_sed < 30, zz_sed) 
          
        mask_air = np.ma.masked_where(v_wat > 5 , v_wat)
        mask_wat = np.ma.masked_where(v_wat < 30 , v_wat)        
        mask_sed_air = np.ma.masked_where(v_sed < 40, v_sed)
       
        sed_maxmin = readdata.make_maxmin(
            self,zz_sed,start,stop,index,'sediment')    
        sedmin = sed_maxmin[0]     
        sedmax = sed_maxmin[1]     
        
        X_urm,Y = np.meshgrid(x,y)
        
        if self.datescale_checkbox.isChecked() == True:             
            X_urm = readdata.use_num2date(self,self.time_units,X) 
            readdata.format_time_axis2(self,self.ax2,xlen)
       
        # plot masks for sediment and water               
        self.ax.pcolormesh(X_urm,Y,mask_sed_air
                           ,vmin = 50,vmax = 1000000,
                           cmap = 'copper_r')  
        self.ax2.pcolormesh(X_urm,Y,mask_wat,
                            vmin = 0,vmax = 10000000,
                            cmap = 'tab10_r') 
        CS1 = self.ax2.pcolormesh(X_urm,Y, zz_sed,
                            vmin = sedmin,vmax = sedmax,    
                            cmap= self.cmap1)        
        
        if sedmax > self.e_crit_max or sedmax < self.e_crit_min :
            format = mtick.FuncFormatter(fmt)
            #self.gs.update(left = 0.05,right = self.right_gs)
        else: 
            format = None    
        cb_sed = plt.colorbar(CS1,cax = self.cax1,format = format) 
        #cb_sed = readdata.add_colorbar(CS1,self.ax2,self.cax1)         
           
    elif self.sediment == True: 
                                 
        readdata.grid_plot(self,2)
                              
        self.ax2.set_ylabel('h, cm',fontsize= self.font_txt) 
        self.ax2.set_xlabel('Number of day',fontsize= self.font_txt)
                        
        X_sed,Y_sed = np.meshgrid(x,y_sed)  
                    
        maxmin = readdata.make_maxmin(self,
                    zz,start,stop,index,'sediment')    
        sedmin = maxmin[0]     
        sedmax = maxmin[1] 
                
        #sed_ticks = readdata.ticks(sedmin,sedmax)
        sed_levs = np.linspace(sedmin,sedmax,
                            num = self.num)  
                              
        self.ax2.set_xlim(np.min(X_sed),np.max(X_sed))
        self.ax2.set_ylim(self.ysedmax,self.ysedmin) #ysedmin                                                                
        self.ax2.axhline(0, color='white', linestyle = '--',
                         linewidth = 1)       
        
        
        if self.datescale_checkbox.isChecked() == True:  
            X_sed = readdata.use_num2date(self,self.time_units,X_sed)     
            readdata.format_time_axis2(self,self.ax2,xlen)        
                  
        if self.interpolate_checkbox.isChecked():
            CS1 = self.ax2.contourf(X_sed,Y_sed, zz, levels = sed_levs,        
                              extend="both", cmap= self.cmap1)                  
        else: 
            CS1 = self.ax2.pcolor(X_sed,Y_sed, zz, #mesh
                                 vmin = sedmin, vmax = sedmax,    
                             cmap= self.cmap1) 
    
        if self.yearlines_checkbox.isChecked()==True and \
           self.datescale_checkbox.isChecked()== False:
            for n in range(start,stop):
                if n%365 == 0: 
                    self.ax2.axvline(n, color='white',
                                      linestyle = '--') 
                         
        if sedmax > self.e_crit_max or sedmax < self.e_crit_min:
            format = mtick.FuncFormatter(fmt)
            #self.gs.update(left = 0.05,right = self.right_gs)
        else: 
            format = None               
        cb_sed = plt.colorbar(CS1,cax = self.cax1,format = format)
        #cb_sed.set_ticks(sed_ticks)   
              
    if self.datescale_checkbox.isChecked() == True:          
        X = readdata.use_num2date(self,self.time_units,X)     
        readdata.format_time_axis2(self,self.ax,xlen)   
                             
    maxmin = readdata.make_maxmin(self,zz,start,stop,index,'water')    
    watmin = maxmin[0]     
    watmax = maxmin[1]
    #ax.set_title(index)
    #wat_ticks = readdata.ticks(watmin,watmax)
        
    self.ax.set_title(index + ', ' + data_units) 
    self.ax.set_ylim(self.y1max,self.ny1min)   
    self.ax.set_ylabel('h, m',fontsize= self.font_txt)
     
    wat_levs = np.linspace(watmin,watmax,num = self.num)
                            
    if self.interpolate_checkbox.isChecked():
        CS = self.ax.contourf(X,Y, zz, 
                         levels = wat_levs, extend="both", 
                              cmap= self.cmap)        
    else:       
        CS = self.ax.pcolormesh(X,Y, zz, vmin = watmin, vmax = watmax,    
                        cmap= self.cmap) 
        

      
    self.ax.set_xlim(np.min(X),np.max(X))
       
    if self.yearlines_checkbox.isChecked()==True  and \
       self.datescale_checkbox.isChecked()== False:
        for n in range(start,stop):
            if n%365 == 0: 
                self.ax.axvline(n, color='white', linestyle = '--')     
                

                 
    #cb = plt.colorbar(CS,self.ax,self.cax,
    #                  pad=0.02,aspect = 4,
    #         format=mtick.FuncFormatter(readdata.fmt)) 
    
    if watmax > 10000 or watmax < 0.001:
        format = mtick.FuncFormatter(fmt)
        #self.gs.update(left = 0.05,right = self.right_gs)        
    else: 
        format = None
          
    cb = plt.colorbar(CS, self.cax, 
                          format = format)
    
    #plt.colorbar(CS,cax = self.cax)   #, ticks = wat_ticks   
    #cb.set_ticks(wat_ticks)


    self.canvas.draw()
