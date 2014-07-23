
import pydash as pyd


def test_compact():
    case = [0, 1, 2, 3]
    expected = [1, 2, 3]
    actual = pyd.compact(case)

    assert actual == expected

    case = [True, False, None, True, 1, 'foo']
    expected = [True, True, 1, 'foo']
    actual = pyd.compact(case)

    assert actual == expected


def test_difference():
    lst = [1, 2, 3, 4]
    lst1 = [2, 4]
    lst2 = [3, 5, 6]

    result = pyd.difference(lst, lst1, lst2)
    expected = [1]

    assert result == expected


def test_where():
    stooges = [
        {'name': 'moe', 'age': 40},
        {'name': 'larry', 'age': 50}
    ]

    assert pyd.where(stooges, {'age': 40}) == [{'name': 'moe', 'age': 40}]


def test_pluck():
    stooges = [
        {'name': 'moe', 'age': 40},
        {'name': 'larry', 'age': 50}
    ]

    assert pyd.pluck(stooges, 'name') == ['moe', 'larry']


def test_rest():
    lst = [1, 2, 3]
    assert pyd.rest(lst) == [2, 3]
    assert pyd.rest(lst, 2) == [3]

    filter_fn = lambda val, index, lst: val < 3
    assert pyd.rest(lst, filter_fn) == [3]

    food = [
        {'name': 'banana', 'organic': True},
        {'name': 'beet',   'organic': False},
    ]

    expected = [{'name': 'beet', 'organic': False}]

    assert pyd.rest(food, 'organic') == expected

    food = [
        {'name': 'apple',  'type': 'fruit'},
        {'name': 'banana', 'type': 'fruit'},
        {'name': 'beet',   'type': 'vegetable'},
        {'name': 'peach', 'type': 'fruit'}
    ]
    expected = [
        {'name': 'beet', 'type': 'vegetable'},
        {'name': 'peach', 'type': 'fruit'}
    ]

    assert pyd.rest(food, {'type': 'fruit'}) == expected

    # verify alias
    assert pyd.tail is pyd.rest


def test_find_index():
    food = ['apple', 'banana', 'beet']
    fn = lambda item, *args: item.startswith('b')
    assert pyd.find_index(food, fn) == 1

    food = [
        {'name': 'apple',  'type': 'fruit'},
        {'name': 'banana', 'type': 'fruit'},
        {'name': 'beet',   'type': 'vegetable'}
    ]
    assert pyd.find_index(food, {'name': 'banana'}) == 1


def test_find_last_index():
    food = ['apple', 'banana', 'beet']
    fn = lambda item, *args: item.startswith('b')
    assert pyd.find_last_index(food, fn) == 2

    food = [
        {'name': 'apple',  'type': 'fruit'},
        {'name': 'banana', 'type': 'fruit'},
        {'name': 'beet',   'type': 'vegetable'}
    ]
    assert pyd.find_last_index(food, {'type': 'fruit'}) == 1


def test_first():
    assert pyd.first([1, 2, 3]) == 1
    assert pyd.first([1, 2, 3], 2) == [1, 2]
    assert pyd.first([1, 2, 3], lambda item, *args: item < 3) == [1, 2]

    food = [
        {'name': 'banana', 'organic': True},
        {'name': 'beet',   'organic': False},
    ]

    # using "pyd.pluck" callback shorthand
    expected = [{'name': 'banana', 'organic': True}]
    assert pyd.first(food, 'organic') == expected

    food = [
        {'name': 'apple',  'type': 'fruit'},
        {'name': 'banana', 'type': 'fruit'},
        {'name': 'beet',   'type': 'vegetable'},
        {'name': 'peach', 'type': 'fruit'}
    ]

    # using "pyd.where" callback shorthand
    expected = [
        {'name': 'apple', 'type': 'fruit'},
        {'name': 'banana', 'type': 'fruit'}

    ]
    assert pyd.first(food, {'type': 'fruit'}) == expected

    # verify alias
    pyd.head is pyd.first
    pyd.take is pyd.first


def test_flatten():
    array = [1, ['2222'], [3, [[4]]]]
    assert pyd.flatten(array) == [1, '2222', 3, 4]
    assert pyd.flatten(array, True) == [1, '2222', 3, [[4]]]

    # test pluck style callback
    stooges = [
        {'name': 'curly', 'quotes': ['Oh, a wise guy, eh?', 'Poifect!']},
        {'name': 'moe', 'quotes': ['Spread out!', 'You knucklehead!']}
    ]

    expected = [
        'Oh, a wise guy, eh?', 'Poifect!',
        'Spread out!',
        'You knucklehead!'
    ]

    assert pyd.flatten(stooges, 'quotes') == expected


