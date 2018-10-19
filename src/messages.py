from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap


class Messages: 
    global capy_path
    capy_path = 'img/capybara.png'
    pixsize = 164
    def no_sediment():
        
        msg = QMessageBox() 
        msg.setText("Uncheck menu Properties/Use sediment Subplot")    
        pixmap = QPixmap(capy_path)
        pixmap1 = pixmap.scaled(164, 164)
        msg.setIconPixmap(pixmap1)
        msg.exec_()  
     
    def no_limits(text): 
        msg = QMessageBox() 
        msg.setText("Manual limits for {} are not defined".format(text))    
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
        pixmap1 = pixmap.scaled(124, 124)
        msg.setIconPixmap(pixmap1)      
         
        msg.exec_() 