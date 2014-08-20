"""String functions.

.. versionadded:: 1.1.0
"""

import re
import string

from .arrays import compact
from .objects import is_string, is_reg_exp
from .._compat import (
    text_type,
    string_types,
    html_unescape
)


__all__ = [
    'camel_case',
    'capitalize',
    'ends_with',
    'escape',
    'escape_reg_exp',
    'escape_re',
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
]


HTML_ESCAPES = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '`': '&#96;'
}

RE_WORD_SEPARATORS = re.compile('[ {0}]'.format(re.escape(string.punctuation)))


def camel_case(text):
    """Converts `text` to camel case.

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to camel case.

    .. versionadded:: 1.1.0
    """
    text = ''.join(word.title()
                   for word in RE_WORD_SEPARATORS.split(text_type(text)))
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
    text = text_type(text)

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
    return ''.join(HTML_ESCAPES.get(char, char) for char in text_type(text))


def escape_reg_exp(text):
    r"""Escapes the RegExp special characters in `text`.

    Args:
        text (str): String to escape.

    Returns:
        str: RegExp escaped string.

    .. versionadded:: 1.1.0
    """
    return re.escape(text)


escape_re = escape_reg_exp


def kebab_case(text):
    """Converts `text` to kebab case (a.k.a. spinal case).

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to kebab case.

    .. versionadded:: 1.1.0
    """
    return ('-'.join(word
                     for word in RE_WORD_SEPARATORS.split(text_type(text))
                     if word)
            .lower())


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
    text = text_type(text)
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
    text = text_type(text)
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
    text = text_type(text)
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
    return text_type(text) * int(n)


def snake_case(text):
    """Converts `text` to snake case.

    Args:
        text (str): String to convert.

    Returns:
        str: String converted to snake case.

    .. versionadded:: 1.1.0
    """
    return ('_'.join(word
                     for word in RE_WORD_SEPARATORS.split(text_type(text))
                     if word)
            .lower())


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
    text = text_type(text)

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
    return text_type(text).strip(chars)


def trim_left(text, chars=None):
    """Removes leading  whitespace or specified characters from `text`.

    Args:
        text (str): String to trim.
        chars (str, optional): Specific characters to remove.

    Returns:
        str: Trimmed string.

    .. versionadded:: 1.1.0
    """
    return text_type(text).lstrip(chars)


def trim_right(text, chars=None):
    """Removes trailing whitespace or specified characters from `text`.

    Args:
        text (str): String to trim.
        chars (str, optional): Specific characters to remove.

    Returns:
        str: Trimmed string.

    .. versionadded:: 1.1.0
    """
    return text_type(text).rstrip(chars)


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
    text = text_type(text)[:text_len]

    trunc_len = len(text)

    if is_string(separator):
        trunc_len = text.rfind(separator)
    elif is_reg_exp(separator):
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
