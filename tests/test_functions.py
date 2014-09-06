
import time

import pydash as pyd

from .fixtures import parametrize


@parametrize('case,expected', [
    ((2, lambda: 3), 3),
    ((-1, lambda: 3), 3),
])
def test_after(case, expected):
    done = pyd.after(*case)

    for _ in range(case[0] - 1):
        ret = done()
        assert ret is None

    ret = done()
    assert ret == expected


@parametrize('case,expected', [
    ((2, lambda: 3), 3),
    ((-1, lambda: 3), 3),
])
def test_before(case, expected):
    done = pyd.before(*case)

    for _ in range(case[0] - 1):
        ret = done()
        assert ret == expected

    ret = done()
    assert ret is None


@parametrize('case,arg,expected', [
    ((pyd.is_boolean, pyd.is_empty), [False, True], True),
    ((pyd.is_boolean, pyd.is_empty), [False, None], False),
])
def test_conjoin(case, arg, expected):
    assert pyd.conjoin(*case)(arg) == expected


@parametrize('case,arglist,expected', [
    ((lambda a, b, c: [a, b, c],), [(1, 2, 3)], [1, 2, 3]),
    ((lambda a, b, c: [a, b, c],), [(1, 2), (3,)], [1, 2, 3]),
    ((lambda a, b, c: [a, b, c],), [(1,), (2,), (3,)], [1, 2, 3]),
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
    ((lambda a, b, c: [a, b, c],), [(1, 2, 3)], [1, 2, 3]),
    ((lambda a, b, c: [a, b, c],), [(2, 3), (1,)], [1, 2, 3]),
    ((lambda a, b, c: [a, b, c],), [(3,), (2,), (1,)], [1, 2, 3]),
    ((lambda *a: sum(a), 3), [(1, 1, 1)], 3),
    ((lambda *a: sum(a), 3), [(1,), (1,), (1,)], 3),
])
def test_curry_right(case, arglist, expected):
    curried = pyd.curry_right(*case)

    # Run test twice to verify curried can be reused
    for _ in range(2):
        ret = curried
        for args in arglist:
            ret = ret(*args)

        assert ret == expected


def test_debounce():
    func = lambda: pyd.now()

    wait = 250
    debounced = pyd.debounce(func, wait)

    start = pyd.now()
    present = pyd.now()

    expected = debounced()

    while (present - start) <= wait + 100:
        result = debounced()
        present = pyd.now()

    assert result == expected

    time.sleep(wait / 1000.0)
    result = debounced()

    assert result > expected


def test_debounce_max_wait():
    func = lambda: pyd.now()

    wait = 250
    max_wait = 300
    debounced = pyd.debounce(func, wait, max_wait=max_wait)

    start = pyd.now()
    present = pyd.now()

    expected = debounced()

    while (present - start) <= (max_wait + 5):
        result = debounced()
        present = pyd.now()

    assert result > expected


@parametrize('func,wait,args,kargs,expected', [
    (lambda a, b, c: (a, b, c), 250, (1, 2), {'c': 3}, (1, 2, 3))
])
def test_delay(func, wait, args, kargs, expected):
    start = time.time() * 1000
    result = pyd.delay(func, wait, *args, **kargs)
    stop = time.time() * 1000

    assert (wait - 5) <= (stop - start) <= (wait + 5)
    assert result == expected


@parametrize('case,arg,expected', [
    ((pyd.is_boolean, pyd.is_empty), [False, True], True),
    ((pyd.is_boolean, pyd.is_empty), [False, None], True),
    ((pyd.is_string, pyd.is_number), ['one', 1, 'two', 2], True),
    ((pyd.is_string, pyd.is_number), [True, False, None, []], False),
])
def test_disjoin(case, arg, expected):
    assert pyd.disjoin(*case)(arg) == expected


@parametrize('case,args,expected', [
    ((lambda x: '!!!' + x + '!!!', lambda x: 'Hi {0}'.format(x)),
     ('Bob',),
     'Hi !!!Bob!!!'),
    ((lambda x: x + x, lambda x: x * x),
     (5,),
     100)
])
def test_flow(case, args, expected):
    assert pyd.flow(*case)(*args) == expected


@parametrize('case,args,expected', [
    ((lambda x: 'Hi {0}'.format(x), lambda x: '!!!' + x + '!!!'),
     ('Bob',),
     'Hi !!!Bob!!!'),
    ((lambda x: x + x, lambda x: x * x),
     (5,),
     50)
])
def test_flow_right(case, args, expected):
    assert pyd.flow_right(*case)(*args) == expected


@parametrize('case', [
    pyd.compose
])
def test_flow_right_aliases(case):
    assert pyd.flow_right is case


@parametrize('func,args,expected', [
    (lambda x: x + x, (2, 0), 2),
    (lambda x: x + x, (2, 1), 4),
    (lambda x: x + x, (2, 2), 8),
    (lambda x: x + x, (2, 3), 16)
])
def test_iterated(func, args, expected):
    assert pyd.iterated(func)(*args) == expected


@parametrize('funcs,args,expected', [
    ((lambda a: a[0], lambda a: a[-1]), ('Foobar',), ['F', 'r']),
    ((lambda a, b: a[0] + b[-1], lambda a, b: a[-1] + b[0]),
     ('Foobar', 'Barbaz'),
     ['Fz', 'rB']),
])
def test_juxtapose(funcs, args, expected):
    assert pyd.juxtapose(*funcs)(*args) == expected


@parametrize('func,args', [
    (lambda item: item, (True,)),
    (lambda item: item, (False,)),
])
def test_negate(func, args):
    assert pyd.negate(func)(*args) == (not func(*args))


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


def test_throttle():
    func = lambda: pyd.now()
    wait = 250
    throttled = pyd.throttle(func, wait)

    start = pyd.now()
    present = pyd.now()

    expected = throttled()

    while (present - start) < (wait - 50):
        result = throttled()
        present = pyd.now()

    assert result == expected

    time.sleep(100 / 1000.0)
    assert throttled() > expected


@parametrize('case,args,expected', [
    ((lambda a: a.strip(), lambda func, text: '<p>{0}</p>'.format(func(text))),
     ('  hello world!  ',),
     '<p>hello world!</p>')
])
def test_wrap(case, args, expected):
    assert pyd.wrap(*case)(*args) == expected
