from collections import UserDict, namedtuple
import math
from operator import attrgetter, itemgetter, methodcaller
from types import MappingProxyType

import pytest

import pydash as _

from . import helpers


parametrize = pytest.mark.parametrize


@parametrize("factory", [dict, MappingProxyType])
def test_reduce_right_mapping_order(factory):
    collection = factory({"a": "A", "b": "B", "c": "C"})
    keys = []

    def join(acc, value, key):
        keys.append(key)
        return acc + value

    assert _.reduce_right(collection, join, "") == "CBA"
    assert keys == ["c", "b", "a"]
    assert list(collection.items()) == [("a", "A"), ("b", "B"), ("c", "C")]
    assert _.reductions_right(collection, lambda acc, value: acc + value, "") == ["C", "CB", "CBA"]
    assert _.reduce_right(factory({}), join, "") == ""


@parametrize(
    "case,expected",
    [
        ((["a", "b", "c", "d", "e"], [0], [2], [4]), ["a", "c", "e"]),
        ((["moe", "larry", "curly"], 0, 2), ["moe", "curly"]),
        (({"a": 1, "b": 2, "c": 3}, "a", "b"), [1, 2]),
    ],
)
def test_at(case, expected):
    assert _.at(*case) == expected


@parametrize(
    "case,expected",
    [
        (([4.3, 6.1, 6.4], lambda num: int(math.floor(num))), {4: 1, 6: 2}),
        (([{"one": 1}, {"one": 1}, {"two": 2}, {"one": 1}], {"one": 1}), {True: 3, False: 1}),
        (([{"one": 1}, {"one": 1}, {"two": 2}, {"one": 1}], "one"), {1: 3, None: 1}),
        (({1: 0, 2: 0, 4: 3},), {0: 2, 3: 1}),
        # pydash.floor/ceil/round_ have an optional `precision` arg; when used as
        # an iteratee the collection index must not be passed as precision.
        (([6.1, 4.2, 6.3], _.floor), {6.0: 2, 4.0: 1}),
        (([6.1, 4.2, 6.3], _.ceil), {7.0: 2, 5.0: 1}),
        (([1.1, 1.9, 2.1], _.round_), {1.0: 1, 2.0: 2}),
    ],
)
def test_count_by(case, expected):
    assert _.count_by(*case) == expected


@parametrize(
    "case,expected",
    [
        (([True, 1, None, "yes"], bool), False),
        (([True, 1, None, "yes"],), False),
        (([{"name": "moe", "age": 40}, {"name": "larry", "age": 50}], "age"), True),
        (([{"name": "moe", "age": 40}, {"name": "larry", "age": 50}], {"age": 50}), False),
    ],
)
def test_every(case, expected):
    assert _.every(*case) == expected


@parametrize(
    "case,expected",
    [
        (([0, True, False, None, 1, 2, 3],), [True, 1, 2, 3]),
        (([1, 2, 3, 4, 5, 6], lambda num: num % 2 == 0), [2, 4, 6]),
        (
            (
                [
                    {"name": "barney", "age": 36, "blocked": False},
                    {"name": "fred", "age": 40, "blocked": True},
                ],
                "blocked",
            ),
            [{"name": "fred", "age": 40, "blocked": True}],
        ),
        (
            (
                [
                    {"name": "barney", "age": 36, "blocked": False},
                    {"name": "fred", "age": 40, "blocked": True},
                ],
                {"age": 36},
            ),
            [{"name": "barney", "age": 36, "blocked": False}],
        ),
        (
            ([{"name": "moe", "age": 40}, {"name": "larry", "age": 50}], {"age": 40}),
            [{"name": "moe", "age": 40}],
        ),
    ],
)
def test_filter_(case, expected):
    assert _.filter_(*case) == expected


