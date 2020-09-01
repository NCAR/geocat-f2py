import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from geocat.temp.fortran import (dlinint2)

def _linint2(xi, yi, fi, xo, yo, icycx, xmsg, shape):
    fo = dlinint2(xi, yi, fi, xo, yo, icycx=icycx, xmsg=xmsg,)
    fo = np.asarray(fo)
    fo = fo.reshape(shape) # reshape returns a copy. it does not modify the original array.
    print(fo.shape)
    return fo

def linint2( fi, xo, yo, icycx=0, xmsg=-99):
    # '''
    if not isinstance(fi, xr.DataArray):
        raise Exception("fi is required to be an xarray.DataArray")

    xi = fi.coords[fi.dims[-1]]
    yi = fi.coords[fi.dims[-2]]

    # ensure rightmost dimensions of input are not chunked
    if list(fi.chunks)[-2:] != [yi.shape, xi.shape]:
        raise Exception("fi must be unchunked along the last two dimensions")
    # '''

    # fo datastructure elements
    fo_chunks = list(fi.chunks)
    fo_chunks[-2:] = (yo.shape, xo.shape)
    print(fo_shape)
    #print(fo_chunks)
    fo_dtype = fi.dtype

    fo = map_blocks(
        _linint2,
        yi,
        xi,
        fi.data,
        yo,
        xo,
        icycx,
        xmsg,
        shape,
        chunks=fo_chunks,
        dtype=fo_dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2, fi.ndim - 1],
    )
    fo.compute()
    '''
    coords = {
        k: v if k not in fi.dims[-2:] else (xo if k == fi.dims[-1] else yo)
        for (k, v) in fi.coords.items()
    }

    fo = xr.DataArray(fo, attrs=fi.attrs, dims=fi.dims, coords=coords)
    #'''
    return fo


def linint2_tests():
    n = 127

    xi = np.linspace(1, 10, 10)
    yi = np.linspace(1, 10, 20)
    xo = np.linspace(1, 10, 20)
    yo = np.linspace(1, 10, 40)
    fi = np.linspace(1, 200, 20000).reshape((10, 10, 20, 10))
    # '''
    chunks = {
        'time': 1,
        'alt': 1,
        'lat': fi.shape[2],
        'lon': fi.shape[3],
    }
    # '''

    fi = xr.DataArray(
        fi,
        dims=['time', 'alt', 'lat', 'lon'],
        coords={
            'lat': yi,
            'lon': xi,
        },
    ).chunk(chunks)

    fo = linint2(
        fi,
        xo,
        yo,
    )

    #print(fo)
    print("done")


linint2_tests()
