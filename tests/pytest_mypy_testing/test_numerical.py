from decimal import Decimal
from fractions import Fraction
import math
import typing as t

import pytest
from typing_extensions import assert_type

import pydash as _


@pytest.mark.mypy_testing
def test_mypy_add() -> None:
    reveal_type(_.add(10, 5))  # R: builtins.int
    reveal_type(_.add(10.1, 5))  # R: builtins.float
    reveal_type(_.add(10, 5.5))  # R: builtins.float


@pytest.mark.mypy_testing
def test_mypy_sum_() -> None:
    reveal_type(_.sum_([1, 2, 3, 4]))  # R: builtins.int
    reveal_type(_.sum_([1.5, 2, 3, 4]))  # R: builtins.float
    reveal_type(_.sum_({"hello": 1, "bye": 2}))  # R: builtins.int


@pytest.mark.mypy_testing
def test_mypy_sum_by() -> None:
    reveal_type(_.sum_by([1, 2, 3, 4], lambda x: x ** 2))  # R: builtins.int


@pytest.mark.mypy_testing
def test_mypy_mean() -> None:
    assert_type(_.mean([1, 2, 3, 4]), float)


@pytest.mark.mypy_testing
def test_mypy_mean_by() -> None:
    assert_type(_.mean_by([1, 2, 3, 4], lambda x: x ** 2), float)


@pytest.mark.mypy_testing
def test_mypy_mean_numeric_results() -> None:
    decimals = [Decimal("1"), Decimal("2")]
    assert_type(_.mean(decimals), t.Union[Decimal, float])
    assert_type(_.mean({"a": Decimal("1")}), t.Union[Decimal, float])
    assert_type(_.mean([Fraction(1), Fraction(2)]), t.Union[Fraction, float])
    assert_type(_.mean([1j, 2j]), t.Union[complex, float])
    assert_type(_.mean([1, 2]), float)
    assert_type(_.mean([1.0, 2.0]), float)
    assert_type(_.chain(decimals).mean().value(), t.Union[Decimal, float])
    empty: list[Decimal] = []
    assert_type(_.mean(empty), t.Union[Decimal, float])
    assert math.isnan(_.mean(empty))
    assert _.mean(decimals) == Decimal("1.5")


@pytest.mark.mypy_testing
def test_mypy_mean_by_numeric_results() -> None:
    assert_type(_.mean_by(["1", "2"], Decimal), t.Union[Decimal, float])
    assert_type(_.mean_by({"a": "1"}, Decimal), t.Union[Decimal, float])
    assert_type(_.mean_by([1, 2], lambda x: x * 2), float)
    assert_type(_.chain(["1", "2"]).mean_by(Decimal).value(), t.Union[Decimal, float])
    assert _.mean_by(["1", "2"], Decimal) == Decimal("1.5")


@pytest.mark.mypy_testing
def test_mypy_moving_mean_numeric_results() -> None:
    decimals = [Decimal("1"), Decimal("2"), Decimal("3")]
    assert_type(_.moving_mean(decimals, 2), list[t.Union[Decimal, float]])
    assert_type(_.moving_mean([1, 2, 3], 2), list[float])
    assert_type(_.chain(decimals).moving_mean(2).value(), list[t.Union[Decimal, float]])
    assert _.moving_mean(decimals, 2) == [Decimal("1.5"), Decimal("2.5")]


@pytest.mark.mypy_testing
def test_mypy_ceil() -> None:
    reveal_type(_.ceil(3.275))  # R: builtins.float
    reveal_type(_.ceil(3.215, 1))  # R: builtins.float
    reveal_type(_.ceil(6.004, 2))  # R: builtins.float


@pytest.mark.mypy_testing
def test_mypy_clamp() -> None:
    reveal_type(_.clamp(-10, -5, 5))  # R: builtins.int
    reveal_type(_.clamp(10, -5, 5))  # R: builtins.int
    reveal_type(_.clamp(10, 5))  # R: builtins.int
    reveal_type(_.clamp(-10, 5))  # R: builtins.int


@pytest.mark.mypy_testing
def test_mypy_divide() -> None:
    reveal_type(_.divide(20, 5))  # R: builtins.float
    reveal_type(_.divide(1.5, 3))  # R: builtins.float
    reveal_type(_.divide(None, None))  # R: builtins.float
    reveal_type(_.divide(5, None))  # R: builtins.float


@pytest.mark.mypy_testing
def test_mypy_floor() -> None:
    reveal_type(_.floor(3.75))  # R: builtins.float
    reveal_type(_.floor(3.215, 1))  # R: builtins.float
    reveal_type(_.floor(0.046, 2))  # R: builtins.float


@pytest.mark.mypy_testing
def test_mypy_max_() -> None:
    reveal_type(_.max_([1, 2, 3, 4]))  # R: builtins.int

    empty_int_list: t.List[int] = []
    reveal_type(_.max_(empty_int_list, default=-1))  # R: builtins.int


@pytest.mark.mypy_testing
def test_mypy_max_by() -> None:
    def floor(x: float) -> int:
        return math.floor(x)

    reveal_type(_.max_by([1.0, 1.5, 1.8], floor))  # R: builtins.float
    reveal_type(_.max_by([{'a': 1}, {'a': 2}, {'a': 3}], 'a'))  # R: builtins.dict[builtins.str, builtins.int]

    empty_int_list: t.List[int] = []
    reveal_type(_.max_by(empty_int_list, default=-1))  # R: builtins.int


