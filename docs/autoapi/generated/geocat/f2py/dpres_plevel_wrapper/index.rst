:mod:`geocat.f2py.dpres_plevel_wrapper`
=======================================

.. py:module:: geocat.f2py.dpres_plevel_wrapper


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   geocat.f2py.dpres_plevel_wrapper.dpres_plevel
   geocat.f2py.dpres_plevel_wrapper._dpres_plevel
   geocat.f2py.dpres_plevel_wrapper._sanity_check


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


.. function:: _dpres_plevel(plev, psfc, ptop, msg_py)


.. function:: _sanity_check(pressure_levels, pressure_surface, pressure_top)


