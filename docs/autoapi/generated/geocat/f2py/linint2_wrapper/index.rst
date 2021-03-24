:mod:`geocat.f2py.linint2_wrapper`
==================================

.. py:module:: geocat.f2py.linint2_wrapper


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   geocat.f2py.linint2_wrapper._linint1
   geocat.f2py.linint2_wrapper._linint2
   geocat.f2py.linint2_wrapper._linint2pts
   geocat.f2py.linint2_wrapper.linint1
   geocat.f2py.linint2_wrapper.linint2
   geocat.f2py.linint2_wrapper.linint2pts
   geocat.f2py.linint2_wrapper.linint2_points


.. function:: _linint1(xi, fi, xo, icycx, msg_py, shape)


.. function:: _linint2(xi, yi, fi, xo, yo, icycx, msg_py, shape)


.. function:: _linint2pts(xi, yi, fi, xo, yo, icycx, msg_py, shape)


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


