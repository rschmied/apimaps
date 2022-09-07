.PHONY: clean help requirements tests

# VERSION := $(shell dunamai from any)

clean:  ## clean up the directory
	rm -rf .mypy_cache .pytest_cache
	rm -f .coverage coverage.xml coverage.lcov
	rm -rf dist

tests:  ## run all unit tests
	coverage run -m pytest tests
	coverage xml

devinstall:  ## install all dev and test dependency
	poetry install --with dev,test

requirements:  ## update the requirements.txt file
	poetry export --with test --format=requirements.txt --output=tests/requirements.txt

# version:  ## set the version to latest git tag
# 	echo "__version__ = \"${VERSION}\"" > src/apimaps/_version.py

build:
	@VERSION=$$(dunamai from any) && \
	poetry version $$VERSION && \
	poetry build

help: ## Show help text
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "    \033[36m%-20s\033[0m %s\n", $$1, $$2}'
