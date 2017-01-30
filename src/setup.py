from distutils.core import setup
import py2exe
import matplotlib
from netCDF4 import Dataset

setup(windows=[{"script":"main.py"}],
      options = {
                 "py2exe": 
                    { "dll_excludes": ["api-ms-win-core-string-l1-1-0.dll",
                        "MSVFW32.dll",
                        "AVIFIL32.dll",
                        "AVICAP32.dll",
                        "ADVAPI32.dll",
                        "CRYPT32.dll",
                        "WLDAP32.dll"]
                    }
                },
      data_files=matplotlib.get_py2exe_datafiles()
     )