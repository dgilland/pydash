# -*- coding: utf-8 -*-
"""Utility functions.

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import, division

from collections import namedtuple
from datetime import datetime
from functools import partial
import math
from random import uniform, randint
import re

import pydash as pyd
from .helpers import callit, getargcount, base_get, iterator, NoValue
from ._compat import _range, iteritems, string_types


__all__ = (
    'attempt',
    'cond',
    'conforms',
    'conforms_to',
    'constant',
    'default_to',
    'identity',
    'iteratee',
    'matches',
    'matches_property',
    'memoize',
    'method',
    'method_of',
    'noop',
    'nth_arg',
    'now',
    'over',
    'over_every',
    'over_some',
    'properties',
    'property_',
    'property_of',
    'random',
    'range_',
    'range_right',
    'result',
    'stub_list',
    'stub_dict',
    'stub_false',
    'stub_string',
    'stub_true',
    'times',
    'to_path',
    'unique_id',
)

# These regexes are used in to_path() to parse deep path strings.

# This is used to split a deep path string into dict keys or list indexex.
# This matches "." as delimiter (unless it is escaped by "//") and
# "[<integer>]" as delimiter while keeping the "[<integer>]" as an item.
RE_PATH_KEY_DELIM = re.compile(r'(?<!\\)(?:\\\\)*\.|(\[\d+\])')

# Matches on path strings like "[<integer>]". This is used to test whether a
# path string part is a list index.
RE_PATH_LIST_INDEX = re.compile(r'^\[\d+\]$')


ID_COUNTER = 0

PathToken = namedtuple('PathToken', ['key', 'default_factory'])


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


def cond(pairs, *extra_pairs):
    """Creates a function that iterates over `pairs` and invokes the
    corresponding function of the first predicate to return truthy.

    Args:
        pairs (list): A list of predicate-function pairs.

    Returns:
        function: Returns the new composite function.

    Example:

        >>> func = cond([[matches({'a': 1}), constant('matches A')],\
                         [matches({'b': 2}), constant('matches B')],\
                         [stub_true, lambda value: value]])
        >>> func({'a': 1, 'b': 2})
        'matches A'
        >>> func({'a': 0, 'b': 2})
        'matches B'
        >>> func({'a': 0, 'b': 0}) == {'a': 0, 'b': 0}
        True

    .. versionadded:: 4.0.0

    .. versionchanged:: 4.2.0
        Fixed missing argument passing to matched function and added
        support for passing in a single list of pairs instead of just pairs as
        separate arguments.
    """
    if extra_pairs:
        pairs = [pairs] + list(extra_pairs)

    for pair in pairs:
        try:
            assert len(pair) == 2
        except Exception:
            raise ValueError('Each predicate-function pair should contain '
                             'exactly two elements')

        if not all(map(callable, pair)):
            raise TypeError('Both predicate-function pair should be callable')

    def _cond(*args):
        for pair in pairs:
            predicate, iteratee = pair

            if callit(predicate, *args):
                return iteratee(*args)

    return _cond


def conforms(source):
    """Creates a function that invokes the predicate properties of `source`
    with the corresponding property values of a given object, returning
    ``True`` if all predicates return truthy, else ``False``.

    Args:
        source (dict|list): The object of property predicates to conform to.

    Returns:
        function: Returns the new spec function.

    Example:

        >>> func = conforms({'b': lambda n: n > 1})
        >>> func({'b': 2})
        True
        >>> func({'b': 0})
        False
        >>> func = conforms([lambda n: n > 1, lambda n: n == 0])
        >>> func([2, 0])
        True
        >>> func([0, 0])
        False

    .. versionadded:: 4.0.0
    """
    def _conforms(obj):
        for key, predicate in iterator(source):
            if not pyd.has(obj, key) or not predicate(obj[key]):
                return False
        return True

    return _conforms


def conforms_to(obj, source):
    """Checks if `obj` conforms to `source` by invoking the predicate
    properties of `source` with the corresponding property values of `obj`.

    Args:
        obj (dict|list): The object to inspect.
        source (dict|list): The object of property predicates to conform to.

    Example:

        >>> conforms_to({'b': 2}, {'b': lambda n: n > 1})
        True
        >>> conforms_to({'b': 0}, {'b': lambda n: n > 1})
        False
        >>> conforms_to([2, 0], [lambda n: n > 1, lambda n: n == 0])
        True
        >>> conforms_to([0, 0], [lambda n: n > 1, lambda n: n == 0])
        False

    .. versionadded:: 4.0.0
    """
    return conforms(source)(obj)


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

    .. versionchanged:: 4.0.0
        Returned function ignores arguments instead of raising exception.
    """
    return partial(identity, value)


