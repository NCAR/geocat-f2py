import warnings

import numpy as np
import xarray as xr
from dask.array.core import map_blocks

from .errors import ChunkError, CoordinateError
from .fortran import dlinint1, dlinint2, dlinint2pts
from .missing_values import fort2py_msg, py2fort_msg

# Dask Wrappers _<funcname>()
# These Wrapper are executed within dask processes, and should do anything that
# can benefit from parallel excution.


def _linint1(xi, fi, xo, icycx, msg_py, shape):
    # ''' signature : fo = dlinint1(xi,fi,xo,[icycx,xmsg,iopt])
    # missing value handling
    fi, msg_py, msg_fort = py2fort_msg(fi, msg_py=msg_py)
    # fortran call
    fo = dlinint1(
        xi,
        fi,
        xo,
        icycx=icycx,
        xmsg=msg_fort,
    )
    # numpy and reshape
    fo = np.asarray(fo)
    fo = fo.reshape(shape)
    # missing value handling
    fi, msg_fort, msg_py = fort2py_msg(fi, msg_fort=msg_fort, msg_py=msg_py)
    fo, msg_fort, msg_py = fort2py_msg(fo, msg_fort=msg_fort, msg_py=msg_py)
    return fo


def _linint2(xi, yi, fi, xo, yo, icycx, msg_py, shape):
    # ''' signature : fo = dlinint2(xi,yi,fi,xo,yo,[icycx,xmsg,iopt])
    # missing value handling
    fi, msg_py, msg_fort = py2fort_msg(fi, msg_py=msg_py)
    # fortran call
    fo = dlinint2(
        xi,
        yi,
        fi,
        xo,
        yo,
        icycx=icycx,
        xmsg=msg_fort,
    )
    # numpy and reshape
    fo = np.asarray(fo)
    fo = fo.reshape(shape)
    # missing value handling
    fort2py_msg(fi, msg_fort=msg_fort, msg_py=msg_py)
    fort2py_msg(fo, msg_fort=msg_fort, msg_py=msg_py)
    return fo


def _linint2pts(xi, yi, fi, xo, yo, icycx, msg_py, shape):
    # ''' signature : fo = dlinint2pts(xi,yi,fi,xo,yo,[icycx,xmsg])

    # missing value handling
    fi, msg_py, msg_fort = py2fort_msg(fi, msg_py=msg_py)

    # fortran call

    fo, error_code = dlinint2pts(xi, yi, fi, xo, yo, icycx=icycx, xmsg=msg_fort)

    # Catch warnings
    if error_code == 1:
        warnings.warn(
            "WARNING linint2pts: Not enough points in input arrays or output coordinates!"
        )
    elif error_code == 2:
        warnings.warn(
            "WARNING linint2pts: x_in should be a monotonically increasing array !"
        )
    elif error_code == 3:
        warnings.warn(
            "WARNING linint2pts: y_in should be a monotonically increasing array !"
        )

    # numpy and reshape
    fo = np.asarray(fo)
    fo = fo.reshape(shape)

    # missing value handling
    fort2py_msg(fi, msg_fort=msg_fort, msg_py=msg_py)
    fort2py_msg(fo, msg_fort=msg_fort, msg_py=msg_py)
    return fo


# Outer Wrappers <funcname>()
# These Wrappers are excecuted in the __main__ python process, and should be
# used for any tasks which would not benefit from parallel execution.


