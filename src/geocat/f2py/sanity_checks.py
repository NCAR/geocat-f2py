import numpy as np
import xarray as xr
import dask as da


def sanity_check (user_variable_1, var_name=None, data_type=None, min_dimensions=None, dimensions=None, shape=None, is_xarray=None, is_none=None):

    if data_type is not None:
        if not (user_variable_1.dtype == data_type):
            raise Exception(var_name + " failed data_type check")

    if dimensions is not None:
        if not (user_variable_1.ndim == dimensions):
            raise Exception(var_name + " failed dimensions check")

    if shape is not None:
        if not (user_variable_1.shape == shape):
            raise Exception(var_name + " failed shape check")

    if is_xarray is not None:
        if is_xarray is True:
            if not isinstance(user_variable_1, xr.DataArray):
                raise Exception(var_name + " is not a xarray.DataArray")

    if is_none is not None:
        if is_none is True:
            if user_variable_1 is not None:
                raise Exception(var_name + " is not None")
        else:
            if user_variable_1 is None:
                raise Exception(var_name + " is None")

    if min_dimensions is not None:
        if not (user_variable_1.ndim >= min_dimensions):
            raise Exception(var_name + " failed min_dimensions check")


    return True



my_var = np.int16([[2,2],[2,2]])
sanity_check(my_var, var_name="my_var", dimensions=2)