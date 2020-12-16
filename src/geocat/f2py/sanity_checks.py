import numpy as np
import xarray as xr
from geocat.f2py.errors import (CoordinateError, ChunkError, DimensionError)

from dask.array.core import map_blocks

from geocat.f2py.fortran import (drcm2rgrid, drgrid2rcm)
from .errors import (ChunkError, CoordinateError)
from geocat.f2py.missing_values import (fort2py_msg, py2fort_msg)

def chunks(yi, xi, fi):
    '''
    Checks if right most dimensions of data is chunked 
    
    Args:
        
        yi (:class:`numpy.ndarray`):
            An n dimensional array that specifies the Y or latitude coordinates
            of fi. 
            
        xi (:class:`numpy.ndarray`):
            An n dimensional array that specifies the X or longitude coordinates
            of fi.
            
        fi (:class:`numpy.ndarray`):
            A multi-dimensional array to be interpolated. The rightmost two
            dimensions, (latitude, longitude) or (Y, X), are the dimensions to 
            be interpolated.

    '''
    if list(fi.chunks)[-2:] != [yi.shape, xi.shape]:
        raise ChunkError("fi must be unchunked along the rightmost two dimensions")
        
def coord2d_check(lat2d, lon2d):
    '''
    Checks if lat2d and lon2d have been provided to function
    
    Args:
        
        lat2d (:class:`numpy.ndarray`):
            A 2-dimensional array that specifies the Y or latitude coordinates
            of fi. 
            
         lon2d (:class:`numpy.ndarray`):
            A 2-dimensional array that specifies the X or longitude coordinates
            of fi.

    '''
    
    if (lat2d is None) | (lon2d is None):
         raise CoordinateError(
             "rcm2points: lat2d and lon2d should always be provided")

def coord1d_check(yi, xi, fi):
    '''
    Checks if yi and xi, or lat1d and lon1d, has been provided to function
    
    Args:
        yi (:class:`numpy.ndarray`):
            A 1-dimensional array that specifies the Y or latitude coordinates of fi.  
            
        xi (:class:`numpy.ndarray`):
            A 1-dimensional array that specifies the X or longitude coordinates of fi.
        
        fi (:class:`xarray.DataArray` or :class:`numpy.ndarray`):
            A multi-dimensional array to be interpolated. The rightmost two
            dimensions, (latitude, longitude) or (Y, X), are the dimensions 
            to be interpolated.
    '''
    if not isinstance(fi, xr.DataArray):
        if (yi is None) | (xi is None):
            raise CoordinateError(
                "Arguments yi or xi must be provided explicitly unless fi is an xarray.DataArray.")

