import math
import pydash
from pydash import fp, repack
from .fixtures import parametrize

# The following pydash functions are exposed unmodified:
#   compact
#   flatten
#   flatten_deep
#   from_pairs
#   head
#   initial
#   last
#   reverse
#   sorted_uniq
#   tail
#   uniq
#   unzip


# The following pydash functions are excluded:
#   pop
#   push
#   shift
#   splice
#   unshift

# The following functions should get special implementation
#   sort -> sort_by, sort_with


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 1), [[1], [2], [3], [4], [5]]),
    (([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]),
    (([1, 2, 3, 4, 5], 3), [[1, 2, 3], [4, 5]]),
    (([1, 2, 3, 4, 5], 4), [[1, 2, 3, 4], [5]]),
    (([1, 2, 3, 4, 5], 5), [[1, 2, 3, 4, 5]]),
    (([1, 2, 3, 4, 5], 6), [[1, 2, 3, 4, 5]]),
])
def test_chunk(case, expected):
    a, b = case
    assert fp.chunk(b)(a) == expected
    assert fp.chunk(b, a) == expected


@parametrize('case,expected', [
    (((), []), []),
    (((), [1, 2, 3]), [1, 2, 3]),
    (([1, 2, 3], ()), [1, 2, 3]),
    (([1, 2, 3], []), [1, 2, 3]),
    (([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6]),
    (([1, 2, 3], [4, 5, 6], [7]), [1, 2, 3, 4, 5, 6, 7]),
    ((1, [2], 3, 4), [1, 2, 3, 4]),
])
def test_concat(case, expected):
    a, b = repack("a, *b", *case)
    assert fp.concat(a)(*b) == expected
    assert fp.concat(a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4], [],), [1, 2, 3, 4]),
    (([1, 2, 3, 4], [2, 4, 3],), [1]),
    (([1, 2, 3, 4], [2, 4], [3, 5, 6],), [1]),
    (([1, 1, 1, 1], [2, 4], [3, 5, 6],), [1, 1, 1, 1])
])
def test_difference(case, expected):
    a, b = repack("a, *b", *case)
    assert fp.difference(a)(*b) == expected
    assert fp.difference(a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4], [], None), [1, 2, 3, 4]),
    (([1, 2, 3, 4], [2], [4], None), [1, 3]),
    (([1.2, 1.6, 2.8], [2.1], round), [1.2, 2.8]),
    (([1.2, 1.6, 2.8], [2.1], [3.2], round), [1.2]),
    (([{'a': 1}, {'a': 2, 'b': 2}], [{'a': 1}], 'a'), [{'a': 2, 'b': 2}]),
])
def test_difference_by(case, expected):
    a, b, c = repack("a, *b, c", *case)
    assert fp.difference_by(c)(a)(*b) == expected
    assert fp.difference_by(c)(a, *b) == expected
    assert fp.difference_by(c, a)(*b) == expected
    assert fp.difference_by(c, a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4], [], None), [1, 2, 3, 4]),
    (([1, 2, 3, 4], [2], [4], None), [1, 3]),
    (([{'a': 1}, {'a': 2, 'b': 2}], [{'a': 1}],
        lambda a, b: a['a'] == b['a']), [{'a': 2, 'b': 2}]),
])
def test_difference_with(case, expected):
    a, b, c = repack("a, *b, c", *case)
    assert fp.difference_with(c)(a)(*b) == expected
    assert fp.difference_with(c)(a, *b) == expected
    assert fp.difference_with(c, a)(*b) == expected
    assert fp.difference_with(c, a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 1), [2, 3, 4, 5]),
    (([1, 2, 3, 4, 5], 2), [3, 4, 5]),
    (([1, 2, 3, 4, 5], 5), []),
])
def test_drop(case, expected):
    a, b = case
    assert fp.drop(b, a) == expected
    assert fp.drop(b)(a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], lambda item: item < 3), [3, 4, 5]),
])
def test_drop_while(case, expected):
    a, b = case
    assert fp.drop_while(b)(a) == expected
    assert fp.drop_while(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 1), [1, 2, 3, 4]),
    (([1, 2, 3, 4, 5], 2), [1, 2, 3]),
    (([1, 2, 3, 4, 5], 5), []),
])
def test_drop_right(case, expected):
    a, b = case
    assert fp.drop_right(b, a) == expected
    assert fp.drop_right(b)(a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], lambda item: item > 3), [1, 2, 3]),
])
def test_drop_right_while(case, expected):
    a, b = case
    assert fp.drop_right_while(b)(a) == expected
    assert fp.drop_right_while(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 2, 1, 5, 6, 5, 5, 5]), [2, 1, 5]),
])
def test_duplicates(case, expected):
    a = case
    assert fp.duplicates(a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 0, 0, None), [0, 0, 0, 0, 0]),
    (([1, 2, 3, 4, 5], 0, 2, None), [1, 2, 0, 0, 0]),
    (([1, 2, 3, 4, 5], 0, 2, 3), [1, 2, 0, 4, 5]),
    (([1, 2, 3, 4, 5], 0, 0, 5), [0, 0, 0, 0, 0]),
    (([1, 2, 3, 4, 5], 0, 0, 8), [0, 0, 0, 0, 0]),
    (([1, 2, 3, 4, 5], 0, 0, -1), [0, 0, 0, 0, 5]),
])
def test_fill(case, expected):
    a, b, c, d = case
    assert fp.fill(c)(d)(b)(a) == expected
    assert fp.fill(c, d)(b)(a) == expected
    assert fp.fill(c)(d, b)(a) == expected
    assert fp.fill(c)(d)(b, a) == expected
    assert fp.fill(c, d, b, a) == expected
    assert a != expected


