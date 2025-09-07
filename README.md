# Termgraph

A command-line tool and Python library that draws basic graphs in the terminal.

Graph types supported:
- Bar Graphs
- Color charts  
- Multi-variable
- Stacked charts
- Histograms
- Horizontal or Vertical
- Calendar heatmaps
- Emoji!

## Quick Start

### Command Line Usage

```
termgraph data/ex1.dat

# Reading data from data/ex1.dat

2007: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 183.32
2008: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 231.23
2009: ▇ 16.43
2010: ▇▇▇▇ 50.21
2011: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 508.97
2012: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 212.05
2014: ▏ 1.00
```

### Python Module Usage

```python
from termgraph import Data, Args, BarChart

# Create data
data = Data([[10], [25], [50], [40]], ["Q1", "Q2", "Q3", "Q4"])

# Configure chart options  
args = Args(
    title="Quarterly Sales",
    width=50,
    format="{:.0f}",
    suffix="K"
)

# Create and display chart
chart = BarChart(data, args)
chart.draw()
```

Output:
```
# Quarterly Sales

Q1: ▇▇▇▇▇▇▇▇▇▇ 10K
Q2: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 25K  
Q3: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 50K
Q4: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 40K
```

For stacked charts with categories:

```python  
from termgraph import Data, Args, StackedChart

# Multi-category data: [Desktop, Mobile] for each quarter
data = Data([[20, 15], [25, 30], [35, 40], [30, 35]], 
           ["Q1", "Q2", "Q3", "Q4"], 
           categories=["Desktop", "Mobile"])

args = Args(title="Sales by Platform", width=50, suffix="K")
chart = StackedChart(data, args) 
chart.draw()
```

## More Examples

### Custom Tick Marks

An example using emoji as custom tick:

```
termgraph data/ex1.dat --custom-tick "🏃" --width 20 --title "Running Data"

# Running Data

2007: 🏃🏃🏃🏃🏃🏃🏃 183.32
2008: 🏃🏃🏃🏃🏃🏃🏃🏃🏃 231.23
2009:  16.43
2010: 🏃 50.21
2011: 🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃 508.97
2012: 🏃🏃🏃🏃🏃🏃🏃🏃 212.05
2014:  1.00

```


An example using stdin and emoji:

```
echo "Label,3,9,1" | termgraph --custom-tick "😀" --no-label


😀😀😀 3.00
😀😀😀😀😀😀😀😀😀 9.00
😀 1.00

```

### Color Charts

Most results can be copied and pasted wherever you like, since they use standard block characters. However the color charts will not show, since they use terminal escape codes for color. A couple images to show color examples:

```
termgraph data/ex4.dat --color {blue,red}
```

<img src="https://user-images.githubusercontent.com/45363/43405623-1a2cc4d4-93cf-11e8-8c96-b7134d8986a2.png" width="655" alt="Multi variable bar chart with colors" />

```
termgraph data/ex7.dat --color {yellow,magenta} --stacked --title "Stacked Data"
```

<img src="https://user-images.githubusercontent.com/45363/43405624-1a4a821c-93cf-11e8-84f3-f45c65b7ca98.png" width="686" alt="Multi variable stacked bar chart with colors" />

### Calendar Heatmap

Calendar Heatmap, expects first column to be date in yyyy-mm-dd

```
termgraph --calendar --start-dt 2017-07-01 data/cal.dat
```

<img src="https://user-images.githubusercontent.com/45363/43405619-1a15998a-93cf-11e8-8a3f-abfd2f6104a5.png" width="596" alt="Calendar Heatmap" />



## Usage

#### Command Line Interface

* Create data file with two columns either comma or space separated.
  The first column is your labels, the second column is a numeric data

* termgraph [datafile]

* Help: termgraph -h

#### Command Line Arguments

```
usage: termgraph [-h] [options] [filename]

draw basic graphs on terminal

positional arguments:
  filename              data file name (comma or space separated). Defaults to stdin.

options:
  -h, --help            show this help message and exit
  --title TITLE         Title of graph
  --width WIDTH         width of graph in characters default:50
  --format FORMAT       format specifier to use.
  --suffix SUFFIX       string to add as a suffix to all data points.
  --no-labels           Do not print the label column
  --no-values           Do not print the values at end
  --space-between       Print a new line after every field
  --color [COLOR ...]   Graph bar color( s )
  --vertical            Vertical graph
  --stacked             Stacked bar graph
  --histogram           Histogram
  --bins BINS           Bins of Histogram
  --different-scale     Categories have different scales.
  --calendar            Calendar Heatmap chart
  --start-dt START_DT   Start date for Calendar chart
  --custom-tick CUSTOM_TICK
                        Custom tick mark, emoji approved
  --delim DELIM         Custom delimiter, default , or space
  --verbose             Verbose output, helpful for debugging
  --label-before        Display the values before the bars
  --no-readable         Disable the readable numbers
  --percentage          Display the number in percentage
  --version             Display version and exit
```

### Python API

All chart types are available as classes:

```python
from termgraph import (
    Data, Args, 
    BarChart, StackedChart, VerticalChart, HistogramChart
)

# Basic setup
data = Data([[10], [20]], ["A", "B"])  
args = Args(title="My Chart")

# Choose your chart type
chart = BarChart(data, args)        # Horizontal bars
# chart = StackedChart(data, args)  # Stacked bars  
# chart = VerticalChart(data, args) # Vertical bars
# chart = HistogramChart(data, args) # Histogram

chart.draw()
```

Available Args options:
- `title`: Chart title
- `width`: Width in characters (default: 50)  
- `format`: Number format string (default: "{:<5.2f}")
- `suffix`: Add suffix to all values
- `no_labels`: Don't show labels
- `no_values`: Don't show values
- `colors`: List of color names

## Background

I wanted a quick way to visualize data stored in a simple text file. I initially created some scripts in R that generated graphs but this was a two step process of creating the graph and then opening the generated graph.

After seeing [command-line sparklines](https://github.com/holman/spark) I figured I could do the same thing using block characters for bar charts.

### Contribute

All contributions are welcome! For detailed information about the project structure, development workflow, and contribution guidelines, please see [CONTRIBUTING.md](CONTRIBUTING.md).

**Quick Start:**
- 🐛 **Bug reports** and 🚀 **feature requests**: Use [GitHub Issues](https://github.com/mkaz/termgraph/issues)
- 🔧 **Code contributions**: See our [development workflow](CONTRIBUTING.md#development-workflow)  
- 📚 **Documentation**: Help improve our guides and examples

**Code Quality:** We use `ruff` for linting and formatting, `mypy` for type checking, and maintain comprehensive test coverage.

Thanks to all the [contributors](https://github.com/mkaz/termgraph/graphs/contributors)!


### License

MIT License, see [LICENSE.txt](LICENSE.txt)
