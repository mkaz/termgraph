# Termgraph Python API Documentation

Termgraph is a Python library for creating terminal-based charts and graphs. This documentation covers using termgraph as a Python module for programmatic chart generation.

## Quick Start

```python
from termgraph import Data, BarChart, Args

# Create data
data = Data([23, 45, 56, 78, 32], ["A", "B", "C", "D", "E"])

# Create and display chart
chart = BarChart(data)
chart.draw()
```

## Installation

```bash
pip install termgraph
```

## Core Components

Termgraph consists of three main classes:

1. **[Data](data-class.md)** - Handles data storage, validation, and normalization
2. **[Chart Classes](chart-classes.md)** - Various chart types (Bar, Stacked, Vertical, Histogram)
3. **[Args](args-class.md)** - Configuration and styling options

## Basic Usage

### Simple Bar Chart

```python
from termgraph import Data, BarChart

# Sales data
data = Data(
    data=[150, 230, 180, 290, 210],
    labels=["Jan", "Feb", "Mar", "Apr", "May"]
)

chart = BarChart(data)
chart.draw()
```

Output:
```
Jan: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 150.00
Feb: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 230.00
Mar: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 180.00
Apr: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 290.00
May: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 210.00
```

### Styled Chart

```python
from termgraph import Data, BarChart, Args, Colors

data = Data(
    data=[150, 230, 180, 290, 210],
    labels=["Jan", "Feb", "Mar", "Apr", "May"]
)

args = Args(
    width=60,
    title="Monthly Sales Report",
    colors=[Colors.Green],
    suffix=" units",
    format="{:<6.0f}"
)

chart = BarChart(data, args)
chart.draw()
```

Output:
```
# Monthly Sales Report

Jan: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 150    units
Feb: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 230    units
Mar: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 180    units
Apr: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 290    units
May: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 210    units
```

## Chart Types

### Bar Chart (Horizontal)

Best for comparing values across categories.

```python
from termgraph import Data, BarChart, Args, Colors

# Single series
data = Data([45, 32, 78, 56, 23], ["Product A", "Product B", "Product C", "Product D", "Product E"])
chart = BarChart(data, Args(colors=[Colors.Blue]))
chart.draw()
```

### Multi-Series Bar Chart

Compare multiple data series side by side.

```python
from termgraph import Data, BarChart, Args, Colors

# Quarterly sales for two products
data = Data(
    data=[
        [120, 80],   # Q1: Product A, Product B
        [150, 95],   # Q2: Product A, Product B
        [180, 110],  # Q3: Product A, Product B
        [200, 125]   # Q4: Product A, Product B
    ],
    labels=["Q1", "Q2", "Q3", "Q4"],
    categories=["Product A", "Product B"]
)

args = Args(
    title="Quarterly Sales Comparison",
    colors=[Colors.Blue, Colors.Red],
    width=50
)

chart = BarChart(data, args)
chart.draw()
```

### Stacked Bar Chart

Show parts of a whole.

```python
from termgraph import Data, StackedChart, Args, Colors

# Budget breakdown
data = Data(
    data=[
        [30, 20, 10],  # Q1: Marketing, Development, Operations
        [35, 25, 15],  # Q2: Marketing, Development, Operations
        [40, 30, 20],  # Q3: Marketing, Development, Operations
        [45, 35, 25]   # Q4: Marketing, Development, Operations
    ],
    labels=["Q1", "Q2", "Q3", "Q4"],
    categories=["Marketing", "Development", "Operations"]
)

args = Args(
    title="Budget Allocation by Quarter",
    colors=[Colors.Green, Colors.Blue, Colors.Yellow],
    suffix="K"
)

chart = StackedChart(data, args)
chart.draw()
```

### Vertical Chart (Column Chart)

Good for time series or when you have many categories.

```python
from termgraph import Data, VerticalChart, Args, Colors

data = Data([23, 45, 56, 78, 32, 67, 45], ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

args = Args(
    title="Daily Website Visits",
    colors=[Colors.Cyan],
    width=40
)

chart = VerticalChart(data, args)
chart.draw()
```

### Histogram

Show distribution of continuous data.

```python
from termgraph import Data, HistogramChart, Args, Colors

# Temperature readings that will be binned
data = Data(
    data=[[15.2, 18.7, 22.1, 19.5, 25.3, 28.9, 24.4, 21.8, 26.2, 23.7, 20.1, 17.6]],
    labels=["Temperature Data"]
)

args = Args(
    title="Temperature Distribution",
    bins=6,
    colors=[Colors.Red],
    width=50
)

chart = HistogramChart(data, args)
chart.draw()
```

## Advanced Examples

### Financial Dashboard

```python
from termgraph import Data, BarChart, StackedChart, Args, Colors

# Revenue data
revenue_data = Data(
    data=[
        [450, 380, 290],  # Q1: Americas, EMEA, APAC
        [520, 420, 340],  # Q2: Americas, EMEA, APAC
        [480, 450, 380],  # Q3: Americas, EMEA, APAC
        [600, 480, 420]   # Q4: Americas, EMEA, APAC
    ],
    labels=["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023"],
    categories=["Americas", "EMEA", "APAC"]
)

# Revenue by region (stacked)
print("=== Revenue by Region (Stacked) ===")
stacked_args = Args(
    title="Quarterly Revenue by Region",
    colors=[Colors.Blue, Colors.Green, Colors.Yellow],
    width=60,
    suffix="K USD",
    format="{:<5.0f}"
)
stacked_chart = StackedChart(revenue_data, stacked_args)
stacked_chart.draw()

# Regional comparison (side by side)
print("\n=== Regional Performance Comparison ===")
bar_args = Args(
    title="Regional Performance by Quarter",
    colors=[Colors.Blue, Colors.Green, Colors.Yellow],
    width=60,
    suffix="K USD",
    space_between=True
)
bar_chart = BarChart(revenue_data, bar_args)
bar_chart.draw()
```

