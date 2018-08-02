#!/usr/bin/env python3
# coding=utf-8

# termgraph.py - draw basic graphs on terminal
# https://github.com/mkaz/termgraph

from __future__ import print_function
from colorama import init
from itertools import *
from datetime import datetime
from datetime import timedelta
import random

import argparse
import sys

VERSION='0.1.3'

init()

# ANSI escape SGR Parameters color codes
available_colors = {
    'red': 91,
    'blue': 94,
    'green': 92,
    'magenta': 95,
    'yellow': 93,
    'black': 90,
    'cyan': 96
}

dow = [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ]
DELIM = ','
TICK = '▇'
SM_TICK = '▏'

try:
    range = xrange
except NameError:
    pass

# Parses and returns arguments.
def initArgs():
    parser = argparse.ArgumentParser( description='draw basic graphs on terminal' )
    parser.add_argument( 'filename', nargs='?', default="-", help='data file name (comma or space separated). Defaults to stdin.' )
    parser.add_argument( '--title', help='Title of graph' )
    parser.add_argument( '--width', type=int, default=50, help='width of graph in characters default:50' )
    parser.add_argument( '--format', default='{:<5.2f}', help='format specifier to use.' )
    parser.add_argument( '--suffix', default='', help='string to add as a suffix to all data points.' )
    parser.add_argument( '--no-labels', action='store_true', help='Do not print the label column' )
    parser.add_argument( '--color', nargs='*', choices=available_colors, help='Graph bar color( s )' )
    parser.add_argument( '--vertical', action= 'store_true', help='Vertical graph' )
    parser.add_argument( '--stacked', action='store_true', help='Stacked bar graph' )
    parser.add_argument( '--different-scale', action='store_true', help='Categories have different scales.' )
    parser.add_argument( '--calendar', action='store_true', help='Calendar Heatmap chart' )
    parser.add_argument( '--start-dt', help='Start date for Calendar chart' )
    parser.add_argument( '--custom-tick', default='', help='Custom tick mark, emoji approved' )
    parser.add_argument( '--delim', default='', help='Custom delimiter, default , or space' )
    parser.add_argument( '--verbose', action='store_true', help='Verbose output, helpful for debugging' )
    parser.add_argument( '--version', action='store_true', help='Display version and exit' )
    args = vars( parser.parse_args() )

    if args['custom_tick'] != '':
        global TICK, SM_TICK
        TICK = args['custom_tick']
        SM_TICK = ''

    if args['delim'] != '':
        global DELIM
        DELIM = args['delim']

    return args


# Main function
def main():
    args = initArgs()

    if args['version']:
        print('termgraph v{}'.format( VERSION ))
        sys.exit()

    categories, labels, data, colors = read_data( args )
    if args['calendar']:
        calendar_heatmap( data, labels, args )
    else:
        chart( colors, data, args, labels )

# Return minimum value in list of list
def findMin( a ):
    return min( [b[-1] for b in a] )

# Return maximum value in list of list
def findMax( a ):
    return max( [b[-1] for b in a] )

# Return maximum length for lebels
def findMaxLabelLength( a ):
    s = 0
    for i in range( len( a ) ):
        if ( len( a[i] ) > s ):
            s = len( a[i] )
    return s

# Normalizes data and returns them.
def normalize( data, width ):
    min_dat = findMin( data )
    # We offset by the minimum if there's a negative.
    off_data = []
    if min_dat < 0:
        min_dat = abs( min_dat )
        for dat in data:
            off_data.append( [_d + min_dat for _d in dat] )
    else:
        off_data = data
    min_dat = findMin( off_data )
    max_dat = findMax( off_data )

    if max_dat < width:
        # Don't need to normalize if the max value
        # is less than the width we allow.
        return off_data

    norm_factor = width / float( max_dat - min_dat )
    normal_dat = []
    for dat in off_data:
        normal_dat.append( [ ( _v - min_dat ) * norm_factor for _v in dat ] )
    return normal_dat

# Prepares the horizontal graph.
# Each row is printed through print_row function.
def horiontal_rows( labels, data, normal_dat, args, colors ):
    val_min = findMin( data )

    for i in range( len( labels ) ):
        if args['no_labels']:
            # Hide the labels.
            label = ''
        else:
            label = "{:<{x}}: ".format( labels[i], x=findMaxLabelLength( labels ) )

        values = data[i]
        num_blocks = normal_dat[i]

        for j in range( len( values ) ):
            # In Multiple series graph 1st category has label at the beginning,
            # whereas the rest categories have only spaces.
            if j > 0:
                len_label = len( label )
                label = ' ' * len_label
            tail = ' {}{}'.format( args['format'].format( values[j] ), args['suffix'] )
            if colors:
                color = colors[j]
            else:
                color = None
            if not args['vertical']:
                print( label, end="" )
            yield ( values[j], int( num_blocks[j] ), val_min, color )
            if not args['vertical']:
                print( tail )

