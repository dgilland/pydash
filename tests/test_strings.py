
import re

import pydash as _
from pydash._compat import urlsplit, parse_qsl
from .fixtures import parametrize


@parametrize('case,expected', [
    ('foo bar baz', 'fooBarBaz'),
    ('foo  bar baz', 'fooBarBaz'),
    ('foo__bar_baz', 'fooBarBaz'),
    ('foo-_bar-_-baz', 'fooBarBaz'),
    ('foo!bar,baz', 'fooBarBaz'),
    ('--foo.bar;baz', 'fooBarBaz'),
])
def test_camel_case(case, expected):
    assert _.camel_case(case) == expected


@parametrize('case,expected', [
    ('foo', 'Foo'),
    ('foo bar', 'Foo bar'),
    ('fOO bar', 'Foo bar'),
])
def test_capitalize(case, expected):
    assert _.capitalize(case) == expected


@parametrize('case,expected', [
    ('\xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xCB\xCC\xCD\xCE\xCF'
     '\xD0\xD1\xD2\xD3\xD4\xD5\xD6\xD7\xD8\xD9\xDA\xDB\xDC\xDD\xDE\xDF'
     '\xE0\xE1\xE2\xE3\xE4\xE5\xE6\xE7\xE8\xE9\xEA\xEB\xEC\xED\xEE\xEF'
     '\xF0\xF1\xF2\xF3\xF4\xF5\xF6\xF7\xF8\xF9\xFA\xFB\xFC\xFD\xFE\xFF',
     'AAAAAAAeCEEEEIIII'
     'DNOOOOO OUUUUYThss'
     'aaaaaaaeceeeeiiii'
     'dnooooo ouuuuythy')
])
def test_deburr(case, expected):
    assert _.deburr(case) == expected


@parametrize('case,expected', [
    (('abc', 'c'), True),
    (('abc', 'b'), False),
    (('abc', 'c', 3), True),
    (('abc', 'c', 2), False),
    (('abc', 'b', 2), True),
    (('abc', 'b', 1), False),
])
def test_ends_with(case, expected):
    assert _.ends_with(*case) == expected


@parametrize('case,expected', [
    ('abc<> &"\'`efg', 'abc&lt;&gt; &amp;&quot;&#39;&#96;efg')
])
def test_escape(case, expected):
    assert _.escape(case) == expected


@parametrize('case,expected', [
    ('[pydash](http://pydash.readthedocs.org/)',
     '\[pydash\]\(http\:\/\/pydash\.readthedocs\.org\/\)')
])
def test_escape_reg_exp(case, expected):
    assert _.escape_reg_exp(case) == expected


@parametrize('case', [
    _.escape_re
])
def test_escape_reg_exp_aliases(case):
    assert _.escape_reg_exp is case


@parametrize('case,expected', [
    (('string',), ['s', 't', 'r', 'i', 'n', 'g']),
    (('string1,string2', ','), ['string1', 'string2']),
])
def test_explode(case, expected):
    assert _.explode(*case) == expected


@parametrize('case,expected', [
    ((['s', 't', 'r', 'i', 'n', 'g'],), 'string'),
    ((['string1', 'string2'], ','), 'string1,string2'),
])
def test_implode(case, expected):
    assert _.implode(*case) == expected


@parametrize('case,expected', [
    (('/[A-Z]/', 'Hello World'), ['H']),
    (('/[A-Z]/g', 'Hello World'), ['H', 'W']),
    (('/[A-Z]/i', 'hello world'), ['h']),
    (('/[A-Z]/gi', 'hello world'),
     ['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd']),
    (('/[A-Z]/', '12345'), [])
])
def test_js_match(case, expected):
    assert _.js_match(*case) == expected


