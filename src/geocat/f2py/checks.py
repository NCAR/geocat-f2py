import dask as da
import numpy as np
import xarray as xr


def check(user_variable,
          var_name='variable',
          data_type=None,
          max_dimensions=None,
          min_dimensions=None,
          dimensions=None,
          shape=None,
          is_xarray=None,
          is_none=None,
          is_numpy=None,
          is_chunked=None,
          comparison=None,
          unchunked_dims=None,
          exceptions=True):
    """Function of data checks for use in wrapper functions.

    user_variable : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        Variable of interest

    data_type : :class:`type` or :type:`tuple of types`:
        Desired data_type of user_variable
        ex: data_type=np.ndarray

    max_dimensions : :class:`tuple`:
        Maximum number of dimensions needed from user_variable for function
        ex: max_dimensions=(3) or max_dimensions=3

    min_dimensions : :class:`tuple`:
        Minimum number of dimensions needed from user_variable for function
        ex: min_dimensions=(3) or min_dimensions=3

    dimensions : :class:`tuple`:
        Number of dimensions needed from user_variable for function
        ex: dimensions=(3) or dimensions=3

    shape : :class:`tuple`:
        Checks user_variable's shape
        ex: shape=(3, 3, 3)

    is_xarray : :class:`bool`:
        Checking whether user_variable is of class xarray.DataArray.
        Valid inputs are True or False

    is_none : :class:`bool`:
        Checking whether user_variable is of class NoneType.
        Valid input is True or False

    comparison : :class:`n/a`:
        Compares user variable against item passed in as comparison
        Valid input is anything

    unchunked_dims : :class:`tuple`:
        Checks for unchunked dimensions in user_variable
        ex: check(user_variable, unchunked_dims=[3]) *must include brackets*

    exceptions : :class:`bool`:
        Allows user to turn off exceptions in the check functions
        Valid input is True or False

    is_numpy : :class:`bool`:
        Checks whether variable is of class numpy.ndarray
        Valid input is True or False

    is_chunked : :class:`bool`:
        Checks whether variable is chunked
        Valid input is True or False
    """
    return_value = True

    if data_type is not None:
        if not isinstance(user_variable, data_type):
            if exceptions:
                raise TypeError(var_name + " failed data_type check.")
            else:
                return_value = False

    if dimensions is not None:
        if not (user_variable.ndim == dimensions):
            if exceptions:
                raise Exception(var_name + " failed dimensions check")
            else:
                return_value = False

    if shape is not None:
        if not (user_variable.shape == shape):
            if exceptions:
                raise Exception(var_name + " failed shape check")
            else:
                return_value = False

    if is_none is not None:
        if is_none is True:
            if user_variable is not None:
                if exceptions:
                    raise Exception(var_name + " is not None")
                else:
                    return_value = False
        if is_none is False:
            if user_variable is None:
                if exceptions:
                    raise Exception(var_name + " is None")
                else:
                    return_value = False

    if min_dimensions is not None:
        if not (user_variable.ndim >= min_dimensions):
            if exceptions:
                raise Exception(var_name + " failed min_dimensions check")
            else:
                return_value = False

    if max_dimensions is not None:
        if not (user_variable.ndim <= max_dimensions):
            if exceptions:
                raise Exception(var_name + " failed max_dimensions check")
            else:
                return_value = False

    if comparison is not None:
        if not (user_variable == comparison):
            if exceptions:
                raise Exception(var_name + " failed comparison check")
            else:
                return_value = False

    if is_numpy is not None:
        if is_numpy is True:
            if not isinstance(user_variable_1, np.array):
                if exceptions:
                    raise Exception(var_name + " is not a numpy.Array")
                else:
                    return_value = False
        if is_numpy is False:
            if isinstance(user_variable_1, np.array):
                if exceptions:
                    raise Exception(var_name + " is an numpy.Array")
                else:
                    return_value = False

    #
    # Xarray specific checks
    #
    if is_xarray is not None:
        if is_xarray is True:
            if not isinstance(user_variable_1, xr.DataArray):
                if exceptions:
                    raise Exception(var_name + " is not a xarray.DataArray")
                else:
                    return_value = False
        if is_xarray is False:
            if isinstance(user_variable_1, xr.DataArray):
                if exceptions:
                    raise Exception(var_name + " is an xarray.DataArray")
                else:
                    return_value = False

    if is_chunked is not None:
        if is_chunked is True:
            if var_name.chunks is None:
                if exceptions:
                    raise Exception(var_name + "is not chunked")
                else:
                    return_value = False
        if is_chunked is False:
            if var_name.chunks is not None:
                if exceptions:
                    raise Exception(var_name + "is chunked")
                else:
                    return_value = False

    if unchunked_dims is not None:
        for dim in unchunked_dims:
            if len(user_variable.chunks[dim]) > 1:
                if exceptions:
                    raise Exception(var_name +
                                    " must not be chunked along dimension " +
                                    str(dim))
                else:
                    return_value = False

    return return_value
