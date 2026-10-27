from typing import Any

import pytest
from typing_extensions import assert_type

import pydash as _


@pytest.mark.mypy_testing
def test_invoke_map_callable_types() -> None:
    def prefix(value: str, *, text: str) -> str:
        return text + value

    assert_type(_.invoke_map(["ab", "cd"], str.upper), list[str])
    assert_type(_.invoke_map(["ab", "c"], len), list[int])
    assert_type(_.invoke_map(["ab"], "upper"), list[Any])
    assert_type(_.chain(["ab"]).invoke_map(str.upper).value(), list[str])
    assert_type(_.invoke_map(["ab"], prefix, text="!"), list[str])
