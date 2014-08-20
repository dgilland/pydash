
import datetime
import decimal
import re

import pydash as pyd
from pydash.api.utilities import iterator

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

    for key, value in iterator(actual):
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

        for key, value in iterator(actual):
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
])
def test_functions(case, expected):
    assert pyd.functions(*case) == expected


@parametrize('case', [
    pyd.methods,
])
def test_functions_aliases(case):
    assert pyd.functions is case


@parametrize('case,expected', [
    (({'a': 1, 'b': 2, 'c': 3}, 'b'), True),
    (([1, 2, 3], 0), True),
    (([1, 2, 3], 1), True),
    (([1, 2, 3], 3), False),
])
def test_has(case, expected):
    assert pyd.has(*case) == expected


@parametrize('case,expected', [
    (True, True),
    (False, True),
    (0, False),
    ('', False),
])
def test_is_boolean(case, expected):
    assert pyd.is_boolean(case) == expected


@parametrize('case,expected', [
    (datetime.date.today(), True),
    (datetime.datetime.today(), True),
    ('2014-01-01', False),
    ('2014-01-01T00:00:00', False),
    (1, False)
])
def test_is_date(case, expected):
    assert pyd.is_date(case) == expected


@parametrize('case,expected', [
    (True, True),
    (0, True),
    (123.45, True),
    ('', True),
    ({}, True),
    ([], True),
    (False, True),
    (None, True),
    ({'a': 1}, False),
    ([1], False),
    ('Hello', False),
    (['Hello', 'World'], False),
])
def test_is_empty(case, expected):
    assert pyd.is_empty(case) == expected


@parametrize('case,expected', [
    ((1, 1), True),
    ((1, 2), False),
    (('1', '1'), True),
    (('1', '2'), False),
    (([1], {'a': 1}), False),
    (([1], {'a': 1}, lambda a, b: True), True),
    (({'a': 1}, {'a': 1}), True),
    (({'a': 1}, {'b': 1}, lambda a, b: None if isinstance(a, dict) else True),
     False),
    (([1, 2, 3], [1, 2, 3]), True),
    (([1, 2, 3], [1, 2]), False),
    (([1, 2], [1, 2, 3]), False),
    (([1, 2, 3], [1, 2], lambda a, b: None if isinstance(a, list) else True),
     False),
    (([1, 2], [1, 2, 3], lambda a, b: None if isinstance(a, list) else True),
     False),
    ((['hello', 'goodbye'], ['hi', 'goodbye'], fixtures.is_equal_callback0),
     True)
])
def test_is_equal(case, expected):
    assert pyd.is_equal(*case) == expected


@parametrize('case,expected', [
    (Exception(), True),
    ({}, False),
    ([], False)
])
def test_is_error(case, expected):
    assert pyd.is_error(case) == expected


@parametrize('case,expected', [
    (lambda x: x + 1, True),
    ('Hello, world!', False),
])
def test_is_function(case, expected):
    assert pyd.is_function(case) == expected


@parametrize('case,expected', [
    ([1, 2, 3], True),
    ({}, False),
])
def test_is_list(case, expected):
    assert pyd.is_list(case) == expected


@parametrize('case,expected', [
    (0, False),
    (123456789123456789123456789, False),
    (123.45, False),
    (decimal.Decimal(1), False),
    ('1', True)
])
def test_is_nan(case, expected):
    assert pyd.is_nan(case) == expected


@parametrize('case,expected', [
    (None, True),
    (0, False),
])
def test_is_none(case, expected):
    assert pyd.is_none(case) == expected


@parametrize('case,expected', [
    (0, True),
    (123456789123456789123456789, True),
    (123.45, True),
    (decimal.Decimal(1), True),
    ('1', False)
])
def test_is_number(case, expected):
    assert pyd.is_number(case) == expected


@parametrize('case,expected', [
    ({}, True),
    ([], True),
    (1, False),
    ('a', False),
    (iter([]), False),
    (iter({}), False)
])
def test_is_object(case, expected):
    assert pyd.is_object(case) == expected


@parametrize('case,expected', [
    ({}, True),
    ([], False),
    (1, False),
    ('a', False),
    (iter([]), False),
    (iter({}), False)
])
def test_is_plain_object(case, expected):
    assert pyd.is_plain_object(case) == expected


@parametrize('case,expected', [
    (re.compile(''), True),
    ('', False),
    ('Hello, world!', False),
    (1, False),
    ({}, False),
    ([], False),
    (None, False)
])
def test_is_reg_exp(case, expected):
    assert pyd.is_reg_exp(case) == expected


@parametrize('case', [
    pyd.is_re
])
def test_keys_aliases(case):
    assert pyd.is_reg_exp is case


@parametrize('case,expected', [
    ('', True),
    ('Hello, world!', True),
    (1, False),
    ({}, False),
    ([], False),
    (None, False)
])
def test_is_string(case, expected):
    assert pyd.is_string(case) == expected


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


@parametrize('case', [
    pyd.values_in
])
def test_values_aliases(case):
    assert pyd.values is case
