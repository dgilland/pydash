.. _upgrading:

Upgrading
*********

From v3.x.x to v4.0.0
=====================

Start by reading the full list of changes in ``v4.0.0`` at the :ref:`Changelog <changelog-v4.0.0>`. There are a significant amount of backwards-incompatibilities that will likely need to be addressed:

- All function aliases have been removed in favor of having a single named function for everything. This was done to make things less confusing by having only a single named function that performs an action vs. potentially using two different names for the same function.
- A few functions have been removed whose functionality was duplicated by another function.
- Some functions have been renamed for consistency and to align with Lodash.
- Many functions have had their callback argument moved to another function to align with Lodash.
- The generic ``callback`` argument has been renamed to either ``iteratee``, ``predicate``, or ``comparator``. This was done to make it clearer what the callback is doing and to align more with Lodash's naming conventions.

Once the shock of those backwards-incompatibilities has worn off, discover 72 new functions:

- 19 new array methods

    - :func:`pydash.arrays.difference_by`
    - :func:`pydash.arrays.difference_with`
    - :func:`pydash.arrays.from_pairs`
    - :func:`pydash.arrays.intersection_by`
    - :func:`pydash.arrays.intersection_with`
    - :func:`pydash.arrays.nth`
    - :func:`pydash.arrays.pull_all`
    - :func:`pydash.arrays.sorted_index_by`
    - :func:`pydash.arrays.sorted_index_of`
    - :func:`pydash.arrays.sorted_last_index_by`
    - :func:`pydash.arrays.sorted_last_index_of`
    - :func:`pydash.arrays.sorted_uniq`
    - :func:`pydash.arrays.union_by`
    - :func:`pydash.arrays.union_with`
    - :func:`pydash.arrays.uniq_by`
    - :func:`pydash.arrays.uniq_with`
    - :func:`pydash.arrays.xor_by`
    - :func:`pydash.arrays.xor_with`
    - :func:`pydash.arrays.zip_object_deep`

- 6 new collection methods

    - :func:`pydash.collections.flat_map`
    - :func:`pydash.collections.flat_map_deep`
    - :func:`pydash.collections.flat_depth`
    - :func:`pydash.collections.flatten_depth`
    - :func:`pydash.collections.invoke_map`
    - :func:`pydash.collections.sample_size`

- 2 new function methods

    - :func:`pydash.functions.flip`
    - :func:`pydash.functions.unary`

- 12 new object methods

    - :func:`pydash.objects.assign_with`
    - :func:`pydash.objects.clone_deep_with`
    - :func:`pydash.objects.clone_with`
    - :func:`pydash.objects.invert_by`
    - :func:`pydash.objects.merge_with`
    - :func:`pydash.objects.omit_by`
    - :func:`pydash.objects.pick_by`
    - :func:`pydash.objects.set_with`
    - :func:`pydash.objects.to_integer`
    - :func:`pydash.objects.unset`
    - :func:`pydash.objects.update`
    - :func:`pydash.objects.udpate_with`

- 8 new numerical methods

    - :func:`pydash.numerical.clamp`
    - :func:`pydash.numerical.divide`
    - :func:`pydash.numerical.max_by`
    - :func:`pydash.numerical.mean_by`
    - :func:`pydash.numerical.min_by`
    - :func:`pydash.numerical.multiply`
    - :func:`pydash.numerical.subtract`
    - :func:`pydash.numerical.sum_by`

- 4 new predicate methods

    - :func:`pydash.predicates.eq`
    - :func:`pydash.predicates.is_equal_with`
    - :func:`pydash.predicates.is_match_with`
    - :func:`pydash.predicates.is_set`

- 6 new string methods

    - :func:`pydash.strings.lower_case`
    - :func:`pydash.strings.lower_first`
    - :func:`pydash.strings.to_lower`
    - :func:`pydash.strings.to_upper`
    - :func:`pydash.strings.upper_case`
    - :func:`pydash.strings.upper_first`

- 15 new utility methods

    - :func:`pydash.utilities.cond`
    - :func:`pydash.utilities.conforms`
    - :func:`pydash.utilities.conforms_to`
    - :func:`pydash.utilities.default_to`
    - :func:`pydash.utilities.nth_arg`
    - :func:`pydash.utilities.over`
    - :func:`pydash.utilities.over_every`
    - :func:`pydash.utilities.over_some`
    - :func:`pydash.utilities.range_right`
    - :func:`pydash.utilities.stub_list`
    - :func:`pydash.utilities.stub_dict`
    - :func:`pydash.utilities.stub_false`
    - :func:`pydash.utilities.stub_string`
    - :func:`pydash.utilities.stub_true`
    - :func:`pydash.utilities.to_path`


From v2.x.x to v3.0.0
=====================

There were several breaking changes in ``v3.0.0``:

- Make ``to_string`` convert ``None`` to empty string. (**breaking change**)
- Make the following functions work with empty strings and ``None``: (**breaking change**)

  - ``camel_case``
  - ``capitalize``
  - ``chars``
  - ``chop``
  - ``chop_right``
  - ``class_case``
  - ``clean``
  - ``count_substr``
  - ``decapitalize``
  - ``ends_with``
  - ``join``
  - ``js_replace``
  - ``kebab_case``
  - ``lines``
  - ``quote``
  - ``re_replace``
  - ``replace``
  - ``series_phrase``
  - ``series_phrase_serial``
  - ``starts_with``
  - ``surround``

