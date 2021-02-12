#''' setup.py is needed, but only to make namespaces happen,
from setuptools import setup, find_packages

from pathlib import Path


#''' moved into function, can now be used other places
def version():
    for line in open('meta.yaml').readlines():
        index = line.find('version')
        if index > -1:
            return line[index + 8:].replace('\'', '').strip()


datadir = Path(__file__).parent / 'src' / 'geocat' / 'f2py' / 'fortran'
files = [str(p.relative_to(datadir)) for p in datadir.rglob('*.so')]

setup(
    name='geocat.f2py',
    version=version(),
    package_dir={
        '': 'src',
        'geocat': 'src/geocat',
        'geocat.f2py': 'src/geocat/f2py',
        'geocat.f2py.fortran': 'src/geocat/f2py/fortran',
    },
    package_data={'geocat.f2py.fortran': files},
    namespace_packages=['geocat'],
    packages=['geocat', 'geocat.f2py', 'geocat.f2py.fortran'],
)
