#!/usr/bin/python
# -*- coding: utf-8 -*-
# this ↑ comment is important to have 
# at the very first line 
# to define using unicode 
import numpy.ma as ma
'''
Created on 14. des. 2016

@author: E.Protsenko
'''


from netCDF4 import Dataset,num2date

import main
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import rc
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
import os, sys 
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

majorLocator = mtick.MultipleLocator(2.)
majorFormatter = mtick.ScalarFormatter(useOffset=False)   
#format y scales to be scalar 
minorLocator = mtick.MultipleLocator(1.)
app1 = QtWidgets.QApplication(sys.argv)
screen_rect = app1.desktop().screenGeometry()
width, height = screen_rect.width(), screen_rect.height()

rc('font', **{'sans-serif' : 'Arial', #for unicode text
                'family' : 'sans-serif'})  
      
def readdata_brom(self,fname): #,varname,fname
    
    self.fh = Dataset(fname)
    
    self.time =  self.fh.variables['time'][:]
    self.time_units = self.fh.variables['time'].units
    self.lentime = len(self.time)  
    self.right_gs = 0.8
    self.e_crit_min = 0.02
    self.e_crit_max = 10000 
    self.fh.close()
def read_num_col(self,fname):
    # Read all variables name from the file 
    # And add them to the qlistwidget        
    self.fh = Dataset(fname)    
    self.names_vars = [] 
    for names,vars in self.fh.variables.items():
        self.names_vars.append(names)  
    flux_list = []
    sink_list = []
    other_list = []
   
    for name in self.names_vars: 
        if name[:4] == 'fick':
            flux_list.append(name) 
        elif name[:4] == 'sink':
            sink_list.append(name)
        elif name not in ['z','z2','kz','time','i']:    
            other_list.append(name) 
            
    # sort variables alphabetically non-case sensitive            
    self.sorted_names =  sorted(other_list, key=lambda s: s.lower())  
    self.sorted_names.extend(flux_list) 
    self.sorted_names.extend(sink_list)    
    
    #Read i variable to know number of columns     
    for names,vars in self.fh.variables.items():
        if names == 'z' or names == 'z2' : 
            pass
        elif names == 'time': # or names == 'i' : 
            pass 
        else :
            if 'i' in self.names_vars:
                self.testvar = np.array(self.fh['i'][:]) 
                self.max_num_col = self.testvar.shape[0]     
                break  
       
def readdata2_brom(self,fname):  
    #print ('in readdata_brom')   
    self.fh = Dataset(fname)
    try:
        self.depth = self.fh.variables['z'][:]  
    except KeyError : 
        self.depth = self.fh.variables['depth'][:] 
    if 'Kz_s' in self.names_vars or 'Kz' in self.names_vars:    
        try: 
            self.depth2 = self.fh.variables['z2'][:]    
        except KeyError : 
            self.depth2 = self.fh.variables['depth2'][:]          
        #middle points   
        try: 
            self.kz =  self.fh.variables['Kz'][:,:] 
        except KeyError : 
            self.kz =  self.fh.variables['Kz_s'][:,:]                 
        self.lendepth2 = len(self.depth2)
        # bbl width depends on depth
        if self.lendepth2 < 50 :
            self.bbl = 0.3 #0.5 
        else :
            self.bbl = 0.5         
    self.time =  self.fh.variables['time'][:]
    self.time_units = self.fh.variables['time'].units
    #time_calendar = self.fh.variables['time'].calendar
    #print (time_calendar)
    self.dates = num2date(self.time[:],
                          units= self.time_units)   
                 
    #print (min(self.dates),max(self.dates))
    #time = dates 
    if 'i' in self.names_vars: 
        self.dist = np.array(self.fh.variables['i']) 

 
def read_all_year_var(self,fname,varname1,varname2,varname3): 
    self.fh = Dataset(fname)  
    self.var1 = self.fh.variables[varname1][:]
    self.var2 = self.fh.variables[varname2][:]
    self.var3 = self.fh.variables[varname3][:]  
    return  self.var1,self.var2, self.var3      
    self.fh.close()
         
