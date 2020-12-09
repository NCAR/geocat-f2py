import numpy as np
import xarray as xr

from .fortran import (dpresplvl)
from .errors import (DimensionError, AttributeError)
from .missing_values import (fort2py_msg, py2fort_msg)


# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.


def _dpres_plevel(plev, psfc, ptop, msg_py):

    if psfc.ndim == 2:
        psfc = np.transpose(psfc, axes=(1,0))
    elif psfc.ndim == 3:
        psfc = np.transpose(psfc, axes=(2,1,0))

    plev, msg_py, msg_fort = py2fort_msg(plev, msg_py=msg_py)

    dp = dpresplvl(plev, psfc, ptop, pmsg=msg_fort)

    dp = np.asarray(dp)
    dp = np.transpose(dp, axes=(3,2,1,0))

    fort2py_msg(dp, msg_fort=msg_fort, msg_py=msg_py)

    return dp


# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.


def dpres_plevel(plev, psfc, ptop=None, msg_py=None, meta=False):

    # ''' Start of boilerplate
    if not isinstance(plev, xr.DataArray):
        plev = xr.DataArray(plev)

    if plev.values.ndim != 1:
        raise DimensionError(
            "ERROR dpres_plevel: The 'plev' array must be 1 dimensional array !"
        )

    if np.size(psfc) == 1:  # if it is a scalar, then construct a ndarray
        psfc = np.asarray(psfc)
        psfc = np.ndarray([1], buffer=psfc, dtype=psfc.dtype)
        psfc = xr.DataArray(psfc)
    elif isinstance(psfc, np.ndarray):
        psfc = xr.DataArray(psfc)

    if psfc.values.ndim > 3:
        raise DimensionError(
            "ERROR dpres_plevel: 'psfc' must be a scalar, or 2 or 3 dimensional array with right most dimensions lat x lon !"
        )

    if "units" in plev.attrs.values() and "units" in psfc.attrs.values():
        if plev.attrs["units"] != psfc.attrs["units"]:
            raise AttributeError(
                "ERROR dpres_plevel: Units of 'plev' and 'psfc' needs to match !"
            )
    elif "units" in plev.attrs.values() or "units" in psfc.attrs.values():
        raise AttributeError(
            "ERROR dpres_plevel: Either of 'plev' and 'psfc' has ""units"" attribute but the other does not !"
        )

    if isinstance(ptop, np.ndarray) or isinstance(ptop, xr.DataArray):
        raise DimensionError(
            "ERROR dpres_plevel: The 'ptop' value must be a scalar !"
        )

    if ptop is None:
        ptop = min(plev)
    else:
        if ptop > min(plev):
            raise ValueError(
                "ERROR dpres_plevel: The 'ptop' value must be <= min(plev) !")

    dp = _dpres_plevel(plev.values, psfc.values, ptop, msg_py)

    if psfc.values.ndim == 1:
        dp = dp.reshape(dp.shape[1])
    elif psfc.values.ndim == 2:
        dp = dp.reshape(dp.shape[1], dp.shape[2], dp.shape[3])



    dp = xr.DataArray(dp)



    return dp
