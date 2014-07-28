
import math

import pydash as pyd
from .fixtures import parametrize


@parametrize('case,expected', [
    ([0, 1, 2, 3], [1, 2, 3]),
    ([True, False, None, True, 1, 'foo'], [True, True, 1, 'foo'])
])
def test_compact(case, expected):
    assert pyd.compact(case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4], [2, 4], [3, 5, 6]), [1])
])
def test_difference(case, expected):
    assert pyd.difference(*case) == expected


@parametrize('case,expected', [
    ([1, 2, 3], [2, 3]),
    ([], [])
])
def test_rest(case, expected):
    assert pyd.rest(case) == expected


@parametrize('alias', [
    pyd.tail,
    pyd.drop,
])
def test_rest_aliases(alias):
    assert pyd.rest is alias


@parametrize('case,filter_by,expected', [
    (['apple', 'banana', 'beet'], lambda item, *args: item.startswith('b'), 1),
    ([{'name': 'apple',  'type': 'fruit'},
      {'name': 'banana', 'type': 'fruit'},
      {'name': 'beet',   'type': 'vegetable'}],
     {'name': 'banana'},
     1)
])
def test_find_index(case, filter_by, expected):
    assert pyd.find_index(case, filter_by) == expected


@parametrize('case,filter_by,expected', [
    (['apple', 'banana', 'beet'], lambda item, *args: item.startswith('b'), 2),
    ([{'name': 'apple',  'type': 'fruit'},
      {'name': 'banana', 'type': 'fruit'},
      {'name': 'beet',   'type': 'vegetable'}],
     {'type': 'fruit'},
     1)
])
def test_find_last_index(case, filter_by, expected):
    assert pyd.find_last_index(case, filter_by) == expected


@parametrize('case,expected', [
    ([1, 2, 3], 1),
    ([], None)
])
def test_first(case, expected):
    assert pyd.first(case) == expected


@parametrize('case,filter_by,expected', [
    ([1, ['2222'], [3, [[4]]]], None, [1, '2222', 3, 4]),
    ([1, ['2222'], [3, [[4]]]], True, [1, '2222', 3, [[4]]]),
    ([{'name': 'curly', 'quotes': ['Oh, a wise guy, eh?', 'Poifect!']},
      {'name': 'moe', 'quotes': ['Spread out!', 'You knucklehead!']}],
     'quotes',
     ['Oh, a wise guy, eh?', 'Poifect!',
      'Spread out!',
      'You knucklehead!'])
])
def test_flatten(case, filter_by, expected):
    assert pyd.flatten(case, filter_by) == expected


@parametrize('case,value,from_index,expected', [
    ([1, 2, 3, 1, 2, 3], 2, 0, 1),
    ([1, 2, 3, 1, 2, 3], 2, 3, 4),
    ([1, 1, 2, 2, 3, 3], 2, True, 2),
    ([1, 1, 2, 2, 3, 3], 4, 0, False),
    ([1, 1, 2, 2, 3, 3], 2, 10, False)
])
def test_index_of(case, value, from_index, expected):
    assert pyd.index_of(case, value, from_index) == expected


@parametrize('case,expected', [
    ([1, 2, 3], [1, 2]),
    ([1], [])
])
def test_initial(case, expected):
    assert pyd.initial(case) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [101, 2, 1, 10], [2, 1]), [1, 2])
])
def test_intersection(case, expected):
    assert pyd.intersection(*case) == expected


@parametrize('case,expected', [
    ([1, 2, 3], 3),
    ([], None)
])
def test_last(case, expected):
    assert pyd.last(case) == expected


@parametrize('case,value,from_index,expected', [
    ([1, 2, 3, 1, 2, 3], 2, 0, 4),
    ([1, 2, 3, 1, 2, 3], 2, 3, 1)
])
def test_last_index_of(case, value, from_index, expected):
    assert pyd.last_index_of(case, value, from_index) == expected


@parametrize('case,values,expected', [
    ([1, 2, 3, 1, 2, 3], [2, 3], [1, 1])
])
def test_pull(case, values, expected):
    assert pyd.pull(case, *values) == expected


@parametrize('case,filter_by,expected', [
    ([1, 2, 3, 4, 5, 6], lambda x, *args: x % 2 == 0, [2, 4, 6])
])
def test_remove(case, filter_by, expected):
    original = list(case)
    assert pyd.remove(case, filter_by) == expected
    assert set(case).intersection(expected) == set([])
    assert set(original) == set(case + expected)