def linint1(fi, xo, xi=None, icycx=0, msg_py=None):
    # ''' signature : fo = dlinint1(xi,fi,xo,[icycx,xmsg,iopt])
    """Interpolates from one series to another using piecewise linear
    interpolation across the rightmost dimension.

    linint1 uses piecewise linear interpolation to interpolate from
    one series to another.  The series may be cyclic in the X
    direction.

    If missing values are present, then linint1 will perform the
    piecewise linear interpolation at all points possible, but
    will return missing values at coordinates which could not
    be used.

    If any of the output coordinates xo are outside those of the
    input coordinates xi, the fo values at those coordinates will
    be set to missing (i.e. no extrapolation is performed).


    Parameters
    ----------

    fi : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        An array of one or more dimensions. If xi is passed in as an
        argument, then the size of the rightmost dimension of fi
        must match the rightmost dimension of xi.

        If missing values are present, then linint1 will perform the
        piecewise linear interpolation at all points possible, but
        will return missing values at coordinates which could not be
        used.

        Note:
            This variable must be
            supplied as a :class:`xarray.DataArray` in order to copy
            the dimension names to the output. Otherwise, default
            names will be used.

    xo : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        A one-dimensional array that specifies the X coordinates of
        the return array. It must be strictly monotonically
        increasing or decreasing, but may be unequally spaced.

        If the output coordinates (xo) are outside those of the
        input coordinates (xi), then the fo values at those
        coordinates will be set to missing (i.e. no extrapolation is
        performed).

    xi (:class:`numpy.ndarray`):
        An array that specifies the X coordinates of the fi array.
        Most frequently, this array is one-dimensional.  It must be
        strictly monotonically increasing or decreasing, but can be
        unequally spaced.
        If xi is multi-dimensional, then its
        dimensions must be the same as fi's dimensions. If it is
        one-dimensional, its length must be the same as the rightmost
        (fastest varying) dimension of fi.

        Note:
            If fi is of type :class:`xarray.DataArray` and xi is
            left unspecified, then the rightmost coordinate
            dimension of fi will be used. If fi is not of type
            :class:`xarray.DataArray`, then xi becomes a mandatory
            parameter. This parameter must be specified as a keyword
            argument.

    icycx : :obj:`bool`:
        An option to indicate whether the rightmost dimension of fi
        is cyclic. This should be set to True only if you have
        global data, but your longitude values don't quite wrap all
        the way around the globe. For example, if your longitude
        values go from, say, -179.75 to 179.75, or 0.5 to 359.5,
        then you would set this to True.

    msg_py : :obj:`numpy.number`:
        A numpy scalar value that represent a missing value in fi.
        This argument allows a user to use a missing value scheme
        other than NaN or masked arrays, similar to what NCL allows.

    Returns
    -------
    fo : :class:`xarray.DataArray`:
        The interpolated series. The returned value will have the same
        dimensions as fi, except for the rightmost dimension which
        will have the same dimension size as the length of xo.
        The return type will be double if fi is double, and float
        otherwise.

    Examples
    --------

    Example 1: Using linint1 with :class:`xarray.DataArray` input
    .. code-block:: python
        import numpy as np
        import xarray as xr
        import geocat.comp
        fi_np = np.random.rand(80)  # random 80-element array
        # xi does not have to be equally spaced, but it is
        # in this example
        xi = np.arange(80)
        # create target coordinate array, in this case use the same
        # min/max values as xi, but with different spacing
        xo = np.linspace(xi.min(), xi.max(), 100)
        # create :class:`xarray.DataArray` and chunk it using the
        # full shape of the original array.
        # note that xi is attached as a coordinate array
        fi = xr.DataArray(fi_np,
                          dims=['x'],
                          coords={'x': xi}
                         ).chunk(fi_np.shape)
        fo = geocat.comp.linint1(fi, xo, icycx=0)
    """

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):
        if (xi is None):
            raise CoordinateError(
                "linint2: Argument xi must be provided explicitly unless fi is an xarray.DataArray."
            )

        fi = xr.DataArray(fi,)
        fi_chunk = dict([(k, v) for (k, v) in zip(list(fi.dims), list(fi.shape))
                        ])

        fi = xr.DataArray(
            fi.data,
            coords={
                fi.dims[-1]: xi,
            },
            dims=fi.dims,
        ).chunk(fi_chunk)

    xi = fi.coords[fi.dims[-1]]

    # ensure rightmost dimensions of input are not chunked
    if fi.chunks is None:
        fi = fi.chunk()

    if list(fi.chunks)[-1:] != [xi.shape]:
        raise Exception("fi must be unchunked along the last dimension")

    # fi data structure elements and autochunking
    fi_chunks = list(fi.dims)
    fi_chunks[:-1] = [
        (k, 1) for (k, v) in zip(list(fi.dims)[:-1],
                                 list(fi.chunks)[:-1])
    ]
    fi_chunks[-1:] = [
        (k, v[0]) for (k, v) in zip(list(fi.dims)[-1:],
                                    list(fi.chunks)[-1:])
    ]
    fi_chunks = dict(fi_chunks)
    fi = fi.chunk(fi_chunks)

    # fo datastructure elements
    fo_chunks = list(fi.chunks)
    fo_chunks[-1:] = (xo.shape,)
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    fo_coords = {k: v for (k, v) in fi.coords.items()}
    fo_coords[fi.dims[-1]] = xo
    # ''' end of boilerplate

    fo = map_blocks(
        _linint1,
        xi,
        fi.data,
        xo,
        icycx,
        msg_py,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 1],
        new_axis=[fi.ndim - 1],
    )

    fo = xr.DataArray(fo.compute(),
                      attrs=fi.attrs,
                      dims=fi.dims,
                      coords=fo_coords)
    return fo


