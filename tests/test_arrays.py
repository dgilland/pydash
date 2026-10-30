from bisect import bisect_left, bisect_right
import math
import typing as t

import pytest

import pydash as _


parametrize = pytest.mark.parametrize


class NoTruthList(list[t.Any]):
    def __bool__(self):
        raise ValueError("The truth value of an array is ambiguous")


class FalseList(list[t.Any]):
    def __bool__(self):
        return False


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5],), [[1], [2], [3], [4], [5]]),
        (([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]),
        (([1, 2, 3, 4, 5], 3), [[1, 2, 3], [4, 5]]),
        (([1, 2, 3, 4, 5], 4), [[1, 2, 3, 4], [5]]),
        (([1, 2, 3, 4, 5], 5), [[1, 2, 3, 4, 5]]),
        (([1, 2, 3, 4, 5], 6), [[1, 2, 3, 4, 5]]),
        (([1, 2, 3, 4, 5], 0), []),
        (([1, 2, 3], -1), []),
        (([], 0), []),
    ],
)
def test_chunk(case, expected):
    assert _.chunk(*case) == expected


@parametrize(
    "case,expected",
    [([0, 1, 2, 3], [1, 2, 3]), ([True, False, None, True, 1, "foo"], [True, True, 1, "foo"])],
)
def test_compact(case, expected):
    assert _.compact(case) == expected


@parametrize(
    "case,expected",
    [
        ((), []),
        (([],), []),
        (([1, 2, 3],), [1, 2, 3]),
        (([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6]),
        (([1, 2, 3], [4, 5, 6], [7]), [1, 2, 3, 4, 5, 6, 7]),
        ((1, [2], 3, 4), [1, 2, 3, 4]),
    ],
)
def test_concat(case, expected):
    assert _.concat(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4],), [1, 2, 3, 4]),
        (([1, 2, 3, 4], []), [1, 2, 3, 4]),
        (([1, 2, 3, 4], [2, 4], [3, 5, 6]), [1]),
        (([1, 1, 1, 1], [2, 4], [3, 5, 6]), [1, 1, 1, 1]),
    ],
)
def test_difference(case, expected):
    assert _.difference(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4],), [1, 2, 3, 4]),
        (([1, 2, 3, 4], []), [1, 2, 3, 4]),
        (([{"a": 1}, {"a": 2, "b": 2}], [{"a": 1}], "a"), [{"a": 2, "b": 2}]),
    ],
)
def test_difference_by(case, expected):
    assert _.difference_by(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4],), [1, 2, 3, 4]),
        (([1, 2, 3, 4], []), [1, 2, 3, 4]),
        (
            ([{"a": 1}, {"a": 2, "b": 2}], [{"a": 1}], lambda item, other: item["a"] == other["a"]),
            [{"a": 2, "b": 2}],
        ),
    ],
)
def test_difference_with(case, expected):
    assert _.difference_with(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5],), [2, 3, 4, 5]),
        (([1, 2, 3, 4, 5], 1), [2, 3, 4, 5]),
        (([1, 2, 3, 4, 5], 2), [3, 4, 5]),
        (([1, 2, 3, 4, 5], 5), []),
        (([1, 2, 3, 4, 5], 6), []),
    ],
)
def test_drop(case, expected):
    assert _.drop(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5], lambda item: item < 3), [3, 4, 5]),
        ((iter([1, 2, 3, 4, 5]), lambda item: item < 3), [3, 4, 5]),
    ],
)
def test_drop_while(case, expected):
    assert _.drop_while(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5],), [1, 2, 3, 4]),
        (([1, 2, 3, 4, 5], 1), [1, 2, 3, 4]),
        (([1, 2, 3, 4, 5], 2), [1, 2, 3]),
        (([1, 2, 3, 4, 5], 5), []),
        (([1, 2, 3, 4, 5], 6), []),
    ],
)
def test_drop_right(case, expected):
    assert _.drop_right(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5], lambda item: item > 3), [1, 2, 3]),
    ],
)
def test_drop_right_while(case, expected):
    assert _.drop_right_while(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 2, 1, 5, 6, 5, 5, 5],), [2, 1, 5]),
        ((["A", "b", "C", "a", "B", "c"], lambda letter: letter.lower()), ["a", "B", "c"]),
    ],
)
def test_duplicates(case, expected):
    assert _.duplicates(*case) == expected


@parametrize("arity", [2, 3])
def test_duplicates_passes_index_and_collection_to_iteratee(arity):
    records = [{"value": 10}, {"value": 20}, {"value": 30}, {"value": 40}]
    calls = []

    def two_args(value, index):
        calls.append((value, index))
        return index % 2

    def three_args(value, index, collection):
        assert collection is records
        return two_args(value, index)

    result = _.duplicates(records, two_args if arity == 2 else three_args)

    assert result == [records[2], records[3]]
    assert result[0] is records[2]
    assert result[1] is records[3]
    assert calls == list(zip(records, range(len(records))))


def test_duplicates_applies_falsey_iteratee_shorthands():
    records = [{"": "same", "id": "first"}, {"": "same", "id": "second"}]
    original = [record.copy() for record in records]

    result = _.duplicates(records, "")

    assert result == [records[1]]
    assert result[0] is records[1]
    assert records == original


def test_duplicates_applies_numeric_zero_iteratee_as_property_path():
    records = [{"0": "same", "id": "first"}, {"0": "same", "id": "second"}]

    result = _.duplicates(records, 0)

    assert result == [records[1]]
    assert result[0] is records[1]


def test_duplicates_applies_falsey_callable_iteratee():
    class FalseyIteratee:
        def __bool__(self):
            raise AssertionError("duplicates must not evaluate callable truthiness")

        def __call__(self, record):
            return record["group"]

    records = [
        {"group": "same", "id": "first"},
        {"group": "same", "id": "second"},
        {"group": "other", "id": "third"},
    ]

    result = _.duplicates(records, FalseyIteratee())

    assert result == [records[1]]
    assert result[0] is records[1]


def test_duplicates_applies_empty_matcher_iteratee():
    records = [{"id": "first"}, {"id": "second"}]

    result = _.duplicates(records, {})

    assert result == [records[1]]
    assert result[0] is records[1]


def test_duplicates_preserves_duplicate_order_and_identity():
    records = [
        {"group": "a", "id": "first-a"},
        {"group": "b", "id": "first-b"},
        {"group": "a", "id": "second-a"},
        {"group": "b", "id": "second-b"},
    ]

    result = _.duplicates(records, "group")

    assert result == [records[2], records[3]]
    assert result[0] is records[2]
    assert result[1] is records[3]


def test_duplicates_falsey_iteratee_controls_and_empty_input():
    records = [1, 2, 3, 4, 5]

    assert _.duplicates([]) == []
    assert _.duplicates([], "") == []
    assert _.duplicates(records) == []
    assert _.duplicates(records, None) == []
    assert _.duplicates(records, lambda value: value % 2) == [3, 4, 5]


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5], 0), [0, 0, 0, 0, 0]),
        (([1, 2, 3, 4, 5], 0, 2), [1, 2, 0, 0, 0]),
        (([1, 2, 3, 4, 5], 0, 2, 3), [1, 2, 0, 4, 5]),
        (([1, 2, 3, 4, 5], 0, 0, 5), [0, 0, 0, 0, 0]),
        (([1, 2, 3, 4, 5], 0, 0, 8), [0, 0, 0, 0, 0]),
        (([1, 2, 3, 4, 5], 0, 0, -1), [0, 0, 0, 0, 5]),
        # start after end must be a no-op and must not grow the array.
        (([1, 2, 3, 4], "x", 4, 1), [1, 2, 3, 4]),
        (([1, 2, 3, 4, 5], 0, 3, 2), [1, 2, 3, 4, 5]),
        # negative start supported the same way slicing does.
        (([1, 2, 3, 4, 5], 0, -2), [1, 2, 3, 0, 0]),
        (([1, 2, 3, 4, 5], 0, -2, -1), [1, 2, 3, 0, 5]),
        # reversed negative span is a no-op, not an array-growing overlap.
        (([1, 2, 3], "x", -1, -2), [1, 2, 3]),
    ],
)
def test_fill(case, expected):
    array = case[0]
    assert _.fill(*case) == expected
    assert array == expected


