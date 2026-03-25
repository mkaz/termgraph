from termgraph.data import Data
from termgraph.args import Args
from termgraph.chart import BarChart, StackedChart, VerticalChart, HistogramChart

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

def test_custom_tick_appears_in_output():
    labels = ["A", "B"]
    data_values = [[10], [20]]
    data = Data(data_values, labels)
    args = Args(custom_tick="😀")

    def test(ChartType):
        chart = ChartType(data, args)

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            chart.draw()
        output = f.getvalue()

        # Assert that the custom tick appears in the output
        assert "😀" in output

    run_for_all_charts(test, with_histo=True)

def run_for_all_charts(func, with_histo=False):
    """ Runs a test function with all chart types, HistogramChart is optional as data format works differently there"""
    charts = [BarChart, StackedChart, VerticalChart]

    if with_histo:
        charts.append(HistogramChart)

    for chart in charts:
        print(f"running {func.__name__} for {chart.__name__}")
        func(chart)

def test_format_default():
    labels = ["A", "B"]
    data_values = [[10000], [20000]]
    data = Data(data_values, labels)
    args = Args()

    def test(ChartType):
        chart = ChartType(data, args)

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            chart.draw()
        output = f.getvalue()

        # values are default formatted and converted to readable
        assert "10.00K" in output
        assert "20.00K" in output

    run_for_all_charts(test)

def test_format_no_readable():
    labels = ["A", "B"]
    data_values = [[10000], [20000]]
    data = Data(data_values, labels)
    args = Args(no_readable=True)

    def test(ChartType):
        chart = ChartType(data, args)

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            chart.draw()
        output = f.getvalue()

        # values are not converted to readable format
        assert "10000" in output
        assert "20000" in output
        assert "10.00K" not in output
        assert "20.00K" not in output

    run_for_all_charts(test)

def test_format_percentage():
    labels = ["A", "B"]
    data_values = [[0.1], [0.275]]
    data = Data(data_values, labels)
    args = Args(percentage=True)

    def test(ChartType):
        chart = ChartType(data, args)

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            chart.draw()
        output = f.getvalue()

        # values are converted to percentage
        assert "10.00%" in output
        assert "27.50%" in output

    run_for_all_charts(test)

def test_format_custom_format():
    labels = ["A", "B"]
    data_values = [[10.375], [400.00000]]
    data = Data(data_values, labels)
    args = Args(format="{:3.1f}")

    def test(ChartType):
        chart = ChartType(data, args)

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            chart.draw()
        output = f.getvalue()

        # values are formatted with custom format
        assert "10.4" in output
        assert "400.0" in output

    run_for_all_charts(test)

def test_format_no_values():
    labels = ["A", "B"]
    data_values = [[10], [20]]
    data = Data(data_values, labels)
    args = Args(no_values=True)

    def test(ChartType):
        chart = ChartType(data, args)

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            chart.draw()
        output = f.getvalue()

        # values are not printed at all
        assert "10" not in output
        assert "20" not in output

    run_for_all_charts(test)

def test_format_suffix():
    labels = ["A", "B"]
    data_values = [[10], [20]]
    data = Data(data_values, labels)
    args = Args(suffix="suf")

    def test(ChartType):
        chart = ChartType(data, args)

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            chart.draw()
        output = f.getvalue()

        # values are suffixed
        assert "10.00suf" in output
        assert "20.00suf" in output

    run_for_all_charts(test)

def test_no_values_with_suffix():
    labels = ["A", "B"]
    data_values = [[10], [20]]
    data = Data(data_values, labels)
    args = Args(no_values=True, suffix="suf")

    def test(ChartType):
        chart = ChartType(data, args)

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            chart.draw()
        output = f.getvalue()

        # suffix not printed with no_values
        assert "suf" not in output
        assert "10" not in output
        assert "20" not in output

    run_for_all_charts(test)