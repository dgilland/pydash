"""Functions that operate on lists.

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import

from collections import Iterable
from bisect import bisect_left, bisect_right
from math import ceil

from .._compat import string_types
from .utilities import (
    create_callback,
    _iter_callback,
    _iter_unique,
    _deprecated
)


__all__ = [
    'chunk',
    'compact',
    'difference',
    'drop',
    'drop_right',
    'drop_right_while',
    'drop_while',
    'find_index',
    'find_last_index',
    'first',
    'flatten',
    'head',
    'index_of',
    'initial',
    'intersection',
    'last',
    'last_index_of',
    'object_',
    'pull',
    'pull_at',
    'remove',
    'rest',
    'slice_',
    'sorted_index',
    'sorted_last_index',
    'tail',
    'take',
    'take_right',
    'take_right_while',
    'take_while',
    'union',
    'uniq',
    'unique',
    'without',
    'xor',
    'zip_',
    'unzip',
    'zip_object',
]


def chunk(array, size=1):
    """Creates a list of elements split into groups the length of `size`. If
    `array` can't be split evenly, the final chunk will be the remaining
    elements.

    Args:
        array (list): List to chunk.
        size (int, optional): Chunk size. Defaults to ``1``.

    Returns:
        list: New list containing chunks of `array`.

    .. versionadded:: 1.1.0
    """
    chunks = int(ceil(len(array) / float(size)))
    return [array[i * size:(i + 1) * size] for i in range(chunks)]


def compact(array):
    """Creates a list with all falsey values of array removed.

    Args:
        array (list): List to compact.

    Returns:
        list: Compacted list.

    .. versionadded:: 1.0.0
    """
    return [item for item in array if item]


def difference(array, *lists):
    """Creates a list of list elements not present in the other lists.

    Args:
        array (list): List to process.
        lists (list): Lists to check.

    Returns:
        list: Difference of the lists.

    .. versionadded:: 1.0.0
    """
    return (list(difference(set(array).difference(lists[0]),
                            *lists[1:])) if lists
            else array)


def drop(array, n):
    """Creates a slice of `array` with `n` elements dropped from the beginning.

    Args:
        array (list): List to process.
        n (int): Number of elements to drop.

    Returns:
        list: Dropped list.

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
       Added ``n`` argument and removed as alias of :func:`rest`.
    """
    return drop_while(array, lambda _, index, *args: index < n)


def drop_right(array, n):
    """Creates a slice of `array` with `n` elements dropped from the end.

    Args:
        array (list): List to process.
        n (int): Number of elements to drop.

    Returns:
        list: Dropped list.

    .. versionadded:: 1.1.0
    """
    length = len(array)
    return drop_right_while(array,
                            lambda _, index, *args: (length - index) <= n)


def drop_right_while(array, callback=None):
    """Creates a slice of `array` excluding elements dropped from the end.
    Elements are dropped until the `callback` returns falsey. The `callback` is
    invoked with three arguments: ``(value, index, array)``.

    Args:
        array (list): List to process.
        callback (mixed): Callback called per iteration

    Returns:
        list: Dropped list.

    .. versionadded:: 1.1.0
    """
    n = len(array)
    for is_true, _, _, _ in _iter_callback(array, callback, reverse=True):
        if is_true:
            n -= 1
        else:
            break

    return array[:n]


def drop_while(array, callback=None):
    """Creates a slice of `array` excluding elements dropped from the
    beginning. Elements are dropped until the `callback` returns falsey. The
    `callback` is invoked with three arguments: ``(value, index, array)``.

    Args:
        array (list): List to process.
        callback (mixed): Callback called per iteration

    Returns:
        list: Dropped list.

    .. versionadded:: 1.1.0
    """
    n = 0
    for is_true, _, _, _ in _iter_callback(array, callback):
        if is_true:
            n += 1
        else:
            break

    return array[n:]


def find_index(array, callback=None):
    """This method is similar to :func:`pydash.api.collections.find`, except
    that it returns the index of the element that passes the callback check,
    instead of the element itself.

    Args:
        array (list): List to process.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        int: Index of found item or ``-1`` if not found.

    .. versionadded:: 1.0.0
    """
    n = -1
    for is_true, _, i, _ in _iter_callback(array, callback):
        if is_true:
            n = i
            break

    return n


def find_last_index(array, callback=None):
    """This method is similar to :func:`find_index`, except that it iterates
    over elements from right to left.

    Args:
        array (list): List to process.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        int: Index of found item or ``-1`` if not found.

    .. versionadded:: 1.0.0
    """
    n = -1
    for is_true, _, i, _ in _iter_callback(array, callback, reverse=True):
        if is_true:
            n = i
            break

    return n


def first(array):
    """Return the first element of `array`.

    Args:
        array (list): List to process.

    Returns:
        mixed: First element of list.

    See Also:
        - :func:`first` (main definition)
        - :func:`head` (alias)
        - :func:`take` (alias)

    .. versionadded:: 1.0.0
    """
    return array[0] if array else None


head = first


def flatten(array, callback=None, _depth=0):
    """Flattens a nested array (the nesting can be to any depth). If callback
    is True, array will only be flattened a single level. If callback is
    passed, each element of array is passed through a callback before
    flattening.

    Args:
        array (list): List to process.
        callback (mixed, optional): Callback applied per iteration. If ``True``
            then flatten shallowly.

    Returns:
        list: Flattened list.

    .. versionadded:: 1.0.0
    """

    shallow = False

    if callback is True:
        shallow = True
    elif callback:
        cbk = create_callback(callback)
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
        array (list): List to search.
        value (mixed): Value to search for.
        from_index (int, optional): Index to search from.

    Returns:
        int: Index of found item or ``-1`` if not found.

    .. versionadded:: 1.0.0
    """
    try:
        return array.index(value, from_index)
    except ValueError:
        return -1


