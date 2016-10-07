# -*- coding: utf-8 -*-
"""Numerical/mathemetical related functions.

.. versionadded:: 2.1.0
"""

from __future__ import absolute_import, division

import math

import pydash as pyd
from .helpers import itercallback, iterator
from ._compat import _range


__all__ = (
    'add',
    'average',
    'avg',
    'ceil',
    'curve',
    'floor',
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
)


INFINITY = float('inf')


def add(collection, callback=None):
    """Sum each element in `collection`. If callback is passed, each element of
    `collection` is passed through a callback before the summation is computed.
    If `collection` and `callback` are numbers, they are added together.

    Args:
        collection (list|dict|number): Collection to process or first number to
            add.
        callback (mixed|number, optional): Callback applied per iteration or
            second number to add.

    Returns:
        number: Result of summation.

    Example:

        >>> add([1, 2, 3, 4])
        10
        >>> add([1, 2, 3, 4], lambda x: x ** 2)
        30
        >>> add(1, 5)
        6

    See Also:
        - :func:`add` (main definition)
        - :func:`sum_` (alias)

    .. versionadded:: 2.1.0

    .. versionchanged:: 3.3.0
        Support adding two numbers when passed as positional arguments.
    """
    if pyd.is_number(collection) and pyd.is_number(callback):
        return collection + callback
    else:
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

    Example:

        >>> average([1, 2, 3, 4])
        2.5
        >>> average([1, 2, 3, 4], lambda x: x ** 2)
        7.5

    See Also:
        - :func:`average` (main definition)
        - :func:`avg` (alias)
        - :func:`mean` (alias)

    .. versionadded:: 2.1.0
    """
    return add(collection, callback) / pyd.size(collection)


avg = average
mean = average


def ceil(x, precision=0):
    """Round number up to precision.

    Args:
        x (number): Number to round up.
        precision (int, optional): Rounding precision. Defaults to ``0``.

    Returns:
        int: Number rounded up.

    Example:

        >>> ceil(3.275) == 4.0
        True
        >>> ceil(3.215, 1) == 3.3
        True
        >>> ceil(6.004, 2) == 6.01
        True

    .. versionadded:: 3.3.0
    """
    return rounder(math.ceil, x, precision)


def floor(x, precision=0):
    """Round number down to precision.

    Args:
        x (number): Number to round down.
        precision (int, optional): Rounding precision. Defaults to ``0``.

    Returns:
        int: Number rounded down.

    Example:

        >>> floor(3.75) == 3.0
        True
        >>> floor(3.215, 1) == 3.2
        True
        >>> floor(0.046, 2) == 0.04
        True

    .. versionadded:: 3.3.0
    """
    return rounder(math.floor, x, precision)


def median(collection, callback=None):
    """Calculate median of each element in `collection`. If callback is passed,
    each element of `collection` is passed through a callback before the
    median is computed.

    Args:
        collection (list|dict): Collection to process.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        float: Result of median.

    Example:

        >>> median([1, 2, 3, 4, 5])
        3
        >>> median([1, 2, 3, 4])
        2.5

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

    Example:

        >>> moving_average(range(10), 1)
        [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        >>> moving_average(range(10), 5)
        [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        >>> moving_average(range(10), 10)
        [4.5]

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

    Example:

        >>> power(5, 2)
        25
        >>> power(12.5, 3)
        1953.125

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

    Example:

        >>> round_(3.275) == 3.0
        True
        >>> round_(3.275, 1) == 3.3
        True

    See Also:
        - :func:`round_` (main definition)
        - :func:`curve` (alias)

    .. versionadded:: 2.1.0
    """
    return rounder(round, x, precision)


curve = round_


def scale(array, maximum=1):
    """Scale list of value to a maximum number.

    Args:
        array (list): Numbers to scale.
        maximum (number): Maximum scale value.

    Returns:
        list: Scaled numbers.

    Example:

        >>> scale([1, 2, 3, 4])
        [0.25, 0.5, 0.75, 1.0]
        >>> scale([1, 2, 3, 4], 1)
        [0.25, 0.5, 0.75, 1.0]
        >>> scale([1, 2, 3, 4], 4)
        [1.0, 2.0, 3.0, 4.0]
        >>> scale([1, 2, 3, 4], 2)
        [0.5, 1.0, 1.5, 2.0]

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

    Example:

        >>> slope((1, 2), (4, 8))
        2.0

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

    Example:

        >>> round(std_deviation([1, 18, 20, 4]), 2) == 8.35
        True

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

    Example:

        >>> transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

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

    Example:

        >>> variance([1, 18, 20, 4])
        69.6875

    .. versionadded:: 2.1.0
    """
    ave = average(array)

    def var(x):
        return power(x - ave, 2)

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

    Example:

        >>> results = zscore([1, 2, 3])

        # [-1.224744871391589, 0.0, 1.224744871391589]

    .. versionadded:: 2.1.0
    """
    array = pyd.map_(collection, callback)
    ave = average(array)
    sig = sigma(array)

    return pyd.map_(array, lambda item: (item - ave) / sig)


#
# Utility methods not a part of the main API
#

def rounder(func, x, precision):
    precision = pow(10, precision)

    def rounder_func(item):
        return func(item * precision) / precision

    result = None

    if pyd.is_number(x):
        result = rounder_func(x)
    elif pyd.is_iterable(x):
        try:
            result = pyd.map_(x, rounder_func)
        except TypeError:
            pass

    return result
