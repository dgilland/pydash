from pydash.fp import convert
from .fixtures import parametrize


_ = convert.Placeholder


def test_immutable():
    def f(a, *b):
        a.extend(b)
        return a
    g = convert.immutable(f)
    a = [1, 2]
    assert g(a, 3, 4) == [1, 2, 3, 4]
    assert a == [1, 2]


@parametrize('count', range(1, 6))
def test_applycap(count):
    f = lambda *args: len(args)
    assert convert.applycap(count)(f)(*range(5)) == count


@parametrize('case,expected', [
    (([1, 2, 0], False, (1, 2, 3, 4, 5)), (2, 3, 1, 4, 5)),
    (([1, 2, 0], True, (1, 2, 3, 4, 5)), (2, 3, 4, 5, 1)),
])
def test_getargs(case, expected):
    assert convert.getargs(*case) == expected


def test_curry():
    f = lambda *args: args
    g = convert.curry_ex(3)(f)
    assert g(1)(2, 3) == (1, 2, 3)
    assert g(1, 2)(3) == (1, 2, 3)
    assert g(1)(2)(3) == (1, 2, 3)


def test_curry_placeholder():
    f = lambda *args: args
    assert convert.curry_ex(2)(f)(_)(2, 3) == (3, 2)
    assert convert.curry_ex(2)(f)(1)(2, 3) == (1, 2, 3)
    assert convert.curry_ex(3)(f)(1)(_, 3)(2) == (1, 2, 3)


@parametrize('case,expected', [
    (([1, 2, 3], [4, 5]), (1, 2, 3, 4, 5)),
    (([1, _, 3], [4, 5]), (1, 4, 3, 5)),
])
def test_replace_args(case, expected):
    assert convert.replace_args(*case) == expected
