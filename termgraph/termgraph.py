from __future__ import annotations
import argparse
import sys
from datetime import datetime, timedelta
from colorama import just_fix_windows_console
import importlib.metadata
from typing import NoReturn

from .constants import AVAILABLE_COLORS, DAYS
from .data import Data
from .args import Args
from .chart import Chart, BarChart, StackedChart, HistogramChart, VerticalChart

__version__ = importlib.metadata.version("termgraph")

# colorama
just_fix_windows_console()


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

    return args


def main():
    """Main function."""
    args = init_args()

    if args["version"]:
        print(f"termgraph v{__version__}")
        sys.exit()

    data_obj = Data.from_file(args["filename"], args)
    colors = _extract_colors(data_obj, args)

    try:
        if args["calendar"]:
            # calendar_heatmap still uses old interface
            calendar_heatmap(data_obj.data, data_obj.labels, args)
        else:
            chart(data_obj, args, colors)
    except BrokenPipeError:
        pass


def chart(data_obj: Data, args: dict, colors: list) -> None:
    """Handle the normalization of data and the printing of the graph."""
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

    # Choose chart type
    chart_obj: Chart
    if args["stacked"]:
        chart_obj = StackedChart(data_obj, chart_args)
    elif args["histogram"]:
        chart_obj = HistogramChart(data_obj, chart_args)
    elif args["vertical"]:
        chart_obj = VerticalChart(data_obj, chart_args)
    else:
        chart_obj = BarChart(data_obj, chart_args)

    chart_obj.draw()


def _extract_colors(data_obj: Data, args: dict) -> list[int]:
    """Extract and validate colors from args based on data dimensions.

    Args:
        data_obj: Data object containing the chart data
        args: Dictionary of arguments including optional "color" and "stacked"

    Returns:
        List of color codes for each category
    """
    colors: list[int] = []

    # Determine number of categories from data dimensions
    if data_obj.dims and len(data_obj.dims) > 1:
        len_categories = data_obj.dims[1]
    else:
        len_categories = 1

    # If user inserts colors, they should be as many as the categories.
    raw_colors = args.get("color")
    if raw_colors is not None:
        if len(raw_colors) != len_categories:
            print(">> Error: Color and category array sizes don't match")

        colors = [_validate_color(color) for color in raw_colors]

    # If user hasn't inserted colors, pick the first n colors
    # from the dict (n = number of categories).
    if args.get("stacked") and not colors:
        colors = [v for v in list(AVAILABLE_COLORS.values())[:len_categories]]

    return colors


def _invalid_color_error() -> NoReturn:
    """Print the standard invalid-color message and exit."""
    print(
        ">> Error:  invalid color. choose from 'red', 'blue', 'green', 'magenta', 'yellow', 'black', 'cyan', or a 256-color ANSI code (0-255)"
    )
    sys.exit(2)


def _validate_color(color: str) -> int:
    """Validate a single color value and return its ANSI code.

    A color is valid if it is either a name found in AVAILABLE_COLORS
    (e.g. "red") or a 256-color ANSI code in the range 0-255 (passed as
    a string). Anything else exits the program with
    error 2.
    """
    if color in AVAILABLE_COLORS:
        return AVAILABLE_COLORS[color]

    try:
        code = int(color)
    except ValueError:
        _invalid_color_error()

    if 0 <= code <= 255:
        return code

    _invalid_color_error()


def read_data(args: dict) -> tuple[list, list, list, list]:
    """Read data from a file or stdin and returns it.

    DEPRECATED: This function is deprecated. Use Data.from_file() and _extract_colors() instead.

    Filename includes (categories), labels and data.
    We append categories and labels to lists.
    Data are inserted to a list of lists due to the categories.

    i.e.
    labels = ['2001', '2002', '2003', ...]
    categories = ['boys', 'girls']
    data = [ [20.4, 40.5], [30.7, 100.0], ...]"""

    # Use new Data.from_file() method
    data_obj = Data.from_file(args["filename"], args)
    colors = _extract_colors(data_obj, args)

    return data_obj.categories, data_obj.labels, data_obj.data, colors


def calendar_heatmap(data: dict, labels: list, args: dict) -> None:
    """Print a calendar heatmap."""
    colornum = _validate_color(args["color"][0]) if args["color"] else AVAILABLE_COLORS["blue"]

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


# DEPRECATED: Use Data.normalize() directly instead
def normalize(data: list, width: int) -> list:
    """Normalize the data and return it.

    DEPRECATED: This function is deprecated. Use Data(data, labels).normalize(width) directly.
    """
    # Create a temporary Data object and use its normalize method
    temp_data = Data(data, [f"label_{i}" for i in range(len(data))])
    return temp_data.normalize(width)


if __name__ == "__main__":
    main()