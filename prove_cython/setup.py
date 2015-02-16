__author__ = 'davide'

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize([Extension("collatz", ["src/collatz.pyx"],
    	                   include_dirs=[numpy.get_include()],
                           requires=['statsmodels'], requires=['statsmodels'],
                           requires=['PyQt5'], requires=['posix_ipc'],
                           requires=['matplotlib'], requires=['pandas'])])
)
