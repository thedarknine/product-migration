.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: *

## BUILD ==============================================================

## Run the application
run:
	python3 app.py

## Initialize environment
init: install shell

## Install dependencies
install:
	python3 -m venv venv
	pipenv install

## Enter virtual environment
shell:
	pipenv shell


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