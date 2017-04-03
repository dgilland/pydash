.. _deeppath:

Deep Path Strings
=================

.. testsetup::

    import pydash


A deep path string is used to access a nested data structure of arbitrary length. Each level is separated by a ``"."`` and can be used on both dictionaries and lists. If a ``"."`` is contained in one of the dictionary keys, then it can be escaped using ``"\"``. For accessing a dictionary key that is a number, it can be wrapped in brackets like ``"[1]"``.

Examples:


.. doctest::

    >>> data = {'a': {'b': {'c': [0, 0, {'d': [0, {1: 2}]}]}}}
    >>> pydash.get(data, 'a.b.c.2.d.1.[1]')
    2

    >>> data = {'a': {'b.c.d': 2}}
    >>> pydash.get(data, r'a.b\.c\.d')
    2


Pydash's callback system supports the deep property style callback using deep path strings.
