
import math

import pydash as pyd

from . import fixtures
from .fixtures import parametrize


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
    (([1, 2, 3],), 3),
    (({'a': 3, 'b': 2, 'c': 1},), 3),
    ((['anaconda', 'bison', 'camel'], lambda x: len(x)), 'anaconda'),
    (([{'name': 'barney', 'age': 36}, {'name': 'fred',   'age': 40}], 'age',),
     {'name': 'fred', 'age': 40}),
    (([{'name': 'barney', 'age': 36}, {'name': 'fred',   'age': 40}],
      lambda chr: chr['age']),
     {'name': 'fred', 'age': 40}),
])
def test_max_(case, expected):
    assert pyd.max_(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3],), 1),
    (({'a': 3, 'b': 2, 'c': 1},), 1),
    ((['anaconda', 'bison', 'cat'], lambda x: len(x)), 'cat'),
    (([{'name': 'barney', 'age': 36}, {'name': 'fred',   'age': 40}], 'age',),
     {'name': 'barney', 'age': 36}),
    (([{'name': 'barney', 'age': 36}, {'name': 'fred',   'age': 40}],
      lambda chr: chr['age']),
     {'name': 'barney', 'age': 36}),
])
def test_min_(case, expected):
    assert pyd.min_(*case) == expected


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
    (([{'one': 1}, {'one': 1}, {'two': 2}, {'one': 1}], {'one': 1}),
     {True: 3, False: 1}),
    (([{'one': 1}, {'one': 1}, {'two': 2}, {'one': 1}], 'one'),
     {1: 3, None: 1}),
    (({1: 0, 2: 0, 4: 3},), {0: 2, 3: 1})
])
def test_count_by(case, expected):
    assert pyd.count_by(*case) == expected


@parametrize('case,expected', [
    (([0, True, False, None, 1, 2, 3],), [True, 1, 2, 3]),
    (([1, 2, 3, 4, 5, 6], lambda num, *args: num % 2 == 0), [2, 4, 6]),
    (([{'name': 'barney', 'age': 36, 'blocked': False},
       {'name': 'fred',   'age': 40, 'blocked': True}],
      'blocked'),
     [{'name': 'fred', 'age': 40, 'blocked': True}]),
    (([{'name': 'barney', 'age': 36, 'blocked': False},
       {'name': 'fred',   'age': 40, 'blocked': True}],
      {'age': 36}),
     [{'name': 'barney', 'age': 36, 'blocked': False}]),
])
def test_filter_(case, expected):
    assert pyd.filter_(*case) == expected


@parametrize('case,expected', [
    (([{'name': 'barney',  'age': 36, 'blocked': False},
       {'name': 'fred',    'age': 40, 'blocked': True},
       {'name': 'pebbles', 'age': 1,  'blocked': False}],
      lambda c, *args: c['age'] < 40),
     {'name': 'barney', 'age': 36, 'blocked': False}),
    (([{'name': 'barney',  'age': 36, 'blocked': False},
       {'name': 'fred',    'age': 40, 'blocked': True},
       {'name': 'pebbles', 'age': 1,  'blocked': False}],
      {'age': 1}),
     {'name': 'pebbles', 'age': 1, 'blocked': False}),
    (([{'name': 'barney',  'age': 36, 'blocked': False},
       {'name': 'fred',    'age': 40, 'blocked': True},
       {'name': 'pebbles', 'age': 1,  'blocked': False}],
      'blocked'),
     {'name': 'fred', 'age': 40, 'blocked': True}),
    (([{'name': 'barney',  'age': 36, 'blocked': False},
       {'name': 'fred',    'age': 40, 'blocked': True},
       {'name': 'pebbles', 'age': 1,  'blocked': False}],),
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
    (([1, 2, 3], fixtures.noop), [1, 2, 3]),
    (([1, 2, 3], lambda value, *args: value < 2), [1, 2, 3]),
    (({'one': 1, 'two': 2, 'three': 3}, fixtures.noop),
     {'one': 1, 'two': 2, 'three': 3}),
])
def test_for_each(case, expected):
    assert pyd.for_each(*case) == expected


@parametrize('case', [
    pyd.each
])
def test_for_each_aliases(case):
    assert pyd.for_each is case


@parametrize('case,expected', [
    (([1, 2, 3], fixtures.noop), [1, 2, 3]),
    (([1, 2, 3], lambda value, *args: value < 2), [1, 2, 3]),
    (({'one': 1, 'two': 2, 'three': 3}, fixtures.noop),
     {'one': 1, 'two': 2, 'three': 3}),
])
def test_for_each_right(case, expected):
    assert pyd.for_each_right(*case) == expected


@parametrize('case', [
    pyd.each_right
])
def test_for_each_right_aliases(case):
    assert pyd.for_each_right is case


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


@parametrize('case,expected', [
    (([[5, 1, 7], [3, 2, 1]], 'sort'), [None, None]),
    (([[5, 1, 7], [3, 2, 1]], lambda lst: sorted(lst)),
     [[1, 5, 7], [1, 2, 3]]),
    (([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}], 'get', 'a'), [1, 3]),
    (([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}], 'get', 'c'), [None, None]),
    ((['anaconda', 'bison', 'cat'], 'count', 'a'), [3, 0, 1]),
    (([1, 2, 3], lambda item, num: item + num, 1), [2, 3, 4]),
])
def test_invoke(case, expected):
    assert pyd.invoke(*case) == expected


@parametrize('case', [
    [1, 2, 3, 4, 5, 6],
])
def test_sample(case):
    assert pyd.sample(case) in case


@parametrize('case', [
    ([1, 2, 3, 4, 5, 6], 2),
    ([1, 2, 3, 4, 5, 6], 3),
    ([1, 2, 3, 4, 5, 6], 4),
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
def test_reduce_right(case, expected):
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


@parametrize('case,expected', [
    (([0, True, False, None, 1, 2, 3],), [0, False, None]),
    (([1, 2, 3, 4, 5, 6], lambda num, *args: num % 2 == 0), [1, 3, 5]),
    (([{'name': 'barney', 'age': 36, 'blocked': False},
       {'name': 'fred',   'age': 40, 'blocked': True}],
      'blocked'),
     [{'name': 'barney', 'age': 36, 'blocked': False}]),
    (([{'name': 'barney', 'age': 36, 'blocked': False},
       {'name': 'fred',   'age': 40, 'blocked': True}],
      {'age': 36}),
     [{'name': 'fred', 'age': 40, 'blocked': True}]),
])
def test_reject(case, expected):
    assert pyd.reject(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3], lambda x: math.sin(x)), [3, 1, 2]),
    (([
        {'name': 'barney',  'age': 36},
        {'name': 'fred',    'age': 40},
        {'name': 'barney',  'age': 26},
        {'name': 'fred',    'age': 30},
    ], 'age'), [
        {'name': 'barney',  'age': 26},
        {'name': 'fred',    'age': 30},
        {'name': 'barney',  'age': 36},
        {'name': 'fred',    'age': 40},
    ]),
])
def test_sort_by(case, expected):
    assert pyd.sort_by(*case) == expected


@parametrize('case,expected', [
    (('cat',), ['c', 'a', 't']),
])
def test_to_list(case, expected):
    assert pyd.to_list(*case) == expected
