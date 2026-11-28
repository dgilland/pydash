from copy import deepcopy

import pytest

import pydash as _


parametrize = pytest.mark.parametrize


pydash_methods = _.filter_(dir(_), lambda m: callable(getattr(_, m, None)))


def test_chaining_methods():
    chain = _.chain([])

    for method in dir(_):
        if not callable(method):
            continue

        chained = getattr(chain, method)
        assert chained.method is getattr(_, method)


@parametrize(
    "value,methods", [([1, 2, 3, 4], [("without", (2, 3)), ("reject", (lambda x: x > 1,))])]
)
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
        _.chain([]).foobar  # noqa: B018
    except _.InvalidMethod:
        raised = True

    assert raised


def test_invalid_method_subclasses_attribute_error():
    # NOTE: This needs to subclass AttributeError due to compatibility with typing.Protocol and
    #  runtime_checkable. See https://github.com/dgilland/pydash/issues/165
    assert issubclass(_.InvalidMethod, AttributeError)


def test_chaining_lazy():
    tracker = {"called": False}

    def interceptor(value):
        tracker["called"] = True
        return value.pop()

    chain = _.chain([1, 2, 3, 4, 5]).initial().tap(interceptor)

    assert not tracker["called"]

    chain = chain.last()

    assert not tracker["called"]

    result = chain.value()

    assert tracker["called"]
    assert result == 3


def test_chaining_late_value():
    square_sum = _.chain().power(2).sum()
    assert square_sum([1, 2, 3, 4]) == 30


def test_chaining_late_value_reuse():
    square_sum = _.chain().power(2).sum()
    assert square_sum([1, 2, 3, 4]) == 30
    assert square_sum([2]) == 4


def test_chaining_late_value_override():
    square_sum = _.chain([1, 2, 3, 4]).power(2).sum()
    assert square_sum([5, 6, 7, 8]) == 174


@parametrize("keyword", [False, True])
def test_chaining_saved_method_calls_are_independent(keyword):
    mapper = _.chain([1, 2]).map_
    calls = []

    def double(value):
        calls.append(value)
        return value * 2

    if keyword:
        first = mapper(iteratee=double)
        second = mapper(iteratee=lambda value: value + 10)
    else:
        first = mapper(double)
        second = mapper(lambda value: value + 10)

    assert calls == []
    assert second.value() == [11, 12]
    assert calls == []
    assert first.value() == [2, 4]
    assert calls == [1, 2]
    assert first.plant([3]).value() == [6]
    assert first.commit().value() == [2, 4]
    assert second.value() == [11, 12]


def test_chaining_saved_method_preserves_existing_pipeline():
    power = _.chain([1, 2, 3]).power
    squares = power(2).sum()
    cubes = power(3).sum()

    assert squares.value() == 14
    assert cubes.value() == 36
    assert squares([4, 5]) == 41
    assert squares.value() == 14


def test_chaining_saved_method_with_late_values():
    power = _.chain().map_(lambda value: value + 1).power
    squares = power(2).sum()
    cubes = power(3).sum()

    assert squares([1, 2]) == 13
    assert cubes([1, 2]) == 35
    assert squares([3]) == 16
    assert cubes([3]) == 64


def test_chaining_plant():
    value = [1, 2, 3, 4]
    square_sum1 = _.chain(value).power(2).sum()

    def root_value(wrapper):
        if isinstance(wrapper._value, _.chaining.chaining.ChainWrapper):
            return root_value(wrapper._value)
        return wrapper._value

    assert root_value(square_sum1._value) == value

    test_value = [5, 6, 7, 8]
    square_sum2 = square_sum1.plant(test_value)

    assert root_value(square_sum1._value) == value
    assert root_value(square_sum2._value) == test_value

    assert square_sum1.value() == 30
    assert square_sum2.value() == 174


def test_chaining_commit():
    chain = _.chain([1, 2, 3, 4]).power(2).sum()
    committed = chain.commit()

    assert chain is not committed
    assert chain.value() == committed.value()


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
    methods = _.filter_(pydash_methods, lambda m: m.endswith("_"))
    assert methods

    for method in methods:
        assert getattr(_._, method[:-1]) is getattr(_, method)


def test_dash_method_call():
    value = [1, 2, 3, 4, 5]
    assert _._.initial(value) == _.initial(value)


def test_dash_alias():
    assert _.py_ is _._


@parametrize(
    "case,expected",
    [
        ([1, 2, 3], "[1, 2, 3]"),
    ],
)
def test_chaining_value_to_string(case, expected):
    assert _.chain(case).to_string() == expected


@parametrize("value,interceptor,expected", [([1, 2, 3, 4, 5], lambda value: value.pop(), 3)])
def test_tap(value, interceptor, expected):
    actual = _.chain(value).initial().tap(interceptor).last().value()
    assert actual == expected
