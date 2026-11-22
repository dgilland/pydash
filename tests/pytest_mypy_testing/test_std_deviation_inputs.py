from collections import UserDict
from decimal import Decimal

import pytest
from typing_extensions import assert_type

from pydash import chain, std_deviation


@pytest.mark.mypy_testing
def test_std_deviation_accepts_existing_inputs() -> None:
    assert_type(std_deviation(iter([1, 2, 3])), float)
    assert_type(std_deviation(UserDict({"a": 1, "b": 2})), float)
    assert_type(std_deviation([Decimal("1.5"), Decimal("2.5")]), float)
    assert_type(chain((1, 2, 3)).std_deviation().value(), float)
