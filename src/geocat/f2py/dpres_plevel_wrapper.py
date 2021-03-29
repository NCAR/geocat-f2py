import numpy as np
import xarray as xr

from .errors import AttributeError, DimensionError, MetaError
from .fortran import dpresplvl
from .missing_values import fort2py_msg, py2fort_msg

# Single Wrapper <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.


def dpres_plevel(pressure_levels,
                 pressure_surface,
                 pressure_top=None,
                 msg_py=None,
                 meta=False):
    """Calculates the pressure layer thicknesses of a constant pressure level
    coordinate system.

    Parameters
    ----------

    pressure_levels : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        A one dimensional array containing the constant pressure levels. May be
        in ascending or descending order. Must have the same units as `pressure_surface`.

    pressure_surface : :obj:`numpy.number` or :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        A scalar or an array of up to three dimensions containing the surface
        pressure data in Pa or hPa (mb). The rightmost dimensions must be latitude
        and longitude. Must have the same units as `pressure_levels`.

    pressure_top : :class:`numpy.number`:
        A scalar specifying the top of the column. pressure_top should be <= min(pressure_levels).
        Must have the same units as `pressure_levels`.

    msg_py : :obj:`numpy.number`:
        A numpy scalar value that represent a missing value in fi.
        This argument allows a user to use a missing value scheme
        other than NaN or masked arrays, similar to what NCL allows.

    meta : :obj:`bool`:
        If set to True and the input arrays (pressure_levels and pressure_surface) are Xarray,
        the metadata from the input arrays will be copied to the output array; default is False.
        WARNING: This option is not currently supported. Though, even if it is false,
        Xarray.Dataarray.attrs of `pressure_surface` is being retained in the output.

    Returns
    -------

    dp : :class:`xarray.DataArray`:
        If pressure_surface is a scalar, the return variable will be a
        one-dimensional array the same size as `pressure_levels`; if `pressure_surface`
        is two-dimensional [e.g. (lat,lon)] or three-dimensional [e.g. (time,lat,lon)],
        then the return array will have an additional level dimension: (lev,lat,lon)
        or (time,lev,lat,lon). The returned type will be double
        if `pressure_surface` is double, float otherwise.

    Description
    -----------

        Calculates the layer pressure thickness of a constant pressure level system. It
        is analogous to `dpres_hybrid_ccm` for hybrid coordinates. At each grid point the
        sum of the pressure thicknesses equates to [pressure_surface - pressure_top]. At each
        grid point, the returned values above `pressure_top` and below `pressure_surface` will
        be set to the missing value of `pressure_surface`. If there is no missing value
        for `pressure_surface` then the missing value will be set to the default for
        float or double appropriately. If `pressure_top` or `pressure_surface` is between
        pressure_levels levels then the layer thickness is modifed accordingly.
        If `pressure_surface` is set to a missing value, all layer thicknesses
        are set to the appropriate missing value.

        The primary purpose of this function is to return layer thicknesses to be used to
        weight observations for integrations.

    Examples
    --------

    Example 1: Using dpres_plevel with :class:`xarray.DataArray` input

    .. code-block:: python

        import numpy as np
        import xarray as xr
        import geocat.comp

        # Open a netCDF data file using xarray default engine and load the data stream
        ds = xr.open_dataset("./SOME_NETCDF_FILE.nc")

        # [INPUT] Grid & data info on the source
        pressure_surface = ds.PS
        pressure_levels = ds.LEV
        pressure_top = 0.0

        # Call the function
        result_dp = geocat.comp.dpres_plevel(pressure_levels, pressure_surface, pressure_top)
    """

    # Apply basic sanity checks on the input data
    pressure_levels, pressure_surface, pressure_top = _sanity_check(
        pressure_levels, pressure_surface, pressure_top)

    # Inner wrapper call
    dp = _dpres_plevel(pressure_levels.values, pressure_surface.values,
                       pressure_top, msg_py)

    # Reshape output based on the dimensionality of pressure_surface
    if pressure_surface.ndim == 1:
        dp = dp.reshape(dp.shape[1])
    elif pressure_surface.ndim == 2:
        dp = dp.reshape(dp.shape[0] * dp.shape[1], dp.shape[2], dp.shape[3])

    if meta:
        raise MetaError(
            "ERROR dpres_plevel: Retention of metadata (other than Xarray.Dataarray.attrs) is not yet supported !"
        )

        # TODO: Retaining possible metadata might be revised in the future
    else:
        dp = xr.DataArray(dp, attrs=pressure_surface.attrs)

    return dp


