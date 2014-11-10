Changelog
=========


v2.3.0 (2014-11-10)
-------------------

- Support ``type`` callbacks (e.g. ``int``, ``float``, ``str``, etc.) by only passing a single callback argument when invoking the callback.
- Drop official support for Python 3.2. Too many testing dependencies no longer work on it.


v2.2.0 (2014-10-28)
-------------------

- Add ``append``.
- Add ``deep_get``.
- Add ``deep_has``.
- Add ``deep_map_values``.
- Add ``deep_set``.
- Add ``deep_pluck``.
- Add ``deep_property``.
- Add ``join``.
- Add ``pop``.
- Add ``push``.
- Add ``reverse``.
- Add ``shift``.
- Add ``sort``.
- Add ``splice``.
- Add ``unshift``.
- Add ``url``.
- Fix bug in ``snake_case`` that resulted in returned string not being converted to lower case.
- Fix bug in chaining method access test which skipped the actual test.
- Make ``_`` instance alias method access to methods with a trailing underscore in their name. For example, ``_.map()`` becomes an alias for ``map_()``.
- Make ``deep_prop`` an alias of ``deep_property``.
- Make ``has`` work with deep paths.
- Make ``has_path`` an alias of ``deep_has``.
- Make ``get_path`` handle escaping the ``.`` delimiter for string keys.
- Make ``get_path`` handle list indexing using strings such as ``'0.1.2'`` to access ``'value'`` in ``[[0, [0, 0, 'value']]]``.
- Make ``concat`` an alias of ``cat``.


v2.1.0 (2014-09-17)
-------------------

- Add ``add``, ``sum_``.
- Add ``average``, ``avg``, ``mean``.
- Add ``mapiter``.
- Add ``median``.
- Add ``moving_average``, ``moving_avg``.
- Add ``power``, ``pow_``.
- Add ``round_``, ``curve``.
- Add ``scale``.
- Add ``slope``.
- Add ``std_deviation``, ``sigma``.
- Add ``transpose``.
- Add ``variance``.
- Add ``zscore``.


v2.0.0 (2014-09-11)
-------------------

- Add ``_`` instance that supports both method chaining and module method calling.
- Add ``cat``.
- Add ``conjoin``.
- Add ``deburr``.
- Add ``disjoin``.
- Add ``explode``.
- Add ``flatten_deep``.
- Add ``flow``.
- Add ``flow_right``.
- Add ``get_path``.
- Add ``has_path``.
- Add ``implode``.
- Add ``intercalate``.
- Add ``interleave``.
- Add ``intersperse``.
- Add ``is_associative``.
- Add ``is_even``.
- Add ``is_float``.
- Add ``is_decreasing``.
- Add ``is_increasing``.
- Add ``is_indexed``.
- Add ``is_instance_of``.
- Add ``is_integer``.
- Add ``is_json``.
- Add ``is_monotone``.
- Add ``is_negative``.
- Add ``is_odd``.
- Add ``is_positive``.
- Add ``is_strictly_decreasing``.
- Add ``is_strictly_increasing``.
- Add ``is_zero``.
- Add ``iterated``.
- Add ``js_match``.
- Add ``js_replace``.
- Add ``juxtapose``.
- Add ``mapcat``.
- Add ``reductions``.
- Add ``reductions_right``.
- Add ``rename_keys``.
- Add ``set_path``.
- Add ``split_at``.
- Add ``thru``.
- Add ``to_string``.
- Add ``update_path``.
- Add ``words``.
- Make callback function calling adapt to argspec of given callback function. If, for example, the full callback signature is ``(item, index, obj)`` but the passed in callback only supports ``(item)``, then only ``item`` will be passed in when callback is invoked. Previously, callbacks had to support all arguments or implement star-args.
- Make ``chain`` lazy and only compute the final value when ``value`` called.
- Make ``compose`` an alias of ``flow_right``.
- Make ``flatten`` shallow by default, remove callback option, and add ``is_deep`` option. (**breaking change**)
- Make ``is_number`` return ``False`` for boolean ``True`` and ``False``. (**breaking change**)
- Make ``invert`` accept ``multivalue`` argument.
- Make ``result`` accept ``default`` argument.
- Make ``slice_`` accept optional ``start`` and ``end`` arguments.
- Move files in ``pydash/api/`` to ``pydash/``. (**possible breaking change**)
- Move predicate functions from ``pydash.api.objects`` to ``pydash.api.predicates``. (**possible breaking change**)
- Rename ``create_callback`` to ``iteratee``. (**breaking change**)
- Rename ``functions`` to ``callables`` in order to allow ``functions.py`` to exist at the root of the pydash module folder. (**breaking change**)
- Rename *private* utility function ``_iter_callback`` to ``itercallback``. (**possible breaking change**)
- Rename *private* utility function ``_iter_list_callback`` to ``iterlist_callback``. (**possible breaking change**)
- Rename *private* utility function ``_iter_dict_callback`` to ``iterdict_callback``. (**possible breaking change**)
- Rename *private* utility function ``_iterate`` to ``iterator``. (**possible breaking change**)
- Rename *private* utility function ``_iter_dict`` to ``iterdict``. (**possible breaking change**)
- Rename *private* utility function ``_iter_list`` to ``iterlist``. (**possible breaking change**)
- Rename *private* utility function ``_iter_unique`` to ``iterunique``. (**possible breaking change**)
- Rename *private* utility function ``_get_item`` to ``getitem``. (**possible breaking change**)
- Rename *private* utility function ``_set_item`` to ``setitem``. (**possible breaking change**)
- Rename *private* utility function ``_deprecated`` to ``deprecated``. (**possible breaking change**)
- Undeprecate ``tail`` and make alias of ``rest``.


