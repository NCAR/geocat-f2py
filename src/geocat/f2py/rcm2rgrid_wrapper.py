import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from .errors import ChunkError, CoordinateError
from .fortran import drcm2rgrid, drgrid2rcm
from .missing_values import fort2py_msg, py2fort_msg

# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.


def _rcm2rgrid(lat2d, lon2d, fi, lat1d, lon1d, msg_py, shape):

    fi = np.transpose(fi, axes=(2, 1, 0))
    lat2d = np.transpose(lat2d, axes=(1, 0))
    lon2d = np.transpose(lon2d, axes=(1, 0))

    fi, msg_py, msg_fort = py2fort_msg(fi, msg_py=msg_py)

    fo = drcm2rgrid(lat2d, lon2d, fi, lat1d, lon1d, xmsg=msg_fort)
    fo = np.asarray(fo)
    fo = np.transpose(fo, axes=(2, 1, 0))

    fort2py_msg(fo, msg_fort=msg_fort, msg_py=msg_py)

    return fo


def _rgrid2rcm(lat1d, lon1d, fi, lat2d, lon2d, msg_py, shape):

    fi = np.transpose(fi, axes=(2, 1, 0))
    lat2d = np.transpose(lat2d, axes=(1, 0))
    lon2d = np.transpose(lon2d, axes=(1, 0))

    fi, msg_py, msg_fort = py2fort_msg(fi, msg_py=msg_py)

    fo = drgrid2rcm(lat1d, lon1d, fi, lat2d, lon2d, xmsg=msg_fort)
    fo = np.asarray(fo)
    fo = np.transpose(fo, axes=(2, 1, 0))

    fort2py_msg(fo, msg_fort=msg_fort, msg_py=msg_py)

    return fo


# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.


