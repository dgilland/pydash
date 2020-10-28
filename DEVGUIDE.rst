Developer Guide
===============

This guide provides an overview of the tooling this project uses and how to execute developer workflows using the developer CLI.


Python Environments
-------------------

This Python project is tested against different Python versions. For local development, it is a good idea to have those versions installed so that tests can be run against each.

There are libraries that can help with this. Which tools to use is largely a matter of preference, but below are a few recommendations.

For managing multiple Python versions:

- pyenv_
- OS package manager (e.g. apt, yum, homebrew, etc)
- Build from source

For managing Python virtualenvs:

- pyenv-virtualenv_
- pew_
- python-venv_


Tooling
-------

The following tools are used by this project:

=============  ==========================  ==================
Tool           Description                 Configuration
=============  ==========================  ==================
black_         Code formatter              ``pyproject.toml``
isort_         Import statement formatter  ``setup.cfg``
docformatter_  Docstring formatter         ``setup.cfg``
flake8_        Code linter                 ``setup.cfg``
pylint_        Code linter                 ``pylintrc``
pytest_        Test framework              ``setup.cfg``
tox_           Test environment manager    ``tox.ini``
invoke_        CLI task execution library  ``tasks.py``
=============  ==========================  ==================


Workflows
---------

The following workflows use developer CLI commands via `invoke`_ and are defined in ``tasks.py``.

Autoformat Code
+++++++++++++++

To run all autoformatters:

::

    inv fmt

This is the same as running each autoformatter individually:

::

    inv black
    inv isort
    inv docformatter


Lint
++++

To run all linters:

::

    inv lint

This is the same as running each linter individually:

::

    inv flake8
    inv pylint


Test
++++

To run all unit tests:

::

    inv unit


To run unit tests and builds:

::

    inv test


Test on All Supported Python Versions
+++++++++++++++++++++++++++++++++++++

To run tests on all supported Python versions:

::

    tox

This requires that the supported versions are available on the PATH.


Build Package
+++++++++++++

To build the package:

::

    inv build

This will output the source and binary distributions under ``dist/``.


Build Docs
++++++++++

To build documentation:

::

    inv docs

This will output the documentation under ``docs/_build/``.


Serve Docs
++++++++++

To serve docs over HTTP:

::

    inv docs -s|--server [-b|--bind 127.0.0.1] [-p|--port 8000]

    inv docs -s
    inv docs -s -p 8080
    inv docs -s -b 0.0.0.0 -p 8080


Delete Build Files
++++++++++++++++++

To remove all build and temporary files:

::

    inv clean

This will remove Python bytecode files, egg files, build output folders, caches, and tox folders.


Release Package
+++++++++++++++

To release a new version of the package to https://pypi.org:

::

    inv release


CI/CD
-----

This project uses `Github Actions <https://docs.github.com/en/free-pro-team@latest/actions>`_ for CI/CD:

- https://github.com/dgilland/fnc/actions


.. _pyenv: https://github.com/pyenv/pyenv
.. _pyenv-virtualenv: https://github.com/pyenv/pyenv-virtualenv
.. _pew: https://github.com/berdario/pew
.. _python-venv: https://docs.python.org/3/library/venv.html
.. _black: https://black.readthedocs.io
.. _isort: https://pycqa.github.io/isort/
.. _docformatter: https://github.com/myint/docformatter
.. _flake8: https://flake8.pycqa.org
.. _pylint: https://www.pylint.org/
.. _pytest: https://docs.pytest.org
.. _tox: https://tox.readthedocs.io
.. _invoke: http://docs.pyinvoke.org
