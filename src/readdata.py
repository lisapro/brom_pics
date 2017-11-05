#!/usr/bin/python
# -*- coding: utf-8 -*-
# this ↑ comment is important to have 
# at the very first line 
# to define using unicode 
'''
Created on 14. des. 2016

@author: E.Protsenko
'''


from netCDF4 import Dataset,num2date

import main
import numpy as np
import numpy.ma as ma
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import rc
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
import os, sys 
import matplotlib.dates as mdates

#getcontext().prec = 6 
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
    self.depth = self.fh.variables['z'][:]  
    
    if 'kz' in self.names_vars or 'Kz' in self.names_vars:    
        self.depth2 = self.fh.variables['z2'][:] 
        #middle points   
        self.kz =  self.fh.variables['Kz'][:,:] 
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
    
    '''    
    #define color maps 
    try:
        cmap_name = self.cmap_water_box.currentText()
        cmap1_name = self.cmap_water_box.currentText()
        #plt.cm.varidis #jet #gnuplot#jet#gist_rainbow
        self.cmap = plt.get_cmap(cmap_name) 
        self.cmap1 = plt.get_cmap(cmap1_name) 
    except ValueError:
        self.cmap = plt.get_cmap('jet')
        self.cmap1 = plt.get_cmap('gist_rainbow')'''
        
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
        
        if self.kz[1,n,0] == 0:
            self.y2max = self.depth2[n]         
            self.ny2max = n  
            #print ('y2max' ,self.y2max)      
            break  
        if self.kz[1,n,0] != 0 and n == (len(self.depth2)-2):       
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
         
def varmax(self,variable,vartype,start,stop): 
    if vartype == 'watdist': #water
        n = variable[start:stop,0:self.ny1max].max() 

    elif vartype == 'seddist' :#sediment dist 
        n = variable[start:stop,self.nysedmin:].max()
  
    elif vartype == 'wattime': #time plot water
        n = ma.max(variable[0:self.ny1max,:]) #.max()
      
    elif vartype == 'sedtime' : #time plot sediment
        n = variable[self.nysedmin-2:,:].max()

                                                                                         
    self.watmax =  n   
    return self.watmax

# make "beautiful"  values to show on ticks  
def int_value(self,n,minv,maxv):
    num = self.num
         
    if (maxv - minv) >= num*10. and ( 
     maxv - minv) < num*100. :
        m = math.ceil(n/10)*10.
    elif ( maxv -  minv) >= num and (
         maxv -  minv) < 10.*num :
        m = math.ceil(n)        
    elif ( maxv -  minv) > num/10. and (
         maxv -  minv) < num :
        m = (math.ceil(n*10.))/10.        
    elif ( maxv -  minv) > num/100. and (
         maxv -  minv) < num/10. :
        m = (math.ceil(n*100.))/100.          
    elif ( maxv -  minv) > num/1000. and (
         maxv -  minv) < num/100. :
        m = (math.ceil(n*1000.))/1000.                      
    else :
        m = n  
          
    return m    

def varmin(self,variable,vartype,start,stop):
    
    if vartype == 'watdist': #dist plot water
        n = np.floor(variable[start:stop,0:self.ny1max].min())        
    elif vartype == 'seddist' :  #dist plot sediment
        n = np.floor(variable[start:stop,self.nysedmin:].min())        
    elif vartype == 'wattime' : #time plot water
        n = (ma.min(variable[0:self.ny1max,start:stop]))         
    elif vartype == 'sedtime'  : #time plot sediment
        n = np.floor(variable[self.nysedmin-2:,start:stop].min()) 
    '''            
    # make "beautiful"  values to show on ticks
    ##print ('varmin', n)            
    if n > 10000. and n <= 100000.:  
        n = int(np.floor(n/ 1000.0)) * 1000 - 1000.
    elif n > 1000. and n <= 10000.:  
        n = int(np.floor(n / 100.0)) * 100  #- 20.                                 
    elif n >= 100. and n < 1000.:
        n = int(np.floor(float(n) / 10.0)) * 10 - 1.
    elif n >= 1. and n < 100. :
        n =  int(np.floor(float(n)))  - 1.  
    elif n >= 0.1 and n < 1. :
        n =  (np.floor(n*10.))/10. - 0.1  
    elif n >= 0.01 and n < 0.1 :
        n =  (np.floor(n*100.))/100. 
    elif n >= 0.001 and n < 0.01 :
        n =  (np.floor(n*1000.))/1000.
    elif n >= 0.0001 and n < 0.001 :
        n =  (np.floor(n*10000))/10000 -  0.0001   
    elif n >= 0.00001 and n < 0.0001 :
        n =  (np.floor(n*100000))/100000 '''
  
    self.watmin =  n  
                 
    return self.watmin

