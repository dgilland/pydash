"""Collections
"""

from __future__ import absolute_import

import random

from .arrays import flatten
from .utilities import matches, property_, callback as make_callback
from .utils import iter_callback, iterate


def at(collection, *indexes):  # pylint: disable=invalid-name
    """Creates a list of elements from the specified indexes, or keys, of the
    collection. Indexes may be specified as individual arguments or as arrays
    of indexes.

    Args:
        collection (iterable): collection to iterate over
        indexes (mixed): the indexes of `collection` to retrieve, specified as
            individual indexes or arrays of indexes

    Returns:
        list: filtered list
    """
    indexes = flatten(indexes)
    return [collection[i] for i in indexes]


def contains(collection, target, from_index=0):
    """Checks if a given value is present in a collection using strict equality
    for comparisons, i.e. ===. If `from_index` is negative, it is used as the
    offset from the end of the collection.
    """
    if isinstance(collection, dict):
        collection = collection.values()
    else:
        # only makes sense to do this if `collection` is not a dict
        collection = collection[from_index:]

    return target in collection


include = contains


def count_by(collection, callback):
    """Creates an object composed of keys generated from the results of running
    each element of `collection` through the callback.
    """
    ret = dict()
    cbk = make_callback(callback)

    for value in collection:
        key = cbk(value)

        ret.setdefault(key, 0)
        ret[key] += 1

    return ret


def every(collection, callback=None):
    """Checks if the callback returns a truthy value for all elements of a
    collection. The callback is invoked with three arguments:
    (value, index|key, collection). If a property name is passed for callback,
    the created :func:`pluck` style callback will return the property value of
    the given element. If an object is passed for callback, the created
    :func:`where` style callback will return true for elements that have the
    properties of the given object, else ``False``.

    Args:
        collection (iterable): collection to iterate over
        callback (mixed, optional): callback applied per iteration

    Returns:
        bool: whether all elements are truthy
    """

    if callback:
        cbk = make_callback(callback)
        collection = [cbk(item) for item in collection]

    return all(collection)


all_ = every


def filter_(collection, callback=None):
    """Iterates over elements of a collection, returning an list of all
    elements the callback returns truthy for.
    """
    if callback is None:
        callback = lambda item, *args: item

    return [value
            for is_true, value, _, _ in iter_callback(collection, callback)
            if is_true]


select = filter_


def find(collection, callback=None):
    """Iterates over elements of a collection, returning the first element that
    the callback returns truthy for.
    """
    found = None
    for is_true, _, key, _ in iter_callback(collection, callback):
        if is_true:
            found = collection[key]
            # only return first found item
            break

    return found


detect = find
find_where = find


def find_last(collection, callback=None):
    """This method is like :func:`find` except that it iterates over elements
    of a `collection` from right to left.
    """
    return find(list(reversed(collection)), callback)


def for_each(collection, callback):
    """Iterates over elements of a collection, executing the callback for each
    element.
    """
    for ret, _, _, _ in iter_callback(collection, callback):
        if ret is False:
            break

    return collection


each = for_each


def for_each_right(collection, callback):
    """This method is like :func:`for_each` except that it iterates over
    elements of a `collection` from right to left.
    """
    if isinstance(collection, dict):
        # Dicts have no order, nothing to be done.
        iterator = collection
    else:
        iterator = reversed(collection)

    for_each(iterator, callback)

    return collection


each_right = for_each_right


def group_by(collection, callback):
    """Creates an object composed of keys generated from the results of running
    each element of a `collection` through the callback.
    """
    ret = dict()
    cbk = make_callback(callback)

    for value in collection:
        key = cbk(value)
        ret.setdefault(key, [])
        ret[key].append(value)

    return ret


def index_by(collection, callback):
    """Creates an object composed of keys generated from the results of running
    each element of the collection through the given callback.
    """
    ret = dict()
    cbk = make_callback(callback)

    for value in collection:
        ret[cbk(value)] = value

    return ret


def invoke(collection, method_name, *args):
    """Invokes the method named by `method_name` on each element in the
    `collection` returning a list of the results of each invoked method.
    """
    lst = []

    for item in collection:
        if callable(method_name):
            lst.append(method_name(item, *args))
        else:
            lst.append(getattr(item, method_name)(*args))

    return lst


