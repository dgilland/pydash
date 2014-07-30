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


def get_item(obj, key, **kargs):
    """Safely get an item by `key` from a sequence or mapping object.

    Args:
        obj (mixed): sequence or mapping to retrieve item from
        key (mixed): hash key or integer index identifying which item to
            retrieve
        **default (mixed, optional): default value to return if `key` not
            found in `obj`

    Returns:
        mixed: `obj[key]` or `default`
    """
    use_default = 'default' in kargs
    default = kargs.get('default')

    try:
        ret = obj[key]
    except (KeyError, IndexError):
        if use_default:
            ret = default
        else:  # pragma: no cover
            raise

    return ret


def set_item(obj, key, value):
    """Set an object's `key` to `value`. If `obj` is a ``list`` and the
    `key` is the next available index position, append to list; otherwise,
    raise ``IndexError``.

    Args:
        obj (mixed): object to assign value to
        key (mixed): dict or list index to assign to
        value (mixed): value to assign

    Returns:
        None

    Raises:
        IndexError: if `obj` is a ``list`` and `key` is greater than length of
            `obj`
    """
    if isinstance(obj, dict):
        obj[key] = value
    elif isinstance(obj, list):
        if key < len(obj):
            obj[key] = value
        elif key == len(obj):
            obj.append(value)
        else:  # pragma: no cover
            # Trigger exception by assigning to invalid index.
            obj[key] = value
