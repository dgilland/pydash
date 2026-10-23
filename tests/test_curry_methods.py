from functools import partial

import pytest

import pydash as _


class Methods:
    label = "base"

    def instance(receiver, left, right):
        return receiver.label, left, right

    def positional_only(receiver, left, right, /):
        return receiver.label, left, right

    @classmethod
    def class_method(receiver, left, right):
        return receiver.label, left, right

    @staticmethod
    def static(left, right):
        return left, right

    def zero(receiver):
        return receiver.label

    def defaults(receiver, left=10, right=20):
        return receiver.label, left, right

    def mixed(receiver, left, *, right):
        return receiver.label, left, right

    def extras(receiver, left, **kwargs):
        return receiver.label, left, kwargs

    def variadic(*args):
        return args

    def named_variadic(receiver, *args):
        return receiver.label, args


class Derived(Methods):
    label = "derived"


@pytest.mark.parametrize("curry", [_.curry, _.curry_right])
@pytest.mark.parametrize(
    "method,label",
    [
        (Methods().instance, "base"),
        (Derived().instance, "derived"),
        (Methods.class_method, "base"),
        (Methods().class_method, "base"),
        (Derived.class_method, "derived"),
    ],
)
def test_bound_method_curry(curry, method, label):
    curried = curry(method)
    assert curried.arity == 2
    assert curried._argcount == 2
    for _attempt in range(2):
        assert curried(1, 2) == (label, 1, 2)
        first, second = (2, 1) if curry is _.curry_right else (1, 2)
        remaining = curried(first)
        assert remaining._argcount == 1
        assert remaining(second) == (label, 1, 2)
        assert curried(right=2)(left=1) == (label, 1, 2)
        assert curried(left=1)(right=2) == (label, 1, 2)


@pytest.mark.parametrize("curry", [_.curry, _.curry_right])
@pytest.mark.parametrize("chained", [False, True])
def test_bound_method_curry_as_iteratee(curry, chained):
    curried = curry(Methods().instance)("fixed")
    if chained:
        actual = _.chain([1, 2]).map_(curried).value()
    else:
        actual = _.map_([1, 2], curried)
    expected = (
        [("base", 1, "fixed"), ("base", 2, "fixed")]
        if curry is _.curry_right
        else [("base", "fixed", 1), ("base", "fixed", 2)]
    )
    assert actual == expected


@pytest.mark.parametrize("curry", [_.curry, _.curry_right])
def test_bound_method_curry_zero_and_defaults(curry):
    assert curry(Methods().zero)() == "base"
    curried = curry(Methods().defaults)
    assert curried.arity == 2
    assert curried(1, 2) == ("base", 1, 2)
    assert curry(Methods().defaults, arity=0)() == ("base", 10, 20)
    assert curry(Methods().defaults, arity=1)(1, 2) == ("base", 1, 20)
    first, second = (2, 1) if curry is _.curry_right else (1, 2)
    assert curry(Methods().positional_only)(first)(second) == ("base", 1, 2)


@pytest.mark.parametrize("curry", [_.curry, _.curry_right])
def test_curry_other_callable_controls(curry):
    receiver = Methods()
    assert curry(Methods.instance)(receiver, 1, 2) == ("base", 1, 2)
    assert curry(Methods.static)(1, 2) == (1, 2)
    assert curry(partial(Methods.static, 1))(2) == (1, 2)
    assert curry(receiver.variadic).arity == 0
    assert curry(receiver.variadic)() == (receiver,)
    assert curry(receiver.named_variadic).arity == 1
    assert curry(receiver.named_variadic)(1, 2) == ("base", (1,))

    class Callable:
        def __call__(self, left, right):
            return left, right

    assert curry(Callable()).arity == 3
    assert curry(Callable(), arity=2)(1, 2) == (1, 2)
    assert curry(receiver.instance, arity=2)(1, 2) == ("base", 1, 2)


@pytest.mark.parametrize("curry", [_.curry, _.curry_right])
def test_bound_method_curry_keyword_parameter_controls(curry):
    assert curry(Methods().mixed)(1, right=2) == ("base", 1, 2)
    assert curry(Methods().extras)(1, tag=2) == ("base", 1, {"tag": 2})
