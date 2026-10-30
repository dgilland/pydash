from decimal import Decimal
from fractions import Fraction
import math
from typing import Union

import pytest
from typing_extensions import assert_type

import pydash as _


@pytest.mark.mypy_testing
def test_mean_numeric_results() -> None:
    decimals = [Decimal("1"), Decimal("2")]
    assert_type(_.mean(decimals), Union[Decimal, float])
    assert_type(_.mean({"a": Decimal("1")}), Union[Decimal, float])
    assert_type(_.mean([Fraction(1), Fraction(2)]), Union[Fraction, float])
    assert_type(_.mean([1j, 2j]), Union[complex, float])
    assert_type(_.mean([1, 2]), float)
    assert_type(_.mean([1.0, 2.0]), float)
    assert_type(_.chain(decimals).mean().value(), Union[Decimal, float])
    empty: list[Decimal] = []
    assert_type(_.mean(empty), Union[Decimal, float])
    assert math.isnan(_.mean(empty))
    assert _.mean(decimals) == Decimal("1.5")


@pytest.mark.mypy_testing
def test_mean_by_numeric_results() -> None:
    assert_type(_.mean_by(["1", "2"], Decimal), Union[Decimal, float])
    assert_type(_.mean_by({"a": "1"}, Decimal), Union[Decimal, float])
    assert_type(_.mean_by([1, 2], lambda x: x * 2), float)
    assert_type(_.chain(["1", "2"]).mean_by(Decimal).value(), Union[Decimal, float])
    assert _.mean_by(["1", "2"], Decimal) == Decimal("1.5")


@pytest.mark.mypy_testing
def test_moving_mean_numeric_results() -> None:
    decimals = [Decimal("1"), Decimal("2"), Decimal("3")]
    assert_type(_.moving_mean(decimals, 2), list[Union[Decimal, float]])
    assert_type(_.moving_mean([1, 2, 3], 2), list[float])
    assert_type(_.chain(decimals).moving_mean(2).value(), list[Union[Decimal, float]])
    assert _.moving_mean(decimals, 2) == [Decimal("1.5"), Decimal("2.5")]
