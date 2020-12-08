import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from .fortran import (triple2grid, triple2grid1, trip2grd3)
from .errors import (ChunkError, CoordinateError)
from .missing_values import (fort2py_msg, py2fort_msg)


# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.


def _triple2grid(x, y, data, xgrid, ygrid, msg_py):
    # signature:  grid = triple2grid(x,y,data,xgrid,ygrid,msg_py)


# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.

def triple2grid(x, y, data, xgrid, ygrid, msg_py):
    # signature:  grid = triple2grid(x,y,data,xgrid,ygrid,msg_py)