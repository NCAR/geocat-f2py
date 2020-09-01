import numpy as np
import xarray as xr
from .fortran.linint2 import (dlinint2)


def linint2(fi: xr.DataArray, xo: np.ndarray, yo: np.ndarray):

    fo = dlinint2(xi, yi, fi, xo, yo)
    return fo
