import tempfile
from io import StringIO
from unittest.mock import patch

from termgraph import termgraph as tg


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


def test_concatenate_neighboring_labels():
    with tempfile.NamedTemporaryFile("w") as tmp:
        args = {
            "filename": tmp.name,
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
        tmp.write(
            """
label one 1 2 3
label two 5 6 7
label three 9 10 11
        """
        )
        tmp.seek(0)
        _categories, labels, data, _colors = tg.read_data(args)
        assert labels == ["label one", "label two", "label three"]
        assert data == [[1.0, 2.0, 3.0], [5.0, 6.0, 7.0], [9.0, 10.0, 11.0]]


def test_labels_at_end_of_row():
    """Check that we can identify labels that come after the data"""
    with tempfile.NamedTemporaryFile("w") as tmp:
        args = {
            "filename": tmp.name,
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
        tmp.write(
            """
1 2 3 A
5 6 7 B
9 10 11 C
        """
        )
        tmp.seek(0)
        _categories, labels, data, _colors = tg.read_data(args)
        assert labels == ["A", "B", "C"]
        assert data == [[1.0, 2.0, 3.0], [5.0, 6.0, 7.0], [9.0, 10.0, 11.0]]


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


def test_read_data_custom_delimiter():
    """Test that custom delimiter (pipe) works correctly"""
    args = {
        "filename": "data/ex_pipe.dat",
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
        "delim": "|",
        "verbose": False,
        "version": False,
    }
    categories, labels, data, colors = tg.read_data(args)
    assert categories == ["Category A", "Category B", "Category C"]
    assert labels == ["Label One", "Label Two", "Label Three"]
    assert data == [[10.5, 20.3, 15.8], [25.0, 18.5, 30.2], [12.1, 22.7, 19.4]]
    assert colors == []
