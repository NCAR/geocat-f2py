:mod:`geocat.f2py`
==================

.. py:module:: geocat.f2py


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   fortran/index.rst


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   dpres_plevel_wrapper/index.rst
   errors/index.rst
   linint2_wrapper/index.rst
   missing_values/index.rst
   moc_globe_atl_wrapper/index.rst
   rcm2points_wrapper/index.rst
   rcm2rgrid_wrapper/index.rst
   triple_to_grid_wrapper/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   geocat.f2py.dpres_plevel
   geocat.f2py.linint1
   geocat.f2py.linint2
   geocat.f2py.linint2pts
   geocat.f2py.linint2_points
   geocat.f2py.py2fort_msg
   geocat.f2py.fort2py_msg
   geocat.f2py.moc_globe_atl
   geocat.f2py.rcm2points
   geocat.f2py.rcm2rgrid
   geocat.f2py.rgrid2rcm
   geocat.f2py.grid_to_triple
   geocat.f2py.triple_to_grid
   geocat.f2py.grid2triple
   geocat.f2py.triple2grid


.. function:: dpres_plevel(pressure_levels, pressure_surface, pressure_top=None, msg_py=None, meta=False)

   Calculates the pressure layer thicknesses of a constant pressure level coordinate system.

   :param pressure_levels: A one dimensional array containing the constant pressure levels. May be
                           in ascending or descending order. Must have the same units as `pressure_surface`.
   :type pressure_levels: :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param pressure_surface: A scalar or an array of up to three dimensions containing the surface
                            pressure data in Pa or hPa (mb). The rightmost dimensions must be latitude
                            and longitude. Must have the same units as `pressure_levels`.
   :type pressure_surface: :obj:`numpy.number` or :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param pressure_top: A scalar specifying the top of the column. pressure_top should be <= min(pressure_levels).
                        Must have the same units as `pressure_levels`.
   :type pressure_top: :class:`numpy.number`:
   :param msg_py: A numpy scalar value that represent a missing value in fi.
                  This argument allows a user to use a missing value scheme
                  other than NaN or masked arrays, similar to what NCL allows.
   :type msg_py: :obj:`numpy.number`:
   :param meta: If set to True and the input arrays (pressure_levels and pressure_surface) are Xarray,
                the metadata from the input arrays will be copied to the output array; default is False.
                WARNING: This option is not currently supported. Though, even if it is false,
                Xarray.Dataarray.attrs of `pressure_surface` is being retained in the output.
   :type meta: :obj:`bool`:

   :returns: * **dp** (:class:`xarray.DataArray`:) -- If pressure_surface is a scalar, the return variable will be a
               one-dimensional array the same size as `pressure_levels`; if `pressure_surface`
               is two-dimensional [e.g. (lat,lon)] or three-dimensional [e.g. (time,lat,lon)],
               then the return array will have an additional level dimension: (lev,lat,lon)
               or (time,lev,lat,lon). The returned type will be double
               if `pressure_surface` is double, float otherwise.
             * *Description*
             * *-----------* -- Calculates the layer pressure thickness of a constant pressure level system. It
               is analogous to `dpres_hybrid_ccm` for hybrid coordinates. At each grid point the
               sum of the pressure thicknesses equates to [pressure_surface - pressure_top]. At each
               grid point, the returned values above `pressure_top` and below `pressure_surface` will
               be set to the missing value of `pressure_surface`. If there is no missing value
               for `pressure_surface` then the missing value will be set to the default for
               float or double appropriately. If `pressure_top` or `pressure_surface` is between
               pressure_levels levels then the layer thickness is modifed accordingly.
               If `pressure_surface` is set to a missing value, all layer thicknesses
               are set to the appropriate missing value.

               The primary purpose of this function is to return layer thicknesses to be used to
               weight observations for integrations.

   .. admonition:: Examples

      Example 1: Using dpres_plevel with :class:`xarray.DataArray` input

      .. code-block:: python

          import numpy as np
          import xarray as xr
          import geocat.comp

          # Open a netCDF data file using xarray default engine and load the data stream
          ds = xr.open_dataset("./SOME_NETCDF_FILE.nc")

          # [INPUT] Grid & data info on the source
          pressure_surface = ds.PS
          pressure_levels = ds.LEV
          pressure_top = 0.0

          # Call the function
          result_dp = geocat.comp.dpres_plevel(pressure_levels, pressure_surface, pressure_top)


