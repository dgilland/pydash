"""Functions that operate on lists.

.. versionadded:: 1.0.0
"""

from __future__ import absolute_import

from bisect import bisect_left, bisect_right
from math import ceil

import pydash as pyd
from .helpers import itercallback
from ._compat import cmp_to_key


__all__ = [
    'append',
    'cat',
    'chunk',
    'compact',
    'concat',
    'difference',
    'drop',
    'drop_right',
    'drop_right_while',
    'drop_while',
    'find_index',
    'find_last_index',
    'first',
    'flatten',
    'flatten_deep',
    'head',
    'index_of',
    'initial',
    'intercalate',
    'interleave',
    'intersection',
    'intersperse',
    'join',
    'last',
    'last_index_of',
    'mapcat',
    'object_',
    'pull',
    'pull_at',
    'push',
    'remove',
    'rest',
    'reverse',
    'shift',
    'slice_',
    'sort',
    'sorted_index',
    'sorted_last_index',
    'splice',
    'split_at',
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
    'unshift',
    'unzip',
    'zip_object',
]


def cat(*arrays):
    """Concatenates zero or more lists into one.

    Args:
        arrays (list): Lists to concatenate.

    Returns:
        list: Concatenated list.

    .. versionadded:: 2.0.0
    """
    return flatten(arrays)


concat = cat


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
    for is_true, _, _, _ in itercallback(array, callback, reverse=True):
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
    for is_true, _, _, _ in itercallback(array, callback):
        if is_true:
            n += 1
        else:
            break

    return array[n:]


def find_index(array, callback=None):
    """This method is similar to :func:`pydash.collections.find`, except
    that it returns the index of the element that passes the callback check,
    instead of the element itself.

    Args:
        array (list): List to process.
        callback (mixed, optional): Callback applied per iteration.

    Returns:
        int: Index of found item or ``-1`` if not found.

    .. versionadded:: 1.0.0
    """
    search = (i for is_true, _, i, _ in itercallback(array, callback)
              if is_true)
    return next(search, -1)


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
    search = (i for is_true, _, i, _ in itercallback(array,
                                                     callback,
                                                     reverse=True)
              if is_true)
    return next(search, -1)


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


def flatten(array, is_deep=False):
    """Flattens a nested array. If `is_deep` is ``True`` the array is
    recursively flattened, otherwise it is only flattened a single level.

    Args:
        array (list): List to process.
        is_deep (bool, optional): Whether to recursively flatten `array`.

    Returns:
        list: Flattened list.

    .. versionadded:: 1.0.0

    .. versionchanged:: 2.0.0
        Removed ``callback`` option. Added ``is_deep`` option. Made it shallow
        by default.
    """
    return list(iterflatten(array, is_deep=is_deep))


def flatten_deep(array):
    """Flattens a nested array recursively. This is the same as calling
    ``flatten(array, is_deep=True)``.

    Args:
        array (list): List to process.

    Returns:
        list: Flattened list.

    .. versionadded:: 2.0.0
    """
    return flatten(array, is_deep=True)


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


def intercalate(array, separator):
    """Like :func:`intersperse` for lists of lists but shallowly flattening the
    result.

    Args:
        array (list): List to intercalate.
        separator (mixed): Element to insert.

    Returns:
        list: Intercalated list.

    .. versionadded:: 2.0.0
    """
    return flatten(intersperse(array, separator))


def interleave(*arrays):
    """Merge multiple lists into a single list by inserting the next element of
    each list by sequential round-robin into the new list.

    Args:
        arrays (list): Lists to interleave.

    Retruns:
        list: Interleaved list.

    .. versionadded:: 2.0.0
    """
    return list(iterinterleave(*arrays))


def intersection(*arrays):
    """Computes the intersection of all the passed-in arrays.

    Args:
        arrays (list): Lists to process.

    Returns:
        list: Intersection of provided lists.

    .. versionadded:: 1.0.0
    """

    return list(set(arrays[0]).intersection(*arrays))


