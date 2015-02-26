.. _upgrading:

Upgrading
*********


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

- Callback functions no longer require the full call signature definition. See :ref:`differences-callbacks` for more details.
- A new "_" instance was added which supports both method chaining and module method calling. See :ref:`api-dash-instance` for more details.


.. seealso::
    For a full listing of changes in ``v2.0.0``, check out the :ref:`Changelog <changelog-v2.0.0>`.
