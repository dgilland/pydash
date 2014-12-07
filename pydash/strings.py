"""String functions.

.. versionadded:: 1.1.0
"""

from functools import partial
import re

import pydash as pyd
from ._compat import (
    html_unescape,
    iteritems,
    parse_qsl,
    PY26,
    urlencode,
    urlsplit,
    urlunsplit
)


__all__ = [
    'camel_case',
    'capitalize',
    'deburr',
    'ends_with',
    'escape',
    'escape_reg_exp',
    'escape_re',
    'explode',
    'implode',
    'js_match',
    'js_replace',
    'kebab_case',
    'pad',
    'pad_left',
    'pad_right',
    'repeat',
    'snake_case',
    'starts_with',
    'trim',
    'trim_left',
    'trim_right',
    'trunc',
    'unescape',
    'url',
    'words',
]


HTML_ESCAPES = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '`': '&#96;'
}

DEBURRED_LETTERS = {
    '\xC0': 'A',
    '\xC1': 'A',
    '\xC2': 'A',
    '\xC3': 'A',
    '\xC4': 'A',
    '\xC5': 'A',
    '\xE0': 'a',
    '\xE1': 'a',
    '\xE2': 'a',
    '\xE3': 'a',
    '\xE4': 'a',
    '\xE5': 'a',
    '\xC7': 'C',
    '\xE7': 'c',
    '\xD0': 'D',
    '\xF0': 'd',
    '\xC8': 'E',
    '\xC9': 'E',
    '\xCA': 'E',
    '\xCB': 'E',
    '\xE8': 'e',
    '\xE9': 'e',
    '\xEA': 'e',
    '\xEB': 'e',
    '\xCC': 'I',
    '\xCD': 'I',
    '\xCE': 'I',
    '\xCF': 'I',
    '\xEC': 'i',
    '\xED': 'i',
    '\xEE': 'i',
    '\xEF': 'i',
    '\xD1': 'N',
    '\xF1': 'n',
    '\xD2': 'O',
    '\xD3': 'O',
    '\xD4': 'O',
    '\xD5': 'O',
    '\xD6': 'O',
    '\xD8': 'O',
    '\xF2': 'o',
    '\xF3': 'o',
    '\xF4': 'o',
    '\xF5': 'o',
    '\xF6': 'o',
    '\xF8': 'o',
    '\xD9': 'U',
    '\xDA': 'U',
    '\xDB': 'U',
    '\xDC': 'U',
    '\xF9': 'u',
    '\xFA': 'u',
    '\xFB': 'u',
    '\xFC': 'u',
    '\xDD': 'Y',
    '\xFD': 'y',
    '\xFF': 'y',
    '\xC6': 'Ae',
    '\xE6': 'ae',
    '\xDE': 'Th',
    '\xFE': 'th',
    '\xDF': 'ss',
    '\xD7': ' ',
    '\xF7': ' '
}

# Use Javascript style regex to make Lo-Dash compatibility easier.
RE_WORDS = '/[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*)|[A-Z]?[a-z]+[0-9]*|[A-Z]+|[0-9]+/g'
RE_LATIN1 = '/[\xC0-\xFF]/g'


def camel_case(text):
    """Converts `text` to camel case.

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to camel case.

    .. versionadded:: 1.1.0
    """
    text = ''.join(word.title() for word in words(pyd.to_string(text)))
    return text[0].lower() + text[1:]


def capitalize(text):
    """Capitalizes the first character of `text`.

    Args:
        text (str): String to capitalize.

    Returns:
        str: Capitalized string.

    .. versionadded:: 1.1.0
    """
    return text.capitalize()


def deburr(text):
    """Deburrs `text` by converting latin-1 supplementary letters to basic
    latin letters.

    Args:
        text (str): String to deburr.

    Returns:
        str: Deburred string.

    .. versionadded:: 2.0.0
    """
    return js_replace(RE_LATIN1,
                      text,
                      lambda match: DEBURRED_LETTERS.get(match.group(),
                                                         match.group()))


def ends_with(text, target, position=None):
    """Checks if `text` ends with a given target string.

    Args:
        text (str): String to check.
        target (str): String to check for.
        position (int, optional): Position to search from. Defaults to
            end of `text`.

    Returns:
        bool: Whether `text` ends with `target`.

    .. versionadded:: 1.1.0
    """
    text = pyd.to_string(text)

    if position is None:
        position = len(text)

    return text[:position].endswith(target)


