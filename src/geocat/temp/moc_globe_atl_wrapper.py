import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from .fortran import mocloops
from .errors import (ChunkError, CoordinateError)
from .missing_values import (fort2py_msg, py2fort_msg)

# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.

def _moc_globe_atl(lat_aux_grid, a_wvel, a_bolus, a_submeso, t_lat, rmlak, msg_py):
    # signature:  tmp1,tmp2,tmp3 = mocloops(tlat,lat_aux_grid,rmlak,work1,work2,work3,wmsg)
    work1 = a_wvel
    work2 = a_bolus
    work3 = a_submeso

    work1 = np.transpose(work1, axes=(2, 1, 0))
    work2 = np.transpose(work2, axes=(2, 1, 0))
    work3 = np.transpose(work3, axes=(2, 1, 0))

    # transpositions
    t_lat = np.transpose(t_lat, axes=(1, 0))
    rmlak = np.transpose(rmlak, axes=(2, 1, 0))

    # missing value handing for a_wvel (work1)
    work1, msg_py, msg_fort = py2fort_msg(work1, msg_py=msg_py)

    # fortran call
    tmp1, tmp2, tmp3 = mocloops(t_lat, lat_aux_grid, rmlak, work1, work2, work3, msg_fort)

    # Un-transpose arrays for output
    tmp1 = np.transpose(tmp1, axes=(2, 1, 0))
    tmp2 = np.transpose(tmp2, axes=(2, 1, 0))
    tmp3 = np.transpose(tmp3, axes=(2, 1, 0))

    # missing value handling
    tmp1, msg_fort, msg_py = fort2py_msg(tmp1, msg_fort=msg_fort, msg_py=msg_py)
    tmp2, msg_fort, msg_py = fort2py_msg(tmp2, msg_fort=msg_fort, msg_py=msg_py)
    tmp3, msg_fort, msg_py = fort2py_msg(tmp3, msg_fort=msg_fort, msg_py=msg_py)

    # Merge output arrays
    tmp_out = xr.DataArray(np.stack((tmp1, tmp2, tmp3)))

    return tmp_out

# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.

def moc_globe_atl(lat_aux_grid, a_wvel, a_bolus, a_submeso, t_lat, rmlak, msg_py=None):

    # ''' Start of boilerplate
    if not isinstance(a_wvel, xr.DataArray):
        a_wvel = xr.DataArray(a_wvel)

    fo = _moc_globe_atl(
    lat_aux_grid,
    a_wvel.values,
    a_bolus,
    a_submeso,
    t_lat,
    rmlak,
    msg_py)

    return fo