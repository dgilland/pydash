# -*- coding: utf-8 -*-

import datetime as dt

import pydash as _

from . import fixtures
from .fixtures import parametrize


today = dt.date.today()


@parametrize('case,expected', [
    (({'name': 'fred'}, {'employer': 'slate'}),
     {'name': 'fred', 'employer': 'slate'}),
    (({'name': 'fred'}, {'employer': 'slate'}, {'employer': 'medium'}),
     {'name': 'fred', 'employer': 'medium'}),
    (({'name': 'fred'}, {'age': 26}, lambda obj, src: src + 1),
     {'name': 'fred', 'age': 27}),
])
def test_assign(case, expected):
    assert _.assign(*case) == expected


@parametrize('case', [
    _.extend
])
def test_assign_aliases(case):
    assert _.assign is case


@parametrize('case,expected', [
    (({'name': 'fred', 'greet': lambda: 'Hello, world!'},), ['greet']),
    ((['fred', lambda: 'Hello, world!'],), [1]),
])
def test_callables(case, expected):
    assert _.callables(*case) == expected


@parametrize('case', [
    _.methods,
])
def test_callables_aliases(case):
    assert _.callables is case


@parametrize('case,args', [
    ({'a': {'d': 1}, 'b': {'c': 2}}, ()),
    ({'a': {'d': 1}, 'b': {'c': 2}}, (False, lambda v: v)),
    ([{'a': {'d': 1}, 'b': {'c': 2}}], ())
])
def test_clone(case, args):
    actual = _.clone(case, *args)

    assert actual is not case

    for key, value in _.helpers.iterator(actual):
        assert value is case[key]


@parametrize('case,kargs', [
    ({'a': {'d': 1}, 'b': {'c': 2}}, {}),
    ({'a': {'d': 1}, 'b': {'c': 2}}, {'callback': lambda v: v}),
    ([{'a': {'d': 1}, 'b': {'c': 2}}], {})
])
def test_clone_deep(case, kargs):
    kargs['is_deep'] = True
    actuals = [_.clone(case, **kargs),
               _.clone_deep(case, callback=kargs.get('callback'))]

    for actual in actuals:
        assert actual is not case

        for key, value in _.helpers.iterator(actual):
            assert value is not case[key]


@parametrize('case,expected', [
    (({'level1': {
        'value': 'value 1',
        'level2': {
            'value': 'value 2',
            'level3': {
                'value': 'value 3'
            }
        }}},
      lambda value, property_path: '.'.join(property_path) + '==' + value),
     {'level1': {
         'value': 'level1.value==value 1',
         'level2': {
             'value': 'level1.level2.value==value 2',
             'level3': {
                 'value': 'level1.level2.level3.value==value 3'
             }
         }}}),
    (([['value 1', [['value 2', ['value 3']]]]],
      lambda value, property_path: (_.join(property_path, '.') +
                                    '==' +
                                    value)),
     [['0.0==value 1', [['0.1.0.0==value 2', ['0.1.0.1.0==value 3']]]]]),
])
def test_deep_map_values(case, expected):
    assert _.deep_map_values(*case) == expected


@parametrize('case,expected', [
    (({'name': 'barney'}, {'name': 'fred', 'employer': 'slate'}),
     {'name': 'barney', 'employer': 'slate'}),
])
def test_defaults(case, expected):
    assert _.defaults(*case) == expected


@parametrize('case,expected', [
    (({'user': {'name': 'barney'}}, {'user': {'name': 'fred', 'age': 36}}),
     {'user': {'name': 'barney', 'age': 36}})
])
def test_defaults_deep(case, expected):
    assert _.defaults_deep(*case) == expected


@parametrize('case,expected', [
    ([1, 2, 3], {0: 1, 1: 2, 2: 3}),
    ({0: 1, 1: 2, 2: 3}, {0: 1, 1: 2, 2: 3}),
])
def test_to_dict(case, expected):
    assert _.to_dict(case) == expected


@parametrize('case', [
    _.to_plain_object
])
def test_to_dict_aliases(case):
    assert _.to_dict is case


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, {1: 'a', 2: 'b', 3: 'c'}),
    ([1, 2, 3], {1: 0, 2: 1, 3: 2}),
])
def test_invert(case, expected):
    assert _.invert(case) == expected


