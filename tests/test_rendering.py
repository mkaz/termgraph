from termgraph import termgraph as tg


def test_horiz_rows_yields_correct_values():
    labels = ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    data = [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
    normal_dat = [
        [17.94594168946985],
        [22.661771364450654],
        [1.5187904797527412],
        [4.843789987597693],
        [50.0],
        [20.77386459830305],
        [0.0],
    ]
    args = {
        "filename": "data/ex1.dat",
        "title": None,
        "width": 50,
        "format": "{:<5.2f}",
        "suffix": "",
        "no_labels": False,
        "color": None,
        "vertical": False,
        "stacked": False,
        "different_scale": False,
        "calendar": False,
        "start_dt": None,
        "custom_tick": "",
        "delim": "",
        "no_values": False,
        "verbose": False,
        "version": False,
    }
    colors = []

    rows = []
    for row in tg.horiz_rows(labels, data, normal_dat, args, colors):
        rows.append(row)

    assert rows == [
        (183.32, 17, 1.0, None, "2007: ", " 183.32", None),
        (231.23, 22, 1.0, None, "2008: ", " 231.23", None),
        (16.43, 1, 1.0, None, "2009: ", " 16.43", None),
        (50.21, 4, 1.0, None, "2010: ", " 50.21", None),
        (508.97, 50, 1.0, None, "2011: ", " 508.97", None),
        (212.05, 20, 1.0, None, "2012: ", " 212.05", None),
        (1.0, 0, 1.0, None, "2014: ", " 1.00 ", None),
    ]


def test_vertically_returns_correct_result():
    args = {
        "filename": "data/ex2.dat",
        "title": None,
        "width": 50,
        "format": "{:<5.2f}",
        "suffix": "",
        "no_labels": False,
        "color": None,
        "vertical": True,
        "stacked": False,
        "different_scale": False,
        "calendar": False,
        "start_dt": None,
        "custom_tick": "",
        "delim": "",
        "verbose": False,
        "version": False,
    }
    value = 2.0
    num_blocks = 2
    val_min = 2.0
    color = None
    result = tg.vertically(value, num_blocks, val_min, color, args)
    assert result == [("▇",), ("▇",)]


def test_percentage_flag_displays_values_as_percentages():
    """Test that percentage=True converts values to percentages (e.g., 1 -> 100%, 2 -> 200%)"""
    labels = ["1", "2", "3", "4", "5"]
    data = [[1], [2], [3], [4], [5]]
    normal_dat = [[10], [20], [30], [40], [50]]  # Normalized values
    args = {
        "suffix": "",
        "format": "{:.0f}",
        "percentage": True,  # This should convert values to percentages
    }
    colors = []

    rows = []
    for row in tg.horiz_rows(labels, data, normal_dat, args, colors):
        rows.append(row)

    # Values should be displayed as percentages: 1->100%, 2->200%, etc.
    assert rows == [
        (1, 10, 1, None, "1: ", " 100%", None),
        (2, 20, 1, None, "2: ", " 200%", None),
        (3, 30, 1, None, "3: ", " 300%", None),
        (4, 40, 1, None, "4: ", " 400%", None),
        (5, 50, 1, None, "5: ", " 500%", None),
    ]
