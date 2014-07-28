"""Utils
"""

from __future__ import absolute_import

from ._compat import string_types, iteritems


def make_callback(callback):
    """Create a callback function from a mixed type `callback`"""
    # FIXME: Resolve circular imports
    from .collections import pluck, where

    if callable(callback):
        cbk = callback
    elif isinstance(callback, string_types):
        cbk = lambda item, *args: pluck([item], callback)[0]
    elif isinstance(callback, dict):
        cbk = lambda item, *args: where([item], callback)
    elif isinstance(callback, (int, float)):
        cbk = lambda item, i, *args: i < callback
    else:
        cbk = lambda item, *args: item

    return cbk


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
    seen_add = seen.add
    for i, item in enumerate(array):
        if item not in seen and not seen_add(item):
            yield (i, item)


def iter_unique(array):
    """Return iterator to find unique list."""
    seen = []
    for i, item in enumerate(array):
        if item not in seen:
            seen.append(item)
            yield (i, item)
