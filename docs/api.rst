.. _api:

*************
API Reference
*************

All public functions are available from the main module.


.. code-block:: python

    import pydash

    pydash.<function>


This is the recommended way to use pydash.


.. code-block:: python

    # OK (importing main module)
    import pydash
    pydash.where({})

    # OK (import from main module)
    from pydash import where
    where({})

    # NOT RECOMMENDED (importing from submodule)
    from pydash.collections import where


Only the main pydash module API is guaranteed to adhere to semver. It's possible that backwards incompatibility outside the main module API could be broken between minor releases.


.. _api-dash-instance:

"_" Instance
============

There is a special ``_`` instance available from ``pydash`` that supports method calling and method chaining from a single object:


.. code-block:: python

    from pydash import _

    # Method calling
    _.initial([1, 2, 3, 4, 5]) == [1, 2, 3, 4]

    # Method chaining
    _([1, 2, 3, 4, 5]).initial().value() == [1, 2, 3, 4]

    # Method aliasing to underscore suffixed methods that shadow builtin names
    _.map is _.map_
    _([1, 2, 3]).map(_.to_string).value() == _([1, 2, 3]).map_(_.to_string).value()


The ``_`` instance is basically a combination of using ``pydash.<function>`` and ``pydash.chain``.

A full listing of aliased ``_`` methods:

- ``_.object`` is :func:`pydash.arrays.object_`
- ``_.slice`` is :func:`pydash.arraysslice_`
- ``_.zip`` is :func:`pydash.arrayszip_`
- ``_.all`` is :func:`pydash.collections.all_`
- ``_.any`` is :func:`pydash.collections.any_`
- ``_.filter`` is :func:`pydash.collections.filter_`
- ``_.map`` is :func:`pydash.collection.map_`
- ``_.max`` is :func:`pydash.collection.max_`
- ``_.min`` is :func:`pydash.collection.min_`
- ``_.reduce`` is :func:`pydash.collection.reduce_`
- ``_.pow`` is :func:`pydash.numerical.pow_`
- ``_.round`` is :func:`pydash.numerical.round_`
- ``_.sum`` is :func:`pydash.numerical.sum_`
- ``_.property`` is :func:`pydash.utilities.property_`
- ``_.range`` is :func:`pydash.utilities.range_`


Arrays
======

.. automodule:: pydash.arrays
    :members:


Chaining
========

.. automodule:: pydash.chaining
    :members:


Collections
===========

.. automodule:: pydash.collections
    :members:


Functions
=========

.. automodule:: pydash.functions
    :members:


Numerical
=========

.. automodule:: pydash.numerical
    :members:


Objects
=======

.. automodule:: pydash.objects
    :members:


Predicates
==========

.. automodule:: pydash.predicates
    :members:


Strings
=======

.. automodule:: pydash.strings
    :members:


Utilities
=========

.. automodule:: pydash.utilities
    :members:
