# -*- coding: utf-8 -*-

import math
import warnings

import pydash as _
from .fixtures import parametrize


@parametrize('case,expected', [
    ((), []),
    (([],), []),
    (([1, 2, 3],), [1, 2, 3]),
    (([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6]),
    (([1, 2, 3], [4, 5, 6], [7]), [1, 2, 3, 4, 5, 6, 7]),
    ((1, [2], 3, 4), [1, 2, 3, 4]),
])
def test_cat(case, expected):
    assert _.cat(*case) == expected


@parametrize('alias', [
    _.concat
])
def test_cat_aliases(alias):
    _.cat is alias


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5],), [[1], [2], [3], [4], [5]]),
    (([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]),
    (([1, 2, 3, 4, 5], 3), [[1, 2, 3], [4, 5]]),
    (([1, 2, 3, 4, 5], 4), [[1, 2, 3, 4], [5]]),
    (([1, 2, 3, 4, 5], 5), [[1, 2, 3, 4, 5]]),
    (([1, 2, 3, 4, 5], 6), [[1, 2, 3, 4, 5]]),
])
def test_chunk(case, expected):
    assert _.chunk(*case) == expected


@parametrize('case,expected', [
    ([0, 1, 2, 3], [1, 2, 3]),
    ([True, False, None, True, 1, 'foo'], [True, True, 1, 'foo'])
])
def test_compact(case, expected):
    assert _.compact(case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4], [2, 4], [3, 5, 6]), [1])
])
def test_difference(case, expected):
    assert _.difference(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5],), [2, 3, 4, 5]),
    (([1, 2, 3, 4, 5], 1), [2, 3, 4, 5]),
    (([1, 2, 3, 4, 5], 2), [3, 4, 5]),
    (([1, 2, 3, 4, 5], 5), []),
    (([1, 2, 3, 4, 5], 6), []),
])
def test_drop(case, expected):
    assert _.drop(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], lambda item: item < 3), [3, 4, 5]),
])
def test_drop_while(case, expected):
    assert _.drop_while(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5],), [1, 2, 3, 4]),
    (([1, 2, 3, 4, 5], 1), [1, 2, 3, 4]),
    (([1, 2, 3, 4, 5], 2), [1, 2, 3]),
    (([1, 2, 3, 4, 5], 5), []),
    (([1, 2, 3, 4, 5], 6), []),
])
def test_drop_right(case, expected):
    assert _.drop_right(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], lambda item: item > 3), [1, 2, 3]),
])
def test_drop_right_while(case, expected):
    assert _.drop_right_while(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 2, 1, 5, 6, 5, 5, 5],), [2, 1, 5]),
    ((['A', 'b', 'C', 'a', 'B', 'c'], lambda letter: letter.lower()),
     ['a', 'B', 'c'])
])
def test_duplicates(case, expected):
    assert _.duplicates(*case) == expected


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
    assert _.every(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 0), [0, 0, 0, 0, 0]),
    (([1, 2, 3, 4, 5], 0, 2), [1, 2, 0, 0, 0]),
    (([1, 2, 3, 4, 5], 0, 2, 3), [1, 2, 0, 4, 5]),
    (([1, 2, 3, 4, 5], 0, 0, 5), [0, 0, 0, 0, 0]),
    (([1, 2, 3, 4, 5], 0, 0, 8), [0, 0, 0, 0, 0]),
    (([1, 2, 3, 4, 5], 0, 0, -1), [0, 0, 0, 0, 5]),
])
def test_fill(case, expected):
    array = case[0]
    assert _.fill(*case) == expected
    assert array == expected


@parametrize('case,filter_by,expected', [
    (['apple', 'banana', 'beet'], lambda item: item.startswith('b'), 1),
    ([{'name': 'apple', 'type': 'fruit'},
      {'name': 'banana', 'type': 'fruit'},
      {'name': 'beet', 'type': 'vegetable'}],
     {'name': 'banana'},
     1),
    (['apple', 'banana', 'beet'], lambda: False, -1)
])
def test_find_index(case, filter_by, expected):
    assert _.find_index(case, filter_by) == expected


