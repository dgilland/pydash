"""
This module provides the CLI interface for invoke tasks.

All tasks can be executed from this file's directory using:

$ inv <task>

Where <task> is a function defined below with the @task decorator.
"""

from functools import partial
import os
from pathlib import Path
import sys
import tempfile

from invoke import Context, Exit, UnexpectedExit, run as _run, task


PACKAGE_NAME = "pydash"
PACKAGE_SOURCE = f"src/{PACKAGE_NAME}"
MYPY_TESTS_DIR = "tests/pytest_mypy_testing"
TEST_TARGETS = f"{PACKAGE_SOURCE} tests"
LINT_TARGETS = f"{TEST_TARGETS} tasks.py"
EXIT_EXCEPTIONS = (Exit, UnexpectedExit, SystemExit)


# Set pyt=True to enable colored output when available.
run = partial(_run, pty=True)


@task()
def fmt(ctx: Context, target: str = "", quiet: bool = False) -> None:
    """Autoformat code and docstrings."""
    if not quiet:
        print("Running ruff format")
    ruff_format(ctx, target, quiet=quiet)

    if not quiet:
        print("Running ruff lint fixes")
    ruff_fix(ctx, target, quiet=quiet)


@task()
def ruff_format(ctx: Context, target: str = "", quiet: bool = False) -> None:
    """Autoformat code and docstrings using ruff."""
    run(f"ruff format {target}", hide=quiet)


@task()
def ruff_fix(ctx: Context, target: str = "", quiet: bool = False) -> None:
    """Autofix fixable lint issues using ruff."""
    run(f"ruff check {target} --fix", hide=quiet)


@task()
def ruff_format_check(ctx: Context) -> None:
    """Check code for static errors using pylint."""
    run("ruff format --check")


@task()
def ruff_check(ctx: Context) -> None:
    """Check code for static errors using pylint."""
    run("ruff check")


@task()
def mypy(ctx: Context) -> None:
    """Check code using mypy type checker."""
    run(f"mypy {LINT_TARGETS} --no-error-summary")


@task()
def lint(ctx: Context) -> None:
    """Run linters."""
    linters = {
        "ruff-format-check": ruff_format_check,
        "ruff-check": ruff_check,
        "mypy": mypy,
    }

    # in python 3.8 and before the ast module doesn't have the `unparse` function
    # which is needed for the generation
    if sys.version_info >= (3, 9):
        linters["chaining-types-update-required"] = chaining_types_update_required

    failures = []

    print(f"Preparing to run linters: {', '.join(linters)}\n")

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
        raise Exit(f"ERROR: linters failed: {failed}")


@task(help={"args": "Override default pytest arguments"})
def test(
    ctx: Context, args: str = f"{TEST_TARGETS} --cov={PACKAGE_NAME}", with_mypy_tests: bool = False
) -> None:
    """Run unit tests using pytest."""
    tox_env_site_packages_dir = os.getenv("TOX_ENV_SITE_PACKAGES_DIR")
    if tox_env_site_packages_dir:
        # Re-path package source to match tox env so that we generate proper coverage report.
        tox_env_pkg_src = os.path.join(tox_env_site_packages_dir, os.path.basename(PACKAGE_SOURCE))
        args = args.replace(PACKAGE_SOURCE, tox_env_pkg_src)

    ignored_dirs = f"--ignore={MYPY_TESTS_DIR}" if with_mypy_tests is False else ""

    run(f"pytest {args} {ignored_dirs}")


@task()
def ci(ctx: Context) -> None:
    """Run linters and tests."""
    print("Building package")
    build(ctx)

    print("Building docs")
    docs(ctx)

    print("Checking linters")
    lint(ctx)

    print("Running unit tests")
    test(ctx)


@task()
def docs(ctx: Context, serve: bool = False, bind: str = "127.0.0.1", port: int = 8000) -> None:
    """Build docs."""
    run("rm -rf docs/_build")
    run("sphinx-build -q -W -b html docs docs/_build/html")

    if serve:
        print(f"Serving docs on {bind} port {port} (http://{bind}:{port}/) ...")
        run(f"python -m http.server -b {bind} --directory docs/_build/html {port}", hide=True)


@task()
def build(ctx: Context) -> None:
    """Build Python package."""
    run("rm -rf dist build docs/_build")
    run("python -m build")


@task()
def clean(ctx: Context) -> None:
    """Remove temporary files related to development."""
    run("find . -type f -name '*.py[cod]' -delete -o -type d -name __pycache__ -delete")
    run("rm -rf .tox .coverage .cache .pytest_cache **/.egg* **/*.egg* dist build .mypy_cache")


@task(pre=[build])
def release(ctx: Context) -> None:
    """Release Python package."""
    run("twine upload dist/*")


@task()
def generate_mypy_test(ctx: Context, file: str) -> None:
    """Generate base mypy test ready to be filled from doctests inside a python file."""
    run(
        "python scripts/mypy_doctests_generator.py"
        f" {file} tests/pytest_mypy_testing/test_{Path(file).name}"
    )


@task()
def generate_chaining_types(
    ctx: Context, output: str = "src/pydash/chaining/all_funcs.pyi"
) -> None:
    """Generates `all_funcs.pyi` stub file that types the chaining interface."""
    run(
        "python scripts/chaining_type_generator.py"
        f" --class_name AllFuncs --output {output} --wrapper Chain"
    )
    fmt(ctx, output, quiet=True)


@task()
def chaining_types_update_required(ctx: Context) -> None:
    with tempfile.NamedTemporaryFile(suffix=".pyi", dir=".") as tmp_file:
        generate_chaining_types(ctx, tmp_file.name)

        with open("src/pydash/chaining/all_funcs.pyi", "rb") as current_file:
            current = current_file.read()
        with open(tmp_file.name, "rb") as formatted_tmp_file:
            new = formatted_tmp_file.read()

        if current != new:
            err_msg = (
                "ERROR: src/pydash/chaining/all_funcs.pyi is out of date. Please run "
                "`inv generate-chaining-types` and commit the changes."
            )
            print(err_msg, file=sys.stderr)
            raise Exit()
