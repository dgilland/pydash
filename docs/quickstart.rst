Quickstart
==========

The functions available from pydash can be used in two styles.

The first is by using the module directly or importing from it:


.. doctest::

    >>> import pydash as pyd
    >>> from pydash import flatten

    # Arrays
    >>> flatten([1, 2, [3, [4, 5, [6, 7]]]])
    [1, 2, 3, [4, 5, [6, 7]]]

    >>> pyd.flatten_deep([1, 2, [3, [4, 5, [6, 7]]]])
    [1, 2, 3, 4, 5, 6, 7]

    # Collections
    >>> pyd.pluck([{'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}], 'name')
    ['moe', 'larry']

    # Functions
    >>> curried = pyd.curry(lambda a, b, c: a + b + c)
    >>> curried(1, 2)(3)
    6

    # Objects
    >>> pyd.omit({'name': 'moe', 'age': 40}, 'age')
    {'name': 'moe'}

    # Utilities
    >>> pyd.times(3, lambda index: index)
    [0, 1, 2]

    # Chaining
    >>> pyd.chain([1, 2, 3, 4]).without(2, 3).reject(lambda x: x > 1).value()
    [1]


The second style is to use the ``_`` instance:


.. doctest::

    >>> from pydash import _

    >>> _.flatten([1, 2, [3, [4, 5, [6, 7]]]])
    [1, 2, 3, [4, 5, [6, 7]]]

    >>> _([1, 2, 3, 4]).without(2, 3).reject(lambda x: x > 1).value()
    [1]


.. seealso::
    For further details consult :ref:`API Reference <api>`.
