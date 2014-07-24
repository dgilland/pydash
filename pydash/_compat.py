# pylint: skip-file
"""Python 2/3 compatibility

    Some py2/py3 compatibility support based on a stripped down
    version of six so we don't have to depend on a specific version
    of it.

    Borrowed from
    https://github.com/mitsuhiko/flask/blob/master/flask/_compat.py
"""

import sys


PY3 = sys.version_info[0] == 3
_identity = lambda x: x


if PY3:
    text_type = str
    string_types = (str,)
    integer_types = (int,)

    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())

    _range = range

    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value

    implements_to_string = _identity
else:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)

    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()

    _range = xrange

    exec('def reraise(tp, value, tb=None):\n raise tp, value, tb')

    def implements_to_string(cls):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls
