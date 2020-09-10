try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

#import distutils.sysconfig

with open("src/geocat/temp/version.py") as f:
    exec(f.read())

setup(name="geocat.temp",
      package_dir={
          '': 'src',
          'geocat': 'src/geocat',
          'geocat.temp': 'src/geocat/temp',
          'geocat.temp.fortran': 'src/geocat/temp/fortran',
      },
      namespace_packages=['geocat'],
      packages=["geocat", "geocat.temp", "geocat.temp.fortran"],
      version=__version__,
      install_requires=['numpy', 'xarray', 'dask[complete]'])
