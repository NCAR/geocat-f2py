from abc import ABCMeta
from unittest import TestCase
import numpy as np
# from dask.array.tests.test_xarray import xr
import xarray as xr

from geocat.f2py import eofunc


class BaseEOFuncTestClass(metaclass=ABCMeta):
    _sample_data_eofunc = []

    # _sample_data[ 0 ]
    _sample_data_eofunc.append([[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11],
                                 [12, 13, 14, 15]],
                                [[16, 17, 18, 19], [20, 21, 22, 23],
                                 [24, 25, 26, 27], [28, 29, 30, 31]],
                                [[32, 33, 34, 35], [36, 37, 38, 39],
                                 [40, 41, 42, 43], [44, 45, 46, 47]],
                                [[48, 49, 50, 51], [52, 53, 54, 55],
                                 [56, 57, 58, 59], [60, 61, 62, 63]]])

    # _sample_data[ 1 ]
    _sample_data_eofunc.append(np.arange(64, dtype='double').reshape((4, 4, 4)))

    # _sample_data[ 2 ]
    tmp_data = np.asarray([
        0, 1, -99, -99, 4, -99, 6, -99, 8, 9, 10, -99, 12, -99, 14, 15, 16, -99,
        18, -99, 20, 21, 22, -99, 24, 25, 26, 27, 28, -99, 30, -99, 32, 33, 34,
        35, 36, -99, 38, 39, 40, -99, 42, -99, 44, 45, 46, -99, 48, 49, 50, 51,
        52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63
    ],
                          dtype='double').reshape((4, 4, 4))
    _sample_data_eofunc.append(tmp_data)

    # _sample_data[ 3 ]
    tmp_data = np.asarray([
        0, 1, -99, -99, 4, -99, 6, -99, 8, 9, 10, -99, 12, -99, 14, 15, 16, -99,
        18, -99, 20, 21, 22, -99, 24, 25, 26, 27, 28, -99, 30, -99, 32, 33, 34,
        35, 36, -99, 38, 39, 40, -99, 42, -99, 44, 45, 46, -99, 48, 49, 50, 51,
        52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63
    ],
                          dtype='double').reshape((4, 4, 4))
    tmp_data[tmp_data == -99] = np.nan
    _sample_data_eofunc.append(tmp_data)

    # _sample_data[ 4 ]
    _sample_data_eofunc.append(np.arange(64, dtype='int64').reshape((4, 4, 4)))

    # _nc_ds = xr.open_dataset("sst.nc")