@parametrize('case,filter_by,expected', [
    (['apple', 'banana', 'beet'], lambda item: item.startswith('b'), 1),
    ([{'name': 'apple', 'type': 'fruit'},
      {'name': 'banana', 'type': 'fruit'},
      {'name': 'beet', 'type': 'vegetable'}],
     {'name': 'banana'},
     1),
    (['apple', 'banana', 'beet'], lambda: False, -1)
])
def test_find_index(case, filter_by, expected):
    assert fp.find_index(filter_by)(case) == expected
    assert fp.find_index(filter_by, case) == expected


@parametrize('case,filter_by,expected', [
    (['apple', 'banana', 'beet'], lambda item: item.startswith('b'), 2),
    ([{'name': 'apple', 'type': 'fruit'},
      {'name': 'banana', 'type': 'fruit'},
      {'name': 'beet', 'type': 'vegetable'}],
     {'type': 'fruit'},
     1),
    (['apple', 'banana', 'beet'], lambda: False, -1)
])
def test_find_last_index(case, filter_by, expected):
    assert fp.find_last_index(filter_by)(case) == expected
    assert fp.find_last_index(filter_by, case) == expected


@parametrize('case,expected', [
    (([1, ['2222'], [3, [[4]]]], 1), [1, '2222', 3, [[4]]]),
    (([1, ['2222'], [3, [[4]]]], 2), [1, '2222', 3, [4]]),
    (([1, ['2222'], [3, [[4]]]], 3), [1, '2222', 3, 4]),
])
def test_flatten_depth(case, expected):
    a, b = case
    assert fp.flatten_depth(b)(a) == expected
    assert fp.flatten_depth(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 1, 2, 3], 2), 1),
    (([1, 2, 3, 1, 2, 3], 2, 0), 1),
    (([1, 2, 3, 1, 2, 3], 2, 3), 4),
    (([1, 1, 2, 2, 3, 3], 2, True), 2),
    (([1, 1, 2, 2, 3, 3], 4, 0), -1),
    (([1, 1, 2, 2, 3, 3], 2, 10), -1),
    (([1, 1, 2, 2, 3, 3], 0, 0), -1),
])
def test_index_of(case, expected):
    a, b, c = repack("a, b, *c", *case)
    assert fp.index_of(b)(a, *c) == expected
    assert fp.index_of(b, a, *c) == expected


@parametrize('case,expected', [
    (([[10, 20], [30, 40], [50, 60]], [1, 2, 3]),
     [10, 20, 1, 2, 3, 30, 40, 1, 2, 3, 50, 60]),
    (([[[10, 20]], [[30, 40]], [50, [60]]], [1, 2, 3]),
     [[10, 20], 1, 2, 3, [30, 40], 1, 2, 3, 50, [60]]),
])
def test_intercalate(case, expected):
    a, b = case
    assert fp.intercalate(b)(a) == expected
    assert fp.intercalate(b, a) == expected