def map_(collection, callback=None):
    """Creates an array of values by running each element in the collection
    through the callback. The callback is invoked with three arguments:
    (value, index|key, collection). If a property name is passed for callback,
    the created :func:`pluck` style callback will return the property value of
    the given element. If an object is passed for callback, the created
    :func:`where` style callback will return true for elements that have the
    properties of the given object, else false.

    Args:
        collection (iterable): collection to iterate over
        callback (mixed, optional): callback applied per iteration

    Returns:
        list: mapped list
    """
    if not callback:
        callback = lambda value, *args: value

    return [result[0] for result in iter_callback(collection, callback)]


collect = map_


def max_(collection, callback=None):
    """Retrieves the maximum value of a `collection`."""
    if not callback:
        if isinstance(collection, dict):
            return max(collection.values())
        else:
            return max(collection)

    return max(collection, key=make_callback(callback))


def min_(collection, callback=None):
    """Retrieves the minimum value of a `collection`."""
    if not callback:
        if isinstance(collection, dict):
            return min(collection.values())
        else:
            return min(collection)

    return min(collection, key=make_callback(callback))


def pluck(collection, key):
    """Retrieves the value of a specified property from all elements in the
    collection.

    Args:
        collection (iterable): list of dicts
        key (str): collection's key to pluck

    Returns:
        list: plucked list
    """
    # TODO: Do we want to use get() and return None if missing or error out?
    return map_(collection, property_(key))


def reduce_(collection, callback=None, accumulator=None):
    """Reduces a collection to a value which is the accumulated result of
    running each element in the collection through the callback, where each
    successive callback execution consumes the return value of the previous
    execution.
    """
    iterable = iterate(collection)

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
        result = callback(result, item, index)

    return result


foldl = reduce_
inject = reduce_


def reduce_right(collection, callback=None, accumulator=None):
    """This method is like :func:`reduce_` except that it iterates over
    elements of a `collection` from right to left.
    """
    if not isinstance(collection, dict):
        collection = sorted(collection, reverse=True)
    return reduce_(collection, callback, accumulator)


foldr = reduce_right


def reject(collection, callback=None):
    """The opposite of :func:`filter_` this method returns the elements of a
    collection that the callback does **not** return truthy for.
    """
    if callback is None:
        callback = lambda item, *args: item

    return [value
            for is_true, value, _, _ in iter_callback(collection, callback)
            if not is_true]


def sample(collection, n=None):
    """Retrieves a random element or `n` random elements from a `collection`.
    """
    num = min(n or 1, len(collection))
    sampled = random.sample(collection, num)
    return sampled[0] if n is None else sampled


def shuffle(collection):
    """Creates a list of shuffled values, using a version of the Fisher-Yates
    shuffle.
    """
    # Make copy of collection since random.shuffle works on list in-place.
    collection = list(collection)

    # NOTE: random.shuffle uses Fisher-Yates.
    random.shuffle(collection)

    return collection


def size(collection):
    """Gets the size of the `collection` by returning `len(collection)` for
    iterable objects.
    """
    return len(collection)


def some(collection, callback=None):
    """Checks if the callback returns a truthy value for any element of a
    collection. The callback is invoked with three arguments:
    (value, index|key, collection). If a property name is passed for callback,
    the created :func:`pluck` style callback will return the property value of
    the given element. If an object is passed for callback, the created
    :func:`where` style callback will return true for elements that have the
    properties of the given object, else false.

    Args:
        collection (iterable): collection to iterate over
        callbacked (mixed, optional): callback applied per iteration

    Returns:
        bool: whether any of the elements are truthy
    """

    if callback:
        cbk = make_callback(callback)
        collection = [cbk(item) for item in collection]

    return any(collection)


any_ = some


def sort_by(collection, callback):
    """Creates a list of elements, sorted in ascending order by the results of
    running each element in a `collection` through the callback.
    """
    return sorted(collection, key=make_callback(callback))


def to_list(collection):
    """Converts the collection to a list."""
    return list(collection)


def where(collection, properties):
    """Examines each element in a collection, returning an array of all
    elements that have the given properties.

    Args:
        collection (iterable): collection to iterate over
        properties (dict): property values to filter by

    Returns:
        list: filtered list
    """
    return filter_(collection, matches(properties))
