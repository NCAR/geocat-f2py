import numpy as np
import xarray as xr
from geocat.temp import *

def linint2_tests():
    xi = np.linspace(1, 10, 10)
    yi = np.linspace(1, 10, 20)
    xo = np.linspace(1, 10, 20)
    yo = np.linspace(1, 10, 40)
    fi = np.linspace(1, 200, 200000).reshape((100, 10, 20, 10))
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

    print(fo.values)
    print("done")

linint2_tests()