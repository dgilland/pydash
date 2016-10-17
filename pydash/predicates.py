# -*- coding: utf-8 -*-
"""Predicate functions that return boolean evaluations of objects.

.. versionadded:: 2.0.0
"""

from __future__ import absolute_import

import datetime
from itertools import islice
import json
import operator
import re
from types import BuiltinFunctionType

import pydash as pyd
from .helpers import iterator
from ._compat import (
    builtins,
    integer_types,
    izip,
    number_types,
    string_types
)


__all__ = (
    'gt',
    'gte',
    'lt',
    'lte',
    'in_range',
    'is_associative',
    'is_blank',
    'is_boolean',
    'is_bool',
    'is_builtin',
    'is_date',
    'is_decreasing',
    'is_dict',
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
    'is_int',
    'is_iterable',
    'is_json',
    'is_list',
    'is_match',
    'is_monotone',
    'is_nan',
    'is_native',
    'is_negative',
    'is_none',
    'is_number',
    'is_num',
    'is_object',
    'is_odd',
    'is_plain_object',
    'is_positive',
    'is_re',
    'is_reg_exp',
    'is_strictly_decreasing',
    'is_strictly_increasing',
    'is_string',
    'is_tuple',
    'is_zero',
)


RegExp = type(re.compile(''))


def gt(value, other):
    """Checks if `value` is greater than `other`.

    Args:
        value (number): Value to compare.
        other (number): Other value to compare.

    Returns:
        bool: Whether `value` is greater than `other`.

    Example:

        >>> gt(5, 3)
        True
        >>> gt(3, 5)
        False
        >>> gt(5, 5)
        False

    .. versionadded:: 3.3.0
    """
    return value > other


def gte(value, other):
    """Checks if `value` is greater than or equal to `other`.

    Args:
        value (number): Value to compare.
        other (number): Other value to compare.

    Returns:
        bool: Whether `value` is greater than or equal to `other`.

    Example:

        >>> gte(5, 3)
        True
        >>> gte(3, 5)
        False
        >>> gte(5, 5)
        True

    .. versionadded:: 3.3.0
    """
    return value >= other


def lt(value, other):
    """Checks if `value` is less than `other`.

    Args:
        value (number): Value to compare.
        other (number): Other value to compare.

    Returns:
        bool: Whether `value` is less than `other`.

    Example:

        >>> lt(5, 3)
        False
        >>> lt(3, 5)
        True
        >>> lt(5, 5)
        False

    .. versionadded:: 3.3.0
    """
    return value < other


def lte(value, other):
    """Checks if `value` is less than or equal to `other`.

    Args:
        value (number): Value to compare.
        other (number): Other value to compare.

    Returns:
        bool: Whether `value` is less than or equal to `other`.

    Example:

        >>> lte(5, 3)
        False
        >>> lte(3, 5)
        True
        >>> lte(5, 5)
        True

    .. versionadded:: 3.3.0
    """
    return value <= other


def in_range(value, start=0, end=None):
    """Checks if `value` is between `start` and up to but not including `end`.
    If `end` is not specified it defaults to `start` with `start` becoming
    ``0``.

    Args:

        value (int|float): Number to check.
        start (int|float, optional): Start of range inclusive. Defaults to
            ``0``.
        end (int|float, optional): End of range exclusive. Defaults to `start`.

    Returns:
        bool: Whether `value` is in range.

    Example:

        >>> in_range(2, 4)
        True
        >>> in_range(4, 2)
        False
        >>> in_range(2, 1, 3)
        True
        >>> in_range(3, 1, 2)
        False
        >>> in_range(2.5, 3.5)
        True
        >>> in_range(3.5, 2.5)
        False

    .. versionadded:: 3.1.0
    """
    if not is_number(value):
        return False

    if not is_number(start):
        start = 0

    if end is None:
        end = start
        start = 0
    elif not is_number(end):
        end = 0

    return start <= value < end


def is_associative(value):
    """Checks if `value` is an associative object meaning that it can be
    accessed via an index or key

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is associative.

    Example:

        >>> is_associative([])
        True
        >>> is_associative({})
        True
        >>> is_associative(1)
        False
        >>> is_associative(True)
        False

    .. versionadded:: 2.0.0
    """
    return hasattr(value, '__getitem__')


def is_blank(text):
    r"""Checks if `text` contains only whitespace characters.

    Args:
        text (str): String to test.

    Returns:
        bool: Whether `text` is blank.

    Example:

        >>> is_blank('')
        True
        >>> is_blank(' \r\n ')
        True
        >>> is_blank(False)
        False

    .. versionadded:: 3.0.0
    """
    try:
        ret = bool(re.match(r'^(\s+)?$', text))
    except TypeError:
        ret = False

    return ret


