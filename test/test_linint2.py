import sys
import time
import unittest as ut

import numpy as np
import xarray as xr

# Import from directory structure if coverage test, or from installed
# packages otherwise
if "--cov" in str(sys.argv):
    from src.geocat.f2py import ChunkError, CoordinateError, linint2
else:
    from geocat.f2py import ChunkError, CoordinateError, linint2

n = 127

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


# TODO: All of these tests should be revisited since they indeed are not
#  checking any actually interpolated values.
class Test_linint2_float64(ut.TestCase):

    def test_linint2(self):
        fi = xr.DataArray(fi_np,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo)
        np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)

    def test_linint2_msg(self):
        fi = xr.DataArray(fi_np,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo, msg_py=fi_np[0, 0, 0, 0])
        np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)

    def test_linint2_nan(self):
        fi_np_copy = fi_np.copy()
        fi_np_copy[:, :, 0, 0] = np.nan
        fi = xr.DataArray(fi_np_copy,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo)
        np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)

    def test_linint2_masked(self):
        fi_mask = np.zeros(fi_np.shape, dtype=bool)
        fi_mask[:, :, 0, 0] = True
        fi_ma = np.ma.MaskedArray(fi_np, mask=fi_mask)
        fi = xr.DataArray(fi_ma,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo)
        np.testing.assert_array_equal(fi, fo[..., ::2, ::2].values)


class Test_linint2_float32(ut.TestCase):

    def test_linint2_float32(self):
        fi = xr.DataArray(fi_np.astype(np.float32),
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo)
        np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)

    def test_linint2_msg_float32(self):
        fi_np_copy = fi_np.astype(np.float32)
        fi = xr.DataArray(fi_np,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo, msg_py=fi_np_copy[0, 0, 0, 0])
        np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)

    def test_linint2_nan_float32(self):
        fi_np_copy = fi_np.astype(np.float32)
        fi_np_copy[:, :, 0, 0] = np.nan
        fi = xr.DataArray(fi_np_copy,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo)
        np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)

    def test_linint2_masked_float32(self):
        fi_mask = np.zeros(fi_np.shape, dtype=bool)
        fi_mask[:, :, 0, 0] = True
        fi_ma = np.ma.MaskedArray((fi_np * 100).astype(np.float32),
                                  mask=fi_mask)
        fi = xr.DataArray(fi_ma,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo)
        np.testing.assert_array_equal(fi, fo[..., ::2, ::2].values)


class Test_linint2_int32(ut.TestCase):

    def test_linint2_int32(self):
        fi = xr.DataArray((fi_np * 100).astype(np.int32),
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo)
        np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)

    def test_linint2_msg_int32(self):
        fi_np_copy = fi_np.astype(np.int32)
        fi = xr.DataArray(fi_np,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo, msg_py=fi_np_copy[0, 0, 0, 0])
        np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)

    def test_linint2_masked_int32(self):
        fi_mask = np.zeros(fi_np.shape, dtype=bool)
        fi_mask[:, :, 0, 0] = True
        fi_ma = np.ma.MaskedArray((fi_np * 100).astype(np.int32), mask=fi_mask)
        fi = xr.DataArray(fi_ma,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo)
        np.testing.assert_array_equal(fi, fo[..., ::2, ::2].values)


class Test_linint2_int64(ut.TestCase):

    def test_linint2_int64(self):
        fi = xr.DataArray((fi_np * 100).astype(np.int64),
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo)
        np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)
        print("Good after assertion")

    def test_linint2_msg_int64(self):
        fi_np_copy = (fi_np * 100).astype(np.int64)
        fi = xr.DataArray(fi_np,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo, msg_py=fi_np_copy[0, 0, 0, 0])
        np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)

    def test_linint2_masked_int64(self):
        fi_mask = np.zeros(fi_np.shape, dtype=bool)
        fi_mask[:, :, 0, 0] = True
        fi_ma = np.ma.MaskedArray((fi_np * 100).astype(np.int64), mask=fi_mask)
        fi = xr.DataArray(fi_ma,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo)
        np.testing.assert_array_equal(fi, fo[..., ::2, ::2].values)


class Test_linint2_dask(ut.TestCase):

    def test_linint2_chunked_leftmost(self):
        # use 1 for time and level chunk sizes
        chunks = {
            'time': 1,
            'level': 1,
            'lat': fi_np.shape[2],
            'lon': fi_np.shape[3]
        }
        fi = xr.DataArray(fi_np,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi, xo, yo)
        np.testing.assert_array_equal(fi.values, fo[..., ::2, ::2].values)

    def test_linint2_chunked_interp(self):
        # use 1 for interpolated dimension chunk sizes -- this should throw a ChunkError
        chunks = {'time': 1, 'level': 1, 'lat': 1, 'lon': 1}
        fi = xr.DataArray(fi_np,
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi,
                              'lon': xi
                          }).chunk(chunks)
        with self.assertRaises(ChunkError):
            fo = linint2(fi, xo, yo)


class Test_linint2_numpy(ut.TestCase):

    def test_linint2_fi_np(self):
        fo = linint2(fi_np, xo, yo, xi=xi, yi=yi)
        np.testing.assert_array_equal(fi_np, fo[..., ::2, ::2])

    def test_linint2_fi_np_no_xi_yi(self):
        with self.assertRaises(CoordinateError):
            fo = linint2(fi_np, xo, yo, 0)

    def test_linint2_fi_np_no_yi(self):
        with self.assertRaises(CoordinateError):
            fo = linint2(fi_np, xo, yo, xi=xi)

    def test_linint2_fi_np_no_xi(self):
        with self.assertRaises(CoordinateError):
            fo = linint2(fi_np, xo, yo, yi=yi)


# class Test_linint2_non_monotonic(ut.TestCase):
#
#     def test_linint2_non_monotonic_xr(self):
#         fi = xr.DataArray(fi_np[:, :, ::-1, :],
#                           dims=['time', 'level', 'lat', 'lon'],
#                           coords={
#                               'lat': yi_reverse,
#                               'lon': xi
#                           }).chunk(chunks)
#         with self.assertWarns(_ncomp.NcompWarning):
#             linint2(fi, xo, yo).compute()
#
#     def test_linint2_non_monotonic_np(self):
#         with self.assertWarns(geocat.ncomp._ncomp.NcompWarning):
#             linint2(fi_np[:, :, ::-1, :],
#                                  xo,
#                                  yo,
#                                  xi=xi,
#                                  yi=yi_reverse)


class Test_linint2_non_contiguous(ut.TestCase):

    def test_linint2_non_contiguous_xr(self):
        fi = xr.DataArray(fi_np[:, :, ::-1, :],
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi_reverse,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi[:, :, ::-1, :], xo, yo)
        np.testing.assert_array_equal(fi[:, :, ::-1, :].values,
                                      fo[..., ::2, ::2].values)

    def test_linint2_non_contiguous_np(self):
        fi = xr.DataArray(fi_np[:, :, ::-1, :],
                          dims=['time', 'level', 'lat', 'lon'],
                          coords={
                              'lat': yi_reverse,
                              'lon': xi
                          }).chunk(chunks)
        fo = linint2(fi[:, :, ::-1, :].values,
                     xo,
                     yo,
                     xi=xi,
                     yi=yi_reverse[::-1])
        np.testing.assert_array_equal(fi[:, :, ::-1, :], fo[..., ::2, ::2])
