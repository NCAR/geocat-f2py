import numpy as np
import xarray as xr
import geocat.f2py

import sys
import time
import unittest as ut


# Size of the grids
ny = 2
mx = 3

# Nominal input
data = np.asarray([2.740655, 2.745848, 4.893587, 2.965059, 1.707929, 0.746007]).reshape((ny, mx))

# Missing value = np.nan input
data_nan = data.copy()
data_nan[0, 1] = np.nan
data_nan[1, 2] = np.nan

# Missing value = -99 input
data_msg = data_nan.copy()
data_msg[np.isnan(data_msg)] = -99

# Coordinates
x = np.asarray([1.0, 3.0, 5.0])
y = np.asarray([2.0, 4.0])

# Expected output
out_expected = np.asarray([1, 3, 5, 1, 3, 5, 2, 2, 2, 4, 4, 4, 2.740655, 2.745848, 4.893587, 2.965059, 1.707929, 0.746007])\
                .reshape((3, ny * mx))
out_expected_msg = np.asarray([1, 5, 1, 3, 2, 2, 4, 4, 2.740655, 4.893587, 2.965059, 1.707929])\
                    .reshape((3, 4))

# TODO: These unit tests are way less than a minimum required number for a reasonable
# TODO: coverage and will need to be revisited before or after geocat.ncomp deprecation.
class Test_grid_to_triple_float64(ut.TestCase):

    def test_grid_to_triple_float64(self):
        out = geocat.f2py.grid_to_triple(data, x, y)
        np.testing.assert_array_equal(out_expected, out.values)

    def test_grid_to_triple_float64_nan(self):
        out = geocat.f2py.grid_to_triple(data_nan, x, y)
        np.testing.assert_array_equal(out_expected_msg, out.values)

    def test_grid_to_triple_float64_nan_2(self):
        out = geocat.f2py.grid_to_triple(data_nan, x, y, msg_py=np.nan)
        np.testing.assert_array_equal(out_expected_msg, out.values)

    def test_grid_to_triple_float64_msg(self):
        out = geocat.f2py.grid_to_triple(data_msg, x, y, msg_py=-99)
        np.testing.assert_array_equal(out_expected_msg, out.values)

class Test_grid_to_triple_float32(ut.TestCase):

    def test_grid_to_triple_float32(self):
        data_asfloat32 = data.astype(np.float32)
        out = geocat.f2py.grid_to_triple(data_asfloat32,
                                     x.astype(np.float32),
                                     y.astype(np.float32))
        np.testing.assert_array_equal(out_expected.astype(np.float32), out)

    def test_grid_to_triple_float32_nan(self):
        data_asfloat32_nan = data_nan.astype(np.float32)
        out = geocat.f2py.grid_to_triple(data_asfloat32_nan,
                                     x.astype(np.float32),
                                     y.astype(np.float32))
        np.testing.assert_array_equal(out_expected_msg.astype(np.float32), out)

    def test_grid_to_triple_float32_nan_2(self):
        data_asfloat32_nan = data_nan.astype(np.float32)
        out = geocat.f2py.grid_to_triple(data_asfloat32_nan,
                                     x.astype(np.float32),
                                     y.astype(np.float32),
                                     msg_py=np.nan)
        np.testing.assert_array_equal(out_expected_msg.astype(np.float32), out)

    def test_grid_to_triple_float32_msg(self):
        data_asfloat32_msg = data_msg.astype(np.float32)
        out = geocat.f2py.grid_to_triple(data_asfloat32_msg,
                                     x.astype(np.float32),
                                     y.astype(np.float32),
                                     msg_py=-99)
        np.testing.assert_array_equal(out_expected_msg.astype(np.float32), out)

# a = Test_grid_to_triple_float32()
# a.test_grid_to_triple_float32_msg()