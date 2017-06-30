#!/usr/bin/python
# -*- coding: utf-8 -*-

# this comment is important to have 
# at the very first line 
# to use unicode 

'''
Created on 14. des. 2016

@author: E.Protsenko
'''
#import helpform
import math
import os,sys
import numpy as np
from netCDF4 import Dataset,num2date
from PyQt4 import QtGui, QtCore
#from PyQt4.QtGui import QSpinBox,QLabel,QComboBox,QCheckBox

from matplotlib import rc, style
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt4agg import (
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates

import readdata
import time_plot 
import dist_plot

class Window(QtGui.QDialog):
    #QDialog - the base class of dialog windows.Inherits QWidget.
    #QMainWindow - 
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # function to display the names of the window flags        
        # Qt.Window Indicates that the widget is a window, 
        # usually with a window system frame and a title bar
        # ! it is not possible to unset this flag if the widget 
        # does not have a parent.
        
        self.setWindowFlags(QtCore.Qt.Window)   
        self.setWindowTitle("BROM Pictures")
        self.setWindowIcon(QtGui.QIcon('bromlogo2.png'))
        #self.help_button.setIconSize(QtCore.QSize(50,50))         
        self.figure = plt.figure(figsize=(11.69 , 8.27), dpi=100,
                                  facecolor='white') 

        #for unicode text     
        rc('font', **{'sans-serif' : 'Arial', 
                           'family' : 'sans-serif'})  
        rc({'savefig.transparent' : True})
                
        # open file system to choose needed nc file 
        self.fname = str(QtGui.QFileDialog.getOpenFileName(self,
        'Open netcdf ', os.getcwd(), "netcdf (*.nc);; all (*)")) 
          
        totitle = os.path.split(self.fname)[1]
        self.totitle = totitle[16:-3]
            
        readdata.readdata_brom(self,self.fname)     
              
        
         
              
        # Create widgets
        self.label_choose_var = QtGui.QLabel('Choose variable:')                   
        self.time_prof_box = QtGui.QComboBox()  
        self.qlistwidget = QtGui.QListWidget()      
        self.qlistwidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)

           
                           
        self.dist_prof_button = QtGui.QPushButton() 
        self.scale_all_axes = QtGui.QCheckBox(
            "Scale:\nall columns, all time") 
         
        #self.dist_prof_checkbox = QtGui.QCheckBox(
        #self.choose_scale = QtGui.QComboBox() 
                
        self.yearlines_checkbox = QtGui.QCheckBox(
            'Draw year lines')   
        
        self.datescale_checkbox = QtGui.QCheckBox(
            'Format time axis')   
        #self.injlines_checkbox = QtGui.QCheckBox(
        #    'Draw inject lines')   
            

                  
        self.time_prof_last_year =  QtGui.QPushButton()    
        self.time_prof_all =  QtGui.QPushButton()       
                    
        self.all_year_test_button =  QtGui.QPushButton()               
        self.numcol_2d = QtGui.QSpinBox()        
            
        self.numday_box = QtGui.QSpinBox() 
        self.numday_stop_box = QtGui.QSpinBox()        
        self.textbox = QtGui.QLineEdit()  
        self.textbox2 = QtGui.QLineEdit()           
        self.fick_box = QtGui.QPushButton() 
        self.help_button = QtGui.QPushButton(' ')
        
   

        
        ## add only 2d arrays to variables list       
        ## We skip z and time since they are 1d array, 
        ## we need to know the shape of other arrays
        ## If the file includes other 1d var, it 
        ## could raise an err, such var should be skipped also
        
        self.fh =  Dataset(self.fname)
        self.names_vars = [] 
        for names,vars in self.fh.variables.items():
            if names == 'z' or names == 'z2' : 
                self.names_vars.append(names)
            elif names == 'time' or names == 'i' : 
                self.names_vars.append(names) 
            else :
                self.time_prof_box.addItem(names)
                self.names_vars.append(names)  
                
        if 'i' in self.names_vars: 
            self.dist = np.array(self.fh.variables['i'])  
                    
        # sort variables alphabetically non-case sensitive        
        self.sorted_names =  sorted(self.names_vars, key=lambda s: s.lower())  
        self.qlistwidget.addItems(self.sorted_names)
        
                     
        #Read i variable to know number of columns 
        for names,vars in self.fh.variables.items():
            if names == 'z' or names == 'z2' : 
                pass
            elif names == 'time': # or names == 'i' : 
                pass 
            else :
                if 'i' in self.names_vars:
                    #print ("we try")
                    testvar = np.array(self.fh['i'][:])      
                    break  
                
        self.fh.close()  
                        
        self.label_maxday = QtGui.QLabel('max day: '+ str(self.lentime-1))
        self.label_maxcol = QtGui.QLabel('max\ncolumn: '+ str(testvar.shape[0]-1)) 
        
        if 'i' in self.names_vars:                        
            self.numcol_2d.setRange(0, int(testvar.shape[0]-1))               
            self.numday_box.setRange(0, self.lentime-1)              
            self.numday_stop_box.setRange(0, self.lentime-1)             
            self.numday_stop_box.setValue(self.lentime-1)
            
        ### Define connection between clicking the button and 
        ### calling the function to plot figures         
                          
        #self.all_year_1d_box.currentIndexChanged.connect(
        #    self.all_year_charts)                   
        #self.numcol_2d.valueChanged.connect(
        #    self.time_profile) 
        
        self.time_prof_last_year.released.connect(self.call_print_lyr)
        self.all_year_test_button.released.connect(self.all_year_test)
        self.time_prof_all.released.connect(self.call_print_allyr)        
        self.fick_box.released.connect(self.fluxes)        
        #self.dist_prof_button.released.connect(self.dist_profile)   
                
        self.dist_prof_button.released.connect(self.call_print_dist)         
        

     
        
        #self.buttonBox.released.connect(self.setPenProperties) 
        self.help_button.released.connect(self.help_dialog)

        # Create widget 2         
        self.all_year_box = QtGui.QComboBox()
        
        # add items to Combobox         
        self.time_prof_all.setText('Time: all year')
        self.fick_box.setText('Fluxes SWI')
        self.all_year_test_button.setText('1D plot')
        self.time_prof_last_year.setText('Time: last year')               
        self.dist_prof_button.setText('Show Dist Profile')       
                         
        self.canvas = FigureCanvas(self.figure)    
        self.toolbar = NavigationToolbar(self.canvas, self) #, self.qfigWidget
        #self.canvas.setMinimumSize(self.canvas.size())
        
        ## The QGridLayout class lays out widgets in a grid          
        self.grid = QtGui.QGridLayout(self)
        
        readdata.widget_layout(self)        
        readdata.readdata2_brom(self,self.fname)   
                 
        if 'Kz'  in self.names_vars :
            readdata.calculate_ywat(self)
            readdata.calculate_ybbl(self)   
            readdata.y2max_fill_water(self)        
            readdata.depth_sed(self)
            readdata.calculate_ysed(self)
            readdata.calculate_ysed(self)
            readdata.calc_nysedmin(self)  
            readdata.y_coords(self)        
        else: 
            self.sediment = False
   
        
        readdata.colors(self)
        readdata.set_widget_styles(self) 
        
  
        self.num = 50. 
        self.dialog = QtGui.QDialog
        
    def fluxes(self): 
        plt.clf()     
        try:
            index = str(self.qlistwidget.currentItem().text())
        except AttributeError:       
            messagebox = QtGui.QMessageBox.about(
                self, "Retry",'Choose variable,please') 
            return None           
        numcol = self.numcol_2d.value() # 
        start = self.numday_box.value() 
        stop = self.numday_stop_box.value() 
        selected_items = self.qlistwidget.selectedItems()
        
        tosed = '#d3b886'
        towater = "#c9ecfd" 
        linecolor = "#1da181" 
        var1 = str(selected_items[0].text())
        
        z = np.array(self.fh.variables[var1])
        z_units = self.fh.variables[var1].units
        
        zz =  z[:,:,numcol] #1column
        
        if len(selected_items)== 1:
            
            #print (zz.shape)
            gs = gridspec.GridSpec(1,1)
            ax00 = self.figure.add_subplot(gs[0])
            ax00.set_xlabel('Julian day')   
            if self.yearlines_checkbox.isChecked() == True:
                for n in range(start,stop):
                    if n%365 == 0: 
                        ax00.axvline(n,
                        color='black',
                        linestyle = '--') 
            #if self.injlines_checkbox.isChecked()== True: 
            #        ax00.axvline(365,color='red', linewidth = 2,
            #                linestyle = '--',zorder = 10) 
            #        ax00.axvline(730,color='red',linewidth = 2,#1825 730
            #                linestyle = '--',zorder = 10)                            
        elif len(selected_items)== 2:
            gs = gridspec.GridSpec(2,1)
            
            ax00 = self.figure.add_subplot(gs[0])
            ax01 = self.figure.add_subplot(gs[1])
            ax01.set_xlabel('Julian day')  
            if self.yearlines_checkbox.isChecked() == True:
                for n in range(start,stop):
                    if n%365 == 0: 
                        ax00.axvline(n,color='black',
                        linestyle = '--') 
                        ax01.axvline(n,color='black',
                        linestyle = '--') 
                # injection   
            if self.injlines_checkbox.isChecked()== True: 
                    ax00.axvline(365,color='red', linewidth = 2,
                            linestyle = '--',zorder = 10) 
                    ax00.axvline(730,color='red',linewidth = 2,#1825 730
                            linestyle = '--',zorder = 10)  
                      
                    ax01.axvline(365,color='red', linewidth = 2,
                            linestyle = '--',zorder = 10) 
                    ax01.axvline(730,color='red',linewidth = 2,
                            linestyle = '--',zorder = 10)    
                                                                       
            #print (str(selected_items[1].text()))
            var2 = str(selected_items[1].text())
            z2_units = self.fh.variables[var2].units
            z2 = np.array(self.fh.variables[str(selected_items[1].text())])
            zz2 =  z2[:,:,numcol] #1column
            ax01.set_title(var2+', '+ z2_units)
            ax01.set_ylabel('Fluxes') #Label y axis
            ax01.set_xlim(start,stop)
            ax01.axhline(0, color='black', linestyle = '--') 
            fick2 = []
            for n in range(start,stop): 
                # take values for fluxes at sed-vat interf
                fick2.append(zz2[n][self.nysedmin])   
            fick2 = np.array(fick2)     
            ax01.plot(self.time[start:stop],fick2, linewidth = 1 ,
                        color = linecolor, zorder = 10)  
            #if self.yearlines_checkbox.isChecked() == True:
            #    for n in range(start,stop):
            #        if n%365 == 0: 
            #            ax01.axvline(n,
            #            color='black', linestyle = '--')      
            ax01.fill_between(self.time[start:stop], fick2, 0,
                               where= fick2 >= 0. , 
                               color = tosed, label= u"down" )
            ax01.fill_between(self.time[start:stop],  fick2, 0 ,
                          where= fick2 < 0.,color = towater, label=u"up")            
            ax01.set_ylim(max(fick2),min(fick2)) 
        else : 
            messagebox = QtGui.QMessageBox.about(
                self, "Retry",'Choose 1 or 2 variables,please') 
            return None  
        
        
        ax00.set_title(var1+', '+ z_units )
        
        self.figure.suptitle(str(self.totitle),fontsize=16)
        #                , fontweight='bold')
        #print (z_units, var1)
        ax00.set_ylabel('Fluxes') #Label y axis
        
        #ax00.text(0, 0, 'column{}'.format(numcol), style='italic')
        #bbox={'facecolor':'red', 'alpha':0.5,'pad':10}
        
        fick = []
        for n in range(start,stop): 
            # take values for fluxes at sed-vat interf
            fick.append(zz[n][self.nysedmin])
        fick = np.array(fick) 
        ax00.set_xlim(start,stop)
        ax00.axhline(0, color='black', linestyle = '--') 

        ax00.plot(self.time[start:stop],fick, linewidth = 1 ,
                  color = linecolor, zorder = 10)  

        ax00.fill_between(self.time[start:stop],fick,0,
                          where = fick >=0, color = tosed, label= u"down" )
        ax00.fill_between(self.time[start:stop],  fick, 0 ,
                          where= fick < 0.,color = towater, label=u"up")
        ax00.set_ylim(max(fick),min(fick)) 
        #                  where = fick > 0 ,
        #                  , interpolate=True) 
        
        #ax.fill_between(x, y1, y2, where=y2 >= y1,
        # facecolor='green', interpolate=True)         
        #rc({'savefig.transparent' : True})
        self.canvas.draw()
              

    ## function to plot figure where 
    ## xaxis - is horizontal distance between columns
    ## yaxis is depth 
    
    
    def call_print_dist(self): 
        dist_plot.dist_profile(self)
            
    def call_print_lyr(self): 
        stop = len(self.time)
        start = stop - 365
        time_plot.time_profile(self,start,stop)
        #self.time_profile(start,stop) 
            
    def call_print_allyr(self):
        
        #start = min(self.dates)
        #stop = max(self.dates)        
        start = self.numday_box.value() 
        stop = self.numday_stop_box.value()  
        #stop = len(self.time)
        #start = 0
        time_plot.time_profile(self,start,stop)
        #self.time_profile(start,stop)   
        
        
        
    def save_figure(self): 
        #does not work 
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        printer.setPageSize(QtGui.QPrinter.A9)
        printer.setColorMode(QtGui.QPrinter.Color)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(self.edit.text())
        self.render(printer)
        #plt.savefig('pdf_fig.pdf',format = 'pdf')    
        #self.figure.savefig('pic.png', format='png')
        
        
        
    def all_year_test(self):  
        plt.clf()        
        try:
            index = str(self.qlistwidget.currentItem().text())
        except AttributeError: 
            print ("Choose the variable to print ")       
            messagebox = QtGui.QMessageBox.about(self, "Retry",
                                                 'Choose variable,please') 
            return None 
         
        start = self.numday_box.value() 
        stop = self.numday_stop_box.value() 
        #index = str(self.time_prof_box.currentText())
        #print ('test all year', index) 
        data_units = self.fh.variables[index].units                
        self.figure.patch.set_facecolor('white') 
        gs = gridspec.GridSpec(3,1) 
        gs.update(left=0.3, right=0.7,top = 0.94,bottom = 0.04,
                   wspace=0.2,hspace=0.3) 
        
        ax00 = self.figure.add_subplot(gs[0]) # water         
        ax10 = self.figure.add_subplot(gs[1]) # bbl
        ax20 = self.figure.add_subplot(gs[2]) # sediment 
        
        for axis in (ax00,ax10,ax20):
            axis.yaxis.grid(True,'minor')
            axis.xaxis.grid(True,'major')                
            axis.yaxis.grid(True,'major')    
                         
        numcol = self.numcol_2d.value() # 
        # read chosen variable 
        z = np.array(self.fh.variables[index])
        z = np.array(z[:,:,numcol]) 
        #print (z.shape)
        
        ax00.set_title(index +', ' + data_units) 
        
        #Label y axis        
        ax00.set_ylabel('h, m', 
                        fontsize= self.font_txt) 
        ax10.set_ylabel('h, m', 
                        fontsize= self.font_txt)   
        ax20.set_ylabel('h, cm', 
                        fontsize= self.font_txt)
        
        ax00.set_ylim(self.y1max,0) 
        ax00.axhspan(self.y1max,0,color='#dbf0fd',
                     alpha = 0.7,label = "water" )
         
        
        ax10.set_ylim(self.y2max, self.y1max)   
        ax10.axhspan(self.y2max, self.y1max,color='#c5d8e3',
                     alpha = 0.4, label = "bbl"  )                
        
        
        ax20.set_ylim(self.ysedmax, self.ysedmin) 

        ax20.axhspan(self.ysedmin,0,
                     color='#c5d8e3',alpha = 0.4,
                     label = "bbl"  )        
        ax20.axhspan(self.ysedmax,0,
                     color='#b08b52',alpha = 0.4,
                     label = "sediment"  )
        
        
        for n in range(start,stop,10):#365
            """if (n>0 and n <60) or (n>=335 and n<365) : #"winter"
            #if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter"                               
                ax00.plot(z[n][0:self.ny2max],
                      self.depth[0:self.ny2max],
                      self.wint,alpha = self.a_w, 
                      linewidth = self.linewidth , zorder = 10) 
             
                ax10.plot(z[n][0:self.ny2max],
                      self.depth[0:self.ny2max],
                      self.wint,alpha = self.a_w, 
                      linewidth = self.linewidth , zorder = 10) 
            
                ax20.plot(z[n][self.nysedmin-1:],
                      self.depth_sed[self.nysedmin-1:],
                      self.wint, alpha = self.a_w,
                      linewidth = self.linewidth, zorder = 10) """  
            #else: 
            ax00.plot(z[n][0:self.ny2max],
                  self.depth[0:self.ny2max],
                  self.spr_aut,alpha = self.a_w, 
                  linewidth = self.linewidth , zorder = 10) 

            ax10.plot(z[n][0:self.ny2max],
                  self.depth[0:self.ny2max],
                  self.spr_aut,alpha = self.a_w, 
                  linewidth = self.linewidth , zorder = 10) 
        
            ax20.plot(z[n][self.nysedmin-1:],
                  self.depth_sed[self.nysedmin-1:],
                  self.spr_aut, alpha = self.a_w,
                  linewidth = self.linewidth, zorder = 10)                          
            #ax20.scatter(z[n][self.nysedmin-1:],
            #      self.depth_sed[self.nysedmin-1:]) 
                          
        self.canvas.draw()     
    
    
    
    '''def all_year_charts(self): 
        #messagebox = QtGui.QMessageBox.about(self, "Next time",
        #                                     'it does not work yet =(')           
        plt.clf()
        gs = gridspec.GridSpec(3,3) 
        gs.update(left=0.06, right=0.93,top = 0.94,bottom = 0.04,
                   wspace=0.2,hspace=0.1)   
        self.figure.patch.set_facecolor('white') 
        #self.figure.patch.set_facecolor(self.background) 
        #Set the background color  
        ax00 = self.figure.add_subplot(gs[0]) # water         
        ax10 = self.figure.add_subplot(gs[1]) # water
        ax20 = self.figure.add_subplot(gs[2]) # water 
 
        ax01 = self.figure.add_subplot(gs[3])          
        ax11 = self.figure.add_subplot(gs[4])
        ax21 = self.figure.add_subplot(gs[5])

        ax02 = self.figure.add_subplot(gs[6])    
        ax12 = self.figure.add_subplot(gs[7])
        ax22 = self.figure.add_subplot(gs[8])
   
        ax00.set_ylabel('Depth (m)',fontsize= self.font_txt) #Label y axis
        ax01.set_ylabel('Depth (m)',fontsize= self.font_txt)   
        ax02.set_ylabel('Depth (cm)',fontsize= self.font_txt) 
                                     
        for n in range(1,len(self.vars)):
            if (self.all_year_1d_box.currentIndex() == n) :
                
                varname1 = self.vars[n][0] 
                varname2 = self.vars[n][1] 
                varname3 = self.vars[n][2] 
                #print (n)
                z123 = readdata.read_all_year_var(self,
                            self.fname,varname1,varname2,varname3)

                z0 = np.array(z123[0])
                z1 = np.array(z123[1])
                z2 = np.array(z123[2])
                
                ax00.set_title(str(self.titles_all_year[n][0]), 
                fontsize=self.xlabel_fontsize, fontweight='bold') 
                
                ax10.set_title(str(self.titles_all_year[n][1]), 
                fontsize=self.xlabel_fontsize, fontweight='bold') 
                
                ax20.set_title(str(self.titles_all_year[n][2]), 
                fontsize=self.xlabel_fontsize, fontweight='bold')                                 
                self.num_var = n  

        for axis in (ax00,ax10,ax20,ax01,ax11,ax21,ax02,ax12,ax22):
            #water          
            axis.yaxis.grid(True,'minor')
            axis.xaxis.grid(True,'major')                
            axis.yaxis.grid(True,'major') 
                    
        ax00.set_ylim(self.y1max,0)   
        ax10.set_ylim(self.y1max,0)  
        ax20.set_ylim(self.y1max,0) 
        
        ax01.set_ylim(self.y2max, self.y2min)   
        ax11.set_ylim(self.y2max, self.y2min)  
        ax21.set_ylim(self.y2max, self.y2min) 

        ax02.set_ylim(self.ysedmax, self.ysedmin)   
        ax12.set_ylim(self.ysedmax, self.ysedmin)  
        ax22.set_ylim(self.ysedmax, self.ysedmin) 
        #
        #n0 = self.varmax(self,z0,1) #[0:self.y2max_fill_water,:].max() 
        start = 0
        stop = 365 
        #### to change""!!!!
        
        
        watmin0 = readdata.varmin(self,z0,"wattime",start,stop) 
        watmin1 = readdata.varmin(self,z1,"wattime",start,stop) 
        watmin2 = readdata.varmin(self,z2,"wattime",start,stop)          

        watmax0 = readdata.varmax(self,z0,"wattime",start,stop) 
        watmax1 = readdata.varmax(self,z1,"wattime",start,stop)
        watmax2 = readdata.varmax(self,z2,"wattime",start,stop)  
                 
        sed_min0 = readdata.varmin(self,z0,"sedtime",start,stop) 
        sed_min1 = readdata.varmin(self,z1,"sedtime",start,stop) 
        sed_min2 = readdata.varmin(self,z2,"sedtime",start,stop)    

        sed_max0 = readdata.varmax(self,z0,"sedtime",start,stop) 
        sed_max1 = readdata.varmax(self,z1,"sedtime",start,stop)         
        sed_max2 = readdata.varmax(self,z2,"sedtime",start,stop)         
        
        if self.num_var == 5: #pH 
            watmax1 = 9
            watmin1 = 6.5
        elif self.num_var == 2: #po4, so4
            watmax0 = 3  
            #watmax1 = 7000.          
            #watmin1 = 4000.            
        else:
            pass
                    
        
        self.m0ticks = readdata.ticks(watmin0,watmax0)
        self.m1ticks = readdata.ticks(watmin1,watmax1)
        self.m2ticks = readdata.ticks(watmin2,watmax2)  
        
        self.sed_m0ticks = readdata.ticks(sed_min0,sed_max0)
        self.sed_m1ticks = readdata.ticks(sed_min1,sed_max1)
        self.sed_m2ticks = readdata.ticks(sed_min2,sed_max2)                 
        #for axis in (ax00,ax10,ax20):             
        
        ax00.set_xlim(watmin0,watmax0)   
        ax01.set_xlim(watmin0,watmax0)         
        ax02.set_xlim(sed_min0,sed_max0)
        
        ax10.set_xlim(watmin1,watmax1)   
        ax11.set_xlim(watmin1,watmax1)         
        ax12.set_xlim(sed_min1,sed_max1)         
         
        ax20.set_xlim(watmin2,watmax2)   
        ax21.set_xlim(watmin2,watmax2)         
        ax22.set_xlim(sed_min2,sed_max2) 
                
        ax10.set_xlim(watmin1,watmax1)   
        ax11.set_xlim(watmin1,watmax1)         
        #ax12.set_xlim(sed_min1,sed_max1) 
                     
        ax20.set_xlim(watmin2,watmax2)   
        ax21.set_xlim(watmin2,watmax2)         
        #ax22.set_xlim(sed_min2,sed_max2)                  
        #water

                     
        ax00.fill_between(
                        self.m0ticks, self.y1max, 0,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w
        ax01.fill_between(
                        self.m0ticks, self.y2min_fill_bbl ,self.y2min,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w    
        ax01.fill_between(self.m0ticks, self.y2max, self.y2min_fill_bbl,
                               facecolor= self.bbl_col1, alpha=self.a_bbl) 
            
        ax02.fill_between(self.sed_m0ticks,self.ysedmin_fill_sed,-10,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)          
        ax02.fill_between(self.sed_m0ticks, self.ysedmax, self.ysedmin_fill_sed,
                               facecolor= self.sed_col1, alpha=self.a_s)          
        
            #axis.fill_between(self.xticks, self.y2max, self.y2min_fill_bbl,
            #                   facecolor= self.bbl_color, alpha=self.alpha_bbl)        
            
        ax10.fill_between(
                        self.m1ticks, self.y1max, 0,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w
        
        ax11.fill_between(
                        self.m1ticks, self.y2min_fill_bbl ,self.y2min,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w    
        ax11.fill_between(self.m1ticks, self.y2max, self.y2min_fill_bbl,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)      
        ax12.fill_between(self.sed_m1ticks,self.ysedmin_fill_sed,-10,
                               facecolor= self.bbl_col1, alpha=self.a_bbl) 
        ax12.fill_between(self.sed_m1ticks, self.ysedmax, self.ysedmin_fill_sed,
                              facecolor= self.sed_col1, alpha=self.a_s)        
        ax20.fill_between(
                        self.m2ticks, self.y1max, 0,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w
        
        ax21.fill_between(
                        self.m2ticks, self.y2min_fill_bbl ,self.y2min,
                        facecolor= self.wat_col1, alpha=0.1 ) #self.a_w    
        ax21.fill_between(self.m2ticks, self.y2max, self.y2min_fill_bbl,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)     
        ax22.fill_between(self.sed_m2ticks,self.ysedmin_fill_sed,-10,
                               facecolor= self.bbl_col1, alpha=self.a_bbl)                         
        ax22.fill_between(self.sed_m2ticks, self.ysedmax, self.ysedmin_fill_sed,
                               facecolor= self.sed_col1, alpha=self.a_s) 
                            

        
                
        for n in range(0,3): #365
            if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter" 
                linewidth = self.linewidth
                                  
                ax00.plot(z0[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth , zorder = 10) 
                ax10.plot(z1[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth , zorder = 10)
                ax20.plot(z2[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 )  
                
                ax01.plot(z0[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
                ax11.plot(z1[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth , zorder = 10)
                ax21.plot(z2[n],self.depth,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
    
                ax02.plot(z0[n],self.depth_sed,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
                ax12.plot(z1[n],self.depth_sed,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 )
                ax22.plot(z2[n],self.depth_sed,self.wint,alpha = 
                          self.a_w, linewidth = linewidth, zorder = 10 ) 
            elif n >= 150 and n < 249: #"summer"
                ax00.plot(z0[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
                ax10.plot(z1[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )
                ax20.plot(z2[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )  
                
                ax01.plot(z0[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
                ax11.plot(z1[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )
                ax21.plot(z2[n],self.depth,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
    
                ax02.plot(z0[n],self.depth_sed,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
                ax12.plot(z1[n],self.depth_sed,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 )
                ax22.plot(z2[n],self.depth_sed,self.summ,alpha = 
                          self.a_s, linewidth = linewidth, zorder = 10 ) 
            else : #"autumn and spring"
                ax00.plot(z0[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 ) 
                ax10.plot(z1[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 )
                ax20.plot(z2[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 )  
                
                ax01.plot(z0[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 ) 
                ax11.plot(z1[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 )
                ax21.plot(z2[n],self.depth,self.spr_aut,alpha = 
                          self.a_aut, linewidth = linewidth, zorder = 10 ) 
    
                ax02.plot(z0[n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut, zorder = 10) 
                ax12.plot(z1[n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut, zorder = 10)
                ax22.plot(z2[n],self.depth_sed,self.spr_aut,
                          alpha = self.a_aut, zorder = 10)      
     
        self.canvas.draw()  ''' 
        
          
    def help_dialog(self):
        messagebox = QtGui.QMessageBox.about(
                self, "Help",
                ' <b> Help Dialog</b> <br /> '
                ' Time: all year <br />'
                ' Time: last year  <br />'
                ' new line<br />'
                ' new line<br />'
                ' new line<br />'
                ' new line<br />'
                ' new line<br />'
                ' new line<br />'
                ) 
        
        
        #self.dialog = PropertiesDlg(self)
        #self.dialog.setWindowTitle("Title") 
        
        #self.dialog.button.setChecked()   
        #self.value = None
        '''if self.dialog.exec_():
            
            self.checker = self.dialog.button
            if self.dialog.button.isChecked(): 
                self.value = True
            else : 
                self.value = False              
            #if self.checker.isChecked():                
            #    print ('1') 
            #else:
            #    print("Nope")
        return self.value '''
    
