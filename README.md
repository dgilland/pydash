# pydash

[![Package Version](https://pypip.in/v/pydash/badge.png)](https://pypi.python.org/pypi/pydash/)
[![Build Status](https://travis-ci.org/dgilland/pydash.png?branch=master)](https://travis-ci.org/dgilland/pydash)
[![Coverage Status](https://coveralls.io/repos/dgilland/pydash/badge.png?branch=master)](https://coveralls.io/r/dgilland/pydash)
[![License](https://pypip.in/license/pydash/badge.png)](https://pypi.python.org/pypi/pydash/)


Python port of the [Lodash](http://lodash.com/) Javascript library.

Currently, alpha stage.






## Differences between Lodash

- Function names use `snake_case` instead of `camelCase`.
- Any Lodash function which shares its name with a reserved Python keyword will have an `_` appended after it (e.g. `filter` in Lodash would be `filter_` in Pydash.
- Extra callback args must be explictly handled. In Javascript, it's perfectly fine to pass in extra arguments to a function that aren't explictly accepted by that function (e.g. `function foo(a1){}; foo(1, 2, 3);`). In Python, those extra arguments must be explictly handled (e.g. `def foo(a1, *args): ...; foo(1, 2, 3)`). Therefore, callbacks passed to `pydash` functions must use named args or a catch-all like `*args` since each callback is passed `item`, `index`, and `array`.


## License

This software is licensed under the MIT License.
