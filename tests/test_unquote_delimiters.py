"""Quote and unquote agree on the complete delimiter string."""

import pytest

import pydash


@pytest.mark.parametrize("delimiter", ["**", "<<<", "🙂🙂", -8])
@pytest.mark.parametrize("text", ["hello", "", "**nested**"])
def test_unquote_round_trips_quote_with_complete_delimiter(text, delimiter):
    assert pydash.unquote(pydash.quote(text, delimiter), delimiter) == text


@pytest.mark.parametrize(
    "text, delimiter",
    [
        ("**hello", "**"),
        ("hello**", "**"),
        ("*hello*", "**"),
        ("aaa", "aa"),
        ("*", "**"),
        ("hello", ""),
        ("hello", None),
    ],
)
def test_unquote_does_not_remove_incomplete_or_empty_delimiters(text, delimiter):
    assert pydash.unquote(text, delimiter) == text


def test_unquote_removes_one_delimiter_pair():
    assert pydash.unquote("****hello****", "**") == "**hello**"