# make "beautiful"  values to show on ticks 
def ticks(minv,maxv):    
        
    if (maxv - minv) >= 50000. and (
         maxv - minv) < 150000.  :
        ticks = np.arange(minv,maxv,50000) #+10000.        
    elif (maxv - minv) >= 10000. and (
         maxv - minv) < 50000.  :
        ticks = np.arange(minv,maxv,5000) #+5000.        
    elif (maxv - minv) > 3000. and (
       maxv - minv) < 10000.  : 
        ticks = np.arange(minv,maxv,1000) #+1000.        
    elif (maxv - minv) > 1500. and ( 
     maxv - minv) <= 3000. :
        #print('in 1500-3000')
        ticks = np.arange(minv,maxv,500) #+500.                        
    elif (maxv - minv) >= 1000. and ( 
     maxv - minv) <= 1500. :
        #print('in 1000-1500',maxv-minv)
        ticks = np.arange((math.trunc(minv/10)*10),maxv,200)           
    elif (maxv - minv) >= 300. and ( 
     maxv - minv) <= 1000. :
        #print('in 300-1000',maxv-minv)
        ticks = np.arange((math.trunc(minv/10)*10),maxv,100)   
        if minv < 100 :
            ticks = np.arange(0,maxv,100)   #+100.               
    elif (maxv - minv) >= 100. and ( 
     maxv - minv) < 300. :
        ticks = np.arange(minv-10,maxv,50) #+50. 
    elif (maxv - minv) > 50. and ( 
     maxv - minv) < 100. :
        ticks = np.arange(minv,maxv,10) #+10.        
    elif (maxv - minv) > 20. and ( 
     maxv - minv) <= 50. :
        ticks = np.arange(minv,maxv,5) #+5.
    elif (maxv - minv) > 3. and ( 
     maxv - minv) <= 20. :
        ticks = np.arange(minv,maxv,1) #+1.
    elif (maxv - minv) >= 1. and ( 
     maxv - minv) <= 3. :
        ticks = np.arange(minv,maxv,0.5) #+1.         
    elif (maxv - minv) > 0.2 and ( 
     maxv - minv) <= 1. :
        ticks = np.arange(minv,maxv,0.1) #+1.                  
    elif (maxv - minv) > 0.02 and ( 
     maxv - minv) <= 0.2 : 
        ticks = np.arange((math.trunc(minv/10)*10),maxv,0.01) 
    else : 
        ticks = [minv,maxv]    
        #+ (maxv - minv)/2.                  

    return ticks
    #print (ticks)
#function to define y limits 
# 
'''
def y_lim(self,axis): 
    if axis in (self.ax00,self.ax10,self.ax20):   #water          
        axis.fill_between(self.xticks, self.y1max, self.y1min,
                          facecolor= self.wat_col, alpha=self.a_w)  
    elif axis in (self.ax01,self.ax11,self.ax21):  #BBL
        axis.fill_between(self.xticks, self.y2max, self.y2min_fill_bbl,
                           facecolor= self.bbl_col, alpha=self.a_bbl)
        #plt.setp(axis.get_xticklabels(), visible=False)                                           
    elif axis in (self.ax02,self.ax12,self.ax22): #sediment 
        axis.fill_between(self.xticks, self.ysedmax_fill_bbl,
                           self.ysedmin, facecolor= self.bbl_col, alpha=self.a_bbl)  
        axis.fill_between(self.xticks, self.ysedmax, self.ysedmin_fill_sed,
                           facecolor= self.sed_col, alpha=self.a_sed)    
'''

