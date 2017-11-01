# -*- coding: utf-8 -*-

import time

import pydash as _

import pytest

from .fixtures import parametrize


@parametrize('case,expected', [
    ((lambda a, b: a / b, 4, 2), 2)
])
def test_attempt(case, expected):
    assert _.attempt(*case) == expected


@parametrize('case,expected', [
    ((lambda a, b: a / b, 4, 0), ZeroDivisionError)
])
def test_attempt_exception(case, expected):
    assert isinstance(_.attempt(*case), expected)


@parametrize('pairs,case,expected', [
    (([_.matches({'b': 2}), _.constant('matches B')],
      [_.matches({'a': 1}), _.constant('matches A')]),
     {'a': 1, 'b': 2},
     'matches B'),
    (([_.matches({'b': 2}), _.constant('matches B')],
      [_.matches({'a': 1}), _.invert]),
     {'a': 1, 'b': 3},
     {1: 'a', 3: 'b'}),
    (([_.matches({'a': 1}), _.constant('matches A')],
      [_.matches({'b': 2}), _.constant('matches B')]),
     {'a': 1, 'b': 2},
     'matches A')
])
def test_cond(pairs, case, expected):
    func = _.cond(*pairs)
    assert func(case) == expected


@parametrize('case,expected', [
    ([_.matches({'b': 2})], ValueError),
    ([_.matches({'b': 2}), _.matches({'a': 1}), _.constant('matches B')],
     ValueError),
    ([1, 2], ValueError),
    ([[1, 2]], TypeError),
    ([_.matches({'b': 2}), 2], ValueError)
])
def test_cond_exception(case, expected):
    with pytest.raises(expected):
        _.cond(case)


@parametrize('source,case,expected', [
    ({'a': lambda n: n == 0, 'b': lambda n: n < 0},
     {'a': 0, 'b': -1},
     True),
    ({'a': lambda n: n == 0, 'b': lambda n: n < 0},
     {'a': 1, 'b': -1},
     False),
    ({'a': lambda n: n == 0, 'b': lambda n: n < 0},
     {'a': 0, 'b': 1},
     False),
    ({'b': lambda n: n > 1},
     {'b': 2},
     True),
    ({'b': lambda n: n > 1},
     {'b': 0},
     False),
    ([lambda n: n == 0, lambda n: n < 1],
     [0, -1],
     True),
    ([lambda n: n == 0, lambda n: n < 1],
     [1, -1],
     False),
    ([lambda n: n == 0, lambda n: n < 1],
     [0, 1],
     False),
])
def test_conforms(source, case, expected):
    func = _.conforms(source)
    assert func(case) == expected


@parametrize('source,case,expected', [
    ({'a': lambda n: n == 0, 'b': lambda n: n < 0},
     {'a': 0, 'b': -1},
     True),
    ({'a': lambda n: n == 0, 'b': lambda n: n < 0},
     {'a': 1, 'b': -1},
     False),
    ({'a': lambda n: n == 0, 'b': lambda n: n < 0},
     {'a': 0, 'b': 1},
     False),
    ({'b': lambda n: n > 1},
     {'b': 2},
     True),
    ({'b': lambda n: n > 1},
     {'b': 0},
     False),
    ([lambda n: n == 0, lambda n: n < 1],
     [0, -1],
     True),
    ([lambda n: n == 0, lambda n: n < 1],
     [1, -1],
     False),
    ([lambda n: n == 0, lambda n: n < 1],
     [0, 1],
     False),
])
def test_conforms_to(source, case, expected):
    assert _.conforms_to(case, source) == expected


@parametrize('case', [
    'foo',
    'bar'
])
def test_constant(case):
    assert _.constant(case)() == case


@parametrize('case,expected', [
    (([1, 10]), 1),
    (([None, 10]), 10),
    (([[1, 2], [3, 4]]), [1, 2]),
    (([None, [3, 4]]), [3, 4])
])
def test_default_to(case, expected):
    assert _.default_to(*case) == expected