@parametrize(
    "case,filter_by,expected",
    [
        (["apple", "banana", "beet"], lambda item: item.startswith("b"), 1),
        (
            [
                {"name": "apple", "type": "fruit"},
                {"name": "banana", "type": "fruit"},
                {"name": "beet", "type": "vegetable"},
            ],
            {"name": "banana"},
            1,
        ),
        (["apple", "banana", "beet"], lambda: False, -1),
    ],
)
def test_find_index(case, filter_by, expected):
    assert _.find_index(case, filter_by) == expected


@parametrize(
    "case,filter_by,expected",
    [
        (["apple", "banana", "beet"], lambda item: item.startswith("b"), 2),
        (
            [
                {"name": "apple", "type": "fruit"},
                {"name": "banana", "type": "fruit"},
                {"name": "beet", "type": "vegetable"},
            ],
            {"type": "fruit"},
            1,
        ),
        (["apple", "banana", "beet"], lambda: False, -1),
    ],
)
def test_find_last_index(case, filter_by, expected):
    assert _.find_last_index(case, filter_by) == expected


@parametrize(
    "case,expected",
    [
        ([1, ["2222"], [3, [[4]]]], [1, "2222", 3, [[4]]]),
        ([iter([1, 2]), iter([3, [[4]]])], [1, 2, 3, [[4]]]),
        ([{"a": 1}, [2]], [{"a": 1}, 2]),
    ],
)
def test_flatten(case, expected):
    assert _.flatten(case) == expected


@parametrize(
    "case,expected",
    [
        ([1, ["2222"], [3, [[4]]]], [1, "2222", 3, 4]),
        ([iter([1, [2]]), iter([[3, [4]]])], [1, 2, 3, 4]),
        ([{"a": 1}, [2]], [{"a": 1}, 2]),
    ],
)
def test_flatten_deep(case, expected):
    assert _.flatten_deep(case) == expected


@parametrize(
    "case,expected",
    [
        (([1, ["2222"], [3, [[4]]]],), [1, "2222", 3, [[4]]]),
        (([1, ["2222"], [3, [[4]]]], 1), [1, "2222", 3, [[4]]]),
        (([1, ["2222"], [3, [[4]]]], 2), [1, "2222", 3, [4]]),
        (([1, ["2222"], [3, [[4]]]], 3), [1, "2222", 3, 4]),
        (([iter([1, [2]])], 1), [1, [2]]),
        (([iter([1, [2]])], 2), [1, 2]),
    ],
)
def test_flatten_depth(case, expected):
    assert _.flatten_depth(*case) == expected


@parametrize(
    "case,expected",
    [
        ([["a", 1], ["b", 2]], {"a": 1, "b": 2}),
        ([["a", 1], ["b", 2], ["c", 3]], {"a": 1, "b": 2, "c": 3}),
    ],
)
def test_from_pairs(case, expected):
    assert _.from_pairs(case) == expected


@parametrize("case,expected", [([1, 2, 3], 1), ([], None)])
def test_head(case, expected):
    assert _.head(case) == expected


@parametrize(
    "case,value,from_index,expected",
    [
        ([1, 2, 3, 1, 2, 3], 2, 0, 1),
        ([1, 2, 3, 1, 2, 3], 2, 3, 4),
        ([1, 1, 2, 2, 3, 3], 2, True, 2),
        ([1, 1, 2, 2, 3, 3], 4, 0, -1),
        ([1, 1, 2, 2, 3, 3], 2, 10, -1),
        ([1, 1, 2, 2, 3, 3], 0, 0, -1),
    ],
)
def test_index_of(case, value, from_index, expected):
    assert _.index_of(case, value, from_index) == expected


@parametrize("case,expected", [([1, 2, 3], [1, 2]), ([1], [])])
def test_initial(case, expected):
    assert _.initial(case) == expected


@parametrize(
    "case,expected",
    [
        (([[10, 20], [30, 40], [50, 60]], [1, 2, 3]), [10, 20, 1, 2, 3, 30, 40, 1, 2, 3, 50, 60]),
        (
            ([[[10, 20]], [[30, 40]], [50, [60]]], [1, 2, 3]),
            [[10, 20], 1, 2, 3, [30, 40], 1, 2, 3, 50, [60]],
        ),
    ],
)
def test_intercalate(case, expected):
    assert _.intercalate(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2], [3, 4]), [1, 3, 2, 4]),
        (([1, 2], [3, 4], [5, 6]), [1, 3, 5, 2, 4, 6]),
        (([1, 2], [3, 4, 5], [6]), [1, 3, 6, 2, 4, 5]),
        (([1, 2, 3], [4], [5, 6]), [1, 4, 5, 2, 6, 3]),
    ],
)
def test_interleave(case, expected):
    assert _.interleave(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], [101, 2, 1, 10], [2, 1]), [1, 2]),
        (([1, 1, 2, 2], [1, 1, 2, 2]), [1, 2]),
        (([1, 2, 3], [4]), []),
        (([1, 2, 3],), [1, 2, 3]),
        (([], [101, 2, 1, 10], [2, 1]), []),
        (([],), []),
    ],
)
def test_intersection(case, expected):
    assert _.intersection(*case) == expected


@parametrize("factory", [iter, lambda values: (value for value in values)])
def test_intersection_iterators(factory):
    assert _.intersection([3, 1, 2, 3], factory([1, 2, 3]), factory([2, 3])) == [3, 2]
    assert _.intersection([1, 2], factory([])) == []


@parametrize("factory", [iter, lambda values: (value for value in values)])
def test_intersection_by_iterators(factory):
    assert _.intersection_by([3.1, 1.1, 2.1], factory([1.2, 2.2, 3.2]), int) == [3.1, 1.1, 2.1]


@parametrize("factory", [iter, lambda values: (value for value in values)])
def test_intersection_with_iterators(factory):
    assert _.intersection_with([3, 1, 2], factory([1, 2, 3]), comparator=lambda a, b: a == b) == [
        3,
        1,
        2,
    ]


