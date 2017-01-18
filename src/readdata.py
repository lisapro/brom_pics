'''
Created on 14. des. 2016

@author: ELP
'''
from netCDF4 import Dataset
import main
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import calc_resolution
from PyQt4 import QtGui
import sys 
#getcontext().prec = 6 
majorLocator = mtick.MultipleLocator(2.)
majorFormatter = mtick.ScalarFormatter(useOffset=False)   #format y scales to be scalar 
minorLocator = mtick.MultipleLocator(1.)

app1 = QtGui.QApplication(sys.argv)
screen_rect = app1.desktop().screenGeometry()
width, height = screen_rect.width(), screen_rect.height()
#print (width, height)    
    
def readdata_brom(self,fname): 

    fh = Dataset(fname)
    self.depth = fh.variables['z'][:] 
    self.depth2 = fh.variables['z2'][:] #middle points
    self.alk =  fh.variables['Alk'][:,:,:]
    self.temp =  fh.variables['T'][:,:]
    self.sal =  fh.variables['S'][:,:]
    self.kz =  fh.variables['Kz'][:,:]
    self.dic =  fh.variables['DIC'][:,:]
    self.phy =  fh.variables['Phy'][:,:]
    self.het =  fh.variables['Het'][:,:]
    self.no3 =  fh.variables['NO3'][:,:]
    self.po4 =  fh.variables['PO4'][:,:]
    self.nh4 =  fh.variables['NH4'][:,:]
    self.pon =  fh.variables['PON'][:,:]
    self.don =  fh.variables['DON'][:,:]
    self.o2  =  fh.variables['O2'][:,:]
    self.mn2 =  fh.variables['Mn2'][:,:]
    self.mn3 =  fh.variables['Mn3'][:,:]
    self.mn4 =  fh.variables['Mn4'][:,:]
    self.h2s =  fh.variables['H2S'][:,:]
    self.mns =  fh.variables['MnS'][:,:]
    self.mnco3 =  fh.variables['MnCO3'][:,:]
    self.fe2 =  fh.variables['Fe2'][:,:]
    self.fe3 =  fh.variables['Fe3'][:,:]
    self.fes =  fh.variables['FeS'][:,:]
    self.feco3 =  fh.variables['FeCO3'][:,:]
    self.no2 =  fh.variables['NO2'][:,:]
    self.s0 =  fh.variables['S0'][:,:]
    self.s2o3 =  fh.variables['S2O3'][:,:]
    self.so4 =  fh.variables['SO4'][:,:]
    self.si =  fh.variables['Si'][:,:]
    self.si_part =  fh.variables['Sipart'][:,:]
    self.baae =  fh.variables['Baae'][:,:]
    self.bhae =  fh.variables['Bhae'][:,:]
    self.baan =  fh.variables['Baan'][:,:]
    self.bhan =  fh.variables['Bhan'][:,:]
    self.caco3 =  fh.variables['CaCO3'][:,:]
    self.fes2 =  fh.variables['FeS2'][:,:]
    self.ch4 =  fh.variables['CH4'][:,:]
    self.ph =  fh.variables['pH'][:,:]
    self.pco2 =  fh.variables['pCO2'][:,:]
    self.om_ca =  fh.variables['Om_Ca'][:,:]
    self.om_ar =  fh.variables['Om_Ar'][:,:]
    self.co3 =  fh.variables['CO3'][:,:]
    self.ca =  fh.variables['Ca'][:,:]
    self.time =  fh.variables['time'][:]
    
    self.vars = ([],[self.o2],[self.no3 ],[self.no2],
    [self.si], [self.alk],[self.po4],[self.nh4],
    [self.h2s ],[self.pon], [self.don],[self.dic],[self.phy],
    [self.het], [self.mn2], [self.mn3], [self.mn4],[self.mns],
    [self.mnco3], [self.fe2], [self.fe3 ], [self.fes],
    [self.feco3 ], [self.fes2],[self.s0], [self.s2o3], 
    [self.so4], [self.si_part], [self.baae], [self.bhae],
    [self.baan], [self.bhan], [self.caco3], [self.ch4],
    [self.ph], [self.pco2], [self.om_ca], [self.om_ar],
    [self.co3], [self.ca],[self.sal], [self.temp],[self.kz])
    
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
    self.var_names_charts_year = (('All year charts'),
        ('NO2, NO3, NH4'),
        ('PO4','SO4',' O2'),
        ('H2S', 'PON', 'DON'),('DIC, Phy, Het'), 
        ('pCO2','pH','Alk'),
        ('MNII','MnIII','MnIV'),
        ('MnS', 'MnCO3','bhan'), 
        ('FeII','FeIII','FeS'),
        ('FeCO3','FeS2','Si'),  
        ('S0' ,'S2O3','Si_part'),
        ('baae', 'bhae','baan'),
        ('caco3', 'ch4', 'om_ca'), 
        ('om_ar', 'co3', 'ca'),
        ('sal','Temperature','Kz'))  
    
    # list of titles to add to figures at All year charts    
    self.titles_all_year = (('All year charts'),
        (r'$\rm NO _2 $',r'$\rm NO _3 $',r'$\rm NH _4 $'),
        ('PO4','SO4',' O2'),
        ('H2S', 'PON', 'DON'),
        ('DIC', 'Phy', 'Het'), 
        ('pCO2','pH','Alk'),
        ('MNII','MnIII','MnIV'),
        ('MnS', 'MnCO3','bhan'), 
        ('FeII','FeIII','FeS'),
        ('FeCO3','FeS2','Si'),  
        ('S0' ,'S2O3','Si_part'),
        ('baae', 'bhae','baan'),
        ('caco3', 'ch4', 'om_ca'), 
        ('om_ar', 'co3', 'ca'),
        ('sal','Temperature','Kz'))     
     
    # list of variable names to connect titles and variables 
    self.vars_year = ([],
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
                      [[self.sal],[self.temp],[self.kz]],                                                                                 
    )
    
    fh.close()
    # numbers of first days of each month to add to combobox 'One day'                           
    self.monthes_start = [1,32,61,92,122,153,183,
                          214,245,275,306,336,366]



    
