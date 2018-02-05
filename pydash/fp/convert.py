import operator
import re

import pydash as pyd


def immutable(f):
    return lambda target, *args: f(pyd.clone_deep(target), *args)


def applycap(count):
    def _applycap(f):
        def g(*args):
            newargs = args[:count]
            return f(*newargs)
        return g
    return _applycap


def rearg_ex(order, extended=False):
    return lambda f: lambda *args: f(*getargs(order, extended, args))


def getargs(order, extended, args):
    count = len(order)
    base = operator.itemgetter(*order)(args)
    if extended and count < len(args):
        index = order.index(max(order)) + 1
        return base[:index] + args[count:] + base[index:]
    return base


def curry(count):
    return lambda f: pyd.curry(f, count)


def convert(order, f, mutates=None, cap=False):
    count = len(order)
    if mutates is None:
        # guess whether or not we need to deep clone the arguments
        mutates = re.search(r'\bmodif[iy]', f.__doc__ or "", re.I)
    transforms = pyd.compact([
        immutable if mutates else None,
        applycap(count) if cap else None,
        rearg_ex(order, not cap) if order != sorted(order) else None,
        curry(count),
    ])
    return pyd.flow(*transforms)(f)
