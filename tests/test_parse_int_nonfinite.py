"""Non-finite numeric inputs are not parseable integers."""

from decimal import Decimal

import pytest

import pydash


@pytest.mark.parametrize(
    "value", [float("inf"), float("-inf"), Decimal("Infinity"), Decimal("-Infinity")]
)
@pytest.mark.parametrize("radix", [None, 0, 10])
def test_parse_int_returns_none_for_infinite_numbers(value, radix):
    assert pydash.parse_int(value, radix) is None


@pytest.mark.parametrize(
    "value", [float("nan"), Decimal("NaN"), "inf", "-inf", "not a number", None]
)
def test_parse_int_other_unparseable_values_are_unchanged(value):
    assert pydash.parse_int(value) is None


@pytest.mark.parametrize("value", [10**400, -(10**400)])
def test_parse_int_preserves_finite_large_integers(value):
    assert pydash.parse_int(value) == value
