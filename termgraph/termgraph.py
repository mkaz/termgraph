#!/usr/bin/env python3
# coding=utf-8
"""This module allows drawing basic graphs in the terminal."""

# termgraph.py - draw basic graphs on terminal
# https://github.com/mkaz/termgraph

from __future__ import print_function, annotations
from typing import List, Tuple, Dict
import argparse
import sys
import math
from datetime import datetime, timedelta
from itertools import zip_longest
from colorama import init  # type: ignore
import os
import re

VERSION = "0.5.3"

init()

# ANSI escape SGR Parameters color codes
AVAILABLE_COLORS = {
    "red": 91,
    "blue": 94,
    "green": 92,
    "magenta": 95,
    "yellow": 93,
    "black": 90,
    "cyan": 96,
}

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
UNITS = ["", "K", "M", "B", "T"]
DELIM = ","
TICK = "▇"
SM_TICK = "▏"

try:
    range = xrange  # type: ignore
except NameError:
    pass


def init_args() -> Dict:
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
        "--space-between",
        action="store_true",
        help="Print a new line after every field",
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
    parser.add_argument(
        "--percentage", action="store_true", help="Display the number in percentage, as {:.0%}"
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
    try:
        if args["calendar"]:
            calendar_heatmap(data, labels, args)
        else:
            chart(colors, data, args, labels)
    except BrokenPipeError:
        pass


def find_min(data: List):
    """Return the minimum value in sublist of list."""
    return min([min(sublist) for sublist in data])


def find_max(data: List):
    """Return the maximum value in sublist of list."""
    return max([max(sublist) for sublist in data])


def normalize(data: List, width: int) -> List:
    """Normalize the data and return it."""

    # We offset by the minimum if there's a negative.
    data_offset = []
    min_datum = find_min(data)
    if min_datum < 0:
        min_datum = abs(min_datum)
        for datum in data:
            data_offset.append([d + min_datum for d in datum])
    else:
        data_offset = data
    min_datum = find_min(data_offset)
    max_datum = find_max(data_offset)

    if min_datum == max_datum:
        return data_offset

    # max_dat / width is the value for a single tick. norm_factor is the
    # inverse of this value
    # If you divide a number to the value of single tick, you will find how
    # many ticks it does contain basically.
    norm_factor = width / float(max_datum)
    normal_data = []
    for datum in data_offset:
        normal_data.append([v * norm_factor for v in datum])

    return normal_data


def find_max_label_length(labels: List) -> int:
    """Return the maximum length for the labels."""
    return max([len(label) for label in labels])


def cvt_to_readable(num, percentage=False):
    """Return the number in a human readable format

    Eg:
    125000 -> 125.0K
    12550 -> 12.55K
    19561100 -> 19.561M
    """
    if percentage:
      return (num * 100, "%")


    if num != 0:
        neg = num < 0
        num = abs(num)

        # Find the degree of the number like if it is in thousands or millions, etc.
        index = math.floor(math.log(num) / math.log(1000))

        # Converts the number to the human readable format and returns it.
        newNum = round(num / (1000 ** index), 3)
        newNum *= -1 if neg else 1
        degree = UNITS[index]

    else:
        newNum = 0
        degree = UNITS[0]

    return (newNum, degree)


def hist_rows(data: List, args: Dict, colors: List):
    """Prepare the Histgram graph.
    Each row is printed through the print_row function."""

    val_min = find_min(data)
    val_max = find_max(data)

    # Calculate borders
    class_min = math.floor(val_min)
    class_max = math.ceil(val_max)
    class_range = class_max - class_min
    class_width = class_range / args["bins"]

    border = class_min
    borders = []
    max_len = len(str(border))

    for b in range(args["bins"] + 1):
        borders.append(border)
        len_border = len(str(border))
        if len_border > max_len:
            max_len = len_border
        border += class_width
        border = round(border, 1)

    # Count num of data via border
    count_list = []

    for start, end in zip(borders[:-1], borders[1:]):
        count = 0
        #        for d in [d]
        for v in [row[0] for row in data]:
            if start <= v < end:
                count += 1

        count_list.append([count])

    normal_counts = normalize(count_list, args["width"])

    for i, border in enumerate(zip(borders[:-1], borders[1:])):
        if colors:
            color = colors[0]
        else:
            color = None

        if not args.get("no_labels"):
            print("{:{x}} – {:{x}}: ".format(border[0], border[1], x=max_len), end="")

        num_blocks = normal_counts[i]

        yield (count_list[i][0], int(num_blocks[0]), 0, color)

        if args.get("no_values"):
            tail = ""
        else:
            tail = " {}{}".format(
                args["format"].format(count_list[i][0]), args["suffix"]
            )
        print(tail)


def horiz_rows(
    labels: List,
    data: List,
    normal_dat: List,
    args: Dict,
    colors: List,
    doprint: bool = True,
):
    """Prepare the horizontal graph.
    Each row is printed through the print_row function."""
    val_min = find_min(data)

    for i in range(len(labels)):
        if args["no_labels"]:
            # Hide the labels.
            label = ""
        else:
            if args.get("label_before"):
                fmt = "{:<{x}}"
            else:
                fmt = "{:<{x}}: "
            label = fmt.format(labels[i], x=find_max_label_length(labels))

        values = data[i]
        num_blocks = normal_dat[i]

        if args.get("space_between") and i != 0:
            print()

        for j in range(len(values)):
            # In Multiple series graph 1st category has label at the beginning,
            # whereas the rest categories have only spaces.
            if j > 0:
                len_label = len(label)
                label = " " * len_label
            if args.get("label_before"):
                fmt = "{}{}{}"
            else:
                fmt = " {}{}{}"

            if args["no_values"]:
                tail = args["suffix"]
            else:
                val, deg = cvt_to_readable(values[j], percentage=args["percentage"])
                tail = fmt.format(args["format"].format(val), deg, args["suffix"])

            if colors:
                color = colors[j]
            else:
                color = None

            if not args.get("label_before") and not args.get("vertical"):
                print(label, end="")

            yield (
                values[j],
                int(num_blocks[j]),
                val_min,
                color,
                label,
                tail,
                args.get("label_before") and not args.get("vertical"),
            )

            if not args.get("label_before") and not args.get("vertical"):
                print(tail)


# Prints a row of the horizontal graph.
def print_row(
    value,
    num_blocks: int,
    val_min: int,
    color: bool,
    label: bool = False,
    tail: bool = False,
    doprint: bool = False,
):
    """A method to print a row for a horizontal graphs.
    i.e:
    1: ▇▇ 2
    2: ▇▇▇ 3
    3: ▇▇▇▇ 4
    """
    sys.stdout.write("\033[0m")  # no color
    if value == 0.0:
        sys.stdout.write("\033[90m")  # dark gray

    if doprint:
        print(label, tail, " ", end="")

    if (num_blocks < 1 and (value > val_min or value > 0)) or (
        doprint and value == 0.0
    ):
        # Print something if it's not the smallest
        # and the normal value is less than one.
        sys.stdout.write(SM_TICK)
    else:
        if color:
            sys.stdout.write(f"\033[{color}m")  # Start to write colorized.
        for _ in range(num_blocks):
            sys.stdout.write(TICK)

    if color:
        sys.stdout.write("\033[0m")  # Back to original.

    if doprint:
        print()


def stacked_graph(
    labels: List,
    data: List,
    normal_data: List,
    len_categories: int,
    args: Dict,
    colors: List,
):
    """Prepare the horizontal stacked graph.
    Each row is printed through the print_row function."""
    val_min = find_min(data)

    for i in range(len(labels)):
        if args["no_labels"]:
            # Hide the labels.
            label = ""
        else:
            label = "{:<{x}}: ".format(labels[i], x=find_max_label_length(labels))

        if args.get("space_between") and i != 0:
            print()

        print(label, end="")

        values = data[i]
        num_blocks = normal_data[i]

        for j in range(len(values)):
            print_row(values[j], int(num_blocks[j]), val_min, colors[j])

        tail = " {}{}".format(args["format"].format(sum(values)), args["suffix"])
        print(tail)


# FIXME: globals for vertical, not ideal
value_list, zipped_list, vertical_list, maxi = [], [], [], 0


def vertically(value, num_blocks: int, val_min: int, color: bool, args: Dict) -> List:
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
    for row in zip_longest(*vertical_list, fillvalue=" "):
        zipped_list.append(row)

    counter, result_list = 0, []

    # Combined with the maxi variable, escapes the appending method at
    # the correct point or the default one (width).
    for i in reversed(zipped_list):
        result_list.append(i)
        counter += 1

        if maxi == args["width"]:
            if counter == (args["width"]):
                break
        else:
            if counter == maxi:
                break

    # Return a list of rows which will be used to print the result vertically.
    return result_list


def print_vertical(vertical_rows: List, labels: List, color: bool, args: Dict) -> None:
    """Print the whole vertical graph."""
    if color:
        sys.stdout.write(
            "\033[{color}m".format(color=color)
        )  # Start to write colorized.

    for row in vertical_rows:
        print(*row)

    sys.stdout.write("\033[0m")  # End of printing colored

    if not args["no_values"]:
        print("-" * len(row) + "Values" + "-" * len(row))
        for value in zip_longest(*value_list, fillvalue=" "):
            print("  ".join(value))

    if not args["no_labels"]:
        print("-" * len(row) + "Labels" + "-" * len(row))
        # Print Labels
        for label in zip_longest(*labels, fillvalue=""):
            print("  ".join(label))


def chart(colors: List, data: List, args: Dict, labels: List) -> None:
    """Handle the normalization of data and the printing of the graph."""
    len_categories = len(data[0])
    if len_categories > 1:
        # Stacked graph
        if args["stacked"]:
            normal_dat = normalize(data, args["width"])
            stacked_graph(labels, data, normal_dat, len_categories, args, colors)
            return

        if not colors:
            colors = [None] * len_categories

        # Multiple series graph with different scales
        # Normalization per category
        if args["different_scale"]:
            for i in range(len_categories):
                cat_data = []
                for dat in data:
                    cat_data.append([dat[i]])

                # Normalize data, handle negatives.
                normal_cat_data = normalize(cat_data, args["width"])

                # Generate data for a row.
                for row in horiz_rows(
                    labels, cat_data, normal_cat_data, args, [colors[i]]
                ):
                    # Print the row
                    if args["vertical"]:
                        # FIXME: passing args is getting complex
                        vertic = vertically(row[0], row[1], row[2], row[3], args=args)
                    else:
                        print_row(*row)
                        print("\n")

                # The above gathers data for vertical and does not print
                # the final print happens at once here
                if args["vertical"]:
                    print_vertical(vertic, labels, colors[i], args)

                print()
                value_list.clear(), zipped_list.clear(), vertical_list.clear()
            return

    if args["histogram"]:
        if args["vertical"]:
            print(">> Error: Vertical graph for Histogram" " is not supported yet.")
            sys.exit(1)

        for row in hist_rows(data, args, colors):
            print_row(*row)
            print()
        return

    # One category/Multiple series graph with same scale
    # All-together normalization
    if not args["stacked"]:
        normal_dat = normalize(data, args["width"])
        sys.stdout.write("\033[0m")  # no color
        for row in horiz_rows(labels, data, normal_dat, args, colors):
            if not args["vertical"]:
                print_row(*row)
            else:
                # FIXME: passing args is getting complex
                vertic = vertically(row[0], row[1], row[2], row[3], args=args)

        if args["vertical"] and len_categories == 1:
            if colors:
                color = colors[0]
            else:
                color = None

            print_vertical(vertic, labels, color, args)

        print()


def check_data(labels: List, data: List, args: Dict) -> List:
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
    if args["color"] is not None:
        # Decompose arguments for Windows
        if os.name == "nt":
            colorargs = re.findall(r"[a-z]+", args["color"][0])
            if len(colorargs) != len_categories:
                print(">> Error: Color and category array sizes don't match")
            for color in colorargs:
                if color not in AVAILABLE_COLORS:
                    print(
                        ">> Error: invalid color. choose from 'red', 'blue', 'green', 'magenta', 'yellow', 'black', 'cyan'"
                    )
                    sys.exit(2)
        else:
            if len(args["color"]) != len_categories:
                print(">> Error: Color and category array sizes don't match")
            for color in args["color"]:
                if color not in AVAILABLE_COLORS:
                    print(
                        ">> Error: invalid color. choose from 'red', 'blue', 'green', 'magenta', 'yellow', 'black', 'cyan'"
                    )
                    sys.exit(2)

        if os.name == "nt":
            for color in colorargs:
                colors.append(AVAILABLE_COLORS.get(color))
        else:
            for color in args["color"]:
                colors.append(AVAILABLE_COLORS.get(color))

    # Vertical graph for multiple series of same scale is not supported yet.
    if args["vertical"] and len_categories > 1 and not args["different_scale"]:
        print(
            ">> Error: Vertical graph for multiple series of same "
            "scale is not supported yet."
        )
        sys.exit(1)

    # If user hasn't inserted colors, pick the first n colors
    # from the dict (n = number of categories).
    if args["stacked"] and not colors:
        colors = [v for v in list(AVAILABLE_COLORS.values())[:len_categories]]

    return colors


def print_categories(categories: List, colors: List) -> None:
    """Print a tick and the category's name for each category above
    the graph."""
    for i in range(len(categories)):
        if colors:
            sys.stdout.write(
                "\033[{color_i}m".format(color_i=colors[i])
            )  # Start to write colorized.
            sys.stdout.write(f"\033[{colors[i]}m")  # Start to write colorized.

        sys.stdout.write(TICK + " " + categories[i] + "  ")
        if colors:
            sys.stdout.write("\033[0m")  # Back to original.

    print("\n\n")


def read_data(args: Dict) -> Tuple[List, List, List, List]:
    """Read data from a file or stdin and returns it.

    Filename includes (categories), labels and data.
    We append categories and labels to lists.
    Data are inserted to a list of lists due to the categories.

    i.e.
    labels = ['2001', '2002', '2003', ...]
    categories = ['boys', 'girls']
    data = [ [20.4, 40.5], [30.7, 100.0], ...]"""

    filename = args["filename"]
    stdin = filename == "-"

    if args["verbose"]:
        print(">> Reading data from {src}".format(src=("stdin" if stdin else filename)))

    print("")
    if args["title"]:
        print("# " + args["title"] + "\n")

    categories, labels, data, colors = ([] for _ in range(4))

    f = None

    try:
        f = sys.stdin if stdin else open(filename, "r")
        for line in f:
            line = line.strip()
            if line:
                if not line.startswith("#"):
                    if line.find(DELIM) > 0:
                        cols = line.split(DELIM)
                    else:
                        cols = line.split()

                    # Line contains categories.
                    if line.startswith("@"):
                        cols[0] = cols[0].replace("@ ", "")
                        categories = cols

                    # Line contains label and values.
                    else:
                        labels.append(cols[0].strip())
                        data_points = []
                        for i in range(1, len(cols)):
                            data_points.append(float(cols[i].strip()))

                        data.append(data_points)
    except FileNotFoundError:
        print(
            ">> Error: The specified file [{fname}] does not exist.".format(
                fname=filename
            )
        )
        sys.exit()
    except IOError:
        print("An IOError has occurred!")
        sys.exit()
    finally:
        if f is not None:
            f.close()

    # Check that all data are valid. (i.e. There are no missing values.)
    colors = check_data(labels, data, args)
    if categories:
        # Print categories' names above the graph.
        print_categories(categories, colors)

    return categories, labels, data, colors


def calendar_heatmap(data: Dict, labels: List, args: Dict) -> None:
    """Print a calendar heatmap."""
    if args["color"]:
        colornum = AVAILABLE_COLORS.get(args["color"][0])
    else:
        colornum = AVAILABLE_COLORS.get("blue")

    dt_dict = {}
    for i in range(len(labels)):
        dt_dict[labels[i]] = data[i][0]

    # get max value
    max_val = float(max(data)[0])

    tick_1 = "░"
    tick_2 = "▒"
    tick_3 = "▓"
    tick_4 = "█"

    if args["custom_tick"]:
        tick_1 = tick_2 = tick_3 = tick_4 = args["custom_tick"]

    # check if start day set, otherwise use one year ago
    if args["start_dt"]:
        start_dt = datetime.strptime(args["start_dt"], "%Y-%m-%d")
    else:
        start = datetime.now()
        start_dt = datetime(year=start.year - 1, month=start.month, day=start.day)

    # modify start date to be a Monday, subtract weekday() from day
    start_dt = start_dt - timedelta(start_dt.weekday())

    # TODO: legend doesn't line up properly for all start dates/data
    # top legend for months
    sys.stdout.write("     ")
    for month in range(13):
        month_dt = datetime(
            year=start_dt.year, month=start_dt.month, day=1
        ) + timedelta(days=month * 31)
        sys.stdout.write(month_dt.strftime("%b") + " ")
        if args["custom_tick"]:  # assume custom tick is emoji which is one wider
            sys.stdout.write(" ")

    sys.stdout.write("\n")

    for day in range(7):
        sys.stdout.write(DAYS[day] + ": ")
        for week in range(53):
            day_ = start_dt + timedelta(days=day + week * 7)
            day_str = day_.strftime("%Y-%m-%d")

            if day_str in dt_dict:
                if dt_dict[day_str] > max_val * 0.75:
                    tick = tick_4
                elif dt_dict[day_str] > max_val * 0.50:
                    tick = tick_3
                elif dt_dict[day_str] > max_val * 0.25:
                    tick = tick_2
                # show nothing if value is zero
                elif dt_dict[day_str] == 0.0:
                    tick = " "
                # show values for less than 0.25
                else:
                    tick = tick_1
            else:
                tick = " "

            if colornum:
                sys.stdout.write("\033[{colornum}m".format(colornum=colornum))

            sys.stdout.write(tick)
            if colornum:
                sys.stdout.write("\033[0m")

        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
