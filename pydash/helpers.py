"""Generic utility methods not part of main API.
"""

from functools import wraps
import inspect
import warnings

import pydash as pyd
from ._compat import iteritems


class _NoValue(object):
    """Represents an unset value. Used to differeniate between an explicit
    ``None`` and an unset value.
    """
    pass


#: Singleton object that differeniates between an explicit ``None`` value and
#: an unset value.
NoValue = _NoValue()


def call_callback(callback, *args):
    """Inspect argspec of `callback` function and only pass the supported
    arguments when calling it.
    """
    maxargs = len(args)
    argspec = None

    try:
        argspec = inspect.getargspec(callback)
    except TypeError:
        try:
            argspec = inspect.getargspec(getattr(callback, '__call__', None))
        except TypeError:  # pragma: no cover
            pass
    finally:
        if isinstance(callback, type):
            # Only pass single argument to type callbacks. This is for things
            # like int(), float(), str(), etc.
            argcount = 1
        elif argspec and argspec.varargs:
            # Callback supports variable arguments.
            argcount = maxargs
        elif argspec:
            # Use inspected arg count.
            argcount = len(argspec.args)
        else:  # pragma: no cover
            argcount = maxargs

    argstop = min([maxargs, argcount])

    return callback(*args[:argstop])


def itercallback(collection, callback=None, reverse=False):
    """Return iterative callback based on collection type."""
    if isinstance(collection, dict):
        return iterdict_callback(collection, callback, reverse=reverse)
    else:
        return iterlist_callback(collection, callback, reverse=reverse)


def iterlist_callback(obj, callback=None, reverse=False):
    """Return iterative list callback."""
    cbk = pyd.iteratee(callback)
    obj_len = len(obj)

    if reverse:
        items = list(reversed(obj))
    else:
        items = obj

    for key, item in enumerate(items):
        if reverse:
            key = obj_len - key - 1

        yield (call_callback(cbk, item, key, obj), item, key, obj)


def iterdict_callback(obj, callback=None, reverse=False):
    """Return iterative dict callback."""
    cbk = pyd.iteratee(callback)

    if reverse:
        items = reversed(list(iteritems(obj)))
    else:
        items = iteritems(obj)

    for key, item in items:
        yield (call_callback(cbk, item, key, obj), item, key, obj)


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


def get_item(obj, key, default=NoValue):
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
    try:
        try:
            ret = obj[key]
        except TypeError:
            # It's possible that a string integer is being used to access a
            # list index. Re-try object access using casted integer.
            ret = obj[int(key)]
    except (KeyError, IndexError, TypeError):
        if default is not NoValue:
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