class Test_eofunc(TestCase, BaseEOFuncTestClass):

    def test_eofunc_00(self):
        data = self._sample_data_eofunc[0]

        results = eofunc(data, 1)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), results.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(7, len(attrs))

        self.assertAlmostEqual(5.33333, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(26.66666, attrs['eval'][0], 4)
        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

    def test_eofunc_01(self):
        data = self._sample_data_eofunc[1]

        results = eofunc(data, 1)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(7, len(attrs))

        self.assertAlmostEqual(5.33333, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(26.66666, attrs['eval'][0], 4)
        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

    def test_eofunc_02(self):
        data = self._sample_data_eofunc[1]

        results = eofunc(data, 1, jopt="covariance")
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(7, len(attrs))

        self.assertAlmostEqual(5.33333, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(26.66666, attrs['eval'][0], 4)
        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

    def test_eofunc_03(self):
        data = self._sample_data_eofunc[1]

        results = eofunc(data, 1, jopt="correlation")
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(7, len(attrs))

        self.assertAlmostEqual(3.20000, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(16.00000, attrs['eval'][0], 4)

        self.assertEqual("correlation", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

    def test_eofunc_04(self):
        data = self._sample_data_eofunc[1]
        with self.assertRaises(ValueError):
            eofunc(data, 1, jopt="Not_supported")

    def test_eofunc_05(self):
        data = self._sample_data_eofunc[1]
        with self.assertRaises(ValueError):
            eofunc(data, 1, jopt=0)

    def test_eofunc_06(self):
        data = self._sample_data_eofunc[1]

        results = eofunc(data, 1, jopt="correlation", pcrit=32.0)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(3.20000, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(16.00000, attrs['eval'][0], 4)
        self.assertAlmostEqual(32.00, attrs["pcrit"], 4)

        self.assertEqual("correlation", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

    def test_eofunc_07(self):
        data = self._sample_data_eofunc[1]

        results = eofunc(data, 1, jopt="correlation", pcrit=32)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(3.20000, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(16.00000, attrs['eval'][0], 4)
        self.assertAlmostEqual(32.00, attrs["pcrit"], 4)

        self.assertEqual("correlation", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

    def test_eofunc_08(self):
        data = self._sample_data_eofunc[3]

        results = eofunc(data, 1, jopt="correlation", pcrit=32)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        expected_results = [
            0.0600, 0.1257, 0.1778, 0.2675, 0.1257, 0.1778, 0.3404, 0.1257,
            0.3404, 0.2675, 0.1257, 0.1778, 0.3404, 0.3404, 0.3404, 0.3404
        ]
        for e in zip(expected_results, eof.reshape((16, 1)).tolist()):
            self.assertAlmostEqual(e[0], e[1][0], 4)

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(2.9852, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(98.71625, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(14.9260, attrs['eval'][0], 4)

        self.assertEqual("correlation", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertTrue(np.isnan(data[0, 0, 3]))

    def test_eofunc_09(self):
        data = self._sample_data_eofunc[3]

        results = eofunc(data,
                         1,
                         jopt="correlation",
                         pcrit=32,
                         missing_value=np.nan)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        expected_results = [
            0.0600, 0.1257, 0.1778, 0.2675, 0.1257, 0.1778, 0.3404, 0.1257,
            0.3404, 0.2675, 0.1257, 0.1778, 0.3404, 0.3404, 0.3404, 0.3404
        ]
        for e in zip(expected_results, eof.reshape((16, 1)).tolist()):
            self.assertAlmostEqual(e[0], e[1][0], 4)

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(2.9852, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(98.71625, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(14.9260, attrs['eval'][0], 4)

        self.assertEqual("correlation", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertTrue(np.isnan(data[0, 0, 3]))

    def test_eofunc_10(self):
        data = self._sample_data_eofunc[3]

        with self.assertRaises(ValueError):
            eofunc(data, 1, jopt="correlation", pcrit=32, missing_value=42)

    def test_eofunc_11(self):
        data = self._sample_data_eofunc[2]

        results = eofunc(data,
                         1,
                         jopt="correlation",
                         pcrit=32,
                         missing_value=-99.0)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        expected_results = [
            0.0600, 0.1257, 0.1778, 0.2675, 0.1257, 0.1778, 0.3404, 0.1257,
            0.3404, 0.2675, 0.1257, 0.1778, 0.3404, 0.3404, 0.3404, 0.3404
        ]
        for e in zip(expected_results, eof.reshape((16, 1)).tolist()):
            self.assertAlmostEqual(e[0], e[1][0], 4)

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(2.9852, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(98.71625, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(14.9260, attrs['eval'][0], 4)

        self.assertEqual("correlation", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertAlmostEqual(-99.0, data[0, 0, 3], 1)

    def test_eofunc_12(self):
        data = self._sample_data_eofunc[2]

        results = eofunc(data,
                         1,
                         jopt="correlation",
                         pcrit=32,
                         missing_value=-99)  #None-double
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        expected_results = [
            0.0600, 0.1257, 0.1778, 0.2675, 0.1257, 0.1778, 0.3404, 0.1257,
            0.3404, 0.2675, 0.1257, 0.1778, 0.3404, 0.3404, 0.3404, 0.3404
        ]
        for e in zip(expected_results, eof.reshape((16, 1)).tolist()):
            self.assertAlmostEqual(e[0], e[1][0], 4)

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(2.9852, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(98.71625, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(14.9260, attrs['eval'][0], 4)

        self.assertEqual("correlation", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertAlmostEqual(-99.0, data[0, 0, 3], 1)

    def test_eofunc_13(self):
        data = self._sample_data_eofunc[2]

        results = eofunc(data,
                         1,
                         jopt="correlation",
                         pcrit=32,
                         missing_value=np.int8(-99))  # None-double np.number
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        expected_results = [
            0.0600, 0.1257, 0.1778, 0.2675, 0.1257, 0.1778, 0.3404, 0.1257,
            0.3404, 0.2675, 0.1257, 0.1778, 0.3404, 0.3404, 0.3404, 0.3404
        ]
        for e in zip(expected_results, eof.reshape((16, 1)).tolist()):
            self.assertAlmostEqual(e[0], e[1][0], 4)

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(2.9852, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(98.71625, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(14.9260, attrs['eval'][0], 4)

        self.assertEqual("correlation", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertAlmostEqual(-99.0, data[0, 0, 3], 1)

    def test_eofunc_14(self):
        data = self._sample_data_eofunc[4]

        results = eofunc(data, 1)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(7, len(attrs))

        self.assertAlmostEqual(5.33333, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(26.66666, attrs['eval'][0], 4)

        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

    def test_eofunc_15(self):
        data = xr.DataArray(self._sample_data_eofunc[0])
        data.attrs["prop1"] = "prop1"
        data.attrs["prop2"] = 2

        results = eofunc(data, 1)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), results.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(7, len(attrs))

        self.assertAlmostEqual(5.33333, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(26.66666, attrs['eval'][0], 4)
        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])
        self.assertFalse("prop1" in attrs)
        self.assertFalse("prop2" in attrs)

    def test_eofunc_16(self):
        data = xr.DataArray(self._sample_data_eofunc[0])
        data.attrs["prop1"] = "prop1"
        data.attrs["prop2"] = 2

        results = eofunc(data, 1, meta=True)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), results.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(9, len(attrs))

        self.assertAlmostEqual(5.33333, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(26.66666, attrs['eval'][0], 4)
        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])
        self.assertTrue("prop1" in attrs)
        self.assertTrue("prop2" in attrs)
        self.assertEqual("prop1", attrs["prop1"])
        self.assertEqual(2, attrs["prop2"])

    def test_eofunc_n_01(self):
        data = self._sample_data_eofunc[1]

        results = eofunc(data, 1, time_dim=1)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(7, len(attrs))

        self.assertAlmostEqual(85.33333, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(426.66666, attrs['eval'][0], 4)

        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

    def test_eofunc_n_02(self):
        data = self._sample_data_eofunc[1]

        results = eofunc(data, 1, time_dim=1, jopt="correlation")
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(7, len(attrs))

        self.assertAlmostEqual(3.2000, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(16.0000, attrs['eval'][0], 4)

        self.assertEqual("correlation", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

    def test_eofunc_n_03(self):
        data = self._sample_data_eofunc[1]

        results = eofunc(data, 1, time_dim=0, jopt="covariance", pcrit=32)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(1365.3333, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(6826.6667, attrs['eval'][0], 4)
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

    def test_eofunc_n_03_1(self):
        data = self._sample_data_eofunc[1]

        results = eofunc(data, 1, time_dim=0, jopt="covariance", pcrit=32)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        for e in np.nditer(eof):
            self.assertAlmostEqual(0.25, e, 2)

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(1365.3333, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(100.0, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(6826.6667, attrs['eval'][0], 4)
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

    def test_eofunc_n_04(self):
        data = self._sample_data_eofunc[3]

        results = eofunc(data, 1, time_dim=1, jopt="covariance", pcrit=32)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        expected_results = [
            0.3139, 0.1243, 0.1274, -99.0, 0.3139, 0.0318, 0.3139, -99.0,
            0.3139, 0.2821, 0.3139, 0.0303, 0.3139, 0.3139, 0.3139, 0.3139
        ]
        for e in zip(expected_results, eof.reshape((16, 1)).tolist()):
            if (e[0] != -99):
                self.assertAlmostEqual(e[0], e[1][0], 4)
            else:
                self.assertTrue(np.isnan(e[1]))

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(84.75415, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(102.4951, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(339.0166, attrs['eval'][0], 4)
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

        self.assertTrue(np.isnan(data[0, 0, 3]))

    def test_eofunc_n_05(self):
        data = self._sample_data_eofunc[3]

        results = eofunc(data,
                         1,
                         time_dim=1,
                         jopt="covariance",
                         pcrit=32,
                         missing_value=np.nan)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        expected_results = [
            0.3139, 0.1243, 0.1274, -99.0, 0.3139, 0.0318, 0.3139, -99.0,
            0.3139, 0.2821, 0.3139, 0.0303, 0.3139, 0.3139, 0.3139, 0.3139
        ]
        for e in zip(expected_results, eof.reshape((16, 1)).tolist()):
            if (e[0] != -99):
                self.assertAlmostEqual(e[0], e[1][0], 4)
            else:
                self.assertTrue(np.isnan(e[1]))

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(84.75415, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(102.4951, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(339.0166, attrs['eval'][0], 4)
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

        self.assertTrue(np.isnan(data[0, 0, 3]))

    def test_eofunc_n_06(self):
        data = self._sample_data_eofunc[3]

        with self.assertRaises(ValueError):
            eofunc(data, 1, time_dim=1, missing_value=42)

    def test_eofunc_n_07(self):
        data = self._sample_data_eofunc[2]

        results = eofunc(data,
                         1,
                         time_dim=1,
                         jopt="covariance",
                         pcrit=32,
                         missing_value=np.float64(-99.0))
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        expected_results = [
            0.3139, 0.1243, 0.1274, -99.0, 0.3139, 0.0318, 0.3139, -99.0,
            0.3139, 0.2821, 0.3139, 0.0303, 0.3139, 0.3139, 0.3139, 0.3139
        ]
        for e in zip(expected_results, eof.reshape((16, 1)).tolist()):
            if (e[0] != -99):
                self.assertAlmostEqual(e[0], e[1][0], 4)
            else:
                self.assertTrue(np.isnan(e[1]))

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(84.75415, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(102.4951, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(339.0166, attrs['eval'][0], 4)
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

        self.assertEqual(-99, data[0, 0, 3])

    def test_eofunc_n_08(self):
        data = self._sample_data_eofunc[2]

        results = eofunc(data,
                         1,
                         time_dim=1,
                         jopt="covariance",
                         pcrit=32,
                         missing_value=-99)
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        expected_results = [
            0.3139, 0.1243, 0.1274, -99.0, 0.3139, 0.0318, 0.3139, -99.0,
            0.3139, 0.2821, 0.3139, 0.0303, 0.3139, 0.3139, 0.3139, 0.3139
        ]
        for e in zip(expected_results, eof.reshape((16, 1)).tolist()):
            if (e[0] != -99):
                self.assertAlmostEqual(e[0], e[1][0], 4)
            else:
                self.assertTrue(np.isnan(e[1]))

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(84.75415, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(102.4951, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(339.0166, attrs['eval'][0], 4)
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

        self.assertEqual(-99, data[0, 0, 3])

    def test_eofunc_n_09(self):
        data = self._sample_data_eofunc[2]

        results = eofunc(data,
                         1,
                         time_dim=1,
                         jopt="covariance",
                         pcrit=32,
                         missing_value=np.int8(-99))
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        expected_results = [
            0.3139, 0.1243, 0.1274, -99.0, 0.3139, 0.0318, 0.3139, -99.0,
            0.3139, 0.2821, 0.3139, 0.0303, 0.3139, 0.3139, 0.3139, 0.3139
        ]
        for e in zip(expected_results, eof.reshape((16, 1)).tolist()):
            if (e[0] != -99):
                self.assertAlmostEqual(e[0], e[1][0], 4)
            else:
                self.assertTrue(np.isnan(e[1]))

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(84.75415, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(102.4951, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(339.0166, attrs['eval'][0], 4)
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

        self.assertEqual(-99, data[0, 0, 3])

    def test_eofunc_n_10(self):
        data = self._sample_data_eofunc[2]

        results = eofunc(data,
                         1,
                         time_dim=1,
                         jopt="covariance",
                         pcrit=32,
                         missing_value=np.int8(-99))
        eof = results.data
        attrs = results.attrs

        self.assertEqual((1, 4, 4), eof.shape)

        expected_results = [
            0.3139, 0.1243, 0.1274, -99.0, 0.3139, 0.0318, 0.3139, -99.0,
            0.3139, 0.2821, 0.3139, 0.0303, 0.3139, 0.3139, 0.3139, 0.3139
        ]
        for e in zip(expected_results, eof.reshape((16, 1)).tolist()):
            if (e[0] != -99):
                self.assertAlmostEqual(e[0], e[1][0], 4)
            else:
                self.assertTrue(np.isnan(e[1]))

        self.assertEqual(8, len(attrs))

        self.assertAlmostEqual(84.75415, attrs['eval_transpose'][0], 4)
        self.assertAlmostEqual(102.4951, attrs['pcvar'][0], 1)
        self.assertAlmostEqual(339.0166, attrs['eval'][0], 4)
        self.assertAlmostEqual(32.00000, attrs['pcrit'][0], 4)

        self.assertEqual("covariance", attrs['matrix'])
        self.assertEqual("transpose", attrs['method'])

        self.assertEqual(-99, data[0, 0, 3])

    # def test_sst_01(self):
    #     sst = self._nc_ds.sst
    #
    #     actual_response = eofunc(sst, 5, time_dim=0)
    #
    #     expected_response = self._nc_ds.evec
    #
    #     np.testing.assert_array_almost_equal(expected_response.data,
    #                                          actual_response.data)
    #
    #     np.testing.assert_array_almost_equal(
    #         expected_response.attrs["eval_transpose"],
    #         actual_response.attrs["eval_transpose"])
    #
    #     np.testing.assert_array_almost_equal(expected_response.attrs["eval"],
    #                                          actual_response.attrs["eval"])
    #
    #     np.testing.assert_array_almost_equal(expected_response.attrs["pcvar"],
    #                                          actual_response.attrs["pcvar"])
    #
    #     np.testing.assert_equal(actual_response.attrs["matrix"],
    #                             expected_response.attrs["matrix"])
    #
    #     np.testing.assert_equal(actual_response.attrs["method"],
    #                             expected_response.attrs["method"])


# class Test_eofunc_ts(TestCase, BaseEOFuncTestClass):
#
#     def test_01(self):
#         sst = self._nc_ds.sst
#         evec = self._nc_ds.evec
#         expected_tsout = self._nc_ds.tsout
#
#         actual_tsout = eofunc_ts(sst.data, evec.data, time_dim=0)
#
#         np.testing.assert_equal(actual_tsout.shape, expected_tsout.shape)
#
#         np.testing.assert_array_almost_equal(actual_tsout, expected_tsout.data)
#
#         np.testing.assert_array_almost_equal(actual_tsout.attrs["ts_mean"],
#                                              expected_tsout.attrs["ts_mean"])
#
#         np.testing.assert_equal(actual_tsout.attrs["matrix"],
#                                 expected_tsout.attrs["matrix"])
#
#     def test_02(self):
#         sst = self._nc_ds.sst
#         evec = self._nc_ds.evec
#         expected_tsout = self._nc_ds.tsout
#
#         actual_tsout = eofunc_ts(sst, evec, time_dim=0, meta=True)
#
#         np.testing.assert_equal(actual_tsout.shape, expected_tsout.shape)
#
#         np.testing.assert_array_almost_equal(actual_tsout, expected_tsout.data)
#
#         np.testing.assert_array_almost_equal(actual_tsout.attrs["ts_mean"],
#                                              expected_tsout.attrs["ts_mean"])
#
#         np.testing.assert_equal(actual_tsout.attrs["matrix"],
#                                 expected_tsout.attrs["matrix"])
#
#         for k, v in sst.attrs.items():
#             np.testing.assert_equal(actual_tsout.attrs[k], v)
#
#         np.testing.assert_equal(actual_tsout.coords["time"].data,
#                                 sst.coords["time"].data)
#
#         # print(actual_tsout)


a = Test_eofunc()
a.test_eofunc_02()