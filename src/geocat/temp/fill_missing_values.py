import numpy as np

# MSG_FILL_INT8       = ((signed char)-127)
# MSG_FILL_CHAR       = ((char)0)
# MSG_FILL_INT16      = ((short)-32767)
# MSG_FILL_INT32      = (-2147483647L)
# MSG_FILL_FLOAT      = (9.9692099683868690e+36f) /* near 15 * 2^119 */
MSG_FILL_DOUBLE     = 9.9692099683868690e+36
# MSG_FILL_UINT8      = (255)
# MSG_FILL_UINT16     = (65535)
# MSG_FILL_UINT32     = (4294967295U)
# MSG_FILL_INT64      = ((long long)-9223372036854775806LL)
# MSG_FILL_UINT64     = ((unsigned long long)18446744073709551614ULL)
MSG_FILL_STRING     = ""

dtype_default_fill = {
    "DEFAULT_FILL"          : np.float64(MSG_FILL_DOUBLE),
     # np.dtype(np.int8)      : np.int8(MSG_FILL_INT8),
     # np.dtype(np.uint8)     : np.uint8(MSG_FILL_UINT8),
     # np.dtype(np.int16)     : np.int16(MSG_FILL_INT16),
     # np.dtype(np.uint16)    : np.uint16(MSG_FILL_UINT16),
     # np.dtype(np.int32)     : np.int32(MSG_FILL_INT32),
     # np.dtype(np.uint32)    : np.uint32(MSG_FILL_UINT32),
     # np.dtype(np.int64)     : np.int64(MSG_FILL_INT64),
     # np.dtype(np.uint64)    : np.uint64(MSG_FILL_UINT64),
     # np.dtype(np.float32)   : np.float32(MSG_FILL_FLOAT),
     np.dtype(np.float64)   : np.float64(MSG_FILL_DOUBLE),
}


def treat_in_msg(ndarray, xmsg):
    xmsg_indices = None
    xmsg_fill = xmsg

    if xmsg is None or np.isnan(xmsg):          # if no missing value specified, assume NaNs
        xmsg_indices = np.isnan(ndarray)
        try:
            xmsg_fill =  dtype_default_fill[ndarray.dtype]
        except KeyError:
            xmsg_fill =  dtype_default_fill['DEFAULT_FILL']
    else:
        xmsg_indices = (ndarray == xmsg)

    if xmsg_indices.any():
        ndarray[xmsg_indices] = xmsg_fill

    return xmsg_fill


def treat_out_msg(ndarray, xmsg, xmsg_fill):

    #todo: Should we force output missing value to (1) always be np.nan or (2) whatever it was given in input
    #      Current code here implements (2) while most GeoCAT-ncomp functions implemented (1) (e.g. linint2)

    if xmsg is None or np.isnan(xmsg):
        ndarray[ndarray == xmsg_fill] = xmsg
