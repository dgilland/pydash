import typing as t

import pytest
from typing_extensions import assert_type

import pydash as _


@pytest.mark.mypy_testing
def test_zip_object_iterable_value_types() -> None:
    assert_type(_.zip_object(["a", "b"], (1, 2)), t.Dict[str, int])
    assert_type(_.zip_object(["a", "b"], range(2)), t.Dict[str, int])
    assert_type(_.zip_object(["a", "b"], iter([1, 2])), t.Dict[str, int])
    assert_type(_.zip_object(["a", "b"], (n for n in [1, 2])), t.Dict[str, int])
    assert_type(_.zip_object(["a", "b"], {"x": 1, "y": 2}.values()), t.Dict[str, int])
    assert_type(_.zip_object(iter(["a", "b"]), "xy"), t.Dict[str, str])


@pytest.mark.mypy_testing
def test_zip_object_chained_iterable_value_types() -> None:
    assert_type(_.chain(["a", "b"]).zip_object((1, 2)).value(), t.Dict[str, int])
    assert_type(_.chain(["a", "b"]).zip_object(range(2)).value(), t.Dict[str, int])
    assert_type(_.chain(["a", "b"]).zip_object(iter([1, 2])).value(), t.Dict[str, int])


@pytest.mark.mypy_testing
def test_zip_object_deep_sequence_value_types() -> None:
    values: t.Sequence[int] = range(2)
    assert_type(_.zip_object_deep(["a.b", "a.c"], values), t.Dict[t.Any, t.Any])
    assert_type(_.zip_object_deep(["a.b", "a.c"], (1, 2)), t.Dict[t.Any, t.Any])
    assert_type(_.chain(["a.b", "a.c"]).zip_object_deep(values).value(), t.Dict[t.Any, t.Any])
