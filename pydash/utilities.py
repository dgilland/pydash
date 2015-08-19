# -*- coding: utf-8 -*-
"""Utility functions.

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import, division

from datetime import datetime
from random import uniform, randint

import pydash as pyd
from .helpers import get_item
from ._compat import _range, string_types


__all__ = (
    'attempt',
    'constant',
    'callback',
    'deep_property',
    'deep_prop',
    'identity',
    'iteratee',
    'matches',
    'matches_property',
    'memoize',
    'method',
    'method_of',
    'noop',
    'now',
    'prop',
    'prop_of',
    'property_',
    'property_of',
    'random',
    'range_',
    'result',
    'times',
    'unique_id',
)


ID_COUNTER = 0


def attempt(func, *args, **kargs):
    """Attempts to execute `func`, returning either the result or the caught
    error object.

    Args:
        func (function): The function to attempt.

    Returns:
        mixed: Returns the `func` result or error object.

    Example:

        >>> results = attempt(lambda x: x/0, 1)
        >>> assert isinstance(results, ZeroDivisionError)

    .. versionadded:: 1.1.0
    """
    try:
        ret = func(*args, **kargs)
    except Exception as ex:  # pylint: disable=broad-except
        ret = ex

    return ret


def constant(value):
    """Creates a function that returns `value`.

    Args:
        value (mixed): Constant value to return.

    Returns:
        function: Function that always returns `value`.

    Example:

        >>> pi = constant(3.14)
        >>> pi() == 3.14
        True

    .. versionadded:: 1.0.0
    """
    return lambda: value


def deep_property(path):
    """Creates a :func:`pydash.collections.pluck` style function, which returns
    the key value of a given object.

    Args:
        key (mixed): Key value to fetch from object.

    Returns:
        function: Function that returns object's key value.

    Example:

        >>> deep_property('a.b.c')({'a': {'b': {'c': 1}}})
        1
        >>> deep_property('a.1.0.b')({'a': [5, [{'b': 1}]]})
        1
        >>> deep_property('a.1.0.b')({}) is None
        True

    See Also:
        - :func:`deep_property` (main definition)
        - :func:`deep_prop` (alias)

    .. versionadded:: 1.0.0
    """
    return lambda obj: pyd.get(obj, path)


deep_prop = deep_property


def identity(*args):
    """Return the first argument provided to it.

    Args:
        *args (mixed): Arguments.

    Returns:
        mixed: First argument or ``None``.

    Example:

        >>> identity(1)
        1
        >>> identity(1, 2, 3)
        1
        >>> identity() is None
        True

    .. versionadded:: 1.0.0
    """
    return args[0] if args else None


def iteratee(func):
    """Return a pydash style callback. If `func` is a property name the created
    callback will return the property value for a given element. If `func` is
    an object the created callback will return ``True`` for elements that
    contain the equivalent object properties, otherwise it will return
    ``False``.

    Args:
        func (mixed): Object to create callback function from.

    Returns:
        function: Callback function.

    Example:

        >>> get_data = iteratee('data')
        >>> get_data({'data': [1, 2, 3]})
        [1, 2, 3]
        >>> is_active = iteratee({'active': True})
        >>> is_active({'active': True})
        True
        >>> is_active({'active': 0})
        False
        >>> iteratee(['a', 5])({'a': 5})
        True
        >>> iteratee(['a.b'])({'a.b': 5})
        5
        >>> iteratee('a.b')({'a': {'b': 5}})
        5
        >>> iteratee(lambda a, b: a + b)(1, 2)
        3
        >>> ident = iteratee(None)
        >>> ident('a')
        'a'
        >>> ident(1, 2, 3)
        1

    See Also:
        - :func:`iteratee` (main definition)
        - :func:`callback` (alias)

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.0.0
        Renamed ``create_callback()`` to :func:`iteratee`.

    .. versionchanged:: 3.0.0
        Made pluck style callback support deep property access.

    .. versionchanged:: 3.1.0
        - Added support for shallow pluck style property access via single item
        list/tuple.
        - Added support for matches property style callback via two item
        list/tuple.
    """
    if callable(func):
        cbk = func
    else:
        if isinstance(func, string_types):
            cbk = deep_prop(func)
        elif isinstance(func, (list, tuple)) and len(func) == 1:
            cbk = prop(func[0])
        elif isinstance(func, (list, tuple)) and len(func) > 1:
            cbk = matches_property(*func[:2])
        elif isinstance(func, dict):
            cbk = matches(func)
        else:
            cbk = identity

        # Optimize callback by specifying the exact number of arguments the
        # callback takes so that arg inspection (costly process) can be
        # skipped in helpers.callit().
        cbk._argcount = 1

    return cbk


callback = iteratee


def matches(source):
    """Creates a :func:`pydash.collections.where` style predicate function
    which performs a deep comparison between a given object and the `source`
    object, returning ``True`` if the given object has equivalent property
    values, else ``False``.

    Args:
        source (dict): Source object used for comparision.

    Returns:
        function: Function that compares an object to `source` and returns
            whether the two objects contain the same items.

    Example:

        >>> matches({'a': {'b': 2}})({'a': {'b': 2, 'c':3}})
        True
        >>> matches({'a': 1})({'b': 2, 'a': 1})
        True
        >>> matches({'a': 1})({'b': 2, 'a': 2})
        False

    .. versionadded:: 1.0.0

    .. versionchanged:: 3.0.0
        Use :func:`pydash.predicates.is_match` as matching function.
    """
    return lambda obj: pyd.is_match(obj, source)


def matches_property(key, value):
    """Creates a function that compares the property value of `key` on a given
    object to `value`.

    Args:
        key (str): Object key to match against.
        value (mixed): Value to compare to.

    Returns:
        function: Function that compares `value` to an object's `key` and
            returns whether they are equal.

    Example:

        >>> matches_property('a', 1)({'a': 1, 'b': 2})
        True
        >>> matches_property(0, 1)([1, 2, 3])
        True
        >>> matches_property('a', 2)({'a': 1, 'b': 2})
        False

    .. versionadded:: 3.1.0
    """
    prop_key = prop(key)
    return lambda obj: matches(value)(prop_key(obj))


def memoize(func, resolver=None):
    """Creates a function that memoizes the result of `func`. If `resolver` is
    provided it will be used to determine the cache key for storing the result
    based on the arguments provided to the memoized function. By default, all
    arguments provided to the memoized function are used as the cache key.
    The result cache is exposed as the cache property on the memoized function.

    Args:
        func (function): Function to memoize.
        resolver (function, optional): Function that returns the cache key to
            use.

    Returns:
        function: Memoized function.

    Example:

        >>> ident = memoize(identity)
        >>> ident(1)
        1
        >>> ident.cache['(1,){}'] == 1
        True
        >>> ident(1, 2, 3)
        1
        >>> ident.cache['(1, 2, 3){}'] == 1
        True

    .. versionadded:: 1.0.0
    """
    def memoized(*args, **kargs):  # pylint: disable=missing-docstring
        if resolver:
            key = resolver(*args, **kargs)
        else:
            key = '{0}{1}'.format(args, kargs)

        if key not in memoized.cache:
            memoized.cache[key] = func(*args, **kargs)

        return memoized.cache[key]
    memoized.cache = {}

    return memoized


def method(path, *args, **kargs):
    """Creates a function that invokes the method at `path` on a given object.
    Any additional arguments are provided to the invoked method.

    Args:
        path (str): Object path of method to invoke.
        *args (mixed): Global arguments to apply to method when invoked.
        **kargs (mixed): Global keyword argument to apply to method when
            invoked.

    Returns:
        function: Function that invokes method located at path for object.

    Example:

        >>> obj = {'a': {'b': [None, lambda x: x]}}
        >>> echo = method('a.b.1')
        >>> echo(obj, 1) == 1
        True
        >>> echo(obj, 'one') == 'one'
        True

    .. versionadded:: 3.3.0
    """
    def _method(obj, *_args, **_kargs):
        func = pyd.partial(pyd.get(obj, path), *args, **kargs)
        return func(*_args, **_kargs)
    return _method


def method_of(obj, *args, **kargs):
    """The opposite of :func:`method`. This method creates a function that
    invokes the method at a given path on object. Any additional arguments are
    provided to the invoked method.

    Args:
        obj (mixed): The object to query.
        *args (mixed): Global arguments to apply to method when invoked.
        **kargs (mixed): Global keyword argument to apply to method when
            invoked.

    Returns:
        function: Function that invokes method located at path for object.

    Example:

        >>> obj = {'a': {'b': [None, lambda x: x]}}
        >>> dispatch = method_of(obj)
        >>> dispatch('a.b.1', 1) == 1
        True
        >>> dispatch('a.b.1', 'one') == 'one'
        True

    .. versionadded:: 3.3.0
    """
    def _method_of(path, *_args, **_kargs):
        func = pyd.partial(pyd.get(obj, path), *args, **kargs)
        return func(*_args, **_kargs)
    return _method_of


def noop(*args, **kargs):  # pylint: disable=unused-argument
    """A no-operation function.

    .. versionadded:: 1.0.0
    """
    pass


def now():
    """Return the number of milliseconds that have elapsed since the Unix epoch
    (1 January 1970 00:00:00 UTC).

    Returns:
        int: Milliseconds since Unix epoch.

    .. versionadded:: 1.0.0

    .. versionchanged:: 3.0.0
        Use ``datetime`` module for calculating elapsed time.
    """
    epoch = datetime.utcfromtimestamp(0)
    delta = datetime.utcnow() - epoch

    if hasattr(delta, 'total_seconds'):
        seconds = delta.total_seconds()
    else:  # pragma: no cover
        # PY26
        seconds = ((delta.microseconds +
                    (delta.seconds + delta.days * 24 * 3600) * 10**6) /
                   10**6)

    return int(seconds * 1000)


def property_(key):
    """Creates a :func:`pydash.collections.pluck` style function, which returns
    the key value of a given object.

    Args:
        key (mixed): Key value to fetch from object.

    Returns:
        function: Function that returns object's key value.

    Example:

        >>> get_data = prop('data')
        >>> get_data({'data': 1})
        1
        >>> get_data({}) is None
        True
        >>> get_first = prop(0)
        >>> get_first([1, 2, 3])
        1

    See Also:
        - :func:`property_` (main definition)
        - :func:`prop` (alias)

    .. versionadded:: 1.0.0
    """
    return lambda obj: get_item(obj, key, default=None)


prop = property_


def property_of(obj):
    """The inverse of :func:`property_`. This method creates a function that
    returns the key value of a given key on `obj`.

    Args:
        obj (dict|list): Object to fetch values from.

    Returns:
        function: Function that returns object's key value.

    Example:

        >>> getter = prop_of({'a': 1, 'b': 2, 'c': 3})
        >>> getter('a')
        1
        >>> getter('b')
        2
        >>> getter('x') is None
        True

    See Also:
        - :func:`property_of` (main definition)
        - :func:`prop_of` (alias)

    .. versionadded:: 3.0.0
    """
    return lambda key: property_(key)(obj)


prop_of = property_of


def random(start=0, stop=1, floating=False):
    """Produces a random number between `start` and `stop` (inclusive). If only
    one argument is provided a number between 0 and the given number will be
    returned. If floating is truthy or either `start` or `stop` are floats a
    floating-point number will be returned instead of an integer.

    Args:
        start (int): Minimum value.
        stop (int): Maximum value.
        floating (bool, optional): Whether to force random value to ``float``.
            Default is ``False``.

    Returns:
        int|float: Random value.

    Example:

        >>> 0 <= random() <= 1
        True
        >>> 5 <= random(5, 10) <= 10
        True
        >>> isinstance(random(floating=True), float)
        True

    .. versionadded:: 1.0.0
    """
    floating = any([isinstance(start, float),
                    isinstance(stop, float),
                    floating is True])

    if stop < start:
        stop, start = start, stop

    if floating:
        rnd = uniform(start, stop)
    else:
        rnd = randint(start, stop)

    return rnd


def range_(*args):
    """Creates a list of numbers (positive and/or negative) progressing from
    start up to but not including end. If start is less than stop a zero-length
    range is created unless a negative step is specified.

    Args:
        stop (int): Integer - 1 to stop at. Defaults to ``1``.
        start (int, optional): Integer to start with. Defaults to ``0``.
        step (int, optional): If positive the last element is the largest
            ``start + i * step`` less than `stop`. If negative the last
            element is the smallest ``start + i * step`` greater than `stop`.
            Defaults to ``1``.

    Returns:
        list: List of integers in range

    Example:

        >>> list(range_(5))
        [0, 1, 2, 3, 4]
        >>> list(range_(1, 4))
        [1, 2, 3]
        >>> list(range_(0, 6, 2))
        [0, 2, 4]

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
        Moved to :mod:`pydash.uilities`.

    .. versionchanged:: 3.0.0
        Return generator instead of list.
    """
    return _range(*args)


def result(obj, key, default=None):
    """Return the value of property `key` on `obj`. If `key` value is a
    function it will be invoked and its result returned, else the property
    value is returned. If `obj` is falsey then `default` is returned.

    Args:
        obj (list|dict): Object to retrieve result from.
        key (mixed): Key or index to get result from.
        default (mixed, optional): Default value to return if `obj` is falsey.
            Defaults to ``None``.

    Returns:
        mixed: Result of ``obj[key]`` or ``None``.

    Example:

        >>> result({'a': 1, 'b': lambda: 2}, 'a')
        1
        >>> result({'a': 1, 'b': lambda: 2}, 'b')
        2
        >>> result({'a': 1, 'b': lambda: 2}, 'c') is None
        True
        >>> result({'a': 1, 'b': lambda: 2}, 'c', default=False)
        False

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.0.0
        Added ``default`` argument.
    """
    if not obj:
        return default

    ret = get_item(obj, key, default=default)

    if callable(ret):
        ret = ret()

    return ret


def times(callback, n):
    """Executes the callback `n` times, returning a list of the results of each
    callback execution. The callback is invoked with one argument: ``(index)``.

    Args:
        callback (function): Function to execute.
        n (int): Number of times to execute `callback`.

    Returns:
        list: A list of results from calling `callback`.

    Example:

        >>> times(lambda i: i, 5)
        [0, 1, 2, 3, 4]

    .. versionadded:: 1.0.0

    .. versionchanged:: 3.0.0
        Reordered arguments to make `callback` first.
    """
    # pylint: disable=redefined-outer-name
    return [callback(index) for index in _range(n)]


def unique_id(prefix=None):
    """Generates a unique ID. If `prefix` is provided the ID will be appended
    to  it.

    Args:
        prefix (str, optional): String prefix to prepend to ID value.

    Returns:
        str: ID value.

    Example:

        >>> unique_id()
        '1'
        >>> unique_id('id_')
        'id_2'
        >>> unique_id()
        '3'

    .. versionadded:: 1.0.0
    """
    # pylint: disable=global-statement
    global ID_COUNTER
    ID_COUNTER += 1

    return '{0}{1}'.format(pyd.to_string('' if prefix is None else prefix),
                           pyd.to_string(ID_COUNTER))