# Prints a row of the horizontal graph.
def print_row(value, num_blocks, val_min, color):
    """A method to print a row for a horizontal graphs.

    i.e:
    1: ▇▇ 2
    2: ▇▇▇ 3
    3: ▇▇▇▇ 4
    """
    if color:
        sys.stdout.write( f'\033[{color}m' ) # Start to write colorized.
    if num_blocks < 1 and (value > val_min or value > 0):
        # Print something if it's not the smallest
        # and the normal value is less than one.
        sys.stdout.write( SM_TICK )
    else:
        for _ in range( num_blocks ):
            sys.stdout.write( TICK )
    if color:
        sys.stdout.write( '\033[0m' ) # Back to original.

# Prepares the horizontal Stacked graph.
# Each row is printed through print_row function.
def stacked_graph( labels, data, normal_data, len_categories, args, colors ):
    val_min = findMin( data )

    for i in range( len( labels ) ):
        if args['no_labels']:
            # Hide the labels.
            label = ''
        else:
            label = "{}: ".format( labels[i] )
        print( label, end="" )
        values = data[i]
        num_blocks = normal_data[i]

        for j in range( len( values ) ):
            print_row( values[j], int(num_blocks[j]), val_min, colors[j] )
        tail = ' {}{}'.format( args['format'].format(sum(values)), args['suffix'] )
        print( tail )

value_list, zipped_list, vertical_list, maxi = [], [], [], 0

# Prepares the vertical graph.
# The whole graph is printed through the print_vertical function.
def vertically( value, num_blocks, val_min, color ):
    global maxi, value_list

    value_list.append( str( value ) )
    # In case the number of blocks at the end of the normalization is less
    # than the default number, use the maxi variable to escape.
    if maxi < num_blocks:
        maxi = num_blocks

    if num_blocks > 0:
        vertical_list.append( ( TICK * num_blocks ) )
    else:
        vertical_list.append( SM_TICK )
    # Zip_longest method in order to turn them vertically.
    for row in zip_longest( *vertical_list, fillvalue='  ' ):
        zipped_list.append( row )

    counter, result_list = 0, []
    # Combined with the maxi variable, escapes the appending method at
    # the correct point or the default one (width).
    for i in reversed( zipped_list ):
        result_list.append( i )
        counter+=1

        if maxi == args['width']:
            if counter==( args['width'] ):
                break
        else:
            if counter == maxi:
                break
    # Return a list of rows which will be used to print the result vertically.
    return result_list

# Prints the whole vertical graph.
def print_vertical( vertical_rows, labels, color, args ):

    if color:
        sys.stdout.write( f'\033[{color}m' ) # Start to write colorized.

    for j in vertical_rows:
        print(*j)
    sys.stdout.write( '\033[0m' ) # End of printing colored

    print( "-" * len( j ) + "Values" + "-" * len( j ) )
    # Print Values
    for l in zip_longest( *value_list, fillvalue=' ' ):
        print( "  ".join( l ) )
    if args['no_labels'] == False:
        print( "-" * len( j ) + "Labels" + "-" * len( j ) )
        # Print Labels
        for k in zip_longest( *labels,fillvalue='' ):
            print( "  ".join( k ) )

# Handles the normalization of data and the print of the graph.
def chart( colors, data, args, labels ):
    len_categories = len( data[0] )
    if len_categories > 1:
        # Stacked graph
        if args['stacked']:
            normal_dat = normalize( data, args['width'] )
            stacked_graph( labels, data, normal_dat, len_categories, args, colors )
        else:
            if not colors:
                colors = [None] * len_categories
            # Multiple series graph with different scales
            # Normalization per category
            if args['different_scale']:
                for i in range( len_categories ):
                    category_data = []
                    for dat in data:
                        category_data.append( [dat[i]] )
                    # Normalize data, handle negatives.
                    normal_category_data = normalize( category_data, args['width'] )
                    # Generate data for a row.
                    for row in horiontal_rows( labels, category_data, normal_category_data, args, [ colors[i] ] ):
                        # Print the row
                        if not args['vertical']:
                            print_row( *row )
                        else:
                            vertic = vertically( *row )
                    # Vertical graph
                    if args['vertical']:
                        print_vertical( vertic, labels, colors[i], args )
                    print()
                    value_list.clear(), zipped_list.clear(), vertical_list.clear()
    # One category/Multiple series graph with same scale
    # All-together normalization
    if len_categories == 1 or not args['different_scale']:
        if not args['stacked']:
            normal_dat = normalize( data, args['width'] )
            for row in horiontal_rows( labels, data, normal_dat, args, colors ):
                if not args['vertical']:
                    print_row( *row )
                else:
                    vertic = vertically( *row )
            if args['vertical'] and len_categories == 1:
                if colors:
                    color = colors[0]
                else:
                    color = None
                print_vertical( vertic, labels, color, args )
            print()

