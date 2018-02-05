import operator
import re

import pydash as pyd


def immutable(f):
    return lambda target, *args: f(pyd.clone_deep(target), *args)


def applycap(count):
    return lambda f: lambda *args: f(*args[:count])


def rearg_ex(order, extended=False):
    return lambda f: lambda *args: f(*getargs(order, extended, args))


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
