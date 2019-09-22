#!/usr/bin/env python3
# coding=utf-8
"""This module allows drawing basic graphs in the terminal."""

# termgraph.py - draw basic graphs on terminal
# https://github.com/mkaz/termgraph

from __future__ import print_function
import argparse
import sys
from datetime import datetime, timedelta
from itertools import zip_longest
from colorama import init


VERSION = '0.2.0'

init()

# ANSI escape SGR Parameters color codes
AVAILABLE_COLORS = {
    'red': 91,
    'blue': 94,
    'green': 92,
    'magenta': 95,
    'yellow': 93,
    'black': 90,
    'cyan': 96
}

DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
DELIM = ','
TICK = '▇'
SM_TICK = '▏'

try:
    range = xrange
except NameError:
    pass

def init_args():
    """Parse and return the arguments."""
    parser = argparse.ArgumentParser(
        description='draw basic graphs on terminal')
    parser.add_argument(
        'filename',
        nargs='?',
        default="-",
        help='data file name (comma or space separated). Defaults to stdin.')
    parser.add_argument(
        '--title',
        help='Title of graph'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=50,
        help='width of graph in characters default:50'
    )
    parser.add_argument(
        '--format',
        default='{:<5.2f}',
        help='format specifier to use.'
    )
    parser.add_argument(
        '--suffix',
        default='',
        help='string to add as a suffix to all data points.'
    )
    parser.add_argument(
        '--no-labels',
        action='store_true',
        help='Do not print the label column'
    )
    parser.add_argument(
        '--color',
        nargs='*',
        choices=AVAILABLE_COLORS,
        help='Graph bar color( s )'
    )
    parser.add_argument(
        '--vertical',
        action='store_true',
        help='Vertical graph'
    )
    parser.add_argument(
        '--stacked',
        action='store_true',
        help='Stacked bar graph'
    )
    parser.add_argument(
        '--different-scale',
        action='store_true',
        help='Categories have different scales.'
    )
    parser.add_argument(
        '--calendar',
        action='store_true',
        help='Calendar Heatmap chart'
    )
    parser.add_argument(
        '--start-dt',
        help='Start date for Calendar chart'
    )
    parser.add_argument(
        '--custom-tick',
        default='',
        help='Custom tick mark, emoji approved'
    )
    parser.add_argument(
        '--delim',
        default='',
        help='Custom delimiter, default , or space'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output, helpful for debugging'
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='Display version and exit'
    )
    if len(sys.argv) == 1:
        if sys.stdin.isatty():
            parser.print_usage()
            sys.exit(2)

    args = vars(parser.parse_args())

    if args['custom_tick'] != '':
        global TICK, SM_TICK
        TICK = args['custom_tick']
        SM_TICK = ''

    if args['delim'] != '':
        global DELIM
        DELIM = args['delim']

    return args


def main():
    """Main function."""
    args = init_args()

    if args['version']:
        print('termgraph v{}'.format(VERSION))
        sys.exit()

    _, labels, data, colors = read_data(args)
    if args['calendar']:
        calendar_heatmap(data, labels, args)
    else:
        chart(colors, data, args, labels)

def find_min(list_):
    """Return the minimum value in sublist of list."""
    return min([sublist[-1] for sublist in list_])

def find_max(list_):
    """Return the maximum value in sublist of list."""
    return max([sublist[-1] for sublist in list_])

def find_max_label_length(labels):
    """Return the maximum length for the labels."""
    length = 0
    for i in range(len(labels)):
        if len(labels[i]) > length:
            length = len(labels[i])

    return length