def escape(text):
    r"""Converts the characters ``&``, ``<``, ``>``, ``"``, ``'``, and ``\``` in
    `text` to their corresponding HTML entities.

    Args:
        text (str): String to escape.

    Returns:
        str: HTML escaped string.

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
        Moved function to Strings module.
    """
    # NOTE: Not using _compat.html_escape because Lo-Dash escapes certain chars
    # differently (e.g. "'" isn't escaped by html_escape() but is by Lo-Dash).
    return ''.join(HTML_ESCAPES.get(char, char)
                   for char in pyd.to_string(text))


def escape_reg_exp(text):
    """Escapes the RegExp special characters in `text`.

    Args:
        text (str): String to escape.

    Returns:
        str: RegExp escaped string.

    .. versionadded:: 1.1.0
    """
    return re.escape(text)


escape_re = escape_reg_exp


def explode(text, delimiter=None):
    """Splits `text` on `delimiter`. If `delimiter` not provided or ``None``,
    then `text` is split on every character.

    Args:
        text (str): String to explode.
        delimiter (str, optional): Delimiter string to split on. Defaults to
            ``None``.

    Returns:
        list: Exploded string.

    .. versionadded:: 2.0.0
    """
    if delimiter:
        ret = text.split(delimiter)
    else:
        # Splits text into list of characters.
        ret = list(text)

    return ret


def implode(array, delimiter=''):
    """Joins an iterable into a string using `delimiter` between each element.

    Args:
        array (iterable): Iterable to implode.
        delimiter (str): Delimiter to using when joining. Defaults to ``''``.

    Returns:
        str: Imploded iterable.

    .. versionadded:: 2.0.0
    """
    return delimiter.join(array)


def js_match(reg_exp, text):
    """Return list of matches using Javascript style regular expression.

    Args:
        reg_exp (str): Javascript style regular expression.
        text (str): String to evaluate.

    Returns:
        list: List of matches.

    .. versionadded:: 2.0.0
    """
    return js_to_py_re_find(reg_exp)(text)


def js_replace(reg_exp, text, repl):
    """Replace `text` with `repl` using Javascript style regular expression to
    find matches.

    Args:
        reg_exp (str): Javascript style regular expression.
        text (str): String to evaluate.
        repl (str): Replacement string.

    Returns:
        str: Modified string.

    .. versionadded:: 2.0.0
    """
    return js_to_py_re_replace(reg_exp)(text, repl)


def kebab_case(text):
    """Converts `text` to kebab case (a.k.a. spinal case).

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to kebab case.

    .. versionadded:: 1.1.0
    """
    return '-'.join(wrd for wrd in words(pyd.to_string(text)) if wrd.lower())


def pad(text, length, chars=' '):
    """Pads `text` on the left and right sides if it is shorter than the
    given padding length. The `chars` string may be truncated if the number of
    padding characters can't be evenly divided by the padding length.

    Args:
        text (str): String to pad.
        length (int): Amount to pad.
        chars (str, optional): Chars to pad with. Defaults to ``" "``.

    Returns:
        str: Padded string.

    .. versionadded:: 1.1.0
    """
    text = pyd.to_string(text)
    text_len = len(text)
    length = max((length, text_len))

    padding = (length - text_len)
    left_pad = padding // 2
    right_pad = padding - left_pad

    text = repeat(chars, left_pad) + text + repeat(chars, right_pad)

    if len(text) > length:
        # This handles cases when `chars` is more than one character.
        text = text[left_pad:-right_pad]

    return text


def pad_left(text, length, chars=' '):
    """Pads `text` on the left side if it is shorter than the given padding
    length. The `chars` string may be truncated if the number of padding
    characters can't be evenly divided by the padding length.

    Args:
        text (str): String to pad.
        length (int): Amount to pad.
        chars (str, optional): Chars to pad with. Defaults to ``" "``.

    Returns:
        str: Padded string.

    .. versionadded:: 1.1.0
    """
    text = pyd.to_string(text)
    length = max((length, len(text)))
    return (repeat(chars, length) + text)[-length:]


