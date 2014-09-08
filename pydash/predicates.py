"""Predicate functions that return boolean evaluations of objects.

.. versionadded:: 2.0.0
"""

from __future__ import absolute_import

import datetime
from itertools import islice
import json
import operator
import re

import pydash as pyd
from .helpers import iterator
from ._compat import integer_types, number_types, string_types, izip


__all__ = [
    'is_associative',
    'is_boolean',
    'is_date',
    'is_decreasing',
    'is_empty',
    'is_equal',
    'is_error',
    'is_even',
    'is_float',
    'is_function',
    'is_increasing',
    'is_indexed',
    'is_instance_of',
    'is_integer',
    'is_json',
    'is_list',
    'is_monotone',
    'is_nan',
    'is_negative',
    'is_none',
    'is_number',
    'is_object',
    'is_odd',
    'is_plain_object',
    'is_positive',
    'is_re',
    'is_reg_exp',
    'is_strictly_decreasing',
    'is_strictly_increasing',
    'is_string',
    'is_zero',
]


RegExp = type(re.compile(''))


def is_associative(value):
    """Checks if `value` is an associative object meaning that it can be
    accessed via an index or key

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is associative.

    .. versionadded:: 2.0.0
    """
    return hasattr(value, '__getitem__')


def is_boolean(value):
    """Checks if `value` is a boolean value.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a boolean.

    .. versionadded:: 1.0.0
    """
    return isinstance(value, bool)


def is_date(value):
    """Check if `value` is a date object.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a date object.

    Note:
        This will also return ``True`` for datetime objects.

    .. versionadded:: 1.0.0
    """
    return isinstance(value, datetime.date)


def is_decreasing(value):
    """Check if `value` is monotonically increasing.

    Args:
        value (list): Value to check.

    Returns:
        bool: Whether `value` is monotonically increasing.

    .. versionadded:: 2.0.0
    """
    return is_monotone(value, operator.ge)


def is_empty(value):
    """Checks if `value` is empty.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is empty.

    Note:
        Returns ``True`` for booleans and numbers.

    .. versionadded:: 1.0.0
    """
    return any([is_boolean(value), is_number(value), not value])


def is_equal(a, b, callback=None):
    """Performs a comparison between two values to determine if they are
    equivalent to each other. If a callback is provided it will be executed to
    compare values. If the callback returns ``None``, comparisons will be
    handled by the method instead. The callback is invoked with two arguments:
    ``(a, b)``.

    Args:
        a (list|dict): Object to compare.
        b (list|dict): Object to compare.
        callback (mixed, optional): Callback used to compare values from `a`
            and `b`.

    Returns:
        bool: Whether `a` and `b` are equal.

    .. versionadded:: 1.0.0
    """
    # If callback provided, use it for comparision.
    equal = callback(a, b) if callable(callback) else None

    # Return callback results if anything but None.
    if equal is not None:
        pass
    elif (callable(callback) and
          type(a) is type(b) and
          isinstance(a, (list, dict)) and
          isinstance(b, (list, dict)) and
          len(a) == len(b)):
        # Walk a/b to determine equality using callback.
        for key, value in iterator(a):
            if pyd.has(b, key):
                equal = is_equal(value, b[key], callback)
            else:
                equal = False

            if not equal:
                break
    else:
        # Use basic == comparision.
        equal = a == b

    return equal


def is_error(value):
    """Checks if `value` is an ``Exception``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is an exception.

    .. versionadded:: 1.1.0
    """
    return isinstance(value, Exception)


def is_even(value):
    """Checks if `value` is even.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is even.

    .. versionadded:: 2.0.0
    """
    return is_number(value) and value % 2 == 0


def is_float(value):
    """Checks if `value` is a float.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a float.

    .. versionadded:: 2.0.0
    """
    return isinstance(value, float)


def is_function(value):
    """Checks if `value` is a function.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is callable.

    .. versionadded:: 1.0.0
    """
    return callable(value)


def is_increasing(value):
    """Check if `value` is monotonically increasing.

    Args:
        value (list): Value to check.

    Returns:
        bool: Whether `value` is monotonically increasing.

    .. versionadded:: 2.0.0
    """
    return is_monotone(value, operator.le)


