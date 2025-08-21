# Justfile for termgraph
# Run `just` to see available recipes

# Default recipe to display available commands
default:
    @just --list

# Install development dependencies
install:
    uv sync --dev

# Install production dependencies only
install-prod:
    uv sync

# Clean build artifacts
clean:
    rm -rf dist/
    rm -rf build/
    rm -rf *.egg-info/
    rm -rf htmlcov/
    rm -rf .pytest_cache/
    rm -rf .ruff_cache/
    find . -type d -name __pycache__ -delete
    find . -type f -name "*.pyc" -delete

# Run tests
test:
    uv run python -m pytest

# Run tests with verbose output
test-verbose:
    uv run python -m pytest -v

# Run specific test file
test-file file:
    uv run python -m pytest {{file}} -v

# Lint code with ruff
lint:
    uv run python -m ruff check .

# Format code with ruff
lint-fix:
    uv run python -m ruff check --fix .
    uv run python -m ruff format .

typecheck:
    uv run python -m mypy termgraph/

# Run all quality checks (lint, format, typecheck)
check: lint typecheck

# Build distribution packages
build: clean
    uv run python -m build

# Check distribution packages
check-dist: build
    uv run python -m twine check dist/*

# Publish to PyPI
publish: build check-dist
    uv run python -m twine upload dist/*

# Run the application with sample data
run-example:
    uv run python -m termgraph.termgraph data/ex1.dat

# Run the application with custom data
run file:
    uv run python -m termgraph.termgraph {{file}}

