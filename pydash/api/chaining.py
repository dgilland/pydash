"""Chaining

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import

import pydash

from .exceptions import InvalidMethod
from .._compat import text_type


__all__ = [
    'chain',
    'tap',
]


class Chain(object):
    """Enables chaining of pydash functions."""

    def __init__(self, value):
        self._value = value

    def value(self):
        """Return current value of the chain operations.

        Returns:
            mixed: Current value of chain operations.

        See Also:
            - :meth:`value` (main definition)
            - :meth:`value_of` (alias)
        """
        return self._value

    value_of = value

    def to_string(self):
        """Return current value as string.

        Returns:
            str: Current value of chain operations casted to ``str``.
        """
        return text_type(self.value())

    def __getattr__(self, attr):
        """Proxy attribute access to :mod:`pydash`.

        Args:
            attr (str): Name of :mod:`pydash` function to chain.

        Returns:
            ChainWrapper: New instance of :class:`ChainWrapper` with value
                passed on.

        Raises:
            InvalidMethod: Raised if `attr` is not a valid :mod:`pydash`
                function.
        """
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

        Returns:
            Chain: New instance of :class:`Chain` with the results of
                :attr:`method` passed in as value.
        """
        return Chain(self.method(self.value, *args, **kargs))


def chain(value):
    """Creates a :class:`Chain` object which wraps the given value to enable
    intuitive method chaining.

    Args:
        value (mixed): Value to initialize chain operations with.

    Returns:
        :class:`Chain`: Instance of :class:`Chain` initialized with `value`.

    .. versionadded:: 1.0.0
    """
    return Chain(value)


def tap(value, interceptor):
    """Invokes interceptor with the value as the first argument and then
    returns value. The purpose of this method is to "tap into" a method chain
    in order to perform operations on intermediate results within the chain.

    Args:
        value (mixed): Current value of chain operation.
        interceptor (function): Function called on `value`.

    Returns:
        mixed: `value` after `interceptor` call.

    .. versionadded:: 1.0.0
    """
    interceptor(value)
    return value
