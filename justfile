# Justfile for termgraph
# Run `just` to see available recipes

# Default recipe to display available commands
default:
    @just --list

# Install development dependencies
install:
    uv run python -m pip install -e ".[dev]"

# Install production dependencies only
install-prod:
    uv run python -m pip install -e .

# Clean build artifacts
clean:
    rm -rf dist/
    rm -rf build/
    rm -rf *.egg-info/
    rm -rf .coverage
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

# Run tests with coverage
test-coverage:
    uv run python -m pytest --cov=termgraph --cov-report=term-missing --cov-report=html

# Run specific test file
test-file file:
    uv run python -m pytest {{file}} -v

# Lint code with ruff
lint:
    uv run python -m ruff check .

# Format code with ruff
format:
    uv run python -m ruff format .

# Check formatting without making changes
format-check:
    uv run python -m ruff format --check .

# Run type checking with mypy
typecheck:
    uv run python -m mypy termgraph/

# Run all quality checks (lint, format, typecheck)
check: lint format-check typecheck

# Fix linting issues automatically
fix:
    uv run python -m ruff check --fix .
    uv run python -m ruff format .

# Build distribution packages
build: clean
    uv run python -m build

# Check distribution packages
check-dist: build
    uv run python -m twine check dist/*

# Publish to PyPI
publish: build check-dist
    uv run python -m twine upload dist/*

# Publish to Test PyPI
publish-test: build check-dist
    uv run python -m twine upload --repository testpypi dist/*

# Run the application with sample data
run-example:
    uv run python -m termgraph.termgraph data/ex1.dat

# Run the application with custom data
run file:
    uv run python -m termgraph.termgraph {{file}}

# Generate test coverage report and open in browser
coverage-html: test-coverage
    @echo "Opening coverage report in browser..."
    @uv run python -c "import webbrowser; webbrowser.open('htmlcov/index.html')"

# Run performance benchmark (if you add benchmarking later)
benchmark:
    @echo "No benchmarks configured yet"

# Setup pre-commit hooks
setup-hooks:
    @echo "Setting up git pre-commit hook..."
    @echo '#!/bin/sh\njust check' > .git/hooks/pre-commit
    @chmod +x .git/hooks/pre-commit
    @echo "Pre-commit hook installed!"

# Development environment setup
setup: install setup-hooks
    @echo "Development environment setup complete!"

# Check if project is ready for release
release-check: clean check test-coverage check-dist
    @echo "✅ Project is ready for release!"
