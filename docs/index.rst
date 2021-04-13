.. GeoCAT-f2py documentation master file, created by
   sphinx-quickstart on Thu Feb 25 09:38:11 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GeoCAT-f2py
===========

GeoCAT-f2py wraps, in Python, the compiled language implementations of some of the
computational functions found under the
`GeoCAT-comp <https://geocat-comp.readthedocs.io/en/latest/>`_ umbrella.

GeoCAT-comp is the computational component of the `GeoCAT <https://geocat.ucar.edu/>`_
project. GeoCAT-comp provides implementations of computational functions for operating
on geosciences data. Many of these functions originated in NCL and were translated into
Python with the help of GeoCAT-comp; however, developers are welcome to come up with
novel computational functions for geosciences data.

Many of the computational functions in
`GeoCAT-comp <https://geocat-comp.readthedocs.io/en/latest/>`_ are implemented in a pure
Python fashion. However, there are some others that are implemented in Fortran but wrapped
up in Python. Python codes that calls the Fortran functionality with the help of
`Numpy's f2py <https://numpy.org/doc/stable/f2py/>`_ are handled within GeoCAT-f2py.
Therefore, the end users of `GeoCAT-comp <https://geocat-comp.readthedocs.io/en/latest/>`_
and/or developers basing their implementations entirely in Python need not concern
themselves with GeoCAT-f2py.


.. toctree::
   :maxdepth: 2

   ./installation
   ./api
   ./examples
   ./citation
   ./support



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


--------------------

*The National Center for Atmospheric Research is sponsored by the National
Science Foundation. Any opinions, findings and conclusions or recommendations
expressed in this material do not necessarily reflect the views of the
National Science Foundation.*
