.. _differences:

Lodash Differences
===================


Naming Conventions
------------------

pydash adheres to the following conventions:

- Function names use ``snake_case`` instead of ``camelCase``.
- Any Lodash function that shares its name with a reserved Python keyword will have an ``_`` appended after it (e.g. ``filter`` in Lodash would be ``filter_`` in pydash).
- Lodash's ``toArray()`` is pydash's ``to_list()``.
- Lodash's ``functions()`` is pydash's ``callables()``. This particular name difference was chosen in order to allow for the ``functions.py`` module file to exist at root of the project. Previously, ``functions.py`` existed in ``pydash/api/`` but in ``v2.0.0``, it was decided to move everything in ``api/`` to ``pydash/``. Therefore, to avoid import ambiguities, the ``functions()`` function was renamed.
- Lodash's ``is_native()`` is pydash's ``is_builtin()``. This aligns better with Python's builtins terminology.


Callbacks
---------

There are a few differences between extra callback style support:

- Pydash has an explicit shallow property access of the form ``['some_property']`` as in ``pydash.map_([{'a.b': 1, 'a': {'b': 3}}, {'a.b': 2, 'a': {'b': 4}}], ['a.b'])`` would evaulate to ``[1, 2]`` and not ``[3, 4]`` (as would be the case for ``'a.b'``).


Extra Functions
---------------

In addition to porting Lodash, pydash contains functions found in lodashcontrib_, lodashdeep_, lodashmath_, and underscorestring_.


Function Behavior
-----------------

Some of pydash's functions behave differently:

- :func:`pydash.utilities.memoize` uses all passed in arguments as the cache key by default instead of only using the first argument.


Templating
----------

- pydash doesn't have ``template()``. See :ref:`Templating <templating>` for more details.


.. _lodashcontrib: https://github.com/node4good/lodash-contrib
.. _lodashdeep: https://github.com/marklagendijk/lodash-deep
.. _lodashmath: https://github.com/Delapouite/lodash.math
.. _underscorestring: https://github.com/epeli/underscore.string
