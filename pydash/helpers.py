# -*- coding: utf-8 -*-
"""Generic utility methods not part of main API.
"""

from __future__ import absolute_import

from collections import Iterable
from functools import wraps
from operator import attrgetter, itemgetter
import warnings

import pydash as pyd
from ._compat import iteritems, getfullargspec, string_types


class _NoValue(object):
    """Represents an unset value. Used to differeniate between an explicit
    ``None`` and an unset value.
    """
    pass


#: Singleton object that differeniates between an explicit ``None`` value and
#: an unset value.
NoValue = _NoValue()


def callit(iteratee, *args, **kargs):
    """Inspect argspec of `iteratee` function and only pass the supported
    arguments when calling it.
    """
    maxargs = len(args)
    argcount = (kargs['argcount'] if 'argcount' in kargs
                else getargcount(iteratee, maxargs))
    argstop = min([maxargs, argcount])

    return iteratee(*args[:argstop])


def getargcount(iteratee, maxargs):
    """Return argument count of iteratee function."""
    if hasattr(iteratee, '_argcount'):
        # Optimization feature where argcount of iteratee is known and properly
        # set by initator.
        return iteratee._argcount

    argspec = None

    if isinstance(iteratee, type) or pyd.is_builtin(iteratee):
        # Only pass single argument to type iteratees or builtins.
        argcount = 1
    else:
        try:
            argspec = getfullargspec(iteratee)

            if argspec and not argspec.varargs:
                # Use inspected arg count.
                argcount = len(argspec.args)
            else:
                # Assume all args are handleable
                argcount = maxargs
        except TypeError:  # pragma: no cover
            argcount = 1

    return argcount


def iteriteratee(obj, iteratee=None, reverse=False):
    """Return iterative iteratee based on collection type."""
    cbk = pyd.iteratee(iteratee)
    items = iterator(obj)

    if reverse:
        items = reversed(tuple(items))

    # Precompute argcount to avoid repeated calculations during iteratee loop.
    argcount = getargcount(cbk, maxargs=3)

    for key, item in items:
        yield (callit(cbk, item, key, obj, argcount=argcount),
               item,
               key,
               obj)


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


def base_get(obj, key, default=NoValue):
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
        mixed: `obj[key]`, `obj.key`, or `default`.

    Raises:
        KeyError: If `obj` is missing key, index, or attribute and no default
            value provided.
    """
    # Build list of getters to try to retrieve key value from obj.
    getters = [itemgetter(key)]

    try:
        # Only add list index getter if key can be cast as integer.
        getters.append(itemgetter(int(key)))
    except Exception:
        pass

    if not isinstance(obj, (dict, list)):
        # Don't add attrgetter for dict/list objects since we don't want class
        # methods/attributes returned for them.
        try:
            # Only add attribute getter if key is string.
            getters.append(attrgetter(key))
        except Exception:  # pragma: no cover
            pass

    for getter in getters:
        try:
            ret = getter(obj)
            break
        except Exception:  # pragma: no cover
            pass
    else:
        # The for-loop didn't break which means we weren't able to find key.
        if default is NoValue:
            # Raise if there's no default provided.
            raise KeyError('Object "{0}" does not have key "{1}"'
                           .format(repr(obj), key))
        ret = default

    return ret


def base_set(obj, key, value, allow_override=True):
    """Set an object's `key` to `value`. If `obj` is a ``list`` and the
    `key` is the next available index position, append to list; otherwise, pad
    the list of ``None`` and then append to the list.

    Args:
        obj (list|dict): Object to assign value to.
        key (mixed): Key or index to assign to.
        value (mixed): Value to assign.
    """
    if isinstance(obj, dict):
        if allow_override or key not in obj:
            obj[key] = value
    elif isinstance(obj, list):
        key = int(key)

        if key < len(obj):
            if allow_override:
                obj[key] = value
        else:
            if key > len(obj):
                # Pad list object with None values up to the index key so we
                # can append the value into the key index.
                obj[:] = (obj + [None] * key)[:key]
            obj.append(value)

    return obj


def parse_iteratee(iteratee_keyword, *args, **kargs):
    """Try to find iteratee function passed in either as a keyword argument or
    as the last positional argument in `args`.
    """
    iteratee = kargs.get(iteratee_keyword)
    last_arg = args[-1]

    if (iteratee is None and
            (callable(last_arg) or
             isinstance(last_arg, string_types) or
             isinstance(last_arg, dict) or
             last_arg is None)):
        iteratee = last_arg
        args = args[:-1]

    return (iteratee, args)


class iterator_with_default(object):
    """A wrapper around an iterator object that provides a default."""
    def __init__(self, collection, default):
        self.iter = iter(collection)
        self.default = default

    def __iter__(self):
        return self

    def next_default(self):
        ret = self.default
        self.default = NoValue
        return ret

    def __next__(self):
        ret = next(self.iter, self.next_default())
        if ret is NoValue:
            raise StopIteration
        return ret

    next = __next__


def deprecated(func):  # pragma: no cover
    """This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    """
    @wraps(func)
    def wrapper(*args, **kargs):
        warnings.warn('Call to deprecated function {0}.'.format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=3)
        return func(*args, **kargs)

    return wrapper