def calculate_ywat(self):
    for n in range(0,(len(self.depth2)-1)):
        if self.depth2[n+1] - self.depth2[n] >= 0.5:
            pass
        elif self.depth2[n+1] - self.depth2[n] < 0.50:    
            y1max = (self.depth2[n])
            self.y1max = y1max                                                      
            self.ny1max = n
            break
  
def calculate_ybbl(self):
    for n in range(0,(len(self.depth2)-1)):
        if self.kz[1,n] == 0:
            self.y2max = self.depth2[n]         
            self.ny2max = n         
            break  
        

            
def y2max_fill_water(self):
    for n in range(0,(len(self.depth2)-1)):
#        if depth[_]-depth[_?]
        if self.depth2[n+1] - self.depth2[n] >= 0.5:
            pass
        elif self.depth2[n+1] - self.depth2[n] < 0.50:
#            watmax =  depth[n],depth[n]-depth[n+1],n
            self.y2max_fill_water = self.depth2[n] 
            self.nbblmin = n            
            break 
         
def calculate_ysed(self):
    for n in range(0,(len(self.depth_sed))):
        if self.kz[1,n] == 0:
            ysed = self.depth_sed[n]  
            self.ysedmin =  ysed - 10
            self.ysedmax =  self.depth_sed[len(self.depth_sed)-1] 
            self.y3min = self.depth_sed[self.nbblmin+2]
            #here we cach part of BBL to add to 
            #the sediment image                
            break            
