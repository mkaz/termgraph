from termgraph.module import Data, BarChart, Args, Colors

data = Data([[10], [50], [80], [100]], ["Label 1", "Label 2", "Label 3", "Label 4"])
chart = BarChart(
    data,
    Args(
        colors=[Colors.Red],
        suffix="%",
    ),
)

chart.draw()