__all__ = ["Args", "BarChart", "Chart", "Colors", "Data", "HistogramChart", "HorizontalChart", "StackedChart", "VerticalChart", "main"]

def __getattr__(name):
    if name == "main":
        from .termgraph import main
        return main
    elif name in ["Data", "Args", "Colors", "Chart", "HorizontalChart", "BarChart", "StackedChart", "VerticalChart", "HistogramChart"]:
        # Import from the new modular structure
        if name == "Data":
            from .data import Data
            return Data
        elif name == "Args":
            from .args import Args
            return Args
        elif name in ["Colors", "Chart", "HorizontalChart", "BarChart", "StackedChart", "VerticalChart", "HistogramChart"]:
            from .chart import (
                BarChart,
                Chart,
                Colors,
                HistogramChart,
                HorizontalChart,
                StackedChart,
                VerticalChart,
            )
            return {"Colors": Colors, "Chart": Chart, "HorizontalChart": HorizontalChart, "BarChart": BarChart, "StackedChart": StackedChart, "VerticalChart": VerticalChart, "HistogramChart": HistogramChart}[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")