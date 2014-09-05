"""Generic utility methods not part of main API.
"""

from functools import wraps
import warnings

import pydash as pyd
from ._compat import iteritems


def itercallback(collection, callback=None, reverse=False):
    """Return iterative callback based on collection type."""
    if isinstance(collection, dict):
        return iterdict_callback(collection, callback, reverse=reverse)
    else:
        return iterlist_callback(collection, callback, reverse=reverse)


def iterlist_callback(array, callback=None, reverse=False):
    """Return iterative list callback."""
    cbk = pyd.iteratee(callback)
    array_len = len(array)

    if reverse:
        iterable = list(reversed(array))
    else:
        iterable = array

    for index, item in enumerate(iterable):
        if reverse:
            index = array_len - index - 1

        yield (cbk(item, index, array), item, index, array)


def iterdict_callback(collection, callback=None, reverse=False):
    """Return iterative dict callback."""
    cbk = pyd.iteratee(callback)

    if reverse:
        items = reversed(list(iteritems(collection)))
    else:
        items = iteritems(collection)

    for key, value in items:
        yield (cbk(value, key, collection), value, key, collection)


def iterator(collection):
    """Return iterative based on collection type."""
    if isinstance(collection, dict):
        return iterdict(collection)
    else:
        return iterlist(collection)


def iterdict(collection):
    """Return iterative dict."""
    return iteritems(collection)


def iterlist(array):
    """Return iterative list."""
    for i, item in enumerate(array):
        yield i, item


def get_item(obj, key, **kargs):
    """Safely get an item by `key` from a sequence or mapping object when
    `default` provided.

    Args:
        obj (list|dict): Sequence or mapping to retrieve item from.
        key (mixed): Key or index identifying which item to retrieve.

    Keyword Args:
        use_default (bool, optional): Whether to use `default` value when
            `key` doesn't exist in `obj`.
        default (mixed, optional): Default value to return if `key` not
            found in `obj`.

    Returns:
        mixed: `obj[key]` or `default`.

    Raises:
        KeyError|IndexError|TypeError: If `obj` is missing key or index and no
            default value provided.
    """
    use_default = kargs.get('use_default', 'default' in kargs)
    default = kargs.get('default')

    try:
        ret = obj[key]
    except (KeyError, IndexError, TypeError):
        if use_default:
            ret = default
        else:  # pragma: no cover
            raise

    return ret


def set_item(obj, key, value, allow_override=True):
    """Set an object's `key` to `value`. If `obj` is a ``list`` and the
    `key` is the next available index position, append to list; otherwise,
    raise ``IndexError``.

    Args:
        obj (list|dict): Object to assign value to.
        key (mixed): Key or index to assign to.
        value (mixed): Value to assign.

    Returns:
        None

    Raises:
        IndexError: If `obj` is a ``list`` and `key` is greater than length of
            `obj`.
    """
    if isinstance(obj, dict):
        if allow_override or key not in obj:
            obj[key] = value
    elif isinstance(obj, list):
        if key < len(obj):
            if allow_override:
                obj[key] = value
        elif key == len(obj):
            obj.append(value)
        else:  # pragma: no cover
            # Trigger exception by assigning to invalid index.
            obj[key] = value


def deprecated(func):  # pragma: no cover
    """This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    """
    @wraps(func)
    def wrapper(*args, **kargs):  # pylint: disable=missing-docstring
        warnings.warn('Call to deprecated function {0}.'.format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=3)
        return func(*args, **kargs)

    return wrapper
