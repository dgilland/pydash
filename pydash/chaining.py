"""Method chaining interface.

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import

import pydash as pyd


__all__ = [
    'chain',
    'tap',
    'thru',
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
        if isinstance(self._value, ChainWrapper):
            # pylint: disable=maybe-no-member
            self._value = self._value.unwrap()
        return self._value

    value_of = value

    def to_string(self):
        """Return current value as string.

        Returns:
            str: Current value of chain operations casted to ``str``.
        """
        return pyd.to_string(self.value())

    @staticmethod
    def get_method(name):
        """Return valid pydash method.

        Args:
            name (str): Name of pydash method to get.

        Returns:
            function: pydash callable.

        Raises:
            InvalidMethod: Raised if `name` is not a valid :mod:`pydash`
                method.
        """
        method = getattr(pyd, name, None)

        if not callable(method) and not name.endswith('_'):
            # Alias method names not ending in underscore to their underscore
            # counterpart. This allows chaining of functions like "map_()"
            # using "map()" instead.
            method = getattr(pyd, name + '_', None)

        if not callable(method):
            raise pyd.InvalidMethod('Invalid pydash method: {0}'.format(name))

        return method

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
        return ChainWrapper(self._value, self.get_method(attr))


class ChainWrapper(object):
    """Wrap :mod:`pydash` method call within a :class:`ChainWrapper` context.
    """
    def __init__(self, value, method):
        self._value = value
        self.method = method
        self.args = ()
        self.kargs = {}

    def unwrap(self):
        """Execute :meth:`method` with :attr:`_value`, :attr:`args`, and
        :attr:`kargs`. If :attr:`_value` is an instance of
        :class:`ChainWrapper`, then unwrap it before calling :attr:`method`.
        """
        if isinstance(self._value, ChainWrapper):
            self._value = self._value.unwrap()
        return self.method(self._value, *self.args, **self.kargs)

    def __call__(self, *args, **kargs):
        """Invoke the :attr:`method` with :attr:`value` as the first argument
        and return a new :class:`Chain` object with the return value.

        Returns:
            Chain: New instance of :class:`Chain` with the results of
                :attr:`method` passed in as value.
        """
        self.args = args
        self.kargs = kargs
        return Chain(self)


class _Dash(object):
    """Class that provides attribute access to valid :mod:`pydash` methods and
    callable access to :mod:`pydash` method chaining.
    """

    def __getattr__(self, attr):
        """Proxy to :meth:`Chain.get_method`."""
        return Chain.get_method(attr)

    def __call__(self, value):
        """Return a new instance of :class:`Chain` with `value` as the seed."""
        return Chain(value)


def chain(value):
    """Creates a :class:`Chain` object which wraps the given value to enable
    intuitive method chaining. Chaining is lazy and won't compute a final value
    until :meth:`Chain.value` is called.

    Args:
        value (mixed): Value to initialize chain operations with.

    Returns:
        :class:`Chain`: Instance of :class:`Chain` initialized with `value`.

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.0.0
        Made chaining lazy.
    """
    return Chain(value)


def tap(value, interceptor):
    """Invokes `interceptor` with the `value` as the first argument and then
    returns `value`. The purpose of this method is to "tap into" a method chain
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


def thru(value, interceptor):
    """Returns the result of calling `interceptor` on `value`. The purpose of
    this method is to pass `value` through a function during a method chain.

    Args:
        value (mixed): Current value of chain operation.
        interceptor (function): Function called with `value`.

    Returns:
        mixed: Results of ``interceptor(value)``.

    .. versionadded:: 2.0.0
    """
    return interceptor(value)
