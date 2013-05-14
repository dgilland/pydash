
import pydash as _

def test_compact():
    case = [0, 1, 2, 3]
    expected = [1, 2, 3]
    actual = _.compact(case)

    assert actual == expected

    case = [True, False, None, True, 1, 'foo']
    expected = [True, True, 1, 'foo']
    actual = _.compact(case)

    assert actual == expected

def test_difference():
    lst = [1, 2, 3, 4]
    lst1 = [2, 4]
    lst2 = [3, 5, 6]

    result = _.difference(lst, lst1, lst2)
    expected = [1]

    assert result == expected

def test_where():
    stooges = [
        { 'name': 'moe', 'age': 40 },
        { 'name': 'larry', 'age': 50 }
    ]

    assert _.where(stooges, {'age': 40}) == [{ 'name': 'moe', 'age': 40 }]

def test_pluck():
    stooges = [
        { 'name': 'moe', 'age': 40 },
        { 'name': 'larry', 'age': 50 }
    ]

    assert _.pluck(stooges, 'name') == ['moe', 'larry']

def test_rest():
    lst = [1, 2, 3]
    assert _.rest(lst) == [2, 3]
    assert _.rest(lst, 2) == [3]

    filter_fn = lambda val, index, lst: val < 3
    assert _.rest(lst, filter_fn) == [3]

    food = [
        { 'name': 'banana', 'organic': True },
        { 'name': 'beet',   'organic': False },
    ]
    assert _.rest(food, 'organic') == [{ 'name': 'beet', 'organic': False }]

    food = [
        { 'name': 'apple',  'type': 'fruit' },
        { 'name': 'banana', 'type': 'fruit' },
        { 'name': 'beet',   'type': 'vegetable' },
        { 'name': 'peach', 'type': 'fruit' }
    ]
    assert _.rest(food, {'type': 'fruit'}) == [{'name': 'beet', 'type': 'vegetable' }, { 'name': 'peach', 'type': 'fruit' }]

def test_find_index():
    food = ['apple', 'banana', 'beet']
    fn = lambda item, *args: item.startswith('b')
    assert _.find_index(food, fn) == 1

    food = [
        { 'name': 'apple',  'type': 'fruit' },
        { 'name': 'banana', 'type': 'fruit' },
        { 'name': 'beet',   'type': 'vegetable' }
    ]
    assert _.find_index(food, {'name': 'banana'}) == 1

def test_first():
    assert _.first([1, 2, 3]) == 1
    assert _.first([1, 2, 3], 2) == [1, 2]
    assert _.first([1, 2, 3], lambda item, *args: item < 3) == [1, 2]

    food = [
        { 'name': 'banana', 'organic': True },
        { 'name': 'beet',   'organic': False },
    ]

    # using "_.pluck" callback shorthand
    assert _.first(food, 'organic') == [{ 'name': 'banana', 'organic': True }]

    food = [
        { 'name': 'apple',  'type': 'fruit' },
        { 'name': 'banana', 'type': 'fruit' },
        { 'name': 'beet',   'type': 'vegetable' },
        { 'name': 'peach', 'type': 'fruit' }
    ]

    # using "_.where" callback shorthand
    assert _.first(food, { 'type': 'fruit' }) == [{ 'name': 'apple', 'type': 'fruit' }, { 'name': 'banana', 'type': 'fruit' }]

