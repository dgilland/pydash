"""Python port of Lo-Dash
"""

from __future__ import absolute_import

from .__meta__ import (
    __title__,
    __summary__,
    __url__,
    __version__,
    __author__,
    __email__,
    __license__
)


#
# Arrays
#

from .api.arrays import (
    compact,
    difference,
    drop,
    find_index,
    find_last_index,
    first,
    flatten,
    head,
    index_of,
    initial,
    intersection,
    last,
    last_index_of,
    object_,
    pull,
    range_,
    remove,
    rest,
    sorted_index,
    tail,
    take,
    union,
    uniq,
    unique,
    unzip,
    without,
    xor,
    zip_,
    zip_object,
)


#
# Chaining
#

from .api.chaining import (
    chain,
    tap,
)


#
# Collections
#

from .api.collections import (
    all_,
    any_,
    at,
    collect,
    contains,
    count_by,
    detect,
    each,
    each_right,
    every,
    filter_,
    find,
    find_last,
    find_where,
    foldl,
    foldr,
    for_each,
    for_each_right,
    group_by,
    include,
    index_by,
    inject,
    invoke,
    map_,
    max_,
    min_,
    pluck,
    reduce_,
    reduce_right,
    reject,
    sample,
    select,
    shuffle,
    size,
    some,
    sort_by,
    to_list,
    where,
)


#
# Functions
#

from .api.functions import (
    after,
    compose,
    curry,
    debounce,
    delay,
    once,
    partial,
    partial_right,
    throttle,
    wrap,
)


#
# Objects
#

from .api.objects import (
    assign,
    clone,
    clone_deep,
    defaults,
    extend,
    find_key,
    find_last_key,
    for_in,
    for_in_right,
    for_own,
    for_own_right,
    functions,
    has,
    invert,
    is_boolean,
    is_date,
    is_empty,
    is_equal,
    is_function,
    is_list,
    is_nan,
    is_none,
    is_number,
    is_object,
    is_plain_object,
    is_string,
    keys,
    map_values,
    merge,
    methods,
    omit,
    pairs,
    parse_int,
    pick,
    transform,
    values,
)


#
# Utilities
#

from .api.utilities import (
    callback,
    constant,
    create_callback,
    escape,
    identity,
    matches,
    memoize,
    noop,
    now,
    prop,
    property_,
    random,
    result,
    times,
    unescape,
    unique_id,
)


#
# Exceptions
#
from .api.exceptions import (
    InvalidMethod
)
