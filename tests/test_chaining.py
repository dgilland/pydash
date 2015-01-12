# -*- coding: utf-8 -*-

from copy import deepcopy

import pydash as _

from .fixtures import parametrize


pydash_methods = _.filter_(dir(_), lambda m: callable(getattr(_, m, None)))


def test_chaining_methods():
    chain = _.chain([])

    for method in dir(_):
        if not callable(method):
            continue

        chained = getattr(chain, method)
        assert chained.method is getattr(_, method)


@parametrize('value,methods', [
    ([1, 2, 3, 4], [('without', (2, 3)),
                    ('reject', (lambda x: x > 1,))])
])
def test_chaining(value, methods):
    expected = deepcopy(value)
    actual = _.chain(deepcopy(value))

    for method, args in methods:
        expected = getattr(_, method)(expected, *args)
        actual = getattr(actual, method)(*args)

    assert actual.value() == expected


def test_chaining_invalid_method():
    raised = False

    try:
        _.chain([]).foobar
    except _.InvalidMethod:
        raised = True

    assert raised


def test_chaining_value_alias():
    chained = _.chain((1, 2))
    assert chained.value() is chained.value_of()


def test_chaining_lazy():
    tracker = {'called': False}

    def interceptor(value):
        tracker['called'] = True
        return value.pop()

    chn = _.chain([1, 2, 3, 4, 5]).initial().tap(interceptor)

    assert not tracker['called']

    chn = chn.last()

    assert not tracker['called']

    result = chn.value()

    assert tracker['called']
    assert result == 3


def test_dash_instance_chaining():
    value = [1, 2, 3, 4]
    from__ = _._(value).without(2, 3).reject(lambda x: x > 1)
    from_chain = _.chain(value).without(2, 3).reject(lambda x: x > 1)

    assert from__.value() == from_chain.value()


def test_dash_instance_methods():
    assert pydash_methods

    for method in pydash_methods:
        assert getattr(_._, method) is getattr(_, method)


def test_dash_suffixed_method_aliases():
    methods = _.filter_(pydash_methods, lambda m: m.endswith('_'))
    assert methods

    for method in methods:
        assert getattr(_._, method[:-1]) is getattr(_, method)


def test_dash_method_call():
    value = [1, 2, 3, 4, 5]
    assert _._.initial(value) == _.initial(value)


def test_dash_alias():
    assert _.py_ is _._


@parametrize('case,expected', [
    ([1, 2, 3], '[1, 2, 3]'),
])
def test_chaining_value_to_string(case, expected):
    assert _.chain(case).to_string() == expected


@parametrize('value,interceptor,expected', [
    ([1, 2, 3, 4, 5], lambda value: value.pop(), 3)
])
def test_tap(value, interceptor, expected):
    actual = _.chain(value).initial().tap(interceptor).last().value()
    assert actual == expected


@parametrize('value,func,expected', [
    ([1, 2, 3, 4, 5], lambda value: [sum(value)], 10)
])
def test_thru(value, func, expected):
    assert _.chain(value).initial().thru(func).last().value()