def default_to(value, default_value):
    """Checks :attr:`value` to determine whether a default value should be
    returned in its place. The :attr:`default_value` is returned if value is
    None.

    Args:
        value (mixed): Value passed in by the user.
        default_value (mixed): Default value passed in by the user.

    Returns:
        mixed: Returns :attr:`value` if :attr:`value` is given otherwise
            returns :attr:`default_value`.

    Example:

        >>> default_to(1, 10)
        1
        >>> default_to(None, 10)
        10

    .. versionadded:: 4.0.0
    """
    return default_value if value is None else value


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
    """Return a pydash style iteratee. If `func` is a property name the created
    iteratee will return the property value for a given element. If `func` is
    an object the created iteratee will return ``True`` for elements that
    contain the equivalent object properties, otherwise it will return
    ``False``.

    Args:
        func (mixed): Object to create iteratee function from.

    Returns:
        function: Iteratee function.

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
        >>> iteratee(('a', ['c', 'd', 'e']))({'a': 1, 'c': {'d': {'e': 3}}})
        [1, 3]
        >>> iteratee(lambda a, b: a + b)(1, 2)
        3
        >>> ident = iteratee(None)
        >>> ident('a')
        'a'
        >>> ident(1, 2, 3)
        1

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.0.0
        Renamed ``create_iteratee()`` to :func:`iteratee`.

    .. versionchanged:: 3.0.0
        Made pluck style iteratee support deep property access.

    .. versionchanged:: 3.1.0
        - Added support for shallow pluck style property access via single item
        list/tuple.
        - Added support for matches property style iteratee via two item
        list/tuple.

    .. versionchanged:: 4.0.0
        Removed alias ``callback``.

    .. versionchanged:: 4.1.0
        Return :func:`properties` callback when `func` is a ``tuple``.
    """
    if callable(func):
        cbk = func
    else:
        if isinstance(func, int):
            func = str(func)

        if isinstance(func, string_types):
            cbk = property_(func)
        elif isinstance(func, list) and len(func) == 1:
            cbk = property_(func)
        elif isinstance(func, list) and len(func) > 1:
            cbk = matches_property(*func[:2])
        elif isinstance(func, tuple):
            cbk = properties(*func)
        elif isinstance(func, dict):
            cbk = matches(func)
        else:
            cbk = identity

        # Optimize iteratee by specifying the exact number of arguments the
        # iteratee takes so that arg inspection (costly process) can be
        # skipped in helpers.callit().
        cbk._argcount = 1

    return cbk


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
    prop_accessor = property_(key)
    return lambda obj: matches(value)(prop_accessor(obj))


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
    def memoized(*args, **kargs):
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


def nth_arg(pos=0):
    """Creates a function that gets the argument at index n. If n is negative,
    the nth argument from the end is returned.

    Args:
        pos (int): The index of the argument to return.

    Returns:
        function: Returns the new pass-thru function.

    Example:

        >>> func = nth_arg(1)
        >>> func(11, 22, 33, 44)
        22
        >>> func = nth_arg(-1)
        >>> func(11, 22, 33, 44)
        44

    .. versionadded:: 4.0.0
    """
    def _nth_arg(*args):
        try:
            position = math.ceil(float(pos))
        except ValueError:
            position = 0

        return pyd.get(args, position)

    return _nth_arg


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


def over(funcs):
    """Creates a function that invokes all functions in `funcs` with the
    arguments it receives and returns their results.

    Args:
        funcs (list): List of functions to be invoked.

    Returns:
        function: Returns the new pass-thru function.

    Example:

        >>> func = over([max, min])
        >>> func(1, 2, 3, 4)
        [4, 1]

    .. versionadded:: 4.0.0
    """
    def _over(*args):
        return [func(*args) for func in funcs]

    return _over


