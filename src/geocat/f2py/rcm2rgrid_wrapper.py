import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from .fortran import (drcm2rgrid, drgrid2rcm)
from .errors import (ChunkError, CoordinateError)
from .missing_values import (fort2py_msg, py2fort_msg)


# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.


def _rcm2rgrid(lat2d, lon2d, fi, lat1d, lon1d, msg_py, shape):

    fi = np.transpose(fi, axes=(2,1,0))
    lat2d = np.transpose(lat2d, axes=(1,0))
    lon2d = np.transpose(lon2d, axes=(1,0))

    fi, msg_py, msg_fort = py2fort_msg(fi, msg_py=msg_py)

    fo = drcm2rgrid(lat2d, lon2d, fi, lat1d, lon1d, xmsg=msg_fort)
    fo = np.asarray(fo)
    fo = np.transpose(fo, axes=(2,1,0))

    fort2py_msg(fo, msg_fort=msg_fort, msg_py=msg_py)

    return fo


def _rgrid2rcm(lat1d, lon1d, fi, lat2d, lon2d, msg_py, shape):

    fi = np.transpose(fi, axes=(2,1,0))
    lat2d = np.transpose(lat2d, axes=(1,0))
    lon2d = np.transpose(lon2d, axes=(1,0))

    fi, msg_py, msg_fort = py2fort_msg(fi, msg_py=msg_py)

    fo = drgrid2rcm(lat1d, lon1d, fi, lat2d, lon2d, xmsg=msg_fort)
    fo = np.asarray(fo)
    fo = np.transpose(fo, axes=(2,1,0))

    fort2py_msg(fo, msg_fort=msg_fort, msg_py=msg_py)

    return fo


# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.


def rcm2rgrid(lat2d, lon2d, fi, lat1d, lon1d, msg_py=None):

    if (lon2d is None) | (lat2d is None):
        raise CoordinateError(
            "rcm2rgrid: lon2d and lat2d should always be provided")

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):

        fi = xr.DataArray(
            fi,
        )
        fi_chunk = dict([(k, v) for (k, v) in zip(list(fi.dims), list(fi.shape))])

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
    if list(fi.chunks)[-2:] != [(lat2d.shape[0],), (lat2d.shape[1],)]:
                             # [(lon2d.shape[0]), (lon2d.shape[1])] would also be used
        raise ChunkError("rcm2rgrid: fi must be unchunked along the rightmost two dimensions")

    # fi data structure elements and autochunking
    fi_chunks = list(fi.dims)
    fi_chunks[:-2] = [(k, 1) for (k, v) in zip(list(fi.dims)[:-2], list(fi.chunks)[:-2])]
    fi_chunks[-2:] = [(k, v[0]) for (k, v) in zip(list(fi.dims)[-2:], list(fi.chunks)[-2:])]
    fi_chunks = dict(fi_chunks)
    fi = fi.chunk(fi_chunks)

    # fo datastructure elements
    fo_chunks = list(fi.chunks)
    fo_chunks[-2:] = (lat1d.shape, lon1d.shape)
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    fo_coords = {
        k: v for (k, v) in fi.coords.items()
    }
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
        msg_py,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2, fi.ndim - 1],
    )
    fo = xr.DataArray(fo.compute(), attrs=fi.attrs, dims=fi.dims, coords=fo_coords)
    return fo


def rgrid2rcm(lat1d, lon1d, fi, lat2d=None, lon2d=None, msg_py=None):

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):
        if (lon1d is None) | (lat1d is None):
            raise CoordinateError(
                "rgrid2rcm: Arguments lon1d and lat1d must be provided explicitly unless fi is an xarray.DataArray.")

        fi = xr.DataArray(
            fi,
        )
        fi_chunk = dict([(k, v) for (k, v) in zip(list(fi.dims), list(fi.shape))])

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

    # ensure rightmost dimensions of input are not chunked
    if list(fi.chunks)[-2:] != [lat1d.shape, lon1d.shape]:
        raise Exception("fi must be unchunked along the last two dimensions")

    # fi data structure elements and autochunking
    fi_chunks = list(fi.dims)
    fi_chunks[:-2] = [(k, 1) for (k, v) in zip(list(fi.dims)[:-2], list(fi.chunks)[:-2])]
    fi_chunks[-2:] = [(k, v[0]) for (k, v) in zip(list(fi.dims)[-2:], list(fi.chunks)[-2:])]
    fi_chunks = dict(fi_chunks)
    fi = fi.chunk(fi_chunks)

    # fo datastructure elements
    fo_chunks = list(fi.chunks)
    fo_chunks[-2:] = [(lat2d.shape[0],), (lat2d.shape[1],)]
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    fo_coords = {
        k: v for (k, v) in fi.coords.items()
    }
    # fo_coords[fi.dims[-1]] = lon2d
    # fo_coords[fi.dims[-2]] = lat2d
    # ''' end of boilerplate

    fo = map_blocks(
        _rgrid2rcm,
        lat1d,
        lon1d,
        fi.data,
        lat2d,
        lon2d,
        msg_py,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2, fi.ndim - 1],
    )
    fo = xr.DataArray(fo.compute(), attrs=fi.attrs, dims=fi.dims, coords=fo_coords)
    return fo
