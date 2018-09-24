import unittest
from unittest.mock import patch
from io import StringIO
from termgraph import termgraph as tg

class TermgraphTest(unittest.TestCase):
    def test_initArgs(self):
        tg.initArgs()

    def test_main(self):
        pass

    def test_findMin_returns_lowest_value(self):
        minimum = tg.findMin([[183.32], [231.23], [16.43], [50.21],
                              [508.97], [212.05], [1.0]])
        assert minimum == 1.0

    def test_findMax_returns_highest_value(self):
        maximum = tg.findMax([[183.32], [231.23], [16.43], [50.21],
                              [508.97], [212.05], [1.0]])
        assert maximum == 508.97

    def test_findMaxLabelLength_returns_correct_length(self):
        length = tg.findMaxLabelLength(['2007', '2008', '2009', '2010', '2011',
                                        '2012', '2014'])
        assert length == 4
        length = tg.findMaxLabelLength(['aaaaaaaa', 'bbb', 'cccccccccccccc', 'z'])
        assert length == 14

    def test_normalize_returns_correct_results(self):
        expected = [[18.00891997563707], [22.715484213214925],
                    [1.6140440497475292], [4.932510757019078], [50.0],
                    [20.83128671630941], [0.09823761714835845]]
        results = tg.normalize([[183.32], [231.23], [16.43], [50.21], [508.97],
                                [212.05], [1.0]], 50)
        assert results == expected

    def test_normalize_with_negative_datapoint_returns_correct_results(self):
        expected = [[18.625354066709058], [23.241227816636798],
                    [2.546389964737846], [5.8009133475923464], [50.0],
                    [21.393336801741913], [0.0]]
        results = tg.normalize([[183.32], [231.23], [16.43], [50.21], [508.97],
                                [212.05], [-10.0]], 50)
        assert results == expected

    def test_normalize_with_larger_width_does_not_normalize(self):
        expected = [[183.32], [231.23], [16.43], [50.21], [508.97], [212.05], [1.0]]
        results = tg.normalize(expected, 20000)
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
        for row in tg.horiontal_rows(labels, data, normal_dat, args, colors):
            rows.append(row)
        assert rows == [(183.32, 17, 1.0, None), (231.23, 22, 1.0, None),
                        (16.43, 1, 1.0, None), (50.21, 4, 1.0, None),
                        (508.97, 50, 1.0, None), (212.05, 20, 1.0, None),
                        (1.0, 0, 1.0, None)]
    
    def test_horizontal_rows_no_labels_yields_no_labels(self):
        with patch('sys.stdout', new=StringIO()) as output:
            labels = ['2007', '2008', '2009', '2010', '2011',
                      '2012', '2014']
            data = [[183.32], [231.23], [16.43], [50.21], [508.97],
                    [212.05], [1.0]]
            normal_dat = [[17.94594168946985], [22.661771364450654],
                          [1.5187904797527412], [4.843789987597693],
                          [50.0], [20.77386459830305], [0.0]]
            args = {'filename': 'data/ex1.dat', 'title': None,
                    'width': 50, 'format': '{:<5.2f}', 'suffix': '',
                    'no_labels': True, 'color': None, 'vertical': False,
                    'stacked': False, 'different_scale': False,
                    'calendar': False, 'start_dt': None, 'custom_tick': '',
                    'delim': '', 'verbose': False, 'version': False}
            colors = []

            rows = []
            for row in tg.horiontal_rows(labels, data, normal_dat, args, colors):
                rows.append(row)
            assert rows == [(183.32, 17, 1.0, None), (231.23, 22, 1.0, None),
                            (16.43, 1, 1.0, None), (50.21, 4, 1.0, None),
                            (508.97, 50, 1.0, None), (212.05, 20, 1.0, None),
                            (1.0, 0, 1.0, None)]
            output = output.getvalue().strip()
            assert output == '183.32\n 231.23\n 16.43\n 50.21\n 508.97\n 212.05\n 1.00'

    def test_horizontal_rows_multiple_series_only_has_label_at_beginning(self):
        with patch('sys.stdout', new=StringIO()) as output:
            labels = ['2007', '2008', '2009', '2010', '2011',
                      '2012', '2014']
            data = [[183.32, 190.52, 90.0], [231.23, 50.0, 80.6],
                    [16.43, 53.1, 76.54], [50.21, 7.0, 0.0], [508.97, 10.45, 7.0],
                    [212.05, 20.2, -4.4], [30.0, 9.0, 9.8]]
            normal_dat = [[99.4279661016949, 103.2415254237288, 49.99999999999999],
                          [124.80402542372879, 28.813559322033893, 45.02118644067796],
                          [11.032838983050844, 30.455508474576266, 42.87076271186441],
                          [28.924788135593214, 6.038135593220338, 2.330508474576271],
                          [271.9120762711864, 7.865466101694914, 6.038135593220338],
                          [114.64512711864406, 13.02966101694915, 0.0],
                          [18.220338983050844, 7.097457627118644, 7.521186440677965]]
            args = {'filename': 'data/ex5.dat', 'title': None, 'width': 50,
                    'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                    'color': None, 'vertical': False, 'stacked': False,
                    'different_scale': False, 'calendar': False, 'start_dt': None,
                    'custom_tick': '', 'delim': '', 'verbose': False,
                    'version': False}
            colors = [None, None, None]

            rows = []
            for row in tg.horiontal_rows(labels, data, normal_dat, args, colors):
                rows.append(row)
            assert rows == [(183.32, 99, -4.4, None), (190.52, 103, -4.4, None),
                            (90.0, 49, -4.4, None), (231.23, 124, -4.4, None),
                            (50.0, 28, -4.4, None), (80.6, 45, -4.4, None),
                            (16.43, 11, -4.4, None), (53.1, 30, -4.4, None),
                            (76.54, 42, -4.4, None), (50.21, 28, -4.4, None),
                            (7.0, 6, -4.4, None), (0.0, 2, -4.4, None),
                            (508.97, 271, -4.4, None), (10.45, 7, -4.4, None),
                            (7.0, 6, -4.4, None), (212.05, 114, -4.4, None),
                            (20.2, 13, -4.4, None), (-4.4, 0, -4.4, None),
                            (30.0, 18, -4.4, None), (9.0, 7, -4.4, None),
                            (9.8, 7, -4.4, None)]
            output = output.getvalue().strip()
            assert output == '2007:  183.32\n       190.52\n       90.00\n2008:  231.23\n       50.00\n       80.60\n2009:  16.43\n       53.10\n       76.54\n2010:  50.21\n       7.00 \n       0.00 \n2011:  508.97\n       10.45\n       7.00 \n2012:  212.05\n       20.20\n       -4.40\n2014:  30.00\n       9.00 \n       9.80'

    def test_print_row_prints_correct_block_count(self):
        with patch('sys.stdout', new=StringIO()) as output:
            tg.print_row('2007: 183.32', 17, 1.0, None)
            output = output.getvalue().strip()
            assert output == '▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇'

    def test_stacked_graph_prints_correct_graph(self):
        with patch('sys.stdout', new=StringIO()) as output:
            labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
            data = [[183.32, 190.52], [231.23, 5.0], [16.43, 53.1], [50.21, 7.0],
                    [508.97, 10.45], [212.05, 20.2], [30.0, 20.0]]
            normal_data = [[48.059508408796894, 50.0], [60.971862871927556, 0.0],
                           [3.080530401034929, 12.963561880120743],
                           [12.184670116429496, 0.5390254420008624],
                           [135.82632600258734, 1.4688443294523499],
                           [55.802608883139285, 4.096593359206555],
                           [6.737818025010781, 4.042690815006468]]
            len_categories = 2
            args = {'filename': 'data/ex4.dat', 'title': None, 'width': 50,
                    'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                    'color': None, 'vertical': False, 'stacked': True,
                    'different_scale': False, 'calendar': False,
                    'start_dt': None, 'custom_tick': '', 'delim': '',
                    'verbose': False, 'version': False}
            colors = [91, 94]
            tg.stacked_graph(labels, data, normal_data, len_categories, args,
                             colors)
            output = output.getvalue().strip()
            assert output == '2007: [91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇[0m[94m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇[0m 373.84\n2008: [91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇[0m[94m▏[0m 236.23\n2009: [91m▇▇▇[0m[94m▇▇▇▇▇▇▇▇▇▇▇▇[0m 69.53\n2010: [91m▇▇▇▇▇▇▇▇▇▇▇▇[0m[94m▏[0m 57.21\n2011: [91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇[0m[94m▇[0m 519.42\n2012: [91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇[0m[94m▇▇▇▇[0m 232.25\n2014: [91m▇▇▇▇▇▇[0m[94m▇▇▇▇[0m 50.00'

    def test_stacked_graph_no_label_prints_no_labels(self):
        with patch('sys.stdout', new=StringIO()) as output:
            labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
            data = [[183.32, 190.52], [231.23, 5.0], [16.43, 53.1], [50.21, 7.0],
                    [508.97, 10.45], [212.05, 20.2], [30.0, 20.0]]
            normal_data = [[48.059508408796894, 50.0], [60.971862871927556, 0.0],
                           [3.080530401034929, 12.963561880120743],
                           [12.184670116429496, 0.5390254420008624],
                           [135.82632600258734, 1.4688443294523499],
                           [55.802608883139285, 4.096593359206555],
                           [6.737818025010781, 4.042690815006468]]
            len_categories = 2
            args = {'filename': 'data/ex4.dat', 'title': None, 'width': 50,
                    'format': '{:<5.2f}', 'suffix': '', 'no_labels': True,
                    'color': None, 'vertical': False, 'stacked': True,
                    'different_scale': False, 'calendar': False,
                    'start_dt': None, 'custom_tick': '', 'delim': '',
                    'verbose': False, 'version': False}
            colors = [91, 94]
            tg.stacked_graph(labels, data, normal_data, len_categories, args,
                             colors)
            output = output.getvalue().strip()
            assert output == '\x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m\x1b[94m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 373.84\n\x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m\x1b[94m▏\x1b[0m 236.23\n\x1b[91m▇▇▇\x1b[0m\x1b[94m▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 69.53\n\x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m\x1b[94m▏\x1b[0m 57.21\n\x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m\x1b[94m▇\x1b[0m 519.42\n\x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m\x1b[94m▇▇▇▇\x1b[0m 232.25\n\x1b[91m▇▇▇▇▇▇\x1b[0m\x1b[94m▇▇▇▇\x1b[0m 50.00'

    def test_vertically_returns_correct_result(self):
        args = {'filename': 'data/ex2.dat', 'title': None, 'width': 50,
                'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                'color': None, 'vertical': True, 'stacked': False,
                'different_scale': False, 'calendar': False, 'start_dt': None,
                'custom_tick': '', 'delim': '', 'verbose': False,
                'version': False}
        value = 2.0
        num_blocks = 2
        val_min = 2.0
        color = None
        result = tg.vertically(value, num_blocks, val_min, color, args)
        assert result == [('▇',), ('▇',)]

    def test_print_vertical(self):
        pass

    def test_chart_prints_correct_chart(self):
        with patch('sys.stdout', new=StringIO()) as output:
            colors = []
            data = [[183.32], [231.23], [16.43], [50.21], [508.97],
                    [212.05], [1.0]]
            args = {'filename': 'data/ex1.dat', 'title': None, 'width': 50,
                    'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                    'color': None, 'vertical': False, 'stacked': False,
                    'different_scale': False, 'calendar': False,
                    'start_dt': None, 'custom_tick': '', 'delim': '',
                    'verbose': False, 'version': False}
            labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
            tg.chart(colors, data, args, labels)
            output = output.getvalue().strip()
            assert output == '2007: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 183.32\n2008: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 231.23\n2009: ▇ 16.43\n2010: ▇▇▇▇ 50.21\n2011: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 508.97\n2012: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 212.05\n2014: ▏ 1.00'

    def test_chart_multiple_series_prints_correctly(self):
        with patch('sys.stdout', new=StringIO()) as output:
            colors = [91, 94]
            data = [[183.32, 190.52], [231.23, 5.0], [16.43, 53.1], [50.21, 7.0],
                    [508.97, 10.45], [212.05, 20.2], [30.0, 20.0]]
            args = {'filename': 'data/ex4.dat', 'title': None, 'width': 50,
                    'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                    'color': None, 'vertical': False, 'stacked': False,
                    'different_scale': False, 'calendar': False,
                    'start_dt': None, 'custom_tick': '', 'delim': '',
                    'verbose': False, 'version': False}
            labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
            tg.chart(colors, data, args, labels)
            output = output.getvalue().strip()
            assert output == '2007: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 183.32\n      \x1b[94m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 190.52\n2008: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 231.23\n      \x1b[94m▇\x1b[0m 5.00 \n2009: \x1b[91m▇▇▇▇\x1b[0m 16.43\n      \x1b[94m▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 53.10\n2010: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 50.21\n      \x1b[94m▇\x1b[0m 7.00 \n2011: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 508.97\n      \x1b[94m▇▇\x1b[0m 10.45\n2012: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 212.05\n      \x1b[94m▇▇▇▇▇\x1b[0m 20.20\n2014: \x1b[91m▇▇▇▇▇▇▇\x1b[0m 30.00\n      \x1b[94m▇▇▇▇▇\x1b[0m 20.00'

    def test_chart_multiple_series_no_colors_prints_correctly(self):
        with patch('sys.stdout', new=StringIO()) as output:
            colors = []
            data = [[183.32, 190.52], [231.23, 5.0], [16.43, 53.1], [50.21, 7.0],
                    [508.97, 10.45], [212.05, 20.2], [30.0, 20.0]]
            args = {'filename': 'data/ex4.dat', 'title': None, 'width': 50,
                    'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                    'color': None, 'vertical': False, 'stacked': False,
                    'different_scale': False, 'calendar': False,
                    'start_dt': None, 'custom_tick': '', 'delim': '',
                    'verbose': False, 'version': False}
            labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
            tg.chart(colors, data, args, labels)
            output = output.getvalue().strip()
            assert output == '2007: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 183.32\n      ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 190.52\n2008: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 231.23\n      ▏ 5.00 \n2009: ▇▇▇ 16.43\n      ▇▇▇▇▇▇▇▇▇▇▇▇ 53.10\n2010: ▇▇▇▇▇▇▇▇▇▇▇▇ 50.21\n      ▏ 7.00 \n2011: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 508.97\n      ▇ 10.45\n2012: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 212.05\n      ▇▇▇▇ 20.20\n2014: ▇▇▇▇▇▇ 30.00\n      ▇▇▇▇ 20.00'

    def test_chart_multiple_series_different_scale_prints_correctly(self):
        with patch('sys.stdout', new=StringIO()) as output:
            colors = [91, 94]
            data = [[183.32, 190.52], [231.23, 5.0], [16.43, 53.1], [50.21, 7.0],
                    [508.97, 10.45], [212.05, 20.2], [30.0, 20.0]]
            args = {'filename': 'data/ex4.dat', 'title': None, 'width': 50,
                    'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                    'color': None, 'vertical': False, 'stacked': False,
                    'different_scale': True, 'calendar': False,
                    'start_dt': None, 'custom_tick': '', 'delim': '',
                    'verbose': False, 'version': False}
            labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
            tg.chart(colors, data, args, labels)
            output = output.getvalue().strip()
            assert output == '2007: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 183.32\n2008: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 231.23\n2009: \x1b[91m▏\x1b[0m 16.43\n2010: \x1b[91m▇▇▇\x1b[0m 50.21\n2011: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 508.97\n2012: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 212.05\n2014: \x1b[91m▇\x1b[0m 30.00\n\n2007: \x1b[94m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 190.52\n2008: \x1b[94m▏\x1b[0m 5.00 \n2009: \x1b[94m▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 53.10\n2010: \x1b[94m▏\x1b[0m 7.00 \n2011: \x1b[94m▇\x1b[0m 10.45\n2012: \x1b[94m▇▇▇▇\x1b[0m 20.20\n2014: \x1b[94m▇▇▇▇\x1b[0m 20.00'

    def test_chart_stacked_prints_correctly(self):
        with patch('sys.stdout', new=StringIO()) as output:
            colors = [91, 94]
            data = [[183.32, 190.52], [231.23, 5.0], [16.43, 53.1], [50.21, 7.0],
                    [508.97, 10.45], [212.05, 20.2], [30.0, 20.0]]
            args = {'filename': 'data/ex4.dat', 'title': None, 'width': 50,
                    'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                    'color': None, 'vertical': False, 'stacked': True,
                    'different_scale': False, 'calendar': False,
                    'start_dt': None, 'custom_tick': '', 'delim': '',
                    'verbose': False, 'version': False}
            labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
            tg.chart(colors, data, args, labels)
            output = output.getvalue().strip()
            assert output == '2007: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m\x1b[94m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 373.84\n2008: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m\x1b[94m▇\x1b[0m 236.23\n2009: \x1b[91m▇▇▇▇\x1b[0m\x1b[94m▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m 69.53\n2010: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m\x1b[94m▇\x1b[0m 57.21\n2011: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m\x1b[94m▇▇\x1b[0m 519.42\n2012: \x1b[91m▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇\x1b[0m\x1b[94m▇▇▇▇▇\x1b[0m 232.25\n2014: \x1b[91m▇▇▇▇▇▇▇\x1b[0m\x1b[94m▇▇▇▇▇\x1b[0m 50.00'

    def test_check_data_returns_correct_result(self):
        labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
        data = [[183.32], [231.23], [16.43], [50.21], [508.97],
                [212.05], [1.0]]
        args = {'filename': 'data/ex1.dat', 'title': None, 'width': 50,
                'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                'color': None, 'vertical': False, 'stacked': False,
                'different_scale': False, 'calendar': False,
                'start_dt': None, 'custom_tick': '', 'delim': '',
                'verbose': False, 'version': False}
        result = tg.check_data(labels, data, args)
        assert result == []

    def test_check_data_with_color_returns_correct_result(self):
        labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
        data = [[183.32], [231.23], [16.43], [50.21], [508.97],
                [212.05], [1.0]]
        args = {'filename': 'data/ex1.dat', 'title': None, 'width': 50,
                'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                'color': ['red'], 'vertical': False, 'stacked': False,
                'different_scale': False, 'calendar': False,
                'start_dt': None, 'custom_tick': '', 'delim': '',
                'verbose': False, 'version': False}
        result = tg.check_data(labels, data, args)
        assert result == [91]

    def test_check_data_stacked_with_no_color_returns_correct_result(self):
        labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
        data = [[183.32, 190.52], [231.23, 5.0], [16.43, 53.1], [50.21, 7.0],
                [508.97, 10.45], [212.05, 20.2], [30.0, 20.0]]
        args = {'filename': 'data/ex4.dat', 'title': None, 'width': 50,
                'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                'color': None, 'vertical': False, 'stacked': True,
                'different_scale': False, 'calendar': False,
                'start_dt': None, 'custom_tick': '', 'delim': '',
                'verbose': False, 'version': False}
        result = tg.check_data(labels, data, args)
        assert result == [91, 94]

    def test_check_data_vertical_multiple_series_same_scale_exits_with_one(self):
        labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
        data = [[183.32, 190.52], [231.23, 5.0], [16.43, 53.1], [50.21, 7.0],
                [508.97, 10.45], [212.05, 20.2], [30.0, 20.0]]
        args = {'filename': 'data/ex4.dat', 'title': None, 'width': 50,
                'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                'color': None, 'vertical': True, 'stacked': False,
                'different_scale': False, 'calendar': False,
                'start_dt': None, 'custom_tick': '', 'delim': '',
                'verbose': False, 'version': False}
        with self.assertRaises(SystemExit) as cm:
            tg.check_data(labels, data, args)

        self.assertEqual(cm.exception.code, 1)

    def test_check_data_mismatching_color_and_category_count_exits_with_one(self):
        labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
        data = [[183.32], [231.23], [16.43], [50.21], [508.97],
                [212.05], [1.0]]
        args = {'filename': 'data/ex1.dat', 'title': None, 'width': 50,
                'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                'color': ['red', 'blue'], 'vertical': False, 'stacked': False,
                'different_scale': False, 'calendar': False,
                'start_dt': None, 'custom_tick': '', 'delim': '',
                'verbose': False, 'version': False}
        with self.assertRaises(SystemExit) as cm:
            tg.check_data(labels, data, args)

        self.assertEqual(cm.exception.code, 1)

    def test_check_data_mismatching_data_and_labels_count_exits_with_one(self):
        labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
        data = [[183.32], [231.23], [16.43], [50.21], [508.97],
                [212.05]]
        args = {'filename': 'data/ex1.dat', 'title': None, 'width': 50,
                'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                'color': None, 'vertical': False, 'stacked': False,
                'different_scale': False, 'calendar': False,
                'start_dt': None, 'custom_tick': '', 'delim': '',
                'verbose': False, 'version': False}
        with self.assertRaises(SystemExit) as cm:
            tg.check_data(labels, data, args)

        self.assertEqual(cm.exception.code, 1)

    def test_check_data_missing_data_for_categories_count_exits_with_one(self):
        labels = ['2007', '2008', '2009', '2010', '2011', '2012', '2014']
        data = [[183.32, 190.52], [231.23, 5.0], [16.43, 53.1], [50.21, 7.0],
                [508.97, 10.45], [212.05], [30.0, 20.0]]
        args = {'filename': 'data/ex4.dat', 'title': None, 'width': 50,
                'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                'color': None, 'vertical': False, 'stacked': False,
                'different_scale': False, 'calendar': False,
                'start_dt': None, 'custom_tick': '', 'delim': '',
                'verbose': False, 'version': False}
        with self.assertRaises(SystemExit) as cm:
            tg.check_data(labels, data, args)

        self.assertEqual(cm.exception.code, 1)

    def test_print_categories_prints_correct_categories(self):
        with patch('sys.stdout', new=StringIO()) as output:
            categories = ['Boys', 'Girls']
            colors = [91, 94]
            tg.print_categories(categories, colors)
            output = output.getvalue().strip()
            assert output == "\x1b[91m▇ Boys  \x1b[0m\x1b[94m▇ Girls  \x1b[0m"

    def test_read_data_returns_correct_results(self):
        args = {'filename': 'data/ex4.dat', 'title': None, 'width': 50,
                'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                'color': None, 'vertical': False, 'stacked': False,
                'different_scale': False, 'calendar': False, 'start_dt': None,
                'custom_tick': '', 'delim': '', 'verbose': False,
                'version': False}
        categories, labels, data, colors = tg.read_data(args)
        assert categories == ['Boys', 'Girls']
        assert labels == ['2007', '2008', '2009', '2010',
                          '2011', '2012', '2014']
        assert data == [[183.32, 190.52], [231.23, 5.0], [16.43, 53.1],
                        [50.21, 7.0], [508.97, 10.45], [212.05, 20.2],
                        [30.0, 20.0]]
        assert colors == []

    def test_read_data_with_title_prints_title(self):
        with patch('sys.stdout', new=StringIO()) as output:
            args = {'filename': 'data/ex4.dat', 'title': 'spaghetti', 'width': 50,
                    'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                    'color': None, 'vertical': False, 'stacked': False,
                    'different_scale': False, 'calendar': False, 'start_dt': None,
                    'custom_tick': '', 'delim': '', 'verbose': False,
                    'version': False}
            tg.read_data(args)
            output = output.getvalue().strip()
            assert output == '# spaghetti\n\n▇ Boys  \x1b[0m▇ Girls  \x1b[0m'

    def test_read_data_verbose(self):
        with patch('sys.stdout', new=StringIO()) as output:
            args = {'filename': 'data/ex1.dat', 'title': None, 'width': 50,
                    'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
                    'color': None, 'vertical': False, 'stacked': False,
                    'different_scale': False, 'calendar': False, 'start_dt': None,
                    'custom_tick': '', 'delim': '', 'verbose': True,
                    'version': False}
            tg.read_data(args)
            output = output.getvalue().strip()
            assert output == '>> Reading data from data/ex1.dat'

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
            tg.calendar_heatmap(data, labels, args)
            output = output.getvalue().strip()
            assert output == 'Jun Jul Aug Sep Oct Nov Dec Jan Feb Mar Apr May Jun \nMon: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nTue: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nWed: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\nThu: \x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▓\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nFri: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nSat: \x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m░\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▓\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m█\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nSun: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m'

    def test_calendar_heatmap_color_prints_correctly(self):
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
                    'color': ['red'], 'vertical': False, 'stacked': False,
                    'different_scale': False, 'calendar': True,
                    'start_dt': '2017-07-01', 'custom_tick': '',
                    'delim': '', 'verbose': False, 'version': False}
            tg.calendar_heatmap(data, labels, args)
            output = output.getvalue().strip()
            assert output == 'Jun Jul Aug Sep Oct Nov Dec Jan Feb Mar Apr May Jun \nMon: \x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m▒\x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\nTue: \x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\nWed: \x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\nThu: \x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m▓\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\nFri: \x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\nSat: \x1b[91m▒\x1b[0m\x1b[91m▒\x1b[0m\x1b[91m░\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▓\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m█\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\nSun: \x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m▒\x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m\x1b[91m \x1b[0m'

    def test_calendar_heatmap_custom_tick_prints_correctly(self):
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
                    'start_dt': '2017-07-01', 'custom_tick': '😮',
                    'delim': '', 'verbose': False, 'version': False}
            tg.calendar_heatmap(data, labels, args)
            output = output.getvalue().strip()
            assert output == 'Jun  Jul  Aug  Sep  Oct  Nov  Dec  Jan  Feb  Mar  Apr  May  Jun  \nMon: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m😮\x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nTue: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nWed: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\nThu: \x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nFri: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nSat: \x1b[94m😮\x1b[0m\x1b[94m😮\x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nSun: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m😮\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m'

    def test_calendar_heatmap_without_start_date_prints_correctly(self):
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
                    'start_dt': None, 'custom_tick': '',
                    'delim': '', 'verbose': False, 'version': False}
            tg.calendar_heatmap(data, labels, args)
            output = output.getvalue().strip()
            #file = open('/tmp/file.txt', 'w')
            #file.write(repr(output))
            #file.close()
            assert output == 'Aug Sep Oct Nov Dec Jan Feb Mar Apr May Jun Jul Aug \nMon: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nTue: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nWed: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nThu: \x1b[94m▒\x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m▓\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nFri: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nSat: \x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▓\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m█\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\nSun: \x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m▒\x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m\x1b[94m \x1b[0m'
