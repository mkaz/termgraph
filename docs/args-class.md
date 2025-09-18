# Args Class API Documentation

The `Args` class manages chart configuration options and arguments. It provides a centralized way to control chart appearance, behavior, and formatting.

## Constructor

```python
from termgraph import Args

# Default args
args = Args()

# Custom args
args = Args(
    width=60,
    title="My Chart",
    colors=["red", "blue"],
    suffix=" units"
)
```

### Parameters

All parameters are optional and provided as keyword arguments. If not specified, default values are used.

## Configuration Options

### Chart Dimensions

#### `width` (int, default: 50)
The width of the chart in characters.

```python
args = Args(width=80)  # Wide chart
args = Args(width=30)  # Narrow chart
```

### Chart Appearance

#### `title` (str, default: None)
Chart title displayed at the top.

```python
args = Args(title="Monthly Sales Report")
```

#### `colors` (list, default: None)
List of color codes for chart series. Use color names or ANSI codes.

```python
from termgraph import Colors

args = Args(colors=[Colors.Blue, Colors.Green, Colors.Red])
# Or use color names
args = Args(colors=["blue", "green", "red"])
```

Available color constants:
- `Colors.Black`
- `Colors.Red`
- `Colors.Green`
- `Colors.Yellow`
- `Colors.Blue`
- `Colors.Magenta`
- `Colors.Cyan`

#### `custom_tick` (str, default: "")
Custom character to use for chart bars instead of the default block character.

```python
args = Args(custom_tick="*")   # Use asterisks
args = Args(custom_tick="=")   # Use equals signs
args = Args(custom_tick="█")   # Use solid blocks
```

### Value Formatting

#### `format` (str, default: "{:<5.2f}")
Python format string for numeric values.

```python
args = Args(format="{:<6.1f}")    # 6 chars wide, 1 decimal
args = Args(format="{:>8.0f}")    # Right-aligned, no decimals
args = Args(format="{:+.2f}")     # Always show sign
```

#### `suffix` (str, default: "")
Text appended to each value.

```python
args = Args(suffix=" units")      # Append units
args = Args(suffix="K")           # Thousands
args = Args(suffix="$")           # Currency
```

#### `percentage` (bool, default: False)
Format values as percentages.

```python
# Convert 0.75 to 75%
args = Args(percentage=True)
```

#### `no_readable` (bool, default: False)
Disable automatic conversion of large numbers to readable format (e.g., 1000 → 1K).

```python
args = Args(no_readable=True)  # Show raw numbers
```

### Label and Value Display

#### `no_labels` (bool, default: False)
Hide row labels.

```python
args = Args(no_labels=True)  # Hide all labels
```

#### `no_values` (bool, default: False)
Hide numeric values next to bars.

```python
args = Args(no_values=True)  # Show only bars
```

#### `label_before` (bool, default: False)
Display labels before the bars instead of to the left with colons.

```python
args = Args(label_before=True)
# Changes "Label: ████" to "Label ████"
```

### Chart Layout

#### `space_between` (bool, default: False)
Add blank lines between chart rows.

```python
args = Args(space_between=True)  # More readable spacing
```

#### `vertical` (bool, default: False)
Create vertical/column charts instead of horizontal bars.

```python
args = Args(vertical=True)  # Column chart
```

### Multi-Series Options

#### `different_scale` (bool, default: False)
Use different scales for each data series in multi-series charts.

```python
# Useful when series have very different ranges
args = Args(different_scale=True)
```

#### `stacked` (bool, default: False)
Create stacked bar charts for multi-series data.

```python
args = Args(stacked=True)  # Stack series on top of each other
```

### Histogram Options

#### `histogram` (bool, default: False)
Enable histogram mode.

```python
args = Args(histogram=True, bins=10)
```

#### `bins` (int, default: 5)
Number of bins for histogram charts.

```python
args = Args(bins=8)   # 8 histogram bins
args = Args(bins=15)  # Fine-grained histogram
```

### Data Input Options

#### `filename` (str, default: "-")
Input filename (used by CLI, usually not needed for API usage).

#### `delim` (str, default: "")
Custom delimiter for data parsing.

### Calendar Options

#### `calendar` (bool, default: False)
Enable calendar heatmap mode.

#### `start_dt` (date, default: None)
Start date for calendar charts.

