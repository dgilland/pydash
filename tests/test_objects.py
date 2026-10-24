from argparse import Namespace
from collections import defaultdict, namedtuple
from copy import deepcopy
import datetime as dt
from decimal import Decimal

import pytest

import pydash as _

from . import helpers


parametrize = pytest.mark.parametrize

today = dt.date.today()

SomeNamedTuple = namedtuple("SomeNamedTuple", ["a", "b"])


@parametrize(
    "case,expected",
    [
        (({"name": "fred"}, {"employer": "slate"}), {"name": "fred", "employer": "slate"}),
        (
            ({"name": "fred"}, {"employer": "slate"}, {"employer": "medium"}),
            {"name": "fred", "employer": "medium"},
        ),
    ],
)
def test_assign(case, expected):
    assert _.assign(*case) == expected


@parametrize(
    "case,expected",
    [
        (({"name": "fred"}, {"age": 26}, lambda obj, src: src + 1), {"name": "fred", "age": 27}),
    ],
)
def test_assign_with(case, expected):
    assert _.assign_with(*case) == expected


class Customizer:
    def __init__(self, callback):
        self.callback = callback
        self.calls = []

    def __call__(self, *args):
        self.calls.append(args)
        return self.callback(*args)


class FalseBoolCustomizer(Customizer):
    def __bool__(self):
        return False


class EmptyCustomizer(Customizer):
    def __len__(self):
        return 0


class NoTruthCustomizer(Customizer):
    def __bool__(self):
        raise AssertionError("customizer truth value must not be inspected")


CUSTOMIZERS = [FalseBoolCustomizer, EmptyCustomizer, NoTruthCustomizer]


@parametrize("factory", CUSTOMIZERS)
@parametrize("positional", [False, True])
@parametrize("use_default", [False, True])
def test_assign_with_calls_supplied_customizer(factory, positional, use_default):
    customizer = factory(lambda old, new, *_: None if use_default else old + new)
    target = {"a": 5}
    source = {"a": 10}
    if positional:
        result = _.assign_with(target, source, customizer)
    else:
        result = _.assign_with(target, source, customizer=customizer)
    assert result is target
    assert result == {"a": 10 if use_default else 15}
    assert len(customizer.calls) == 1
    old, new, key, obj, src = customizer.calls[0]
    assert (old, new, key) == (5, 10, "a")
    assert obj is target
    assert src == source


@parametrize("factory", CUSTOMIZERS)
@parametrize("helper", [_.set_with, _.update_with])
def test_path_helpers_call_supplied_customizer(factory, helper):
    customizer = factory(lambda *_: {})
    target = {}
    value = 7 if helper is _.set_with else lambda old: (old or 0) + 7
    result = helper(target, "[0][1][2]", value, customizer=customizer)
    assert result is target
    assert result == {0: {1: {2: 7}}}
    assert len(customizer.calls) == 2
    assert customizer.calls[0] == (None, 0, target)
    assert customizer.calls[1] == (None, 1, target[0])


@parametrize("name", ["assign", "assign_with"])
@parametrize("chained", [False, True])
@parametrize("populated", [False, True])
def test_assignment_accepts_no_sources(name, chained, populated):
    nested = {"keep": [1, 2]}
    target = {"nested": nested} if populated else {}
    if chained:
        result = getattr(_.chain(target), name)().value()
    else:
        result = getattr(_, name)(target)
    assert result is target
    assert target == ({"nested": {"keep": [1, 2]}} if populated else {})
    if populated:
        assert target["nested"] is nested


def test_explicit_none_customizer_accepts_no_sources():
    target = {"a": 1}
    assert _.assign_with(target, customizer=None) is target


@parametrize("positional", [False, True])
def test_no_source_does_not_call_customizer(positional):
    calls = []

    def customizer(value):
        calls.append(value)

    target = {"a": 1}
    if positional:
        result = _.assign_with(target, customizer)
    else:
        result = _.assign_with(target, customizer=customizer)
    assert result is target
    assert calls == []


@parametrize(
    "case,expected",
    [
        (({"name": "fred", "greet": lambda: "Hello, world!"},), ["greet"]),
        ((["fred", lambda: "Hello, world!"],), [1]),
    ],
)
def test_callables(case, expected):
    assert _.callables(*case) == expected


@parametrize(
    "case",
    [
        {"a": {"d": 1}, "b": {"c": 2}},
        [{"a": {"d": 1}, "b": {"c": 2}}],
    ],
)
def test_clone(case):
    result = _.clone(case)

    assert result is not case

    for key, value in _.helpers.iterator(result):
        assert value is case[key]


@parametrize(
    "case,iteratee,expected",
    [
        ({"a": {"d": 1}, "b": {"c": 2}}, lambda v: v, {"a": {"d": 1}, "b": {"c": 2}}),
        (
            {"a": 1, "b": 2, "c": {"d": 3}},
            lambda v, k: v + 2 if isinstance(v, int) and k else None,
            {"a": 3, "b": 4, "c": {"d": 3}},
        ),
    ],
)
def test_clone_with(case, iteratee, expected):
    result = _.clone_with(case, iteratee)

    assert result == expected


@parametrize(
    "case",
    [
        {"a": {"d": 1}, "b": {"c": 2}},
        {"a": {"d": 1}, "b": {"c": 2}},
        [{"a": {"d": 1}, "b": {"c": 2}}],
    ],
)
def test_clone_deep(case):
    result = _.clone_deep(case)

    assert result is not case

    for key, value in _.helpers.iterator(result):
        assert value is not case[key]


@parametrize(
    "case,iteratee,expected",
    [
        ({"a": {"d": 1}, "b": {"c": 2}}, lambda v: v, {"a": {"d": 1}, "b": {"c": 2}}),
        (
            {"a": 1, "b": 2, "c": {"d": 3}},
            lambda v, k: v + 2 if isinstance(v, int) and k else None,
            {"a": 3, "b": 4, "c": {"d": 5}},
        ),
        (["a"], lambda a: None, ["a"]),
        ("a", lambda a: None, "a"),
    ],
)
def test_clone_deep_with(case, iteratee, expected):
    result = _.clone_deep_with(case, iteratee)

    assert result == expected