def test_intersection_with_non_sized_iterables():
    class NonSizedIterable:
        def __init__(self, values):
            self.values = values

        def __iter__(self):
            return iter(self.values)

    assert _.intersection([3, 1, 2, 3], NonSizedIterable([1, 2, 3])) == [3, 1, 2]
    assert _.intersection_by([3.1, 1.1, 2.1], NonSizedIterable([1.2, 2.2, 3.2]), int) == [
        3.1,
        1.1,
        2.1,
    ]
    assert _.intersection_with(
        [3, 1, 2], NonSizedIterable([1, 2, 3]), comparator=lambda a, b: a == b
    ) == [3, 1, 2]


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], [101, 2, 1, 10], [2, 1], None), [1, 2]),
        (([1, 2, 3], [4]), []),
        (([1, 2, 3],), [1, 2, 3]),
        (([], [101, 2, 1, 10], [2, 1]), []),
        (([],), []),
        (([1, 2, 3], [101, 2, 1, 10], [2, 1], lambda a: 1 if a < 10 else 0), [1]),
        (([{"a": 1}, {"a": 2}, {"a": 3}], [{"a": 2}], "a"), [{"a": 2}]),
    ],
)
def test_intersection_by(case, expected):
    assert _.intersection_by(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], [101, 2, 1, 10], [2, 1], None), [1, 2]),
        (([1, 2, 3], [4]), []),
        (([1, 2, 3],), [1, 2, 3]),
        (([], [101, 2, 1, 10], [2, 1]), []),
        (([],), []),
        (
            (["A", "b", "cC"], ["a", "cc"], ["A", "CC"], lambda a, b: a.lower() == b.lower()),
            ["A", "cC"],
        ),
    ],
)
def test_intersection_with(case, expected):
    assert _.intersection_with(*case) == expected


@parametrize(
    "case,expected",
    [
        (([], "x"), []),
        (([1, 2, 3, 4], 10), [1, 10, 2, 10, 3, 10, 4]),
        (([1, 2, 3, 4], [0, 0, 0]), [1, [0, 0, 0], 2, [0, 0, 0], 3, [0, 0, 0], 4]),
        (
            ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [0, 0, 0]),
            [[1, 2, 3], [0, 0, 0], [4, 5, 6], [0, 0, 0], [7, 8, 9]],
        ),
    ],
)
def test_intersperse(case, expected):
    assert _.intersperse(*case) == expected


@parametrize("case,expected", [([1, 2, 3], 3), ([], None)])
def test_last(case, expected):
    assert _.last(case) == expected


@parametrize(
    "case,value,from_index,expected",
    [
        ([1, 2, 3, 1, 2, 3], 2, 0, -1),
        ([1, 2, 3, 1, 2, 3], 2, 3, 1),
        ([1, 2, 3, 1, 2, 3], 0, 0, -1),
        ([0, 1, 2, 3, 4, 5], 3, 0, -1),
        ([0, 1, 2, 3, 4, 5], 3, 1, -1),
        ([0, 1, 2, 3, 4, 5], 3, 2, -1),
        ([0, 1, 2, 3, 4, 5], 3, 3, 3),
        ([0, 1, 2, 3, 4, 5], 3, 4, 3),
        ([0, 1, 2, 3, 4, 5], 3, 5, 3),
        ([0, 1, 2, 3, 4, 5], 3, 6, 3),
        ([0, 1, 2, 3, 4, 5], 3, -1, 3),
        ([0, 1, 2, 3, 4, 5], 3, -2, 3),
        ([0, 1, 2, 3, 4, 5], 3, -3, 3),
        ([0, 1, 2, 3, 4, 5], 3, -4, -1),
        ([0, 1, 2, 3, 4, 5], 3, -5, -1),
        ([0, 1, 2, 3, 4, 5], 3, -6, -1),
        ([0, 1, 2, 3, 4, 5], 3, None, 3),
        ([1, 2, 3], 1, None, 0),
        ([1, 2, 3], 1, 0, 0),
        ([5, 2, 3], 5, None, 0),
    ],
)
def test_last_index_of(case, value, from_index, expected):
    assert _.last_index_of(case, value, from_index) == expected


@parametrize(
    "case,expected",
    [(([1, 2, None, 4, None, 6], lambda x, i: [str(i)] if x is None else []), ["2", "4"])],
)
def test_mapcat(case, expected):
    assert _.mapcat(*case) == expected


@parametrize(
    "case,pos,expected",
    [([11, 22, 33], 2, 33), ([11, 22, 33], 0, 11), ([11, 22, 33], -1, 33), ([11, 22, 33], 4, None)],
)
def test_nth(case, pos, expected):
    assert _.nth(case, pos) == expected


@parametrize(
    "factory,pos,expected",
    [
        (lambda: iter([11, 22, 33]), 0, 11),
        (lambda: iter([11, 22, 33]), 2, 33),
        (lambda: iter([11, 22, 33]), -1, 33),
        (lambda: iter([11, 22, 33]), 4, None),
        (lambda: (x for x in [11, 22, 33]), 1, 22),
        (lambda: zip([11, 22], "ab"), 1, (22, "b")),
        ({11: "a", 22: "b"}.keys, 1, 22),
        (lambda: iter([]), 0, None),
    ],
)
def test_nth_with_non_sequence_iterables(factory, pos, expected):
    # nth is annotated Iterable, but indexed by position, which needs a
    # sequence. These used to return None.
    assert _.nth(factory(), pos) == expected


@parametrize(
    "case,pos,expected",
    [({0: "x", 1: "y"}, 0, "x"), ({0: "x", 1: "y"}, 1, "y"), ({"a": 1}, 0, None)],
)
def test_nth_indexes_a_mapping_by_key(case, pos, expected):
    # A mapping is looked up by key rather than by position, so it must not be
    # realized into a list of its keys.
    assert _.nth(case, pos) == expected


@parametrize(
    "case,expected,after",
    [
        (([1, 2, 3],), 3, [1, 2]),
        (([1, 2, 3], 0), 1, [2, 3]),
        (([1, 2, 3], 1), 2, [1, 3]),
    ],
)
def test_pop(case, expected, after):
    array = case[0]
    assert _.pop(*case) == expected
    assert array == after


@parametrize("case,values,expected", [([1, 2, 3, 1, 2, 3], [2, 3], [1, 1])])
def test_pull(case, values, expected):
    assert _.pull(case, *values) == expected


@parametrize(
    "case,values,expected",
    [
        ([1, 2, 3, 1, 2, 3], [2, 3], [1, 1]),
        ([1, 2, 3, 1, 2, 3], [1, 2, 3], []),
        ([1, 2, 3, 1, 2, 3], [1, 2, 3, 1, 2, 3], []),
    ],
)
def test_pull_all(case, values, expected):
    assert _.pull_all(case, values) == expected


@parametrize(
    "case,values,iteratee,expected",
    [
        ([1, 2, 3, 1, 2, 3], [2, 3], None, [1, 1]),
        ([1, 2, 3, 1, 2, 3], [2, 3], lambda item: item + 2, [1, 1]),
    ],
)
def test_pull_all_by(case, values, iteratee, expected):
    assert _.pull_all_by(case, values, iteratee) == expected


@parametrize(
    "case,values,iteratee,expected",
    [
        ([1, 2, 3, 1, 2, 3], [2, 3], None, [1, 1]),
        ([1, 2, 3, 1, 2, 3], [2, 3], lambda a, b: a == b, [1, 1]),
        ([1, 2, 3, 1, 2, 3], [2, 3], lambda a, b: a != b, []),
    ],
)
def test_pull_all_with(case, values, iteratee, expected):
    assert _.pull_all_with(case, values, iteratee) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 1, 2, 3], [2, 3]), [1, 2, 2, 3]),
        (([1, 2, 3, 1, 2, 3], [3, 2]), [1, 2, 2, 3]),
        (([1, 2, 3, 1, 2, 3], 3, 2), [1, 2, 2, 3]),
        (([], 0), []),
        (([1, 2, 3], 5), [1, 2, 3]),
        (([1], 0, 0), []),
    ],
)
def test_pull_at(case, expected):
    assert _.pull_at(*case) == expected


