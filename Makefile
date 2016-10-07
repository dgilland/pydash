
##
# TravisCI
##

.PHONY: travisci-install
travisci-install:
	pip install -r requirements-dev.txt

.PHONY: travisci-test
travisci-test:
	invoke test
