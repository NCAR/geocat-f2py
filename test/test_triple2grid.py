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
method=1


# Nominal input
data = np.asarray([2.740654945373535, 2.745847702026367, 4.893587112426758, 2.965059041976929, 1.707929134368896,
                   0.746006965637207, -0.7178658246994019, 2.754249572753906, 2.863926410675049, -1.335241436958313,
                   2.835823774337769, 2.470905065536499, -4.649940013885498, 1.027701020240784, 1.107181429862976,
                   2.509441375732422, 1.35484516620636, -0.2372681051492691, 3.031233072280884, -0.004878446459770203,
                   3.338273763656616, -0.3412730693817139, 0.3352730870246887, 4.383576393127441])\
                .reshape((dim0, dim1, m_x_i))


# Missing value = np.nan input
data_nan = data.copy()
data_nan[0, 0, 1] = np.nan
data_nan[1, 2, 3] = np.nan

# Missing value = -99 input
data_msg = data_nan.copy()
data_msg[np.isnan(data_msg)] = -99

# Input coordinates
x_in = np.asarray([1.0, 3.0, 5.0, 7.0])
y_in = np.asarray([2.0, 4.0, 6.0, 8.0])

# Output coordinates
x_out = np.asarray([1.5, 2.5, 3.5])
y_out = np.asarray([2.2, 7.8])


# Expected output
out_expected = np.asarray([2.740654945373535,   np.nan, np.nan, np.nan, np.nan, 2.745847702026367,
                           1.707929134368896,   np.nan, np.nan, np.nan, np.nan, 0.746006965637207,
                           2.863926410675049,   np.nan, np.nan, np.nan, np.nan, -1.335241436958313,
                           -4.649940013885498,  np.nan, np.nan, np.nan, np.nan, 1.027701020240784,
                           1.35484516620636,    np.nan, np.nan, np.nan, np.nan, -0.2372681051492691,
                           3.338273763656616,   np.nan, np.nan, np.nan, np.nan, -0.3412730693817139])\
                        .reshape((dim0, dim1, n_y_out, m_x_out))

out_expected_msg_nan = np.full((dim0, dim1, n_y_out, m_x_out), np.nan)

out_expected_msg_99 = np.full((dim0, dim1, n_y_out, m_x_out), -99)

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



def prepare_masked(fo_masked, fo):
    for i in range(fo.shape[0]):
        for j in range(fo.shape[1]):
            fo_masked[i, j] = np.diag(fo[i, j, ::2, ::2])


# Size of the grids
n = 12
m = 12

in_size_M = int(m / 2) + 1
x = np.zeros((in_size_M))
y = np.zeros((in_size_M))
for i in range(in_size_M):
    x[i] = float(i)
    y[i] = float(i)

xgrid_npoints_M = m + 1
ygrid_npoints_N = n + 1
xgrid = np.zeros((xgrid_npoints_M))
ygrid = np.zeros((ygrid_npoints_N))
for i in range(xgrid_npoints_M):
    xgrid[i] = float(i) * 0.5
for i in range(ygrid_npoints_N):
    ygrid[i] = float(i) * 0.5

#create and fill input data array (fi)
fi = np.random.randn(3, in_size_M, in_size_M)
fo_masked = np.zeros((3, in_size_M, in_size_M))
fi_asfloat32 = fi.astype(np.float32)


# TODO: These unit tests are way less than a minimum required number for a reasonable
# TODO: coverage and will need to be revisited before or after geocat.ncomp deprecation.
class Test_triple_to_grid_float64(ut.TestCase):

    def test_triple_to_grid_float64(self):
        out = geocat.f2py.triple_to_grid(data, x_in, y_in, x_out, y_out)
        np.testing.assert_array_equal(out_expected, out.values)

    def test_triple_to_grid_float64_distmx(self):
        out = geocat.f2py.triple_to_grid(data, x_in, y_in, x_out, y_out, method=method, distmx=distmx)
        np.testing.assert_array_equal(out_expected_distmx, out.values)

    def test_triple_to_grid_float64_nan(self):
        out = geocat.f2py.triple_to_grid(data_nan, x_in, y_in, x_out, y_out, msg=np.nan)
        np.testing.assert_array_equal(out_expected_msg_nan, out.values)

    def test_triple_to_grid_float64_msg(self):
        out = geocat.f2py.triple_to_grid(data_msg, x_in, y_in, x_out, y_out, msg=-99)
        np.testing.assert_array_equal(out_expected_msg_99, out.values)

    def test_triple_to_grid_float64_distmx_nan(self):
        out = geocat.f2py.triple_to_grid(data_nan, x_in, y_in, x_out, y_out, msg=np.nan, method=method, distmx=distmx)
        np.testing.assert_array_equal(out_expected_distmx_msg_nan, out.values)

    def test_triple_to_grid_float64_distmx_msg(self):
        out = geocat.f2py.triple_to_grid(data_msg, x_in, y_in, x_out, y_out, msg=-99, method=method, distmx=distmx)
        np.testing.assert_array_equal(out_expected_distmx_msg_99, out.values)


class Test_triple_to_grid_float32(ut.TestCase):

    def test_triple_to_grid_float64(self):
        out = geocat.f2py.triple_to_grid(data.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32))
        np.testing.assert_array_equal(out_expected.astype(np.float32), out.values)

    def test_triple_to_grid_float64_distmx(self):
        out = geocat.f2py.triple_to_grid(data.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32),
                                         method=method,
                                         distmx=distmx)
        np.testing.assert_array_equal(out_expected_distmx.astype(np.float32), out.values)

    def test_triple_to_grid_float64_nan(self):
        out = geocat.f2py.triple_to_grid(data_nan.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32),
                                         msg=np.nan)
        np.testing.assert_array_equal(out_expected_msg_nan.astype(np.float32), out.values)

    def test_triple_to_grid_float64_msg(self):
        out = geocat.f2py.triple_to_grid(data_msg.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32),
                                         msg=-99)
        np.testing.assert_array_equal(out_expected_msg_99, out.values)

    def test_triple_to_grid_float64_distmx_nan(self):
        out = geocat.f2py.triple_to_grid(data_nan.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32),
                                         msg=np.nan,
                                         method=method,
                                         distmx=distmx)
        np.testing.assert_array_equal(out_expected_distmx_msg_nan.astype(np.float32), out.values)

    def test_triple_to_grid_float64_distmx_msg(self):
        out = geocat.f2py.triple_to_grid(data_msg.astype(np.float32),
                                         x_in.astype(np.float32),
                                         y_in.astype(np.float32),
                                         x_out.astype(np.float32),
                                         y_out.astype(np.float32),
                                         msg=-99,
                                         method=method,
                                         distmx=distmx)
        np.testing.assert_array_equal(out_expected_distmx_msg_99.astype(np.float32), out.values)

    def test_triple2grid_float32(self):
        fo = geocat.f2py.triple_to_grid(fi_asfloat32,
                                        x.astype(np.float32),
                                        y.astype(np.float32),
                                        xgrid.astype(np.float32),
                                        ygrid.astype(np.float32))
        prepare_masked(fo_masked, fo.values)
        np.testing.assert_array_equal(fi_asfloat32, fo_masked)