def multiply_numbers(value, *_):
    return value * 10 if isinstance(value, int) else None


@parametrize(
    "source,expected",
    [
        ({"outer": {"count": 1}}, {"outer": {"count": 10}}),
        ([[1], {"count": 2}], [[10], {"count": 20}]),
        ({"items": [1, {"count": 2}]}, {"items": [10, {"count": 20}]}),
    ],
)
def test_deep_customization_does_not_mutate_source(source, expected):
    before = deepcopy(source)
    result = _.clone_deep_with(source, multiply_numbers)
    assert source == before
    assert result == expected
    assert result is not source
    for key, value in _.helpers.iterator(source):
        assert result[key] is not value


def test_default_customizer_preserves_isolation():
    source = {"outer": {"items": []}}
    result = _.clone_deep_with(source, lambda *_: None)
    result["outer"]["items"].append("new")
    assert source == {"outer": {"items": []}}
    assert result == {"outer": {"items": ["new"]}}


def test_customizer_observes_original_values():
    child = {"count": 1}
    source = {"child": child}
    seen = []

    def customizer(value, *_):
        if isinstance(value, dict):
            seen.append(value)
        return multiply_numbers(value)

    result = _.clone_deep_with(source, customizer)
    assert len(seen) == 2
    assert seen[0] is source
    assert seen[1] is child
    assert child == {"count": 1}
    assert result == {"child": {"count": 10}}


def test_shared_children_stay_shared_in_the_clone():
    shared = {"count": 1}
    source = {"first": shared, "second": shared}
    result = _.clone_deep_with(source, multiply_numbers)
    assert source == {"first": {"count": 1}, "second": {"count": 1}}
    assert result["first"] == {"count": 10}
    assert result["first"] is result["second"]
    assert result["first"] is not shared


@parametrize("kind", [dict, list])
def test_self_references_stay_inside_the_clone(kind):
    source = kind()
    if kind is dict:
        source["self"] = source
        key = "self"
    else:
        source.append(source)
        key = 0
    result = _.clone_deep_with(source, lambda *_: None)
    assert result is not source
    assert result[key] is result
    assert source[key] is source


def test_mutual_references_stay_inside_the_clone():
    source = {"items": []}
    source["items"].append(source)
    result = _.clone_deep_with(source, lambda *_: None)
    assert result["items"][0] is result
    assert result["items"] is not source["items"]
    assert source["items"][0] is source


def test_customizer_failure_does_not_partially_modify_the_source():
    source = {"outer": {"first": 1, "second": 2}}

    def customizer(value, key, *_):
        if key == "second":
            raise ValueError("customization failed")
        return multiply_numbers(value)

    with pytest.raises(ValueError, match="customization failed"):
        _.clone_deep_with(source, customizer)
    assert source == {"outer": {"first": 1, "second": 2}}


def test_deepcopied_dictionary_keys_remain_cloned():
    key = object()
    source = {key: {"count": 1}}
    result = _.clone_deep_with(source, multiply_numbers)
    assert len(result) == 1
    cloned_key = next(iter(result))
    assert cloned_key is not key
    assert result[cloned_key] == {"count": 10}
    assert source[key] == {"count": 1}


@parametrize("replacement", [False, 0, "", [], {}])
def test_explicit_root_override_is_returned_unchanged(replacement):
    source = {"items": [1]}
    result = _.clone_deep_with(source, lambda *_: replacement)
    assert result is replacement
    assert source == {"items": [1]}


def test_explicit_nested_override_is_not_recursively_cloned():
    source = {"branch": {"count": 1}}
    replacement = {"count": 2}
    result = _.clone_deep_with(source, lambda value, key: replacement if key == "branch" else None)
    assert result["branch"] is replacement
    assert source == {"branch": {"count": 1}}


@parametrize(
    "case,expected",
    [
        (
            ({"name": "barney"}, {"name": "fred", "employer": "slate"}),
            {"name": "barney", "employer": "slate"},
        ),
    ],
)
def test_defaults(case, expected):
    assert _.defaults(*case) == expected


@parametrize(
    "case,expected",
    [
        (
            ({"user": {"name": "barney"}}, {"user": {"name": "fred", "age": 36}}),
            {"user": {"name": "barney", "age": 36}},
        ),
        (({}, {"a": {"b": ["c"]}}, {"a": {"b": ["d"]}}), {"a": {"b": ["c"]}}),
        (
            ({"a": {"b": [{"d": "e"}]}}, {"a": {"b": [{"d": "f"}]}}, {"a": {"b": [{"g": "h"}]}}),
            {"a": {"b": [{"d": "e", "g": "h"}]}},
        ),
        (
            (
                {"a": {"b": [{"d": "e"}]}},
                {"a": {"b": [{"d": "f"}, {"g": "h"}]}},
                {"a": {"b": [{"i": "j"}]}},
            ),
            {"a": {"b": [{"d": "e", "i": "j"}]}},
        ),
        (
            (
                {"a": {"b": [{"d": "e"}, {"x": "y"}]}},
                {"a": {"b": [{"d": "f"}, {"g": "h"}]}},
                {"a": {"b": [{"i": "j"}]}},
            ),
            {"a": {"b": [{"d": "e", "i": "j"}, {"x": "y", "g": "h"}]}},
        ),
    ],
)
def test_defaults_deep(case, expected):
    assert _.defaults_deep(*case) == expected


@parametrize(
    "case,expected",
    [
        ([1, 2, 3], {0: 1, 1: 2, 2: 3}),
        ({0: 1, 1: 2, 2: 3}, {0: 1, 1: 2, 2: 3}),
    ],
)
def test_to_dict(case, expected):
    assert _.to_dict(case) == expected


