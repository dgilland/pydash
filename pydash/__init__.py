# -*- coding: utf-8 -*-
"""Python port of Lo-Dash
"""

from .__pkg__ import (
    __description__,
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
    chunk,
    compact,
    concat,
    difference,
    difference_by,
    difference_with,
    drop,
    drop_right,
    drop_right_while,
    drop_while,
    duplicates,
    fill,
    find_index,
    find_last_index,
    flatten,
    flatten_deep,
    flatten_depth,
    from_pairs,
    head,
    index_of,
    initial,
    intercalate,
    interleave,
    intersection,
    intersection_by,
    intersection_with,
    intersperse,
    last,
    last_index_of,
    mapcat,
    nth,
    pop,
    pull,
    pull_all,
    pull_all_by,
    pull_all_with,
    pull_at,
    push,
    remove,
    reverse,
    shift,
    slice_,
    sort,
    sorted_index,
    sorted_index_by,
    sorted_index_of,
    sorted_last_index,
    sorted_last_index_by,
    sorted_last_index_of,
    sorted_uniq,
    sorted_uniq_by,
    splice,
    split_at,
    tail,
    take,
    take_right,
    take_right_while,
    take_while,
    union,
    union_by,
    union_with,
    uniq,
    uniq_by,
    uniq_with,
    unshift,
    unzip,
    unzip_with,
    without,
    xor,
    xor_by,
    xor_with,
    zip_,
    zip_with,
    zip_object,
    zip_object_deep
)


#
# Chaining
#

from .chaining import (
    chain,
    tap,
    thru,
    _Dash
)


#
# Collections
#

from .collections import (
    at,
    count_by,
    every,
    filter_,
    find,
    find_last,
    flat_map,
    flat_map_deep,
    flat_map_depth,
    for_each,
    for_each_right,
    group_by,
    includes,
    invoke_map,
    key_by,
    map_,
    order_by,
    partition,
    pluck,
    reduce_,
    reduce_right,
    reductions,
    reductions_right,
    reject,
    sample,
    sample_size,
    shuffle,
    size,
    some,
    sort_by,
    to_list
)


#
# Functions
#

from .functions import (
    after,
    ary,
    before,
    conjoin,
    curry,
    curry_right,
    debounce,
    delay,
    disjoin,
    flip,
    flow,
    flow_right,
    iterated,
    juxtapose,
    negate,
    once,
    over_args,
    partial,
    partial_right,
    rearg,
    spread,
    throttle,
    unary,
    wrap,
)


#
# Numerical
#

from .numerical import (
    add,
    ceil,
    clamp,
    divide,
    floor,
    max_,
    max_by,
    mean,
    mean_by,
    median,
    min_,
    min_by,
    moving_mean,
    multiply,
    power,
    round_,
    scale,
    slope,
    std_deviation,
    subtract,
    sum_,
    sum_by,
    transpose,
    variance,
    zscore,
)


#
# Objects
#

from .objects import (
    assign,
    assign_with,
    callables,
    clone,
    clone_deep,
    clone_deep_with,
    clone_with,
    defaults,
    defaults_deep,
    find_key,
    find_last_key,
    for_in,
    for_in_right,
    get,
    has,
    invert,
    invert_by,
    invoke,
    keys,
    map_keys,
    map_values,
    map_values_deep,
    merge,
    merge_with,
    omit,
    omit_by,
    parse_int,
    pick,
    pick_by,
    rename_keys,
    set_,
    set_with,
    to_boolean,
    to_dict,
    to_integer,
    to_number,
    to_pairs,
    to_string,
    transform,
    unset,
    update,
    update_with,
    values
)


#
# Predicates
#

from .predicates import (
    eq,
    gt,
    gte,
    lt,
    lte,
    in_range,
    is_associative,
    is_blank,
    is_boolean,
    is_builtin,
    is_date,
    is_decreasing,
    is_dict,
    is_empty,
    is_equal,
    is_equal_with,
    is_error,
    is_even,
    is_float,
    is_function,
    is_increasing,
    is_indexed,
    is_instance_of,
    is_integer,
    is_iterable,
    is_json,
    is_list,
    is_match,
    is_match_with,
    is_monotone,
    is_nan,
    is_negative,
    is_none,
    is_number,
    is_object,
    is_odd,
    is_positive,
    is_reg_exp,
    is_set,
    is_strictly_decreasing,
    is_strictly_increasing,
    is_string,
    is_tuple,
    is_zero,
)


#
# Strings
#

from .strings import (
    camel_case,
    capitalize,
    chars,
    chop,
    chop_right,
    clean,
    count_substr,
    deburr,
    decapitalize,
    ends_with,
    ensure_starts_with,
    ensure_ends_with,
    escape,
    escape_reg_exp,
    has_substr,
    human_case,
    insert_substr,
    join,
    kebab_case,
    lines,
    lower_case,
    lower_first,
    number_format,
    pad,
    pad_end,
    pad_start,
    pascal_case,
    predecessor,
    prune,
    quote,
    reg_exp_js_match,
    reg_exp_js_replace,
    reg_exp_replace,
    repeat,
    replace,
    replace_end,
    replace_start,
    separator_case,
    series_phrase,
    series_phrase_serial,
    slugify,
    snake_case,
    split,
    start_case,
    starts_with,
    strip_tags,
    substr_left,
    substr_left_end,
    substr_right,
    substr_right_end,
    successor,
    surround,
    swap_case,
    title_case,
    to_lower,
    to_upper,
    trim,
    trim_end,
    trim_start,
    truncate,
    unescape,
    unquote,
    upper_case,
    upper_first,
    url,
    words,
)

#
# Utilities
#

from .utilities import (
    attempt,
    cond,
    conforms,
    conforms_to,
    constant,
    default_to,
    iteratee,
    identity,
    matches,
    matches_property,
    memoize,
    method,
    method_of,
    noop,
    now,
    nth_arg,
    over,
    over_every,
    over_some,
    properties,
    property_,
    property_of,
    random,
    range_,
    range_right,
    result,
    stub_list,
    stub_dict,
    stub_false,
    stub_string,
    stub_true,
    times,
    to_path,
    unique_id,
)


#
# Exceptions
#

from .exceptions import (
    InvalidMethod
)


#
# "_" Instance
#

py_ = _Dash()
_ = py_
