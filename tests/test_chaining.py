
from copy import deepcopy

import pydash as pyd

from .fixtures import parametrize


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
