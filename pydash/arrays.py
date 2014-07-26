"""Arrays
"""

from __future__ import absolute_import

from collections import Iterable
from bisect import bisect_left

from ._compat import string_types, _range
from .utils import (
    _make_callback,
    _iter_callback,
    _iter_unique_set,
    _iter_unique
)


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
    n = find_index(reversed(array), callback)

    if n is not -1:
        n = len(array) - n - 1

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
    if all([isinstance(array, Iterable),
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
    """Removes all provided values from the given array using strict equality
    for comparisons, i.e. ===.

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
        # FIXME: Resolve circular imports
        from .collections import where

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
