# Chart Classes API Documentation

Termgraph provides several chart classes for different visualization needs. All chart classes inherit from the base `Chart` class and work with `Data` and `Args` objects.

## Base Classes

### Chart (Abstract Base Class)

The `Chart` class is the foundation for all chart types.

```python
from termgraph import Chart, Data, Args

# Chart is abstract - use specific chart implementations
# chart = Chart(data, args)  # Don't do this
```

**Constructor Parameters:**
- **data** (Data): Data object containing the values and labels
- **args** (Args): Configuration arguments for the chart

**Methods:**
- `draw()`: Abstract method implemented by subclasses to render the chart

### Colors Class

Provides predefined color constants for chart styling.

```python
from termgraph import Colors

# Available colors
Colors.Black    # Black color code
Colors.Red      # Red color code
Colors.Green    # Green color code
Colors.Yellow   # Yellow color code
Colors.Blue     # Blue color code
Colors.Magenta  # Magenta color code
Colors.Cyan     # Cyan color code
```

## Chart Types

### BarChart

Creates horizontal bar charts. Supports both single and multi-series data.

```python
from termgraph import Data, BarChart, Args

# Single series bar chart
data = Data([23, 45, 56, 78, 32], ["A", "B", "C", "D", "E"])
chart = BarChart(data)
chart.draw()
```

**Features:**
- Horizontal bars with customizable width
- Multi-series support with categories
- Different scaling options
- Color support
- Value formatting

#### Single Series Example

```python
from termgraph import Data, BarChart, Args, Colors

# Simple bar chart
data = Data(
    data=[150, 230, 180, 290, 210],
    labels=["Jan", "Feb", "Mar", "Apr", "May"]
)

args = Args(
    width=50,
    title="Monthly Sales",
    colors=[Colors.Green],
    suffix=" units"
)

chart = BarChart(data, args)
chart.draw()
```

Output:
```
# Monthly Sales

Jan  : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 150.00 units
Feb  : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 230.00 units
Mar  : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 180.00 units
Apr  : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 290.00 units
May  : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 210.00 units
```

#### Multi-Series Example

```python
from termgraph import Data, BarChart, Args, Colors

# Multi-series bar chart
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
    width=40,
    title="Quarterly Sales by Product",
    colors=[Colors.Blue, Colors.Red],
    space_between=True
)

chart = BarChart(data, args)
chart.draw()
```

Output:
```
# Quarterly Sales by Product

▇ Product A  ▇ Product B

Q1: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 120.00
    ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 80.00

Q2: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 150.00
    ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 95.00

Q3: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 180.00
    ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 110.00

Q4: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 200.00
    ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 125.00
```

#### Different Scale Example

```python
from termgraph import Data, BarChart, Args, Colors

# Different scales for each series
data = Data(
    data=[
        [1200, 45],    # Revenue (thousands), Satisfaction (%)
        [1500, 52],
        [1800, 48],
        [2000, 58]
    ],
    labels=["Q1", "Q2", "Q3", "Q4"],
    categories=["Revenue ($K)", "Satisfaction (%)"]
)

args = Args(
    width=30,
    different_scale=True,  # Each series uses its own scale
    colors=[Colors.Green, Colors.Yellow],
    title="Revenue vs Customer Satisfaction"
)

chart = BarChart(data, args)
chart.draw()
```

### StackedChart

Creates stacked bar charts where multiple values are stacked on top of each other.

```python
from termgraph import Data, StackedChart, Args, Colors

# Stacked bar chart
data = Data(
    data=[
        [30, 20, 10],  # Desktop, Mobile, Tablet
        [25, 30, 15],
        [20, 35, 20],
        [15, 40, 25]
    ],
    labels=["Q1", "Q2", "Q3", "Q4"],
    categories=["Desktop", "Mobile", "Tablet"]
)

args = Args(
    width=50,
    title="Traffic Sources by Quarter",
    colors=[Colors.Blue, Colors.Green, Colors.Yellow]
)

chart = StackedChart(data, args)
chart.draw()
```

Output:
```
# Traffic Sources by Quarter

▇ Desktop  ▇ Mobile  ▇ Tablet

Q1: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 60.00
Q2: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 70.00
Q3: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 75.00
Q4: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 80.00
```

### VerticalChart

Creates vertical bar charts (column charts).

```python
from termgraph import Data, VerticalChart, Args, Colors

# Vertical bar chart
data = Data(
    data=[23, 45, 56, 78, 32],
    labels=["A", "B", "C", "D", "E"]
)

args = Args(
    width=40,
    title="Vertical Chart Example",
    colors=[Colors.Cyan]
)

chart = VerticalChart(data, args)
chart.draw()
```

Output:
```
# Vertical Chart Example

    ▇
    ▇
    ▇ ▇
    ▇ ▇
▇ ▇ ▇ ▇
▇ ▇ ▇ ▇
▇ ▇ ▇ ▇ ▇
▇ ▇ ▇ ▇ ▇
▇ ▇ ▇ ▇ ▇
----------------
23.00  45.00  56.00  78.00  32.00
----------------
A  B  C  D  E
```

### HistogramChart

Creates histogram charts that bin continuous data into ranges.

