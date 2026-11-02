import pytest

import pydash as _


def broken_generator(error):
    yield 1
    raise error


class BrokenSequence:
    def __init__(self, error):
        self.error = error

    def __getitem__(self, index):
        if index == 0:
            return 1
        raise self.error


class BrokenLengthHint:
    def __init__(self, error):
        self.error = error
        self.values = iter([1, 2])

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.values)

    def __length_hint__(self):
        raise self.error


class NonIterable:
    def __iter__(self):
        raise TypeError("iteration is unavailable")


@pytest.mark.parametrize("factory", [broken_generator, BrokenSequence])
@pytest.mark.parametrize("chained", [False, True])
def test_to_list_propagates_errors_after_obtaining_iterator(factory, chained):
    error = TypeError("item computation failed")
    source = factory(error)

    with pytest.raises(TypeError) as caught:
        if chained:
            _.chain(source).to_list().value()
        else:
            _.to_list(source)

    assert caught.value is error


@pytest.mark.parametrize("chained", [False, True])
def test_to_list_ignores_typeerror_in_optional_length_hint(chained):
    error = TypeError("length hint is unavailable")
    source = BrokenLengthHint(error)
    result = _.chain(source).to_list().value() if chained else _.to_list(source)

    assert result == list(BrokenLengthHint(error)) == [1, 2]


@pytest.mark.parametrize("source", [None, 42, object(), NonIterable()])
@pytest.mark.parametrize("chained", [False, True])
def test_to_list_still_wraps_noniterable_values(source, chained):
    result = _.chain(source).to_list().value() if chained else _.to_list(source)

    assert len(result) == 1
    assert result[0] is source
