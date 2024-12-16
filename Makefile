.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: *

## BUILD ==============================================================

## Run the application
run:
	poetry run python main.py

## Install dependencies
install:
	poetry install

## Check all before commit
pre-commit: cs cs-doc test-report

## Lint code
cs:
#pylint --disable=trailing-whitespace main.py
	poetry run pylint --output-format=colorized main.py sources/models/*.py sources/utilities/*.py sources/classes/*.py tests/models/*.py tests/classes/*.py tests/utilities/*.py
	poetry run black main.py sources/models/*.py sources/utilities/*.py sources/classes/*.py tests/models/*.py tests/classes/*.py tests/utilities/*.py --diff

## Lint docstrings
cs-doc:
#	numpydoc lint main.py sources/models/*.py sources/utilities/*.py sources/classes/*.py tests/classes/*.py tests/utilities/*.py
	poetry run ruff check

## Run tests
test:
	poetry run pytest 
# poetry run pytest -vv --cov=classes --cov=utilities
# poetry run pytest tests/classes/openproject_test.py::test_get_all

## Run tests with coverage report
test-report:
	poetry run pytest -v --cov=sources/classes --cov=sources/models --cov=sources/utilities --cov-report=html:./.tmp/coverage


## FORMATTER ==========================================================

# APPLICATION
APPLICATION := Product Migration

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

TARGET_MAX_CHAR_NUM=20
## Show this help
help:
	@echo '# ${YELLOW}${APPLICATION}${RESET} / ${GREEN}${ENV}${RESET}'
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			gsub(":", " ", helpCommand); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort