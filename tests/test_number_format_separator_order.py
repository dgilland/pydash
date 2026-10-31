from decimal import Decimal

import pytest

import pydash as _


@pytest.mark.parametrize("number,prefix", [(1234567, ""), (-1234567, "-")])
@pytest.mark.parametrize("separator", ["ab", "<>", "\u202f\u2009"])
def test_number_format_keeps_separator_character_order(number, prefix, separator):
    assert (
        _.number_format(number, 2, ":", separator)
        == prefix + separator.join(["1", "234", "567"]) + ":00"
    )


def test_number_format_decimal_and_chain_controls():
    value = Decimal("12345.67")
    assert _.number_format(value, 2, ",", "ab") == "12ab345,67"
    assert _.chain(12345).number_format(0, ".", "ab").value() == "12ab345"


def test_single_or_empty_separator_controls():
    assert _.number_format(-12345, 0, ".", ",") == "-12,345"
    assert _.number_format(12345, 0, ".", "") == "12345"
