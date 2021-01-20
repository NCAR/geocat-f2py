# THIS IS A DEVELOPMENT PERFORMANCE TESTING CLASS, REMOVE WHEN NO LONGER NEEDED

import time
import dask
import dask.distributed as dd
from dask.array.core import map_blocks
import numpy as np
import xarray as xr
from geocat.f2py import (linint1, linint2, linint2pts)


def linint1_test():
    xi = np.linspace(1, 10, 200)
    xo = np.linspace(1, 10, 1000)
    fi = np.linspace(1, 200, 200000).reshape((100, 10, 200))
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
    xi = np.linspace(1, 10, 500)
    yi = np.linspace(1, 10, 200)
    xo = np.linspace(1, 10, 2000)
    yo = np.linspace(1, 10, 1000)
    fi = np.linspace(1, 200, 10000000).reshape((10, 10, 200, 500))
    # '''
    chunks = {
        'time': 1,
        'alt': 1,
        'lat': yi.shape[0],
        'lon': xi.shape[0],
    }
    # '''
    #'''
    fi = xr.DataArray(
        fi,
        coords={
            'lat': yi,
            'lon': xi,
        },
        dims=['time', 'alt', 'lat', 'lon'],
    ).chunk(chunks)
    #'''

    fo = linint2(
        fi,
        xo,
        yo,
        xi=xi,
        yi=yi,
    )


def linint2pts_test():
    xi = np.linspace(1, 10, 100)
    yi = np.linspace(1, 10, 100)
    xo = np.linspace(1, 10, 500)
    yo = np.linspace(1, 10, 500)
    fi = np.linspace(1, 200, 10000000).reshape((100, 10, 100, 100))
    #'''
    chunks = {
        'time': 1,
        'alt': 1,
        'lat': yi.shape,
        'lon': xi.shape,
    }
    #'''
    #'''
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
    )


if __name__ == '__main__':
    cluster = dd.LocalCluster(n_workers=8, threads_per_worker=1)
    print(cluster.dashboard_link)
    client = dd.Client(cluster)
    t0 = time.time()

    fo = linint2_test()
    t1 = time.time()
    print(t1 - t0)
    client.close()
