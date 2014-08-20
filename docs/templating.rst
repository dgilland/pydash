.. _templating:

Templating
==========

Author here. Currenly, pydash doesn't support templating; this has been intentional. There already exist many mature and battle-tested templating engines like `Jinja2`_ and `Mako`_. I never wanted to roll my own, but I was also reluctant to include this or that engine as a dependency. I have toyed with a few templating ideas, though:

1. Provide a thin wrapper around `String Format`_ and facilitate HTML escaping but provide nothing beyond that; no code execution, no interpolate delimiters, no imports.
2. Provide a thin wrapper around one of the templating libraries (i.e. choose one and make it a dependency) and defer everything to it.
3. Provide an interface to a templating library so that you get ``pydash.template()`` but you set the engine yourself.
4. All of the above.
5. Leave templating out of pydash.

I'm still on the fence about committing to any of the above options so this is still an open question. Most likely I will make a decision by ``v1.2.0`` or ``v1.3.0``.


.. _Jinja2: http://jinja.pocoo.org/
.. _Mako: http://www.makotemplates.org/
.. _String Format: https://docs.python.org/2/library/string.html#formatstrings
