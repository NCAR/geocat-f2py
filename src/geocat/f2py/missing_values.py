import numpy as np

#all missing values are represented by all 1's in their dtype, int8 would be bin_11111111 or dec_-128

msg_dtype = {
    np.str: np.str(''),
    np.int8: np.int8(np.iinfo(np.int8).min),
    np.int16: np.int16(np.iinfo(np.int16).min),
    np.int32: np.int32(np.iinfo(np.int32).min),
    np.int64: np.int64(np.iinfo(np.int64).min),
    np.float32: np.float32(np.finfo(np.float32).min),
    np.float64: np.float64(np.finfo(np.float64).min),
    np.float128: np.float128(np.finfo(np.float128).min),
    np.uint8: np.uint8(np.iinfo(np.uint8).max),
    np.uint16: np.uint16(np.iinfo(np.uint16).max),
    np.uint32: np.uint32(np.iinfo(np.uint32).max),
    np.uint64: np.uint64(np.iinfo(np.uint64).max),
}

# lists of classes of dtypes
supported_dtypes = msg_dtype.keys()
float_dtypes = [np.float32, np.float64, np.float128]
int_dtypes = [np.int8, np.int16, np.int32, np.int64]
uint_dtypes = [np.uint8, np.uint16, np.uint32, np.uint64]
string_dtypes = [np.str]


# python to fortran
def py2fort_msg(ndarray, msg_py=None, msg_fort=None):
    msg_indices = None

    ndtype = ndarray.dtype.type
    if ndtype not in supported_dtypes:
        raise Exception("The ndarray.dtype.type of " + np.dtype(ndtype).name +
                        " is not a supported type")

    if msg_py is None:
        if ndtype in float_dtypes:
            msg_py = np.nan
        else:
            msg_py = msg_dtype[ndtype]

    if msg_fort is None:
        msg_fort = msg_dtype[ndtype]

    if np.isnan(msg_py):
        msg_indices = np.isnan(ndarray)
    else:
        msg_indices = (ndarray == msg_py)

    if msg_indices.any():
        ndarray[msg_indices] = msg_fort

    return ndarray, msg_py, msg_fort


#todo: Should we force output missing value to (1) always be np.nan or (2) whatever it was given in input
#      Current code here implements (2) while most GeoCAT-ncomp functions implemented (1) (e.g. linint2)
def fort2py_msg(ndarray, msg_fort=None, msg_py=None):
    msg_indices = None

    ndtype = ndarray.dtype.type
    if ndtype not in msg_dtype.keys():
        raise Exception("The ndarray.dtype.type of " + np.dtype(ndtype).name +
                        " is not a supported type")

    if msg_fort is None:
        msg_fort = msg_dtype[ndtype]

    if msg_py is None:
        if ndtype in float_dtypes:
            msg_py = np.nan
        else:
            msg_py = msg_dtype[ndtype]

    msg_indices = (ndarray == msg_fort)

    if msg_indices.any():
        ndarray[msg_indices] = msg_py

    return ndarray, msg_fort, msg_py
