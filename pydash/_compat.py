# pylint: skip-file
"""Python 2/3 compatibility

    Some py2/py3 compatibility support based on a stripped down
    version of six so we don't have to depend on a specific version
    of it.

    Borrowed from
    https://github.com/mitsuhiko/flask/blob/master/flask/_compat.py
"""

import sys
import cgi
from decimal import Decimal
from functools import partial


PY3 = sys.version_info[0] == 3
_identity = lambda x: x


if PY3:
    from html.parser import HTMLParser
    text_type = str
    string_types = (str,)
    integer_types = (int,)
    number_types = (int, float, Decimal)

    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())

    _range = range

    implements_to_string = _identity
else:
    from HTMLParser import HTMLParser
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
    number_types = (int, long, float, Decimal)

    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()

    _range = xrange

    def implements_to_string(cls):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls


html_escape = partial(cgi.escape, quote=True)
html_unescape = HTMLParser().unescape