v1.1.0 (2014-08-19)
-------------------

- Add ``attempt``.
- Add ``before``.
- Add ``camel_case``.
- Add ``capitalize``.
- Add ``chunk``.
- Add ``curry_right``.
- Add ``drop_right``.
- Add ``drop_right_while``.
- Add ``drop_while``.
- Add ``ends_with``.
- Add ``escape_reg_exp`` and ``escape_re``.
- Add ``is_error``.
- Add ``is_reg_exp`` and ``is_re``.
- Add ``kebab_case``.
- Add ``keys_in`` as alias of ``keys``.
- Add ``negate``.
- Add ``pad``.
- Add ``pad_left``.
- Add ``pad_right``.
- Add ``partition``.
- Add ``pull_at``.
- Add ``repeat``.
- Add ``slice_``.
- Add ``snake_case``.
- Add ``sorted_last_index``.
- Add ``starts_with``.
- Add ``take_right``.
- Add ``take_right_while``.
- Add ``take_while``.
- Add ``trim``.
- Add ``trim_left``.
- Add ``trim_right``.
- Add ``trunc``.
- Add ``values_in`` as alias of ``values``.
- Create ``pydash.api.strings`` module.
- Deprecate ``tail``.
- Modify ``drop`` to accept ``n`` argument and remove as alias of ``rest``.
- Modify ``take`` to accept ``n`` argument and remove as alias of ``first``.
- Move ``escape`` and ``unescape`` from ``pydash.api.utilities`` to ``pydash.api.strings``. (**possible breaking change**)
- Move ``range_`` from ``pydash.api.arrays`` to ``pydash.api.utilities``. (**possible breaking change**)


v1.0.0 (2014-08-05)
-------------------

