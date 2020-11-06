$PYTHON setup.py install     # Python command to install the script.

cd src/geocat/temp/fortran
f2py -c --fcompiler=gnu95 linint2.pyf linint2.f
f2py -c --fcompiler=gnu95 rcm2rgrid.pyf rcm2rgrid.f linmsg_dp.f
f2py -c --fcompiler=gnu95 eof_scripps.pyf eof_scripps.f90
cd ../../../..

pip install .
