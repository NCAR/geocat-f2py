import numpy as np
import xarray as xr
from dask.array.core import map_blocks
import time

from geocat.temp.fortran import (deof11)


# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.

def _eof11(d, nmodes, icovcor, dmsg):
    #''' eigenvalues,eigenvectors,variance,princomp = deof11(d,nmodes,[icovcor,dmsg])
    eigenvalues, eigenvectors, variance, princomp = deof11(d,nmodes,[icovcor,dmsg])
    return eigenvalues, eigenvectors, variance, princomp

def eof11(d, nmodes, icovcor=0, dmsg=-99):
    # this is effectivly a stub, since this is not a parallelizable task.
    return _eof11(d, nmodes, icovcor, dmsg)

def eof_test():
    d = np.random.random((1000,10000))
    nmodes = 10
    print(eof11(d, nmodes))

start = time.time()
eof_test()
end = time.time()
print(end-start)