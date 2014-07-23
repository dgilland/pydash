# How to Contribute

## Table of Contents

- [Overview](#overview)
- [Guidelines](#guidelines)
- [Branching](#branching)
- [Continuous Integration](#continuous-integration)
- [Project CLI](#project-cli)

## Overview

1. Fork the repo.
2. Build development environment run tests to ensure a clean, working slate.
4. Improve/fix the code.
5. Add test cases if new functionality introduced or bug fixed (100% test coverage).
6. Ensure tests pass.
7. Add yourself to `CONTRIBUTORS.md`.
8. Push to your fork and submit a pull request to the `develop` branch.

## Branching

There are two main development branches: `master` and `develop`. `master` represents the currently released version while `develop` is the latest development work. When submitting a pull request, be sure to submit to `develop`. The originating branch you submit from can be any name though.

## Guidelines

Some simple guidelines to follow when contributing code:

- Adhere to [PEP8][].
- Clean, well documented code.
- All tests pass.
- 100% test coverage.

## Continuous Integration

Integration testing is provided by [Travis-CI][]: https://travis-ci.org/dgilland/alchy.

Test coverage reporting is provided by [Coveralls][]: https://coveralls.io/r/dgilland/alchy.

## Project CLI

Some useful CLI commands when working on the project are below. **NOTE:** All commands are run from the root of the project and require `make`.

### make build

Run the `clean` and `install` commands.

```
make build
```

### make install

Create virtualenv `env/` and installs Python dependencies.

```
make install
```

### make clean

Remove build/test related temporary files like `env/`, `.tox`, `.coverage`, and `__pycache__`.

```
make clean
```

### make test

Run unittests under the virtualenv's default Python version. Does not test all support Python versions. To test all supported versions, see `make test-full`.

```
make test
```

### make test-full

Run unittest and linting for all supported Python versions. **NOTE:** This will fail if you do not have all Python versions installed on your system. If you are on an Ubuntu based system, the [Dead Snakes PPA][] is a good resource for easily installing multiple Python versions. If for whatever reason you're unable to have all Python versions on your development machine, note that Travis-CI will run full integration tests on all pull requests (minus linting).

```
make test-full
```

### make lint

Run `make pylint` and `make pep8` commands.

```
make lint
```

### make pylint

Run `pylint` compliance check on code base.

```python
make pylint
```

### make pep8

Run [PEP8][] compliance check on code base.

```
make pep8
```