@parametrize(
    "indexes,expected",
    [
        ((0, 0), [2, 3, 4]),
        ((1, 1), [1, 3, 4]),
        ((3, 3), [1, 2, 3]),
        ((-1, -1), [1, 2, 3]),
        (([0, 0, 2, 2],), [2, 4]),
        (([0, 2], 0, 2), [2, 4]),
        ((0, 0, 10, 10), [2, 3, 4]),
    ],
)
def test_pull_at_duplicate_indexes(indexes, expected):
    array = [1, 2, 3, 4]

    result = _.pull_at(array, *indexes)

    assert result is array
    assert array == expected


@parametrize(
    "indexes,expected",
    [
        ((-1, -2), [1, 2]),
        ((-2, -1), [1, 2]),
        ((1, -3), [1, 3, 4]),
        ((3, -1), [1, 2, 3]),
        ((0, -1), [2, 3]),
        (([0, -4, -1], 3), [2, 3]),
        ((-5, 4, -1), [1, 2, 3]),
    ],
)
def test_pull_at_normalizes_original_indexes(indexes, expected):
    array = [1, 2, 3, 4]

    result = _.pull_at(array, *indexes)

    assert result is array
    assert array == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], 4), [1, 2, 3, 4]),
        (([1, 2, 3], 4, 5), [1, 2, 3, 4, 5]),
        (([1, 2, 3], [4, 5], 6, [7, 8]), [1, 2, 3, [4, 5], 6, [7, 8]]),
    ],
)
def test_push(case, expected):
    assert _.push(*case) == expected


@parametrize(
    "case,filter_by,expected",
    [
        ([1, 2, 3, 4, 5, 6], lambda x: x % 2 == 0, [2, 4, 6]),
        ([1, 2, 3, 4], lambda x: x >= 3, [3, 4]),
    ],
)
def test_remove(case, filter_by, expected):
    original = list(case)
    assert _.remove(case, filter_by) == expected
    assert set(case).intersection(expected) == set([])
    assert set(original) == set(case + expected)


@parametrize(
    "case,expected",
    [
        ([1, 2, 3, 4], [4, 3, 2, 1]),
        ("abcdef", "fedcba"),
    ],
)
def test_reverse(case, expected):
    assert _.reverse(case) == expected


@parametrize(
    "case,expected,after",
    [
        ([1, 2, 3], 1, [2, 3]),
    ],
)
def test_shift(case, expected, after):
    assert _.shift(case) == expected
    assert case == after


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5], 0, 1), [1]),
        (([1, 2, 3, 4, 5], 1, 3), [2, 3]),
        (([1, 2, 3, 4, 5], 1, 4), [2, 3, 4]),
        (([1, 2, 3, 4, 5], 1, 5), [2, 3, 4, 5]),
        (([1, 2, 3, 4, 5], 0, -1), [1, 2, 3, 4]),
        (([1, 2, 3, 4, 5], 2), [3]),
        (([1, 2, 3, 4, 5], -1), [5]),
        (([1, 2, 3, 4, 5], -2), [4]),
        (([1, 2, 3, 4, 5], -3), [3]),
        (([1, 2, 3, 4, 5], -5), [1]),
    ],
)
def test_slice_(case, expected):
    assert _.slice_(*case) == expected


@parametrize("array", [[1, 2, 3], (1, 2, 3), "abc"])
@parametrize("start", [-5, -6, -(10**100)])
def test_slice_single_item_before_start(array, start):
    assert _.slice_(array, start) == array[:0]


@parametrize("array", [[1, 2, 3], (1, 2, 3), "abc"])
def test_slice_explicit_negative_end(array):
    assert _.slice_(array, -5, -1) == array[:-1]


@parametrize(
    "case,expected",
    [
        (([2, 1, 3, 4, 6, 5],), [1, 2, 3, 4, 5, 6]),
        (([2, 1, 3, 4, 6, 5], None, None, True), [6, 5, 4, 3, 2, 1]),
        (([{"v": 2}, {"v": 3}, {"v": 1}], None, lambda x: x["v"]), [{"v": 1}, {"v": 2}, {"v": 3}]),
        (([2, 1, 3, 4, 6, 5], lambda a, b: -1 if a > b else 1), [6, 5, 4, 3, 2, 1]),
    ],
)
def test_sort(case, expected):
    array = case[0]
    assert _.sort(*case) == expected
    assert array == expected


def test_sort_comparator_key_exception():
    with pytest.raises(ValueError):
        _.sort([], comparator=lambda: None, key=lambda: None)


class FalseySortCallable:
    def __init__(self, callback):
        self.callback = callback

    def __bool__(self):
        return False

    def __call__(self, *args):
        return self.callback(*args)


@parametrize("reverse,expected", [(False, [3, 2, 1]), (True, [1, 2, 3])])
def test_sort_falsey_comparator(reverse, expected):
    comparator = FalseySortCallable(lambda left, right: right - left)
    assert not comparator
    array = [1, 3, 2]

    result = _.sort(array, comparator=comparator, reverse=reverse)

    assert result is array
    assert array == expected


@parametrize("falsey_comparator,falsey_key", [(True, False), (False, True), (True, True)])
def test_sort_falsey_comparator_key_exception(falsey_comparator, falsey_key):
    def comparator(left, right):
        return left - right

    def key(value):
        return value

    comparator_arg = FalseySortCallable(comparator) if falsey_comparator else comparator
    key_arg = FalseySortCallable(key) if falsey_key else key
    assert bool(comparator_arg) is not falsey_comparator
    assert bool(key_arg) is not falsey_key

    with pytest.raises(ValueError, match="mutually exclusive"):
        _.sort([], comparator=comparator_arg, key=key_arg)


def test_sort_falsey_key_without_comparator():
    key = FalseySortCallable(lambda value: -value)
    assert not key
    array = [1, 3, 2]

    assert _.sort(array, key=key) is array
    assert array == [3, 2, 1]


@parametrize(
    "case,expected",
    [
        (([4, 4, 5, 5, 6, 6], 5), 2),
        (([20, 30, 40, 40, 50], 40), 2),
        (([20, 30, 50], 40), 2),
        (([20, 30, 50], 10), 0),
    ],
)
def test_sorted_index(case, expected):
    assert _.sorted_index(*case) == expected


@parametrize(
    "case,expected",
    [
        (([{"x": 20}, {"x": 30}, {"x": 50}], {"x": 40}, "x"), 2),
        (
            (
                ["twenty", "thirty", "fifty"],
                "forty",
                lambda x: {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50}[x],
            ),
            2,
        ),
    ],
)
def test_sorted_index_by(case, expected):
    assert _.sorted_index_by(*case) == expected


@parametrize(
    "array,value,expected",
    [
        ([2, 3, 4, 10, 10], 10, 3),
        ([10, 10, 4, 2, 3], 11, -1),
    ],
)
def test_sorted_index_of(array, value, expected):
    assert _.sorted_index_of(array, value) == expected


@parametrize(
    "case,expected",
    [
        (([4, 4, 5, 5, 6, 6], 5), 4),
        (([20, 30, 40, 40, 50], 40), 4),
        (([20, 30, 50], 10), 0),
    ],
)
def test_sorted_last_index(case, expected):
    assert _.sorted_last_index(*case) == expected


@parametrize(
    "case,expected",
    [
        (([{"x": 20}, {"x": 30}, {"x": 50}], {"x": 40}, "x"), 2),
        (
            (
                ["twenty", "thirty", "fifty"],
                "forty",
                lambda x: {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50}[x],
            ),
            2,
        ),
    ],
)
def test_sorted_last_index_by(case, expected):
    assert _.sorted_last_index_by(*case) == expected


