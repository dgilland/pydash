import pydash as _


def typed_function(row: int, index: int, col: list):
    return row + 1


def test_annotated_iteratee():
    assert _.map_([1, 2], typed_function) == [2, 3]
