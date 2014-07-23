
import collections
from bisect import bisect_left


#
# Arrays
#

def compact(array):
    """.. py:method:: compact(array)

    Creates a list with all falsey values of array removed.

    :param list array: list to compact
    :rtype: list
    """
    return filter(None, array)


def difference(array, *lists):
    """.. py:method:: difference(array[, *lists])

    Creates a list of list elements not present in the other lists

    :param list array: the list to process
    :param list lists: lists to check
    :rtype: list
    """
    return (list(difference(set(array).difference(lists[0]),
                            *lists[1:])) if lists
            else array)


def find_index(array, callback):
    """.. py:method:: find_index(array, callback|where)

    This method is similar to _.find, except that it returns the index of the
    element that passes the callback check, instead of the element itself.

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


def first(array, callback=None):
    """.. py:method:: first(array[, callback|n|pluck|where=None])

    Gets the first element of the array. If a number n is passed, the first n
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
    """.. py:method:: flatten(array[, callback|pluck|where=None])

    Flattens a nested array (the nesting can be to any depth). If callback is
    True, array will only be flattened a single level. If callback is passed,
    each element of array is passed through a callback before flattening.

    :param list array: list to flatten
    :param mixed callback: callback to filter array
    :rtype: list
    """

    shallow = False

    if callback is True:
        shallow = True
    elif callback:
        array = map(_make_callback(callback), array)
        callback = None

    lst = []
    if all([isinstance(array, collections.Iterable),
            not isinstance(array, basestring),
            not (shallow and _depth > 1)]):
        for a in array:
            lst.extend(flatten(a, callback, _depth + 1))
    else:
        lst.append(array)

    return lst


