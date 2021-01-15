from oop import Data, BarChart, Args, Colors

data = Data([[128, 228], [332, 42]], ["6th G", "7th G"])
chart = BarChart(data, Args(colors=[Colors.Red, Colors.Magenta], space_between=True))

chart.draw()
