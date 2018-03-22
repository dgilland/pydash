"fp variant of arrays functions"
import pydash as pyd
from .convert import convert
__all__ = (
    "chunk",
    "compact",
    "concat",
    "difference",
    "difference_by",
    "difference_with",
    "drop",
    "drop_while",
    "drop_right",
    "drop_right_while",
    "duplicates",
    "fill",
    "find_index",
    "find_last_index",
    "flatten",
    "flatten_deep",
    "flatten_depth",
    "from_pairs",
    "head",
    "index_of",
    "initial",
    "intercalate",
    "interleave",
    "intersection",
    "intersection_by",
    "intersection_with",
    "intersperse",
    "last",
    "last_index_of",
    "mapcat",
    "nth",
    "pull",
    "pull_all",
    "pull_all_by",
    "pull_all_with",
    "pull_at",
    "remove",
    "repack",
    "reverse",
    "slice_",
    "sorted_index",
    "sorted_index_by",
    "sorted_index_of",
    "sorted_last_index",
    "sorted_last_index_by",
    "sorted_last_index_of",
    "sorted_uniq",
    "sorted_uniq_by",
    "split_at",
    "tail",
    "take",
    "take_right",
    "take_right_while",
    "take_while",
    "union",
    "union_by",
    "union_with",
    "uniq",
    "uniq_by",
    "uniq_with",
    "unzip",
    "unzip_with",
    "without",
    "xor",
    "xor_by",
    "xor_with",
    "zip_",
    "zip_object",
    "zip_object_deep",
    "zip_with",
)


