Lo-Dash Differences
===================

- Function names use ``snake_case`` instead of ``camelCase``.
- Any Lo-Dash function that shares its name with a reserved Python keyword will have an ``_`` appended after it (e.g. ``filter`` in Lo-Dash would be ``filter_`` in pydash.
- Extra callback args must be explictly handled. In Javascript, it's perfectly fine to pass in extra arguments to a function that aren't explictly accepted by that function (e.g. ``function foo(a1){}; foo(1, 2, 3);``). In Python, those extra arguments must be explictly handled (e.g. ``def foo(a1, *args): ...; foo(1, 2, 3)``). Therefore, callbacks passed to ``pydash`` functions must use named args or a catch-all like ``*args`` since each callbacks will be passed arguments like ``(value, index|key, array)``. **NOTE:** *Future versions of pydash may attempt to infer the number of arguments a callback can handle and only pass what's supported.*
- Lo-Dash's ``toArray`` is pydash's ``to_list``.
- In addition to ``property_``, pydash has ``prop`` as an alias.
- In addition to ``escape_reg_exp`` and ``is_reg_exp``, pydash has ``escape_re`` and ``is_re`` as aliases.
- pydash's ``memoize`` uses all passed in arguments as the cache key by default instead of only using the first argument like Lo-Dash does.
- pydash doesn't have ``template``. See :ref:`Templating <templating>` for more details.