@parametrize('case,expected', [
    ((['moe', 'larry'], [30, 40]), {'moe': 30, 'larry': 40}),
    (([['moe', 30], ['larry', 40]],), {'moe': 30, 'larry': 40}),
])
def test_zip_object(case, expected):
    assert pyd.zip_object(*case) == expected


@parametrize('alias', [
    pyd.object
])
def test_zip_object_aliases(alias):
    pyd.zip_object is alias


@parametrize('case,expected', [
    ((['moe', 'larry', 'curly'],
      [30, 40, 35],
      [True, False, True]),
     [['moe', 30, True], ['larry', 40, False], ['curly', 35, True]])
])
def test_zip_(case, expected):
    assert pyd.zip(*case) == expected


@parametrize('case,expected', [
    ([['moe', 30, True], ['larry', 40, False], ['curly', 35, True]],
     [['moe', 'larry', 'curly'], [30, 40, 35], [True, False, True]])
])
def test_unzip(case, expected):
    pyd.unzip(case) == expected


@parametrize('case,expected', [
    ((10,), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ((1, 11), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    ((0, 30, 5), [0, 5, 10, 15, 20, 25]),
    ((0, -10, -1), [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]),
    ((0,), []),
])
def test_range_(case, expected):
    assert pyd.range(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 1, 0, 3, 1, 4], 0, 1), [2, 3, 4])
])
def test_without(case, expected):
    assert pyd.without(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [5, 2, 1, 4]), [3, 5, 4]),
    (([1, 2, 5], [2, 3, 5], [3, 4, 5]), [1, 4, 5])
])
def test_xor(case, expected):
    assert set(pyd.xor(*case)) == set(expected)


@parametrize('case,filter_by,expected', [
    ([1, 2, 1, 3, 1], None, [1, 2, 3]),
    ([dict(a=1), dict(a=2), dict(a=1)], None, [dict(a=1), dict(a=2)]),
    ([1, 2, 1.5, 3, 2.5], lambda num, *args: math.floor(num), [1, 2, 3]),
    ([{'name': 'banana', 'type': 'fruit'},
      {'name': 'apple', 'type': 'fruit'},
      {'name': 'beet',   'type': 'vegetable'},
      {'name': 'beet',   'type': 'vegetable'},
      {'name': 'carrot', 'type': 'vegetable'},
      {'name': 'carrot', 'type': 'vegetable'}],
     {'type': 'vegetable'},
     [{'name': 'banana', 'type': 'fruit'},
      {'name': 'beet', 'type': 'vegetable'}]),
    ([{'x': 1, 'y': 1}, {'x': 2, 'y': 1}, {'x': 1, 'y': 1}],
     'x',
     [{'x': 1, 'y': 1}, {'x': 2, 'y': 1}]),
    (['A', 'b', 'C', 'a', 'B', 'c'],
     lambda letter: letter.lower(),
     ['A', 'b', 'C'])
])
def test_uniq(case, filter_by, expected):
    assert pyd.uniq(case, filter_by) == expected


@parametrize('alias', [
    pyd.unique
])
def test_uniq_aliases(alias):
    assert pyd.uniq is alias


@parametrize('case,expected', [
    (([1, 2, 3], [101, 2, 1, 10], [2, 1]), [1, 2, 3, 101, 10])
])
def test_union(case, expected):
    assert pyd.union(*case) == expected


@parametrize('case,expected', [
    (([20, 30, 50], 40), 2),
    (([20, 30, 50], 10), 0),
    (([{'x': 20}, {'x': 30}, {'x': 50}], {'x': 40}, 'x'), 2),
    ((['twenty', 'thirty', 'fifty'],
      'fourty',
      lambda x: {'twenty': 20, 'thirty': 30, 'fourty': 40, 'fifty': 50}[x]),
     2)
])
def test_sorted_index(case, expected):
    assert pyd.sorted_index(*case) == expected


@parametrize('case,expected', [
    (([True, 1, None, 'yes'], bool), False),
    (([True, 1, None, 'yes'],), False),
    (([{'name': 'moe', 'age': 40},
       {'name': 'larry', 'age': 50}],
      'age'),
     True),
    (([{'name': 'moe', 'age': 40},
       {'name': 'larry', 'age': 50}],
      {'age': 50}),
     False)
])
def test_every(case, expected):
    assert pyd.every(*case) == expected
