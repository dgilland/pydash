"""Python port of Lo-Dash
"""

import collections
from bisect import bisect_left
import random

from ._compat import string_types, iteritems, _range


#
# Arrays
#

def compact(array):
    """Creates a list with all falsey values of array removed.

    :param list array: list to compact
    :rtype: list
    """
    return [item for item in array if item]


def difference(array, *lists):
    """Creates a list of list elements not present in the other lists

    :param list array: the list to process
    :param list lists: lists to check
    :rtype: list
    """
    return (list(difference(set(array).difference(lists[0]),
                            *lists[1:])) if lists
            else array)


def find_index(array, callback):
    """This method is similar to _.find, except that it returns the index of
    the element that passes the callback check, instead of the element itself.

    :param list array: list to process
    :param function callback: filter function or where dict
    :rtype: list
    """
    n = -1
    for is_true, _, i, _ in _iter_callback(array, callback):
        if is_true:
            n = i
            break

    return n


def find_last_index(array, callback):
    """This method is similar to _.find_index, except that it iterates over
    elements from right to left.

    :param list array: list to process
    :param function callback: filter function or where dict
    :rtype: list
    """
    n = -1
    array = list(array)
    array.reverse()
    for is_true, _, i, _ in _iter_callback(array, callback):
        if is_true:
            n = len(array) - i - 1
            break

    return n


def first(array, callback=None):
    """Gets the first element of the array. If a number n is passed, the first
    n elements of the array are returned. If a callback function is passed,
    elements at the beginning of the array are returned as long as the callback
    returns truthy. The callback is invoked with three arguments:
    (value, index, array). If a property name is passed for callback, the
    created "_.pluck" style callback will return the property value of the
    given element. If an object is passed for callback, the created "_.where"
    style callback will return true for elements that have the properties of
    the given object, else false.

    :param list array: list to select from
    :param mixed callback: callback to filter array
    :rtype: mixed
    """
    n = 0
    for is_true, _, _, _ in _iter_callback(array, callback):
        if is_true:
            n += 1
        else:
            break

    ret = array[:n]

    if callback in (None, 1):
        ret = ret[0]

    return ret


head = first
take = first


def flatten(array, callback=None, _depth=0):
    """Flattens a nested array (the nesting can be to any depth). If callback
    is True, array will only be flattened a single level. If callback is
    passed, each element of array is passed through a callback before
    flattening.

    :param list array: list to flatten
    :param mixed callback: callback to filter array
    :rtype: list
    """

    shallow = False

    if callback is True:
        shallow = True
    elif callback:
        cbk = _make_callback(callback)
        array = [cbk(item) for item in array]
        callback = None

    lst = []
    if all([isinstance(array, collections.Iterable),
            not isinstance(array, string_types),
            not (shallow and _depth > 1)]):
        for arr in array:
            lst.extend(flatten(arr, callback, _depth + 1))
    else:
        lst.append(array)

    return lst


def index_of(array, value, from_index=0):
    """Gets the index at which the first occurrence of value is found.

    :param list array: list to search
    :param mixed value: value to search for
    :param integer from_index: the index to search from
    :rtype: integer
    """
    try:
        return array.index(value, from_index)
    except ValueError:
        return False


def initial(array, callback=1):
    """Gets all but the last element of array. If a number n is passed, the
    last n elements are excluded from the result. If a callback function is
    passed, elements at the end of the array are excluded from the result as
    long as the callback returns truthy.

    :param list array: list to query
    :param mixed callback: The function called per element or the number of
                           elements to exclude
    """

    lst = array[::-1]
    n = len(array)
    for is_true, _, _, _ in _iter_callback(lst, callback):
        if is_true:
            n -= 1
        else:
            break

    ret = array[:n]

    return ret


def intersection(*arrays):
    """Computes the intersection of all the passed-in arrays using strict
    equality for comparisons, i.e. ===.

    :param list *arrays: arrays to process
    :rtype: list
    """

    return list(set(arrays[0]).intersection(*arrays))


def last(array, callback=None):
    """Gets the last element of the array. If a number n is passed, the last n
    elements of the array are returned. If a callback function is passed,
    elements at the beginning of the array are returned as long as the callback
    returns truthy. The callback is invoked with three arguments:
    (value, index, array). If a property name is passed for callback, the
    created "_.pluck" style callback will return the property value of the
    given element. If an object is passed for callback, the created "_.where"
    style callback will return true for elements that have the properties of
    the given object, else false.

    :param list array: list to select from
    :param mixed callback: callback to filter array
    :rtype: mixed
    """

    # reverse array, call first(), and reverse again
    lst = first(array[::-1], callback)
    if isinstance(lst, list):
        lst = lst[::-1]

    return lst


