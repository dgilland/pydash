"""Functions that wrap other functions.

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import

import inspect
import time

from .objects import is_number
from .utilities import now


__all__ = [
    'after',
    'before',
    'compose',
    'curry',
    'curry_right',
    'debounce',
    'delay',
    'negate',
    'once',
    'partial',
    'partial_right',
    'throttle',
    'wrap',
]


class After(object):
    """Wrap a function in an after context."""
    def __init__(self, n, func):
        try:
            n = int(n)
            assert n >= 0
        except (ValueError, AssertionError):
            n = 0

        self.n = n
        self.func = func

    def __call__(self, *args, **kargs):
        """Return results of :attr:`func` after :attr:`n` calls."""
        self.n -= 1

        if self.n <= 0:
            return self.func(*args, **kargs)


class Before(After):
    """Wrap a function in a before context."""
    def __call__(self, *args, **kargs):
        self.n -= 1

        if self.n > 0:
            return self.func(*args, **kargs)


class Compose(object):
    """Wrap a function in a compose context."""
    def __init__(self, *funcs):
        self.funcs = funcs

    def __call__(self, *args, **kargs):
        """Return results of composing :attr:`funcs`."""
        funcs = list(self.funcs)

        # Compose functions in reverse order starting with the first.
        ret = (funcs.pop())(*args, **kargs)

        for func in reversed(funcs):
            ret = func(ret)

        return ret


class Curry(object):
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
        args = self.compose_args(args)
        kargs.update(self.kargs)

        if (len(args) + len(kargs)) >= self.arity:
            curried = self.func(*args, **kargs)
        else:
            # NOTE: Use self.__class__ so that subclasses will use their own
            # class to generate next iteration of call.
            curried = self.__class__(self.func, self.arity, args, kargs)

        return curried

    def compose_args(self, new_args):
        """Combine `self.args` with `new_args` and return."""
        return tuple(list(self.args) + list(new_args))


class CurryRight(Curry):
    """Wrap a function in a curry-right context."""
    def compose_args(self, new_args):
        return tuple(list(new_args) + list(self.args))


class Debounce(object):
    """Wrap a function in a debounce context."""
    def __init__(self, func, wait, max_wait=False):
        self.func = func
        self.wait = wait
        self.max_wait = max_wait

        self.last_result = None

        # Initialize last_* times to be prior to the wait periods so that func
        # is primed to be executed on first call.
        self.last_call = now() - self.wait
        self.last_execution = (now() - max_wait if is_number(max_wait)
                               else None)

    def __call__(self, *args, **kargs):
        """Execute :attr:`func` if function hasn't been called witinin last
        :attr:`wait` milliseconds or in last :attr:`max_wait` milliseconds.
        Return results of last successful call.
        """
        present = now()

        if any([(present - self.last_call) >= self.wait,
                (self.max_wait and
                 (present - self.last_execution) >= self.max_wait)]):
            self.last_result = self.func(*args, **kargs)
            self.last_execution = present

        self.last_call = present

        return self.last_result


class Negate(object):
    """Wrap a function in a negate context."""
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kargs):
        """Return negated results of calling `self.func`."""
        return not self.func(*args, **kargs)


class Once(object):
    """Wrap a function in a once context."""
    def __init__(self, func):
        self.func = func
        self.result = None
        self.called = False

    def __call__(self, *args, **kargs):
        """Return results from the first call of `self.func`."""
        if not self.called:
            self.result = self.func(*args, **kargs)
            self.called = True

        return self.result


class Partial(object):
    """Wrap a function in a partial context."""
    def __init__(self, func, args, from_right=False):
        self.func = func
        self.args = args
        self.from_right = from_right

    def __call__(self, *args, **kargs):
        """Return results from `self.func` with `self.args` + `args. Apply args
        from left or right depending on `self.from_right`.
        """
        if self.from_right:
            args = list(args) + list(self.args)
        else:
            args = list(self.args) + list(args)

        return self.func(*args, **kargs)


class Throttle(object):
    """Wrap a function in a throttle context."""
    def __init__(self, func, wait):
        self.func = func
        self.wait = wait

        self.last_result = None
        self.last_execution = now() - self.wait

    def __call__(self, *args, **kargs):
        """Execute :attr:`func` if function hasn't been called witinin last
        :attr:`wait` milliseconds. Return results of last successful call.
        """
        present = now()

        if (present - self.last_execution) >= self.wait:
            self.last_result = self.func(*args, **kargs)
            self.last_execution = present

        return self.last_result


def after(n, func):
    """Creates a function that executes `func`, with the arguments of the
    created function, only after being called `n` times.

    Args:
        n (int): Number of times `func` must be called before it is executed.
        func (function): Function to execute.

    Returns:
        After: Function wrapped in an :class:`After` context.

    .. versionadded:: 1.0.0
    """
    return After(n, func)


def before(n, func):
    """Creates a function that executes `func`, with the arguments of the
    created function, until it has been called `n` times.

    Args:
        n (int): Number of times `func` may be executed.
        func (function): Function to execute.

    Returns:
        Before: Function wrapped in an :class:`Before` context.

    .. versionadded:: 1.1.0
    """
    return Before(n, func)


def compose(*funcs):
    """Creates a function that is the composition of the provided functions,
    where each function consumes the return value of the function that follows.
    For example, composing the functions ``f()``, ``g()``, and ``h()`` produces
    ``f(g(h()))``.

    Args:
        *funcs (function): Function(s) to compose.

    Returns:
        Compose: Function(s) wrapped in a :class:`Compose` context.

    .. versionadded:: 1.0.0
    """
    return Compose(*funcs)


def curry(func, arity=None):
    """Creates a function which accepts one or more arguments of `func` that
    when  invoked either executes `func` returning its result, if all `func`
    arguments have been provided, or returns a function that accepts one or
    more of the remaining `func` arguments, and so on.

    Args:
        func (function): Function to curry.
        arity (int, optional): Number of function arguments that can be
            accepted by curried function. Default is to use the number of
            arguments that are accepted by `func`.

    Returns:
        Curry: Function wrapped in a :class:`Curry` context.

    .. versionadded:: 1.0.0
    """
    return Curry(func, arity)


def curry_right(func, arity=None):
    """This method is like :func:`curry` except that arguments are applied to
    `func` in the manner of :func:`partial_right` instead of :func:`partial`.

    Args:
        func (function): Function to curry.
        arity (int, optional): Number of function arguments that can be
            accepted by curried function. Default is to use the number of
            arguments that are accepted by `func`.

    Returns:
        CurryRight: Function wrapped in a :class:`CurryRight` context.

    .. versionadded:: 1.1.0
    """
    return CurryRight(func, arity)


def debounce(func, wait, max_wait=False):
    """Creates a function that will delay the execution of `func` until after
    `wait` milliseconds have elapsed since the last time it was invoked.
    Subsequent calls to the debounced function will return the result of the
    last `func` call.

    Args:
        func (function): Function to execute.
        wait (int): Milliseconds to wait before executing `func`.
        max_wait (optional): Maximum time to wait before executing `func`.

    Returns:
        Debounce: Function wrapped in a :class:`Debounce` context.

    .. versionadded:: 1.0.0
    """
    return Debounce(func, wait, max_wait=max_wait)


def delay(func, wait, *args, **kargs):
    """Executes the `func` function after `wait` milliseconds. Additional
    arguments will be provided to `func` when it is invoked.

    Args:
        func (function): Function to execute.
        wait (int): Milliseconds to wait before executing `func`.
        *args (optional): Arguments to pass to `func`.
        **kargs (optional): Keyword arguments to pass to `func`.

    Returns:
        mixed: Return from `func`.

    .. versionadded:: 1.0.0
    """
    time.sleep(wait / 1000.0)
    return func(*args, **kargs)


def negate(func):
    """Creates a function that negates the result of the predicate `func`. The
    `func` function is executed with the arguments of the created function.

    Args:
        func (function): Function to negate execute.

    Returns:
        Negate: Function wrapped in a :class:`Negate` context.

    .. versionadded:: 1.1.0
    """
    return Negate(func)


def once(func):
    """Creates a function that is restricted to execute func once. Repeat calls
    to the function will return the value of the first call.

    Args:
        func (function): Function to execute.

    Returns:
        Once: Function wrapped in a :class:`Once` context.

    .. versionadded:: 1.0.0
    """
    return Once(func)


def partial(func, *args):
    """Creates a function that, when called, invokes `func` with any additional
    partial arguments prepended to those provided to the new function.

    Args:
        func (function): Function to execute.
        *args (optional): Partial arguments to prepend to function call.

    Returns:
        Partial: Function wrapped in a :class:`Partial` context.

    .. versionadded:: 1.0.0
    """
    return Partial(func, args)


def partial_right(func, *args):
    """This method is like :func:`partial` except that partial arguments are
    appended to those provided to the new function.

    Args:
        func (function): Function to execute.
        *args (optional): Partial arguments to append to function call.

    Returns:
        Partial: Function wrapped in a :class:`Partial` context.

    .. versionadded:: 1.0.0
    """
    return Partial(func, args, from_right=True)


def throttle(func, wait):
    """Creates a function that, when executed, will only call the `func`
    function at most once per every `wait` milliseconds. Subsequent calls to
    the throttled function will return the result of the last `func` call.

    Args:
        func (function): Function to throttle.
        wait (int): Milliseconds to wait before calling `func` again.

    Returns:
        mixed: Results of last `func` call.

    .. versionadded:: 1.0.0
    """
    return Throttle(func, wait)


def wrap(value, func):
    """Creates a function that provides value to the wrapper function as its
    first argument. Additional arguments provided to the function are appended
    to those provided to the wrapper function.

    Args:
        value (mixed): Value provided as first argument to function call.
        func (function): Function to execute.

    Returns:
        Partial: Function wrapped in a :class:`Partial` context.

    .. versionadded:: 1.0.0
    """
    return Partial(func, (value,))