def over_every(funcs):
    """Creates a function that checks if all of the functions in `funcs` return
    truthy when invoked with the arguments it receives.

    Args:
        funcs (list): List of functions to be invoked.

    Returns:
        function: Returns the new pass-thru function.

    Example:

        >>> func = over_every([bool, lambda x: x is not None])
        >>> func(1)
        True

    .. versionadded:: 4.0.0
    """
    def _over_every(*args):
        return all(over(funcs)(*args))

    return _over_every


def over_some(funcs):
    """Creates a function that checks if any of the functions in `funcs` return
    truthy when invoked with the arguments it receives.

    Args:
        funcs (list): List of functions to be invoked.

    Returns:
        function: Returns the new pass-thru function.

    Example:

        >>> func = over_some([bool, lambda x: x is None])
        >>> func(1)
        True

    .. versionadded:: 4.0.0
    """
    def _over_some(*args):
        return any(over(funcs)(*args))

    return _over_some


def property_(path):
    """Creates a function that returns the value at path of a given object.

    Args:
        path (str|list): Path value to fetch from object.

    Returns:
        function: Function that returns object's path value.

    Example:

        >>> get_data = property_('data')
        >>> get_data({'data': 1})
        1
        >>> get_data({}) is None
        True
        >>> get_first = property_(0)
        >>> get_first([1, 2, 3])
        1

    .. versionadded:: 1.0.0

    .. versionchanged:: 4.0.1
        Made property accessor work with deep path strings.
    """
    return lambda obj: pyd.get(obj, path)


def properties(*paths):
    """Like :func:`property_` except that it returns a list of values at each
    path in `paths`.

    Args:
        *path (str|list): Path values to fetch from object.

    Returns:
        function: Function that returns object's path value.

    Example:

        >>> getter = properties('a', 'b', ['c', 'd', 'e'])
        >>> getter({'a': 1, 'b': 2, 'c': {'d': {'e': 3}}})
        [1, 2, 3]

    .. versionadded:: 4.1.0
    """
    return lambda obj: [getter(obj)
                        for getter in (pyd.property_(path) for path in paths)]


