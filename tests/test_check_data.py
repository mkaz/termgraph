import pytest
from termgraph import termgraph as tg


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


def test_check_data_empty_labels_exits_with_one():
    """Test that check_data exits with code 1 when labels list is empty"""
    labels = []
    data = [[183.32], [231.23]]
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


def test_check_data_empty_data_exits_with_one():
    """Test that check_data exits with code 1 when data list is empty"""
    labels = ["2007", "2008"]
    data = []
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