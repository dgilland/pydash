# -*- coding: utf-8 -*-
"""Functions that operate on lists, dicts, and other objects.

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import

import copy
import math
import re

import pydash as pyd
from .helpers import (
    iterator,
    itercallback,
    get_item,
    set_item,
    NoValue,
    callit,
    getargcount
)
from ._compat import iteritems, text_type


__all__ = (
    'assign',
    'callables',
    'clone',
    'clone_deep',
    'deep_get',
    'deep_has',
    'deep_set',
    'deep_map_values',
    'defaults',
    'defaults_deep',
    'extend',
    'find_key',
    'find_last_key',
    'for_in',
    'for_in_right',
    'for_own',
    'for_own_right',
    'get',
    'get_path',
    'has',
    'has_path',
    'invert',
    'keys',
    'keys_in',
    'map_keys',
    'map_values',
    'merge',
    'methods',
    'omit',
    'pairs',
    'parse_int',
    'pick',
    'rename_keys',
    'set_',
    'set_path',
    'to_boolean',
    'to_dict',
    'to_number',
    'to_plain_object',
    'to_string',
    'transform',
    'update_path',
    'values',
    'values_in',
)


# These regexes are used in path_keys() to parse deep path strings.

# This is used to split a deep path string into dict keys or list indexex.
# This matches "." as delimiter (unless it is escaped by "//") and
# "[<integer>]" as delimiter while keeping the "[<integer>]" as an item.
RE_PATH_KEY_DELIM = re.compile(r'(?<!\\)(?:\\\\)*\.|(\[\d+\])')

# Matches on path strings like "[<integer>]". This is used to test whether a
# path string part is a list index.
RE_PATH_LIST_INDEX = re.compile(r'^\[\d+\]$')


def assign(obj, *sources, **kargs):
    """Assigns own enumerable properties of source object(s) to the destination
    object. If `callback` is supplied, it is invoked with two arguments:
    ``(obj_value, source_value)``.

    Args:
        obj (dict): Destination object whose properties will be modified.
        sources (dict): Source objects to assign to `obj`.

    Keyword Args:
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        dict: Modified `obj`.

    Warning:
        `obj` is modified in place.

    Example:

        >>> obj = {}
        >>> obj2 = assign(obj, {'a': 1}, {'b': 2}, {'c': 3})
        >>> obj == {'a': 1, 'b': 2, 'c': 3}
        True
        >>> obj is obj2
        True

    See Also:
        - :func:`assign` (main definition)
        - :func:`extend` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.3.2
        Apply :func:`clone_deep` to each `source` before assigning to `obj`.

    .. versionchanged:: 3.0.0
        Allow callbacks to accept partial arguments.

    .. versionchanged:: 3.4.4
        Shallow copy each `source` instead of deep copying.
    """
    sources = list(sources)
    callback = kargs.get('callback')

    if callback is None and callable(sources[-1]):
        callback = sources.pop()

    argcount = (getargcount(callback, maxargs=2) if callback is not None
                else None)

    for source in sources:
        source = source.copy()

        for key, value in iteritems(source):
            obj[key] = (value if callback is None
                        else callit(callback,
                                    obj.get(key),
                                    value,
                                    argcount=argcount))

    return obj


extend = assign


def callables(obj):
    """Creates a sorted list of keys of an object that are callable.

    Args:
        obj (list|dict): Object to inspect.

    Returns:
        list: All keys whose values are callable.

    Example:

        >>> callables({'a': 1, 'b': lambda: 2, 'c': lambda: 3})
        ['b', 'c']

    See Also:
        - :func:`callables` (main definition)
        - :func:`methods` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.0.0
        Renamed ``functions`` to ``callables``.
    """
    return sorted(key for key, value in iterator(obj) if callable(value))


methods = callables


def clone(value, is_deep=False, callback=None):
    """Creates a clone of `value`. If `is_deep` is ``True`` nested valueects
    will also be cloned, otherwise they will be assigned by reference. If a
    callback is provided it will be executed to produce the cloned values. The
    callback is invoked with one argument: ``(value)``.

    Args:
        value (list|dict): Object to clone.
        is_deep (bool, optional): Whether to perform deep clone.
        callback (mixed, optional): Callback applied per iteration.

    Example:

        >>> x = {'a': 1, 'b': 2, 'c': {'d': 3}}
        >>> y = clone(x)
        >>> y == y
        True
        >>> x is y
        False
        >>> x['c'] is y['c']
        True
        >>> z = clone(x, is_deep=True)
        >>> x == z
        True
        >>> x['c'] is z['c']
        False

    Returns:
        list|dict: Cloned object.

    .. versionadded:: 1.0.0
    """
    if callback is None:
        callback = pyd.identity

    copier = copy.deepcopy if is_deep else copy.copy
    value = copier(value)

    obj = [(key, callback(val)) for key, val in iterator(value)]

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

    Example:

        >>> x = {'a': 1, 'b': 2, 'c': {'d': 3}}
        >>> y = clone_deep(x)
        >>> y == y
        True
        >>> x is y
        False
        >>> x['c'] is y['c']
        False

    .. versionadded:: 1.0.0
    """
    return clone(value, is_deep=True, callback=callback)


def deep_map_values(obj, callback=None, property_path=NoValue):
    """Map all non-object values in `obj` with return values from `callback`.
    The callback is invoked with two arguments: ``(obj_value, property_path)``
    where ``property_path`` contains the list of path keys corresponding to the
    path of ``obj_value``.

    Args:
        obj (list|dict): Object to map.
        callback (function): Callback applied to each value.

    Returns:
        mixed: The modified object.

    Warning:
        `obj` is modified in place.

    Example:

        >>> x = {'a': 1, 'b': {'c': 2}}
        >>> y = deep_map_values(x, lambda val: val * 2)
        >>> y == {'a': 2, 'b': {'c': 4}}
        True
        >>> z = deep_map_values(x, lambda val, props: props)
        >>> z == {'a': ['a'], 'b': {'c': ['b', 'c']}}
        True

    .. versionadded: 2.2.0

    .. versionchanged:: 3.0.0
        Allow callbacks to accept partial arguments.
    """
    properties = path_keys(property_path)

    if pyd.is_object(obj):
        deep_callback = (
            lambda value, key: deep_map_values(value,
                                               callback,
                                               pyd.flatten([properties, key])))
        return pyd.extend(obj, map_values(obj, deep_callback))
    else:
        return callit(callback, obj, properties)


def defaults(obj, *sources):
    """Assigns own enumerable properties of source object(s) to the destination
    object for all destination properties that resolve to undefined.

    Args:
        obj (dict): Destination object whose properties will be modified.
        sources (dict): Source objects to assign to `obj`.

    Returns:
        dict: Modified `obj`.

    Warning:
        `obj` is modified in place.

    Example:

        >>> obj = {'a': 1}
        >>> obj2 = defaults(obj, {'b': 2}, {'c': 3}, {'a': 4})
        >>> obj is obj2
        True
        >>> obj == {'a': 1, 'b': 2, 'c': 3}
        True

    .. versionadded:: 1.0.0
    """
    for source in sources:
        for key, value in iteritems(source):
            obj.setdefault(key, value)

    return obj


def defaults_deep(obj, *sources):
    """This method is like :func:`defaults` except that it recursively assigns
    default properties.

    Args:
        obj (dict): Destination object whose properties will be modified.
        sources (dict): Source objects to assign to `obj`.

    Returns:
        dict: Modified `obj`.

    Warning:
        `obj` is modified in place.

    Example:

        >>> obj = {'a': {'b': 1}}
        >>> obj2 = defaults_deep(obj, {'a': {'b': 2, 'c': 3}})
        >>> obj is obj2
        True
        >>> obj == {'a': {'b': 1, 'c': 3}}
        True

    .. versionadded:: 3.3.0
    """
    def setter(obj, key, value):
        obj.setdefault(key, value)

    return merge(obj, *sources, _setter=setter)