def linint2(fi, xo, yo, xi=None, yi=None, icycx=0, msg_py=None):
    """Interpolates a regular grid to a rectilinear one using bi-linear
    interpolation.
    linint2 uses bilinear interpolation to interpolate from one
    rectilinear grid to another. The input grid may be cyclic in the x
    direction. The interpolation is first performed in the x direction,
    and then in the y direction.
    Parameters
    ----------
    fi : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        An array of two or more dimensions. If xi is passed in as an
        argument, then the size of the rightmost dimension of fi
        must match the rightmost dimension of xi. Similarly, if yi
        is passed in as an argument, then the size of the second-
        rightmost dimension of fi must match the rightmost dimension
        of yi.
        If missing values are present, then linint2 will perform the
        bilinear interpolation at all points possible, but will
        return missing values at coordinates which could not be
        used.
        Note:
            This variable must be
            supplied as a :class:`xarray.DataArray` in order to copy
            the dimension names to the output. Otherwise, default
            names will be used.
    xo : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        A one-dimensional array that specifies the X coordinates of
        the return array. It must be strictly monotonically
        increasing, but may be unequally spaced.
        For geo-referenced data, xo is generally the longitude
        array.
        If the output coordinates (xo) are outside those of the
        input coordinates (xi), then the fo values at those
        coordinates will be set to missing (i.e. no extrapolation is
        performed).
    yo : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        A one-dimensional array that specifies the Y coordinates of
        the return array. It must be strictly monotonically
        increasing, but may be unequally spaced.
        For geo-referenced data, yo is generally the latitude array.
        If the output coordinates (yo) are outside those of the
        input coordinates (yi), then the fo values at those
        coordinates will be set to missing (i.e. no extrapolation is
        performed).
    xi (:class:`numpy.ndarray`):
        An array that specifies the X coordinates of the fi array.
        Most frequently, this is a 1D strictly monotonically
        increasing array that may be unequally spaced. In some
        cases, xi can be a multi-dimensional array (see next
        paragraph). The rightmost dimension (call it nxi) must have
        at least two elements, and is the last (fastest varying)
        dimension of fi.
        If xi is a multi-dimensional array, then each nxi subsection
        of xi must be strictly monotonically increasing, but may be
        unequally spaced. All but its rightmost dimension must be
        the same size as all but fi's rightmost two dimensions.
        For geo-referenced data, xi is generally the longitude
        array.
        Note:
            If fi is of type :class:`xarray.DataArray` and xi is
            left unspecified, then the rightmost coordinate
            dimension of fi will be used. If fi is not of type
            :class:`xarray.DataArray`, then xi becomes a mandatory
            parameter. This parameter must be specified as a keyword
            argument.
    yi (:class:`numpy.ndarray`):
        An array that specifies the Y coordinates of the fi array.
        Most frequently, this is a 1D strictly monotonically
        increasing array that may be unequally spaced. In some
        cases, yi can be a multi-dimensional array (see next
        paragraph). The rightmost dimension (call it nyi) must have
        at least two elements, and is the second-to-last dimension
        of fi.
        If yi is a multi-dimensional array, then each nyi subsection
        of yi must be strictly monotonically increasing, but may be
        unequally spaced. All but its rightmost dimension must be
        the same size as all but fi's rightmost two dimensions.
        For geo-referenced data, yi is generally the latitude array.
        Note:
            If fi is of type :class:`xarray.DataArray` and xi is
            left unspecified, then the second-to-rightmost
            coordinate dimension of fi will be used. If fi is not of
            type :class:`xarray.DataArray`, then xi becomes a
            mandatory parameter. This parameter must be specified as
            a keyword argument.
    icycx : :obj:`bool`:
        An option to indicate whether the rightmost dimension of fi
        is cyclic. This should be set to True only if you have
        global data, but your longitude values don't quite wrap all
        the way around the globe. For example, if your longitude
        values go from, say, -179.75 to 179.75, or 0.5 to 359.5,
        then you would set this to True.
    msg_py : :obj:`numpy.number`:
        A numpy scalar value that represent a missing value in fi.
        This argument allows a user to use a missing value scheme
        other than NaN or masked arrays, similar to what NCL allows.
    Returns
    -------
    fo : :class:`xarray.DataArray`:
        The interpolated grid. If the *meta*
        parameter is True, then the result will include named dimensions
        matching the input array. The returned value will have the same
        dimensions as fi, except for the rightmost two dimensions which
        will have the same dimension sizes as the lengths of yo and xo.
        The return type will be double if fi is double, and float
        otherwise.
    Examples
    --------
    Example 1: Using linint2 with :class:`xarray.DataArray` input
    .. code-block:: python
        import numpy as np
        import xarray as xr
        import geocat.comp
        fi_np = np.random.rand(30, 80)  # random 30x80 array
        # xi and yi do not have to be equally spaced, but they are
        # in this example
        xi = np.arange(80)
        yi = np.arange(30)
        # create target coordinate arrays, in this case use the same
        # min/max values as xi and yi, but with different spacing
        xo = np.linspace(xi.min(), xi.max(), 100)
        yo = np.linspace(yi.min(), yi.max(), 50)
        # create :class:`xarray.DataArray` and chunk it using the
        # full shape of the original array.
        # note that xi and yi are attached as coordinate arrays
        fi = xr.DataArray(fi_np,
                          dims=['lat', 'lon'],
                          coords={'lat': yi, 'lon': xi}
                         ).chunk(fi_np.shape)
        fo = geocat.comp.linint2(fi, xo, yo, icycx=0)
    """

    # ''' Start of boilerplate
    if not isinstance(fi, xr.DataArray):
        if (xi is None) | (yi is None):
            raise CoordinateError(
                "linint2: Arguments xi and yi must be provided explicitly unless fi is an xarray.DataArray."
            )

        fi = xr.DataArray(fi,)
        fi_chunk = dict([(k, v) for (k, v) in zip(list(fi.dims), list(fi.shape))
                        ])

        fi = xr.DataArray(
            fi.data,
            coords={
                fi.dims[-1]: xi,
                fi.dims[-2]: yi,
            },
            dims=fi.dims,
        ).chunk(fi_chunk)

    xi = fi.coords[fi.dims[-1]]
    yi = fi.coords[fi.dims[-2]]

    # ensure rightmost dimensions of input are not chunked
    if fi.chunks is None:
        fi = fi.chunk()

    if list(fi.chunks)[-2:] != [yi.shape, xi.shape]:
        raise ChunkError(
            "linint2: fi must be unchunked along the rightmost two dimensions")

    # fi data structure elements and autochunking
    fi_chunks = list(fi.dims)
    fi_chunks[:-2] = [
        (k, 1) for (k, v) in zip(list(fi.dims)[:-2],
                                 list(fi.chunks)[:-2])
    ]
    fi_chunks[-2:] = [
        (k, v[0]) for (k, v) in zip(list(fi.dims)[-2:],
                                    list(fi.chunks)[-2:])
    ]
    fi_chunks = dict(fi_chunks)
    fi = fi.chunk(fi_chunks)

    # fo datastructure elements
    fo_chunks = list(fi.chunks)
    fo_chunks[-2:] = (yo.shape, xo.shape)
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    fo_coords = {k: v for (k, v) in fi.coords.items()}
    fo_coords[fi.dims[-1]] = xo
    fo_coords[fi.dims[-2]] = yo
    # ''' end of boilerplate

    fo = map_blocks(
        _linint2,
        yi,
        xi,
        fi.data,
        yo,
        xo,
        icycx,
        msg_py,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2, fi.ndim - 1],
    )
    fo = xr.DataArray(fo.compute(),
                      attrs=fi.attrs,
                      dims=fi.dims,
                      coords=fo_coords)
    return fo