@parametrize('case,expected', [
    (('/[A-Z]/', 'Hello World', '!'), '!ello World'),
    (('/[A-Z]/g', 'Hello World', '!'), '!ello !orld'),
    (('/[A-Z]/i', 'hello world', '!'), '!ello world'),
    (('/[A-Z]/gi', 'hello world', '!'), '!!!!! !!!!!'),
])
def test_js_replace(case, expected):
    assert _.js_replace(*case) == expected


@parametrize('case,expected', [
    ('foo  bar baz', 'foo-bar-baz'),
    ('foo__bar_baz', 'foo-bar-baz'),
    ('foo-_bar-_-baz', 'foo-bar-baz'),
    ('foo!bar,baz', 'foo-bar-baz'),
    ('--foo.bar;baz', 'foo-bar-baz'),
])
def test_kebab_case(case, expected):
    assert _.kebab_case(case) == expected


@parametrize('case,expected', [
    (('abc', 8), '  abc   '),
    (('abc', 8, '_-'), '_-abc_-_'),
    (('abc', 3), 'abc'),
])
def test_pad(case, expected):
    assert _.pad(*case) == expected


@parametrize('case,expected', [
    (('aaaaa', 3), 'aaaaa'),
    (('aaaaa', 6), ' aaaaa'),
    (('aaaaa', 10), '     aaaaa'),
    (('aaaaa', 6, 'b'), 'baaaaa'),
    (('aaaaa', 6, 'bc'), 'caaaaa'),
    (('aaaaa', 9, 'bc'), 'bcbcaaaaa'),
])
def test_pad_left(case, expected):
    assert _.pad_left(*case) == expected


@parametrize('case,expected', [
    (('aaaaa', 3), 'aaaaa'),
    (('aaaaa', 6), 'aaaaa '),
    (('aaaaa', 10), 'aaaaa     '),
    (('aaaaa', 6, 'b'), 'aaaaab'),
    (('aaaaa', 6, 'bc'), 'aaaaab'),
    (('aaaaa', 9, 'bc'), 'aaaaabcbc'),
])
def test_pad_right(case, expected):
    assert _.pad_right(*case) == expected


@parametrize('case,expected', [
    ('foo  bar baz', 'foo_bar_baz'),
    ('foo__bar_baz', 'foo_bar_baz'),
    ('foo-_bar-_-baz', 'foo_bar_baz'),
    ('foo!bar,baz', 'foo_bar_baz'),
    ('--foo.bar;baz', 'foo_bar_baz'),
    ('FooBar', 'foo_bar'),
])
def test_snake_case(case, expected):
    assert _.snake_case(case) == expected


@parametrize('case,expected', [
    (('abc', 'a'), True),
    (('abc', 'b'), False),
    (('abc', 'a', 0), True),
    (('abc', 'a', 1), False),
    (('abc', 'b', 1), True),
    (('abc', 'b', 2), False),
])
def test_starts_with(case, expected):
    assert _.starts_with(*case) == expected


@parametrize('case,expected', [
    (('  fred  ',), 'fred'),
    (('-_-fred-_-', '_-'), 'fred'),
])
def test_trim(case, expected):
    assert _.trim(*case) == expected


@parametrize('case,expected', [
    (('  fred  ',), 'fred  '),
    (('-_-fred-_-', '_-'), 'fred-_-'),
])
def test_trim_left(case, expected):
    assert _.trim_left(*case) == expected


@parametrize('case,expected', [
    (('  fred  ',), '  fred'),
    (('-_-fred-_-', '_-'), '-_-fred'),
])
def test_trim_right(case, expected):
    assert _.trim_right(*case) == expected


@parametrize('case,expected', [
    (('hi-diddly-ho there, neighborino',), 'hi-diddly-ho there, neighbo...'),
    (('hi-diddly-ho there, neighborino', 24), 'hi-diddly-ho there, n...'),
    (('hi-diddly-ho there, neighborino', 24, '...', ' '),
     'hi-diddly-ho there,...'),
    (('hi-diddly-ho there, neighborino', 24, '...', re.compile(',? +')),
     'hi-diddly-ho there...'),
    (('hi-diddly-ho there, neighborino', 30, ' [...]'),
     'hi-diddly-ho there, neig [...]')
])
def test_trunc(case, expected):
    assert _.trunc(*case) == expected


