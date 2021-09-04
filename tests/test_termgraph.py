from unittest.mock import patch
from io import StringIO
from termgraph import termgraph as tg
import pytest


def test_init_args():
    tg.init_args()


def test_find_min_returns_lowest_value():
    minimum = tg.find_min(
        [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
    )
    assert minimum == 1.0


def test_find_max_returns_highest_value():
    maximum = tg.find_max(
        [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
    )
    assert maximum == 508.97


def test_find_max_label_length_returns_correct_length():
    length = tg.find_max_label_length(
        ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    )
    assert length == 4
    length = tg.find_max_label_length(["aaaaaaaa", "bbb", "cccccccccccccc", "z"])
    assert length == 14


def test_normalize_returns_correct_results():
    expected = [
        [18.00891997563707],
        [22.715484213214925],
        [1.6140440497475292],
        [4.932510757019078],
        [50.0],
        [20.83128671630941],
        [0.09823761714835845],
    ]
    results = tg.normalize(
        [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]], 50
    )
    assert results == expected


def test_normalize_with_all_zeros_returns_correct_results():
    expected = [
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
    ]
    results = tg.normalize([[0], [0], [0], [0], [0], [0], [0]], 50)
    assert results == expected


def test_normalize_with_negative_datapoint_returns_correct_results():
    expected = [
        [18.625354066709058],
        [23.241227816636798],
        [2.546389964737846],
        [5.8009133475923464],
        [50.0],
        [21.393336801741913],
        [0.0],
    ]
    results = tg.normalize(
        [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [-10.0]], 50
    )
    assert results == expected


def test_normalize_with_larger_width_does_not_normalize():
    data = [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
    expected = [
        [7203.567990254828],
        [9086.193685285969],
        [645.6176198990117],
        [1973.0043028076311],
        [20000.0],
        [8332.514686523764],
        [39.29504685934338],
    ]
    results = tg.normalize(data, 20000)
    assert results == expected


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


def test_check_data_returns_correct_result():
    labels = ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    data = [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
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
        "verbose": False,
        "version": False,
    }
    result = tg.check_data(labels, data, args)
    assert result == []


def test_check_data_with_color_returns_correct_result():
    labels = ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    data = [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
    args = {
        "filename": "data/ex1.dat",
        "title": None,
        "width": 50,
        "format": "{:<5.2f}",
        "suffix": "",
        "no_labels": False,
        "color": ["red"],
        "vertical": False,
        "stacked": False,
        "different_scale": False,
        "calendar": False,
        "start_dt": None,
        "custom_tick": "",
        "delim": "",
        "verbose": False,
        "version": False,
    }
    result = tg.check_data(labels, data, args)
    assert result == [91]


def test_check_data_stacked_with_no_color_returns_correct_result():
    labels = ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    data = [
        [183.32, 190.52],
        [231.23, 5.0],
        [16.43, 53.1],
        [50.21, 7.0],
        [508.97, 10.45],
        [212.05, 20.2],
        [30.0, 20.0],
    ]
    args = {
        "filename": "data/ex4.dat",
        "title": None,
        "width": 50,
        "format": "{:<5.2f}",
        "suffix": "",
        "no_labels": False,
        "color": None,
        "vertical": False,
        "stacked": True,
        "different_scale": False,
        "calendar": False,
        "start_dt": None,
        "custom_tick": "",
        "delim": "",
        "verbose": False,
        "version": False,
    }
    result = tg.check_data(labels, data, args)
    assert result == [91, 94]


def test_check_data_vertical_multiple_series_same_scale_exits_with_one():
    labels = ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    data = [
        [183.32, 190.52],
        [231.23, 5.0],
        [16.43, 53.1],
        [50.21, 7.0],
        [508.97, 10.45],
        [212.05, 20.2],
        [30.0, 20.0],
    ]
    args = {
        "filename": "data/ex4.dat",
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
    with pytest.raises(SystemExit) as e:
        tg.check_data(labels, data, args)
        assert e.exception.code == 1


def test_check_data_mismatching_color_and_category_count():
    labels = ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    data = [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
    args = {
        "filename": "data/ex1.dat",
        "title": None,
        "width": 50,
        "format": "{:<5.2f}",
        "suffix": "",
        "no_labels": False,
        "color": ["red", "blue"],
        "vertical": False,
        "stacked": False,
        "different_scale": False,
        "calendar": False,
        "start_dt": None,
        "custom_tick": "",
        "delim": "",
        "verbose": False,
        "version": False,
    }
    assert tg.check_data(labels, data, args)


def test_check_data_mismatching_data_and_labels_count_exits_with_one():
    labels = ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    data = [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05]]
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
        "verbose": False,
        "version": False,
    }
    with pytest.raises(SystemExit) as e:
        tg.check_data(labels, data, args)
        assert e.exception.code == 1


def test_check_data_missing_data_for_categories_count_exits_with_one():
    labels = ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    data = [
        [183.32, 190.52],
        [231.23, 5.0],
        [16.43, 53.1],
        [50.21, 7.0],
        [508.97, 10.45],
        [212.05],
        [30.0, 20.0],
    ]
    args = {
        "filename": "data/ex4.dat",
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
        "verbose": False,
        "version": False,
    }
    with pytest.raises(SystemExit) as e:
        tg.check_data(labels, data, args)
        assert e.exception.code == 1


def test_read_data_returns_correct_results():
    args = {
        "filename": "data/ex4.dat",
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
        "verbose": False,
        "version": False,
    }
    categories, labels, data, colors = tg.read_data(args)
    assert categories == ["Boys", "Girls"]
    assert labels == ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    assert data == [
        [183.32, 190.52],
        [231.23, 5.0],
        [16.43, 53.1],
        [50.21, 7.0],
        [508.97, 10.45],
        [212.05, 20.2],
        [30.0, 20.0],
    ]
    assert colors == []


def test_read_data_with_title_prints_title():
    with patch("sys.stdout", new=StringIO()) as output:
        args = {
            "filename": "data/ex4.dat",
            "title": "spaghetti",
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
            "verbose": False,
            "version": False,
        }
        tg.read_data(args)
        output = output.getvalue().strip()
        assert output == "# spaghetti\n\n▇ Boys  ▇ Girls"


def test_read_data_verbose():
    with patch("sys.stdout", new=StringIO()) as output:
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
            "verbose": True,
            "version": False,
        }
        tg.read_data(args)
        output = output.getvalue().strip()
        assert output == ">> Reading data from data/ex1.dat"


def test_cvt_to_readable():
    data = [
        0.0000000000001234567,
        0.000000000001234567,
        0.00000000001234567,
        0.0000000001234567,
        0.000000001234567,
        0.00000001234567,
        0.0000001234567,
        0.000001234567,
        0.00001234567,
        0.0001234567,
        0.001234567,
        0.01234567,
        0.1234567,
        1.234567,
        12.34567,
        123.4567,
        1234.567,
        12345.67,
        123456.7,
        1234567.0,
        12345670.0,
        123456700.0,
        1234567000.0,
        12345670000.0,
        123456700000.0,
        1234567000000.0,
        12345670000000.0,
        123456700000000.0,
        1234567000000000.0,
        12345670000000000.0]
    expected = [
        '123.46e-15',
        '1.24e-12',
        '12.35e-12',
        '123.46e-12',
        '1.24e-9',
        '12.35e-9',
        '123.46e-9',
        '1.24e-6',
        '12.35e-6',
        '123.46e-6',
        '1.24e-3',
        '12.35e-3',
        '123.46e-3',
        '1.23',
        '12.35',
        '123.46',
        '1.24K',
        '12.35K',
        '123.46K',
        '1.24M',
        '12.35M',
        '123.46M',
        '1.24B',
        '12.35B',
        '123.46B',
        '1.24T',
        '12.35T',
        '123.46T',
        '1234567000000000.00',
        '12345670000000000.00'
    ]
    result1 = [tg.cvt_to_readable(x) for x in data]
    result2 = ['{0:<.2f}{1}'.format(x[0], x[1]) for x in result1]
    assert result2 == expected