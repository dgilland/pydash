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

As of ``v2.0.0``, callback functions no longer need to handle all possible arguments. Prior to ``v2.0.0``, callbacks had to define all arguments or have star-args:


.. code-block:: python

    # Valid in v1
    def mycallback(item, value, obj):
        pass

    # Valid in v1
    def mycallback(item, *args):
        pass

    # Invalid in v1
    def mycallback(item):
        pass


But in ``v2.0.0`` partial callback signatures are handled properly:


.. code-block:: python

    # Valid in v2
    def mycallback(item, value, obj):
        pass

    # Valid in v2
    def mycallback(item, *args):
        pass

    # Valid in v2
    def mycallback(item):
        pass


Extra Aliases
-------------

The following extra function aliases exist in pydash but not in Lo-Dash:

- :func:`pydash.utilities.prop` >> :func:`pydash.utilities.property_`
- :func:`pydash.objects.is_re` >> :func:`pydash.objects.is_reg_exp`
- :func:`pydash.strings.escape_re` >> :func:`pydash.strings.escape_reg_exp`


Extra Functions
---------------

The following functions exist in pydash but not in Lo-Dash:

- `pydash.arrays.cat`
- `pydash.functions.conjoin`
- `pydash.functions.disjoin`
- `pydash.strings.explode`
- `pydash.objects.get_path`
- `pydash.objects.has_path`
- `pydash.strings.implode`
- `pydash.arrays.intercalate`
- `pydash.arrays.interleave`
- `pydash.arrays.intersperse`
- `pydash.predicates.is_associative`
- `pydash.predicates.is_even`
- `pydash.predicates.is_float`
- `pydash.predicates.is_decreasing`
- `pydash.predicates.is_increasing`
- `pydash.predicates.is_indexed`
- `pydash.predicates.is_instance_of`
- `pydash.predicates.is_integer`
- `pydash.predicates.is_json`
- `pydash.predicates.is_monotone`
- `pydash.predicates.is_negative`
- `pydash.predicates.is_odd`
- `pydash.predicates.is_positive`
- `pydash.predicates.is_strictly_decreasing`
- `pydash.predicates.is_strictly_increasing`
- `pydash.predicates.is_zero`
- `pydash.functions.iterated`
- `pydash.functions.juxtapose`
- `pydash.arrays.mapcat`
- `pydash.collections.reductions`
- `pydash.collections.reductions_right`
- `pydash.objects.rename_keys`
- `pydash.objects.set_path`
- `pydash.arrays.split_at`
- `pydash.objects.to_string`
- `pydash.objects.update_path`


Function Behavior
-----------------

Some of pydash's functions behave differently:

- :func:`pydash.utilities.memoize` uses all passed in arguments as the cache key by default instead of only using the first argument.


Templating
----------

- pydash doesn't have ``template()``. See :ref:`Templating <templating>` for more details.
