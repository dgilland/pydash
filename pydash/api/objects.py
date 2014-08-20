"""Functions that operate on lists, dicts, and other objects.

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import

import copy
import datetime
import re

from .arrays import flatten
from .utilities import (
    identity,
    _iterate,
    _iter_callback,
    _get_item,
    _set_item
)
from .._compat import (
    iteritems,
    number_types,
    string_types,
    text_type
)


__all__ = [
    'assign',
    'clone',
    'clone_deep',
    'defaults',
    'extend',
    'find_key',
    'find_last_key',
    'for_in',
    'for_in_right',
    'for_own',
    'for_own_right',
    'functions',
    'has',
    'invert',
    'is_boolean',
    'is_date',
    'is_empty',
    'is_equal',
    'is_error',
    'is_function',
    'is_list',
    'is_nan',
    'is_none',
    'is_number',
    'is_object',
    'is_plain_object',
    'is_re',
    'is_reg_exp',
    'is_string',
    'keys',
    'keys_in',
    'map_values',
    'merge',
    'methods',
    'omit',
    'pairs',
    'parse_int',
    'pick',
    'transform',
    'update',
    'values',
    'values_in',
]


RegExp = type(re.compile(''))


def assign(obj, *sources, **kargs):
    """Assigns own enumerable properties of source object(s) to the destination
    object.

    Args:
        obj (dict): Destination object whose properties will be modified.
        *sources (dict): Source objects to assign to `obj`.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        dict: Modified `obj`.

    Warning:
        `obj` is modified in place.

    See Also:
        - :func:`assign` (main definition)
        - :func:`extend` (alias)

    .. versionadded:: 1.0.0
    """
    sources = list(sources)
    callback = kargs.get('callback')

    if callback is None and callable(sources[-1]):
        callback = sources.pop()

    for source in sources:
        for key, value in iteritems(source):
            obj[key] = (value if callback is None
                        else callback(obj.get(key), value))

    return obj


extend = assign


def clone(value, is_deep=False, callback=None):
    """Creates a clone of `value`. If `is_deep` is ``True`` nested valueects
    will also be cloned, otherwise they will be assigned by reference. If a
    callback is provided it will be executed to produce the cloned values. The
    callback is invoked with one argument: ``(value)``.

    Args:
        value (list|dict): Object to clone.
        is_deep (bool, optional): Whether to perform deep clone.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        list|dict: Cloned object.

    .. versionadded:: 1.0.0
    """
    if callback is None:
        callback = identity

    copier = copy.deepcopy if is_deep else copy.copy
    value = copier(value)

    obj = [(key, callback(val)) for key, val in _iterate(value)]

    if isinstance(value, list):
        obj = [val for _, val in obj]
    else:
        obj = dict(obj)

    return obj


def clone_deep(value, callback=None):
    """Creates a deep clone of `value`. If a callback is provided it will be
    executed to produce the cloned values. The callback is invoked with one
    argument: ``(value)``.

    Args:
        value (list|dict): Object to clone.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        list|dict: Cloned object.

    .. versionadded:: 1.0.0
    """
    return clone(value, is_deep=True, callback=callback)


def defaults(obj, *sources):
    """Assigns own enumerable properties of source object(s) to the destination
    object for all destination properties that resolve to undefined.

    Args:
        obj (dict): Destination object whose properties will be modified.
        *sources (dict): Source objects to assign to `obj`.

    Returns:
        dict: Modified `obj`.

    Warning:
        `obj` is modified in place.

    .. versionadded:: 1.0.0
    """
    for source in sources:
        for key, value in iteritems(source):
            obj.setdefault(key, value)

    return obj


def find_key(obj, callback=None):
    """This method is like :func:`pydash.api.arrays.find_index` except that it
    returns the key of the first element that passes the callback check,
    instead of the element itself.

    Args:
        obj (list|dict): Object to search.
        callback (mixed): Callback applied per iteration.

    Returns:
        mixed: Found key or ``None``.

    See Also:
        - :func:`find_key` (main definition)
        - :func:`find_last_key` (alias)

    .. versionadded:: 1.0.0
    """
    for result, _, key, _ in _iter_callback(obj, callback):
        if result:
            return key


find_last_key = find_key


def for_in(obj, callback=None):
    """Iterates over own and inherited enumerable properties of `obj`,
    executing `callback` for each property.

    Args:
        obj (list|dict): Object to process.
        callback (mixed): Callback applied per iteration.

    Returns:
        list|dict: `obj`.

    See Also:
        - :func:`for_in` (main definition)
        - :func:`for_own` (alias)

    .. versionadded:: 1.0.0
    """
    for result, _, _, _ in _iter_callback(obj, callback):
        if result is False:
            break

    return obj


for_own = for_in


def for_in_right(obj, callback=None):
    """This function is like :func:`for_in` except it iterates over the
    properties in reverse order.

    Args:
        obj (list|dict): Object to process.
        callback (mixed): Callback applied per iteration.

    Returns:
        list|dict: `obj`.

    See Also:
        - :func:`for_in_right` (main definition)
        - :func:`for_own_right` (alias)

    .. versionadded:: 1.0.0
    """
    for result, _, _, _ in _iter_callback(obj, callback, reverse=True):
        if result is False:
            break

    return obj


for_own_right = for_in_right


def functions(obj):
    """Creates a list of keys of an object that are callable.

    Args:
        obj (list|dict): Object to inspect.

    Returns:
        list: All keys whose values are callable.

    See Also:
        - :func:`functions` (main definition)
        - :func:`methods` (alias)

    .. versionadded:: 1.0.0
    """
    return [key for key, value in _iterate(obj) if callable(value)]


methods = functions


def has(obj, key):
    """Checks if `key` exists as a key of `obj`.

    Args:
        obj (mixed): Object to test.
        key (mixed): Key to test for.

    Returns:
        bool: Whether `obj` has `key`.

    .. versionadded:: 1.0.0
    """
    return key in (key for key, value in _iterate(obj))


def invert(obj):
    """Creates an object composed of the inverted keys and values of the given
    object.

    Args:
        obj (dict): dict to invert

    Returns:
        dict: Inverted dict

    Note:
        Assumes `dict` values are hashable as `dict` keys.

    .. versionadded:: 1.0.0
    """
    return dict((value, key) for key, value in _iterate(obj))


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
        for key, value in _iterate(a):
            if has(b, key):
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


def is_function(value):
    """Checks if `value` is a function.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is callable.

    .. versionadded:: 1.0.0
    """
    return callable(value)


def is_list(value):
    """Checks if `value` is a list.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a list.

    .. versionadded:: 1.0.0
    """
    return isinstance(value, list)


def is_nan(value):
    """Checks if `value` is not a number.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is not a number.

    .. versionadded:: 1.0.0
    """
    return not is_number(value)


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
    return isinstance(value, number_types)


def is_object(value):
    """Checks if `value` is a ``list`` or ``dict``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is ``list`` or ``dict``.

    .. versionadded:: 1.0.0
    """
    return isinstance(value, (list, dict))


def is_plain_object(value):
    """Checks if `value` is a ``dict``.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a ``dict``.

    .. versionadded:: 1.0.0
    """
    return isinstance(value, dict)


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


def is_string(value):
    """Checks if `value` is a string.

    Args:
        value (mixed): Value to check.

    Returns:
        bool: Whether `value` is a string.

    .. versionadded:: 1.0.0
    """
    return isinstance(value, string_types)


def keys(obj):
    """Creates a list composed of the keys of `obj`.

    Args:
        obj (mixed): Object to extract keys from.

    Returns:
        list: List of keys.

    See Also:
        - :func:`keys` (main definition)
        - :func:`keys_in` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
       Added :func:`keys_in` as alias.
    """
    return [key for key, _ in _iterate(obj)]


keys_in = keys


def map_values(obj, callback=None):
    """Creates an object with the same keys as `obj` and values generated by
    running each property of `obj` through the `callback`. The callback is
    invoked with three arguments: ``(value, key, object)``. If a property name
    is provided for `callback` the created :func:`pydash.api.collections.pluck`
    style callback will return the property value of the given element. If an
    object is provided for callback the created
    :func:`pydash.api.collections.where` style callback will return ``True``
    for elements that have the properties of the given object, else ``False``.

    Args:
        obj (list|dict): Object to map.
        callback (mixed): Callback applied per iteration.

    Returns:
        list|dict: Results of running `obj` through `callback`.

    .. versionadded:: 1.0.0
    """
    ret = {}

    for result, _, key, _ in _iter_callback(obj, callback):
        ret[key] = result

    return ret


def merge(obj, *sources, **kargs):
    """Recursively merges own enumerable properties of the source object(s)
    that don't resolve to undefined into the destination object. Subsequent
    sources will overwrite property assignments of previous sources. If a
    callback is provided it will be executed to produce the merged values of
    the destination and source properties. If the callback returns undefined
    merging will be handled by the method instead. The callback is invoked with
    two arguments: ``(obj_value, source_value)``.

    Args:
        obj (dict): Destination object to merge source(s) into.
        *sources (dict): Source objects to merge from. subsequent sources
            overwrite previous ones.

    Keyword Args:
        callback (function, optional): Callback function to handle merging
            (must be passed in as keyword argument).

    Returns:
        dict: Merged object.

    Warning:
        `obj` is modified in place.

    .. versionadded:: 1.0.0
    """
    callback = kargs.get('callback')

    for source in sources:
        update(obj, source, callback)

    return obj


def omit(obj, callback=None, *properties):
    """Creates a shallow clone of object excluding the specified properties.
    Property names may be specified as individual arguments or as lists of
    property names. If a callback is provided it will be executed for each
    property of object omitting the properties the callback returns truthy for.
    The callback is invoked with three arguments: ``(value, key, object)``.

    Args:
        obj (mixed): Object to process.
        *properties (str): Property values to omit.
        callback (mixed, optional): Callback used to determine whic properties
            to omit.

    Returns:
        dict: Results of omitting properties.

    .. versionadded:: 1.0.0
    """
    if not callable(callback):
        callback = callback if callback is not None else []
        properties = flatten([callback, properties])
        callback = lambda value, key, item: key in properties

    return dict((key, value) for key, value in _iterate(obj)
                if not callback(value, key, obj))


def pairs(obj):
    """Creates a two dimensional list of an object's key-value pairs, i.e.
    ``[[key1, value1], [key2, value2]]``.

    Args:
        obj (mixed): Object to process.

    Returns:
        list: Two dimensional list of object's key-value pairs.

    .. versionadded:: 1.0.0
    """
    return [[key, value] for key, value in _iterate(obj)]


def parse_int(value, radix=None):
    """Converts the given `value` into an integer of the specified `radix`. If
    `radix` is falsey a radix of ``10`` is used unless the `value` is a
    hexadecimal, in which case a radix of 16 is used.

    Args:
        value (mixed): Value to parse.
        radix (int, optional): Base to convert to.

    Returns:
        mixed: Integer if parsable else ``None``.

    .. versionadded:: 1.0.0
    """
    if not radix and is_string(value):
        try:
            # Check if value is hexadcimal and if so use base-16 conversion.
            int(value, 16)
        except ValueError:
            pass
        else:
            radix = 16

    if not radix:
        radix = 10

    try:
        # NOTE: Must convert value to string when supplying radix to int().
        # Dropping radix arg when 10 is needed to allow floats to parse
        # correctly.
        args = (value,) if radix == 10 else (text_type(value), radix)
        parsed = int(*args)
    except (ValueError, TypeError):
        parsed = None

    return parsed


def pick(obj, callback=None, *properties):
    """Creates a shallow clone of object composed of the specified properties.
    Property names may be specified as individual arguments or as lists of
    property names. If a callback is provided it will be executed for each
    property of object picking the properties the callback returns truthy for.
    The callback is invoked with three arguments: ``(value, key, object)``.

    Args:
        obj (list|dict): Object to pick from.
        *properties (str): Property values to pick.
        callback (mixed, optional): Callback used to determine whic properties
            to pick.

    Returns:
        dict: Results of picking properties.

    .. versionadded:: 1.0.0
    """
    if not callable(callback):
        callback = callback if callback is not None else []
        properties = flatten([callback, properties])
        callback = lambda value, key, item: key in properties

    return dict((key, value) for key, value in _iterate(obj)
                if callback(value, key, obj))


def transform(obj, callback=None, accumulator=None):
    """An alternative to :func:`pydash.api.collections.reduce`, this method
    transforms `obj` to a new accumulator object which is the result of running
    each of its properties through a callback, with each callback execution
    potentially mutating the accumulator object. The callback is invoked with
    four arguments: ``(accumulator, value, key, object)``. Callbacks may exit
    iteration early by explicitly returning ``False``.

    Args:
        obj (list|dict): Object to process.
        callback (mixed): Callback applied per iteration.
        accumulator (mixed, optional): Accumulated object. Defaults to
            ``list``.

    Returns:
        mixed: Accumulated object.

    .. versionadded:: 1.0.0
    """
    if callback is None:
        callback = lambda accumulator, *args: accumulator

    if accumulator is None:
        accumulator = []

    for key, value in _iterate(obj):
        result = callback(accumulator, value, key, obj)
        if result is False:
            break

    return accumulator


def update(obj, source, callback=None):
    """Update properties of `obj` with `source`. If a callback is provided,
    it will be executed to produce the updated values of the destination and
    source properties. The callback is invoked with two arguments:
    ``(obj_value, source_value)``.

    Args:
        obj (dict): destination object to merge source(s) into
        source (dict): source object to merge from
        callback (function, optional): callback function to handle merging

    Returns:
        mixed: merged object

    Warning:
        `obj` is modified in place.

    .. versionadded:: 1.0.0
    """

    for key, src_value in _iterate(source):
        obj_value = _get_item(obj, key, default=None)
        is_sequences = all([src_value,
                            isinstance(src_value, list),
                            isinstance(obj_value, list)])
        is_mappings = all([src_value,
                           isinstance(src_value, dict),
                           isinstance(obj_value, dict)])

        if (is_sequences or is_mappings) and not callback:
            result = update(obj_value, src_value)
        elif callback:
            result = callback(obj_value, src_value)
        else:
            result = src_value

        _set_item(obj, key, result)

    return obj


def values(obj):
    """Creates a list composed of the values of `obj`.

    Args:
        obj (mixed): Object to extract values from.

    Returns:
        list: List of values.

    See Also:
        - :func:`values` (main definition)
        - :func:`values_in` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
       Added :func:`values_in` as alias.
    """
    return [value for _, value in _iterate(obj)]


values_in = values
