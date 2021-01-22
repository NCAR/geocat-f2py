import numpy as np
import xarray as xr
from dask.array.core import map_blocks
import time

from geocat.f2py.fortran import (deofts7)
from geocat.f2py.missing_values import (fort2py_msg, py2fort_msg)


# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.
def _eofts7(x, evec, nobs, msta, msg_py, jopt):
    # evects = deofts7(x,evec,[nobs,msta,xmsg,jopt])

    # missing value handling
    x, msg_py, msg_fort = py2fort_msg(x, msg_py=msg_py)

    # fortran call
    evects = deofts7(x, evec, nobs, msta, xmsg=msg_fort, jopt=jopt)

    # missing value handling
    x, msg_fort, msg_py = fort2py_msg(x, msg_fort=msg_fort, msg_py=msg_py)

    #return result
    return evects

def eofts7(x, evec, nobs = None, msta = None, msg_py = None, jopt = None):
    # This is not a parallizable task

    # handle optionals
    if nobs is None:
        nobs = x.shape[0]
    if msta is None:
        msta = x.shape[1]
    if jopt is None:
        jopt = 0;

    # return inner computation. No Dask call, as this is not parallelizable
    return _eofts7(x, evec, nobs, msta, msg_py, jopt)

def eofts7_test():
    x = np.random.random((1000,1000))
    evec = x
    print(eofts7(x, evec))

start = time.time()
eofts7_test()
end = time.time()
print(end-start)