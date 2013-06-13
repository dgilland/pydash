
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

    # verify alias
    assert _.tail is _.rest

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
    _.take is _.first

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

def test_intersection():
    assert _.intersection([1, 2, 3], [101, 2, 1, 10], [2, 1]) == [1, 2]

def test_last():
    assert _.last([1, 2, 3]) == 3
    assert _.last([1, 2, 3], 2) == [2, 3]
    assert _.last([1, 2, 3], lambda num, *args: num > 1) == [2, 3]

    # test pluck style callback
    food = [
        { 'name': 'beet',   'organic': False },
        { 'name': 'carrot', 'organic': True }
    ]

    assert _.last(food, 'organic') == [{ 'name': 'carrot', 'organic': True }]

    # test where style callback
    food = [
        { 'name': 'banana', 'type': 'fruit' },
        { 'name': 'beet',   'type': 'vegetable' },
        { 'name': 'carrot', 'type': 'vegetable' }
    ]

    assert _.last(food, { 'type': 'vegetable' }) == [{ 'name': 'beet', 'type': 'vegetable' }, { 'name': 'carrot', 'type': 'vegetable' }]

def test_last_index_of():
    assert _.last_index_of([1, 2, 3, 1, 2, 3], 2) == 4
    assert _.last_index_of([1, 2, 3, 1, 2, 3], 2, 3) == 1

def test_zip_object():
    assert _.zip_object(['moe', 'larry'], [30, 40]) == { 'moe': 30, 'larry': 40 }
    assert _.zip_object([['moe', 30], ['larry', 40]]) == { 'moe': 30, 'larry': 40 }

    # verify alias
    _.obj is _.zip_object

def test_zipup():
    assert _.zipup(['moe', 'larry', 'curly'], [30, 40, 35], [True, False, True]) == [['moe', 30, True], ['larry', 40, False], ['curly', 35, True]]

def test_unzip():
    assert _.unzip([['moe', 30, True], ['larry', 40, False], ['curly', 35, True]]) == [['moe', 'larry', 'curly'], [30, 40, 35], [True, False, True]]

def test_ranged():
    assert _.ranged is range

    assert _.ranged(10) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert _.ranged(1, 11) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert _.ranged(0, 30, 5) == [0, 5, 10, 15, 20, 25]
    assert _.ranged(0, -10, -1) == [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
    assert _.ranged(0) == []

def test_without():
    assert _.without([1, 2, 1, 0, 3, 1, 4], 0, 1) == [2, 3, 4]

def test_uniq():

    assert _.uniq([1, 2, 1, 3, 1]) == [1, 2, 3]
    assert _.uniq([dict(a=1), dict(a=2), dict(a=1)]) == [dict(a=1), dict(a=2)]

    # using function callback
    import math
    assert _.uniq([1, 2, 1.5, 3, 2.5], lambda num, *args: math.floor(num)) == [1, 2, 3]

    # test where style callback
    food = [
        { 'name': 'banana', 'type': 'fruit' },
        { 'name': 'apple', 'type': 'fruit' },
        { 'name': 'beet',   'type': 'vegetable' },
        { 'name': 'beet',   'type': 'vegetable' },
        { 'name': 'carrot', 'type': 'vegetable' },
        { 'name': 'carrot', 'type': 'vegetable' }
    ]

    assert _.uniq(food, { 'type': 'vegetable' }) == [
        { 'name': 'beet', 'type': 'vegetable' },
        { 'name': 'carrot', 'type': 'vegetable' }
    ]

    # test pluck style callback
    pluck = [
        { 'x': 1, 'y': 1 },
        { 'x': 2, 'y': 1 },
        { 'x': 1, 'y': 1 }
    ]

    assert _.uniq(pluck, 'x') == [{ 'x': 1, 'y': 1 }, { 'x': 2, 'y': 1 }]

    # verify alias
    assert _.unique is _.uniq

def test_union():
    assert _.union([1, 2, 3], [101, 2, 1, 10], [2, 1]) == [1, 2, 3, 101, 10]

def test_sorted_index():
    assert _.sorted_index([20, 30, 50], 40) == 2
    assert _.sorted_index([20, 30, 50], 10) == 0

    # test pluck style callback
    assert _.sorted_index([{ 'x': 20 }, { 'x': 30 }, { 'x': 50 }], { 'x': 40 }, 'x' ) == 2

    # test function callback
    lookup = {
      'words': { 'twenty': 20, 'thirty': 30, 'fourty': 40, 'fifty': 50 }
    }

    callback = lambda word: lookup['words'][word]
    assert _.sorted_index(['twenty', 'thirty', 'fifty'], 'fourty', callback) == 2

def test_every():
    assert _.every([True, 1, None, 'yes'], bool) is False
    assert _.every([True, 1, None, 'yes']) is False

    stooges = [
        { 'name': 'moe', 'age': 40 },
        { 'name': 'larry', 'age': 50 }
    ]

    # test pluck style callback
    assert _.every(stooges, 'age') is True

    # test where style callback
    assert _.every(stooges, { 'age': 50 }) is False

def test_some():
    assert _.some([None, 0, 'yes', False], bool) is True
    assert _.some([None, 0, 'yes', False]) is True

    food = [
        { 'name': 'apple',  'organic': False, 'type': 'fruit' },
        { 'name': 'carrot', 'organic': True,  'type': 'vegetable' }
    ]

    # test pluck style callback
    assert _.some(food, 'organic') is True

    # test where style callback
    assert _.some(food, { 'type': 'meat' }) is False

def test_collect():
    assert _.collect([1, 2, 3]) == [1, 2, 3]
    assert _.collect([1, 2, 3], lambda num, *args: num * 3) == [3, 6, 9]

    assert sorted(_.collect({ 'one': 1, 'two': 2, 'three': 3 }, lambda num, *args: num * 3)) == [3, 6, 9]

    stooges = [
        { 'name': 'moe', 'age': 40 },
        { 'name': 'larry', 'age': 50 }
    ]

    assert _.collect(stooges, 'name') == ['moe', 'larry']

