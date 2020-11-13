#''' setup.py is needed, but only to make namespaces happen, 
version = '0.2.1'

from setuptools import setup, find_packages

from pathlib import Path

datadir = Path(__file__).parent / 'src'/ 'geocat' / 'temp' / 'fortran'
files = [str(p.relative_to(datadir)) for p in datadir.rglob('*.so')]

setup(
      name='geocat.temp',
      version=version,
      package_dir={
                   '': 'src',
                   'geocat': 'src/geocat',
                   'geocat.temp': 'src/geocat/temp',
                   'geocat.temp.fortran': 'src/geocat/temp/fortran',
                   },
      package_data={'geocat.temp.fortran': files},
      namespace_packages=['geocat'],
      packages=['geocat','geocat.temp', 'geocat.temp.fortran'],
      )