docstrings = {

    # chunk
    "chunk": """
Creates a list of elements split into groups the length of `size`. If
`array` can't be split evenly, the final chunk will be the remaining
elements.

Arity: 2

Args:
    size (int): Chunk size. Defaults to ``1``.
    array (list): List to chunk.

Returns:
    list: New list containing chunks of `array`.
Example:

    >>> chunk(2, [1, 2, 3, 4, 5])
    [[1, 2], [3, 4], [5]]

.. versionadded:: 1.1.0
""",

    # compact

    # concat
    "concat": """
Concatenates zero or more lists into one.

Arity: 2

Args:
    arrays (list): Lists to concatenate.

Returns:
    list: Concatenated list.
Example:


.. versionadded:: 2.0.0

.. versionchanged:: 4.0.0
    Renamed from ``cat`` to ``concat``.
""",

    # difference
    "difference": """
Creates a list of list elements not present in others.

Arity: 2

Args:
    array (list): List to process.
    others (list): Lists to check.

Returns:
    list: Difference between `others`.
Example:

    >>> difference([1, 2, 3], [1], [2])
    [3]

.. versionadded:: 1.0.0
""",

    # difference_by
    "difference_by": """
This method is like :func:`difference` except that it accepts an
iteratee which is invoked for each element of each array to generate the
criterion by which they're compared. The order and references of result
values are determined by `array`. The iteratee is invoked with one
argument: ``(value)``.

Arity: 3

Args:
    iteratee (mixed): Function to transform the elements of the
        arrays. Defaults to :func:`.identity`.
    array (list): The array to find the difference of.
    others (list): Lists to check for difference with `array`.

Returns:
    list: Difference between `others`.
Example:

    >>> difference_by(round, [1.2, 1.5, 1.7, 2.8], [0.9, 3.2])
    [1.5, 1.7]

.. versionadded:: 4.0.0
""",

    # difference_with
    "difference_with": """
This method is like :func:`difference` except that it accepts a
comparator which is invoked to compare the elements of all arrays. The
order and references of result values are determined by the first array.
The comparator is invoked with two arguments: ``(arr_val, oth_val)``.

Arity: 3

Args:
    comparator (callable): Function to compare the elements of
        the arrays. Defaults to :func:`.is_equal`.
    array (list): The array to find the difference of.
    others (list): Lists to check for difference with `array`.

Returns:
    list: Difference between `others`.
Example:

    >>> array = ['apple', 'banana', 'pear']
    >>> others = ['avocado', 'pumpkin'], ['peach']
    >>> comparator = lambda a, b: a[0] == b[0]
    >>> difference_with(comparator, array, *others)
    ['banana']

.. versionadded:: 4.0.0
""",

    # drop
    "drop": """
Creates a slice of `array` with `n` elements dropped from the beginning.

Arity: 2

Args:
    n (int): Number of elements to drop. Defaults to ``1``.
    array (list): List to process.

Returns:
    list: Dropped list.
Example:

    >>> drop(2, [1, 2, 3, 4])
    [3, 4]

.. versionadded:: 1.0.0

.. versionchanged:: 1.1.0
    Added ``n`` argument and removed as alias of :func:`rest`.

.. versionchanged:: 3.0.0
    Made ``n`` default to ``1``.
""",

    # drop_while
    "drop_while": """
Creates a slice of `array` excluding elements dropped from the
beginning. Elements are dropped until the `predicate` returns falsey. The
`predicate` is invoked with three arguments: ``(value, index, array)``.

Arity: 2

Args:
    predicate (mixed): Predicate called per iteration
    array (list): List to process.

Returns:
    list: Dropped list.
Example:

    >>> drop_while(lambda x: x < 3, [1, 2, 3, 4])
    [3, 4]

.. versionadded:: 1.1.0
""",

    # drop_right
    "drop_right": """
Creates a slice of `array` with `n` elements dropped from the end.

Arity: 2

Args:
    n (int): Number of elements to drop. Defaults to ``1``.
    array (list): List to process.

Returns:
    list: Dropped list.
Example:

    >>> drop_right(2, [1, 2, 3, 4])
    [1, 2]

.. versionadded:: 1.1.0

.. versionchanged:: 3.0.0
    Made ``n`` default to ``1``.
""",

    # drop_right_while
    "drop_right_while": """
Creates a slice of `array` excluding elements dropped from the end.
Elements are dropped until the `predicate` returns falsey. The `predicate`
is invoked with three arguments: ``(value, index, array)``.

Arity: 2

Args:
    predicate (mixed): Predicate called per iteration
    array (list): List to process.

Returns:
    list: Dropped list.
Example:

    >>> drop_right_while(lambda x: x >= 3, [1, 2, 3, 4])
    [1, 2]

.. versionadded:: 1.1.0
""",

    # duplicates
    "duplicates": """
Creates a unique list of duplicate values from `array`. If iteratee is
passed, each element of array is passed through a iteratee before
duplicates are computed. The iteratee is invoked with three arguments:
``(value, index, array)``. If an object path is passed for iteratee, the
created iteratee will return the path value of the given element. If an
object is passed for iteratee, the created filter style iteratee will
return ``True`` for elements that have the properties of the given object,
else ``False``.

Arity: 2

Args:
    iteratee (mixed): Iteratee applied per iteration.
    array (list): List to process.

Returns:
    list: List of duplicates.
Example:


.. versionadded:: 3.0.0
""",

    # fill
    "fill": """
Fills elements of array with value from `start` up to, but not
including, `end`.

Arity: 4

Args:
    start (int): Index to start filling. Defaults to ``0``.
    end (int): Index to end filling. Defaults to ``len(array)``.
    value (mixed): Value to fill with.
    array (list): List to fill.

Returns:
    list: Filled `array`.
Example:

    >>> fill(1, 3, 0, [1, 2, 3, 4, 5])
    [1, 0, 0, 4, 5]
    >>> fill(0, 100, 0, [1, 2, 3, 4, 5])
    [0, 0, 0, 0, 0]

.. versionadded:: 3.1.0
""",

    # find_index
    "find_index": """
This method is similar to :func:`pydash.collections.find`, except
that it returns the index of the element that passes the predicate check,
instead of the element itself.

Arity: 2

Args:
    predicate (mixed): Predicate applied per iteration.
    array (list): List to process.

Returns:
    int: Index of found item or ``-1`` if not found.
Example:

    >>> find_index(lambda x: x >= 3, [1, 2, 3, 4])
    2
    >>> find_index(lambda x: x > 4, [1, 2, 3, 4])
    -1

.. versionadded:: 1.0.0
""",

    # find_last_index
    "find_last_index": """
This method is similar to :func:`find_index`, except that it iterates
over elements from right to left.

Arity: 2

Args:
    predicate (mixed): Predicate applied per iteration.
    array (list): List to process.

Returns:
    int: Index of found item or ``-1`` if not found.
Example:

    >>> find_last_index(lambda x: x >= 3, [1, 2, 3, 4])
    3
    >>> find_index([1, 2, 3, 4], lambda x: x > 4)
    -1

.. versionadded:: 1.0.0
""",

    # flatten

    # flatten_deep

    # flatten_depth
    "flatten_depth": """
Recursively flatten `array` up to `depth` times.

Arity: 2

Args:
    depth (int): Depth to flatten to. Defaults to ``1``.
    array (list): List to flatten.

Returns:
    list: Flattened list.
Example:

    >>> flatten_depth(1, [[[1], [2, [3]], [[4]]]])
    [[1], [2, [3]], [[4]]]
    >>> flatten_depth(2, [[[1], [2, [3]], [[4]]]])
    [1, 2, [3], [4]]
    >>> flatten_depth(3, [[[1], [2, [3]], [[4]]]])
    [1, 2, 3, 4]
    >>> flatten_depth(4, [[[1], [2, [3]], [[4]]]])
    [1, 2, 3, 4]

.. versionadded:: 4.0.0
""",

    # from_pairs

    # head

    # index_of
    "index_of": """
Gets the index at which the first occurrence of value is found.

Arity: 2

Args:
    value (mixed): Value to search for.
    array (list): List to search.
    from_index (int, optional): Index to search from.

Returns:
    int: Index of found item or ``-1`` if not found.
Example:

    >>> index_of(2, [1, 2, 3, 4])
    1
    >>> index_of(2, [2, 1, 2, 3])
    2

.. versionadded:: 1.0.0
""",

    # initial

    # intercalate
    "intercalate": """
Like :func:`intersperse` for lists of lists but shallowly flattening the
result.

Arity: 2

Args:
    separator (mixed): Element to insert.
    array (list): List to intercalate.

Returns:
    list: Intercalated list.
Example:

    >>> intercalate('x', [1, [2], [3], 4])
    [1, 'x', 2, 'x', 3, 'x', 4]


.. versionadded:: 2.0.0
""",

    # interleave
    "interleave": """
Merge multiple lists into a single list by inserting the next element of
each list by sequential round-robin into the new list.

Arity: 2

Args:
    arrays (list): Lists to interleave.

Returns:
    list: Interleaved list.
Example:


.. versionadded:: 2.0.0
""",

    # intersection
    "intersection": """
Computes the intersection of all the passed-in arrays.

Arity: 2

Args:
    array (list): The array to find the intersection of.
    others (list): Lists to check for intersection with `array`.

Returns:
    list: Intersection of provided lists.
Example:

    >>> intersection([1, 2, 3], [1, 2, 3, 4, 5], [2, 3])
    [2, 3]


.. versionadded:: 1.0.0

.. versionchanged:: 4.0.0
    Support finding intersection of unhashable types.
""",

    # intersection_by
    "intersection_by": """
This method is like :func:`intersection` except that it accepts an
iteratee which is invoked for each element of each array to generate the
criterion by which they're compared. The order and references of result
values are determined by `array`. The iteratee is invoked with one
argument: ``(value)``.

Arity: 3

Args:
    iteratee (mixed): Function to transform the elements of the
        arrays. Defaults to :func:`.identity`.
    array (list): The array to find the intersection of.
    others (list): Lists to check for intersection with `array`.

Returns:
    list: Intersection of provided lists.
Example:

    >>> intersection_by(round, [1.2, 1.5, 1.7, 2.8], [0.9, 3.2])
    [1.2, 2.8]

.. versionadded:: 4.0.0
""",

    # intersection_with
    "intersection_with": """
This method is like :func:`intersection` except that it accepts a
comparator which is invoked to compare the elements of all arrays. The
order and references of result values are determined by the first array.
The comparator is invoked with two arguments: ``(arr_val, oth_val)``.

Arity: 3

Args:
    comparator (callable): Function to compare the elements of
        the arrays. Defaults to :func:`.is_equal`.
    array (list): The array to find the intersection of.
    others (list): Lists to check for intersection with `array`.

Returns:
    list: Intersection of provided lists.
Example:

    >>> array = ['apple', 'banana', 'pear']
    >>> others = ['avocado', 'pumpkin'], ['peach']
    >>> comparator = lambda a, b: a[0] == b[0]
    >>> intersection_with(comparator, array, *others)
    ['pear']

.. versionadded:: 4.0.0
""",

    # intersperse
    "intersperse": """
Insert a separating element between the elements of `array`.

Arity: 2

Args:
    separator (mixed): Element to insert.
    array (list): List to intersperse.

Returns:
    list: Interspersed list.
Example:

    >>> intersperse('x', [1, [2], [3], 4])
    [1, 'x', [2], 'x', [3], 'x', 4]

.. versionadded:: 2.0.0
""",

    # last

    # last_index_of
    "last_index_of": """
Gets the index at which the last occurrence of value is found.

Arity: 2

Args:
    value (mixed): Value to search for.
    array (list): List to search.
    from_index (int, optional): Index to search from.

Returns:
    int: Index of found item or ``False`` if not found.
Example:

    >>> last_index_of(2, [1, 2, 2, 4])
    2
    >>> last_index_of(2, [1, 2, 2, 4])
    1

.. versionadded:: 1.0.0
""",

    # mapcat
    "mapcat": """
Map a iteratee to each element of a list and concatenate the results
into a single list using :func:`cat`.

Arity: 2

Args:
    iteratee (mixed): Iteratee to apply to each element.
    array (list): List to map and concatenate.

Returns:
    list: Mapped and concatenated list.
Example:

    >>> mapcat(lambda x: list(range(x)), range(4))
    [0, 0, 1, 0, 1, 2]

.. versionadded:: 2.0.0
""",

    # nth
    "nth": """
Gets the element at index n of array.

Arity: 2

Args:
    pos (int): Index of element to return.
    array (list): List passed in by the user.

Returns:
    mixed: Returns the element at :attr:`pos`.
Example:

    >>> nth(0, [1, 2, 3])
    1
    >>> nth(2, [3, 4, 5, 6])
    5
    >>> nth(-1, [11, 22, 33])
    33

.. versionadded:: 4.0.0
""",

    # pull
    "pull": """
Removes all provided values from the given array.

Arity: 2

Args:
    values (mixed): Values to remove.
    array (list): List to pull from.

Returns:
    list: Resulting `array`.
Note:
    The fp variant of pull takes
    exactly 2 arguments

Example:

    >>> pull(2, [1, 2, 2, 3, 3, 4])
    [1, 4]

.. versionadded:: 1.0.0

.. versionchanged:: 4.0.0
    :func:`pull` method now calls :func:`pull_all` method for the desired
    functionality.
""",

    # pull_all
    "pull_all": """
Removes all provided values from the given array.

Arity: 2

Args:
    values (list): Values to remove.
    array (list): Array to modify.

Returns:
    list: Resulting `array`.
Example:

    >>> pull_all([2, 3], [1, 2, 2, 3, 3, 4])
    [1, 4]

.. versionadded:: 4.0.0
""",

    # pull_all_by
    "pull_all_by": """
This method is like :func:`pull_all` except that it accepts iteratee
which is invoked for each element of array and values to generate the
criterion by which they're compared. The iteratee is invoked with one
argument: ``(value)``.

Arity: 3

Args:
    iteratee (mixed): Function to transform the elements of the
        arrays. Defaults to :func:`.identity`.
    values (list): Values to remove.
    array (list): Array to modify.

Returns:
    list: Resulting `array`.
Example:

    >>> array = [{'x': 1}, {'x': 2}, {'x': 3}, {'x': 1}]
    >>> pull_all_by('x', [{'x': 1}, {'x': 3}], array)
    [{'x': 2}]

.. versionadded:: 4.0.0
""",

    # pull_all_with
    "pull_all_with": """
This method is like :func:`pull_all` except that it accepts comparator
which is invoked to compare elements of array to values. The comparator is
invoked with two arguments: ``(arr_val, oth_val)``.

Arity: 3

Args:
    comparator (callable): Function to compare the elements of
        the arrays. Defaults to :func:`.is_equal`.
    values (list): Values to remove.
    array (list): Array to modify.

Returns:
    list: Resulting `array`.
Example:

    >>> array = [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}, {'x': 5, 'y': 6}]
    >>> res = pull_all_with(lambda a, b: a == b, [{'x': 3, 'y': 4}], array)
    >>> res == [{'x': 1, 'y': 2}, {'x': 5, 'y': 6}]
    True
    >>> array = [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}, {'x': 5, 'y': 6}]
    >>> res = pull_all_with(lambda a, b: a != b, [{'x': 3, 'y': 4}], array)
    >>> res == [{'x': 3, 'y': 4}]
    True

.. versionadded:: 4.0.0
""",

    # pull_at
    "pull_at": """
Removes elements from `array` corresponding to the specified indexes and
returns a list of the removed elements. Indexes may be specified as a list
of indexes or as individual arguments.

Arity: 2

Args:
    indexes (int): Indexes to pull.
    array (list): List to pull from.

Returns:
    list: Resulting `array`.
Note:
    The fp variant of pull_at takes
    exactly 2 arguments

Example:

    >>> pull_at(0, [1, 2, 3, 4])
    [2, 4]

.. versionadded:: 1.1.0
""",

    # remove
    "remove": """
Removes all elements from a list that the predicate returns truthy for
and returns an array of removed elements.

Arity: 2

Args:
    predicate (mixed): Predicate applied per iteration.
    array (list): List to remove elements from.

Returns:
    list: Removed elements of `array`.
Example:

    >>> array = [1, 2, 3, 4]
    >>> items = remove(lambda x: x >= 3, array)
    >>> items
    [3, 4]
    >>> array
    [1, 2]

.. versionadded:: 1.0.0
""",

    # repack
    "repack": """
Repacks an iterable for destructuring assignment
to provide extended iterable unpacking functionality in python 2.7

Arity: 2

Args:
    lhs (str): desired assignment structure, would be valid lhs in python 3
    *items: items to repack for assignment

Returns:
    tuple: items structured for assigment
Example:

""",

    # reverse

    # slice_
    "slice_": """
Slices `array` from the `start` index up to, but not including, the
`end` index.

Arity: 3

Args:
    start (int): Start index. Defaults to ``0``.
    end (int): End index. Defaults to selecting the value at
        ``start`` index.
    array (list): Array to slice.

Returns:
    list: Sliced list.
Example:

    >>> slice_(1, 3, [1, 2, 3, 4])
    [2, 3]

.. versionadded:: 1.1.0
""",

    # sorted_index
    "sorted_index": """
Uses a binary search to determine the lowest index at which `value`
should be inserted into `array` in order to maintain its sort order.

Arity: 2

Args:
    value (mixed): Value to evaluate.
    array (list): List to inspect.

Returns:
    int: Returns the index at which `value` should be inserted into        `array`.
Example:

    >>> sorted_index(2, [1, 2, 2, 3, 4])
    1

.. versionadded:: 1.0.0

.. versionchanged:: 4.0.0
    Move iteratee support to :func:`sorted_index_by`.
""",

    # sorted_index_by
    "sorted_index_by": """
This method is like :func:`sorted_index` except that it accepts
iteratee which is invoked for `value` and each element of `array` to
compute their sort ranking. The iteratee is invoked with one argument:
``(value)``.

Arity: 3

Args:
    value (mixed): Value to evaluate.
    iteratee (mixed): The iteratee invoked per element. Defaults
        to :func:`.identity`.
    array (list): List to inspect.

Returns:
    int: Returns the index at which `value` should be inserted into        `array`.
Example:

    >>> array = [{'x': 4}, {'x': 5}]
    >>> sorted_index_by({'x': 4}, lambda o: o['x'], array)
    0
    >>> sorted_index_by({'x': 4}, 'x', array)
    0

.. versionadded:: 4.0.0
""",

    # sorted_index_of
    "sorted_index_of": """
Returns the index of the matched `value` from the sorted `array`, else
``-1``.

Arity: 2

Args:
    value (mixed): Value to search for.
    array (list): Array to inspect.

Returns:
    int: Returns the index of the first matched value, else ``-1``.
Example:

    >>> sorted_index_of(3, [3, 5, 7, 10])
    0
    >>> sorted_index_of(10, [10, 10, 5, 7, 3])
    -1

.. versionadded:: 4.0.0
""",

    # sorted_last_index
    "sorted_last_index": """
This method is like :func:`sorted_index` except that it returns the
highest index at which `value` should be inserted into `array` in order to
maintain its sort order.

Arity: 2

Args:
    value (mixed): Value to evaluate.
    array (list): List to inspect.

Returns:
    int: Returns the index at which `value` should be inserted into        `array`.
Example:

    >>> sorted_last_index(2, [1, 2, 2, 3, 4])
    3

.. versionadded:: 1.1.0

.. versionchanged:: 4.0.0
    Move iteratee support to :func:`sorted_last_index_by`.
""",

    # sorted_last_index_by
    "sorted_last_index_by": """
This method is like :func:`sorted_last_index` except that it accepts
iteratee which is invoked for `value` and each element of `array` to
compute their sort ranking. The iteratee is invoked with one argument:
``(value)``.

Arity: 3

Args:
    value (mixed): Value to evaluate.
    iteratee (mixed): The iteratee invoked per element. Defaults
        to :func:`.identity`.
    array (list): List to inspect.

Returns:
    int: Returns the index at which `value` should be inserted into        `array`.
Example:

    >>> array = [{'x': 4}, {'x': 5}]
    >>> sorted_last_index_by({'x': 4}, lambda o: o['x'], array)
    1
    >>> sorted_last_index_by({'x': 4}, 'x', array)
    1
""",

    # sorted_last_index_of
    "sorted_last_index_of": """
This method is like :func:`last_index_of` except that it performs a
binary search on a sorted `array`.

Arity: 2

Args:
    value (mixed): Value to search for.
    array (list): Array to inspect.

Returns:
    int: Returns the index of the matched value, else ``-1``.
Example:

    >>> sorted_last_index_of(5, [4, 5, 5, 5, 6])
    3
    >>> sorted_last_index_of(6, [6, 5, 5, 5, 4])
    -1

.. versionadded:: 4.0.0
""",

    # sorted_uniq

    # sorted_uniq_by
    "sorted_uniq_by": """
This method is like :func:`sorted_uniq` except that it accepts iteratee
which is invoked for each element in array to generate the criterion by
which uniqueness is computed. The order of result values is determined by
the order they occur in the array. The iteratee is invoked with one
argument: ``(value)``.

Arity: 2

Args:
    iteratee (mixed): Function to transform the elements of the
        arrays. Defaults to :func:`.identity`.
    array (list): List of values to be sorted.

Returns:
    list: Unique list.
Example:

    >>> sorted_uniq_by(lambda val: val % 2, [3, 2, 1, 3, 2, 1])
    [2, 3]

.. versionadded:: 4.0.0
""",

    # split_at
    "split_at": """
Returns a list of two lists composed of the split of `array` at `index`.

Arity: 2

Args:
    index (int): Index to split at.
    array (list): List to split.

Returns:
    list: Split list.
Example:

    >>> split_at(2, [1, 2, 3, 4])
    [[1, 2], [3, 4]]

.. versionadded:: 2.0.0
""",

    # tail

    # take
    "take": """
Creates a slice of `array` with `n` elements taken from the beginning.

Arity: 2

Args:
    n (int): Number of elements to take. Defaults to ``1``.
    array (list): List to process.

Returns:
    list: Taken list.
Example:

    >>> take(2, [1, 2, 3, 4])
    [1, 2]

.. versionadded:: 1.0.0

.. versionchanged:: 1.1.0
    Added ``n`` argument and removed as alias of :func:`first`.

.. versionchanged:: 3.0.0
    Made ``n`` default to ``1``.
""",

    # take_right
    "take_right": """
Creates a slice of `array` with `n` elements taken from the end.

Arity: 2

Args:
    n (int): Number of elements to take. Defaults to ``1``.
    array (list): List to process.

Returns:
    list: Taken list.
Example:

    >>> take_right(2, [1, 2, 3, 4])
    [3, 4]

.. versionadded:: 1.1.0

.. versionchanged:: 3.0.0
    Made ``n`` default to ``1``.
""",

    # take_right_while
    "take_right_while": """
Creates a slice of `array` with elements taken from the end. Elements
are taken until the `predicate` returns falsey. The `predicate` is
invoked with three arguments: ``(value, index, array)``.

Arity: 2

Args:
    predicate (mixed): Predicate called per iteration
    array (list): List to process.

Returns:
    list: Dropped list.
Example:

    >>> take_right_while(lambda x: x >= 3, [1, 2, 3, 4])
    [3, 4]

.. versionadded:: 1.1.0
""",

    # take_while
    "take_while": """
Creates a slice of `array` with elements taken from the beginning.
Elements are taken until the `predicate` returns falsey. The
`predicate` is invoked with three arguments: ``(value, index, array)``.

Arity: 2

Args:
    predicate (mixed): Predicate called per iteration
    array (list): List to process.

Returns:
    list: Taken list.
Example:

    >>> take_while(lambda x: x < 3, [1, 2, 3, 4])
    [1, 2]

.. versionadded:: 1.1.0
""",

    # union
    "union": """
Computes the union of the passed-in arrays.

Arity: 2

Args:
    array (list): List to union with.
    others (list): Lists to unionize with `array`.

Returns:
    list: Unionized list.
Example:

    >>> union([1, 2, 3], [2, 3, 4], [3, 4, 5])
    [1, 2, 3, 4, 5]

.. versionadded:: 1.0.0
""",

    # union_by
    "union_by": """
This method is similar to :func:`union` except that it accepts iteratee
which is invoked for each element of each arrays to generate the criterion
by which uniqueness is computed.

Arity: 3

Args:
    iteratee (function): Function to invoke on each element.
    array (list): List to unionize with.
    others (list): Lists to unionize with `array`.

Returns:
    list: Unionized list.
Example:

    >>> union_by(lambda x: x % 2, [1, 2, 3], [2, 3, 4])
    [1, 2]
    >>> union_by(lambda x: x % 9, [1, 2, 3], [2, 3, 4])
    [1, 2, 3, 4]

.. versionadded:: 4.0.0
""",

    # union_with
    "union_with": """
This method is like :func:`union` except that it accepts comparator
which is invoked to compare elements of arrays. Result values are chosen
from the first array in which the value occurs.

Arity: 3

Args:
    comparator (callable): Function to compare the elements of
        the arrays. Defaults to :func:`.is_equal`.
    array (list): List to unionize with.
    others (list): Lists to unionize with `array`.

Returns:
    list: Unionized list.
Example:

    >>> comparator = lambda a, b: a % 2 == b % 2
    >>> union_with(comparator, [1, 2, 3], [2, 3, 4])
    [1, 2]

.. versionadded:: 4.0.0
""",

    # uniq

    # uniq_by
    "uniq_by": """
This method is like :func:`uniq` except that it accepts iteratee which
is invoked for each element in array to generate the criterion by which
uniqueness is computed. The order of result values is determined by the
order they occur in the array. The iteratee is invoked with one argument:
``(value)``.

Arity: 2

Args:
    iteratee (mixed): Function to transform the elements of the
        arrays. Defaults to :func:`.identity`.
    array (list): List to process.

Returns:
    list: Unique list.
Example:

    >>> uniq_by(lambda val: val % 2, [1, 2, 3, 1, 2, 3])
    [1, 2]

.. versionadded:: 4.0.0
""",

    # uniq_with
    "uniq_with": """
This method is like _.uniq except that it accepts comparator which is
invoked to compare elements of array. The order of result values is
determined by the order they occur in the array.The comparator is invoked
with two arguments: ``(value, other)``.

Arity: 2

Args:
    comparator (callable): Function to compare the elements of
        the arrays. Defaults to :func:`.is_equal`.
    array (list): List to process.

Returns:
    list: Unique list.
Example:

    >>> uniq_with(lambda a, b: a % 2 == b % 2, [1, 2, 3, 4, 5])
    [1, 2]

.. versionadded:: 4.0.0
""",

    # unzip

    # unzip_with
    "unzip_with": """
This method is like :func:`unzip` except that it accepts a iteratee to
specify how regrouped values should be combined. The iteratee is invoked
with four arguments: ``(accumulator, value, index, group)``.

Arity: 2

Args:
    iteratee (callable): Function to combine regrouped values.
    array (list): List to process.

Returns:
    list: Unzipped list.
Example:

    >>> from pydash import add
    >>> unzip_with(add, [[1, 10, 100], [2, 20, 200]])
    [3, 30, 300]

.. versionadded:: 3.3.0
""",

    # without
    "without": """
Creates an array with all occurrences of the passed values removed.

Arity: 2

Args:
    values (mixed): Values to remove.
    array (list): List to filter.

Returns:
    list: Filtered list.
Note:
    The fp variant of without takes
    exactly 2 arguments

Example:

    >>> without(2, [1, 2, 3, 2, 4, 4])
    [1, 3]

.. versionadded:: 1.0.0
""",

    # xor
    "xor": """
Creates a list that is the symmetric difference of the provided lists.

Arity: 2

Args:
    array (list): List to process.
    *lists (list): Lists to xor with.

Returns:
    list: XOR'd list.
Example:

    >>> xor([1, 3, 4], [1, 2, 4], [2])
    [3]

.. versionadded:: 1.0.0
""",

    # xor_by
    "xor_by": """
This method is like :func:`xor` except that it accepts iteratee which is
invoked for each element of each arrays to generate the criterion by which
by which they're compared. The order of result values is determined by the
order they occur in the arrays. The iteratee is invoked with one argument:
``(value)``.

Arity: 3

Args:
    iteratee (mixed): Function to transform the elements of the
        arrays. Defaults to :func:`.identity`.
    array (list): List to process.
    *lists (list): Lists to xor with.

Returns:
    list: XOR'd list.
Example:

    >>> xor_by(round, [2.1, 1.2], [2.3, 3.4])
    [1.2, 3.4]
    >>> xor_by('x', [{'x': 1}], [{'x': 2}, {'x': 1}])
    [{'x': 2}]

.. versionadded:: 4.0.0
""",

    # xor_with
    "xor_with": """
This method is like :func:`xor` except that it accepts comparator which
is invoked to compare elements of arrays. The order of result values is
determined by the order they occur in the arrays. The comparator is invoked
with two arguments: ``(arr_val, oth_val)``.

Arity: 3

Args:
    comparator (callable): Function to compare the elements of
        the arrays. Defaults to :func:`.is_equal`.
    array (list): List to process.
    *lists (list): Lists to xor with.

Returns:
    list: XOR'd list.
Example:

    >>> objects = [{'x': 1, 'y': 2}, {'x': 2, 'y': 1}]
    >>> others = [{'x': 1, 'y': 1}, {'x': 1, 'y': 2}]
    >>> expected = [{'y': 1, 'x': 2}, {'y': 1, 'x': 1}]
    >>> xor_with(lambda a, b: a == b, objects, others) == expected
    True

.. versionadded:: 4.0.0
""",

    # zip_
    "zip_": """
Groups the elements of each array at their corresponding indexes.
Useful for separate data sources that are coordinated through matching
array indexes.

Arity: 2

Args:
    arrays (list): Lists to process.

Returns:
    list: Zipped list.
Example:


.. versionadded:: 1.0.0
""",

    # zip_object
    "zip_object": """
Creates a dict composed from lists of keys and values. Pass either a
single two dimensional list, i.e. ``[[key1, value1], [key2, value2]]``, or
two lists, one of keys and one of corresponding values.

Arity: 2

Args:
    keys (list): Either a list of keys or a list of ``[key, value]`` pairs.
    values (list): List of values to zip.

Returns:
    dict: Zipped dict.
Example:

    >>> zip_object([1, 2, 3], [4, 5, 6])
    {1: 4, 2: 5, 3: 6}

.. versionadded:: 1.0.0

.. versionchanged:: 4.0.0
    Removed alias ``object_``.
""",

    # zip_object_deep
    "zip_object_deep": """
This method is like :func:`zip_object` except that it supports property
paths.

Arity: 2

Args:
    keys (list): Either a list of keys or a list of ``[key, value]`` pairs.
    values (list): List of values to zip.

Returns:
    dict: Zipped dict.
Example:

    >>> expected = {'a': {'b': {'c': 1, 'd': 2}}}
    >>> zip_object_deep(['a.b.c', 'a.b.d'], [1, 2]) == expected
    True

.. versionadded:: 4.0.0
""",

    # zip_with
    "zip_with": """
This method is like :func:`zip` except that it accepts a iteratee to
specify how grouped values should be combined. The iteratee is invoked with
four arguments: ``(accumulator, value, index, group)``.

Arity: 3

Args:
    *arrays (list): Lists to process.
    iteratee (function): Function to combine grouped values.

Returns:
    list: Zipped list of grouped elements.
Example:

    >>> from pydash import add

.. versionadded:: 3.3.0
""",
}