@parametrize(
    "case,expected",
    [
        (
            (
                [
                    {"name": "barney", "age": 36, "blocked": False},
                    {"name": "fred", "age": 40, "blocked": True},
                    {"name": "pebbles", "age": 1, "blocked": False},
                ],
                lambda c: c["age"] < 40,
            ),
            {"name": "barney", "age": 36, "blocked": False},
        ),
        (
            (
                [
                    {"name": "barney", "age": 36, "blocked": False},
                    {"name": "fred", "age": 40, "blocked": True},
                    {"name": "pebbles", "age": 1, "blocked": False},
                ],
                {"age": 1},
            ),
            {"name": "pebbles", "age": 1, "blocked": False},
        ),
        (
            (
                [
                    {"name": "barney", "age": 36, "blocked": False},
                    {"name": "fred", "age": 40, "blocked": True},
                    {"name": "pebbles", "age": 1, "blocked": False},
                ],
                "blocked",
            ),
            {"name": "fred", "age": 40, "blocked": True},
        ),
        (
            (
                [
                    {"name": "barney", "age": 36, "blocked": False},
                    {"name": "fred", "age": 40, "blocked": True},
                    {"name": "pebbles", "age": 1, "blocked": False},
                ],
            ),
            {"name": "barney", "age": 36, "blocked": False},
        ),
        (({"abc": 1, "xyz": 2, "c": 3}.keys(), lambda x: "y" in x), "xyz"),
        (({"abc": 1, "xyz": 2, "c": 3}.values(), lambda x: x < 2), 1),
    ],
)
def test_find(case, expected):
    assert _.find(*case) == expected


def test_find_class_object():
    obj = helpers.Object(a=1, b=2)
    assert _.find([None, {}, obj], {"b": 2}) == obj


def test_find_namedtuple():
    User = namedtuple("User", ["first_name", "last_name"])
    obj = User(first_name="Bob", last_name="Smith")
    assert _.find([None, {}, obj], {"first_name": "Bob"}) == obj


@parametrize(
    "case,expected",
    [(({"abc": 1, "xyz": 2, "c": 3}.values(), helpers.Filter(lambda x: x < 2)), 1)],
)
def test_find_using_callable_class(case, expected):
    assert _.find(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3, 4], lambda num: num % 2 == 1), 3),
        (({"abc": 1, "xyz": 2, "c": 3}.keys(), lambda x: "y" in x), "xyz"),
        (({"abc": 1, "xyz": 2, "c": 3}.values(), lambda x: x < 2), 1),
    ],
)
def test_find_last(case, expected):
    assert _.find_last(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], None), [1, 2, 3]),
        (([[1], [2], [3]], None), [1, 2, 3]),
        (([[[1]], [[2]], [[3]]], None), [[1], [2], [3]]),
        (([1, 2, 3], lambda x: [x - 1]), [0, 1, 2]),
        (([1, 2, 3], lambda x: [[x], [x]]), [[1], [1], [2], [2], [3], [3]]),
    ],
)
def test_flat_map(case, expected):
    assert _.flat_map(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], None), [1, 2, 3]),
        (([[1], [2], [3]], None), [1, 2, 3]),
        (([[[1]], [[2]], [[3]]], None), [1, 2, 3]),
        (([1, 2, 3], lambda x: [x - 1]), [0, 1, 2]),
        (([1, 2, 3], lambda x: [[x], [x]]), [1, 1, 2, 2, 3, 3]),
    ],
)
def test_flat_map_deep(case, expected):
    assert _.flat_map_deep(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], None), [1, 2, 3]),
        (([[1], [2], [3]], None), [1, 2, 3]),
        (([[[1]], [[2]], [[3]]], None), [[1], [2], [3]]),
        (([[[1]], [[2]], [[3]]], None, 1), [[1], [2], [3]]),
        (([[[1]], [[2]], [[3]]], None, 2), [1, 2, 3]),
    ],
)
def test_flat_map_depth(case, expected):
    assert _.flat_map_depth(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], helpers.noop), [1, 2, 3]),
        (([1, 2, 3], lambda value: value < 2), [1, 2, 3]),
        (({"one": 1, "two": 2, "three": 3}, helpers.noop), {"one": 1, "two": 2, "three": 3}),
    ],
)
def test_for_each(case, expected):
    assert _.for_each(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], helpers.noop), [1, 2, 3]),
        (([1, 2, 3], lambda value: value < 2), [1, 2, 3]),
        (({"one": 1, "two": 2, "three": 3}, helpers.noop), {"one": 1, "two": 2, "three": 3}),
    ],
)
def test_for_each_right(case, expected):
    assert _.for_each_right(*case) == expected


