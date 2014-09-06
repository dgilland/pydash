
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

    for key, value in pyd.utils.iterator(actual):
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

        for key, value in pyd.utils.iterator(actual):
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
    # NOTE: The expected is a list of values but find_key returns only a single
    # value. However, since dicts do not have an order, it's unknown what the
    # "first" returned value will be.
    (({'barney':  {'age': 36, 'blocked': False},
       'fred':    {'age': 40, 'blocked': True},
       'pebbles': {'age': 1,  'blocked': False}},
      lambda obj, *args: obj['age'] < 40),
     ['pebbles', 'barney']),
    (({'barney':  {'age': 36, 'blocked': False},
       'fred':    {'age': 40, 'blocked': True},
       'pebbles': {'age': 1,  'blocked': False}},),
     ['barney', 'fred', 'pebbles']),
    (([1, 2, 3],), [0])
])
def test_find_key(case, expected):
    assert pyd.find_key(*case) in expected


@parametrize('case', [
    pyd.find_last_key
])
def test_find_key_aliases(case):
    assert pyd.find_key is case


@parametrize('case,expected', [
    (({'name': 'fred', 'employer': 'slate'}, fixtures.for_in_callback0),
     ({'name': 'fredfred', 'employer': 'slateslate'},)),
    (({'name': 'fred', 'employer': 'slate'}, fixtures.for_in_callback1),
     ({'name': 'fredfred', 'employer': 'slate'},
      {'name': 'fred', 'employer': 'slateslate'})),
    (([1, 2, 3], fixtures.for_in_callback2), ([False, True, 3],))
])
def test_for_in(case, expected):
    assert pyd.for_in(*case) in expected


@parametrize('case', [
    pyd.for_own
])
def test_for_in_aliases(case):
    assert pyd.for_in is case


@parametrize('case,expected', [
    (({'name': 'fred', 'employer': 'slate'}, fixtures.for_in_callback0),
     ({'name': 'fredfred', 'employer': 'slateslate'},)),
    (({'name': 'fred', 'employer': 'slate'}, fixtures.for_in_callback1),
     ({'name': 'fredfred', 'employer': 'slate'},
      {'name': 'fred', 'employer': 'slateslate'})),
    (([1, 2, 3], fixtures.for_in_callback2), ([1, True, 'index:2'],))
])
def test_for_in_right(case, expected):
    assert pyd.for_in_right(*case) in expected


@parametrize('case', [
    pyd.for_own_right,
])
def test_for_in_right_aliases(case):
    assert pyd.for_in_right is case


@parametrize('case,expected', [
    (({'name': 'fred', 'greet': lambda: 'Hello, world!'},), ['greet']),
    ((['fred', lambda: 'Hello, world!'],), [1]),
])
def test_functions(case, expected):
    assert pyd.functions(*case) == expected


@parametrize('case', [
    pyd.methods,
])
def test_functions_aliases(case):
    assert pyd.functions is case


@parametrize('case,expected', [
    (({'one': {'two': {'three': 4}}}, 'one.two'), {'three': 4}),
    (({'one': {'two': {'three': 4}}}, 'one.two.three'), 4),
    (({'one': {'two': {'three': 4}}}, ['one', 'two']), {'three': 4}),
    (({'one': {'two': {'three': 4}}}, ['one', 'two', 'three']), 4),
    (({'one': {'two': {'three': 4}}}, 'one.four'), None),
    (({'one': {'two': {'three': 4}}}, 'five'), None),
    (({'one': ['two', {'three': [4, 5]}]}, ['one', 1, 'three', 1]), 5),
    (({'one': ['two', {'three': [4, 5]}]}, 'one.[1].three.[1]'), 5),
    (({'one': ['two', {'three': [4, 5]}]}, 'one.1.three.1'), None),
    ((['one', {'two': {'three': [4, 5]}}], '[1].two.three.[0]'), 4),
])
def test_get_path(case, expected):
    assert pyd.get_path(*case) == expected


@parametrize('case,expected', [
    (({'one': {'two': {'three': 4}}}, 'one.two'), True),
    (({'one': {'two': {'three': 4}}}, 'one.two.three'), True),
    (({'one': {'two': {'three': 4}}}, ['one', 'two']), True),
    (({'one': {'two': {'three': 4}}}, ['one', 'two', 'three']), True),
    (({'one': {'two': {'three': 4}}}, 'one.four'), False),
    (({'one': {'two': {'three': 4}}}, 'five'), False),
    (({'one': ['two', {'three': [4, 5]}]}, ['one', 1, 'three', 1]), True),
    (({'one': ['two', {'three': [4, 5]}]}, 'one.[1].three.[1]'), True),
    (({'one': ['two', {'three': [4, 5]}]}, 'one.1.three.1'), False),
    ((['one', {'two': {'three': [4, 5]}}], '[1].two.three.[0]'), True),
])
def test_has_path(case, expected):
    assert pyd.has_path(*case) == expected


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, ['a', 'b', 'c']),
    ([1, 2, 3], [0, 1, 2])
])
def test_keys(case, expected):
    assert set(pyd.keys(case)) == set(expected)


