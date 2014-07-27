"""Functions
"""

from __future__ import absolute_import

import inspect


class Curry(object):  # pylint: disable=too-few-public-methods
    """Wrap a function in a curry context."""

    def __init__(self, func, arity, args=None, kargs=None):
        self.func = func
        self.arity = (len(inspect.getargspec(func).args) if arity is None
                      else arity)
        self.args = () if args is None else args
        self.kargs = {} if kargs is None else kargs

    def __call__(self, *args, **kargs):
        """Store `args` and `kargs` and call `self.func` if we've reached or
        exceeded the function arity.
        """
        args = tuple(list(self.args) + list(args))
        kargs.update(self.kargs)

        if (len(args) + len(kargs)) >= self.arity:
            curried = self.func(*args, **kargs)
        else:
            curried = Curry(self.func, self.arity, args, kargs)

        return curried


class Once(object):  # pylint: disable=too-few-public-methods
    """Wrap a function in a once context."""

    def __init__(self, func):
        self.func = func
        self.result = None
        self.called = False

    def __call__(self, *args, **kargs):
        if not self.called:
            self.result = self.func(*args, **kargs)
            self.called = True

        return self.result


def after(n, func):
    """Creates a function that executes `func`, with the arguments of the
    created function, only after being called `n` times.
    """
    try:
        n = int(n)
        assert n >= 0
    except (ValueError, AssertionError):
        n = 0

    def wrapper(*args, **kargs):  # pylint: disable=missing-docstring
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
    def wrapper(*args, **kargs):  # pylint: disable=missing-docstring
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
    return Curry(func, arity)


def once(func):
    """Creates a function that is restricted to execute func once. Repeat calls
    to the function will return the value of the first call.
    """
    return Once(func)
