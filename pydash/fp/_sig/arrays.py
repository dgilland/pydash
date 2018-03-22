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
}