def y_coords(self):       
#        self.y2min = self.y2max - 2*(self.y2max - self.y1max)   #calculate the position of y2min, for catching part of BBL 
    self.ny2min = self.ny2max - 2*(self.ny2max - self.ny1max) 
    self.y2min_fill_bbl = self.y2max_fill_water = self.y1max #y2max_fill_water() #109.5 #BBL-water interface
    self.ysedmax_fill_bbl = 0
    self.ysedmin_fill_sed = 0
    self.y1min = 0
    self.y2min = self.y2max - 2*(self.y2max - self.y1max)   
          
    #calculate the position of y2min, for catching part of BBL 


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

def depth_sed2(self):
    to_float = []
    for item in self.depth2:
        to_float.append(float(item)) #make a list of floats from tuple 
    depth_sed2 = [] # list for storing final depth data for sediment 
    v=0  
    for i in to_float:
        v = (i- self.y2max)*100  #convert depth from m to cm
        depth_sed2.append(v)
        self.depth_sed2 = depth_sed2  
                   
def varmax(self,variable,vartype):
    if vartype == 0: #water
        n = variable[0:self.ny2max-1,:].max() 
           
    elif vartype == 1 :#sediment
        n = variable[self.nbblmin:,:].max()
    if n > 10000. and n <= 100000.:  
        n = int(math.ceil(n/ 1000.0)) * 1000 + 1000
    elif n > 1000. and n <= 10000.:  
        n = int(math.ceil(n / 100.0)) * 100  + 100                                 
    elif n >= 100. and n < 1000.:
        n = int(math.ceil(n / 10.0)) * 10 + 10
    elif n >= 1. and n < 100. :
        n =  int(np.ceil(n))  + 1
    elif n >= 0.1 and n < 1. :
        n =  (math.ceil(n*10.))/10. + 0.1  
    elif n >= 0.01 and n < 0.1 :
        n =  (math.ceil(n*100.))/100. 
    elif n >= 0.001 and n < 0.01 :
        n =  (math.ceil(n*1000.))/1000.
    elif n >= 0.0001 and n < 0.001 :
        n =  (math.ceil(n*10000))/10000  
    elif n >= 0.00001 and n < 0.0001 :
        n =  (math.ceil(n*100000))/100000                                                                                         
    self.watmax =  n
    
    return self.watmax

def int_value(self,n,min,max):
    num = self.num
    
    if (max - min) >= num*10. and ( 
     max - min) < num*100. :
        m = math.ceil(n/10)*10.
    elif ( max -  min) >= num and (
         max -  min) < 10.*num :
        m = math.ceil(n)        
    elif ( max -  min) > num/10. and (
         max -  min) < num :
        m = (math.ceil(n*10.))/10.        
    elif ( max -  min) > num/100. and (
         max -  min) < num/10. :
        m = (math.ceil(n*100.))/100.          
    elif ( max -  min) > num/1000. and (
         max -  min) < num/100. :
        m = (math.ceil(n*1000.))/1000.                      
    else :
        m = n  
          
    return m    
