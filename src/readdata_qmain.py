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
            max_num_col = testvar.shape[0]-1
        else :
            max_num_col = 0
            
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
                y2max = depth2[n] 
                ny2max = n
                break 
                                                  
        return y2max,ny2max      
            
    
    def depth_sed(self,depth,y2max):
        depth_sed = (depth-y2max)*100  
        return depth_sed 
    
    def units(self):               
        return  np.array(
        self.fh.variables[self.index].units) 
    
    def variable(self,start,stop): 
        z =  np.array(self.fh.variables[self.index][start:stop]) 
        xlen = stop - start 
        ylen = self.leny()
        x_range = range(0,xlen) 
        y_range = range(0,ylen)
        
        # check the column to plot  
        if z.ndim > 2:    
            ncol = 0 
            # self.numcol_2d.value()    
            # check if we have 2D array 
            if z.shape[2] > 1:  
                z = ma.array(
                [z[n][m][ncol] for n in x_range \
                       for m in y_range]
                )
                                
        z = z.flatten().reshape(xlen,ylen).T             
        zz = ma.masked_invalid(z) 
        return zz
    
        
    def time(self,start,stop):
        t = self.fh.variables['time'][start:stop] 
        return t
    
    def time_units(self):
        t = self.fh.variables['time'].units
        return t
            
    def lentime(self):
        time = self.fh.variables['time'][:] 
        return len(time)   
    
    def leny(self):
        depth = self.depth()
        return len(depth)
    
    def close(self):
        self.fh.close()
        self.fh = None  
        
def format_time_axis(self, xaxis,xlen,X_arr): 
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