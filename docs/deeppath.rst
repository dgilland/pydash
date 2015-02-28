.. _deeppath:

Deep Path Strings
=================

.. testsetup::

    import pydash


A deep path string is used to access a nested data structure of arbitrary length. Each level is separated by a ``"."`` and can be used on both dictionaries and lists. If a ``"."`` is contained in one of the dictionary keys, then it can be escaped using ``"\"``. For accessing a dictionary key that is a number, it can be wrapped in brackets like ``"[1]"``.

Examples:


.. doctest::

    >>> data = {'a': {'b': {'c': [0, 0, {'d': [0, {1: 2}]}]}}}
    >>> pydash.deep_get(data, 'a.b.c.2.d.1.[1]')
    2

    >>> data = {'a': {'b.c.d': 2}}
    >>> pydash.deep_get(data, r'a.b\.c\.d')
    2


Functions that support deep path strings include:

- :func:`pydash.collections.deep_pluck`
- :func:`pydash.objects.deep_get`
- :func:`pydash.objects.deep_has`
- :func:`pydash.objects.deep_set`
- :func:`pydash.utilities.deep_property`/:func:`pydash.utilities.deep_prop`

Pydash's callback system also supports the deep property style callback using deep path strings.