.. py:exception:: Error

   Bases: :class:`Exception`

   Base class for exceptions in this module.


.. py:exception:: AttributeError

   Bases: :class:`geocat.f2py.errors.Error`

   Exception raised when the arguments of GeoCAT-comp functions argument
   has a mismatch of attributes with other arguments.


.. py:exception:: ChunkError

   Bases: :class:`geocat.f2py.errors.Error`

   Exception raised when a Dask array is chunked in a way that is
   incompatible with an _ncomp function.


.. py:exception:: CoordinateError

   Bases: :class:`geocat.f2py.errors.Error`

   Exception raised when a GeoCAT-comp function is passed a NumPy array as
   an argument without a required coordinate array being passed separately.


.. py:exception:: DimensionError

   Bases: :class:`geocat.f2py.errors.Error`

   Exception raised when the arguments of GeoCAT-comp functions argument
   has a mismatch of the necessary dimensionality.


.. py:exception:: MetaError

   Bases: :class:`geocat.f2py.errors.Error`

   Exception raised when the support for the retention of metadata is not
   supported.


.. function:: linint1(fi, xo, xi=None, icycx=0, msg_py=None)


.. function:: linint2(fi, xo, yo, xi=None, yi=None, icycx=0, msg_py=None)

   Interpolates a regular grid to a rectilinear one using bi-linear
   interpolation.

   linint2 uses bilinear interpolation to interpolate from one
   rectilinear grid to another. The input grid may be cyclic in the x
   direction. The interpolation is first performed in the x direction,
   and then in the y direction.

   :param fi: An array of two or more dimensions. If xi is passed in as an
              argument, then the size of the rightmost dimension of fi
              must match the rightmost dimension of xi. Similarly, if yi
              is passed in as an argument, then the size of the second-
              rightmost dimension of fi must match the rightmost dimension
              of yi.

              If missing values are present, then linint2 will perform the
              bilinear interpolation at all points possible, but will
              return missing values at coordinates which could not be
              used.

              Note:

                  This variable must be
                  supplied as a :class:`xarray.DataArray` in order to copy
                  the dimension names to the output. Otherwise, default
                  names will be used.
   :type fi: :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param xo: A one-dimensional array that specifies the X coordinates of
              the return array. It must be strictly monotonically
              increasing, but may be unequally spaced.

              For geo-referenced data, xo is generally the longitude
              array.

              If the output coordinates (xo) are outside those of the
              input coordinates (xi), then the fo values at those
              coordinates will be set to missing (i.e. no extrapolation is
              performed).
   :type xo: :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param yo: A one-dimensional array that specifies the Y coordinates of
              the return array. It must be strictly monotonically
              increasing, but may be unequally spaced.

              For geo-referenced data, yo is generally the latitude array.

              If the output coordinates (yo) are outside those of the
              input coordinates (yi), then the fo values at those
              coordinates will be set to missing (i.e. no extrapolation is
              performed).
   :type yo: :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param xi (:class:`numpy.ndarray`): An array that specifies the X coordinates of the fi array.
                                       Most frequently, this is a 1D strictly monotonically
                                       increasing array that may be unequally spaced. In some
                                       cases, xi can be a multi-dimensional array (see next
                                       paragraph). The rightmost dimension (call it nxi) must have
                                       at least two elements, and is the last (fastest varying)
                                       dimension of fi.

                                       If xi is a multi-dimensional array, then each nxi subsection
                                       of xi must be strictly monotonically increasing, but may be
                                       unequally spaced. All but its rightmost dimension must be
                                       the same size as all but fi's rightmost two dimensions.

                                       For geo-referenced data, xi is generally the longitude
                                       array.

                                       Note:
                                           If fi is of type :class:`xarray.DataArray` and xi is
                                           left unspecified, then the rightmost coordinate
                                           dimension of fi will be used. If fi is not of type
                                           :class:`xarray.DataArray`, then xi becomes a mandatory
                                           parameter. This parameter must be specified as a keyword
                                           argument.
   :param yi (:class:`numpy.ndarray`): An array that specifies the Y coordinates of the fi array.
                                       Most frequently, this is a 1D strictly monotonically
                                       increasing array that may be unequally spaced. In some
                                       cases, yi can be a multi-dimensional array (see next
                                       paragraph). The rightmost dimension (call it nyi) must have
                                       at least two elements, and is the second-to-last dimension
                                       of fi.

                                       If yi is a multi-dimensional array, then each nyi subsection
                                       of yi must be strictly monotonically increasing, but may be
                                       unequally spaced. All but its rightmost dimension must be
                                       the same size as all but fi's rightmost two dimensions.

                                       For geo-referenced data, yi is generally the latitude array.

                                       Note:
                                           If fi is of type :class:`xarray.DataArray` and xi is
                                           left unspecified, then the second-to-rightmost
                                           coordinate dimension of fi will be used. If fi is not of
                                           type :class:`xarray.DataArray`, then xi becomes a
                                           mandatory parameter. This parameter must be specified as
                                           a keyword argument.
   :param icycx: An option to indicate whether the rightmost dimension of fi
                 is cyclic. This should be set to True only if you have
                 global data, but your longitude values don't quite wrap all
                 the way around the globe. For example, if your longitude
                 values go from, say, -179.75 to 179.75, or 0.5 to 359.5,
                 then you would set this to True.
   :type icycx: :obj:`bool`:
   :param msg_py: A numpy scalar value that represent a missing value in fi.
                  This argument allows a user to use a missing value scheme
                  other than NaN or masked arrays, similar to what NCL allows.
   :type msg_py: :obj:`numpy.number`:

   :returns: **fo** -- The interpolated grid. If the *meta*
             parameter is True, then the result will include named dimensions
             matching the input array. The returned value will have the same
             dimensions as fi, except for the rightmost two dimensions which
             will have the same dimension sizes as the lengths of yo and xo.
             The return type will be double if fi is double, and float
             otherwise.
   :rtype: :class:`xarray.DataArray`:

   .. admonition:: Examples

      Example 1: Using linint2 with :class:`xarray.DataArray` input

      .. code-block:: python

          import numpy as np
          import xarray as xr
          import geocat.comp

          fi_np = np.random.rand(30, 80)  # random 30x80 array

          # xi and yi do not have to be equally spaced, but they are
          # in this example
          xi = np.arange(80)
          yi = np.arange(30)

          # create target coordinate arrays, in this case use the same
          # min/max values as xi and yi, but with different spacing
          xo = np.linspace(xi.min(), xi.max(), 100)
          yo = np.linspace(yi.min(), yi.max(), 50)

          # create :class:`xarray.DataArray` and chunk it using the
          # full shape of the original array.
          # note that xi and yi are attached as coordinate arrays
          fi = xr.DataArray(fi_np,
                            dims=['lat', 'lon'],
                            coords={'lat': yi, 'lon': xi}
                           ).chunk(fi_np.shape)

          fo = geocat.comp.linint2(fi, xo, yo, icycx=0)


