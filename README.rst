pydash
======

Python port of the `Lodash <http://lodash.com/>`_ Javascript library.

Currently, work in progress.

Differences between Lodash
--------------------------

- Function names use ``snake_case`` instead of ``camelCase``.
- Extra callback args must be explictly handled. In Javascript, it's perfectly fine to pass in extra arguments to a function that aren't explictly accepted by that function (e.g. ``function foo(a1){}; foo(1, 2, 3);``). In Python, those extra arguments must be explictly handled (e.g. ``def foo(a1, *args): ...; foo(1, 2, 3)``). Therefore, callbacks passed to ``pydash`` functions must use named args or a catch-all like *args since each callback is passed ``item``, ``index``, and ``array``.
- The function ``_.object`` is renamed to ``_.obj`` since ``object`` is a Python reserved keyword.
- The function ``_.zip`` is renamed to ``_.zipper`` since ``zip`` is a Python reserved keyword.

License
-------

This software is licensed under the MIT License.