@parametrize('case,expected', [
    (([1, 2], [3, 4]), [1, 3, 2, 4]),
    (([1, 2], [3, 4], [5, 6]), [1, 3, 5, 2, 4, 6]),
    (([1, 2], [3, 4, 5], [6]), [1, 3, 6, 2, 4, 5]),
    (([1, 2, 3], [4], [5, 6]), [1, 4, 5, 2, 6, 3]),
])
def test_interleave(case, expected):
    a, b = repack("a, *b", *case)
    assert fp.interleave(a)(*b) == expected
    assert fp.interleave(a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [101, 2, 1, 10], [2, 1]), [1, 2]),
    (([1, 1, 2, 2], [1, 1, 2, 2]), [1, 2]),
    (([1, 2, 3], [4]), []),
    (([], [101, 2, 1, 10], [2, 1]), []),
    (([], ()), [])
])
def test_intersection(case, expected):
    a, b = repack("a, *b", *case)
    assert fp.intersection(a)(*b) == expected
    assert fp.intersection(a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [101, 2, 1, 10], [2], None), [2]),
    (([1, 2, 3], [101, 2, 1, 10], lambda a: 1 if a < 10 else 0), [1]),
    (([{'a': 1}, {'a': 2}, {'a': 3}], [{'a': 2}], 'a'), [{'a': 2}])
])
def test_intersection_by(case, expected):
    a, b, c = repack("a, *b, c", *case)
    assert fp.intersection_by(c)(a)(*b) == expected
    assert fp.intersection_by(c)(a, *b) == expected
    assert fp.intersection_by(c, a)(*b) == expected
    assert fp.intersection_by(c, a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [101, 2, 1, 10], None), [1, 2]),
    (([1, 2, 3], [101, 2, 1, 10], [1], None), [1]),
    (([], [101, 2, 1, 10], [2, 1], None), []),
    ((['A', 'b', 'cC'], ['a', 'cc'],
      lambda a, b: a.lower() == b.lower()),
     ['A', 'cC'])
])
def test_intersection_with(case, expected):
    a, b, c = repack("a, *b, c", *case)
    assert fp.intersection_with(c)(a)(*b) == expected
    assert fp.intersection_with(c)(a, *b) == expected
    assert fp.intersection_with(c, a)(*b) == expected
    assert fp.intersection_with(c, a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4], 10), [1, 10, 2, 10, 3, 10, 4]),
    (([1, 2, 3, 4], [0, 0, 0]), [1, [0, 0, 0], 2, [0, 0, 0], 3, [0, 0, 0], 4]),
    (([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [0, 0, 0]),
     [[1, 2, 3], [0, 0, 0], [4, 5, 6], [0, 0, 0], [7, 8, 9]]),
])
def test_intersperse(case, expected):
    a, b = case
    assert fp.intersperse(b)(a) == expected
    assert fp.intersperse(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 1, 2, 3], 2, 0), -1),
    (([1, 2, 3, 1, 2, 3], 2, 3), 1),
    (([1, 2, 3, 1, 2, 3], 0, 0), -1),
    (([0, 1, 2, 3, 4, 5], 3, 0), -1),
    (([0, 1, 2, 3, 4, 5], 3, 1), -1),
    (([0, 1, 2, 3, 4, 5], 3, 2), -1),
    (([0, 1, 2, 3, 4, 5], 3, 3), 3),
    (([0, 1, 2, 3, 4, 5], 3, 4), 3),
    (([0, 1, 2, 3, 4, 5], 3, 5), 3),
    (([0, 1, 2, 3, 4, 5], 3, 6), 3),
    (([0, 1, 2, 3, 4, 5], 3, -1), 3),
    (([0, 1, 2, 3, 4, 5], 3, -2), 3),
    (([0, 1, 2, 3, 4, 5], 3, -3), 3),
    (([0, 1, 2, 3, 4, 5], 3, -4), -1),
    (([0, 1, 2, 3, 4, 5], 3, -5), -1),
    (([0, 1, 2, 3, 4, 5], 3, -6), -1),
    (([0, 1, 2, 3, 4, 5], 3, None), 3),
    (([0, 1, 2, 3, 4, 5], 3), 3),
])
def test_last_index_of(case, expected):
    a, b, c = repack("a, b, *c", *case)
    assert fp.last_index_of(b)(a, *c) == expected
    assert fp.last_index_of(b, a, *c) == expected


