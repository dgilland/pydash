from pydash.fp import convert


def test_immutable():
    def f(a, *b):
        a.extend(b)
        return a
    g = convert.immutable(f)
    a = [1, 2]
    assert g(a, 3, 4) == [1, 2, 3, 4]
    assert a == [1, 2]
