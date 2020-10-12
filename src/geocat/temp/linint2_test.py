import time

import dask.distributed as dd
import numpy as np
import xarray as xr

from geocat.temp import *


def linint1_test():
    xi = np.linspace(1, 10, 20)
    xo = np.linspace(1, 10, 40)
    fi = np.linspace(1, 200, 20000).reshape((100, 10, 20))
    # '''
    chunks = {
        'time': 1,
        'alt': 1,
        'lon': xi.shape,
    }
    # '''

    fi = xr.DataArray(
        fi,
        coords={
            'lon': xi,
        },
        dims=['time', 'alt', 'lon'],
    ).chunk(chunks)

    fo = linint1(
        fi,
        xo,
    )



def linint2_test():
    xi = np.linspace(1, 10, 100)
    yi = np.linspace(1, 10, 2000)
    xo = np.linspace(1, 10, 200)
    yo = np.linspace(1, 10, 4000)
    fi = np.linspace(1, 200, 20000000).reshape((10, 10, 2000, 100))
    # '''
    chunks = {
        'time': 1,
        'alt': 1,
        'lat': yi.shape,
        'lon': xi.shape,
    }
    # '''

    fi = xr.DataArray(
        fi,
        coords={
            'lat': yi,
            'lon': xi,
        },
        dims=['time', 'alt', 'lat', 'lon'],
    ).chunk(chunks)

    fo = linint2(
        fi,
        xo,
        yo,
    )



def linint2pts_test():
    xi = np.linspace(1, 10, 10)
    yi = np.linspace(1, 10, 10)
    xo = np.linspace(1, 10, 400)
    yo = np.linspace(1, 10, 400)
    fi = np.linspace(1, 200, 100000).reshape((100, 10, 10, 10))
    #'''
    chunks = {
        'time': 1,
        'alt': 1,
        'lat': yi.shape,
        'lon': xi.shape,
    }
    #'''
    '''
    fi = xr.DataArray(
        fi,
        coords={
            'lat': yi,
            'lon': xi,
        },
        dims=['time', 'alt', 'lat', 'lon'],

    ).chunk(chunks)
    #'''

    fo = linint2pts(
        fi,
        xo,
        yo,
        xi=xi,
        yi=yi,
    )



if __name__ == '__main__':
    cluster = dd.LocalCluster()
    client = dd.Client(cluster)
    t0 = time.time()

    # linint1_test()
    linint2_test()
    # linint2pts_test()

    t1 = time.time()

    print(t1 - t0)