### Debugging

#### `verbose` (bool, default: False)
Enable verbose output for debugging.

```python
args = Args(verbose=True)  # Show debug information
```

## Methods

### `get_arg(arg: str) -> Union[int, str, bool, None]`
Get the value of a specific argument.

```python
args = Args(width=60, title="Test")

width = args.get_arg("width")    # Returns 60
title = args.get_arg("title")    # Returns "Test"
```

### `update_args(**kwargs) -> None`
Update multiple arguments after initialization.

```python
args = Args(width=50)
args.update_args(width=80, title="Updated Chart")
```

## Examples

### Basic Configuration

```python
from termgraph import Args, Colors

# Simple configuration
args = Args(
    width=50,
    title="Sales Data",
    colors=[Colors.Blue],
    suffix=" units"
)
```

### Advanced Formatting

```python
from termgraph import Args

# Detailed formatting options
args = Args(
    width=70,
    title="Financial Performance Q4 2023",
    format="{:>8.2f}",      # Right-aligned, 2 decimals
    suffix="K USD",         # Thousands of dollars
    space_between=True,     # Better readability
    no_readable=True        # Show exact numbers
)
```

### Multi-Series Configuration

```python
from termgraph import Args, Colors

# Multi-series with different colors
args = Args(
    width=60,
    title="Product Comparison",
    colors=[Colors.Green, Colors.Blue, Colors.Red],
    different_scale=False,  # Use same scale
    space_between=True
)
```

### Stacked Chart Configuration

```python
from termgraph import Args, Colors

# Stacked chart setup
args = Args(
    width=50,
    title="Market Share Evolution",
    colors=[Colors.Blue, Colors.Green, Colors.Yellow],
    stacked=True,
    format="{:<4.0f}",
    suffix="%"
)
```

### Histogram Configuration

```python
from termgraph import Args, Colors

# Histogram settings
args = Args(
    width=60,
    title="Data Distribution",
    histogram=True,
    bins=10,
    colors=[Colors.Cyan],
    format="{:<3.0f}"
)
```

### Minimal Bar Chart

```python
from termgraph import Args

# Clean, minimal appearance
args = Args(
    width=40,
    no_values=True,     # Hide numbers
    custom_tick="▓",    # Custom bar character
    colors=["green"]
)
```

### Percentage Chart

```python
from termgraph import Args, Colors

# Percentage display
args = Args(
    width=50,
    title="Completion Status",
    percentage=True,
    colors=[Colors.Green],
    format="{:<3.0f}",
    suffix="%"
)
```

### Vertical Chart Configuration

```python
from termgraph import Args, Colors

# Column chart setup
args = Args(
    width=30,
    title="Vertical Sales Chart",
    vertical=True,
    colors=[Colors.Blue],
    no_labels=False
)
```

## Default Values Reference

```python
# All default values
default_args = {
    "filename": "-",
    "title": None,
    "width": 50,
    "format": "{:<5.2f}",
    "suffix": "",
    "no_labels": False,
    "no_values": False,
    "space_between": False,
    "colors": None,
    "vertical": False,
    "stacked": False,
    "histogram": False,
    "bins": 5,
    "different_scale": False,
    "calendar": False,
    "start_dt": None,
    "custom_tick": "",
    "delim": "",
    "verbose": False,
    "label_before": False,
    "percentage": False,
    "no_readable": False,
}
```

## Error Handling

The Args class validates argument names:

```python
from termgraph import Args

try:
    # Invalid argument name
    args = Args(invalid_option=True)
except Exception as e:
    print(f"Error: {e}")  # "Invalid Argument: invalid_option"

try:
    # Invalid argument in get_arg
    args = Args()
    value = args.get_arg("nonexistent")
except Exception as e:
    print(f"Error: {e}")  # "Invalid Argument: nonexistent"
```

## Integration with Charts

The Args object is passed to chart constructors:

```python
from termgraph import Data, BarChart, Args, Colors

# Create data and args
data = Data([10, 20, 30], ["A", "B", "C"])
args = Args(
    width=40,
    title="Sample Chart",
    colors=[Colors.Green]
)

# Create and draw chart
chart = BarChart(data, args)
chart.draw()
```

For more information about chart types, see [Chart Classes Documentation](chart-classes.md).
For data preparation, see [Data Class Documentation](data-class.md).