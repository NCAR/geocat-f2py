import numpy as np
import xarray as xr

from .fortran import (dpresplvl)
from .errors import (DimensionError, AttributeError)
from .missing_values import (fort2py_msg, py2fort_msg)


# Inner Wrapper _<funcname>()
# This wrapper handles transpose of the input and output data
# as well as missing value representations before
# and after the Fortran function call.


def _dpres_plevel(plev, psfc, ptop, msg_py):

    # Transpose psfc before Fortran function call
    if psfc.ndim == 2:
        psfc = np.transpose(psfc, axes=(1,0))
    elif psfc.ndim == 3:
        psfc = np.transpose(psfc, axes=(2,1,0))

    # Handle Python2Fortran missing value conversion
    plev, msg_py, msg_fort = py2fort_msg(plev, msg_py=msg_py)

    # Fortran function call
    dp = dpresplvl(plev, psfc, ptop, pmsg=msg_fort)

    # Transpose output before returning it to outer wrapper
    dp = np.asarray(dp)
    dp = np.transpose(dp, axes=(3,2,1,0))

    # Handle Fortran2Python missing value conversion back
    fort2py_msg(dp, msg_fort=msg_fort, msg_py=msg_py)

    return dp


# Outer Wrapper <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.

def dpres_plevel(plev, psfc, ptop=None, msg_py=None, meta=False):
    """Calculates the pressure layer thicknesses of a constant pressure level coordinate system.

            Args:

                plev (:class:`xarray.DataArray` or :class:`numpy.ndarray`):
                    A one dimensional array containing the constant pressure levels. May be
                    in ascending or descending order. Must have the same units as `psfc`.

                psfc (:obj:`numpy.number` or :class:`xarray.DataArray` or :class:`numpy.ndarray`):
                    A scalar or an array of up to three dimensions containing the surface
                    pressure data in Pa or hPa (mb). The rightmost dimensions must be latitude
                    and longitude. Must have the same units as `plev`.

                ptop (:class:`numpy.number`):
                    A scalar specifying the top of the column. ptop should be <= min(plev).
                    Must have the same units as `plev`.

                msg_py (:obj:`numpy.number`):
                    A numpy scalar value that represent a missing value in fi.
                    This argument allows a user to use a missing value scheme
                    other than NaN or masked arrays, similar to what NCL allows.

                meta (:obj:`bool`):
                    If set to True and the input array is an Xarray, the metadata
                    from the input array will be copied to the output array;
                    default is False.
                    Warning: this option is not currently supported.

            Returns:
                :class:`xarray.DataArray`: If psfc is a scalar, the return variable will be a
                one-dimensional array the same size as `plev`; if `psfc` is two-dimensional
                [e.g. (lat,lon)] or three-dimensional [e.g. (time,lat,lon)], then the return
                array will have an additional level dimension: (lev,lat,lon) or (time,lev,lat,lon).
                The returned type will be double if `psfc` is double, float otherwise.

            Description:
                Calculates the layer pressure thickness of a constant pressure level system. It
                is analogous to `dpres_hybrid_ccm` for hybrid coordinates. At each grid point the
                sum of the pressure thicknesses equates to [psfc-ptop]. At each grid point, the
                returned values above `ptop` and below `psfc` will be set to the missing value of `psfc`.
                If there is no missing value for `psfc` then the missing value will be set to the default
                for float or double appropriately. If `ptop` or `psfc` is between plev levels
                then the layer thickness is modifed accordingly. If `psfc` is set to a missing value, all
                layer thicknesses are set to the appropriate missing value.

                The primary purpose of this function is to return layer thicknesses to be used to
                weight observations for integrations.

            Examples:

                Example 1: Using dpres_plevel with :class:`xarray.DataArray` input

                .. code-block:: python

                    import numpy as np
                    import xarray as xr
                    import geocat.comp

                    # Open a netCDF data file using xarray default engine and load the data stream
                    ds = xr.open_dataset("./SOME_NETCDF_FILE.nc")

                    # [INPUT] Grid & data info on the source
                    psfc = ds.PS
                    plev = ds.LEV
                    ptop = 0.0

                    # Call the function
                    result_dp = geocat.comp.dpres_plevel(plev, psfc, ptop)
            """

    # ''' Start of boilerplate
    if not isinstance(plev, xr.DataArray):
        plev = xr.DataArray(plev)

    if plev.values.ndim != 1:
        raise DimensionError(
            "ERROR dpres_plevel: The 'plev' array must be 1 dimensional array !"
        )

    if np.size(psfc) == 1:  # if it is a scalar, then construct an xaray.dataarray
        psfc = np.asarray(psfc)
        psfc = np.ndarray([1], buffer=psfc, dtype=psfc.dtype)
        psfc = xr.DataArray(psfc)
    elif isinstance(psfc, np.ndarray):
        psfc = xr.DataArray(psfc)

    if psfc.values.ndim > 3:
        raise DimensionError(
            "ERROR dpres_plevel: 'psfc' must be a scalar, or 2 or 3 dimensional array with right most dimensions lat x lon !"
        )

    # plev and psfc must have the same units.
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
