# -*- coding: utf-8 -*-
"""Method chaining interface.

.. testsetup::

    from pydash.arrays import *

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import

import pydash as pyd
from .helpers import NoValue


__all__ = (
    'chain',
    'tap',
    'thru',
)


class Chain(object):
    """Enables chaining of :attr:`module` functions."""

    #: Object that contains attribute references to available methods.
    module = pyd

    def __init__(self, value=NoValue):
        self._value = value

    def value(self):
        """Return current value of the chain operations.

        Returns:
            mixed: Current value of chain operations.

        See Also:
            - :meth:`value` (main definition)
            - :meth:`value_of` (alias)
        """
        return self(self._value)

    value_of = value
    run = value

    def to_string(self):
        """Return current value as string.

        Returns:
            str: Current value of chain operations casted to ``str``.
        """
        return self.module.to_string(self.value())

    @classmethod
    def get_method(cls, name):
        """Return valid :attr:`module` method.

        Args:
            name (str): Name of pydash method to get.

        Returns:
            function: :attr:`module` callable.

        Raises:
            InvalidMethod: Raised if `name` is not a valid :attr:`module`
                method.
        """
        method = getattr(cls.module, name, None)

        if not callable(method) and not name.endswith('_'):
            # Alias method names not ending in underscore to their underscore
            # counterpart. This allows chaining of functions like "map_()"
            # using "map()" instead.
            method = getattr(cls.module, name + '_', None)

        if not callable(method):
            raise cls.module.InvalidMethod(('Invalid pydash method: {0}'
                                            .format(name)))

        return method

    def __getattr__(self, attr):
        """Proxy attribute access to :attr:`module`.

        Args:
            attr (str): Name of :attr:`module` function to chain.

        Returns:
            ChainWrapper: New instance of :class:`ChainWrapper` with value
                passed on.

        Raises:
            InvalidMethod: Raised if `attr` is not a valid function.
        """
        return ChainWrapper(self._value, self.get_method(attr))

    def __call__(self, value):
        """Return result of passing `value` through chained methods.

        Args:
            value (mixed): Initial value to pass through chained methods.

        Returns:
            mixed: Result of method chain evaluation of `value`.
        """
        if isinstance(self._value, ChainWrapper):
            # pylint: disable=maybe-no-member
            value = self._value.unwrap(value)
        return value


class ChainWrapper(object):
    """Wrap :class:`Chain` method call within a :class:`ChainWrapper` context.
    """
    def __init__(self, value, method):
        self._value = value
        self.method = method
        self.args = ()
        self.kargs = {}

    def _generate(self):
        """Generate a copy of this instance."""
        # pylint: disable=attribute-defined-outside-init
        new = self.__class__.__new__(self.__class__)
        new.__dict__ = self.__dict__.copy()
        return new

    def unwrap(self, value=NoValue):
        """Execute :meth:`method` with :attr:`_value`, :attr:`args`, and
        :attr:`kargs`. If :attr:`_value` is an instance of
        :class:`ChainWrapper`, then unwrap it before calling :attr:`method`.
        """
        # Generate a copy of ourself so that we don't modify the chain wrapper
        # _value directly. This way if we are late passing a value, we don't
        # "freeze" the chain wrapper value when a value is first passed.
        # Otherwise, we'd locked the chain wrapper value permanently and not be
        # able to reuse it.
        wrapper = self._generate()

        if isinstance(wrapper._value, ChainWrapper):
            wrapper._value = wrapper._value.unwrap(value)

        if wrapper._value is not NoValue:
            value = wrapper._value

        return wrapper.method(value, *wrapper.args, **wrapper.kargs)

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

    def __call__(self, value=NoValue):
        """Return a new instance of :class:`Chain` with `value` as the seed."""
        return Chain(value)


def chain(value=NoValue):
    """Creates a :class:`Chain` object which wraps the given value to enable
    intuitive method chaining. Chaining is lazy and won't compute a final value
    until :meth:`Chain.value` is called.

    Args:
        value (mixed): Value to initialize chain operations with.

    Returns:
        :class:`Chain`: Instance of :class:`Chain` initialized with `value`.

    Example:

        >>> chain([1, 2, 3, 4]).map(lambda x: x * 2).sum().value()
        20
        >>> chain().map(lambda x: x * 2).sum()([1, 2, 3, 4])
        20

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.0.0
        Made chaining lazy.

    .. versionchanged:: 3.0.0
        Added support for late passing of `value`.
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

    Example:

        >>> data = []
        >>> def log(value): data.append(value)
        >>> chain([1, 2, 3, 4]).map(lambda x: x * 2).tap(log).value()
        [2, 4, 6, 8]
        >>> data
        [[2, 4, 6, 8]]

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

    Example:

        >>> chain([1, 2, 3, 4]).thru(lambda x: x * 2).value()
        [1, 2, 3, 4, 1, 2, 3, 4]

    .. versionadded:: 2.0.0
    """
    return interceptor(value)
