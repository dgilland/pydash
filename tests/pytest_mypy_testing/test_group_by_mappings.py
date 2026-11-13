import typing as t

import pytest
from typing_extensions import assert_type

import pydash as _


@pytest.mark.mypy_testing
def test_mypy_group_by_mappings() -> None:
    def parity(value: int) -> int:
        return value % 2

    values: t.Mapping[str, int] = {"first": 1, "second": 3}
    assert_type(_.group_by(values, parity), t.Dict[int, t.List[int]])
    assert_type(_.group_by(values), t.Dict[t.Any, t.List[int]])

    records: t.Mapping[str, t.Dict[str, int]] = {"first": {"kind": 1}}
    assert_type(_.group_by(records, "kind"), t.Dict[t.Any, t.List[t.Dict[str, int]]])