def varmin(self,variable,vartype):
    if vartype == 0 :
        n = np.round(variable[0:365].min())
    elif vartype == 1 : 
        n = variable[:,self.ny2min:].min()            
    if n >= 28000.:
        n = 28000. #np.ceil(n)        
    if n >= 27000 and n < 28000:
        n = 27000#np.ceil(n)
    if n >= 26000 and n < 27000:
        n = 26000#np.ceil(n)
    if n >= 25000 and n < 26000:
        n = 25000#np.ceil(n)
    elif n >= 22500 and n < 25000 :
        n = 22500#np.ceil(n)              
    elif n >= 20000 and n < 22500:
        n = 20000#np.ceil(n)            
    elif n >= 10000 and n < 20000:
        n = 10000#np.ceil(n)    
    elif n >= 7000 and n < 10000:  
        n = 7000                     
    elif n >= 5000 and n < 7000:  
        n =5000         
    elif n >= 1000 and n < 5000:  
        n = 1000        
    elif n >= 500 and n < 1000:  
        n = 500 
    elif n >= 350 and n < 500:  
        n = 350.                       
    elif n >= 200. and n < 350:  
        n = 200          
    elif n >= 100 and n < 200:  
        n = 100          
    elif n >= 50 and n < 100:
        n = 50    
    elif n >= 25 and n < 50:
        n = 25                             
    elif n >= 10 and n < 25:
        n = 10            
    elif n >= 6 and n < 10:
        n = 6
    elif n >= 5 and n < 6:
        n = 5            
    elif n >= 2.5 and n < 5:
        n = 2.5     
    elif n >= 1. and n < 2.5:
        n = 1.                     
    elif n >=  0.5 and n <1:
        n = 0.5                     
    elif n >= 0.05 and n < 0.5:
        n = 0.05           
    elif n >=  0.005 and n <0.05:
        n = 0.005         
    elif n >=  0.0005 and n <= 0.005:
        n = 0.0005
    elif n >=  0.00005 and  n  <0.0005 :
        n = 0.00005 
    self.watmin = int(np.floor(n))                          
    return self.watmin
def ticks(min,max):      
    if (max - min) >= 50000. and (
         max - min) < 150000.  :
        ticks = np.arange(min,max+10000.,50000)        
    elif (max - min) >= 10000. and (
         max - min) < 50000.  :
        ticks = np.arange(min,max+5000.,5000)        
    elif (max - min) >= 3000. and (
       max - min) < 10000.  : 
        ticks = np.arange(min,max+1000.,1000)        
    elif (max - min) >= 1500. and ( 
     max - min) < 3000. :
        ticks = np.arange(min,max+500.,500)                        
    elif (max - min) >= 300. and ( 
     max - min) < 1500. :
        ticks = np.arange(min,max+100.,100)        
    elif (max - min) >= 100. and ( 
     max - min) < 300. :
        ticks = np.arange(min,max+50.,50) 
    elif (max - min) >= 50. and ( 
     max - min) < 100. :
        ticks = np.arange(min,max+10.,10)        
    elif (max - min) >= 20. and ( 
     max - min) < 50. :
        ticks = np.arange(min,max+5.,5)
    elif (max - min) >= 3. and ( 
     max - min) < 20. :
        ticks = np.arange(min,max+1.,1)
    elif (max - min) >= 1. and ( 
     max - min) < 3. :
        ticks = np.arange(min,max+1.,0.5)         
    elif (max - min) >= 0.2 and ( 
     max - min) < 1. :
        ticks = np.arange(min,max+1.,0.1)                  
    else : 
        #ticks = np.arange(min,max+0.05, 0.005)    
        ticks = np.arange(min,max + (max - min)/2., (max - min)/2.)                   
    return ticks

    def y_lim(self,axis): #function to define y limits 
        if axis in (self.ax00,self.ax10,self.ax20):   #water          
            axis.fill_between(self.xticks, self.y1max, self.y1min,
                              facecolor= self.wat_color, alpha=self.alpha_wat)  
        elif axis in (self.ax01,self.ax11,self.ax21):  #BBL
            axis.fill_between(self.xticks, self.y2max, self.y2min_fill_bbl,
                               facecolor= self.bbl_color, alpha=self.alpha_bbl)
            #plt.setp(axis.get_xticklabels(), visible=False)                                           
        elif axis in (self.ax02,self.ax12,self.ax22): #sediment 
            axis.fill_between(self.xticks, self.ysedmax_fill_bbl,
                               self.ysedmin, facecolor= self.bbl_color, alpha=self.alpha_bbl)  
            axis.fill_between(self.xticks, self.ysedmax, self.ysedmin_fill_sed, facecolor= self.sed_color, alpha=self.alpha_sed)    




