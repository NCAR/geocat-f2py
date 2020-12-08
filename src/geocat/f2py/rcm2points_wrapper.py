import numpy as np
import xarray as xr

from dask.array.core import map_blocks
from geocat.f2py.fortran import (drcm2points)
from geocat.f2py.errors import (CoordinateError, ChunkError)
from geocat.f2py.missing_values import (fort2py_msg, py2fort_msg)


# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.


def _rcm2points(yi, xi, fi, yo, xo, msg_py, opt, shape):
    # fo = drcm2points(yi,xi,fi,yo,xo,[xmsg,opt])
    fi = np.transpose(fi, axes=[0,1])
    # yi = np.transpose(yi, axes=(1,0))
    # xi = np.transpose(xi, axes=(1,0))

    fi, msg_py, msg_fort = py2fort_msg(fi, msg_py=msg_py)
    print(fi)
    fo = drcm2points(yi, xi, fi, yo, xo, xmsg=msg_fort, opt=opt)
    fo = np.asarray(fo)
    fo = fo.reshape(shape)
    
    fort2py_msg(fi, msg_fort=msg_fort, msg_py=msg_py)
    fort2py_msg(fo, msg_fort=msg_fort, msg_py=msg_py)
    
    return fo


# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.


# def rcm2points(lat2d,lon2d, fi, lat1d, lon1d, opt=0, msg=None):
def rcm2points(yi,
               xi,
               fi,
               yo,
               xo,
               msg_py=None,
               opt=0):
    
         # ''' signature : fo = drcm2points(yi,xi,fi,yo,xo,[xmsg,opt])

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):
        if (xi is None) | (yi is None):
            raise CoordinateError(
                "rcm2points: Arguments xi and yi must be provided explicitly unless fi is an xarray.DataArray.")

        fi = xr.DataArray(
            fi,
        )
        fi_chunk = dict([(k, v) for (k, v) in zip(list(fi.dims), list(fi.shape))])

        fi = fi.chunk(fi_chunk)

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
    fo_chunks[-2:] = (xo.shape,)
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    
    
    # ''' end of boilerplate

    fo = map_blocks(
        _rcm2points,
        yi,
        xi,
        fi.data,
        yo,
        xo,
        msg_py,
        opt,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2],
    )
    fo = xr.DataArray(fo.compute(), attrs=fi.attrs)
    return fo