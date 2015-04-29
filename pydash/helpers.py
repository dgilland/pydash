# -*- coding: utf-8 -*-
"""Generic utility methods not part of main API.
"""

from __future__ import absolute_import

from collections import Iterable
from functools import wraps
import inspect
import re
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
        elif pyd.is_builtin(callback):
            argcount = guess_builtin_argcount(callback) or maxargs
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


def guess_builtin_argcount(obj):
    """Return guess as to how many arguments can be supplied to a builtin
    function or method. This relies on the fact that the docstring for builtins
    follows a predictable pattern.
    """
    try:
        # Try to split the arguments between the first set of "(...)" which
        # would correspond to argument list of the function.
        count = len((re.search(r'\((.+)\)',
                               obj.__doc__.split('\n')[0])
                     .groups()[0]
                     .split(',')))
    except Exception:  # pragma: no cover pylint: disable=broad-except
        count = None

    return count


def itercallback(obj, callback=None, reverse=False):
    """Return iterative callback based on collection type."""
    cbk = pyd.iteratee(callback)
    items = iterator(obj)

    if reverse:
        items = reversed(tuple(items))

    for key, item in items:
        yield (call_callback(cbk, item, key, obj), item, key, obj)


def iterator(obj):
    """Return iterative based on object type."""
    if isinstance(obj, dict):
        return iteritems(obj)
    elif hasattr(obj, 'iteritems'):
        return obj.iteritems()
    elif hasattr(obj, 'items'):
        return iter(obj.items())
    elif isinstance(obj, Iterable):
        return enumerate(obj)
    else:
        return iteritems(getattr(obj, '__dict__', {}))


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
        KeyError|IndexError|TypeError|AttributeError: If `obj` is missing key
            or index and no default value provided.
    """
    try:
        try:
            ret = obj[key]
        except TypeError:
            # It's possible that a string integer is being used to access a
            # list index. Re-try object access using casted integer.
            ret = obj[int(key)]
    except (KeyError, IndexError, TypeError, AttributeError):
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
        try:
            key = int(key)
        except ValueError:  # pragma: no cover
            pass

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