# Checks that all data were inserted correctly and returns colors.
def check_data( labels, data, args ):
    len_categories = len( data[0] )
    # Check that there are data for all labels.
    if len( labels ) != len( data ):
        print(">> Error: Label and data array sizes don't match")
        sys.exit( 1 )
    # Check that there are data for all categories per label.
    for dat in data:
        if len( dat ) != len_categories:
            print( ">> Error: There are missing values" )
            sys.exit( 1 )
    colors = []
    # If user inserts colors, they should be as many as the categories.
    if args['color'] is not None:
        if len( args['color'] ) != len_categories:
            print( ">> Error: Color and category array sizes don't match" )
            sys.exit( 1 )
        for c in args['color']:
            colors.append( available_colors.get( c ) )
    # Vertical graph for multiple series of same scale is not supported yet.
    if args['vertical'] and len_categories > 1 and not args['different_scale']:
        print( ">> Error: Vertical graph for multiple series of same scale is not supported yet." )
        sys.exit( 1 )
    # If user hasn't inserted colors, pick the first n colors
    # from the dict (n = number of categories).
    if args['stacked'] and not colors:
        colors = [v for v in list( available_colors.values() )[:len_categories]]
    return colors

# Prints a tick and the category's name for each category above the graph.
def print_categories( categories, colors ):
    for i in range( len( categories ) ):
        if colors:
            sys.stdout.write( f'\033[{colors[i]}m' ) # Start to write colorized.
        sys.stdout.write( TICK + ' ' + categories[i] + '  ' )
        sys.stdout.write( '\033[0m' ) # Back to original.
    print( '\n\n' )

# Reads data from a file or stdin and returns them.
def read_data( args ):
    '''
    Filename includes (categories), labels and data.
    We append categories and labels to lists.
    Data are inserted to a list of lists due to the categories.

    i.e.
    labels = ['2001', '2002', '2003', ...]
    categories = ['boys', 'girls']
    data = [ [20.4, 40.5], [30.7, 100.0], ...]
    '''
    filename = args['filename']
    stdin = filename == '-'

    if args['verbose']:
        print( f'>> Reading data from {( "stdin" if stdin else filename )}' )

    print('')
    if args['title']:
        print( '# ' + args['title'] + '\n'  )

    categories, labels, data, colors = ( [] for i in range(4) )

    f = sys.stdin if stdin else open( filename, "r" )
    for line in f:
        line = line.strip()
        if line:
            if not line.startswith( '#' ):
                if line.find( DELIM ) > 0:
                    cols = line.split( DELIM )
                else:
                    cols = line.split()
                # Line contains categories.
                if line.startswith( '@' ):
                    cols[0] = cols[0].replace( "@ ", "" )
                    categories = cols
                # Line contains label and values.
                else:
                    labels.append( cols[0].strip() )
                    data_points = []
                    for i in range( 1, len( cols ) ):
                        data_points.append( float( cols[i].strip() ) )
                    data.append( data_points )
    f.close()

    # Check that all data are valid. (i.e. There are no missing values.)
    colors = check_data( labels, data, args )
    if categories:
        # Print categories' names above the graph.
        print_categories( categories, colors )

    return categories, labels, data, colors

def calendar_heatmap( data, labels, args ):
    if args['color']:
        colornum = available_colors.get( args['color'][0] )
    else:
        colornum = available_colors.get( 'blue' )

    dtdict = {}
    for i in range( len( labels ) ):
       dtdict[ labels[i] ] = data[i][0]

    # get max value
    maxval = float( max( data )[0] )

    TICK_1 = "░"
    TICK_2 = "▒"
    TICK_3 = "▓"
    TICK_4 = "█"

    if args['custom_tick']:
        TICK_1 = TICK_2 = TICK_3 = TICK_4 = args['custom_tick']

    # check if start day set, otherwise use one year ago
    if args['start_dt']:
        st_day = datetime.strptime(args['start_dt'], '%Y-%m-%d')
    else:
        st = datetime.now()
        st_day = datetime(year=st.year-1, month=st.month, day=st.day)

    # modify start date to be a Monday, subtract weekday() from day
    st_day = st_day - timedelta( st_day.weekday() )

    # TODO: legend doesn't line up properly for all start dates/data
    # top legend for months
    sys.stdout.write( "     " )
    for mo in range( 13 ):
        mo_dt = datetime(year=st_day.year, month=st_day.month, day=1) + timedelta( days=mo*31 )
        sys.stdout.write( mo_dt.strftime( "%b" ) + " " )
        if args['custom_tick']: #assume custom tick is emoji which is one wider
            sys.stdout.write(" ")
    sys.stdout.write( '\n' )

    for day in range( 7 ):
        sys.stdout.write( dow[ day ] + ': ' )
        for week in range( 53 ):
            d = st_day + timedelta( days=day + week*7 )
            dstr = d.strftime( "%Y-%m-%d" )

            if dstr in dtdict:
                if dtdict[dstr] > maxval * 0.75:
                    T = TICK_4
                elif dtdict[dstr] > maxval * 0.50:
                    T = TICK_3
                elif dtdict[dstr] > maxval * 0.25:
                    T = TICK_2
                else:
                    T = TICK_1
            else:
                T = ' '

            if colornum:
                sys.stdout.write( f'\033[{colornum}m' )
            sys.stdout.write( T )
            if colornum:
                sys.stdout.write( '\033[0m' )
        sys.stdout.write( '\n' )


if __name__ == "__main__":
    main()
