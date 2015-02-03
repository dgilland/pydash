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

Method chaining is lazy until ``.value()`` is called. After ``.value()`` is called, the computed value is stored so that execution only happens once:

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

    >>> result = lazy.value()

    # The computed value is returned without calling any of the methods again.

    >>> assert result == [1, 2, 3, 4]


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

