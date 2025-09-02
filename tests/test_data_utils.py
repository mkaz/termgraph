from termgraph.data import Data


def test_find_min_returns_lowest_value():
    data_values = [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
    labels = [str(i) for i in range(len(data_values))]
    data_obj = Data(data_values, labels)
    minimum = data_obj.find_min()
    assert minimum == 1.0


def test_find_max_returns_highest_value():
    data_values = [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
    labels = [str(i) for i in range(len(data_values))]
    data_obj = Data(data_values, labels)
    maximum = data_obj.find_max()
    assert maximum == 508.97


def test_find_max_label_length_returns_correct_length():
    labels1 = ["2007", "2008", "2009", "2010", "2011", "2012", "2014"]
    data_obj1 = Data([[0]] * len(labels1), labels1)
    length = data_obj1.find_max_label_length()
    assert length == 4
    
    labels2 = ["aaaaaaaa", "bbb", "cccccccccccccc", "z"]
    data_obj2 = Data([[0]] * len(labels2), labels2)
    length = data_obj2.find_max_label_length()
    assert length == 14