def is_boolean(value):
    """Checks if `value` is a boolean value.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a boolean.

    Example:

        >>> is_boolean(True)
        True
        >>> is_boolean(False)
        True
        >>> is_boolean(0)
        False

    See Also:
        - :func:`is_boolean` (main definition)
        - :func:`is_bool` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 3.0.0
        Added ``is_bool`` as alias.
    """
    return isinstance(value, bool)


is_bool = is_boolean


def is_builtin(value):
    """Checks if `value` is a Python builtin function or method.

    Args:
        value (function): Value to check.

    Returns:
        bool: Whether `value` is a Python builtin function or method.

    Example:

        >>> is_builtin(1)
        True
        >>> is_builtin(list)
        True
        >>> is_builtin('foo')
        False

    See Also:
        - :func:`is_builtin` (main definition)
        - :func:`is_native` (alias)

    .. versionadded:: 3.0.0
    """
    try:
        return isinstance(value, BuiltinFunctionType) or value in builtins
    except TypeError:  # pragma: no cover
        return False


is_native = is_builtin


def is_date(value):
    """Check if `value` is a date object.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a date object.

    Example:

        >>> import datetime
        >>> is_date(datetime.date.today())
        True
        >>> is_date(datetime.datetime.today())
        True
        >>> is_date('2014-01-01')
        False

    Note:
        This will also return ``True`` for datetime objects.

    .. versionadded:: 1.0.0
    """
    return isinstance(value, datetime.date)


def is_decreasing(value):
    """Check if `value` is monotonically decreasing.

    Args:
        value (list): Value to check.

    Returns:
        bool: Whether `value` is monotonically decreasing.

    Example:

        >>> is_decreasing([5, 4, 4, 3])
        True
        >>> is_decreasing([5, 5, 5])
        True
        >>> is_decreasing([5, 4, 5])
        False

    .. versionadded:: 2.0.0
    """
    return is_monotone(value, operator.ge)


def is_dict(value):
    """Checks if `value` is a ``dict``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a ``dict``.

    Example:

        >>> is_dict({})
        True
        >>> is_dict([])
        False

    See Also:
        - :func:`is_dict` (main definition)
        - :func:`is_plain_object` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 3.0.0
        Added :func:`is_dict` as main definition and made
        :func:`is_plain_object` an alias.
    """
    return isinstance(value, dict)


is_plain_object = is_dict


def is_empty(value):
    """Checks if `value` is empty.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is empty.

    Example:

        >>> is_empty(0)
        True
        >>> is_empty(1)
        True
        >>> is_empty(True)
        True
        >>> is_empty('foo')
        False
        >>> is_empty(None)
        True
        >>> is_empty({})
        True

    Note:
        Returns ``True`` for booleans and numbers.

    .. versionadded:: 1.0.0
    """
    return any([is_boolean(value), is_number(value), not value])


def is_equal(value, other, callback=None):
    """Performs a comparison between two values to determine if they are
    equivalent to each other. If a callback is provided it will be executed to
    compare values. If the callback returns ``None``, comparisons will be
    handled by the method instead. The callback is invoked with two arguments:
    ``(value, other)``.

    Args:
        value (list|dict): Object to compare.
        other (list|dict): Object to compare.
        callback (mixed, optional): Callback used to compare values from
            `value` and `other`.

    Returns:
        bool: Whether `value` and `other` are equal.

    Example:

        >>> is_equal([1, 2, 3], [1, 2, 3])
        True
        >>> is_equal('a', 'A')
        False
        >>> is_equal('a', 'A', lambda a, b: a.lower() == b.lower())
        True

    .. versionadded:: 1.0.0
    """
    # If callback provided, use it for comparision.
    equal = callback(value, other) if callable(callback) else None

    # Return callback results if anything but None.
    if equal is not None:
        pass
    elif (callable(callback) and
          type(value) is type(other) and
          isinstance(value, (list, dict)) and
          isinstance(other, (list, dict)) and
          len(value) == len(other)):
        # Walk a/b to determine equality using callback.
        for key, value in iterator(value):
            if pyd.has(other, key):
                equal = is_equal(value, other[key], callback)
            else:
                equal = False

            if not equal:
                break
    else:
        # Use basic == comparision.
        equal = value == other

    return equal


def is_error(value):
    """Checks if `value` is an ``Exception``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is an exception.

    Example:

        >>> is_error(Exception())
        True
        >>> is_error(Exception)
        False
        >>> is_error(None)
        False

    .. versionadded:: 1.1.0
    """
    return isinstance(value, Exception)


def is_even(value):
    """Checks if `value` is even.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is even.

    Example:

        >>> is_even(2)
        True
        >>> is_even(3)
        False
        >>> is_even(False)
        False

    .. versionadded:: 2.0.0
    """
    return is_number(value) and value % 2 == 0


