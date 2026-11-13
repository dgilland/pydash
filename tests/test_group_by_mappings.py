from collections import UserDict
from types import MappingProxyType

import pytest

import pydash as _


@pytest.mark.parametrize("factory", [dict, UserDict, MappingProxyType])
@pytest.mark.parametrize(
    "collection,iteratee,expected",
    [
        ({"first": 1, "second": 2, "third": 1}, None, {1: [1, 1], 2: [2]}),
        (
            {"first": 1, "second": 2, "third": 3},
            lambda value: value % 2,
            {1: [1, 3], 0: [2]},
        ),
        (
            {"first": {"kind": "a"}, "second": {"kind": "b"}, "third": {"kind": "a"}},
            "kind",
            {"a": [{"kind": "a"}, {"kind": "a"}], "b": [{"kind": "b"}]},
        ),
        (
            {"first": {"kind": "a"}, "second": {"kind": "b"}},
            {"kind": "a"},
            {True: [{"kind": "a"}], False: [{"kind": "b"}]},
        ),
    ],
)
def test_group_by_mapping_values(factory, collection, iteratee, expected):
    mapping = factory(collection)
    assert _.group_by(mapping, iteratee) == expected
    assert dict(mapping) == collection
