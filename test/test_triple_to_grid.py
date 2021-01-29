import numpy as np
import xarray as xr
import geocat.f2py

import unittest as ut

# Dimensions of the input data and its coordinates
dim0 = 2
dim1 = 3
m_x_i = 4

# Dimensions of the output data coordinates
n_y_out = 2
m_x_out = 3

# Options for function call
# For default inputs and unit tests, optiona are not set
# To explicitly test options, msg_py and distmx will be set
msg_nan = np.nan
msg_99 = -99
distmx = 275
method_0 = 0


# Nominal input
data = np.asarray([2.740654945373535, 2.745847702026367, 4.893587112426758, 2.965059041976929, 1.707929134368896,
                   0.746006965637207, -0.7178658246994019, 2.754249572753906, 2.863926410675049, -1.335241436958313,
                   2.835823774337769, 2.470905065536499, -4.649940013885498, 1.027701020240784, 1.107181429862976,
                   2.509441375732422, 1.35484516620636, -0.2372681051492691, 3.031233072280884, -0.004878446459770203,
                   3.338273763656616, -0.3412730693817139, 0.3352730870246887, 4.383576393127441])\
                .reshape((dim0, dim1, m_x_i))


# Missing value = np.nan input
data_msg_nan = data.copy()
data_msg_nan[0, 0, 1] = np.nan
data_msg_nan[1, 2, 3] = np.nan

# Missing value = -99 input
data_msg_99 = data_msg_nan.copy()
data_msg_99[np.isnan(data_msg_99)] = -99

# Input coordinates
x_in = np.asarray([1.0, 3.0, 5.0, 7.0])
y_in = np.asarray([2.0, 4.0, 6.0, 8.0])

# Output coordinates
x_out = np.asarray([1.5, 2.5, 3.5])
y_out = np.asarray([2.2, 7.8])


# Expected output for default optional arguments
out_expected = np.asarray([2.740654945373535,   np.nan, np.nan, np.nan, np.nan, 2.745847702026367,
                           1.707929134368896,   np.nan, np.nan, np.nan, np.nan, 0.746006965637207,
                           2.863926410675049,   np.nan, np.nan, np.nan, np.nan, -1.335241436958313,
                           -4.649940013885498,  np.nan, np.nan, np.nan, np.nan, 1.027701020240784,
                           1.35484516620636,    np.nan, np.nan, np.nan, np.nan, -0.2372681051492691,
                           3.338273763656616,   np.nan, np.nan, np.nan, np.nan, -0.3412730693817139])\
                        .reshape((dim0, dim1, n_y_out, m_x_out))

out_expected_msg_nan = out_expected.copy()
out_expected_msg_nan[0,0,1,2] = np.nan

out_expected_msg_99 = out_expected_msg_nan.copy()
out_expected_msg_99[np.isnan(out_expected_msg_99)] = -99

# Expected output for `method=0`
out_expected_method_0 = out_expected.copy()

out_expected_method_0_msg_nan = out_expected_msg_nan.copy()

out_expected_method_0_msg_99 = out_expected_msg_99.copy()


# Expected output for `distmx=275`
out_expected_distmx = np.asarray([2.740654945373535,    np.nan, np.nan, np.nan, np.nan, np.nan,
                                  1.707929134368896,    np.nan, np.nan, np.nan, np.nan, np.nan,
                                  2.863926410675049,    np.nan, np.nan, np.nan, np.nan, np.nan,
                                  -4.649940013885498,   np.nan, np.nan, np.nan, np.nan, np.nan,
                                  1.35484516620636,     np.nan, np.nan, np.nan, np.nan, np.nan,
                                  3.338273763656616,    np.nan, np.nan, np.nan, np.nan, np.nan])\
                            .reshape((dim0, dim1, n_y_out, m_x_out))

out_expected_distmx_msg_nan = out_expected_distmx.copy()

out_expected_distmx_msg_99 = out_expected_distmx_msg_nan.copy()
out_expected_distmx_msg_99[np.isnan(out_expected_distmx_msg_99)] = -99