def rcm2rgrid(lat2d, lon2d, fi, lat1d, lon1d, msg=None, meta=False):
    """Interpolates data on a curvilinear grid (i.e. RCM, WRF, NARR) to a
    rectilinear grid.

    Parameters
    ----------

    lat2d : :class:`numpy.ndarray`:
        A two-dimensional array that specifies the latitudes locations
        of fi. Because this array is two-dimensional it is not an associated
        coordinate variable of `fi`. The latitude order must be south-to-north.

    lon2d : :class:`numpy.ndarray`:
        A two-dimensional array that specifies the longitude locations
        of fi. Because this array is two-dimensional it is not an associated
        coordinate variable of `fi`. The latitude order must be west-to-east.

    fi : :class:`numpy.ndarray`:
        A multi-dimensional array to be interpolated. The rightmost two
        dimensions (latitude, longitude) are the dimensions to be interpolated.

    lat1d : :class:`numpy.ndarray`:
        A one-dimensional array that specifies the latitude coordinates of
        the regular grid. Must be monotonically increasing.

    lon1d : :class:`numpy.ndarray`:
        A one-dimensional array that specifies the longitude coordinates of
        the regular grid. Must be monotonically increasing.

    msg : :obj:`numpy.number`:
        A numpy scalar value that represent a missing value in fi.
        This argument allows a user to use a missing value scheme
        other than NaN or masked arrays, similar to what NCL allows.

    meta : :obj:`bool`:
        If set to True and the input array is an Xarray, the metadata
        from the input array will be copied to the output array;
        default is False.
        Warning: This option is not currently supported.

    Returns
    -------

    fo : :class:`numpy.ndarray`:
        The interpolated grid. A multi-dimensional array
        of the same size as fi except that the rightmost dimension sizes have been
        replaced by the sizes of lat1d and lon1d respectively.
        Double if fi is double, otherwise float.

    Description
    -----------

        Interpolates RCM (Regional Climate Model), WRF (Weather Research and Forecasting) and
        NARR (North American Regional Reanalysis) grids to a rectilinear grid. Actually, this
        function will interpolate most grids that use curvilinear latitude/longitude grids.
        No extrapolation is performed beyond the range of the input coordinates. Missing values
        are allowed but ignored.

        The weighting method used is simple inverse distance squared. Missing values are allowed
        but ignored.

        The code searches the input curvilinear grid latitudes and longitudes for the four
        grid points that surround a specified output grid coordinate. Because one or more of
        these input points could contain missing values, fewer than four points
        could be used in the interpolation.

        Curvilinear grids which have two-dimensional latitude and longitude coordinate axes present
        some issues because the coordinates are not necessarily monotonically increasing. The simple
        search algorithm used by rcm2rgrid is not capable of handling all cases. The result is that,
        sometimes, there are small gaps in the interpolated grids. Any interior points not
        interpolated in the initial interpolation pass will be filled using linear interpolation.

        In some cases, edge points may not be filled.

    Examples
    --------

    Example 1: Using rcm2rgrid with :class:`xarray.DataArray` input

    .. code-block:: python

        import numpy as np
        import xarray as xr
        import geocat.comp

        # Open a netCDF data file using xarray default engine and load the data stream
        ds = xr.open_dataset("./ruc.nc")

        # [INPUT] Grid & data info on the source curvilinear
        ht_curv=ds.DIST_236_CBL[:]
        lat2D_curv=ds.gridlat_236[:]
        lon2D_curv=ds.gridlon_236[:]

        # [OUTPUT] Grid on destination rectilinear grid (or read the 1D lat and lon from
        #          an other .nc file.
        newlat1D_rect=np.linspace(lat2D_curv.min(), lat2D_curv.max(), 100)
        newlon1D_rect=np.linspace(lon2D_curv.min(), lon2D_curv.max(), 100)

        ht_rect = geocat.comp.rcm2rgrid(lat2D_curv, lon2D_curv, ht_curv, newlat1D_rect, newlon1D_rect)
    """
    if (lon2d is None) | (lat2d is None):
        raise CoordinateError(
            "rcm2rgrid: lon2d and lat2d should always be provided")

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):

        fi = xr.DataArray(fi,)
        fi_chunk = dict([(k, v) for (k, v) in zip(list(fi.dims), list(fi.shape))
                        ])

        fi = xr.DataArray(
            fi.data,
            # coords={
            #     fi.dims[-1]: lon2d,
            #     fi.dims[-2]: lat2d,
            # },
            dims=fi.dims,
        ).chunk(fi_chunk)

    # lon2d = fi.coords[fi.dims[-1]]
    # lat2d = fi.coords[fi.dims[-2]]

    # ensure rightmost dimensions of input are not chunked
    if fi.chunks is None:
        fi = fi.chunk()

    if list(fi.chunks)[-2:] != [(lat2d.shape[0],), (lat2d.shape[1],)]:
        # [(lon2d.shape[0]), (lon2d.shape[1])] would also be used
        raise ChunkError(
            "rcm2rgrid: fi must be unchunked along the rightmost two dimensions"
        )

    # fi data structure elements and autochunking
    fi_chunks = list(fi.dims)
    fi_chunks[:-2] = [
        (k, 1) for (k, v) in zip(list(fi.dims)[:-2],
                                 list(fi.chunks)[:-2])
    ]
    fi_chunks[-2:] = [
        (k, v[0]) for (k, v) in zip(list(fi.dims)[-2:],
                                    list(fi.chunks)[-2:])
    ]
    fi_chunks = dict(fi_chunks)
    fi = fi.chunk(fi_chunks)

    # fo datastructure elements
    fo_chunks = list(fi.chunks)
    fo_chunks[-2:] = (lat1d.shape, lon1d.shape)
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    fo_coords = {k: v for (k, v) in fi.coords.items()}
    fo_coords[fi.dims[-1]] = lon1d
    fo_coords[fi.dims[-2]] = lat1d
    # ''' end of boilerplate

    fo = map_blocks(
        _rcm2rgrid,
        lat2d,
        lon2d,
        fi.data,
        lat1d,
        lon1d,
        msg,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2, fi.ndim - 1],
    )
    fo = xr.DataArray(fo.compute(),
                      attrs=fi.attrs,
                      dims=fi.dims,
                      coords=fo_coords)
    return fo


