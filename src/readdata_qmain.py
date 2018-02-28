'''
Created on 14. jan. 2018

@author: ELP
'''

import numpy.ma as ma
from netCDF4 import Dataset
import numpy as np

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
            max_num_col = None
            
        return max_num_col  
           
    def depth(self):
        try:
            depth = self.fh.variables['z'][:]  
        except KeyError : 
            depth = self.fh.variables['depth'][:]  
    
    def sed_depth(self,depth):
        print (depth)
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
        '''        
        def check_middlepoints(self),z:      
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
            print ("wrong depth array size")'''            
                          
        return depth 
    
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
                for n in range(0,xlen): #xlen                    
                    for m in range(0,ylen):  
                        # take only n's
                        # column for brom             
                        z2d.append(
                            z[n][m][numcol]) 
                z = ma.array(z2d)
                                
        z = z.flatten()   
        z = z.reshape(xlen,ylen)       
        tomask_zz = z.T  
        #mask NaNs         
        zz = ma.masked_invalid(tomask_zz) 
        return zz
    
    def time(self):
        t = self.fh.variables['time'][self.start:self.stop] 
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
              
        '''## read chosen variable and data units     
        
        data_units = self.fh.variables[index].units
        # read only part 
        
        ylen1 = len(self.depth) 
         
        xlen = len(x) '''        