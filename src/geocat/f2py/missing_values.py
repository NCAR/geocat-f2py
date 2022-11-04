import numpy as np


def get_msg_dtype(ty):
    if np.issubdtype(ty, np.integer):
        return np.iinfo(ty).max
    elif np.issubdtype(ty, np.floating) or np.issubdtype(ty, np.complexfloating):
        return np.finfo(ty).max
    elif np.issubdtype(ty, np.flexible):
        return str('')
    else:
        raise Exception(f"The ndarray.dtype.type of {ty.name} is not a supported type")


def get_py_msg_val(ty):
    if np.issubdtype(ty, np.integer):
        return np.iinfo(ty).max
    elif np.issubdtype(ty, np.floating):
        return np.nan
    elif np.issubdtype(ty, np.complexfloating):
        return np.nan + np.nan * 1j
    elif np.issubdtype(ty, np.flexible):
        return str('')
    else:
        raise Exception(f"The ndarray.dtype.type of {ty.name} is not a supported type")


def py2fort_msg(ndarray, msg_py=None, msg_fort=None):
    msg_indices = None
    ndtype = ndarray.dtype.type

    if msg_py is None:
        msg_py = get_py_msg_val(ndtype)

    if msg_fort is None:
        msg_fort = get_msg_dtype(ndtype)
        
    if np.isnan(msg_py):
        msg_indices = np.isnan(ndarray)
    else:
        msg_indices = (ndarray == msg_py)

    if msg_indices.any():
        ndarray[msg_indices] = msg_fort

    return ndarray, msg_py, msg_fort


def fort2py_msg(ndarray, msg_fort=None, msg_py=None):
    msg_indices = None
    ndtype = ndarray.dtype.type

    if msg_fort is None:
        msg_fort = get_msg_dtype(ndtype)

    if msg_py is None:
        msg_py = get_py_msg_val(ndtype)

    msg_indices = (ndarray == msg_fort)

    if msg_indices.any():
        ndarray[msg_indices] = msg_py

    return ndarray, msg_fort, msg_py