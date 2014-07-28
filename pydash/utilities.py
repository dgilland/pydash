"""Utilities
"""

from __future__ import absolute_import

import time
from random import uniform, randint


from .utils import make_callback


def now():
    """Return the number of milliseconds that have elapsed since the Unix epoch
    (1 January 1970 00:00:00 UTC).
    """
    return int(time.time() * 1000)


def constant(value):
    """Creates a function that returns `value`."""
    return lambda: value


def identity(*args):
    """Return the first argument provided to it."""
    return args[0] if args else None


def property_(key):
    """Creates a :func:`pluck` style function, which returns the key value of a
    given object.
    """
    return make_callback(key)


prop = property_


def random(start=0, stop=1, floating=False):
    """Produces a random number between `start` and `stop` (inclusive). If only
    one argument is provided a number between 0 and the given number will be
    returned. If floating is truthy or either `start` or `stop` are floats a
    floating-point number will be returned instead of an integer.
    """
    floating = any([isinstance(start, float),
                    isinstance(stop, float),
                    floating])

    if stop < start:
        stop, start = start, stop

    if floating:
        rnd = uniform(start, stop)
    else:
        rnd = randint(start, stop)

    return rnd


def noop(*args, **kargs):
    """A no-operation function."""
    pass
