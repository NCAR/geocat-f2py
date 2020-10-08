#''' setup.py is needed, but only to make namespaces happen, 
version = '0.1'

from setuptools import setup

setup(
      name='geocat.temp',
      version=version,
      package_dir={
                   '': 'src',
                   'geocat': 'src/geocat',
                   'geocat.temp': 'src/geocat/temp',
                   'geocat.temp.fortran': 'src/geocat/temp/fortran',
                   },
      namespace_packages=['geocat'],
      packages=['geocat','geocat.temp','geocat.temp.fortran'],
      install_requires=['numpy','dask[complete]','xarray'],
      )