def pad_right(text, length, chars=' '):
    """Pads `text` on the right side if it is shorter than the given padding
    length. The `chars` string may be truncated if the number of padding
    characters can't be evenly divided by the padding length.

    Args:
        text (str): String to pad.
        length (int): Amount to pad.
        chars (str, optional): Chars to pad with. Defaults to ``" "``.

    Returns:
        str: Padded string.

    .. versionadded:: 1.1.0
    """
    text = pyd.to_string(text)
    length = max((length, len(text)))
    return (text + repeat(chars, length))[:length]


def repeat(text, n=0):
    """Repeats the given string `n` times.

    Args:
        text (str): String to repeat.
        n (int, optional): Number of times to repeat the string.

    Returns:
        str: Repeated string.

    .. versionadded:: 1.1.0
    """
    return pyd.to_string(text) * int(n)


def snake_case(text):
    """Converts `text` to snake case.

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to snake case.

    .. versionadded:: 1.1.0
    """
    return '_'.join(wrd.lower() for wrd in words(pyd.to_string(text)) if wrd)


def starts_with(text, target, position=None):
    """Checks if `text` starts with a given target string.

    Args:
        text (str): String to check.
        target (str): String to check for.
        position (int, optional): Position to search from. Defaults to
            beginning of `text`.

    Returns:
        bool: Whether `text` starts with `target`.

    .. versionadded:: 1.1.0
    """
    text = pyd.to_string(text)

    if position is None:
        position = 0

    return text[position:].startswith(target)


def trim(text, chars=None):
    """Removes leading and trailing whitespace or specified characters from
    `text`.

    Args:
        text (str): String to trim.
        chars (str, optional): Specific characters to remove.

    Returns:
        str: Trimmed string.

    .. versionadded:: 1.1.0
    """
    return pyd.to_string(text).strip(chars)


def trim_left(text, chars=None):
    """Removes leading  whitespace or specified characters from `text`.

    Args:
        text (str): String to trim.
        chars (str, optional): Specific characters to remove.

    Returns:
        str: Trimmed string.

    .. versionadded:: 1.1.0
    """
    return pyd.to_string(text).lstrip(chars)


def trim_right(text, chars=None):
    """Removes trailing whitespace or specified characters from `text`.

    Args:
        text (str): String to trim.
        chars (str, optional): Specific characters to remove.

    Returns:
        str: Trimmed string.

    .. versionadded:: 1.1.0
    """
    return pyd.to_string(text).rstrip(chars)


def trunc(text, length=30, omission='...', separator=None):
    """Truncates `text` if it is longer than the given maximum string length.
    The last characters of the truncated string are replaced with the omission
    string which defaults to ``...``.

    Args:
        text (str): String to truncate.
        length (int, optional): Maximum string length. Defaults to ``30``.
        omission (str, optional): String to indicate text is omitted.
        separator (mixed, optional): Separator pattern to truncate to.

    Returns:
        str: Truncated string.

    .. versionadded:: 1.1.0
    """
    omission_len = len(omission)
    text_len = length - omission_len
    text = pyd.to_string(text)[:text_len]

    trunc_len = len(text)

    if pyd.is_string(separator):
        trunc_len = text.rfind(separator)
    elif pyd.is_re(separator):
        last = None
        for match in separator.finditer(text):
            last = match

        if last is not None:
            trunc_len = last.start()

    return text[:trunc_len] + omission


def unescape(text):
    """The inverse of :func:`escape`. This method converts the HTML entities
    ``&amp;``, ``&lt;``, ``&gt;``, ``&quot;``, ``&#39;``, and ``&#96;`` in
    `text` to their corresponding characters.

    Args:
        text (str): String to unescape.

    Returns:
        str: HTML unescaped string.

    .. versionadded:: 1.0.0

    .. versionchanged:: 1.1.0
        Moved to Strings module.
    """
    return html_unescape(text)


