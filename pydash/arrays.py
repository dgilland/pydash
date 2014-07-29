"""Arrays
"""

from __future__ import absolute_import

from collections import Iterable
from bisect import bisect_left

from ._compat import string_types, _range
from .utilities import callback as make_callback
from .utils import (
    iter_callback,
    iter_unique_set,
    iter_unique
)


def compact(array):
    """Creates a list with all falsey values of array removed.

    Args:
        array (list): list to compact

    Returns:
        list: Compacted list
    """
    return [item for item in array if item]


def difference(array, *lists):
    """Creates a list of list elements not present in the other lists

    Args:
        array (list): the list to process
        lists (list): lists to check

    Returns:
        list: the difference of the lists
    """
    return (list(difference(set(array).difference(lists[0]),
                            *lists[1:])) if lists
            else array)


def find_index(array, callback=None):
    """This method is similar to :func:`pydash.collections.find`, except that
    it returns the index of the element that passes the callback check, instead
    of the element itself.

    Args:
        array (list): list to process
        callback (mixed, optional): callback applied per iteration

    Returns:
        int: index of found item
    """
    n = -1
    for is_true, _, i, _ in iter_callback(array, callback):
        if is_true:
            n = i
            break

    return n


def find_last_index(array, callback=None):
    """This method is similar to :func:`find_index`, except that it iterates
    over elements from right to left.

    Args:
        array (list): list to process
        callback (mixed, optional): callback applied per iteration

    Returns:
        int: index of found item
    """
    n = find_index(reversed(array), callback)

    if n is not -1:
        n = len(array) - n - 1

    return n


def first(array):
    """Return the first element of `array`."""
    return array[0] if array else None


head = first
take = first


def flatten(array, callback=None, _depth=0):
    """Flattens a nested array (the nesting can be to any depth). If callback
    is True, array will only be flattened a single level. If callback is
    passed, each element of array is passed through a callback before
    flattening.

    Args:
        array (list): list to flatten
        callback (mixed, optional): callback applied per iteration (if `True`
            then return shallow flatten)

    Returns:
        list: flattened list
    """

    shallow = False

    if callback is True:
        shallow = True
    elif callback:
        cbk = make_callback(callback)
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

    Args:
        array (list): list to search
        value (mixed): value to search for
        from_index (int, optional): the index to search from

    Returns:
        int: index of found item or ``False`` if not found
    """
    try:
        return array.index(value, from_index)
    except ValueError:
        return False


def initial(array):
    """Return all but the last element of `array`."""
    return array[:-1]


def intersection(*arrays):
    """Computes the intersection of all the passed-in arrays using strict
    equality for comparisons, i.e. ===.

    Args:
        arrays (list): arrays to process

    Returns:
        list: the intersection of provided lists
    """

    return list(set(arrays[0]).intersection(*arrays))


def last(array):
    """Return the last element of `array`."""
    return array[-1] if array else None


def last_index_of(array, value, from_index=0):
    """Gets the index at which the first occurrence of value is found

    Args:
        array (list): list to search
        value (mixed): value to search for
        from_index (int, optional): the index to search from

    Returns:
        int: index of found item or ``False`` if not found
    """
    # reverse array, call index_of(), and subtract from max index
    return len(array) - 1 - index_of(array[::-1], value, from_index)


def pull(array, *values):
    """Removes all provided values from the given array using strict equality
    for comparisons, i.e. ===.

    Args:
        array (list): list to modify
        values (mixed): values to remove

    Returns
        list: modified array

    Warning:
        Modified array in place
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
    for is_true, _, i, _ in iter_callback(array, callback):
        if is_true:
            removed.append(array.pop(i))

    return removed


def rest(array):
    """Return all but the first element of `array`."""
    return array[1:]


tail = rest
drop = rest


def sorted_index(array, value, callback=None):
    """Determine the smallest index at which the value should be inserted into
    array in order to maintain the sort order of the sorted array. If callback
    is passed, it will be executed for value and each element in array to
    compute their sort ranking. The callback is invoked with one argument:
    (value). If a property name is passed for callback, the created
    :func:`pydash.collection.pluck` style callback will return the property
    value of the given element. If an object is passed for callback, the
    created :func:`pydash.collections.where` style callback will return true
    for elements that have the properties of the given object, else ``False``.

    Args:
        array (list): list to inspect
        value (mixed): value to evaluate
        callback (mixed, optional): callback to determine sort key

    Returns:
        int: smallest index
    """

    if callback:
        # generate array of sorted keys computed using callback
        cbk = make_callback(callback)
        array = sorted(cbk(item) for item in array)
        value = cbk(value)

    return bisect_left(array, value)


def union(*arrays):
    """Computes the union of the passed-in arrays using strict equality for
    comparisons, i.e. ===.

    Args:
        arrays (list): lists to unionize

    Returns:
        list: unionized list
    """
    return uniq(flatten(arrays))


def uniq(array, callback=None):
    """Creates a duplicate-value-free version of the array using strict
    equality for comparisons, i.e. ===. If callback is passed, each element of
    array is passed through a callback before uniqueness is computed. The
    callback is invoked with three arguments: (value, index, array). If a
    property name is passed for callback, the created
    :func:`pydash.collection.pluck` style callback will return the property
    value of the given element. If an object is passed for callback, the
    created :func:`where` style callback will return ``True`` for elements that
    have the properties of the given object, else ``False``.

    Args:
        array (list): list to process
        callback (mixed, optional): callback applied per iteration

    Returns:
        list: uniqued list
    """
    if callback:
        cbk = make_callback(callback)
        computed = [cbk(item) for item in array]
    else:
        computed = array

    try:
        # Try faster version of uniqifier which requires all array elements to
        # be hashable.
        lst = [array[i] for i, _ in iter_unique_set(computed)]
    except Exception:  # pylint: disable=broad-except
        # Fallback to version which doesn't require hashable elements but is
        # slower.
        lst = [array[i] for i, _ in iter_unique(computed)]

    return lst


unique = uniq


def without(array, *values):
    """Creates an array with all occurrences of the passed values removed using
    strict equality for comparisons, i.e. ===.

    Args:
        array (list): list to filter
        values (mixed): values to remove

    Returns:
        list: filtered list
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

    Args:
        arrays (list): lists to process

    Returns:
        list: zipped list
    """
    # zip returns as a list of tuples so convert to list of lists
    return [list(item) for item in zip(*arrays)]


def unzip(array):
    """The inverse of :func:`zip_`, this method splits groups of
    elements into lists composed of elements from each group at their
    corresponding indexes.

    Args:
        array (list): list to process

    Returns:
        list: unzipped list
    """
    return zip_(*array)


def zip_object(keys, values=None):
    """Creates a dict composed from lists of keys and values. Pass either a
    single two dimensional list, i.e. ``[[key1, value1], [key2, value2]]``, or
    two lists, one of keys and one of corresponding values.

    Args:
        keys (list): either a list of keys or a list of ``[key, value]`` pairs
        values (list, optional): list of values to zip

    Returns:
        dict: zipped dict
    """

    if values is None:
        zipped = keys
    else:
        zipped = zip(keys, values)

    return dict(zipped)


object_ = zip_object
