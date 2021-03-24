:mod:`geocat.f2py.rcm2points_wrapper`
=====================================

.. py:module:: geocat.f2py.rcm2points_wrapper


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   geocat.f2py.rcm2points_wrapper._rcm2points
   geocat.f2py.rcm2points_wrapper.rcm2points


.. function:: _rcm2points(lat2d, lon2d, fi, lat1d, lon1d, msg_py, opt, shape)


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


