"""
Numerical/mathemetical related functions.

.. versionadded:: 2.1.0
"""

import math
import operator
from operator import (
    add,
    mul as multiply,
    pow,
    sub as subtract,
    truediv as divide,
)
import re
from statistics import mean, median, stdev as std_deviation, variance
from typing import Iterable, List, TypeVar

import pydash as pyd

from .helpers import UNSET, iterator, iterator_with_default, iteriteratee


T = TypeVar("T")

__all__ = (
    "add",
    "ceil",
    "clamp",
    "divide",
    "floor",
    "max_",
    "max_by",
    "mean",
    "mean_by",
    "median",
    "min_",
    "min_by",
    "moving_mean",
    "multiply",
    "power",
    "round_",
    "scale",
    "slope",
    "std_deviation",
    "sum_",
    "sum_by",
    "subtract",
    "transpose",
    "variance",
    "zscore",
)


INFINITY = float("inf")


def sum_(collection):
    """
    Sum each element in `collection`.

    Args:
        collection (list|dict|number): Collection to process or first number to add.

    Returns:
        number: Result of summation.

    Example:

        >>> sum_([1, 2, 3, 4])
        10

    .. versionadded:: 2.1.0

    .. versionchanged:: 3.3.0
        Support adding two numbers when passed as positional arguments.

    .. versionchanged:: 4.0.0
        Move iteratee support to :func:`sum_by`. Move two argument addition to
        :func:`add`.
    """
    return sum_by(collection)


def sum_by(collection: Iterable, iteratee=lambda x: x):
    """
    Sum each element in `collection`. If iteratee is passed, each element of `collection` is passed
    through a iteratee before the summation is computed.

    Args:
        collection (list|dict|number): Collection to process or first number to add.
        iteratee (mixed|number, optional): Iteratee applied per iteration or second number to add.

    Returns:
        number: Result of summation.

    Example:

        >>> sum_by([1, 2, 3, 4], lambda x: x ** 2)
        30

    .. versionadded:: 4.0.0
    """
    return sum(map(iteratee, collection))


def mean_by(collection, iteratee=lambda x: x):
    """
    Calculate arithmetic mean of each element in `collection`. If iteratee is passed, each element
    of `collection` is passed through a iteratee before the mean is computed.

    Args:
        collection (list|dict): Collection to process.
        iteratee (mixed, optional): Iteratee applied per iteration.

    Returns:
        float: Result of mean.

    Example:

        >>> mean_by([1, 2, 3, 4], lambda x: x ** 2)
        7.5

    .. versionadded:: 4.0.0
    """
    return sum_by(collection, iteratee) / len(collection)


def ceil(x, precision=0):
    """
    Round number up to precision.

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


def clamp(x, lower, upper=None):
    """
    Clamps number within the inclusive lower and upper bounds.

    Args:
        x (number): Number to clamp.
        lower (number, optional): Lower bound.
        upper (number): Upper bound

    Returns:
        number

    Example:

        >>> clamp(-10, -5, 5)
        -5
        >>> clamp(10, -5, 5)
        5
        >>> clamp(10, 5)
        5
        >>> clamp(-10, 5)
        -10

    .. versionadded:: 4.0.0
    """
    if upper is None:
        upper = lower
        lower = x

    if x < lower:
        x = lower
    elif x > upper:
        x = upper

    return x


def divide(dividend, divisor):
    """
    Divide two numbers.

    Args:
        dividend (int/float): The first number in a division.
        divisor (int/float): The second number in a division.

    Returns:
        int/float: Returns the quotient.

    Example:

        >>> divide(20, 5)
        4.0
        >>> divide(1.5, 3)
        0.5
        >>> divide(None, None)
        1.0
        >>> divide(5, None)
        5.0

    .. versionadded:: 4.0.0
    """
    return call_math_operator(dividend, divisor, operator.truediv, 1)


def floor(x, precision=0):
    """
    Round number down to precision.

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


def max_(collection, default=UNSET):
    """
    Retrieves the maximum value of a `collection`.

    Args:
        collection (list|dict): Collection to iterate over.
        default (mixed, optional): Value to return if `collection` is empty.

    Returns:
        mixed: Maximum value.

    Example:

        >>> max_([1, 2, 3, 4])
        4
        >>> max_([], default=-1)
        -1

    .. versionadded:: 1.0.0

    .. versionchanged:: 4.0.0
        Moved iteratee iteratee support to :func:`max_by`.
    """
    return max_by(collection, default=default)


def max_by(collection, iteratee=lambda x: x, default=UNSET):
    """
    Retrieves the maximum value of a `collection`.

    Args:
        collection (list|dict): Collection to iterate over.
        iteratee (mixed, optional): Iteratee applied per iteration.
        default (mixed, optional): Value to return if `collection` is empty.

    Returns:
        mixed: Maximum value.

    Example:

        >>> max_by([1.0, 1.5, 1.8], math.floor)
        1.0
        >>> max_by([{'a': 1}, {'a': 2}, {'a': 3}], 'a')
        {'a': 3}
        >>> max_by([], default=-1)
        -1

    .. versionadded:: 4.0.0
    """
    if isinstance(collection, dict):
        collection = collection.values()

    return max(collection, key=iteratee, default=default)