def y_lim1(self,axis): 

    self.xticks =(np.arange(0,100000))#function to define y limits 
    if axis in (self.ax00,self.ax10,self.ax20,
                self.ax30,self.ax40,self.ax50):   #water
        axis.set_ylim([self.y2min, 0])
        axis.yaxis.grid(True,'minor')
        axis.xaxis.grid(True,'major')                
        axis.yaxis.grid(True,'major') 
#            axis.fill_between(self.xticks1, self.y1max, self.y1min, facecolor= self.wat_color1, alpha=self.alpha_wat)
    elif axis in (self.ax01,self.ax11,self.ax21,
        self.ax31,self.ax41,self.ax51):  #BBL
        axis.set_ylim([self.y2max, self.y2min])
        axis.fill_between(self.xticks, self.y2max,
            self.y2min_fill_bbl,
            facecolor= self.bbl_col, 
            alpha=self.a_bbl)
        axis.yaxis.grid(True,'minor')
        axis.yaxis.grid(True,'major')   
        axis.xaxis.grid(True,'major')              
#            axis.fill_between(self.xticks1, self.y2max_fill_water, self.y2min, facecolor= self.wat_color, alpha= self.alpha_wat) 
#            axis.fill_between(self.xticks1, self.y2max, self.y2min_fill_bbl, facecolor= self.bbl_color, alpha= self.alpha_bbl)
        plt.setp(axis.get_xticklabels(), visible=False) 
    elif axis in (self.ax02,self.ax12,
            self.ax22,self.ax32,self.ax42,self.ax52): #sediment 
        axis.set_ylim([self.ysedmax, self.ysedmin])   #[y3max, y3min]   
        axis.fill_between(self.xticks,
            self.ysedmax_fill_bbl, self.ysedmin,
            facecolor= self.bbl_col,
            alpha=self.a_bbl)  
        axis.fill_between(self.xticks,
            self.ysedmax, self.ysedmin_fill_sed,
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
    min = varmin(self,var,type) #0 - water 
    max = varmax(self,var,type)
    axis.set_xlim([min,max])  
    #tick = ticks(watmin,watmax)
    axis.set_xticks(np.arange(min,max+((max - min)/2.),
            ((max - min)/2.)))      
        
        
        
def colors(self):
    self.spr_aut ='#998970'#'#cecebd'#'#ffffd1'#'#e5e5d2'  
    self.wint = '#8dc0e7' 
    self.summ = '#d0576f' 
    self.a_w = 0.5 #alpha (transparency) for winter
    self.a_bbl = 0.3 
    self.a_s = 0.5 #alpha (transparency) for summer
    self.a_aut = 0.5 #alpha (transparency) for autumn and spring    
    self.wat_col = '#c9ecfd' # calc_resolution for filling water,bbl and sediment 
    self.bbl_col = '#2873b8' # for plot 1,2,3,4,5,1_1,2_2,etc.
    self.sed_col= '#916012'


    
    self.labelaxis_x =  1.10 #positions of labels 
    self.labelaxis1_y = 1.02
    dx = 0.15#(height / 30000.) #0.1
    dy = 14 #height/96
    self.labelaxis2_y = 1.02 + dx
    self.labelaxis3_y = 1.02 + dx * 2.
    self.labelaxis4_y = 1.02 + dx * 3.
    self.labelaxis5_y = 1.02 + dx * 4.

    self.axis1 = 0
    self.axis2 = 0 + dy 
    self.axis3 = 0 + dy * 2
    self.axis4 = 0 + dy * 3
    self.axis5 = 0 + dy * 4  

    self.font_txt = 15 #(height / 190.)  # text on figure 2 (Water; BBL, Sed) 
    self.xlabel_fontsize = 10 #(height / 170.) #14 #axis labels      
    self.ticklabel_fontsize = 10 #(height / 190.) #14 #axis labels   
    self.linewidth = 0.7        
    #print (self.xlabel_fontsize)
    