def colors(self):
    self.spr_aut ='#998970'
    self.wint =  '#8dc0e7'
    self.summ = '#d0576f' 
    self.a_w = 0.4 #alpha_wat alpha (transparency) for winter
    self.a_bbl = 0.3     
    self.a_s = 0.4 #alpha (transparency) for summer
    self.a_aut = 0.4 #alpha (transparency) for autumn and spring    
    self.wat_col = '#c9ecfd' 
 
    self.bbl_col = '#2873b8' 
    self.sed_col= '#916012'
    self.wat_col1 = '#c9ecfd'  
    self.bbl_col1 = '#ccd6de'
    self.sed_col1 = '#a3abb1'
           
    self.font_txt = 15 #(height / 190.)
    # text on figure 2 (Water; BBL, Sed) 
    self.xlabel_fontsize = 10
    #(height / 170.) #14 #axis labels      
    self.ticklabel_fontsize = 10 #(height / 190.) #14 #axis labels   
    self.linewidth = 0.7   
             
def axis_pos(self): # for plot with all var in one page 
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
  
def calculate_ywat(self):
    for n in range(0,(len(self.depth2))):
        if self.depth2[n+1] - self.depth2[n] >= self.bbl:
            if n == self.lendepth2-2: # len(self.depth2):
                y1max = (self.depth2[n]-1)
                self.ny1min = (self.depth[0])
                self.y1max = y1max                                                     
                self.ny1max = n-1
                self.sediment = False
                #print ('no sediment y wat', self.y1max)        
                break  
        elif self.depth2[n+1] - self.depth2[n] < self.bbl:   
            self.y1max = (self.depth[n])                               
            self.ny1max = n #-1
            self.sediment = True
            if self.ny1max == 0 :
                self.y1max = (self.depth[len(self.depth2)-2])
                self.ny1max = len(self.depth2)
                self.sediment = False            
            #print ('calc_y_wat_y1max', self.y1max,self.ny1max)
            break
        
  
def calculate_ybbl(self):
    for n in range(0,(len(self.depth2)-1)):
        try: 
            if self.kz[1,n,0] == 0:
                self.y2max = self.depth2[n]         
                self.ny2max = n  
                #print ('y2max' ,self.y2max)      
                break  
            if self.kz[1,n,0] != 0 and n == (len(self.depth2)-2):       
                self.y2max = self.depth2[n]         
                self.ny2max = n  
                #print ('no sediment' , self.kz[0,n,0],n)   
        except IndexError: 
            if self.kz[1,n] == 0:
                self.y2max = self.depth2[n]         
                self.ny2max = n  
                #print ('y2max' ,self.y2max)      
                break  
            if self.kz[1,n] != 0 and n == (len(self.depth2)-2):       
                self.y2max = self.depth2[n]         
                self.ny2max = n  
                #print ('no sediment' , self.kz[0,n,0],n)                 
def y2max_fill_water(self):
    
    for n in range(0,(len(self.depth2)-1)):
        if self.depth2[n+1] - self.depth2[n] >= self.bbl:
            pass
        elif self.depth2[n+1] - self.depth2[n] < self.bbl:
            self.y2max_fill_water = self.depth2[n] 
            self.nbblmin = n            
            break 
         
def calculate_ysed(self):
    for n in range(0,(len(self.depth_sed))):
        try: 
            if self.kz[1,n,0] == 0:
                ysed = self.depth_sed[n] #0 cm depth             
                self.ysedmin =  ysed - 10
                self.ysedmax =  self.depth_sed[len(self.depth_sed)-1]        
                self.y3min = self.depth_sed[self.nbblmin+2]
                #here we cach part of BBL to add to 
                #the sediment image                
                break  
            else : 
                self.ysedmax =  max(self.depth_sed) 
        except IndexError:                
            if self.kz[1,n] == 0:
                ysed = self.depth_sed[n] #0 cm depth             
                self.ysedmin =  ysed - 10
                self.ysedmax =  self.depth_sed[len(self.depth_sed)-1]        
                self.y3min = self.depth_sed[self.nbblmin+2]                
                break  
            else : 
                self.ysedmax =  max(self.depth_sed)                 
                
            
def calc_nysedmin(self):
    m = 0      
    self.ysedmin = - 10           
    for n in (self.depth_sed):
        if n >= self.ysedmin :
            self.nysedmin = m 
            break
        else: 
            m = m+1
    return self.nysedmin    
 
         
def y_coords(self):       

    #calculate the position of y2min, for catching part of BBL 
    self.ny2min = self.ny2max - 2*(self.ny2max - self.ny1max) 
    self.y2min_fill_bbl = self.y2max_fill_water = self.y1max #y2max_fill_water()
    #109.5 #BBL-water interface
    self.ysedmax_fill_bbl = 0
    self.ysedmin_fill_sed = 0
    self.y1min = 0
    self.y2min = self.y2max - 2*(self.y2max - self.y1max)   
          
    #calculate the position of y2min, for catching part of BBL 

