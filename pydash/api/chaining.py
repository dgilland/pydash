"""Chaining
"""

from __future__ import absolute_import

import pydash

from .exceptions import InvalidMethod
from .._compat import text_type


class Chain(object):
    """Enables chaining of pydash functions."""

    def __init__(self, value):
        self._value = value

    def value(self):
        """Return current value of the chain operations."""
        return self._value

    value_of = value

    def to_string(self):
        """Return current value as string."""
        return text_type(self.value())

    def __getattr__(self, attr):
        """Proxy attribute access to :mod:`pydash`."""
        method = getattr(pydash, attr, None)

        # TODO: Be more stringent about which methods are valid?

        if callable(method):
            return ChainWrapper(self.value(), getattr(pydash, attr))
        else:
            raise InvalidMethod('Invalid pydash method: {0}'.format(attr))


class ChainWrapper(object):
    """Wrap :mod:`pydash` method call within a :class:`Chain` context."""
    def __init__(self, value, method):
        self.value = value
        self.method = method

    def __call__(self, *args, **kargs):
        """Invoke the :attr:`method` with :attr:`value` as the first argument
        and return a new :class:`Chain` object with the return value.
        """
        return Chain(self.method(self.value, *args, **kargs))


def chain(value):
    """Creates a :class:`Chain` object which wraps the given value to enable
    intuitive method chaining.
    """
    return Chain(value)


def tap(value, interceptor):
    """Invokes interceptor with the value as the first argument and then
    returns value. The purpose of this method is to "tap into" a method chain
    in order to perform operations on intermediate results within the chain.
    """
    interceptor(value)
    return value
