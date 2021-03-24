:mod:`geocat.f2py.triple_to_grid_wrapper`
=========================================

.. py:module:: geocat.f2py.triple_to_grid_wrapper


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   geocat.f2py.triple_to_grid_wrapper._grid_to_triple
   geocat.f2py.triple_to_grid_wrapper._triple_to_grid
   geocat.f2py.triple_to_grid_wrapper._triple_to_grid_2d
   geocat.f2py.triple_to_grid_wrapper.grid_to_triple
   geocat.f2py.triple_to_grid_wrapper.triple_to_grid
   geocat.f2py.triple_to_grid_wrapper.triple_to_grid_2d
   geocat.f2py.triple_to_grid_wrapper.grid2triple
   geocat.f2py.triple_to_grid_wrapper.triple2grid


.. function:: _grid_to_triple(x, y, z, msg_py)


.. function:: _triple_to_grid(data, x_in, y_in, x_out, y_out, shape, method=None, distmx=None, domain=None, msg_py=None)


.. function:: _triple_to_grid_2d(x_in, y_in, data, x_out, y_out, msg_py)


.. function:: grid_to_triple(data, x_in=None, y_in=None, msg_py=None)

   Converts a two-dimensional grid with one-dimensional coordinate variables
   to an array where each grid value is associated with its coordinates.

   :param data: Two-dimensional array of size ny x mx containing the data values.
                Missing values may be present in `data`, but they are ignored.
   :type data: :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param x_in: Coordinates associated with the right dimension of the variable `data`.
                If `data` is of type :class:`xarray.DataArray` and `x_in` is unspecified,
                then it comes as the associated coordinate of `data` (if `x_in` is explicitly
                given, then it will be used for calculations). If `data` is of type
                :class:`numpy.ndarray`, then it must be explicitly given as input and it
                must have the same dimension (call it `mx`) as the right dimension of `data`.
   :type x_in: :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param y_in: Coordinates associated with the left dimension of the variable `data`.
                If `data` is of type :class:`xarray.DataArray` and `y_in` is unspecified,
                then it comes as the associated coordinate of `data` (if `y_in` is explicitly
                given, then it will be used for calculations). If `data` is of type
                :class:`numpy.ndarray`, then it must be explicitly given as input and it
                must have the same dimension (call it `ny`) as the left dimension of `data`.
   :type y_in: :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param msg_py: A numpy scalar value that represent a missing value in `data`.
                  This argument allows a user to use a missing value scheme
                  other than NaN or masked arrays, similar to what NCL allows.
   :type msg_py: :obj:`numpy.number`:

   :returns: **out** -- The maximum size of the returned array will be 3 x ld, where ld <= ny x mx.
             If no missing values are encountered in `data`, then ld = ny x mx. If missing
             values are encountered in `data`, they are not returned and hence ld will be
             equal to ny x mx minus the number of missing values found in `data`.
             The return array will be double if any of the input arrays are double, and float
             otherwise.
   :rtype: :class:`xarray.DataArray`:

   .. admonition:: Examples

      Example 1: Using grid_to_triple with :class:`xarray.DataArray` input

      .. code-block:: python

          import numpy as np
          import xarray as xr
          import geocat.comp

          # Open a netCDF data file using xarray default engine and load the data stream
          ds = xr.open_dataset("./NETCDF_FILE.nc")

          # [INPUT] Grid & data info on the source curvilinear
          data = ds.DIST_236_CBL[:]
          x_in = ds.gridlat_236[:]
          y_in = ds.gridlon_236[:]

          output = geocat.comp.grid_to_triple(data, x_in, y_in)


