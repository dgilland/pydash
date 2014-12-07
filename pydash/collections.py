"""Functions that operate on lists and dicts.

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import

import random

import pydash as pyd

from .helpers import itercallback, iterator, call_callback, NoValue


__all__ = [
    'all_',
    'any_',
    'at',
    'collect',
    'contains',
    'count_by',
    'deep_pluck',
    'detect',
    'each',
    'each_right',
    'every',
    'filter_',
    'find',
    'find_last',
    'find_where',
    'foldl',
    'foldr',
    'for_each',
    'for_each_right',
    'group_by',
    'include',
    'index_by',
    'inject',
    'invoke',
    'map_',
    'mapiter',
    'max_',
    'min_',
    'partition',
    'pluck',
    'reduce_',
    'reduce_right',
    'reductions',
    'reductions_right',
    'reject',
    'sample',
    'select',
    'shuffle',
    'size',
    'some',
    'sort_by',
    'to_list',
    'where',
]


def at(collection, *indexes):  # pylint: disable=invalid-name
    """Creates a list of elements from the specified indexes, or keys, of the
    collection. Indexes may be specified as individual arguments or as arrays
    of indexes.

    Args:
        collection (list|dict): Collection to iterate over.
        indexes (mixed): The indexes of `collection` to retrieve, specified as
            individual indexes or arrays of indexes.

    Returns:
        list: filtered list

    .. versionadded:: 1.0.0
    """
    indexes = pyd.flatten_deep(indexes)
    return [collection[i] for i in indexes]


def contains(collection, target, from_index=0):
    """Checks if a given value is present in a collection. If `from_index` is
    negative, it is used as the offset from the end of the collection.

    Args:
        collection (list|dict): Collection to iterate over.
        target (mixed): Target value to compare to.
        from_index (int, optional): Offset to start search from.

    Returns:
        bool: Whether `target` is in `collection`.

    See Also:
        - :func:`contains` (main definition)
        - :func:`include` (alias)

    .. versionadded:: 1.0.0
    """
    if isinstance(collection, dict):
        collection = collection.values()
    else:
        # only makes sense to do this if `collection` is not a dict
        collection = collection[from_index:]

    return target in collection


include = contains


def count_by(collection, callback=None):
    """Creates an object composed of keys generated from the results of running
    each element of `collection` through the callback.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        dict: Dict containing counts by key.

    .. versionadded:: 1.0.0
    """
    ret = {}

    for result in itercallback(collection, callback):
        ret.setdefault(result[0], 0)
        ret[result[0]] += 1

    return ret


def deep_pluck(collection, path):
    """Like pluck but works with deep paths.

    Args:
        collection (list|dict): list of dicts
        path (str|list): collection's path to pluck

    Returns:
        list: plucked list

    .. versionadded:: 2.2.0
    """
    return map_(collection, pyd.deep_property(path))


def every(collection, callback=None):
    """Checks if the callback returns a truthy value for all elements of a
    collection. The callback is invoked with three arguments:
    ``(value, index|key, collection)``. If a property name is passed for
    callback, the created :func:`pluck` style callback will return the property
    value of the given element. If an object is passed for callback, the
    created :func:`where` style callback will return ``True`` for elements that
    have the properties of the given object, else ``False``.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        bool: Whether all elements are truthy.

    See Also:
        - :func:`every` (main definition)
        - :func:`all_` (alias)

    .. versionadded:: 1.0.0
    """

    if callback:
        cbk = pyd.iteratee(callback)
        collection = [cbk(item) for item in collection]

    return all(collection)


all_ = every


def filter_(collection, callback=None):
    """Iterates over elements of a collection, returning an list of all
    elements the callback returns truthy for.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        list: Filtered list.

    See Also:
        - :func:`select` (main definition)
        - :func:`filter_` (alias)

    .. versionadded:: 1.0.0
    """
    return [value
            for is_true, value, _, _ in itercallback(collection, callback)
            if is_true]


select = filter_


def find(collection, callback=None):
    """Iterates over elements of a collection, returning the first element that
    the callback returns truthy for.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        mixed: First element found or ``None``.

    See Also:
        - :func:`find` (main definition)
        - :func:`detect` (alias)
        - :func:`find_where` (alias)

    .. versionadded:: 1.0.0
    """
    search = (collection[key]
              for is_true, _, key, _ in itercallback(collection, callback)
              if is_true)
    return next(search, None)


detect = find
find_where = find


def find_last(collection, callback=None):
    """This method is like :func:`find` except that it iterates over elements
    of a `collection` from right to left.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        mixed: Last element found or ``None``.

    .. versionadded:: 1.0.0
    """
    search = (collection[key]
              for is_true, _, key, _ in itercallback(collection,
                                                     callback,
                                                     reverse=True)
              if is_true)
    return next(search, None)


def for_each(collection, callback=None):
    """Iterates over elements of a collection, executing the callback for each
    element.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        list|dict: `collection`

    See Also:
        - :func:`for_each` (main definition)
        - :func:`each` (alias)

    .. versionadded:: 1.0.0
    """
    next((None for ret, _, _, _ in itercallback(collection, callback)
          if ret is False),
         None)
    return collection


each = for_each


def for_each_right(collection, callback):
    """This method is like :func:`for_each` except that it iterates over
    elements of a `collection` from right to left.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        list|dict: `collection`

    See Also:
        - :func:`for_each_right` (main definition)
        - :func:`each_right` (alias)

    .. versionadded:: 1.0.0
    """
    next((None for ret, _, _, _ in itercallback(collection,
                                                callback,
                                                reverse=True)
          if ret is False),
         None)
    return collection


each_right = for_each_right


def group_by(collection, callback=None):
    """Creates an object composed of keys generated from the results of running
    each element of a `collection` through the callback.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        dict: Results of grouping by `callback`.

    .. versionadded:: 1.0.0
    """
    ret = {}
    cbk = pyd.iteratee(callback)

    for value in collection:
        key = cbk(value)
        ret.setdefault(key, [])
        ret[key].append(value)

    return ret


def index_by(collection, callback=None):
    """Creates an object composed of keys generated from the results of running
    each element of the collection through the given callback.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        dict: Results of indexing by `callback`.

    .. versionadded:: 1.0.0
    """
    ret = {}
    cbk = pyd.iteratee(callback)

    for value in collection:
        ret[cbk(value)] = value

    return ret


def invoke(collection, method_name, *args, **kargs):
    """Invokes the method named by `method_name` on each element in the
    `collection` returning a list of the results of each invoked method.

    Args:
        collection (list|dict): Collection to iterate over.
        method_name (str): Name of method to invoke.
        args (optional): Arguments to pass to method call.
        kargs (optional): Keyword arguments to pass to method call.

    Returns:
        list: List of results of invoking method of each item.

    .. versionadded:: 1.0.0
    """
    lst = []

    for item in collection:
        if callable(method_name):
            lst.append(method_name(item, *args, **kargs))
        else:
            lst.append(getattr(item, method_name)(*args, **kargs))

    return lst


def map_(collection, callback=None):
    """Creates an array of values by running each element in the collection
    through the callback. The callback is invoked with three arguments:
    ``(value, index|key, collection)``. If a property name is passed for
    callback, the created :func:`pluck` style callback will return the property
    value of the given element. If an object is passed for callback, the
    created :func:`where` style callback will return ``True`` for elements that
    have the properties of the given object, else ``False``.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        list: Mapped list.

    See Also:
        - :func:`map_` (main definition)
        - :func:`collect` (alias)

    .. versionadded:: 1.0.0
    """
    return list(mapiter(collection, callback))


collect = map_


def mapiter(collection, callback=None):
    """Like :func:`map_` except returns a generator.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        generator: Each mapped item.

    .. versionadded:: 2.1.0
    """
    for result in itercallback(collection, callback):
        yield result[0]


def max_(collection, callback=None):
    """Retrieves the maximum value of a `collection`.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        mixed: Maximum value.

    .. versionadded:: 1.0.0
    """
    if isinstance(collection, dict):
        collection = collection.values()

    return max(collection, key=pyd.iteratee(callback))


def min_(collection, callback=None):
    """Retrieves the minimum value of a `collection`.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        mixed: Minimum value.

    .. versionadded:: 1.0.0
    """
    if isinstance(collection, dict):
        collection = collection.values()

    return min(collection, key=pyd.iteratee(callback))


def partition(collection, callback=None):
    """Creates an array of elements split into two groups, the first of which
    contains elements the `callback` returns truthy for, while the second of
    which contains elements the `callback` returns falsey for. The `callback`
    is invoked with three arguments: ``(value, index|key, collection)``.

    If a property name is provided for `callback` the created :func:`pluck`
    style callback returns the property value of the given element.

    If an object is provided for `callback` the created :func:`where` style
    callback returns ``True`` for elements that have the properties of the
    given object, else ``False``.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        list: List of grouped elements.

    .. versionadded:: 1.1.0
    """
    trues = []
    falses = []

    for is_true, value, _, _ in itercallback(collection, callback):
        if is_true:
            trues.append(value)
        else:
            falses.append(value)

    return [trues, falses]


def pluck(collection, key):
    """Retrieves the value of a specified property from all elements in the
    collection.

    Args:
        collection (list|dict): list of dicts
        key (str): collection's key to pluck

    Returns:
        list: plucked list

    .. versionadded:: 1.0.0
    """
    return map_(collection, pyd.prop(key))


def reduce_(collection, callback=None, accumulator=None):
    """Reduces a collection to a value which is the accumulated result of
    running each element in the collection through the callback, where each
    successive callback execution consumes the return value of the previous
    execution.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed): Callback applied per iteration.
        accumulator (mixed, optional): Initial value of aggregator. Default is
            to use the result of the first iteration.

    Returns:
        mixed: Accumulator object containing results of reduction.

    See Also:
        - :func:`reduce_` (main definition)
        - :func:`foldl` (alias)
        - :func:`inject` (alias)

    .. versionadded:: 1.0.0
    """
    iterable = iterator(collection)

    if accumulator is None:
        try:
            _, accumulator = next(iterable)
        except StopIteration:
            raise TypeError(
                'reduce_() of empty sequence with no initial value')

    result = accumulator

    if callback is None:
        callback = lambda item, *args: item

    for index, item in iterable:
        result = call_callback(callback, result, item, index)

    return result


foldl = reduce_
inject = reduce_


def reduce_right(collection, callback=None, accumulator=None):
    """This method is like :func:`reduce_` except that it iterates over
    elements of a `collection` from right to left.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed): Callback applied per iteration.
        accumulator (mixed, optional): Initial value of aggregator. Default is
            to use the result of the first iteration.

    Returns:
        mixed: Accumulator object containing results of reduction.

    See Also:
        - :func:`reduce_right` (main definition)
        - :func:`foldr` (alias)

    .. versionadded:: 1.0.0
    """
    if not isinstance(collection, dict):
        collection = sorted(collection, reverse=True)
    return reduce_(collection, callback, accumulator)


foldr = reduce_right


def reductions(collection, callback=None, accumulator=None, from_right=False):
    """This function is like :func:`reduce_` except that it returns a list of
    every intermediate value in the reduction operation.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed): Callback applied per iteration.
        accumulator (mixed, optional): Initial value of aggregator. Default is
            to use the result of the first iteration.

    Returns:
        list: Results of each reduction operation.

    Note:
        The last element of the returned list would be the result of using
        :func:`reduce_`.

    .. versionadded:: 2.0.0
    """
    if callback is None:
        callback = lambda item, *args: item

    results = []

    def interceptor(result, item, index):  # pylint: disable=missing-docstring
        result = call_callback(callback, result, item, index)
        results.append(result)
        return result

    reducer = reduce_right if from_right else reduce_
    reducer(collection, interceptor, accumulator)

    return results


def reductions_right(collection, callback=None, accumulator=None):
    """This method is like :func:`reductions` except that it iterates over
    elements of a `collection` from right to left.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed): Callback applied per iteration.
        accumulator (mixed, optional): Initial value of aggregator. Default is
            to use the result of the first iteration.

    Returns:
        list: Results of each reduction operation.

    Note:
        The last element of the returned list would be the result of using
        :func:`reduce_`.

    .. versionadded:: 2.0.0
    """
    return reductions(collection, callback, accumulator, from_right=True)


def reject(collection, callback=None):
    """The opposite of :func:`filter_` this method returns the elements of a
    collection that the callback does **not** return truthy for.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        list: Rejected elements of `collection`.

    .. versionadded:: 1.0.0
    """
    return [value
            for is_true, value, _, _ in itercallback(collection, callback)
            if not is_true]


def sample(collection, n=None):
    """Retrieves a random element or `n` random elements from a `collection`.

    Args:
        collection (list|dict): Collection to iterate over.
        n (int, optional): Number of random samples to return.

    Returns:
        list|mixed: List of sampled collection value if `n` is provided, else
            single value from collection if `n` is ``None``.

    .. versionadded:: 1.0.0
    """
    num = min(n or 1, len(collection))
    sampled = random.sample(collection, num)
    return sampled[0] if n is None else sampled


def shuffle(collection):
    """Creates a list of shuffled values, using a version of the Fisher-Yates
    shuffle.

    Args:
        collection (list|dict): Collection to iterate over.

    Returns:
        list: Shuffled list of values.

    .. versionadded:: 1.0.0
    """
    if isinstance(collection, dict):
        collection = collection.values()

    # Make copy of collection since random.shuffle works on list in-place.
    collection = list(collection)

    # NOTE: random.shuffle uses Fisher-Yates.
    random.shuffle(collection)

    return collection


def size(collection):
    """Gets the size of the `collection` by returning `len(collection)` for
    iterable objects.

    Args:
        collection (list|dict): Collection to iterate over.

    Returns:
        int: Collection length.

    .. versionadded:: 1.0.0
    """
    return len(collection)


def some(collection, callback=None):
    """Checks if the callback returns a truthy value for any element of a
    collection. The callback is invoked with three arguments:
    ``(value, index|key, collection)``. If a property name is passed for
    callback, the created :func:`pluck` style callback will return the property
    value of the given element. If an object is passed for callback, the
    created :func:`where` style callback will return ``True`` for elements that
    have the properties of the given object, else ``False``.

    Args:
        collection (list|dict): Collection to iterate over.
        callbacked (mixed, optional): Callback applied per iteration.

    Returns:
        bool: Whether any of the elements are truthy.

    See Also:
        - :func:`some` (main definition)
        - :func:`any_` (alias)

    .. versionadded:: 1.0.0
    """

    if callback:
        cbk = pyd.iteratee(callback)
        collection = [cbk(item) for item in collection]

    return any(collection)


any_ = some


def sort_by(collection, callback=None):
    """Creates a list of elements, sorted in ascending order by the results of
    running each element in a `collection` through the callback.

    Args:
        collection (list|dict): Collection to iterate over.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        list: Sorted list.

    .. versionadded:: 1.0.0
    """
    if isinstance(collection, dict):
        collection = collection.values()

    return sorted(collection, key=pyd.iteratee(callback))


def to_list(collection):
    """Converts the collection to a list.

    Args:
        collection (list|dict): Collection to iterate over.

    Returns:
        list: Collection converted to list.

    .. versionadded:: 1.0.0
    """
    if isinstance(collection, dict):
        ret = collection.values()
    else:
        ret = list(collection)

    return ret


def where(collection, properties):
    """Examines each element in a collection, returning an array of all
    elements that have the given properties.

    Args:
        collection (list|dict): Collection to iterate over.
        properties (dict): property values to filter by

    Returns:
        list: filtered list.

    .. versionadded:: 1.0.0
    """
    return filter_(collection, pyd.matches(properties))
