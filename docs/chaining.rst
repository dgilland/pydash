.. _method-chaining:

Method Chaining
***************

Method chaining in pydash is quite simple.


An initial value is provided:


.. code-block:: python

    from pydash import py_
    py_([1, 2, 3, 4])

    # Or through the chain() function
    import pydash
    pydash.chain([1, 2, 3, 4])


Methods are chained:


.. code-block:: python

    py_([1, 2, 3, 4]).without(2, 3).reject(lambda x: x > 1)


A final value is computed:


.. code-block:: python

    result = py_([1, 2, 3, 4]).without(2, 3).reject(lambda x: x > 1).value()


Lazy Evaluation
===============

Method chaining is deferred (lazy) until ``.value()`` (or it's aliases ``.value_of`` or ``.run()``) is called:

.. doctest::

    >>> from __future__ import print_function
    >>> from pydash import py_

    >>> def echo(value): print(value)

    >>> lazy = py_([1, 2, 3, 4]).each(echo)

    # None of the methods have been called yet.

    >>> result = lazy.value()
    1
    2
    3
    4

    # Each of the chained methods have now been called.

    >>> assert result == [1, 2, 3, 4]

    >>> result = lazy.run()
    1
    2
    3
    4


Committing a Chain
==================

If one wishes to create a new chain object seeded with the computed value of another chain, then one can use the ``commit`` method:

.. doctest::

    >>> committed = lazy.commit()
    1
    2
    3
    4

    >>> committed.value()
    [1, 2, 3, 4]

    >>> lazy.value()
    1
    2
    3
    4
    [1, 2, 3, 4]


Committing is equivalent to:

.. code-block:: python

    committed = py_(lazy.value())


Late Value Passing
==================

In :ref:`v3.0.0 <changelog-v3.0.0>` the concept of late value passing was introduced to method chaining. This allows method chains to be re-used with different root values supplied. Essentially, ad-hoc functions can be created via the chaining syntax.


.. doctest::

    >>> square_sum = py_().power(2).sum()
    >>> assert square_sum([1, 2, 3]) == 14
    >>> assert square_sum([4, 5, 6]) == 77

    >>> square_sum_square = square_sum.power(2)
    >>> assert square_sum_square([1, 2, 3]) == 196
    >>> assert square_sum_square([4, 5, 6]) == 5929


Planting a Value
================

To replace the initial value of a chain, use the ``plant`` method which will return a cloned chained using the new initial value:

.. doctest::

    >>> chained = py_([1, 2, 3, 4]).power(2).sum()
    >>> chained.run()
    30
    >>> rechained = chained.plant([5, 6, 7, 8])
    >>> rechained.run()
    174
    >>> chained.run()
    30


Module Access
=============

Another feature of the ``py_`` object, is that it provides module access to ``pydash``:


.. doctest::

    >>> import pydash
    >>> from pydash import py_

    >>> assert py_.add is pydash.add
    >>> py_.add([1, 2, 3]) == pydash.add([1, 2, 3])
    True


Through ``py_`` any function that ends with ``"_"`` can be accessed without the trailing ``"_"``:


.. doctest::

    >>> py_.filter([1, 2, 3], lambda x: x > 1) == pydash.filter_([1, 2, 3], lambda x: x > 1)
    True