@parametrize('case,expected', [
    ([1, 2, 3], {1: [0], 2: [1], 3: [2]}),
    ({'first': 'fred', 'second': 'barney', 'third': 'fred'},
     {'fred': ['first', 'third'], 'barney': ['second']}),
])
def test_invert_multivalue(case, expected):
    result = _.invert(case, multivalue=True)
    for key in result:
        assert set(result[key]) == set(expected[key])


@parametrize('case,expected', [
    # NOTE: The expected is a list of values but find_key returns only a single
    # value. However, since dicts do not have an order, it's unknown what the
    # "first" returned value will be.
    (({'barney': {'age': 36, 'blocked': False},
       'fred': {'age': 40, 'blocked': True},
       'pebbles': {'age': 1, 'blocked': False}},
      lambda obj: obj['age'] < 40),
     ['pebbles', 'barney']),
    (({'barney': {'age': 36, 'blocked': False},
       'fred': {'age': 40, 'blocked': True},
       'pebbles': {'age': 1, 'blocked': False}},),
     ['barney', 'fred', 'pebbles']),
    (([1, 2, 3],), [0])
])
def test_find_key(case, expected):
    assert _.find_key(*case) in expected


@parametrize('case', [
    _.find_last_key
])
def test_find_key_aliases(case):
    assert _.find_key is case


@parametrize('case,expected', [
    (({'name': 'fred', 'employer': 'slate'}, fixtures.for_in_callback0),
     ({'name': 'fredfred', 'employer': 'slateslate'},)),
    (({'name': 'fred', 'employer': 'slate'}, fixtures.for_in_callback1),
     ({'name': 'fredfred', 'employer': 'slate'},
      {'name': 'fred', 'employer': 'slateslate'})),
    (([1, 2, 3], fixtures.for_in_callback2), ([False, True, 3],))
])
def test_for_in(case, expected):
    assert _.for_in(*case) in expected


@parametrize('case', [
    _.for_own
])
def test_for_in_aliases(case):
    assert _.for_in is case


@parametrize('case,expected', [
    (({'name': 'fred', 'employer': 'slate'}, fixtures.for_in_callback0),
     ({'name': 'fredfred', 'employer': 'slateslate'},)),
    (({'name': 'fred', 'employer': 'slate'}, fixtures.for_in_callback1),
     ({'name': 'fredfred', 'employer': 'slate'},
      {'name': 'fred', 'employer': 'slateslate'})),
    (([1, 2, 3], fixtures.for_in_callback2), ([1, True, 'index:2'],))
])
def test_for_in_right(case, expected):
    assert _.for_in_right(*case) in expected


@parametrize('case', [
    _.for_own_right,
])
def test_for_in_right_aliases(case):
    assert _.for_in_right is case


@parametrize('case,expected', [
    (({'one': {'two': {'three': 4}}}, 'one.two'), {'three': 4}),
    (({'one': {'two': {'three': 4}}}, 'one.two.three'), 4),
    (({'one': {'two': {'three': 4}}}, ['one', 'two']), {'three': 4}),
    (({'one': {'two': {'three': 4}}}, ['one', 'two', 'three']), 4),
    (({'one': {'two': {'three': 4}}}, 'one.four'), None),
    (({'one': {'two': {'three': 4}}}, 'five'), None),
    (({'one': ['two', {'three': [4, 5]}]}, ['one', 1, 'three', 1]), 5),
    (({'one': ['two', {'three': [4, 5]}]}, 'one.[1].three.[1]'), 5),
    (({'one': ['two', {'three': [4, 5]}]}, 'one.1.three.1'), 5),
    ((['one', {'two': {'three': [4, 5]}}], '[1].two.three.[0]'), 4),
    ((['one', {'two': {'three': [4, [{'four': [5]}]]}}],
      '[1].two.three[1][0].four[0]'),
     5),
    ((range(50), '[42]'), 42),
    (([[[[[[[[[[42]]]]]]]]]], '[0][0][0][0][0][0][0][0][0][0]'), 42),
    (([range(50)], '[0][42]'), 42),
    (({'a': [{'b': range(50)}]}, 'a[0].b[42]'), 42),
    (({'lev.el1': {'lev\\el2': {'level3': ['value']}}},
      'lev\\.el1.lev\\\\el2.level3.[0]'),
     'value'),
])
def test_get(case, expected):
    assert _.get(*case) == expected


