.PHONY: build clean clean-env clean-files install test pytest test-full test-setuppy lint pep8 pylint docs release travisci-install travisci-test

##
# Variables
##

ENV_NAME = env
ENV_ACT = . env/bin/activate;
PIP = $(ENV_NAME)/bin/pip
PYTEST_ARGS = --doctest-modules -v -s
PYTEST_TARGET = pydash tests
COVERAGE_ARGS = --cov-config setup.cfg --cov-report term-missing --cov
COVERAGE_TARGET = pydash

##
# Targets
##

# project initialization/clean-up
build: clean install

clean: clean-env clean-files

clean-env:
	rm -rf $(ENV_NAME)

clean-files:
	rm -rf .tox
	rm -rf .coverage
	find . -name \*.pyc -type f -delete
	find . -name \*.test.db -type f -delete
	find . -depth -name __pycache__ -type d -exec rm -rf {} \;
	rm -rf dist *.egg* build

install:
	rm -rf $(ENV_NAME)
	virtualenv --no-site-packages $(ENV_NAME)
	$(PIP) install -r requirements.txt


# testing
test: pep8 pytest

pytest:
	$(ENV_ACT) py.test $(PYTEST_ARGS) $(COVERAGE_ARGS) $(COVERAGE_TARGET) $(PYTEST_TARGET)

test-full: pylint-errors test-setuppy clean-files

test-setuppy:
	python setup.py test


# linting
lint: pylint pep8

pep8:
	$(ENV_ACT) pep8 $(PYTEST_TARGET)

pylint:
	$(ENV_ACT) pylint $(COVERAGE_TARGET)

pylint-errors:
	$(ENV_ACT) pylint -E $(COVERAGE_TARGET)


# code release
master:
	git checkout master
	git merge develop
	git push origin master
	git push --tags
	git checkout develop

release:
	$(ENV_ACT) python setup.py sdist bdist_wheel
	$(ENV_ACT) twine upload dist/*
	rm -rf dist *.egg* build

# docs
docs:
	rm -rf docs/_build
	$(ENV_ACT) cd docs; make doctest
	$(ENV_ACT) cd docs; make html

##
# TravisCI
##

travisci-install:
	pip install -r requirements-travis.txt

travisci-test:
	pep8 $(PYTEST_TARGET)
	pylint -E $(COVERAGE_TARGET)
	py.test $(PYTEST_ARGS) $(COVERAGE_ARGS) $(COVERAGE_TARGET) $(PYTEST_TARGET)