@pytest.mark.mypy_testing
def test_mypy_median() -> None:
    assert_type(_.median([1, 2, 3, 4, 5]), t.Union[float, int])
    assert_type(_.median([1, 2, 3, 4]), t.Union[float, int])


@pytest.mark.mypy_testing
def test_mypy_median_decimal_types() -> None:
    decimals = [Decimal("1"), Decimal("2")]
    assert_type(_.median(decimals), t.Union[float, Decimal])
    assert_type(_.median({"a": Decimal("1")}), t.Union[float, Decimal])
    assert_type(_.median(["1", "2"], Decimal), t.Union[float, Decimal])
    assert_type(_.chain(decimals).median().value(), t.Union[float, Decimal])
    assert_type(_.median([1, 2]), t.Union[float, int])
    assert_type(_.median([1.0, 2.0]), float)
    assert_type(_.median({1: Decimal("1")}), t.Union[float, Decimal])
    empty: list[Decimal] = []
    assert_type(_.median(empty), t.Union[float, Decimal])
    mixed: list[t.Union[int, Decimal]] = [1, Decimal("2")]
    assert_type(_.median(mixed), t.Union[float, int, Decimal])


@pytest.mark.mypy_testing
def test_mypy_min_() -> None:
    reveal_type(_.min_([1, 2, 3, 4]))  # R: builtins.int

    empty_int_list: t.List[int] = []
    reveal_type(_.min_(empty_int_list, default=100))  # R: builtins.int


@pytest.mark.mypy_testing
def test_mypy_min_by() -> None:
    def floor(x: float) -> int:
        return math.floor(x)

    reveal_type(_.min_by([1.8, 1.5, 1.0], floor))  # R: builtins.float
    reveal_type(_.min_by([{'a': 1}, {'a': 2}, {'a': 3}], 'a'))  # R: builtins.dict[builtins.str, builtins.int]

    empty_int_list: t.List[int] = []
    reveal_type(_.min_by(empty_int_list, default=100))  # R: builtins.int


@pytest.mark.mypy_testing
def test_mypy_moving_mean() -> None:
    assert_type(_.moving_mean(range(10), 1), t.List[float])


@pytest.mark.mypy_testing
def test_mypy_multiply() -> None:
    reveal_type(_.multiply(4, 5))  # R: builtins.int
    reveal_type(_.multiply(10.5, 4))  # R: builtins.float
    reveal_type(_.multiply(10, 4.5))  # R: builtins.float
    reveal_type(_.multiply(None, 10))  # R: builtins.int
    reveal_type(_.multiply(10, None))  # R: builtins.int
    reveal_type(_.multiply(None, 5.5))  # R: builtins.float
    reveal_type(_.multiply(5.5, None))  # R: builtins.float
    reveal_type(_.multiply(None, None))  # R: builtins.int


@pytest.mark.mypy_testing
def test_mypy_power() -> None:
    reveal_type(_.power(5, 2))  # R: Union[builtins.int, builtins.float]
    reveal_type(_.power(12.5, 3))  # R: builtins.float


@pytest.mark.mypy_testing
def test_mypy_power_list_scalar_exponents() -> None:
    floats = [1.5, 2.0]
    assert_type(_.power(floats, 2), t.List[float])
    assert_type(_.power(floats, 0.5), t.List[float])
    assert_type(_.power(floats, -1), t.List[float])
    assert_type(_.chain(floats).power(2).value(), t.List[float])
    assert_type(_.power([1, 2], 2), t.List[t.Union[int, float]])
    assert _.power(floats, 2) == [2.25, 4.0]


@pytest.mark.mypy_testing
def test_mypy_power_rejects_list_exponents() -> None:
    if t.TYPE_CHECKING:
        floats = [1.5, 2.0]
        _.power(floats, [2])  # type: ignore[call-overload]


@pytest.mark.mypy_testing
def test_mypy_round_() -> None:
    reveal_type(_.round_(3.275))  # R: builtins.float
    reveal_type(_.round_(3.275, 1))  # R: builtins.float


@pytest.mark.mypy_testing
def test_mypy_scale() -> None:
    reveal_type(_.scale([1, 2, 3, 4]))  # R: builtins.list[builtins.float]
    reveal_type(_.scale([1, 2, 3, 4], 1))  # R: builtins.list[builtins.float]


@pytest.mark.mypy_testing
def test_mypy_slope() -> None:
    reveal_type(_.slope((1, 2), (4, 8)))  # R: builtins.float


@pytest.mark.mypy_testing
def test_mypy_std_deviation() -> None:
    reveal_type(_.std_deviation([1, 18, 20, 4]))  # R: builtins.float


@pytest.mark.mypy_testing
def test_mypy_subtract() -> None:
    reveal_type(_.subtract(10, 5))  # R: builtins.int
    reveal_type(_.subtract(-10, 4))  # R: builtins.int
    reveal_type(_.subtract(2, 0.5))  # R: builtins.float


@pytest.mark.mypy_testing
def test_mypy_transpose() -> None:
    reveal_type(_.transpose([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))  # R: builtins.list[builtins.list[builtins.int]]


@pytest.mark.mypy_testing
def test_mypy_variance() -> None:
    reveal_type(_.variance([1, 18, 20, 4]))  # R: builtins.float


@pytest.mark.mypy_testing
def test_mypy_var() -> None:
    reveal_type(_.zscore([1, 2, 3]))  # R: builtins.list[builtins.float]
