"""
termgraph.py - draw basic graphs on terminal
https://github.com/mkaz/termgraph
"""

from __future__ import annotations
import argparse
import sys
from datetime import datetime, timedelta
from itertools import zip_longest
from colorama import init  # type: ignore
import os
import re
import importlib.metadata

from .constants import AVAILABLE_COLORS, DAYS, DELIM, TICK, SM_TICK
from .utils import cvt_to_readable, normalize, print_row_core
from .data import Data
from .args import Args
from .chart import Chart, BarChart, StackedChart, HistogramChart

__version__ = importlib.metadata.version("termgraph")

init()


def init_args() -> dict:
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
        "--no-readable", action="store_true", help="Disable the readable numbers"
    )
    parser.add_argument(
        "--percentage", action="store_true", help="Display the number in percentage"
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
        print(f"termgraph v{__version__}")
        sys.exit()

    _, labels, data, colors = read_data(args)
    try:
        if args["calendar"]:
            calendar_heatmap(data, labels, args)
        else:
            chart(colors, data, args, labels)
    except BrokenPipeError:
        pass



def horiz_rows(
    labels: list,
    data: list,
    normal_dat: list,
    args: dict,
    colors: list,
    doprint: bool = True,
):
    """Prepare the horizontal graph.
    Each row is printed through the print_row function."""
    # Create Data object to use class methods
    data_obj = Data(data, labels)
    val_min = data_obj.find_min()

    for i in range(len(labels)):
        if args.get("no_labels"):
            # Hide the labels.
            label = ""
        else:
            if args.get("label_before"):
                fmt = "{:<{x}}"
            else:
                fmt = "{:<{x}}: "
            label = fmt.format(labels[i], x=data_obj.find_max_label_length())

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

            if args.get("no_values"):
                tail = args["suffix"]
            else:
                if not args.get("no_readable"):
                    val, deg = cvt_to_readable(values[j], args.get("percentage"))
                    tail = fmt.format(args["format"].format(val), deg, args["suffix"])
                else:
                    tail = fmt.format(
                        args["format"].format(values[j]), "", args["suffix"]
                    )

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
    val_min: float,
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
    if doprint:
        print(label, tail, " ", end="")

    print_row_core(
        value=value,
        num_blocks=num_blocks,
        val_min=val_min,
        color=color,
        zero_as_small_tick=doprint
    )

    if doprint:
        print()




# FIXME: globals for vertical, not ideal
value_list, zipped_list, vertical_list, maxi = [], [], [], 0


def vertically(value, num_blocks: int, val_min: int, color: bool, args: dict) -> list:
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


def print_vertical(vertical_rows: list, labels: list, color: bool, args: dict) -> None:
    """Print the whole vertical graph."""
    if color:
        sys.stdout.write(f"\033[{color}m")  # Start to write colorized.

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


def chart(colors: list, data: list, args: dict, labels: list) -> None:
    """Handle the normalization of data and the printing of the graph."""
    len_categories = len(data[0])
    
    # Simple bar chart case - use the BarChart class
    if len_categories == 1 and not args["stacked"] and not args["histogram"] and not args["vertical"]:
        # Convert CLI args dict to chart Args class, mapping incompatible keys
        chart_args_dict = dict(args)
        if "color" in chart_args_dict:
            chart_args_dict["colors"] = chart_args_dict.pop("color")
        
        # Remove CLI-specific args that don't belong in chart Args
        cli_only_args = ["filename", "delim", "verbose", "version"]
        for cli_arg in cli_only_args:
            chart_args_dict.pop(cli_arg, None)
        
        chart_args = Args(**chart_args_dict)
        if colors:
            chart_args.update_args(colors=colors)
        
        # Create Data object and chart
        data_obj = Data(data, labels)
        chart_obj: Chart = BarChart(data_obj, chart_args)
        chart_obj.draw()
        return
    
    # Complex cases still use the old procedural code until we can extend chart classes
    if len_categories > 1:
        # Stacked graph
        if args["stacked"]:
            # Convert CLI args dict to chart Args class, mapping incompatible keys
            chart_args_dict = dict(args)
            if "color" in chart_args_dict:
                chart_args_dict["colors"] = chart_args_dict.pop("color")
            
            # Remove CLI-specific args that don't belong in chart Args
            cli_only_args = ["filename", "delim", "verbose", "version"]
            for cli_arg in cli_only_args:
                chart_args_dict.pop(cli_arg, None)
            
            chart_args = Args(**chart_args_dict)
            if colors:
                chart_args.update_args(colors=colors)
            
            # Create Data object and chart
            data_obj = Data(data, labels)
            stacked_chart: Chart = StackedChart(data_obj, chart_args)
            stacked_chart.draw()
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
                value_list.clear()
                zipped_list.clear()
                vertical_list.clear()
            return

    if args["histogram"]:
        if args["vertical"]:
            print(">> Error: Vertical graph for Histogram is not supported yet.")
            sys.exit(1)

        # Convert CLI args dict to chart Args class, mapping incompatible keys
        chart_args_dict = dict(args)
        if "color" in chart_args_dict:
            chart_args_dict["colors"] = chart_args_dict.pop("color")
        
        # Remove CLI-specific args that don't belong in chart Args
        cli_only_args = ["filename", "delim", "verbose", "version"]
        for cli_arg in cli_only_args:
            chart_args_dict.pop(cli_arg, None)
        
        chart_args = Args(**chart_args_dict)
        if colors:
            chart_args.update_args(colors=colors)
        
        # Create Data object and chart
        data_obj = Data(data, labels)
        hist_chart: Chart = HistogramChart(data_obj, chart_args)
        hist_chart.draw()
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


def check_data(labels: list, data: list, args: dict) -> list:
    """Check that all data were inserted correctly. Return the colors."""
    # Check for empty arguments
    if not labels:
        print(">> Error: No labels provided")
        sys.exit(1)

    if not data:
        print(">> Error: No data provided")
        sys.exit(1)

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


def print_categories(categories: list, colors: list) -> None:
    """Print a tick and the category's name for each category above
    the graph."""
    for i in range(len(categories)):
        if colors:
            sys.stdout.write(f"\033[{colors[i]}m")  # Start to write colorized.

        sys.stdout.write(TICK + " " + categories[i] + "  ")
        if colors:
            sys.stdout.write("\033[0m")  # Back to original.

    print("\n\n")


def read_data(args: dict) -> tuple[list, list, list, list]:
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
        print(f">> Reading data from {('stdin' if stdin else filename)}")

    print("")
    if args["title"]:
        print("# " + args["title"] + "\n")

    categories: list[str] = []
    labels: list[str | None] = []
    data: list = []
    colors: list = []

    f = None

    try:
        f = sys.stdin if stdin else open(filename, "r")
        for line in f:
            line = line.strip()
            if line:
                if not line.startswith("#"):
                    # Line contains categories.
                    if line.startswith("@"):
                        cols = line.split(DELIM)
                        cols[0] = cols[0].replace("@ ", "")
                        categories = cols

                    # Line contains label and values.
                    else:
                        if line.find(DELIM) > 0:
                            cols = line.split(DELIM)
                            delim = DELIM
                        else:
                            cols = line.split()
                            delim = " "
                        labeled_row = _label_row([col.strip() for col in cols], delim)
                        data.append(labeled_row.data)
                        labels.append(labeled_row.label)
    except FileNotFoundError:
        print(f">> Error: The specified file [{filename}] does not exist.")
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


class _LabeledRow:
    def __init__(self, label: str | None, data: list[float]):
        self.label = label
        self.data = data


def _label_row(row: list[str], delim: str) -> _LabeledRow:
    data = []
    labels: list[str] = []
    labelling = False

    for text in row:
        datum = _maybe_float(text)
        if datum is None and not labels:
            labels.append(text)
            labelling = True
        elif datum is None and labelling:
            labels.append(text)
        elif datum is not None:
            data.append(datum)
            labelling = False
        else:
            raise ValueError("Multiple labels not allowed: {labels}, {text}")

    if labels:
        label = delim.join(labels)
    else:
        label = row[0]
        data.pop(0)

    return _LabeledRow(label=label, data=data)


def _maybe_float(text: str) -> float | None:
    try:
        return float(text)
    except ValueError:
        return None


def calendar_heatmap(data: dict, labels: list, args: dict) -> None:
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
                sys.stdout.write(f"\033[{colornum}m")

            sys.stdout.write(tick)
            if colornum:
                sys.stdout.write("\033[0m")

        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
