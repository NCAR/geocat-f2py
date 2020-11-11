#!/bin/sh

cd src/geocat/temp/fortran
f2py -c --fcompiler=gnu95 linint2.pyf linint2.f
f2py -c --fcompiler=gnu95 rcm2rgrid.pyf rcm2rgrid.f linmsg_dp.f
f2py -c --fcompiler=gnu95 eof_scripps.pyf eof_scripps.f90
f2py -c --fcompiler=gnu95 moc_loops.pyf moc_loops.f
cd ../../../..

python -m pip install . --no-deps -vv
