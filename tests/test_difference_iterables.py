import pytest

import pydash


@pytest.mark.parametrize("factory", [list, tuple, iter])
@pytest.mark.parametrize("name", ["difference", "difference_by", "difference_with"])
def test_difference_accepts_iterable_sources(factory, name):
    function = getattr(pydash, name)
    assert function(factory([1, 2, 3, 1]), [1, 3]) == [2]
    assert function(factory([1, 2])) == [1, 2]


@pytest.mark.parametrize("name", ["difference", "difference_by", "difference_with"])
def test_exclusion_iterator_is_reused_for_every_value(name):
    function = getattr(pydash, name)
    assert function([1, 2, 3, 1], iter([1, 3])) == [2]
    assert function([1, 2], iter([])) == [1, 2]


def test_iterable_difference_respects_callbacks_and_keeps_references():
    first = {"id": 1}
    second = {"id": 2}
    values = [first, second, first]
    assert pydash.difference_by(iter(values), iter([{"id": 1}]), "id") == [second]
    result = pydash.difference_with(
        iter(values), iter([{"id": 1}]), lambda left, right: left["id"] == right["id"]
    )
    assert len(result) == 1
    assert result[0] is second
    assert values == [first, second, first]
