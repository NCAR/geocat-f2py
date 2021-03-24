:mod:`geocat.f2py.errors`
=========================

.. py:module:: geocat.f2py.errors


Module Contents
---------------

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


