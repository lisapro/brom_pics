#!/usr/bin/python
# -*- coding: utf-8 -*-
# this ↑ comment is important to have 
# at the very first line 
# to define using unicode 
'''
Created on 14. des. 2016

@author: E.Protsenko
'''


from netCDF4 import Dataset
import main
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import rc
from PyQt4 import QtGui
import os, sys 

#getcontext().prec = 6 
majorLocator = mtick.MultipleLocator(2.)
majorFormatter = mtick.ScalarFormatter(useOffset=False)   
#format y scales to be scalar 
minorLocator = mtick.MultipleLocator(1.)

app1 = QtGui.QApplication(sys.argv)
screen_rect = app1.desktop().screenGeometry()
width, height = screen_rect.width(), screen_rect.height()

rc('font', **{'sans-serif' : 'Arial', #for unicode text
                'family' : 'sans-serif'})  
      
def readdata_brom(self): #,varname,fname
     
    '''self.fh = Dataset(fname)
    self.depth = self.fh.variables['z'][:] 
    self.depth2 = self.fh.variables['z2'][:] #middle points
    self.alk =  self.fh.variables['Alk'][:,:,:]
    self.temp =  self.fh.variables['T'][:,:]
    self.sal =  self.fh.variables['S'][:,:]
    self.kz =  self.fh.variables['Kz'][:,:]
    self.dic =  self.fh.variables['DIC'][:,:]
    self.phy =  self.fh.variables['Phy'][:,:]
    self.het =  self.fh.variables['Het'][:,:]
    self.no3 =  self.fh.variables['NO3'][:,:]
    self.po4 =  self.fh.variables['PO4'][:,:]
    self.nh4 =  self.fh.variables['NH4'][:,:]
    self.pon =  self.fh.variables['PON'][:,:]
    self.don =  self.fh.variables['DON'][:,:]
    self.o2  =  np.array(self.fh.variables['O2'][:,:])
    self.mn2 =  self.fh.variables['Mn2'][:,:]
    self.mn3 =  self.fh.variables['Mn3'][:,:]
    self.mn4 =  self.fh.variables['Mn4'][:,:]
    self.h2s =  self.fh.variables['H2S'][:,:]
    self.mns =  self.fh.variables['MnS'][:,:]
    self.mnco3 =  self.fh.variables['MnCO3'][:,:]
    self.fe2 =  self.fh.variables['Fe2'][:,:]
    self.fe3 =  self.fh.variables['Fe3'][:,:]
    self.fes =  self.fh.variables['FeS'][:,:]
    self.feco3 =  self.fh.variables['FeCO3'][:,:]
    self.no2 =  self.fh.variables['NO2'][:,:]
    self.s0 =  self.fh.variables['S0'][:,:]
    self.s2o3 =  self.fh.variables['S2O3'][:,:]
    self.so4 =  self.fh.variables['SO4'][:,:]
    self.si =  self.fh.variables['Si'][:,:]
    self.si_part =  self.fh.variables['Sipart'][:,:]
    self.baae =  self.fh.variables['Baae'][:,:]
    self.bhae =  self.fh.variables['Bhae'][:,:]
    self.baan =  self.fh.variables['Baan'][:,:]
    self.bhan =  self.fh.variables['Bhan'][:,:]
    self.caco3 =  self.fh.variables['CaCO3'][:,:]
    self.fes2 =  self.fh.variables['FeS2'][:,:]
    self.ch4 =  self.fh.variables['CH4'][:,:]
    self.ph =  self.fh.variables['pH'][:,:]
    self.pco2 =  self.fh.variables['pCO2'][:,:]
    self.om_ca =  self.fh.variables['Om_Ca'][:,:]
    self.om_ar =  self.fh.variables['Om_Ar'][:,:]
    self.co3 =  self.fh.variables['CO3'][:,:]
    self.ca =  self.fh.variables['Ca'][:,:]
    self.time =  self.fh.variables['time'][:]
    self.fick_o2 = self.fh.variables['fick:O2'][:]
    self.fick_no2 = self.fh.variables['fick:NO2'][:]    
    self.fick_no3 = self.fh.variables['fick:NO3'][:]        
    self.fick_si = self.fh.variables['fick:Si'][:]  
    self.fick_h2s = self.fh.variables['fick:H2S'][:]              
    self.fick_nh4 = self.fh.variables['fick:NH4'][:]        
    self.fick_dic = self.fh.variables['fick:DIC'][:]        
    self.fick_alk = self.fh.variables['fick:Alk'][:]        
    self.fick_po4 = self.fh.variables['fick:PO4'][:]''' 
       
    self.vars = ([],
    ['NO2','NO3','NH4'],
    ['PO4', 'SO4','O2'],
    ['H2S','PON','DON'],
    ['DIC','Phy','Het'],
    ['pCO2','pH','Alk'],
    ['Mn2','Mn3','Mn4'],
    ['MnS','MnCO3','Bhan'])

    # list of names to add to Combobox All year charts
    self.var_names_charts_year = (('All year(last) graphs'),
        ('NO2, NO3, NH4'),
        ('PO4, SO4, O2'),
        ('H2S, PON, DON'),
        ('DIC, Phy, Het'), 
        ('pCO2,pH,Alk'),
        ('MNII,MnIII,MnIV'),
        ('MnS, MnCO3,bhan'), 
        ('FeII,FeIII,FeS'),
        ('FeCO3,FeS2,Si'),  
        ('S0 ,S2O3,Si_part'),
        ('baae, bhae,baan'),
        ('caco3, ch4, om_ca'), 
        ('om_ar, co3, ca'),
        ('salinity,Temperature,O2'))        
         
    '''self.vars = ([],['NO2','NO3','NH4'],
    [self.si], [self.alk],[self.po4],[self.nh4],
    [self.h2s ],[self.pon], [self.don],[self.dic],[self.phy],
    [self.het], [self.mn2], [self.mn3], [self.mn4],[self.mns],
    [self.mnco3], [self.fe2], [self.fe3 ], [self.fes],
    [self.feco3 ], [self.fes2],[self.s0], [self.s2o3], 
    [self.so4], [self.si_part], [self.baae], [self.bhae],
    [self.baan], [self.bhan], [self.caco3], [self.ch4],
    [self.ph], [self.pco2], [self.om_ca], [self.om_ar],
    [self.co3], [self.ca],[self.sal], [self.temp])'''
    
    #Variable names to add to combobox with time profiles
    self.var_names_profile = ('Time profile','O2' ,'NO3' ,'no2', 'Si', 'Alk',
    'PO4','NH4', 'H2S','PON',  'DON',  'DIC','Phy', 'Het', 
    'MnII',  'MnIII',  'MnIV','MnS', 'MnCO3', 
    'FeII' ,'FeIII' , 'FeS','FeCO3', 'FeS2',  
    'S0' ,'S2O3', 'SO4', 'Si_part',
    'baae', 'bhae', 'baan', 'bhan',
    'CaCO3', 'CH4', 'pH', 'pCO2','om_Ca', 
    'om_ar', 'CO3', 'ca', 'sal', 'Temperature')  
      
    # list of names to add to Combobox All year charts
    self.var_names_charts_year = (('All year(last) graphs'),
        ('NO2, NO3, NH4'),
        ('PO4, SO4, O2'),
        ('H2S, PON, DON'),('DIC, Phy, Het'), 
        ('pCO2,pH,Alk'),
        ('MNII,MnIII,MnIV'),
        ('MnS, MnCO3,bhan'), 
        ('FeII,FeIII,FeS'),
        ('FeCO3,FeS2,Si'),  
        ('S0 ,S2O3,Si_part'),
        ('baae, bhae,baan'),
        ('caco3, ch4, om_ca'), 
        ('om_ar, co3, ca'),
        ('salinity,Temperature,O2'))  
    #len
    # list of titles to add to figures at All year charts    
    self.titles_all_year = (('All year charts'),
        (r'$\rm NO _2   \mu M/l$',r'$\rm NO _3  \mu M/l $',
         r'$\rm NH _4   \mu M/l$'),
        (r'$\rm PO _4 $',r'$\rm SO _4 $', r'$\rm O _2 \mu M/l $'),
        (r'$\rm H _2 S $', r'$\rm PON $', r'$\rmDON $'),
        (r'$\rm DIC $', r'$\rm Phy $', r'$\rm Het $'), 
        (r'$\rm pCO _2 $',r'$\rm pH $',r'$\rm Alk $'),
        (r'$\rm MnII $',r'$\rm MnIII $',r'$\rm MnIV $'),
        (r'$\rm MnS $', r'$\rm MnCO _3 $',r'$\rm bhan $'), 
        (r'$\rm FeII $',r'$\rm FeIII $',r'$\rm FeS $'),
        (r'$\rm FeCO _3 $',r'$\rm FeS _2 $',r'$\rm Si $'),  
        (r'$\rm S ^0 $' ,r'$\rm S _2 O _3 $',r'$\rm Si part $'),
        (r'$\rm Baae $', r'$\rm Bhae $',r'$\rm Baan $'),
        (r'$\rm CaCO _3 $', r'$\rm CH _4 $', r'$\rm \Omega Ca $'), 
        (r'$\rm \Omega Aragonite $', r'$\rm CO _3 $', r'$\rm Ca $'),
        (r'$\rm Salinity $',r'$\rm Temperature $',r'$\rm O _2 $'))     
     
    # list of variable names to connect titles and variables 
    '''self.vars_year = ([],
                      [[self.no2],[self.no3],[self.nh4]],
                      [[self.po4],[self.so4],[self.o2]],
                      [[self.h2s],[self.pon],[self.don]],
                      [[self.dic],[self.phy],[self.het]],
                      [[self.pco2],[self.ph],[self.alk]],                      
                      [[self.mn2],[self.mn3],[self.mn4]],
                      [[self.mns],[self.mnco3],[self.bhan]], 
                      [[self.fe2],[self.fe3],[self.fes]],
                      [[self.feco3],[self.fes2],[self.si]],
                      [[self.s0],[self.s2o3],[self.si_part]], 
                      [[self.baae],[self.bhae],[self.baan]],                                                                                        
                      [[self.caco3],[self.ch4],[self.om_ca]],     
                      [[self.om_ar],[self.co3],[self.ca]],       
                      [[self.sal],[self.temp],[self.o2]],                                                                             
    ) 
    
    self.fh.close() '''
    #self.lentime = len(self.time)
    # numbers of first days of each month to add to combobox 'One day'                           
    self.months_start = [1,32,61,92,122,153,183,
                          214,245,275,306,336,366]
    
    '''self.resolutions = [('Resoluton'),(1000,700),(842,595),
                        (2339,1654),(3508,2480),
                        (4677,3307),(40,10)]'''

    #def calc_last_year(self):
    #self.start_last_year = self.lentime - 365  
    #self.last_year_time = self.time[self.start_last_year:]


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
    if 'i' in self.names_vars: 
        self.dist = np.array(self.fh.variables['i']) 

 
