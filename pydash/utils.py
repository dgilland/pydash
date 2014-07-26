"""Utils
"""

from ._compat import string_types, iteritems


def _make_callback(callback):
    """Create a callback function from a mixed type `callback`"""
    from .collection import pluck, where
    if hasattr(callback, '__call__'):
        cbk = callback
    elif isinstance(callback, string_types):
        key = callback
        cbk = lambda item, *args: pluck([item], key)[0]
    elif isinstance(callback, dict):
        cbk = lambda item, *args: where([item], callback)
    else:
        index = callback if isinstance(callback, int) else 1
        cbk = lambda item, i, *args: i < index

    return cbk


def _iter_callback(collection, callback=None):
    """Return iterative callback based on collection type."""
    if isinstance(collection, dict):
        return _iter_dict_callback(collection, callback)
    else:
        return _iter_list_callback(collection, callback)


def _iter_list_callback(array, callback=None):
    """Return iterative list callback."""
    cbk = _make_callback(callback)
    for i, item in enumerate(array):
        yield (cbk(item, i, array), item, i, array)


def _iter_dict_callback(collection, callback=None):
    """Return iterative dict callback."""
    cbk = _make_callback(callback)
    for key, value in iteritems(collection):
        yield (cbk(value, key, collection),)


def _iter(collection):
    """Return iterative based on collection type."""
    if isinstance(collection, dict):
        return _iter_dict(collection)
    else:
        return _iter_list(collection)


def _iter_dict(collection):
    """Return iterative dict."""
    return iteritems(collection)


def _iter_list(array):
    """Return iterative list."""
    for i, item in enumerate(array):
        yield i, item


def _iter_unique_set(array):
    """Return iterator to find unique set."""
    seen = set()
    seen_add = seen.add
    for i, item in enumerate(array):
        if item not in seen and not seen_add(item):
            yield (i, item)


def _iter_unique(array):
    """Return iterator to find unique list."""
    seen = []
    for i, item in enumerate(array):
        if item not in seen:
            seen.append(item)
            yield (i, item)
