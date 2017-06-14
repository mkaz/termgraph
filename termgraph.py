#!/usr/bin/env python
# coding=utf-8

# termgraph.py - draw basic graphs on terminal
# https://github.com/mkaz/termgraph

# Marcus Kazmierczak
# http://mkaz.com/

from __future__ import print_function

import argparse
import sys

# TODO: change TICK character
TICK = '▇'
SM_TICK = '|'

# sample bar chart data
# labels = ['2007', '2008', '2009', '2010', '2011']
# data = [183.32, 231.23, 16.43, 50.21, 508.97]

try:
    range = xrange
except NameError:
    pass


def normalize(data, width):
    min_dat = min(data)
    # We offset by the mininum if there's a negative
    if min_dat < 0:
        min_dat = abs(min_dat)
        off_data = [_d + min_dat for _d in data]
    else:
        off_data = data
    min_dat = min(off_data)
    max_dat = max(off_data)

    if max_dat < width:
        # Don't need to normalize if the max value
        # is less than the width we allow.
        return off_data

    avg_dat = sum(off_data) / float(len(off_data))
    norm_factor = width / float(max_dat - min_dat)

    normal_dat = [(_v - min_dat) * norm_factor for _v in off_data]
    return normal_dat

def horiontal_rows(labels, data, normal_dat, args):
    val_min = min(data)
    for i in range(len(labels)):
        if args['ignore_labels']:
            # Hide the labels.
            label = ''
        else:
            label = "{}: ".format(labels[i])

        value = data[i]
        num_blocks = normal_dat[i]
        tail = ' {}{}'.format(args['format'].format(value), args['suffix'])
        yield (label, value, int(num_blocks), val_min, tail)

def print_row(label, value, num_blocks, val_min, tail):
    """A method to print a row for a horizontal graphs.

    i.e:
    1: ▇▇ 2
    2: ▇▇▇ 3
    3: ▇▇▇▇ 4
    """
    print(label, end="")
    if num_blocks < 1 and (value > val_min or value > 0):
        # Print something if it's not the smallest
        # and the normal value is less than one.
        sys.stdout.write(SM_TICK)
    else:
        for i in range(num_blocks):
            sys.stdout.write(TICK)
    print(tail)

def chart(labels, data, args):
    # Normalize data, handle negatives.
    normal_dat = normalize(data, args['width'])

    # Generate data for a row.
    for row in horiontal_rows(labels, data, normal_dat, args):
        # Print the row
        print_row(*row)

def main(args):
    # determine type of graph

    # read data
    labels, data = read_data(args['filename'])

    # Normalize data, handle negatives.
    normal_dat = normalize(data, args['width'])

    # Generate data for a row.
    for row in horiontal_rows(labels, data, normal_dat, args):
        # Print the row
        print_row(*row)


def init():
    parser = argparse.ArgumentParser(description='draw basic graphs on terminal')
    parser.add_argument('filename', nargs='?', default="-",
                        help='data file name (comma or space separated). Defaults to stdin.')
    parser.add_argument('--width', type=int, default=50,
                        help='width of graph in characters default:50')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--format', default='{:<5.2f}',
                        help='format specifier to use.')
    parser.add_argument('--suffix', default='',
                        help='string to add as a suffix to all data points.')
    parser.add_argument('--ignore-labels', action='store_true',
                        help='Do not print the label column')
    args = vars(parser.parse_args())
    return args


def read_data(filename):
    """Read filename as tuple of two lists.

    Read file:
    label1 1
    label2 2

    Return:
    (['label1', 'label2'], [1.0, 2.0])
    """
    # TODO: add verbose flag
    stdin = filename == '-'

    print("------------------------------------")
    print("Reading data from", ("stdin" if stdin else filename))
    print("------------------------------------\n")

    labels = []
    data = []

    f = sys.stdin if stdin else open(filename, "r")
    for line in f:
        line = line.strip()
        if line:
            if not line.startswith('#'):
                if line.find(",") > 0:
                    cols = line.split(',')
                else:
                    cols = line.split()
                labels.append(cols[0].strip())
                data_point = cols[1].strip()
                data.append(float(data_point))

    f.close()
    if len(labels) != len(data):
        print(">> Error: Label and data array sizes don't match")
        sys.exit(1)
    return labels, data


if __name__ == "__main__":
    args = init()
    main(args)
