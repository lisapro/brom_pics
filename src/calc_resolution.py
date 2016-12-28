'''
Created on 17. des. 2016

@author: ELP
'''
import sys
from PyQt4 import QtGui   
    
    
class myQLabel(QtGui.QLabel):
    def __init__(self, *args, **kargs):
        super(myQLabel, self).__init__(*args, **kargs)

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored,
                                             QtGui.QSizePolicy.Ignored))  

        self.setMinSize(14)

    def setMinSize(self, minfs):        

        f = self.font()
        f.setPixelSize(minfs)
        br = QtGui.QFontMetrics(f).boundingRect(self.text())

        self.setMinimumSize(br.width(), br.height())

    def resizeEvent(self, event):
        super(myQLabel, self).resizeEvent(event)

        if not self.text():
            return

        #--- fetch current parameters ----

        f = self.font()
        cr = self.contentsRect()

        #--- find the font size that fits the contentsRect ---

        fs = 1                    
        while True:

            f.setPixelSize(fs)
            br =  QtGui.QFontMetrics(f).boundingRect(self.text())

            if br.height() <= cr.height() and br.width() <= cr.width():
                fs += 1
            else:
                f.setPixelSize(max(fs - 1, 1)) # backtrack
                break  

        #--- update font size ---

        self.setFont(f)  
        self.fontsize = fs 
        
        
                    