from copy import deepcopy
from functools import partial
import sys

import pytest

import pydash as _
from pydash.chaining.chaining import ChainWrapper
from pydash.helpers import UNSET


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


@parametrize("evaluation", ["value", "late", "override", "plant", "commit"])
def test_long_chains(evaluation):
    length = sys.getrecursionlimit() + 100
    chain = _.chain() if evaluation == "late" else _.chain(1)
    for _index in range(length):
        chain = chain.add(1)

    if evaluation == "value":
        assert chain.value() == length + 1
    elif evaluation == "late":
        assert chain(2) == length + 2
        assert chain(3) == length + 3
    elif evaluation == "override":
        assert chain(2) == length + 2
        assert chain.value() == length + 1
    elif evaluation == "plant":
        assert chain.plant(2).value() == length + 2
        assert chain.value() == length + 1
    else:
        committed = chain.commit()
        assert committed.value() == length + 1
        assert committed.value() == chain.value()


@parametrize("length", [3, sys.getrecursionlimit() + 100])
def test_long_chain_callback_order_and_reuse(length):
    calls = []

    def step(value, index):
        calls.append(index)
        return value + 1

    chain = _.chain(0)
    for index in range(length):
        chain = chain.apply(partial(step, index=index))

    assert calls == []
    for _attempt in range(2):
        calls.clear()
        assert chain.value() == length
        assert calls == list(range(length))


def test_chain_preserves_wrapper_unwrap_overrides():
    calls = []

    class CustomWrapper(ChainWrapper):
        def unwrap(self, value=UNSET):
            calls.append("override")
            return super().unwrap(value) * 2

    inner = CustomWrapper(3, lambda value: value + 1)
    outer = ChainWrapper(inner, lambda value: value - 1)
    assert outer.unwrap() == 7
    assert outer.unwrap(5) == 11
    assert calls == ["override", "override"]


def test_chain_preserves_instance_unwrap_overrides():
    inner = ChainWrapper(3, lambda value: value + 1)
    inner.unwrap = lambda value=UNSET: 42
    outer = ChainWrapper(inner, lambda value: value + 1)
    assert outer.unwrap() == 43


def test_chain_preserves_unwrap_bound_to_another_wrapper():
    other = ChainWrapper(10, lambda value: value + 2)
    inner = ChainWrapper(3, lambda value: value + 1)
    inner.unwrap = other.unwrap
    outer = ChainWrapper(inner, lambda value: value + 1)
    assert outer.unwrap() == 13
    assert outer.unwrap(5) == 8


def test_chain_looks_up_unwrap_descriptors_once():
    lookups = []

    class CustomWrapper(ChainWrapper):
        @property
        def unwrap(self):
            lookups.append(self)
            return lambda value=UNSET: 42

    inner = CustomWrapper(3, lambda value: value + 1)
    outer = ChainWrapper(inner, lambda value: value + 1)
    assert outer.unwrap() == 43
    assert lookups == [inner]


@parametrize("nested", [False, True])
@parametrize("value", [UNSET, 5])
def test_chain_method_properties_observe_resolved_clone_values(nested, value):
    class PropertyWrapper(ChainWrapper):
        def __init__(self, initial):
            self._value = initial
            self.args = ()
            self.kwargs = {}

        @property
        def method(self):
            return lambda argument: (argument, self._value)

    initial = ChainWrapper(2, lambda argument: argument + 1) if nested else 2
    wrapper = PropertyWrapper(initial)
    expected = (2 if value is UNSET else value) + int(nested)
    assert wrapper.unwrap(value) == (expected, expected)
    assert wrapper._value is initial


def test_chain_preserves_replaced_base_unwrap(monkeypatch):
    original = ChainWrapper.unwrap
    calls = []

    def recording_unwrap(wrapper, value=UNSET):
        calls.append(wrapper)
        return original(wrapper, value)

    monkeypatch.setattr(ChainWrapper, "unwrap", recording_unwrap)
    inner = ChainWrapper(2, lambda value: value + 1)
    outer = ChainWrapper(inner, lambda value: value + 1)
    assert outer.unwrap() == 4
    assert calls == [outer, inner]


@parametrize("value", [UNSET, 7])
def test_chain_preserves_unset_result_fallback(value):
    inner = ChainWrapper(3, lambda _value: UNSET)
    outer = ChainWrapper(inner, lambda result: result)
    assert outer.unwrap(value) is value


def test_chain_stops_at_callback_errors_and_can_be_retried():
    calls = []
    failure = RuntimeError("callback failed")

    def step(value):
        calls.append(value)
        if len(calls) == 1:
            raise failure
        return value + 1

    chain = _.chain(1).apply(step).add(2)
    with pytest.raises(RuntimeError) as exc:
        chain.value()
    assert exc.value is failure
    assert calls == [1]
    assert chain.value() == 4
    assert calls == [1, 1]


@parametrize("length", [1, 3])
def test_chain_preserves_errors_for_cyclic_wrappers(length):
    first = ChainWrapper(0, _.identity)
    outer = first
    for _index in range(length - 1):
        outer = ChainWrapper(outer, _.identity)
    first._value = outer

    with pytest.raises(RecursionError):
        outer.unwrap()


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
