import numpy as np
import xarray as xr
import geocat.f2py
n = 10

n= 10

xi = np.linspace(0, n, num=n // 2 + 1, dtype=np.float64)
yi = np.linspace(0, n, num=n // 2 + 1, dtype=np.float64)
yi_reverse = yi[::-1].copy()
xo = np.linspace(xi.min(), xi.max(), num=xi.shape[0] * 2 - 1)
yo = np.linspace(yi.min(), yi.max(), num=yi.shape[0] * 2 - 1)
fi_np = np.random.rand(96, 3, len(yi), len(xi)).astype(np.float64)

chunks = {
    'time': fi_np.shape[0],
    'level': fi_np.shape[1],
    'lat': fi_np.shape[2],
    'lon': fi_np.shape[3]
}


def test_linint2():
    fi = xr.DataArray(fi_np,
                      dims=['time', 'level', 'lat', 'lon'],
                      coords={
                          'lat': yi,
                          'lon': xi
                      }).chunk(chunks)
    fo = geocat.temp.linint2(fi, xo, yo, 0)
    np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)

test_linint2()