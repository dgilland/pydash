import collections

def compact(array):
    '''
    .. py:method:: compact(array)

    Creates a list with all falsey values of array removed.

    :param list array: list to compact
    :rtype: list
    '''
    return filter(None, array)

def difference(array, *lists):
    '''
    .. py:method:: difference(array[, *lists])

    Creates a list of list elements not present in the other lists

    :param list array: the list to process
    :param list lists: lists to check
    :rtype: list
    '''
    return list( difference(set(array).difference(lists[0]), *lists[1:]) ) if lists else array

def rest(array, callback=None):
    '''
    .. py:method:: rest(array[, callback|n|pluck|where=None])

    Return all but the first value of array.
    If a number n is passed, the first n values are excluded from the result.
    If a callback function is passed, elements at the beginning of the array are excluded from the result as long as the callback returns truthy.
    The callback is invoked with three arguments; (value, index, array).
    If a property name is passed for callback, the created "_.pluck" style callback will return the property value of the given element.
    If an object is passed for callback, the created "_.where" style callback will return true for elements that have the properties of the given object, else false.

    :param list array: the list to process
    :param mixed callback: callback to filter by
    :rtype: list
    '''

    n = 0
    for is_true, _, _, _ in _iter_callback(array, callback):
        if is_true:
            n += 1
        else:
            break

    return array[n:]

def find_index(array, callback):
    '''
    .. py:method:: find_index(array, callback|where)

    This method is similar to _.find, except that it returns the index of the element that passes the callback check, instead of the element itself.

    :param list array: list to process
    :param function callback: filter function or where dict
    :rtype: list
    '''
    n = -1
    for is_true, _, i, _ in _iter_callback(array, callback):
        if is_true:
            n = i
            break

    return n

def first(array, callback=None):
    '''
    .. py:method:: first(array[, callback|n|pluck|where=None])

    Gets the first element of the array.
    If a number n is passed, the first n elements of the array are returned.
    If a callback function is passed, elements at the beginning of the array are returned as long as the callback returns truthy.
    The callback is invoked with three arguments; (value, index, array).
    If a property name is passed for callback, the created "_.pluck" style callback will return the property value of the given element.
    If an object is passed for callback, the created "_.where" style callback will return true for elements that have the properties of the given object, else false.

    :param list array: list to select from
    :param mixed callback: callback to filter array
    :rtype: mixed
    '''
    n = 0
    for is_true, _, _, _ in _iter_callback(array, callback):
        if is_true:
            n += 1
        else:
            break

    ret = array[:n]

    if callback in (None, 1):
        ret = ret[0]

    return ret

head = first

def flatten(array, callback=None, _depth=0):
    '''
    .. py:method:: flatten(array[, callback|pluck|where=None])

    Flattens a nested array (the nesting can be to any depth).
    If callback is True, array will only be flattened a single level.
    If callback is passed, each element of array is passed through a callback before flattening.

    :param list array: list to flatten
    :param mixed callback: callback to filter array
    :rtype: list
    '''

    shallow = False
    if callback is True:
        shallow = True
    elif callback:
        array = map(_make_callback(callback), array)
        callback = None

    lst = []
    if all([ isinstance(array, collections.Iterable), not isinstance(array, basestring), not (shallow and _depth > 1) ]):
        for a in array:
            lst.extend(flatten(a, callback, _depth+1))
    else:
        lst.append(array)

    return lst

def index_of(array, value, from_index=0):
    '''
    .. py:method:: index_of(array, value[, from_index=0])

    Gets the index at which the first occurrence of value is found

    :param list array: list to search
    :param mixed value: value to search for
    :param integer from_index: the index to search from
    :rtype: integer
    '''
    try:
        return array.index(value, from_index)
    except ValueError:
        return False

def initial(array, callback=1):
    '''
    .. py:method:: initial(array[, callback|n|pluck|where=None)

    Gets all but the last element of array.
    If a number n is passed, the last n elements are excluded from the result.
    If a callback function is passed, elements at the end of the array are excluded from the result as long as the callback returns truthy.

    :param list array: list to query
    :param mixed callback: The function called per element or the number of elements to exclude
    '''

    lst = array[::-1]
    n = len(array)
    for is_true, _, _, _ in _iter_callback(lst, callback):
        if is_true:
            n -= 1
        else:
            break

    ret = array[:n]

    return ret

def where(collection, properties):
    '''
    .. py:method:: where(collection, properties)

    Examines each element in a collection, returning an array of all elements that have the given properties.

    :param collection: a list of dicts
    :param properties: the dict of property values to filter by
    :rtype: list
    '''
    filter_fn = lambda item: _where(item, properties)
    return filter(filter_fn, collection)

def _where(superset, subset):
    '''Helper function for where()'''
    return all(item in superset.items() for item in subset.items())

def pluck(collection, key):
    '''
    .. py:method:: pluck(collection, key)

    Retrieves the value of a specified property from all elements in the collection.

    :param collection: a list of dicts
    :param key: the key value to pluck
    :rtype: list
    '''
    return map(lambda x: x.get(key), collection)

def _make_callback(callback):
    '''Create a callback function from a mixed type `callback`'''
    if hasattr(callback, '__call__'):
        cb = callback
    elif isinstance(callback, basestring):
        key = callback
        cb = lambda item, *args: pluck([item], key)[0]
    elif isinstance(callback, dict):
        cb = lambda item, *args: where([item], callback)
    else:
        index = callback if isinstance(callback, int) else 1
        cb = lambda item, i, *args: i < index

    return cb

def _iter_callback(array, callback=None):
    cb = _make_callback(callback)
    return ( (cb(item, i, array), item, i, array) for i, item in enumerate(array) )

