
import pydash as pyd
from pydash.utils import iterate

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


@parametrize('case', [
    pyd.extend
])
def test_assign_aliases(case):
    assert pyd.assign is case


@parametrize('case,args', [
    ({'a': {'d': 1}, 'b': {'c': 2}}, ()),
    ({'a': {'d': 1}, 'b': {'c': 2}}, (False, lambda v: v)),
    ([{'a': {'d': 1}, 'b': {'c': 2}}], ())
])
def test_clone(case, args):
    actual = pyd.clone(case, *args)

    assert actual is not case

    for key, value in iterate(actual):
        assert value is case[key]


@parametrize('case,kargs', [
    ({'a': {'d': 1}, 'b': {'c': 2}}, {}),
    ({'a': {'d': 1}, 'b': {'c': 2}}, {'callback': lambda v: v}),
    ([{'a': {'d': 1}, 'b': {'c': 2}}], {})
])
def test_clone_deep(case, kargs):
    kargs['is_deep'] = True
    actuals = [pyd.clone(case, **kargs),
               pyd.clone_deep(case, callback=kargs.get('callback'))]

    for actual in actuals:
        assert actual is not case

        for key, value in iterate(actual):
            assert value is not case[key]


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, {1: 'a', 2: 'b', 3: 'c'}),
    ([1, 2, 3], {1: 0, 2: 1, 3: 2})
])
def test_invert(case, expected):
    assert pyd.invert(case) == expected


@parametrize('case,expected', [
    (({'name': 'barney'}, {'name': 'fred', 'employer': 'slate'}),
     {'name': 'barney', 'employer': 'slate'}),
])
def test_defaults(case, expected):
    assert pyd.defaults(*case) == expected


@parametrize('case,expected', [
    (({'barney':  {'age': 36, 'blocked': False},
       'fred':    {'age': 40, 'blocked': True},
       'pebbles': {'age': 1,  'blocked': False}},
      lambda obj, *args: obj['age'] < 40), ['pebbles', 'barney']),
])
def test_find_key(case, expected):
    assert pyd.find_key(*case) in expected


@parametrize('case', [
    pyd.find_last_key
])
def test_find_key_aliases(case):
    assert pyd.find_key is case


@parametrize('case,expected', [
    (({'name': 'fred', 'employer': 'slate'}, lambda *args: fixtures.noop),
     {'name': 'fred', 'employer': 'slate'}),
    (({'name': 'fred', 'employer': 'slate'}, lambda *args: False),
     {'name': 'fred', 'employer': 'slate'}),
])
def test_for_in(case, expected):
    assert pyd.for_in(*case) == expected


@parametrize('case', [
    pyd.for_in_right,
    pyd.for_own,
    pyd.for_own_right,
])
def test_for_in_aliases(case):
    assert pyd.for_in is case


@parametrize('case,expected', [
    (({'name': 'fred', 'greet': lambda: 'Hello, world!'},), ['greet']),
])
def test_functions_(case, expected):
    assert pyd.functions_(*case) == expected


@parametrize('case', [
    pyd.methods,
])
def test_functions_aliases(case):
    assert pyd.functions_ is case


@parametrize('case,expected', [
    (({'a': 1, 'b': 2, 'c': 3}, 'b'), True),
])
def test_has(case, expected):
    assert pyd.has(*case) == expected


@parametrize('case,expected', [
    (([1, 2, 3],), True),
])
def test_is_list(case, expected):
    assert pyd.is_list(*case) == expected


@parametrize('case,expected', [
    ((True,), True),
    ((False,), True),
    ((0,), False),
    (('',), False),
])
def test_is_boolean(case, expected):
    assert pyd.is_boolean(*case) == expected


@parametrize('case,expected', [
    ((True,), True),
    ((0,), True),
    ((123.45,), True),
    (('',), True),
    (({},), True),
    (([],), True),
    (('Hello',), False),
    ((['Hello', 'World'],), False),
])
def test_is_empty(case, expected):
    assert pyd.is_empty(*case) == expected


