.. _changelog:

Changelog
=========


v3.4.5 (2016-10-16)
-------------------

- Add optional ``default`` parameter to ``min_`` and ``max_`` functions that is used when provided iterable is empty.
- Fix bug in ``is_match`` where comparison between an empty ``source`` argument returned ``None`` instead of ``True``.


v3.4.4 (2016-09-06)
-------------------

- Shallow copy each source in ``assign``/``extend`` instead of deep copying.
- Call ``copy.deepcopy`` in ``merge`` instead of the more resource intensive ``clone_deep``.


v3.4.3 (2016-04-07)
-------------------

- Fix minor issue in deep path string parsing so that list indexing in paths can be specified as ``foo[0][1].bar`` instead of ``foo.[0].[1].bar``. Both formats are now supported.


v3.4.2 (2016-03-24)
-------------------

- Fix bug in ``start_case`` where capitalized characters after the first character of a word where mistakenly cast to lower case.


v3.4.1 (2015-11-03)
-------------------

- Fix Python 3.5, inspect, and  pytest compatibility issue with ``py_`` chaining object when doctest run on ``pydash.__init__.py``.


v3.4.0 (2015-09-22)
-------------------

- Optimize callback system for performance.

  - Explicitly store arg count on callback for ``pydash`` generated callbacks where the arg count is known. This avoids the costly ``inspect.getargspec`` call.
  - Eliminate usage of costly ``guess_builtin_argcount`` which parsed docstrings, and instead only ever pass a single argument to a builtin callback function.

- Optimize ``get``/``set`` so that regex parsing is only done when special characters are contained in the path key whereas before, all string paths were parsed.
- Optimize ``is_builtin`` by checking for ``BuiltinFunctionType`` instance and then using ``dict`` look up table instead of a ``list`` look up.
- Optimize ``is_match`` by replacing call to ``has`` with a ``try/except`` block.
- Optimize ``push``/``append`` by using a native loop instead of callback mapping.


v3.3.0 (2015-07-23)
-------------------

- Add ``ceil``.
- Add ``defaults_deep``.
- Add ``floor``.
- Add ``get``.
- Add ``gt``.
- Add ``gte``.
- Add ``is_iterable``.
- Add ``lt``.
- Add ``lte``.
- Add ``map_keys``.
- Add ``method``.
- Add ``method_of``.
- Add ``mod_args``.
- Add ``set_``.
- Add ``unzip_with``.
- Add ``zip_with``.
- Make ``add`` support adding two numbers if passed in positionally.
- Make ``get`` main definition and ``get_path`` its alias.
- Make ``set_`` main definition and ``deep_set`` its alias.


v3.2.2 (2015-04-29)
-------------------

- Catch ``AttributeError`` in ``helpers.get_item`` and return default value if set.


v3.2.1 (2015-04-29)
-------------------

- Fix bug in ``reduce_right`` where collection was not reversed correctly.


v3.2.0 (2015-03-03)
-------------------

- Add ``sort_by_order`` as alias of ``sort_by_all``.
- Fix ``is_match`` to not compare ``obj`` and ``source`` types using ``type`` and instead use ``isinstance`` comparisons exclusively.
- Make ``sort_by_all`` accept an ``orders`` argument for specifying the sort order of each key via boolean ``True`` (for ascending) and ``False`` (for descending).
- Make ``words`` accept a ``pattern`` argument to override the default regex used for splitting words.
- Make ``words`` handle single character words better.


v3.1.0 (2015-02-28)
-------------------

- Add ``fill``.
- Add ``in_range``.
- Add ``matches_property``.
- Add ``spread``.
- Add ``start_case``.
- Make callbacks support ``matches_property`` style as ``[key, value]`` or ``(key, value)``.
- Make callbacks support shallow ``property`` style callbacks as ``[key]`` or ``(key,)``.


.. _changelog-v3.0.0:

v3.0.0 (2015-02-25)
-------------------

- Add ``ary``.
- Add ``chars``.
- Add ``chop``.
- Add ``chop_right``.
- Add ``clean``.
- Add ``commit`` method to ``chain`` that returns a new chain with the computed ``chain.value()`` as the initial value of the chain.
- Add ``count_substr``.
- Add ``decapitalize``.
- Add ``duplicates``.
- Add ``has_substr``.
- Add ``human_case``.
- Add ``insert_substr``.
- Add ``is_blank``.
- Add ``is_bool`` as alias of ``is_boolean``.
- Add ``is_builtin``, ``is_native``.
- Add ``is_dict`` as alias of ``is_plain_object``.
- Add ``is_int`` as alias of ``is_integer``.
- Add ``is_match``.
- Add ``is_num`` as alias of ``is_number``.
- Add ``is_tuple``.
- Add ``join`` as alias of ``implode``.
- Add ``lines``.
- Add ``number_format``.
- Add ``pascal_case``.
- Add ``plant`` method to ``chain`` that returns a cloned chain with a new initial value.
- Add ``predecessor``.
- Add ``property_of``, ``prop_of``.
- Add ``prune``.
- Add ``re_replace``.
- Add ``rearg``.
- Add ``replace``.
- Add ``run`` as alias of ``chain.value``.
- Add ``separator_case``.
- Add ``series_phrase``.
- Add ``series_phrase_serial``.
- Add ``slugify``.
- Add ``sort_by_all``.
- Add ``strip_tags``.
- Add ``substr_left``.
- Add ``substr_left_end``.
- Add ``substr_right``.
- Add ``substr_right_end``.
- Add ``successor``.
- Add ``swap_case``.
- Add ``title_case``.
- Add ``truncate`` as alias of ``trunc``.
- Add ``to_boolean``.
- Add ``to_dict``, ``to_plain_object``.
- Add ``to_number``.
- Add ``underscore_case`` as alias of ``snake_case``.
- Add ``unquote``.
- Fix ``deep_has`` to return ``False`` when ``ValueError`` raised during path checking.
- Fix ``pad`` so that it doesn't over pad beyond provided length.
- Fix ``trunc``/``truncate`` so that they handle texts shorter than the max string length correctly.
- Make the following functions work with empty strings and ``None``: (**breaking change**) Thanks k7sleeper_!

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

