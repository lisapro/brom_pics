#!/usr/bin/python
# -*- coding: utf-8 -*-
# this ↑ comment is important to have 
# at the very first line 
# to define using unicode 

'''
Created on 30. jun. 2017

@author: ELP
'''

from PyQt4 import QtGui


text = (' <a href= "https://github.com/lisapro/brom_pics2/wiki">'
    ' Find online help here </a>')

def show(self):
        messagebox = QtGui.QMessageBox.about(
                self, "Help",
                text
                ) 
        
        
        