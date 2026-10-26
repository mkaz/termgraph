"""This module allows drawing basic graphs in the terminal."""

# termgraph.py - draw basic graphs on terminal
# https://github.com/mkaz/termgraph

# Import all classes from their dedicated files to maintain backward compatibility
from .args import Args
from .chart import (
    BarChart,
    Chart,
    Colors,
    HistogramChart,
    HorizontalChart,
    StackedChart,
)
from .data import Data

# Re-export everything to maintain existing API
__all__ = ['Args', 'BarChart', 'Chart', 'Colors', 'Data', 'HistogramChart', 'HorizontalChart', 'StackedChart']
