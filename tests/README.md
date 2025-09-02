# Tests

This directory contains the test suite for termgraph, organized into logical groups for better maintainability and clarity.

## Test Organization

The test suite is split into focused files based on functionality:

### `test_check_data.py`
Tests for the `check_data()` function that validates input data and arguments.
- Data validation (empty labels, empty data)
- Label/data size matching
- Color validation
- Category validation
- Error handling and exit codes

### `test_data_utils.py`
Tests for utility functions that operate on data.
- `find_min()` - finding minimum values in datasets
- `find_max()` - finding maximum values in datasets  
- `find_max_label_length()` - calculating label dimensions

### `test_normalize.py`
Tests for data normalization functionality.
- Basic normalization with various datasets
- Edge cases (all zeros, negative values)
- Different width scaling
- Boundary conditions

### `test_rendering.py`
Tests for chart rendering and display functions.
- `horiz_rows()` - horizontal chart row generation
- `vertically()` - vertical chart rendering
- Chart formatting and layout

### `test_read_data.py`
Tests for data input and parsing functionality.
- File reading from various formats
- Label parsing (beginning, end, multi-word)
- Category detection
- Title and verbose output
- Data format validation

### `test_init.py`
Tests for initialization and setup functions.
- Argument parsing and initialization

## Running Tests

### All Tests
```bash
just test           # Run all tests
just test-verbose   # Run all tests with verbose output
```

### Individual Test Files
```bash
just test-file tests/test_check_data.py
just test-file tests/test_normalize.py
# etc.
```

### Specific Tests
```bash
uv run python -m pytest tests/test_check_data.py::test_check_data_empty_labels_exits_with_one
uv run python -m pytest tests/test_normalize.py::test_normalize_with_negative_datapoint_returns_correct_results
```

## Adding New Tests

When adding new tests, place them in the appropriate file based on functionality:

- **Data validation** → `test_check_data.py`
- **Math/calculation utilities** → `test_data_utils.py` 
- **Data scaling/normalization** → `test_normalize.py`
- **Chart drawing/output** → `test_rendering.py`
- **File parsing/input** → `test_read_data.py`
- **Setup/configuration** → `test_init.py`

If your test doesn't fit into any existing category, consider:
1. Whether it belongs in an existing file with a broader scope
2. Creating a new focused test file (e.g., `test_calendar.py` for calendar-specific functionality)

## Test Conventions

- Use descriptive test names that explain what is being tested
- Include docstrings for complex test scenarios
- Use `pytest.raises(SystemExit)` for testing error conditions that call `sys.exit()`
- Mock external dependencies (files, stdout) when needed
- Keep test data realistic but minimal

## Dependencies

Tests use the following packages:
- `pytest` - Test runner and framework
- `tempfile` - For creating temporary test files
- `unittest.mock` - For mocking dependencies
- `io.StringIO` - For capturing stdout in tests

## File Structure

```
tests/
├── README.md              # This file
├── test_check_data.py     # Data validation tests
├── test_data_utils.py     # Utility function tests
├── test_init.py           # Initialization tests
├── test_normalize.py      # Data normalization tests
├── test_read_data.py      # Data reading/parsing tests
├── test_rendering.py      # Chart rendering tests
└── coverage-report.sh     # Coverage report generator
```
