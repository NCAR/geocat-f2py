import numpy as np
import xarray as xr

from eofs.xarray import Eof



def eofunc_eofs(data, neofs=1, time_dim=0, eofscaling=0, weights=None, center=True, ddof=1, neigs=None, vfscaled=False, meta=False):
    """
    Computes empirical orthogonal functions (EOFs, aka: Principal Component Analysis).

    This implementation uses `eofs` package (https://anaconda.org/conda-forge/eofs), which is built upon the
    following study: Dawson, Andrew, "eofs: A library for EOF analysis of meteorological, oceanographic, and
    climate data," Journal of Open Research Software, vol. 4, no. 1, 2016.

    This implementation provides a few convenience to the user on top of `eofs` package that are described below
    in the Parameters section.

    Parameters
    ----------
    data : :class:`xarray.DataArray` or :class:`numpy.ndarray` or :class:`list`
        Should contain numbers or `np.nan` for missing value representation. It must be at least a 2-dimensional array.

        When input data is of type `xarray.DataArray`, `eofs.xarray` package assumes the left-most dimension
        (i.e. `dim_0`) is the `time` dimension. In this case, that dimension should have the name "time".

        When input data is of type `numpy.ndarray` or `list`, this function still assumes the leftmost dimension
        to be the numbe of observations or `time` dimension: however, in this case, user is allowed to input otherwise.
        If the input do not have its leftmost dimension as the `time` or number of observations, then the user should
        specify with `time_dim=x` to define which dimension must be treated as time or number of observations

    neofs:
        A scalar integer that specifies the number of empirical orthogonal functions (i.e. eigenvalues and
        eigenvectors) to be returned. This is usually less than or equal to the minimum number of observations or
        number of variables.

    eofscaling:
        (From `eofs` package): Sets the scaling of the EOFs. The following values are accepted:
            - 0 : Un-scaled EOFs (default).
            - 1 : EOFs are divided by the square-root of their eigenvalues.
            - 2 : EOFs are multiplied by the square-root of their eigenvalues.

    weights:
        (From `eofs` package): An array of weights whose shape is compatible with those of the input array dataset.
        The weights can have the same shape as dataset or a shape compatible with an array broadcast (i.e., the shape
        of the weights can can match the rightmost parts of the shape of the input array dataset). If the input array
        dataset does not require weighting then the value None may be used. Defaults to None (no weighting).

    center:
        (From `eofs` package): If True, the mean along the first axis of dataset (the time-mean) will be removed prior
        to analysis. If False, the mean along the first axis will not be removed. Defaults to True (mean is removed).

        The covariance interpretation relies on the input data being anomaly data with a time-mean of 0. Therefore this
        option should usually be set to True. Setting this option to True has the useful side effect of propagating
        missing values along the time dimension, ensuring that a solution can be found even if missing values occur
        in different locations at different times.

    ddof:
        (From `eofs` package): ‘Delta degrees of freedom’. The divisor used to normalize the covariance matrix is
        N - ddof where N is the number of samples. Defaults to 1.

    time_dim:
        An integer defining the time dimension if it is not the leftmost dimension. When input data is of type
        `xarray.DataArray`, this is ignored (assuming `xarray.DataArray` has its leftmost dimension with the exact
        name 'time'). It must be between ``0`` and ``data.ndim - 1`` or it could be ``-1`` indicating the last
        dimension. Defaults to 0.

    neigs:
        (From `eofs` package): Number of eigenvalues to return. Defaults to all eigenvalues. If the number of
        eigenvalues requested is more than the number that are available, then all available eigenvalues will be
        returned.

    vfscaled:
        (From `eofs` package): If True, scale the errors by the sum of the eigenvalues. This yields typical errors
        with the same scale as the values returned by Eof.varianceFraction. If False then no scaling is done.
        Defaults to False.

    meta:
        If set to True and the input array is an Xarray, the metadata from the input array will be copied to the
        output array. Defaults to False.

    Returns
    -------
        A multi-dimensional array containing EOFs. The returned array will be of the same size as data with the
        leftmost dimension removed and an additional dimension of the size `neofs` added.

        The return variable will have associated with it the following attributes:

        eigenvalues:
            A one-dimensional array of size `neofs` that contains the eigenvalues associated with each EOF.

        eofsAsCorrelation:
            (From `eofs` package): Correlation map EOFs.

            Empirical orthogonal functions (EOFs) expressed as the correlation between the principal component
            time series (PCs) and the time series of the Eof input dataset at each grid point.

        eofsAsCovariance:
            (From `eofs` package): Covariance map EOFs.

            Empirical orthogonal functions (EOFs) expressed as the covariance between the principal component
            time series (PCs) and the time series of the Eof input dataset at each grid point.

        northTest:
            (From `eofs` package): Typical errors for eigenvalues.

            The method of North et al. (1982) is used to compute the typical error for each eigenvalue. It is
            assumed that the number of times in the input data set is the same as the number of independent
            realizations. If this assumption is not valid then the result may be inappropriate.

        totalAnomalyVariance:
            (From `eofs` package): Total variance associated with the field of anomalies (the sum of the eigenvalues).

        varianceFraction:
            (From `eofs` package): Fractional EOF mode variances.

            The fraction of the total variance explained by each EOF mode, values between 0 and 1 inclusive..

    """

    # ''' Start of boilerplate
    if not isinstance(data, xr.DataArray):

        data = np.asarray(data)

        if (time_dim >= data.ndim) or (time_dim < -data.ndim):
            raise ValueError(
                "ERROR eofunc_efs: `time_dim` out of bound."
            )

        # Transpose data if time_dim is not 0 (i.e. the first/left-most dimension)
        dims_to_transpose = np.arange(data.ndim)
        dims_to_transpose[time_dim] = 0
        dims_to_transpose[0] = time_dim
        data = np.transpose(data, axes=dims_to_transpose)

        dims = [f"dim_{i}" for i in range(data.ndim)]
        dims[0] = 'time'

        data = xr.DataArray(
            data,
            dims=dims,
        )

    # Checking number of EOFs
    if neofs <= 0:
        raise ValueError("ERROR eofunc_eofs: num_eofs must be a positive non-zero integer value.")

    solver = Eof(data, weights=weights, center=center, ddof=ddof)

    eofs = solver.eofs(neofs=neofs, eofscaling=eofscaling)

    # Populate attributes for output
    attrs = {}

    if meta:
        attrs = data.attrs

    attrs['eigenvalues'] = solver.eigenvalues(neigs=neigs)
    attrs['eofsAsCorrelation'] = solver.eofsAsCorrelation(neofs=neofs)
    attrs['eofsAsCovariance'] = solver.eofsAsCovariance(neofs=neofs, pcscaling=0)
    attrs['northTest'] = solver.northTest(neigs=neigs, vfscaled=vfscaled)
    attrs['totalAnomalyVariance'] = solver.totalAnomalyVariance()
    attrs['varianceFraction'] = solver.varianceFraction(neigs=neigs)

    if meta:
        dims = ["eof"] + [data.dims[i] for i in range(data.ndim) if i != time_dim]
        coords = {
            k: v for (k, v) in data.coords.items() if k != data.dims[time_dim]
        }
    else:
        dims = ["eof"] + [f"dim_{i}" for i in range(data.ndim) if i != time_dim]
        coords = {}

    return xr.DataArray(eofs, attrs=attrs, dims=dims, coords=coords)