@parametrize('case,expected', [
    ((lambda x: x + 1,), True),
    (('Hello, world!',), False),
])
def test_is_function(case, expected):
    assert pyd.is_function(*case) == expected


@parametrize('case,expected', [
    ((None,), True),
    ((0,), False),
])
def test_is_none(case, expected):
    assert pyd.is_none(*case) == expected


@parametrize('case,expected', [
    (('',), True),
    (('Hello, world!',), True),
])
def test_is_string(case, expected):
    assert pyd.is_string(*case) == expected


@parametrize('case,expected', [
    ((0,), True),
    ((123456789123456789123456789,), True),
    ((123.45,), True),
])
def test_is_number(case, expected):
    assert pyd.is_number(*case) == expected


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, ['a', 'b', 'c']),
    ([1, 2, 3], [0, 1, 2])
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


@parametrize('case,callback,expected', [
    (({'characters': [{'name': 'barney'}, {'name': 'fred'}]},
      {'characters': [{'age': 36}, {'age': 40}]}),
     None,
     {'characters': [{'name': 'barney', 'age': 36},
                     {'name': 'fred', 'age': 40}]}),
    (({'characters': [{'name': 'barney'}, {'name': 'fred'}, {}]},
      {'characters': [{'age': 36}, {'age': 40}]}),
     None,
     {'characters': [{'name': 'barney', 'age': 36},
                     {'name': 'fred', 'age': 40},
                     {}]}),
    (({'characters': [{'name': 'barney'}, {'name': 'fred'}]},
      {'characters': [{'age': 36}, {'age': 40}, {}]}),
     None,
     {'characters': [{'name': 'barney', 'age': 36},
                     {'name': 'fred', 'age': 40},
                     {}]}),
    (({'characters': [{'name': 'barney'}, {'name': 'fred'}]},
      {'characters': [{'age': 36}, {'age': 40}]},
      {'characters': [{'score': 5}, {'score': 7}]}),
     None,
     {'characters': [{'name': 'barney', 'age': 36, 'score': 5},
                     {'name': 'fred', 'age': 40, 'score': 7}]}),
    (({'characters': {'barney': {'age': 36}, 'fred': {'score': 7}}},
      {'characters': {'barney': {'score': 5}, 'fred': {'age': 40}}}),
     None,
     {'characters': {'barney': {'age': 36, 'score': 5},
                     'fred': {'age': 40, 'score': 7}}}),
    (({'characters': {'barney': {'age': 36}, 'fred': {'score': 7}}},
      {'characters': {'barney': [5], 'fred': 7}}),
     None,
     {'characters': {'barney': [5],
                     'fred': 7}}),
    (({'characters': {'barney': {'age': 36}, 'fred': {'score': 7}}},
      {'foo': {'barney': [5], 'fred': 7}}),
     None,
     {'characters': {'barney': {'age': 36}, 'fred': {'score': 7}},
      'foo': {'barney': [5], 'fred': 7}}),
    (({'fruits': ['apple'], 'vegetables': ['beet']},
      {'fruits': ['banana'], 'vegetables': ['carrot']}),
     lambda a, b: a + b if isinstance(a, list) else b,
     {'fruits': ['apple', 'banana'], 'vegetables': ['beet', 'carrot']})
])
def test_merge(case, callback, expected):
    assert pyd.merge(*case, callback=callback) == expected


@parametrize('case,expected', [
    (({'a': 1, 'b': 2, 'c': 3}, 'a'), {'b': 2, 'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, 'a', 'b'), {'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a', 'b']), {'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a'], ['b']), {'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, lambda value, key, *args: key in ['a']),
     {'b': 2, 'c': 3}),
    (([1, 2, 3],), {0: 1, 1: 2, 2: 3})
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
    ({'a': 1, 'b': 2, 'c': 3}, [1, 2, 3]),
    ([1, 2, 3], [1, 2, 3])
])
def test_values(case, expected):
    assert set(pyd.values(case)) == set(expected)