@parametrize(
    "case,expected",
    [
        ({"a": 1, "b": 2, "c": 3}, [1, 2, 3]),
        ([1, 2, 3], [1, 2, 3]),
        ((1, 2), [1, 2]),
        (1, [1]),
    ],
)
def test_to_list(case, expected):
    result = _.to_list(case)
    assert result == expected
    assert isinstance(result, list)


@parametrize(
    "case,expected",
    [
        ({"a": 1, "b": 2, "c": 3}, {1: "a", 2: "b", 3: "c"}),
        ([1, 2, 3], {1: 0, 2: 1, 3: 2}),
    ],
)
def test_invert(case, expected):
    assert _.invert(case) == expected


@parametrize(
    "case,expected",
    [
        (([1, 2, 3],), {1: [0], 2: [1], 3: [2]}),
        (
            ({"first": "fred", "second": "barney", "third": "fred"},),
            {"fred": ["first", "third"], "barney": ["second"]},
        ),
        (({"a": 1, "b": 2}, lambda val: val * 2), {2: ["a"], 4: ["b"]}),
    ],
)
def test_invert_by(case, expected):
    result = _.invert_by(*case)
    for key in result:
        assert set(result[key]) == set(expected[key])


@parametrize(
    "case,expected",
    [
        (({"a": 1, "b": 2}, "get", "a"), 1),
        (({"a": {"b": {"c": [1, 2, 3, 3]}}}, "a.b.c.count", 3), 2),
        (({}, "count"), None),
    ],
)
def test_invoke(case, expected):
    assert _.invoke(*case) == expected


@parametrize(
    "case",
    [
        ({}, "__globals__"),
        ({}, "__builtins__"),
        ({}, "__class__"),
        ({}, "a.__globals__.b"),
        ({}, "a.__builtins__.b"),
        ({}, "a.__class__.b"),
        ([], "__globals__"),
        ([], "__builtins__"),
        ([], "__class__"),
        ([], "a.__globals__.b"),
        ([], "a.__builtins__.b"),
        ([], "a.__class__.b"),
    ],
)
def test_invoke__raises_for_objects_when_path_restricted(case):
    with pytest.raises(KeyError, match="access to restricted key"):
        _.invoke(*case)


@parametrize(
    "case,expected",
    [
        # NOTE: The expected is a list of values but find_key returns only a single
        # value. However, since dicts do not have an order, it's unknown what the
        # "first" returned value will be.
        (
            (
                {
                    "barney": {"age": 36, "blocked": False},
                    "fred": {"age": 40, "blocked": True},
                    "pebbles": {"age": 1, "blocked": False},
                },
                lambda obj: obj["age"] < 40,
            ),
            ["pebbles", "barney"],
        ),
        (
            (
                {
                    "barney": {"age": 36, "blocked": False},
                    "fred": {"age": 40, "blocked": True},
                    "pebbles": {"age": 1, "blocked": False},
                },
            ),
            ["barney", "fred", "pebbles"],
        ),
        (([1, 2, 3],), [0]),
    ],
)
def test_find_key(case, expected):
    assert _.find_key(*case) in expected


@parametrize(
    "case,expected",
    [
        # NOTE: The expected is a list of values but find_last_key returns only a
        # single value. However, since dicts do not have an order, it's unknown
        # what the "first" returned value will be.
        (
            (
                {
                    "barney": {"age": 36, "blocked": False},
                    "fred": {"age": 40, "blocked": True},
                    "pebbles": {"age": 1, "blocked": False},
                },
                lambda obj: obj["age"] < 40,
            ),
            ["pebbles", "barney"],
        ),
        (
            (
                {
                    "barney": {"age": 36, "blocked": False},
                    "fred": {"age": 40, "blocked": True},
                    "pebbles": {"age": 1, "blocked": False},
                },
            ),
            ["barney", "fred", "pebbles"],
        ),
        (([1, 2, 3],), [2]),
    ],
)
def test_find_last_key(case, expected):
    assert _.find_last_key(*case) in expected


@parametrize(
    "case,expected",
    [
        (
            ({"name": "fred", "employer": "slate"}, helpers.for_in_iteratee0),
            ({"name": "fredfred", "employer": "slateslate"},),
        ),
        (
            ({"name": "fred", "employer": "slate"}, helpers.for_in_iteratee1),
            ({"name": "fredfred", "employer": "slate"}, {"name": "fred", "employer": "slateslate"}),
        ),
        (([1, 2, 3], helpers.for_in_iteratee2), ([False, True, 3],)),
    ],
)
def test_for_in(case, expected):
    assert _.for_in(*case) in expected


@parametrize(
    "case,expected",
    [
        (
            ({"name": "fred", "employer": "slate"}, helpers.for_in_iteratee0),
            ({"name": "fredfred", "employer": "slateslate"},),
        ),
        (
            ({"name": "fred", "employer": "slate"}, helpers.for_in_iteratee1),
            ({"name": "fredfred", "employer": "slate"}, {"name": "fred", "employer": "slateslate"}),
        ),
        (([1, 2, 3], helpers.for_in_iteratee2), ([1, True, "index:2"],)),
    ],
)
def test_for_in_right(case, expected):
    assert _.for_in_right(*case) in expected


