
import pydash as pyd
from .fixtures import parametrize


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5],), 15),
    (([{'b': 4}, {'b': 5}, {'b': 6}], 'b'), 15),
    (([0, 14, 0.2],), 14.2),
    (({'one': {'a': 1}, 'two': {'a': 2}, 'three': {'a': 3}}, 'a'), 6),
])
def test_add(case, expected):
    assert pyd.add(*case) == expected


@parametrize('case', [
    pyd.sum_
])
def test_add_aliases(case):
    assert pyd.add is case


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5],), 3),
    (([{'b': 4}, {'b': 5}, {'b': 6}], 'b'), 5),
    (([0, 0.5, 1],), 0.5),
    (({'one': {'a': 1}, 'two': {'a': 2}, 'three': {'a': 3}}, 'a'), 2),
])
def test_average(case, expected):
    assert pyd.average(*case) == expected


@parametrize('case', [
    pyd.avg,
    pyd.mean
])
def test_average_aliases(case):
    assert pyd.average is case


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 3), [2, 3, 4]),
    (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3), [2, 3, 4, 5, 6, 7, 8, 9]),
    (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4),
     [2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5]),
])
def test_moving_average(case, expected):
    assert pyd.moving_average(*case) == expected


@parametrize('case', [
    pyd.moving_avg
])
def test_moving_average_aliases(case):
    assert pyd.moving_average is case


@parametrize('case,expected', [
    ((2, 3), 8),
    ((3, 4), 81),
    (([1, 2, 3, 4, 5], 2), [1, 4, 9, 16, 25]),
    (('junk', 2), None),
])
def test_power(case, expected):
    assert pyd.power(*case) == expected


@parametrize('case', [
    pyd.pow_
])
def test_power_aliases(case):
    assert pyd.power is case


@parametrize('case,expected', [
    ((2.5,), 3),
    ((2.499,), 2),
    ((2.499, 2), 2.50),
    (([2.5, 2.499, 2.555], 2), [2.50, 2.50, 2.56]),
    (('junk',), None)
])
def test_round_(case, expected):
    assert pyd.round_(*case) == expected


@parametrize('case', [
    pyd.curve
])
def test_round__aliases(case):
    assert pyd.round_ is case


@parametrize('case,expected', [
    (([2, 5, 10], 1), [0.2, 0.5, 1]),
    (([1, 2, 5], 1), [0.2, 0.4, 1]),
    (([1, 2, 5], 5), [1, 2, 5]),
    (([1, 2, 5],), [0.2, 0.4, 1]),
])
def test_scale(case, expected):
    assert pyd.scale(*case) == expected


@parametrize('case,expected', [
    (([0, 0], [5, 5]), 1),
    (([0, 0], [1, 10]), 10),
    (([0, 0], [0, 10]), float('inf')),
    (([0, 0], [10, 0]), 0),
])
def test_slope(case, expected):
    assert pyd.slope(*case) == expected


@parametrize('case,expected', [
    ([1, 2, 3], (2.0 / 3.0) ** 0.5),
])
def test_std_deviation(case, expected):
    assert pyd.std_deviation(case) == expected


@parametrize('case', [
    pyd.sigma
])
def test_std_deviation_aliases(case):
    assert pyd.std_deviation is case


@parametrize('case,expected', [
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 4, 7], [2, 5, 8], [3, 6, 9]]),
])
def test_transpose(case, expected):
    assert pyd.transpose(case) == expected


@parametrize('case,expected', [
    ([1, 2, 3], 2.0 / 3.0),
])
def test_variance(case, expected):
    assert pyd.variance(case) == expected


@parametrize('case,expected', [
    (([1, 2, 3],), [-1.225, 0.0, 1.225]),
    (([{'a': 1}, {'a': 2}, {'a': 3}], 'a'), [-1.225, 0.0, 1.225]),
])
def test_zscore(case, expected):
    assert pyd.map_(pyd.zscore(*case), lambda v: round(v, 3)) == expected