def find_key(obj, callback=None):
    """This method is like :func:`pydash.arrays.find_index` except that it
    returns the key of the first element that passes the callback check,
    instead of the element itself.

    Args:
        obj (list|dict): Object to search.
        callback (mixed): Callback applied per iteration.

    Returns:
        mixed: Found key or ``None``.

    Example:

        >>> find_key({'a': 1, 'b': 2, 'c': 3}, lambda x: x == 1)
        'a'
        >>> find_key([1, 2, 3, 4], lambda x: x == 1)
        0

    See Also:
        - :func:`find_key` (main definition)
        - :func:`find_last_key` (alias)

    .. versionadded:: 1.0.0
    """
    for result, _, key, _ in itercallback(obj, callback):
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

    Example:

        >>> obj = {}
        >>> def cb(v, k): obj[k] = v
        >>> results = for_in({'a': 1, 'b': 2, 'c': 3}, cb)
        >>> results == {'a': 1, 'b': 2, 'c': 3}
        True
        >>> obj == {'a': 1, 'b': 2, 'c': 3}
        True

    See Also:
        - :func:`for_in` (main definition)
        - :func:`for_own` (alias)

    .. versionadded:: 1.0.0
    """
    walk = (None for ret, _, _, _ in itercallback(obj, callback)
            if ret is False)
    next(walk, None)
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

    Example:

        >>> data = {'product': 1}
        >>> def cb(v): data['product'] *= v
        >>> for_in_right([1, 2, 3, 4], cb)
        [1, 2, 3, 4]
        >>> data['product'] == 24
        True

    See Also:
        - :func:`for_in_right` (main definition)
        - :func:`for_own_right` (alias)

    .. versionadded:: 1.0.0
    """
    walk = (None for ret, _, _, _ in itercallback(obj, callback, reverse=True)
            if ret is False)
    next(walk, None)
    return obj


for_own_right = for_in_right


def get(obj, path, default=None):
    """Get the value at any depth of a nested object based on the path
    described by `path`. If path doesn't exist, `default` is returned.

    Args:
        obj (list|dict): Object to process.
        path (str|list): List or ``.`` delimited string of path describing
            path.

    Keyword Arguments:
        default (mixed): Default value to return if path doesn't exist.
            Defaults to ``None``.

    Returns:
        mixed: Value of `obj` at path.

    Example:

        >>> get({}, 'a.b.c') is None
        True
        >>> get({'a': {'b': {'c': [1, 2, 3, 4]}}}, 'a.b.c.1')
        2
        >>> get({'a': {'b': [0, {'c': [1, 2]}]}}, 'a.b.1.c.1')
        2
        >>> get({'a': {'b': [0, {'c': [1, 2]}]}}, 'a.b.1.c.2') is None
        True

    See Also:
        - :func:`get` (main definition)
        - :func:`get_path` (alias)
        - :func:`deep_get` (alias)

    .. versionadded:: 2.0.0

    .. versionchanged:: 2.2.0
        Support escaping "." delimiter in single string path key.

    .. versionchanged:: 3.3.0

        - Added :func:`get` as main definition and :func:`get_path` as alias.
        - Made :func:`deep_get` an alias.
    """
    for key in path_keys(path):
        obj = get_item(obj, key, default=default)
        if obj is None:
            break

    return obj


get_path = get
deep_get = get


