Quickstart
==========

.. doctest::

    >>> import pydash as pyd

    # Arrays
    >>> pyd.flatten([1, 2, [3, [4, 5, [6, 7]]]])
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
    >>> pyd.chain([1, 2, 3, 4]).without(2, 3).reject(lambda x, *args: x > 1).value()
    [1]


.. seealso::
    For further details consult :ref:`Main API Reference <apimain>`.
