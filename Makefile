.PHONY: clean devinstall export help tests

clean:  ## clean up the directory
	rm -rf .mypy_cache .pytest_cache
	rm -f .coverage coverage.xml coverage.lcov
	rm -rf dist

tests:  ## run all unit tests
	coverage run -m pytest tests
	coverage xml

devinstall:  ## install all dev and test dependency
	poetry install --with dev,test

export:  ## update the requirements.txt file
	poetry export --with test  \
		--format=requirements.txt \
		--output=tests/requirements.txt \
		--without-hashes 

build:
	poetry build

help: ## Show help text
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "    \033[36m%-20s\033[0m %s\n", $$1, $$2}'