@parametrize('case,expected', [
    ((1,), 1),
    ((1, 2), 1),
    ((), None)
])
def test_identity(case, expected):
    assert _.identity(*case) == expected


@parametrize('case,arg,expected', [
    ('name',
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     ['fred', 'barney']),
    ('friends.1',
     [{'name': 'fred', 'age': 40, 'friends': ['barney', 'betty']},
      {'name': 'barney', 'age': 36, 'friends': ['fred', 'wilma']}],
     ['betty', 'wilma']),
    (['friends.1'],
     [{'name': 'fred', 'age': 40, 'friends.1': 'betty'},
      {'name': 'barney', 'age': 36, 'friends.1': 'wilma'}],
     ['betty', 'wilma']),
    ({'name': 'fred'},
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     [True, False]),
    (lambda obj: obj['age'],
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     [40, 36]),
    (None,
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}]),
    (['name', 'fred'],
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     [True, False]),
    (1, [[0, 1], [2, 3], [4, 5]], [1, 3, 5]),
    (('a', 'b.c', ['d', 0, 'f']),
     [{'a': 1, 'b': {'c': 2}, 'd': [{'f': 3}, 4]}],
     [[1, 2, 3]]),
    (('a',),
     [{'a': 1}],
     [[1]]),
])
def test_iteratee(case, arg, expected):
    getter = _.iteratee(case)
    assert _.map_(arg, getter) == expected


@parametrize('case,arg,expected', [
    ({'age': 36}, {'name': 'barney', 'age': 36}, True),
    ({'age': 36}, {'name': 'barney', 'age': 40}, False),
    ({'a': {'b': 2}}, {'a': {'b': 2, 'c': 3}}, True),
])
def test_matches(case, arg, expected):
    assert _.matches(case)(arg) is expected


@parametrize('case,arg,expected', [
    (('a', 1), {'a': 1, 'b': 2}, True),
    (('a', 2), {'a': 1, 'b': 2}, False),
    ((1, 2), [1, 2, 3], True),
    ((1, 3), [1, 2, 3], False),
])
def test_matches_property(case, arg, expected):
    assert _.matches_property(*case)(arg) is expected


@parametrize('case,args,kargs,key', [
    ((lambda a, b: a + b,), (1, 2), {}, '(1, 2){}'),
    ((lambda a, b: a + b,), (1,), {'b': 2}, "(1,){'b': 2}"),
    ((lambda a, b: a + b, lambda a, b: a * b), (1, 2), {}, 2),
    ((lambda a, b: a + b, lambda a, b: a * b), (1,), {'b': 2}, 2),
])
def test_memoize(case, args, kargs, key):
    memoized = _.memoize(*case)
    expected = case[0](*args, **kargs)
    assert memoized(*args, **kargs) == expected
    assert memoized.cache
    assert memoized.cache[key] == expected


@parametrize('case,args,kargs,expected', [
    (('a.b',), ({'a': {'b': lambda x, y: x + y}}, 1, 2), {}, 3),
    (('a.b',), ({'a': {'b': lambda x, y: x + y}}, 1,), {'y': 2}, 3),
    (('a.b', 1), ({'a': {'b': lambda x, y: x + y}}, 2,), {}, 3),
])
def test_method(case, args, kargs, expected):
    assert _.method(*case)(*args, **kargs) == expected


@parametrize('case,args,kargs,expected', [
    (({'a': {'b': lambda x, y: x + y}},), ('a.b', 1, 2), {}, 3),
    (({'a': {'b': lambda x, y: x + y}},), ('a.b', 1,), {'y': 2}, 3),
])
def test_method_of(case, args, kargs, expected):
    assert _.method_of(*case)(*args, **kargs) == expected


@parametrize('case,expected', [
    ((), None),
    ((1, 2, 3), None)
])
def test_noop(case, expected):
    assert _.noop(*case) == expected


