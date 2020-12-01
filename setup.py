#''' setup.py is needed, but only to make namespaces happen, 
version = '0.2.1'

from setuptools import setup, find_packages

from pathlib import Path

datadir = Path(__file__).parent / 'src'/ 'geocat' / 'f2py' / 'fortran'
files = [str(p.relative_to(datadir)) for p in datadir.rglob('*.so')]

setup(
      name='geocat.f2py',
      version=version,
      package_dir={
                   '': 'src',
                   'geocat': 'src/geocat',
                   'geocat.f2py': 'src/geocat/f2py',
                   'geocat.f2py.fortran': 'src/geocat/f2py/fortran',
                   },
      package_data={'geocat.f2py.fortran': files},
      namespace_packages=['geocat'],
      packages=['geocat','geocat.f2py', 'geocat.f2py.fortran'],
      )

