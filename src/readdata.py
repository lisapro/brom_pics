#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 14. des. 2016

@author: Elizaveta Protsenko
'''

from netCDF4 import Dataset,num2date
import main,math, os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import rc
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets 
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import numpy.ma as ma
import itertools
from messages import Messages
#format scales to be scalar 
majorLocator = mtick.MultipleLocator(2.)
majorFormatter = mtick.ScalarFormatter(useOffset=False)   
minorLocator = mtick.MultipleLocator(1.)
app1 = QtWidgets.QApplication(sys.argv)
screen_rect = app1.desktop().screenGeometry()
width, height = screen_rect.width(), screen_rect.height()

rc('font', **{'sans-serif' : 'Arial', #for unicode text
                'family' : 'sans-serif'})  
      
def readdata_brom(self,fname): 
    
    self.fh = Dataset(fname)    
    self.time =  self.fh.variables['time'][:]
    self.time_units = self.fh.variables['time'].units
    self.lentime = len(self.time)  
    self.right_gs = 0.8
    self.e_crit_min = 0.02
    self.e_crit_max = 10000 
    self.num = 50. 
    self.fh.close()
    
def read_num_col(self,fname):
    # Read all variables name from the file 
    # And add them to the qlistwidget        
    fh = Dataset(fname)        
    self.names_vars = [n for n,v in fh.variables.items()] 
        
    flux_l,sink_l,other_l  = [],[],[]
    for name in self.names_vars: 
        if name[:4] == 'fick':
            flux_l.append(name) 
        elif name[:4] == 'sink':
            sink_l.append(name)
        elif name not in ['z','z2','kz','time','i']:    
            other_l.append(name) 
               
    # sort variables alphabetically non-case sensitive            
    self.sorted_names =  sorted(other_l, key=lambda s: s.lower()) 
    self.sorted_names  = list(itertools.chain(self.sorted_names,
                 flux_l,sink_l))
     
    #Read i variable to know number of columns     
    for names,vars in fh.variables.items():
        if names not in ['z','z2','time'] and 'i' in self.names_vars: 
            self.testvar = np.array(fh['i'][:]) 
            self.max_num_col = self.testvar.shape[0]     
            break  
    fh.close()  
    
def readdata2_brom(self,fname):  
  
    fh = Dataset(fname)
    try:
        self.depth = fh.variables['z'][:]  
    except KeyError : 
        self.depth = fh.variables['depth'][:] 
    if 'Kz_s' in self.names_vars or 'Kz' in self.names_vars:    
        try: 
            self.depth2 = fh.variables['z2'][:]    
        except KeyError : 
            self.depth2 = fh.variables['depth2'][:]          
        #middle points   
        try: 
            self.kz =  fh.variables['Kz'][:,:] 
        except KeyError : 
            self.kz =  fh.variables['Kz_s'][:,:]                 
        self.lendepth2 = len(self.depth2)
        # bbl width depends on depth
        if self.lendepth2 < 50 :
            self.bbl = 0.3 
        else :
            self.bbl = 0.5         
    self.time =  fh.variables['time'][:]
    self.time_units = fh.variables['time'].units
    self.dates = num2date(self.time[:],
                          units= self.time_units)   
                 
    if 'i' in self.names_vars: 
        self.dist = np.array(fh.variables['i']) 
    fh.close()
          
def colors(self):
    self.spr_aut ='#998970'
    self.wint =  '#8dc0e7'
    self.summ = '#d0576f' 
    self.a_w = 0.7
    self.a_bbl = 0.3     
    self.a_s = 0.4 
    self.a_aut = 0.4      
    self.wat_col = '#eef9fe' #c5d8e3' #'#d9e4e9' #
    self.bbl_col = '#2873b8'  
    self.sed_col=  '#CFB997' #'#916012'
    self.wat_col1 = '#c9ecfd'  
    self.bbl_col1 = '#ccd6de'
    self.sed_col1 = '#a3abb1'
           
    self.font_txt = 15

    # text on figure 2 (Water; BBL, Sed) 
    self.xlabel_fontsize = 10  
    self.ticklabel_fontsize = 10
    self.linewidth = 0.7   
             
def calculate_ywat(self):
    ld2 = self.lendepth2
    for n in range(0,ld2):
        dif = self.depth2[n+1] - self.depth2[n]
        if dif >= self.bbl and n == ld2-2:
            self.y1max = self.depth2[n]-1
            self.ny1min = self.depth[0]                                                  
            self.ny1max = n-1
            self.sediment = False   
            break
         
        elif dif < self.bbl:   
            self.y1max = (self.depth[n])                               
            self.ny1max = n 
            self.sediment = True
            if self.ny1max == 0 :
                self.y1max = (self.depth[-2])
                self.ny1max = ld2
                self.sediment = False            
            break
         
def calculate_ybbl(self):
    ld2 = self.lendepth2
    for n in range(0,(len(self.depth2)-1)):
        try: 
            if self.kz[1,n,0] == 0:
                self.y2max = self.depth2[n]         
                self.ny2max = n     
                break  
            if self.kz[1,n,0] != 0 and n == ld2-2:       
                self.y2max = self.depth2[n]         
                self.ny2max = n   
        except IndexError: 
            if self.kz[1,n] == 0:
                self.y2max = self.depth2[n]         
                self.ny2max = n  
                break  
            if self.kz[1,n] != 0 and n == ld2-2:       
                self.y2max = self.depth2[n]         
                self.ny2max = n  

def y2max_fill_water(self):
    for n in range(0,self.lendepth2-1):
        dif = self.depth2[n+1] - self.depth2[n]
        if dif >= self.bbl:
            pass
        elif dif < self.bbl:
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
                #here we catch part of BBL to add to 
                #the sediment image                
                break  
            else : 
                self.ysedmax =  max(self.depth_sed) 
        except IndexError:                
            if self.kz[1,n] == 0:
                ysed = self.depth_sed[n] #0 cm depth             
                self.ysedmin =  ysed - 10
                self.ysedmax =  self.depth_sed[-1]        
                self.y3min = self.depth_sed[self.nbblmin+2]                
                break  
            else : 
                self.ysedmax =  max(self.depth_sed)                 
                
            
def calc_nysedmin(self):    
    self.ysedmin = - 10           
    for m,n in enumerate(self.depth_sed,start = 0):
        if n >= self.ysedmin :
            self.nysedmin = m 
            break
        else: 
            pass
    return self.nysedmin    
 
         
def y_coords(self):       

    #calculate the position of y2min, for catching part of BBL 
    self.ny2min = self.ny2max - 2*(self.ny2max - self.ny1max) 
    self.y2min_fill_bbl = self.y2max_fill_water = self.y1max
    self.ysedmax_fill_bbl = 0
    self.ysedmin_fill_sed = 0
    self.y1min = 0 
    self.y2min = self.y2max - 2*(self.y2max - self.y1max)   

# calc depth in cm from sed/wat interface 
def depth_sed(self):
    self.depth_sed =  [(i- self.y2max)*100 for i in self.depth.tolist()]
    self.depth_sed2 = [(i- self.y2max)*100 for i in self.depth2.tolist()]

def ticks_2(minv,maxv):  
    ''' make "beautiful" values to show on ticks '''  
    minv = float(minv)
    maxv = float(maxv)
    assert minv < maxv       
    dif = maxv - minv 
    step_raw = dif/4  
    if dif >= 1000:
        step = math.trunc(step_raw*100)/100
        start_tick = (math.trunc((minv)/100)*100)
    elif dif >= 100:
        step = math.trunc((step_raw*10)/10)
        start_tick = (math.trunc((minv)/10)*10)
    elif dif > 5:
        step = int(step_raw) 
        start_tick = int(minv)
    elif dif >= 1: 
        step = round(step_raw,1) 
        start_tick = round(minv,1)    
    elif dif >= 0.03 and dif < 1:
        step = round(step_raw,2)        
        start_tick = round(minv,2) 
    else : 
        step = step_raw     
        start_tick = minv   
    ticks = np.arange(start_tick,maxv+step,step)    
    return ticks

'''def ticks(minv,maxv):  
    #TODO: Rewrite it 
    if maxv > 1 :
        minv = np.floor(minv)
        minv = (math.trunc(minv/10)*10)
    dif = maxv - minv  
    if minv > 100 :
        minv = (math.trunc(minv/100)*100) 
        
    if 50000. <= dif < 150000. :     
        step = 50000
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
    elif 300.<= dif <  1000. : 
        ticks = np.arange((math.trunc(minv/100)*100),maxv,100)   
        if minv < 100 :
            ticks = np.arange(0,maxv,100)                
    elif  100.  <= dif < 300. :
        ticks = np.arange(minv,maxv,20)  
        
    if dif >= 100:
        step = ((dif/3)/100)*100
        ticks = np.arange(minv,maxv,step)    
        
    elif 50. <= dif < 100. : 
        #dif > 50. and dif < 100. :
        ticks = np.arange(minv,maxv,10)         
    elif dif > 20. and dif <= 50. :
        ticks = np.arange(minv,maxv,5) 
    elif dif > 10. and dif <= 20. :
        ticks = np.arange(minv,maxv,2)        
    elif dif > 3. and dif <= 10. :
        ticks = np.arange(minv,maxv,1) 
    elif dif >= 1. and dif <= 3. :
        ticks = np.arange(minv,maxv,0.5)      
    elif dif > 0.2 and dif <= 1. :
        ticks = np.arange(minv,maxv,0.1)                 
    elif dif > 0.02 and dif <= 0.2 : 
        ticks = np.arange((math.trunc(minv/10)*10),maxv,0.01) 
    elif dif == 0:
        ticks = np.arange(minv - minv/100.,
                maxv + minv/100.,minv/1000.)
    else : 
        ticks = [minv,maxv]                     
    return ticks'''
             
def set_widget_styles(self):
    # Push buttons style
    for button in (self.time_prof_all,self.time_prof_lyr,
                 self.dist_prof_button,self.fick_box, 
                 self.all_year_button,self.help_button,
                 self.dist_time_button):   
        button.setStyleSheet(
        'QPushButton {background-color: #c2b4ae; border-width: 5px;'
        '  padding: 2px; font: bold 15px; }')   
          
    self.help_button.setIcon(QtGui.QIcon('help.png'))   
    self.help_button.setIconSize(QtCore.QSize(30,30))   

    self.help_button.setStyleSheet('QPushButton{border: 0px solid;}')
         
    self.qlistwidget.setStyleSheet(
    'QListWidget{font: 25 px; background-color: #eadfda;  }')
     
    self.lbl_choose_var.setStyleSheet(
        'QLabel {border-width: 7px;'
        '  padding: 7px; font: bold 15px; }')        
    

def widget_layout(self): 
       
        #first line        
        #self.grid.addWidget(self.help_button,0,0,1,1) # help_dialog           
        self.grid.addWidget(self.toolbar,         0,0,1,4)         
        self.grid.addWidget(self.time_prof_all,   0,3,1,1)  
        self.grid.addWidget(self.cmap_groupBox,   0,4,3,1) 
        self.grid.addWidget(self.dist_groupBox,   0,5,3,1)        
        self.grid.addWidget(self.time_groupBox,   0,6,3,1)  
        self.grid.addWidget(self.flux_groupBox,   0,7,3,1)                    
        self.grid.addWidget(self.options_groupBox,0,8,3,1)  
        
        #second line   
        self.grid.addWidget(self.dist_time_button,    1,0,1,1)            
        self.grid.addWidget(self.fick_box,            1,2,1,1)                                   
        self.grid.addWidget(self.time_prof_lyr,       1,3,1,1)  
        
        #third line      
        self.grid.addWidget(self.lbl_choose_var,      2,0,1,1)         
        self.grid.addWidget(self.all_year_button,     2,2,1,1)                   
        self.grid.addWidget(self.dist_prof_button,    2,3,1,1)         
 
        #4th line        
        self.grid.addWidget(self.canvas,              3,2,1,8) 
        self.grid.addWidget(self.qlistwidget,         3,0,2,2)  

def cmap_list(self):
    self.cmap_list = ['jet','inferno','rainbow',
                      'viridis','plasma','Paired',
                      'magma','Greys','Greys_r','ocean']
    return self.cmap_list    

def use_num2date(self,time_units,X_subplot):   
    X_subplot = num2date(X_subplot,units = time_units) 
    return X_subplot

def get_startstop(self):
    start = self.numday_box.value() 
    stop = self.numday_stop_box.value()  
    if stop <= start:
        stop = len(self.time)
        start = 0     
        Messages.StartStop()          
    return start,stop 


def format_time_axis2(self, xaxis,xlen):   
    xaxis.xaxis_date()

    if xlen > 365 and xlen < 365*5 : 
        frmt = '%m/%Y'
    elif xlen >= 365*5 :
        frmt = '%Y'        
    elif xlen <= 365: 
        frmt = '%b'
    if self.time_units == 'seconds since 2012-01-01 00:00:00':
        if xlen < 50 :
            frmt = '%d %b %H:%M'    
            xaxis.set_xticklabels(xaxis.get_xticklabels(), rotation=10)
        else: 
            frmt = '%b/%d '             
    xaxis.xaxis.set_major_formatter(
        mdates.DateFormatter(frmt))   

def plot_inj_lines(self,numday,col,axis):
    axis.axvline(numday,color= col, linewidth = 2,
                   linestyle = '--',zorder = 10) 


def grid_plot(self,numplots):
    if numplots == 1:
        self.gs = gridspec.GridSpec(1, 1) 
        self.gs.update(left = 0.07,right = 0.85,hspace=0.25)
        self.cax = self.figure.add_axes([0.86, 0.1, 0.02, 0.8])        
        self.ax = self.figure.add_subplot(self.gs[0])  
             
    if numplots == 2: 
        self.gs = gridspec.GridSpec(2, 1) 
        self.gs.update(left = 0.07,right = 0.85,hspace=0.25)
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
        
def varmax(self,var,lims):
    return ma.max(var[lims[0]:lims[1],lims[2]:lims[3]]) 
  
def varmin(self,var,lims):
    return ma.min(var[lims[0]:lims[1],lims[2]:lims[3]]) 

def check_minmax(self,cmin,cmax,index):
    ''' Checks if values of max and min are the same or masked'''
    if self.exact_limits.isChecked():  
        pass     
    else:              
        if cmin is ma.masked or cmax is ma.masked: 
            cmin = 0,
            cmax = 1
        elif  cmin ==  cmax :
            if cmax == 0: 
                cmin = 0            
                cmax = 0.1
            else:     
                cmax = cmax + cmax/1000.
                cmin = cmin - cmax/1000. 
               
        if index == 'pH': 
            cmin = float(format(float(cmin), '.2f')) 
            cmax = float(format(float(cmax), '.2f'))           
        elif cmax > 100 :
            cmax = math.trunc(cmax*100)/100
            cmin = math.trunc(cmin*100)/100   
        elif cmax > 10  :
            cmax = math.trunc(cmax*10)/10
            cmin = math.trunc(cmin*10)/10    
        elif cmax > 1  :
            cmax = math.trunc(cmax*10)/10
            cmin = math.trunc(cmin*10)/10      
        elif cmax > 0.1  :
            cmax = math.trunc(cmax*100)/100
            cmin = math.trunc(cmin*100)/100

    assert cmin < cmax                 
    return float(cmin),float(cmax)        
        
def make_maxmin(self,var,start,stop,index,type):
    
    lim_dict = dict(
        wat_dist = (start,stop,0,self.ny1max),
        sed_dist = (start,stop,self.nysedmin,None),
        wat_time = (0,self.ny1max,None,None),
        sed_time = (self.nysedmin,None,None,None))
                             
    if  self.change_limits.isChecked():
        
        ''' Get manually typed values '''
        if (len(self.box_minw.text()) > 0  and 
            len(self.box_maxw.text()) > 0 and
            len(self.box_maxsed.text()) > 0 and 
            len(self.box_minsed.text()) > 0   ) :
            
            funcs = dict(
                wat_time = (self.box_minw,
                            self.box_maxw),
                wat_dist = (self.box_minw,
                            self.box_maxw),
                sed_time = (self.box_minsed,
                            self.box_maxsed),
                sed_dist = (self.box_minsed,
                            self.box_maxsed))
            
            min = float(funcs[type][0].text())
            max = float(funcs[type][1].text())
        else: 
            Messages.no_limits('sediment or water')
            
            lims = lim_dict[type] 
            min = varmin(self,var,lims)     
            max = varmax(self,var,lims)         
           
    else: 
        lims = lim_dict[type]  
        min = varmin(self,var,lims)     
        max = varmax(self,var,lims) 
                        
    maxmin = check_minmax(self,min,max,index)           
    return maxmin
def water_make_maxmin(self,var,start,stop,index,type):
    
    lim_dict = dict(
        wat_dist = (start,stop,0,self.ny1max),
        wat_time = (0,self.ny1max,None,None))
                             
    if  self.change_limits.isChecked():
        
        ''' Get manually typed values '''
        if (len(self.box_minw.text()) > 0  and 
            len(self.box_maxw.text()) > 0 ) :
            
            funcs = dict(
                wat_time = (self.box_minw,
                            self.box_maxw),
                wat_dist = (self.box_minw,
                            self.box_maxw))
            
            min = float(funcs[type][0].text())
            max = float(funcs[type][1].text())
        else: 
            Messages.no_limits('sediment or water')
            
            lims = lim_dict[type] 
            min = varmin(self,var,lims)     
            max = varmax(self,var,lims)         
           
    else: 
        lims = lim_dict[type]  
        min = varmin(self,var,lims)     
        max = varmax(self,var,lims) 
                
    maxmin = check_minmax(self,min,max,index)           
    return maxmin

def check_var_ischosen(self):
    "checks if var is chosen"
    try:
        index = str(self.qlistwidget.currentItem().text())
        return index
    except AttributeError:     
        messagebox = QtWidgets.QMessageBox.about(
            self, "Retry", 'Choose variable,please') 
        return False

def check_is2d(self,index):
    "checks if model array is 2d "
    fh =  Dataset(self.fname)             
    data = np.array(fh.variables[index])
    fh.close()
    if data.shape[2] < 2: 
        messagebox = QtWidgets.QMessageBox.about(self, "Retry,please",
                                             'it is 1D BROM')        
        return False                                             
    else: 
        return True    

def check_2d_and_index(self): 
    index = check_var_ischosen(self)
    if index != False:
        twoD = check_is2d(self,index)   
        if twoD == True:    
            return twoD,index

def fmt(x, pos):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return r'${} \times 10^{{{}}}$'.format(a, b)   
  
def get_format(self,vmax):
    if vmax > self.e_crit_max or vmax < self.e_crit_min:
        return mtick.FuncFormatter(fmt)
    else: 
        return None   
