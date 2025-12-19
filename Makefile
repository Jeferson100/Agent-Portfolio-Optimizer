#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = Agent-Portfolio-Optimizer
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

uv_install:
	uv pip install --upgrade pip && \
		uv pip install -r pyproject.toml

uv_dev_install:
	uv pip install -e ".[dev]"

install:
	pip install --upgrade pip && \
		pip install -r requirements.txt

import_format:
	uv run isort src/

format:
	uv run black src/

ruff_format:
	uv run ruff format src/

lint:
	uv run pylint --disable=R,C src/

ruff_lint:
	uv run ruff check src/

typepyright:
	uv run pyright src/

typemypy:
	uv run mypy src/

typepyrefly:
	uv run pyrefly check src/

## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	@echo ">>> Creating virtual environment using uv..."
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> Virtual environment created in .venv"
	@echo ">>> Activate it in your terminal with:"
	@echo ">>>   Windows: .\.venv\Scripts\activate"
	@echo ">>>   Unix/macOS: source ./.venv/bin/activate"

## Run tests
test:
	python scripts/run_tests.py

test_verbose:
	uv run pytest -v

test_coverage:
	python scripts/run_tests.py --coverage

test_unit:
	python scripts/run_tests.py --unit

test_integration:
	python scripts/run_tests.py --integration

test_fast:
	python scripts/run_tests.py --fast

test_all:
	python scripts/run_tests.py --all

test_watch:
	uv run pytest-watch

test_specific:
	uv run pytest $(TEST_PATH)

refactor: format lint

all: uv_install uv_dev_install import_format format lint typepyright typepyrefly import_format ruff_format ruff_lint test