@parametrize('args,pos,expected', [
    ([11, 22, 33, 44], 0, 11),
    ([11, 22, 33, 44], -1, 44),
    ([11, 22, 33, 44], -4, 11),
    ([11, 22, 33, 44], -5, None),
    ([11, 22, 33, 44], 4, None),
    ([11, 22, 33], '1', 22),
    ([11, 22, 33], 'xyz', 11),
    ([11, 22, 33], 1.45, 33),
    ([11, 22, 33], 1.51, 33)
])
def test_nth_arg(args, pos, expected):
    func = _.nth_arg(pos)
    assert func(*args) == expected


def test_now():
    present = int(time.time() * 1000)
    # Add some leeway when comparing time.
    assert (present - 1) <= _.now() <= (present + 1)


@parametrize('funcs,data,expected', [
    ([max, min], [1, 2, 3, 4], [4, 1])
])
def test_over(funcs, data, expected):
    assert _.over(funcs)(*data) == expected


@parametrize('funcs,data,expected', [
    ([lambda x: x is not None, bool], [1], True),
    ([lambda x: x is None, bool], [1], False)
])
def test_over_every(funcs, data, expected):
    assert _.over_every(funcs)(*data) == expected


@parametrize('funcs,data,expected', [
    ([lambda x: x is not None, bool], [1], True),
    ([lambda x: x is None, bool], [1], True),
    ([lambda x: x is False, lambda y: y == 2], [True], False)
])
def test_over_some(funcs, data, expected):
    assert _.over_some(funcs)(*data) == expected


@parametrize('case,arg,expected', [
    ('name',
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     ['fred', 'barney']),
    ('name',
     [{'name': 'fred', 'age': 40},
      {'name': 'barney', 'age': 36}],
     ['fred', 'barney']),
    ('spouse.name',
     [{'name': 'fred', 'age': 40, 'spouse': {'name': 'wilma'}},
      {'name': 'barney', 'age': 36, 'spouse': {'name': 'betty'}}],
     ['wilma', 'betty'])
])
def test_property_(case, arg, expected):
    assert _.map_(arg, _.property_(case)) == expected


@parametrize('case,arg,expected', [
    ({'name': 'fred', 'age': 40}, ['name', 'age'], ['fred', 40]),
])
def test_property_of(case, arg, expected):
    assert _.map_(arg, _.property_of(case)) == expected


@parametrize('case,minimum,maximum', [
    ((), 0, 1),
    ((25,), 0, 25),
    ((5, 10), 5, 10)
])
def test_random(case, minimum, maximum):
    for x in range(50):
        rnd = _.random(*case)
        assert isinstance(rnd, int)
        assert minimum <= rnd <= maximum


@parametrize('case,floating,minimum,maximum', [
    ((), True, 0, 1),
    ((25,), True, 0, 25),
    ((5, 10), True, 5, 10),
    ((5.0, 10), False, 5, 10),
    ((5, 10.0), False, 5, 10),
    ((5.0, 10.0), False, 5, 10),
    ((5.0, 10.0), True, 5, 10),
])
def test_random_float(case, floating, minimum, maximum):
    for x in range(50):
        rnd = _.random(*case, floating=floating)
        assert isinstance(rnd, float)
        assert minimum <= rnd <= maximum