@parametrize(
    "case,expected",
    [
        (([4.2, 6.1, 6.4], lambda num: int(math.floor(num))), {4: [4.2], 6: [6.1, 6.4]}),
    ],
)
def test_group_by(case, expected):
    assert _.group_by(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], 1), True),
        (([1, 2, 3], 1, 2), False),
        (({"name": "fred", "age": 40}, "fred"), True),
        (("pebbles", "eb"), True),
    ],
)
def test_includes(case, expected):
    assert _.includes(*case) == expected


@parametrize(
    "case,expected",
    [
        (([{"a": {"b": 2}}, {"a": {"c": 3}}], "a.items"), [{"b": 2}.items(), {"c": 3}.items()]),
        (
            ([{"a": {"b": {"c": 2}}}, {"a": {"b": {"c": 3}}}], "a.b.items"),
            [{"c": 2}.items(), {"c": 3}.items()],
        ),
    ],
)
def test_invoke_map(case, expected):
    assert _.invoke_map(*case) == expected


@parametrize(
    "case,expected",
    [
        (
            ([{"dir": "left", "code": 97}, {"dir": "right", "code": 100}], "dir"),
            {"left": {"dir": "left", "code": 97}, "right": {"dir": "right", "code": 100}},
        ),
    ],
)
def test_key_by(case, expected):
    assert _.key_by(*case) == expected


@parametrize(
    "case,expected,sort_results",
    [
        (([1, 2, 3],), [1, 2, 3], False),
        (([1.1, 2.1, 3.1], int), [1, 2, 3], False),
        (([1, 2, 3], lambda num: num * 3), [3, 6, 9], False),
        (([[1], [2, 3], [4, 5, 6]], len), [1, 2, 3], False),
        (({"one": 1, "two": 2, "three": 3}, lambda num: num * 3), [3, 6, 9], True),
        (
            ([{"name": "moe", "age": 40}, {"name": "larry", "age": 50}], "name"),
            ["moe", "larry"],
            False,
        ),
        (
            (
                [
                    {"level1": {"level2": {"level3": {"value": 1}}}},
                    {"level1": {"level2": {"level3": {"value": 2}}}},
                    {"level1": {"level2": {"level3": {"value": 3}}}},
                    {"level1": {"level2": {"level3": {"value": 4}}}},
                    {"level1": {"level2": {}}},
                    {},
                ],
                "level1.level2.level3.value",
            ),
            [1, 2, 3, 4, None, None],
            False,
        ),
        (([[0, 1], [2, 3], [4, 5]], 1), [1, 3, 5], False),
        (
            (
                [{"a": 1, "b": 2, "c": -1}, {"a": 3, "b": 4, "c": -1}, {"a": 5, "b": 6, "c": -1}],
                itemgetter("a", "b"),
            ),
            [(1, 2), (3, 4), (5, 6)],
            False,
        ),
        (
            (
                [helpers.Object(a=1, b=2, c=-1), helpers.Object(a=3, b=4, c=-1)],
                attrgetter("a", "b"),
            ),
            [(1, 2), (3, 4)],
            False,
        ),
        (
            (
                [{"a": 1, "b": 2, "c": -1}, {"a": 3, "b": 4}, {"a": 5}],
                methodcaller("__len__"),
            ),
            [3, 2, 1],
            False,
        ),
    ],
)
def test_map_(case, expected, sort_results):
    actual = _.map_(*case)

    if sort_results:
        actual = sorted(actual)

    assert actual == expected


def test_map_using_class_instance_method_with_kwargs():
    class Thing:
        def double(self, value, **kwargs):
            return value * 2

    values = [1, 2, 3]
    thing = Thing()
    result = _.map_(values, thing.double)
    assert result == [2, 4, 6]


