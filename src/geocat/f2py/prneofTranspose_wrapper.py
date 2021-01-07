import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from .fortran import xrveoft as dxrveoft #renaming slightly to avoid collision later on
from .missing_values import (fort2py_msg, py2fort_msg)

# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.

def _xrveoft(xdata, nrobs, ncsta, xmsg, neval, jopt):
    #eval,evec,pcvar,trace = dxrveoft(xdata,[nrobs,ncsta,xmsg,neval,jopt]) # xrveoft as dxrveoft for namespace reasons

    # missing value handling
    xdata, msg_py, msg_fort = py2fort_msg(xdata, msg_py=msg_py)

    # fortran call
    eval, evec, pcvar, trace = dxrveoft(xdata, nrobs=nrobs, ncsta=ncsta, xmsg=msg_fort, jopt=jopt)

    # missing value handling
    xdata, msg_py, msg_fort = fort2py_msg(xdata, msg_fort=msg_fort, msg_py=msg_py)

    #return result
    return eval, evec, pcvar, trace


def xrveoft(xdata, nrobs=None, ncsta=None, msg_py=None, neval=None,  jopt=None):
    # This is not a parallizable task

    # handle optionals
    if nrobs is None:
        nrobs = xdata.shape[0]
    if ncsta is None:
        ncsta = xdata.shape[1]
    if neval is None:
        neval = ncsta
    if jopt is None:
        jopt = 0;

    # return inner computation. No Dask call, as this is not parallelizable
    return _xrveoft(xdata, nrobs, ncsta, xmsg, jopt)