def last_index_of(array, value, from_index=0):
    """Gets the index at which the first occurrence of value is found

    :param list array: list to search
    :param mixed value: value to search for
    :param integer from_index: the index to search from
    :rtype: integer
    """
    # reverse array, call index_of(), and subtract from max index
    return len(array) - 1 - index_of(array[::-1], value, from_index)


def pull(array, *values):
    """Removes all provided values from the given array using strict equality for
    comparisons, i.e. ===.

    :param list array: list to modify
    :param *values: values to remove
    :rtype: list
    """
    for value in values:
        while array.count(value) > 0:
            array.remove(value)

    return array


def range_(*args, **kargs):
    """Creates a list of numbers (positive and/or negative) progressing from
    start up to but not including end. If start is less than stop a zero-length
    range is created unless a negative step is specified.
    """
    return list(_range(*args, **kargs))


def remove(array, callback=None):
    """Removes all elements from a list that the callback returns truthy for
    and returns an array of removed elements.
    """
    removed = []
    for is_true, _, i, _ in _iter_callback(array, callback):
        if is_true:
            removed.append(array.pop(i))

    return removed


def rest(array, callback=None):
    """Return all but the first value of array. If a number n is passed, the
    first n values are excluded from the result. If a callback function is
    passed, elements at the beginning of the array are excluded from the result
    as long as the callback returns truthy. The callback is invoked with three
    arguments: (value, index, array). If a property name is passed for
    callback, the created "_.pluck" style callback will return the property
    value of the given element. If an object is passed for callback, the
    created "_.where" style callback will return true for elements that have
    the properties of the given object, else false.

    :param list array: the list to process
    :param mixed callback: callback to filter by
    :rtype: list
    """

    n = 0
    for is_true, _, _, _ in _iter_callback(array, callback):
        if is_true:
            n += 1
        else:
            break

    return array[n:]


tail = rest
drop = rest


def sorted_index(array, value, callback=None):
    """Determine the smallest index at which the value should be inserted into
    array in order to maintain the sort order of the sorted array. If callback
    is passed, it will be executed for value and each element in array to
    compute their sort ranking. The callback is invoked with one argument:
    (value). If a property name is passed for callback, the created "_.pluck"
    style callback will return the property value of the given element. If an
    object is passed for callback, the created "_.where" style callback will
    return true for elements that have the properties of the given object, else
    false.

    :param list array: list to inspect
    :param mixed value: value to evaluate
    :param mixed callback: callback to determine sort key
    :rtype: integer
    """

    if callback:
        # generate array of sorted keys computed using callback
        cbk = _make_callback(callback)
        array = sorted(cbk(item) for item in array)
        value = cbk(value)

    return bisect_left(array, value)


def union(*arrays):
    """Computes the union of the passed-in arrays using strict equality for
    comparisons, i.e. ===.

    :param list *arrays: lists to unionize
    :rtype: list
    """
    return uniq(flatten(arrays))


def uniq(array, callback=None):
    """Creates a duplicate-value-free version of the array using strict
    equality for comparisons, i.e. ===. If callback is passed, each element of
    array is passed through a callback before uniqueness is computed. The
    callback is invoked with three arguments: (value, index, array). If a
    property name is passed for callback, the created "_.pluck" style callback
    will return the property value of the given element. If an object is passed
    for callback, the created "_.where" style callback will return true for
    elements that have the properties of the given object, else false.

    :param list array: list to process
    :param mixed callback: callback to filter array
    :rtype: list
    """

    if isinstance(callback, dict):
        # where style callback; filter list using where
        array = where(array, callback)
        callback = None

    if callback:
        cbk = _make_callback(callback)
        computed = [cbk(item) for item in array]
    else:
        computed = array

    try:
        # Try faster version of uniqifier which requires all array elements to
        # be hashable.
        lst = [array[i] for i, _ in _iter_unique_set(computed)]
    except Exception:  # pylint: disable=broad-except
        # Fallback to version which doesn't require hashable elements but is
        # slower.
        lst = [array[i] for i, _ in _iter_unique(computed)]

    return lst


unique = uniq


def without(array, *values):
    """Creates an array with all occurrences of the passed values removed using
    strict equality for comparisons, i.e. ===.

    :param list array: list to filter
    :param mixed *values: values to remove
    :rtype: list
    """
    return [a for a in array if a not in values]