@parametrize(
    "case,expected",
    [
        (
            (
                [
                    {"a": 1, "b": 2, "c": 3},
                    {"a": 1, "b": 2, "c": 4},
                    {"a": 1, "b": 2, "c": 5},
                    {"a": 1, "b": 1, "c": 6},
                    {"a": 1, "b": 1, "c": 7},
                    {"a": 2, "b": 2, "c": 8},
                    {"a": 2, "b": 2, "c": 9},
                    {"a": 2, "b": 2, "c": 10},
                    {"a": 3, "b": 1, "c": 11},
                ],
                "a",
            ),
            {
                1: [
                    {"a": 1, "b": 2, "c": 3},
                    {"a": 1, "b": 2, "c": 4},
                    {"a": 1, "b": 2, "c": 5},
                    {"a": 1, "b": 1, "c": 6},
                    {"a": 1, "b": 1, "c": 7},
                ],
                2: [{"a": 2, "b": 2, "c": 8}, {"a": 2, "b": 2, "c": 9}, {"a": 2, "b": 2, "c": 10}],
                3: [{"a": 3, "b": 1, "c": 11}],
            },
        ),
        (
            (
                [
                    {"a": 1, "b": 2, "c": 3},
                    {"a": 1, "b": 2, "c": 4},
                    {"a": 1, "b": 2, "c": 5},
                    {"a": 1, "b": 1, "c": 6},
                    {"a": 1, "b": 1, "c": 7},
                    {"a": 2, "b": 2, "c": 8},
                    {"a": 2, "b": 2, "c": 9},
                    {"a": 2, "b": 2, "c": 10},
                    {"a": 3, "b": 1, "c": 11},
                ],
                "a",
                "b",
            ),
            {
                1: {
                    2: [
                        {"a": 1, "b": 2, "c": 3},
                        {"a": 1, "b": 2, "c": 4},
                        {"a": 1, "b": 2, "c": 5},
                    ],
                    1: [{"a": 1, "b": 1, "c": 6}, {"a": 1, "b": 1, "c": 7}],
                },
                2: {
                    2: [
                        {"a": 2, "b": 2, "c": 8},
                        {"a": 2, "b": 2, "c": 9},
                        {"a": 2, "b": 2, "c": 10},
                    ]
                },
                3: {1: [{"a": 3, "b": 1, "c": 11}]},
            },
        ),
        (
            (
                [
                    {"a": 1, "b": 2, "c": 3},
                    {"a": 1, "b": 2, "c": 4},
                    {"a": 1, "b": 2, "c": 5},
                    {"a": 1, "b": 1, "c": 6},
                    {"a": 1, "b": 1, "c": 7},
                    {"a": 2, "b": 2, "c": 8},
                    {"a": 2, "b": 2, "c": 9},
                    {"a": 2, "b": 2, "c": 10},
                    {"a": 3, "b": 1, "c": 11},
                ],
            ),
            [
                {"a": 1, "b": 2, "c": 3},
                {"a": 1, "b": 2, "c": 4},
                {"a": 1, "b": 2, "c": 5},
                {"a": 1, "b": 1, "c": 6},
                {"a": 1, "b": 1, "c": 7},
                {"a": 2, "b": 2, "c": 8},
                {"a": 2, "b": 2, "c": 9},
                {"a": 2, "b": 2, "c": 10},
                {"a": 3, "b": 1, "c": 11},
            ],
        ),
    ],
)
def test_nest(case, expected):
    assert _.nest(*case) == expected


