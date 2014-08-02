How to Contribute
*****************

- Overview_
- Guidelines_
- Branching_
- `Continuous Integration`_
- `Project CLI`_


Overview
========

1. Fork the repo.
2. Build development environment run tests to ensure a clean, working slate.
3. Improve/fix the code.
4. Add test cases if new functionality introduced or bug fixed (100% test coverage).
5. Ensure tests pass.
6. Add yourself to ``AUTHORS.rst``.
7. Push to your fork and submit a pull request to the ``develop`` branch.


Guidelines
==========

Some simple guidelines to follow when contributing code:

- Adhere to `PEP8`_.
- Clean, well documented code.
- All tests must pass.
- 100% test coverage.


Branching
=========

There are two main development branches: ``master`` and ``develop``. ``master`` represents the currently released version while ``develop`` is the latest development work. When submitting a pull request, be sure to submit to ``develop``. The originating branch you submit from can be any name though.


Continuous Integration
======================

Integration testing is provided by `Travis-CI`_ at https://travis-ci.org/dgilland/pydash.

Test coverage reporting is provided by `Coveralls`_ at https://coveralls.io/r/dgilland/pydash.


Project CLI
===========

Some useful CLI commands when working on the project are below. **NOTE:** All commands are run from the root of the project and require ``make``.

make build
----------

Run the ``clean`` and ``install`` commands.

::

    make build


make install
------------

Install Python dependencies into virtualenv located at ``env/``.

::

    make install


make clean
----------

Remove build/test related temporary files like ``env/``, ``.tox``, ``.coverage``, and ``__pycache__``.

::

    make clean


make test
---------

Run unittests under the virtualenv's default Python version. Does not test all support Python versions. To test all supported versions, see `make test-full`_.

::

    make test


make test-full
--------------

Run unittest and linting for all supported Python versions. **NOTE:** This will fail if you do not have all Python versions installed on your system. If you are on an Ubuntu based system, the `Dead Snakes PPA`_ is a good resource for easily installing multiple Python versions. If for whatever reason you're unable to have all Python versions on your development machine, note that Travis-CI will run full integration tests on all pull requests.

::

    make test-full


make lint
---------

Run ``make pylint`` and ``make pep8`` commands.

::

    make lint


make pylint
-----------

Run ``pylint`` compliance check on code base.

::

    make pylint


make pep8
---------

Run `PEP8`_ compliance check on code base.

::

    make pep8


make docs
---------

Build documentation to ``docs/_build/``.

::

    make docs


.. _Travis-CI: https://travis-ci.org/
.. _Coveralls: https://coveralls.io/
.. _Dead Snakes PPA: https://launchpad.net/~fkrull/+archive/deadsnakes
.. _PEP8: http://legacy.python.org/dev/peps/pep-0008/
