.PHONY: clean requirements tests

clean:
	rm -rf .mypy_cache .pytest_cache
	rm -f .coverage coverage.xml coverage.lcov

tests:
	coverage run -m pytest tests
	coverage xml

requirements:
	poetry export --with dev --format=requirements.txt  --output=tests/requirements.txt
