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

    # OK
    from pydash import where
    where({})

    # OK
    import pydash
    pydash.where({})

    # NOT OK
    from pydash.collections import where


Only the main pydash module API is guaranteed to adhere to semver. It's possible that backwards incompatibility could be broken between minor releases outside the main module API.


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


The ``_`` instance is basically a combination of using ``pydash.<function>`` and ``pydash.chain``.


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
