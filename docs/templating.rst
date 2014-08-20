.. _templating:

Templating
==========

Currenly, pydash doesn't support templating. Having a custom templating engine was never a goal of pydash even though Lo-Dash includes one. There already exist many mature and battle-tested templating engines like `Jinja2`_ and `Mako`_ which would be much more suited to handling templating needs. However, how best to implement templating in pydash remains an open issue.

Here are a few options to consider:

1. Provide a thin wrapper around `String Format`_ and facilitate HTML escaping but provide nothing beyond that; no code execution, no interpolate delimiters, no imports.
2. Provide a thin wrapper around one of the templating libraries (i.e. choose one and make it a dependency) and defer everything to it.
3. Provide an interface to a templating library so that you get ``pydash.template()`` but you set the engine yourself.
4. All of the above.
5. Leave templating out of pydash.

No decision has been made yet, but one will likely be made by ``v1.2.0`` or ``v1.3.0``.


.. _Jinja2: http://jinja.pocoo.org/
.. _Mako: http://www.makotemplates.org/
.. _String Format: https://docs.python.org/2/library/string.html#formatstrings
