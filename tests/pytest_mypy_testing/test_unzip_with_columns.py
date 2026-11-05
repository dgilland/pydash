import typing as t

import pytest
from typing_extensions import assert_type

import pydash as _


@pytest.mark.mypy_testing
def test_unzip_with_without_iteratee_returns_variable_length_columns() -> None:
    rows = [(1, 2), (3, 4), (5, 6)]
    result = _.unzip_with(iter(rows))
    assert_type(result, t.List[t.Tuple[int, ...]])
    assert result == [(1, 3, 5), (2, 4, 6)]
    chained = _.chain(rows).unzip_with(None).value()
    assert_type(chained, t.List[t.Tuple[int, ...]])
    assert chained == result
