
import xarray as xr
import matplotlib.pyplot as plt 
import readdata
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
def make_plot(self,index,start,stop,depth): 
    plt.clf() 

    da = xr.open_dataset(self.fname)[index]  
    data_units = da.units
    var = da[start:stop,depth,:]
 
    readdata.get_cmap(self)
    readdata.grid_plot(self,1)     

    X,Y = np.meshgrid(var.time,var.i)
    readdata.format_time_axis2(self,self.ax,len(var.time))     
    if self.interpolate_checkbox.isChecked():
        CS = self.ax.contourf(X,Y, var.values.T, cmap = self.cmap)     
    else:
        CS = self.ax.pcolormesh(X,Y, var.values.T, cmap = self.cmap)
    self.ax.set_title(index + ', ' + data_units)        
    self.ax.set_xlim(np.min(X),np.max(X)) 
    self.ax.set_ylabel('Distance,m ',  fontsize= self.font_txt)
    format = readdata.get_format(self,var.values.T.max())
    cb = plt.colorbar(CS, self.cax,format = format)  #, ticks = wat_ticks            
    da.close()
    self.canvas.draw()



if __name__ == '__main__':
    fname = r'E:\Users\EYA\Horten\_EGU2019\BROM_Horten_out_April.nc'
    f = xr.open_dataset(fname).variables.keys()
    p = xr.open_dataset(fname) #['pH'] 

    print (p)
    #flux_l = [n for n in names_vars if n.startswith('fick')]  
    #sink_l = [n for n in names_vars if n.startswith('sink')]
    #other_l = [n for n in names_vars if (not n.startswith(('fick', 'sink','z','z2','kz','time','i')))]
   


    #print(other_l)
    #class Test():
    #    def __init__(self):
    #        self.fname = r'E:\Users\EYA\Horten\_for_Paper\BROM_Horten_out_13c_6pl .nc'
    #        make_plot(self,'pH',0,10,5)    
    #Test()'''      