def rgrid2rcm(lat1d, lon1d, fi, lat2d, lon2d, msg=None, meta=False):
    """Interpolates data on a rectilinear lat/lon grid to a curvilinear grid
    like those used by the RCM, WRF and NARR models/datasets.

    Parameters
    ----------

    lat1d : :class:`numpy.ndarray`:
        A one-dimensional array that specifies the latitude coordinates of
        the regular grid. Must be monotonically increasing.

    lon1d : :class:`numpy.ndarray`:
        A one-dimensional array that specifies the longitude coordinates of
        the regular grid. Must be monotonically increasing.

    fi : :class:`numpy.ndarray`:
        A multi-dimensional array to be interpolated. The rightmost two
        dimensions (latitude, longitude) are the dimensions to be interpolated.

    lat2d : :class:`numpy.ndarray`:
        A two-dimensional array that specifies the latitude locations
        of fi. Because this array is two-dimensional it is not an associated
        coordinate variable of `fi`.

    lon2d : :class:`numpy.ndarray`:
        A two-dimensional array that specifies the longitude locations
        of fi. Because this array is two-dimensional it is not an associated
        coordinate variable of `fi`.

    msg :obj:`numpy.number`:
        A numpy scalar value that represent a missing value in fi.
        This argument allows a user to use a missing value scheme
        other than NaN or masked arrays, similar to what NCL allows.

    meta :obj:`bool`:
        If set to True and the input array is an Xarray, the metadata
        from the input array will be copied to the output array;
        default is False.
        Warning: this option is not currently supported.

    Returns
    -------

    fo : :class:`numpy.ndarray`: The interpolated grid. A multi-dimensional array of the
    same size as `fi` except that the rightmost dimension sizes have been replaced
    by the sizes of `lat2d` and `lon2d` respectively. Double if `fi` is double,
    otherwise float.

    Description
    -----------

        Interpolates data on a rectilinear lat/lon grid to a curvilinear grid, such as those
    used by the RCM (Regional Climate Model), WRF (Weather Research and Forecasting) and
    NARR (North American Regional Reanalysis) models/datasets. No extrapolation is
    performed beyond the range of the input coordinates. The method used is simple inverse
    distance weighting. Missing values are allowed but ignored.

    Examples
    --------

    Example 1: Using rgrid2rcm with :class:`xarray.DataArray` input

    .. code-block:: python

        import numpy as np
        import xarray as xr
        import geocat.comp

        # Open a netCDF data file using xarray default engine and load the data stream
        # input grid and data
        ds_rect = xr.open_dataset("./DATAFILE_RECT.nc")

        # [INPUT] Grid & data info on the source rectilinear
        ht_rect   =ds_rect.SOME_FIELD[:]
        lat1D_rect=ds_rect.gridlat_[:]
        lon1D_rect=ds_rect.gridlon_[:]

        # Open a netCDF data file using xarray default engine and load the data stream
        # for output grid
        ds_curv = xr.open_dataset("./DATAFILE_CURV.nc")

        # [OUTPUT] Grid on destination curvilinear grid (or read the 2D lat and lon from
        #          an other .nc file
        newlat2D_rect=ds_curv.gridlat2D_[:]
        newlon2D_rect=ds_curv.gridlat2D_[:]

        ht_curv = geocat.comp.rgrid2rcm(lat1D_rect, lon1D_rect, ht_rect, newlat2D_curv, newlon2D_curv)
    """

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):
        if (lon1d is None) | (lat1d is None):
            raise CoordinateError(
                "rgrid2rcm: Arguments lon1d and lat1d must be provided explicitly unless fi is an xarray.DataArray."
            )

        fi = xr.DataArray(fi,)
        fi_chunk = dict([(k, v) for (k, v) in zip(list(fi.dims), list(fi.shape))
                        ])

        fi = xr.DataArray(
            fi.data,
            coords={
                fi.dims[-1]: lon1d,
                fi.dims[-2]: lat1d,
            },
            dims=fi.dims,
        ).chunk(fi_chunk)

    lon1d = fi.coords[fi.dims[-1]]
    lat1d = fi.coords[fi.dims[-2]]

    # Convert 2d arrays to xarray for map_blocks call below if they are numpy
    lat2d = xr.DataArray(lat2d)
    lon2d = xr.DataArray(lon2d)

    # If an unchunked Xarray input is given, chunk it just with its dims
    if fi.chunks is None:
        fi = fi.chunk()

    if list(fi.chunks)[-2:] != [lat1d.shape, lon1d.shape]:
        raise Exception("fi must be unchunked along the last two dimensions")

    # fi data structure elements and autochunking
    fi_chunks = list(fi.dims)
    fi_chunks[:-2] = [
        (k, 1) for (k, v) in zip(list(fi.dims)[:-2],
                                 list(fi.chunks)[:-2])
    ]
    fi_chunks[-2:] = [
        (k, v[0]) for (k, v) in zip(list(fi.dims)[-2:],
                                    list(fi.chunks)[-2:])
    ]
    fi_chunks = dict(fi_chunks)
    fi = fi.chunk(fi_chunks)

    # fo datastructure elements
    fo_chunks = list(fi.chunks)
    fo_chunks[-2:] = [(lat2d.shape[0],), (lat2d.shape[1],)]
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    fo_coords = {k: v for (k, v) in fi.coords.items()}
    # fo_coords[fi.dims[-1]] = lon2d
    # fo_coords[fi.dims[-2]] = lat2d
    # ''' end of boilerplate

    fo = map_blocks(
        _rgrid2rcm,
        lat1d,
        lon1d,
        fi.data,
        lat2d.data,
        lon2d.data,
        msg,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2, fi.ndim - 1],
    )

    fo = xr.DataArray(fo.compute(), attrs=fi.attrs, dims=fi.dims)
    return fo
