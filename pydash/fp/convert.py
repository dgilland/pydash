import operator
import re

import pydash as pyd


def immutable(f):
    return lambda target, *args: f(pyd.clone_deep(target), *args)


def applycap(count):
    return lambda f: lambda *args: f(*args[:count])


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
    return lambda f: lambda *args: f(*getargs(order, interpose, args))


def getargs(order, interpose, args):
    count = len(order)
    base = operator.itemgetter(*order)(args)
    if interpose:
        index = order.index(max(order)) + 1
        return base[:index] + args[count:] + base[index:]
    return base + args[count:]


def curry(count):
    return lambda f: pyd.curry(f, count)


def convert(order, f, mutates=None, cap=False, interpose=True):
    count = len(order)
    rearg = order != sorted(order)
    if mutates is None:
        # guess whether or not we need to deep clone the arguments
        mutates = re.search(r'\bmodif[iy]', f.__doc__ or "", re.I)
    transforms = pyd.compact([
        immutable if mutates else None,
        applycap(count) if cap and not rearg else None,
        rearg_ex(order, interpose and not cap) if rearg else None,
        curry(count),
    ])
    return pyd.flow(*transforms)(f)
