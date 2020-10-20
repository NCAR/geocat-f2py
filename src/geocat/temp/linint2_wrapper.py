import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from .errors import (ChunkError, CoordinateError)
from geocat.temp.fortran import (dlinint1, dlinint2, dlinint2pts)


# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.

def _linint1(xi, fi, xo, icycx, xmsg, shape):
    # ''' signature : fo = dlinint1(xi,fi,xo,[icycx,xmsg,iopt])
    fo = dlinint1(xi, fi, xo, icycx=icycx, xmsg=xmsg, )
    fo = np.asarray(fo)
    fo = fo.reshape(shape)
    return fo


def _linint2(xi, yi, fi, xo, yo, icycx, xmsg, shape):
    # ''' signature : fo = dlinint2(xi,yi,fi,xo,yo,[icycx,xmsg,iopt])
    fo = dlinint2(xi, yi, fi, xo, yo, icycx=icycx, xmsg=xmsg, )
    fo = np.asarray(fo)
    fo = fo.reshape(shape)
    return fo


def _linint2pts(xi, yi, fi, xo, yo, icycx, xmsg, shape):
    # ''' signature : fo = dlinint2pts(xi,yi,fi,xo,yo,[icycx,xmsg])
    fo = dlinint2pts(xi, yi, fi, xo, yo, icycx=icycx, xmsg=xmsg, )
    fo = np.asarray(fo)
    fo = fo.reshape(shape)
    return fo


# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.

def linint1(fi, xo, icycx=0, xmsg=-99):
    # ''' signature : fo = dlinint1(xi,fi,xo,[icycx,xmsg,iopt])

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):
        raise Exception("fi is required to be an xarray.DataArray")

    xi = fi.coords[fi.dims[-1]]

    # ensure rightmost dimensions of input are not chunked
    if list(fi.chunks)[-1:] != [xi.shape]:
        raise Exception("fi must be unchunked along the last dimension")

    # fo datastructure elements
    fo_chunks = list(fi.chunks)
    fo_chunks[-1:] = (xo.shape,)
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    fo_coords = {
        k: v for (k, v) in fi.coords.items()
    }
    fo_coords[fi.dims[-1]] = xo
    # ''' end of boilerplate

    fo = map_blocks(
        _linint1,
        xi,
        fi.data,
        xo,
        icycx,
        xmsg,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 1],
        new_axis=[fi.ndim - 1],
    )

    fo = xr.DataArray(fo.compute(), attrs=fi.attrs, dims=fi.dims, coords=fo_coords)
    return fo


def linint2(fi, xo, yo, xi=None, yi=None, icycx=0, xmsg=-99):
    # ''' signature : fo = dlinint2(xi,yi,fi,xo,yo,[icycx,xmsg,iopt])

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):
        if (xi is None) | (yi is None):
            raise CoordinateError(
                "linint2: Arguments xi and yi must be provided explicitly unless fi is an xarray.DataArray.")

        fi = xr.DataArray(
            fi,
        )
        fi_chunk = dict([(k, v) for (k, v) in zip(list(fi.dims), list(fi.shape))])

        fi = xr.DataArray(
            fi.data,
            coords={
                fi.dims[-1]: xi,
                fi.dims[-2]: yi,
            },
            dims=fi.dims,
        ).chunk(fi_chunk)

    xi = fi.coords[fi.dims[-1]]
    yi = fi.coords[fi.dims[-2]]


    # ensure rightmost dimensions of input are not chunked
    if list(fi.chunks)[-2:] != [yi.shape, xi.shape]:
        raise ChunkError("linint2: fi must be unchunked along the rightmost two dimensions")

    # fi data structure elements and autochunking
    fi_chunks = list(fi.dims)
    fi_chunks[:-2] = [(k, 1) for (k, v) in zip(list(fi.dims)[:-2], list(fi.chunks)[:-2])]
    fi_chunks[-2:] = [(k, v[0]) for (k, v) in zip(list(fi.dims)[-2:], list(fi.chunks)[-2:])]
    fi_chunks = dict(fi_chunks)
    fi = fi.chunk(fi_chunks)

    # fo datastructure elements
    fo_chunks = list(fi.chunks)
    fo_chunks[-2:] = (yo.shape, xo.shape)
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    fo_coords = {
        k: v for (k, v) in fi.coords.items()
    }
    fo_coords[fi.dims[-1]] = xo
    fo_coords[fi.dims[-2]] = yo
    # ''' end of boilerplate

    fo = map_blocks(
        _linint2,
        yi,
        xi,
        fi.data,
        yo,
        xo,
        icycx,
        xmsg,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2, fi.ndim - 1],
    )
    fo = xr.DataArray(fo.compute(), attrs=fi.attrs, dims=fi.dims, coords=fo_coords)
    return fo


def linint2pts(fi, xo, yo, icycx=0, xmsg=-99):
    # ''' signature : fo = dlinint2pts(xi,yi,fi,xo,yo,[icycx,xmsg,iopt])

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):
        raise Exception("fi is required to be an xarray.DataArray")

    xi = fi.coords[fi.dims[-1]]
    yi = fi.coords[fi.dims[-2]]

    if xo.shape != yo.shape:
        raise Exception("xo and yo, be be of equal length")

    # ensure rightmost dimensions of input are not chunked
    if list(fi.chunks)[-2:] != [yi.shape, xi.shape]:
        raise Exception("fi must be unchunked along the last two dimensions")

    # fo datastructure elements
    fo_chunks = list(fi.chunks)
    fo_chunks[-2:] = (xo.shape,)
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    fo_shape = fo_shape
    fo_coords = {
        k: v for (k, v) in fi.coords.items()
    }
    # fo_coords.remove(fi.dims[-1]) # this dimension dissapears
    fo_coords[fi.dims[-1]] = xo  # remove this line omce dims are figured out
    fo_coords[fi.dims[-2]] = yo  # maybe replace with 'pts'
    # ''' end of boilerplate

    fo = map_blocks(
        _linint2pts,
        yi,
        xi,
        fi.data,
        yo,
        xo,
        icycx,
        xmsg,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2],
    )
    fo = xr.DataArray(fo.compute(), attrs=fi.attrs)
    return fo
