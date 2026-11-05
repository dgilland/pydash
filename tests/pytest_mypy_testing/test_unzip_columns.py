import typing as t

import pytest
from typing_extensions import assert_type

import pydash as _


@pytest.mark.mypy_testing
def test_unzip_pair_columns() -> None:
    rows = [(1, "a"), (2, "b"), (3, "c")]
    result = _.unzip(rows)
    assert_type(result, t.List[t.Union[t.Tuple[int, ...], t.Tuple[str, ...]]])
    assert result == [(1, 2, 3), ("a", "b", "c")]


@pytest.mark.mypy_testing
def test_unzip_wider_columns() -> None:
    triples = [(1, "a", b"x"), (2, "b", b"y")]
    result = _.unzip(triples)
    assert_type(result, t.List[t.Union[t.Tuple[int, ...], t.Tuple[str, ...], t.Tuple[bytes, ...]]])
    assert result == [(1, 2), ("a", "b"), (b"x", b"y")]

    quads = [(1, "a", b"x", 1.5)]
    result4 = _.unzip(quads)
    assert_type(
        result4,
        t.List[
            t.Union[t.Tuple[int, ...], t.Tuple[str, ...], t.Tuple[bytes, ...], t.Tuple[float, ...]]
        ],
    )
    assert result4 == [(1,), ("a",), (b"x",), (1.5,)]

    quints = [(1, "a", b"x", 1.5, None)]
    result5 = _.unzip(quints)
    assert_type(
        result5,
        t.List[
            t.Union[
                t.Tuple[int, ...],
                t.Tuple[str, ...],
                t.Tuple[bytes, ...],
                t.Tuple[float, ...],
                t.Tuple[None, ...],
            ]
        ],
    )
    assert result5 == [(1,), ("a",), (b"x",), (1.5,), (None,)]


@pytest.mark.mypy_testing
def test_unzip_iterator_columns() -> None:
    rows: t.Iterator[t.Tuple[int, str]] = iter([(1, "a"), (2, "b"), (3, "c")])
    result = _.unzip(rows)
    assert_type(result, t.List[t.Union[t.Tuple[int, ...], t.Tuple[str, ...]]])
    assert result == [(1, 2, 3), ("a", "b", "c")]


@pytest.mark.mypy_testing
def test_unzip_chain_columns() -> None:
    rows = [(1, "a"), (2, "b"), (3, "c")]
    result = _.chain(rows).unzip().value()
    assert_type(result, t.List[t.Union[t.Tuple[int, ...], t.Tuple[str, ...]]])
    assert result == [(1, 2, 3), ("a", "b", "c")]
