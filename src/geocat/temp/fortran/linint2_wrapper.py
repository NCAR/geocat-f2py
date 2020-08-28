from linint2 import (dlinint1, dlinint2, dlinint2pts)
import numpy as np

n = 127

xi = np.linspace(1,10,10)
yi = np.linspace(1,10,20)
xo = np.linspace(1,10,20)
yo = np.linspace(1,10,40)
fi = np.linspace(1, 200, 200).reshape((10, 20))

print(fi)

fo = dlinint2(xi, yi, fi, xo, yo)

print(fo)