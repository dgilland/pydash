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
    append,
    cat,
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
    first,
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
    object_,
    pop,
    pull,
    pull_at,
    push,
    remove,
    rest,
    reverse,
    shift,
    slice_,
    sort,
    sorted_index,
    sorted_last_index,
    sorted_uniq,
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
    unique,
    unshift,
    unzip,
    unzip_with,
    without,
    xor,
    zip_,
    zip_with,
    zip_object,
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
    all_,
    any_,
    at,
    collect,
    contains,
    count_by,
    deep_pluck,
    detect,
    each,
    each_right,
    every,
    filter_,
    find,
    find_last,
    find_where,
    flat_map,
    flat_map_deep,
    flat_map_depth,
    foldl,
    foldr,
    for_each,
    for_each_right,
    group_by,
    include,
    index_by,
    inject,
    invoke,
    invoke_map,
    map_,
    mapiter,
    partition,
    pluck,
    reduce_,
    reduce_right,
    reductions,
    reductions_right,
    reject,
    sample,
    sample_size,
    select,
    shuffle,
    size,
    some,
    sort_by,
    sort_by_all,
    sort_by_order,
    to_list,
    where,
)


#
# Functions
#

from .functions import (
    after,
    ary,
    before,
    compose,
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
    mod_args,
    negate,
    once,
    partial,
    partial_right,
    pipe,
    pipe_right,
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
    curve,
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
    pow_,
    power,
    round_,
    scale,
    sigma,
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
    callables,
    clone,
    clone_deep,
    deep_get,
    deep_has,
    deep_map_values,
    deep_set,
    defaults,
    defaults_deep,
    extend,
    find_key,
    find_last_key,
    for_in,
    for_in_right,
    for_own,
    for_own_right,
    get,
    get_path,
    has,
    has_path,
    invert,
    keys,
    keys_in,
    map_keys,
    map_values,
    merge,
    methods,
    omit,
    pairs,
    parse_int,
    pick,
    rename_keys,
    set_,
    set_path,
    to_boolean,
    to_dict,
    to_number,
    to_plain_object,
    to_string,
    transform,
    update_path,
    values,
    values_in,
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
    is_bool,
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
    is_int,
    is_iterable,
    is_json,
    is_list,
    is_match,
    is_monotone,
    is_nan,
    is_native,
    is_negative,
    is_none,
    is_number,
    is_num,
    is_object,
    is_odd,
    is_plain_object,
    is_positive,
    is_re,
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
    escape_re,
    explode,
    has_substr,
    human_case,
    implode,
    insert_substr,
    join,
    js_match,
    js_replace,
    kebab_case,
    lines,
    lower_case,
    lower_first,
    number_format,
    pad,
    pad_left,
    pad_right,
    pascal_case,
    predecessor,
    prune,
    quote,
    re_replace,
    repeat,
    replace,
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
    trim_left,
    trim_right,
    trunc,
    truncate,
    underscore_case,
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
    callback,
    cond,
    conforms,
    conforms_to,
    constant,
    deep_property,
    deep_prop,
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
    prop,
    prop_of,
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