# Inner Wrapper _<funcname>()
# This wrapper basically calls the Fortran function. It also handles
# transpose of the input and output data as well as missing value
# representations before and after the Fortran function call.


def _dpres_plevel(plev, psfc, ptop, msg_py):

    # Transpose pressure_surface before Fortran function call
    if psfc.ndim == 2:
        psfc = np.transpose(psfc, axes=(1, 0))
    elif psfc.ndim == 3:
        psfc = np.transpose(psfc, axes=(2, 1, 0))

    # Handle Python2Fortran missing value conversion
    psfc, msg_py, msg_fort = py2fort_msg(psfc, msg_py=msg_py)

    # Fortran function call
    dp = dpresplvl(plev, psfc, np.float64(1000), pmsg=msg_fort)

    # Transpose output to corect dimension order before returning it to outer wrapper
    dp = np.asarray(dp)
    dp = np.transpose(dp, axes=(3, 2, 1, 0))

    # Handle Fortran2Python missing value conversion back
    fort2py_msg(psfc, msg_fort=msg_fort, msg_py=msg_py)
    fort2py_msg(dp, msg_fort=msg_fort, msg_py=msg_py)

    return dp


# TODO: WIll revisit this after merging sanity check module to repo.
def _sanity_check(pressure_levels, pressure_surface, pressure_top):
    # ''' Basic sanity checks
    if not isinstance(pressure_levels, xr.DataArray):
        pressure_levels = xr.DataArray(pressure_levels)

    if pressure_levels.ndim != 1:
        raise DimensionError(
            "ERROR dpres_plevel: The 'pressure_levels' array must be 1 dimensional array !"
        )

    if np.size(pressure_surface
              ) == 1:  # if it is a scalar, then construct an xarray.dataarray
        pressure_surface = np.asarray(pressure_surface)
        pressure_surface = np.ndarray([1],
                                      buffer=pressure_surface,
                                      dtype=pressure_surface.dtype)
        pressure_surface = xr.DataArray(pressure_surface)
    elif isinstance(pressure_surface, np.ndarray):
        pressure_surface = xr.DataArray(pressure_surface)

    if pressure_surface.ndim > 3:
        raise DimensionError(
            "ERROR dpres_plevel: 'pressure_surface' must be a scalar, or 2 or 3 dimensional "
            "array with right most dimensions lat x lon !")

    # pressure_levels and pressure_surface must have the same units, if they have any.
    if "units" in pressure_levels.attrs.keys(
    ) and "units" in pressure_surface.attrs.keys():
        if pressure_levels.attrs["units"] != pressure_surface.attrs["units"]:
            raise AttributeError(
                "ERROR dpres_plevel: Units of 'pressure_levels' and 'pressure_surface' needs to match !"
            )
    elif "units" in pressure_levels.attrs.keys(
    ) or "units" in pressure_surface.attrs.keys():
        raise AttributeError(
            "ERROR dpres_plevel: Either of 'pressure_levels' and 'pressure_surface' "
            "has "
            "units"
            " attribute but the other does not !")

    if isinstance(pressure_top, np.ndarray) or isinstance(
            pressure_top, xr.DataArray):
        raise DimensionError(
            "ERROR dpres_plevel: The 'pressure_top' value must be a scalar !")

    pressure_level_min = np.min(pressure_levels.values)
    if pressure_top is None:
        pressure_top = pressure_level_min
    else:
        if pressure_top > pressure_level_min:
            raise ValueError(
                "ERROR dpres_plevel: The 'pressure_top' value must be <= min(pressure_levels) !"
            )

    return pressure_levels, pressure_surface, pressure_top
