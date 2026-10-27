from decimal import Decimal
from typing import Union

import pytest
from typing_extensions import assert_type

import pydash as _


@pytest.mark.mypy_testing
def test_median_decimal_types() -> None:
    decimals = [Decimal("1"), Decimal("2")]
    assert_type(_.median(decimals), Union[float, Decimal])
    assert_type(_.median({"a": Decimal("1")}), Union[float, Decimal])
    assert_type(_.median(["1", "2"], Decimal), Union[float, Decimal])
    assert_type(_.chain(decimals).median().value(), Union[float, Decimal])
    assert_type(_.median([1, 2]), Union[float, int])
    assert_type(_.median([1.0, 2.0]), float)
    assert_type(_.median({1: Decimal("1")}), Union[float, Decimal])
    empty: list[Decimal] = []
    assert_type(_.median(empty), Union[float, Decimal])
    mixed: list[Union[int, Decimal]] = [1, Decimal("2")]
    assert_type(_.median(mixed), Union[float, int, Decimal])