@parametrize(
    "case,expected",
    [
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                [],
            ),
            [
                {"user": "barney", "age": 36},
                {"user": "fred", "age": 40},
                {"user": "barney", "age": 26},
                {"user": "fred", "age": 30},
            ],
        ),
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                ["user", "age"],
            ),
            [
                {"user": "barney", "age": 26},
                {"user": "barney", "age": 36},
                {"user": "fred", "age": 30},
                {"user": "fred", "age": 40},
            ],
        ),
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                ["-user", "age"],
            ),
            [
                {"user": "fred", "age": 30},
                {"user": "fred", "age": 40},
                {"user": "barney", "age": 26},
                {"user": "barney", "age": 36},
            ],
        ),
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                ["user", "-age"],
            ),
            [
                {"user": "barney", "age": 36},
                {"user": "barney", "age": 26},
                {"user": "fred", "age": 40},
                {"user": "fred", "age": 30},
            ],
        ),
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                ["-user", "-age"],
            ),
            [
                {"user": "fred", "age": 40},
                {"user": "fred", "age": 30},
                {"user": "barney", "age": 36},
                {"user": "barney", "age": 26},
            ],
        ),
        (
            (
                {
                    1: {"user": "barney", "age": 36},
                    2: {"user": "fred", "age": 40},
                    3: {"user": "barney", "age": 26},
                    4: {"user": "fred", "age": 30},
                },
                ["user", "age"],
            ),
            [
                {"user": "barney", "age": 26},
                {"user": "barney", "age": 36},
                {"user": "fred", "age": 30},
                {"user": "fred", "age": 40},
            ],
        ),
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                [],
                True,
            ),
            [
                {"user": "barney", "age": 36},
                {"user": "fred", "age": 40},
                {"user": "barney", "age": 26},
                {"user": "fred", "age": 30},
            ],
        ),
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                ["user", "age"],
                True,
            ),
            list(
                reversed(
                    [
                        {"user": "barney", "age": 26},
                        {"user": "barney", "age": 36},
                        {"user": "fred", "age": 30},
                        {"user": "fred", "age": 40},
                    ]
                )
            ),
        ),
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                ["-user", "age"],
                True,
            ),
            list(
                reversed(
                    [
                        {"user": "fred", "age": 30},
                        {"user": "fred", "age": 40},
                        {"user": "barney", "age": 26},
                        {"user": "barney", "age": 36},
                    ]
                )
            ),
        ),
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                ["user", "-age"],
                True,
            ),
            list(
                reversed(
                    [
                        {"user": "barney", "age": 36},
                        {"user": "barney", "age": 26},
                        {"user": "fred", "age": 40},
                        {"user": "fred", "age": 30},
                    ]
                )
            ),
        ),
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                ["-user", "-age"],
                True,
            ),
            list(
                reversed(
                    [
                        {"user": "fred", "age": 40},
                        {"user": "fred", "age": 30},
                        {"user": "barney", "age": 36},
                        {"user": "barney", "age": 26},
                    ]
                )
            ),
        ),
        (
            (
                {
                    1: {"user": "barney", "age": 36},
                    2: {"user": "fred", "age": 40},
                    3: {"user": "barney", "age": 26},
                    4: {"user": "fred", "age": 30},
                },
                ["user", "age"],
                True,
            ),
            list(
                reversed(
                    [
                        {"user": "barney", "age": 26},
                        {"user": "barney", "age": 36},
                        {"user": "fred", "age": 30},
                        {"user": "fred", "age": 40},
                    ]
                )
            ),
        ),
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                ["user", "age"],
                [False, True],
                True,
            ),
            list(
                reversed(
                    [
                        {"user": "fred", "age": 30},
                        {"user": "fred", "age": 40},
                        {"user": "barney", "age": 26},
                        {"user": "barney", "age": 36},
                    ]
                )
            ),
        ),
        (
            (
                [
                    {"user": "barney", "age": 36},
                    {"user": "fred", "age": 40},
                    {"user": "barney", "age": 26},
                    {"user": "fred", "age": 30},
                ],
                ["user", "age"],
                [False],
                True,
            ),
            list(
                reversed(
                    [
                        {"user": "fred", "age": 30},
                        {"user": "fred", "age": 40},
                        {"user": "barney", "age": 26},
                        {"user": "barney", "age": 36},
                    ]
                )
            ),
        ),
    ],
)
def test_order_by(case, expected):
    assert _.order_by(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], lambda item: item % 2), [[1, 3], [2]]),
        (([1.2, 2.3, 3.4], lambda item: math.floor(item) % 2), [[1.2, 3.4], [2.3]]),
        (
            (
                [
                    {"name": "barney", "age": 36},
                    {"name": "fred", "age": 40, "blocked": True},
                    {"name": "pebbles", "age": 1},
                ],
                {"age": 1},
            ),
            [
                [{"name": "pebbles", "age": 1}],
                [{"name": "barney", "age": 36}, {"name": "fred", "age": 40, "blocked": True}],
            ],
        ),
        (
            (
                [
                    {"name": "barney", "age": 36},
                    {"name": "fred", "age": 40, "blocked": True},
                    {"name": "pebbles", "age": 1},
                ],
                "blocked",
            ),
            [
                [{"name": "fred", "age": 40, "blocked": True}],
                [{"name": "barney", "age": 36}, {"name": "pebbles", "age": 1}],
            ],
        ),
    ],
)
def test_partition(case, expected):
    assert _.partition(*case) == expected