.. function:: linint2pts(fi, xo, yo, icycx=False, msg_py=None, xi=None, yi=None)

   Interpolates from a rectilinear grid to an unstructured grid or locations using bilinear interpolation.

   :param fi: An array of two or more dimensions. The two rightmost
              dimensions (nyi x nxi) are the dimensions to be used in
              the interpolation. If user-defined missing values are
              present (other than NaNs), the value of `msg_py` must be
              set appropriately.
   :type fi: :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param xo: A one-dimensional array that specifies the X (longitude)
              coordinates of the unstructured grid.
   :type xo: :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param yo: A one-dimensional array that specifies the Y (latitude)
              coordinates of the unstructured grid. It must be the same
              length as `xo`.
   :type yo: :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param icycx: An option to indicate whether the rightmost dimension of fi
                 is cyclic. Default valus is 0. This should be set to True
                 only if you have global data, but your longitude values
                 don't quite wrap all the way around the globe. For example,
                 if your longitude values go from, say, -179.75 to 179.75,
                 or 0.5 to 359.5, then you would set this to True.
   :type icycx: :obj:`bool`:
   :param msg_py: A numpy scalar value that represent a missing value in fi.
                  This argument allows a user to use a missing value scheme
                  other than NaN or masked arrays, similar to what NCL allows.
   :type msg_py: :obj:`numpy.number`:
   :param xi: A strictly monotonically increasing array that specifies
              the X [longitude] coordinates of the `fi` array. `xi` might
              be defined as the coordinates of `fi` when `fi` is of type
              `xarray.DataArray`; in this case `xi` may not be explicitly
              given as a function argument.
   :type xi: :class:`xarray.DataArray` or :class:`numpy.ndarray`:
   :param yi: A strictly monotonically increasing array that specifies
              the Y [latitude] coordinates of the `fi` array. ``yi` might
              be defined as the coordinates of `fi` when `fi` is of type
              `xarray.DataArray`; in this case `yi` may not be explicitly
              given as a function argument.
   :type yi: :class:`xarray.DataArray` or :class:`numpy.ndarray`:

   :returns: * **fo** (:class:`numpy.ndarray`:) -- The returned value will have the same dimensions as `fi`,
               except for the rightmost dimension which will have the same
               dimension size as the length of `yo` and `xo`. The return
               type will be double if `fi` is double, and float otherwise.
             * *Description*
             * *-----------* -- The `linint2pts` function uses bilinear interpolation to interpolate
               from a rectilinear grid to an unstructured grid.

               If missing values are present, then `linint2pts` will perform the
               piecewise linear interpolation at all points possible, but will return
               missing values at coordinates which could not be used. If one or more
               of the four closest grid points to a particular (xo, yo) coordinate
               pair are missing, then the return value for this coordinate pair will
               be missing.

               If the user inadvertently specifies output coordinates (xo, yo) that
               are outside those of the input coordinates (xi, yi), the output value
               at this coordinate pair will be set to missing as no extrapolation
               is performed.

               `linint2pts` is different from `linint2` in that `xo` and `yo` are
               coordinate pairs, and need not be monotonically increasing. It is
               also different in the dimensioning of the return array.

               This function could be used if the user wanted to interpolate gridded
               data to, say, the location of rawinsonde sites or buoy/xbt locations.

               Warning: if `xi` contains longitudes, then the `xo` values must be in the
               same range. In addition, if the `xi` values span 0 to 360, then the `xo`
               values must also be specified in this range (i.e. -180 to 180 will not work).

   .. admonition:: Examples

      Example 1: Using linint2pts with :class:`xarray.DataArray` input

          .. code-block:: python

          import numpy as np
          import xarray as xr
          import geocat.comp

          fi_np = np.random.rand(30, 80)  # random 30x80 array

          # xi and yi do not have to be equally spaced, but they are
          # in this example
          xi = np.arange(80)
          yi = np.arange(30)

          # create target coordinate arrays, in this case use the same
          # min/max values as xi and yi, but with different spacing
          xo = np.linspace(xi.min(), xi.max(), 100)
          yo = np.linspace(yi.min(), yi.max(), 50)

          # create :class:`xarray.DataArray` and chunk it using the
          # full shape of the original array.
          # note that xi and yi are attached as coordinate arrays
          fi = xr.DataArray(fi_np,
                            dims=['lat', 'lon'],
                            coords={'lat': yi, 'lon': xi}
                           ).chunk(fi_np.shape)

          fo = geocat.comp.linint2pts(fi, xo, yo, 0)


.. function:: linint2_points(fi, xo, yo, icycx, msg=None, meta=False, xi=None, yi=None)


.. function:: py2fort_msg(ndarray, msg_py=None, msg_fort=None)


.. function:: fort2py_msg(ndarray, msg_fort=None, msg_py=None)


.. function:: moc_globe_atl(lat_aux_grid, a_wvel, a_bolus, a_submeso, t_lat, rmlak, msg=None, meta=False)

   Facilitates calculating the meridional overturning circulation for the
   globe and Atlantic.

   Args:

   lat_aux_grid : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
       Latitude grid for transport diagnostics.

   a_wvel : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
       Area weighted Eulerian-mean vertical velocity [TAREA*WVEL].

   a_bolus : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
       Area weighted Eddy-induced (bolus) vertical velocity [TAREA*WISOP].

   a_submeso : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
       Area weighted submeso vertical velocity [TAREA*WSUBM].

   tlat : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
       Array of t-grid latitudes.

   rmlak : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
       Basin index number: [0]=Globe, [1]=Atlantic

   msg : :obj:`numpy.number`:
     A numpy scalar value that represent a missing value.
     This argument allows a user to use a missing value scheme
     other than NaN or masked arrays, similar to what NCL allows.

   meta : :obj:`bool`:
       If set to True and the input array is an Xarray, the metadata
       from the input array will be copied to the output array;
       default is False.
       Warning: this option is not currently supported.

   :returns: **fo** -- A multi-dimensional array of size
             [moc_comp] x [n_transport_reg] x [kdepth] x [nyaux] where:

             - moc_comp refers to the three components returned
             - n_transport_reg refers to the Globe and Atlantic
             - kdepth is the the number of vertical levels of the work arrays
             - nyaux is the size of the lat_aux_grid

             The type of the output data will be double only if a_wvel or a_bolus or
             a_submesa is of type double. Otherwise, the return type will be float.
   :rtype: :class:`xarray.DataArray`:

   .. admonition:: Examples

      # Input data can be read from a data set as follows:
      import xarray as xr

      ds = xr.open_dataset("input.nc")

      lat_aux_grid = ds.lat_aux_grid
      a_wvel = ds.a_wvel
      a_bolus = ds.a_bolus
      a_submeso = ds.a_submeso
      tlat = ds.tlat
      rmlak = ds.rmlak

      # (1) Calling with xArray inputs and default arguments (Missing value = np.nan, NO meta information)
      out_arr = moc_globe_atl(lat_aux_grid, a_wvel, a_bolus, a_submeso, tlat, rmlak)

      # (2) Calling with Numpy inputs and default arguments (Missing value = np.nan, NO meta information)
      out_arr = moc_globe_atl(lat_aux_grid.values, a_wvel.values, a_bolus.values, a_submeso.values,
                              tlat.values, rmlak.values)

      # (3) Calling with xArray inputs and user-defined arguments (Missing value = np.nan, NO meta information)
      out_arr = moc_globe_atl(lat_aux_grid, a_wvel, a_bolus, a_submeso, tlat, rmlak, msg=-99.0, meta=True)

      # (4) Calling with Numpy inputs and user-defined arguments (Missing value = np.nan, NO meta information)
      out_arr = moc_globe_atl(lat_aux_grid.values, a_wvel.values, a_bolus.values, a_submeso.values,
                              tlat.values, rmlak.values, msg=-99.0, meta=True)


.. function:: rcm2points(lat2d, lon2d, fi, lat1d, lon1d, opt=0, msg=None, meta=False)

   Interpolates data on a curvilinear grid (i.e. RCM, WRF, NARR) to an unstructured grid.

   Paraemeters
   -----------

   lat2d : :class:`numpy.ndarray`:
           A two-dimensional array that specifies the latitudes locations
           of fi. The latitude order must be south-to-north.

       lon2d : :class:`numpy.ndarray`:
           A two-dimensional array that specifies the longitude locations
           of fi. The latitude order must be west-to-east.

       fi : :class:`numpy.ndarray`:
           A multi-dimensional array to be interpolated. The rightmost two
           dimensions (latitude, longitude) are the dimensions to be interpolated.

       lat1d : :class:`numpy.ndarray`:
           A one-dimensional array that specifies the latitude coordinates of
           the output locations.

       lon1d : :class:`numpy.ndarray`:
           A one-dimensional array that specifies the longitude coordinates of
           the output locations.

       opt : :obj:`numpy.number`:
           opt=0 or 1 means use an inverse distance weight interpolation.
           opt=2 means use a bilinear interpolation.

   msg : :obj:`numpy.number`:
           A numpy scalar value that represent a missing value in fi.
           This argument allows a user to use a missing value scheme
           other than NaN or masked arrays, similar to what NCL allows.

   meta : :obj:`bool`:
       If set to True and the input array is an Xarray, the metadata
       from the input array will be copied to the output array;
       default is False.
       Warning: This option is not currently supported.

   :returns: * **:class:`numpy.ndarray`** (*The interpolated grid. A multi-dimensional array*)
             * *of the same size as fi except that the rightmost dimension sizes have been*
             * *replaced by the number of coordinate pairs (lat1dPoints, lon1dPoints).*
             * *Double if fi is double, otherwise float.*

   Description
   -----------

       Interpolates data on a curvilinear grid, such as those used by the RCM (Regional Climate Model),
       WRF (Weather Research and Forecasting) and NARR (North American Regional Reanalysis)
       models/datasets to an unstructured grid. All of these have latitudes that are oriented south-to-north.
       A inverse distance squared algorithm is used to perform the interpolation.
       Missing values are allowed and no extrapolation is performed.


.. function:: rcm2rgrid(lat2d, lon2d, fi, lat1d, lon1d, msg=None, meta=False)

   Interpolates data on a curvilinear grid (i.e. RCM, WRF, NARR) to a rectilinear grid.

   :param lat2d: A two-dimensional array that specifies the latitudes locations
                 of fi. Because this array is two-dimensional it is not an associated
                 coordinate variable of `fi`. The latitude order must be south-to-north.
   :type lat2d: :class:`numpy.ndarray`:
   :param lon2d: A two-dimensional array that specifies the longitude locations
                 of fi. Because this array is two-dimensional it is not an associated
                 coordinate variable of `fi`. The latitude order must be west-to-east.
   :type lon2d: :class:`numpy.ndarray`:
   :param fi: A multi-dimensional array to be interpolated. The rightmost two
              dimensions (latitude, longitude) are the dimensions to be interpolated.
   :type fi: :class:`numpy.ndarray`:
   :param lat1d: A one-dimensional array that specifies the latitude coordinates of
                 the regular grid. Must be monotonically increasing.
   :type lat1d: :class:`numpy.ndarray`:
   :param lon1d: A one-dimensional array that specifies the longitude coordinates of
                 the regular grid. Must be monotonically increasing.
   :type lon1d: :class:`numpy.ndarray`:
   :param msg: A numpy scalar value that represent a missing value in fi.
               This argument allows a user to use a missing value scheme
               other than NaN or masked arrays, similar to what NCL allows.
   :type msg: :obj:`numpy.number`:
   :param meta: If set to True and the input array is an Xarray, the metadata
                from the input array will be copied to the output array;
                default is False.
                Warning: This option is not currently supported.
   :type meta: :obj:`bool`:

   :returns: * **fo** (:class:`numpy.ndarray`:) -- The interpolated grid. A multi-dimensional array
               of the same size as fi except that the rightmost dimension sizes have been
               replaced by the sizes of lat1d and lon1d respectively.
               Double if fi is double, otherwise float.
             * *Description*
             * *-----------* -- Interpolates RCM (Regional Climate Model), WRF (Weather Research and Forecasting) and
               NARR (North American Regional Reanalysis) grids to a rectilinear grid. Actually, this
               function will interpolate most grids that use curvilinear latitude/longitude grids.
               No extrapolation is performed beyond the range of the input coordinates. Missing values
               are allowed but ignored.

               The weighting method used is simple inverse distance squared. Missing values are allowed
               but ignored.

               The code searches the input curvilinear grid latitudes and longitudes for the four
               grid points that surround a specified output grid coordinate. Because one or more of
               these input points could contain missing values, fewer than four points
               could be used in the interpolation.

               Curvilinear grids which have two-dimensional latitude and longitude coordinate axes present
               some issues because the coordinates are not necessarily monotonically increasing. The simple
               search algorithm used by rcm2rgrid is not capable of handling all cases. The result is that,
               sometimes, there are small gaps in the interpolated grids. Any interior points not
               interpolated in the initial interpolation pass will be filled using linear interpolation.

               In some cases, edge points may not be filled.

   .. admonition:: Examples

      Example 1: Using rcm2rgrid with :class:`xarray.DataArray` input

      .. code-block:: python

          import numpy as np
          import xarray as xr
          import geocat.comp

          # Open a netCDF data file using xarray default engine and load the data stream
          ds = xr.open_dataset("./ruc.nc")

          # [INPUT] Grid & data info on the source curvilinear
          ht_curv=ds.DIST_236_CBL[:]
          lat2D_curv=ds.gridlat_236[:]
          lon2D_curv=ds.gridlon_236[:]

          # [OUTPUT] Grid on destination rectilinear grid (or read the 1D lat and lon from
          #          an other .nc file.
          newlat1D_rect=np.linspace(lat2D_curv.min(), lat2D_curv.max(), 100)
          newlon1D_rect=np.linspace(lon2D_curv.min(), lon2D_curv.max(), 100)

          ht_rect = geocat.comp.rcm2rgrid(lat2D_curv, lon2D_curv, ht_curv, newlat1D_rect, newlon1D_rect)


.. function:: rgrid2rcm(lat1d, lon1d, fi, lat2d, lon2d, msg=None, meta=False)

   Interpolates data on a rectilinear lat/lon grid to a curvilinear grid like
   those used by the RCM, WRF and NARR models/datasets.

   :param lat1d: A one-dimensional array that specifies the latitude coordinates of
                 the regular grid. Must be monotonically increasing.
   :type lat1d: :class:`numpy.ndarray`:
   :param lon1d: A one-dimensional array that specifies the longitude coordinates of
                 the regular grid. Must be monotonically increasing.
   :type lon1d: :class:`numpy.ndarray`:
   :param fi: A multi-dimensional array to be interpolated. The rightmost two
              dimensions (latitude, longitude) are the dimensions to be interpolated.
   :type fi: :class:`numpy.ndarray`:
   :param lat2d: A two-dimensional array that specifies the latitude locations
                 of fi. Because this array is two-dimensional it is not an associated
                 coordinate variable of `fi`.
   :type lat2d: :class:`numpy.ndarray`:
   :param lon2d: A two-dimensional array that specifies the longitude locations
                 of fi. Because this array is two-dimensional it is not an associated
                 coordinate variable of `fi`.
   :type lon2d: :class:`numpy.ndarray`:
   :param msg :obj:`numpy.number`: A numpy scalar value that represent a missing value in fi.
                                   This argument allows a user to use a missing value scheme
                                   other than NaN or masked arrays, similar to what NCL allows.
   :param meta :obj:`bool`: If set to True and the input array is an Xarray, the metadata
                            from the input array will be copied to the output array;
                            default is False.
                            Warning: this option is not currently supported.

   :returns: * **fo** (:class:`numpy.ndarray`: The interpolated grid. A multi-dimensional array of the)
             * same size as `fi` except that the rightmost dimension sizes have been replaced
             * by the sizes of `lat2d` and `lon2d` respectively. Double if `fi` is double,
             * *otherwise float.*
             * *Description*
             * *-----------* -- Interpolates data on a rectilinear lat/lon grid to a curvilinear grid, such as those
             * *used by the RCM (Regional Climate Model), WRF (Weather Research and Forecasting) and*
             * *NARR (North American Regional Reanalysis) models/datasets. No extrapolation is*
             * *performed beyond the range of the input coordinates. The method used is simple inverse*
             * *distance weighting. Missing values are allowed but ignored.*

   .. admonition:: Examples

      Example 1: Using rgrid2rcm with :class:`xarray.DataArray` input

      .. code-block:: python

          import numpy as np
          import xarray as xr
          import geocat.comp

          # Open a netCDF data file using xarray default engine and load the data stream
          # input grid and data
          ds_rect = xr.open_dataset("./DATAFILE_RECT.nc")

          # [INPUT] Grid & data info on the source rectilinear
          ht_rect   =ds_rect.SOME_FIELD[:]
          lat1D_rect=ds_rect.gridlat_[:]
          lon1D_rect=ds_rect.gridlon_[:]

          # Open a netCDF data file using xarray default engine and load the data stream
          # for output grid
          ds_curv = xr.open_dataset("./DATAFILE_CURV.nc")

          # [OUTPUT] Grid on destination curvilinear grid (or read the 2D lat and lon from
          #          an other .nc file
          newlat2D_rect=ds_curv.gridlat2D_[:]
          newlon2D_rect=ds_curv.gridlat2D_[:]

          ht_curv = geocat.comp.rgrid2rcm(lat1D_rect, lon1D_rect, ht_rect, newlat2D_curv, newlon2D_curv)


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


.. function:: grid2triple(x_in, y_in, data, msg_py)


.. function:: triple2grid(x_in, y_in, data, x_out, y_out, **kwargs)


