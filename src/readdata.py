'''
Created on 14. des. 2016

@author: ELP
'''
from netCDF4 import Dataset
import main
import numpy as np
import math
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
    [self.co3], [self.ca],[self.sal], [self.temp])
    
    self.var_names_profile = ('Time profile','O2' ,'no3' ,'no2', 'si', 'alk',
    'po4','nh4', 'h2s','pon',  'don',  'dic','phy', 'het', 
    'mn2',  'mn3',  'mn4','mns', 'mnco3', 
    'fe2' ,'fe3' , 'fes','feco3', 'fes2',  
    's0' ,'s2o3', 'so4', 'si_part',
    'baae', 'bhae', 'baan', 'bhan',
    'caco3', 'ch4', 'ph', 'pco2','om_ca', 
    'om_ar', 'co3', 'ca', 'sal', 'Temperature')    

    self.var_names_charts_year = (('All year charts'),
        ('NO2','NO3','NH4'),
        ('PO4','SO4',' O2'),
        ('H2S, PON, DON'),('DIC, Phy, Het'), 
    ('MNII,MnIII,MnIV'),('MnS', 'MnCO3'), 
    ('FeII,FeIII' ), ('FeS,FeCO3,FeS2'),  
    ('S0' ,'S2O3'),('Si,Si_part,pH'),
    ('baae, bhae,baan,bhan'),('caco3', 'ch4', 'pco2','om_ca'), 
    ('om_ar', 'co3', 'ca'), ('sal,Temperature'))  

    self.vars_year = ([],
                      [[self.no2],[self.no3],[self.nh4]],
                      [[self.po4],[self.so4],[self.o2]],
                      []
    )
    
    fh.close()
                          
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
  
                   
def varmax(self,variable,vartype):
    if vartype == 0: #water
        n = variable[0:self.ny2max-1,:].max() 
           
    elif vartype == 1 :#sediment
        n = variable[self.nbblmin:,:].max()
    if n > 10000. and n <= 100000.:  
        n = int(math.ceil(n / 1000.0)) * 1000  
    elif n > 1000. and n <= 10000.:  
        n = int(math.ceil(n / 100.0)) * 100                                   
    elif n >= 100. and n < 1000.:
        n = int(math.ceil(n / 10.0)) * 10
    elif n >= 1. and n < 100. :
        n =  int(np.ceil(n)) 
    elif n >= 0.1 and n < 1. :
        n =  (math.ceil(n*10.))/10.  
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
    if (max - min) >= 50000. :
        ticks = np.arange(min,max+5000.,10000)
        
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
    elif (max - min) >= 20. and ( 
     max - min) < 100. :
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
        ticks = np.arange(min,max+0.5, 0.05)                    
    return ticks
