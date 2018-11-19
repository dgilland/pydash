Quickstart
==========

The functions available from pydash can be used in two styles.

The first is by using the module directly or importing from it:


.. doctest::

    >>> import pydash

    # Arrays
    >>> pydash.flatten([1, 2, [3, [4, 5, [6, 7]]]])
    [1, 2, 3, [4, 5, [6, 7]]]

    >>> pydash.flatten_deep([1, 2, [3, [4, 5, [6, 7]]]])
    [1, 2, 3, 4, 5, 6, 7]

    # Collections
    >>> pydash.map_([{'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}], 'name')
    ['moe', 'larry']

    # Functions
    >>> curried = pydash.curry(lambda a, b, c: a + b + c)
    >>> curried(1, 2)(3)
    6

    # Objects
    >>> pydash.omit({'name': 'moe', 'age': 40}, 'age')
    {'name': 'moe'}

    # Utilities
    >>> pydash.times(3, lambda index: index)
    [0, 1, 2]

    # Chaining
    >>> pydash.chain([1, 2, 3, 4]).without(2, 3).reject(lambda x: x > 1).value()
    [1]


The second style is to use the ``py_`` or ``_`` instances (they are the same object as two different aliases):


.. doctest::

    >>> from pydash import py_

    # Method calling which is equivalent to pydash.flatten(...)
    >>> py_.flatten([1, 2, [3, [4, 5, [6, 7]]]])
    [1, 2, 3, [4, 5, [6, 7]]]

    # Method chaining which is equivalent to pydash.chain(...)
    >>> py_([1, 2, 3, 4]).without(2, 3).reject(lambda x: x > 1).value()
    [1]

    # Late method chaining
    >>> py_().without(2, 3).reject(lambda x: x > 1)([1, 2, 3, 4])
    [1]


.. seealso::
    For further details consult :ref:`API Reference <api>`.
