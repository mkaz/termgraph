"""This module allows drawing basic graphs in the terminal."""

# termgraph.py - draw basic graphs on terminal
# https://github.com/mkaz/termgraph

import sys
import colorama
from .constants import DAYS, DELIM, TICK, SM_TICK, AVAILABLE_COLORS
from .utils import cvt_to_readable

colorama.init()


class Colors:
    """Class representing available color values for graphs."""

    Black = AVAILABLE_COLORS["black"]
    Red = AVAILABLE_COLORS["red"]
    Green = AVAILABLE_COLORS["green"]
    Yellow = AVAILABLE_COLORS["yellow"]
    Blue = AVAILABLE_COLORS["blue"]
    Magenta = AVAILABLE_COLORS["magenta"]
    Cyan = AVAILABLE_COLORS["cyan"]


class Data:
    """Class representing the data for the chart."""

    def __init__(
        self,
        data: list,
        labels: list[str],
        categories: list[str] = None,
    ):
        """Initialize data

        :labels: The labels of the data
        :data: The data to graph on the chart
        :categories: The categories of the data
        """

        if len(data) != len(labels):
            raise Exception("The dimensions of the data and labels must be the same")

        self.labels = labels
        self.data = data
        self.categories = categories or []
        self.dims = self._find_dims(data, labels)

    def _find_dims(self, data, labels, dims=None) -> tuple[int]:
        if dims is None:
            dims = []
        if all([isinstance(data[i], list) for i in range(len(data))]):
            last = None

            for i in range(len(data)):
                curr = self._find_dims(data[i], labels[i], dims + [len(data)])

                if i != 0 and last != curr:
                    raise Exception(
                        f"The inner dimensions of the data are different\nThe dimensions of {data[i - 1]} is different than the dimensions of {data[i]}"
                    )

                last = curr

            return last

        else:
            dims.append(len(data))

        return tuple(dims)

    def find_min(self) -> int | float:
        """Return the minimum value in sublist of list."""

        return min([min(sublist) for sublist in self.data])

    def find_max(self) -> int | float:
        """Return the maximum value in sublist of list."""

        return max([max(sublist) for sublist in self.data])

    def find_min_label_length(self) -> int:
        """Return the minimum length for the labels."""

        return min([len(label) for label in self.labels])

    def find_max_label_length(self) -> int:
        """Return the maximum length for the labels."""

        return max([len(label) for label in self.labels])

    def __str__(self):
        """Returns the string representation of the data.
        :returns: The data in a tabular format
        """

        maxlen_labels = max([len(label) for label in self.labels] + [len("Labels")]) + 1

        if len(self.categories) == 0:
            maxlen_data = max([len(str(data)) for data in self.data]) + 1

        else:
            maxlen_categories = max([len(category) for category in self.categories])
            maxlen_data = (
                max(
                    [
                        len(str(self.data[i][j]))
                        for i in range(len(self.data))
                        for j in range(len(self.categories))
                    ]
                )
                + maxlen_categories
                + 4
            )

        output = [
            f"{' ' * (maxlen_labels - len('Labels'))}Labels | Data",
            f"{'-' * (maxlen_labels + 1)}|{'-' * (maxlen_data + 1)}",
        ]

        for i in range(len(self.data)):
            line = f"{' ' * (maxlen_labels - len(self.labels[i])) + self.labels[i]} |"

            if len(self.categories) == 0:
                line += f" {self.data[i]}"

            else:
                for j in range(len(self.categories)):
                    if j == 0:
                        line += f" ({self.categories[j]}) {self.data[i][0]}\n"

                    else:
                        line += f"{' ' * maxlen_labels} | ({self.categories[j]}) {self.data[i][j]}"
                        line += (
                            "\n"
                            if j < len(self.categories) - 1
                            else f"\n{' ' * maxlen_labels} |"
                        )

            output.append(line)

        return "\n".join(output)

    def __repr__(self):
        return f"Data(data={self.data if len(str(self.data)) < 25 else str(self.data)[:25] + '...'}, labels={self.labels}, categories={self.categories})"


class Args:
    """Class representing the arguments to modify the graph."""

    default = {
        "filename": "-",
        "title": None,
        "width": 50,
        "format": "{:<5.2f}",
        "suffix": "",
        "no_labels": False,
        "no_values": False,
        "space_between": False,
        "colors": None,
        "vertical": False,
        "stacked": False,
        "histogram": False,
        "bins": 5,
        "different_scale": False,
        "calendar": False,
        "start_dt": None,
        "custom_tick": "",
        "delim": "",
        "verbose": False,
        "label_before": False,
    }

    def __init__(self, **kwargs):
        """Initialize the Args object."""

        self.args = dict(self.default)

        for arg, value in list(kwargs.items()):
            if arg in self.args:
                self.args[arg] = value
            else:
                raise Exception(f"Invalid Argument: {arg}")

    def get_arg(self, arg: str) -> int | str | bool | None:
        """Returns the value for the argument given.

        :arg: The name of the argument.
        :returns: The value of the argument.

        """

        if arg in self.args:
            return self.args[arg]
        else:
            raise Exception(f"Invalid Argument: {arg}")

    def update_args(self, **kwargs) -> None:
        """Updates the arguments"""

        for arg, value in list(kwargs.items()):
            if arg in self.args:
                self.args[arg] = value
            else:
                raise Exception(f"Invalid Argument: {arg}")


