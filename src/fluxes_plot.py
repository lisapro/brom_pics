#!/usr/bin/python
# -*- coding: utf-8 -*-
# this ↑ comment is important to have 
# at the very first line 
# to define using unicode 

'''
Created on 30. jun. 2017

@author: ELP
'''
import matplotlib.pyplot as plt
from PyQt5 import QtGui,QtWidgets
import numpy as np
import readdata
import matplotlib.gridspec as gridspec
from netCDF4 import Dataset 

def fluxes(self,start,stop): 
    plt.clf()     
    try:
        index = str(self.qlistwidget.currentItem().text())
    except AttributeError:       
        messagebox = QtWidgets.QMessageBox.about(
            self, "Retry",'Choose variable,please') 
        return None 
              
    numcol = self.numcol_2d.value() # 
    fh =  Dataset(self.fname)      
    selected_items = self.qlistwidget.selectedItems()
    
    tosed = '#d3b886'
    towater = "#c9ecfd" 
    linecolor = "#1da181" 
    var1 = str(selected_items[0].text())
   
    z = np.array(fh.variables[var1])
    z_units = fh.variables[var1].units
    
    zz =  z[:,:,numcol] #1column
    X = np.array(self.time[start:stop])
    
    if len(selected_items)== 1:
        
        gs = gridspec.GridSpec(1,1)
        ax00 = self.figure.add_subplot(gs[0]) 
        if self.yearlines_checkbox.isChecked() == True:
            for n in range(start,stop):
                if n%365 == 0: 
                    ax00.axvline(n, 
                                 color='black',
                    linestyle = '--') 
                                           
    elif len(selected_items)== 2:
        gs = gridspec.GridSpec(2,1)
        
        ax00 = self.figure.add_subplot(gs[0])
        ax01 = self.figure.add_subplot(gs[1])
        
          
        if self.yearlines_checkbox.isChecked() == True:
            for n in range(start,stop):
                if n%365 == 0: 
                    ax00.axvline(n,color='black',
                    linestyle = '--') 
                    ax01.axvline(n,color='black',
                    linestyle = '--') 

                                                                   
        var2 = str(selected_items[1].text())
        z2_units = fh.variables[var2].units
        z2 = np.array(fh.variables[str(selected_items[1].text())])
        zz2 =  z2[:,:,numcol] #1column
        ax01.set_title(var2+', '+ z2_units)
        ax01.set_ylabel('Fluxes') #Label y axis
        ax01.set_xlim(start,stop)
        ax01.axhline(0, color='black', linestyle = '--') 
 
        fick2 = np.array([zz2[n][self.nysedmin] for n in range(start,stop)])  
        ax01.plot(X,fick2, linewidth = 1 ,
                    color = linecolor, zorder = 10)  

        ax01.fill_between(X, fick2, 0,
                           where= fick2 >= 0. , 
                           color = tosed, label= u"down" )
        ax01.fill_between(X,  fick2, 0 ,
                      where= fick2 < 0.,color = towater, label=u"up")            
        ax01.set_ylim(max(fick2),min(fick2)) 
        #m = np.mean(fick2)
        #ax01.axhline(m,c = 'r', linestyle = '--',label = 'mean')
    else : 
        messagebox = QtWidgets.QMessageBox.about(
            self, "Retry",'Choose 1 or 2 variables,please') 
        return None  
    
    
    ax00.set_title(var1+', '+ z_units )        
    ax00.set_ylabel('Fluxes') #Label y axis
    
    # take values for fluxes at sed-vat interf        
    fick = np.array([zz[n][self.nysedmin] for n in range(start,stop)])                 
    ax00.axhline(0, color='black', linestyle = '--') #Line at SWI

    if self.datescale_checkbox.isChecked() == True:          
        X = readdata.use_num2date(self,self.time_units,X) 
        readdata.format_time_axis2(self,ax00,len(X))         
    else: 
        ax00.set_xlabel('Julian day')  
        
    ax00.set_xlim(X[0],X[-1:])    
    ax00.plot(X,fick, linewidth = 1 ,color = linecolor, zorder = 10)  
    
    ax00.fill_between(X,fick,0, where = fick >=0,
                      color = tosed, label= u"down" )
    ax00.fill_between(X,fick,0, where= fick < 0,
                      color = towater, label=u"up")
    
    if self.manual_limits_flux.isChecked():
        min_fick = float(self.flux_min_box.text())
        max_fick = float(self.flux_max_box.text())
    else: 
        min_fick = min(fick)
        max_fick = max(fick)
        
    if self.reverse_flux_checkbox.isChecked() == True:
        ax00.set_ylim(min_fick,max_fick)
    else:        
        ax00.set_ylim(max_fick,min_fick) 

    fh.close()
    self.canvas.draw()
        
 
    '''
        #self.figure.suptitle(str(self.totitle),fontsize=16)
        #                , fontweight='bold')    
    
    
        #m = np.mean(fick)
        #ax00.axhline(m,c = 'r', linestyle = '--',label = 'mean', zorder = 10)
        #print(X)    
        # injection      
    
            #if self.yearlines_checkbox.isChecked() == True:
            #    for n in range(start,stop):
            #        if n%365 == 0: 
            #            ax01.axvline(n,
            #            color='black', linestyle = '--')          
    
    if self.injlines_checkbox.isChecked()== True: 
            ax00.axvline(365,color='red', linewidth = 2,
                    linestyle = '--',zorder = 10) 
            ax00.axvline(730,color='red',linewidth = 2,#1825 730
                    linestyle = '--',zorder = 10)  
              
            ax01.axvline(365,color='red', linewidth = 2,
                    linestyle = '--',zorder = 10) 
            ax01.axvline(730,color='red',linewidth = 2,
                    linestyle = '--',zorder = 10)   ''' 
          