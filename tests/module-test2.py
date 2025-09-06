from termgraph.data import Data
from termgraph.args import Args
from termgraph.chart import BarChart, HistogramChart, Colors

# Original Bar Chart
print("--- Simple Bar Chart ---")
data = Data([[10], [50], [80], [100]], ["Label 1", "Label 2", "Label 3", "Label 4"])
chart = BarChart(
    data,
    Args(
        colors=[Colors.Red],
        suffix="%",
    ),
)
chart.draw()

# Different Scale Chart
print("\n--- Different Scale Chart ---")
diff_scale_data = Data([[10, 1000], [20, 2000], [30, 3000]], ["A", "B", "C"], ["Category 1", "Category 2"])
diff_scale_chart = BarChart(
    diff_scale_data,
    Args(
        title="Different Scale Example",
        different_scale=True,
        colors=[Colors.Cyan, Colors.Yellow]
    )
)
diff_scale_chart.draw()

# Histogram
print("\n--- Histogram ---")
hist_data_values = [[1], [2], [2], [3], [3], [3], [4], [4], [4], [4], [5], [5], [5], [5], [5]]
hist_data = Data(hist_data_values, [str(i) for i in range(len(hist_data_values))])
histogram = HistogramChart(
    hist_data,
    Args(
        title="Histogram Example",
        colors=[Colors.Green],
        bins=4
    )
)
histogram.draw()