def normalize(data, width):
    """Normalize the data and return it."""
    min_dat = find_min(data)
    # We offset by the minimum if there's a negative.
    off_data = []
    if min_dat < 0:
        min_dat = abs(min_dat)
        for dat in data:
            off_data.append([_d + min_dat for _d in dat])
    else:
        off_data = data
    min_dat = find_min(off_data)
    max_dat = find_max(off_data)

    if max_dat < width:
        # Don't need to normalize if the max value
        # is less than the width we allow.
        return off_data

    # max_dat / width is the value for a single tick. norm_factor is the
    # inverse of this value
    # If you divide a number to the value of single tick, you will find how
    # many ticks it does contain basically.
    norm_factor = width / float(max_dat)
    normal_dat = []
    for dat in off_data:
        normal_dat.append([_v * norm_factor for _v in dat])

    return normal_dat

def horiz_rows(labels, data, normal_dat, args, colors):
    """Prepare the horizontal graph.
       Each row is printed through the print_row function."""
    val_min = find_min(data)

    for i in range(len(labels)):
        if args['no_labels']:
            # Hide the labels.
            label = ''
        else:
            label = "{:<{x}}: ".format(labels[i],
                                       x=find_max_label_length(labels))

        values = data[i]
        num_blocks = normal_dat[i]

        for j in range(len(values)):
            # In Multiple series graph 1st category has label at the beginning,
            # whereas the rest categories have only spaces.
            if j > 0:
                len_label = len(label)
                label = ' ' * len_label
            tail = ' {}{}'.format(args['format'].format(values[j]),
                                  args['suffix'])
            if colors:
                color = colors[j]
            else:
                color = None

            if not args['vertical']:
                print(label, end="")

            yield(values[j], int(num_blocks[j]), val_min, color)

            if not args['vertical']:
                print(tail)

# Prints a row of the horizontal graph.
def print_row(value, num_blocks, val_min, color):
    """A method to print a row for a horizontal graphs.

    i.e:
    1: ▇▇ 2
    2: ▇▇▇ 3
    3: ▇▇▇▇ 4
    """
    if color:
        sys.stdout.write(f'\033[{color}m') # Start to write colorized.

    if num_blocks < 1 and (value > val_min or value > 0):
        # Print something if it's not the smallest
        # and the normal value is less than one.
        sys.stdout.write(SM_TICK)
    else:
        for _ in range(num_blocks):
            sys.stdout.write(TICK)

    if color:
        sys.stdout.write('\033[0m') # Back to original.

def stacked_graph(labels, data, normal_data, len_categories, args, colors):
    """Prepare the horizontal stacked graph.
       Each row is printed through the print_row function."""
    val_min = find_min(data)

    for i in range(len(labels)):
        if args['no_labels']:
            # Hide the labels.
            label = ''
        else:
            label = "{:<{x}}: ".format(labels[i],
                                       x=find_max_label_length(labels))

        print(label, end="")
        values = data[i]
        num_blocks = normal_data[i]

        for j in range(len(values)):
            print_row(values[j], int(num_blocks[j]), val_min, colors[j])

        tail = ' {}{}'.format(args['format'].format(sum(values)),
                              args['suffix'])
        print(tail)

value_list, zipped_list, vertical_list, maxi = [], [], [], 0

def vertically(value, num_blocks, val_min, color, args):
    """Prepare the vertical graph.
       The whole graph is printed through the print_vertical function."""
    global maxi, value_list

    value_list.append(str(value))

    # In case the number of blocks at the end of the normalization is less
    # than the default number, use the maxi variable to escape.
    if maxi < num_blocks:
        maxi = num_blocks

    if num_blocks > 0:
        vertical_list.append((TICK * num_blocks))
    else:
        vertical_list.append(SM_TICK)

    # Zip_longest method in order to turn them vertically.
    for row in zip_longest(*vertical_list, fillvalue='  '):
        zipped_list.append(row)

    counter, result_list = 0, []

    # Combined with the maxi variable, escapes the appending method at
    # the correct point or the default one (width).
    for i in reversed(zipped_list):
        result_list.append(i)
        counter += 1

        if maxi == args['width']:
            if counter == (args['width']):
                break
        else:
            if counter == maxi:
                break

    # Return a list of rows which will be used to print the result vertically.
    return result_list

