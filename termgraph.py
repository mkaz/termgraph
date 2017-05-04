#!/usr/bin/env python
# coding=utf-8

# termgraph.py - draw basic graphs on terminal
# https://github.com/mkaz/termgraph

# Marcus Kazmierczak
# http://mkaz.com/

from __future__ import print_function

import argparse
import sys

# TODO: change tick character
tick = '▇'
sm_tick = '|'

# sample bar chart data
# labels = ['2007', '2008', '2009', '2010', '2011']
# data = [183.32, 231.23, 16.43, 50.21, 508.97]

try:
    range = xrange
except NameError:
    pass


def main(args):
    # determine type of graph

    # read data
    labels, data = read_data(args['filename'], args['title'], args['no_title'])

    chart(labels, data, args)


def chart(labels, data, args):

    # verify data
    m = len(labels)
    if m != len(data):
        print(">> Error: Label and data array sizes don't match")
        sys.exit(1)

    # massage data
    # normalize for graph
    max = 0
    for i in range(m):
        if data[i] > max:
            max = data[i]

    label_width = 0
    for label in labels:
        label_width = max(label_width, len(label))

    step = max / args['width']
    # display graph
    for i in range(m):
        print_blocks(labels[i], data[i], step, args, label_width)

    print()


def print_blocks(label, count, step, args, label_width):
    # TODO: add flag to hide data labels
    blocks = int(count / step)
    print("{}: {}".format(label, ' ' * label_width), end="")
    if count < step:
        sys.stdout.write(sm_tick)
    else:
        for i in range(blocks):
            sys.stdout.write(tick)

    print(args['format'].format(count) + args['suffix'])


def init():
    parser = argparse.ArgumentParser(description='draw basic graphs on terminal')
    parser.add_argument('--no-title', action='store_true',
                        help='Does not print title. Overrides --title.')
    parser.add_argument('--title', help='Title of graph')
    parser.add_argument('filename', nargs='?', default="-",
                        help='data file name (comma or space separated). Defaults to stdin.')
    parser.add_argument('--width', type=int, default=50,
                        help='width of graph in characters default:50')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--format', default='{:>5.0f}',
                        help='format specifier to use.')
    parser.add_argument('--suffix', default='',
                        help='string to add as a suffix to all data points.')
    args = vars(parser.parse_args())
    return args


def read_data(filename, title, no_title):
    # TODO: add verbose flag
    stdin = filename == '-'

    if not no_title:
        print("------------------------------------")
        if title:
            print(title)
        else:
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
    return labels, data


if __name__ == "__main__":
    args = init()
    main(args)