@parametrize(
    "case,expected",
    [
        (([{"name": "moe", "age": 40}, {"name": "larry", "age": 50}], "name"), ["moe", "larry"]),
        (
            (
                [
                    {"level1": {"level2": {"level3": {"value": 1}}}},
                    {"level1": {"level2": {"level3": {"value": 2}}}},
                    {"level1": {"level2": {"level3": {"value": 3}}}},
                    {"level1": {"level2": {"level3": {"value": 4}}}},
                    {"level1": {"level2": {}}},
                    {},
                ],
                "level1.level2.level3.value",
            ),
            [1, 2, 3, 4, None, None],
        ),
    ],
)
def test_pluck(case, expected):
    assert _.pluck(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], None), 1),
        (([1, 2, 3], helpers.reduce_iteratee0), 6),
        (({"a": 1, "b": 2, "c": 3}, helpers.reduce_iteratee1, {}), {"a": 3, "b": 6, "c": 9}),
    ],
)
def test_reduce_(case, expected):
    assert _.reduce_(*case) == expected


@parametrize("mapping_type", [dict, MappingProxyType])
@parametrize("values,expected", [({"first": 1}, 1), ({"first": 1, "second": 2, "third": 3}, 6)])
def test_reduce_mapping_without_accumulator(mapping_type, values, expected):
    collection = mapping_type(values)
    visited = []

    def accumulate(total, value, key):
        visited.append(key)
        return total + value

    assert _.reduce_(collection, accumulate) == expected
    assert visited == list(values)[1:]
    assert dict(collection) == values


@parametrize("mapping_type", [dict, MappingProxyType])
def test_reduce_empty_mapping_without_accumulator(mapping_type):
    with pytest.raises(TypeError, match=r"reduce_\(\) of empty sequence with no initial value"):
        _.reduce_(mapping_type({}), lambda total, value: total + value)


@parametrize("case,exception", [(([],), TypeError)])
def test_reduce_raise(case, exception):
    raised = False

    try:
        _.reduce_(*case)
    except exception:
        raised = True

    assert raised


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], None), 3),
        (([1, 2, 3], helpers.reduce_iteratee0), 6),
        (([[0, 1], [2, 3], [4, 5]], helpers.reduce_right_iteratee0), [4, 5, 2, 3, 0, 1]),
        (({"a": 1, "b": 2, "c": 3}, helpers.reduce_iteratee1, {}), {"a": 3, "b": 6, "c": 9}),
    ],
)
def test_reduce_right(case, expected):
    assert _.reduce_right(*case) == expected


@parametrize("case,exception", [(([],), TypeError)])
def test_reduce_right_exception(case, exception):
    raised = False

    try:
        _.reduce_right(*case)
    except exception:
        raised = True

    assert raised


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], None), [1, 1]),
        (([1, 2, 3], helpers.reduce_iteratee0), [3, 6]),
        (([1, 2, 3, 4, 5], helpers.reduce_iteratee0, 0), [1, 3, 6, 10, 15]),
    ],
)
def test_reductions(case, expected):
    assert _.reductions(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], None), [3, 3]),
        (([1, 2, 3], helpers.reduce_iteratee0), [5, 6]),
        (
            ([[0, 1], [2, 3], [4, 5]], helpers.reduce_right_iteratee0),
            [[4, 5, 2, 3], [4, 5, 2, 3, 0, 1]],
        ),
    ],
)
def test_reductions_right(case, expected):
    assert _.reductions_right(*case) == expected


