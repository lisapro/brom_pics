'''
Created on 22. mar. 2017

@author: ELP
'''
from netCDF4 import Dataset
import os 
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSpinBox,QLabel,QComboBox


fname = 'BROM_Baltic_out_10y.nc'

#str(QtGui.QFileDialog.getOpenFileName('Open netcdf ', os.getcwd(), 
#                                              "netcdf (*.nc);; all (*)"))
fh = Dataset(fname)

i = 0
#def readfile(name, varname):  
#    name = fh.variables[varname][:]
#    return name, varname 


    
print (varnames_list)    
            #self.time_prof_box.addItem(str(names))




'''
for name, variable in fh.variables.items():   
    #name = variable # fh.variables['z'][:] # [{}.format(name)] 
    print (variable)        #name , variable 
    #for attrname in variable.ncattrs():
    #    print (attrname[0], '----')
    #print("{} -- {}".format(attrname)) #, getattr(variable, attrname)'''