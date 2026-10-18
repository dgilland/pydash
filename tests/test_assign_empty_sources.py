"""An empty source sequence is an identity operation for assignment."""

import pytest

import pydash


@pytest.mark.parametrize("name", ["assign", "assign_with"])
@pytest.mark.parametrize("chained", [False, True])
@pytest.mark.parametrize("populated", [False, True])
def test_assignment_accepts_no_sources(name, chained, populated):
    nested = {"keep": [1, 2]}
    target = {"nested": nested} if populated else {}
    if chained:
        result = getattr(pydash.chain(target), name)().value()
    else:
        result = getattr(pydash, name)(target)
    assert result is target
    assert target == ({"nested": {"keep": [1, 2]}} if populated else {})
    if populated:
        assert target["nested"] is nested


def test_explicit_none_customizer_accepts_no_sources():
    target = {"a": 1}
    assert pydash.assign_with(target, customizer=None) is target


@pytest.mark.parametrize("positional", [False, True])
def test_no_source_does_not_call_customizer(positional):
    calls = []

    def customizer(value):
        calls.append(value)

    target = {"a": 1}
    if positional:
        result = pydash.assign_with(target, customizer)
    else:
        result = pydash.assign_with(target, customizer=customizer)
    assert result is target
    assert calls == []
