'''
Created on 8. mar. 2017

@author: ELP

import os,sys
#from import Image, ImageDraw, ImageFont, ImageFilter
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSpinBox,QLabel,QComboBox
#from numpy import nan
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt4agg import (
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
#import calc_resolution
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib import style
import matplotlib.ticker as mtick
#import matplotlib as mpl
import math
from matplotlib import rc
from netCDF4 import Dataset

class Window(QtGui.QDialog):
    def __init__(self, parent=None, ):
        super(Window, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window) 
        
        #self.setWindowTitle("BROM Pictures")
        #self.setWindowIcon(QtGui.QIcon('bromlogo.png'))
        
        #app1 = QtGui.QApplication(sys.argv)
        #screen_rect = app1.desktop().screenGeometry()
        #width, height = screen_rect.width(), screen_rect.height()
        
        self.figure = plt.figure(figsize=(50, 20),# dpi=100,
                                  facecolor='white') 
             
        rc('font', **{'sans-serif' : 'Arial', #for unicode text
                           'family' : 'sans-serif'})          
        
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.qscroll = QtGui.QScrollArea(self.canvas)
        self.qscroll.setGeometry(QtCore.QRect(0, 0, 5, 500))
        self.qscroll.setFrameStyle(QtGui.QFrame.NoFrame)
        #self. qlayout.addWidget(qscroll)
        self.qscrollContents = QtGui.QWidget()

        self.qscrollLayout.setGeometry(QtCore.QRect(0, 0, 1000, 1000))

        self.qscroll.setWidget(self.qscrollContents)
        self.qscroll.setWidgetResizable(False)
        
        fname = str(QtGui.QFileDialog.getOpenFileName(self, #unicode
        'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)"))   
        

         
        layout = QtGui.QHBoxLayout()
        layout.addStretch()
        
        self.grid = QtGui.QGridLayout(self)
        self.grid.addLayout(layout, 0, 0)
        self.grid.addWidget(self.toolbar,1,0,1,1) 
        self.grid.addWidget(self.canvas, 2,0,1,5)
        self.grid.addWidget(self.qscroll, 3,0,1,5) 
        self.qscrollLayout.grid.addWidget(self.qscrollContents)                         
        self.readdata_brom(fname) 
        self.mainnn()        
              
    def readdata_brom(self,fname): 
        fh = Dataset(fname)
        self.depth = fh.variables['z'][:] 
        self.depth2 = fh.variables['z2'][:] #middle points
        self.alk =  fh.variables['Alk'][:,:,:]
        self.temp =  fh.variables['T'][:,:]
        self.sal =  fh.variables['S'][:,:]
        self.kz =  fh.variables['Kz'][:,:]
        self.time =  fh.variables['time'][:]
        fh.close()

    def mainnn(self):
        gs = gridspec.GridSpec(2, 1) 
        x = self.time #np.arange(6)
        y = self.depth #np.arange(5)
        z = self.alk
        #y_sed = self.depth_sed        
        z1 = np.array(z).flatten()
        zz = z1.reshape((len(x),len(y))).T        
        #print (self.time)
        
        X,Y = np.meshgrid(x,y)
        #X_sed,Y_sed = np.meshgrid(x,y_sed)
        ax = self.figure.add_subplot(gs[0])
        #ax2 = self.figure.add_subplot(gs[1])   
        
        cmap = plt.cm.jet #gnuplot#jet#gist_rainbow                
        cmap1 = plt.cm.rainbow #define color maps
        
        CS = ax.contourf(X,Y, zz, #levels= int_wat_levs,
                              cmap=cmap,
                              origin='lower')
        cax = self.figure.add_axes([0.92, 0.53, 0.02, 0.35])
        #CS1 = ax2.contourf(X_sed,Y_sed, zz, #levels = int_sed_levs,
        #                      cmap=cmap1,
        #                      origin='lower')
        cb = plt.colorbar(CS,cax = cax) #,ticks = wat_ticks       
        self.canvas.draw()                 
        
        #plt.show()
                
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()

    main.setStyleSheet("background-color:#d8c9c2;")
    main.show()

    sys.exit(app.exec_()) '''
from PyQt4 import QtCore, QtGui
import os,sys

#import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

qapp = QtGui.QApplication(sys.argv)
qwidget = QtGui.QWidget()
qwidget.setGeometry(QtCore.QRect(0, 0, 500, 500))
qlayout = QtGui.QHBoxLayout(qwidget)
qwidget.setLayout(qlayout)

qscroll = QtGui.QScrollArea(qwidget)
qscroll.setGeometry(QtCore.QRect(0, 0, 500, 500))
qscroll.setFrameStyle(QtGui.QFrame.NoFrame)
qlayout.addWidget(qscroll)

qscrollContents = QtGui.QWidget()
qscrollLayout = QtGui.QVBoxLayout(qscrollContents)
qscrollLayout.setGeometry(QtCore.QRect(0, 0, 1000, 1000))

qscroll.setWidget(qscrollContents)
qscroll.setWidgetResizable(True)

    
for i in xrange(5):
    qfigWidget = QtGui.QWidget(qscrollContents)
    
    fig = Figure((5.0, 4.0), dpi=100)
    canvas = FigureCanvas(fig)
    canvas.setParent(qfigWidget)
    #toolbar = NavigationToxolbar(canvas, qfigWidget)
    axes = fig.add_subplot(111)
    axes.plot([1,2,3,4])
    
    # place plot components in a layout
    plotLayout = QtGui.QVBoxLayout()
    plotLayout.addWidget(canvas)
    #plotLayout.addWidget(toolbar)
    qfigWidget.setLayout(plotLayout)
    
    # prevent the canvas to shrink beyond a point
    # original size looks like a good minimum size
    canvas.setMinimumSize(canvas.size())
    
    qscrollLayout.addWidget(qfigWidget)    
    
qscrollContents.setLayout(qscrollLayout)

qwidget.show()
exit(qapp.exec_())    