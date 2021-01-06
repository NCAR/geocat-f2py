import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from .fortran import (ddrveof)
from .missing_values import (fort2py_msg, py2fort_msg)

# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.

def _drveof(x, nobs, msta, msg_py, neval, jopt):
    # eval,evec,pcvar,trace = ddrveof(x,[nobs,msta,xmsg,neval,jopt])

    # missing value handling
    x, msg_py, msg_fort = py2fort_msg(x, msg_py=msg_py)

    # fortran call
    eval, evec, pcvar, trace = ddrveof(x, nobs=nobs,msta=msta,xmsg=msg_fort,neval=neval,jopt=jopt )

    # missing value handling
    x, msg_py, msg_fort = fort2py_msg(x, msg_fort=msg_fort, msg_py=msg_py)

    #return result
    return eval, evec, pcvar, trace

def drveof(x, nobs=None, msta=None, msg_py=None, neval=None, jopt=None):
    # This is not a parallizable task

    # handle optionals
    if nobs is None:
        nobs = x.shape[0]
    if msta is None:
        msta = x.shape[1]
    if neval is None:
        neval = msta
    if jopt is None:
        jopt = 0;

    # return inner computation. No Dask call, as this is not parallelizable
    return _drveof(x, nobs, msta, msg_py, neval, jopt)