import numpy as np
import xarray as xr
from dask.array.core import map_blocks

# from .fortran import (grid2triple)
from .fortran import grid2triple as grid2triple_fort

from .errors import (CoordinateError, DimensionError)
from .missing_values import (fort2py_msg, py2fort_msg)


# Dask Wrappers or Internal Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.

def _grid_to_triple(x, y, z, msg_py, shape):
    # ''' signature:  grid = grid_to_triple(x, y, z, msg_py)

    z = np.transpose(z, axes=(1,0))

    # missing value handling
    z, msg_py, msg_fort = py2fort_msg(z, msg_py=msg_py)

    # fortran call
    grid = grid2triple_fort(x, y, z, msg_fort)

    # numpy and reshape
    grid = np.asarray(grid)
    grid = np.transpose(grid, axes=(1, 0))

    # missing value handling
    fort2py_msg(z, msg_fort=msg_fort, msg_py=msg_py)
    fort2py_msg(grid, msg_fort=msg_fort, msg_py=msg_py)

    return grid


def _triple_to_grid(x, y, data, xgrid, ygrid, msg_py):
    # ''' signature:  grid = _triple_to_grid(x,y,data,xgrid,ygrid,msg_py)
    pass


# TODO: Revisit after deprecating geocat.ncomp for implementing this
def _triple_to_grid_2d(x, y, data, xgrid, ygrid, msg_py):
    # ''' signature:  grid = _triple2grid(x,y,data,xgrid,ygrid,msg_py)
    pass


# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.

def grid_to_triple(data, x=None, y=None, msg_py=None):
    # ''' signature:  grid = grid2triple(x,y,z,msg_py)
    """Converts a two-dimensional grid with one-dimensional coordinate variables
           to an array where each grid value is associated with its coordinates.

            Args:

                data (:class:`xarray.DataArray` or :class:`numpy.ndarray`):
                        Two-dimensional array of size ny x mx containing the data values.
                        Missing values may be present in `data`, but they are ignored.

                x (:class:`xarray.DataArray` or :class:`numpy.ndarray`):
                        Coordinates associated with the right dimension of the variable `data`.
                        If `data` is of type :class:`xarray.DataArray` and `x` is unspecified,
                        then it comes from the associated coordinate of `data`. If `data` is of type
                        :class:`numpy.ndarray`, then it must be explicitly given as input and it
                        must have the same dimension (call it `mx`) as the right dimension of `data`.

                y (:class:`xarray.DataArray` or :class:`numpy.ndarray`):
                        Coordinates associated with the left dimension of the variable `data`.
                        If `data` is of type :class:`xarray.DataArray` and `y` is unspecified,
                        then it comes from the associated coordinate of `data`. If `data` is of type
                        :class:`numpy.ndarray`, then it must be explicitly given as input and it
                        must have the same dimension (call it `ny`) as the left dimension of `data`.

                msg (:obj:`numpy.number`):
                    A numpy scalar value that represent a missing value in `data`.
                    This argument allows a user to use a missing value scheme
                    other than NaN or masked arrays, similar to what NCL allows.

            Returns:
                :class:`numpy.ndarray`: If any argument is "double" the return type
                    will be "double"; otherwise a "float" is returned.

            Description:
                The maximum size of the returned array will be 3 x ld where ld <= ny*mx.
                If no missing values are encountered in `data`, then ld=ny*mx. If missing
                values are encountered in `data`, they are not returned and hence ld will be
                equal to ny*mx minus the number of missing values found in `data`. The return
                array will be double if any of the input arrays are double, and float
                otherwise.

            Examples:

                Example 1: Using grid2triple with :class:`xarray.DataArray` input

                .. code-block:: python

                    import numpy as np
                    import xarray as xr
                    import geocat.comp

                    # Open a netCDF data file using xarray default engine and load the data stream
                    ds = xr.open_dataset("./NETCDF_FILE.nc")

                    # [INPUT] Grid & data info on the source curvilinear
                    z=ds.DIST_236_CBL[:]
                    x=ds.gridlat_236[:]
                    y=ds.gridlon_236[:]

                    output = geocat.comp.grid2triple(z, x, y)
        """

    # TODO: Will need to be revisited after sanity_check work is finished
    # Basic sanity checks
    if not isinstance(data, xr.DataArray):
        if (x is None) | (y is None):
            raise CoordinateError(
                "ERROR grid2triple: Argument `x` and `y` must be provided explicitly "
                "unless `data` is an xarray.DataArray.")

        data = xr.DataArray(
            data,
        )

        data = xr.DataArray(
            data.data,
            coords={
                data.dims[-1]: x,
                data.dims[-2]: y,
            },
            dims=data.dims,
        )

    x = data.coords[data.dims[-1]]
    y = data.coords[data.dims[-2]]

    if data.ndim != 2:
        raise DimensionError(
            "ERROR grid2triple: `z` must have two dimensions !\n")

    if x.ndim != 1:
        raise DimensionError(
            "ERROR grid2triple: `x` must have one dimension !\n")
    elif x.shape[0] != data.shape[1]:
        raise DimensionError(
            "ERROR grid2triple: `x` must have the same size (call it `mx`) as the "
            "right dimension of z. !\n")

    if y.ndim != 1:
        raise DimensionError(
            "ERROR grid2triple: `y` must have one dimension !\n")
    elif y.shape[0] != data.shape[0]:
        raise DimensionError(
            "ERROR grid2triple: `y` must have the same size (call it `ny`) as the left dimension of z. !\n")

    outgrid = _grid_to_triple(x.data, y.data, data.data, msg_py, [])

    outgrid = xr.DataArray(outgrid, attrs=data.attrs)

    return outgrid