@pytest.mark.parametrize(
    "function,expected", [(_.sorted_index_by, 12345), (_.sorted_last_index_by, 12346)]
)
def test_sorted_index_by_large_sequence_search(function, expected):
    calls = []

    def rank(value):
        calls.append(value)
        return value["rank"]

    values = [{"rank": index} for index in range(65536)]
    assert function(values, {"rank": 12345}, rank) == expected
    # Searching an already sorted sequence should need only logarithmic key work.
    assert len(calls) <= len(values).bit_length() + 1


@pytest.mark.parametrize("function", [_.sorted_index_by, _.sorted_last_index_by])
@pytest.mark.parametrize("size", [0, 1, 2, 17])
def test_sorted_index_by_matches_bisect(function, size):
    keys = [index // 3 for index in range(size)]
    values = [{"rank": key} for key in keys]
    bisect = bisect_left if function is _.sorted_index_by else bisect_right
    for target in range(-1, size + 1):
        assert function(values, {"rank": target}, "rank") == bisect(keys, target)


@parametrize(
    "array,value,expected",
    [
        ([], 1, -1),
        ((), 1, -1),
        (range(0), 1, -1),
        ([2, 3, 3, 4], 1, -1),
        ([2, 3, 3, 4], 2, 0),
        ([2, 3, 3, 4], 3, 2),
        ([2, 3, 3, 4], 5, -1),
        ([2, 3, 4, 10, 10], 10, 4),
        ([10, 10, 4, 2, 3], 11, -1),
    ],
)
def test_sorted_last_index_of(array, value, expected):
    assert _.sorted_last_index_of(array, value) == expected


@parametrize(
    "case,expected", [([2, 2, 1, 0.5, 4], [0.5, 1, 2, 4]), ([4, -2, -2, 0.5, -1], [-2, -1, 0.5, 4])]
)
def test_sorted_uniq(case, expected):
    assert _.sorted_uniq(case) == expected


@parametrize(
    "case,iteratee,expected",
    [
        ([2.5, 3, 1, 2, 1.5], math.floor, [1, 2.5, 3]),
        (["A", "b", "C", "a", "B", "c"], lambda letter: letter.lower(), ["A", "C", "b"]),
    ],
)
def test_sorted_uniq_by(case, iteratee, expected):
    assert _.sorted_uniq_by(case, iteratee) == expected


@parametrize(
    "iteratee,expected",
    [(len, ["a", "bb"]), (lambda word: [len(word)], ["a", "bb"]), (lambda word: None, ["bb"])],
)
def test_sorted_uniq_by_distinct_criterion_types(iteratee, expected):
    words = ["bb", "a", "c", "dd"]
    assert _.sorted_uniq_by(words, iteratee) == expected
    assert _.chain(words).sorted_uniq_by(iteratee).value() == expected
    assert words == ["bb", "a", "c", "dd"]


@parametrize(
    "case,expected,after",
    [
        (([1, 2, 3], 1, 0, "splice"), [], [1, "splice", 2, 3]),
        (([1, 2, 3, 4], 0, -2), [], [1, 2, 3, 4]),
        (([1, 2, 3, 4], 1, -2, 9), [], [1, 9, 2, 3, 4]),
        (([1, 2, 3, 4], -3, -2, 9), [], [1, 9, 2, 3, 4]),
        (([1, 2, 3, 4], 1, -10), [], [1, 2, 3, 4]),
        (([1, 2, 3], 1, 1, "splice"), [2], [1, "splice", 3]),
        (([1, 2, 3], 0, 2, "splice", "slice", "dice"), [1, 2], ["splice", "slice", "dice", 3]),
        (([1, 2, 3], 0), [1, 2, 3], []),
        (([1, 2, 3], 1), [2, 3], [1]),
        (([1, 2, 3, 4], -1, 1), [4], [1, 2, 3]),
        (([1, 2, 3, 4], -2, 1, 9), [3], [1, 2, 9, 4]),
        (([1, 2, 3, 4], -2, None, 9, 8), [3, 4], [1, 2, 9, 8]),
        (([1, 2, 3, 4], -1, 0, 9, 8), [], [1, 2, 3, 9, 8, 4]),
        (([1, 2, 3, 4], -4, 2, 9, 8), [1, 2], [9, 8, 3, 4]),
        (([1, 2, 3, 4], -5, 1, 9), [1], [9, 2, 3, 4]),
        (([1, 2, 3, 4], -100, None, 9, 8), [1, 2, 3, 4], [9, 8]),
        (([1, 2, 3, 4], -2, 10, 9), [3, 4], [1, 2, 9]),
        (([1, 2, 3, 4], 99, 0, 9, 8), [], [1, 2, 3, 4, 9, 8]),
        (([1, 2, 3, 4], 99, None, 9, 8), [], [1, 2, 3, 4, 9, 8]),
        (([], -1, None, 9, 8), [], [9, 8]),
        (([], 99, 0, 9, 8), [], [9, 8]),
    ],
)
def test_splice(case, expected, after):
    array = case[0]
    assert _.splice(*case) == expected
    assert array == after


@parametrize(
    "case,expected",
    [
        (("123", 1, 0, "splice"), "1splice23"),
        (("1234", 0, -2), "1234"),
        (("1234", 1, -2, "x"), "1x234"),
        (("1234", -3, -2, "x"), "1x234"),
        (("1234", 1, -10), "1234"),
        (("1234", -1, 1, "a"), "123a"),
        (("1234", -2, 1, "a"), "12a4"),
        (("1234", -2, None, "a", "b"), "12ab"),
        (("1234", -1, 0, "a", "b"), "123ab4"),
        (("1234", -5, 1, "a"), "a234"),
        (("1234", 99, 0, "a", "b"), "1234ab"),
        (("", -1, None, "a", "b"), "ab"),
        (("", 99, 0, "a", "b"), "ab"),
    ],
)
def test_splice_string(case, expected):
    assert _.splice(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4, 5]]),
        (([1, 2, 3, 4, 5], 0), [[], [1, 2, 3, 4, 5]]),
    ],
)
def test_split_at(case, expected):
    assert _.split_at(*case) == expected


@parametrize("case,expected", [([1, 2, 3], [2, 3]), ([], [])])
def test_tail(case, expected):
    assert _.tail(case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5],), [1]),
        (([1, 2, 3, 4, 5], 1), [1]),
        (([1, 2, 3, 4, 5], 2), [1, 2]),
        (([1, 2, 3, 4, 5], 5), [1, 2, 3, 4, 5]),
        (([1, 2, 3, 4, 5], 6), [1, 2, 3, 4, 5]),
    ],
)
def test_take(case, expected):
    assert _.take(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5], lambda item: item < 3), [1, 2]),
        ((iter([1, 2, 3, 4, 5]), lambda item: item < 3), [1, 2]),
    ],
)
def test_take_while(case, expected):
    assert _.take_while(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5],), [5]),
        (([1, 2, 3, 4, 5], 1), [5]),
        (([1, 2, 3, 4, 5], 2), [4, 5]),
        (([1, 2, 3, 4, 5], 5), [1, 2, 3, 4, 5]),
        (([1, 2, 3, 4, 5], 6), [1, 2, 3, 4, 5]),
    ],
)
def test_take_right(case, expected):
    assert _.take_right(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4, 5], lambda item: item > 3), [4, 5]),
    ],
)
def test_take_right_while(case, expected):
    assert _.take_right_while(*case) == expected


@parametrize(
    "case,expected",
    [
        ([1, 2, 1, 3, 1], [1, 2, 3]),
        ([dict(a=1), dict(a=2), dict(a=1)], [dict(a=1), dict(a=2)]),
    ],
)
def test_uniq(case, expected):
    assert _.uniq(case) == expected