def xor(array, *lists):
    """Creates a list that is the symmetric difference of the provided lists.
    """
    return (list(xor(set(array).symmetric_difference(lists[0]),
                     *lists[1:])) if lists
            else array)


def zip_(*arrays):
    """Groups the elements of each array at their corresponding indexes.
    Useful for separate data sources that are coordinated through matching
    array indexes.

    :param list *arrays: lists to process
    :rtype: list
    """
    # zip returns as a list of tuples so convert to list of lists
    return [list(item) for item in zip(*arrays)]


def unzip(array):
    """The inverse of :func:`zipper`, this method splits groups of
    elements into lists composed of elements from each group at their
    corresponding indexes.

    :param list array: list to process
    :rtype: list
    """
    return zip_(*array)


def zip_object(keys, values=None):
    """Creates a dict composed from lists of keys and values. Pass either a
    single two dimensional list, i.e. [[key1, value1], [key2, value2]], or two
    lists, one of keys and one of corresponding values.

    :param list keys: either a list of keys or a list of [key, value] pairs
    :param list values: list of values
    :rtype: dict
    """

    if values is None:
        zipped = keys
    else:
        zipped = zip(keys, values)

    return dict(zipped)


object_ = zip_object


#
# Collections
#

def at(collection, *indexes):
    """Creates an array of elements from the specified indexes, or keys, of the
    collection. Indexes may be specified as individual arguments or as arrays
    of indexes.

    :param iterable collection: the collection to iterate over
    :param mixed indexes: the indexes of `collection` to retrieve, specified as
                          individual indexes or arrays of indexes
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
    cb = _make_callback(callback)

    for value in collection:
        key = cb(value)

        ret.setdefault(key, 0)
        ret[key] += 1

    return ret


def every(collection, callback=None):
    """Checks if the callback returns a truthy value for all elements of a
    collection. The callback is invoked with three arguments:
    (value, index|key, collection). If a property name is passed for callback,
    the created "_.pluck" style callback will return the property value of the
    given element. If an object is passed for callback, the created "_.where"
    style callback will return true for elements that have the properties of
    the given object, else false.

    :param iterable collection: the collection to iterate over
    :param mixed callback: function called per iteration
    :rtype: boolean
    """

    if callback:
        cbk = _make_callback(callback)
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
            for is_true, value, _, _ in _iter_callback(collection, callback)
            if is_true]


select = filter_


def find(collection, callback=None):
    """Iterates over elements of a collection, returning the first element that
    the callback returns truthy for.
    """
    found = None
    for is_true, _, key, _ in _iter_callback(collection, callback):
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
    found = None
    collection = list(collection)
    collection.reverse()
    for is_true, value, key, _ in _iter_callback(collection, callback):
        if is_true:
            found = collection[key]
            # only return first found item
            break

    return found


def for_each(*args, **kargs):  # pragma: no cover
    """Iterates over elements of a collection, executing the callback for each
    element.
    """
    raise NotImplementedError


each = for_each


def for_each_right(*args, **kargs):  # pragma: no cover
    """This method is like :func:`for_each` except that it iterates over
    elements of a `collection` from right to left.
    """
    raise NotImplementedError


each_right = for_each_right


def group_by(*args, **kargs):  # pragma: no cover
    """Creates an object composed of keys generated from the results of running
    each element of a `collection` through the callback.
    """
    raise NotImplementedError


def index_by(*args, **kargs):  # pragma: no cover
    """Creates an object composed of keys generated from the results of running
    each element of the collection through the given callback.
    """
    raise NotImplementedError


def invoke(*args, **kargs):  # pragma: no cover
    """Invokes the method named by `method_name` on each element in the
    `collection` returning a list of the results of each invoked method.
    """
    raise NotImplementedError


def map_(collection, callback=None):
    """Creates an array of values by running each element in the collection
    through the callback. The callback is invoked with three arguments:
    (value, index|key, collection). If a property name is passed for callback,
    the created "_.pluck" style callback will return the property value of the
    given element. If an object is passed for callback, the created "_.where"
    style callback will return true for elements that have the properties of
    the given object, else false.

    :param iterable collection: the collection to iterate over
    :param mixed callback: function called per iteration
    :rtype: list
    """
    if not callback:
        callback = lambda value, *args: value

    return [result[0] for result in _iter_callback(collection, callback)]


collect = map_


def max_(*args, **kargs):  # pragma: no cover
    """Retrieves the maximum value of a `collection`."""
    raise NotImplementedError


def min_(*args, **kargs):  # pragma: no cover
    """Retrieves the minimum value of a `collection`."""
    raise NotImplementedError


def pluck(collection, key):
    """Retrieves the value of a specified property from all elements in the
    collection.

    :param collection: a list of dicts
    :param key: the key value to pluck
    :rtype: list
    """
    # TODO: Do we want to use get() and return None if missing or error out?
    return [item.get(key) for item in collection]


def reduce_(collection, callback=None, accumulator=None):
    """Reduces a collection to a value which is the accumulated result of
    running each element in the collection through the callback, where each
    successive callback execution consumes the return value of the previous
    execution.
    """
    iterable = _iter(collection)

    if accumulator is None:
        try:
            _, accumulator = next(iterable)
            offset = 1
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


def reduce_right(collection, callback=None, accumulator=None):  # pragma: no cover
    """This method is like :func:`reduce_` except that it iterates over
    elements of a `collection` from right to left.
    """
    if not isinstance(collection, dict):
        collection = sorted(collection, reverse=True)
    return reduce_(collection, callback, accumulator)


foldr = reduce_right


def reject(*args, **kargs):  # pragma: no cover
    """The opposite of :func:`filter_` this method returns the elements of a
    collection that the callback does **not** return truthy for.
    """
    raise NotImplementedError


def sample(collection, n=None):
    """Retrieves a random element or `n` random elements from a `collection`.
    """
    nn = min(n or 1, len(collection))
    sampled = random.sample(collection, nn)
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
    the created "_.pluck" style callback will return the property value of the
    given element. If an object is passed for callback, the created "_.where"
    style callback will return true for elements that have the properties of
    the given object, else false.

    :param iterable collection: the collection to iterate over
    :param mixed callback: function called per iteration
    :rtype: boolean
    """

    if callback:
        cbk = _make_callback(callback)
        collection = [cbk(item) for item in collection]

    return any(collection)