def triple_to_grid(x, y, data, xgrid, ygrid, **kwargs):
    # ''' signature:  grid = triple2grid(x,y,data,xgrid,ygrid,msg_py)
    """Places unstructured (randomly-spaced) data onto the nearest locations of a rectilinear grid.

        Args:

    	x (:class:`numpy.ndarray`):
                One-dimensional arrays of the same length containing the coordinates
                associated with the data values. For geophysical variables, x
                correspond to longitude.

    	y (:class:`numpy.ndarray`):
                One-dimensional arrays of the same length containing the coordinates
                associated with the data values. For geophysical variables, y
                correspond to latitude.

    	data (:class:`numpy.ndarray`):
                A multi-dimensional array, whose rightmost dimension is the same
                length as `x` and `y`, containing the values associated with the `x`
                and `y` coordinates. Missing values, may be present but will be ignored.

    	xgrid (:class:`numpy.ndarray`):
                A one-dimensional array of length M containing the `x` coordinates
                associated with the returned two-dimensional grid. For geophysical
                variables, these are longitudes. The coordinates' values must be
                monotonically increasing.

    	ygrid (:class:`numpy.ndarray`):
                A one-dimensional array of length N containing the `y` coordinates
                associated with the returned two-dimensional grid. For geophysical
                variables, these are latitudes. The coordinates' values must be
                monotonically increasing.

        **kwargs:
            extra options for the function. Currently the following are supported:
            - ``method``: An integer value that defaults to 1 if option is True,
                          and 0 otherwise. A value of 1 means to use the great
                          circle distance formula for distance calculations.
            - ``domain``: A float value that should be set to a value >= 0. The
                          default is 1.0. If present, the larger this factor the
                          wider the spatial domain allowed to influence grid boundary
                          points. Typically, `domain` is 1.0 or 2.0. If `domain` <= 0.0,
                          then values located outside the grid domain specified by
                          `xgrid` and `ygrid` arguments will not be used.
            - ``distmx``: Setting option@distmx allows the user to specify a search
                          radius (km) beyond which observations are not considered
                          for nearest neighbor. Only applicable when `method` = 1.
                          The default `distmx`=1e20 (km) means that every grid point
                          will have a nearest neighbor. It is suggested that users
                          specify some reasonable value for distmx.
            - ``msg`` (:obj:`numpy.number`): A numpy scalar value that represent
                          a missing value in `data`. This argument allows a user to
                          use a missing value scheme other than NaN or masked arrays,
                          similar to what NCL allows.
            - ``meta`` (:obj:`bool`): If set to True and the input array is an Xarray,
                          the metadata from the input array will be copied to the
                          output array; default is False.
                          Warning: this option is not currently supported.

        Returns:
    	:class:`numpy.ndarray`: The return array will be K x N x M, where K
            represents the leftmost dimensions of data. It will be of type double if
            any of the input is double, and float otherwise.

        Description:
            This function puts unstructured data (randomly-spaced) onto the nearest
            locations of a rectilinear grid. A default value of `domain` option is
            now set to 1.0 instead of 0.0.

            This function does not perform interpolation; rather, each individual
            data point is assigned to the nearest grid point. It is possible that
            upon return, grid will contain grid points set to missing value if
            no `x(n)`, `y(n)` are nearby.

        Examples:

    	Example 1: Using triple2grid with :class:`xarray.DataArray` input

    	.. code-block:: python

    	    import numpy as np
    	    import xarray as xr
    	    import geocat.comp

    	    # Open a netCDF data file using xarray default engine and load the data stream
    	    ds = xr.open_dataset("./ruc.nc")

    	    # [INPUT] Grid & data info on the source curvilinear
    	    data = ds.DIST_236_CBL[:]
    	    x = ds.gridlat_236[:]
    	    y = ds.gridlon_236[:]
    	    xgrid = ds.gridlat_236[:]
    	    ygrid = ds.gridlon_236[:]


    	    # [OUTPUT] Grid on destination points grid (or read the 1D lat and lon from
    	    #	       an other .nc file.
    	    newlat1D_points=np.linspace(lat2D_curv.min(), lat2D_curv.max(), 100)
    	    newlon1D_points=np.linspace(lon2D_curv.min(), lon2D_curv.max(), 100)

    	    output = geocat.comp.triple2grid(x, y, data, xgrid, ygrid)
        """


# TODO: Revisit after deprecating geocat.ncomp for implementing this
def triple_to_grid_2d(x, y, data, xgrid, ygrid, msg_py):
    # ''' signature:  grid = triple2grid2d(x,y,data,xgrid,ygrid,msg_py)
    pass



# Transparent wrappers for geocat.ncomp backwards compatibility
def grid2triple(x, y, z, msg=None, meta=False):

    return grid_to_triple(z, x, y, msg)
