import sys
import time
import unittest as ut

import numpy as np
import numpy.testing as nt
import xarray as xr

# Import from directory structure if coverage test, or from installed
# packages otherwise
if "--cov" in str(sys.argv):
    from src.geocat.f2py import rgrid2rcm
else:
    from geocat.f2py import rgrid2rcm

# nominal input
fi_nom = np.asarray([
    1.870327, 1.872924, 2.946794, 1.98253, 1.353965, 0.8730035, 0.1410671,
    1.877125, 1.931963, -0.1676207, 1.917912, 1.735453, -1.82497, 1.01385,
    1.053591, 1.754721, 1.177423, 0.381366, 2.015617, 0.4975608, 2.169137,
    0.3293635, 0.6676366, 2.691788
]).reshape((2, 4, 3))

# nan input
fi_nan = fi_nom.copy()
fi_nan[0, 0, 0] = np.nan
fi_nan[0, 2, 2] = np.nan

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
    1.870327, 1.98253, 0.1410671, -0.1676207, 1.872924, 1.353965, 1.877125,
    1.917912, 2.946794, 0.8730035, 1.931963, 1.735453, -1.82497, 1.754721,
    2.015617, 0.3293635, 1.01385, 1.177423, 0.4975608, 0.6676366, 1.053591,
    0.381366, 2.169137, 2.691788
]).reshape((2, 3, 4))

fo_nan_expected = np.asarray([
    1.812921, 1.98253, 0.1410671, -0.1676207, 1.872924, 1.353965, 1.877125,
    1.917912, 2.946794, 0.8730035, np.nan, 1.735453, -1.82497, 1.754721,
    2.015617, 0.3293635, 1.01385, 1.177423, 0.4975608, 0.6676366, 1.053591,
    0.381366, 2.169137, 2.691788
]).reshape((2, 3, 4))

fo_msg_expected = np.asarray([
    1.812921, 1.98253, 0.1410671, -0.1676207, 1.872924, 1.353965, 1.877125,
    1.917912, 2.946794, 0.8730035, -99, 1.735453, -1.82497, 1.754721, 2.015617,
    0.3293635, 1.01385, 1.177423, 0.4975608, 0.6676366, 1.053591, 0.381366,
    2.169137, 2.691788
]).reshape((2, 3, 4))


# run tests
class Test_rgrid2rcm(ut.TestCase):
    """Test_rgrid2rcm_float64 This unit test covers the nominal, nan, and msg
    cases of 64 bit float input for rgrid2rcm."""

    def test_rgrid2rcm_float64_nom(self):
        nt.assert_array_almost_equal(
            fo_nom_expected,
            rgrid2rcm(lat, lon, fi_nom.astype(np.float64), lat2d, lon2d))

    def test_rgrid2rcm_float64_nan(self):
        nt.assert_array_almost_equal(
            fo_nan_expected,
            rgrid2rcm(lat, lon, fi_nan.astype(np.float64), lat2d, lon2d))

    def test_rgrid2rcm_float64_msg(self):
        nt.assert_array_almost_equal(
            fo_msg_expected,
            rgrid2rcm(lat,
                      lon,
                      fi_msg.astype(np.float64),
                      lat2d,
                      lon2d,
                      msg=msg64))

    def test_rgrid2rcm_float32_nom(self):
        nt.assert_array_almost_equal(
            fo_nom_expected,
            rgrid2rcm(lat, lon, fi_nom.astype(np.float32), lat2d, lon2d))

    def test_rgrid2rcm_float32_nan(self):
        nt.assert_array_almost_equal(
            fo_nan_expected,
            rgrid2rcm(lat, lon, fi_nan.astype(np.float32), lat2d, lon2d))

    def test_rgrid2rcm_float32_msg(self):
        nt.assert_array_almost_equal(
            fo_msg_expected,
            rgrid2rcm(lat,
                      lon,
                      fi_msg.astype(np.float32),
                      lat2d,
                      lon2d,
                      msg=msg32))
