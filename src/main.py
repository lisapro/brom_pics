#!/usr/bin/python
# Filename: readfile.py
# Import standard (i.e., non GOTM-GUI) modules.
import os,sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QSpinBox,QLabel
#from numpy import nan
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import readdata,colors
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib import style
import matplotlib.ticker as mtick
import matplotlib as mpl


class Window(QtGui.QDialog):
     
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
   
        self.setWindowTitle("BROM Pictures")
        self.setWindowIcon(QtGui.QIcon('bromlogo.png'))
        #self.setWindowState(QtCore.Qt.WindowMaximized)
        self.figure = plt.figure(figsize = (30,20),facecolor='white')
        
        #text(1, 1, 's', fontdict=None, )
        #self.ax.set_text('s')
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        fname = unicode(QtGui.QFileDialog.getOpenFileName(self,
        'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)"))   
        readdata.readdata_brom(self,fname) 
        colors.colors(self)   
        readdata.calculate_watmax(self)
        readdata.calculate_bblmax(self)       
        readdata.y2min(self)
        
        readdata.depth_sed(self) #calc depthes in cm
        readdata.calculate_sedmin(self)
        #readdata.calculate_sedmax(self)  
       
        self.time_prof_box = QtGui.QComboBox()
        for i in self.var_names_profile:
            self.time_prof_box.addItem(str(i))
        self.time_prof_box.currentIndexChanged.connect(self.time_profile)        
        
        self.all_year_box = QtGui.QComboBox()
        for i in self.var_names_charts_year:
            self.all_year_box.addItem(str(i))
        self.all_year_box.currentIndexChanged.connect(self.all_year_charts) 
                
        #self.time_prof_box.addItems(vars)
        #self.button1.setStyleSheet('QPushButton {background-color: #faebd7;}')      
        #self.button1.clicked.connect(self.plot1) #Plot PO4,SO4,o2     
           
      

        # set the layout
        layout = QtGui.QGridLayout()
        layout.addWidget(self.toolbar,0,1,1,7) 
        layout.addWidget(self.time_prof_box,0,4,1,1)   
        layout.addWidget(self.all_year_box,0,5,1,1)         
                                              
        layout.addWidget(self.canvas,2,1,1,8)#pos y,pos x,len y,lenx         
        #layout.addWidget(self.button1,3,1,1,1) 
               
        self.setLayout(layout)        
        
      
    '''def showDialog(self):   
        fname = unicode(QtGui.QFileDialog.getOpenFileName(self,
        'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)"))   
        readdata.readdata_brom(self,fname)'''         

    def time_profile(self):
        readdata.y_coords(self)
        readdata.calculate_watmax(self)
        readdata.vars(self)
        readdata.calculate_bblmax(self)
        plt.clf()
        for n in range(1,len(self.var_names_profile)):
            if (self.time_prof_box.currentIndex() == n) :
                z = self.vars[n] #self.po4
                title = self.time_prof_box.currentText() 
                  
                                 
        gs = gridspec.GridSpec(2, 1) 
        x = self.time #np.arange(6)
        y = self.depth #np.arange(5)
        y_sed = self.depth_sed
        
        z1 = np.array(z).flatten()
        zz = z1.reshape((len(x),len(y))).T
        
        watmin = np.trunc(zz[0:self.ny1max,:].min())   #np.round       
        watmax = np.ceil(zz[0:self.ny1max,:].max())
        var_sed_min = np.trunc(zz[self.ny1max:,0:len(x)].min())
        var_sed_max = np.ceil(zz[self.ny1max:len(y),0:len(x)].max())  
        readdata.sedmax(self,zz)
        #if  var_sed_max <= 1:
        #    var_sed_max = zz[self.ny1max:35,0:365].max() 
        #    var_sed_min = 0 
         
        #print (watmin) 
        #np.ceil(zz[self.ny1max:,:].max())
        '''def calculate_watmax(self):
            for n in range(0,(len(self.depth2))):#-1
                if self.depth2[n+1] - self.depth2[n] >= 0.5:
                    pass
                elif self.depth2[n+1] - self.depth2[n] < 0.50:    
                    self.y1max = (self.depth2[n])
                    self.ny1max = n                               
                    break'''                 
                              
        X,Y = np.meshgrid(x,y)
        X_sed,Y_sed = np.meshgrid(x,y_sed)
        ax = self.figure.add_subplot(gs[0])
        ax2 = self.figure.add_subplot(gs[1])        
        #self.figure, (ax, ax2) = plt.subplots(2, 1, sharex=True)
        #f.set_size_inches(11.69,8.27)

        ax.set_title(title)
        ax.set_ylim(self.y1max,0)       
        ax2.set_ylim(self.ysedmax,self.ysedmin)
        ax.set_xlim(0,len(x))
        num = 20    
        #print ('watmax',watmax,np.ceil(watmax),np.round(watmax)) 
               
        cmap = plt.cm.jet #gnuplot#jet#gist_rainbow
        clevs = np.linspace(watmin-(-watmin+watmax)/5,
                            watmax+(-watmin+watmax)/5,num=num)
        cmap1 = plt.cm.rainbow #define color maps
        clevs1 = np.linspace(var_sed_min-(-var_sed_min+var_sed_max)/5,
                             var_sed_max+(-var_sed_min+var_sed_max)/5,
                             num = num)
        
        
        CS = ax.contourf(X,Y, zz, 50,#levels= clevs
                              cmap=cmap,
                              origin='lower')
        
        CS1 = ax2.contourf(X_sed,Y_sed, zz, 50, #levels= clevs1
                              cmap=cmap1,
                              origin='lower')
        
        cax = self.figure.add_axes([0.92, 0.51, 0.02, 0.35])#x,y,thick,length
        cax1 = self.figure.add_axes([0.92, 0.1, 0.02, 0.35])#x,y,thick,length
        
        plt.colorbar(CS,cax = cax)
        plt.colorbar(CS1,cax = cax1 )
        #cbar = CS.colorbar(cax, )
        #cbar.ax.set_yticklabels(['< -1', '0', '> 1'])# vertically oriented colorbar
        #self.figure.suptitle('Berre lagoon', fontsize=25, fontweight='bold')
        #f.savefig('test.png', dpi=300) 
        #plt.show()   

        self.canvas.draw() 
    def all_year_charts(self):
        readdata.var_year(self)
        readdata.calculate_watmax(self) 
        #readdata.calculate_nwatmax(self)
        readdata.calculate_bblmax(self)
        #readdata.calculate_nbblmax(self)
        readdata.calculate_watmax(self)
        readdata.y_coords(self)
        
        
        
        plt.clf()
        gs = gridspec.GridSpec(3,3) 
        gs.update(left=0.06, right=0.93,top = 0.94,bottom = 0.04,
                   wspace=0.2,hspace=0.1)   
        #self.figure.patch.set_facecolor(self.background) 
        #Set the background color  
        ax00 = self.figure.add_subplot(gs[0]) # water         
        ax10 = self.figure.add_subplot(gs[1])
        ax20 = self.figure.add_subplot(gs[2])
        
        ax01 = self.figure.add_subplot(gs[3]) # water         
        ax11 = self.figure.add_subplot(gs[4])
        ax21 = self.figure.add_subplot(gs[5])

        ax02 = self.figure.add_subplot(gs[6]) # water         
        ax12 = self.figure.add_subplot(gs[7])
        ax22 = self.figure.add_subplot(gs[8])
                             
        for n in range(1,len(self.var_names_charts_year)):
            if (self.all_year_box.currentIndex() == n) :
                z0 = np.array(self.vars_year[n][0])
                z1 = np.array(self.vars_year[n][1]) #self.po4
                z2 = np.array(self.vars_year[n][2])
                title0 = self.var_titles_charts_year[n][0] 
                title1 = self.var_titles_charts_year[n][1] 
                title2 = self.var_titles_charts_year[n][2]
                
        ax00.set_title(title0) 
        ax10.set_title(title1)
        ax20.set_title(title2)

        for axis in (ax00,ax10,ax20,ax01,ax11,ax21,ax02,ax12,ax22):   #water          
            axis.yaxis.grid(True,'minor')
            axis.xaxis.grid(True,'major')                
            axis.yaxis.grid(True,'major') 
                    
        ax00.set_ylim(self.y1max,0)   
        ax10.set_ylim(self.y1max,0)  
        ax20.set_ylim(self.y1max,0) 
        
        ax01.set_ylim(self.y2max, self.y1max)   
        ax11.set_ylim(self.y2max, self.y1max)  
        ax21.set_ylim(self.y2max, self.y1max) 

        ax02.set_ylim(self.ysedmax, self.ysedmin)   
        ax12.set_ylim(self.ysedmax, self.ysedmin)  
        ax22.set_ylim(self.ysedmax, self.ysedmin) 
        
                
        for n in range(0,len(self.time)):
            if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter"                  
                ax00.plot(z0[0][n],self.depth,self.wint,alpha = self.a_w) 
                ax10.plot(z1[0][n],self.depth,self.wint,alpha = self.a_w)
                ax20.plot(z2[0][n],self.depth,self.wint,alpha = self.a_w)  
                
                ax01.plot(z0[0][n],self.depth,self.wint,alpha = self.a_w) 
                ax11.plot(z1[0][n],self.depth,self.wint,alpha = self.a_w)
                ax21.plot(z2[0][n],self.depth,self.wint,alpha = self.a_w) 
    
                ax02.plot(z0[0][n],self.depth_sed,self.wint,alpha = self.a_w) 
                ax12.plot(z1[0][n],self.depth_sed,self.wint,alpha = self.a_w)
                ax22.plot(z2[0][n],self.depth_sed,self.wint,alpha = self.a_w) 
            elif n >= 150 and n < 249: #"summer"
                ax00.plot(z0[0][n],self.depth,self.summ,alpha = self.a_s) 
                ax10.plot(z1[0][n],self.depth,self.summ,alpha = self.a_s)
                ax20.plot(z2[0][n],self.depth,self.summ,alpha = self.a_s)  
                
                ax01.plot(z0[0][n],self.depth,self.summ,alpha = self.a_s) 
                ax11.plot(z1[0][n],self.depth,self.summ,alpha = self.a_s)
                ax21.plot(z2[0][n],self.depth,self.summ,alpha = self.a_s) 
    
                ax02.plot(z0[0][n],self.depth_sed,self.summ,alpha = self.a_s) 
                ax12.plot(z1[0][n],self.depth_sed,self.summ,alpha = self.a_s)
                ax22.plot(z2[0][n],self.depth_sed,self.summ,alpha = self.a_s) 
            else : #"autumn and spring"
                ax00.plot(z0[0][n],self.depth,self.spr_aut,alpha = self.a_aut) 
                ax10.plot(z1[0][n],self.depth,self.spr_aut,alpha = self.a_aut)
                ax20.plot(z2[0][n],self.depth,self.spr_aut,alpha = self.a_aut)  
                
                ax01.plot(z0[0][n],self.depth,self.spr_aut,alpha = self.a_aut) 
                ax11.plot(z1[0][n],self.depth,self.spr_aut,alpha = self.a_aut)
                ax21.plot(z2[0][n],self.depth,self.spr_aut,alpha = self.a_aut) 
    
                ax02.plot(z0[0][n],self.depth_sed,self.spr_aut,alpha = self.a_aut) 
                ax12.plot(z1[0][n],self.depth_sed,self.spr_aut,alpha = self.a_aut)
                ax22.plot(z2[0][n],self.depth_sed,self.spr_aut,alpha = self.a_aut)                                 
        self.canvas.draw() 
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()
    main.setStyleSheet("background-color:#d8c9c2;")
    main.show()
    
    sys.exit(app.exec_()) 