def property_of(obj):
    """The inverse of :func:`property_`. This method creates a function that
    returns the key value of a given key on `obj`.

    Args:
        obj (dict|list): Object to fetch values from.

    Returns:
        function: Function that returns object's key value.

    Example:

        >>> getter = property_of({'a': 1, 'b': 2, 'c': 3})
        >>> getter('a')
        1
        >>> getter('b')
        2
        >>> getter('x') is None
        True

    .. versionadded:: 3.0.0

    .. versionchanged:: 4.0.0
        Removed alias ``prop_of``.
    """
    return lambda key: property_(key)(obj)


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
    start up to but not including end. If `start` is less than `stop`,
    a zero-length range is created unless a negative `step` is specified.

    Args:
        start (int, optional): Integer to start with. Defaults to ``0``.
        stop (int): Integer to stop at.
        step (int, optional): The value to increment or decrement by. Defaults
            to ``1``.

    Yields:
        int: Next integer in range.

    Example:

        >>> list(range_(5))
        [0, 1, 2, 3, 4]
        >>> list(range_(1, 4))
        [1, 2, 3]
        >>> list(range_(0, 6, 2))
        [0, 2, 4]
        >>> list(range_(4, 1))
        [4, 3, 2]

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
        Moved to :mod:`pydash.uilities`.

    .. versionchanged:: 3.0.0
        Return generator instead of list.

    .. versionchanged:: 4.0.0
        Support decrementing when start argument is greater than stop argument.
    """
    return base_range(*args)


def range_right(*args):
    """Similar to :func:`range_`, except that it populates the values in
    descending order.

    Args:
        start (int, optional): Integer to start with. Defaults to ``0``.
        stop (int): Integer to stop at.
        step (int, optional): The value to increment or decrement by. Defaults
            to ``1`` if `start` < `stop` else ``-1``.

    Yields:
        int: Next integer in range.

    Example:

        >>> list(range_right(5))
        [4, 3, 2, 1, 0]
        >>> list(range_right(1, 4))
        [3, 2, 1]
        >>> list(range_right(0, 6, 2))
        [4, 2, 0]

    .. versionadded:: 4.0.0
    """
    return base_range(*args, from_right=True)


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

    ret = base_get(obj, key, default=default)

    if callable(ret):
        ret = ret()

    return ret


def stub_list():
    """Returns empty "list".

    Returns:
        list: Empty list.

    Example:

        >>> stub_list()
        []

    .. versionadded:: 4.0.0
    """
    return []


def stub_dict():
    """Returns empty "dict".

    Returns:
        dict: Empty dict.

    Example:

        >>> stub_dict()
        {}

    .. versionadded:: 4.0.0
    """
    return {}


def stub_false():
    """Returns ``False``.

    Returns:
        bool: False

    Example:

        >>> stub_false()
        False

    .. versionadded:: 4.0.0
    """
    return False


def stub_string():
    """Returns an empty string.

    Returns:
        str: Empty string

    Example:

        >>> stub_string()
        ''

    .. versionadded:: 4.0.0
    """
    return ''


def stub_true():
    """Returns ``True``.

    Returns:
        bool: True

    Example:

        >>> stub_true()
        True

    .. versionadded:: 4.0.0
    """
    return True


def times(n, iteratee=identity):
    """Executes the iteratee `n` times, returning a list of the results of each
    iteratee execution. The iteratee is invoked with one argument: ``(index)``.

    Args:
        n (int): Number of times to execute `iteratee`.
        iteratee (function): Function to execute.

    Returns:
        list: A list of results from calling `iteratee`.

    Example:

        >>> times(5, lambda i: i)
        [0, 1, 2, 3, 4]

    .. versionadded:: 1.0.0

    .. versionchanged:: 3.0.0
        Reordered arguments to make `iteratee` first.

    .. versionchanged:: 4.0.0

        - Re-reordered arguments to make `iteratee` last argument.
        - Added functionality for handling `iteratee` with zero positional
          arguments.
    """
    argcount = getargcount(iteratee, maxargs=1)
    return [callit(iteratee, index, argcount=argcount) for index in _range(n)]


def to_path(value):
    """Converts values to a property path array.

    Args:
        value (mixed): Value to convert.

    Returns:
        list: Returns the new property path array.

    Example:

        >>> to_path('a.b.c')
        ['a', 'b', 'c']
        >>> to_path('a[0].b.c')
        ['a', 0, 'b', 'c']
        >>> to_path('a[0][1][2].b.c')
        ['a', 0, 1, 2, 'b', 'c']

    .. versionadded:: 4.0.0

    .. versionchanged:: 4.2.1
        Ensure returned path is always a list.
    """
    tokens = to_path_tokens(value)
    if isinstance(tokens, list):
        path = [token.key if isinstance(token, PathToken)
                else token
                for token in to_path_tokens(value)]
    else:
        path = [tokens]
    return path


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


#
# Helper functions not a part of main API
#


def to_path_tokens(value):
    """Parse `value` into :class:`PathToken` objects."""
    if pyd.is_string(value) and ('.' in value or '[' in value):
        # Since we can't tell whether a bare number is supposed to be dict key
        # or a list index, we support a special syntax where any string-integer
        # surrounded by brackets is treated as a list index and converted to an
        # integer.
        keys = [PathToken(int(key[1:-1]), default_factory=list)
                if RE_PATH_LIST_INDEX.match(key)
                else PathToken(unescape_path_key(key), default_factory=dict)
                for key in filter(None, RE_PATH_KEY_DELIM.split(value))]
    elif pyd.is_string(value) or pyd.is_number(value):
        keys = [PathToken(value, default_factory=dict)]
    elif value is NoValue:
        keys = []
    else:
        keys = value

    return keys


def unescape_path_key(key):
    """Unescape path key."""
    key = key.replace(r'\\', '\\')
    key = key.replace(r'\.', r'.')
    return key


def base_range(*args, **kargs):
    """Yield range values."""
    from_right = kargs.get('from_right', False)

    if len(args) >= 3:
        args = args[:3]
    elif len(args) == 2:
        args = (args[0], args[1], None)
    elif len(args) == 1:
        args = (0, args[0], None)

    if args and args[2] is None:
        check_args = args[:2]
    else:
        check_args = args

    for arg in check_args:
        if not isinstance(arg, int):  # pragma: no cover
            raise TypeError("range cannot interpret '{0}' object as an "
                            "integer".format(type(arg).__name__))

    def gen():
        if not args:
            return

        start, stop, step = args

        if step is None:
            step = 1 if start < stop else -1

        length = int(max([math.ceil((stop - start) / (step or 1)), 0]))

        if from_right:
            start += (step * length) - step
            step *= -1

        while length:
            yield start

            start += step
            length -= 1

    return gen()