@parametrize('case,expected', [
    (([1, 2, None, 4, None, 6],
      lambda x, i: ['{0}'.format(i)] if x is None else []),
     ['2', '4'])
])
def test_mapcat(case, expected):
    a, b = case
    assert fp.mapcat(b)(a) == expected
    assert fp.mapcat(b, a) == expected


@parametrize('case,expected', [
    (([11, 22, 33], 2), 33),
    (([11, 22, 33], 0), 11),
    (([11, 22, 33], -1), 33),
    (([11, 22, 33], 4), None),
    (([11, 22, 33], None), None),
])
def test_nth(case, expected):
    a, b = case
    assert fp.nth(b)(a) == expected
    assert fp.nth(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 1, 2, 3], 2), [1, 3, 1, 3])
])
def test_pull(case, expected):
    # pull is capped to two arguments
    a, b = case
    assert fp.pull(b)(a) == expected
    assert fp.pull(b, a) == expected
    assert a != expected


@parametrize('case,expected', [
    (([1, 2, 3, 1, 2, 3], [2, 3]), [1, 1]),
    (([1, 2, 3, 1, 2, 3], [1, 2, 3]), []),
    (([1, 2, 3, 1, 2, 3], [1, 2, 3, 1, 2, 3]), []),
])
def test_pull_all(case, expected):
    a, b = case
    assert fp.pull_all(b)(a) == expected
    assert fp.pull_all(b, a) == expected
    assert a != expected


@parametrize('case,expected', [
    (([1, 2, 3, 1, 2, 3], [2, 3], None), [1, 1]),
    (([1, 2, 3, 1, 2, 3], [2, 3], lambda item: item + 2), [1, 1])
])
def test_pull_all_by(case, expected):
    a, b, c = case
    assert fp.pull_all_by(c)(b)(a) == expected
    assert fp.pull_all_by(c)(b, a) == expected
    assert fp.pull_all_by(c, b)(a) == expected
    assert fp.pull_all_by(c, b, a) == expected
    assert a != expected


@parametrize('case,expected', [
    (([1, 2, 3, 1, 2, 3], [2, 3], None), [1, 1]),
    (([1, 2, 3, 1, 2, 3], [2, 3], lambda a, b: a == b), [1, 1]),
    (([1, 2, 3, 1, 2, 3], [2, 3], lambda a, b: a != b), [])
])
def test_pull_all_with(case, expected):
    a, b, c = case
    assert fp.pull_all_with(c)(b)(a) == expected
    assert fp.pull_all_with(c)(b, a) == expected
    assert fp.pull_all_with(c, b)(a) == expected
    assert fp.pull_all_with(c, b, a) == expected
    assert a != expected


@parametrize('case,expected', [
    (([1, 2, 3, 1, 2, 3], [2, 3]), [1, 2, 2, 3]),
    (([1, 2, 3, 1, 2, 3], [3, 2]), [1, 2, 2, 3]),
    (([1, 2, 3, 1, 2, 3], 3), [1, 2, 3, 2, 3])
])
def test_pull_at(case, expected):
    a, b = case
    assert fp.pull_at(b)(a) == expected
    assert fp.pull_at(b, a) == expected
    assert a != expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5, 6], lambda x: x % 2 == 0), [2, 4, 6]),
    (([1, 2, 3, 4], lambda x: x >= 3), [3, 4]),
])
def test_remove(case, expected):
    a, b = case
    assert fp.remove(b)(a) == expected
    assert fp.remove(b, a) == expected
    assert a != expected