@parametrize("first,second", [(set, frozenset), (frozenset, set)])
def test_uniq_equal_values_with_different_hashability(first, second):
    original = first({1})
    values = [original, second({1}), first({2}), second({2})]
    result = _.uniq(values)
    assert result == [original, first({2})]
    assert result[0] is original

    records = [{"value": value} for value in values]
    assert _.uniq_by(records, "value") == [records[0], records[2]]


@parametrize(
    "case,iteratee,expected",
    [
        ([1, 2, 1.5, 3, 2.5], math.floor, [1, 2, 3]),
        (
            [
                {"name": "banana", "type": "fruit"},
                {"name": "apple", "type": "fruit"},
                {"name": "beet", "type": "vegetable"},
                {"name": "beet", "type": "vegetable"},
                {"name": "carrot", "type": "vegetable"},
                {"name": "carrot", "type": "vegetable"},
            ],
            {"type": "vegetable"},
            [{"name": "banana", "type": "fruit"}, {"name": "beet", "type": "vegetable"}],
        ),
        (
            [{"x": 1, "y": 1}, {"x": 2, "y": 1}, {"x": 1, "y": 1}],
            "x",
            [{"x": 1, "y": 1}, {"x": 2, "y": 1}],
        ),
        (["A", "b", "C", "a", "B", "c"], lambda letter: letter.lower(), ["A", "b", "C"]),
    ],
)
def test_uniq_by(case, iteratee, expected):
    assert _.uniq_by(case, iteratee) == expected


@parametrize(
    "case,iteratee,expected",
    [
        ([1, 2, 3, 4, 5], lambda a, b: (a % 2) == (b % 2), [1, 2]),
        ([5, 4, 3, 2, 1], lambda a, b: (a % 2) == (b % 2), [5, 4]),
    ],
)
def test_uniq_with(case, iteratee, expected):
    assert _.uniq_with(case, iteratee) == expected


@parametrize(
    "case,expected",
    [(([1, 2, 3], [101, 2, 1, 10], [2, 1]), [1, 2, 3, 101, 10]), (([11, 22, 33],), [11, 22, 33])],
)
def test_union(case, expected):
    assert _.union(*case) == expected


@parametrize(
    "case,iteratee,expected",
    [
        (([1, 2, 3], [2, 3, 4]), lambda x: x % 10, [1, 2, 3, 4]),
        (([1, 2, 3], [2, 3, 4]), lambda x: x % 2, [1, 2]),
        (([1, 2, 3], [2, 3, 4], lambda x: x % 2), None, [1, 2]),
        (([11, 22, 33],), None, [11, 22, 33]),
    ],
)
def test_union_by(case, iteratee, expected):
    assert _.union_by(*case, iteratee=iteratee) == expected


@parametrize(
    "case,expected",
    [
        (([11, 22, 33], [22, 33, 44]), [11, 22, 33, 44]),
        (([11, 22, 33],), [11, 22, 33]),
        (([1, 2, 3], [2, 3, 4], lambda a, b: (a % 2) == (b % 2)), [1, 2]),
    ],
)
def test_union_with(case, expected):
    assert _.union_with(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], 4), [4, 1, 2, 3]),
        (([1, 2, 3], 4, 5), [4, 5, 1, 2, 3]),
        (([1, 2, 3], [4, 5], 6, [7, 8]), [[4, 5], 6, [7, 8], 1, 2, 3]),
    ],
)
def test_unshift(case, expected):
    assert _.unshift(*case) == expected
    assert case[0] == expected


@parametrize(
    "case,expected",
    [
        (
            [("moe", 30, True), ("larry", 40, False), ("curly", 35, True)],
            [("moe", "larry", "curly"), (30, 40, 35), (True, False, True)],
        )
    ],
)
def test_unzip(case, expected):
    assert _.unzip(case) == expected


@parametrize(
    "case,expected",
    [
        (([],), []),
        (([[1, 10, 100], [2, 20, 200]],), [(1, 2), (10, 20), (100, 200)]),
        (([[2, 4, 6], [2, 2, 2]], _.power), [4, 16, 36]),
        ((None,), []),
        (([[1, 10, 100], [2, 20, 200]], max), [2, 20, 200]),
        (([[-1, 2], [3, 4]], abs), [1, 2]),
    ],
)
def test_unzip_with(case, expected):
    assert _.unzip_with(*case) == expected


@parametrize("case,expected", [(([1, 2, 1, 0, 3, 1, 4], 0, 1), [2, 3, 4])])
def test_without(case, expected):
    assert _.without(*case) == expected


@parametrize(
    "case,expected",
    [(([1, 2, 3], [5, 2, 1, 4]), [3, 5, 4]), (([1, 2, 5], [2, 3, 5], [3, 4, 5]), [1, 4, 5])],
)
def test_xor(case, expected):
    assert _.xor(*case) == expected


@parametrize("array", [[1, 1, 2], [1, 2, 1], [1, 2, 2]])
def test_xor_single_array_is_unique(array):
    assert _.xor(array) == [1, 2]


@parametrize(
    "arrays,expected",
    [
        ((), [2.1, 1.1]),
        (([],), [2.1, 1.1]),
        (([3.1, 3.2],), [2.1, 1.1, 3.1]),
        (([3.1, 3.2], [3.3]), [2.1, 1.1]),
    ],
)
@parametrize("positional", [False, True])
def test_xor_by_deduplicates_using_iteratee(arrays, expected, positional):
    array = [2.1, 2.2, 1.1]

    if positional:
        result = _.xor_by(array, *arrays, int)
    else:
        result = _.xor_by(array, *arrays, iteratee=int)

    assert result == expected
    assert array == [2.1, 2.2, 1.1]


def test_xor_by_deduplicates_unhashable_criteria():
    array = [{"id": [1], "name": "first"}, {"id": [1], "name": "second"}]
    assert _.xor_by(iter(array), [], "id") == [array[0]]


def test_xor_accepts_iterable_inputs_without_mutating_lists():
    array = [1, 2, 3]
    other = [2, 4]

    assert _.xor(iter(array), (value for value in other)) == [1, 3, 4]
    assert array == [1, 2, 3]
    assert other == [2, 4]


@parametrize("case,expected", [(([1, 2, 3], [5, 4], lambda val: val % 3), [3])])
def test_xor_by(case, expected):
    assert _.xor_by(*case) == expected


def test_xor_by_with_only_iteratee():
    assert _.xor_by([1, 2], lambda value: value) == [1, 2]


def test_xor_by_consumes_each_iterable_once():
    assert _.xor_by((value for value in [1, 2, 3]), iter([2, 4]), iteratee=lambda value: value) == [
        1,
        3,
        4,
    ]


@parametrize("case,expected", [(([1, 2, 3], [5, 4], lambda a, b: a <= b), [5])])
def test_xor_with(case, expected):
    assert _.xor_with(*case) == expected


def test_xor_with_with_only_comparator():
    assert _.xor_with((1, 2), lambda left, right: left == right) == [1, 2]


@parametrize("as_tuple", [False, True])
@parametrize("keyword", [False, True])
def test_xor_with_single_array_deduplicates_using_comparator(as_tuple, keyword):
    values = [{"id": 1, "name": "first"}, {"id": 1, "name": "second"}, {"id": 2}]
    array = tuple(values) if as_tuple else values

    def comparator(left, right):
        return left["id"] == right["id"]

    result = _.xor_with(array, comparator=comparator) if keyword else _.xor_with(array, comparator)

    assert result == [values[0], values[2]]
    assert len(array) == 3


