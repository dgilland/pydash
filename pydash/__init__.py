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

from .arrays import (
    compact,
    difference,
    find_index,
    find_last_index,
    first,
    head,
    take,
    flatten,
    index_of,
    initial,
    intersection,
    last,
    last_index_of,
    pull,
    range_,
    remove,
    rest,
    tail,
    drop,
    sorted_index,
    union,
    uniq,
    unique,
    without,
    xor,
    zip_,
    unzip,
    zip_object,
    object_,
)


#
# Chaining
#

from .chaining import (
    InvalidMethod,
    chain,
    tap
)


#
# Collections
#

from .collections import (
    at,
    contains,
    count_by,
    every,
    all_,
    filter_,
    select,
    find,
    detect,
    find_where,
    find_last,
    for_each,
    each,
    for_each_right,
    each_right,
    group_by,
    index_by,
    invoke,
    map_,
    collect,
    max_,
    min_,
    pluck,
    reduce_,
    foldl,
    inject,
    reduce_right,
    foldr,
    reject,
    sample,
    shuffle,
    size,
    some,
    any_,
    sort_by,
    to_list,
    where
)


#
# Functions
#

from .functions import (
    after,
    compose,
    curry,
    once,
    partial,
    partial_right,
    wrap
)


#
# Objects
#

from .objects import (
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
    functions_,
    has,
    invert,
    is_list,
    is_boolean,
    is_empty,
    is_function,
    is_none,
    is_number,
    is_string,
    keys,
    map_values,
    merge,
    methods,
    omit,
    pairs,
    pick,
    transform,
    update,
    values
)


#
# Utilities
#

from .utilities import (
    now,
    constant,
    callback,
    create_callback,
    identity,
    matches,
    memoize,
    noop,
    property_,
    prop,
    random,
    result,
    times,
    unique_id
)
