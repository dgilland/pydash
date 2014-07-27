
import pydash as pyd
from .fixtures import parametrize


@parametrize('case,expected', [
    ((2, lambda: 3), 3),
    ((-1, lambda: 3), 3),
])
def test_after(case, expected):
    done = pyd.after(*case)

    # Call done() until n - 1, then check the return value for expected.

    for _ in range(case[0] - 1):
        ret = done()
        assert ret is None

    ret = done()
    assert ret == expected


@parametrize('case,args,expected', [
    ((lambda x: 'Hi {0}'.format(x), lambda x: '!!!' + x + '!!!'),
     ('Bob',),
     'Hi !!!Bob!!!')
])
def test_compose(case, args, expected):
    assert pyd.compose(*case)(*args) == expected


@parametrize('case,arglist,expected', [
    ((lambda a, b, c: a + b + c,), [(1, 1, 1)], 3),
    ((lambda a, b, c: a + b + c,), [(1,), (1, 1)], 3),
    ((lambda a, b, c: a + b + c,), [(1,), (1,), (1,)], 3),
    ((lambda *a: sum(a), 3), [(1, 1, 1)], 3),
    ((lambda *a: sum(a), 3), [(1,), (1,), (1,)], 3),
])
def test_curry(case, arglist, expected):
    curried = pyd.curry(*case)

    # Run test twice to verify curried can be reused
    for _ in range(2):
        ret = curried
        for args in arglist:
            ret = ret(*args)

        assert ret == expected


@parametrize('case,arglist,expected', [
    (lambda a: a * a, [(2,), (4,)], 4)
])
def test_once(case, arglist, expected):
    for args in arglist:
        pyd.once(case)(*args) == expected


@parametrize('case,case_args,args,expected', [
    (lambda a, b, c: a + b + c, ('a', 'b'), ('c',), 'abc')
])
def test_partial(case, case_args, args, expected):
    assert pyd.partial(case, *case_args)(*args) == expected


@parametrize('case,case_args,args,expected', [
    (lambda a, b, c: a + b + c, ('a', 'b'), ('c',), 'cab')
])
def test_partial_right(case, case_args, args, expected):
    assert pyd.partial_right(case, *case_args)(*args) == expected


@parametrize('case,args,expected', [
    ((lambda a: a.strip(), lambda func, text: '<p>{0}</p>'.format(func(text))),
     ('  hello world!  ',),
     '<p>hello world!</p>')
])
def test_wrap(case, args, expected):
    assert pyd.wrap(*case)(*args) == expected

