import numpy as np
import xarray as xr
from .fortran import (dlinint2)


def linint2(fi, xo, yo):
    fo = dlinint2(xi, yi, fi, xo, yo)
    return fo