@parametrize('case,filter_by,expected', [
    (['apple', 'banana', 'beet'], lambda item: item.startswith('b'), 2),
    ([{'name': 'apple', 'type': 'fruit'},
      {'name': 'banana', 'type': 'fruit'},
      {'name': 'beet', 'type': 'vegetable'}],
     {'type': 'fruit'},
     1),
    (['apple', 'banana', 'beet'], lambda: False, -1)
])
def test_find_last_index(case, filter_by, expected):
    assert _.find_last_index(case, filter_by) == expected


@parametrize('case,expected', [
    ([1, 2, 3], 1),
    ([], None)
])
def test_first(case, expected):
    assert _.first(case) == expected


@parametrize('case,expected', [
    (([1, ['2222'], [3, [[4]]]],), [1, '2222', 3, [[4]]]),
    (([1, ['2222'], [3, [[4]]]], True), [1, '2222', 3, 4]),
])
def test_flatten(case, expected):
    assert _.flatten(*case) == expected


@parametrize('case,expected', [
    ([1, ['2222'], [3, [[4]]]], [1, '2222', 3, 4]),
])
def test_flatten_deep(case, expected):
    assert _.flatten_deep(case) == expected


@parametrize('case,value,from_index,expected', [
    ([1, 2, 3, 1, 2, 3], 2, 0, 1),
    ([1, 2, 3, 1, 2, 3], 2, 3, 4),
    ([1, 1, 2, 2, 3, 3], 2, True, 2),
    ([1, 1, 2, 2, 3, 3], 4, 0, -1),
    ([1, 1, 2, 2, 3, 3], 2, 10, -1),
    ([1, 1, 2, 2, 3, 3], 0, 0, -1),
])
def test_index_of(case, value, from_index, expected):
    assert _.index_of(case, value, from_index) == expected


@parametrize('case,expected', [
    ([1, 2, 3], [1, 2]),
    ([1], [])
])
def test_initial(case, expected):
    assert _.initial(case) == expected


@parametrize('case,expected', [
    (([[10, 20], [30, 40], [50, 60]], [1, 2, 3]),
     [10, 20, 1, 2, 3, 30, 40, 1, 2, 3, 50, 60]),
    (([[[10, 20]], [[30, 40]], [50, [60]]], [1, 2, 3]),
     [[10, 20], 1, 2, 3, [30, 40], 1, 2, 3, 50, [60]]),
])
def test_intercalate(case, expected):
    assert _.intercalate(*case) == expected


@parametrize('case,expected', [
    (([1, 2], [3, 4]), [1, 3, 2, 4]),
    (([1, 2], [3, 4], [5, 6]), [1, 3, 5, 2, 4, 6]),
    (([1, 2], [3, 4, 5], [6]), [1, 3, 6, 2, 4, 5]),
    (([1, 2, 3], [4], [5, 6]), [1, 4, 5, 2, 6, 3]),
])
def test_interleave(case, expected):
    assert _.interleave(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [101, 2, 1, 10], [2, 1]), [1, 2])
])
def test_intersection(case, expected):
    assert _.intersection(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4], 10), [1, 10, 2, 10, 3, 10, 4]),
    (([1, 2, 3, 4], [0, 0, 0]), [1, [0, 0, 0], 2, [0, 0, 0], 3, [0, 0, 0], 4]),
    (([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [0, 0, 0]),
     [[1, 2, 3], [0, 0, 0], [4, 5, 6], [0, 0, 0], [7, 8, 9]]),
])
def test_intersperse(case, expected):
    assert _.intersperse(*case) == expected


@parametrize('case,expected', [
    ([1, 2, 3], 3),
    ([], None)
])
def test_last(case, expected):
    assert _.last(case) == expected


