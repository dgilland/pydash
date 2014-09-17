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
- :func:`pydash.predicates.is_re` >> :func:`pydash.predicates.is_reg_exp`
- :func:`pydash.strings.escape_re` >> :func:`pydash.strings.escape_reg_exp`


Extra Functions
---------------

The following functions exist in pydash but not in Lo-Dash:

- :func:`pydash.numerical.add`, :func:`pydash.numerical.sum_`
- :func:`pydash.numerical.average`, :func:`pydash.numerical.avg`, :func:`pydash.numerical.mean`
- :func:`pydash.arrays.cat`
- :func:`pydash.functions.conjoin`
- :func:`pydash.functions.disjoin`
- :func:`pydash.strings.explode`
- :func:`pydash.objects.get_path`
- :func:`pydash.objects.has_path`
- :func:`pydash.strings.implode`
- :func:`pydash.arrays.intercalate`
- :func:`pydash.arrays.interleave`
- :func:`pydash.arrays.intersperse`
- :func:`pydash.predicates.is_associative`
- :func:`pydash.predicates.is_even`
- :func:`pydash.predicates.is_float`
- :func:`pydash.predicates.is_decreasing`
- :func:`pydash.predicates.is_increasing`
- :func:`pydash.predicates.is_indexed`
- :func:`pydash.predicates.is_instance_of`
- :func:`pydash.predicates.is_integer`
- :func:`pydash.predicates.is_json`
- :func:`pydash.predicates.is_monotone`
- :func:`pydash.predicates.is_negative`
- :func:`pydash.predicates.is_odd`
- :func:`pydash.predicates.is_positive`
- :func:`pydash.predicates.is_strictly_decreasing`
- :func:`pydash.predicates.is_strictly_increasing`
- :func:`pydash.predicates.is_zero`
- :func:`pydash.functions.iterated`
- :func:`pydash.functions.juxtapose`
- :func:`pydash.arrays.mapcat`
- :func:`pydash.collections.mapiter`
- :func:`pydash.numerical.median`
- :func:`pydash.numerical.moving_average`, :func:`pydash.numerical.moving_avg`
- :func:`pydash.numerical.power`, :func:`pydash.numerical.pow_`
- :func:`pydash.collections.reductions`
- :func:`pydash.collections.reductions_right`
- :func:`pydash.objects.rename_keys`
- :func:`pydash.numerical.round_`, :func:`pydash.numerical.curve`
- :func:`pydash.numerical.scale`
- :func:`pydash.objects.set_path`
- :func:`pydash.numerical.slope`
- :func:`pydash.numerical.std_deviation`, :func:`pydash.numerical.sigma`
- :func:`pydash.arrays.split_at`
- :func:`pydash.objects.to_string`
- :func:`pydash.numerical.transpose`
- :func:`pydash.objects.update_path`
- :func:`pydash.numerical.variance`
- :func:`pydash.numerical.zscore`


Function Behavior
-----------------

Some of pydash's functions behave differently:

- :func:`pydash.utilities.memoize` uses all passed in arguments as the cache key by default instead of only using the first argument.


Templating
----------

- pydash doesn't have ``template()``. See :ref:`Templating <templating>` for more details.