@parametrize('case,expected', [
    (("a, b, c", 1, 2, 3), (1, 2, 3)),
    (("a, *b, c", 1, 3), (1, (), 3)),
    (("a, *b, c", 1, 2, 3), (1, (2,), 3)),
    (("a, *b, c", 1, 2, 3, 4), (1, (2, 3), 4)),
    (("a, b, *c", 1, 2, 3, 4), (1, 2, (3, 4))),
])
def test_repack(case, expected):
    a, b = repack("a, *b", *case)
    assert fp.repack(a)(*b) == expected
    assert fp.repack(a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 0, 1), [1]),
    (([1, 2, 3, 4, 5], 1, 3), [2, 3]),
    (([1, 2, 3, 4, 5], 1, 4), [2, 3, 4]),
    (([1, 2, 3, 4, 5], 1, 5), [2, 3, 4, 5]),
    (([1, 2, 3, 4, 5], 0, -1), [1, 2, 3, 4]),
    (([1, 2, 3, 4, 5], 2, None), [3]),
    (([1, 2, 3, 4, 5], -1, None), [5]),
    (([1, 2, 3, 4, 5], -2, None), [4]),
    (([1, 2, 3, 4, 5], -3, None), [3]),
    (([1, 2, 3, 4, 5], -5, None), [1]),
])
def test_slice_(case, expected):
    a, b, c = case
    assert fp.slice_(b, c)(a) == expected
    assert fp.slice_(b)(c)(a) == expected
    assert fp.slice_(b)(c, a) == expected
    assert fp.slice_(b, c, a) == expected


@parametrize('case,expected', [
    (([4, 4, 5, 5, 6, 6], 5), 2),
    (([20, 30, 40, 40, 50], 40), 2),
    (([20, 30, 50], 40), 2),
    (([20, 30, 50], 10), 0),
])
def test_sorted_index(case, expected):
    a, b = case
    assert fp.sorted_index(b)(a) == expected
    assert fp.sorted_index(b, a) == expected


@parametrize('case,expected', [
    (([{'x': 20}, {'x': 30}, {'x': 50}], {'x': 40}, 'x'), 2),
    ((['twenty', 'thirty', 'fifty'],
      'fourty',
      lambda x: {'twenty': 20, 'thirty': 30, 'fourty': 40, 'fifty': 50}[x]),
     2)
])
def test_sorted_index_by(case, expected):
    a, b, c = case
    assert fp.sorted_index_by(b, c)(a) == expected
    assert fp.sorted_index_by(b)(c)(a) == expected
    assert fp.sorted_index_by(b)(c, a) == expected
    assert fp.sorted_index_by(b, c, a) == expected


@parametrize('case,expected', [
    (([2, 3, 4, 10, 10], 10), 3),
    (([10, 10, 4, 2, 3], 11), -1),
])
def test_sorted_index_of(case, expected):
    a, b = case
    assert fp.sorted_index_of(b)(a) == expected
    assert fp.sorted_index_of(b, a) == expected


@parametrize('case,expected', [
    (([4, 4, 5, 5, 6, 6], 5), 4),
    (([20, 30, 40, 40, 50], 40), 4),
    (([20, 30, 50], 10), 0),
])
def test_sorted_last_index(case, expected):
    a, b = case
    assert fp.sorted_last_index(b)(a) == expected
    assert fp.sorted_last_index(b, a) == expected


@parametrize('case,expected', [
    (([{'x': 20}, {'x': 30}, {'x': 50}], {'x': 40}, 'x'), 2),
    ((['twenty', 'thirty', 'fifty'],
      'fourty',
      lambda x: {'twenty': 20, 'thirty': 30, 'fourty': 40, 'fifty': 50}[x]),
     2)
])
def test_sorted_last_index_by(case, expected):
    a, b, c = case
    assert fp.sorted_last_index_by(b, c)(a) == expected
    assert fp.sorted_last_index_by(b)(c)(a) == expected
    assert fp.sorted_index_by(b)(c, a) == expected
    assert fp.sorted_index_by(b, c, a) == expected


@parametrize('case,expected', [
    (([2, 3, 4, 10, 10], 10), 4),
    (([10, 10, 4, 2, 3], 11), -1),
])
def test_sorted_last_index_of(case, expected):
    a, b = case
    assert fp.sorted_last_index_of(b)(a) == expected
    assert fp.sorted_last_index_of(b, a) == expected


