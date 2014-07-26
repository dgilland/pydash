
import math

import pytest

import pydash as pyd
from . import fixtures


# pytest.mark is a generator so create alias for convenience
parametrize = pytest.mark.parametrize


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


@parametrize('case,filter_by,expected,', [
    ([{'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}],
     {'age': 40},
     [{'name': 'moe', 'age': 40}])
])
def test_where(case, filter_by, expected):
    assert pyd.where(case, filter_by) == expected


@parametrize('case,filter_by,expected', [
    ([{'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}],
     'name',
     ['moe', 'larry'])
])
def test_pluck(case, filter_by, expected):
    assert pyd.pluck(case, filter_by) == expected


@parametrize('case,filter_by,expected', [
    ([1, 2, 3], None, [2, 3]),
    ([1, 2, 3], 2, [3]),
    ([1, 2, 3], lambda val, index, lst: val < 3, [3]),
    ([{'name': 'banana', 'organic': True},
      {'name': 'beet',   'organic': False}],
     'organic',
     [{'name': 'beet', 'organic': False}]),
    ([{'name': 'apple',  'type': 'fruit'},
      {'name': 'banana', 'type': 'fruit'},
      {'name': 'beet',   'type': 'vegetable'},
      {'name': 'peach', 'type': 'fruit'}],
     {'type': 'fruit'},
     [{'name': 'beet', 'type': 'vegetable'},
      {'name': 'peach', 'type': 'fruit'}])
])
def test_rest(case, filter_by, expected):
    assert pyd.rest(case, filter_by) == expected


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


@parametrize('case,filter_by,expected', [
    ([1, 2, 3], None, 1),
    ([1, 2, 3], 2, [1, 2]),
    ([1, 2, 3], lambda item, *args: item < 3, [1, 2]),
    ([{'name': 'banana', 'organic': True},
      {'name': 'beet',   'organic': False}],
     'organic',
     [{'name': 'banana', 'organic': True}]),
    ([{'name': 'apple',  'type': 'fruit'},
      {'name': 'banana', 'type': 'fruit'},
      {'name': 'beet',   'type': 'vegetable'},
      {'name': 'peach', 'type': 'fruit'}],
     {'type': 'fruit'},
     [{'name': 'apple', 'type': 'fruit'},
      {'name': 'banana', 'type': 'fruit'}]),
])
def test_first(case, filter_by, expected):
    assert pyd.first(case, filter_by) == expected


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


@parametrize('case,filter_by,expected', [
    ([1, 2, 3], 1, [1, 2]),
    ([1, 2, 3], 2, [1]),
    ([1, 2, 3], lambda num, *args: num > 1, [1]),
    ([{'name': 'beet',   'organic': False},
      {'name': 'carrot', 'organic': True}],
     'organic',
     [{'name': 'beet',   'organic': False}]),
    ([{'name': 'banana', 'type': 'fruit'},
      {'name': 'beet',   'type': 'vegetable'},
      {'name': 'carrot', 'type': 'vegetable'}],
     {'type': 'vegetable'},
     [{'name': 'banana', 'type': 'fruit'}])
])
def test_initial(case, filter_by, expected):
    assert pyd.initial(case, filter_by) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [101, 2, 1, 10], [2, 1]), [1, 2])
])
def test_intersection(case, expected):
    assert pyd.intersection(*case) == expected


@parametrize('case,filter_by,expected', [
    ([1, 2, 3], None, 3),
    ([1, 2, 3], 2, [2, 3]),
    ([1, 2, 3], lambda num, *args: num > 1, [2, 3]),
    ([{'name': 'beet',   'organic': False},
      {'name': 'carrot', 'organic': True}],
     'organic',
     [{'name': 'carrot', 'organic': True}]),
    ([{'name': 'banana', 'type': 'fruit'},
      {'name': 'beet',   'type': 'vegetable'},
      {'name': 'carrot', 'type': 'vegetable'}],
     {'type': 'vegetable'},
     [{'name': 'beet', 'type': 'vegetable'},
      {'name': 'carrot', 'type': 'vegetable'}])
])
def test_last(case, filter_by, expected):
    assert pyd.last(case, filter_by) == expected


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
    pyd.object_
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
    assert pyd.zip_(*case) == expected


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
    assert pyd.range_(*case) == expected


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
     [{'name': 'beet', 'type': 'vegetable'},
      {'name': 'carrot', 'type': 'vegetable'}]),
    ([{'x': 1, 'y': 1},
      {'x': 2, 'y': 1},
      {'x': 1, 'y': 1}],
     'x',
     [{'x': 1, 'y': 1}, {'x': 2, 'y': 1}])
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


@parametrize('case,expected', [
    (([None, 0, 'yes', False], bool), True),
    (([None, 0, 'yes', False],), True),
    (([{'name': 'apple',  'organic': False, 'type': 'fruit'},
       {'name': 'carrot', 'organic': True,  'type': 'vegetable'}],
      'organic'),
     True),
    (([{'name': 'apple',  'organic': False, 'type': 'fruit'},
       {'name': 'carrot', 'organic': True,  'type': 'vegetable'}],
      {'type': 'meat'}),
     False)
])
def test_some(case, expected):
    assert pyd.some(*case) == expected


@parametrize('case,expected,sort_results', [
    (([1, 2, 3],), [1, 2, 3], False),
    (([1, 2, 3], lambda num, *args: num * 3), [3, 6, 9], False),
    (({'one': 1, 'two': 2, 'three': 3}, lambda num, *args: num * 3),
     [3, 6, 9],
     True),
    (([{'name': 'moe', 'age': 40},
       {'name': 'larry', 'age': 50}],
      'name'),
     ['moe', 'larry'],
     False)
])
def test_map_(case, expected, sort_results):
    actual = pyd.map_(*case)
    if sort_results:
        actual = sorted(actual)

    assert actual == expected


