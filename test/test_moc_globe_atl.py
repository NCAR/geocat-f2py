import unittest as ut
import numpy as np
import xarray as xr
import numpy.testing as nt

import geocat.f2py

# Dimensions
nyaux = 3  # nyaux = lat_aux_grid->shape[0]
kdep = 4  # kdep  = a_wvel/a_bolus/a_submeso->shape[0]
nlat = 5  # nlat  = a_wvel/a_bolus/a_submeso->shape[1] AND tlat->shape[0] AND rmlak->shape[1]
mlon = 6  # mlon  = a_wvel/a_bolus/a_submeso->shape[2] AND tlat->shape[1] AND rmlak->shape[2]

kdepnyaux2 = 2 * kdep * nyaux
nlatmlon = nlat * mlon
kdepnlatmlon = kdep * nlatmlon

# Generate arbitrary data
tmp_a = np.linspace(1, kdepnlatmlon, num=kdepnlatmlon).reshape(
    (kdep, nlat, mlon))

# nan input
tmp_a_nan = tmp_a.copy()
tmp_a_nan[0, 1, 1] = np.nan
tmp_a_nan[0, 2, 3] = np.nan
tmp_a_nan[1, 1, 1] = np.nan
tmp_a_nan[1, 2, 3] = np.nan

# nan input
tmp_a_msg = tmp_a_nan.copy()
tmp_a_msg[np.isnan(tmp_a_msg)] = -99

# Generate test data
lat_aux_grid = np.asarray([5, 10, 15])
rmlak = np.ones((2, nlat, mlon))
t_lat = np.linspace(1, nlatmlon, num=nlatmlon).reshape((nlat, mlon))

# Generate expected NCL outputs
ncl_truth = [
    0.00, 35.00, 60.00, 0.00, 185.00, 210.00, 0.00, 335.00, 360.00, 0.00,
    485.00, 510.00, 0.00, 35.00, 60.00, 0.00, 185.00, 210.00, 0.00, 335.00,
    360.00, 0.00, 485.00, 510.00, 0.00, 35.00, 60.00, 0.00, 185.00, 210.00,
    0.00, 335.00, 360.00, 0.00, 485.00, 510.00, 0.00, 35.00, 60.00, 0.00,
    185.00, 210.00, 0.00, 335.00, 360.00, 0.00, 485.00, 510.00, 0.00, 35.00,
    60.00, 0.00, 185.00, 210.00, 0.00, 335.00, 360.00, 0.00, 485.00, 510.00,
    0.00, 35.00, 60.00, 0.00, 185.00, 210.00, 0.00, 335.00, 360.00, 0.00,
    485.00, 510.00
]
ncl_truth = np.reshape(ncl_truth, (3, 2, kdep, nyaux))

ncl_truth_msg = [
    0.00, 27.00, 60.00, 0.00, 147.00, 210.00, 0.00, 335.00, 360.00, 0.00,
    485.00, 510.00, 0.00, 27.00, 60.00, 0.00, 147.00, 210.00, 0.00, 335.00,
    360.00, 0.00, 485.00, 510.00, 0.00, 27.00, 60.00, 0.00, 147.00, 210.00,
    0.00, 335.00, 360.00, 0.00, 485.00, 510.00, 0.00, 27.00, 60.00, 0.00,
    147.00, 210.00, 0.00, 335.00, 360.00, 0.00, 485.00, 510.00, 0.00, 27.00,
    60.00, 0.00, 147.00, 210.00, 0.00, 335.00, 360.00, 0.00, 485.00, 510.00,
    0.00, 27.00, 60.00, 0.00, 147.00, 210.00, 0.00, 335.00, 360.00, 0.00,
    485.00, 510.00
]
ncl_truth_msg = np.reshape(ncl_truth_msg, (3, 2, kdep, nyaux))


class Test_Moc_Globe_Atl(ut.TestCase):

    def test_moc_globe_atl_float64(self):

        out_arr = geocat.f2py.moc_globe_atl(lat_aux_grid,
                                            tmp_a.astype(np.float64),
                                            tmp_a.astype(np.float64),
                                            tmp_a.astype(np.float64),
                                            t_lat,
                                            rmlak)

        nt.assert_array_almost_equal(ncl_truth, out_arr)
        nt.assert_equal((3, 2, kdep, nyaux), out_arr.shape)

    def test_moc_globe_atl_float64_xr(self):

        out_arr = geocat.f2py.moc_globe_atl(xr.DataArray(lat_aux_grid),
                                            xr.DataArray(tmp_a.astype(np.float64)),
                                            xr.DataArray(tmp_a.astype(np.float64)),
                                            xr.DataArray(tmp_a.astype(np.float64)),
                                            xr.DataArray(t_lat),
                                            xr.DataArray(rmlak))

        nt.assert_array_almost_equal(ncl_truth, out_arr)
        nt.assert_equal((3, 2, kdep, nyaux), out_arr.shape)

    def test_moc_globe_atl_float32(self):

        out_arr = geocat.f2py.moc_globe_atl(lat_aux_grid,
                                            tmp_a.astype(np.float32),
                                            tmp_a.astype(np.float32),
                                            tmp_a.astype(np.float32),
                                            t_lat,
                                            rmlak)

        nt.assert_array_almost_equal(ncl_truth, out_arr)
        nt.assert_equal((3, 2, kdep, nyaux), out_arr.shape)

    def test_moc_globe_atl_int64(self):

        out_arr = geocat.f2py.moc_globe_atl(lat_aux_grid,
                                            tmp_a.astype(np.int64),
                                            tmp_a.astype(np.int64),
                                            tmp_a.astype(np.int64),
                                            t_lat,
                                            rmlak)

        nt.assert_array_almost_equal(ncl_truth, out_arr)
        nt.assert_equal((3, 2, kdep, nyaux), out_arr.shape)

    def test_moc_globe_atl_msg_99(self):

        out_arr = geocat.f2py.moc_globe_atl(lat_aux_grid,
                                            tmp_a_msg,
                                            tmp_a_msg,
                                            tmp_a_msg,
                                            t_lat,
                                            rmlak,
                                            msg=-99)

        nt.assert_array_almost_equal(ncl_truth_msg, out_arr)
        nt.assert_equal((3, 2, kdep, nyaux), out_arr.shape)

    def test_moc_globe_atl_msg_nan(self):

        out_arr = geocat.f2py.moc_globe_atl(lat_aux_grid,
                                            tmp_a_nan,
                                            tmp_a_nan,
                                            tmp_a_nan,
                                            t_lat,
                                            rmlak,
                                            msg=np.nan)

        nt.assert_array_almost_equal(ncl_truth_msg, out_arr)
        nt.assert_equal((3, 2, kdep, nyaux), out_arr.shape)