@parametrize('case', [
    _.get_path,
    _.deep_get,
])
def test_get_aliases(case):
    assert _.get is case


@parametrize('case,expected', [
    (({'a': 1, 'b': 2, 'c': 3}, 'b'), True),
    (([1, 2, 3], 0), True),
    (([1, 2, 3], 1), True),
    (([1, 2, 3], 3), False),
    (({'a': 1, 'b': 2, 'c': 3}, 'b'), True),
    (([1, 2, 3], 0), True),
    (([1, 2, 3], 1), True),
    (([1, 2, 3], 3), False),
    (({'one': {'two': {'three': 4}}}, 'one.two'), True),
    (({'one': {'two': {'three': 4}}}, 'one.two.three'), True),
    (({'one': {'two': {'three': 4}}}, ['one', 'two']), True),
    (({'one': {'two': {'three': 4}}}, ['one', 'two', 'three']), True),
    (({'one': {'two': {'three': 4}}}, 'one.four'), False),
    (({'one': {'two': {'three': 4}}}, 'five'), False),
    (({'one': ['two', {'three': [4, 5]}]}, ['one', 1, 'three', 1]), True),
    (({'one': ['two', {'three': [4, 5]}]}, 'one.[1].three.[1]'), True),
    (({'one': ['two', {'three': [4, 5]}]}, 'one.1.three.1'), True),
    ((['one', {'two': {'three': [4, 5]}}], '[1].two.three.[0]'), True),
    (({'lev.el1': {r'lev\el2': {'level3': ['value']}}},
      r'lev\.el1.lev\\el2.level3.[0]'),
     True),
])
def test_has(case, expected):
    assert _.has(*case) == expected


@parametrize('case', [
    _.deep_has,
    _.has_path,
])
def test_has_aliases(case):
    assert _.has is case


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, ['a', 'b', 'c']),
    ([1, 2, 3], [0, 1, 2])
])
def test_keys(case, expected):
    assert set(_.keys(case)) == set(expected)


@parametrize('case', [
    _.keys_in
])
def test_keys_aliases(case):
    assert _.keys is case


@parametrize('case,expected', [
    (({'a': 1, 'b': 2, 'c': 3}, lambda num: num * 3),
     {'a': 3, 'b': 6, 'c': 9}),
    (({'fred': {'name': 'fred', 'age': 40},
       'pebbles': {'name': 'pebbles', 'age': 1}},
      'age'),
     {'fred': 40, 'pebbles': 1})
])
def test_map_values(case, expected):
    assert _.map_values(*case) == expected


