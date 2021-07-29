# Installation

This installation guide includes only the GeoCAT-f2py installation and build instructions.
Please refer to [GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html) for
installation of the whole GeoCAT project or [GeoCAT-comp](https://github.com/NCAR/geocat-comp) for
that of the overall computational component of the GeoCAT project.


## Installing GeoCAT-f2py via Conda

The easiest way to install GeoCAT-f2py is using [Conda](http://conda.pydata.org/docs/):

    conda create -n geocat -c conda-forge -c ncar geocat-f2py

where "geocat" is the name of a new conda environment, which can then be
activated using:

    conda activate geocat

If you somewhat need to make use of other software packages, such as Matplotlib,
Cartopy, Jupyter, etc. with GeoCAT-f2py, you may wish to install into your `geocat`
environment.  The following `conda create` command can be used to create a new
`conda` environment that includes some of these additional commonly used Python
packages pre-installed:

    conda create -n geocat -c conda-forge -c ncar geocat-f2py matplotlib cartopy jupyter

Alternatively, if you already created a conda environment using the first
command (without the extra packages), you can activate and install the packages
in an existing environment with the following commands:

    conda activate geocat   # or whatever your environment is called
    conda install -c conda-forge matplotlib cartopy jupyter

Please note that the use of the **conda-forge** channel is essential to guarantee
compatibility between dependency packages.

Also, note that the Conda package manager automatically installs all `required`
dependencies of GeoCAT-f2py, meaning it is not necessary to explicitly install
Python, NumPy, Xarray, or Dask when creating an environment and installing GeoCAT-f2py.
Although packages like Matplotlib are often used with GeoCAT-f2py, they are considered
`optional` dependencies and must be explicitly installed.

If you are interested in learning more about how Conda environments work, please visit the
[managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
page of the Conda documentation.


## Building GeoCAT-f2py from source

Building GeoCAT-f2py from source code is a fairly straightforward task, but
doing so should not be necessary for most users. If you are interested in
building GeoCAT-f2py from source, you will need the following packages to be
installed.

### Required dependencies for building GeoCAT-f2py

- Python 3.7+
- numpy
- [xarray](http://xarray.pydata.org/en/stable/)
- [dask](https://dask.org/)
- [pytest](https://docs.pytest.org/en/stable/)
- [gfortran](https://gcc.gnu.org/wiki/GFortran)
- [LAPACK](http://www.netlib.org/lapack/)

### How to create a Conda environment for building GeoCAT-f2py

The GeoCAT-f2py source code includes two Conda environment definition files in
the `/build_envs` folder under the root directory that can be used to create a
development environment containing all of the packages required to build GeoCAT-f2py.
The file `environment_Linux.yml` is intended to be used on Linux systems, while
`environment_Darwin.yml` should be used on macOS.  It is necessary to have
separate `environment_*.yml` files because Linux and macOS use different
compilers, although the following commands should work on both Linux and macOS:

    conda env create -f build_envs/environment_$(uname).yml
    conda activate geocat_f2py_build


### Installing GeoCAT-f2py from source

Once the dependencies listed above are installed, you can install GeoCAT-f2py
with running the following command from the root-directory:

   `./build.sh`

which will generate all the required shared object (`.so`) files as well as
automatically run the following code:

    pip install .

For compatibility purposes, we strongly recommend using Conda to
configure your build environment as described above.


### Testing a GeoCAT-f2py build

A GeoCAT-f2py build can be tested from the root directory of the source code
repository using the following command (Explicit installation of the
[pytest](https://docs.pytest.org/en/stable/) package may be required, please
see above):

    pytest test