@parametrize(
    "case,expected",
    [
        (({"one": {"two": {"three": 4}}}, "one.two"), {"three": 4}),
        (({"one": {"two": {"three": 4}}}, "one.two.three"), 4),
        (({"one": {"two": {"three": 4}}}, ["one", "two"]), {"three": 4}),
        (({"one": {"two": {"three": 4}}}, ["one", "two", "three"]), 4),
        (({"one": {"two": {"three": 4}}}, "one.four"), None),
        (({"one": {"two": {"three": 4}}}, "one.four.three", []), []),
        (({"one": {"two": {"three": 4}}}, "one.four.0.a", [{"a": 1}]), [{"a": 1}]),
        (({"one": {"two": {"three": [{"a": 1}]}}}, "one.four.three.0.a", []), []),
        (({"one": {"two": {"three": 4}}}, "one.four.three"), None),
        (({"one": {"two": {"three": [{"a": 1}]}}}, "one.four.three.0.a"), None),
        (({"one": {"two": {"three": 4}}}, "one.four.three", 2), 2),
        (({"one": {"two": {"three": [{"a": 1}]}}}, "one.four.three.0.a", 2), 2),
        (({"one": {"two": {"three": 4}}}, "one.four.three", {"test": "value"}), {"test": "value"}),
        (
            ({"one": {"two": {"three": [{"a": 1}]}}}, "one.four.three.0.a", {"test": "value"}),
            {"test": "value"},
        ),
        (({"one": {"two": {"three": 4}}}, "one.four.three", "haha"), "haha"),
        (({"one": {"two": {"three": [{"a": 1}]}}}, "one.four.three.0.a", "haha"), "haha"),
        (({"one": {"two": {"three": 4}}}, "five"), None),
        (({"one": ["two", {"three": [4, 5]}]}, ["one", 1, "three", 1]), 5),
        (({"one": ["two", {"three": [4, 5]}]}, "one.[1].three.[1]"), 5),
        (({"one": ["two", {"three": [4, 5]}]}, "one.1.three.1"), 5),
        ((["one", {"two": {"three": [4, 5]}}], "[1].two.three.[0]"), 4),
        ((["one", {"two": {"three": [4, [{"four": [5]}]]}}], "[1].two.three[1][0].four[0]"), 5),
        ((["one", {"two": {"three": [4, [{"four": [5]}], 6]}}], "[1].two.three[-2][0].four[0]"), 5),
        ((range(50), "[42]"), 42),
        ((range(50), "[-1]"), 49),
        (([[[[[[[[[[42]]]]]]]]]], "[0][0][0][0][0][0][0][0][0][0]"), 42),
        (([range(50)], "[0][42]"), 42),
        (({"a": [{"b": range(50)}]}, "a[0].b[42]"), 42),
        (
            ({"lev.el1": {"lev\\el2": {"level3": ["value"]}}}, "lev\\.el1.lev\\\\el2.level3.[0]"),
            "value",
        ),
        (({"one": ["hello", "there"]}, "one.bad.hello", []), []),
        (({"one": ["hello", None]}, "one.1.hello"), None),
        ((SomeNamedTuple(1, 2), "a"), 1),
        ((SomeNamedTuple(1, 2), 0), 1),
        ((SomeNamedTuple({"c": {"d": 1}}, 2), "a.c.d"), 1),
        (({}, "update"), None),
        (([], "extend"), None),
        (({(1,): {(2,): 3}}, (1,)), {(2,): 3}),
        (({(1,): {(2,): 3}}, [(1,), (2,)]), 3),
        (({object: 1}, object), 1),
        (({object: {object: 1}}, [object, object]), 1),
        (({1: {"name": "John Doe"}}, "1.name"), "John Doe"),
        (({"a": {"": {"b": 1}}}, "a..b"), 1),
        ((helpers.Object(), "[0].field"), None),
    ],
)
def test_get(case, expected):
    assert _.get(*case) == expected


def test_get__should_not_populate_defaultdict():
    data = defaultdict(list)
    _.get(data, "a")
    assert data == {}


@parametrize(
    "obj,path",
    [
        (helpers.Object(), "__init__.__globals__"),
        (SomeNamedTuple(1, 2), "__globals__"),
        (helpers.Object(subobj=helpers.Object()), "subobj.__builtins__"),
        (helpers.Object(subobj=helpers.Object()), "__builtins__"),
        (helpers.Object(), "__class__"),
        (helpers.Object(), "__name__"),
        (helpers.Object(subobj=helpers.Object()), "subobj.__dict__"),
        (helpers.Object(), "__len__"),
    ],
)
def test_get__raises_for_objects_when_path_restricted(obj, path):
    with pytest.raises(KeyError, match="access to restricted key"):
        _.get(obj, path)


@parametrize(
    "obj,path",
    [
        ({}, "__globals__"),
        ({}, "__builtins__"),
        ({}, "__class__"),
        ([], "__globals__"),
        ([], "__builtins__"),
        ([], "__class__"),
    ],
)
def test_get__does_not_raise_for_dict_or_list_when_path_restricted(obj, path):
    assert _.get(obj, path) is None


@parametrize(
    "obj,path",
    [
        (helpers.Object(), "_name"),
        (helpers.Object(), "foo._dict"),
        (helpers.Object(), "_len"),
    ],
)
def test_get__does_not_raise_for_objects_when_path_is_unrestricted(obj, path):
    assert _.get(obj, path) is None


@parametrize(
    "case,expected",
    [
        (({"a": 1, "b": 2, "c": 3}, "b"), True),
        (([1, 2, 3], 0), True),
        (([1, 2, 3], 1), True),
        (([1, 2, 3], 3), False),
        (({"a": 1, "b": 2, "c": 3}, "b"), True),
        (([1, 2, 3], 0), True),
        (([1, 2, 3], 1), True),
        (([1, 2, 3], 3), False),
        (({"one": {"two": {"three": 4}}}, "one.two"), True),
        (({"one": {"two": {"three": 4}}}, "one.two.three"), True),
        (({"one": {"two": {"three": 4}}}, ["one", "two"]), True),
        (({"one": {"two": {"three": 4}}}, ["one", "two", "three"]), True),
        (({"one": {"two": {"three": 4}}}, "one.four"), False),
        (({"one": {"two": {"three": 4}}}, "five"), False),
        (({"one": {"two": {"three": 4}}}, "one.four.three"), False),
        (({"one": {"two": {"three": [{"a": 1}]}}}, "one.four.three.0.a"), False),
        (({"one": ["two", {"three": [4, 5]}]}, ["one", 1, "three", 1]), True),
        (({"one": ["two", {"three": [4, 5]}]}, "one.[1].three.[1]"), True),
        (({"one": ["two", {"three": [4, 5]}]}, "one.1.three.1"), True),
        ((["one", {"two": {"three": [4, 5]}}], "[1].two.three.[0]"), True),
        (({"lev.el1": {r"lev\el2": {"level3": ["value"]}}}, r"lev\.el1.lev\\el2.level3.[0]"), True),
    ],
)
def test_has(case, expected):
    assert _.has(*case) == expected