.. function:: triple_to_grid(data, x_in, y_in, x_out, y_out, method=1, domain=float(1.0), distmx=None, missing_value=np.nan, meta=False)

   Places unstructured (randomly-spaced) data onto the nearest locations of a rectilinear grid.

   :param data: A multi-dimensional array, whose rightmost dimension is the same
                length as `x_in` and `y_in`, containing the values associated with
                the "x" and "y" coordinates. Missing values may be present but
                will be ignored.
   :type data: :class:`xarray.DataArray`: or :class:`numpy.ndarray`:
   :param x_in: One-dimensional arrays of the same length containing the coordinates
                associated with the data values. For geophysical variables, "x"
                correspond to longitude.
   :type x_in: :class:`xarray.DataArray`: or :class:`numpy.ndarray`:
   :param y_in: One-dimensional arrays of the same length containing the coordinates
                associated with the data values. For geophysical variables, "y"
                correspond to latitude.
   :type y_in: :class:`xarray.DataArray`: or :class:`numpy.ndarray`:
   :param x_out: A one-dimensional array of length M containing the "x" coordinates
                 associated with the returned two-grid. For geophysical variables,
                 these are longitudes. The coordinates' values must be
                 monotonically increasing.
   :type x_out: :class:`xarray.DataArray`: or :class:`numpy.ndarray`:
   :param y_out: A one-dimensional array of length N containing the "y" coordinates
                 associated with the returned grid. For geophysical ~variables,
                 these are latitudes. The coordinates' values must be
                 monotonically increasing.
   :type y_out: :class:`xarray.DataArray`: or :class:`numpy.ndarray`:
   :param Optional Parameters:
   :param -------------------:
   :param method: An integer value that can be 0 or 1. The default value is 1.
                  A value of 1 means to use the great circle distance formula
                  for distance calculations.
                  Warning: `method` = 0, together with `domain` = 1.0, could
                  result in many of the target grid points to be set to the
                  missing value if the number of grid points is large (ie: a
                  high resolution grid) and the number of observations
                  relatively small.
   :param domain: A float value that should be set to a value >= 0. The
                  default value is 1.0. If present, the larger this factor,
                  the wider the spatial domain allowed to influence grid boundary
                  points. Typically, `domain` is 1.0 or 2.0. If `domain` <= 0.0,
                  then values located outside the grid domain specified by
                  `x_out` and `y_out` arguments will not be used.
   :param distmx: Setting `distmx` allows the user to specify a search
                  radius (km) beyond which observations are not considered
                  for nearest neighbor. Only applicable when `method` = 1.
                  The default `distmx`=1e20 (km) means that every grid point
                  will have a nearest neighbor. It is suggested that users
                  specify a reasonable value for `distmx`.
   :param missing_value: A numpy scalar value that represent
                         a missing value in `data`. The default value is `np.nan`.
                         If specified explicitly, this argument allows the user to
                         use a missing value scheme other than NaN or masked arrays.
   :type missing_value: :obj:`numpy.number`:
   :param meta: If set to True and the input array is an Xarray,
                the metadata from the input array will be copied to the
                output array; default is False.
                Warning: This option is not yet supported for this function.
   :type meta: :obj:`bool`:

   :returns: * **grid** (:class:`xarray.DataArray`:) -- The returned array will be K x N x M, where K
               represents the leftmost dimensions of `data`, N represent the size of `y_out`,
               and M represent the size of `x_out` coordinate vectors. It will be of type
               double if any of the input is double, and float otherwise.
             * *Description*
             * *-----------* -- This function puts unstructured data (randomly-spaced) onto the nearest
               locations of a rectilinear grid. A default value of `domain` option is
               now set to 1.0 instead of 0.0.

               This function does not perform interpolation; rather, each individual
               data point is assigned to the nearest grid point. It is possible that
               upon return, grid will contain grid points set to missing value if
               no `x_in(n)`, `y_in(n)` are nearby.

   .. admonition:: Examples

      Example 1: Using triple_to_grid with :class:`xarray.DataArray` input

      .. code-block:: python

          import numpy as np
          import xarray as xr
          import geocat.comp

          # Open a netCDF data file using xarray default engine and load the data stream
          ds = xr.open_dataset("./ruc.nc")

          # [INPUT] Grid & data info on the source curvilinear
          data = ds.DIST_236_CBL[:]
          x_in = ds.gridlat_236[:]
          y_in = ds.gridlon_236[:]
          x_out = ds.gridlat_236[:]
          y_out = ds.gridlon_236[:]

       # [OUTPUT] Grid on destination points grid (or read the 1D lat and lon from
       #              an other .nc file.
       newlat1D_points=np.linspace(lat2D_curv.min(), lat2D_curv.max(), 100)
       newlon1D_points=np.linspace(lon2D_curv.min(), lon2D_curv.max(), 100)

       output = geocat.comp.triple_to_grid(data, x_out, y_out, x_in, y_in)


.. function:: triple_to_grid_2d(x_in, y_in, data, x_out, y_out, msg_py)


.. function:: grid2triple(x_in, y_in, data, msg_py)


.. function:: triple2grid(x_in, y_in, data, x_out, y_out, **kwargs)


