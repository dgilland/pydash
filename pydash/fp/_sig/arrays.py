"conversion signatures for fp.arrays"


signatures = [
    ("chunk", "chunk", [1, 0]),
    ("compact", "compact",),
    ("concat", "concat", [0, 1]),
    ("difference", "difference", [0, 1]),
    ("difference_by", "difference_by", [1, 2, 0]),
    ("difference_with", "difference_with", [1, 2, 0]),
    ("drop", "drop", [1, 0]),
    ("drop_while", "drop_while", [1, 0]),
    ("drop_right", "drop_right", [1, 0]),
    ("drop_right_while", "drop_right_while", [1, 0]),
    ("duplicates", "duplicates", [0]),
    ("duplicates_by", "duplicates", [1, 0]),
    ("fill", "fill", [3, 2, 0, 1]),
    ("find_index", "find_index", [1, 0]),
    ("find_last_index", "find_last_index", [1, 0]),
    ("flatten", "flatten",),
    ("flatten_deep", "flatten_deep",),
    ("flatten_depth", "flatten_depth", [1, 0]),
    ("from_pairs", "from_pairs",),
    ("head", "head",),
    ("index_of", "index_of", [1, 0], {"cap": True}),
    ("initial", "initial",),
    ("intercalate", "intercalate", [1, 0]),
    ("interleave", "interleave", [0, 1]),
    ("intersection", "intersection", [0, 1]),
    ("intersection_by", "intersection_by", [1, 2, 0]),
    ("intersection_with", "intersection_with", [1, 2, 0]),
    ("intersperse", "intersperse", [1, 0]),
    ("last", "last",),
    ("last_index_of", "last_index_of", [1, 0], {"cap": True}),
    ("mapcat", "mapcat", [1, 0]),
    ("nth", "nth", [1, 0]),
    ("pull", "pull", [1, 0], {"cap": True}),
    ("pull_all", "pull_all", [1, 0]),
    ("pull_all_by", "pull_all_by", [2, 1, 0]),
    ("pull_all_with", "pull_all_with", [2, 1, 0]),
    ("pull_at", "pull_at", [1, 0], {"cap": True}),
    ("repack", "repack", [0, 1]),
    ("reverse", "reverse",),
    ("slice_", "slice_", [2, 0, 1]),
    ("sorted_index", "sorted_index", [1, 0]),
    ("sorted_index_by", "sorted_index_by", [2, 0, 1]),
    ("sorted_index_of", "sorted_index_of", [1, 0]),
    ("sorted_last_index", "sorted_last_index", [1, 0]),
    ("sorted_last_index_by", "sorted_last_index_by", [2, 0, 1]),
    ("sorted_last_index_of", "sorted_last_index_of", [1, 0]),
    ("sorted_uniq", "sorted_uniq",),
    ("sorted_uniq_by", "sorted_uniq_by", [1, 0]),
    ("split_at", "split_at", [1, 0]),
    ("tail", "tail",),
    ("take", "take", [1, 0]),
    ("take_right", "take_right", [1, 0]),
    ("take_right_while", "take_right_while", [1, 0]),
    ("take_while", "take_while", [1, 0]),
    ("union", "union", [0, 1]),
    ("union_by", "union_by", [1, 2, 0]),
    ("union_with", "union_with", [1, 2, 0]),
    ("uniq", "uniq",),
    ("uniq_by", "uniq_by", [1, 0]),
    ("uniq_with", "uniq_with", [1, 0]),
    ("unzip", "unzip",),
    ("unzip_with", "unzip_with", [1, 0]),
    ("without", "without", [1, 0], {"cap": True}),
    ("xor", "xor", [0, 1]),
    ("xor_by", "xor_by", [1, 2, 0]),
    ("xor_with", "xor_with", [1, 2, 0]),
    ("zip_", "zip_", [0, 1]),
    ("zip_object", "zip_object", [0, 1]),
    ("zip_object_deep", "zip_object_deep", [0, 1]),
    ("zip_with", "zip_with", [1, 2, 0]),
]


docstr_overrides = {
    "duplicates": """
    Creates a unique list of duplicate values from `array`.

    Arity: 1

    Args:
        array (list): List to process.

    Returns:
        list: List of duplicates.

    Example:

        >>> duplicates([0, 1, 3, 2, 3, 1])
        [3, 1]

    .. versionadded:: 3.0.0
    """,
    "duplicates_by": """
    Creates a unique list of duplicate values from `array`.
    Each element of array is passed through `iteratee` before
    duplicates are computed. The iteratee is invoked with three arguments:
    ``(value, index, array)``. If an object path is passed for iteratee, the
    created iteratee will return the path value of the given element. If an
    object is passed for iteratee, the created filter style iteratee will
    return ``True`` for elements that have the properties of the given object,
    else ``False``.

    Args:
        iteratee (mixed, optional): Iteratee applied per iteration.
        array (list): List to process.

    Returns:
        list: List of duplicates.

    Example:

        >>> duplicates_by(lambda v: v // 2, [0,1,2,3,4,6,8,9])
        [1, 3, 9]

    .. versionadded:: 3.0.0
    """,
    "pull": """
    Creates a copy of `array` with all occurrences of specified value
    removed.

    Arity: 2

    Args:
        value (mixed): Value to remove.
        array (list): List to pull from.

    Returns:
        list: Filtered list.

    Note:
        The fp variant of pull takes
        exactly 2 arguments

    Example:

        >>> pull(2, [1, 2, 2, 3, 3, 4])
        [1, 3, 3, 4]

    .. versionadded:: 1.0.0

    .. versionchanged:: 4.0.0
        :func:`pull` method now calls :func:`pull_all` method for the desired
        functionality.
    """,
    "pull_at": """
    Creates a copy of `array` with elements corresponding to the specified
    indexes removed.  Indexes may be specified as a list.

    Arity: 2

    Args:
        indexes (int): Indexes to pull.
        array (list): List to pull from.

    Returns:
        list: Filtered list.

    Note:
        The fp variant of pull_at takes
        exactly 2 arguments

    Example:

        >>> pull_at([0, 2], [1, 2, 3, 4])
        [2, 4]

        >>> pull_at(2, [1, 2, 3, 4])
        [1, 2, 4]


    .. versionadded:: 1.1.0
    """,
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
        [1, 3, 4, 4]

    .. versionadded:: 1.0.0
    """,
    "zip_with": """
    This method is like :func:`zip` except that it accepts a iteratee to
    specify how grouped values should be combined. The iteratee is invoked with
    four arguments: ``(accumulator, value, index, group)``.

    Arity: 3

    Args:
        iteratee (function): Function to combine grouped values.
        *arrays (list): Lists to process.

    Returns:
        list: Zipped list of grouped elements.

    Example:

        >>> from pydash import add
        >>> zip_with(add, [1, 2], [10, 20], [100, 200])
        [111, 222]

    .. versionadded:: 3.3.0
    """
}
