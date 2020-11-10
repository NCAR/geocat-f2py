![actions](https://github.com/NCAR/geocat-f2py/workflows/actions/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/geocat-f2py/badge/?version=latest)](https://geocat-f2py.readthedocs.io/en/latest/?badge=latest)


GeoCAT-comp is both the whole computational component of the [GeoCAT](https://ncar.github.io/GeoCAT) 
project and a single Github repository as described in [GeoCAT-comp](https://github.com/NCAR/geocat-comp). 
As the computational component of [GeoCAT](https://ncar.github.io/GeoCAT), GeoCAT-comp provides implementations of 
computational functions for operating on geosciences data. Many of these functions originated in NCL are pivoted into 
Python with the help of GeoCAT-comp; however, developers are welcome to come up with novel computational functions 
for geosciences data.

Many of the computational functions under GeoCAT-comp are implemented in Fortran 
(or possibly C). However, others can be implemented in a pure Python fashion. To facilitate 
contribution, the whole GeoCAT-comp computational component is split into Github repositories with respect to 
being based on either pure-Python or Python with compiled code dependencies (i.e. Fortran). While pure Python 
implementation as well as user API are implemented within [GeoCAT-comp](https://github.com/NCAR/geocat-comp), 
Python codes that calls the Fortran functionality with the help of Numpy.f2py are handled within GeoCAT-f2py 
(i.e. this repository).


# GeoCAT-f2py

GeoCAT-f2py wraps, in Python, the compiled language implementations of some of the computational functions 
found under the [GeoCAT-comp](https://github.com/NCAR/geocat-comp) umbrella. The compiled language functions 
contained in GeoCAT-f2py (i.e. this repository) as Fortran subroutines are wrapped up in corresponding 
Python wrapper files in the same repository with the help of Numpy.f2py's signature files (.pyf). 

Not all computational functions in GeoCAT computational component have compiled language implementations; 
therefore, developers basing their implementations entirely in Python need not concern themselves with this repo; 
instead, they should engage with [GeoCAT-comp](https://github.com/NCAR/geocat-comp) repo as it invisibly 
imports [GeoCAT-f2py](https://github.com/NCAR/geocat-f2py). However, for those functions that are implemented 
in Fortran, this repo provides a Python interface to those functions via a Numpy.f2py wrapper.


# Documentation

[GeoCAT Homepage](https://geocat.ucar.edu/)

[GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html)

[GeoCAT-comp documentation on Read the Docs](https://geocat-comp.readthedocs.io)


# Installation and build instructions

Please see our documentation for 
[installation and build instructions](https://github.com/NCAR/geocat-f2py/blob/master/INSTALLATION.md).


# Xarray interface vs NumPy interface

GeoCAT-f2py provides a high-level [Xarray](http://xarray.pydata.org/en/stable/) interface under the 
`geocat.f2py` namespace. However, a stripped-down NumPy interface is used under the hood to bridge 
the gap between NumPy arrays and the compiled language data structures. These functions are 
accessible under the `geocat.comp.f2py` namespace, but are minimally documented and are 
intended primarily for internal use.