def print_vertical(vertical_rows, labels, color, args):
    """Print the whole vertical graph."""
    if color:
        sys.stdout.write(f'\033[{color}m') # Start to write colorized.

    for row in vertical_rows:
        print(*row)

    sys.stdout.write('\033[0m') # End of printing colored

    print("-" * len(row) + "Values" + "-" * len(row))
    # Print Values
    for value in zip_longest(*value_list, fillvalue=' '):
        print("  ".join(value))

    if args['no_labels'] == False:
        print("-" * len(row) + "Labels" + "-" * len(row))
        # Print Labels
        for label in zip_longest(*labels, fillvalue=''):
            print("  ".join(label))

def chart(colors, data, args, labels):
    """Handle the normalization of data and the printing of the graph."""
    len_categories = len(data[0])
    if len_categories > 1:
        # Stacked graph
        if args['stacked']:
            normal_dat = normalize(data, args['width'])
            stacked_graph(labels, data, normal_dat, len_categories,
                          args, colors)
            return

        if not colors:
            colors = [None] * len_categories

        # Multiple series graph with different scales
        # Normalization per category
        if args['different_scale']:
            for i in range(len_categories):
                cat_data = []
                for dat in data:
                    cat_data.append([dat[i]])

                # Normalize data, handle negatives.
                normal_cat_data = normalize(cat_data, args['width'])

                # Generate data for a row.
                for row in horiz_rows(labels, cat_data, normal_cat_data,
                                      args, [colors[i]]):
                    # Print the row
                    if not args['vertical']:
                        print_row(*row)
                    else:
                        vertic = vertically(*row, args=args)

                # Vertical graph
                if args['vertical']:
                    print_vertical(vertic, labels, colors[i], args)

                print()
                value_list.clear(), zipped_list.clear(), vertical_list.clear()
                return

    # One category/Multiple series graph with same scale
    # All-together normalization
    if not args['stacked']:
        normal_dat = normalize(data, args['width'])
        for row in horiz_rows(labels, data, normal_dat, args, colors):
            if not args['vertical']:
                print_row(*row)
            else:
                vertic = vertically(*row, args=args)

        if args['vertical'] and len_categories == 1:
            if colors:
                color = colors[0]
            else:
                color = None

            print_vertical(vertic, labels, color, args)

        print()

def check_data(labels, data, args):
    """Check that all data were inserted correctly. Return the colors."""
    len_categories = len(data[0])

    # Check that there are data for all labels.
    if len(labels) != len(data):
        print(">> Error: Label and data array sizes don't match")
        sys.exit(1)

    # Check that there are data for all categories per label.
    for dat in data:
        if len(dat) != len_categories:
            print(">> Error: There are missing values")
            sys.exit(1)

    colors = []

    # If user inserts colors, they should be as many as the categories.
    if args['color'] is not None:
        if len(args['color']) != len_categories:
            print(">> Error: Color and category array sizes don't match")
            sys.exit(1)

        for color in args['color']:
            colors.append(AVAILABLE_COLORS.get(color))

    # Vertical graph for multiple series of same scale is not supported yet.
    if args['vertical'] and len_categories > 1 and not args['different_scale']:
        print(">> Error: Vertical graph for multiple series of same "
              "scale is not supported yet.")
        sys.exit(1)

    # If user hasn't inserted colors, pick the first n colors
    # from the dict (n = number of categories).
    if args['stacked'] and not colors:
        colors = [v for v in list(AVAILABLE_COLORS.values())[:len_categories]]

    return colors

def print_categories(categories, colors):
    """Print a tick and the category's name for each category above
       the graph."""
    for i in range(len(categories)):
        if colors:
            sys.stdout.write(f'\033[{colors[i]}m') # Start to write colorized.

        sys.stdout.write(TICK + ' ' + categories[i] + '  ')
        if colors:
            sys.stdout.write('\033[0m') # Back to original.

    print('\n\n')

