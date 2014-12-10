"""Functions that operate on lists, dicts, and other objects.

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import

import copy
import re

import pydash as pyd
from .helpers import (
    iterator,
    itercallback,
    get_item,
    set_item,
    NoValue,
    call_callback
)
from ._compat import iteritems, text_type


__all__ = [
    'assign',
    'callables',
    'clone',
    'clone_deep',
    'deep_get',
    'deep_has',
    'deep_set',
    'deep_map_values',
    'defaults',
    'extend',
    'find_key',
    'find_last_key',
    'for_in',
    'for_in_right',
    'for_own',
    'for_own_right',
    'get_path',
    'has',
    'has_path',
    'invert',
    'keys',
    'keys_in',
    'map_values',
    'merge',
    'methods',
    'omit',
    'pairs',
    'parse_int',
    'pick',
    'rename_keys',
    'set_path',
    'to_string',
    'transform',
    'update_path',
    'values',
    'values_in',
]


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

    See Also:
        - :func:`assign` (main definition)
        - :func:`extend` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.3.2
        Apply :func:`clone_deep` to each `source` before assigning to `obj`.
    """
    sources = list(sources)
    callback = kargs.get('callback')

    if callback is None and callable(sources[-1]):
        callback = sources.pop()

    for source in sources:
        source = clone_deep(source)

        for key, value in iteritems(source):
            obj[key] = (value if callback is None
                        else callback(obj.get(key), value))

    return obj


extend = assign


def callables(obj):
    """Creates a sorted list of keys of an object that are callable.

    Args:
        obj (list|dict): Object to inspect.

    Returns:
        list: All keys whose values are callable.

    See Also:
        - :func:`functions` (main definition)
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

    .. versionadded:: 1.0.0
    """
    return clone(value, is_deep=True, callback=callback)


def deep_get(obj, path):
    """Get the value at any depth of a nested object based on the path
    described by `path`. If path doesn't exist, ``None`` is returned.

    Args:
        obj (list|dict): Object to process.
        keys (str|list): List or ``.`` delimited string of keys describing
            path.

    Returns:
        mixed: Value of `obj` at path.

    .. versionadded:: 2.2.0
    """
    return get_path(obj, path)


def deep_has(obj, path):
    """Checks if `path` exists as a key of `obj`.

    Args:
        obj (mixed): Object to test.
        path (mixed): Path to test for. Can be a list of nested keys or a ``.``
            delimited string of path describing the path.

    Returns:
        bool: Whether `obj` has `path`.

    See Also:
        - :func:`deep_has` (main definition)
        - :func:`has_path` (alias)

    .. versionchanged: 2.2.0
        Made :func:`has_path` an alias.
    """
    try:
        get_path(obj, path, default=NoValue)
        exists = True
    except (KeyError, IndexError, TypeError):
        exists = False

    return exists


has_path = deep_has


def deep_map_values(obj, callback=None, property_path=NoValue):
    """Map all non-object values in `obj` with return values from `callback`.
    The callback is invoked with two arguments: ``(obj_value, property_path)``
    where ``property_path`` contains the list of path keys corresponding to the
    path of ``obj_value``.

    Args:
        obj (list|dict): Object to map.
        callback (callable): Callback applied to each value.

    Returns:
        mixed: The modified object.

    Warning:
        `obj` is modified in place.

    .. versionadded: 2.2.0
    """
    properties = path_keys(property_path)

    if pyd.is_object(obj):
        deep_callback = (
            lambda value, key: deep_map_values(value,
                                               callback,
                                               pyd.flatten([properties, key])))
        return pyd.extend(obj, map_values(obj, deep_callback))
    else:
        return callback(obj, properties)