def intersperse(array, separator):
    """Insert a separating element between the elements of `array`.

    Args:
        array (list): List to intersperse.
        separator (mixed): Element to insert.

    Returns:
        list: Interspersed list.

    .. versionadded:: 2.0.0
    """
    return list(iterintersperse(array, separator))


def join(array, separator):
    """Return the elements of `array` as a string joined with `separator`.

    Args:
        array (list): List to join.
        separator (str): String to join with.

    Returns:
        str: Joined string.

    ..versionadded:: 2.2.0
    """
    return separator.join(pyd.map_(array, pyd.to_string))


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


def mapcat(array, callback=None):
    """Map a callback to each element of a list and concatenate the results
    into a single list using :func:`cat`.

    Args:
        array (list): List to map and concatenate.
        callback (mixed): Callback to apply to each element.

    Returns:
        list: Mapped and concatenated list.

    .. versionadded:: 2.0.0
    """
    return cat(*pyd.map_(array, callback))


def pop(array, index=-1):
    """Remove element of array at `index` and return element.

    Args:
        array (list): List to pop from.
        index (int, optional): Index to remove element from. Default is ``-1``.

    Returns:
        mixed: Value at `index`.

    Warning:
        `array` is modified in place.

    .. versionadded:: 2.2.0
    """
    return array.pop(index)


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
        indexes (int): Indexes to pull.

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


def push(array, *items):
    """Push items onto the end of `array` and return modified `array`.

    Args:
        array (list): List to push to.
        items (mixed): Items to append.

    Returns:
        list: Modified `array`.

    Warning:
        `array` is modified in place.

    .. versionadded:: 2.2.0
    """
    pyd.each(items, lambda item: array.append(item))
    return array


append = push


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
    for is_true, _, i, _ in itercallback(array, callback):
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

    .. versionadded:: 1.0.0
    """
    return array[1:]


tail = rest


def reverse(array):
    """Return `array` in reverse order.

    Args:
        array (list|string): Object to process.

    Returns:
        list|string: Reverse of object.

    .. versionadded:: 2.2.0
    """
    # NOTE: Using this method to reverse object since it works for both lists
    # and strings.
    return array[::-1]


def shift(array):
    """Remove the first element of `array` and return it.

    Args:
        array (list): List to shift.

    Returns:
        mixed: First element of `array`.

    Warning:
        `array` is modified in place.

    .. versionadded:: 2.2.0
    """
    return pop(array, 0)


def slice_(array, start=0, end=None):
    """Slices `array` from the `start` index up to, but not including, the
    `end` index.

    Args:
        array (list): Array to slice.
        start (int, optional): Start index. Defaults to ``0``.
        end (int, optional): End index. Defaults to selecting the value at
            ``start`` index.

    Returns:
        list: Sliced list.

    .. versionadded:: 1.1.0
    """
    if end is None:
        end = (start + 1) if start >= 0 else (len(array) + start + 1)

    return array[start:end]


def sort(array, comparison=None, key=None, reverse=False):
    """Sort `array` using optional `comparison`, `key`, and `reverse` options
    and return sorted `array`.

    Note:
        Python 3 removed the option to pass a custom comparison function and
        instead only allows a key function. Therefore, if a comparison
        function is passed in, it will be converted to a key function
        automatically using ``functools.cmp_to_key``.

    Args:
        array (list): List to sort.
        comparison (callable, optional): A custom comparison function used to
            sort the list. Function should accept two arguments and return a
            negative, zero, or position number depending on whether the first
            argument is considered smaller than, equal to, or larger than the
            second argument. Default is ``None``. This argument is mutually
            exclusive with `key`.
        key (callback, optional): A function of one argument used to extract a
            a comparison key from each list element. Default is ``None``. This
            argument is mutually exclusive with `comparison`.
        reverse: Whether to reverse the sort. Default is ``False``.

    Returns:
        list: Sorted list.

    Warning:
        `array` is modified in place.

    .. versionadded:: 2.2.0
    """
    if comparison and key:
        raise Exception(
            'The "comparison" and "key" arguments are mutually exclusive')

    if comparison:
        key = cmp_to_key(comparison)

    array.sort(key=key, reverse=reverse)
    return array


def sorted_index(array, value, callback=None):
    """Determine the smallest index at which the value should be inserted into
    array in order to maintain the sort order of the sorted array. If callback
    is passed, it will be executed for value and each element in array to
    compute their sort ranking. The callback is invoked with one argument:
    ``(value)``. If a property name is passed for callback, the created
    :func:`pydash.collections.pluck` style callback will return the
    property value of the given element. If an object is passed for callback,
    the created :func:`pydash.collections.where` style callback will return
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
        callback = pyd.iteratee(callback)
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
        callback = pyd.iteratee(callback)
        array = sorted(callback(item) for item in array)
        value = callback(value)

    return bisect_right(array, value)