@parametrize('case,value,from_index,expected', [
    ([1, 2, 3, 1, 2, 3], 2, 0, -1),
    ([1, 2, 3, 1, 2, 3], 2, 3, 1),
    ([1, 2, 3, 1, 2, 3], 0, 0, -1),
    ([0, 1, 2, 3, 4, 5], 3, 0, -1),
    ([0, 1, 2, 3, 4, 5], 3, 1, -1),
    ([0, 1, 2, 3, 4, 5], 3, 2, -1),
    ([0, 1, 2, 3, 4, 5], 3, 3, 3),
    ([0, 1, 2, 3, 4, 5], 3, 4, 3),
    ([0, 1, 2, 3, 4, 5], 3, 5, 3),
    ([0, 1, 2, 3, 4, 5], 3, 6, 3),
    ([0, 1, 2, 3, 4, 5], 3, -1, 3),
    ([0, 1, 2, 3, 4, 5], 3, -2, 3),
    ([0, 1, 2, 3, 4, 5], 3, -3, 3),
    ([0, 1, 2, 3, 4, 5], 3, -4, -1),
    ([0, 1, 2, 3, 4, 5], 3, -5, -1),
    ([0, 1, 2, 3, 4, 5], 3, -6, -1),
    ([0, 1, 2, 3, 4, 5], 3, None, 3),
])
def test_last_index_of(case, value, from_index, expected):
    assert _.last_index_of(case, value, from_index) == expected


@parametrize('case,expected', [
    (([1, 2, None, 4, None, 6],
      lambda x, i: ['{0}'.format(i)] if x is None else []),
     ['2', '4'])
])
def test_mapcat(case, expected):
    assert _.mapcat(*case) == expected


@parametrize('case,expected,after', [
    (([1, 2, 3],), 3, [1, 2]),
    (([1, 2, 3], 0), 1, [2, 3]),
    (([1, 2, 3], 1), 2, [1, 3]),
])
def test_pop(case, expected, after):
    array = case[0]
    assert _.pop(*case) == expected
    assert array == after


@parametrize('case,values,expected', [
    ([1, 2, 3, 1, 2, 3], [2, 3], [1, 1])
])
def test_pull(case, values, expected):
    assert _.pull(case, *values) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 1, 2, 3], [2, 3]), [1, 2, 2, 3]),
    (([1, 2, 3, 1, 2, 3], [3, 2]), [1, 2, 2, 3]),
    (([1, 2, 3, 1, 2, 3], 3, 2), [1, 2, 2, 3])
])
def test_pull_at(case, expected):
    assert _.pull_at(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3], 4), [1, 2, 3, 4]),
    (([1, 2, 3], 4, 5), [1, 2, 3, 4, 5]),
    (([1, 2, 3], [4, 5], 6, [7, 8]), [1, 2, 3, [4, 5], 6, [7, 8]]),
])
def test_push(case, expected):
    assert _.push(*case) == expected


@parametrize('alias', [
    _.append
])
def test_push_aliases(alias):
    _.push is alias


@parametrize('case,filter_by,expected', [
    ([1, 2, 3, 4, 5, 6], lambda x: x % 2 == 0, [2, 4, 6]),
    ([1, 2, 3, 4], lambda x: x >= 3, [3, 4]),
])
def test_remove(case, filter_by, expected):
    original = list(case)
    assert _.remove(case, filter_by) == expected
    assert set(case).intersection(expected) == set([])
    assert set(original) == set(case + expected)


@parametrize('case,expected', [
    ([1, 2, 3], [2, 3]),
    ([], [])
])
def test_rest(case, expected):
    assert _.rest(case) == expected


@parametrize('alias', [
    _.tail
])
def test_rest_aliases(alias):
    _.rest is alias


@parametrize('case,expected', [
    ([1, 2, 3, 4], [4, 3, 2, 1]),
    ('abcdef', 'fedcba'),
])
def test_reverse(case, expected):
    assert _.reverse(case) == expected


