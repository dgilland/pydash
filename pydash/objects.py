"""Objects
"""

from __future__ import absolute_import

from .arrays import flatten
from .utils import iter_
from ._compat import iteritems, itervalues, iterkeys


def keys(obj):
    """Creates a list composed of the keys of `obj`."""
    return list(iterkeys(obj))


def omit(obj, callback, *properties):
    """Creates a shallow clone of object excluding the specified properties.
    Property names may be specified as individual arguments or as lists of
    property names. If a callback is provided it will be executed for each
    property of object omitting the properties the callback returns truthy for.
    The callback is invoked with three arguments; (value, key, object).
    """
    if not callable(callback):
        properties = flatten([callback, properties])
        callback = lambda value, key, item: key in properties

    return dict((key, value) for key, value in iteritems(obj)
                if not callback(value, key, obj))


def pairs(obj):
    """Creates a two dimensional list of an object's key-value pairs, i.e.
    [[key1, value1], [key2, value2]].
    """
    return [[key, value] for key, value in iteritems(obj)]


def pick(obj, callback, *properties):
    """Creates a shallow clone of object composed of the specified properties.
    Property names may be specified as individual arguments or as lists of
    property names. If a callback is provided it will be executed for each
    property of object picking the properties the callback returns truthy for.
    The callback is invoked with three arguments; (value, key, object).
    """
    if not callable(callback):
        properties = flatten([callback, properties])
        callback = lambda value, key, *args: key in properties

    return dict((key, value) for key, value in iteritems(obj)
                if callback(value, key, obj))


def transform(obj, callback=None, accumulator=None):
    """An alternative to :func:`reduce`, this method transforms `obj` to a new
    accumulator object which is the result of running each of its properties
    through a callback, with each callback execution potentially mutating the
    accumulator object. The callback is invoked with four arguments:
    (accumulator, value, key, object). Callbacks may exit iteration early by
    explicitly returning `False`.
    """
    if callback is None:
        callback = lambda accumulator, *args: accumulator

    if accumulator is None:
        accumulator = []

    for key, value in iter_(obj):
        result = callback(accumulator, value, key, obj)
        if result is False:
            break

    return accumulator


def values(obj):
    """Creates a list composed of the values of `obj`."""
    return list(itervalues(obj))
