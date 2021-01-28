import numpy as np
import numpy.testing as nt
import xarray as xr
import geocat.f2py

import sys
import time
import unittest as ut

# nominal input
fi_nom = np.asarray([
    1.870327, 1.872924, 2.946794, 1.98253, 1.353965, 0.8730035, 0.1410671,
    1.877125, 1.931963, -0.1676207, 1.917912, 1.735453, -1.82497, 1.01385,
    1.053591, 1.754721, 1.177423, 0.381366, 2.015617, 0.4975608, 2.169137,
    0.3293635, 0.6676366, 2.691788
]).reshape((2, 3, 4))

# nan input
fi_nan = fi_nom.copy()
fi_nan[0, 0, 0] = np.nan
fi_nan[0, 2, 2] = np.nan
fi_nan[1, 2, 3] = np.nan

# msg input
fi_msg = fi_nan.copy()
fi_msg[np.isnan(fi_msg)] = -99

#  grids
lat = np.asarray([1, 3, 5, 7])
lon = np.asarray([2, 4, 6])
lat2d = np.asarray([1, 3, 5, 7, 1, 3, 5, 7, 1, 3, 5, 7]).reshape((3, 4))
lon2d = np.asarray([2, 2, 2, 2, 4, 4, 4, 4, 6, 6, 6, 6]).reshape((3, 4))

msg64 = fi_msg[0, 0, 0].astype(np.float64)
msg32 = fi_msg[0, 0, 0].astype(np.float32)

# Expected output
fo_nom_expected = np.asarray([
    1.870327, 1.353965, 1.931963, 1.872924, 0.8730035, -0.1676207, 2.946794,
    0.1410671, 1.917912, 1.98253, 1.877125, 1.735453, -1.82497, 1.177423,
    2.169137, 1.01385, 0.381366, 0.3293635, 1.053591, 2.015617, 0.6676366,
    1.754721, 0.4975608, 2.691788
]).reshape((2, 4, 3))

fo_nan_expected = np.asarray([
    2.439301, 1.353965, 1.931963, 1.872924, 0.8730035, -0.1676207, 2.946794,
    0.1410671, np.nan, 1.98253, 1.877125, 1.735453, -1.82497, 1.177423,
    2.169137, 1.01385, 0.381366, 0.3293635, 1.053591, 2.015617, 0.6676366,
    1.754721, 0.4975608, np.nan
]).reshape((2, 4, 3))

fo_msg_expected = np.asarray([
    2.439301, 1.353965, 1.931963, 1.872924, 0.8730035, -0.1676207, 2.946794,
    0.1410671, -99, 1.98253, 1.877125, 1.735453, -1.82497, 1.177423, 2.169137,
    1.01385, 0.381366, 0.3293635, 1.053591, 2.015617, 0.6676366, 1.754721,
    0.4975608, -99
]).reshape((2, 4, 3))


# run tests
class Test_rcm2rgrid(ut.TestCase):
    """
    Test_rcm2rgrid_float64
    This unit test covers the nominal, nan, and msg cases of 64 bit float input for rcm2rgrid
    """

    def test_rcm2rgrid_float64_nom(self):
        nt.assert_array_almost_equal(
            fo_nom_expected,
            geocat.f2py.rcm2rgrid(lat2d, lon2d, fi_nom.astype(np.float64), lat,
                                  lon))

    def test_rcm2rgrid_float64_nan(self):
        nt.assert_array_almost_equal(
            fo_nan_expected,
            geocat.f2py.rcm2rgrid(lat2d, lon2d, fi_nan.astype(np.float64), lat,
                                  lon))

    def test_rcm2rgrid_float64_msg(self):
        nt.assert_array_almost_equal(
            fo_msg_expected,
            geocat.f2py.rcm2rgrid(lat2d,
                                  lon2d,
                                  fi_msg.astype(np.float64),
                                  lat,
                                  lon,
                                  msg_py=msg64))

    def test_rcm2rgrid_float32_nom(self):
        nt.assert_array_almost_equal(
            fo_nom_expected,
            geocat.f2py.rcm2rgrid(lat2d, lon2d, fi_nom.astype(np.float32), lat,
                                  lon))

    def test_rcm2rgrid_float32_nan(self):
        nt.assert_array_almost_equal(
            fo_nan_expected,
            geocat.f2py.rcm2rgrid(lat2d, lon2d, fi_nan.astype(np.float32), lat,
                                  lon))

    def test_rcm2rgrid_float32_msg(self):
        nt.assert_array_almost_equal(
            fo_msg_expected,
            geocat.f2py.rcm2rgrid(lat2d,
                                  lon2d,
                                  fi_msg.astype(np.float32),
                                  lat,
                                  lon,
                                  msg_py=msg32))
