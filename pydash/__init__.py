
def compact(array):
    '''
    .. py:method:: compact(array)

    Creates a list with all falsey values of array removed.

    :param array: list to compact
    :rtype: list
    '''
    return filter(None, array)

def difference(array, *lists):
    '''
    .. py:method:: difference(array[, *lists])

    Creates a list of list elements not present in the other lists

    :param array: the list to process
    :param lists: lists to check
    :rtype: list
    '''
    return list( difference(set(array).difference(lists[0]), *lists[1:]) ) if lists else array

def rest(array, callback=None):
    '''
    .. py:method:: rest(array[, callback|n|pluck|where])

    Return all but the first value of array.
    If a number n is passed, the first n values are excluded from the result.
    If a callback function is passed, elements at the beginning of the array are excluded from the result as long as the callback returns truthy.
    The callback is invoked with three arguments; (value, index, array).
    If a property name is passed for callback, the created "_.pluck" style callback will return the property value of the given element.
    If an object is passed for callback, the created "_.where" style callback will return true for elements that have the properties of the given object, else false.

    :param array: the list to process
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

    :param array: list to process
    :param callback: filter function or where dict
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
    .. py:method:; first(array[, callback|n|pluck|where)

    Gets the first element of the array.
    If a number n is passed, the first n elements of the array are returned.
    If a callback function is passed, elements at the beginning of the array are returned as long as the callback returns truthy.
    The callback is invoked with three arguments; (value, index, array).
    If a property name is passed for callback, the created "_.pluck" style callback will return the property value of the given element.
    If an object is passed for callback, the created "_.where" style callback will return true for elements that have the properties of the given object, else false.
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

def _iter_callback(array, callback=None):
    if hasattr(callback, '__call__'):
        cb = callback
    elif isinstance(callback, (str,unicode)):
        key = callback
        cb = lambda item, *args: pluck([item], key)[0]
    elif isinstance(callback, dict):
        cb = lambda item, *args: where([item], callback)
    else:
        index = callback if isinstance(callback, int) else 1
        cb = lambda item, i, *args: i < index

    return ( (cb(item, i, array), item, i, array) for i, item in enumerate(array) )
