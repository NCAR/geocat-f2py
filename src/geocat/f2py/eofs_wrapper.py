from typing import Iterable
import numpy as np
import xarray as xr
from dask.array.core import map_blocks
import time

# from geocat.f2py.fortran import (deof11)
from geocat.f2py.missing_values import (fort2py_msg, py2fort_msg)

from eofs.standard import Eof
# from eofs.xarray import Eof



def eofunc_eofs(data, num_eofs=1, weights=None, time_dim=None, meta=False):
    """
    Computes empirical orthogonal functions (EOFs, aka: Principal Component Analysis).

    Args:
        data:
            an iterable object containing numbers. It must be at least a 2-dimensional array. The right-most dimension
            is assumed to be the number of observations. Generally this is the time time dimension. If your right-most
            dimension is not time, you could pass ``time_dim=x`` as an argument to define which dimension must be
            treated as time and/or number of observations. Data must be convertible to numpy.array
        num_eofs:
            A scalar integer that specifies the number of eigenvalues and eigenvectors to be returned. This is usually
            less than or equal to the minimum number of observations or number of variables.
        weights:
        time_dim: an integer defining the time dimension. it must be between ``0`` and ``data.ndim - 1`` or it
            could be ``-1`` indicating the last dimension. The default value is -1.
    """

    # ''' Start of boilerplate
    if not isinstance(data, xr.DataArray):
        data = xr.DataArray(data)

    if time_dim is None:
        time_dim = data.ndim-1

    # Checking number of EOFs
    if num_eofs <= 0:
        raise ValueError("ERROR eofunc_eofs: num_eofs must be a positive non-zero integer value.")

    # TODO: Find a generic solution based on which dimension is "time"
    data_transpose = np.transpose(data.values, axes=(2, 1, 0))

    solver = Eof(data_transpose, weights=weights)

    eofs = solver.eofs(neofs=num_eofs)
    pcs = solver.pcs(npcs=num_eofs, pcscaling=0)

    # Populate attributes for output
    attrs = {}

    if meta:
        attrs = data.attrs

    attrs['eigenvalues'] = solver.eigenvalues()
    attrs['varianceFraction'] = solver.varianceFraction()
    attrs['totalAnomalyVariance'] = solver.totalAnomalyVariance()
    attrs['eofsAsCovariance'] = solver.eofsAsCovariance(neofs=num_eofs)
    attrs['eofsAsCorrelation'] = solver.eofsAsCorrelation(neofs=num_eofs)

    if meta:
        dims = ["evn"] + [data.dims[i] for i in range(data.ndim) if i != time_dim]
        coords = {
            k: v for (k, v) in data.coords.items() if k != data.dims[time_dim]
        }
    else:
        dims = ["evn"] + [f"dim_{i}" for i in range(data.ndim) if i != time_dim]
        coords = {}

    return xr.DataArray(eofs, attrs=attrs, dims=dims, coords=coords)

def eofunc_pcs(data, num_pcs=1, weights=None, time_dim=None, meta=False):
    """
        Computes the principal components (time projection) in the empirical orthogonal function
        analysis.

        Args:
            data:
                an iterable object containing numbers. It must be at least a 2-dimensional array. The right-most dimension
                is assumed to be the number of observations. Generally this is the time time dimension. If your right-most
                dimension is not time, you could pass ``time_dim=x`` as an argument to define which dimension must be
                treated as time and/or number of observations. Data must be convertible to numpy.array
            num_pcs:
                A scalar integer that specifies the number of principal components to be returned. This is usually
                less than or equal to the minimum number of observations or number of variables.
            weights:
            time_dim: an integer defining the time dimension. it must be between ``0`` and ``data.ndim - 1`` or it
                could be ``-1`` indicating the last dimension. The default value is -1.
        """

    # ''' Start of boilerplate
    if not isinstance(data, xr.DataArray):
        data = xr.DataArray(data)

    if time_dim is None:
        time_dim = data.ndim - 1

    # Checking number of EOFs
    if num_pcs <= 0:
        raise ValueError("ERROR eofunc_pcs: num_pcs must be a positive non-zero integer value.")

    # TODO: Find a generic solution based on which dimension is "time"
    data_transpose = data.values
    # data_transpose = np.transpose(data.values, axes=(2, 1, 0))

    solver = Eof(data_transpose, weights=weights)

    pcs = solver.pcs(npcs=num_pcs, pcscaling=0)
    pcs = pcs.transpose()

    # Populate attributes for output
    attrs = {}

    if meta:
        attrs = data.attrs

    dims = ["neval", "time"]
    if meta:
        coords = {"time": data.coords[data.dims[time_dim]]}
    else:
        coords = {}

    return xr.DataArray(pcs, attrs=attrs, dims=dims, coords=coords)


# def eofunc_ts(data: Iterable, evec, **kwargs) -> xr.DataArray:
#     """
#     Calculates the time series of the amplitudes associated with each eigenvalue in an EOF.
#     Args:
#         data: An Iterable convertible to `numpy.ndarray` in which the rightmost dimension is the number of
#               observations. Generally, this is the time dimension. If your rightmost dimension is not time, then pass
#               `time_dim` as an extra options.
#         evec: An Iterable convertible to `numpy.ndarray` containing the EOFs calculated using `eofunc`.
#         **kwargs:
#             extra options controlling the behavior of the function. Currently the following are supported:
#             - ``jopt``: a string that indicates whether to use the covariance matrix or the correlation
#                         matrix. The default is to use the covariance matrix.
#             - ''time_dim``: an integer defining the time dimension. it must be between ``0`` and ``data.ndim - 1`` or it
#                             could be ``-1`` indicating the last dimension. The default value is -1.
#             - ``missing_value``: defines the missing_value. The default is ``np.nan``.
#             - ``meta``: If set to True and the input array is an Xarray, the metadata from the input array will be
#                         copied to the output array; default is False.
#
#     Returns: A two-dimensional array dimensioned by the number of eigenvalues selected in `eofunc` by the size of the
#              time dimension of data. Will contain the following attribute:
#              - `ts_mean`: an array of the same size and type as `evec` containing the means removed from data as part
#                           of the calculation.
#
#     Examples:
#         * Passing a xarray:
#
#         >>> # Openning a data set:
#         ... ds = xr.open_dataset("dataset.nc")
#         >>> # Extracting SST (Sea Surface temperature)
#         ... sst = ds.sst
#         >>> evec = eofunc(sst, 5)
#         >>> ts = eofunc(sst, evec)
#
#         * Passing a numpy array:
#
#         >>> # Openning a data set:
#         ... ds = xr.open_dataset("dataset.nc")
#         >>> # Extracting SST (Sea Surface temperature) as Numpy Array
#         ... sst = ds.sst.data
#         >>> evec = eofunc(sst, 5)
#         >>> ts = eofunc(sst, evec.data)
#
#         * Transferring the attributes from input to the output:
#
#         >>> # Openning a data set:
#         ... ds = xr.open_dataset("dataset.nc")
#         >>> # Extracting SST (Sea Surface temperature)
#         ... sst = ds.sst
#         >>> evec = eofunc(sst, 5)
#         >>> ts = eofunc(sst, evec, meta=True)
#
#         * Defining the time dimension:
#
#         >>> # Openning a data set:
#         ... ds = xr.open_dataset("dataset.nc")
#         >>> # Extracting SST (Sea Surface temperature)
#         ... sst = ds.sst
#         >>> evec = eofunc(sst, 5, time_dim=0)
#         >>> ts = eofunc(sst, evec, time_dim=0)

