""" An attempt to create a setup file for good_perf_cython. """

from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='Good Perf Cython',
    ext_modules=cythonize("src/cython_with_import/good_perf_cython.pyx",
                          language_level="3")
    )
