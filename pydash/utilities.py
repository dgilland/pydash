"""Utilities
"""

from __future__ import absolute_import

import time
from random import uniform, randint

from ._compat import _range, string_types, text_type


ID_COUNTER = 0


def now():
    """Return the number of milliseconds that have elapsed since the Unix epoch
    (1 January 1970 00:00:00 UTC).
    """
    return int(time.time() * 1000)


def constant(value):
    """Creates a function that returns `value`."""
    return lambda: value


def callback(func):
    """Return a callback. If `func` is a property name the created callback
    will return the property value for a given element. If `func` is an object
    the created callback will return `True` for elements that contain the
    equivalent object properties, otherwise it will return `False`.
    """
    if callable(func):
        cbk = func
    elif isinstance(func, string_types):
        cbk = property_(func)
    elif isinstance(func, dict):
        cbk = matches(func)
    else:
        cbk = identity

    return cbk


def identity(*args):
    """Return the first argument provided to it."""
    return args[0] if args else None


def matches(source):
    """Creates a :func:`where` style predicate function which performs a deep
    comparison between a given object and the `source` object, returning `True`
    if the given object has equivalent property values, else `False`.
    """
    return lambda obj, *args: all(item in obj.items()
                                  for item in source.items())


def memoize(func, resolver=None):
    """Creates a function that memoizes the result of `func`. If `resolver` is
    provided it will be used to determine the cache key for storing the result
    based on the arguments provided to the memoized function. By default, all
    arguments provided to the memoized function are used as the cache key.
    The result cache is exposed as the cache property on the memoized function.
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


def noop(*args, **kargs):  # pylint: disable=unused-argument
    """A no-operation function."""
    pass


def property_(key):
    """Creates a :func:`pluck` style function, which returns the key value of a
    given object.
    """
    return lambda obj, *args: obj.get(key)


prop = property_


def random(start=0, stop=1, floating=False):
    """Produces a random number between `start` and `stop` (inclusive). If only
    one argument is provided a number between 0 and the given number will be
    returned. If floating is truthy or either `start` or `stop` are floats a
    floating-point number will be returned instead of an integer.
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


def result(obj, key):
    """Return the value of property `key` on `obj`. If `key` value is a
    function it will be invoked and its result returned, else the property
    value is returned. If `obj` is falsey then `None` is returned.
    """
    if not obj:
        return None

    ret = obj.get(key)

    if callable(ret):
        ret = ret()

    return ret


def times(n, callback):
    """Executes the callback `n` times, returning a list of the results of each
    callback execution. The callback is invoked with one argument: (index).
    """
    return [callback(index) for index in _range(n)]


def unique_id(prefix=None):
    """Generates a unique ID. If `prefix` is provided the ID will be appended
    to  it.
    """
    global ID_COUNTER
    ID_COUNTER += 1

    return text_type('' if prefix is None else prefix) + text_type(ID_COUNTER)
