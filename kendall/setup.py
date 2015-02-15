__author__ = 'davide'

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

pyx_sources = ['src/kendall.pyx']
cmdclass = {'build_ext': build_ext}

pyx_ext = Extension('kendall',
                    pyx_sources,
                    include_dirs=[numpy.get_include()])

setup(name='kendall',
      ext_modules=[pyx_ext],
      cmdclass=cmdclass)