def read_all_year_var(self,fname,varname1,varname2,varname3): 
    self.fh = Dataset(fname)  
    self.var1 = self.fh.variables[varname1][:]
    self.var2 = self.fh.variables[varname2][:]
    self.var3 = self.fh.variables[varname3][:]  
    return  self.var1,self.var2, self.var3      

    #print ('var', self.var)
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
        
    #define color maps 
    self.cmap = plt.cm.jet #gnuplot#jet#gist_rainbow
    self.cmap1 = plt.cm.rainbow 

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
    for n in range(0,(len(self.depth2)-1)):
        if self.depth2[n+1] - self.depth2[n] >= self.bbl:
            if n == self.lendepth2-2: # len(self.depth2):
                y1max = (self.depth2[n]-1)
                self.ny1min = (self.depth[0])
                self.y1max = y1max                                                     
                self.ny1max = n-1
                self.sediment = False
                print ('no sediment y wat', self.y1max)        
                break  
        elif self.depth2[n+1] - self.depth2[n] < self.bbl:   
            self.y1max = (self.depth2[n]-1)                                               
            self.ny1max = n-1
            self.sediment = True
            #print ('calc_y_wat_y1max', self.y1max)
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
        n = variable[0:self.ny1max,:].max()
        print (n)      
    elif vartype == 'sedtime' : #time plot sediment
        n = variable[self.nysedmin-2:,:].max()
        print (n) 
        
    # make "beautiful"  values to show on ticks         2   
    if n > 10000. and n <= 100000.:  
        n = int(math.ceil(n/ 1000.0)) * 1000 + 1000.
    elif n > 1000. and n <= 10000.:  
        n = int(math.ceil(n / 100.0)) * 100  + 10.                                 
    elif n >= 100. and n < 1000.:
        n = int(math.ceil(float(n) / 10.0)) * 10 + 10.
    elif n >= 1. and n < 100. :
        n =  int(np.ceil(float(n)))  + 1.  
    elif n >= 0.1 and n < 1. :
        n =  (math.ceil(n*10.))/10. + 0.1  
    elif n >= 0.01 and n < 0.1 :
        n =  (math.ceil(n*100.))/100. 
    elif n >= 0.001 and n < 0.01 :
        n =  (math.ceil(n*1000.))/1000.
    elif n >= 0.0001 and n < 0.001 :
        n =  (math.ceil(n*10000))/10000 +  0.0001   
    elif n >= 0.00001 and n < 0.0001 :
        n =  (math.ceil(n*100000))/100000 
                                                                                               
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
        print (start,stop,variable.shape)
        n = np.floor(variable[0:self.ny1max,:].min())  
        print ("min",n )      
    elif vartype == 'sedtime'  : #time plot sediment
        n = np.floor(variable[self.nysedmin-2:,:].min()) 
                
 

    '''
    if vartype == 0: #water
        n = variable[start:stop,0:self.ny1max].max() 
          
    elif vartype == 1 :#sediment
        n = variable[start:stop,self.nysedmin:].max()
  
    elif vartype == 2: #time plot water
        n = variable[0:self.ny1max,start:stop].max()
        print (n)      
    elif vartype == 3 : #time plot sediment
        n = variable[self.nysedmin-2:,start:stop].max()
        print (n) '''



        
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
        n =  (np.floor(n*100000))/100000 
  
    self.watmin =  n  
                 
    return self.watmin