# calc depth in cm from sed/wat interface 
def depth_sed(self):
    to_float = []
    for item in self.depth:
        to_float.append(float(item)) #make a list of floats from tuple 
    depth_sed = [] # list for storing final depth data for sediment 
    v=0  
    for i in to_float:
        v = (i- self.y2max)*100  #convert depth from m to cm
        depth_sed.append(v)
        self.depth_sed = depth_sed
        
    to_float = []
    for item in self.depth2:
        to_float.append(float(item)) #make a list of floats from tuple 
    depth_sed2 = [] # list for storing final depth data for sediment 
    v=0 
     
    for i in to_float:
        v = (i- self.y2max)*100  #convert depth from m to cm
        depth_sed2.append(v)
        self.depth_sed2 = depth_sed2  
        #print ('in depth_sed2') 
                
def MinMaxFunctions(self,start,stop):
    """ dict values are limits for array """    
    return dict(watdist = (start,stop,0,self.ny1max),
                seddist = (start,stop,self.nysedmin,None),
                wattime = (0,self.ny1max,None,None),
                sedtime = (self.nysedmin,None,None,None))      
  
def varmax(self,var,vartype,start,stop): 
    """ dict values are limits for array """
    functions = dict(watdist = (start,stop,0,self.ny1max),
                     seddist = (start,stop,self.nysedmin,None),
                     wattime = (0,self.ny1max,None,None),
                     sedtime = (self.nysedmin,None,None,None))
    #functions = self.MinMaxFunctions(start,stop)
    lims = functions[vartype]
    return ma.max(var[lims[0]:lims[1],lims[2]:lims[3]])     
                                                                                  
def varmin(self,var,vartype,start,stop):
    functions = dict(watdist = (start,stop,0,self.ny1max),
                     seddist = (start,stop,self.nysedmin,None),
                     wattime = (0,self.ny1max,None,None),
                     sedtime = (self.nysedmin,None,None,None))
    #functions = self.MinMaxFunctions(start,stop)
    lims = functions[vartype]            
    return ma.min(var[lims[0]:lims[1],lims[2]:lims[3]]) 

def check_minmax(self,call_min,call_max):
    if call_min == call_max :
        if call_max == 0: 
            call_max = 0.1
            call_min = 0
        else:     
            call_max = call_max + call_max/1000.
            call_min = call_min - call_max/1000. 
            
    return call_min,call_max

# make "beautiful"  values to show on ticks 
def ticks(minv,maxv):    
    if maxv > 1 :
        minv = np.floor(minv)
        minv = (math.trunc(minv/10)*10)
    dif = maxv - minv  
    #maxv = maxv + 100 
    if minv > 100 :
        minv = (math.trunc(minv/100)*100) 
         
    if dif >= 50000. and dif < 150000.  :
        ticks = np.arange(minv,maxv,50000)        
    elif dif >= 10000. and dif < 50000. :
        ticks = np.arange(minv,maxv,5000)        
    elif dif > 3000. and dif < 10000.  : 
        ticks = np.arange(minv,maxv,1000)       
    elif dif > 1500. and dif <= 3000. :
        ticks = np.arange(minv,maxv,500)                         
    elif dif >= 1000. and dif <= 1500. :
        ticks = np.arange(
            (math.trunc(minv/100)*100),
            maxv,200)           
    elif dif >= 300. and dif <= 1000. :
        ticks = np.arange((math.trunc(minv/100)*100),maxv,100)   
        if minv < 100 :
            ticks = np.arange(0,maxv,100)                
    elif dif >= 100. and ( 
     maxv - minv) < 300. :
        ticks = np.arange(minv,maxv,20) #+50. 
    elif dif > 50. and dif < 100. :
        ticks = np.arange(minv,maxv,10) #+10.        
    elif dif > 20. and dif <= 50. :
        ticks = np.arange(minv,maxv,5) #+5.
    elif dif > 10. and dif <= 20. :
        ticks = np.arange(minv,maxv,2) #+1.        
    elif dif > 3. and dif <= 10. :
        ticks = np.arange(minv,maxv,1) #+1.
    elif dif >= 1. and dif <= 3. :
        ticks = np.arange(minv,maxv,0.5) #+1.         
    elif dif > 0.2 and dif <= 1. :
        ticks = np.arange(minv,maxv,0.1) #+1.                  
    elif dif > 0.02 and dif <= 0.2 : 
        ticks = np.arange((math.trunc(minv/10)*10),maxv,0.01) 
    elif dif == 0:
        ticks = np.arange(minv - minv/100.,
                maxv + minv/100.,minv/1000.)
    else : 
        ticks = [minv,maxv]    
        #+ dif/2.                  
    return ticks

