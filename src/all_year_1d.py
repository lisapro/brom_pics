#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 30. jun. 2017

@author: Elizaveta Protsenko
'''

from netCDF4 import Dataset 
import matplotlib.pyplot as plt
from PyQt5 import QtGui,QtWidgets
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter
import readdata

def plot(self,start,stop): 
               
    plt.clf() 
    self.figure.patch.set_facecolor('white')  
         
    try:
        index = str(self.qlistwidget.currentItem().text())
    except AttributeError: 
        print ("Choose the variable to print ")       
        messagebox = QtWidgets.QMessageBox.about(self, "Retry",
                                             'Choose variable,please') 
        return None 
    self.fh =  Dataset(self.fname)    
    
    gs = gridspec.GridSpec(3,1) 
    gs.update(left=0.3, right=0.7,top = 0.94,bottom = 0.04,
               wspace=0.2,hspace=0.3) 
    
    self.ax00 = self.figure.add_subplot(gs[0])     
    self.ax10 = self.figure.add_subplot(gs[1]) 
    self.ax20 = self.figure.add_subplot(gs[2])  
    
    for axis in (self.ax00,self.ax10,self.ax20):
        axis.yaxis.grid(True,'minor')
        axis.xaxis.grid(True,'major')                
        axis.yaxis.grid(True,'major')    
                         
    # read chosen variable 
    numcol = self.numcol_2d.value()
    z = np.array(self.fh.variables[index][:,:,numcol])

    data_units = self.fh.variables[index].units 
    self.ax00.set_title(index +', ' + data_units) 

    self.ax10.yaxis.set_major_formatter(
        ScalarFormatter(useOffset=False))
        
    def add_colr_lims(axis,bot,top,col,lims = True,text = 'h, m'):
        axis.axhspan(bot,top,color = col)
        if lims == True:
            axis.set_ylabel(text,fontsize= self.font_txt)   
            axis.set_ylim(bot,top)
        else: 
            pass
        
    add_colr_lims(self.ax00,self.y1max,0,self.wat_col)
    add_colr_lims(self.ax10,self.y2max,self.y1max,self.wat_col)     
    add_colr_lims(self.ax20,self.ysedmax,
                  self.ysedmin,self.sed_col,text ='h, cm')      
    add_colr_lims(self.ax20,self.ysedmin,0,self.wat_col,lims = False)
         
    
    if  self.change_limits.isChecked():
        functions = dict(wat = (self.box_minw,
                                self.box_maxw),
                         sed = (self.box_minsed,
                                self.box_maxsed))
        
        watmin = float(functions['wat'][0].text())
        watmax = float(functions['wat'][1].text())               
        sedmin = float(functions['sed'][0].text())
        sedmax = float(functions['sed'][1].text())
        
        self.ax00.set_xlim(watmin,watmax)      
        self.ax10.set_xlim(watmin,watmax)       
        self.ax20.set_xlim(sedmin,sedmax)   
        
    if (stop - start) > 365:
        step  = 10 
    else: 
        step = 2      
    for n in range(start,stop,step):

        self.ax00.plot(z[n][0:self.ny2max],
              self.depth[0:self.ny2max],
              self.spr_aut,alpha = self.a_w, 
              linewidth = self.linewidth , zorder = 8) 

        self.ax10.plot(z[n][0:self.ny2max],
              self.depth[0:self.ny2max],
              self.spr_aut,alpha = self.a_w, 
              linewidth = self.linewidth , zorder = 8) 
    
        self.ax20.plot(z[n][self.nysedmin-1:],
              self.depth_sed[self.nysedmin-1:],
              self.spr_aut, alpha = self.a_w,
              linewidth = self.linewidth, zorder = 8)                          

    self.fh.close()                  
    self.canvas.draw()     