- Reorder function arguments for ``after`` from ``(n, func)`` to ``(func, n)``. (**breaking change**)
- Reorder function arguments for ``before`` from ``(n, func)`` to ``(func, n)``. (**breaking change**)
- Reorder function arguments for ``times`` from ``(n, callback)`` to ``(callback, n)``. (**breaking change**)
- Reorder function arguments for ``js_match`` from ``(reg_exp, text)`` to ``(text, reg_exp)``. (**breaking change**)
- Reorder function arguments for ``js_replace`` from ``(reg_exp, text, repl)`` to ``(text, reg_exp, repl)``. (**breaking change**)


And some potential breaking changes:

- Move ``arrays.join`` to ``strings.join`` (**possible breaking change**).
- Rename ``join``/``implode``'s second parameter from ``delimiter`` to ``separator``. (**possible breaking change**)
- Rename ``split``/``explode``'s second parameter from ``delimiter`` to ``separator``. (**possible breaking change**)


Some notable new features/functions:

- 31 new string methods

    - :func:`pydash.strings.chars`
    - :func:`pydash.strings.chop`
    - :func:`pydash.strings.chop_right`
    - :func:`pydash.strings.class_case`
    - :func:`pydash.strings.clean`
    - :func:`pydash.strings.count_substr`
    - :func:`pydash.strings.decapitalize`
    - :func:`pydash.strings.has_substr`
    - :func:`pydash.strings.human_case`
    - :func:`pydash.strings.insert_substr`
    - :func:`pydash.strings.lines`
    - :func:`pydash.strings.number_format`
    - :func:`pydash.strings.pascal_case`
    - :func:`pydash.strings.predecessor`
    - :func:`pydash.strings.prune`
    - :func:`pydash.strings.re_replace`
    - :func:`pydash.strings.replace`
    - :func:`pydash.strings.separator_case`
    - :func:`pydash.strings.series_phrase`
    - :func:`pydash.strings.series_phrase_serial`
    - :func:`pydash.strings.slugify`
    - :func:`pydash.strings.split`
    - :func:`pydash.strings.strip_tags`
    - :func:`pydash.strings.substr_left`
    - :func:`pydash.strings.substr_left_end`
    - :func:`pydash.strings.substr_right`
    - :func:`pydash.strings.substr_right_end`
    - :func:`pydash.strings.successor`
    - :func:`pydash.strings.swap_case`
    - :func:`pydash.strings.title_case`
    - :func:`pydash.strings.unquote`

- 1 new array method

    - :func:`pydash.arrays.duplicates`

- 2 new function methods

    - :func:`pydash.functions.ary`
    - :func:`pydash.functions.rearg`

- 1 new collection method:

    - :func:`pydash.collections.sort_by_all`

- 4 new object methods

    - :func:`pydash.objects.to_boolean`
    - :func:`pydash.objects.to_dict`
    - :func:`pydash.objects.to_number`
    - :func:`pydash.objects.to_plain_object`

- 4 new predicate methods

    - :func:`pydash.predicates.is_blank`
    - :func:`pydash.predicates.is_builtin` and alias :func:`pydash.predicates.is_native`
    - :func:`pydash.predicates.is_match`
    - :func:`pydash.predicates.is_tuple`

- 1 new utility method

    - :func:`pydash.utilities.prop_of` and alias :func:`pydash.utilities.property_of`

- 6 new aliases:

    - :func:`pydash.predicates.is_bool` for :func:`pydash.predicates.is_boolean`
    - :func:`pydash.predicates.is_dict` for :func:`pydash.predicates.is_plain_object`
    - :func:`pydash.predicates.is_int` for :func:`pydash.predicates.is_integer`
    - :func:`pydash.predicates.is_num` for :func:`pydash.predicates.is_number`
    - :func:`pydash.strings.truncate` for :func:`pydash.strings.trunc`
    - :func:`pydash.strings.underscore_case` for :func:`pydash.strings.snake_case`

- Chaining can now accept the root ``value`` argument late.
- Chains can be re-used with differnt initial values via ``chain().plant``.
- New chains can be created using the chain's computed value as the new chain's initial value via ``chain().commit``.
- Support iteration over class instance properties for non-list, non-dict, and non-iterable objects.


Late Value Chaining
-------------------

The passing of the root ``value`` argument for chaining can now be done "late" meaning that you can build chains without providing a value at the beginning. This allows you to build a chain and re-use it with different root values:

.. doctest::

    >>> from pydash import py_

    >>> square_sum = py_().power(2).sum()

    >>> [square_sum([1, 2, 3]), square_sum([4, 5, 6]), square_sum([7, 8, 9])]
    [14, 77, 194]


.. seealso::
    - For more details on method chaining, check out :ref:`Method Chaining <method-chaining>`.
    - For a full listing of changes in ``v3.0.0``, check out the :ref:`Changelog <changelog-v3.0.0>`.


From v1.x.x to v2.0.0
=====================

There were several breaking and potentially breaking changes in ``v2.0.0``:

- :func:`pydash.arrays.flatten` is now shallow by default. Previously, it was deep by default. For deep flattening, use either ``flatten(..., is_deep=True)`` or ``flatten_deep(...)``.
- :func:`pydash.predicates.is_number` now returns ``False`` for boolean ``True`` and ``False``. Previously, it returned ``True``.
- Internally, the files located in ``pydash.api`` were moved to ``pydash``. If you imported from ``pydash.api.<module>``, then it's recommended to change your imports to pull from ``pydash``.
- The function ``functions()`` was renamed to ``callables()`` to avoid ambiguities with the module ``functions.py``.


Some notable new features:

- Callback functions no longer require the full call signature definition.
- A new "_" instance was added which supports both method chaining and module method calling. See :ref:`api-dash-instance` for more details.


.. seealso::
    For a full listing of changes in ``v2.0.0``, check out the :ref:`Changelog <changelog-v2.0.0>`.