def is_indexed(value):
    """Checks if `value` is integer indexed, i.e., ``list`` or ``str``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is integer indexed.

    .. versionadded:: 2.0.0
    """
    return is_list(value) or is_string(value)


def is_instance_of(value, types):
    """Checks if `value` is an instance of `types`.

    Args:
        value (mixed): Value to check.
        types (mixed): Types to check against. Pass as ``tuple`` to check if
            `value` is one of multiple types.

    Returns:
        bool: Whether `value` is an instance of `types`.

    .. versionadded:: 2.0.0
    """
    return isinstance(value, types)


def is_integer(value):
    """Checks if `value` is a integer.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a integer.

    .. versionadded:: 2.0.0
    """
    return is_number(value) and isinstance(value, integer_types)


def is_json(value):
    """Checks if `value` is a valid JSON string.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is JSON.

    .. versionadded:: 2.0.0
    """
    try:
        json.loads(value)
        return True
    except Exception:  # pylint: disable=broad-except
        return False


def is_list(value):
    """Checks if `value` is a list.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a list.

    .. versionadded:: 1.0.0
    """
    return isinstance(value, list)


def is_monotone(value, op):
    """Checks if `value` is monotonic when `operator` used for comparison.

    Args:
        value (list): Value to check.
        op (function): Operation to used for comparison.

    Returns:
        bool: Whether `value` is monotone.

    .. versionadded:: 2.0.0
    """
    if not is_list(value):
        value = [value]

    search = (False for x, y in izip(value, islice(value, 1, None))
              if not op(x, y))

    return next(search, True)


def is_nan(value):
    """Checks if `value` is not a number.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is not a number.

    .. versionadded:: 1.0.0
    """
    return not is_number(value)


def is_negative(value):
    """Checks if `value` is negative.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is negative.

    .. versionadded:: 2.0.0
    """
    return is_number(value) and value < 0


def is_none(value):
    """Checks if `value` is `None`.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is ``None``.

    .. versionadded:: 1.0.0
    """
    return value is None


def is_number(value):
    """Checks if `value` is a number.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a number.

    Note:
        Returns ``True`` for ``int``, ``long`` (PY2), ``float``, and
        ``decimal.Decimal``.

    .. versionadded:: 1.0.0
    """
    return not is_boolean(value) and isinstance(value, number_types)


def is_object(value):
    """Checks if `value` is a ``list`` or ``dict``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is ``list`` or ``dict``.

    .. versionadded:: 1.0.0
    """
    return isinstance(value, (list, dict))


def is_odd(value):
    """Checks if `value` is odd.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is odd.

    .. versionadded:: 2.0.0
    """
    return is_number(value) and value % 2 != 0


def is_plain_object(value):
    """Checks if `value` is a ``dict``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a ``dict``.

    .. versionadded:: 1.0.0
    """
    return isinstance(value, dict)


def is_positive(value):
    """Checks if `value` is positive.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is positive.

    .. versionadded:: 2.0.0
    """
    return is_number(value) and value > 0


def is_reg_exp(value):
    """Checks if `value` is a ``RegExp`` object.

    Args:
        value (mxied): Value to check.

    Returns:
        bool: Whether `value` is a RegExp object.

    See Also:
        - :func:`is_reg_exp` (main definition)
        - :func:`is_re` (alias)

    .. versionadded:: 1.1.0
    """
    return isinstance(value, RegExp)


is_re = is_reg_exp


def is_strictly_decreasing(value):
    """Check if `value` is strictly decreasing.

    Args:
        value (list): Value to check.

    Returns:
        bool: Whether `value` is strictly decreasing.

    .. versionadded:: 2.0.0
    """
    return is_monotone(value, operator.gt)


def is_strictly_increasing(value):
    """Check if `value` is strictly increasing.

    Args:
        value (list): Value to check.

    Returns:
        bool: Whether `value` is strictly increasing.

    .. versionadded:: 2.0.0
    """
    return is_monotone(value, operator.lt)


def is_string(value):
    """Checks if `value` is a string.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a string.

    .. versionadded:: 1.0.0
    """
    return isinstance(value, string_types)


def is_zero(value):
    """Checks if `value` is ``0``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is ``0``.

    .. versionadded:: 2.0.0
    """
    return value is 0
