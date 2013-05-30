
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

    # verify alias
    _.head is _.first

def test_flatten():
    array = [1, ['2222'], [3, [[4]]]]
    assert _.flatten(array) == [1, '2222', 3, 4]
    assert _.flatten(array, True) == [1, '2222', 3, [[4]]]

    # test pluck style callback
    stooges = [
        { 'name': 'curly', 'quotes': ['Oh, a wise guy, eh?', 'Poifect!'] },
        { 'name': 'moe', 'quotes': ['Spread out!', 'You knucklehead!'] }
    ]

    assert _.flatten(stooges, 'quotes') == ['Oh, a wise guy, eh?', 'Poifect!', 'Spread out!', 'You knucklehead!']

def test_index_of():
    assert _.index_of([1, 2, 3, 1, 2, 3], 2) == 1
    assert _.index_of([1, 2, 3, 1, 2, 3], 2, 3) == 4
    assert _.index_of([1, 1, 2, 2, 3, 3], 2, True) == 2
    assert _.index_of([1, 1, 2, 2, 3, 3], 4) is False
    assert _.index_of([1, 1, 2, 2, 3, 3], 2, 10) is False

def test_initial():
    assert _.initial([1, 2, 3]) == [1, 2]
    assert _.initial([1, 2, 3], 2) == [1]
    assert _.initial([1, 2, 3], lambda num, *args: num > 1) == [1]

    # test pluck style callback
    food = [
        { 'name': 'beet',   'organic': False },
        { 'name': 'carrot', 'organic': True }
    ]
    assert _.initial(food, 'organic') == [{ 'name': 'beet',   'organic': False }]

    # test where style callback
    food = [
        { 'name': 'banana', 'type': 'fruit' },
        { 'name': 'beet',   'type': 'vegetable' },
        { 'name': 'carrot', 'type': 'vegetable' }
    ]
    assert _.initial(food, { 'type': 'vegetable' }) == [{ 'name': 'banana', 'type': 'fruit' }]