def url(*paths, **params):
    """Combines a series of URL paths into a single URL. Optionally, pass in
    keyword arguments to append query parameters.

    Args:
        paths (str): URL paths to combine.

    Keyword Args:
        params (str, optional): Query parameters.

    Returns:
        str: URL string.

    .. versionadded:: 2.2.0
    """
    paths_list = []
    params_list = flatten_url_params(params)

    for path in paths:
        scheme, netloc, path, query, fragment = urlsplit(path)
        query = parse_qsl(query)
        params_list += query
        paths_list.append(urlunsplit((scheme, netloc, path, '', fragment)))

    path = delimitedpathjoin('/', *paths_list)
    scheme, netloc, path, query, fragment = urlsplit(path)
    query = urlencode(params_list)

    return urlunsplit((scheme, netloc, path, query, fragment))


def words(text):
    """Return list of words contained in `text`.

    Args:
        text (str): String to split.

    Returns:
        list: List of words.

    .. versionadded:: 2.0.0
    """
    return js_match(RE_WORDS, text)


#
# Utility functions not a part of main API
#


def js_to_py_re_find(reg_exp):
    """Return Python regular expression matching function based on Javascript
    style regexp.
    """
    pattern, options = reg_exp[1:].rsplit('/', 1)
    flags = re.I if 'i' in options else 0

    def find(text):  # pylint: disable=missing-docstring
        if 'g' in options:
            results = re.findall(pattern, text, flags=flags)
        else:
            results = re.search(pattern, text, flags=flags)

            if results:
                results = [results.group()]
            else:
                results = []

        return results

    return find


def js_to_py_re_replace(reg_exp):
    """Return Python regular expression substitution function based on
    Javascript style regexp.
    """
    pattern, options = reg_exp[1:].rsplit('/', 1)
    count = 0 if 'g' in options else 1
    flags = re.I if 'i' in options else 0

    def replace(text, repl):  # pylint: disable=missing-docstring
        if PY26:  # pragma: no cover
            sub = partial(re.compile(pattern, flags=flags).sub, count=count)
        else:
            sub = partial(re.sub, pattern, count=count, flags=flags)

        return sub(repl, text)

    return replace


def delimitedpathjoin(delimiter, *paths):
    """Join delimited path using specified delimiter.

    >>> assert delimitedpathjoin('.', '') == ''
    >>> assert delimitedpathjoin('.', '.') == '.'
    >>> assert delimitedpathjoin('.', ['', '.a']) == '.a'
    >>> assert delimitedpathjoin('.', ['a', '.']) == 'a.'
    >>> assert delimitedpathjoin('.', ['', '.a', '', '', 'b']) == '.a.b'
    >>> ret = '.a.b.c.d.e.'
    >>> assert delimitedpathjoin('.', ['.a.', 'b.', '.c', 'd', 'e.']) == ret
    >>> assert delimitedpathjoin('.', ['a', 'b', 'c']) == 'a.b.c'
    >>> ret = 'a.b.c.d.e.f'
    >>> assert delimitedpathjoin('.', ['a.b', '.c.d.', '.e.f']) == ret
    >>> ret = '.a.b.c.1.'
    >>> assert delimitedpathjoin('.', '.', 'a', 'b', 'c', 1, '.') == ret
    >>> assert delimitedpathjoin('.', []) == ''
    """
    paths = [pyd.to_string(path) for path in pyd.flatten_deep(paths) if path]

    if len(paths) == 1:
        # Special case where there's no need to join anything.
        # Doing this because if path==[delimiter], then an extra delimiter
        # would be added if the else clause ran instead.
        path = paths[0]
    else:
        leading = delimiter if paths and paths[0].startswith(delimiter) else ''
        trailing = delimiter if paths and paths[-1].endswith(delimiter) else ''
        middle = delimiter.join([path.strip(delimiter)
                                 for path in paths if path.strip(delimiter)])
        path = ''.join([leading, middle, trailing])

    return path


def flatten_url_params(params):
    """Flatten URL params into list of tuples. If any param value is a list or
    tuple, then map each value to the param key.
    >>> params = [('a', 1), ('a', [2, 3])]
    >>> assert flatten_url_params(params) == [('a', 1), ('a', 2), ('a', 3)]
    >>> params = {'a': [1, 2, 3]}
    >>> assert flatten_url_params(params) == [('a', 1), ('a', 2), ('a', 3)]
    """
    if isinstance(params, dict):
        params = list(iteritems(params))

    flattened = []
    for param, value in params:
        if isinstance(value, (list, tuple)):
            flattened += zip([param] * len(value), value)
        else:
            flattened.append((param, value))

    return flattened
