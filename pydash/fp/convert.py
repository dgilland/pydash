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


def rearg(order):
    return lambda f: pyd.rearg(f, order)


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
        rearg(order) if order != sorted(order) else None,
        curry(count),
    ])
    return pyd.flow(*transforms)(f)
