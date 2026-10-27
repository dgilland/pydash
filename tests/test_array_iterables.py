import typing as t

import pytest

import pydash as _


class NoTruthList(list[t.Any]):
    def __bool__(self):
        raise ValueError("The truth value of an array is ambiguous")


class FalseList(list[t.Any]):
    def __bool__(self):
        return False


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


def test_none_unzip_input():
    assert _.unzip_with(None) == []
