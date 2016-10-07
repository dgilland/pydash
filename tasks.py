# -*- coding: utf-8 -*-

from invoke import run, task


REQUIREMENTS = 'requirements-dev.txt'
PACKAGE_NAME = 'pydash'
FLAKE8_IGNORE = ','.join([
    'F401',  # `module` imported but unused
    'F811',  # redefinition of unused `name` from line `N`
])
PYLINT_IGNORE = ','.join([
    'not-callable',
    'no-self-argument',
    'no-member',
    'no-value-for-parameter',
    'method-hidden'
])
TEST_TARGETS = ' '.join([PACKAGE_NAME, 'tests'])
COV_TARGET = PACKAGE_NAME


@task
def clean(ctx):
    """Remove temporary files related to development."""
    run('find . -name \*.py[cod] -type f -delete')
    run('find . -depth -name __pycache__ -type d -exec rm -rf {} \;')
    run('rm -rf .tox .coverage .cache .egg* *.egg* dist build')


@task
def install(ctx):
    """Install package development dependencies."""
    run('pip install -r {0}'.format(REQUIREMENTS))


@task
def flake8(ctx):
    """Run flake8 checker."""
    run('flake8 --ignore={0} {1}'.format(FLAKE8_IGNORE, TEST_TARGETS))


@task
def pylint(ctx):
    """Run pylint checker."""
    run('pylint -E -d {0} {1}'.format(PYLINT_IGNORE, TEST_TARGETS))


@task(pre=[flake8, pylint])
def lint(ctx):
    """Run static linter."""
    pass


@task
def unit(ctx):
    """Run unit tests."""
    run('py.test --cov {0} {1}'.format(COV_TARGET, TEST_TARGETS))


@task(pre=[lint, unit])
def test(ctx):
    """Run all tests."""
    pass


@task(post=[clean])
def tox(ctx):
    """Run tox testing."""
    run('tox -c tox.ini')


@task
def docs(ctx, serve=False, port=8000):
    """Build documentation."""
    run('rm -rf {0}'.format('docs/_build'))
    run('cd docs && make doctest && make html')

    if serve:
        print('Serving docs on port {0} ...'.format(port))
        run('cd {0} && python -m http.server {1}'
            .format('docs/_build/html', port))


@task
def build(ctx):
    """Build package distribution."""
    run('python setup.py sdist bdist_wheel')


@task(pre=[build], post=[clean])
def release(ctx):
    """Upload package distribution to PyPI."""
    run('twine upload dist/*')
