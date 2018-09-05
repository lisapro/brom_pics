'''
Created on 14. jan. 2018

@author: ELP
'''
from netCDF4 import num2date 
import numpy.ma as ma
from netCDF4 import Dataset
import numpy as np
import matplotlib.dates as mdates
class ReadVar:
    def __init__(self,filename,
                 index = None,start = None,
                  stop = None):
        
        self.index = index
        self.filename = filename   
        self.fh =  Dataset(filename)
        self.start = start
        self.stop = stop
        #self.fh.close()
        
    def get_variables_list(self):             
        ''' Gets the list of variables,
        and sort it rewrite it with regular 
        expressions, use variables.keys()'''        
        names_vars = [] 
        for names,vars in self.fh.variables.items():
            names_vars.append(names)  
        flux_list = []
        sink_list = []
        other_list = []
       
        for name in names_vars: 
            if name[:4] == 'fick':
                flux_list.append(name) 
            elif name[:4] == 'sink':
                sink_list.append(name)
            elif name not in ['z','z2','kz','time','i']:    
                other_list.append(name)
        sorted_names =  sorted(other_list,
                    key=lambda s: s.lower())  
        sorted_names = (sorted_names + 
                    flux_list + sink_list)              
        return sorted_names        
    
    def max_numcol(self):
        if 'i' in self.fh.variables.keys() :
            testvar = np.array(self.fh['i'][:]) 
            max_num_col = testvar.shape[0]
        else :
            max_num_col = 1
            
        return max_num_col  
           
    def depth(self):
        try:
            depth = self.fh.variables['z'][:]  
        except KeyError : 
            depth = self.fh.variables['depth'][:]
        return depth 
          
    def y_watmax(self):
        try: 
            depth2 = self.fh.variables['z2'][:]
            kz = self.fh.variables['Kz'][:]
        except:
            return None,None     
               
        for n,item in enumerate(depth2):
            if kz[1,n,0] == 0:
                print ('in')
                y2max = depth2[n] 
                ny2max = n
                break 
                                                  
        return y2max,ny2max      
        
     
   
                        
    
    
    def depth_sed(self,depth,y2max):
        depth_sed = (depth - y2max)*100        
        return depth_sed 
        '''
        to_float = []
        for item in self.depth:
            to_float.append(float(item)) #make a list of floats from tuple 
        depth_sed = [] # list for storing final depth data for sediment 
        v=0  
        for i in to_float:
            v = (i- self.y2max)*100  #convert depth from m to cm
            depth_sed.append(v)
            self.depth_sed= depth_sed        
        pass
              
        
        def check_middlepoints(self):      
        # check if the variable is defined on
        # middlepoints  
        
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
                          
        return depth '''
    
    def units(self):               
        return  np.array(
        self.fh.variables[self.index].units) 
    
    def variable(self):     
        z =  np.array(self.fh.variables[self.index][self.start:self.stop]) 
        xlen = self.lentime()
        ylen = self.leny()
        
        # check the column to plot  
        if z.ndim > 2:    
            numcol = 0 
            # self.numcol_2d.value() 
            # to change later  
            z2d = []        
            # check if we have 2D array 
            if z.shape[2] > 1:  
                z2d = [z[n][m][numcol] for n in range(0,xlen) \
                       for m in ranage(0,ylen)]
                z = ma.array(z2d)
                #for n in range(0,xlen): #xlen                    
                #    for m in range(0,ylen):  
                        # take only n's           
                #        z2d.append(
                #            z[n][m][numcol]) 
                
                                
        z = z.flatten()   
        z = z.reshape(xlen,ylen)       
        tomask_zz = z.T  
        #mask NaNs         
        zz = ma.masked_invalid(tomask_zz) 
        return zz
    
    def time(self):
        t = self.fh.variables['time'][self.start:self.stop] 
        return t
    
    def time_units(self):
        t = self.fh.variables['time'].units
        return t
            
    def lentime(self):
        time = self.time()
        return len(time)   
    
    def leny(self):
        depth = self.depth()
        return len(depth)
    
    def close(self):
        self.fh.close()
        self.fh = None  
        
def format_time_axis(self, xaxis,xlen,X_arr): 
    print (self.time_units)
    X = num2date(X_arr,units = self.time_units)   
    xaxis.xaxis_date()
    if xlen > 365 and xlen < 365*5 : 
        xaxis.xaxis.set_major_formatter(
            mdates.DateFormatter('%m/%Y'))  
    elif xlen >= 365*5 :
        xaxis.xaxis.set_major_formatter(
            mdates.DateFormatter('%Y'))          
    elif xlen <= 365: 
        xaxis.xaxis.set_major_formatter(
            mdates.DateFormatter('%b'))
    return X                     