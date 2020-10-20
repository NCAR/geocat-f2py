import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from geocat.temp.fortran import (deof11)


# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.

def _eof11():
    #''' eigenvalues,eigenvectors,variance,princomp = deof11(d,nmodes,[icovcor,dmsg])