def splice(array, index, how_many=None, *items):
    """Modify the contents of `array` by inserting elements starting at `index`
    and removing `how_many` number of elements after `index`.

    Args:
        array (list): List to splice.
        index (int): Index to splice at.
        how_many (int, optional): Number of items to remove starting at
            `index`. If ``None`` then all items after `index` are removed.
            Default is ``None``.
        items (mixed): Elements to insert starting at `index`. Each item is
            inserted in the order given.

    Returns:
        list: The removed elements of `array`.

    Warning:
        `array` is modified in place.

    .. versionadded:: 2.2.0
    """
    if how_many is None:
        how_many = len(array) - index

    removed = array[index:index + how_many]
    del array[index:index + how_many]

    for item in reverse(items):
        array.insert(index, item)

    return removed


def split_at(array, index):
    """Returns a list of two lists composed of the split of `array` at `index`.

    Args:
        array (list): List to split.
        index (int): Index to split at.

    Returns:
        list: Split list.

    .. versionadded:: 2.0.0
    """
    return [take(array, index), drop(array, index)]


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
    for is_true, _, _, _ in itercallback(array, callback, reverse=True):
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
    for is_true, _, _, _ in itercallback(array, callback):
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
    created :func:`pydash.collections.pluck` style callback will return the
    property value of the given element. If an object is passed for callback,
    the created :func:`pydash.collections.where` style callback will return
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
        cbk = pyd.iteratee(callback)
        computed = [cbk(item) for item in array]
    else:
        computed = array

    # NOTE: User array[i] instead of item since callback could have modified
    # returned item values.
    lst = [array[i] for i, _ in iterunique(computed)]

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


def unshift(array, *items):
    """Insert the given elements at the beginning of `array` and return the
    modified list.

    Args:
        array (list): List to modify.
        items (mixed): Items to insert.

    Returns:
        list: Modified list.

    Warning:
        `array` is modified in place.

    .. versionadded:: 2.2.0
    """
    for item in reverse(items):
        array.insert(0, item)

    return array


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


#
# Utility methods not a part of the main API
#


def iterflatten(array, is_deep=False, depth=0):
    """Iteratively flatten a list shallowly or deeply."""
    for item in array:
        if isinstance(item, (list, tuple)) and (is_deep or depth == 0):
            for subitem in iterflatten(item, is_deep, depth + 1):
                yield subitem
        else:
            yield item


def iterinterleave(*arrays):
    """Interleave multiple lists."""
    iters = [iter(arr) for arr in arrays]

    while iters:
        nextiters = []
        for itr in iters:
            try:
                yield next(itr)
                nextiters.append(itr)
            except StopIteration:
                pass

        iters = nextiters


def iterintersperse(iterable, separator):
    """Iteratively intersperse iterable."""
    iterable = iter(iterable)
    yield next(iterable)
    for item in iterable:
        yield separator
        yield item


def iterunique(array):
    """Return iterator to find unique list."""
    seen = []
    for i, item in enumerate(array):
        if item not in seen:
            seen.append(item)
            yield (i, item)
