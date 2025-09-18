# Data Class API Documentation

The `Data` class is the core data container for termgraph charts. It handles data validation, normalization, and provides methods for working with both flat and nested data structures.

## Constructor

```python
from termgraph import Data

# Basic usage
data = Data(data=[10, 20, 30, 40], labels=["Q1", "Q2", "Q3", "Q4"])

# With categories for multi-series data
data = Data(
    data=[[10, 15], [20, 25], [30, 35], [40, 45]],
    labels=["Q1", "Q2", "Q3", "Q4"],
    categories=["Product A", "Product B"]
)
```

### Parameters

- **data** (list): Required. The numeric data to be graphed. Can be:
  - Flat list: `[10, 20, 30, 40]`
  - Nested list: `[[10, 15], [20, 25], [30, 35]]`
- **labels** (list[str]): Required. Labels for each data point/row
- **categories** (list[str], optional): Category names for multi-series data

### Validation

The constructor validates that:
- Both `data` and `labels` are provided
- Data and labels have the same length
- For nested data, all inner lists have consistent dimensions

## Methods

### Data Statistics

#### `find_min() -> Union[int, float]`
Returns the minimum value in the dataset.

```python
# Flat data
data = Data([10, 5, 30, 15], ["A", "B", "C", "D"])
print(data.find_min())  # Output: 5

# Nested data
data = Data([[10, 5], [30, 15], [20, 25]], ["X", "Y", "Z"])
print(data.find_min())  # Output: 5
```

#### `find_max() -> Union[int, float]`
Returns the maximum value in the dataset.

```python
# Flat data
data = Data([10, 5, 30, 15], ["A", "B", "C", "D"])
print(data.find_max())  # Output: 30

# Nested data
data = Data([[10, 5], [30, 15], [20, 25]], ["X", "Y", "Z"])
print(data.find_max())  # Output: 30
```

### Label Methods

#### `find_min_label_length() -> int`
Returns the length of the shortest label.

```python
data = Data([10, 20, 30], ["A", "BB", "CCC"])
print(data.find_min_label_length())  # Output: 1
```

#### `find_max_label_length() -> int`
Returns the length of the longest label.

```python
data = Data([10, 20, 30], ["A", "BB", "CCC"])
print(data.find_max_label_length())  # Output: 3
```

### Data Normalization

#### `normalize(width: int) -> list`
Normalizes data values to fit within the specified width for chart rendering.

```python
# Flat data normalization
data = Data([10, 20, 30, 40], ["Q1", "Q2", "Q3", "Q4"])
normalized = data.normalize(50)  # Normalize to 50 character width
print(normalized)  # [12.5, 25.0, 37.5, 50.0]

# Nested data normalization
data = Data([[10, 15], [20, 25], [30, 35]], ["X", "Y", "Z"])
normalized = data.normalize(40)
print(normalized)  # [[11.43, 17.14], [22.86, 28.57], [34.29, 40.0]]
```

The normalize method:
- Handles negative values by offsetting all data
- Scales values proportionally to the target width
- Preserves relative relationships between data points
- Works with both flat and nested data structures

## Properties

### `data`
The raw data provided during initialization.

### `labels`
The labels for each data row/point.

### `categories`
Category names for multi-series data (empty list if not provided).

### `dims`
Tuple representing the dimensions of the data structure.

```python
# Flat data
data = Data([10, 20, 30], ["A", "B", "C"])
print(data.dims)  # (3,)

# Nested data
data = Data([[10, 15], [20, 25]], ["X", "Y"])
print(data.dims)  # (2, 2)
```

## Examples

### Basic Flat Data

```python
from termgraph import Data

# Simple sales data
sales_data = Data(
    data=[150, 230, 180, 290, 210],
    labels=["Jan", "Feb", "Mar", "Apr", "May"]
)

print(f"Min sales: {sales_data.find_min()}")  # Min sales: 150
print(f"Max sales: {sales_data.find_max()}")  # Max sales: 290
print(f"Data: {sales_data}")
```

### Multi-Series Data with Categories

```python
from termgraph import Data

# Quarterly sales for two products
quarterly_data = Data(
    data=[
        [120, 80],   # Q1: Product A, Product B
        [150, 95],   # Q2: Product A, Product B
        [180, 110],  # Q3: Product A, Product B
        [200, 125]   # Q4: Product A, Product B
    ],
    labels=["Q1", "Q2", "Q3", "Q4"],
    categories=["Product A", "Product B"]
)

print(f"Dimensions: {quarterly_data.dims}")  # (4, 2)
print(f"Categories: {quarterly_data.categories}")
```

### Working with Negative Values

```python
from termgraph import Data

# Profit/Loss data with negative values
pnl_data = Data(
    data=[-50, 30, -20, 80, 45],
    labels=["Jan", "Feb", "Mar", "Apr", "May"]
)

# Normalization handles negative values automatically
normalized = pnl_data.normalize(40)
print(f"Normalized data: {normalized}")
```

### Data Validation Examples

```python
from termgraph import Data

# These will raise exceptions:
try:
    # Missing labels
    Data([10, 20, 30])
except Exception as e:
    print(f"Error: {e}")

try:
    # Mismatched dimensions
    Data([10, 20], ["A", "B", "C"])
except Exception as e:
    print(f"Error: {e}")

try:
    # Inconsistent nested structure
    Data([[10, 20], [30]], ["A", "B"])
except Exception as e:
    print(f"Error: {e}")
```

## String Representation

The `Data` class provides a tabular string representation:

```python
data = Data(
    data=[[100, 150], [200, 250], [300, 350]],
    labels=["Product 1", "Product 2", "Product 3"],
    categories=["Sales", "Revenue"]
)

print(data)
```

Output:
```
    Labels | Data
-----------|---------------
 Product 1 | (Sales) 100
           | (Revenue) 150
           |
 Product 2 | (Sales) 200
           | (Revenue) 250
           |
 Product 3 | (Sales) 300
           | (Revenue) 350
           |
```

## Integration with Charts

The `Data` class is designed to work seamlessly with all chart types:

```python
from termgraph import Data, BarChart, Args

# Create data
data = Data([45, 32, 78, 56, 23], ["A", "B", "C", "D", "E"])

# Create chart with custom arguments
args = Args(width=60, colors=["red"])
chart = BarChart(data, args)

# Draw the chart
chart.draw()
```

For more examples of using Data with different chart types, see the [Chart Classes Documentation](chart-classes.md).