#function to define y limits  
def y_lim1(self,axis): 
    self.xticks =(np.arange(0,100000))
    if axis in (self.ax00,self.ax10,self.ax20,
                self.ax30,self.ax40,self.ax50): #water
        axis.set_ylim([self.y2min, 0])
        axis.yaxis.grid(True,'minor')
        axis.xaxis.grid(True,'major')                
        axis.yaxis.grid(True,'major') 

    elif axis in (self.ax01,self.ax11,self.ax21,
                  self.ax31,self.ax41,self.ax51): #BBL
        axis.set_ylim([self.y2max, self.y2min])
        axis.fill_between(self.xticks, self.y2max,
            self.y2min_fill_bbl,facecolor= self.bbl_col, 
            alpha=self.a_bbl)
        axis.yaxis.grid(True,'minor')
        axis.yaxis.grid(True,'major')   
        axis.xaxis.grid(True,'major')  
          
        # Set a property to on an artist object.
        # remove xticklabels          
        plt.setp(axis.get_xticklabels(), visible=False) 
        
    elif axis in (self.ax02,self.ax12,
            self.ax22,self.ax32,self.ax42,self.ax52): #sediment 
        axis.set_ylim([self.ysedmax, self.ysedmin]) 
        axis.fill_between(self.xticks, self.ysedmax_fill_bbl,
                          self.ysedmin,facecolor= self.bbl_col,
                          alpha=self.a_bbl)  
        axis.fill_between(self.xticks, self.ysedmax,
                          self.ysedmin_fill_sed,
                          facecolor= self.sed_col,
                          alpha=self.a_s)    
        axis.yaxis.set_major_locator(majorLocator)
        
        #define yticks
        axis.yaxis.set_major_formatter(majorFormatter)
        axis.yaxis.set_minor_locator(minorLocator)
        axis.yaxis.grid(True,'minor')
        axis.yaxis.grid(True,'major')
        axis.xaxis.grid(True,'major')      
                
def setmaxmin(self,axis,var,type):
    minv = varmin(self,var,type) #0 - water 
    maxv = varmax(self,var,type)
    axis.set_xlim([minv,maxv])  
    #tick = ticks(watmin,watmax)
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
          
    self.help_button.setIcon(QtGui.QIcon('hepl.png'))   
    self.help_button.setIconSize(QtCore.QSize(30,30))   
    # set zero border.
    self.help_button.setStyleSheet('QPushButton{border: 0px solid;}')
    
    
    # Combo boxes style
    #for axis in (self.time_prof_box): #,self.all_year_1d_box
    #self.time_prof_box.setStyleSheet(
    #    'QComboBox {background-color: #c2b4ae; border-width: 7px;'
    #    '  padding: 7px; font: bold 14px; }')  
        
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

        #self.grid.addWidget(self.yearlines_checkbox,1,7,1,1)          
        #self.grid.addWidget(self.textbox2,1,6,1,1)  
 
        #third line              
        self.grid.addWidget(self.canvas, 2, 1,1,8)     
        self.grid.addWidget(self.qlistwidget,2,0,2,1) 
        self.grid.addWidget(self.label_choose_var,1,0,1,1)  
  
def cmap_list(self):
    self.cmap_list = ['jet','inferno','rainbow','viridis','plasma','Paired']
    return self.cmap_list    

def use_num2date(self, xaxis,xlen,time_units,X_subplot):   
    X_subplot = num2date(X_subplot,
                            units = time_units) 

    return X_subplot

def format_time_axis2(self, xaxis,xlen,time_units,X_subplot):   
    if xlen > 365:
        xaxis.xaxis_date()
        xaxis.xaxis.set_major_formatter(
            mdates.DateFormatter('%m/%Y'))  
    else : 
        xaxis.xaxis_date()
        xaxis.xaxis.set_major_formatter(
            mdates.DateFormatter('%b'))   



def format_time_axis(self, xaxis,xlen,time_units,X_subplot):   
    #self.format_time = num2date(X_subplot,
    #                        units = time_units)  
    X_subplot = num2date(X_subplot,
                            units = time_units) 
    # self.format_time       

    #if self.datescale_checkbox.isChecked() == True: 
    if xlen > 365:
        xaxis.xaxis_date()
        xaxis.xaxis.set_major_formatter(
            mdates.DateFormatter('%m/%Y'))  
    else : 
        xaxis.xaxis_date()
        xaxis.xaxis.set_major_formatter(
            mdates.DateFormatter('%b'))   
    return X_subplot