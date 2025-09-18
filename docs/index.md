# Termgraph API Documentation

Welcome to the Termgraph Python API documentation. Termgraph is a command-line tool for creating terminal-based charts and graphs, and can also be used as a Python library for programmatic chart generation.

## Documentation Structure

### 📖 **[Getting Started](README.md)**
Complete overview with examples and best practices for using termgraph as a Python module.

### 📊 **[Data Class](data-class.md)**
Learn how to prepare and structure your data for charts:
- Data validation and normalization
- Working with flat and nested data
- Handling categories and labels
- Examples with real-world data

### 📈 **[Chart Classes](chart-classes.md)**
Comprehensive guide to all available chart types:
- **BarChart** - Horizontal bar charts (single and multi-series)
- **StackedChart** - Stacked bar charts for part-to-whole relationships
- **VerticalChart** - Column charts for time series data
- **HistogramChart** - Distribution charts for continuous data
- **Colors** - Color constants for styling

### ⚙️ **[Args Class](args-class.md)**
Configuration options for customizing chart appearance and behavior:
- Chart dimensions and layout
- Value formatting and display
- Color schemes and styling
- Chart-specific options

## Quick Navigation

### Common Tasks

| Task | Documentation |
|------|---------------|
| Create a simple bar chart | [README.md - Quick Start](README.md#quick-start) |
| Work with multi-series data | [Data Class - Multi-Series](data-class.md#multi-series-data-with-categories) |
| Customize chart colors | [Args Class - Colors](args-class.md#colors) |
| Format numeric values | [Args Class - Value Formatting](args-class.md#value-formatting) |
| Create stacked charts | [Chart Classes - StackedChart](chart-classes.md#stackedchart) |
| Handle negative values | [Data Class - Negative Values](data-class.md#working-with-negative-values) |

### Chart Type Selection

| Data Type | Recommended Chart | Documentation |
|-----------|------------------|---------------|
| Simple categories | BarChart | [Chart Classes - BarChart](chart-classes.md#barchart) |
| Time series | VerticalChart | [Chart Classes - VerticalChart](chart-classes.md#verticalchart) |
| Parts of a whole | StackedChart | [Chart Classes - StackedChart](chart-classes.md#stackedchart) |
| Data distribution | HistogramChart | [Chart Classes - HistogramChart](chart-classes.md#histogramchart) |
| Multi-series comparison | BarChart (multi-series) | [Chart Classes - Multi-Series](chart-classes.md#multi-series-example) |

### Example Scenarios

| Scenario | Example Location |
|----------|------------------|
| Financial dashboard | [README.md - Financial Dashboard](README.md#financial-dashboard) |
| Performance metrics | [README.md - Performance Metrics](README.md#performance-metrics-dashboard) |
| Project tracking | [README.md - Project Status](README.md#project-status-tracking) |
| Sales analysis | [README.md - Sales Trend](README.md#sales-trend-analysis) |
| Data validation | [Data Class - Validation](data-class.md#data-validation-examples) |

## Code Examples by Complexity

### Beginner
- [Simple bar chart](README.md#simple-bar-chart)
- [Basic styling](README.md#styled-chart)
- [Single series data](data-class.md#basic-flat-data)

### Intermediate
- [Multi-series charts](chart-classes.md#multi-series-example)
- [Custom formatting](args-class.md#advanced-formatting)
- [Different chart types](README.md#chart-types)

### Advanced
- [Financial dashboard](README.md#financial-dashboard)
- [Different scales](chart-classes.md#different-scale-example)
- [Complex data structures](data-class.md#multi-series-data-with-categories)

## API Classes Overview

```python
from termgraph import Data, BarChart, StackedChart, VerticalChart, HistogramChart, Args, Colors

# Core workflow
data = Data([10, 20, 30], ["A", "B", "C"])        # Data preparation
args = Args(width=50, colors=[Colors.Blue])        # Configuration
chart = BarChart(data, args)                       # Chart creation
chart.draw()                                       # Visualization
```

## Installation and Setup

```bash
# Install termgraph
pip install termgraph

# Basic usage in Python
python -c "from termgraph import Data, BarChart; chart = BarChart(Data([1,2,3], ['A','B','C'])); chart.draw()"
```

## Support and Contributing

- **Issues**: Report bugs and feature requests on [GitHub Issues](https://github.com/mkaz/termgraph/issues)
- **Documentation**: This documentation is maintained alongside the codebase
- **Examples**: Additional examples can be found in the repository's test files

---

**Note**: This documentation covers using termgraph as a Python library. For command-line usage, see the main README in the repository root.