def is_float(value):
    """Checks if `value` is a float.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a float.

    Example:

        >>> is_float(1.0)
        True
        >>> is_float(1)
        False

    .. versionadded:: 2.0.0
    """
    return isinstance(value, float)


def is_function(value):
    """Checks if `value` is a function.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is callable.

    Example:

        >>> is_function(list)
        True
        >>> is_function(lambda: True)
        True
        >>> is_function(1)
        False

    .. versionadded:: 1.0.0
    """
    return callable(value)


def is_increasing(value):
    """Check if `value` is monotonically increasing.

    Args:
        value (list): Value to check.

    Returns:
        bool: Whether `value` is monotonically increasing.

    Example:

        >>> is_increasing([1, 3, 5])
        True
        >>> is_increasing([1, 1, 2, 3, 3])
        True
        >>> is_increasing([5, 5, 5])
        True
        >>> is_increasing([1, 2, 4, 3])
        False

    .. versionadded:: 2.0.0
    """
    return is_monotone(value, operator.le)


def is_indexed(value):
    """Checks if `value` is integer indexed, i.e., ``list``, ``str`` or
    ``tuple``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is integer indexed.

    Example:

        >>> is_indexed('')
        True
        >>> is_indexed([])
        True
        >>> is_indexed(())
        True
        >>> is_indexed({})
        False

    .. versionadded:: 2.0.0

    .. versionchanged:: 3.0.0
        Return ``True`` for tuples.
    """
    return isinstance(value, (list, tuple, string_types))


def is_instance_of(value, types):
    """Checks if `value` is an instance of `types`.

    Args:
        value (mixed): Value to check.
        types (mixed): Types to check against. Pass as ``tuple`` to check if
            `value` is one of multiple types.

    Returns:
        bool: Whether `value` is an instance of `types`.

    Example:

        >>> is_instance_of({}, dict)
        True
        >>> is_instance_of({}, list)
        False

    .. versionadded:: 2.0.0
    """
    return isinstance(value, types)


def is_integer(value):
    """Checks if `value` is a integer.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is an integer.

    Example:

        >>> is_integer(1)
        True
        >>> is_integer(1.0)
        False
        >>> is_integer(True)
        False

    See Also:
        - :func:`is_integer` (main definition)
        - :func:`is_int` (alias)

    .. versionadded:: 2.0.0

    .. versionchanged:: 3.0.0
        Added ``is_int`` as alias.
    """
    return is_number(value) and isinstance(value, integer_types)


is_int = is_integer


def is_iterable(value):
    """Checks if `value` is an iterable.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is an iterable.

    Example:

        >>> is_iterable([])
        True
        >>> is_iterable({})
        True
        >>> is_iterable(())
        True
        >>> is_iterable(5)
        False
        >>> is_iterable(True)
        False

    .. versionadded:: 3.3.0
    """
    try:
        iter(value)
    except TypeError:
        return False
    else:
        return True


def is_json(value):
    """Checks if `value` is a valid JSON string.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is JSON.

    Example:

        >>> is_json({})
        False
        >>> is_json('{}')
        True
        >>> is_json({"hello": 1, "world": 2})
        False
        >>> is_json('{"hello": 1, "world": 2}')
        True

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

    Example:

        >>> is_list([])
        True
        >>> is_list({})
        False
        >>> is_list(())
        False

    .. versionadded:: 1.0.0
    """
    return isinstance(value, list)


def is_match(obj, source, callback=None):
    """Performs a comparison between `obj` and `source` to determine if `obj`
    contains equivalent property values as `source`. If a callback is provided
    it will be executed to compare values. If the callback returns ``None``,
    comparisons will be handled by the method instead. The callback is invoked
    with two arguments: ``(obj, source)``.

    Args:
        obj (list|dict): Object to compare.
        source (list|dict): Object of property values to match.
        callback (mixed, optional): Callback used to compare values from `obj`
            and `source`.

    Returns:
        bool: Whether `obj` is a match or not.


    Example:

        >>> is_match({'a': 1, 'b': 2}, {'b': 2})
        True
        >>> is_match({'a': 1, 'b': 2}, {'b': 3})
        False
        >>> is_match({'a': [{'b': [{'c': 3, 'd': 4}]}]},\
                     {'a': [{'b': [{'d': 4}]}]})
        True

    .. versionadded:: 3.0.0

    .. versionchanged:: 3.2.0
        Don't compare `obj` and `source` using ``type``. Use ``isinstance``
        exclusively.
    """
    # If callback provided, use it for comparision.
    equal = callback(obj, source) if callable(callback) else None

    # Return callback results if anything but None.
    if equal is not None:
        pass
    elif (isinstance(obj, dict) and isinstance(source, dict) or
          isinstance(obj, list) and isinstance(source, list) or
          isinstance(obj, tuple) and isinstance(source, tuple)):
        # Set equal to True if source is empty, otherwise, False and then allow
        # deep comparison to determine equality.
        equal = not source

        # Walk a/b to determine equality.
        for key, value in iterator(source):
            try:
                equal = is_match(obj[key], value, callback)
            except Exception:  # pylint: disable=broad-except
                equal = False

            if not equal:
                break
    else:
        # Use basic == comparision.
        equal = obj == source

    return equal


