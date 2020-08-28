from linint2 import (dlinint1, dlinint2, dlinint2pts)
import numpy as np

n = 127

xi = np.linspace(1,10,11)
yi = np.linspace(1,10,11)
xo = np.linspace(1,10,22)
yo = np.linspace(1,10,22)
fi_np = np.random.rand(len(yi), len(xi)).astype(np.float64)



fo = dlinint2(xi,yi,fi_np,xo,yo)

print(fo)