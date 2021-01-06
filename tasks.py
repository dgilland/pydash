"""
This module provides the CLI interface for invoke tasks.

All tasks can be executed from this file's directory using:

    $ inv <task>

Where <task> is a function defined below with the @task decorator.
"""

from functools import partial
import os

from invoke import Exit, UnexpectedExit, run as _run, task


PACKAGE_NAME = "pydash"
PACKAGE_SOURCE = f"src/{PACKAGE_NAME}"
TEST_TARGETS = f"{PACKAGE_SOURCE} tests"
LINT_TARGETS = f"{TEST_TARGETS} tasks.py"
EXIT_EXCEPTIONS = (Exit, UnexpectedExit, SystemExit)


# Set pyt=True to enable colored output when available.
run = partial(_run, pty=True)


@task
def black(ctx, quiet=False):
    """Autoformat code using black."""
    run(f"black {LINT_TARGETS}", hide=quiet)


@task
def isort(ctx, quiet=False):
    """Autoformat Python imports."""
    run(f"isort {LINT_TARGETS}", hide=quiet)


@task
def docformatter(ctx):
    """Autoformat docstrings using docformatter."""
    run(
        f"docformatter -r {LINT_TARGETS} "
        f"--in-place --pre-summary-newline --wrap-descriptions 100 --wrap-summaries 100"
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
    run(f"flake8 --format=pylint {LINT_TARGETS}")


@task
def pylint(ctx):
    """Check code for static errors using pylint."""
    run(f"pylint {LINT_TARGETS}")


@task
def lint(ctx):
    """Run linters."""
    linters = {"flake8": flake8, "pylint": pylint}
    failures = []

    for name, linter in linters.items():
        print(f"Running {name}")
        try:
            linter(ctx)
        except EXIT_EXCEPTIONS:
            failures.append(name)
            result = "FAILED"
        else:
            result = "PASSED"
        print(f"{result}\n")

    if failures:
        failed = ", ".join(failures)
        raise Exit(f"ERROR: Linters that failed: {failed}")


@task(help={"args": "Override default pytest arguments"})
def unit(ctx, args=f"{TEST_TARGETS} --cov={PACKAGE_NAME} --flake8 --pylint"):
    """Run unit tests using pytest."""
    tox_env_site_packages_dir = os.getenv("TOX_ENV_SITE_PACKAGES_DIR")
    if tox_env_site_packages_dir:
        # Re-path package source to match tox env so that we generate proper coverage report.
        tox_env_pkg_src = os.path.join(tox_env_site_packages_dir, os.path.basename(PACKAGE_SOURCE))
        args = args.replace(PACKAGE_SOURCE, tox_env_pkg_src)

    run(f"pytest {args}")


@task
def test(ctx):
    """Run linters and tests."""
    print("Building package")
    build(ctx)

    print("Building docs")
    docs(ctx)

    print("Checking linters")
    lint(ctx)

    print("Running unit tests")
    unit(ctx, args=f"{TEST_TARGETS} --cov={PACKAGE_NAME}")


@task
def docs(ctx, serve=False, bind="127.0.0.1", port=8000):
    """Build docs."""
    run("rm -rf docs/_build")
    run("sphinx-build -q -W -b html docs docs/_build/html")

    if serve:
        print(f"Serving docs on {bind} port {port} (http://{bind}:{port}/) ...")
        run(f"python -m http.server -b {bind} --directory docs/_build/html {port}", hide=True)


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