def read_data(args):
    """Read data from a file or stdin and returns it.

       Filename includes (categories), labels and data.
       We append categories and labels to lists.
       Data are inserted to a list of lists due to the categories.

       i.e.
       labels = ['2001', '2002', '2003', ...]
       categories = ['boys', 'girls']
       data = [ [20.4, 40.5], [30.7, 100.0], ...]"""
    filename = args['filename']
    stdin = filename == '-'

    if args['verbose']:
        print(f'>> Reading data from {( "stdin" if stdin else filename )}')

    print('')
    if args['title']:
        print('# ' + args['title'] + '\n')

    categories, labels, data, colors = ([] for i in range(4))

    f = sys.stdin if stdin else open(filename, "r")
    for line in f:
        line = line.strip()
        if line:
            if not line.startswith('#'):
                if line.find(DELIM) > 0:
                    cols = line.split(DELIM)
                else:
                    cols = line.split()

                # Line contains categories.
                if line.startswith('@'):
                    cols[0] = cols[0].replace("@ ", "")
                    categories = cols

                # Line contains label and values.
                else:
                    labels.append(cols[0].strip())
                    data_points = []
                    for i in range(1, len(cols)):
                        data_points.append(float(cols[i].strip()))

                    data.append(data_points)
    f.close()

    # Check that all data are valid. (i.e. There are no missing values.)
    colors = check_data(labels, data, args)
    if categories:
        # Print categories' names above the graph.
        print_categories(categories, colors)

    return categories, labels, data, colors

def calendar_heatmap(data, labels, args):
    """Print a calendar heatmap."""
    if args['color']:
        colornum = AVAILABLE_COLORS.get(args['color'][0])
    else:
        colornum = AVAILABLE_COLORS.get('blue')

    dt_dict = {}
    for i in range(len(labels)):
        dt_dict[labels[i]] = data[i][0]

    # get max value
    max_val = float(max(data)[0])

    tick_1 = "░"
    tick_2 = "▒"
    tick_3 = "▓"
    tick_4 = "█"

    if args['custom_tick']:
        tick_1 = tick_2 = tick_3 = tick_4 = args['custom_tick']

    # check if start day set, otherwise use one year ago
    if args['start_dt']:
        start_dt = datetime.strptime(args['start_dt'], '%Y-%m-%d')
    else:
        start = datetime.now()
        start_dt = datetime(year=start.year-1, month=start.month,
                            day=start.day)

    # modify start date to be a Monday, subtract weekday() from day
    start_dt = start_dt - timedelta(start_dt.weekday())

    # TODO: legend doesn't line up properly for all start dates/data
    # top legend for months
    sys.stdout.write("     ")
    for month in range(13):
        month_dt = datetime(year=start_dt.year, month=start_dt.month, day=1) +\
                   timedelta(days=month*31)
        sys.stdout.write(month_dt.strftime("%b") + " ")
        if args['custom_tick']: #assume custom tick is emoji which is one wider
            sys.stdout.write(" ")

    sys.stdout.write('\n')

    for day in range(7):
        sys.stdout.write(DAYS[day] + ': ')
        for week in range(53):
            day_ = start_dt + timedelta(days=day + week*7)
            day_str = day_.strftime("%Y-%m-%d")

            if day_str in dt_dict and dt_dict[day_str] != 0.0:
                if dt_dict[day_str] > max_val * 0.75:
                    tick = tick_4
                elif dt_dict[day_str] > max_val * 0.50:
                    tick = tick_3
                elif dt_dict[day_str] > max_val * 0.25:
                    tick = tick_2
                else:
                    tick = tick_1
            else:
                tick = ' '

            if colornum:
                sys.stdout.write(f'\033[{colornum}m')

            sys.stdout.write(tick)
            if colornum:
                sys.stdout.write('\033[0m')

        sys.stdout.write('\n')


if __name__ == "__main__":
    main()
