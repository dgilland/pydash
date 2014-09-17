"""Numerical/mathemetical related functions.

.. versionadded:: 2.1.0
"""

from __future__ import absolute_import, division

import math

import pydash as pyd
from .helpers import itercallback, iterator
from ._compat import _range


__all__ = [
    'add',
    'average',
    'avg',
    'curve',
    'mean',
    'median',
    'moving_average',
    'moving_avg',
    'pow_',
    'power',
    'round_',
    'scale',
    'sigma',
    'slope',
    'std_deviation',
    'sum_',
    'transpose',
    'variance',
    'zscore',
]


INFINITY = float('inf')


def add(collection, callback=None):
    """Sum each element in `collection`. If callback is passed, each element of
    `collection` is passed through a callback before the summation is computed.

    Args:
        collection (list|dict): Collection to process.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        number: Result of summation.

    See Also:
        - :func:`add` (main definition)
        - :func:`sum_` (alias)

    .. versionadded:: 2.1.0
    """
    return sum(result[0] for result in itercallback(collection, callback))


sum_ = add


def average(collection, callback=None):
    """Calculate arithmetic mean of each element in `collection`. If callback
    is passed, each element of `collection` is passed through a callback before
    the mean is computed.

    Args:
        collection (list|dict): Collection to process.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        float: Result of mean.

    See Also:
        - :func:`average` (main definition)
        - :func:`avg` (alias)
        - :func:`mean` (alias)

    .. versionadded:: 2.1.0
    """
    return add(collection, callback) / pyd.size(collection)


avg = average
mean = average


def median(collection, callback=None):
    """Calculate median of each element in `collection`. If callback is passed,
    each element of `collection` is passed through a callback before the
    median is computed.

    Args:
        collection (list|dict): Collection to process.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        float: Result of median.

    .. versionadded:: 2.1.0
    """
    length = len(collection)
    middle = (length + 1) / 2
    collection = [ret[0] for ret in itercallback(sorted(collection), callback)]

    if pyd.is_odd(length):
        result = collection[int(middle - 1)]
    else:
        left = int(middle - 1.5)
        right = int(middle - 0.5)
        result = (collection[left] + collection[right]) / 2

    return result


def moving_average(array, size):
    """Calculate moving average of each element of `array`. If callback is
    passed, each element of `array` is passed through a callback before the
    moving average is computed.

    Args:
        array (list): List to process.
        size (int): Window size.

    Returns:
        list: Result of moving average.

    See Also:
        - :func:`moving_averge` (main definition)
        - :func:`moving_avg` (alias)

    .. versionadded:: 2.1.0
    """
    result = []
    size = int(size)

    for i in _range(size - 1, len(array) + 1):
        window = array[i - size:i]

        if len(window) == size:
            result.append(average(window))

    return result


moving_avg = moving_average


def power(x, n):
    """Calculate exponentiation of `x` raised to the `n` power.

    Args:
        x (number): Base number.
        n (number): Exponent.

    Returns:
        number: Result of calculation.

    See Also:
        - :func:`power` (main definition)
        - :func:`pow_` (alias)

    .. versionadded:: 2.1.0
    """
    if pyd.is_number(x):
        result = pow(x, n)
    elif pyd.is_list(x):
        result = pyd.map_(x, lambda item: pow(item, n))
    else:
        result = None

    return result


pow_ = power


def round_(x, precision=0):
    """Round number to precision.

    Args:
        x (number): Number to round.
        precision (int, optional): Rounding precision. Defaults to ``0``.

    Returns:
        int: Rounded number.

    See Also:
        - :func:`round_` (main definition)
        - :func:`curve` (alias)

    .. versionadded:: 2.1.0
    """
    rounder = pyd.partial_right(round, precision)

    if pyd.is_number(x):
        result = rounder(x)
    elif pyd.is_list(x):
        # pylint: disable=unnecessary-lambda
        result = pyd.map_(x, lambda item: rounder(item))
    else:
        result = None

    return result


curve = round_


def scale(array, maximum=1):
    """Scale list of value to a maximum number.

    Args:
        array (list): Numbers to scale.
        maximum (number): Maximum scale value.

    Returns:
        list: Scaled numbers.

    .. versionadded:: 2.1.0
    """
    array_max = max(array)
    return pyd.map_(array, lambda item: item * (maximum / array_max))


def slope(point1, point2):
    """Calculate the slope between two points.

    Args:
        point1 (list|tuple): X and Y coordinates of first point.
        point2 (list|tuple): X and Y cooredinates of second point.

    Returns:
        float: Calculated slope.

    .. versionadded:: 2.1.0
    """
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]

    if x1 == x2:
        result = INFINITY
    else:
        result = (y2 - y1) / (x2 - x1)

    return result


def std_deviation(array):
    """Calculate standard deviation of list of numbers.

    Args:
        array (list): List to process.

    Returns:
        float: Calculated standard deviation.

    See Also:
        - :func:`std_deviation` (main definition)
        - :func:`sigma` (alias)

    .. versionadded:: 2.1.0
    """
    return math.sqrt(variance(array))


sigma = std_deviation


def transpose(array):
    """Transpose the elements of `array`.

    Args:
        array (list): List to process.

    Returns:
        list: Transposed list.

    .. versionadded:: 2.1.0
    """
    trans = []

    for y, row in iterator(array):
        for x, col in iterator(row):
            trans = pyd.set_path(trans, col, [x, y])

    return trans


def variance(array):
    """Calculate the variance of the elements in `array`.

    Args:
        array (list): List to process.

    Returns:
        float: Calculated variance.

    .. versionadded:: 2.1.0
    """
    ave = average(array)
    var = lambda x: power(x - ave, 2)
    return pyd._(array).map_(var).average().value()


def zscore(collection, callback=None):
    """Calculate the standard score assuming normal distribution. If callback
    is passed, each element of `collection` is passed through a callback before
    the standard score is computed.

    Args:
        collection (list|dict): Collection to process.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        float: Calculated standard score.

    .. versionadded:: 2.1.0
    """
    array = pyd.map_(collection, callback)
    ave = average(array)
    sig = sigma(array)

    return pyd.map_(array, lambda item: (item - ave) / sig)
