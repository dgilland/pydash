.. _fp:

*************
FP Variations
*************

Pydash exposes a variant set of its functions which are auto-curried,
iteratee-first, data-last, and non-mutating.
These functions are available in ``pydash.fp``.
The creation of this module is inspired by, and reflects much of the
functionality in ``lodash/fp``, however it differs in a few significant
ways as well.

Currying
=========

The fp variant functions are curried, meaning that one can provide
arguments in multiple function calls, like so:

.. code-block:: python

    # the following two calls are equivalent
    fp.union_by(lambda x: x % 2, [1, 2, 3], [2, 3, 4])

    fp.union_by(lambda x: x % 2)([1, 2, 3])([2, 3, 4])


This means that each function must receive a fixed minimum 
number of arguments.  Keyword arguments are not supported.
As much as possible, support is provided for multiple data
arguments where the original function allows it:


.. code-block:: python

    fp.intersection_by(round)([1.2, 1.5, 1.7, 2.8], [0.9, 3.2], [1.1])

In some cases, a default parameter value can be specified by passing
``None``:

.. code-block:: python

    fp.intersection_by(None, [1, 2, 3], [2, 3, 4])

Rearranged Arguments
=====================

Method arguments are rearranged to facilitate composition.
In most cases, iteratee is given first and data last.


Placeholder
===========

It is possible to provide arguments in a different order by use of the
placeholder.  A placeholder is filled by the first available argument:

.. code-block:: python

    from pydash.fp import _

    # the following two calls are equivalent
    fp.intersperse(0)([1, 2, 3])

    fp.intersperse(_, [1, 2, 3])(0)


No Mutation
=============

Some pydash functions mutate the target object.
The fp variants of these functions are *non-mutating*.


Iteratee Capping
=================

In contradistinction to ``lodash/fp``, iteratees in ``pydash.fp`` are *not*
capped.


Arrays
======

.. automodule:: pydash.fp.arrays
    :members:
