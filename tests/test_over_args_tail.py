"""Partially transforming arguments must preserve the untransformed tail."""

import pytest

import pydash


@pytest.mark.parametrize(
    "transforms, arguments, expected",
    [
        ([], (3, 4), (3, 4)),
        ([lambda value: value * 2], (3, 4, 5), (6, 4, 5)),
        ([lambda value: value * 2, str], (3, 4, 5), (6, "4", 5)),
        ([[lambda value: value * 2]], (3, 4), (6, 4)),
        ([str, str], (3,), ("3",)),
        ([str], (), ()),
    ],
)
def test_over_args_preserves_arguments_without_transforms(transforms, arguments, expected):
    wrapped = pydash.over_args(lambda *values: values, *transforms)
    assert wrapped(*arguments) == expected


def test_over_args_keeps_tail_references():
    marker = object()
    wrapped = pydash.over_args(lambda first, second: (first, second), str)
    result = wrapped(1, marker)
    assert result[0] == "1"
    assert result[1] is marker


def test_over_args_transforms_only_present_arguments():
    seen = []

    def record(value):
        seen.append(value)
        return value * 2

    wrapped = pydash.over_args(lambda *values: values, record, record, record)
    assert wrapped(2) == (4,)
    assert seen == [2]
