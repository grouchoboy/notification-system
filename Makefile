default: help
	@echo ""
	@echo "You need to specify a subcommand"
	@exit 1

help:
	@echo "install              - install all the dependencies"
	@echo "example              - run the example application"
	@echo "test                 - run tests"
	@echo "coverage             - run tests and report coverage in html"
	@echo "mypy                 - check types with mypy"
	@echo "format               - format the source code"
	@echo "format-check         - check for format error without change any file"

install:
	poetry install

example:
	poetry run python example.py

mypy:
	poetry run mypy notification_system tests

test:
	poetry run pytest --cov

coverage:
	poetry run pytest --cov --cov-report=html

format:
	poetry run black notification_system tests
	poetry run isort notification_system/**.py tests/**.py

format-check:
	poetry run black --check notification_system tests