@parametrize('case,expected', [
    (({'characters': [{'name': 'barney'}, {'name': 'fred'}]},
      {'characters': [{'age': 36}, {'age': 40}]}),
     {'characters': [{'name': 'barney', 'age': 36},
                     {'name': 'fred', 'age': 40}]}),
    (({'characters': [{'name': 'barney'}, {'name': 'fred'}, {}]},
      {'characters': [{'age': 36}, {'age': 40}]}),
     {'characters': [{'name': 'barney', 'age': 36},
                     {'name': 'fred', 'age': 40},
                     {}]}),
    (({'characters': [{'name': 'barney'}, {'name': 'fred'}]},
      {'characters': [{'age': 36}, {'age': 40}, {}]}),
     {'characters': [{'name': 'barney', 'age': 36},
                     {'name': 'fred', 'age': 40},
                     {}]}),
    (({'characters': [{'name': 'barney'}, {'name': 'fred'}]},
      {'characters': [{'age': 36}, {'age': 40}]},
      {'characters': [{'score': 5}, {'score': 7}]}),
     {'characters': [{'name': 'barney', 'age': 36, 'score': 5},
                     {'name': 'fred', 'age': 40, 'score': 7}]}),
    (({'characters': {'barney': {'age': 36}, 'fred': {'score': 7}}},
      {'characters': {'barney': {'score': 5}, 'fred': {'age': 40}}}),
     {'characters': {'barney': {'age': 36, 'score': 5},
                     'fred': {'age': 40, 'score': 7}}}),
    (({'characters': {'barney': {'age': 36}, 'fred': {'score': 7}}},
      {'characters': {'barney': [5], 'fred': 7}}),
     {'characters': {'barney': [5],
                     'fred': 7}}),
    (({'characters': {'barney': {'age': 36}, 'fred': {'score': 7}}},
      {'foo': {'barney': [5], 'fred': 7}}),
     {'characters': {'barney': {'age': 36}, 'fred': {'score': 7}},
      'foo': {'barney': [5], 'fred': 7}}),
    (({'fruits': ['apple'], 'vegetables': ['beet']},
      {'fruits': ['banana'], 'vegetables': ['carrot']},
      lambda a, b: a + b if isinstance(a, list) else b),
     {'fruits': ['apple', 'banana'], 'vegetables': ['beet', 'carrot']}),
    (({'foo': {'bar': 1}}, {'foo': {}}),
     {'foo': {'bar': 1}})
])
def test_merge(case, expected):
    assert _.merge(*case) == expected


def test_merge_no_link_dict():
    case1 = {'foo': {'bar': None}}
    case2 = {'foo': {'bar': False}}
    result = _.merge({}, case1, case2)
    result['foo']['bar'] = True

    assert case1 == {'foo': {'bar': None}}
    assert case2 == {'foo': {'bar': False}}


def test_merge_no_link_list():
    case = {'foo': [{}]}
    result = _.merge({}, case)
    result['foo'][0]['bar'] = True

    assert case == {'foo': [{}]}


@parametrize('case,expected', [
    (({'a': 1, 'b': 2, 'c': 3}, 'a'), {'b': 2, 'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, 'a', 'b'), {'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a', 'b']), {'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a'], ['b']), {'c': 3}),
    (({'a': 1, 'b': 2, 'c': 3}, lambda value, key: key in ['a']),
     {'b': 2, 'c': 3}),
    (([1, 2, 3],), {0: 1, 1: 2, 2: 3}),
    (([1, 2, 3], 0), {1: 2, 2: 3}),
    (([1, 2, 3], 0, 1), {2: 3})
])
def test_omit(case, expected):
    assert _.omit(*case) == expected


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, [['a', 1], ['b', 2], ['c', 3]]),
    ([1, 2, 3], [[0, 1], [1, 2], [2, 3]])
])
def test_pairs(case, expected):
    assert dict(_.pairs(case)) == dict(expected)


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
    assert _.parse_int(*case) == expected