@parametrize(
    "case,expected",
    [
        (([0, True, False, None, 1, 2, 3],), [0, False, None]),
        (([1, 2, 3, 4, 5, 6], lambda num: num % 2 == 0), [1, 3, 5]),
        (
            (
                [
                    {"name": "barney", "age": 36, "blocked": False},
                    {"name": "fred", "age": 40, "blocked": True},
                ],
                "blocked",
            ),
            [{"name": "barney", "age": 36, "blocked": False}],
        ),
        (
            (
                [
                    {"name": "barney", "age": 36, "blocked": False},
                    {"name": "fred", "age": 40, "blocked": True},
                ],
                {"age": 36},
            ),
            [{"name": "fred", "age": 40, "blocked": True}],
        ),
    ],
)
def test_reject(case, expected):
    assert _.reject(*case) == expected


@parametrize(
    "case",
    [
        [1, 2, 3, 4, 5, 6],
    ],
)
def test_sample(case):
    assert _.sample(case) in case


@parametrize(
    "case,expected_size",
    [
        (([1, 2, 3, 4, 5, 6], 2), 2),
        (([1, 2, 3, 4, 5, 6], 3), 3),
        (([1, 2, 3, 4, 5, 6], 4), 4),
        (([1, 2, 3], 0), 0),
        (((1, 2, 3), 0), 0),
        (([], 0), 0),
        (([1, 2, 3],), 1),
        (([1, 2, 3], None), 1),
        (([],), 0),
        (([], None), 0),
        (([1, 2, 3], 5), 3),
    ],
)
def test_sample_size(case, expected_size):
    collection = case[0]
    sample_n = _.sample_size(*case)

    assert isinstance(sample_n, list)
    assert len(sample_n) == expected_size
    assert set(sample_n).issubset(collection)


@parametrize("case", [[1, 2, 3, 4, 5, 6], {"one": 1, "two": 2, "three": 3}])
def test_shuffle(case):
    shuffled = _.shuffle(case)

    assert len(shuffled) == len(case)

    if isinstance(case, dict):
        assert set(shuffled) == set(case.values())
    else:
        assert set(shuffled) == set(case)


@parametrize("case", [[1, 2, 3, 4, 5], {"1": 1, "2": 2, "3": 3}])
def test_size(case):
    assert _.size(case) == len(case)


@parametrize(
    "case,expected",
    [
        (([None, 0, "yes", False], bool), True),
        (([None, 0, "yes", False],), True),
        (
            (
                [
                    {"name": "apple", "organic": False, "type": "fruit"},
                    {"name": "carrot", "organic": True, "type": "vegetable"},
                ],
                "organic",
            ),
            True,
        ),
        (
            (
                [
                    {"name": "apple", "organic": False, "type": "fruit"},
                    {"name": "carrot", "organic": True, "type": "vegetable"},
                ],
                {"type": "meat"},
            ),
            False,
        ),
    ],
)
def test_some(case, expected):
    assert _.some(*case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3], math.sin), [3, 1, 2]),
        (
            (
                [
                    {"name": "barney", "age": 36},
                    {"name": "fred", "age": 40},
                    {"name": "barney", "age": 26},
                    {"name": "fred", "age": 30},
                ],
                "age",
            ),
            [
                {"name": "barney", "age": 26},
                {"name": "fred", "age": 30},
                {"name": "barney", "age": 36},
                {"name": "fred", "age": 40},
            ],
        ),
        (({"a": 1, "b": 2, "c": 3}, math.sin), [3, 1, 2]),
        (([1, 2, 3], math.sin, True), [2, 1, 3]),
        (
            (
                [
                    {"name": "barney", "age": 36},
                    {"name": "fred", "age": 40},
                    {"name": "barney", "age": 26},
                    {"name": "fred", "age": 30},
                ],
                "age",
                True,
            ),
            [
                {"name": "fred", "age": 40},
                {"name": "barney", "age": 36},
                {"name": "fred", "age": 30},
                {"name": "barney", "age": 26},
            ],
        ),
        (({"a": 1, "b": 2, "c": 3}, math.sin, True), [2, 1, 3]),
    ],
)
def test_sort_by(case, expected):
    assert _.sort_by(*case) == expected


