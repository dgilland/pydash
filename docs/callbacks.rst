Callbacks
=========

.. testsetup::

    import pydash


For functions that support callbacks, there are several callback styles that can be used.


Callable Style
--------------

The most straight-forward callback is a regular callable object. For pydash functions that pass multiple arguments to their callback, the callable's argument signature does not need to support all arguments. Pydash's callback system will try to infer the number of supported arguments of the callable and only pass those arguments to the callback. However, there may be some edge cases where this will fail in which case one will need to wrap the callable in a ``lambda`` or ``def ...`` style function.

The arguments passed to most callbacks are:


.. code-block:: python

    callback(item, index, obj)


where ``item`` is an element of ``obj``, ``index`` is the ``dict`` or ``list`` index, and ``obj`` is the original object being passed in. But not all callbacks support these arguments. Some functions support fewer callback arguments. See :ref:`API Reference <api>` for more details.


.. doctest::

    >>> users = [
    ...     {'name': 'Michelangelo', 'active': False},
    ...     {'name': 'Donatello', 'active': False},
    ...     {'name': 'Leonardo', 'active': True}
    ... ]

    # Single argument callback.
    >>> callback = lambda item: item['name'] == 'Donatello'
    >>> pydash.find_index(users, callback)
    1

    # Two argument callback.
    >>> callback = lambda item, index: index == 3
    >>> pydash.find_index(users, callback)
    -1

    # Three argument callback.
    >>> callback = lambda item, index, obj: obj[index]['active']
    >>> pydash.find_index(users, callback)
    2


Shallow Property Style
----------------------

The shallow property style callback is specified as a one item ``list`` containing the property value to return from an element. Internally, :func:`pydash.utilities.prop` is used to create the callback.


.. doctest::

    >>> users = [
    ...     {'name': 'Michelangelo', 'active': False},
    ...     {'name': 'Donatello', 'active': False},
    ...     {'name': 'Leonardo', 'active': True}
    ... ]
    >>> pydash.find_index(users, ['active'])
    2


Deep Property Style
-------------------

The deep property style callback is specified as a deep property ``string`` of the nested object value to return from an element. Internally, :func:`pydash.utilities.deep_prop` is used to create the callback. See :ref:`Deep Path Strings <deeppath>` for more details.


.. doctest::

    >>> users = [
    ...     {'name': 'Michelangelo', 'location': {'city': 'Rome'}},
    ...     {'name': 'Donatello', 'location': {'city': 'Florence'}},
    ...     {'name': 'Leonardo', 'location': {'city': 'Amboise'}}
    ... ]
    >>> pydash.map_(users, 'location.city')
    ['Rome', 'Florence', 'Amboise']


Matches Property Style
----------------------

The matches property style callback is specified as a two item ``list`` containing a property key and value and returns ``True`` when an element's key is equal to value, else ``False``. Internally, :func:`pydash.utilities.matches_property` is used to create the callback.


.. doctest::

    >>> users = [
    ...     {'name': 'Michelangelo', 'active': False},
    ...     {'name': 'Donatello', 'active': False},
    ...     {'name': 'Leonardo', 'active': True}
    ... ]
    >>> pydash.find_index(users, ['active', False])
    0
    >>> pydash.find_last_index(users, ['active', False])
    1


Matches Style
-------------

The matches style callback is specified as a ``dict`` object and returns ``True`` when an element matches the properties of the object, else ``False``. Internally, :func:`pydash.utilities.matches` is used to create the callback.


.. doctest::

    >>> users = [
    ...     {'name': 'Michelangelo', 'location': {'city': 'Rome'}},
    ...     {'name': 'Donatello', 'location': {'city': 'Florence'}},
    ...     {'name': 'Leonardo', 'location': {'city': 'Amboise'}}
    ... ]
    >>> pydash.map_(users, {'location': {'city': 'Florence'}})
    [False, True, False]
