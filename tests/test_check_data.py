import pytest
from termgraph import termgraph as tg


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