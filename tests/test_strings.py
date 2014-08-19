
import pydash as pyd
from .fixtures import parametrize


@parametrize('case,expected', [
    ('abc<> &"\'`efg', 'abc&lt;&gt; &amp;&quot;&#39;&#96;efg')
])
def test_escape(case, expected):
    assert pyd.escape(case) == expected


@parametrize('case,expected', [
    ('abc&lt;&gt; &amp;&quot;&#39;&#96;efg', 'abc<> &"\'`efg')
])
def test_unescape(case, expected):
    assert pyd.unescape(case) == expected