def index_of(array, value, from_index=0):
    """.. py:method:: index_of(array, value[, from_index=0])

    Gets the index at which the first occurrence of value is found.

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
    """.. py:method:: initial(array[, callback|n|pluck|where=None)

    Gets all but the last element of array. If a number n is passed, the last n
    elements are excluded from the result. If a callback function is passed,
    elements at the end of the array are excluded from the result as long as
    the callback returns truthy.

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
    """.. py:method:: intersection([array1, array2, ...])

    Computes the intersection of all the passed-in arrays using strict equality
    for comparisons, i.e. ===.

    :param list *arrays: arrays to process
    :rtype: list
    """

    return list(set(arrays[0]).intersection(*arrays))


def last(array, callback=None):
    """.. py:method:: last(array[, callback|n|pluck|where=None])

    Gets the last element of the array. If a number n is passed, the last n
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
    """.. py:method:: index_of(array, value[, from_index=0])

    Gets the index at which the first occurrence of value is found

    :param list array: list to search
    :param mixed value: value to search for
    :param integer from_index: the index to search from
    :rtype: integer
    """
    # reverse array, call index_of(), and subtract from max index
    return len(array) - 1 - index_of(array[::-1], value, from_index)


def pull():
    raise NotImplementedError


# functions just like builtin range
range_ = range


def remove():
    raise NotImplementedError


def rest(array, callback=None):
    """.. py:method:: rest(array[, callback|n|pluck|where=None])

    Return all but the first value of array. If a number n is passed, the first
    n values are excluded from the result. If a callback function is passed,
    elements at the beginning of the array are excluded from the result as long
    as the callback returns truthy. The callback is invoked with three
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
    """.. py:method:: sorted_index(array, value[, callback|pluck|where=None])

    Determine the smallest index at which the value should be inserted into
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
        callback = _make_callback(callback)
        array = map(callback, array)
        array.sort()
        value = callback(value)

    return bisect_left(array, value)


def union(*arrays):
    """.. py:method:: union(*arrays)

    Computes the union of the passed-in arrays using strict equality for
    comparisons, i.e. ===.

    :param list *arrays: lists to unionize
    :rtype: list
    """
    return uniq(flatten(arrays))


def uniq(array, callback=None):
    """.. py:method:: unique(array[, callback|pluck|where=None])

    Creates a duplicate-value-free version of the array using strict equality
    for comparisons, i.e. ===. If callback is passed, each element of array is
    passed through a callback before uniqueness is computed. The callback is
    invoked with three arguments: (value, index, array). If a property name is
    passed for callback, the created "_.pluck" style callback will return the
    property value of the given element. If an object is passed for callback,
    the created "_.where" style callback will return true for elements that
    have the properties of the given object, else false.

    :param list array: list to process
    :param mixed callback: callback to filter array
    :rtype: list
    """

    if isinstance(callback, dict):
        # where style callback; filter list using where
        array = where(array, callback)
        callback = None

    if callback:
        computed = map(_make_callback(callback), array)
    else:
        computed = array

    try:
        # Try faster version of uniqifier which requires all array elements to
        # be hashable.
        lst = [array[i] for i, x in _iter_unique_set(computed)]
    except Exception:
        # Fallback to version which doesn't require hashable elements but is
        # slower.
        lst = [array[i] for i, x in _iter_unique(computed)]

    return lst


unique = uniq


def without(array, *values):
    """.. py:method:: without(array, *values)

    Creates an array with all occurrences of the passed values removed using
    strict equality for comparisons, i.e. ===.

    :param list array: list to filter
    :param mixed *values: values to remove
    :rtype: list
    """
    return [a for a in array if a not in values]


def xor():
    raise NotImplementedError


def zip_(*arrays):
    """.. py:method:: zip_([array1, array2, ...])

    Groups the elements of each array at their corresponding indexes.
    Useful for separate data sources that are coordinated through matching
    array indexes.

    :param list *arrays: lists to process
    :rtype: list
    """
    # zip returns as a list of tuples so convert to list of lists
    return map(list, zip(*arrays))


# TODO: Lodash has this as an alias of zip_?
def unzip(array):
    """.. py:method:: unzip(array)

    The inverse of :py:method:`zipper`, this method splits groups of elements
    into arrays composed of elements from each group at their corresponding
    indexes.

    :param list *arrays: list to process
    :rtype: list
    """
    return zip_(*array)


def zip_object(keys, values=None):
    """.. py:method:: zip_object(keys[, values])

    Creates a dict composed from lists of keys and values. Pass either a single
    two dimensional list, i.e. [[key1, value1], [key2, value2]], or two lists,
    one of keys and one of corresponding values.

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
    """.. py:method:: at(collection, [index])

    Creates an array of elements from the specified indexes, or keys, of the
    collection. Indexes may be specified as individual arguments or as arrays
    of indexes.

    :param iterable collection: the collection to iterate over
    :param mixed indexes: the indexes of `collection` to retrieve, specified as
                          individual indexes or arrays of indexes
    """

    indexes = flatten(indexes)
    return [collection[i] for i in indexes]


def contains(collection, target, from_index=0):
    if isinstance(collection, dict):
        collection = collection.values()
    else:
        # only makes sense to do this if `collection` is not a dict
        collection = collection[from_index:]

    return target in collection


include = contains


def count_by(collection, callback):
    raise NotImplementedError


def every(collection, callback=None):
    """.. py:method:: every(collection[, callback|pluck|where=None])

    Checks if the callback returns a truthy value for all elements of a
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
        collection = map(_make_callback(callback), collection)

    return all(collection)


all_ = every


def filter_(collection, callback=None):
    if callback is None:
        callback = lambda item, *args: item

    return [value
            for is_true, value, _, _ in _iter_callback(collection, callback)
            if is_true]


select = filter_


def find(collection, callback=None):
    found = None
    for is_true, value, key, _ in _iter_callback(collection, callback):
        if is_true:
            found = collection[key]
            # only return first found item
            break

    return found


detect = find
find_where = find


def find_last():
    raise NotImplementedError


def for_each():
    raise NotImplementedError


each = for_each


def for_each_right():
    raise NotImplementedError


each_right = for_each_right


def group_by():
    raise NotImplementedError


def index_by():
    raise NotImplementedError


def invoke():
    raise NotImplementedError


def map_(collection, callback=None):
    """
    Creates an array of values by running each element in the collection
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


def min_():
    raise NotImplementedError


def max_():
    raise NotImplementedError


def pluck(collection, key):
    """.. py:method:: pluck(collection, key)

    Retrieves the value of a specified property from all elements in the
    collection.

    :param collection: a list of dicts
    :param key: the key value to pluck
    :rtype: list
    """
    return map(lambda x: x.get(key), collection)


def reduce_():
    raise NotImplementedError


foldl = reduce_
inject = reduce_


def reduce_right():
    raise NotImplementedError


foldr = reduce_right


def reject():
    raise NotImplementedError


def sample():
    raise NotImplementedError


def shuffle():
    raise NotImplementedError


def size():
    raise NotImplementedError


def some(collection, callback=None):
    """.. py:method:: some(collection[, callback|pluck|where=None])

    Checks if the callback returns a truthy value for any element of a
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
        collection = map(_make_callback(callback), collection)

    return any(collection)


any_ = some


def sort_by():
    raise NotImplementedError


def to_list():
    raise NotImplementedError


def where(collection, properties):
    """.. py:method:: where(collection, properties)

    Examines each element in a collection, returning an array of all elements
    that have the given properties.

    :param collection: a list of dicts
    :param properties: the dict of property values to filter by
    :rtype: list
    """
    filter_fn = lambda item: _where(item, properties)
    return filter(filter_fn, collection)


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
        cb = callback
    elif isinstance(callback, basestring):
        key = callback
        cb = lambda item, *args: pluck([item], key)[0]
    elif isinstance(callback, dict):
        cb = lambda item, *args: where([item], callback)
    else:
        index = callback if isinstance(callback, int) else 1
        cb = lambda item, i, *args: i < index

    return cb


def _iter_callback(collection, callback=None):
    """Return iterative callback based on collection type."""
    if isinstance(collection, dict):
        return _iter_dict_callback(collection, callback)
    else:
        return _iter_list_callback(collection, callback)


def _iter_list_callback(array, callback=None):
    """Return iterative list callback."""
    cb = _make_callback(callback)
    return ((cb(item, i, array), item, i, array)
            for i, item in enumerate(array))


def _iter_dict_callback(collection, callback=None):
    """Return iterative dict callback."""
    cb = _make_callback(callback)
    return ((cb(value, key, collection),)
            for key, value in collection.iteritems())


def _iter_unique_set(array):
    """Return iterator to find unique set."""
    seen = set()
    seen_add = seen.add
    for i, x in enumerate(array):
        if x not in seen and not seen_add(x):
            yield (i, x)


def _iter_unique(array):
    """Return iterator to find unique list."""
    seen = []
    for i, x in enumerate(array):
        if x not in seen:
            seen.append(x)
            yield (i, x)
