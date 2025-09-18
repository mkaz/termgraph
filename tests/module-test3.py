from termgraph import Data, Args, BarChart

# Create data
data = Data(
    labels=["Q1", "Q2", "Q3", "Q4"],
    data=[10, 20, 40, 26],
)

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
