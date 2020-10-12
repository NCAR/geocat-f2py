import numpy as np
import xarray as xr
from dask.array.core import map_blocks

# from geocat.temp.fortran import (drcm2rgrid, drgrid2rcm)
from .fortran import (drcm2rgrid, drgrid2rcm)


# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.


def _rcm2rgrid(lat2d, lon2d, fi, lat1d, lon1d, ncrit, xmsg, shape):
    fo = drcm2rgrid(lat2d, lon2d, fi, lat1d, lon1d, icycx=ncrit, xmsg=xmsg)
    fo = np.asarray(fo)
    fo = fo.reshape(shape)
    return fo


def _rgrid2rcm(lat2d, lon2d, fi, lat1d, lon1d, ncrit, xmsg, shape):
    fo = drgrid2rcm(lat2d, lon2d, fi, lat1d, lon1d, icycx=ncrit, xmsg=xmsg)
    fo = np.asarray(fo)
    fo = fo.reshape(shape)
    return fo


# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.

def rcm2rgrid(fi, lon1d, lat1d, lon2d=None, lat2d=None, ncrit=0, xmsg=None):

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):
        if (lon2d == None) | (lat2d == None):
            raise Exception(
                "fi is required to be an xarray.DataArray if xi and yi are not provided")
        fi = xr.DataArray(
            fi,
            coords={
                'xi': lon2d,
                'yi': lat2d,
            }
        )

    lon2d = fi.coords[fi.dims[-1]]
    lat2d = fi.coords[fi.dims[-2]]

    # ensure rightmost dimensions of input are not chunked
    if list(fi.chunks)[-2:] != [lat2d.shape, lon2d.shape]:
        raise Exception("fi must be unchunked along the last two dimensions")

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
        ncrit,
        xmsg,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2, fi.ndim - 1],
    )
    fo = xr.DataArray(fo.compute(), attrs=fi.attrs, dims=fi.dims, coords=fo_coords)
    return fo


def rgrid2rcm(fi, lon1d, lat1d, lon2d=None, lat2d=None, ncrit=0, xmsg=None):

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):
        if (lon2d == None) | (lat2d == None):
            raise Exception(
                "fi is required to be an xarray.DataArray if xi and yi are not provided")
        fi = xr.DataArray(
            fi,
            coords={
                'xi': lon2d,
                'yi': lat2d,
            }
        )

    lon2d = fi.coords[fi.dims[-1]]
    lat2d = fi.coords[fi.dims[-2]]

    # ensure rightmost dimensions of input are not chunked
    if list(fi.chunks)[-2:] != [lat2d.shape, lon2d.shape]:
        raise Exception("fi must be unchunked along the last two dimensions")

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
        _rgrid2rcm,
        lat2d,
        lon2d,
        fi.data,
        lat1d,
        lon1d,
        ncrit,
        xmsg,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2, fi.ndim - 1],
    )
    fo = xr.DataArray(fo.compute(), attrs=fi.attrs, dims=fi.dims, coords=fo_coords)
    return fo