def has(obj, path):
    """Checks if `path` exists as a key of `obj`.

    Args:
        obj (mixed): Object to test.
        path (mixed): Path to test for. Can be a list of nested keys or a ``.``
            delimited string of path describing the path.

    Returns:
        bool: Whether `obj` has `path`.

    Example:

        >>> has([1, 2, 3], 1)
        True
        >>> has({'a': 1, 'b': 2}, 'b')
        True
        >>> has({'a': 1, 'b': 2}, 'c')
        False
        >>> has({'a': {'b': [0, {'c': [1, 2]}]}}, 'a.b.1.c.1')
        True
        >>> has({'a': {'b': [0, {'c': [1, 2]}]}}, 'a.b.1.c.2')
        False

    See Also:
        - :func:`has` (main definition)
        - :func:`deep_has` (alias)
        - :func:`has_path` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 3.0.0
        Return ``False`` on ``ValueError`` when checking path.

    .. versionchanged:: 3.3.0

        - Added :func:`deep_has` as alias.
        - Added :func:`has_path` as alias.
    """
    try:
        get(obj, path, default=NoValue)
        exists = True
    except (KeyError, IndexError, TypeError, ValueError):
        exists = False

    return exists


deep_has = has
has_path = has


def invert(obj, multivalue=False):
    """Creates an object composed of the inverted keys and values of the given
    object.

    Args:
        obj (dict): Dict to invert.
        multivalue (bool, optional): Whether to return inverted values as
            lists. Defaults to ``False``.

    Returns:
        dict: Inverted dict.

    Example:

        >>> results = invert({'a': 1, 'b': 2, 'c': 3})
        >>> results == {1: 'a', 2: 'b', 3: 'c'}
        True
        >>> results = invert({'a': 1, 'b': 2, 'c': 1}, multivalue=True)
        >>> set(results[1]) == set(['a', 'c'])
        True

    Note:
        Assumes `dict` values are hashable as `dict` keys.

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.0.0
        Added ``multivalue`` argument.
    """
    result = {}
    for key, value in iterator(obj):
        if multivalue:
            result.setdefault(value, []).append(key)
        else:
            result[value] = key

    return result


def keys(obj):
    """Creates a list composed of the keys of `obj`.

    Args:
        obj (mixed): Object to extract keys from.

    Returns:
        list: List of keys.

    Example:

        >>> keys([1, 2, 3])
        [0, 1, 2]
        >>> set(keys({'a': 1, 'b': 2, 'c': 3})) == set(['a', 'b', 'c'])
        True

    See Also:
        - :func:`keys` (main definition)
        - :func:`keys_in` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
        Added :func:`keys_in` as alias.
    """
    return [key for key, _ in iterator(obj)]


keys_in = keys


def map_keys(obj, callback=None):
    """Creates an object with the same values as `obj` and keys generated by
    running each property of `obj` through the `callback`. The callback is
    invoked with three arguments: ``(value, key, object)``. If a property name
    is provided for `callback` the created :func:`pydash.collections.pluck`
    style callback will return the property value of the given element. If an
    object is provided for callback the created
    :func:`pydash.collections.where` style callback will return ``True``
    for elements that have the properties of the given object, else ``False``.

    Args:
        obj (list|dict): Object to map.
        callback (mixed): Callback applied per iteration.

    Returns:
        list|dict: Results of running `obj` through `callback`.

    Example:

        >>> callback = lambda value, key: key * 2
        >>> results = map_keys({'a': 1, 'b': 2, 'c': 3}, callback)
        >>> results == {'aa': 1, 'bb': 2, 'cc': 3}
        True

    .. versionadded:: 3.3.0
    """
    return dict((result, value)
                for result, value, _, _ in itercallback(obj, callback))


def map_values(obj, callback=None):
    """Creates an object with the same keys as `obj` and values generated by
    running each property of `obj` through the `callback`. The callback is
    invoked with three arguments: ``(value, key, object)``. If a property name
    is provided for `callback` the created :func:`pydash.collections.pluck`
    style callback will return the property value of the given element. If an
    object is provided for callback the created
    :func:`pydash.collections.where` style callback will return ``True``
    for elements that have the properties of the given object, else ``False``.

    Args:
        obj (list|dict): Object to map.
        callback (mixed): Callback applied per iteration.

    Returns:
        list|dict: Results of running `obj` through `callback`.

    Example:

        >>> results = map_values({'a': 1, 'b': 2, 'c': 3}, lambda x: x * 2)
        >>> results == {'a': 2, 'b': 4, 'c': 6}
        True
        >>> results = map_values({'a': 1, 'b': {'d': 4}, 'c': 3}, {'d': 4})
        >>> results == {'a': False, 'b': True, 'c': False}
        True

    .. versionadded:: 1.0.0
    """
    return dict((key, result)
                for result, _, key, _ in itercallback(obj, callback))


