import xarray as xr
import numpy as np
import dask as da

'''
Checks wrapper functions to ensure data is correctly formatted and stops code from running if not.
'''

def check(user_variable_1,
          var_name='variable',
          data_type=None,
          max_dimensions=None,
          min_dimensions=None,
          dimensions=None,
          shape=None,
          is_xarray=None,
          is_none=None,
          comparison=None,
          unchunked_dims=None):

    if data_type is not None:
        ''' 
        data_type input of type or tuple of types
        ex: data_type=np.ndarray
        '''
        if not isinstance(user_variable_1, data_type): #== data_type):
            raise Exception(var_name + " failed data_type check")

    if dimensions is not None:
        '''
        Number of dimensions of variable in type tuple
        ex: dimensions=(3) or dimensions=3
        '''
        if not (user_variable_1.ndim == dimensions):
            raise Exception(var_name + " failed dimensions check")

    if shape is not None:
        '''
        Input variable's shape of type tuple
        ex: shape=(3, 3, 3) or shape=(3,3,3)
        '''
        if not (user_variable_1.shape == shape):
            raise Exception(var_name + " failed shape check")

    if is_none is not None:
        if is_none is True:
            if user_variable_1 is not None:
                raise Exception(var_name + " is not None")
        if is_none is False:
            if user_variable_1 is None:
                raise Exception(var_name + " is None")

    if min_dimensions is not None:
        '''
        Minimum number of dimensions needed from variable for function in type tuple
        ex: min_dimensions=(3) or min_dimensions=3
        '''
        if not (user_variable_1.ndim >= min_dimensions):
            raise Exception(var_name + " failed min_dimensions check")

    if max_dimensions is not None:
        '''
        Maximum number of dimensions allowed from variable for function in type tuple
        ex: max_dimensions=(3) or max_dimensions=3
        '''
        if not (user_variable_1.ndim <= max_dimensions):
            raise Exception(var_name + " failed max_dimensions check")

    if comparison is not None:
        if not (user_variable_1 == comparison):
            raise Exception(var_name + " failed comparison check")

    #
    # Xarray specific checks
    #

    if is_xarray is not None:
        '''
        Checking that input data is of class xarray.DataArray. 
        Input is True or False
        '''
        if is_xarray is True:
            if not isinstance(user_variable_1, xr.DataArray):
                raise Exception(var_name + " is not a xarray.DataArray")
            else: pass
        if is_xarray is False:
            if isinstance(user_variable_1, xr.DataArray):
                pass
                # raise Exception(var_name + " is an xarray.DataArray")
            else:
                print(var_name + " is not xarray.DataArray, reformatting...")
                return True

    if unchunked_dims is not None:
        '''
        Checking that input data is chunked correctly. 
        Input is type tuple
        ex: unchunked_dims=[3] *must include brackets*
        '''
        for dim in unchunked_dims:
            if len(user_variable_1.chunks[dim]) > 1:
                raise Exception(var_name +
                                " must not be chunked along dimension " +
                                str(dim))

    return True
