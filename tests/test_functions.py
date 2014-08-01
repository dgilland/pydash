
import time

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

    while (present - start) <= max_wait:
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
