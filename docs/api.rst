.. _api:

*************
API Reference
*************

.. testsetup::

    import math
    import operator
    import re
    from pydash.functions import Curry, CurryRight
    from pydash import *


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

py\_ Instance
=============

There is a special ``py_`` instance available from ``pydash`` that supports method calling and method chaining from a single object:


.. code-block:: python

    from pydash import py_

    # Method calling
    py_.initial([1, 2, 3, 4, 5]) == [1, 2, 3, 4]

    # Method chaining
    py_([1, 2, 3, 4, 5]).initial().value() == [1, 2, 3, 4]

    # Method aliasing to underscore suffixed methods that shadow builtin names
    py_.map is py_.map_
    py_([1, 2, 3]).map(_.to_string).value() == py_([1, 2, 3]).map_(_.to_string).value()


The ``py_`` instance is basically a combination of using ``pydash.<function>`` and ``pydash.chain``.

A full listing of aliased ``py_`` methods:

- ``_.object`` is :func:`pydash.arrays.object_`
- ``_.slice`` is :func:`pydash.arrays.slice_`
- ``_.zip`` is :func:`pydash.arrays.zip_`
- ``_.all`` is :func:`pydash.collections.all_`
- ``_.any`` is :func:`pydash.collections.any_`
- ``_.filter`` is :func:`pydash.collections.filter_`
- ``_.map`` is :func:`pydash.collections.map_`
- ``_.max`` is :func:`pydash.collections.max_`
- ``_.min`` is :func:`pydash.collections.min_`
- ``_.reduce`` is :func:`pydash.collections.reduce_`
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