def test_has__should_not_populate_defaultdict():
    data = defaultdict(list)
    _.has(data, "a")
    assert data == {}


@parametrize("case,expected", [({"a": 1, "b": 2, "c": 3}, ["a", "b", "c"]), ([1, 2, 3], [0, 1, 2])])
def test_keys(case, expected):
    assert set(_.keys(case)) == set(expected)


@parametrize(
    "case,expected",
    [
        (({"a": 1, "b": 2, "c": 3}, lambda num: num * 3), {"a": 3, "b": 6, "c": 9}),
        (
            (
                {"fred": {"name": "fred", "age": 40}, "pebbles": {"name": "pebbles", "age": 1}},
                "age",
            ),
            {"fred": 40, "pebbles": 1},
        ),
    ],
)
def test_map_values(case, expected):
    assert _.map_values(*case) == expected


@parametrize(
    "case,expected",
    [
        (
            (
                {
                    "level1": {
                        "value": "value 1",
                        "level2": {"value": "value 2", "level3": {"value": "value 3"}},
                    }
                },
                lambda value, property_path: ".".join(property_path) + "==" + value,
            ),
            {
                "level1": {
                    "value": "level1.value==value 1",
                    "level2": {
                        "value": "level1.level2.value==value 2",
                        "level3": {"value": "level1.level2.level3.value==value 3"},
                    },
                }
            },
        ),
        (
            (
                [["value 1", [["value 2", ["value 3"]]]]],
                lambda value, property_path: _.join(property_path, ".") + "==" + value,
            ),
            [["0.0==value 1", [["0.1.0.0==value 2", ["0.1.0.1.0==value 3"]]]]],
        ),
    ],
)
def test_map_values_deep(case, expected):
    assert _.map_values_deep(*case) == expected


@parametrize("explicit_none", [False, True])
@parametrize("obj", [{"a": [1, {"b": None, "c": False}], "d": ""}, [1, {"a": [2]}], {}, []])
def test_map_values_deep_default_iteratee(obj, explicit_none):
    expected = deepcopy(obj)
    args = (None,) if explicit_none else ()

    assert _.map_values_deep(obj, *args) is obj
    assert obj == expected


def test_map_values_deep_default_iteratee_chained():
    child = {"value": 2}
    obj = {"items": [1, child]}

    assert _.chain(obj).map_values_deep().value() is obj
    assert obj == {"items": [1, {"value": 2}]}
    assert obj["items"][1] is child


@parametrize(
    "case,expected",
    [
        (
            (
                {"characters": [{"name": "barney"}, {"name": "fred"}]},
                {"characters": [{"age": 36}, {"age": 40}]},
            ),
            {"characters": [{"name": "barney", "age": 36}, {"name": "fred", "age": 40}]},
        ),
        (
            (
                {"characters": [{"name": "barney"}, {"name": "fred"}, {}]},
                {"characters": [{"age": 36}, {"age": 40}]},
            ),
            {"characters": [{"name": "barney", "age": 36}, {"name": "fred", "age": 40}, {}]},
        ),
        (
            (
                {"characters": [{"name": "barney"}, {"name": "fred"}]},
                {"characters": [{"age": 36}, {"age": 40}, {}]},
            ),
            {"characters": [{"name": "barney", "age": 36}, {"name": "fred", "age": 40}, {}]},
        ),
        (
            (
                {"characters": [{"name": "barney"}, {"name": "fred"}]},
                {"characters": [{"age": 36}, {"age": 40}]},
                {"characters": [{"score": 5}, {"score": 7}]},
            ),
            {
                "characters": [
                    {"name": "barney", "age": 36, "score": 5},
                    {"name": "fred", "age": 40, "score": 7},
                ]
            },
        ),
        (
            (
                {"characters": {"barney": {"age": 36}, "fred": {"score": 7}}},
                {"characters": {"barney": {"score": 5}, "fred": {"age": 40}}},
            ),
            {"characters": {"barney": {"age": 36, "score": 5}, "fred": {"age": 40, "score": 7}}},
        ),
        (
            (
                {"characters": {"barney": {"age": 36}, "fred": {"score": 7}}},
                {"characters": {"barney": [5], "fred": 7}},
            ),
            {"characters": {"barney": [5], "fred": 7}},
        ),
        (
            (
                {"characters": {"barney": {"age": 36}, "fred": {"score": 7}}},
                {"foo": {"barney": [5], "fred": 7}},
            ),
            {
                "characters": {"barney": {"age": 36}, "fred": {"score": 7}},
                "foo": {"barney": [5], "fred": 7},
            },
        ),
        (({"foo": {"bar": 1}}, {"foo": {}}), {"foo": {"bar": 1}}),
        (({},), {}),
        (([],), []),
        ((None,), None),
        ((None, {"a": 1}), None),
        ((None, None, None, {"a": 1}), None),
        (({"a": 1}, None), {"a": 1}),
        (({"a": 1}, None, None, None, {"b": 2}), {"a": 1, "b": 2}),
        (({"a": None}, None, None, None, {"b": None}), {"a": None, "b": None}),
    ],
)
def test_merge(case, expected):
    assert _.merge(*case) == expected


