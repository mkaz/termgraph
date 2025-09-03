# Contributing to Termgraph

Thank you for your interest in contributing to Termgraph! This document provides guidance on the project structure and how to contribute effectively.

## Project Structure

Termgraph has been designed with a clean, modular architecture that supports both command-line usage and programmatic access.

### Architecture Overview

```
termgraph/
├── termgraph/
│   ├── __init__.py          # Package entry point with lazy imports
│   ├── termgraph.py         # CLI implementation and main entry point
│   ├── data.py             # Data class - handles all data operations
│   ├── args.py             # Args class - configuration management
│   ├── chart.py            # Chart classes - rendering and display
│   ├── module.py           # Backward compatibility module
│   ├── utils.py            # Utility functions (formatting, normalization)
│   └── constants.py        # Shared constants (colors, characters, units)
├── tests/                   # Test suite organized by functionality
├── data/                    # Sample data files for testing
└── README.md               # Project documentation
```

### Core Components

#### **Data Class (`data.py`)**
The `Data` class is responsible for:
- Data validation and structure verification
- Finding min/max values and label lengths
- Handling categories and multi-dimensional data
- Providing a clean interface for data operations

```python
from termgraph import Data

data = Data([[1, 2], [3, 4]], ["Label1", "Label2"])
print(data.find_max())  # 4
```

#### **Args Class (`args.py`)**
The `Args` class manages:
- Chart configuration options
- Default values and validation
- Type-safe access to arguments

```python
from termgraph import Args

args = Args(width=100, title="My Chart", percentage=True)
print(args.get_arg("width"))  # 100
```

#### **Chart Classes (`chart.py`)**
Chart classes handle:
- Chart rendering and display logic
- Header and legend printing
- Color management
- Different chart types (Bar, Horizontal, etc.)

```python
from termgraph import Data, Args, BarChart

data = Data([[10], [20]], ["A", "B"])
args = Args(title="Test Chart")
chart = BarChart(data, args)
chart.draw()
```

### Design Principles

1. **Class-Based Architecture**: Everything is organized around focused classes with clear responsibilities
2. **Single Source of Truth**: No duplicate implementations - data operations live in Data class, rendering in Chart classes
3. **Backward Compatibility**: All existing APIs are maintained through import forwarding
4. **Modular Organization**: Each class has its own file for better maintainability

## Development Workflow

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mkaz/termgraph.git
   cd termgraph
   ```

2. **Install development dependencies:**
   ```bash
   just install
   # or manually: uv sync --dev
   ```

3. **Run tests to verify setup:**
   ```bash
   just test
   ```

### Development Commands

We use `just` as our command runner. Available commands:

```bash
just                    # Show available commands
just install           # Install development dependencies
just test              # Run the test suite
just test-file <file>   # Run specific test file
just lint              # Check code with ruff
just lint-fix          # Fix code formatting issues
just typecheck         # Run mypy type checking
just check             # Run all quality checks (lint + typecheck)
just run-example       # Run with sample data
```

### Testing

Our test suite is organized by functionality:

```
tests/
├── README.md              # Testing documentation
├── test_check_data.py     # Data validation tests
├── test_data_utils.py     # Data utility function tests
├── test_normalize.py      # Data normalization tests
├── test_rendering.py      # Chart rendering tests
├── test_read_data.py      # Data parsing tests
└── test_init.py          # Initialization tests
```

**Adding New Tests:**
- Data validation → `test_check_data.py`
- Data operations → `test_data_utils.py`
- Chart rendering → `test_rendering.py`
- File parsing → `test_read_data.py`

### Code Quality

We maintain high code quality through:

- **Ruff** for linting and formatting
- **MyPy** for type checking
- **Comprehensive test suite** with good coverage
- **Clear naming conventions** and documentation

**Before submitting a PR:**
1. Run `just check` to verify code quality
2. Run `just test` to ensure all tests pass
3. Add tests for new functionality
4. Update documentation if needed

## Contributing Guidelines

### Reporting Issues

When reporting bugs or requesting features:
1. Check existing [GitHub Issues](https://github.com/mkaz/termgraph/issues)
2. Provide clear reproduction steps for bugs
3. Include sample data files when relevant
4. Specify your Python version and OS

### Pull Requests

1. **Fork the repository** and create a feature branch
2. **Write tests** for new functionality
3. **Follow existing code patterns** and class structure
4. **Maintain backward compatibility** - don't break existing APIs
5. **Update documentation** if your changes affect usage
6. **Run quality checks** before submitting

### API Design Guidelines

When adding new features:

#### **For Data Operations:**
- Add methods to the `Data` class
- Ensure they work with the existing data structure
- Add corresponding procedural functions in `data.py` for backward compatibility

#### **For Chart Options:**
- Add new arguments to `Args.default` dictionary
- Update CLI argument parsing in `termgraph.py`
- Ensure the option works in both CLI and programmatic usage

#### **For Chart Types:**
- Extend existing chart classes or create new ones inheriting from `Chart`
- Follow the existing rendering patterns
- Ensure compatibility with all chart options (colors, formatting, etc.)

### Examples of Good Contributions

#### Adding a New Chart Option:
```python
# 1. Add to Args.default in args.py
"new_option": False,

# 2. Add CLI argument in termgraph.py  
parser.add_argument("--new-option", action="store_true", help="Enable new option")

# 3. Use in chart rendering
if self.args.get_arg("new_option"):
    # implement feature
```

#### Adding a Data Operation:
```python
# 1. Add method to Data class in data.py
def new_operation(self) -> float:
    return some_calculation(self.data)

# 2. Add backward compatibility function
def new_operation(data: list) -> float:
    data_obj = Data(data, [str(i) for i in range(len(data))])
    return data_obj.new_operation()

# 3. Add tests in test_data_utils.py
def test_new_operation():
    # test implementation
```

## Questions?

- 💬 **Discussion**: Use [GitHub Issues](https://github.com/mkaz/termgraph/issues) for questions
- 🐛 **Bugs**: Report via [GitHub Issues](https://github.com/mkaz/termgraph/issues)
- 🚀 **Features**: Request via [GitHub Issues](https://github.com/mkaz/termgraph/issues)

Thank you for contributing to Termgraph! 🎉