def setmaxmin(self,axis,var,type):
    minv = varmin(self,var,type) #0 - water 
    maxv = varmax(self,var,type)
    axis.set_xlim([minv,maxv])  
    axis.set_xticks(np.arange(minv,maxv+((maxv - minv)/2.),
            ((maxv - minv)/2.)))      
        
def set_widget_styles(self):
    
    # Push buttons style
    for axis in (self.time_prof_all,self.time_prof_last_year,
                 self.dist_prof_button,self.fick_box, 
                 self.all_year_button,self.help_button):   
        axis.setStyleSheet(
        'QPushButton {background-color: #c2b4ae; border-width: 5px;'
        '  padding: 2px; font: bold 15px; }')   
          
    self.help_button.setIcon(QtGui.QIcon('help.png'))   
    self.help_button.setIconSize(QtCore.QSize(30,30))   
    # set zero border.
    self.help_button.setStyleSheet('QPushButton{border: 0px solid;}')
         
    self.qlistwidget.setStyleSheet(
    'QListWidget{font: 25 px; background-color: #eadfda;  }')
     
    self.label_choose_var.setStyleSheet(
        'QLabel {border-width: 7px;'
        '  padding: 7px; font: bold 15px; }')        
    

def widget_layout(self): 
       
        #first line 
        
        self.grid.addWidget(self.help_button,0,0,1,1) # help_dialog           
        self.grid.addWidget(self.toolbar,0,1,1,1) 
        self.grid.addWidget(self.fick_box,0,2,1,1)         
        self.grid.addWidget(self.time_prof_all,0,3,1,1)  
        self.grid.addWidget(self.cmap_groupBox,0,4,2,1) 
        self.grid.addWidget(self.dist_groupBox,0,5,2,1)        
        self.grid.addWidget(self.time_groupBox,0,6,2,1)                      
        self.grid.addWidget(self.options_groupBox,0,7,2,1)  
        
        #second line                        
        self.grid.addWidget(self.time_prof_last_year,1,2,1,1) 
        #self.grid.addWidget(self.all_year_1d_box,1,2,1,1)         
        self.grid.addWidget(self.all_year_button,1,1,1,1)    
        self.grid.addWidget(self.dist_prof_button,1,3,1,1)         
        #self.grid.addWidget(self.yearlines_checkbox,1,7,1,1)          
        #self.grid.addWidget(self.textbox2,1,6,1,1)  
 
        #third line              
        self.grid.addWidget(self.canvas, 2, 1,1,8)     
        self.grid.addWidget(self.qlistwidget,2,0,2,1) 
        self.grid.addWidget(self.label_choose_var,1,0,1,1)  
  
def cmap_list(self):
    self.cmap_list = ['jet','inferno','rainbow','viridis','plasma','Paired']
    return self.cmap_list    

def use_num2date(self,time_units,X_subplot):   
    X_subplot = num2date(X_subplot,
                            units = time_units) 
    return X_subplot

def format_time_axis2(self, xaxis,xlen):   
    if xlen > 365 and xlen < 365*5 :
        xaxis.xaxis_date()
        xaxis.xaxis.set_major_formatter(
            mdates.DateFormatter('%m/%Y'))  
    elif xlen >= 365*5 :
        xaxis.xaxis_date()
        xaxis.xaxis.set_major_formatter(
            mdates.DateFormatter('%Y'))          
    elif xlen <= 365: 
        xaxis.xaxis_date()
        xaxis.xaxis.set_major_formatter(
            mdates.DateFormatter('%b'))   

def plot_inj_lines(self,numday,col,axis):
    axis.axvline(numday,color= col, linewidth = 2,
                   linestyle = '--',zorder = 10) 


def grid_plot(self,numplots):
    if numplots == 1:
        self.gs = gridspec.GridSpec(1, 1) 
        self.gs.update(left = 0.07,right = 0.85)
        self.cax = self.figure.add_axes([0.9, 0.1, 0.02, 0.8])        
        self.ax = self.figure.add_subplot(self.gs[0])  
             
    if numplots == 2: 
        self.gs = gridspec.GridSpec(2, 1) 
        self.gs.update(left = 0.07,right = 0.85 )
        self.cax1 = self.figure.add_axes([0.86, 0.11, 0.02, 0.35])
        self.cax = self.figure.add_axes([0.86, 0.53, 0.02, 0.35])    
        self.ax = self.figure.add_subplot(self.gs[0])
        self.ax2 = self.figure.add_subplot(self.gs[1])       

