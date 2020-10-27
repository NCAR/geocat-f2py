import numpy as np

#all missing values are represented by all 1's in their dtype, int8 would be bin_11111111 or dec_-128
MSG_CHAR        = np.iinfo(np.character).min
MSG_INT8        = np.iinfo(np.int8).min
MSG_INT16       = np.iinfo(np.int16).min
MSG_INT32       = np.iinfo(np.int32).min
MSG_INT64       = np.iinfo(np.int64).min
MSG_FLOAT32     = np.finfo(np.float32).min
MSG_FLOAT64     = np.finfo(np.float64).min
MSG_FLOAT128    = np.finfo(np.float128).min
MSG_UINT8       = np.iinfo(np.uint8).max
MSG_UINT16      = np.iinfo(np.uint16).max
MSG_UINT32      = np.iinfo(np.uint32).max
MSG_UINT64      = np.iinfo(np.uint64).max
MSG_STRING      = ""


msg_dtype = {
    'DEFAULT'               : np.float64(MSG_FLOAT64),
     np.dtype(np.int8)      : np.int8(MSG_INT8),
     np.dtype(np.uint8)     : np.uint8(MSG_UINT8),
     np.dtype(np.int16)     : np.int16(MSG_INT16),
     np.dtype(np.uint16)    : np.uint16(MSG_UINT16),
     np.dtype(np.int32)     : np.int32(MSG_INT32),
     np.dtype(np.uint32)    : np.uint32(MSG_UINT32),
     np.dtype(np.int64)     : np.int64(MSG_INT64),
     np.dtype(np.uint64)    : np.uint64(MSG_UINT64),
     np.dtype(np.float32)   : np.float32(MSG_FLOAT),
     np.dtype(np.float64)   : np.float64(MSG_FLOAT64),
}


def py2fort_msg(ndarray, msg_py=np.nan, msg_fort='DEFAULT'):
    msg_indices = None

    if np.isnan(msg_py):
        msg_indices = np.isnan(ndarray)
    else:
        msg_indices = (ndarray == msg_py)

    msg_fort =  msg_dtype[ndarray.dtype]

    if msg_indices.any():
        ndarray[msg_indices] = msg_fort

    return ndarray, msg_py, msg_fort


    #todo: Should we force output missing value to (1) always be np.nan or (2) whatever it was given in input
    #      Current code here implements (2) while most GeoCAT-ncomp functions implemented (1) (e.g. linint2)
def fort2py_msg(ndarray, msg_fort='DEFAULT', msg_py=np.nan,):
    msg_indices = None

    msg_indices = (ndarray == msg_fort) # from fort to py we don't need to worry about np.nans.

    if msg_indices.any():
        ndarray[msg_indices] = msg_py

    return ndarray, msg_fort, msg_py