def linint2pts(fi, xo, yo, icycx=False, msg_py=None, xi=None, yi=None):
    """Interpolates from a rectilinear grid to an unstructured grid or
    locations using bilinear interpolation.

    Parameters
    ----------
    fi : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        An array of two or more dimensions. The two rightmost
        dimensions (nyi x nxi) are the dimensions to be used in
        the interpolation. If user-defined missing values are
        present (other than NaNs), the value of `msg_py` must be
        set appropriately.
    xo : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        A one-dimensional array that specifies the X (longitude)
        coordinates of the unstructured grid.
    yo : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        A one-dimensional array that specifies the Y (latitude)
        coordinates of the unstructured grid. It must be the same
        length as `xo`.
    icycx : :obj:`bool`:
        An option to indicate whether the rightmost dimension of fi
        is cyclic. Default valus is 0. This should be set to True
        only if you have global data, but your longitude values
        don't quite wrap all the way around the globe. For example,
        if your longitude values go from, say, -179.75 to 179.75,
        or 0.5 to 359.5, then you would set this to True.
    msg_py : :obj:`numpy.number`:
        A numpy scalar value that represent a missing value in fi.
        This argument allows a user to use a missing value scheme
        other than NaN or masked arrays, similar to what NCL allows.
    xi : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        A strictly monotonically increasing array that specifies
        the X [longitude] coordinates of the `fi` array. `xi` might
        be defined as the coordinates of `fi` when `fi` is of type
        `xarray.DataArray`; in this case `xi` may not be explicitly
        given as a function argument.
    yi : :class:`xarray.DataArray` or :class:`numpy.ndarray`:
        A strictly monotonically increasing array that specifies
        the Y [latitude] coordinates of the `fi` array. ``yi` might
        be defined as the coordinates of `fi` when `fi` is of type
        `xarray.DataArray`; in this case `yi` may not be explicitly
        given as a function argument.
    Returns
    -------
    fo: :class:`numpy.ndarray`:
        The returned value will have the same dimensions as `fi`,
        except for the rightmost dimension which will have the same
        dimension size as the length of `yo` and `xo`. The return
        type will be double if `fi` is double, and float otherwise.
    Description
    -----------
        The `linint2pts` function uses bilinear interpolation to interpolate
        from a rectilinear grid to an unstructured grid.
        If missing values are present, then `linint2pts` will perform the
        piecewise linear interpolation at all points possible, but will return
        missing values at coordinates which could not be used. If one or more
        of the four closest grid points to a particular (xo, yo) coordinate
        pair are missing, then the return value for this coordinate pair will
        be missing.
        If the user inadvertently specifies output coordinates (xo, yo) that
        are outside those of the input coordinates (xi, yi), the output value
        at this coordinate pair will be set to missing as no extrapolation
        is performed.
        `linint2pts` is different from `linint2` in that `xo` and `yo` are
        coordinate pairs, and need not be monotonically increasing. It is
        also different in the dimensioning of the return array.
        This function could be used if the user wanted to interpolate gridded
        data to, say, the location of rawinsonde sites or buoy/xbt locations.

        Warning: if `xi` contains longitudes, then the `xo` values must be in the
        same range. In addition, if the `xi` values span 0 to 360, then the `xo`
        values must also be specified in this range (i.e. -180 to 180 will not work).

    Examples
    --------
    Example 1: Using linint2pts with :class:`xarray.DataArray` input
        .. code-block:: python
        import numpy as np
        import xarray as xr
        import geocat.comp
        fi_np = np.random.rand(30, 80)  # random 30x80 array
        # xi and yi do not have to be equally spaced, but they are
        # in this example
        xi = np.arange(80)
        yi = np.arange(30)
        # create target coordinate arrays, in this case use the same
        # min/max values as xi and yi, but with different spacing
        xo = np.linspace(xi.min(), xi.max(), 100)
        yo = np.linspace(yi.min(), yi.max(), 50)
        # create :class:`xarray.DataArray` and chunk it using the
        # full shape of the original array.
        # note that xi and yi are attached as coordinate arrays
        fi = xr.DataArray(fi_np,
                          dims=['lat', 'lon'],
                          coords={'lat': yi, 'lon': xi}
                         ).chunk(fi_np.shape)
        fo = geocat.comp.linint2pts(fi, xo, yo, 0)
    """

    # ''' Start of boilerplate
    # If a Numpy input is given, convert it to Xarray and chunk it just
    # with its dims
    if not isinstance(fi, xr.DataArray):
        if (xi is None) | (yi is None):
            raise CoordinateError(
                "linint2pts: Arguments xi and yi must be provided explicitly unless fi is an xarray.DataArray."
            )

        fi = xr.DataArray(fi)
        fi_chunk = dict([(k, v) for (k, v) in zip(list(fi.dims), list(fi.shape))
                        ])

        fi = xr.DataArray(
            fi.data,
            coords={
                fi.dims[-1]: xi,
                fi.dims[-2]: yi,
            },
            dims=fi.dims,
        ).chunk(fi_chunk)

    # Xarray input
    else:
        # If an unchunked Xarray input is given, chunk it just with its dims
        if (fi.chunks is None):
            fi_chunk = dict([
                (k, v) for (k, v) in zip(list(fi.dims), list(fi.shape))
            ])
            data = fi.chunk(fi_chunk)

    xi = fi.coords[fi.dims[-1]]
    yi = fi.coords[fi.dims[-2]]

    # Ensure the rightmost dimension of input is not chunked
    if fi.chunks is None:
        fi = fi.chunk()

    if list(fi.chunks)[-2:] != [yi.shape, xi.shape]:
        raise ChunkError(
            "ERROR linint2pts: fi must be unchunked along the rightmost two dimensions"
        )

    if xo.shape != yo.shape:
        raise Exception("ERROR linint2pts xo and yo must be of equal length")

    # fi data structure elements and autochunking
    fi_chunks = list(fi.dims)
    fi_chunks[:-2] = [
        (k, 1) for (k, v) in zip(list(fi.dims)[:-2],
                                 list(fi.chunks)[:-2])
    ]
    fi_chunks[-2:] = [
        (k, v[0]) for (k, v) in zip(list(fi.dims)[-2:],
                                    list(fi.chunks)[-2:])
    ]
    fi_chunks = dict(fi_chunks)
    fi = fi.chunk(fi_chunks)

    # fo datastructure elements
    fo_chunks = list(fi.chunks)
    fo_chunks[-2:] = (xo.shape,)
    fo_chunks = tuple(fo_chunks)
    fo_shape = tuple(a[0] for a in list(fo_chunks))
    fo_coords = {k: v for (k, v) in fi.coords.items()}
    # fo_coords.remove(fi.dims[-1]) # this dimension dissapears
    fo_coords[fi.dims[-1]] = xo  # remove this line omce dims are figured out
    fo_coords[fi.dims[-2]] = yo  # maybe replace with 'pts'
    # ''' end of boilerplate

    fo = map_blocks(
        _linint2pts,
        yi,
        xi,
        fi.data,
        yo,
        xo,
        icycx,
        msg_py,
        fo_shape,
        chunks=fo_chunks,
        dtype=fi.dtype,
        drop_axis=[fi.ndim - 2, fi.ndim - 1],
        new_axis=[fi.ndim - 2],
    )
    fo = xr.DataArray(fo.compute(), attrs=fi.attrs)
    return fo


# Transparent wrappers for geocat.ncomp backwards compatibility


def linint2_points(fi, xo, yo, icycx, msg=None, meta=False, xi=None, yi=None):
    warnings.warn(
        "linint2_points function name and signature will be deprecated soon "
        "in a future version. Use `linint2pts` instead!",
        PendingDeprecationWarning)

    return linint2pts(fi, xo, yo, icycx=icycx, msg_py=msg, xi=xi, yi=yi)
