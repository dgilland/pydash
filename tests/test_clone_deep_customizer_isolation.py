"""Deep customizations must write to the cloned graph, leaving the input intact."""

from copy import deepcopy

import pytest

import pydash as _


def multiply_numbers(value, *_):
    return value * 10 if isinstance(value, int) else None


@pytest.mark.parametrize(
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


@pytest.mark.parametrize("kind", [dict, list])
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


@pytest.mark.parametrize("replacement", [False, 0, "", [], {}])
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