def median_by(collection, iteratee=lambda x: x):
    """
    Calculate median of each element in `collection`. If iteratee is passed, each element of
    `collection` is passed through a iteratee before the median is computed.

    Args:
        collection (list|dict): Collection to process.
        iteratee (mixed, optional): Iteratee applied per iteration.

    Returns:
        float: Result of median.

    Example:

        >>> median([1, 2, 3, 4, 5])
        3
        >>> median([1, 2, 3, 4])
        2.5

    .. versionadded:: 2.1.0
    """
    return median(map(iteratee, collection))


def min_(collection, default=UNSET):
    """
    Retrieves the minimum value of a `collection`.

    Args:
        collection (list|dict): Collection to iterate over.
        default (mixed, optional): Value to return if `collection` is empty.

    Returns:
        mixed: Minimum value.

    Example:

        >>> min_([1, 2, 3, 4])
        1
        >>> min_([], default=100)
        100

    .. versionadded:: 1.0.0

    .. versionchanged:: 4.0.0
        Moved iteratee iteratee support to :func:`min_by`.
    """
    return min_by(collection, default=default)


def min_by(collection, iteratee=lambda x: x, default=UNSET):
    """
    Retrieves the minimum value of a `collection`.

    Args:
        collection (list|dict): Collection to iterate over.
        iteratee (mixed, optional): Iteratee applied per iteration.
        default (mixed, optional): Value to return if `collection` is empty.

    Returns:
        mixed: Minimum value.

    Example:

        >>> min_by([1.8, 1.5, 1.0], math.floor)
        1.8
        >>> min_by([{'a': 1}, {'a': 2}, {'a': 3}], 'a')
        {'a': 1}
        >>> min_by([], default=100)
        100

    .. versionadded:: 4.0.0
    """
    if isinstance(collection, dict):
        collection = collection.values()
    return min(collection, key=iteratee, default=default)


def moving_mean(array, size):
    """
    Calculate moving mean of each element of `array`.

    Args:
        array (list): List to process.
        size (int): Window size.

    Returns:
        list: Result of moving average.

    Example:

        >>> moving_mean(range(10), 1)
        [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        >>> moving_mean(range(10), 5)
        [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        >>> moving_mean(range(10), 10)
        [4.5]

    .. versionadded:: 2.1.0

    .. versionchanged:: 4.0.0
        Rename to ``moving_mean`` and remove ``moving_average`` and ``moving_avg`` aliases.
    """
    result = []
    size = int(size)

    for i in range(size - 1, len(array) + 1):
        window = array[i - size : i]

        if len(window) == size:
            result.append(mean(window))

    return result


def power(x, n):
    """
    Calculate exponentiation of `x` raised to the `n` power.

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

    .. versionadded:: 2.1.0

    .. versionchanged:: 4.0.0
        Removed alias ``pow_``.
    """
    if pyd.is_number(x):
        result = pow(x, n)
    elif pyd.is_list(x):
        result = [pow(item, n) for item in x]
    else:
        result = None

    return result


def round_(x, precision=0):
    """
    Round number to precision.

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

    .. versionadded:: 2.1.0

    .. versionchanged:: 4.0.0
        Remove alias ``curve``.
    """
    return rounder(round, x, precision)


def scale(array, maximum=1):
    """
    Scale list of value to a maximum number.

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
    factor = maximum / array_max
    return [item * factor for item in array]


def slope(point1, point2):
    """
    Calculate the slope between two points.

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
    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2:
        result = INFINITY
    else:
        result = (y2 - y1) / (x2 - x1)

    return result


def transpose(array: List[List]):
    """
    Transpose the elements of `array`.

    Args:
        array (list): List to process.

    Returns:
        list: Transposed list.

    Example:

        >>> transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    .. versionadded:: 2.1.0
    """

    return list(zip(*array))


def zscore(collection, iteratee=lambda x: x):
    """
    Calculate the standard score assuming normal distribution. If iteratee is passed, each element
    of `collection` is passed through a iteratee before the standard score is computed.

    Args:
        collection (list|dict): Collection to process.
        iteratee (mixed, optional): Iteratee applied per iteration.

    Returns:
        float: Calculated standard score.

    Example:

        >>> results = zscore([1, 2, 3])

        # [-1.224744871391589, 0.0, 1.224744871391589]

    .. versionadded:: 2.1.0
    """
    array = map(iteratee, collection)
    avg = mean(array)
    sig = std_deviation(array)

    return [(item - avg) / sig for item in array]


#
# Utility methods not a part of the main API
#


def call_math_operator(value1, value2, op, default):
    """Return the result of the math operation on the given values."""
    if not value1:
        value1 = default

    if not value2:
        value2 = default

    if not pyd.is_number(value1):
        try:
            value1 = float(value1)
        except Exception:
            pass

    if not pyd.is_number(value2):
        try:
            value2 = float(value2)
        except Exception:
            pass

    return op(value1, value2)


def rounder(func, x, precision):
    precision = pow(10, precision)

    def rounder_func(item):
        return func(item * precision) / precision

    result = None

    if pyd.is_number(x):
        result = rounder_func(x)
    elif pyd.is_iterable(x):
        try:
            result = [rounder_func(item) for item in x]
        except TypeError:
            pass

    return result
