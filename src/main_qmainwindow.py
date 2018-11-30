import sys 
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import QSize 
from qmainwindow import  Window

def main():
    font = QFont() 
    font.setFamily("Arial")
    font.setPointSize(11) 
    
    app = QApplication(sys.argv)
    app.setApplicationName("BROM NetCDF Viewer")
    app.setOrganizationName("test Ltd.")
    app.setStyle("plastique")
    app.setFont(font)
    
    app_icon = QIcon()
    app_icon.addFile('img/logo.png', QSize(16,16))
    app.setWindowIcon(app_icon)
    
    ex = Window()
    ex.setStyleSheet("background-color: #cad7d9;")
    sys.exit(app.exec_())
    
    
main()    