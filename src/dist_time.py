
import xarray as xr
import matplotlib.pyplot as plt 
import readdata
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
def make_plot(self,index,start,stop,depth): 
    plt.clf() 
    readdata.get_cmap(self)
    readdata.grid_plot(self,1) 
    var = xr.open_dataset(self.fname)[index][start:stop,depth,:]
    X,Y = np.meshgrid(var.time,var.i)
    readdata.format_time_axis2(self,self.ax,len(var.time))     
    if self.interpolate_checkbox.isChecked():
        CS = self.ax.contourf(X,Y, var.values.T, cmap = self.cmap)     
    else:
        CS = self.ax.pcolormesh(X,Y, var.values.T, cmap = self.cmap)
    self.ax.set_xlim(np.min(X),np.max(X)) 

    format = readdata.get_format(self,var.values.T.max())
    cb = plt.colorbar(CS, self.cax,format = format)  #, ticks = wat_ticks            
  
    self.canvas.draw()



if __name__ == '__main__':
    class Test():
        def __init__(self):
            self.fname = r'E:\Users\EYA\Horten\_EGU2019\BROM_Horten_out_April.nc'
            make_plot(self,'pH')    

    Test()        