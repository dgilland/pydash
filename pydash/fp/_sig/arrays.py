"conversion signatures for fp.arrays"


signatures = [
    ("chunk", [1, 0]),
    ("compact",),
    ("concat", [0, 1]),
    ("difference", [0, 1]),
    ("difference_by", [1, 2, 0]),
    ("difference_with", [1, 2, 0]),
    ("drop", [1, 0]),
    ("drop_while", [1, 0]),
    ("drop_right", [1, 0]),
    ("drop_right_while", [1, 0]),
    ("duplicates", [0]),
    ("fill", [3, 2, 0, 1]),
    ("find_index", [1, 0]),
    ("find_last_index", [1, 0]),
    ("flatten",),
    ("flatten_deep",),
    ("flatten_depth", [1, 0]),
    ("from_pairs",),
    ("head",),
    ("index_of", [1, 0], {"cap": True}),
    ("initial",),
    ("intercalate", [1, 0]),
    ("interleave", [0, 1]),
    ("intersection", [0, 1]),
    ("intersection_by", [1, 2, 0]),
    ("intersection_with", [1, 2, 0]),
    ("intersperse", [1, 0]),
    ("last",),
    ("last_index_of", [1, 0], {"cap": True}),
    ("mapcat", [1, 0]),
    ("nth", [1, 0]),
    ("pull", [1, 0], {"cap": True}),
    ("pull_all", [1, 0]),
    ("pull_all_by", [2, 1, 0]),
    ("pull_all_with", [2, 1, 0]),
    ("pull_at", [1, 0], {"cap": True}),
    ("remove", [1, 0]),
    ("repack", [0, 1]),
    ("reverse",),
    ("slice_", [2, 0, 1]),
    ("sorted_index", [1, 0]),
    ("sorted_index_by", [2, 0, 1]),
    ("sorted_index_of", [1, 0]),
    ("sorted_last_index", [1, 0]),
    ("sorted_last_index_by", [2, 0, 1]),
    ("sorted_last_index_of", [1, 0]),
    ("sorted_uniq",),
    ("sorted_uniq_by", [1, 0]),
    ("split_at", [1, 0]),
    ("tail",),
    ("take", [1, 0]),
    ("take_right", [1, 0]),
    ("take_right_while", [1, 0]),
    ("take_while", [1, 0]),
    ("union", [0, 1]),
    ("union_by", [1, 2, 0]),
    ("union_with", [1, 2, 0]),
    ("uniq",),
    ("uniq_by", [1, 0]),
    ("uniq_with", [1, 0]),
    ("unzip",),
    ("unzip_with", [1, 0]),
    ("without", [1, 0], {"cap": True}),
    ("xor", [0, 1]),
    ("xor_by", [1, 2, 0]),
    ("xor_with", [1, 2, 0]),
    ("zip_", [0, 1]),
    ("zip_object", [0, 1]),
    ("zip_object_deep", [0, 1]),
    ("zip_with", [1, 2, 0]),
]


docstr_overrides = {
    "duplicates": """
    Creates a unique list of duplicate values from `array`.

    Arity: 1

    Args:
        array (list): List to process.
        iteratee (mixed, optional): Iteratee applied per iteration.

    Returns:
        list: List of duplicates.

    Example:

        >>> duplicates([0, 1, 3, 2, 3, 1])
        [3, 1]

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
        list: Resulting `array`.

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
    Creates a copy of `array` with elements corresponding to the specified indexes 
    removed.  Indexes may be specified as a list.

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
