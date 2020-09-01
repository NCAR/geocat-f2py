import numpy as np
import xarray as xr

from geocat.temp.fortran import (dlinint2)


def linint2(fi, xo, yo, xi=None, yi=None):
    # '''
    if not isinstance(fi, xr.DataArray):
        fi = xr.DataArray(fi)

    if xi is None:
        xi = fi.coords[fi.dims[-2]]

    if yi is None:
        yi = fi.coords[fi.dims[-1]]

    # '''

    fo = dlinint2(xi, yi, fi, xo, yo)
    return fo


def linint2_tests():
    n = 127

    xi = np.linspace(1, 10, 10)
    yi = np.linspace(1, 10, 20)
    xo = np.linspace(1, 10, 20)
    yo = np.linspace(1, 10, 40)
    fi = np.linspace(1, 200, 200).reshape((1, 10, 20))
    '''
    chunks = {
        'alt': fi.shape[0],
        'lat': fi.shape[1],
        'lon': fi.shape[2],
    }
    #'''

    fi = xr.DataArray(fi,
                      dims=['alt', 'lat', 'lon'],
                      coords={
                          'lat': xi,
                          'lon': yi,
                      },
                      )
    fo = linint2(fi, xo, yo)

    print(fo)


linint2_tests()