@parametrize('case,expected', [
    ((10,), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ((1, 11), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    ((11, 1), [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]),
    ((11, 1, -2), [11, 9, 7, 5, 3]),
    ((11, 1, 2), []),
    ((0, 30, 5), [0, 5, 10, 15, 20, 25]),
    ((0, -10, -1), [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]),
    ((0,), []),
    ((), []),
])
def test_range_(case, expected):
    assert list(_.range_(*case)) == expected


@parametrize('case,expected', [
    ((4,), [3, 2, 1, 0]),
    ((-4,), [-3, -2, -1, 0]),
    ((1, 5), [4, 3, 2, 1]),
    ((0, 20, 5), [15, 10, 5, 0]),
    ((0, -20, -5), [-15, -10, -5, -0]),
    ((0, -4, -1), [-3, -2, -1, 0]),
    ((1, 10), [9, 8, 7, 6, 5, 4, 3, 2, 1]),
    ((-1, 10), [9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1]),
    ((-1, -10), [-9, -8, -7, -6, -5, -4, -3, -2, -1]),
    ((1, 10, 2), [9, 7, 5, 3, 1]),
    ((1, 10, -2), []),
    ((-1, 10, 2), [9, 7, 5, 3, 1, -1]),
    ((-1, 10, -2), []),
    ((-1, -10, 2), []),
    ((-1, -10, -2), [-9, -7, -5, -3, -1]),
    ((10, 1), [2, 3, 4, 5, 6, 7, 8, 9, 10]),
    ((-10, 1), [0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10]),
    ((-10, -1), [-2, -3, -4, -5, -6, -7, -8, -9, -10]),
    ((10, 1, 2), []),
    ((10, 1, -2), [2, 4, 6, 8, 10]),
    ((-10, 1, 2), [0, -2, -4, -6, -8, -10]),
    ((-10, 1, -2), []),
    ((-10, -1, 2), [-2, -4, -6, -8, -10]),
    ((-10, -1, -2), []),
    ((1, 4, 0), [1, 1, 1]),
    ((0,), []),
    ((10,), [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]),
    ((1, 5), [4, 3, 2, 1]),
    ((0, 20, 5), [15, 10, 5, 0]),
    ((0, -4, -1), [-3, -2, -1, 0]),
    ((0,), []),
    ((), []),
])
def test_range_right(case, expected):
    assert list(_.range_right(*case)) == expected


@parametrize('case,expected', [
    (({'cheese': 'crumpets', 'stuff': lambda: 'nonsense'}, 'cheese'),
     'crumpets'),
    (({'cheese': 'crumpets', 'stuff': lambda: 'nonsense'}, 'stuff'),
     'nonsense'),
    (({'cheese': 'crumpets', 'stuff': lambda: 'nonsense'}, 'foo'),
     None),
    ((False, 'foo'), None),
    ((False, 'foo', 'default'), 'default'),
])
def test_result(case, expected):
    assert _.result(*case) == expected


@parametrize('case,expected', [
    (_.times(2, _.stub_list), [[], []]),
    (_.stub_list(), [])
])
def test_stub_list(case, expected):
    assert case == expected


@parametrize('case,expected', [
    (_.times(2, _.stub_dict), [{}, {}]),
    (_.stub_dict(), {})
])
def test_stub_dict(case, expected):
    assert case == expected


@parametrize('case,expected', [
    (_.times(2, _.stub_false), [False, False]),
    (_.stub_false(), False)
])
def test_stub_false(case, expected):
    assert case == expected


@parametrize('case,expected', [
    (_.times(2, _.stub_string), ['', '']),
    (_.stub_string(), '')
])
def test_stub_string(case, expected):
    assert case == expected


@parametrize('case,expected', [
    (_.times(2, _.stub_true), [True, True]),
    (_.stub_true(), True)
])
def test_stub_true(case, expected):
    assert case == expected


@parametrize('case,expected', [
    ((5, lambda i: i * i), [0, 1, 4, 9, 16])
])
def test_times(case, expected):
    assert _.times(*case) == expected


@parametrize('case,expected', [
    ('a.b.c', ['a', 'b', 'c']),
    ('a[0].b.c', ['a', 0, 'b', 'c']),
    ('a[0][1][2].b.c', ['a', 0, 1, 2, 'b', 'c'])
])
def test_to_path(case, expected):
    assert _.to_path(case) == expected


def test_unique_id_setup():
    _.utilities.ID_COUNTER = 0


@parametrize('case,expected', [
    ((), '1'),
    (('foo',), 'foo2')
])
def test_unique_id(case, expected):
    assert _.unique_id(*case) == expected