def initial(array):
    """Return all but the last element of `array`.

    .. versionadded:: 1.0.0
    """
    return array[:-1]


def intersection(*arrays):
    """Computes the intersection of all the passed-in arrays.

    Args:
        arrays (list): Lists to process.

    Returns:
        list: Intersection of provided lists.

    .. versionadded:: 1.0.0
    """

    return list(set(arrays[0]).intersection(*arrays))


def last(array):
    """Return the last element of `array`.

    .. versionadded:: 1.0.0
    """
    return array[-1] if array else None


def last_index_of(array, value, from_index=None):
    """Gets the index at which the last occurrence of value is found.

    Args:
        array (list): List to search.
        value (mixed): Value to search for.
        from_index (int, optional): Index to search from.

    Returns:
        int: Index of found item or ``False`` if not found.

    .. versionadded:: 1.0.0
    """
    index = array_len = len(array)

    try:
        from_index = int(from_index)
    except (TypeError, ValueError):
        pass
    else:
        # Set starting index base on from_index offset.
        index = (max(0, index + from_index) if from_index < 0
                 else min(from_index, index - 1))

    while index:
        if index < array_len and array[index] == value:
            return index
        index -= 1
    return -1


def pull(array, *values):
    """Removes all provided values from the given array.

    Args:
        array (list): List to pull from.
        values (mixed): Values to remove.

    Returns:
        list: Modified `array`.

    Warning:
        `array` is modified in place.

    .. versionadded:: 1.0.0
    """
    for value in values:
        while array.count(value) > 0:
            array.remove(value)

    return array


def pull_at(array, *indexes):
    """Removes elements from `array` corresponding to the specified indexes and
    returns a list of the removed elements. Indexes may be specified as a list
    of indexes or as individual arguments.

    Args:
        array (list): List to pull from.
        *indexes (int): Indexes to pull.

    Returns:
        list: Modified `array`.

    Warning:
        `array` is modified in place.

    .. versionadded:: 1.1.0
    """
    indexes = flatten(indexes)
    for index in sorted(indexes, reverse=True):
        del array[index]

    return array


def remove(array, callback=None):
    """Removes all elements from a list that the callback returns truthy for
    and returns an array of removed elements.

    Args:
        array (list): List to remove elements from.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        list: Removed elements of `array`.

    Warning:
        `array` is modified in place.

    .. versionadded:: 1.0.0
    """
    removed = []
    for is_true, _, i, _ in _iter_callback(array, callback):
        if is_true:
            removed.append(array.pop(i))

    return removed


def rest(array):
    """Return all but the first element of `array`.

    Args:
        array (list): List to process.

    Returns:
        list: Rest of the list.

    See Also:
        - :func:`rest` (main definition)
        - :func:`tail` (alias)
        - :func:`drop` (alias)

    .. versionadded:: 1.0.0
    """
    return array[1:]


@_deprecated
def tail(array):
    """Return all but the first element of `array`.

    .. versionadded:: 1.0.0

    .. deprecated:: 1.1.0
       Use :func:`rest` instead.
    """
    return rest(array)


def slice_(array, start, end):
    """Slices `array` from the `start` index up to, but not including, the
    `end` index.

    Args:
        array (list): Array to slice.
        start (int): Start index.
        end (int): End index.

    Returns:
        list: Sliced list.

    .. versionadded:: 1.1.0
    """
    return array[start:end]


def sorted_index(array, value, callback=None):
    """Determine the smallest index at which the value should be inserted into
    array in order to maintain the sort order of the sorted array. If callback
    is passed, it will be executed for value and each element in array to
    compute their sort ranking. The callback is invoked with one argument:
    ``(value)``. If a property name is passed for callback, the created
    :func:`pydash.api.collections.pluck` style callback will return the
    property value of the given element. If an object is passed for callback,
    the created :func:`pydash.api.collections.where` style callback will return
    ``True`` for elements that have the properties of the given object, else
    ``False``.

    Args:
        array (list): List to inspect.
        value (mixed): Value to evaluate.
        callback (mixed, optional): Callback to determine sort key.

    Returns:
        int: Smallest index.

    .. versionadded:: 1.0.0
    """
    if callback:
        # Generate array of sorted keys computed using callback.
        callback = create_callback(callback)
        array = sorted(callback(item) for item in array)
        value = callback(value)

    return bisect_left(array, value)