### Performance Metrics Dashboard

```python
from termgraph import Data, BarChart, Args, Colors

# Performance metrics with different scales
performance_data = Data(
    data=[
        [95.5, 1250],    # Uptime %, Response Time (ms)
        [98.2, 980],
        [97.1, 1100],
        [99.1, 850],
        [96.8, 1300]
    ],
    labels=["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"],
    categories=["Uptime (%)", "Response Time (ms)"]
)

args = Args(
    title="System Performance Metrics",
    colors=[Colors.Green, Colors.Red],
    different_scale=True,  # Use different scales for each metric
    width=50,
    space_between=True
)

chart = BarChart(performance_data, args)
chart.draw()
```

### Project Status Tracking

```python
from termgraph import Data, BarChart, Args, Colors

# Project completion percentages
projects_data = Data(
    data=[0.85, 0.62, 0.93, 0.78, 0.45, 0.91],
    labels=["Website Redesign", "Mobile App", "Database Migration", "API v2", "Documentation", "Testing Suite"]
)

args = Args(
    title="Project Completion Status",
    colors=[Colors.Green],
    percentage=True,
    width=50,
    format="{:<3.0f}",
    suffix="%"
)

chart = BarChart(projects_data, args)
chart.draw()
```

### Sales Trend Analysis

```python
from termgraph import Data, VerticalChart, BarChart, Args, Colors

# Monthly sales trend
monthly_sales = Data(
    data=[120, 135, 150, 145, 160, 175, 185, 170, 190, 200, 195, 210],
    labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
)

# Vertical chart for trend visualization
print("=== Monthly Sales Trend ===")
vertical_args = Args(
    title="2023 Sales Trend",
    colors=[Colors.Blue],
    width=60
)
vertical_chart = VerticalChart(monthly_sales, vertical_args)
vertical_chart.draw()

# Horizontal chart for precise values
print("\n=== Detailed Monthly Sales ===")
bar_args = Args(
    title="2023 Monthly Sales Details",
    colors=[Colors.Green],
    width=50,
    suffix="K USD",
    format="{:<5.0f}"
)
bar_chart = BarChart(monthly_sales, bar_args)
bar_chart.draw()
```

## Data Formats

### Flat Data (Single Series)

```python
# Simple list of numbers
data = Data([10, 20, 30, 40], ["A", "B", "C", "D"])
```

### Nested Data (Multi-Series)

```python
# List of lists for multiple data series
data = Data(
    data=[
        [10, 15, 20],  # Row 1: three values
        [25, 30, 35],  # Row 2: three values
        [40, 45, 50]   # Row 3: three values
    ],
    labels=["Category 1", "Category 2", "Category 3"],
    categories=["Series A", "Series B", "Series C"]
)
```

### Working with Real Data

```python
import csv
from termgraph import Data, BarChart, Args, Colors

# Reading from CSV (example)
def load_csv_data(filename):
    """Load data from CSV file."""
    data = []
    labels = []

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header

        for row in reader:
            labels.append(row[0])
            data.append(float(row[1]))

    return Data(data, labels)

# Usage
# data = load_csv_data('sales_data.csv')
# chart = BarChart(data, Args(title="Sales Data", colors=[Colors.Blue]))
# chart.draw()
```

## Error Handling

```python
from termgraph import Data, BarChart

try:
    # This will raise an exception - mismatched dimensions
    data = Data([10, 20, 30], ["A", "B"])
    chart = BarChart(data)
    chart.draw()
except Exception as e:
    print(f"Error creating chart: {e}")

try:
    # This will raise an exception - empty data
    data = Data([], [])
    chart = BarChart(data)
    chart.draw()
except Exception as e:
    print(f"Error with empty data: {e}")
```

## Best Practices

### 1. Choose the Right Chart Type

- **Bar Chart**: Comparing categories or values
- **Stacked Chart**: Showing parts of a whole
- **Vertical Chart**: Time series or many categories
- **Histogram**: Distribution of continuous data

### 2. Use Appropriate Colors

```python
# Good: Different colors for different series
args = Args(colors=[Colors.Blue, Colors.Green, Colors.Red])

# Good: Single color for single series
args = Args(colors=[Colors.Blue])

# Avoid: Too many similar colors
```

### 3. Format Values Appropriately

```python
# For percentages
args = Args(percentage=True, format="{:<3.0f}", suffix="%")

# For currency
args = Args(format="{:<6.2f}", suffix=" USD")

# For large numbers
args = Args(suffix="K", format="{:<5.0f}")  # Use K, M, etc.
```

### 4. Set Appropriate Width

```python
# Narrow for simple data
args = Args(width=30)

# Wide for detailed data
args = Args(width=80)

# Consider terminal width limitations
```

## API Reference

- **[Data Class](data-class.md)** - Data handling and normalization
- **[Chart Classes](chart-classes.md)** - All available chart types
- **[Args Class](args-class.md)** - Configuration options

## Examples Repository

For more examples and use cases, see the test files in the repository:
- Basic usage examples
- Complex multi-series charts
- Real-world data scenarios
- Integration patterns

## Contributing

If you find issues or want to contribute improvements to the API documentation, please visit the [GitHub repository](https://github.com/mkaz/termgraph).