def test_xor_with_single_array_deduplicates_by_equality():
    assert _.xor_with([1, 1, 2]) == [1, 2]


@parametrize("extra_arrays", [([],), ([{"id": 3}],), ([{"id": 3}], [{"id": 4}])])
@parametrize("as_tuple", [False, True])
def test_xor_with_deduplicates_using_comparator(extra_arrays, as_tuple):
    values = [{"id": 1, "name": "first"}, {"id": 1, "name": "duplicate"}, {"id": 2}]
    original = values[:]
    array = tuple(values) if as_tuple else values
    expected = [values[0], values[2]] + [value for other in extra_arrays for value in other]

    def comparator(left, right):
        return left["id"] == right["id"]

    assert _.xor_with(array, *extra_arrays, comparator) == expected
    assert _.xor_with(array, *extra_arrays, comparator=comparator) == expected
    assert values == original


def test_xor_with_accepts_tuple_and_secondary_iterator():
    assert _.xor_with((1, 2, 3), iter([2, 4]), comparator=lambda left, right: left == right) == [
        1,
        3,
        4,
    ]


@parametrize(
    "arrays,expected",
    [
        (([{"id": 1}], [{"id": 2}], [{"id": 1, "name": "updated"}]), [{"id": 2}]),
        (
            ([{"id": 1}], [{"id": 2}], [{"id": 1, "name": "updated"}], [{"id": 2}]),
            [],
        ),
    ],
)
def test_xor_by_multiple_arrays(arrays, expected):
    assert _.xor_by(*arrays, "id") == expected
    assert _.xor_by(*arrays, iteratee="id") == expected


@parametrize(
    "arrays,expected",
    [
        (([{"id": 1}], [{"id": 2}], [{"id": 1, "name": "updated"}]), [{"id": 2}]),
        (
            ([{"id": 1}], [{"id": 2}], [{"id": 1, "name": "updated"}], [{"id": 2}]),
            [],
        ),
    ],
)
def test_xor_with_multiple_arrays(arrays, expected):
    def comparator(left, right):
        return left["id"] == right["id"]

    assert _.xor_with(*arrays, comparator) == expected
    assert _.xor_with(*arrays, comparator=comparator) == expected


@parametrize(
    "case,expected",
    [
        (
            (["moe", "larry", "curly"], [30, 40, 35], [True, False, True]),
            [("moe", 30, True), ("larry", 40, False), ("curly", 35, True)],
        )
    ],
)
def test_zip_(case, expected):
    assert _.zip_(*case) == expected


@parametrize(
    "case,expected",
    [
        ((["moe", "larry"], [30, 40]), {"moe": 30, "larry": 40}),
        (([["moe", 30], ["larry", 40]],), {"moe": 30, "larry": 40}),
        (([],), {}),
        (([], []), {}),
    ],
)
def test_zip_object(case, expected):
    assert _.zip_object(*case) == expected


@parametrize(
    "case,expected",
    [
        ((["a.b.c", "a.b.d"], [1, 2]), {"a": {"b": {"c": 1, "d": 2}}}),
        (([["a.b.c", 1], ["a.b.d", 2]],), {"a": {"b": {"c": 1, "d": 2}}}),
        ((["a.b[0].c", "a.b[1].d"], [1, 2]), {"a": {"b": [{"c": 1}, {"d": 2}]}}),
        (([],), {}),
        (([], []), {}),
    ],
)
def test_zip_object_deep(case, expected):
    assert _.zip_object_deep(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2],), [(1,), (2,)]),
        (([1, 2], [3, 4], _.add), [4, 6]),
        (([1, 5], [3, 4], max), [3, 5]),
        (([-1, 2], [3, 4], abs), [1, 2]),
    ],
)
def test_zip_with(case, expected):
    assert _.zip_with(*case) == expected


@parametrize("values", [[1, 1, 2], (1, 1, 2)])
def test_union_deduplicates_a_single_array(values):
    assert _.union(values) == [1, 2]


def test_union_by_honors_an_iteratee_with_a_single_array():
    values = [{"id": 1}, {"id": 1, "extra": True}, {"id": 2}]
    assert _.union_by(values, iteratee="id") == [values[0], values[2]]
    assert _.union_by(values, "id") == [values[0], values[2]]


def test_union_with_honors_a_comparator_with_a_single_array():
    values = [1, 3, 2, 4]

    def comparator(left, right):
        return left % 2 == right % 2

    assert _.union_with(values, comparator=comparator) == [1, 2]
    assert _.union_with(values, comparator) == [1, 2]


@parametrize(
    "array,other,expected",
    [
        ([1, True], [True], [1]),
        ([True, 1], [1], [True]),
        ([1.0, 1], [1], [1.0]),
        ([1, True, 1], [True], [1, 1]),
    ],
)
def test_difference_with_respects_custom_comparison_for_equal_values(array, other, expected):
    def comparator(left, right):
        return type(left) is type(right) and left == right

    result = _.difference_with(array, other, comparator=comparator)
    assert result == expected
    assert result[0] is array[0]


@parametrize(
    "array,other,expected",
    [
        ([1, True], [True], [1]),
        ([True, 1], [1], [True]),
        ([1.0, 1], [1], [1.0]),
        ([1, True, 1], [True], [1, 1]),
    ],
)
def test_difference_by_respects_transformed_values_when_inputs_compare_equal(
    array, other, expected
):
    def iteratee(value):
        return type(value).__name__, value

    result = _.difference_by(array, other, iteratee=iteratee)
    assert result == expected
    assert result[0] is array[0]


@pytest.mark.parametrize("key", [0, ""])
@pytest.mark.parametrize("function,expected", [(_.sorted_index_by, 1), (_.sorted_last_index_by, 3)])
def test_sorted_index_by_falsey_property(function, expected, key):
    values = [{key: 1}, {key: 2}, {key: 2}, {key: 4}]
    assert function(values, {key: 2}, key) == expected


@pytest.mark.parametrize("function,expected", [(_.sorted_index_by, 1), (_.sorted_last_index_by, 3)])
def test_sorted_index_by_falsey_callable(function, expected):
    class Key:
        def __bool__(self):
            return False

        def __call__(self, value):
            return value["rank"]

    values = [{"rank": 1}, {"rank": 2}, {"rank": 2}, {"rank": 4}]
    assert function(values, {"rank": 2}, Key()) == expected


@parametrize("keyword", [False, True])
def test_intersection_with_deduplicates_using_comparator(keyword):
    array = ["A", "a", "B", "b", "C"]
    other = ["a", "b"]

    def comparator(left, right):
        return left.lower() == right.lower()

    if keyword:
        result = _.intersection_with(array, other, comparator=comparator)
    else:
        result = _.intersection_with(array, other, comparator)

    assert result == ["A", "B"]
    assert array == ["A", "a", "B", "b", "C"]
    assert other == ["a", "b"]


def test_intersection_with_deduplication_preserves_first_references():
    first = {"id": 1, "name": "first"}
    duplicate = {"id": 1, "name": "duplicate"}
    second = {"id": 2, "name": "second"}
    result = _.intersection_with(
        [first, duplicate, second],
        [{"id": 1}, {"id": 2}],
        [{"id": 2}, {"id": 1}],
        comparator=lambda left, right: left["id"] == right["id"],
    )

    assert len(result) == 2
    assert result[0] is first
    assert result[1] is second


