""" Setup file for cythonized code """

from distutils.core import setup
from Cython.Build import cythonize

setup(name="good_performance", ext_modules=cythonize("./src/poor_perf_v15.pyx"))
