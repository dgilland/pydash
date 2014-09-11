.. _upgrading:

Upgrading
*********


From v1.0.0 to v2.0.0
=====================

There were several breaking and potentially breaking changes in ``v2.0.0``:

- :func:`pydash.arrays.flatten` is now shallow by default. Previously, it was deep by default. For deep flattening, use either ``flatten(..., is_deep=True)`` or ``flatten_deep(...)``.
- :func:`pydash.predicates.is_number` now returns ``False`` for boolean ``True`` and ``False``. Previously, it returned ``True``.
- Internally, the files located in ``pydash.api`` were moved to ``pydash``. If you imported from ``pydash.api.<module>``, then it's recommended to change your imports to pull from ``pydash``.
- The function ``functions()`` was renamed to ``callables()`` to avoid ambiguities with the module ``functions.py``.


Some notable new features:

- Callback functions no longer require the full call signature definition. See :ref:`differences-callbacks` for more details.
- A new "_" instance was added which supports both method chaining and module method calling. See :ref:`api-dash-instance` for more details.