@parametrize('case,expected', [
    (([2.5, 3, 1, 2, 1.5], lambda num: math.floor(num)), [1, 2.5, 3]),
    ((['A', 'b', 'C', 'a', 'B', 'c'],
     lambda letter: letter.lower()),
     ['A', 'C', 'b'])
])
def test_sorted_uniq_by(case, expected):
    a, b = case
    assert fp.sorted_uniq_by(b)(a) == expected
    assert fp.sorted_uniq_by(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4, 5]]),
    (([1, 2, 3, 4, 5], 0), [[], [1, 2, 3, 4, 5]]),
])
def test_split_at(case, expected):
    a, b = case
    assert fp.split_at(b)(a) == expected
    assert fp.split_at(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 1), [1]),
    (([1, 2, 3, 4, 5], 2), [1, 2]),
    (([1, 2, 3, 4, 5], 5), [1, 2, 3, 4, 5]),
    (([1, 2, 3, 4, 5], 6), [1, 2, 3, 4, 5]),
])
def test_take(case, expected):
    a, b = case
    assert fp.take(b)(a) == expected
    assert fp.take(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], 1), [5]),
    (([1, 2, 3, 4, 5], 2), [4, 5]),
    (([1, 2, 3, 4, 5], 5), [1, 2, 3, 4, 5]),
    (([1, 2, 3, 4, 5], 6), [1, 2, 3, 4, 5]),
])
def test_take_right(case, expected):
    a, b = case
    assert fp.take_right(b)(a) == expected
    assert fp.take_right(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], lambda item: item > 3), [4, 5]),
])
def test_take_right_while(case, expected):
    a, b = case
    assert fp.take_right_while(b)(a) == expected
    assert fp.take_right_while(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], lambda item: item < 3), [1, 2]),
])
def test_take_while(case, expected):
    a, b = case
    assert fp.take_while(b)(a) == expected
    assert fp.take_while(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [101, 2, 1, 10], [2, 1]), [1, 2, 3, 101, 10]),
    (([11, 22, 33], []), [11, 22, 33])
])
def test_union(case, expected):
    a, b = repack("a, *b", *case)
    assert fp.union(a)(*b) == expected
    assert fp.union(a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [2, 3, 4], lambda x: x % 10), [1, 2, 3, 4]),
    (([1, 2, 3], [2, 3, 4], lambda x: x % 2), [1, 2]),
    (([11, 22, 33], [6], None), [11, 22, 33, 6]),
    (([11, 22, 33], [6], [8], None), [11, 22, 33, 6, 8]),
    (([11, 22, 33], [], None), [11, 22, 33]),
])
def test_union_by(case, expected):
    a, b, c = repack("a, *b, c", *case)
    assert fp.union_by(c)(a)(*b) == expected
    assert fp.union_by(c)(a, *b) == expected
    assert fp.union_by(c, a)(*b) == expected
    assert fp.union_by(c, a, *b) == expected


@parametrize('case,expected', [
    (([11, 22, 33], [22, 33, 44], None), [11, 22, 33, 44]),
    (([11, 22, 33], [], None), [11, 22, 33]),
    (([11, 22, 33], [], [26], [48], None), [11, 22, 33, 26, 48]),
    (([1, 2, 3], [2, 3, 4], lambda a, b: (a % 2) == (b % 2)), [1, 2])
])
def test_union_with(case, expected):
    a, b, c = repack("a, *b, c", *case)
    assert fp.union_with(c)(a)(*b) == expected
    assert fp.union_with(c)(a, *b) == expected
    assert fp.union_with(c, a)(*b) == expected
    assert fp.union_with(c, a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 1.5, 3, 2.5], lambda num: math.floor(num)), [1, 2, 3]),
    (([{'name': 'banana', 'type': 'fruit'},
      {'name': 'apple', 'type': 'fruit'},
      {'name': 'beet', 'type': 'vegetable'},
      {'name': 'beet', 'type': 'vegetable'},
      {'name': 'carrot', 'type': 'vegetable'},
      {'name': 'carrot', 'type': 'vegetable'}],
     {'type': 'vegetable'}),
     [{'name': 'banana', 'type': 'fruit'},
      {'name': 'beet', 'type': 'vegetable'}]),
    (([{'x': 1, 'y': 1}, {'x': 2, 'y': 1}, {'x': 1, 'y': 1}], 'x'),
     [{'x': 1, 'y': 1}, {'x': 2, 'y': 1}]),
    ((['A', 'b', 'C', 'a', 'B', 'c'], lambda letter: letter.lower()),
     ['A', 'b', 'C'])
])
def test_uniq_by(case, expected):
    a, b = case
    assert fp.uniq_by(b)(a) == expected
    assert fp.uniq_by(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3, 4, 5], lambda a, b: (a % 2) == (b % 2)), [1, 2]),
    (([5, 4, 3, 2, 1], lambda a, b: (a % 2) == (b % 2)), [5, 4]),
])
def test_uniq_with(case, expected):
    a, b = case
    assert fp.uniq_with(b)(a) == expected
    assert fp.uniq_with(b, a) == expected