@parametrize('case,expected,after', [
    ([1, 2, 3], 1, [2, 3]),
])
def test_shift(case, expected, after):
    assert _.shift(case) == expected
    assert case == after


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 0, 1), [1]),
    (([1, 2, 3, 4, 5], 1, 3), [2, 3]),
    (([1, 2, 3, 4, 5], 1, 4), [2, 3, 4]),
    (([1, 2, 3, 4, 5], 1, 5), [2, 3, 4, 5]),
    (([1, 2, 3, 4, 5], 0, -1), [1, 2, 3, 4]),
    (([1, 2, 3, 4, 5], 2), [3]),
    (([1, 2, 3, 4, 5], -1), [5]),
    (([1, 2, 3, 4, 5], -2), [4]),
    (([1, 2, 3, 4, 5], -3), [3]),
    (([1, 2, 3, 4, 5], -5), [1]),
])
def test_slice_(case, expected):
    assert _.slice_(*case) == expected


@parametrize('case,expected', [
    (([2, 1, 3, 4, 6, 5],), [1, 2, 3, 4, 5, 6]),
    (([2, 1, 3, 4, 6, 5], None, None, True), [6, 5, 4, 3, 2, 1]),
    (([{'v': 2}, {'v': 3}, {'v': 1}], None, lambda x: x['v']),
     [{'v': 1}, {'v': 2}, {'v': 3}]),
    (([2, 1, 3, 4, 6, 5], lambda a, b: -1 if a > b else 1),
     [6, 5, 4, 3, 2, 1]),
])
def test_sort(case, expected):
    array = case[0]
    assert _.sort(*case) == expected
    assert array == expected


def test_sort_comparison_key_exception():
    raised = False
    try:
        _.sort([], comparison=lambda: None, key=lambda: None)
    except Exception:
        raised = True

    assert raised


@parametrize('case,expected', [
    (([4, 4, 5, 5, 6, 6], 5), 2),
    (([20, 30, 40, 40, 50], 40), 2),
    (([20, 30, 50], 40), 2),
    (([20, 30, 50], 10), 0),
    (([{'x': 20}, {'x': 30}, {'x': 50}], {'x': 40}, 'x'), 2),
    ((['twenty', 'thirty', 'fifty'],
      'fourty',
      lambda x: {'twenty': 20, 'thirty': 30, 'fourty': 40, 'fifty': 50}[x]),
     2)
])
def test_sorted_index(case, expected):
    assert _.sorted_index(*case) == expected


@parametrize('case,expected', [
    (([4, 4, 5, 5, 6, 6], 5), 4),
    (([20, 30, 40, 40, 50], 40), 4),
    (([20, 30, 50], 10), 0),
    (([{'x': 20}, {'x': 30}, {'x': 50}], {'x': 40}, 'x'), 2),
    ((['twenty', 'thirty', 'fifty'],
      'fourty',
      lambda x: {'twenty': 20, 'thirty': 30, 'fourty': 40, 'fifty': 50}[x]),
     2)
])
def test_sorted_last_index(case, expected):
    assert _.sorted_last_index(*case) == expected


@parametrize('case,expected,after', [
    (([1, 2, 3], 1, 0, 'splice'), [], [1, 'splice', 2, 3]),
    (([1, 2, 3], 1, 1, 'splice'), [2], [1, 'splice', 3]),
    (([1, 2, 3], 0, 2, 'splice', 'slice', 'dice'), [1, 2],
     ['splice', 'slice', 'dice', 3]),
    (([1, 2, 3], 0), [1, 2, 3], []),
    (([1, 2, 3], 1), [2, 3], [1]),
])
def test_splice(case, expected, after):
    array = case[0]
    assert _.splice(*case) == expected
    assert array == after