def test_intersection_with_unmatched_value_does_not_suppress_match():
    assert _.intersection_with(
        [1, 2], [3], comparator=lambda left, right: abs(left - right) <= 1
    ) == [2]


def test_intersection_with_deduplicates_after_matching_all_arrays():
    assert _.intersection_with(
        [1, 2], [2], [3], comparator=lambda left, right: abs(left - right) <= 1
    ) == [2]


@parametrize("array,expected", [([1, 2], [1]), ([2, 1], [2, 1])])
def test_intersection_with_deduplication_comparator_argument_order(array, expected):
    assert _.intersection_with(array, [0], comparator=lambda left, right: left > right) == expected


@parametrize("function", [_.intersection, _.intersection_by, _.intersection_with])
@parametrize("factory", [list, tuple])
@parametrize("values,expected", [([3, 1, 3, 2, 1], [3, 1, 2]), ([], []), ([3, 1, 2], [3, 1, 2])])
def test_intersection_single_array_is_unique(function, factory, values, expected):
    array = factory(values)

    result = function(array)

    assert isinstance(result, list)
    assert result == expected
    assert result is not array
    assert array == factory(values)


@parametrize("keyword", [False, True])
def test_intersection_by_single_array_uses_iteratee(keyword):
    first = {"id": [1], "name": "first"}
    duplicate = {"id": [1], "name": "duplicate"}
    second = {"id": [2], "name": "second"}
    array = [first, duplicate, second]

    if keyword:
        result = _.intersection_by(array, iteratee="id")
    else:
        result = _.intersection_by(array, "id")

    assert result == [first, second]
    assert result[0] is first
    assert result[1] is second
    assert array == [first, duplicate, second]


@pytest.mark.parametrize("container", [NoTruthList, FalseList])
def test_intersection_by_empty_does_not_evaluate_iteratee(container):
    def unexpected_iteratee(value):
        pytest.fail("An empty intersection should not evaluate the iteratee")

    assert _.intersection_by(container([0]), container(), iteratee=unexpected_iteratee) == []
    assert _.intersection_by(container(), container([0]), iteratee=unexpected_iteratee) == []


@parametrize("keyword", [False, True])
def test_intersection_with_single_array_uses_comparator(keyword):
    first = {"id": 1, "name": "first"}
    duplicate = {"id": 1, "name": "duplicate"}
    second = {"id": 2, "name": "second"}
    array = [first, duplicate, second]

    def comparator(left, right):
        return left["id"] == right["id"]

    if keyword:
        result = _.intersection_with(array, comparator=comparator)
    else:
        result = _.intersection_with(array, comparator)

    assert result == [first, second]
    assert result[0] is first
    assert result[1] is second
    assert array == [first, duplicate, second]


@parametrize("function", [_.intersection_by, _.intersection_with])
def test_intersection_single_array_with_explicit_none(function):
    assert function([3, 1, 3, 2, 1], None) == [3, 1, 2]


@parametrize("array,expected", [([1, 2], [1]), ([2, 1], [2, 1])])
@parametrize("keyword", [False, True])
def test_intersection_with_single_array_comparator_argument_order(array, expected, keyword):
    def comparator(left, right):
        return left > right

    if keyword:
        result = _.intersection_with(array, comparator=comparator)
    else:
        result = _.intersection_with(array, comparator)

    assert result == expected


def test_intersection_single_array_preserves_first_unhashable_values():
    first = {"id": 1}
    duplicate = {"id": 1}
    second = {"id": 2}
    array = [first, duplicate, second]

    result = _.intersection(array)

    assert result == [first, second]
    assert result[0] is first
    assert result[1] is second
    assert array == [first, duplicate, second]


@parametrize("factory", [list, tuple, iter])
def test_zip_with_without_iteratee_keeps_all_arrays(factory):
    assert _.zip_with(factory([1, 2]), factory([3, 4])) == [(1, 3), (2, 4)]
    assert _.zip_with(factory([1, 2]), factory([3, 4]), factory([5, 6])) == [(1, 3, 5), (2, 4, 6)]


def test_zip_with_explicit_optional_iteratee():
    assert _.zip_with([1, 2], [3, 4], None) == [(1, 3), (2, 4)]
    assert _.zip_with([1, 2], [3, 4], iteratee=None) == [(1, 3), (2, 4)]
    assert _.zip_with([1, 2], [3, 4], _.add) == [4, 6]


@parametrize("size", [10**400, 2**53 + 1])
def test_chunk_large_integer_size(size):
    assert _.chunk([1, 2, 3], size) == [[1, 2, 3]]


def test_chunk_does_not_round_large_sequence_length():
    result = _.chunk(range(2**53 + 1), 2**53)
    assert result == [range(2**53), range(2**53, 2**53 + 1)]


@parametrize("function", [_.pull_all_by, _.pull_all_with])
@parametrize("values_factory", [list, iter])
def test_pull_custom_criteria_preserve_equal_distinct_values(function, values_factory):
    array = [1, True, "keep"]
    values = values_factory([1])
    if function is _.pull_all_by:
        result = function(array, values, type)
    else:
        result = function(
            array, values, lambda left, right: type(left) is type(right) and left == right
        )
    assert result is array
    assert len(array) == 2
    assert array[0] is True
    assert array[1] == "keep"


@parametrize("function", [_.xor, _.xor_by, _.xor_with])
def test_xor_many_arrays(function):
    values = [1, 2, 2]
    others = [[], [2, 3]] * 600
    assert function(values, *others) == [1, 2]
    assert values == [1, 2, 2]
    assert others == [[], [2, 3]] * 600


@parametrize("positional", [False, True])
def test_xor_by_many_iterators(positional):
    anchor = {"id": -1}
    others = [iter([{"id": index % 3}]) for index in range(1200)]
    if positional:
        result = _.xor_by(iter([anchor]), *others, "id")
    else:
        result = _.xor_by(iter([anchor]), *others, iteratee="id")
    assert result == [anchor]
    assert all(list(other) == [] for other in others)


@parametrize("positional", [False, True])
def test_xor_with_many_iterators(positional):
    anchor = {"id": -1}
    others = [iter([{"id": index % 3}]) for index in range(1200)]

    def comparator(left, right):
        return left["id"] == right["id"]

    if positional:
        result = _.xor_with((anchor,), *others, comparator)
    else:
        result = _.xor_with((anchor,), *others, comparator=comparator)
    assert result == [anchor]
    assert all(list(other) == [] for other in others)


@pytest.mark.parametrize("container", [NoTruthList, FalseList])
@pytest.mark.parametrize(
    "operation,expected",
    [
        (lambda c: _.uniq_by(c([2, 1, 2])), [2, 1]),
        (lambda c: _.uniq_with(c([2, 1, 2])), [2, 1]),
        (lambda c: _.difference_by([1, 2, 3], c([2])), [1, 3]),
        (lambda c: _.difference_with([1, 2, 3], c([2])), [1, 3]),
        (lambda c: _.intersection_by(c([1, 2, 3]), c([2])), [2]),
        (lambda c: _.intersection_with(c([1, 2, 3]), c([2])), [2]),
        (lambda c: _.unzip_with(c([(1, 2), (3, 4)]), _.add), [4, 6]),
    ],
)
def test_array_operations_do_not_test_input_truth(container, operation, expected):
    assert operation(container) == expected


@pytest.mark.parametrize("container", [NoTruthList, FalseList])
def test_empty_arrays_without_truth_values(container):
    assert _.uniq_by(container()) == []
    assert _.intersection_by([1], container()) == []
    assert _.difference_with([1], container()) == [1]
    assert _.unzip_with(container()) == []
