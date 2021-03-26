import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from .errors import ChunkError, CoordinateError
from .fortran import mocloops
from .missing_values import fort2py_msg, py2fort_msg

# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.


def _moc_loops(lat_aux_grid, a_wvel, a_bolus, a_submeso, t_lat, rmlak, msg_py):
    # signature:  tmp1,tmp2,tmp3 = mocloops(tlat,lat_aux_grid,rmlak,work1,work2,work3,wmsg)
    work1 = a_wvel
    work2 = a_bolus
    work3 = a_submeso

    work1 = np.transpose(work1, axes=(2, 1, 0))
    work2 = np.transpose(work2, axes=(2, 1, 0))
    work3 = np.transpose(work3, axes=(2, 1, 0))

    # transpositions
    t_lat = np.transpose(t_lat, axes=(1, 0))
    rmlak = np.transpose(rmlak, axes=(2, 1, 0))

    # missing value handing for a_wvel (work1)
    work1, msg_py, msg_fort = py2fort_msg(work1, msg_py=msg_py)

    # fortran call
    tmp1, tmp2, tmp3 = mocloops(t_lat, lat_aux_grid, rmlak, work1, work2, work3,
                                msg_fort)

    # Un-transpose arrays for output
    tmp1 = np.transpose(tmp1, axes=(2, 1, 0))
    tmp2 = np.transpose(tmp2, axes=(2, 1, 0))
    tmp3 = np.transpose(tmp3, axes=(2, 1, 0))

    # missing value handling
    tmp1, msg_fort, msg_py = fort2py_msg(tmp1, msg_fort=msg_fort, msg_py=msg_py)
    tmp2, msg_fort, msg_py = fort2py_msg(tmp2, msg_fort=msg_fort, msg_py=msg_py)
    tmp3, msg_fort, msg_py = fort2py_msg(tmp3, msg_fort=msg_fort, msg_py=msg_py)

    # Merge output arrays
    tmp_out = xr.DataArray(np.stack((tmp1, tmp2, tmp3)))

    return tmp_out


# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.


def moc_globe_atl(lat_aux_grid,
                  a_wvel,
                  a_bolus,
                  a_submeso,
                  t_lat,
                  rmlak,
                  msg=None,
                  meta=False):
    """Facilitates calculating the meridional overturning circulation for the
    globe and Atlantic.

    Args:

    lat_aux_grid : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        Latitude grid for transport diagnostics.

    a_wvel : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        Area weighted Eulerian-mean vertical velocity [TAREA*WVEL].

    a_bolus : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        Area weighted Eddy-induced (bolus) vertical velocity [TAREA*WISOP].

    a_submeso : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        Area weighted submeso vertical velocity [TAREA*WSUBM].

    tlat : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        Array of t-grid latitudes.

    rmlak : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        Basin index number: [0]=Globe, [1]=Atlantic

    msg : :obj:`numpy.number`:
      A numpy scalar value that represent a missing value.
      This argument allows a user to use a missing value scheme
      other than NaN or masked arrays, similar to what NCL allows.

    meta : :obj:`bool`:
        If set to True and the input array is an Xarray, the metadata
        from the input array will be copied to the output array;
        default is False.
        Warning: this option is not currently supported.

    Returns
    -------

    fo : :class:`xarray.DataArray`:
        A multi-dimensional array of size
        [moc_comp] x [n_transport_reg] x [kdepth] x [nyaux] where:

        - moc_comp refers to the three components returned
        - n_transport_reg refers to the Globe and Atlantic
        - kdepth is the the number of vertical levels of the work arrays
        - nyaux is the size of the lat_aux_grid

        The type of the output data will be double only if a_wvel or a_bolus or
        a_submesa is of type double. Otherwise, the return type will be float.


    Examples
    --------

        # Input data can be read from a data set as follows:
        import xarray as xr

        ds = xr.open_dataset("input.nc")

        lat_aux_grid = ds.lat_aux_grid
        a_wvel = ds.a_wvel
        a_bolus = ds.a_bolus
        a_submeso = ds.a_submeso
        tlat = ds.tlat
        rmlak = ds.rmlak

        # (1) Calling with xArray inputs and default arguments (Missing value = np.nan, NO meta information)
        out_arr = moc_globe_atl(lat_aux_grid, a_wvel, a_bolus, a_submeso, tlat, rmlak)

        # (2) Calling with Numpy inputs and default arguments (Missing value = np.nan, NO meta information)
        out_arr = moc_globe_atl(lat_aux_grid.values, a_wvel.values, a_bolus.values, a_submeso.values,
                                tlat.values, rmlak.values)

        # (3) Calling with xArray inputs and user-defined arguments (Missing value = np.nan, NO meta information)
        out_arr = moc_globe_atl(lat_aux_grid, a_wvel, a_bolus, a_submeso, tlat, rmlak, msg=-99.0, meta=True)

        # (4) Calling with Numpy inputs and user-defined arguments (Missing value = np.nan, NO meta information)
        out_arr = moc_globe_atl(lat_aux_grid.values, a_wvel.values, a_bolus.values, a_submeso.values,
                                tlat.values, rmlak.values, msg=-99.0, meta=True)
    """

    # ''' Start of boilerplate
    if not isinstance(lat_aux_grid, xr.DataArray):
        lat_aux_grid = xr.DataArray(lat_aux_grid)

    if not isinstance(a_wvel, xr.DataArray):
        a_wvel = xr.DataArray(a_wvel)

    if not isinstance(a_bolus, xr.DataArray):
        a_bolus = xr.DataArray(a_bolus)

    if not isinstance(a_submeso, xr.DataArray):
        a_submeso = xr.DataArray(a_submeso)

    if not isinstance(t_lat, xr.DataArray):
        t_lat = xr.DataArray(t_lat)

    if not isinstance(rmlak, xr.DataArray):
        rmlak = xr.DataArray(rmlak)

    fo = _moc_loops(lat_aux_grid.values, a_wvel.values, a_bolus.values,
                    a_submeso.values, t_lat.values, rmlak.values, msg)

    return fo