@parametrize('case,expected', [
    ('abc&lt;&gt; &amp;&quot;&#39;&#96;efg', 'abc<> &"\'`efg')
])
def test_unescape(case, expected):
    assert _.unescape(case) == expected


@parametrize('case,expected', [
    ({'args': [''], 'kargs': {}}, ''),
    ({'args': ['/'], 'kargs': {}}, '/'),
    ({'args': ['http://github.com'], 'kargs': {}}, 'http://github.com'),
    ({'args': ['http://github.com:80'], 'kargs': {}}, 'http://github.com:80'),
    ({'args': ['http://github.com:80', 'pydash', 'issues/'], 'kargs': {}},
     'http://github.com:80/pydash/issues/'),
    ({'args': ['/foo', 'bar', '/baz', '/qux/'], 'kargs': {}},
     '/foo/bar/baz/qux/'),
    ({'args': ['/foo/bar'], 'kargs': {'a': 1, 'b': 'two'}},
     '/foo/bar?a=1&b=two'),
    ({'args': ['/foo/bar?x=5'], 'kargs': {'a': 1, 'b': 'two'}},
     '/foo/bar?x=5&a=1&b=two'),
    ({'args': ['/foo/bar?x=5', 'baz?z=3'], 'kargs': {'a': 1, 'b': 'two'}},
     '/foo/bar/baz?x=5&a=1&b=two&z=3'),
    ({'args': ['/foo/bar?x=5', 'baz?z=3'], 'kargs': {'a': [1, 2], 'b': 'two'}},
     '/foo/bar/baz?x=5&a=1&a=2&b=two&z=3'),
    ({'args': ['/foo#bar', 'baz'], 'kargs': {'a': [1, 2], 'b': 'two'}},
     '/foo?a=1&a=2&b=two#bar/baz'),
    ({'args': ['/foo', 'baz#bar'], 'kargs': {'a': [1, 2], 'b': 'two'}},
     '/foo/baz?a=1&a=2&b=two#bar'),
])
def test_url(case, expected):
    result = _.url(*case['args'], **case['kargs'])

    r_scheme, r_netloc, r_path, r_query, r_fragment = urlsplit(result)
    e_scheme, e_netloc, e_path, e_query, e_fragment = urlsplit(expected)

    assert r_scheme == e_scheme
    assert r_netloc == e_netloc
    assert r_path == e_path
    assert set(parse_qsl(r_query)) == set(parse_qsl(e_query))
    assert r_fragment == e_fragment


@parametrize('case,expected', [
    ('hello world!', ['hello', 'world']),
    ('hello_world', ['hello', 'world']),
    ('hello!@#$%^&*()_+{}|:"<>?-=[]\;\,.\'/world', ['hello', 'world']),
    ('hello 12345 world', ['hello', '12345', 'world']),
])
def test_words(case, expected):
    assert _.words(case) == expected


@parametrize('source,wrapper,expected', (
    ('hello world!', '*', '*hello world!*'),
    ('hello world!', '**', '**hello world!**'),
    ('', '**', '****'),
    ('hello world!', '', 'hello world!'),
))
def test_surround(source, wrapper, expected):
    assert _.surround(source, wrapper) == expected


@parametrize('source,quote_char,expected', (
    ('hello world!', '*', '*hello world!*'),
    ('hello world!', '**', '**hello world!**'),
    ('', '**', '****'),
    ('hello world!', '', 'hello world!'),
))
def test_quote(source, quote_char, expected):
    assert _.quote(source, quote_char) == expected


@parametrize('source,expected', (
    ('hello world!', '\"hello world!\"'),
    ('', '""'),
))
def test_default_quote(source, expected):
    assert _.quote(source) == expected
