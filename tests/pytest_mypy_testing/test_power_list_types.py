from typing import TYPE_CHECKING, List, Union

import pytest
from typing_extensions import assert_type

import pydash as _


@pytest.mark.mypy_testing
def test_power_list_scalar_exponents() -> None:
    floats = [1.5, 2.0]
    assert_type(_.power(floats, 2), List[float])
    assert_type(_.power(floats, 0.5), List[float])
    assert_type(_.power(floats, -1), List[float])
    assert_type(_.chain(floats).power(2).value(), List[float])
    assert_type(_.power([1, 2], 2), List[Union[int, float]])
    assert _.power(floats, 2) == [2.25, 4.0]


@pytest.mark.mypy_testing
def test_power_rejects_list_exponents() -> None:
    if TYPE_CHECKING:
        floats = [1.5, 2.0]
        _.power(floats, [2])  # type: ignore[call-overload]