def test_merge_no_link_dict():
    case1 = {"foo": {"bar": None}}
    case2 = {"foo": {"bar": False}}
    result = _.merge({}, case1, case2)
    result["foo"]["bar"] = True

    assert case1 == {"foo": {"bar": None}}
    assert case2 == {"foo": {"bar": False}}


def test_merge_no_link_list():
    case = {"foo": [{}]}
    result = _.merge({}, case)
    result["foo"][0]["bar"] = True

    assert case == {"foo": [{}]}


@parametrize(
    "case,expected",
    [
        (
            (
                {"fruits": ["apple"], "others": {"vegetables": ["beet"]}},
                {"fruits": ["banana"], "others": {"vegetables": ["carrot"]}},
                lambda a, b: a + b if isinstance(a, list) else None,
            ),
            {"fruits": ["apple", "banana"], "others": {"vegetables": ["beet", "carrot"]}},
        ),
    ],
)
def test_merge_with(case, expected):
    assert _.merge_with(*case) == expected


@parametrize(
    "case,expected",
    [
        (({"a": 1, "b": 2, "c": 3}, "a"), {"b": 2, "c": 3}),
        (({"a": 1, "b": 2, "c": 3}, "a", "b"), {"c": 3}),
        (({"a": 1, "b": 2, "c": 3}, ["a", "b"]), {"c": 3}),
        (({"a": 1, "b": 2, "c": 3}, ["a"], ["b"]), {"c": 3}),
        (([1, 2, 3],), {0: 1, 1: 2, 2: 3}),
        (([1, 2, 3], 0), {1: 2, 2: 3}),
        (([1, 2, 3], 0, 1), {2: 3}),
        (({"a": {"b": {"c": "d"}}, "e": "f"}, "a.b.c", "e"), {"a": {"b": {}}}),
        (({"a": [{"b": 1, "c": 2}, {"d": 3}]}, "a[0].c", "a[1].d"), {"a": [{"b": 1}, {}]}),
    ],
)
def test_omit(case, expected):
    assert _.omit(*case) == expected


@parametrize(
    "case,expected",
    [
        (({"a": 1, "b": 2, "c": 3}, ["a", "b"]), {"c": 3}),
        (({"a": 1, "b": 2, "c": 3}, lambda value, key: key == "a"), {"b": 2, "c": 3}),
        (([1, 2, 3],), {0: 1, 1: 2, 2: 3}),
        (([1, 2, 3], [0]), {1: 2, 2: 3}),
    ],
)
def test_omit_by(case, expected):
    assert _.omit_by(*case) == expected


@parametrize(
    "case,expected",
    [
        ((1,), 1),
        ((1.0,), 1),
        (("1",), 1),
        (("00001",), 1),
        ((13, 8), 11),
        (("0A",), 10),
        (("08",), 8),
        (("10",), 16),
        (("10", 10), 10),
        (("xyz",), None),
    ],
)
def test_parse_int(case, expected):
    assert _.parse_int(*case) == expected


@parametrize("value", [float("inf"), float("-inf"), Decimal("Infinity"), Decimal("-Infinity")])
@parametrize("radix", [None, 0, 10])
def test_parse_int_returns_none_for_infinite_numbers(value, radix):
    assert _.parse_int(value, radix) is None


@parametrize("value", [float("nan"), Decimal("NaN"), "inf", "-inf", "not a number", None])
def test_parse_int_other_unparseable_values_are_unchanged(value):
    assert _.parse_int(value) is None


@parametrize("value", [10**400, -(10**400)])
def test_parse_int_preserves_finite_large_integers(value):
    assert _.parse_int(value) == value


@parametrize(
    "case,expected",
    [
        (({"a": 1, "b": 2, "c": 3}, "a"), {"a": 1}),
        (({"a": 1, "b": 2, "c": 3}, "a", "b"), {"a": 1, "b": 2}),
        (({"a": 1, "b": 2, "c": 3}, ["a", "b"]), {"a": 1, "b": 2}),
        (({"a": 1, "b": 2, "c": 3}, ["a"], ["b"]), {"a": 1, "b": 2}),
        (([1, 2, 3],), {}),
        (([1, 2, 3], 0), {0: 1}),
        ((helpers.Object(a=1, b=2, c=3), "a"), {"a": 1}),
        ((helpers.ItemsObject({"a": 1, "b": 2, "c": 3}), "a"), {"a": 1}),
        ((helpers.IteritemsObject({"a": 1, "b": 2, "c": 3}), "a"), {"a": 1}),
        (({"a": {"b": 1, "c": 2, "d": 3}}, "a.b", "a.d"), {"a": {"b": 1, "d": 3}}),
        (
            ({"a": [{"b": 1}, {"c": 2}, {"d": 3}]}, "a[0]", "a[2]"),
            {"a": [{"b": 1}, None, {"d": 3}]},
        ),
    ],
)
def test_pick(case, expected):
    assert _.pick(*case) == expected


@parametrize(
    "case,expected",
    [
        (({"a": 1, "b": 2, "c": 3}, ["a", "b"]), {"a": 1, "b": 2}),
        (({"a": 1, "b": 2, "c": 3}, lambda value, key: key in ["a"]), {"a": 1}),
        (([1, 2, 3],), {0: 1, 1: 2, 2: 3}),
        (([1, 2, 3], [0]), {0: 1}),
        ((helpers.Object(a=1, b=2, c=3), "a"), {"a": 1}),
        ((helpers.ItemsObject({"a": 1, "b": 2, "c": 3}), "a"), {"a": 1}),
        ((helpers.IteritemsObject({"a": 1, "b": 2, "c": 3}), "a"), {"a": 1}),
    ],
)
def test_pick_by(case, expected):
    assert _.pick_by(*case) == expected


