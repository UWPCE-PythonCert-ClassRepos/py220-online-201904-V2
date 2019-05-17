from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(
    name='good_performance',
    ext_modules=cythonize("poor_perf_v15.pyx"),
)
