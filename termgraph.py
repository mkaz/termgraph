#!/usr/bin/env python
# coding=utf-8

# termgraph.py - draw basic graphs on terminal
# https://github.com/mkaz/termgraph

# Marcus Kazmierczak
# http://mkaz.com/


import argparse
import sys

#TODO: change tick character
tick = '▇'
sm_tick = '|'

# sample bar chart data
#labels = ['2007', '2008', '2009', '2010', '2011']
#data = [183.32, 231.23, 16.43, 50.21, 508.97]

#TODO: parameterize width
width = 50

def main():

    # determine type of graph
    
    # read data
    if (args['filename']):
        labels, data = read_data(args['filename'])
    else:
        # shouldn't happen since argparse covers empty case
        print ">> Error: No data file specified"
        sys.exit(1)

    # verify data
    m = len(labels)
    if m != len(data):
        print ">> Error: Label and data array sizes don't match"
        sys.exit(1)

    # massage data
    ## normalize for graph
    max = 0
    for i in xrange(m):
        if data[i] > max:
            max = data[i]

    step = max / width
    # display graph
    for i in xrange(m):
        print_blocks(labels[i], data[i], step)

    print


def print_blocks(label, count, step):
    #TODO: add flag to hide data labels
    blocks = int(count / step)
    print "{}: ".format(label),
    if count < step:
        sys.stdout.write(sm_tick)
    else:
        for i in xrange(blocks):
            sys.stdout.write(tick)

    print "{:>7.2f}".format(count)


def init():
    parser = argparse.ArgumentParser(description='draw basic graphs on terminal')
    parser.add_argument('filename', nargs=1, help='data file name (comma or space separated)')
    args = vars(parser.parse_args())
    args['filename'] = args['filename'][0]  # returns as list, we dont want that
    return args


def read_data(filename):
    #TODO: add verbose flag
    print "------------------------------------"
    print "Reading data from", filename
    print "------------------------------------\n"

    labels = []
    data = []

    f = open(filename, "r")
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
    main()