class Chart:
    """Class representing a chart"""

    def __init__(self, data: Data, args: Args()):
        """Initialize the chart

        :data: The data to be displayed on the chart
        :args: The arguments for the chart

        """

        self.data = data
        self.args = args
        self.normal_data = self._normalize()

    def draw(self) -> None:
        """Draw the chart with the given data"""

        raise NotImplementedError()

    def _print_header(self) -> None:
        title = self.args.get_arg("title")

        if title is not None:
            print(f"# {title}\n")

        if len(self.data.categories) > 0:
            colors = self.args.get_arg("colors")

            for i in range(len(self.data.categories)):
                if colors is not None:
                    sys.stdout.write(
                        "\033[{color_i}m".format(color_i=colors[i])
                    )  # Start to write colorized.
                    sys.stdout.write(f"\033[{colors[i]}m")  # Start to write colorized.

                sys.stdout.write(TICK + " " + self.data.categories[i] + "  ")
                if colors:
                    sys.stdout.write("\033[0m")  # Back to original.

        print("\n\n")

    def _normalize(self) -> list[float]:
        """Normalize the data and return it."""

        # We offset by the minimum if there's a negative.
        data_offset = []
        min_datum = self.data.find_min()

        if min_datum < 0:
            min_datum = abs(min_datum)

            data_offset = [[d + min_datum for d in datum] for datum in self.data.data]

        else:
            data_offset = self.data.data

        max_datum = max([max(sublist) for sublist in data_offset])

        # max_dat / width is the value for a single tick. norm_factor is the
        # inverse of this value
        # If you divide a number to the value of single tick, you will find how
        # many ticks it does contain basically.
        norm_factor = self.args.get_arg("width") / float(max_datum)
        normal_data = [[v * norm_factor for v in datum] for datum in data_offset]

        return normal_data


class HorizontalChart(Chart):
    """Class representing a horizontal chart"""

    def __init__(self, data: Data, args: Args = Args()):
        """Initialize the chart

        :data: The data to be displayed on the chart
        :args: The arguments for the chart

        """

        super().__init__(data, args)

    def print_row(
        self,
        value: int | float,
        num_blocks: int | float,
        val_min: int | float,
        color: int,
        label: bool = False,
        tail: bool = False,
    ) -> None:
        """A method to print a row for a horizontal graphs.
        i.e:
        1: ▇▇ 2
        2: ▇▇▇ 3
        3: ▇▇▇▇ 4
        """
        doprint = self.args.get_arg("label_before") and not self.args.get_arg(
            "vertical"
        )

        sys.stdout.write("\033[0m")  # no color

        if value == 0.0:
            sys.stdout.write(f"\033[{Colors.black}m")  # dark gray

        if doprint:
            print(label, tail, " ", end="")

        if (num_blocks < 1 and (value > val_min or value > 0)) or (
            self.args.get_arg("label_before") and value == 0.0
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


class BarChart(HorizontalChart):
    """Class representing a bar chart"""

    def __init__(self, data: Data, args: Args = Args()):
        """Initialize the bar chart

        :data: The data to be displayed on the chart
        :args: The arguments for the chart

        """

        super().__init__(data, args)

    def draw(self) -> None:
        """Draws the chart"""
        self._print_header()

        colors = (
            self.args.get_arg("colors")
            if self.args.get_arg("colors") != None
            else [None] * self.data.dims[1]
        )

        val_min = self.data.find_min()

        for i in range(len(self.data.labels)):
            if self.args.get_arg("no_labels"):
                # Hide the labels.
                label = ""
            else:
                if self.args.get_arg("label_before"):
                    fmt = "{:<{x}}"
                else:
                    fmt = "{:<{x}}: "

                label = fmt.format(
                    self.data.labels[i], x=self.data.find_max_label_length()
                )

            values = self.data.data[i]
            num_blocks = self.normal_data[i]

            if self.args.get_arg("space_between") and i != 0:
                print()

            for j in range(len(values)):
                # In Multiple series graph 1st category has label at the beginning,
                # whereas the rest categories have only spaces.
                if j > 0:
                    len_label = len(label)
                    label = " " * len_label

                if self.args.get_arg("label_before"):
                    fmt = "{}{}{}"

                else:
                    fmt = " {}{}{}"

                if self.args.get_arg("no_values"):
                    tail = self.args.get_arg("suffix")

                else:
                    val, deg = cvt_to_readable(values[j])
                    tail = fmt.format(
                        self.args.get_arg("format").format(val),
                        deg,
                        self.args.get_arg("suffix"),
                    )

                if colors:
                    color = colors[j]

                else:
                    color = None

                if not self.args.get_arg("label_before") and not self.args.get_arg(
                    "vertical"
                ):
                    print(label, end="")

                self.print_row(
                    values[j],
                    int(num_blocks[j]),
                    val_min,
                    color,
                    label,
                    tail,
                )

                if not self.args.get_arg("label_before") and not self.args.get_arg(
                    "vertical"
                ):
                    print(tail)