def maxmin(self):   
    self.kzmin = self.watmin(self.kz)
    self.kzmax = self.watmax(self.kz)
    self.sed_kzmin = self.watmin(self.kz)
    self.sed_kzmax = self.watmax(self.kz)        
    self.salmin = self.watmin(self.sal)
    self.salmax  = self.watmax(self.sal) 
    self.sed_salmin = self.sedmin(self.sal)
    self.sed_salmax = self.sedmax(self.sal)
    self.tempmin = self.watmin(self.temp)
    self.tempmax  = self.watmax(self.temp)
    self.po4max = self.watmax(self.po4) 
    self.po4min = self.watmin(self.po4)
    self.sed_po4min = self.sedmin(self.po4) 
    self.sed_po4max = self.sedmax(self.po4)  
    self.ponmax = self.watmax(self.pon) 
    self.ponmin = self.watmin(self.pon)
    self.sed_ponmin = self.sedmin(self.pon) 
    self.sed_ponmax = self.sedmax(self.pon)        
    self.donmax = self.watmax(self.don) 
    self.donmin = self.watmin(self.don)
    self.sed_donmin = self.sedmin(self.don) 
    self.sed_donmax = self.sedmax(self.don)         
    self.so4min = self.watmin(self.so4)
    self.so4max = self.watmax(self.so4)
    self.sed_so4min = self.sedmin(self.so4)
    self.sed_so4max = self.sedmax(self.so4) 
    self.o2min = self.watmin(self.o2)
    self.o2max = self.watmax(self.o2)            
    self.sed_o2min = self.sedmin(self.o2)            
    self.sed_o2max = self.sedmax(self.o2)
    self.no2min = self.watmin(self.no2)
    self.no2max = self.watmax(self.no2)
    self.sed_no2min = self.sedmin(self.no2)
    self.sed_no2max = self.sedmax(self.no2)
    self.no3min = self.watmin(self.no3)
    self.no3max = self.watmax(self.no3)
    self.sed_no3min = self.sedmin(self.no3)
    self.sed_no3max = self.sedmax(self.no3)             
    self.nh4min = self.watmin(self.nh4)
    self.nh4max = self.watmax(self.nh4)
    self.sed_nh4min = self.sedmin(self.nh4)
    self.sed_nh4max = self.sedmax(self.nh4)        
    self.simin = self.watmin(self.si)
    self.simax = self.watmax(self.si)   
    self.sed_simin = self.sedmin(self.si)
    self.sed_simax = self.sedmax(self.si)   
    self.phmin = self.watmin(self.ph)
    self.phmax = self.watmax(self.ph)   
    self.sed_phmin = self.sedmin(self.ph)
    self.sed_phmax = self.sedmax(self.ph) 

    self.fe2min = self.watmin(self.fe2)
    self.fe2max = self.watmax(self.fe2)
    self.sed_fe2min = self.sedmin(self.fe2)
    self.sed_fe2max = self.sedmax(self.fe2)      

    self.fe3min = self.watmin(self.fe3)
    self.fe3max = self.watmax(self.fe3)
    self.sed_fe3min = self.sedmin(self.fe3)
    self.sed_fe3max = self.sedmax(self.fe3) 

    self.fesmin = self.watmin(self.fes)
    self.fesmax = self.watmax(self.fes)
    self.sed_fesmin = self.sedmin(self.fes)
    self.sed_fesmax = self.sedmax(self.fes) 

    self.fes2min = self.watmin(self.fes2)
    self.fes2max = self.watmax(self.fes2)
    self.sed_fes2min = self.sedmin(self.fes2)
    self.sed_fes2max = self.sedmax(self.fes2) 
              
    self.h2smin = self.watmin(self.h2s)
    self.h2smax = self.watmax(self.h2s)
    self.sed_h2smin = self.sedmin(self.h2s)
    self.sed_h2smax = self.sedmax(self.h2s)
    
    self.mn2min = self.watmin(self.mn2)
    self.mn2max = self.watmax(self.mn2)
    self.sed_mn2min = self.sedmin(self.mn2)
    self.sed_mn2max = self.sedmax(self.mn2)       

    self.mn3min = self.watmin(self.mn3)
    self.mn3max = self.watmax(self.mn3)
    self.sed_mn3min = self.sedmin(self.mn3)
    self.sed_mn3max = self.sedmax(self.mn3) 

    self.mn4min = self.watmin(self.mn4)
    self.mn4max = self.watmax(self.mn4)
    self.sed_mn4min = self.sedmin(self.mn4)
    self.sed_mn4max = self.sedmax(self.mn4) 
    
    self.mnsmin = self.watmin(self.mns)
    self.mnsmax = self.watmax(self.mns)
    self.sed_mnsmin = self.sedmin(self.mns)
    self.sed_mnsmax = self.sedmax(self.mns) 
    
    self.mnco3min = self.watmin(self.mnco3)
    self.mnco3max = self.watmax(self.mnco3)
    self.sed_mnco3min = self.sedmin(self.mnco3)
    self.sed_mnco3max = self.sedmax(self.mnco3) 
    
    self.s0min = self.watmin(self.s0)
    self.s0max = self.watmax(self.s0)
    self.sed_s0min = self.sedmin(self.s0)
    self.sed_s0max = self.sedmax(self.s0) 
    
    self.s2o3min = self.watmin(self.s2o3)
    self.s2o3max = self.watmax(self.s2o3)
    self.sed_s2o3min = self.sedmin(self.s2o3)
    self.sed_s2o3max = self.sedmax(self.s2o3) 
      
    self.baanmin = self.watmin(self.baan)
    self.baanmax = self.watmax(self.baan)
    self.sed_baanmin = self.sedmin(self.baan)
    self.sed_baanmax = self.sedmax(self.baan)              

    self.baaemin = self.watmin(self.baae)
    self.baaemax = self.watmax(self.baae)
    self.sed_baaemin = self.sedmin(self.baae)
    self.sed_baaemax = self.sedmax(self.baae)
    
    self.bhaemin = self.watmin(self.bhae)
    self.bhaemax = self.watmax(self.bhae)
    self.sed_bhaemin = self.sedmin(self.bhae)
    self.sed_bhaemax = self.sedmax(self.bhae)        
    
    self.bhanmin = self.watmin(self.bhan)
    self.bhanmax = self.watmax(self.bhan)
    self.sed_bhanmin = self.sedmin(self.bhan)
    self.sed_bhanmax = self.sedmax(self.bhan)        
    
    self.phymin = self.watmin(self.phy)
    self.phymax = self.watmax(self.phy)
    self.sed_phymin = self.sedmin(self.phy)
    self.sed_phymax = self.sedmax(self.phy)        
    
    self.hetmin = self.watmin(self.het)
    self.hetmax = self.watmax(self.het)
    self.sed_hetmin = self.sedmin(self.het)
    self.sed_hetmax = self.sedmax(self.het)        

    self.simin = self.watmin(self.si)
    self.simax = self.watmax(self.si)
    self.sed_simin = self.sedmin(self.si)
    self.sed_simax = self.sedmax(self.si)     
    
    self.si_partmin = self.watmin(self.si_part)
    self.si_partmax = self.watmax(self.si_part)
    self.sed_si_partmin = self.sedmin(self.si_part)
    self.sed_si_partmax = self.sedmax(self.si_part)        
    
    self.phmin = self.watmin(self.ph)
    self.phmax = self.watmax(self.ph)
    self.sed_phmin = self.sedmin(self.ph)
    self.sed_phmax = self.sedmax(self.ph)          
    
    self.alkmin = self.watmin(self.alk)
    self.alkmax = self.watmax(self.alk)
    self.sed_alkmin = self.sedmin(self.alk)
    self.sed_alkmax = self.sedmax(self.alk)  
    
    self.dicmin = self.watmin(self.dic)
    self.dicmax = self.watmax(self.dic)
    self.sed_dicmin = self.sedmin(self.dic)
    self.sed_dicmax = self.sedmax(self.dic)          

    self.pco2min = self.watmin(self.pco2)
    self.pco2max = self.watmax(self.pco2)
    self.sed_pco2min = self.sedmin(self.pco2)
    self.sed_pco2max = self.sedmax(self.pco2)  

    self.ch4min = self.watmin(self.ch4)
    self.ch4max = self.watmax(self.ch4)
    self.sed_ch4min = self.sedmin(self.ch4)
    self.sed_ch4max = self.sedmax(self.ch4)    
    
    self.om_armin = self.watmin(self.om_ar)
    self.om_armax = self.watmax(self.om_ar)
    self.sed_om_armin = self.sedmin(self.om_ar)
    self.sed_om_armax = self.sedmax(self.om_ar)
    