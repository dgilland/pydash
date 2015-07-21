# -*- coding: utf-8 -*-

import pydash as _
from .fixtures import parametrize


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5],), 15),
    (([{'b': 4}, {'b': 5}, {'b': 6}], 'b'), 15),
    (([0, 14, 0.2],), 14.2),
    (({'one': {'a': 1}, 'two': {'a': 2}, 'three': {'a': 3}}, 'a'), 6),
    ((5, 3), 8),
])
def test_add(case, expected):
    assert _.add(*case) == expected


@parametrize('case', [
    _.sum_
])
def test_add_aliases(case):
    assert _.add is case


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5],), 3),
    (([{'b': 4}, {'b': 5}, {'b': 6}], 'b'), 5),
    (([0, 0.5, 1],), 0.5),
    (({'one': {'a': 1}, 'two': {'a': 2}, 'three': {'a': 3}}, 'a'), 2),
])
def test_average(case, expected):
    assert _.average(*case) == expected


@parametrize('case', [
    _.avg,
    _.mean
])
def test_average_aliases(case):
    assert _.average is case


@parametrize('case,expected', [
    ((4.006,), 5),
    ((6.004, 2), 6.01),
    ((6040, -2), 6100),
    (([4.006, 6.004], 2), [4.01, 6.01]),
])
def test_ceil(case, expected):
    assert _.ceil(*case) == expected


@parametrize('case,expected', [
    ((4.006,), 4),
    ((0.046, 2), 0.04),
    ((4060, -2), 4000),
    (([4.006, 0.046], 2), [4.0, 0.04]),
])
def test_floor(case, expected):
    assert _.floor(*case) == expected


@parametrize('case,expected', [
    (([0, 0, 0, 0, 5],), 0),
    (([0, 0, 1, 2, 5],), 1),
    (([0, 0, 1, 2],), 0.5),
    (([0, 0, 1, 2, 3, 4],), 1.5),
])
def test_median(case, expected):
    assert _.median(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 3), [2, 3, 4]),
    (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3), [2, 3, 4, 5, 6, 7, 8, 9]),
    (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4),
     [2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5]),
])
def test_moving_average(case, expected):
    assert _.moving_average(*case) == expected


@parametrize('case', [
    _.moving_avg
])
def test_moving_average_aliases(case):
    assert _.moving_average is case


@parametrize('case,expected', [
    ((2, 3), 8),
    ((3, 4), 81),
    (([1, 2, 3, 4, 5], 2), [1, 4, 9, 16, 25]),
    (('junk', 2), None),
])
def test_power(case, expected):
    assert _.power(*case) == expected


@parametrize('case', [
    _.pow_
])
def test_power_aliases(case):
    assert _.power is case


@parametrize('case,expected', [
    ((2.51,), 3),
    ((2.499,), 2),
    ((2.499, 2), 2.50),
    (([2.5, 2.499, 2.555], 2), [2.50, 2.50, 2.56]),
    (('junk',), None)
])
def test_round_(case, expected):
    assert _.round_(*case) == expected


@parametrize('case', [
    _.curve
])
def test_round_aliases(case):
    assert _.round_ is case


@parametrize('case,expected', [
    (([2, 5, 10], 1), [0.2, 0.5, 1]),
    (([1, 2, 5], 1), [0.2, 0.4, 1]),
    (([1, 2, 5], 5), [1, 2, 5]),
    (([1, 2, 5],), [0.2, 0.4, 1]),
])
def test_scale(case, expected):
    assert _.scale(*case) == expected


@parametrize('case,expected', [
    (([0, 0], [5, 5]), 1),
    (([0, 0], [1, 10]), 10),
    (([0, 0], [0, 10]), float('inf')),
    (([0, 0], [10, 0]), 0),
])
def test_slope(case, expected):
    assert _.slope(*case) == expected


@parametrize('case,expected', [
    ([1, 2, 3], (2.0 / 3.0) ** 0.5),
])
def test_std_deviation(case, expected):
    assert _.std_deviation(case) == expected


@parametrize('case', [
    _.sigma
])
def test_std_deviation_aliases(case):
    assert _.std_deviation is case


@parametrize('case,expected', [
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 4, 7], [2, 5, 8], [3, 6, 9]]),
])
def test_transpose(case, expected):
    assert _.transpose(case) == expected


@parametrize('case,expected', [
    ([1, 2, 3], 2.0 / 3.0),
])
def test_variance(case, expected):
    assert _.variance(case) == expected


@parametrize('case,expected', [
    (([1, 2, 3],), [-1.225, 0.0, 1.225]),
    (([{'a': 1}, {'a': 2}, {'a': 3}], 'a'), [-1.225, 0.0, 1.225]),
])
def test_zscore(case, expected):
    assert _.map_(_.zscore(*case), lambda v: round(v, 3)) == expected