@parametrize('case', [
    pyd.keys_in
])
def test_keys_aliases(case):
    assert pyd.keys is case


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
    (([1, 2, 3],), {0: 1, 1: 2, 2: 3}),
    (([1, 2, 3], 0), {1: 2, 2: 3}),
    (([1, 2, 3], 0, 1), {2: 3})
])
def test_omit(case, expected):
    assert pyd.omit(*case) == expected


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, [['a', 1], ['b', 2], ['c', 3]]),
    ([1, 2, 3], [[0, 1], [1, 2], [2, 3]])
])
def test_pairs(case, expected):
    assert dict(pyd.pairs(case)) == dict(expected)


@parametrize('case,expected', [
    ((1,), 1),
    ((1.0,), 1),
    (('1',), 1),
    (('00001',), 1),
    ((13, 8), 11),
    (('0A',), 10),
    (('08',), 8),
    (('10',), 16),
    (('10', 10), 10),
    (('xyz',), None)
])
def test_parse_int(case, expected):
    assert pyd.parse_int(*case) == expected


@parametrize('case,expected', [
    (({'a': 1, 'b': 2, 'c': 3}, 'a'), {'a': 1}),
    (({'a': 1, 'b': 2, 'c': 3}, 'a', 'b'), {'a': 1, 'b': 2}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a', 'b']), {'a': 1, 'b': 2}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a'], ['b']), {'a': 1, 'b': 2}),
    (({'a': 1, 'b': 2, 'c': 3}, lambda value, key, *args: key in ['a']),
     {'a': 1}),
    (([1, 2, 3],), {}),
    (([1, 2, 3], 0), {0: 1}),
    (([1, 2, 3], 0, 1), {0: 1, 1: 2})
])
def test_pick(case, expected):
    assert pyd.pick(*case) == expected


@parametrize('case,expected', [
    (({'a': 1, 'b': 2}, {'a': 'A', 'b': 'B'}), {'A': 1, 'B': 2}),
    (({'a': 1, 'b': 2}, {'a': 'A'}), {'A': 1, 'b': 2}),
    (({'a': 1, 'b': 2}, {'c': 'C', 'b': 'B'}), {'a': 1, 'B': 2}),
])
def test_rename_keys(case, expected):
    assert pyd.rename_keys(*case) == expected


@parametrize('case,expected', [
    (({}, 1, ['one', 'two', 'three', 'four']),
     {'one': {'two': {'three': {'four': 1}}}}),
    (({'one': {'two': {}, 'three': {}}}, 1, ['one', 'two', 'three', 'four']),
     {'one': {'two': {'three': {'four': 1}}, 'three': {}}}),
    (({}, 1, 'one'), {'one': 1}),
    (([], 1, [0, 0, 0]), [[[1]]]),
    (([1, 2, [3, 4, [5, 6]]], 7, [2, 2, 1]), [1, 2, [3, 4, [5, 7]]]),
    (([1, 2, [3, 4, [5, 6]]], 7, [2, 2, 2]), [1, 2, [3, 4, [5, 6, 7]]])
])
def test_set_path(case, expected):
    result = pyd.set_path(*case)
    assert result == expected
    assert result is not case[0]


@parametrize('case,expected', [
    (1, '1'),
    (1.25, '1.25'),
    (True, 'True'),
    ([1], '[1]'),
])
def test_to_string(case, expected):
    assert pyd.to_string(case) == expected


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
    (({'rome': 'Republic'},
      lambda value: 'Empire' if value == 'Republic' else value,
      ['rome']),
     {'rome': 'Empire'}),
    (({},
      lambda value: 'Empire' if value == 'Republic' else value,
      ['rome']),
     {'rome': None}),
    (({'earth': {'rome': 'Republic'}},
      lambda value: 'Empire' if value == 'Republic' else value,
      ['earth', 'rome']),
     {'earth': {'rome': 'Empire'}}),
])
def test_update_path(case, expected):
    result = pyd.update_path(*case)
    assert result == expected
    assert result is not case[0]


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, [1, 2, 3]),
    ([1, 2, 3], [1, 2, 3])
])
def test_values(case, expected):
    assert set(pyd.values(case)) == set(expected)


@parametrize('case', [
    pyd.values_in
])
def test_values_aliases(case):
    assert pyd.values is case
