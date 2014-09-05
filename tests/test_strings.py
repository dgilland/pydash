
import re

import pydash as pyd
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
    assert pyd.camel_case(case) == expected


@parametrize('case,expected', [
    ('foo', 'Foo'),
    ('foo bar', 'Foo bar'),
    ('fOO bar', 'Foo bar'),
])
def test_capitalize(case, expected):
    assert pyd.capitalize(case) == expected


@parametrize('case,expected', [
    (('abc', 'c'), True),
    (('abc', 'b'), False),
    (('abc', 'c', 3), True),
    (('abc', 'c', 2), False),
    (('abc', 'b', 2), True),
    (('abc', 'b', 1), False),
])
def test_ends_with(case, expected):
    assert pyd.ends_with(*case) == expected


@parametrize('case,expected', [
    ('abc<> &"\'`efg', 'abc&lt;&gt; &amp;&quot;&#39;&#96;efg')
])
def test_escape(case, expected):
    assert pyd.escape(case) == expected


@parametrize('case,expected', [
    ('[pydash](http://pydash.readthedocs.org/)',
     '\[pydash\]\(http\:\/\/pydash\.readthedocs\.org\/\)')
])
def test_escape_reg_exp(case, expected):
    assert pyd.escape_reg_exp(case) == expected


@parametrize('case', [
    pyd.escape_re
])
def test_escape_reg_exp_aliases(case):
    assert pyd.escape_reg_exp is case


@parametrize('case,expected', [
    (('string',), ['s', 't', 'r', 'i', 'n', 'g']),
    (('string1,string2', ','), ['string1', 'string2']),
])
def test_explode(case, expected):
    assert pyd.explode(*case) == expected


@parametrize('case,expected', [
    ((['s', 't', 'r', 'i', 'n', 'g'],), 'string'),
    ((['string1', 'string2'], ','), 'string1,string2'),
])
def test_implode(case, expected):
    assert pyd.implode(*case) == expected


@parametrize('case,expected', [
    ('foo  bar baz', 'foo-bar-baz'),
    ('foo__bar_baz', 'foo-bar-baz'),
    ('foo-_bar-_-baz', 'foo-bar-baz'),
    ('foo!bar,baz', 'foo-bar-baz'),
    ('--foo.bar;baz', 'foo-bar-baz'),
])
def test_kebab_case(case, expected):
    assert pyd.kebab_case(case) == expected


@parametrize('case,expected', [
    (('abc', 8), '  abc   '),
    (('abc', 8, '_-'), '_-abc_-_'),
    (('abc', 3), 'abc'),
])
def test_pad(case, expected):
    assert pyd.pad(*case) == expected


@parametrize('case,expected', [
    (('aaaaa', 3), 'aaaaa'),
    (('aaaaa', 6), ' aaaaa'),
    (('aaaaa', 10), '     aaaaa'),
    (('aaaaa', 6, 'b'), 'baaaaa'),
    (('aaaaa', 6, 'bc'), 'caaaaa'),
    (('aaaaa', 9, 'bc'), 'bcbcaaaaa'),
])
def test_pad_left(case, expected):
    assert pyd.pad_left(*case) == expected


@parametrize('case,expected', [
    (('aaaaa', 3), 'aaaaa'),
    (('aaaaa', 6), 'aaaaa '),
    (('aaaaa', 10), 'aaaaa     '),
    (('aaaaa', 6, 'b'), 'aaaaab'),
    (('aaaaa', 6, 'bc'), 'aaaaab'),
    (('aaaaa', 9, 'bc'), 'aaaaabcbc'),
])
def test_pad_right(case, expected):
    assert pyd.pad_right(*case) == expected


@parametrize('case,expected', [
    ('foo  bar baz', 'foo_bar_baz'),
    ('foo__bar_baz', 'foo_bar_baz'),
    ('foo-_bar-_-baz', 'foo_bar_baz'),
    ('foo!bar,baz', 'foo_bar_baz'),
    ('--foo.bar;baz', 'foo_bar_baz'),
])
def test_snake_case(case, expected):
    assert pyd.snake_case(case) == expected


@parametrize('case,expected', [
    (('abc', 'a'), True),
    (('abc', 'b'), False),
    (('abc', 'a', 0), True),
    (('abc', 'a', 1), False),
    (('abc', 'b', 1), True),
    (('abc', 'b', 2), False),
])
def test_starts_with(case, expected):
    assert pyd.starts_with(*case) == expected


@parametrize('case,expected', [
    (('  fred  ',), 'fred'),
    (('-_-fred-_-', '_-'), 'fred'),
])
def test_trim(case, expected):
    assert pyd.trim(*case) == expected


@parametrize('case,expected', [
    (('  fred  ',), 'fred  '),
    (('-_-fred-_-', '_-'), 'fred-_-'),
])
def test_trim_left(case, expected):
    assert pyd.trim_left(*case) == expected


@parametrize('case,expected', [
    (('  fred  ',), '  fred'),
    (('-_-fred-_-', '_-'), '-_-fred'),
])
def test_trim_right(case, expected):
    assert pyd.trim_right(*case) == expected


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
    assert pyd.trunc(*case) == expected


@parametrize('case,expected', [
    ('abc&lt;&gt; &amp;&quot;&#39;&#96;efg', 'abc<> &"\'`efg')
])
def test_unescape(case, expected):
    assert pyd.unescape(case) == expected