any_ = some


def sort_by(*args, **kargs):  # pragma: no cover
    """Creates a list of elements, sorted in ascending order by the results of
    running each element in a `collection` through the callback.
    """
    raise NotImplementedError


def to_list(*args, **kargs):  # pragma: no cover
    """Converts the collection to a list."""
    raise NotImplementedError


def where(collection, properties):
    """Examines each element in a collection, returning an array of all
    elements that have the given properties.

    :param collection: a list of dicts
    :param properties: the dict of property values to filter by
    :rtype: list
    """
    filter_fn = lambda item: _where(item, properties)
    return [item for item in collection if filter_fn(item)]


def _where(superset, subset):
    """Helper function for where()"""
    return all(item in superset.items() for item in subset.items())


#
# Object
#


#
# Functions
#


#
# Chaining
#


#
# Utilities
#

def _make_callback(callback):
    """Create a callback function from a mixed type `callback`"""
    if hasattr(callback, '__call__'):
        cbk = callback
    elif isinstance(callback, string_types):
        key = callback
        cbk = lambda item, *args: pluck([item], key)[0]
    elif isinstance(callback, dict):
        cbk = lambda item, *args: where([item], callback)
    else:
        index = callback if isinstance(callback, int) else 1
        cbk = lambda item, i, *args: i < index

    return cbk


def _iter_callback(collection, callback=None):
    """Return iterative callback based on collection type."""
    if isinstance(collection, dict):
        return _iter_dict_callback(collection, callback)
    else:
        return _iter_list_callback(collection, callback)


def _iter_list_callback(array, callback=None):
    """Return iterative list callback."""
    cbk = _make_callback(callback)
    for i, item in enumerate(array):
        yield (cbk(item, i, array), item, i, array)


def _iter_dict_callback(collection, callback=None):
    """Return iterative dict callback."""
    cbk = _make_callback(callback)
    for key, value in iteritems(collection):
        yield (cbk(value, key, collection),)


def _iter(collection):
    """Return iterative based on collection type."""
    if isinstance(collection, dict):
        return _iter_dict(collection)
    else:
        return _iter_list(collection)


def _iter_dict(collection):
    """Return iterative dict."""
    return iteritems(collection)


def _iter_list(array):
    """Return iterative list."""
    for i, item in enumerate(array):
        yield i, item


def _iter_unique_set(array):
    """Return iterator to find unique set."""
    seen = set()
    seen_add = seen.add
    for i, item in enumerate(array):
        if item not in seen and not seen_add(item):
            yield (i, item)


def _iter_unique(array):
    """Return iterator to find unique list."""
    seen = []
    for i, item in enumerate(array):
        if item not in seen:
            seen.append(item)
            yield (i, item)
