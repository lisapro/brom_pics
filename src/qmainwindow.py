#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 8. jan. 2018

@author: ELP
'''

import sys
import numpy as np
from PyQt5.QtWidgets import (QMainWindow,QAction,qApp,QFileDialog,
                QFrame,QSplitter,QLabel,QActionGroup,QSpinBox,QMessageBox,
                QApplication,QTextEdit,QListWidget,QGroupBox,QAbstractItemView,
                QLineEdit,QCheckBox,QGridLayout, QDockWidget,QComboBox,QVBoxLayout,QRadioButton)
from PyQt5.QtGui import QIcon,QKeySequence,QImageWriter,QPixmap
from PyQt5.QtCore import QSettings,QVariant,QSize,QPoint,QTimer,Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
from netCDF4 import num2date 
from tkinter.filedialog import askopenfilename,askdirectory
from matplotlib import gridspec

import os
import readdata_qmain
import path
__version__ = "1.0.0"


class Window(QMainWindow):
    def __init__(self,parent = None):
        super(Window,self).__init__(parent)

        self.initUI()
         
    '''def loadInitialFile(self):
        settings = QSettings()
        fname = (settings.value("LastFile").toString())
        if fname and QFile.exists(fname):
            self.loadFile(fname) '''     
              
    def initUI(self):
                   
        self.filename = None
        
        self.figure = plt.figure(figsize=(7.69 , 5.27),
                        facecolor='None',edgecolor='None')
        self.canvas = FigureCanvas(self.figure)  
        self.setCentralWidget(self.canvas)
        
        logDockWidget = QDockWidget("List of Variables", self)
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
         Qt.RightDockWidgetArea)
        
        self.listWidget = QListWidget()
        self.listWidget.setFocusPolicy(Qt.ClickFocus)
        self.listWidget.setSelectionMode(
            QAbstractItemView.ExtendedSelection)        
        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea,
                            logDockWidget)
        self.printer = None
               
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(
            QFrame.StyledPanel|QFrame.Sunken)
        
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)
        

        fileOpenAct = self.createAction("Open",
                    self.openFile,QKeySequence.Open,None,
                    "Open file")
        fileSaveAct = self.createAction("SaveAs",
                    self.fileSaveAs,QKeySequence.Save,None,
                    "Save figure")
        
        fileQuitAct = self.createAction("&Quit",
                    self.close,"Ctrl+Q", "filequit",
                    "Close the application") 
        
        alltimeicon = r'img\icon.png'       
        pltAllTimeAct = self.createAction("All time",
                    self.callAllTime,icon = alltimeicon,
                    tip = "Click to Plot All time") 
             
        editZoomAct = self.createAction("&Zoom...",
                    self.editZoom,"Alt+Z","editzoom",
                    tip = "Zoom the image")
        editCmapAct = self.createAction("Change Color map",
                    self.changeCmap,
                    tip = "Change Colormap")
        
        self.SedInFileAct = self.createAction(
            "Use sediment Subplot", #slot = self.plotTime,
            tip = "Use sediment Subplot", checkable= True) 
        
        self.SedInFileAct.setChecked(True)     
                  
        self.editCmapLimsAct = self.createAction(
            "Manual Cmap limits",None, "Ctrl+M",
            None,"Use manual cmap limits", True)  
         
        self.interpCmapLimsAct = self.createAction(
            "Dont Interploate Cmap limits",None, "Ctrl+I",
            None,"Don't Interpolate Cmap limits", True)  
              
        self.limsAllCols = self.createAction(
            "All columns Cmap limits",None, None,
            None,"Scale: all columns, all time", True)  
        
        self.showIceAct = self.createAction(
            "Show Ice Thickness",None, None,
            None,"Scale: all columns, all time", True)   

        self.yearLinesAct = self.createAction(
            'Draw year lines',None, None, None,
            'Draw year lines', True)  
                
        self.formatTimeAct = self.createAction(
            'Format time axis',None, None, None,
            'Format time axis', True)
        self.formatTimeAct.setChecked(True) 
        
        self.intepolateAct = self.createAction(
            'Interpolate data',None, None, None,
            'Interpolate data', True)  
                        
        menubar = self.menuBar()
        
        filemenu = self.addMultipleAction(
        'File', 
        [fileOpenAct,fileSaveAct,fileQuitAct],
                        menubar.addMenu)
        
        editMenu = self.addMultipleAction(
        'Edit',
        [editCmapAct,editZoomAct],
        menubar.addMenu)

        proprtsMenu = self.addMultipleAction(
        'Properties',
        [self.editCmapLimsAct,self.SedInFileAct,self.interpCmapLimsAct,            
         self.limsAllCols,self.formatTimeAct,
         self.intepolateAct,self.yearLinesAct],
        menubar.addMenu)
 
        
        self.toolbar1= self.addOneAction('Plot',pltAllTimeAct,self.addToolBar) 
        self.toolbar2 = self.addToolBar('Properties')   
        self.makeToolbar() 
              

     
        self.show()
    
    
    def makeToolbar(self):
        
        self.createCmapLimitsGroup()
        self.createDistGroup()
        self.createTimeGroup()
        self.createRadioButtonsGroup()
        self.toolbar2.addWidget(self.cmap_groupBox)    
        self.toolbar2.addWidget(self.dist_groupBox)   
        self.toolbar2.addWidget(self.time_groupBox)
        self.toolbar2.addWidget(self.radio_groupBox)
        
        
    def updateToolbar(self):
        self.toolbar2.clear()
        self.makeToolbar()
         
    def createCmapLimitsGroup(self):
       
        self.cmap_groupBox = QGroupBox("Colour map limits ")
          
        self.label_minwater = QLabel('min:')        
        self.label_maxwater = QLabel('max:')                
        self.box_minwater = QLineEdit()    
        self.box_maxwater = QLineEdit() 
        self.box_minsed = QLineEdit() 
        self.box_maxsed = QLineEdit() 
        self.cmap_box = QComboBox()
        self.cmap_box.addItems(sorted(m for m in plt.cm.datad ))    
        self.cmap_box.setCurrentIndex(5)
            
        grd = QGridLayout(self.cmap_groupBox) 
                
        grd.addWidget(self.label_minwater,1,0,1,1)
        grd.addWidget(self.box_minwater,1,1,1,1) 
        grd.addWidget(self.box_minsed,2,1,1,1)
               
        grd.addWidget(self.label_maxwater,1,2,1,1)
        grd.addWidget(self.box_maxwater,1,3,1,1)         
        grd.addWidget(self.box_maxsed,2,3,1,1) 

        grd.addWidget(self.cmap_box,1,4,1,1) 
        
        return self 
    
    def createDistGroup(self):  
            
        self.dist_groupBox = QGroupBox("Distance axis")               
        dist_grid = QGridLayout(self.dist_groupBox)
        
        self.col_label = QLabel('Column: ')
        self.numcol_2d = QSpinBox() 
        self.maxcol_label = QLabel('Max (from 0): ')

        try:
            self.nmaxcol_label = QLabel(str(
                        self.max_num_col)) 
            if self.max_num_col > 0:
                self.numcol_2d.setRange(0,self.max_num_col)  
        except AttributeError: 
            self.nmaxcol_label = QLabel(' ') 
                                
        dist_grid.addWidget(self.col_label,0,0,1,1) 
        dist_grid.addWidget(self.numcol_2d,1,0,1,1) 
        dist_grid.addWidget(self.maxcol_label,0,1,1,1)         
        dist_grid.addWidget(self.nmaxcol_label,1,1,1,1) 

        return self 
    
    def createTimeGroup(self):  
     
        #self.last_year_button = QtWidgets.QPushButton('last year')    
        self.time_groupBox = QGroupBox("Time axis")        
    
        self.numday_start_label = QLabel('Start: ') 
        self.numday_stop_label = QLabel('Stop: ')      
        self.maxday_label = QLabel('Maxday: ')  
        try:
            self.value_maxday_l = QLabel(str(self.lentime))
        except AttributeError: 
            self.value_maxday_l = QLabel(' ')           

        self.numday_box = QSpinBox()   
        self.numday_stop_box = QSpinBox()
        try:  
            self.numday_box.setRange(self.start,self.stop-1)   
            self.numday_stop_box.setRange(self.start+1,self.stop)
            self.numday_stop_box.setValue(self.stop)      
        except AttributeError: 
            pass
            
                      
        time_grid = QGridLayout(self.time_groupBox)   
    
        #line 1 
        time_grid.addWidget(self.numday_start_label,0,0,1,1)
        time_grid.addWidget( self.numday_stop_label,0,1,1,1) 
        time_grid.addWidget(      self.maxday_label,0,2,1,1)      
                  
        #line 2             
        time_grid.addWidget(     self.numday_box,1,0,1,1) 
        time_grid.addWidget(self.numday_stop_box,1,1,1,1)             
        time_grid.addWidget( self.value_maxday_l,1,2,1,1)  
        
    def createRadioButtonsGroup(self):
        self.radio_groupBox = QGroupBox("Plot_type")

        self.radio1 = QRadioButton("&All time")
        self.radio2 = QRadioButton("&Last year")
        self.radio3 = QRadioButton("&Distance plot")

        self.radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.radio1)
        vbox.addWidget(self.radio2)
        vbox.addWidget(self.radio3)
        vbox.addStretch(1)
        
        self.radio_groupBox.setLayout(vbox)

       
    def addOneAction(self,text,action,target):
        item = target(text)
        item.addAction(action)
        return item
    
    def addMultipleAction(self,text,actions,target):
        item = target(text)
        item.addActions(actions)
        return item  
         
    def createAction(self, text, slot=None, shortcut=None,
                    icon=None,tip=None, checkable=False): 
        action = QAction(text, self)
        if icon is not None:
            ic = QIcon()
            pixmap1 = QPixmap(icon).scaled(164, 164)
            ic.addPixmap(pixmap1, QIcon.Normal, QIcon.Off) 
            action.setIcon(ic)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action 
    
   
    #TODO: add Zoom            
    def editZoom(self):    
        
        pass
    
    #TODO: add changeCMAP
    def changeCmap(self):
        pass
    
    def openFile(self):
        import numpy as np
        self.filename ,_  = (QFileDialog.getOpenFileName(
            self,'Open netcdf ', os.getcwd(), 
            "netcdf (*.nc);; all (*)"))
        
        self.array = readdata_qmain.ReadVar(self.filename)  
        var_list = self.array.get_variables_list()
        self.listWidget.addItems(var_list)
        self.max_num_col = self.array.max_numcol()                               
        self.lentime = self.array.lentime()  
        self.start = 0        
        self.stop = self.lentime 
           
        self.updateToolbar() 
        
    def fileSaveAs(self):
        if not (self.filename == None):              
            self.plotTime()         
            try:
                formats = [r'bmp',r'png',r'pdf']
                self.fname, _ = QFileDialog.getSaveFileName(self, "Save File", 
                "Figure.png", "All Files (*);; png (*png) ;; pdf  (*pdf)")
                plt.savefig(self.fname, dpi=150) 
            except:
                pass 
        else:
            Messages.Save()
           
            #TODO: implement recent files 
            #sef.addRecentFile(fname)
                
            
    def openFolder(self): 
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        self.directory =  askdirectory()

    def plotTransect(self):
        pass
            
    def plotTime(self):      
        plt.clf()
        try:
            index = str(
            self.listWidget.currentItem().text())
        except AttributeError:   
            QMessageBox.about(self, "Retry",
            'Choose variable,please') 
            return None             
        self.getCmap()   

        array = readdata_qmain.ReadVar(
            self.filename,index)
        z_units = array.units()
        self.time_units = array.time_units()
        
        self.start = self.numday_box.value()
        self.stop = self.numday_stop_box.value()  
        if self.start >= self.stop: 
            Messages.StartStop()  
            self.start = 0 
            self.stop = self.lentime      
            self.updateToolbar()
            
        if self.radio2.isChecked() and self.lentime >=365 :
            self.start = self.stop-365       
            self.updateToolbar()
             
        z = array.variable(self.start,self.stop)
        x = array.time(self.start,self.stop)
        xlen = len(x)
        y = array.depth()     
        from matplotlib.ticker import MaxNLocator       
        if  self.SedInFileAct.isChecked():  
            try: 
                y2max,ny2max = array.y_watmax()   
                y_wat = y[:ny2max-1]
                y_sed = (array.depth_sed(y,y2max))[ny2max-1:] 
                array.close()
                  
                X,Y_wat = np.meshgrid(x,y_wat) 
                X_sed,Y_sed = np.meshgrid(x,y_sed)          
                Z_wat = z[:ny2max-1,:]
                Z_sed = z[ny2max-1:,:]
                          
                gs = gridspec.GridSpec(2, 1)
                gs.update(left = 0.07,right = 0.85 )
                
                self.cax1 = self.figure.add_axes([0.86, 0.11, 0.02, 0.35])
                self.cax = self.figure.add_axes([0.86, 0.53, 0.02, 0.35])                                    
                ax0 = self.figure.add_subplot(gs[0])
                ax1 = self.figure.add_subplot(gs[1]) 
                
                if self.formatTimeAct.isChecked():
                    X = readdata_qmain.format_time_axis(self,ax0,xlen,X) 
                    X_sed = readdata_qmain.format_time_axis(self,ax1,xlen,X_sed)       
                
                if self.intepolateAct.isChecked():
                    levels_wat = MaxNLocator(nbins=25).tick_values(Z_wat.min(), Z_wat.max())       
                    levels_sed = MaxNLocator(nbins=25).tick_values(Z_wat.min(), Z_sed.max())                        
                    CS = ax0.contourf(X,Y_wat,Z_wat, levels = levels_wat,    
                                    cmap= self.cmap) 
                    CS1 = ax1.contourf(X_sed,Y_sed,Z_sed, 
                          levels = levels_sed, cmap= self.cmap) 
                     
                else:       
                 
                    CS = ax0.pcolormesh(X,Y_wat,Z_wat,   
                                    cmap= self.cmap) 
                    CS1 = ax1.pcolormesh(X_sed,Y_sed,Z_sed,       
                                    cmap= self.cmap) 
      
                ax0.set_ylim(np.max(y_wat),np.min(y_wat))
                ax1.set_ylim(np.max(y_sed),np.min(y_sed)) 
                cb = plt.colorbar(CS,cax = self.cax)  
                cb1 = plt.colorbar(CS1,cax = self.cax1)  
                 
            except: 
                Messages.no_sediment() 
                   
        else: 
             
            array.close()                        
            X,Y = np.meshgrid(x,y)     
            Z_wat = z[:,:]
                     
            gs = gridspec.GridSpec(1, 1)
            gs.update(left=0.15, right= 0.95,
                      top = 0.75,bottom = 0.25,
                      wspace=0.2,hspace=0.2)                 
            ax0 = self.figure.add_subplot(gs[0])
            
            if self.formatTimeAct.isChecked():
                X = readdata_qmain.format_time_axis(self,ax0,xlen,X) 
                   
            if self.intepolateAct.isChecked():
                levels = MaxNLocator(nbins=25).tick_values(Z.min(), Z.max()) 
                CS = ax0.contourf(X,Y,Z, levels = levels,cmap= self.cmap)      
            else:                               
                CS = ax0.pcolormesh(X,Y,Z_wat, cmap= self.cmap) 
                
            ax0.set_ylim(np.max(y),np.min(y))
            cb = plt.colorbar(CS)  
        self.canvas.draw() 

    
    
    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            filename = QVariant(self.filename) \
        if self.filename is not None else QVariant()
            settings.setValue("LastFile", filename)
            recentFiles = QVariant(self.recentFiles) \
        if self.recentFiles else QVariant()
            settings.setValue(
            "RecentFiles", recentFiles)
            settings.setValue("MainWindow/Size",
                         QVariant(self.size()))
            settings.setValue("MainWindow/Position",
            QVariant(self.pos()))
            settings.setValue("MainWindow/State",
            QVariant(self.saveState()))
        else:
            event.ignore()  
            
            

    def callAllTime(self):
        ''' calls the function to plot
        all time array or manually input start stop'''        
        if not (self.filename == None):              
            self.plotTime() 
        else:
            Messages.open_file() 
 
            
    def getCmap(self):    
        #TODO: make it changeable 
        try: 
            self.cmap = plt.get_cmap(self.cmap_box.currentText())
            self.cmap1 = plt.get_cmap(self.cmap_box.currentText())    
        except:
            self.cmap  =  plt.get_cmap('gist' )  
            self.cmap1  =  plt.get_cmap('gist' ) 
            
class CustomLabel(QLabel): 
    
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
                                
    def dragEnterEvent(self, e):
        #if e.mimeData().hasFormat('.nc'):
        e.accept() 



class Messages(): 
    global capy_path
    capy_path = 'img/capybara.png'
    
    def no_sediment():
        
        msg = QMessageBox() 
        msg.setText("Uncheck menu Properties/Use sediment Subplot")    
        pixmap = QPixmap(capy_path)
        pixmap1 = pixmap.scaled(164, 164)
        msg.setIconPixmap(pixmap1)
        msg.exec_()  
    def open_file():
        
        msg = QMessageBox()         
        msg.setText("Open Netcdf File,please")    
        pixmap = QPixmap(capy_path)
        pixmap1 = pixmap.scaled(164, 164)
        msg.setIconPixmap(pixmap1)      
         
        msg.exec_()   

    def Save():
        
        msg = QMessageBox()         
        msg.setText("Retry \nThere is nothing to save yet")    
        pixmap = QPixmap(capy_path)
        pixmap1 = pixmap.scaled(164, 164)
        msg.setIconPixmap(pixmap1)      
         
        msg.exec_()          

    def StartStop():
        
        msg = QMessageBox()         
        msg.setText("Retry \nWront start and stop values")    
        pixmap = QPixmap(capy_path)
        pixmap1 = pixmap.scaled(164, 164)
        msg.setIconPixmap(pixmap1)      
         
        msg.exec_() 
                          
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setApplicationName("BROM NetCDF Viewer")
    app.setOrganizationName("test Ltd.")
    app.setStyle("plastique")
    app_icon = QIcon()
    app_icon.addFile('img/logo.png', QSize(16,16))
    app.setWindowIcon(app_icon)
    ex = Window()
    ex.setStyleSheet("background-color:#acc0c4;")
    sys.exit(app.exec_())