@parametrize("key", ["a.b", "a[0]", "[0]", ("a", "b")])
def test_pick_by_literal_keys(key):
    obj = {key: 1, "other": 0}
    calls = []

    def predicate(value, name):
        calls.append((value, name))
        return value == 1

    assert _.pick_by(obj, predicate) == {key: 1}
    assert calls == [(1, key), (0, "other")]
    assert _.pick_by(obj) == {key: 1}


def test_pick_by_literal_key_does_not_read_nested_value():
    obj = {"a.b": 1, "a": {"b": 2}}
    assert _.pick_by(obj, lambda value, key: key == "a.b") == {"a.b": 1}
    assert _.pick_by(obj, ["a.b"]) == {"a": {"b": 2}}


@parametrize(
    "case,expected",
    [
        (({"a": 1, "b": 2}, {"a": "A", "b": "B"}), {"A": 1, "B": 2}),
        (({"a": 1, "b": 2}, {"a": "A"}), {"A": 1, "b": 2}),
        (({"a": 1, "b": 2}, {"c": "C", "b": "B"}), {"a": 1, "B": 2}),
    ],
)
def test_rename_keys(case, expected):
    assert _.rename_keys(*case) == expected


@parametrize(
    "case,expected",
    [
        (({}, ["one", "two", "three", "four"], 1), {"one": {"two": {"three": {"four": 1}}}}),
        (({}, "one.two.three.four", 1), {"one": {"two": {"three": {"four": 1}}}}),
        (
            ({"one": {"two": {}, "three": {}}}, ["one", "two", "three", "four"], 1),
            {"one": {"two": {"three": {"four": 1}}, "three": {}}},
        ),
        (
            ({"one": {"two": {}, "three": {}}}, "one.two.three.four", 1),
            {"one": {"two": {"three": {"four": 1}}, "three": {}}},
        ),
        (({}, "one", 1), {"one": 1}),
        (([], [0, 0, 0], 1), [[[1]]]),
        (([], "[0].[0].[0]", 1), [[[1]]]),
        (([1, 2, [3, 4, [5, 6]]], [2, 2, 1], 7), [1, 2, [3, 4, [5, 7]]]),
        (([1, 2, [3, 4, [5, 6]]], "[2].[2].[1]", 7), [1, 2, [3, 4, [5, 7]]]),
        (([1, 2, [3, 4, [5, 6]]], [2, 2, 2], 7), [1, 2, [3, 4, [5, 6, 7]]]),
        (([1, 2, [3, 4, [5, 6]]], "[2].[2].[2]", 7), [1, 2, [3, 4, [5, 6, 7]]]),
        (({}, "a.b[0].c", 1), {"a": {"b": [{"c": 1}]}}),
        (({}, "a.b[0][0].c", 1), {"a": {"b": [[{"c": 1}]]}}),
        (({}, "a..b", 1), {"a": {"": {"b": 1}}}),
        (({}, "a", tuple), {"a": tuple}),
        (({}, r"a.b\.c.d", 1), {"a": {"b.c": {"d": 1}}}),
    ],
)
def test_set_(case, expected):
    assert _.set_(*case) == expected


def test_set_on_class_works_the_same_with_string_and_list():
    class A:
        def __init__(self):
            self.x = {}

    a1 = A()
    a2 = A()

    assert _.set_(a1, "x.a.b", 1).x == _.set_(a2, ["x", "a", "b"], 1).x


def test_set__raises_for_objects_when_path_restricted():
    class User:
        is_admin = False

    user = User()

    with pytest.raises(KeyError, match="access to restricted key"):
        _.set_(user, "__class__.is_admin", True)

    assert User.is_admin is False
    assert User().is_admin is False


@parametrize(
    "case,expected",
    [
        (({}, "[0][1]", "a", lambda: {}), {0: {1: "a"}}),
        (({}, "[0][1]", dict, lambda: {}), {0: {1: dict}}),
        ((Namespace(), "a.b", 5, lambda: Namespace()), Namespace(a=Namespace(b=5))),  # noqa: PLW0108
        (
            (Namespace(a=Namespace(b=5)), "a.c.d", 55, lambda: Namespace()),  # noqa: PLW0108
            Namespace(a=Namespace(b=5, c=Namespace(d=55))),
        ),
    ],
)
def test_set_with(case, expected):
    assert _.set_with(*case) == expected


@parametrize(
    "case,expected",
    [
        (("1",), True),
        (("0",), False),
        (("true",), True),
        (("True",), True),
        (("false",), False),
        (("False",), False),
        (("",), None),
        (("a",), None),
        ((0,), False),
        ((1,), True),
        (([],), False),
        ((True,), True),
        ((False,), False),
        ((None,), False),
        (("Truthy", ["truthy"]), True),
        (("Falsey", [], ["falsey"]), False),
        (("foobar", ["^[f]"]), True),
        (("ofobar", ["^[f]"]), None),
        (("foobar", [], [".+[r]$"]), False),
        (("foobra", [], [".+[r]$"]), None),
        (("YES", ["^yes$"]), True),
        (("yes", ["^YES$"]), True),
        (("No", [], ["^no$"]), False),
        (("no", [], ["^NO$"]), False),
        (("YeS", ["^y[a-z]s$"]), True),
        (("YES!", ["^yes$"]), None),
        (("X", [r"^\S$"]), True),
        ((" ", [r"^\S$"]), None),
        (("YES", [r"(?-i:^yes$)"]), None),
    ],
)
def test_to_boolean(case, expected):
    assert _.to_boolean(*case) is expected


@parametrize(
    "case,expected",
    [
        (1.4, 1),
        (1.9, 1),
        ("1.4", 1),
        ("1.9", 1),
        (2**53 + 1, 2**53 + 1),
        (-(2**53 + 1), -(2**53 + 1)),
        (str(2**53 + 1), 2**53 + 1),
        (str(-(2**53 + 1)), -(2**53 + 1)),
        (10**400, 10**400),
        (str(10**400), 10**400),
        (float("inf"), 0),
        (float("-inf"), 0),
        ("inf", 0),
        ("-inf", 0),
        (float("nan"), 0),
        ("foo", 0),
        (None, 0),
        (True, 1),
        (False, 0),
        ({}, 0),
        ([], 0),
        ((), 0),
    ],
)
def test_to_integer(case, expected):
    assert _.to_integer(case) == expected


