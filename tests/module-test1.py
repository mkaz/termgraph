from termgraph.data import Data
from termgraph.args import Args
from termgraph.chart import BarChart, StackedChart, Colors

# Original Bar Chart
print("--- Bar Chart ---")
data = Data([[765, 787], [781, 769]], ["6th G", "7th G"], ["Boys", "Girls"])
chart = BarChart(
    data,
    Args(
        title="Total Marks Per Class",
        colors=[Colors.Red, Colors.Magenta],
        space_between=True,
    ),
)
chart.draw()

# Stacked Chart
print("\n--- Stacked Chart ---")
stacked_chart = StackedChart(
    data,
    Args(
        title="Total Marks Per Class (Stacked)",
        colors=[Colors.Green, Colors.Blue],
        space_between=True,
    ),
)
stacked_chart.draw()