import pytest

from termgraph.args import Args
from termgraph.chart import BarChart, StackedChart, VerticalChart
from termgraph.data import Data


@pytest.mark.parametrize("chart_type", [BarChart, StackedChart, VerticalChart])
@pytest.mark.parametrize("options", [{}, {"no_values": True}, {"no_labels": True}])
def test_drawing_chart_again_preserves_output(capsys, chart_type, options):
    data = Data([[3], [5]], ["A", "B"])
    chart = chart_type(data, Args(width=5, **options))

    chart.draw()
    expected = capsys.readouterr().out
    assert "▇" in expected

    for _ in range(2):
        chart.draw()
        assert capsys.readouterr().out == expected