@parametrize('case,expected', [
    (('123', 1, 0, 'splice'), '1splice23'),
])
def test_splice_string(case, expected):
    assert _.splice(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4, 5]]),
    (([1, 2, 3, 4, 5], 0), [[], [1, 2, 3, 4, 5]]),
])
def test_split_at(case, expected):
    assert _.split_at(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5],), [1]),
    (([1, 2, 3, 4, 5], 1), [1]),
    (([1, 2, 3, 4, 5], 2), [1, 2]),
    (([1, 2, 3, 4, 5], 5), [1, 2, 3, 4, 5]),
    (([1, 2, 3, 4, 5], 6), [1, 2, 3, 4, 5]),
])
def test_take(case, expected):
    assert _.take(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], lambda item: item < 3), [1, 2]),
])
def test_take_while(case, expected):
    assert _.take_while(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5],), [5]),
    (([1, 2, 3, 4, 5], 1), [5]),
    (([1, 2, 3, 4, 5], 2), [4, 5]),
    (([1, 2, 3, 4, 5], 5), [1, 2, 3, 4, 5]),
    (([1, 2, 3, 4, 5], 6), [1, 2, 3, 4, 5]),
])
def test_take_right(case, expected):
    assert _.take_right(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], lambda item: item > 3), [4, 5]),
])
def test_take_right_while(case, expected):
    assert _.take_right_while(*case) == expected


@parametrize('case,filter_by,expected', [
    ([1, 2, 1, 3, 1], None, [1, 2, 3]),
    ([dict(a=1), dict(a=2), dict(a=1)], None, [dict(a=1), dict(a=2)]),
    ([1, 2, 1.5, 3, 2.5], lambda num: math.floor(num), [1, 2, 3]),
    ([{'name': 'banana', 'type': 'fruit'},
      {'name': 'apple', 'type': 'fruit'},
      {'name': 'beet', 'type': 'vegetable'},
      {'name': 'beet', 'type': 'vegetable'},
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
    assert _.uniq(case, filter_by) == expected


@parametrize('alias', [
    _.unique
])
def test_uniq_aliases(alias):
    assert _.uniq is alias


@parametrize('case,expected', [
    (([1, 2, 3], [101, 2, 1, 10], [2, 1]), [1, 2, 3, 101, 10])
])
def test_union(case, expected):
    assert _.union(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3], 4), [4, 1, 2, 3]),
    (([1, 2, 3], 4, 5), [4, 5, 1, 2, 3]),
    (([1, 2, 3], [4, 5], 6, [7, 8]), [[4, 5], 6, [7, 8], 1, 2, 3]),
])
def test_unshift(case, expected):
    assert _.unshift(*case) == expected
    assert case[0] == expected


@parametrize('case,expected', [
    ([['moe', 30, True], ['larry', 40, False], ['curly', 35, True]],
     [['moe', 'larry', 'curly'], [30, 40, 35], [True, False, True]])
])
def test_unzip(case, expected):
    assert _.unzip(case) == expected


@parametrize('case,expected', [
    (([],), []),
    (([[1, 10, 100], [2, 20, 200]],), [[1, 2], [10, 20], [100, 200]]),
    (([[2, 4, 6], [2, 2, 2]], _.power), [4, 16, 36]),
])
def test_unzip_with(case, expected):
    assert _.unzip_with(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 1, 0, 3, 1, 4], 0, 1), [2, 3, 4])
])
def test_without(case, expected):
    assert _.without(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [5, 2, 1, 4]), [3, 5, 4]),
    (([1, 2, 5], [2, 3, 5], [3, 4, 5]), [1, 4, 5])
])
def test_xor(case, expected):
    assert set(_.xor(*case)) == set(expected)


@parametrize('case,expected', [
    ((['moe', 'larry', 'curly'],
      [30, 40, 35],
      [True, False, True]),
     [['moe', 30, True], ['larry', 40, False], ['curly', 35, True]])
])
def test_zip_(case, expected):
    assert _.zip_(*case) == expected


@parametrize('case,expected', [
    ((['moe', 'larry'], [30, 40]), {'moe': 30, 'larry': 40}),
    (([['moe', 30], ['larry', 40]],), {'moe': 30, 'larry': 40}),
])
def test_zip_object(case, expected):
    assert _.zip_object(*case) == expected


@parametrize('alias', [
    _.object_
])
def test_zip_object_aliases(alias):
    _.zip_object is alias


@parametrize('case,expected', [
    (([1, 2],), [[1], [2]]),
    (([1, 2], [3, 4], _.add), [4, 6]),
])
def test_zip_with(case, expected):
    assert _.zip_with(*case) == expected
