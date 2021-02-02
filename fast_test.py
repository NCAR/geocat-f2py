# THIS IS A DEVELOPMENT PERFORMANCE TESTING CLASS, REMOVE WHEN NO LONGER NEEDED

import time
import dask
import dask.distributed as dd
from dask.array.core import map_blocks
import numpy as np
import xarray as xr
from geocat.f2py import (eof11, drveof, deofts7)


def full_test():
    x = np.random.random((1000,1000))
    d = drveof(x)
    # print(d[2])
    nmodes = 10
    return eof11(d[1], nmodes)





if __name__ == '__main__':
    cluster = dd.LocalCluster(n_workers=8, threads_per_worker=1)
    client = dd.Client(cluster)

    print(cluster.dashboard_link)

    t0 = time.time()
    fo = full_test()
    print(fo)
    t1 = time.time()
    print(t1 - t0)
    client.close()
