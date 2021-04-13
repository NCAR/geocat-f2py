| CI           | [![GitHub Workflow Status][github-ci-badge]][github-ci-link] [![GitHub Workflow Status][github-conda-build-badge]][github-conda-build-link] [![Code Coverage Status][codecov-badge]][codecov-link] |
| :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| **Docs**     |                                                                    [![Documentation Status][rtd-badge]][rtd-link]                                                                    |
| **Package**  |                                                         [![Conda][conda-badge]][conda-link] [![PyPI][pypi-badge]][pypi-link]                                                         |
| **License**  |                                                                        [![License][license-badge]][repo-link]                                                                        |
| **Citing**   |                                                                             [![DOI][doi-badge]][doi-link]                                                                            |


GeoCAT-comp is both the whole computational component of the [GeoCAT](https://geocat.ucar.edu/)
project and a single Github repository as described in [GeoCAT-comp](https://github.com/NCAR/geocat-comp).
As the computational component of [GeoCAT](https://geocat.ucar.edu/), GeoCAT-comp provides implementations of
computational functions for operating on geosciences data. Many of these functions originated in NCL are pivoted into
Python with the help of GeoCAT-comp; however, developers are welcome to come up with novel computational functions
for geosciences data.

Many of the computational functions in GeoCAT are implemented in a pure Python fashion. However,
there are some others that are implemented in Fortran but wrapped up in Python. To facilitate
contribution, the whole GeoCAT-comp structure is split into two repositories with respect to
being pure-Python or Python with compiled codes (i.e. Fortran) implementations. While pure Python
implementation as well as user API are implemented within
[GeoCAT-comp](https://github.com/NCAR/geocat-comp), Python codes that calls the Fortran functionality
with the help of [Numpy's f2py](https://numpy.org/doc/stable/f2py/) are handled within GeoCAT-f2py
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

# Citing GeoCAT-f2py

NOTE: If you used GeoCAT-f2py through GeoCAT-comp, it is recommended that you cite GeoCAT-comp. Please
refer to [GeoCAT-comp README](https://github.com/NCAR/geocat-comp#readme) for that purpose or
[GeoCAT Citation page](https://geocat.ucar.edu/pages/citation.html) for general information about
citing GeoCAT software packages.

Hiwever, if you used GeoCAT-f2py as a standalomne software tool, cite GeoCAT-f2py using the following
text:

<> Visualization & Analysis Systems Technologies. (Year).
Geoscience Community Analysis Toolkit (GeoCAT-f2py version \<version\>) [Software].
Boulder, CO: UCAR/NCAR - Computational and Informational System Lab. doi:10.5065/A8PP-4358.

Update the GeoCAT-f2py version and year as appropriate. For example:

<> Visualization & Analysis Systems Technologies. (2021).
Geoscience Community Analysis Toolkit (GeoCAT-f2py version 2021.04.0) [Software].
Boulder, CO: UCAR/NCAR - Computational and Informational System Lab. doi:10.5065/A8PP-4358.

For further information, please refer to
[GeoCAT homepage - Citation](https://geocat.ucar.edu/pages/citation.html).





[github-ci-badge]: https://img.shields.io/github/workflow/status/NCAR/geocat-f2py/CI?label=CI&logo=github&style=for-the-badge
[github-conda-build-badge]: https://img.shields.io/github/workflow/status/NCAR/geocat-f2py/build_test?label=conda-builds&logo=github&style=for-the-badge
[github-ci-link]: https://github.com/NCAR/geocat-f2py/actions?query=workflow%3ACI
[github-conda-build-link]: https://github.com/NCAR/geocat-f2py/actions?query=workflow%3Abuild_test
[codecov-badge]: https://img.shields.io/codecov/c/github/NCAR/geocat-f2py.svg?logo=codecov&style=for-the-badge
[codecov-link]: https://codecov.io/gh/NCAR/geocat-f2py
[rtd-badge]: https://img.shields.io/readthedocs/geocat-f2py/latest.svg?style=for-the-badge
[rtd-link]: https://geocat-f2py.readthedocs.io/en/latest/?badge=latest
[pypi-badge]: https://img.shields.io/pypi/v/geocat-f2py?logo=pypi&style=for-the-badge
[pypi-link]: https://pypi.org/project/geocat-f2py
[conda-badge]: https://img.shields.io/conda/vn/ncar/geocat-f2py?logo=anaconda&style=for-the-badge
[conda-link]: https://anaconda.org/ncar/geocat-f2py
[license-badge]: https://img.shields.io/github/license/NCAR/geocat-f2py?style=for-the-badge
[doi-badge]: https://img.shields.io/badge/DOI-10.5065%2Fa8pp--4358-brightgreen?style=for-the-badge
[doi-link]: https://doi.org/10.5065/a8pp-4358
[repo-link]: https://github.com/NCAR/geocat-f2py
