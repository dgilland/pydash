"""Supplied customizer callbacks are independent of their truth value."""

import pytest

import pydash as _


class Customizer:
    def __init__(self, callback):
        self.callback = callback
        self.calls = []

    def __call__(self, *args):
        self.calls.append(args)
        return self.callback(*args)


class FalseBoolCustomizer(Customizer):
    def __bool__(self):
        return False


class EmptyCustomizer(Customizer):
    def __len__(self):
        return 0


class NoTruthCustomizer(Customizer):
    def __bool__(self):
        raise AssertionError("customizer truth value must not be inspected")


CUSTOMIZERS = [FalseBoolCustomizer, EmptyCustomizer, NoTruthCustomizer]


@pytest.mark.parametrize("factory", CUSTOMIZERS)
@pytest.mark.parametrize("positional", [False, True])
@pytest.mark.parametrize("use_default", [False, True])
def test_assign_with_calls_supplied_customizer(factory, positional, use_default):
    customizer = factory(lambda old, new, *_: None if use_default else old + new)
    target = {"a": 5}
    source = {"a": 10}
    if positional:
        result = _.assign_with(target, source, customizer)
    else:
        result = _.assign_with(target, source, customizer=customizer)
    assert result is target
    assert result == {"a": 10 if use_default else 15}
    assert len(customizer.calls) == 1
    old, new, key, obj, src = customizer.calls[0]
    assert (old, new, key) == (5, 10, "a")
    assert obj is target
    assert src == source


@pytest.mark.parametrize("factory", CUSTOMIZERS)
@pytest.mark.parametrize("helper", [_.set_with, _.update_with])
def test_path_helpers_call_supplied_customizer(factory, helper):
    customizer = factory(lambda *_: {})
    target = {}
    value = 7 if helper is _.set_with else lambda old: (old or 0) + 7
    result = helper(target, "[0][1][2]", value, customizer=customizer)
    assert result is target
    assert result == {0: {1: {2: 7}}}
    assert len(customizer.calls) == 2
    assert customizer.calls[0] == (None, 0, target)
    assert customizer.calls[1] == (None, 1, target[0])