- Make callback invocation have better support for builtin functions and methods. Previously, if one wanted to pass a builtin function or method as a callback, it had to be wrapped in a lambda which limited the number of arguments that would be passed it. For example, ``_.each([1, 2, 3], array.append)`` would fail and would need to be converted to ``_.each([1, 2, 3], lambda item: array.append(item)``. That is no longer the case as the non-wrapped method is now supported.
- Make ``capitalize`` accept ``strict`` argument to control whether to convert the rest of the string to lower case or not. Defaults to ``True``.
- Make ``chain`` support late passing of initial ``value`` argument.
- Make ``chain`` not store computed ``value()``. (**breaking change**)
- Make ``drop``, ``drop_right``, ``take``, and ``take_right`` have default ``n=1``.
- Make ``is_indexed`` return ``True`` for tuples.
- Make ``partial`` and ``partial_right`` accept keyword arguments.
- Make ``pluck`` style callbacks support deep paths. (**breaking change**)
- Make ``re_replace`` accept non-string arguments.
- Make ``sort_by`` accept ``reverse`` parameter.
- Make ``splice`` work with strings.
- Make ``to_string`` convert ``None`` to empty string. (**breaking change**)
- Move ``arrays.join`` to ``strings.join``. (**breaking change**)
- Rename ``join``/``implode``'s second parameter from ``delimiter`` to ``separator``. (**breaking change**)
- Rename ``split``/``explode``'s second parameter from ``delimiter`` to ``separator``. (**breaking change**)
- Reorder function arguments for ``after`` from ``(n, func)`` to ``(func, n)``. (**breaking change**)
- Reorder function arguments for ``before`` from ``(n, func)`` to ``(func, n)``. (**breaking change**)
- Reorder function arguments for ``times`` from ``(n, callback)`` to ``(callback, n)``. (**breaking change**)
- Reorder function arguments for ``js_match`` from ``(reg_exp, text)`` to ``(text, reg_exp)``. (**breaking change**)
- Reorder function arguments for ``js_replace`` from ``(reg_exp, text, repl)`` to ``(text, reg_exp, repl)``. (**breaking change**)
- Support iteration over class instance properties for non-list, non-dict, and non-iterable objects.


v2.4.2 (2015-02-03)
-------------------

- Fix ``remove`` so that array is modified after callback iteration.


v2.4.1 (2015-01-11)
-------------------

- Fix ``kebab_case`` so that it casts string to lower case.


v2.4.0 (2015-01-07)
-------------------

- Add ``ensure_ends_with``. Thanks k7sleeper_!
- Add ``ensure_starts_with``. Thanks k7sleeper_!
- Add ``quote``. Thanks k7sleeper_!
- Add ``surround``. Thanks k7sleeper_!


v2.3.2 (2014-12-10)
-------------------

- Fix ``merge`` and ``assign``/``extend`` so they apply ``clone_deep`` to source values before assigning to destination object.
- Make ``merge`` accept a callback as a positional argument if it is last.


v2.3.1 (2014-12-07)
-------------------

- Add ``pipe`` and ``pipe_right`` as aliases of ``flow`` and ``flow_right``.
- Fix ``merge`` so that trailing ``{}`` or ``[]`` don't overwrite previous source values.
- Make ``py_`` an alias for ``_``.


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


.. _changelog-v2.0.0:

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
- Move files in ``pydash/api/`` to ``pydash/``. (**breaking change**)
- Move predicate functions from ``pydash.api.objects`` to ``pydash.api.predicates``. (**breaking change**)
- Rename ``create_callback`` to ``iteratee``. (**breaking change**)
- Rename ``functions`` to ``callables`` in order to allow ``functions.py`` to exist at the root of the pydash module folder. (**breaking change**)
- Rename *private* utility function ``_iter_callback`` to ``itercallback``. (**breaking change**)
- Rename *private* utility function ``_iter_list_callback`` to ``iterlist_callback``. (**breaking change**)
- Rename *private* utility function ``_iter_dict_callback`` to ``iterdict_callback``. (**breaking change**)
- Rename *private* utility function ``_iterate`` to ``iterator``. (**breaking change**)
- Rename *private* utility function ``_iter_dict`` to ``iterdict``. (**breaking change**)
- Rename *private* utility function ``_iter_list`` to ``iterlist``. (**breaking change**)
- Rename *private* utility function ``_iter_unique`` to ``iterunique``. (**breaking change**)
- Rename *private* utility function ``_get_item`` to ``getitem``. (**breaking change**)
- Rename *private* utility function ``_set_item`` to ``setitem``. (**breaking change**)
- Rename *private* utility function ``_deprecated`` to ``deprecated``. (**breaking change**)
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
- Move ``escape`` and ``unescape`` from ``pydash.api.utilities`` to ``pydash.api.strings``. (**breaking change**)
- Move ``range_`` from ``pydash.api.arrays`` to ``pydash.api.utilities``. (**breaking change**)


.. _changelog-v1.0.0:

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


.. _changelog-v0.0.0:

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
.. _k7sleeper: https://github.com/k7sleeper