# TODO: These unit tests are way less than a minimum required number for a reasonable
# TODO: coverage and will need to be revisited before or after geocat.ncomp deprecation.
class Test_triple_to_grid_float64(ut.TestCase):

    def test_triple_to_grid_float64(self):
        out = geocat.f2py.triple_to_grid(data,
                                         x_in,
                                         y_in,
                                         x_out,
                                         y_out)

        np.testing.assert_array_equal(out_expected, out.values)

    def test_triple_to_grid_float64_xr(self):
        out = geocat.f2py.triple_to_grid(xr.DataArray(data),
                                         xr.DataArray(x_in),
                                         xr.DataArray(y_in),
                                         xr.DataArray(x_out),
                                         xr.DataArray(y_out)
                                         )

        np.testing.assert_array_equal(out_expected, out.values)

    def test_triple_to_grid_float64_method_0(self):

        out = geocat.f2py.triple_to_grid(data,
                                         x_in,
                                         y_in,
                                         x_out,
                                         y_out,
                                         method=method_0)

        np.testing.assert_array_equal(out_expected_method_0, out.values)

    def test_triple_to_grid_float64_distmx(self):
        out = geocat.f2py.triple_to_grid(data,
                                         x_in,
                                         y_in,
                                         x_out,
                                         y_out,
                                         distmx=distmx)

        np.testing.assert_array_equal(out_expected_distmx, out.values)

    def test_triple_to_grid_float64_msg_nan(self):
        out = geocat.f2py.triple_to_grid(data_msg_nan,
                                         x_in,
                                         y_in,
                                         x_out,
                                         y_out,
                                         msg=np.nan)

        np.testing.assert_array_equal(out_expected_msg_nan, out.values)

    def test_triple_to_grid_float64_msg_99(self):
        out = geocat.f2py.triple_to_grid(data_msg_99,
                                         x_in,
                                         y_in,
                                         x_out,
                                         y_out,
                                         msg=-99)

        np.testing.assert_array_equal(out_expected_msg_99, out.values)

    def test_triple_to_grid_float64_distmx_msg_nan(self):
        out = geocat.f2py.triple_to_grid(data_msg_nan,
                                         x_in,
                                         y_in,
                                         x_out,
                                         y_out,
                                         msg=np.nan,
                                         distmx=distmx)

        np.testing.assert_array_equal(out_expected_distmx_msg_nan, out.values)

    def test_triple_to_grid_float64_distmx_msg_99(self):
        out = geocat.f2py.triple_to_grid(data_msg_99,
                                         x_in,
                                         y_in,
                                         x_out,
                                         y_out,
                                         msg=-99,
                                         distmx=distmx)

        np.testing.assert_array_equal(out_expected_distmx_msg_99, out.values)


class Test_triple_to_grid_float32(ut.TestCase):

    def test_triple_to_grid_float32(self):
        out = geocat.f2py.triple_to_grid(data.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32))
        np.testing.assert_array_equal(out_expected.astype(np.float32), out.values)

    def test_triple_to_grid_float32_method_0(self):
        out = geocat.f2py.triple_to_grid(data.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32),
                                         method=method_0)
        np.testing.assert_array_equal(out_expected_method_0.astype(np.float32), out.values)

    def test_triple_to_grid_float32_distmx(self):
        out = geocat.f2py.triple_to_grid(data.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32),
                                         distmx=distmx)
        np.testing.assert_array_equal(out_expected_distmx.astype(np.float32), out.values)

    def test_triple_to_grid_float32_msg_nan(self):
        out = geocat.f2py.triple_to_grid(data_msg_nan.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32),
                                         msg=np.nan)
        np.testing.assert_array_equal(out_expected_msg_nan.astype(np.float32), out.values)

    def test_triple_to_grid_float32_msg_99(self):
        out = geocat.f2py.triple_to_grid(data_msg_99.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32),
                                         msg=-99)
        np.testing.assert_array_almost_equal(out_expected_msg_99, out.values)

    def test_triple_to_grid_float32_distmx_msg_nan(self):
        out = geocat.f2py.triple_to_grid(data_msg_nan.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32),
                                         msg=np.nan,
                                         distmx=distmx)
        np.testing.assert_array_equal(out_expected_distmx_msg_nan.astype(np.float32), out.values.astype(np.float32))

    def test_triple_to_grid_float32_distmx_msg_99(self):
        out = geocat.f2py.triple_to_grid(data_msg_99.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32),
                                         msg=-99,
                                         distmx=distmx)
        np.testing.assert_array_equal(out_expected_distmx_msg_99.astype(np.float32), out.values)

a=Test_triple_to_grid_float64()
a.test_triple_to_grid_float64()
a.test_triple_to_grid_float64_xr()