def deep_set(obj, path, value):
    """Sets the value of an object described by `path`. If any part of the
    object path doesn't exist, it will be created.

    Args:
        obj (list|dict): Object to modify.
        path (str | list): Target path to set value to.
        value (mixed): Value to set.

    Returns:
        mixed: Modified `obj`.

    .. versionadded:: 2.2.0
    """
    return set_path(obj, value, path_keys(path))


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

    .. versionadded:: 1.0.0
    """
    for source in sources:
        for key, value in iteritems(source):
            obj.setdefault(key, value)

    return obj


def find_key(obj, callback=None):
    """This method is like :func:`pydash.arrays.find_index` except that it
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


def get_path(obj, path, default=None):
    """Get the value at any depth of a nested object based on the path
    described by `path`. If path doesn't exist, ``None`` is returned.

    Args:
        obj (list|dict): Object to process.
        path (str|list): List or ``.`` delimited string of path describing
            path.

    Returns:
        mixed: Value of `obj` at path.

    .. versionadded:: 2.0.0

    .. versionchanged:: 2.2.0
        Support escaping "." delimiter in single string path key.
    """
    for key in path_keys(path):
        obj = get_item(obj, key, default=default)
        if obj is None:
            break

    return obj


def has(obj, key):
    """Checks if `key` exists as a key of `obj`.

    Args:
        obj (mixed): Object to test.
        key (mixed): Key to test for.

    Returns:
        bool: Whether `obj` has `key`.

    .. versionadded:: 1.0.0
    """
    return deep_has(obj, [key])


def invert(obj, multivalue=False):
    """Creates an object composed of the inverted keys and values of the given
    object.

    Args:
        obj (dict): dict to invert
        multivalue (bool, optional): Whether to return inverted values as
            lists. Defaults to ``False``.

    Returns:
        dict: Inverted dict

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

    See Also:
        - :func:`keys` (main definition)
        - :func:`keys_in` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
        Added :func:`keys_in` as alias.
    """
    return [key for key, _ in iterator(obj)]


keys_in = keys


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

    .. versionadded:: 1.0.0
    """
    return dict((key, result)
                for result, _, key, _ in itercallback(obj, callback))


def merge(obj, *sources, **kargs):
    """Recursively merges own enumerable properties of the source object(s)
    that don't resolve to undefined into the destination object. Subsequent
    sources will overwrite property assignments of previous sources. If a
    callback is provided it will be executed to produce the merged values of
    the destination and source properties. If the callback returns undefined
    merging will be handled by the method instead. The callback is invoked with
    at least two arguments: ``(obj_value, *source_value)``.

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

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.3.2
        Apply :func:`clone_deep` to each `source` before assigning to `obj`.

    .. versionchanged:: 2.3.2
        Allow `callback` to be passed by reference if it is the last positional
        argument.
    """
    sources = list(sources)
    _clone = kargs.get('_clone', True)
    callback = kargs.get('callback')

    if callback is None and callable(sources[-1]):
        callback = sources.pop()

    for source in sources:
        # Don't re-clone if we've already cloned before.
        if _clone:
            source = clone_deep(source)

        for key, src_value in iterator(source):
            obj_value = get_item(obj, key, default=None)
            all_sequences = all([isinstance(src_value, list),
                                 isinstance(obj_value, list)])
            all_mappings = all([isinstance(src_value, dict),
                                isinstance(obj_value, dict)])

            if callback:
                result = callback(obj_value, src_value)
            elif all_sequences or all_mappings:
                result = merge(obj_value, src_value, _clone=False)
            else:
                result = src_value

            set_item(obj, key, result)

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

    .. versionadded:: 1.0.0
    """
    if not callable(callback):
        callback = callback if callback is not None else []
        properties = pyd.flatten_deep([callback, properties])
        callback = lambda value, key, item: key in properties

    return dict((key, value) for key, value in iterator(obj)
                if not call_callback(callback, value, key, obj))