def eofunc_pcs(data, npcs=1, pcscaling=0, weights=None, time_dim=0, meta=False):
    """
        Computes the principal components (time projection) in the empirical orthogonal function
        analysis.

        Args:
            data:
                an iterable object containing numbers. It must be at least a 2-dimensional array. The right-most dimension
                is assumed to be the number of observations. Generally this is the time time dimension. If your right-most
                dimension is not time, you could pass ``time_dim=x`` as an argument to define which dimension must be
                treated as time and/or number of observations. Data must be convertible to numpy.array
            npcs:
                A scalar integer that specifies the number of principal components to be returned. This is usually
                less than or equal to the minimum number of observations or number of variables.
            weights:
            time_dim: an integer defining the time dimension. it must be between ``0`` and ``data.ndim - 1`` or it
                could be ``-1`` indicating the last dimension. The default value is -1.
        """

    # ''' Start of boilerplate
    if not isinstance(data, xr.DataArray):

        data = np.asarray(data)

        if (time_dim >= data.ndim) or (time_dim < -data.ndim):
            raise ValueError(
                "ERROR eofunc_efs: `time_dim` out of bound."
            )

        # Transpose data if time_dim is not 0 (i.e. the first/left-most dimension)
        dims_to_transpose = np.arange(data.ndim)
        dims_to_transpose[time_dim] = 0
        dims_to_transpose[0] = time_dim
        data = np.transpose(data, axes=dims_to_transpose)

        dims = [f"dim_{i}" for i in range(data.ndim)]
        dims[0] = 'time'

        data = xr.DataArray(
            data,
            dims=dims,
        )

    # Checking number of EOFs
    if npcs <= 0:
        raise ValueError("ERROR eofunc_pcs: num_pcs must be a positive non-zero integer value.")

    solver = Eof(data, weights=weights)

    pcs = solver.pcs(npcs=npcs, pcscaling=pcscaling)
    pcs = pcs.transpose()

    # Populate attributes for output
    attrs = {}

    if meta:
        attrs = data.attrs

    dims = ["pc", "time"]
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

def eofunc_ts():
    #TODO WARNING this signature will be deprecated
    #TODO eofunc_pcs
    pass