def merge(obj, *sources, **kargs):
    """Recursively merges own enumerable properties of the source object(s)
    that don't resolve to undefined into the destination object. Subsequent
    sources will overwrite property assignments of previous sources. If a
    callback is provided it will be executed to produce the merged values of
    the destination and source properties. The callback is invoked with at
    least two arguments: ``(obj_value, *source_value)``.

    Args:
        obj (dict): Destination object to merge source(s) into.
        sources (dict): Source objects to merge from. subsequent sources
            overwrite previous ones.

    Keyword Args:
        callback (function, optional): Callback function to handle merging
            (must be passed in as keyword argument).

    Returns:
        dict: Merged object.

    Warning:
        `obj` is modified in place.

    Example:

        >>> obj = {'a': 2}
        >>> obj2 = merge(obj, {'a': 1}, {'b': 2, 'c': 3}, {'d': 4})
        >>> obj2 == {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        True
        >>> obj is obj2
        True

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.3.2
        Apply :func:`clone_deep` to each `source` before assigning to `obj`.

    .. versionchanged:: 2.3.2
        Allow `callback` to be passed by reference if it is the last positional
        argument.

    .. versionchanged:: 3.3.0
        Added internal option for overriding the default setter for obj values.
    """
    sources = list(sources)
    _clone = kargs.get('_clone', True)
    callback = kargs.get('callback')
    setter = kargs.get('_setter', set_item)

    if callback is None and callable(sources[-1]):
        callback = sources.pop()

    for source in sources:
        # Don't re-clone if we've already cloned before.
        if _clone:
            source = copy.deepcopy(source)

        for key, src_value in iterator(source):
            obj_value = get_item(obj, key, default=None)
            all_sequences = all([isinstance(src_value, list),
                                 isinstance(obj_value, list)])
            all_mappings = all([isinstance(src_value, dict),
                                isinstance(obj_value, dict)])

            if callback:
                result = callback(obj_value, src_value)
            elif all_sequences or all_mappings:
                result = merge(obj_value,
                               src_value,
                               _clone=False,
                               _setter=setter)
            else:
                result = src_value

            setter(obj, key, result)

    return obj


def omit(obj, callback=None, *properties):
    """Creates a shallow clone of object excluding the specified properties.
    Property names may be specified as individual arguments or as lists of
    property names. If a callback is provided it will be executed for each
    property of object omitting the properties the callback returns truthy for.
    The callback is invoked with three arguments: ``(value, key, object)``.

    Args:
        obj (mixed): Object to process.
        properties (str): Property values to omit.
        callback (mixed, optional): Callback used to determine whic properties
            to omit.

    Returns:
        dict: Results of omitting properties.

    Example:

        >>> omit({'a': 1, 'b': 2, 'c': 3}, 'b', 'c') == {'a': 1}
        True
        >>> omit([1, 2, 3, 4], 0, 3) == {1: 2, 2: 3}
        True

    .. versionadded:: 1.0.0
    """
    if not callable(callback):
        callback = callback if callback is not None else []
        properties = pyd.flatten_deep([callback, properties])

        # pylint: disable=missing-docstring,function-redefined
        def callback(value, key, item):
            return key in properties

        argcount = 3
    else:
        argcount = getargcount(callback, maxargs=3)

    return dict((key, value) for key, value in iterator(obj)
                if not callit(callback, value, key, obj, argcount=argcount))