# make "beautiful"  values to show on ticks 
def ticks(minv,maxv):          
    if (maxv - minv) >= 50000. and (
         maxv - minv) < 150000.  :
        ticks = np.arange(minv,maxv+10000.,50000)        
    elif (maxv - minv) >= 10000. and (
         maxv - minv) < 50000.  :
        ticks = np.arange(minv,maxv+5000.,5000)        
    elif (maxv - minv) > 3000. and (
       maxv - minv) < 10000.  : 
        ticks = np.arange(minv,maxv+1000.,1000)        
    elif (maxv - minv) > 1500. and ( 
     maxv - minv) <= 3000. :
        ticks = np.arange(minv,maxv+500.,500)                        
    elif (maxv - minv) >= 300. and ( 
     maxv - minv) <= 1500. :
        ticks = np.arange((math.trunc(minv/10)*10),maxv+100.,100)   
        if minv < 100 :
            ticks = np.arange(0,maxv+100.,100)              
    elif (maxv - minv) >= 100. and ( 
     maxv - minv) < 300. :
        ticks = np.arange(minv-10,maxv+50.,50) 
    elif (maxv - minv) > 50. and ( 
     maxv - minv) < 100. :
        ticks = np.arange(minv,maxv+10.,10)        
    elif (maxv - minv) > 20. and ( 
     maxv - minv) <= 50. :
        ticks = np.arange(minv,maxv+5.,5)
    elif (maxv - minv) > 3. and ( 
     maxv - minv) <= 20. :
        ticks = np.arange(minv,maxv+1.,1)
    elif (maxv - minv) >= 1. and ( 
     maxv - minv) <= 3. :
        ticks = np.arange(minv,maxv+1.,0.5)         
    elif (maxv - minv) > 0.2 and ( 
     maxv - minv) <= 1. :
        ticks = np.arange(minv,maxv+1.,0.1)                  
    else :  
        ticks = np.arange(minv,maxv + (maxv - minv)/2., (maxv - minv)/2.)                   
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
                 self.dist_prof_button,
                 self.all_year_test_button):   
        axis.setStyleSheet(
        'QPushButton {background-color: #c2b4ae; border-width: 5px;'
        '  padding: 2px; font: bold 15px; }')     
        
    # Combo boxes style
    for axis in (self.time_prof_box,self.all_year_1d_box): 
        axis.setStyleSheet(
        'QComboBox {background-color: #c2b4ae; border-width: 7px;'
        '  padding: 7px; font: bold 14px; }')  
    #self.time_prof_box.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)   
    
    # Spinbox style
    self.varname_box.setStyleSheet(
    'QSpinBox {background-color: #c2b4ae; border-width: 15px;'
    '  padding: 5px; font: bold 15px; }')        
    
    self.dist_prof_checkbox.setStyleSheet(
    'QCheckBox {border-width: 15px;' #background-color: #c2b4ae; 
    '  padding: 5px; font: bold 15px; }')          
    self.qlistwidget.setStyleSheet(
    'QListWidget{font: 25 px; background-color: #eadfda;  }')
     #background-color: #f9e7de; 
            
    

def widget_layout(self):    
        #first line              
        self.grid.addWidget(self.toolbar,0,1,1,1)        
        self.grid.addWidget(self.time_prof_all,0,2,1,1)  
        self.grid.addWidget(self.dist_prof_button,0,3,1,1)   
         
        #self.grid.addWidget(self.time_prof_box,1,0,1,1)  
              
        self.grid.addWidget(self.numcol_2d ,0,4,1,1)              
        self.grid.addWidget(self.textbox,0,5,1,1)          
        #second line    
        self.grid.addWidget(self.dist_prof_checkbox,0,0,1,1)  
                  
        self.grid.addWidget(self.time_prof_last_year,1,2,1,1) 
        #self.grid.addWidget(self.all_year_1d_box,1,2,1,1)         
        self.grid.addWidget(self.all_year_test_button,1,3,1,1)                         
        self.grid.addWidget(self.numday_box,1,4,1,1)  
        self.grid.addWidget(self.textbox2,1,5,1,1)    
        #third line              
        self.grid.addWidget(self.canvas, 2, 1,1,5)     
        self.grid.addWidget(self.qlistwidget,2,0,1,1) 