```python
from termgraph import Data, HistogramChart, Args, Colors

# Histogram chart
# Note: For histograms, data should be the raw values you want to bin
data = Data(
    data=[[12.5, 15.3, 18.7, 22.1, 25.6, 28.9, 32.4, 35.8, 38.2, 41.7]],
    labels=["Temperature Readings"]
)

args = Args(
    width=40,
    bins=5,  # Number of bins
    title="Temperature Distribution",
    colors=[Colors.Red]
)

chart = HistogramChart(data, args)
chart.draw()
```

Output:
```
# Temperature Distribution

12.0 – 18.0: ▇▇▇▇▇▇▇▇▇▇▇▇ 3.00
18.0 – 24.0: ▇▇▇▇▇▇▇▇ 2.00
24.0 – 30.0: ▇▇▇▇▇▇▇▇ 2.00
30.0 – 36.0: ▇▇▇▇▇▇▇▇ 2.00
36.0 – 42.0: ▇▇▇▇▇▇▇▇▇▇▇▇ 3.00
```

## Configuration Options

All chart classes accept an `Args` object for configuration. See [Args Class Documentation](args-class.md) for complete details.

### Common Options

```python
from termgraph import Args, Colors

args = Args(
    width=50,              # Chart width in characters
    title="My Chart",      # Chart title
    colors=[Colors.Blue],  # Colors for series
    suffix=" units",       # Value suffix
    format="{:<6.1f}",    # Value formatting
    no_labels=False,       # Hide labels
    no_values=False,       # Hide values
    space_between=True     # Add space between bars
)
```

### Chart-Specific Options

```python
# Bar chart specific
args = Args(
    different_scale=True,  # Use different scales for multi-series
    label_before=True      # Show labels before bars
)

# Histogram specific
args = Args(
    bins=10               # Number of histogram bins
)

# Vertical chart specific
args = Args(
    vertical=True         # Enable vertical mode
)
```

## Advanced Examples

### Complex Multi-Series Chart

```python
from termgraph import Data, BarChart, Args, Colors

# Sales data across multiple regions and quarters
data = Data(
    data=[
        [150, 120, 90],   # Q1: North, South, West
        [180, 140, 110],  # Q2: North, South, West
        [200, 160, 130],  # Q3: North, South, West
        [220, 180, 150]   # Q4: North, South, West
    ],
    labels=["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023"],
    categories=["North Region", "South Region", "West Region"]
)

args = Args(
    width=60,
    title="Regional Sales Performance",
    colors=[Colors.Blue, Colors.Green, Colors.Yellow],
    space_between=True,
    suffix="K",
    format="{:<5.0f}"
)

chart = BarChart(data, args)
chart.draw()
```

### Percentage Data with Custom Formatting

```python
from termgraph import Data, BarChart, Args, Colors

# Percentage completion data
data = Data(
    data=[0.65, 0.80, 0.45, 0.92, 0.73],
    labels=["Project A", "Project B", "Project C", "Project D", "Project E"]
)

args = Args(
    width=40,
    title="Project Completion Status",
    colors=[Colors.Green],
    percentage=True,      # Format as percentages
    format="{:<4.0f}",
    suffix="%"
)

chart = BarChart(data, args)
chart.draw()
```

### Negative Values Handling

```python
from termgraph import Data, BarChart, Args, Colors

# Profit/Loss data with negative values
data = Data(
    data=[-50, 30, -20, 80, 45, -15],
    labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
)

args = Args(
    width=50,
    title="Monthly P&L",
    colors=[Colors.Red],  # Single color for all bars
    suffix="K",
    format="{:<+6.0f}"    # Show + for positive values
)

chart = BarChart(data, args)
chart.draw()
```

## Error Handling

Charts will handle common data issues gracefully:

```python
from termgraph import Data, BarChart

try:
    # Empty data
    data = Data([], [])
    chart = BarChart(data)
    chart.draw()
except Exception as e:
    print(f"Error: {e}")

try:
    # Mismatched dimensions
    data = Data([10, 20], ["A"])
    chart = BarChart(data)
    chart.draw()
except Exception as e:
    print(f"Error: {e}")
```

## Integration Example

Complete example showing how to use multiple chart types with the same data:

```python
from termgraph import Data, BarChart, StackedChart, VerticalChart, Args, Colors

# Sample data
data = Data(
    data=[[30, 45], [25, 50], [40, 35], [35, 40]],
    labels=["Q1", "Q2", "Q3", "Q4"],
    categories=["Revenue", "Expenses"]
)

args = Args(
    width=40,
    title="Financial Data",
    colors=[Colors.Green, Colors.Red]
)

# Different chart types with same data
print("=== Bar Chart ===")
bar_chart = BarChart(data, args)
bar_chart.draw()

print("\n=== Stacked Chart ===")
stacked_chart = StackedChart(data, args)
stacked_chart.draw()

print("\n=== Vertical Chart ===")
vertical_chart = VerticalChart(data, args)
vertical_chart.draw()
```

For more information about data preparation, see [Data Class Documentation](data-class.md).
For configuration options, see [Args Class Documentation](args-class.md).