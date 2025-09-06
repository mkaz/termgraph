import pytest
from termgraph.data import Data
from termgraph.args import Args
from termgraph.chart import BarChart, VerticalChart

def test_barchart_draws_correctly():
    labels = ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    data_values = [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
    
    data = Data(data_values, labels)
    args = Args(width=50, no_labels=False, suffix="", no_values=False)
    
    chart = BarChart(data, args)
    
    # Capture the output of the draw method
    import io
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        chart.draw()
    output = f.getvalue()
    
    # Assert that the output contains the expected elements
    assert "2007: " in output
    assert "183.32" in output
    assert "2014: " in output
    assert "1.00" in output

def test_verticalchart_draws_correctly():
    labels = ["A", "B"]
    data_values = [[10], [20]]
    
    data = Data(data_values, labels)
    args = Args(width=10)
    
    chart = VerticalChart(data, args)
    
    import io
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        chart.draw()
    output = f.getvalue()
    
    # Assert that the output contains the expected elements
    assert "▇" in output
    assert "A" in output
    assert "B" in output
    assert "10" in output
    assert "20" in output
