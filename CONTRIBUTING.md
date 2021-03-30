Please first refer to [GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html) for overall
contribution guidelines (such as detailed description of GeoCAT structure, forking, repository cloning,
branching, etc.). Once you determine that a function should be contributed under this repo
(and thus [GeoCAT-comp](https://github.com/NCAR/geocat-comp) in correspondence), please refer to the following
contribution guidelines:


# Adding new functions to GeoCAT-f2py repo

Replicating NCL functions by wrapping up their Fortran routines in Python requires adding a new function to
GeoCAT-f2py.

## Converting NCL functions to GeoCAT-f2py functions

1. Detailed information (description, inputs, outputs, etc.) about NCL functions can be found at the
[NCL webpage](https://www.ncl.ucar.edu/Document/Functions/index.shtml).  Even though some of the NCL functions were
implemented in pure NCL (such functions need to be replicated in a pure Python fashion), most of the NCL functions
were implemented with the use of one or more Fortran routine(s). To find the mapping between any NCL function and
such Fortran functions, the [NCL Github repository](https://github.com/NCAR/ncl) can be used:

   - Search `$NCLSRC/ni/src/lib/nfp/wrapper.c` for relevant `NclRegisterFunc` entry with desired NCL function name
   as the third argument, e.g. "triple2grid" for example:

     `NclRegisterFunc(triple2grid_W,args,"triple2grid",nargs);`

     The first argument is the NCL "C wrapper" function name.

   - Search for `<NCLfunction>_W` in `$NCLSRC/ni/src/lib/nfp/*W.c` (e.g. "triple2grid_W.c" in this case). This
   C wrapper contains the code that has function call(s) to Fortran routine(s).

   - Determine which Fortran routine(s) are needed by walking through the above C wrapper, usually wrapped in an
   `NGCALLF` macro in a loop towards the end of the `_W` function.

2. Search `$GEOCAT-F2PY/src/geocat/f2py/fortran/all_todo` directory to find the Fortran file(s) that contain
the Fortran routines, which were determined in the above step, for the NCL function of interest. For example,
"triple2grid.f" is to be adapted to GeoCAT-f2py for NCL function "triple2grid".

3. Copy the Fortran file(s) into the directory `$GEOCAT-F2PY/src/geocat/f2py/fortran`. Copy also other Fortran files,
if any, on which the essential Fortran file has any dependency, e.g. check the `rcm2rgrid` example for such a case.

   Note: For tracking purposes, it is better not to modify the names of the Fortran files and  Fortran routines inside
   those files.

4. Go to the directory `$GEOCAT-F2PY/src/geocat/f2py/fortran` and generate the f2py signature file(s) (`.pyf`) from
the Fortran file(s) with the following command:

   `f2py <fortran_filename>.f -m <target_module_name> -h <desired_signature_file_name>.pyf`

   For example:

   `f2py rcm2rgrid.f -m rcm2rgrid -h rcm2rgrid.pyf`

   This command will generate the signature file (`.pyf`) in the same directory.

5. Determine which Fortran routine(s) from the Fortran file(s) are needed for being wrapped up in Python,
usually functions in the same function family are shown as "See also" in the NCL documentation webpage,
which would be wrapped up in the same Python script.

6. The descriptions of the functions, which are determined to be wrapped up in Python, require a bit of manual
adjustment in the `.pyf` signature file to let Numpy.f2py know "intent" of each argument in the function signatures,
e.g. intent(in), intent(out), intent(hide). Therefore, "intent" keywords should be added to each argument line
accordingly. `triple2grid.pyf` can be seen for example. Keywords in each argument description line would be
tab-separated for readability purposes.

7. When the manual adjustment of the signature file is done, shared object file (`.so`) needs to be generated in
the same directory (i.e. `$GEOCAT-F2PY/src/geocat/f2py/fortran`) with the command:

   `f2py -c --fcompiler=gnu95 <desired_signature_file_name>.pyf <fortran_file_name>.f <dependency_fortran_file_name_1>.f`

   As can be seen from the command format above, not only the essential Fortran file but also its dependency
   Fortran files should be given to this command besides the `.pyf` signature file. For example:

   `f2py -c --fcompiler=gnu95 rcm2rgrid.pyf rcm2rgrid.f linmsg_dp.f`

   This command will generate the shared object file (`.so`) in the same directory.

   NOTE: `.so` files should be private to local development and shouldn't be pushed to the remote repository
   since they are platform-dependent object files; this is already handled by the `.gitignore` file in this repo.
   However, in order to automate creation of many `.so` files when building GeoCAT-f2py from source code in
   any platform, the command above should be added to the following file:

   `$GEOCAT-F2PY/build.sh`

8. The list of functions from the `.pyf` signature file that would be wrapped in in Python
should be added to the following file:

   `$GEOCAT-F2PY/src/geocat/f2py/fortran/_init_.py`

   as an import. For example:

   `from .rcm2rgrid import (drcm2rgrid, drgrid2rcm)`

9. Now, to wrap up a whole new NCL function or family of NCL functions that handle similar computations in Python,
create a new Python file in the directory `$GEOCAT-F2PY/src/geocat/f2py`.

   - The name of the NCL function(s) that are wrapped up in this Python script can be either (1) the exact same
   NCL name, e.g. `moc_globe_atl` and `rcm2points`, or (2) a newer name of preference (which may be more python
   fashion, more descriptive, etc.), e.g. `triple_to_grid` and `grid_to_triple`.

   - The file name of the Python script can be given depending on the function or function family name that
   are wrapped up in this file, e.g. `rcm2rgrid_wrapper.py` stands for the implementation of both `rcm2rgrid`
   and `rgrid2rcm` functions.

   - In the Python script, the functions that wrap up NCL functionality and are called directly by the end-user
   are user API functions, which are supposed to be included in the `geocat.f2py` namespace. The other functions
   that are used by the user API functions are internal API functions, which preferably starts with an underscore
   ("_") in their names and are not included in the `geocat.f2py` namespace.

   - Each Python wrapper script should import the corresponding Fortran routines from the `fortran` directory.

10. Implementing a wrapper function would, most of time, be straightforward. A Python wrapper function
(i.e. user API function) for each NCL function would handle input data preprocessing (sanity checks, auto-chunking,
etc.) and then would make use of a second (i.e. internal) wrapper function that handles tasks such as missing
value handling and Fortran function calls for every single Dask chunk (where Dask paralelization is applicable).
For example, see

     `$GEOCAT-F2PY/src/geocat/f2py/rcm2rgrid_wrapper.py`.

     In cases where no built-in Dask parallelization is needed, even a single wrapper function would be enough.

11. After the wrapper is implemented, the user API functions should be imported in the following file:

    `$GEOCAT-F2PY/src/geocat/f2py/_init_.py`

    to be included in the namespace.

12. The code should be ready for unit tests after this step.


# Adding unit tests

All new computational functionality needs to include unit testing. For that purpose, please refer to the following
guidelines:

1. Unit tests of the function should be implemented as a separate test file under the `$GEOCATF2PY/test` folder.

2. The [pytest](https://docs.pytest.org/en/stable/contents.html) testing framework is used as a “runner” for the tests.
For further information about `pytest`, see: [pytest documentation](https://docs.pytest.org/en/stable/contents.html).

    - Test scripts themselves are not intended to use `pytest` through implementation. Instead, `pytest` should be used
    only for running test scripts as follows:

        `pytest <test_script_name>.py`

    - Not using `pytest` for implementation allows the unit tests to be also run by using:

        `python -m unittest <test_script_name>.py`

3. Python’s unit testing framework [unittest](https://docs.python.org/3/library/unittest.html) is used for
implementation of the test scripts. For further information about `unittest`,
see: [unittest documentation](https://docs.python.org/3/library/unittest.html).

4. Recommended but not mandatory implementation approach is as follows:

    - Common data structures, variables and functions,  as well as
    expected outputs, which could be used by multiple test methods throughout
    the test script, are defined either under a base test class or in the very
    beginning of the test script for being used by multiple unit test cases.

    - For the sake of having reference results (i.e. expected output or ground truth for not
    all but the most cases), an NCL test script can be written under
    `\test\ncl_tests` folder and its output can be used for each testing
    scenario.

    - Any group of testing functions dedicated to testing a particular
    phenomenon (e.g. a specific edge case, data structure, etc.) is
    implemented by a class, which inherits `TestCase` from Python's
    `unittest` and likely the base test class implemented for the purpose
    mentioned above.

    - Assertions are used for testing various cases such as array comparison.

    - Please see previously implemented test cases for reference of the
    recommended testing approach,
    e.g. [test_moc_globe_atl.py](https://github.com/NCAR/geocat-f2py/blob/main/test/test_moc_globe_atl.py)
