import sys
import time
import unittest as ut

import numpy as np
import numpy.testing as nt
import xarray as xr

# Import from directory structure if coverage test, or from installed
# packages otherwise
if "--cov" in str(sys.argv):
    from src.geocat.f2py import dpres_plevel
else:
    from geocat.f2py import dpres_plevel

# Expected Output
# Pressure levels (Pa)
pressure_levels = np.array([
    1000., 950., 900., 850., 800., 750., 700., 650., 600., 550., 500., 450.,
    400., 350., 300., 250., 200., 175., 150., 125., 100., 80., 70., 60., 50.,
    40., 30., 25., 20., 10.
])    # units hPa
# convert hPa to Pa
pressure_levels = pressure_levels * 100.0

pressure_levels_asfloat32 = pressure_levels.astype(np.float32)

# Surface pressure (scalar and 2D, as well as 2D with np.nan and -99 missing values)
pressure_surface_scalar = 101800.0    # Units of Pa
pressure_surface_2d = np.array([1018.0, 1016.0, 1014.0,
                                1012.0]).reshape(2, 2)    # Units of Pa
pressure_surface_2d = pressure_surface_2d * 100

pressure_surface_2d_asfloat32 = pressure_surface_2d.astype(np.float32)

# missing value of np.nan
pressure_surface_2d_nan = pressure_surface_2d.copy()
pressure_surface_2d_nan[0, 1] = np.nan

pressure_surface_2d_nan_asfloat32 = pressure_surface_2d_nan.astype(np.float32)

# missing value of -99
pressure_surface_2d_msg = pressure_surface_2d_nan.copy()
pressure_surface_2d_msg[np.isnan(pressure_surface_2d_msg)] = -99.0

pressure_surface_2d_msg_asfloat32 = pressure_surface_2d_msg.astype(np.float32)

# Expected Output
# for scalar pressure_surface
expected_dp_psfc_scalar = np.array([
    4300., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000.,
    5000., 5000., 5000., 5000., 5000., 3750., 2500., 2500., 2500., 2250., 1500.,
    1000., 1000., 1000., 1000., 750., 500., 750., 500.
])

# for 2D pressure_surface
expected_dp_psfc_2d = np.array([
    4300., 4100., 3900., 3700., 5000., 5000., 5000., 5000., 5000., 5000., 5000.,
    5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000.,
    5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000.,
    5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000.,
    5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000.,
    5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 5000., 3750., 3750.,
    3750., 3750., 2500., 2500., 2500., 2500., 2500., 2500., 2500., 2500., 2500.,
    2500., 2500., 2500., 2250., 2250., 2250., 2250., 1500., 1500., 1500., 1500.,
    1000., 1000., 1000., 1000., 1000., 1000., 1000., 1000., 1000., 1000., 1000.,
    1000., 1000., 1000., 1000., 1000., 750., 750., 750., 750., 500., 500., 500.,
    500., 750., 750., 750., 750., 500., 500., 500., 500.
]).reshape(30, 2, 2)

# for msg_py = -np.nan input
expected_dp_psfc_2d_msg_nan = expected_dp_psfc_2d.copy()
expected_dp_psfc_2d_msg_nan[0, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[1, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[2, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[3, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[4, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[5, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[6, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[7, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[8, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[9, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[10, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[11, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[12, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[13, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[14, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[15, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[16, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[17, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[18, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[19, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[20, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[21, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[22, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[23, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[24, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[25, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[26, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[27, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[28, 0, 1] = np.nan
expected_dp_psfc_2d_msg_nan[29, 0, 1] = np.nan

# for msg_py = -99 input
expected_dp_psfc_2d_msg_99 = expected_dp_psfc_2d_msg_nan.copy()
expected_dp_psfc_2d_msg_99[np.isnan(expected_dp_psfc_2d_msg_99)] = -99.0


class Test_dpres_plevel_float64_psfc_scalar(ut.TestCase):

    def test_dpres_plevel_float64(self):
        result_dp = dpres_plevel(pressure_levels, pressure_surface_scalar)
        nt.assert_array_equal(expected_dp_psfc_scalar, result_dp.values)


class Test_dpres_plevel_float64_psfc_2d(ut.TestCase):

    def test_dpres_plevel_float64(self):
        result_dp = dpres_plevel(pressure_levels, pressure_surface_2d)
        nt.assert_array_equal(expected_dp_psfc_2d, result_dp.values)

    def test_dpres_plevel_float64_msg_nan(self):
        result_dp = dpres_plevel(pressure_levels, pressure_surface_2d_nan)
        nt.assert_array_equal(expected_dp_psfc_2d_msg_nan, result_dp.values)

    def test_dpres_plevel_float64_msg_99(self):
        result_dp = dpres_plevel(pressure_levels,
                                 pressure_surface_2d_msg,
                                 msg_py=-99.0)
        nt.assert_array_equal(expected_dp_psfc_2d_msg_99, result_dp.values)


class Test_dpres_plevel_float32_psfc_scalar(ut.TestCase):

    def test_dpres_plevel_float32(self):
        plev_asfloat32 = pressure_levels.astype(np.float32)
        result_dp = dpres_plevel(plev_asfloat32, pressure_surface_scalar)
        nt.assert_array_equal(expected_dp_psfc_scalar, result_dp.values)


class Test_dpres_plevel_float32_psfc_2d(ut.TestCase):

    def test_dpres_plevel_float32(self):
        result_dp = dpres_plevel(pressure_levels_asfloat32,
                                 pressure_surface_2d_asfloat32)
        nt.assert_array_equal(expected_dp_psfc_2d, result_dp.values)

    def test_dpres_plevel_float32_msg_nan(self):
        result_dp = dpres_plevel(pressure_levels_asfloat32,
                                 pressure_surface_2d_nan_asfloat32)
        asd = np.sum(result_dp.values != expected_dp_psfc_2d_msg_nan)
        nt.assert_array_almost_equal(expected_dp_psfc_2d_msg_nan,
                                     result_dp.values)

    def test_dpres_plevel_float32_msg_99(self):
        result_dp = dpres_plevel(pressure_levels_asfloat32,
                                 pressure_surface_2d_msg_asfloat32,
                                 msg_py=-99)
        nt.assert_array_equal(expected_dp_psfc_2d_msg_99, result_dp.values)
