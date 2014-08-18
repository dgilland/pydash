"""String functions.
"""

from .._compat import (
    text_type,
    html_unescape
)


HTML_ESCAPES = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '`': '&#96;'
}


__all__ = [
    'escape',
    'unescape',
]


def escape(string):
    r"""Converts the characters ``&``, ``<``, ``>``, ``"``, ``'``, and ``\``` in
    `string` to their corresponding HTML entities.

    Args:
        string (str): String to escape.

    Returns:
        str: HTML escaped string.
    """
    # NOTE: Not using _compat.html_escape because Lo-Dash escapes certain chars
    # differently (e.g. "'" isn't escaped by html_escape() but is by Lo-Dash).
    return ''.join(HTML_ESCAPES.get(char, char) for char in text_type(string))


def unescape(string):
    """The inverse of :func:`escape`. This method converts the HTML entities
    ``&amp;``, ``&lt;``, ``&gt;``, ``&quot;``, ``&#39;``, and ``&#96;`` in
    `string` to their corresponding characters.

    Args:
        string (str): String to unescape.

    Returns:
        str: HTML unescaped string.
    """
    return html_unescape(string)
