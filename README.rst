pydash
******

.. image:: http://img.shields.io/pypi/v/pydash.svg?style=flat
    :target: https://pypi.python.org/pypi/pydash/

.. image:: http://img.shields.io/travis/dgilland/pydash/master.svg?style=flat
    :target: https://travis-ci.org/dgilland/pydash

.. image:: http://img.shields.io/coveralls/dgilland/pydash/master.svg?style=flat
    :target: https://coveralls.io/r/dgilland/pydash

.. image:: http://img.shields.io/pypi/l/pydash.svg?style=flat
    :target: https://pypi.python.org/pypi/pydash/

Python port of the `Lo-Dash <http://Lo-Dash.com/>`_  Javascript library.

Currently, alpha stage.

Current status of initial port: https://github.com/dgilland/pydash/issues/2


Requirements
============

Compatibility
=============

- Python 2.6
- Python 2.7
- Python 3.2
- Python 3.3
- Python 3.4

Dependencies
------------

None.


Installation
============

::

    pip install pydash


Overview
========

Differences between Lo-Dash
---------------------------

- Function names use ``snake_case`` instead of ``camelCase``.
- Any Lo-Dash function which shares its name with a reserved Python keyword will have an ``_`` appended after it (e.g. ``filter`` in Lo-Dash would be ``filter_`` in pydash.
- Extra callback args must be explictly handled. In Javascript, it's perfectly fine to pass in extra arguments to a function that aren't explictly accepted by that function (e.g. ``function foo(a1){}; foo(1, 2, 3);``). In Python, those extra arguments must be explictly handled (e.g. ``def foo(a1, *args): ...; foo(1, 2, 3)``). Therefore, callbacks passed to ``pydash`` functions must use named args or a catch-all like ``*args`` since each callback is passed ``item``, ``index``, and ``array``.
- Lo-Dash's ``toArray`` is pydash's ``to_list``.
- In addition to ``property_``, pydash has ``prop`` as an alias.
- pydash's ``memoize`` uses all passed in arguments as the cache key by default instead of only using the first argument like Lo-Dash does.


License
=======

This software is licensed under the MIT License.
