# AGENTS.md

This file provides guidance to AI agents when working with code in this repository.

## Project Overview

Termgraph is a Python command-line tool that draws basic graphs in the terminal. It supports various graph types including bar graphs, histograms, calendar heatmaps, stacked charts, and multi-variable visualizations with color support and emoji tick marks.

The tool can read data from files or stdin and output ASCII-based graphs directly to the terminal.

## Commands

### Development (using justfile)
- `just` - Show available commands
- `just install` - Install development dependencies using uv
- `just install-prod` - Install production dependencies only
- `just clean` - Remove build artifacts and cache files
- `just build` - Build distribution packages
- `just publish` - Publish to PyPI
- `just check` - Run all quality checks (lint + typecheck)

### Testing
- `just test` - Run the test suite using pytest
- `just test-verbose` - Run tests with verbose output
- `just test-file <file>` - Run specific test file
- `tests/coverage-report.sh` - Generate coverage report and open in browser (requires `coverage` package)

### Code Quality
- `just lint` - Check code with ruff
- `just lint-fix` - Fix code formatting and linting issues
- `just typecheck` - Run mypy type checking

### Running
- `just run-example` - Run with sample data (ex1.dat)
- `just run <file>` - Run with custom data file

### Installation Requirements
- Python 3.9+
- Dependencies: `colorama>=0.4.6` (specified in pyproject.toml)
- Development dependencies: `pytest`, `ruff`, `mypy`, `build`, `twine`
- Uses `uv` for dependency management

## Architecture

### Core Structure
- `termgraph/termgraph.py` - Main entry point with CLI argument parsing and core graph rendering logic
- `termgraph/module.py` - Object-oriented refactored classes (Data, Args, Chart, HorizontalChart, BarChart)
- `termgraph/utils.py` - Utility functions for number formatting
- `termgraph/constants.py` - Shared constants (colors, graph characters, units)
- `termgraph/__init__.py` - Package initialization, imports from termgraph module

### Key Components

**termgraph.py** contains the original procedural implementation with:
- CLI argument parsing via `init_args()`
- Data reading from files/stdin via `read_data()`
- Multiple graph types: horizontal bars, vertical bars, stacked, histograms, calendar heatmaps
- Color support using ANSI escape codes
- Normalization and scaling logic

**module.py** contains a refactored OOP approach with:
- `Data` class - Handles data validation, min/max finding, label management
- `Args` class - Manages chart configuration options
- `Chart` base class - Common functionality like normalization and header printing
- `HorizontalChart` and `BarChart` classes - Specific chart implementations

### Data Format
- Input: CSV or space-separated files with labels in first column, numeric data in subsequent columns
- Categories can be specified with lines starting with "@"
- Supports stdin input with filename "-"

### Graph Types
- Horizontal/vertical bar charts
- Multi-variable charts with same or different scales
- Stacked bar charts
- Histograms with configurable bins
- Calendar heatmaps for date-based data

The codebase shows both the original implementation (termgraph.py) and an in-progress refactor to OOP patterns (module.py), with the main entry point still using the original procedural code.