def test_index_of():
    assert pyd.index_of([1, 2, 3, 1, 2, 3], 2) == 1
    assert pyd.index_of([1, 2, 3, 1, 2, 3], 2, 3) == 4
    assert pyd.index_of([1, 1, 2, 2, 3, 3], 2, True) == 2
    assert pyd.index_of([1, 1, 2, 2, 3, 3], 4) is False
    assert pyd.index_of([1, 1, 2, 2, 3, 3], 2, 10) is False


def test_initial():
    assert pyd.initial([1, 2, 3]) == [1, 2]
    assert pyd.initial([1, 2, 3], 2) == [1]
    assert pyd.initial([1, 2, 3], lambda num, *args: num > 1) == [1]

    # test pluck style callback
    food = [
        {'name': 'beet',   'organic': False},
        {'name': 'carrot', 'organic': True}
    ]

    expected = [{'name': 'beet',   'organic': False}]
    assert pyd.initial(food, 'organic') == expected

    # test where style callback
    food = [
        {'name': 'banana', 'type': 'fruit'},
        {'name': 'beet',   'type': 'vegetable'},
        {'name': 'carrot', 'type': 'vegetable'}
    ]

    expected = [{'name': 'banana', 'type': 'fruit'}]
    assert pyd.initial(food, {'type': 'vegetable'}) == expected


def test_intersection():
    assert pyd.intersection([1, 2, 3], [101, 2, 1, 10], [2, 1]) == [1, 2]


def test_last():
    assert pyd.last([1, 2, 3]) == 3
    assert pyd.last([1, 2, 3], 2) == [2, 3]
    assert pyd.last([1, 2, 3], lambda num, *args: num > 1) == [2, 3]

    # test pluck style callback
    food = [
        {'name': 'beet',   'organic': False},
        {'name': 'carrot', 'organic': True}
    ]

    assert pyd.last(food, 'organic') == [{'name': 'carrot', 'organic': True}]

    # test where style callback
    food = [
        {'name': 'banana', 'type': 'fruit'},
        {'name': 'beet',   'type': 'vegetable'},
        {'name': 'carrot', 'type': 'vegetable'}
    ]

    expected = [
        {'name': 'beet', 'type': 'vegetable'},
        {'name': 'carrot', 'type': 'vegetable'}
    ]

    assert pyd.last(food, {'type': 'vegetable'}) == expected


def test_last_index_of():
    assert pyd.last_index_of([1, 2, 3, 1, 2, 3], 2) == 4
    assert pyd.last_index_of([1, 2, 3, 1, 2, 3], 2, 3) == 1


def test_pull():
    assert pyd.pull([1, 2, 3, 1, 2, 3], 2, 3) == [1, 1]


def test_zip_object():
    expected = {'moe': 30, 'larry': 40}
    assert pyd.zip_object(['moe', 'larry'], [30, 40]) == expected

    expected = {'moe': 30, 'larry': 40}
    assert pyd.zip_object([['moe', 30], ['larry', 40]]) == expected

    # verify alias
    pyd.object_ is pyd.zip_object


def test_zip_():
    expected = [['moe', 30, True], ['larry', 40, False], ['curly', 35, True]]
    actual = pyd.zip_(['moe', 'larry', 'curly'],
                      [30, 40, 35],
                      [True, False, True])

    assert actual == expected


def test_unzip():
    expected = [['moe', 'larry', 'curly'], [30, 40, 35], [True, False, True]]
    actual = pyd.unzip([['moe', 30, True],
                        ['larry', 40, False],
                        ['curly', 35, True]])

    assert actual == expected


