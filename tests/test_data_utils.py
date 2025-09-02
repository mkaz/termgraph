from termgraph import termgraph as tg


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