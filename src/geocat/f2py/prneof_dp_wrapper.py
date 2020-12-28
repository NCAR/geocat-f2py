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

    return eval, evec, pcvar, trace