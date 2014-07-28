
import pydash as pyd

from . import fixtures
from .fixtures import parametrize


@parametrize('case,expected', [
    (({'name': 'fred'}, {'employer': 'slate'}),
     {'name': 'fred', 'employer': 'slate'}),
    (({'name': 'fred'}, {'employer': 'slate'}, {'employer': 'medium'}),
     {'name': 'fred', 'employer': 'medium'}),
    (({'name': 'fred'}, {'age': 26}, lambda obj, src: src + 1),
     {'name': 'fred', 'age': 27}),
])
def test_assign(case, expected):
    assert pyd.assign(*case) == expected


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, ['a', 'b', 'c'])
])
def test_keys(case, expected):
    assert set(pyd.keys(case)) == set(expected)


@parametrize('case,expected', [
    (({'a': 1, 'b': 2, 'c': 3}, lambda num, *args: num * 3),
     {'a': 3, 'b': 6, 'c': 9}),
    (({'fred': {'name': 'fred', 'age': 40},
       'pebbles': {'name': 'pebbles', 'age': 1}},
      'age'),
     {'fred': 40, 'pebbles': 1})
])
def test_map_values(case, expected):
    assert pyd.map_values(*case) == expected


@parametrize('case,expected', [
    (({'a': 1, 'b': 2, 'c': 3}, 'a'), {'b': 2, 'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, 'a', 'b'), {'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a', 'b']), {'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a'], ['b']), {'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, lambda value, key, *args: key in ['a']),
     {'b': 2, 'c': 3}),
])
def test_omit(case, expected):
    assert pyd.omit(*case) == expected


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, [['a', 1], ['b', 2], ['c', 3]]),
])
def test_paris(case, expected):
    assert dict(pyd.pairs(case)) == dict(expected)


@parametrize('case,expected', [
    (({'a': 1, 'b': 2, 'c': 3}, 'a'), {'a': 1}),
    (({'a': 1, 'b': 2, 'c': 3}, 'a', 'b'), {'a': 1, 'b': 2}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a', 'b']), {'a': 1, 'b': 2}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a'], ['b']), {'a': 1, 'b': 2}),
    (({'a': 1, 'b': 2, 'c': 3}, lambda value, key, *args: key in ['a']),
     {'a': 1}),
])
def test_pick(case, expected):
    assert pyd.pick(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], lambda acc, value, key, obj: acc.append((key, value))),
     [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]),
    (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], fixtures.transform_callback0),
     [1, 9, 25]),
    (([1, 2, 3, 4, 5],), [])
])
def test_transform(case, expected):
    assert pyd.transform(*case) == expected


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, [1, 2, 3])
])
def test_values(case, expected):
    assert set(pyd.values(case)) == set(expected)