@parametrize('case', [
    pyd.collect
])
def test_map_aliases(case):
    assert pyd.map_ is case


@parametrize('case,expected', [
    ((['a', 'b', 'c', 'd', 'e'], [0, 2, 4]), ['a', 'c', 'e']),
    ((['moe', 'larry', 'curly'], 0, 2), ['moe', 'curly']),
    (({'a': 1, 'b': 2, 'c': 3}, 'a', 'b'), [1, 2])
])
def test_at(case, expected):
    assert pyd.at(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3], 1), True),
    (([1, 2, 3], 1, 2), False),
    (({'name': 'fred', 'age': 40}, 'fred'), True),
    (('pebbles', 'eb'), True)
])
def test_contains(case, expected):
    assert pyd.contains(*case) == expected


@parametrize('case,expected', [
    (([4.3, 6.1, 6.4], lambda num, *args: int(math.floor(num))), {4: 1, 6: 2}),
])
def test_count_by(case, expected):
    assert pyd.count_by(*case) == expected


@parametrize('case,expected', [
    (([0, True, False, None, 1, 2, 3],), [True, 1, 2, 3]),
    (([1, 2, 3, 4, 5, 6], lambda num, *args: num % 2 == 0), [2, 4, 6]),
    ((fixtures.data.filter_,
      'blocked'),
     [{'name': 'fred', 'age': 40, 'blocked': True}]),
    ((fixtures.data.filter_,
      {'age': 36}),
     [{'name': 'barney', 'age': 36, 'blocked': False}]),
])
def test_filter_(case, expected):
    assert pyd.filter_(*case) == expected


@parametrize('case,expected', [
    ((fixtures.data.find,
      lambda c, *args: c['age'] < 40),
     {'name': 'barney', 'age': 36, 'blocked': False}),
    ((fixtures.data.find,
      {'age': 1}),
     {'name': 'pebbles', 'age': 1, 'blocked': False}),
    ((fixtures.data.find,
      'blocked'),
     {'name': 'fred', 'age': 40, 'blocked': True}),
    ((fixtures.data.find,),
     {'name': 'barney', 'age': 36, 'blocked': False}),
])
def test_find(case, expected):
    assert pyd.find(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4], lambda num, *args: num % 2 == 1), 3),
])
def test_find_last(case, expected):
    assert pyd.find_last(*case) == expected


@parametrize('case,expected', [
    (([4.2, 6.1, 6.4],
      lambda num, *args: int(math.floor(num))),
     {4: [4.2], 6: [6.1, 6.4]}),
])
def test_group_by(case, expected):
    assert pyd.group_by(*case) == expected


@parametrize('case,expected', [
    (([{'dir': 'left', 'code': 97}, {'dir': 'right', 'code': 100}], 'dir'),
     {'left': {'dir': 'left', 'code': 97},
      'right': {'dir': 'right', 'code': 100}}),
])
def test_index_by(case, expected):
    assert pyd.index_by(*case) == expected


@parametrize('case', [
    fixtures.data.sample,
])
def test_sample(case):
    assert pyd.sample(case) in case


@parametrize('case', [
    (fixtures.data.sample, 2),
    (fixtures.data.sample, 3),
    (fixtures.data.sample, 4),
])
def test_sample_list(case):
    collection, n = case
    sample_n = pyd.sample(*case)

    assert isinstance(sample_n, list)
    assert len(sample_n) == min(n, len(collection))
    assert set(sample_n).issubset(collection)


@parametrize('case', [
    [1, 2, 3, 4, 5, 6]
])
def test_shuffle(case):
    shuffled = pyd.shuffle(case)

    assert set(shuffled) == set(case)
    assert len(shuffled) == len(case)


@parametrize('case', [
    [1, 2, 3, 4, 5],
    {'1': 1, '2': 2, '3': 3}
])
def test_size(case):
    assert pyd.size(case) == len(case)


@parametrize('case,expected', [
    (([1, 2, 3], None), 1),
    (([1, 2, 3], fixtures.reduce_callback0), 6),
    (({'a': 1, 'b': 2, 'c': 3}, fixtures.reduce_callback1, {}),
     {'a': 3, 'b': 6, 'c': 9})
])
def test_reduce(case, expected):
    assert pyd.reduce_(*case) == expected


@parametrize('case,exception', [
    (([],), TypeError)
])
def test_reduce_raise(case, exception):
    raised = False

    try:
        pyd.reduce_(*case)
    except exception:
        raised = True

    assert raised


@parametrize('case', [
    pyd.foldl,
    pyd.inject
])
def test_reduce_aliases(case):
    assert pyd.reduce_ is case


@parametrize('case,expected', [
    (([1, 2, 3], None), 3),
    (([1, 2, 3], fixtures.reduce_callback0), 6),
    (([[0, 1], [2, 3], [4, 5]], fixtures.reduce_right_callback0),
     [4, 5, 2, 3, 0, 1]),
    (({'a': 1, 'b': 2, 'c': 3}, fixtures.reduce_callback1, {}),
     {'a': 3, 'b': 6, 'c': 9})
])
def test_reduce(case, expected):
    assert pyd.reduce_right(*case) == expected


@parametrize('case,exception', [
    (([],), TypeError)
])
def test_reduce_right_raise(case, exception):
    raised = False

    try:
        pyd.reduce_right(*case)
    except exception:
        raised = True

    assert raised


@parametrize('case', [
    pyd.foldr
])
def test_reduce_right_aliases(case):
    assert pyd.reduce_right is case