def test_to_integer_preserves_float_conversion_protocol():
    class FloatConvertible:
        def __int__(self):
            return 99

        def __float__(self):
            return 1.9

    class IntegerSubclass(int):
        def __float__(self):
            return 2.9

    class StringSubclass(str):
        def __float__(self):
            return 3.9

    assert _.to_integer(FloatConvertible()) == 1
    assert _.to_integer(IntegerSubclass(99)) == 2
    assert _.to_integer(StringSubclass("99")) == 3


@parametrize(
    "case,expected",
    [(("2.556",), 3.0), (("2.556", 1), 2.6), (("999.999", -1), 990.0), (("foo",), None)],
)
def test_to_number(case, expected):
    assert _.to_number(*case) == expected


@parametrize(
    "case,expected",
    [
        ({"a": 1, "b": 2, "c": 3}, [("a", 1), ("b", 2), ("c", 3)]),
        ([1, 2, 3], [(0, 1), (1, 2), (2, 3)]),
    ],
)
def test_to_pairs(case, expected):
    assert dict(_.to_pairs(case)) == dict(expected)


@parametrize(
    "case,expected",
    [
        (1, "1"),
        (1.25, "1.25"),
        (True, "True"),
        ([1], "[1]"),
        ("d\xc3\xa9j\xc3\xa0 vu", "d\xc3\xa9j\xc3\xa0 vu"),
        ("", ""),
        (None, ""),
        (today, str(today)),
    ],
)
def test_to_string(case, expected):
    assert _.to_string(case) == expected


@parametrize(
    "case,expected",
    [
        (
            ([1, 2, 3, 4, 5], lambda acc, value, key: acc.append((key, value))),
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
        ),
        (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], helpers.transform_iteratee0), [1, 9, 25]),
        (([1, 2, 3, 4, 5],), []),
    ],
)
def test_transform(case, expected):
    assert _.transform(*case) == expected


@parametrize(
    "case,expected",
    [
        (
            (
                {"rome": "Republic"},
                ["rome"],
                lambda value: "Empire" if value == "Republic" else value,
            ),
            {"rome": "Empire"},
        ),
        (({}, ["rome"], lambda value: "Empire" if value == "Republic" else value), {"rome": None}),
        (
            (
                {"earth": {"rome": "Republic"}},
                ["earth", "rome"],
                lambda value: "Empire" if value == "Republic" else value,
            ),
            {"earth": {"rome": "Empire"}},
        ),
    ],
)
def test_update(case, expected):
    assert _.update(*case) == expected


@parametrize(
    "case,expected",
    [
        (({}, "[0][1]", _.constant("a"), lambda *_: {}), {0: {1: "a"}}),
        (({}, "[0][1]", _.constant("a"), {}), {0: {1: "a"}}),
        (({}, "[0][1]", "a", {}), {0: {1: "a"}}),
    ],
)
def test_update_with(case, expected):
    assert _.update_with(*case) == expected


@parametrize(
    "obj,path,expected,new_obj",
    [
        ({"a": [{"b": {"c": 7}}]}, "a.0.b.c", True, {"a": [{"b": {}}]}),
        ([1, 2, 3], "1", True, [1, 3]),
        ([1, 2, 3], 1, True, [1, 3]),
        ([1, [2, 3]], [1, 1], True, [1, [2]]),
        ([1, 2, 3], "[0][0]", False, [1, 2, 3]),
        ([1, 2, 3], "[0][0][0]", False, [1, 2, 3]),
    ],
)
def test_unset(obj, path, expected, new_obj):
    assert _.unset(obj, path) == expected
    assert obj == new_obj


@parametrize("case,expected", [({"a": 1, "b": 2, "c": 3}, [1, 2, 3]), ([1, 2, 3], [1, 2, 3])])
def test_values(case, expected):
    assert set(_.values(case)) == set(expected)


@parametrize("case,expected", [((5, lambda x: x * 2), 10)])
def test_apply(case, expected):
    assert _.apply(*case) == expected


@parametrize(
    "case,expected",
    [((5, lambda x: x * 2, lambda x: x == 5), 10), ((5, lambda x: x * 2, lambda x: x == 10), 5)],
)
def test_apply_if(case, expected):
    assert _.apply_if(*case) == expected


@parametrize("case,expected", [((5, lambda x: x * 2), 10), ((None, lambda x: x * 2), None)])
def test_apply_if_not_none(case, expected):
    assert _.apply_if_not_none(*case) == expected


@parametrize(
    "case,expected",
    [((5, lambda x: x * 2, [ValueError]), 10), ((5, lambda x: x / 0, [ZeroDivisionError]), 5)],
)
def test_apply_catch(case, expected):
    assert _.apply_catch(*case) == expected


def test_invoke_dictionary_callables():
    def add(value, *, increment=1):
        return value + increment

    obj = {"nested": {"add": add}}
    assert _.invoke(obj, "nested.add", 3, increment=2) == 5
    assert _.invoke(obj, ["nested", "add"], 4) == 5
    assert _.method("nested.add", 3, increment=2)(obj) == 5
    assert _.method_of(obj, 4)("nested.add") == 5


def test_invoke_indexed_callables():
    functions = [lambda value: value * 2]
    assert _.invoke(functions, [0], 3) == 6
    assert _.invoke({0: functions[0]}, [0], 4) == 8
    assert _.invoke(functions, [1], 3) is None


def test_invoke_noncallable_attribute():
    class Container:
        value = None

    with pytest.raises(TypeError):
        _.invoke(Container(), "value")
