# -*- coding: utf-8 -*-
import operator
import re

import pydash as pyd


"""
Utilities for creating fp variants of pydash functions
"""


def convert(order, f, cap=False, mutates=None, interpose=True):
    """
    Create fp variant of a function

    Creates auto-curried, iteratee-first/data-last, non-mutating variant
    of a function.

    Args:
        order (list): indices by which to rearrange function arguments
        f (func): the function to wrap
        cap (bool): if True, limits parameters to length of `order`
        mutates (bool): if True, forces deep-clone of first argument
        interpose(bool): if True, interposes extra argments

    Returns:
        function: fp variant of `f`
    """
    count = len(order)
    rearg = order != sorted(order)
    if mutates is None:
        # guess whether or not we need to deep clone the arguments
        mutates = re.search(r'\bmodif[iy]', f.__doc__ or "", re.I)
    transforms = pyd.compact([
        immutable if mutates else None,
        applycap(count) if cap and not rearg else None,
        rearg_ex(order, interpose and not cap) if rearg else None,
        curry_ex(count),
    ])
    return pyd.flow(*transforms)(f)


def immutable(f):
    """
    A transform to deep clone first argument to `f`.
    """
    return lambda target, *args: f(pyd.clone_deep(target), *args)


def applycap(count):
    """
    Create a transform to cap number of arguments to `f`
    """
    def transform(f):
        return lambda *args: f(*args[:count])
    return transform


def rearg_ex(order, interpose=False):
    """
    Create a transform which rearranges arguments to function

    Args:
        order (list): indices of arguments in order they should be passed
        interpose (bool): determines how extra arguments are handled:

            True -  additional arguments will be passed after
            the last argument passed to the *new* function

            True -  additional arguments will be passed at
            the end of the argument list to the *original* function

    Returns:
        function: a rearg transformer

    Example:

        >>> rearg_ex([1, 2, 0], True)(lambda *a: a)('a', 'b', 'c', 'd')
        ('b', 'c', 'd', 'a')
    """
    def transform(f):
        return lambda *args: f(*getargs(order, interpose, args))
    return transform


def getargs(order, interpose, args):
    count = len(order)
    base = operator.itemgetter(*order)(args)
    if interpose:
        index = order.index(max(order)) + 1
        return base[:index] + args[count:] + base[index:]
    return base + args[count:]


class Placeholder:
    """
    Placeholder for `curry_ex`
    """


_ = Placeholder


def curry_ex(count):
    """
    Create a transform which creates an auto-curried function wrapper

    The auto-curried function allows deferring an argument by passing the
    placeholder `_` in its place.

    Args:
        count (int): the number of required arguments.  When `count` or more
            arguments have been provided, the curried function is invoked.

    Returns:
        function: a curry transformer

    Example:

        >>> curry_ex(3)(lambda *a: a)('a')(_)('b', 'c')
        ('a', 'c', 'b')
    """
    def _curry(f, *s):
        def g(*args):
            agg = s + args
            if len(agg) < count + agg.count(_):
                return _curry(f, *agg)
            return f(*replace_args(agg[:count], agg[count:]))
        return g
    return _curry


def replace_args(a, b):
    i = iter(b)
    return tuple(next(i) if v is _ else v for v in a) + tuple(i)