def pairs(obj):
    """Creates a two dimensional list of an object's key-value pairs, i.e.
    ``[[key1, value1], [key2, value2]]``.

    Args:
        obj (mixed): Object to process.

    Returns:
        list: Two dimensional list of object's key-value pairs.

    Example:

        >>> pairs([1, 2, 3, 4])
        [[0, 1], [1, 2], [2, 3], [3, 4]]
        >>> pairs({'a': 1})
        [['a', 1]]

    .. versionadded:: 1.0.0
    """
    return [[key, value] for key, value in iterator(obj)]


def parse_int(value, radix=None):
    """Converts the given `value` into an integer of the specified `radix`. If
    `radix` is falsey, a radix of ``10`` is used unless the `value` is a
    hexadecimal, in which case a radix of 16 is used.

    Args:
        value (mixed): Value to parse.
        radix (int, optional): Base to convert to.

    Returns:
        mixed: Integer if parsable else ``None``.

    Example:

        >>> parse_int('5')
        5
        >>> parse_int('12', 8)
        10
        >>> parse_int('x') is None
        True

    .. versionadded:: 1.0.0
    """
    if not radix and pyd.is_string(value):
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
        args = (value,) if radix == 10 else (to_string(value), radix)
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
        properties (str): Property values to pick.
        callback (mixed, optional): Callback used to determine which properties
            to pick.

    Returns:
        dict: Dict containg picked properties.

    Example:

        >>> pick({'a': 1, 'b': 2, 'c': 3}, 'a', 'b') == {'a': 1, 'b': 2}
        True

    .. versionadded:: 1.0.0
    """
    if not callable(callback):
        callback = callback if callback is not None else []
        properties = pyd.flatten_deep([callback, properties])

        # pylint: disable=missing-docstring,function-redefined
        def callback(value, key, item):
            return key in properties

        argcount = 3
    else:
        argcount = getargcount(callback, maxargs=3)

    # TODO: cache argcount
    return dict((key, value) for key, value in iterator(obj)
                if callit(callback, value, key, obj, argcount=argcount))


def rename_keys(obj, key_map):
    """Rename the keys of `obj` using `key_map` and return new object.

    Args:
        obj (dict): Object to rename.
        key_map (dict): Renaming map whose keys correspond to existing keys in
            `obj` and whose values are the new key name.

    Returns:
        dict: Renamed `obj`.

    Example:

        >>> obj = rename_keys({'a': 1, 'b': 2, 'c': 3}, {'a': 'A', 'b': 'B'})
        >>> obj == {'A': 1, 'B': 2, 'c': 3}
        True

    .. versionadded:: 2.0.0
    """
    return dict((key_map.get(key, key), value)
                for key, value in iteritems(obj))


def set_(obj, path, value):
    """Sets the value of an object described by `path`. If any part of the
    object path doesn't exist, it will be created.

    Args:
        obj (list|dict): Object to modify.
        path (str | list): Target path to set value to.
        value (mixed): Value to set.

    Returns:
        mixed: Modified `obj`.

    Example:

        >>> set_({}, 'a.b.c', 1)
        {'a': {'b': {'c': 1}}}
        >>> set_({}, 'a.0.c', 1)
        {'a': {'0': {'c': 1}}}
        >>> set_([1, 2], '2.0', 1)
        [1, 2, [1]]

    .. versionadded:: 2.2.0

    .. versionchanged:: 3.3.0
        Added :func:`set_` as main definition and :func:`deep_set` as alias.
    """
    return set_path(obj, value, path_keys(path))


deep_set = set_


def set_path(obj, value, keys, default=None):
    """Sets the value of an object described by `keys`. If any part of the
    object path doesn't exist, it will be created with `default`.

    Args:
        obj (list|dict): Object to modify.
        value (mixed): Value to set.
        keys (list): Target path to set value to.
        default (callable, optional): Callable that returns default value to
            assign if path part is not set. Defaults to ``{}`` if `obj` is a
            ``dict`` or ``[]`` if `obj` is a ``list``.

    Returns:
        mixed: Modified `obj`.

    Example:

        >>> set_path({}, 1, ['a', 0], default=[])
        {'a': [1]}
        >>> set_path({}, 1, ['a', 'b']) == {'a': {'b': 1}}
        True

    .. versionadded:: 2.0.0
    """
    # pylint: disable=redefined-outer-name
    return update_path(obj, lambda *_: value, keys, default=default)


def to_boolean(obj, true_values=('true', '1'), false_values=('false', '0')):
    """Convert `obj` to boolean. This is not like the builtin ``bool``
    function. By default commonly considered strings values are converted to
    their boolean equivalent, i.e., ``'0'`` and ``'false'`` are converted to
    ``False`` while ``'1'`` and ``'true'`` are converted to ``True``. If a
    string value is provided that isn't recognized as having a common boolean
    conversion, then the returned value is ``None``. Non-string values of `obj`
    are converted using ``bool``. Optionally, `true_values` and `false_values`
    can be overridden but each value must be a string.

    Args:
        obj (mixed): Object to convert.
        true_values (tuple, optional): Values to consider ``True``. Each value
            must be a string. Comparision is case-insensitive. Defaults to
            ``('true', '1')``.
        false_values (tuple, optional): Values to consider ``False``. Each
            value must be a string. Comparision is case-insensitive. Defaults
            to ``('false', '0')``.

    Returns:
        bool: Boolean value of `obj`.

    Example:

        >>> to_boolean('true')
        True
        >>> to_boolean('1')
        True
        >>> to_boolean('false')
        False
        >>> to_boolean('0')
        False
        >>> assert to_boolean('a') is None

    .. versionadded:: 3.0.0
    """
    if pyd.is_string(obj):
        obj = obj.strip()

        def boolean_match(text, vals):  # pylint: disable=missing-docstring
            if text.lower() in [val.lower() for val in vals]:
                return True
            else:
                return re.match('|'.join(vals), text)

        if true_values and boolean_match(obj, true_values):
            value = True
        elif false_values and boolean_match(obj, false_values):
            value = False
        else:
            value = None
    else:
        value = bool(obj)

    return value


def to_dict(obj):
    """Convert `obj` to ``dict`` by created a new ``dict`` using `obj` keys and
    values.

    Args:
        obj: (mixed): Object to convert.

    Returns:
        dict: Object converted to ``dict``.

    Example:

        >>> obj = {'a': 1, 'b': 2}
        >>> obj2 = to_dict(obj)
        >>> obj2 == obj
        True
        >>> obj2 is not obj
        True

    .. versionadded:: 3.0.0
    """
    return dict(zip(pyd.keys(obj), pyd.values(obj)))


to_plain_object = to_dict


def to_number(obj, precision=0):
    """Convert `obj` to a number. All numbers are retuned as ``float``. If
    precision is negative, round `obj` to the nearest positive integer place.
    If `obj` can't be converted to a number, ``None`` is returned.

    Args:
        obj (str|int|float): Object to convert.
        precision (int, optional): Precision to round number to. Defaults to
            ``0``.

    Returns:
        float: Converted number or ``None`` if can't be converted.

    Example:

        >>> to_number('1234.5678')
        1235.0
        >>> to_number('1234.5678', 4)
        1234.5678
        >>> to_number(1, 2)
        1.0

    .. versionadded:: 3.0.0
    """
    try:
        factor = pow(10, precision)

        if precision < 0:
            # Round down since negative `precision` means we are going to
            # the nearest positive integer place.
            rounder = math.floor
        else:
            rounder = round

        num = rounder(float(obj) * factor) / factor
    except Exception:  # pylint: disable=broad-except
        num = None

    return num


def to_string(obj):
    """Converts an object to string.

    Args:
        obj (mixed): Object to convert.

    Returns:
        str: String representation of `obj`.

    Example:

        >>> to_string(1) == '1'
        True
        >>> to_string(None) == ''
        True
        >>> to_string([1, 2, 3]) == '[1, 2, 3]'
        True
        >>> to_string('a') == 'a'
        True

    .. versionadded:: 2.0.0

    .. versionchanged:: 3.0.0
        Convert ``None`` to empty string.
    """
    if pyd.is_string(obj):
        res = obj
    elif obj is None:
        res = ''
    else:
        res = text_type(obj)
    return res


def transform(obj, callback=None, accumulator=None):
    """An alernative to :func:`pydash.collections.reduce`, this method
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

    Example:

        >>> transform([1, 2, 3, 4],\
                      lambda acc, value, key: acc.append((key, value)))
        [(0, 1), (1, 2), (2, 3), (3, 4)]

    .. versionadded:: 1.0.0
    """
    if callback is None:
        callback = pyd.identity

    if accumulator is None:
        accumulator = []

    argcount = getargcount(callback, maxargs=4)

    walk = (None for key, item in iterator(obj)
            if callit(callback,
                      accumulator,
                      item,
                      key,
                      obj,
                      argcount=argcount) is False)
    next(walk, None)

    return accumulator


def update_path(obj, callback, keys, default=None):
    """Update the value of an object described by `keys` using `callback`. If
    any part of the object path doesn't exist, it will be created with
    `default`. The callback is invoked with the last key value of `obj`:
    ``(value)``

    Args:
        obj (list|dict): Object to modify.
        callback (function): Function that returns updated value.
        keys (list): A list of string keys that describe the object path to
            modify.
        default (mixed, optional): Default value to assign if path part is not
            set. Defaults to ``{}`` if `obj` is a ``dict`` or ``[]`` if `obj`
            is a ``list``.

    Returns:
        mixed: Updated `obj`.

    Example:

        >>> update_path({}, lambda value: value, ['a', 'b'])
        {'a': {'b': None}}
        >>> update_path([], lambda value: value, [0, 0])
        [[None]]

    .. versionadded:: 2.0.0
    """
    # pylint: disable=redefined-outer-name
    if default is None:
        default = {} if isinstance(obj, dict) else []

    if not pyd.is_list(keys):
        keys = [keys]

    last_key = pyd.last(keys)
    obj = clone_deep(obj)
    target = obj

    for key in pyd.initial(keys):
        set_item(target, key, clone_deep(default), allow_override=False)

        try:
            target = target[key]
        except TypeError:
            target = target[int(key)]

    set_item(target, last_key, callback(get_item(target,
                                                 last_key,
                                                 default=None)))

    return obj


def values(obj):
    """Creates a list composed of the values of `obj`.

    Args:
        obj (mixed): Object to extract values from.

    Returns:
        list: List of values.

    Example:

        >>> results = values({'a': 1, 'b': 2, 'c': 3})
        >>> set(results) == set([1, 2, 3])
        True
        >>> values([2, 4, 6, 8])
        [2, 4, 6, 8]

    See Also:
        - :func:`values` (main definition)
        - :func:`values_in` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
        Added :func:`values_in` as alias.
    """
    return [value for _, value in iterator(obj)]


values_in = values


#
# Helper functions not a part of main API
#


def path_keys(keys):
    """Convert keys used to access an object's path into the standard form: a
    list of keys.
    """
    # pylint: disable=redefined-outer-name
    if pyd.is_string(keys) and ('.' in keys or '[' in keys):
        # Since we can't tell whether a bare number is supposed to be dict key
        # or a list index, we support a special syntax where any string-integer
        # surrounded by brackets is treated as a list index and converted to an
        # integer.
        keys = [int(key[1:-1]) if RE_PATH_LIST_INDEX.match(key)
                else unescape_path_key(key)
                for key in filter(None, RE_PATH_KEY_DELIM.split(keys))]
    elif pyd.is_string(keys) or pyd.is_number(keys):
        keys = [keys]
    elif keys is NoValue:
        keys = []

    return keys


def unescape_path_key(key):
    """Unescape path key."""
    key = pyd.js_replace(key, r'/\\\\/g', r'\\')
    key = pyd.js_replace(key, r'/\\\./g', '.')
    return key
