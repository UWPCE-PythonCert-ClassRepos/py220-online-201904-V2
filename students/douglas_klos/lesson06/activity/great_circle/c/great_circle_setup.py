#!python
#cython: language_level=3

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

great_circle_extension = Extension(
    name="py_great_circle",
    sources=["great_circle.pyx"],
    libraries=["great_circle"],
)
setup(
    name="py_great_circle",
    ext_modules=cythonize([great_circle_extension])
)

# setup(
#     name='Python Great Circle',
#     ext_modules=cythonize("great_circle.pyx",  compiler_directives={'language_level' : "3"}),
# )