def _convert(order, func, **kwargs):
    fp_func = convert(order, func, **kwargs)
    fp_func.__doc__ = docstrings.get(func.__name__, func.__doc__)
    return fp_func


chunk = _convert([1, 0], pyd.chunk)
compact = pyd.compact
concat = _convert([0, 1], pyd.concat)
difference = _convert([0, 1], pyd.difference)
difference_by = _convert([1, 2, 0], pyd.difference_by)
difference_with = _convert([1, 2, 0], pyd.difference_with)
drop = _convert([1, 0], pyd.drop)
drop_while = _convert([1, 0], pyd.drop_while)
drop_right = _convert([1, 0], pyd.drop_right)
drop_right_while = _convert([1, 0], pyd.drop_right_while)
duplicates = _convert([1, 0], pyd.duplicates)
fill = _convert([3, 2, 0, 1], pyd.fill)
find_index = _convert([1, 0], pyd.find_index)
find_last_index = _convert([1, 0], pyd.find_last_index)
flatten = pyd.flatten
flatten_deep = pyd.flatten_deep
flatten_depth = _convert([1, 0], pyd.flatten_depth)
from_pairs = pyd.from_pairs
head = pyd.head
index_of = _convert([1, 0], pyd.index_of, **{'interpose': False})
initial = pyd.initial
intercalate = _convert([1, 0], pyd.intercalate)
interleave = _convert([0, 1], pyd.interleave)
intersection = _convert([0, 1], pyd.intersection)
intersection_by = _convert([1, 2, 0], pyd.intersection_by)
intersection_with = _convert([1, 2, 0], pyd.intersection_with)
intersperse = _convert([1, 0], pyd.intersperse)
last = pyd.last
last_index_of = _convert([1, 0], pyd.last_index_of, **{'interpose': False})
mapcat = _convert([1, 0], pyd.mapcat)
nth = _convert([1, 0], pyd.nth)
pull = _convert([1, 0], pyd.pull, **{'cap': True})
pull_all = _convert([1, 0], pyd.pull_all)
pull_all_by = _convert([2, 1, 0], pyd.pull_all_by)
pull_all_with = _convert([2, 1, 0], pyd.pull_all_with)
pull_at = _convert([1, 0], pyd.pull_at, **{'cap': True})
remove = _convert([1, 0], pyd.remove)
repack = _convert([0, 1], pyd.repack)
reverse = pyd.reverse
slice_ = _convert([2, 0, 1], pyd.slice_)
sorted_index = _convert([1, 0], pyd.sorted_index)
sorted_index_by = _convert([2, 0, 1], pyd.sorted_index_by)
sorted_index_of = _convert([1, 0], pyd.sorted_index_of)
sorted_last_index = _convert([1, 0], pyd.sorted_last_index)
sorted_last_index_by = _convert([2, 0, 1], pyd.sorted_last_index_by)
sorted_last_index_of = _convert([1, 0], pyd.sorted_last_index_of)
sorted_uniq = pyd.sorted_uniq
sorted_uniq_by = _convert([1, 0], pyd.sorted_uniq_by)
split_at = _convert([1, 0], pyd.split_at)
tail = pyd.tail
take = _convert([1, 0], pyd.take)
take_right = _convert([1, 0], pyd.take_right)
take_right_while = _convert([1, 0], pyd.take_right_while)
take_while = _convert([1, 0], pyd.take_while)
union = _convert([0, 1], pyd.union)
union_by = _convert([1, 2, 0], pyd.union_by)
union_with = _convert([1, 2, 0], pyd.union_with)
uniq = pyd.uniq
uniq_by = _convert([1, 0], pyd.uniq_by)
uniq_with = _convert([1, 0], pyd.uniq_with)
unzip = pyd.unzip
unzip_with = _convert([1, 0], pyd.unzip_with)
without = _convert([1, 0], pyd.without, **{'cap': True})
xor = _convert([0, 1], pyd.xor)
xor_by = _convert([1, 2, 0], pyd.xor_by)
xor_with = _convert([1, 2, 0], pyd.xor_with)
zip_ = _convert([0, 1], pyd.zip_)
zip_object = _convert([0, 1], pyd.zip_object)
zip_object_deep = _convert([0, 1], pyd.zip_object_deep)
zip_with = _convert([1, 2, 0], pyd.zip_with)
