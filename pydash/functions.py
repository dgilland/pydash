"""Functions
"""

from __future__ import absolute_import

from . import utils


def after(n, func):
    """Creates a function that executes `func`, with the arguments of the
    created function, only after being called `n` times.
    """
    try:
        n = int(n)
        assert n >= 0
    except Exception:
        n = 0

    def wrapper(*args, **kargs):
        # NOTE: `n` won't be available here unless we attach it to the wrapper.
        # There may be a cleaner way to do this.
        wrapper.n -= 1

        if wrapper.n < 1:
            return func(*args, **kargs)
    wrapper.n = n

    return wrapper


def compose(*funcs):
    """Creates a function that is the composition of the provided functions,
    where each function consumes the return value of the function that follows.
    For example, composing the functions f(), g(), and h() produces f(g(h())).
    """
    def wrapper(*args, **kargs):
        # NOTE: Cannot use `funcs` for the variable name of list(funcs) due to
        # the way Python handles closure variables. Basically, `funcs` has to
        # remain unmodified.
        fns = list(funcs)

        # Compose functions in reverse order starting with the first.
        ret = (fns.pop())(*args, **kargs)

        for func in reversed(fns):
            ret = func(ret)

        return ret

    return wrapper


def curry(func, arity=None):
    """Creates a function which accepts one or more arguments of `func` that
    when  invoked either executes `func` returning its result, if all `func`
    arguments have been provided, or returns a function that accepts one or
    more of the remaining `func` arguments, and so on.
    """
    return utils.Curry(func, arity)