def sorted_last_index(array, value, callback=None):
    """This method is like :func:`sorted_index` except that it returns the
    highest index at which a value should be inserted into a given sorted array
    in order to maintain the sort order of the array.

    Args:
        array (list): List to inspect.
        value (mixed): Value to evaluate.
        callback (mixed, optional): Callback to determine sort key.

    Returns:
        int: Highest index.

    .. versionadded:: 1.1.0
    """
    if callback:
        # Generate array of sorted keys computed using callback.
        callback = create_callback(callback)
        array = sorted(callback(item) for item in array)
        value = callback(value)

    return bisect_right(array, value)


def take(array, n):
    """Creates a slice of `array` with `n` elements taken from the beginning.

    Args:
        array (list): List to process.
        n (int): Number of elements to take.

    Returns:
        list: Taken list.

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
       Added ``n`` argument and removed as alias of :func:`first`.
    """
    return take_while(array, lambda _, index, *args: index < n)


def take_right(array, n):
    """Creates a slice of `array` with `n` elements taken from the end.

    Args:
        array (list): List to process.
        n (int): Number of elements to take.

    Returns:
        list: Taken list.

    .. versionadded:: 1.1.0
    """
    length = len(array)
    return take_right_while(array,
                            lambda _, index, *args: (length - index) <= n)


def take_right_while(array, callback=None):
    """Creates a slice of `array` with elements taken from the end. Elements
    are taken until the `callback` returns falsey. The `callback` is
    invoked with three arguments: ``(value, index, array)``.

    Args:
        array (list): List to process.
        callback (mixed): Callback called per iteration

    Returns:
        list: Dropped list.

    .. versionadded:: 1.1.0
    """
    n = len(array)
    for is_true, _, _, _ in _iter_callback(array, callback, reverse=True):
        if is_true:
            n -= 1
        else:
            break

    return array[n:]


def take_while(array, callback=None):
    """Creates a slice of `array` with elements taken from the beginning.
    Elements are taken until the `callback` returns falsey. The
    `callback` is invoked with three arguments: ``(value, index, array)``.

    Args:
        array (list): List to process.
        callback (mixed): Callback called per iteration

    Returns:
        list: Taken list.

    .. versionadded:: 1.1.0
    """
    n = 0
    for is_true, _, _, _ in _iter_callback(array, callback):
        if is_true:
            n += 1
        else:
            break

    return array[:n]


def union(*arrays):
    """Computes the union of the passed-in arrays.

    Args:
        arrays (list): Lists to unionize.

    Returns:
        list: Unionized list.

    .. versionadded:: 1.0.0
    """
    return uniq(flatten(arrays))


def uniq(array, callback=None):
    """Creates a duplicate-value-free version of the array. If callback is
    passed, each element of array is passed through a callback before
    uniqueness is computed. The callback is invoked with three arguments:
    ``(value, index, array)``. If a property name is passed for callback, the
    created :func:`pydash.api.collections.pluck` style callback will return the
    property value of the given element. If an object is passed for callback,
    the created :func:`pydash.api.collections.where` style callback will return
    ``True`` for elements that have the properties of the given object, else
    ``False``.

    Args:
        array (list): List to process.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        list: Unique list.

    See Also:
        - :func:`uniq` (main definition)
        - :func:`unique` (alias)

    .. versionadded:: 1.0.0
    """
    if callback:
        cbk = create_callback(callback)
        computed = [cbk(item) for item in array]
    else:
        computed = array

    # NOTE: User array[i] instead of item since callback could have modified
    # returned item values.
    lst = [array[i] for i, _ in _iter_unique(computed)]

    return lst


unique = uniq


def without(array, *values):
    """Creates an array with all occurrences of the passed values removed.

    Args:
        array (list): List to filter.
        values (mixed): Values to remove.

    Returns:
        list: Filtered list.

    .. versionadded:: 1.0.0
    """
    return [a for a in array if a not in values]


def xor(array, *lists):
    """Creates a list that is the symmetric difference of the provided lists.

    .. versionadded:: 1.0.0
    """
    return (list(xor(set(array).symmetric_difference(lists[0]),
                     *lists[1:])) if lists
            else array)


def zip_(*arrays):
    """Groups the elements of each array at their corresponding indexes.
    Useful for separate data sources that are coordinated through matching
    array indexes.

    Args:
        arrays (list): Lists to process.

    Returns:
        list: Zipped list.

    .. versionadded:: 1.0.0
    """
    # zip returns as a list of tuples so convert to list of lists
    return [list(item) for item in zip(*arrays)]


def unzip(array):
    """The inverse of :func:`zip_`, this method splits groups of
    elements into lists composed of elements from each group at their
    corresponding indexes.

    Args:
        array (list): List to process.

    Returns:
        list: Unzipped list.

    .. versionadded:: 1.0.0
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
        dict: Zipped dict.

    See Also:
        - :func:`zip_object` (main definition)
        - :func:`object_` (alias)

    .. versionadded:: 1.0.0
    """

    if values is None:
        zipped = keys
    else:
        zipped = zip(keys, values)

    return dict(zipped)


object_ = zip_object