@parametrize('case,expected', [
    (([[1, 10, 100], [2, 20, 200]], None), [[1, 2], [10, 20], [100, 200]]),
    (([[2, 4, 6], [2, 2, 2]], pydash.power), [4, 16, 36]),
])
def test_unzip_with(case, expected):
    a, b = case
    assert fp.unzip_with(b)(a) == expected
    assert fp.unzip_with(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 1, 0, 3, 1, 4], 1), [2, 0, 3, 4])
])
def test_without(case, expected):
    a, b = case
    assert fp.without(b)(a) == expected
    assert fp.without(b, a) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [5, 2, 1, 4]), [3, 5, 4]),
    (([1, 2, 5], [2, 3, 5], [3, 4, 5]), [1, 4, 5])
])
def test_xor(case, expected):
    a, b = repack("a, *b", *case)
    assert fp.xor(a)(*b) == expected
    assert fp.xor(a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [5, 4], lambda val: val % 3), [3]),
    (([1, 2, 3], [5, 4], [3], lambda val: val % 3), []),
])
def test_xor_by(case, expected):
    a, b, c = repack("a, *b, c", *case)
    assert fp.xor_by(c)(a)(*b) == expected
    assert fp.xor_by(c)(a, *b) == expected
    assert fp.xor_by(c, a)(*b) == expected
    assert fp.xor_by(c, a, *b) == expected


@parametrize('case,expected', [
    (([1, 2, 3], [5, 4], lambda a, b: a <= b), [5, 4]),
])
def test_xor_with(case, expected):
    a, b, c = repack("a, *b, c", *case)
    assert fp.xor_with(c)(a)(*b) == expected
    assert fp.xor_with(c)(a, *b) == expected
    assert fp.xor_with(c, a)(*b) == expected
    assert fp.xor_with(c, a, *b) == expected


@parametrize('case,expected', [
    ((['moe', 'larry', 'curly'],
      [30, 40, 35],
      [True, False, True]),
     [['moe', 30, True], ['larry', 40, False], ['curly', 35, True]])
])
def test_zip_(case, expected):
    a, b = repack("a, *b", *case)
    assert fp.zip_(a)(*b) == expected
    assert fp.zip_(a, *b) == expected


@parametrize('case,expected', [
    ((['moe', 'larry'], [30, 40]), {'moe': 30, 'larry': 40}),
])
def test_zip_object(case, expected):
    a, b = case
    assert fp.zip_object(a)(b) == expected
    assert fp.zip_object(a, b) == expected


@parametrize('case,expected', [
    ((['a.b.c', 'a.b.d'], [1, 2]), {'a': {'b': {'c': 1, 'd': 2}}}),
    ((['a.b[0].c', 'a.b[1].d'], [1, 2]), {'a': {'b': [{'c': 1}, {'d': 2}]}})
])
def test_zip_object_deep(case, expected):
    a, b = case
    assert fp.zip_object_deep(a)(b) == expected
    assert fp.zip_object_deep(a, b) == expected


@parametrize('case,expected', [
    (([1, 2], [3, 4], pydash.add), [4, 6]),
    (([1, 2], [3, 4], [5, 6], pydash.add), [9, 12]),
])
def test_zip_with(case, expected):
    a, b, c = repack("a, *b, c", *case)
    assert fp.zip_with(c)(a)(*b) == expected
    assert fp.zip_with(c)(a, *b) == expected
    assert fp.zip_with(c, a)(*b) == expected
    assert fp.zip_with(c, a, *b) == expected
