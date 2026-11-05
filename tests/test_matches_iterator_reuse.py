import pytest

import pydash as _


def generator_source(values):
    yield from values


def make_predicate(kind, source):
    if kind == "matches":
        return _.matches(source)
    return _.matches_property("items", source)


def candidate(kind, values):
    return values if kind == "matches" else {"items": values}


@pytest.mark.parametrize("kind", ["matches", "matches_property"])
@pytest.mark.parametrize("make_source", [iter, generator_source])
def test_iterator_criteria_are_reused_for_changing_candidates(kind, make_source):
    predicate = make_predicate(kind, make_source([1, 2]))

    assert predicate(candidate(kind, [1, 2])) is True
    assert predicate(candidate(kind, [9, 9])) is False
    assert predicate(candidate(kind, [1])) is False
    assert predicate(candidate(kind, [1, 2, 3])) is True
    assert predicate(candidate(kind, [1, 9])) is False


@pytest.mark.parametrize("kind", ["matches", "matches_property"])
def test_iterator_criteria_remain_lazy_and_short_circuit(kind):
    consumed = []

    def criteria():
        consumed.append(1)
        yield 1
        raise AssertionError("the unmatched tail should not be read")

    predicate = make_predicate(kind, criteria())
    assert consumed == []
    assert predicate(candidate(kind, [9])) is False
    assert predicate(candidate(kind, [9])) is False
    assert consumed == [1]


@pytest.mark.parametrize("kind", ["matches", "matches_property"])
def test_filter_reuses_iterator_based_predicate(kind):
    first = candidate(kind, [1, 2])
    second = candidate(kind, [9, 9])
    third = candidate(kind, [1, 2, 3])
    predicate = make_predicate(kind, iter([1, 2]))

    result = _.filter_([first, second, third], predicate)
    assert result == [first, third]
    assert result[0] is first
    assert result[1] is third


@pytest.mark.parametrize("kind", ["matches", "matches_property"])
def test_empty_iterator_criteria_remain_vacuous(kind):
    predicate = make_predicate(kind, iter([]))
    assert predicate(candidate(kind, [])) is True
    assert predicate(candidate(kind, [9])) is True


@pytest.mark.parametrize("kind", ["matches", "matches_property"])
def test_reiterable_criteria_still_reflect_mutation(kind):
    source = [1, 2]
    predicate = make_predicate(kind, source)
    assert predicate(candidate(kind, [1, 2])) is True

    source[0] = 9
    assert predicate(candidate(kind, [9, 2])) is True
    assert predicate(candidate(kind, [1, 2])) is False
