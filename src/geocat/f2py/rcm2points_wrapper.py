import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from geocat.f2py.errors import ChunkError, CoordinateError
from geocat.f2py.fortran import drcm2points
from geocat.f2py.missing_values import fort2py_msg, py2fort_msg

from .errors import DimensionError

# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.


def _rcm2points(lat2d, lon2d, fi, lat1d, lon1d, msg_py, opt, shape):
    fi = np.transpose(fi, axes=(2, 1, 0))
    lat2d = np.transpose(lat2d, axes=(1, 0))
    lon2d = np.transpose(lon2d, axes=(1, 0))

    fi, msg_py, msg_fort = py2fort_msg(fi, msg_py=msg_py)

    fo = drcm2points(lat2d, lon2d, fi, lat1d, lon1d, xmsg=msg_fort, opt=opt)
    fo = np.asarray(fo)
    fo = fo.reshape(shape)

    fort2py_msg(fi, msg_fort=msg_fort, msg_py=msg_py)
    fort2py_msg(fo, msg_fort=msg_fort, msg_py=msg_py)

    return fo


# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.


def rcm2points(lat2d, lon2d, fi, lat1d, lon1d, opt=0, msg=None, meta=False):
    """Interpolates data on a curvilinear grid (i.e. RCM, WRF, NARR) to an
    unstructured grid.

    Paraemeters
    -----------
    lat2d : :class:`numpy.ndarray`:
        A two-dimensional array that specifies the latitudes locations
        of fi. The latitude order must be south-to-north.

    lon2d : :class:`numpy.ndarray`:
        A two-dimensional array that specifies the longitude locations
        of fi. The latitude order must be west-to-east.

    fi : :class:`numpy.ndarray`:
        A multi-dimensional array to be interpolated. The rightmost two
        dimensions (latitude, longitude) are the dimensions to be interpolated.

    lat1d : :class:`numpy.ndarray`:
        A one-dimensional array that specifies the latitude coordinates of
        the output locations.

    lon1d : :class:`numpy.ndarray`:
        A one-dimensional array that specifies the longitude coordinates of
        the output locations.

    opt : :obj:`numpy.number`:
        opt=0 or 1 means use an inverse distance weight interpolation.
        opt=2 means use a bilinear interpolation.

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

        :class:`numpy.ndarray`: The interpolated grid. A multi-dimensional array
        of the same size as fi except that the rightmost dimension sizes have been
        replaced by the number of coordinate pairs (lat1dPoints, lon1dPoints).
        Double if fi is double, otherwise float.

    Description
    -----------

        Interpolates data on a curvilinear grid, such as those used by the RCM
        (Regional Climate Model), WRF (Weather Research and Forecasting) and NARR
        (North American Regional Reanalysis) models/datasets to an unstructured grid.
        All of these have latitudes that are oriented south-to-north. An inverse
        distance squared algorithm is used to perform the interpolation. Missing
        values are allowed and no extrapolation is performed.
    """

    if (lon2d is None) | (lat2d is None):
        raise CoordinateError(
            "rcm2points: lon2d and lat2d should always be provided")

    # Basic sanity checks
    if lat2d.shape[0] != lon2d.shape[0] or lat2d.shape[1] != lon2d.shape[1]:
        raise DimensionError(
            "ERROR rcm2points: The input lat/lon grids must be the same size !")

    if lat1d.shape[0] != lon1d.shape[0]:
        raise DimensionError(
            "ERROR rcm2points: The output lat/lon grids must be same size !")

    if lat2d.shape[0] < 2 or lon2d.shape[0] < 2 or lat2d.shape[
            1] < 2 or lon2d.shape[1] < 2:
        raise DimensionError(
            "ERROR rcm2points: The input/output lat/lon grids must have at least 2 elements !"
        )

    if fi.ndim < 2:
        raise DimensionError(
            "ERROR rcm2points: fi must be at least two dimensions !\n")

    if fi.shape[fi.ndim - 2] != lat2d.shape[0] or fi.shape[fi.ndim -
                                                           1] != lon2d.shape[1]:
        raise DimensionError(
            "ERROR rcm2points: The rightmost dimensions of fi must be (nlat2d x nlon2d),"
            "where nlat2d and nlon2d are the size of the lat2d/lon2d arrays !")

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):
        fi = xr.DataArray(fi,)
        fi_chunk = dict([(k, v) for (k, v) in zip(list(fi.dims), list(fi.shape))
                        ])

        fi = xr.DataArray(
            fi.data,
            dims=fi.dims,
        ).chunk(fi_chunk)

    # ensure rightmost dimensions of input are not chunked
    if fi.chunks is None:
        fi = fi.chunk()

    if list(fi.chunks)[-2:] != [(lat2d.shape[0],), (lat2d.shape[1],)]:
        # [(lon2d.shape[0]), (lon2d.shape[1])] could also be used
        raise ChunkError(
            "rcm2points: fi must be unchunked along the rightmost two dimensions"
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
    fo_chunks[-2:] = (lon1d.shape,)
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    # ''' end of boilerplate

    fo = map_blocks(
        _rcm2points,
        lat2d,
        lon2d,
        fi.data,
        lat1d,
        lon1d,
        msg,
        opt,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2],
    )

    fo = xr.DataArray(fo.compute(), attrs=fi.attrs)
    return fo
