
from copy import deepcopy

import pydash as pyd

from .fixtures import parametrize


pydash_methods = pyd.filter_(dir(pyd),
                             lambda m: callable(getattr(pyd, m, None)))


def test_chaining_methods():
    chain = pyd.chain([])

    for method in dir(pyd):
        if not callable(method):
            continue

        chained = getattr(chain, method)
        assert chained.method is getattr(pyd, method)


@parametrize('value,methods', [
    ([1, 2, 3, 4], [('without', (2, 3)),
                    ('reject', (lambda x: x > 1,))])
])
def test_chaining(value, methods):
    expected = deepcopy(value)
    actual = pyd.chain(deepcopy(value))

    for method, args in methods:
        expected = getattr(pyd, method)(expected, *args)
        actual = getattr(actual, method)(*args)

    assert actual.value() == expected


def test_chaining_invalid_method():
    raised = False

    try:
        pyd.chain([]).foobar
    except pyd.InvalidMethod:
        raised = True

    assert raised


def test_chaining_value_alias():
    chained = pyd.chain((1, 2))
    assert chained.value() is chained.value_of()


def test_chaining_lazy():
    tracker = {'called': False}

    def interceptor(value):
        tracker['called'] = True
        return value.pop()

    chn = pyd.chain([1, 2, 3, 4, 5]).initial().tap(interceptor)

    assert not tracker['called']

    chn = chn.last()

    assert not tracker['called']

    result = chn.value()

    assert tracker['called']
    assert result == 3


def test_underscore_instance_chaining():
    value = [1, 2, 3, 4]
    from__ = pyd._(value).without(2, 3).reject(lambda x: x > 1)
    from_chain = pyd.chain(value).without(2, 3).reject(lambda x: x > 1)

    assert from__.value() == from_chain.value()


def test_underscore_instance_methods():
    assert pydash_methods

    for method in pydash_methods:
        assert getattr(pyd._, method) is getattr(pyd, method)


def test_underscore_suffixed_method_aliases():
    methods = pyd.filter_(pydash_methods, lambda m: m.endswith('_'))
    assert methods

    for method in methods:
        assert getattr(pyd._, method[:-1]) is getattr(pyd, method)


def test_underscore_method_call():
    value = [1, 2, 3, 4, 5]
    assert pyd._.initial(value) == pyd.initial(value)


@parametrize('case,expected', [
    ([1, 2, 3], '[1, 2, 3]'),
])
def test_chaining_value_to_string(case, expected):
    assert pyd.chain(case).to_string() == expected


@parametrize('value,interceptor,expected', [
    ([1, 2, 3, 4, 5], lambda value: value.pop(), 3)
])
def test_tap(value, interceptor, expected):
    actual = pyd.chain(value).initial().tap(interceptor).last().value()
    assert actual == expected


@parametrize('value,func,expected', [
    ([1, 2, 3, 4, 5], lambda value: [sum(value)], 10)
])
def test_thru(value, func, expected):
    assert pyd.chain(value).initial().thru(func).last().value()