@parametrize('case,expected', [
    (({'a': 1, 'b': 2, 'c': 3}, 'a'), {'a': 1}),
    (({'a': 1, 'b': 2, 'c': 3}, 'a', 'b'), {'a': 1, 'b': 2}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a', 'b']), {'a': 1, 'b': 2}),
    (({'a': 1, 'b': 2, 'c': 3}, ['a'], ['b']), {'a': 1, 'b': 2}),
    (({'a': 1, 'b': 2, 'c': 3}, lambda value, key: key in ['a']),
     {'a': 1}),
    (([1, 2, 3],), {}),
    (([1, 2, 3], 0), {0: 1}),
    (([1, 2, 3], 0, 1), {0: 1, 1: 2}),
    ((fixtures.Object(a=1, b=2, c=3), 'a'), {'a': 1}),
    ((fixtures.Object(a=1, b=2, c=3), 'a', 'b'), {'a': 1, 'b': 2}),
    ((fixtures.ItemsObject({'a': 1, 'b': 2, 'c': 3}), 'a'), {'a': 1}),
    ((fixtures.IteritemsObject({'a': 1, 'b': 2, 'c': 3}), 'a'), {'a': 1}),
])
def test_pick(case, expected):
    assert _.pick(*case) == expected


@parametrize('case,expected', [
    (({'a': 1, 'b': 2}, {'a': 'A', 'b': 'B'}), {'A': 1, 'B': 2}),
    (({'a': 1, 'b': 2}, {'a': 'A'}), {'A': 1, 'b': 2}),
    (({'a': 1, 'b': 2}, {'c': 'C', 'b': 'B'}), {'a': 1, 'B': 2}),
])
def test_rename_keys(case, expected):
    assert _.rename_keys(*case) == expected


@parametrize('case,expected', [
    (({}, ['one', 'two', 'three', 'four'], 1),
     {'one': {'two': {'three': {'four': 1}}}}),
    (({}, 'one.two.three.four', 1),
     {'one': {'two': {'three': {'four': 1}}}}),
    (({'one': {'two': {}, 'three': {}}}, ['one', 'two', 'three', 'four'], 1),
     {'one': {'two': {'three': {'four': 1}}, 'three': {}}}),
    (({'one': {'two': {}, 'three': {}}}, 'one.two.three.four', 1),
     {'one': {'two': {'three': {'four': 1}}, 'three': {}}}),
    (({}, 'one', 1), {'one': 1}),
    (([], [0, 0, 0], 1), [[[1]]]),
    (([], '[0].[0].[0]', 1), [[[1]]]),
    (([1, 2, [3, 4, [5, 6]]], [2, 2, 1], 7), [1, 2, [3, 4, [5, 7]]]),
    (([1, 2, [3, 4, [5, 6]]], '[2].[2].[1]', 7), [1, 2, [3, 4, [5, 7]]]),
    (([1, 2, [3, 4, [5, 6]]], [2, 2, 2], 7), [1, 2, [3, 4, [5, 6, 7]]]),
    (([1, 2, [3, 4, [5, 6]]], '[2].[2].[2]', 7), [1, 2, [3, 4, [5, 6, 7]]]),
])
def test_set_(case, expected):
    assert _.set_(*case) == expected


@parametrize('case', [
    _.deep_set
])
def test_set_aliases(case):
    assert _.set_ is case


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
    result = _.set_path(*case)
    assert result == expected
    assert result is not case[0]


@parametrize('case,expected', [
    (('1',), True),
    (('0',), False),
    (('true',), True),
    (('True',), True),
    (('false',), False),
    (('False',), False),
    (('',), None),
    (('a',), None),
    ((0,), False),
    ((1,), True),
    (([],), False),
    ((True,), True),
    ((False,), False),
    ((None,), False),
    (('Truthy', ['truthy']), True),
    (('Falsey', [], ['falsey']), False),
    (('foobar', ['^[f]']), True),
    (('ofobar', ['^[f]']), None),
    (('foobar', [], ['.+[r]$']), False),
    (('foobra', [], ['.+[r]$']), None),
])
def test_to_boolean(case, expected):
    assert _.to_boolean(*case) is expected


@parametrize('case,expected', [
    (('2.556',), 3.0),
    (('2.556', 1), 2.6),
    (('999.999', -1), 990.0),
    (('foo',), None)
])
def test_to_number(case, expected):
    assert _.to_number(*case) == expected


@parametrize('case,expected', [
    (1, '1'),
    (1.25, '1.25'),
    (True, 'True'),
    ([1], '[1]'),
    ('d\xc3\xa9j\xc3\xa0 vu', 'd\xc3\xa9j\xc3\xa0 vu'),
    ('', ''),
    (None, ''),
    (today, str(today)),
])
def test_to_string(case, expected):
    assert _.to_string(case) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], lambda acc, value, key: acc.append((key, value))),
     [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]),
    (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], fixtures.transform_callback0),
     [1, 9, 25]),
    (([1, 2, 3, 4, 5],), [])
])
def test_transform(case, expected):
    assert _.transform(*case) == expected


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
    result = _.update_path(*case)
    assert result == expected
    assert result is not case[0]


@parametrize('case,expected', [
    ({'a': 1, 'b': 2, 'c': 3}, [1, 2, 3]),
    ([1, 2, 3], [1, 2, 3])
])
def test_values(case, expected):
    assert set(_.values(case)) == set(expected)


@parametrize('case', [
    _.values_in
])
def test_values_aliases(case):
    assert _.values is case
