.. _differences:

Lo-Dash Differences
===================


Naming Conventions
------------------

pydash adheres to the following conventions:

- Function names use ``snake_case`` instead of ``camelCase``.
- Any Lo-Dash function that shares its name with a reserved Python keyword will have an ``_`` appended after it (e.g. ``filter`` in Lo-Dash would be ``filter_`` in pydash.
- Lo-Dash's ``toArray()`` is pydash's ``to_list()``.
- Lo-Dash's ``functions()`` is pydash's ``callables()``. This particular name difference was chosen in order to allow for the ``functions.py`` module file to exist at root of the project. Previously, ``functions.py`` existed in ``pydash/api/`` but in ``v2.0.0``, it was decided to move everything in ``api/`` to ``pydash/``. Therefore, In to avoid import ambiguities, the ``functions()`` function was renamed.


.. _differences-callbacks:

Callbacks
---------

There are a few differences between extra callback style support:

- Lo-Dash's property style callback form uses shallow property access while the same form in pydash uses deep property access via the deep path string.
- Pydash has an explicit shallow property access of the form ``['some_property']``.


Extra Functions
---------------

In addition to porting Lo-Dash, pydash contains functions found in lodashcontrib_, lodashdeep_, lodashmath_, and underscorestring_.


Function Behavior
-----------------

Some of pydash's functions behave differently:

- :func:`pydash.utilities.memoize` uses all passed in arguments as the cache key by default instead of only using the first argument.


Templating
----------

- pydash doesn't have ``template()``. See :ref:`Templating <templating>` for more details.


.. _lodashcontrib: https://github.com/TheNodeILs/lodash-contrib
.. _lodashdeep: https://github.com/marklagendijk/lodash-deep
.. _lodashmath: https://github.com/Delapouite/lodash.math
.. _underscorestring: https://github.com/epeli/underscore.string
