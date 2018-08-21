import unittest
from unittest.mock import patch
from io import StringIO
from .termgraph import *

class TermgraphTest(unittest.TestCase):
    def test_main(self):
        pass

    def test_findMin_returns_lowest_value(self):
        minimum = findMin([[183.32], [231.23], [16.43], [50.21],
                           [508.97], [212.05], [1.0]])
        assert minimum == 1.0

    def test_findMax_returns_highest_value(self):
        maximum = findMax([[183.32], [231.23], [16.43], [50.21],
                           [508.97], [212.05], [1.0]])
        assert maximum == 508.97

    def test_findMaxLabelLength_returns_correct_length(self):
        length = findMaxLabelLength(['2007', '2008', '2009', '2010', '2011',
                                     '2012', '2014'])
        assert length == 4
        length = findMaxLabelLength(['aaaaaaaa', 'bbb', 'cccccccccccccc', 'z'])
        assert length == 14

    def test_normalize_returns_correct_results(self):
        expected = [[17.94594168946985], [22.661771364450654],
                    [1.5187904797527412], [4.843789987597693], [50.0],
                    [20.77386459830305], [0.0]]
        results = normalize([[183.32], [231.23], [16.43], [50.21], [508.97],
                             [212.05], [1.0]], 50)
        assert results == expected

    def test_horizontal_rows_yields_correct_values(self):
        labels = ['2007', '2008', '2009', '2010', '2011',
                  '2012', '2014']
        data = [[183.32], [231.23], [16.43], [50.21], [508.97],
                [212.05], [1.0]]
        normal_dat = [[17.94594168946985], [22.661771364450654],
                      [1.5187904797527412], [4.843789987597693],
                      [50.0], [20.77386459830305], [0.0]]
        args = {'filename': 'data/ex1.dat', 'title': None,
                'width': 50, 'format': '{:<5.2f}', 'suffix': '',
                'no_labels': False, 'color': None, 'vertical': False,
                'stacked': False, 'different_scale': False,
                'calendar': False, 'start_dt': None, 'custom_tick': '',
                'delim': '', 'verbose': False, 'version': False}
        colors = []
        
        rows = []
        for row in horiontal_rows(labels, data, normal_dat, args, colors):
            rows.append(row)
        assert rows == [(183.32, 17, 1.0, None), (231.23, 22, 1.0, None),
                        (16.43, 1, 1.0, None), (50.21, 4, 1.0, None),
                        (508.97, 50, 1.0, None), (212.05, 20, 1.0, None),
                        (1.0, 0, 1.0, None)]

    def test_print_row_prints_correct_block_count(self):
        with patch('sys.stdout', new=StringIO()) as output:
            print_row('2007: 183.32', 17, 1.0, None)
            output = output.getvalue().strip()
            assert output == '▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇'

    def test_stacked_graph(self):
        pass

    def test_vertically(self):
        pass

    def test_print_vertical(self):
        pass

    def test_chart(self):
        pass

    def test_check_data(self):
        pass

    def test_print_categories(self):
        pass

    def test_read_data(self):
        pass

    def test_calendar_heatmap_prints_correct_heatmap(self):
        with patch('sys.stdout', new=StringIO()) as output:
            data = [[4.52], [4.81], [5.05], [2.0], [5.65], [5.15], [3.75],
                    [3.72], [5.04], [4.6], [4.77], [5.44], [4.3], [4.84],
                    [6.31], [4.31], [4.15], [5.19], [3.65], [4.01], [7.19],
                    [4.21], [4.58], [8.09], [4.04], [4.29], [4.69], [4.31],
                    [5.05], [13.1], [3.6], [4.7], [3.77], [3.8], [3.54],
                    [3.42], [3.31], [3.55], [3.43], [3.79], [4.26]]
            labels = ['2017-07-01', '2017-07-06', '2017-07-08', '2017-07-15',
                      '2017-07-17', '2017-07-19', '2017-07-21', '2017-08-02',
                      '2017-08-03', '2017-08-05', '2017-08-08', '2017-08-10',
                      '2017-08-18', '2017-08-24', '2017-08-27', '2017-08-31',
                      '2017-09-06', '2017-09-08', '2017-09-10', '2017-09-13',
                      '2017-09-16', '2017-09-21', '2017-09-25', '2017-09-28',
                      '2017-10-02', '2017-10-09', '2017-10-13', '2017-10-18',
                      '2017-10-22', '2017-10-28', '2017-11-01', '2017-11-10',
                      '2018-02-06', '2018-03-05', '2018-03-07', '2018-05-16',
                      '2018-05-21', '2018-06-11', '2018-06-13', '2018-06-16',
                      '2018-06-20']
            args = {'filename': 'data/cal.dat', 'title': None, 'width': 50,
                    'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                    'color': None, 'vertical': False, 'stacked': False,
                    'different_scale': False, 'calendar': True,
                    'start_dt': '2017-07-01', 'custom_tick': '',
                    'delim': '', 'verbose': False, 'version': False}
            calendar_heatmap(data, labels, args)
            output = output.getvalue().strip()
            assert output == 'Jun Jul Aug Sep Oct Nov Dec Jan Feb Mar Apr May Jun \nMon: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nTue: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nWed: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\nThu: \x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▓\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nFri: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nSat: \x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m░\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▓\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m█\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nSun: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m'