- Add Python 2.6 and Python 3 support.
- Add ``after``.
- Add ``assign`` and ``extend``. Thanks nathancahill_!
- Add ``callback`` and ``create_callback``.
- Add ``chain``.
- Add ``clone``.
- Add ``clone_deep``.
- Add ``compose``.
- Add ``constant``.
- Add ``count_by``. Thanks nathancahill_!
- Add ``curry``.
- Add ``debounce``.
- Add ``defaults``. Thanks nathancahill_!
- Add ``delay``.
- Add ``escape``.
- Add ``find_key``. Thanks nathancahill_!
- Add ``find_last``. Thanks nathancahill_!
- Add ``find_last_index``. Thanks nathancahill_!
- Add ``find_last_key``. Thanks nathancahill_!
- Add ``for_each``. Thanks nathancahill_!
- Add ``for_each_right``. Thanks nathancahill_!
- Add ``for_in``. Thanks nathancahill_!
- Add ``for_in_right``. Thanks nathancahill_!
- Add ``for_own``. Thanks nathancahill_!
- Add ``for_own_right``. Thanks nathancahill_!
- Add ``functions_`` and ``methods``. Thanks nathancahill_!
- Add ``group_by``. Thanks nathancahill_!
- Add ``has``. Thanks nathancahill_!
- Add ``index_by``. Thanks nathancahill_!
- Add ``identity``.
- Add ``inject``.
- Add ``invert``.
- Add ``invoke``. Thanks nathancahill_!
- Add ``is_list``. Thanks nathancahill_!
- Add ``is_boolean``. Thanks nathancahill_!
- Add ``is_empty``. Thanks nathancahill_!
- Add ``is_equal``.
- Add ``is_function``. Thanks nathancahill_!
- Add ``is_none``. Thanks nathancahill_!
- Add ``is_number``. Thanks nathancahill_!
- Add ``is_object``.
- Add ``is_plain_object``.
- Add ``is_string``. Thanks nathancahill_!
- Add ``keys``.
- Add ``map_values``.
- Add ``matches``.
- Add ``max_``. Thanks nathancahill_!
- Add ``memoize``.
- Add ``merge``.
- Add ``min_``. Thanks nathancahill_!
- Add ``noop``.
- Add ``now``.
- Add ``omit``.
- Add ``once``.
- Add ``pairs``.
- Add ``parse_int``.
- Add ``partial``.
- Add ``partial_right``.
- Add ``pick``.
- Add ``property_`` and ``prop``.
- Add ``pull``. Thanks nathancahill_!
- Add ``random``.
- Add ``reduce_`` and ``foldl``.
- Add ``reduce_right`` and ``foldr``.
- Add ``reject``. Thanks nathancahill_!
- Add ``remove``.
- Add ``result``.
- Add ``sample``.
- Add ``shuffle``.
- Add ``size``.
- Add ``sort_by``. Thanks nathancahill_!
- Add ``tap``.
- Add ``throttle``.
- Add ``times``.
- Add ``transform``.
- Add ``to_list``. Thanks nathancahill_!
- Add ``unescape``.
- Add ``unique_id``.
- Add ``values``.
- Add ``wrap``.
- Add ``xor``.


v0.0.0 (2014-07-22)
-------------------

- Add ``all_``.
- Add ``any_``.
- Add ``at``.
- Add ``bisect_left``.
- Add ``collect``.
- Add ``collections``.
- Add ``compact``.
- Add ``contains``.
- Add ``detect``.
- Add ``difference``.
- Add ``drop``.
- Add ``each``.
- Add ``each_right``.
- Add ``every``.
- Add ``filter_``.
- Add ``find``.
- Add ``find_index``.
- Add ``find_where``.
- Add ``first``.
- Add ``flatten``.
- Add ``head``.
- Add ``include``.
- Add ``index_of``.
- Add ``initial``.
- Add ``intersection``.
- Add ``last``.
- Add ``last_index_of``.
- Add ``map_``.
- Add ``object_``.
- Add ``pluck``.
- Add ``range_``.
- Add ``rest``.
- Add ``select``.
- Add ``some``.
- Add ``sorted_index``.
- Add ``tail``.
- Add ``take``.
- Add ``union``.
- Add ``uniq``.
- Add ``unique``.
- Add ``unzip``.
- Add ``where``.
- Add ``without``.
- Add ``zip_``.
- Add ``zip_object``.


.. _nathancahill: https://github.com/nathancahill
