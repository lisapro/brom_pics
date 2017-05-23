
from netCDF4 import Dataset

fh = Dataset('water_day.nc')

names_vars = [] 
#for names,vars in fh.variables.items():
#    print (names,'  ',vars) #names_vars.append(names) 
data = fh.variables['B_NUT_NH4'].units
print (data)    
'''    
if 'z' in names_vars:
    print ('y')
else: 
    print ('no')         
   
# '''   