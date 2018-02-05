from pydash.fp import convert
from .fixtures import parametrize


def test_immutable():
    def f(a, *b):
        a.extend(b)
        return a
    g = convert.immutable(f)
    a = [1, 2]
    assert g(a, 3, 4) == [1, 2, 3, 4]
    assert a == [1, 2]


@parametrize('case,expected', [
    (([1, 2, 0], False, (1, 2, 3, 4, 5)), (2, 3, 1)),
    (([1, 2, 0], True, (1, 2, 3, 4, 5)), (2, 3, 4, 5, 1)),
])
def test_getargs(case, expected):
    assert convert.getargs(*case) == expected