def test_range_():
    assert pyd.range_ is range

    assert pyd.range_(10) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert pyd.range_(1, 11) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert pyd.range_(0, 30, 5) == [0, 5, 10, 15, 20, 25]
    assert pyd.range_(0, -10, -1) == [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
    assert pyd.range_(0) == []


def test_without():
    assert pyd.without([1, 2, 1, 0, 3, 1, 4], 0, 1) == [2, 3, 4]


def test_uniq():
    expected = [1, 2, 3]
    assert pyd.uniq([1, 2, 1, 3, 1]) == expected

    expected = [dict(a=1), dict(a=2)]
    assert pyd.uniq([dict(a=1), dict(a=2), dict(a=1)]) == expected

    # using function callback
    import math
    expected = [1, 2, 3]
    actual = pyd.uniq([1, 2, 1.5, 3, 2.5], lambda num, *args: math.floor(num))
    assert actual == expected

    # test where style callback
    food = [
        {'name': 'banana', 'type': 'fruit'},
        {'name': 'apple', 'type': 'fruit'},
        {'name': 'beet',   'type': 'vegetable'},
        {'name': 'beet',   'type': 'vegetable'},
        {'name': 'carrot', 'type': 'vegetable'},
        {'name': 'carrot', 'type': 'vegetable'}
    ]

    assert pyd.uniq(food, {'type': 'vegetable'}) == [
        {'name': 'beet', 'type': 'vegetable'},
        {'name': 'carrot', 'type': 'vegetable'}
    ]

    # test pluck style callback
    pluck = [
        {'x': 1, 'y': 1},
        {'x': 2, 'y': 1},
        {'x': 1, 'y': 1}
    ]

    assert pyd.uniq(pluck, 'x') == [{'x': 1, 'y': 1}, {'x': 2, 'y': 1}]

    # verify alias
    assert pyd.unique is pyd.uniq


def test_union():
    assert pyd.union([1, 2, 3], [101, 2, 1, 10], [2, 1]) == [1, 2, 3, 101, 10]


def test_sorted_index():
    assert pyd.sorted_index([20, 30, 50], 40) == 2
    assert pyd.sorted_index([20, 30, 50], 10) == 0

    # test pluck style callback
    actual = pyd.sorted_index([{'x': 20}, {'x': 30}, {'x': 50}],
                              {'x': 40},
                              'x')
    assert actual == 2

    # test function callback
    lookup = {
        'words': {'twenty': 20, 'thirty': 30, 'fourty': 40, 'fifty': 50}
    }

    callback = lambda word: lookup['words'][word]
    actual = pyd.sorted_index(['twenty', 'thirty', 'fifty'],
                              'fourty',
                              callback)

    assert actual == 2


def test_every():
    assert pyd.every([True, 1, None, 'yes'], bool) is False
    assert pyd.every([True, 1, None, 'yes']) is False

    stooges = [
        {'name': 'moe', 'age': 40},
        {'name': 'larry', 'age': 50}
    ]

    # test pluck style callback
    assert pyd.every(stooges, 'age') is True

    # test where style callback
    assert pyd.every(stooges, {'age': 50}) is False


def test_some():
    assert pyd.some([None, 0, 'yes', False], bool) is True
    assert pyd.some([None, 0, 'yes', False]) is True

    food = [
        {'name': 'apple',  'organic': False, 'type': 'fruit'},
        {'name': 'carrot', 'organic': True,  'type': 'vegetable'}
    ]

    # test pluck style callback
    assert pyd.some(food, 'organic') is True

    # test where style callback
    assert pyd.some(food, {'type': 'meat'}) is False


def test_collect():
    assert pyd.collect([1, 2, 3]) == [1, 2, 3]
    assert pyd.collect([1, 2, 3], lambda num, *args: num * 3) == [3, 6, 9]

    actual = pyd.collect({'one': 1, 'two': 2, 'three': 3},
                         lambda num, *args: num * 3)

    assert sorted(actual) == [3, 6, 9]

    stooges = [
        {'name': 'moe', 'age': 40},
        {'name': 'larry', 'age': 50}
    ]

    assert pyd.collect(stooges, 'name') == ['moe', 'larry']


def test_at():
    assert pyd.at(['a', 'b', 'c', 'd', 'e'], [0, 2, 4]) == ['a', 'c', 'e']
    assert pyd.at(['moe', 'larry', 'curly'], 0, 2) == ['moe', 'curly']
    assert pyd.at({'a': 1, 'b': 2, 'c': 3}, 'a', 'b') == [1, 2]


def test_contains():
    assert pyd.contains([1, 2, 3], 1) is True
    assert pyd.contains([1, 2, 3], 1, 2) is False
    assert pyd.contains({'name': 'fred', 'age': 40}, 'fred') is True
    assert pyd.contains('pebbles', 'eb') is True


##def test_count_by():
##    pass


def test_filter_():
    assert pyd.filter_([0, True, False, None, 1, 2, 3]) == [True, 1, 2, 3]

    is_even = lambda num, *args: num % 2 == 0
    assert pyd.filter_([1, 2, 3, 4, 5, 6], is_even) == [2, 4, 6]

    characters = [
        {'name': 'barney', 'age': 36, 'blocked': False},
        {'name': 'fred',   'age': 40, 'blocked': True}
    ]

    expected = [{'name': 'fred', 'age': 40, 'blocked': True}]
    assert pyd.filter_(characters, 'blocked') == expected

    expected = [{'name': 'barney', 'age': 36, 'blocked': False}]
    assert pyd.filter_(characters, {'age': 36}) == expected


def test_find():
    characters = [
        {'name': 'barney',  'age': 36, 'blocked': False},
        {'name': 'fred',    'age': 40, 'blocked': True},
        {'name': 'pebbles', 'age': 1,  'blocked': False}
    ]

    callback = lambda c, *args: c['age'] < 40

    expected = {'name': 'barney', 'age': 36, 'blocked': False}
    assert pyd.find(characters, callback) == expected

    expected = {'name': 'pebbles', 'age': 1, 'blocked': False}
    assert pyd.find(characters, {'age': 1}) == expected

    expected = {'name': 'fred', 'age': 40, 'blocked': True}
    assert pyd.find(characters, 'blocked') == expected

    expected = {'name': 'barney',  'age': 36, 'blocked': False}
    assert pyd.find(characters) == expected
