"""
This module provides the CLI interface for invoke tasks.

All tasks can be executed from this file's directory using:

    $ inv <task>

Where <task> is a function defined below with the @task decorator.
"""

from __future__ import print_function

from functools import partial

from invoke import Exit, UnexpectedExit, run as _run, task


PACKAGE_SOURCE = "src/pydash"
TEST_TARGETS = "{} tests".format(PACKAGE_SOURCE)
LINT_TARGETS = "{} tasks.py".format(PACKAGE_SOURCE)
EXIT_EXCEPTIONS = (Exit, UnexpectedExit, SystemExit)


# Set pyt=True to enable colored output when available.
run = partial(_run, pty=True)


@task
def black(ctx, quiet=False):
    """Autoformat code using black."""
    run("black {}".format(LINT_TARGETS), hide=quiet)


@task
def isort(ctx, quiet=False):
    """Autoformat Python imports."""
    run("isort {}".format(LINT_TARGETS), hide=quiet)


@task
def docformatter(ctx):
    """Autoformat docstrings using docformatter."""
    run(
        "docformatter -r {} "
        "--in-place --pre-summary-newline --wrap-descriptions 100 --wrap-summaries 100".format(
            LINT_TARGETS
        )
    )


@task
def fmt(ctx):
    """Autoformat code and docstrings."""
    print("Running docformatter")
    docformatter(ctx)

    print("Running isort")
    isort(ctx, quiet=True)

    print("Running black")
    black(ctx, quiet=True)


@task
def flake8(ctx):
    """Check code for PEP8 violations using flake8."""
    run("flake8 --format=pylint {}".format(LINT_TARGETS))


@task
def pylint(ctx):
    """Check code for static errors using pylint."""
    run("pylint {}".format(LINT_TARGETS))


@task
def lint(ctx):
    """Run linters."""
    linters = {"flake8": flake8, "pylint": pylint}
    failures = []

    for name, linter in linters.items():
        print("Running {}".format(name))
        try:
            linter(ctx)
        except EXIT_EXCEPTIONS:
            failures.append(name)
            result = "FAILED"
        else:
            result = "PASSED"
        print("{}\n".format(result))

    if failures:
        failed = ", ".join(failures)
        raise Exit("ERROR: Linters that failed: {}".format(failed))


@task(help={"args": "Override default pytest arguments"})
def unit(ctx, args="--cov={} {}".format(PACKAGE_SOURCE, TEST_TARGETS)):
    """Run unit tests using pytest."""
    run("pytest {}".format(args))


@task
def test(ctx):
    """Run linters and tests."""
    print("Building package")
    build(ctx)

    print("Building docs")
    docs(ctx)

    print("Running unit tests")
    unit(ctx)


@task
def docs(ctx, serve=False, bind="127.0.0.1", port=8000):
    """Build docs."""
    run("rm -rf docs/_build")
    run("sphinx-build -q -W -b html docs docs/_build/html")

    if serve:
        print(
            "Serving docs on {bind} port {port} (http://{bind}:{port}/) ...".format(
                bind=bind, port=port
            )
        )
        run(
            "python -m http.server -b {bind} --directory docs/_build/html {port}".format(
                bind=bind, port=port
            ),
            hide=True,
        )


@task
def build(ctx):
    """Build Python package."""
    run("rm -rf dist build docs/_build")
    run("python setup.py -q sdist bdist_wheel")


@task
def clean(ctx):
    """Remove temporary files related to development."""
    run("find . -type f -name '*.py[cod]' -delete -o -type d -name __pycache__ -delete")
    run("rm -rf .tox .coverage .cache .pytest_cache **/.egg* **/*.egg* dist build")


@task(pre=[build])
def release(ctx):
    """Release Python package."""
    run("twine upload dist/*")
