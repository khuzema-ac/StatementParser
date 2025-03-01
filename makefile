# Write makefile commands to create a wheel distribution of the project.

.PHONY: all clean

all:  clean test lint docs build
	
.PHONY: clean	
clean:
# clean build files and .vemv
	# rm -rf .venv
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf build dist *.egg-info
	# python3 -m venv .venv
	# source .venv/bin/activate
	pip install --upgrade pip
	pip install --upgrade build
	pip install -e .[dev]

.PHONY: build
build:
# build with toml file
	pip install --upgrade build
	python -m build
	
.PHONY: install
install:
	pip install .

.PHONY: test
test:
	pytest tests/*.py

.PHONY: lint
lint:
	flake8 bank_statement_parser/*
	flake8 tests/*

.PHONY: docs
docs:
	python -m sphinx -b html docs/build/html

.PHONY: release
release:
# release to pypi with twine and toml file
	pip install --upgrade twine
	pip install --upgrade build
	python -m build
	twine upload dist/*