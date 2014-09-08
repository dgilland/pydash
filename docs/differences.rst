Lo-Dash Differences
===================


Naming Conventions
------------------

pydash adheres to the following conventions:

- Function names use ``snake_case`` instead of ``camelCase``.
- Any Lo-Dash function that shares its name with a reserved Python keyword will have an ``_`` appended after it (e.g. ``filter`` in Lo-Dash would be ``filter_`` in pydash.
- Lo-Dash's ``toArray()`` is pydash's ``to_list()``.
- Lo-Dash's ``functions()`` is pydash's ``callables()``. This particular name difference was chosen in order to allow for the ``functions.py`` module file to exist at root of the project. Previously, ``functions.py`` existed in ``pydash/api/`` but in ``v2.0.0``, it was decided to move everything in ``api/`` to ``pydash/``. Therefore, In to avoid import ambiguities, the ``functions()`` function was renamed.


Callbacks
---------

Callbacks in pydash are handled a little differently due to differences between Javascript and Python:

- Extra callback args must be explictly handled. In Javascript, it's perfectly fine to pass in extra arguments to a function that aren't explictly accepted by that function (e.g. ``function foo(a1){}; foo(1, 2, 3);``). In Python, those extra arguments must be explictly handled (e.g. ``def foo(a1, *args): ...; foo(1, 2, 3)``). Therefore, callbacks passed to ``pydash`` functions must use named args or a catch-all like ``*args`` since each callbacks will be passed arguments like ``(value, index|key, array)``. **NOTE:** *Future versions of pydash may attempt to infer the number of arguments a callback can handle and only pass what's supported.*


Extra Aliases
-------------

The following extra function aliases exist in pydash but not in Lo-Dash:

- :func:`pydash.utilities.prop` >> :func:`pydash.utilities.property_`
- :func:`pydash.objects.is_re` >> :func:`pydash.objects.is_reg_exp`
- :func:`pydash.strings.escape_re` >> :func:`pydash.strings.escape_reg_exp`


Extra Functions
---------------

The following functions exist in pydash but not in Lo-Dash:

- `pydash.arrays.intercalate`
- `pydash.arrays.interleave`
- `pydash.arrays.intersperse`
- `pydash.functions.iterated`


Function Behavior
-----------------

Some of pydash's functions behave differently:

- :func:`pydash.api.utilities.memoize` uses all passed in arguments as the cache key by default instead of only using the first argument.


Templating
----------

- pydash doesn't have ``template()``. See :ref:`Templating <templating>` for more details.
