"""Utils
"""

from __future__ import absolute_import

from .utilities import callback as make_callback
from ._compat import iteritems


def iter_callback(collection, callback=None):
    """Return iterative callback based on collection type."""
    if isinstance(collection, dict):
        return iter_dict_callback(collection, callback)
    else:
        return iter_list_callback(collection, callback)


def iter_list_callback(array, callback=None):
    """Return iterative list callback."""
    cbk = make_callback(callback)
    for i, item in enumerate(array):
        yield (cbk(item, i, array), item, i, array)


def iter_dict_callback(collection, callback=None):
    """Return iterative dict callback."""
    cbk = make_callback(callback)
    for key, value in iteritems(collection):
        yield (cbk(value, key, collection), value, key, collection)


def iter_(collection):
    """Return iterative based on collection type."""
    if isinstance(collection, dict):
        return iter_dict(collection)
    else:
        return iter_list(collection)


def iter_dict(collection):
    """Return iterative dict."""
    return iteritems(collection)


def iter_list(array):
    """Return iterative list."""
    for i, item in enumerate(array):
        yield i, item


def iter_unique_set(array):
    """Return iterator to find unique set."""
    seen = set()
    for i, item in enumerate(array):
        if item not in seen and not seen.add(item):
            yield (i, item)


def iter_unique(array):
    """Return iterator to find unique list."""
    seen = []
    for i, item in enumerate(array):
        if item not in seen:
            seen.append(item)
            yield (i, item)