def is_monotone(value, op):
    """Checks if `value` is monotonic when `operator` used for comparison.

    Args:
        value (list): Value to check.
        op (function): Operation to used for comparison.

    Returns:
        bool: Whether `value` is monotone.

    Example:

        >>> is_monotone([1, 1, 2, 3], operator.le)
        True
        >>> is_monotone([1, 1, 2, 3], operator.lt)
        False

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

    Example:

        >>> is_nan('a')
        True
        >>> is_nan(1)
        False
        >>> is_nan(1.0)
        False

    .. versionadded:: 1.0.0
    """
    return not is_number(value)


def is_negative(value):
    """Checks if `value` is negative.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is negative.

    Example:

        >>> is_negative(-1)
        True
        >>> is_negative(0)
        False
        >>> is_negative(1)
        False

    .. versionadded:: 2.0.0
    """
    return is_number(value) and value < 0


def is_none(value):
    """Checks if `value` is `None`.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is ``None``.

    Example:

        >>> is_none(None)
        True
        >>> is_none(False)
        False

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

    Example:

        >>> is_number(1)
        True
        >>> is_number(1.0)
        True
        >>> is_number('a')
        False

    See Also:
        - :func:`is_number` (main definition)
        - :func:`is_num` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 3.0.0
        Added ``is_num`` as alias.
    """
    return not is_boolean(value) and isinstance(value, number_types)


is_num = is_number


def is_object(value):
    """Checks if `value` is a ``list`` or ``dict``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is ``list`` or ``dict``.

    Example:

        >>> is_object([])
        True
        >>> is_object({})
        True
        >>> is_object(())
        False
        >>> is_object(1)
        False

    .. versionadded:: 1.0.0
    """
    return isinstance(value, (list, dict))


def is_odd(value):
    """Checks if `value` is odd.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is odd.

    Example:

        >>> is_odd(3)
        True
        >>> is_odd(2)
        False
        >>> is_odd('a')
        False

    .. versionadded:: 2.0.0
    """
    return is_number(value) and value % 2 != 0


def is_positive(value):
    """Checks if `value` is positive.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is positive.

    Example:

        >>> is_positive(1)
        True
        >>> is_positive(0)
        False
        >>> is_positive(-1)
        False

    .. versionadded:: 2.0.0
    """
    return is_number(value) and value > 0


def is_reg_exp(value):
    """Checks if `value` is a ``RegExp`` object.

    Args:
        value (mxied): Value to check.

    Returns:
        bool: Whether `value` is a RegExp object.

    Example:

        >>> is_reg_exp(re.compile(''))
        True
        >>> is_reg_exp('')
        False

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

    Example:

        >>> is_strictly_decreasing([4, 3, 2, 1])
        True
        >>> is_strictly_decreasing([4, 4, 2, 1])
        False

    .. versionadded:: 2.0.0
    """
    return is_monotone(value, operator.gt)


def is_strictly_increasing(value):
    """Check if `value` is strictly increasing.

    Args:
        value (list): Value to check.

    Returns:
        bool: Whether `value` is strictly increasing.

    Example:

        >>> is_strictly_increasing([1, 2, 3, 4])
        True
        >>> is_strictly_increasing([1, 1, 3, 4])
        False

    .. versionadded:: 2.0.0
    """
    return is_monotone(value, operator.lt)


def is_string(value):
    """Checks if `value` is a string.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a string.

    Example:

        >>> is_string('')
        True
        >>> is_string(1)
        False

    .. versionadded:: 1.0.0
    """
    return isinstance(value, string_types)


def is_tuple(value):
    """Checks if `value` is a tuple.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a tuple.

    Example:

        >>> is_tuple(())
        True
        >>> is_tuple({})
        False
        >>> is_tuple([])
        False

    .. versionadded:: 3.0.0
    """
    return isinstance(value, tuple)


def is_zero(value):
    """Checks if `value` is ``0``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is ``0``.

    Example:

        >>> is_zero(0)
        True
        >>> is_zero(1)
        False

    .. versionadded:: 2.0.0
    """
    return value is 0