def pairs(obj):
    """Creates a two dimensional list of an object's key-value pairs, i.e.
    ``[[key1, value1], [key2, value2]]``.

    Args:
        obj (mixed): Object to process.

    Returns:
        list: Two dimensional list of object's key-value pairs.

    .. versionadded:: 1.0.0
    """
    return [[key, value] for key, value in iterator(obj)]


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
        callback (mixed, optional): Callback used to determine whic properties
            to pick.

    Returns:
        dict: Results of picking properties.

    .. versionadded:: 1.0.0
    """
    if not callable(callback):
        callback = callback if callback is not None else []
        properties = pyd.flatten_deep([callback, properties])
        callback = lambda value, key, item: key in properties

    return dict((key, value) for key, value in iterator(obj)
                if call_callback(callback, value, key, obj))


def rename_keys(obj, key_map):
    """Rename the keys of `obj` using `key_map` and return new object.

    Args:
        obj (dict): Object to rename.
        key_map (dict): Renaming map whose keys correspond to existing keys in
            `obj` and whose values are the new key name.

    Returns:
        dict: Renamed `obj`.

    .. versionadded:: 2.0.0
    """
    return dict((key_map.get(key, key), value)
                for key, value in iteritems(obj))


def set_path(obj, value, keys, default=None):
    """Sets the value of an object described by `keys`. If any part of the
    object path doesn't exist, it will be created with `default`.

    Args:
        obj (list|dict): Object to modify.
        value (mixed): Value to set.
        keys (list): Target path to set value to.
        default (callable): Callable that returns default value to assign if
            path part is not set. Defaults to ``{}`` is `obj` is a ``dict`` or
            ``[]`` if `obj` is a ``list``.

    Returns:
        mixed: Modified `obj`.

    .. versionadded:: 2.0.0
    """
    # pylint: disable=redefined-outer-name
    return update_path(obj, lambda *_: value, keys, default=default)


def to_string(obj):
    """Converts an object to string.

    Args:
        obj (mixed): Object to convert.

    Returns:
        str: String representation of `obj`.

    .. versionadded:: 2.0.0
    """
    return text_type(obj) if not pyd.is_string(obj) else obj


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

    .. versionadded:: 1.0.0
    """
    if callback is None:
        callback = lambda accumulator, *args: accumulator

    if accumulator is None:
        accumulator = []

    walk = (None for key, item in iterator(obj)
            if call_callback(callback, accumulator, item, key, obj) is False)
    next(walk, None)

    return accumulator


def update_path(obj, callback, keys, default=None):
    """Update the value of an object described by `keys` using `callback`. If
    any part of the object path doesn't exist, it will be created with
    `default`. The callback is invoked with the last key value of `obj`:
    ``(value)``

    Args:
        obj (list|dict): Object to modify.
        callback (callable): Function that returns updated value.
        keys (list): A list of string keys that describe the object path to
            modify.
        default (mixed): Default value to assign if path part is not set.
            Defaults to ``{}`` if `obj` is a ``dict`` or ``[]`` if `obj` is a
            ``list``.

    Returns:
        mixed: Updated `obj`.

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
        target = target[key]

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
    if pyd.is_string(keys):
        # This matches "." as delimiter unless it is escaped by "//".
        re_dot_delim = re.compile(r'(?<!\\)(?:\\\\)*\.')

        # Since we can't tell whether a bare number is supposed to be dict key
        # or a list index, we support a special syntax where any string-integer
        # surrounded by brackets is treated as a list index and converted to an
        # integer.
        re_list_index = re.compile(r'\[[\d\]]')

        keys = [int(key[1:-1]) if re_list_index.match(key)
                else unescape_path_key(key)
                for key in re_dot_delim.split(keys)]
    elif pyd.is_number(keys):
        keys = [keys]
    elif keys is NoValue:
        keys = []

    return keys


def unescape_path_key(key):
    """Unescape path key."""
    key = pyd.js_replace(r'/\\\\/g', key, r'\\')
    key = pyd.js_replace(r'/\\\./g', key, '.')
    return key
