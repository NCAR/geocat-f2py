import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from geocat.temp.fortran import (dlinint2)


def _linint2(xi, yi, fi, xo, yo, icycx, xmsg, shape):
    fo = dlinint2(xi, yi, fi, xo, yo, icycx=icycx, xmsg=xmsg, )
    fo = np.asarray(fo)
    fo = fo.reshape(shape)
    return fo


def linint2(fi, xo, yo, icycx=0, xmsg=-99):
    if not isinstance(fi, xr.DataArray):
        raise Exception("fi is required to be an xarray.DataArray")

    xi = fi.coords[fi.dims[-1]]
    yi = fi.coords[fi.dims[-2]]

    # ensure rightmost dimensions of input are not chunked
    if list(fi.chunks)[-2:] != [yi.shape, xi.shape]:
        raise Exception("fi must be unchunked along the last two dimensions")

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
    fo.compute()
    fo = xr.DataArray(fo, attrs=fi.attrs, dims=fi.dims, coords=fo_coords)
    return fo