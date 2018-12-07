from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap


class Messages: 
    global capy_path
    capy_path = 'img/capybara.png'
    global wiki 
    wiki = '<a href= "https://github.com/lisapro/brom_pics2/wiki"> online help </a>'

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
        msg.setWindowTitle('Something went wrong')
        msg.setText('Specify all limits please {} '.format(wiki))    
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
        msg.setText('Retry, Wrong start and stop values {} '.format(wiki))    
        pixmap = QPixmap(capy_path)
        pixmap1 = pixmap.scaled(124, 124)
        msg.setIconPixmap(pixmap1)      
         
        msg.exec_() 
        
    def radio_button_not_implemented():
        
        msg = QMessageBox()         
        msg.setText("Retry \nRadio button is not implemented yet")    
        pixmap = QPixmap(capy_path)
        pixmap1 = pixmap.scaled(124, 124)
        msg.setIconPixmap(pixmap1)      
         
        msg.exec_()  
             
    def message_text(text = 'No text'):
        msg = QMessageBox()         
        msg.setText(text)    
        pixmap = QPixmap(capy_path)
        pixmap1 = pixmap.scaled(124, 124)
        msg.setIconPixmap(pixmap1)      
         
        msg.exec_()          
                    