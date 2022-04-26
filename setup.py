#''' setup.py is needed, but only to make namespaces happen,
from pathlib import Path

from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().strip().split('\n')


#''' moved into function, can now be used other places
def version():
    for line in open('meta.yaml').readlines():
        index = line.find('set version')
        if index > -1:
            return line[index + 15:].replace('\" %}', '').strip()


datadir = Path(__file__).parent / 'src' / 'geocat' / 'f2py' / 'fortran'
files = [str(p.relative_to(datadir)) for p in datadir.rglob('*.so')]

setup(name='geocat.f2py',
      version=version(),
      maintainer='GeoCAT',
      maintainer_email='geocat@ucar.edu',
      python_requires='>=3.7',
      install_requires=requirements,
      description='''GeoCAT-f2py wraps, in Python, the compiled language
    implementations of some of the computational functions found under the
    GeoCAT-comp umbrella.''',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Scientific/Engineering',
      ],
      include_package_data=True,
      package_dir={
          '': 'src',
          'geocat': 'src/geocat',
          'geocat.f2py': 'src/geocat/f2py',
          'geocat.f2py.fortran': 'src/geocat/f2py/fortran',
      },
      package_data={'geocat.f2py.fortran': files},
      namespace_packages=['geocat'],
      packages=['geocat', 'geocat.f2py', 'geocat.f2py.fortran'],
      url='https://github.com/NCAR/geocat-f2py',
      project_urls={
          'Documentation': 'https://geocat-f2py.readthedocs.io',
          'Source': 'https://github.com/NCAR/geocat-f2py',
          'Tracker': 'https://github.com/NCAR/geocat-f2py/issues',
      },
      zip_safe=False)
