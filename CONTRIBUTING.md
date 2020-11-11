Please first refer to [GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html) for overall 
contribution guidelines (such as detailed description of GeoCAT structure, forking, repository cloning, 
branching, etc.). Once you determine that a function should be contributed under this repo 
(and thus [GeoCAT-comp](https://github.com/NCAR/geocat-comp) in correspondence), please refer to the following 
contribution guidelines:


# Adding new functions to GeoCAT-f2py repo

## Converting NCL functions to GeoCAT-f2py functions

1. Search `$GEOCAT-F2PY/src/geocat/f2py/fortran/all_todo` directory to find the Fortran file for desired NCL 
function(s), "linint2.f" for example to be adapted to GeoCAT-f2py for NCL functions "linint1", "linint2", and 
"linint2_points".

2. Copy the Fortran file into the directory `$GEOCAT-F2PY/src/geocat/f2py/fortran`. Copy also other Fortran files 
if the essential Fortran file has any dependency on. 

3. Go to the directory `$GEOCAT-F2PY/src/geocat/f2py/fortran` and generate the f2py signature file from the 
Fortran file, and its dependencies if any, with the following command:

   f2py -c --fcompiler=gnu95 <desired_signature_file_name>.pyf <fortran_file_name>.f <dependency_fortran_file_name_1>.f
   
   For example: f2py -c --fcompiler=gnu95 rcm2rgrid.pyf rcm2rgrid.f linmsg_dp.f
   
   This command will generate the signature file (`.pyf`) in the same directory.

4. Determine which Fortran routines from the Fortran file are needed for wrapping up in Python, 
usually functions in the same function family are shown as "See also" in the NCL documentation webpage, 
which would be wrapped up in the same Python script.

5. The descriptions of the functions, which are determined to be wrapped in Python, need little bit manual
adjustment in the `.pyf` signature file to let Numpy.f2py know "intent" of each argument in the function signatures,
e.g. intent(in), intent(out), intent(hide). Therefore, intent keywords should be added to each argument line 
accordingly. `linint2.pyf` can be seen for example. Keywords in each argument description line would be 
tab-separated for readability purposes.

6. To be continued...


# Adding unit tests

All new computational functionality needs to include unit testing. For that purpose, please refer to the following 
guideline:

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
    - Common data structures as well as variables and functions, which could be used by multiple test methods throughout 
    the test script, are defined under a base test class or in the beginning of the test script.
    - Any group of testing functions dedicated to testing a particular phenomenon (e.g. a specific edge case, data 
    structure, etc.) is implemented by a class, which inherits TestCase from Python’s `unittest` and likely the base 
    test class, if implemented for the purpose mentioned above.
    - Assertions are used for testing various cases such as array comparison.
    - Please see previously implemented test cases for reference of the recommended testing approach, 
    e.g. [test_moc_globe_atl.py](https://github.com/NCAR/geocat-f2py/blob/master/test/test_moc_globe_atl.py)