class PropertiesDlg(QtGui.QDialog): 
    def __init__(self, parent=None):
        super(PropertiesDlg, self).__init__(parent)
        
        
        #QMessageBox.about(self, "About Image Changer",
        '''         """<b>Image Changer</b> v %s
                 <p>Copyright &copy; 2007 Qtrac Ltd.
                 All rights reserved.
                <p>This application can be used to perform
                simple image manipulations.
                <p>Python %s - Qt %s - PyQt %s on %s""" % (
            __version__, platform.python_version(),
            QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))'''
        
        
        #window = Window(self)
        #print (self.Window.value)
        #self.okButton = QtGui.QPushButton("&OK")
        #self.cancelButton = QtGui.QPushButton("Cancel")
        #self.button = QtGui.QCheckBox('test') 
        #if self.value == True or None:
        #    self.dialog.button.setChecked()
        #layout = QtGui.QGridLayout()
        #layout.addWidget(self.button, 0, 0, 1, 1) 
        #layout.addWidget(self.okButton, 1, 0, 1, 1) 
        
        #layout.addWidget(self.cancelButton, 1, 1, 1, 1)         
        #layout.addWidget(self.buttonBox, 3, 0, 1, 3)
        #self.setLayout(layout) 
        #self.okButton.released.connect(self.accept)
        #self.cancelButton.released.connect(self.reject)
        
        #if self.button.isChecked():
        #    #self.button_event()
        #    print('is checked')
            
        #def button_event(self):
        #    print ('button event')
        #    self.value1 = True 
        #    return self.value1                
        
                       
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()
    main.setStyleSheet("background-color:#d8c9c2;")

    main.show()
    #PySide.QtCore.Qt.WindowFlags
    sys.exit(app.exec_()) 
