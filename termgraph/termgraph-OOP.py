#!/usr/bin/env python3
# coding=utf-8
"""This module allows drawing basic graphs in the terminal."""

# termgraph.py - draw basic graphs on terminal
# https://github.com/mkaz/termgraph

from __future__ import print_function
import argparse
import sys
import math
from datetime import datetime, timedelta
from itertools import zip_longest
from colorama import init
import os
import re

VERSION = "0.4.2"

init()

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DELIM = ","
TICK = "▇"
SM_TICK = "▏"

# Commented it out cause I don't know what its purpose is.
# And the code was running just fine without it.
# I am sorry if I am being stupid here.
# try:
#     range = xrange
# except NameError:
#     pass

class Colors:
    # ANSI escape SGR Parameters color codes
    red = 91
    green = 92
    yellow = 93
    blue = 94
    magenta = 95
    cyan = 96

def init_args():
    """Parse and return the arguments."""
    parser = argparse.ArgumentParser(description="draw basic graphs on terminal")
    parser.add_argument(
        "filename",
        nargs="?",
        default="-",
        help="data file name (comma or space separated). Defaults to stdin.",
    )
    parser.add_argument("--title", help="Title of graph")
    parser.add_argument(
        "--width", type=int, default=50, help="width of graph in characters default:50"
    )
    parser.add_argument("--format", default="{:<5.2f}", help="format specifier to use.")
    parser.add_argument(
        "--suffix", default="", help="string to add as a suffix to all data points."
    )
    parser.add_argument(
        "--no-labels", action="store_true", help="Do not print the label column"
    )
    parser.add_argument(
        "--no-values", action="store_true", help="Do not print the values at end"
    )
    parser.add_argument(
        "--space-between", action="store_true", help="Print a new line after every field"
    )
    parser.add_argument("--color", nargs="*", help="Graph bar color( s )")
    parser.add_argument("--vertical", action="store_true", help="Vertical graph")
    parser.add_argument("--stacked", action="store_true", help="Stacked bar graph")
    parser.add_argument("--histogram", action="store_true", help="Histogram")
    parser.add_argument("--bins", default=5, type=int, help="Bins of Histogram")
    parser.add_argument(
        "--different-scale",
        action="store_true",
        help="Categories have different scales.",
    )
    parser.add_argument(
        "--calendar", action="store_true", help="Calendar Heatmap chart"
    )
    parser.add_argument("--start-dt", help="Start date for Calendar chart")
    parser.add_argument(
        "--custom-tick", default="", help="Custom tick mark, emoji approved"
    )
    parser.add_argument(
        "--delim", default="", help="Custom delimiter, default , or space"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Verbose output, helpful for debugging"
    )
    parser.add_argument(
        "--label-before",
        action="store_true",
        default=False,
        help="Display the values before the bars",
    )
    parser.add_argument(
        "--version", action="store_true", help="Display version and exit"
    )
    if len(sys.argv) == 1:
        if sys.stdin.isatty():
            parser.print_usage()
            sys.exit(2)

    args = vars(parser.parse_args())

    if args["custom_tick"] != "":
        global TICK, SM_TICK
        TICK = args["custom_tick"]
        SM_TICK = ""

    if args["delim"] != "":
        global DELIM
        DELIM = args["delim"]

    return args

def main():
    """Main function."""
    args = init_args()

    if args["version"]:
        print("termgraph v{}".format(VERSION))
        sys.exit()

    _, labels, data, colors = read_data(args)
    if args["calendar"]:
        calendar_heatmap(data, labels, args)
    else:
        chart(colors, data, args, labels)
