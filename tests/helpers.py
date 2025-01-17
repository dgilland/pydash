class Object:
    def __init__(self, **attrs):
        for key, value in attrs.items():
            setattr(self, key, value)


class ItemsObject:
    def __init__(self, items):
        self._items = items

    def items(self):
        if isinstance(self._items, dict):
            return list(self._items.items())
        else:
            return enumerate(self._items)


class IteritemsObject:
    def __init__(self, items):
        self._items = items

    def iteritems(self):
        if isinstance(self._items, dict):
            for key, value in self._items.items():
                yield key, value
        else:
            for i, item in enumerate(self._items):
                yield i, item


class Filter:
    def __init__(self, predicate):
        self.predicate = predicate

    def __call__(self, item):
        return self.predicate(item)


def reduce_iteratee0(total, num):
    return total + num


def reduce_iteratee1(result, num, key):
    result[key] = num * 3
    return result


def reduce_right_iteratee0(a, b):
    return a + b


def noop(*args, **kwargs):
    pass


def transform_iteratee0(result, num):
    num *= num
    if num % 2:
        result.append(num)
        return len(result) < 3


def is_equal_iteratee0(a, b):
    a_greet = a.startswith("h") if hasattr(a, "startswith") else False
    b_greet = b.startswith("h") if hasattr(b, "startswith") else False

    return a_greet == b_greet if a_greet or b_greet else None


def for_in_iteratee0(value, key, obj):
    obj[key] += value


def for_in_iteratee1(value, key, obj):
    obj[key] += value
    return False


def for_in_iteratee2(value, index, obj):
    if index == 2:
        obj[index] = "index:2"
        return True
    elif index == 0:
        obj[index] = False
        return True
    else:
        obj[index] = True
        return False
