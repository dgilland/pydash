# pydash

[![Package Version](http://img.shields.io/pypi/v/pydash.svg?style=flat)](https://pypi.python.org/pypi/pydash/)
[![Build Status](http://img.shields.io/travis/dgilland/pydash/master.svg?style=flat)](https://travis-ci.org/dgilland/pydash)
[![Coverage Status](http://img.shields.io/coveralls/dgilland/pydash/master.svg?style=flat)](https://coveralls.io/r/dgilland/pydash)
[![License](http://img.shields.io/pypi/l/pydash.svg?style=flat)](https://pypi.python.org/pypi/pydash/)


Python port of the [Lo-Dash](http://Lo-Dash.com/) Javascript library.

Currently, alpha stage.

Current status of initial port: https://github.com/dgilland/pydash/issues/2


## Requirements

### Compatibility

- (maybe) Python 2.6
- Python 2.7
- (planned) Python 3

### Dependencies

None.


## Installation

```
pip install pydash
```

## Overview

### Differences between Lo-Dash

- Function names use `snake_case` instead of `camelCase`.
- Any Lo-Dash function which shares its name with a reserved Python keyword will have an `_` appended after it (e.g. `filter` in Lo-Dash would be `filter_` in pydash.
- Extra callback args must be explictly handled. In Javascript, it's perfectly fine to pass in extra arguments to a function that aren't explictly accepted by that function (e.g. `function foo(a1){}; foo(1, 2, 3);`). In Python, those extra arguments must be explictly handled (e.g. `def foo(a1, *args): ...; foo(1, 2, 3)`). Therefore, callbacks passed to `pydash` functions must use named args or a catch-all like `*args` since each callback is passed `item`, `index`, and `array`.


## License

This software is licensed under the MIT License.
