import math
import os,sys
import numpy as np
from netCDF4 import Dataset
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSpinBox,QLabel,QComboBox
from matplotlib import rc
from matplotlib import style
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt4agg import (
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec


fh = Dataset('water_day.nc')

names_vars = [] 
for names,vars in fh.variables.items():
#    if names == 'z' or names == 'z2' : 
#        pass
#    elif names == 'time' or names == 'i' : 
#        pass 
    names_vars.append(names) 
    
if 'z' in names_vars:
    print ('y')
else: 
    print ('no')         
#print (names_vars[1])

#if 'kz' in fh():
#    print ('y')
#else:
#    print ('n') 
       
#try:
#    testvar = np.array(fh['i'][:])
#except AttributeError:
#    print ('var  i not found' )      
#    