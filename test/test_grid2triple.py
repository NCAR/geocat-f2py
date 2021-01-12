import numpy as np
import xarray as xr
import geocat.f2py

import sys
import time
import unittest as ut


def prepare_masked(fo_masked, fo):
    for i in range(fo.shape[0]):
        for j in range(fo.shape[1]):
            fo_masked[i, j] = np.diag(fo[i, j, ::2, ::2])


# Size of the grids
ny = 3
mx = 3

x = np.zeros((mx))
y = np.zeros((ny))
for i in range(mx):
    x[i] = float(i) * 0.5
for i in range(ny):
    y[i] = float(i) * 2.5
z = np.random.randn(ny, mx)


# TODO: These unit tests are way less than a minimum required number for a reasonable
# TODO: coverage and will need to be revisited before or after geocat.ncomp deprecation.
class Test_grid_to_triple_float64(ut.TestCase):

    def test_grid_to_triple_float64(self):
        fo = geocat.f2py.grid_to_triple(z, x, y)
        np.testing.assert_array_equal(z.flatten(), fo[-1, :].values)


class Test_grid_to_triple_float32(ut.TestCase):

    def test_grid_to_triple_float32(self):
        z_asfloat32 = z.astype(np.float32)
        fo = geocat.f2py.grid_to_triple(z_asfloat32,
                                     x.astype(np.float32),
                                     y.astype(np.float32))
        np.testing.assert_array_equal(z_asfloat32.flatten(), fo[-1, :].values)