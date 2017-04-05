__author__ = 'davide'

from distutils.core import setup
from distutils.extension import Extension

import numpy
from Cython.Build import cythonize

setup(
    ext_modules=cythonize([Extension("collatz", ["src/collatz.pyx"],
                                     include_dirs=[numpy.get_include()])])
)
