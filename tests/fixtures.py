
from copy import deepcopy

import pytest

# pytest.mark is a generator so create alias for convenience
parametrize = pytest.mark.parametrize


def reduce_callback0(total, num):
    return total + num


def reduce_callback1(result, num, key):
    result[key] = num * 3
    return result


def reduce_right_callback0(a, b):
    return a + b


def noop(*args, **kargs):
    pass


def transform_callback0(result, num):
    num *= num
    if num % 2:
        result.append(num)
        return len(result) < 3


def is_equal_callback0(a, b):
    a_greet = a.startswith('h') if hasattr(a, 'startswith') else False
    b_greet = b.startswith('h') if hasattr(b, 'startswith') else False

    return a_greet == b_greet if a_greet or b_greet else None


def for_in_callback0(value, key, obj):
    obj[key] += value


def for_in_callback1(value, key, obj):
    obj[key] += value
    return False


def for_in_callback2(value, index, obj):
    if index == 2:
        obj[index] = 'index:2'
        return True
    elif index == 0:
        obj[index] = False
        return True
    else:
        obj[index] = True
        return False