def get_cmap(self):    
    try:
        # take values of cmaps from comboboxes 
        cmap_name = self.cmap_water_box.currentText()
        cmap1_name = self.cmap_sed_box.currentText()
        self.cmap = plt.get_cmap(cmap_name) 
        self.cmap1 = plt.get_cmap(cmap1_name) 
    except ValueError:
        self.cmap = plt.get_cmap('jet')
        self.cmap1 = plt.get_cmap('gist_rainbow')    
        
        
def make_maxmin(self,var,start,stop,index,type):
    if  self.change_limits_checkbox.isChecked():
        if type == 'water_time' or type == 'water_dist':
            min = float(self.box_minwater.text())
            max= float(self.box_maxwater.text()) 
            maxmin = (min,max)
        if type == 'sed_time' or type == 'sed_dist' :          
            min = float(self.box_minsed.text())
            max = float(self.box_maxsed.text())
            maxmin = (min,max)
            
    elif type == 'water_time': 
        maxmin = calculate_wat_maxmin(
            self,var,start,stop,index)
    elif type == 'water_dist': 
        #round(data[start:stop,0:self.ny1max].min(),2) 
        min = varmin(self,var,'watdist',start,stop)
        max = varmax(self,var,'watdist',start,stop) 
        check = check_minmax(self,min,max)
        min = check[0]
        max = check[1]
        maxmin = (min,max)     
               
    elif type == 'sed_time': 
        maxmin = calculate_sed_maxmin(
            self,var,start,stop,index)  
    elif type == 'sed_dist':
        min = varmin(self,var,'seddist',start,stop)
        max = varmax(self,var,'seddist',start,stop)
        check = check_minmax(self,min,max)
        min = check[0]
        max = check[1]                
        maxmin = (min,max)     
    return maxmin
        
def calculate_wat_maxmin(self,var,start,stop,index):        
    zz = var
    if self.scale_all_axes.isChecked(): 
        z_all_columns = np.array(self.fh.variables[index])  
        watmin = round((
            z_all_columns[start:stop,0:self.ny1max,:].min()),0) 
        watmax = round((
            z_all_columns[start:stop,0:self.ny1max,:].max()),2)                         
    elif 'Kz' in self.names_vars and index != 'pH':
        watmin = varmin(self,zz,'wattime',start,stop) 
        watmax = varmax(self,zz,'wattime',start,stop)     
        
    elif 'Kz'in self.names_vars and index == 'pH':       
        # take the value with two decimal places 
        watmin = round(zz[0:self.ny1max,:].min(),2) 
        watmax = round(zz[0:self.ny1max,:].max(),2) 
         
    # if we do not have kz     
    else:  
        self.ny1max = len(self.depth-1)
        self.y1max = max(self.depth)    
        watmin = varmin(self,zz,'wattime',start,stop) 
        watmax = varmax(self,zz,'wattime',start,stop)
    
    check = check_minmax(self,watmin,watmax)
    watmin = check[0]
    watmax = check[1]   
    
    return watmin,watmax 

def calculate_sed_maxmin(self,var,start,stop,index):     
    zz = var  
    if self.scale_all_axes.isChecked(): 
        z_all_columns = np.array(self.fh.variables[index])  
        sed_min  = round((
                z_all_columns[start:stop,self.nysedmin-2:,:].min()),2) 
        sed_max = round((
                z_all_columns[start:stop,self.nysedmin-2:,:].max()),2)                  
    elif index == 'pH': 
        sed_min  = (zz[self.nysedmin-2:,:].min()) 
        sed_max  = (zz[self.nysedmin-2:,:].max())                 
        #sed_ticks = readdata.ticks(sed_min,sed_max) 
        #sed_ticks = (np.floor(sed_ticks*100)/100.)  
    else :
        sed_min = varmin(self,zz,'sedtime',start,stop)
        sed_max = varmax(self,zz,'sedtime',start,stop) 
        
    check = check_minmax(self,sed_min,sed_max)
    sedmin = check[0]
    sedmax = check[1]   
    
    return sedmin,sedmax 

## here we can add contour of some level with interesting value
#add contour to 1 om ar saturation
#ax.contour(X, Y,air,levels = [100],
#     colors=('k',),linestyles=('--',),linewidths=(3,))        
#ax.contour(X, Y,zz,levels = [1],
#         colors=('k',),linestyles=('--',),linewidths=(3,))           #if self.injlines_checkbox.isChecked()== True:       
#    readdata.plot_inj_lines(self,100,'r',ax2) #to change   

#    ax2.axvline(730,color='red',linewidth = 2,
#            linestyle = '--',zorder = 10)  

             