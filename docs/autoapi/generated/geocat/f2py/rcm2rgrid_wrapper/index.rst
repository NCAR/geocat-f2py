:mod:`geocat.f2py.rcm2rgrid_wrapper`
====================================

.. py:module:: geocat.f2py.rcm2rgrid_wrapper


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   geocat.f2py.rcm2rgrid_wrapper._rcm2rgrid
   geocat.f2py.rcm2rgrid_wrapper._rgrid2rcm
   geocat.f2py.rcm2rgrid_wrapper.rcm2rgrid
   geocat.f2py.rcm2rgrid_wrapper.rgrid2rcm


.. function:: _rcm2rgrid(lat2d, lon2d, fi, lat1d, lon1d, msg_py, shape)


.. function:: _rgrid2rcm(lat1d, lon1d, fi, lat2d, lon2d, msg_py, shape)


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


