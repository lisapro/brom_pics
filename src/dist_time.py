
import xarray as xr
import matplotlib.pyplot as plt 
import readdata
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
def make_plot(self,index,start,stop,depth): 
    plt.clf() 
    #readdata.get_cmap(self)
    var = xr.open_dataset(self.fname)[index][start:stop,depth,:]
    X,Y = np.meshgrid(var.time,var.i)
    plt.contourf(X,Y, var.values.T)    
    #plt.show()
    self.canvas.draw()

if __name__ == '__main__':
    class Test():
        def __init__(self):
            self.fname = r'E:\Users\EYA\Horten\_EGU2019\BROM_Horten_out_April.nc'
            make_plot(self,'pH')    

    Test()        