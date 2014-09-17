"""Numerical/mathemetical related functions.

.. versionadded:: 2.1.0
"""

from __future__ import absolute_import, division

import math

import pydash as pyd
from .helpers import itercallback, iterator
from ._compat import _range


__all__ = [
    'add',
    'average',
    'avg',
    'curve',
    'mean',
    'median',
    'moving_average',
    'moving_avg',
    'pow_',
    'power',
    'round_',
    'scale',
    'sigma',
    'slope',
    'std_deviation',
    'sum_',
    'transpose',
    'variance',
    'zscore',
]


INFINITY = float('inf')


def add(collection, callback=None):
    return sum(result[0] for result in itercallback(collection, callback))


sum_ = add


def average(collection, callback=None):
    return add(collection, callback) / pyd.size(collection)


avg = average
mean = average


def median(collection, callback=None):
    length = len(collection)
    middle = (length + 1) / 2
    collection = [ret[0] for ret in itercallback(sorted(collection), callback)]

    if pyd.is_odd(length):
        result = collection[int(middle - 1)]
    else:
        left = int(middle - 1.5)
        right = int(middle - 0.5)
        result = (collection[left] + collection[right]) / 2

    return result


def moving_average(array, size):
    result = []

    for i in _range(size - 1, len(array) + 1):
        window = array[i - size:i]

        if len(window) == size:
            result.append(average(window))

    return result


moving_avg = moving_average


def power(x, n):
    if pyd.is_number(x):
        result = pow(x, n)
    elif pyd.is_list(x):
        result = pyd.map_(x, lambda item: pow(item, n))
    else:
        result = None

    return result


pow_ = power


def round_(x, precision=0):
    rounder = pyd.partial_right(round, precision)

    if pyd.is_number(x):
        result = rounder(x)
    elif pyd.is_list(x):
        result = pyd.map_(x, lambda item: rounder(item))
    else:
        result = None

    return result


curve = round_


def scale(array, maximum=1):
    array_max = max(array)
    return pyd.map_(array, lambda item: item * (maximum / array_max))


def slope(x, y):
    if y[0] == x[0]:
        result = INFINITY
    else:
        result = (y[1] - x[1]) / (y[0] - x[0])

    return result


def std_deviation(array):
    return math.sqrt(variance(array))


sigma = std_deviation


def transpose(array):
    trans = []

    for y, row in iterator(array):
        for x, col in iterator(row):
            trans = pyd.set_path(trans, col, [x, y])

    return trans


def variance(array):
    ave = average(array)
    var = lambda x: power(x - ave, 2)
    return pyd._(array).map_(var).average().value()


def zscore(collection, callback=None):
    array = pyd.map_(collection, callback)
    ave = average(array)
    sig = sigma(array)

    return pyd.map_(array, lambda item: (item - ave) / sig)