@parametrize(
    "case,expected",
    [
        (("cat",), ["c", "a", "t"]),
        ((b"cat",), ["c", "a", "t"]),
        (("cat",), ["c", "a", "t"]),
        (("cat", False), ["cat"]),
        ((b"cat", False), [b"cat"]),
        (("cat", False), ["cat"]),
        (({"a": 1, "b": 2, "c": 3},), [1, 2, 3]),
    ],
)
def test_to_list(case, expected):
    assert set(_.to_list(*case)) == set(expected)


@parametrize("mapping_type", [dict, UserDict, MappingProxyType])
def test_shuffle_returns_mapping_values(mapping_type):
    original = {"a": 1, "b": 1, "c": 2}
    mapping = mapping_type(original)
    assert sorted(_.shuffle(mapping)) == [1, 1, 2]
    assert dict(mapping) == original


@parametrize("function,expected", [(_.every, False), (_.some, True)])
@parametrize(
    "predicate",
    [
        lambda value, index: value == 20 and index == 1,
        lambda value, index, collection: collection[index] == value and index == 1,
    ],
)
def test_quantifier_predicate_arguments(function, expected, predicate):
    assert function([10, 20], predicate) is expected


@parametrize("function,result", [(_.every, True), (_.some, False)])
@parametrize("factory", [dict, UserDict, MappingProxyType])
def test_quantifier_mapping_callback(function, result, factory):
    collection = factory({"first": 10, "second": 20})
    calls = []

    def predicate(value, key, original):
        assert original is collection
        calls.append((value, key))
        return result

    assert function(collection, predicate) is result
    assert calls == [(10, "first"), (20, "second")]


@parametrize("function", [_.every, _.some])
@parametrize("factory", [dict, UserDict, MappingProxyType])
@parametrize("collection,expected", [({"key": False}, False), ({0: True}, True)])
def test_quantifier_mapping_values(function, factory, collection, expected):
    assert function(factory(collection)) is expected


@parametrize("function", [_.every, _.some])
@parametrize("key", [0, ""])
def test_quantifier_falsey_property(function, key):
    assert function([{key: False}], key) is False


@parametrize("function", [_.every, _.some])
def test_quantifier_empty_matching_predicate(function):
    assert function([0], {}) is True


@parametrize("function", [_.every, _.some])
def test_quantifier_falsey_callable(function):
    class FalseyPredicate:
        def __bool__(self):
            return False

        def __call__(self, value):
            return not value

    assert function([True], FalseyPredicate()) is False


@parametrize("function,first", [(_.every, False), (_.some, True)])
def test_quantifier_short_circuits_generator(function, first):
    collection = iter([first, "not visited"])
    calls = []

    def predicate(value, index, original):
        assert original is collection
        calls.append((value, index))
        return value

    assert function(collection, predicate) is first
    assert calls == [(first, 0)]
    assert next(collection) == "not visited"


@parametrize("function,expected", [(_.every, True), (_.some, False)])
def test_quantifier_empty_collection(function, expected):
    def predicate(value):
        pytest.fail("Empty collections must not invoke the predicate")

    assert function(iter(()), predicate) is expected


@parametrize("mapping_type", [dict, UserDict, MappingProxyType])
@parametrize("orders", [None, [False]])
def test_order_by_mapping_values(mapping_type, orders):
    source = {"first": {"score": 3}, "second": {"score": 1}, "third": {"score": 2}}
    collection = mapping_type(source)
    expected = [{"score": 1}, {"score": 2}, {"score": 3}]
    if orders:
        expected.reverse()
    assert _.order_by(collection, ["score"], orders) == expected
    assert dict(collection) == source


@parametrize(
    "target,offset,expected",
    [
        (1, 1, False),
        (2, 1, True),
        (3, 3, False),
        (1, -1, False),
        (3, -1, True),
        (1, -10, True),
        (1, 10, False),
    ],
)
def test_includes_dictionary_offset(target, offset, expected):
    source = {"a": 1, "b": 2, "c": 3}
    assert _.includes(source, target, from_index=offset) is expected
    assert source == {"a": 1, "b": 2, "c": 3}
