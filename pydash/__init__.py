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
    chunk,
    compact,
    difference,
    drop,
    drop_right,
    drop_right_while,
    drop_while,
    find_index,
    find_last_index,
    first,
    flatten,
    flatten_deep,
    head,
    index_of,
    initial,
    intercalate,
    interleave,
    intersection,
    intersperse,
    last,
    last_index_of,
    object_,
    pull,
    pull_at,
    remove,
    rest,
    slice_,
    sorted_index,
    sorted_last_index,
    tail,
    take,
    take_right,
    take_right_while,
    take_while,
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
    partition,
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
    before,
    compose,
    conjoin,
    curry,
    curry_right,
    debounce,
    delay,
    disjoin,
    iterated,
    juxtapose,
    negate,
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
    get_path,
    has,
    has_path,
    invert,
    keys,
    keys_in,
    map_values,
    merge,
    methods,
    omit,
    pairs,
    parse_int,
    pick,
    rename_keys,
    set_path,
    to_string,
    transform,
    update_path,
    values,
    values_in,
)


#
# Predicates
#

from .api.predicates import (
    is_associative,
    is_boolean,
    is_date,
    is_decreasing,
    is_empty,
    is_equal,
    is_error,
    is_even,
    is_float,
    is_function,
    is_increasing,
    is_indexed,
    is_instance_of,
    is_integer,
    is_json,
    is_list,
    is_monotone,
    is_nan,
    is_negative,
    is_none,
    is_number,
    is_object,
    is_odd,
    is_plain_object,
    is_positive,
    is_re,
    is_reg_exp,
    is_strictly_decreasing,
    is_strictly_increasing,
    is_string,
    is_zero,
)


#
# Strings
#

from .api.strings import (
    camel_case,
    capitalize,
    ends_with,
    escape,
    escape_reg_exp,
    escape_re,
    explode,
    implode,
    kebab_case,
    pad,
    pad_left,
    pad_right,
    repeat,
    snake_case,
    starts_with,
    trim,
    trim_left,
    trim_right,
    trunc,
    unescape,
)

#
# Utilities
#

from .api.utilities import (
    attempt,
    callback,
    constant,
    iteratee,
    identity,
    matches,
    memoize,
    noop,
    now,
    prop,
    property_,
    random,
    range_,
    result,
    times,
    unique_id,
)


#
# Exceptions
#
from .api.exceptions import (
    InvalidMethod
)
