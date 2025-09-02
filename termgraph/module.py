"""This module allows drawing basic graphs in the terminal."""

# termgraph.py - draw basic graphs on terminal
# https://github.com/mkaz/termgraph

# Import all classes from their dedicated files to maintain backward compatibility
from .data import Data
from .args import Args
from .chart import Colors, Chart, HorizontalChart, BarChart, StackedChart, HistogramChart

# Re-export everything to maintain existing API
__all__ = ['Data', 'Args', 'Colors', 'Chart', 'HorizontalChart', 'BarChart', 'StackedChart', 'HistogramChart']
