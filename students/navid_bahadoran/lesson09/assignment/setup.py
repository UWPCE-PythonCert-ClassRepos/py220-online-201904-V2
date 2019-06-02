from setuptools import setup, find_packages

setup(name="src", url='https://github.com/navidbahadoran', author='Navid Bahadoran',
      author_email='navid.baahdoran@gmail.com', packages=find_packages(), package_dir={'src': './src'},
      package_data={'src': ['data/*.*']})
# include_package_data=True