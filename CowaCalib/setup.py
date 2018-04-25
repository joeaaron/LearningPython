from distutils.core import setup
import py2exe
import sys
 
#this allows to run it with a simple double click.
#sys.argv.append('py2exe')
 
py2exe_options = {
        "includes": ["sip", "PyQt4", "PyQt4.uic", 
                    "scipy.sparse.csgraph._validation",
                    "scipy.special._ufuncs_cxx", "numpy", "PIL"],
        "dll_excludes": ["MSVCP90.dll","libifcoremd.dll"],
        "compressed": 1,
        "optimize": 2,
        "ascii": 0,
        "bundle_files": 2,
        }
 
setup(
      name = 'COWA CALIBRATE',
      version = '1.0',
      windows = ['main.py',],
      data_files = [('', ['ecatmc.dll'])],
      #zipfile = None,
      options = {'py2exe': py2exe_options},
      )