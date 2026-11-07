# AGENTS.md

## Project

Termgraph is a Python CLI and library for drawing charts in the terminal. It supports horizontal, vertical, stacked, and multi-series bars, histograms, and CLI calendar heatmaps, with options for ANSI colors and custom ticks such as emoji.

The CLI reads files or standard input (omit the filename or pass `-`). Input rows contain a label and numeric values separated by commas, whitespace, or a custom delimiter. Text labels can appear before or after the values. For all-numeric rows, the first field is the label. Category headers start with `@`, and comment lines start with `#`.

See [README.md](README.md) for usage and examples, [docs/](docs/) for the Python API, and [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow. Sample inputs are in `data/`.

## Development

Use Python 3.9 or later, `uv`, and `just`. Runtime and development dependencies are declared in [pyproject.toml](pyproject.toml). The runtime dependency is `colorama>=0.4.6`.

| Command | Purpose |
| --- | --- |
| `just` | List available recipes. |
| `just install` | Sync development dependencies with `uv sync --dev`. |
| `just test` / `just test-verbose` | Run the pytest suite, optionally with verbose output. |
| `just test-file tests/test_charts.py` | Run a single pytest file. |
| `just test-module` | Run the three standalone Python API examples in `tests/module-test*.py`. |
| `just check` | Run Ruff linting and mypy type checking. Run each separately with `just lint` or `just typecheck`. |
| `just lint-fix` | Apply Ruff lint fixes and formatting across the repository. |
| `just run-example` | Run the CLI on `data/ex1.dat`. |
| `just run data/ex1.dat --width 20` | Run the CLI with a data file and optional CLI arguments. |
| `just build` / `just check-dist` | Clean and build distribution packages, with Twine validation via `check-dist`. |

Run `just check` and `just test` before submitting a change. Add tests for new functionality alongside related cases in `tests/`. Update usage documentation when behavior or options change.

## Architecture and compatibility

- `termgraph/termgraph.py` provides the CLI entry point, argument parsing, and chart dispatch. It maps CLI options into `Args` for the chart classes. Calendar heatmaps are rendered by `calendar_heatmap()` in this module.
- `termgraph/data.py` owns input parsing via `Data.from_file()`, data validation and dimensions, label and value statistics, and scaling via `Data.normalize()`.
- `termgraph/args.py` defines chart configuration and defaults. For options shared by the CLI and library, keep `Args.default` and the CLI parser in sync and verify both entry points.
- `termgraph/chart.py` contains the chart hierarchy and rendering. Extend the relevant chart class for rendering changes and reuse `Data` for data operations. Shared output helpers are in `termgraph/utils.py`, and constants are in `termgraph/constants.py`.
- `termgraph/__init__.py` exposes the public Python API through lazy imports. Preserve existing imports and behavior, including the compatibility exports in `termgraph/module.py` and the deprecated `read_data()` and `normalize()` wrappers in `termgraph/termgraph.py`.
