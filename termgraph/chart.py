"""Chart classes for termgraph - handles chart rendering and display."""

from __future__ import annotations
import sys
from typing import Union
import colorama
from .constants import TICK, SM_TICK, AVAILABLE_COLORS
from .utils import cvt_to_readable, normalize, print_row_core
from .data import Data
from .args import Args

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


class Chart:
    """Class representing a chart"""

    def __init__(self, data: Data, args: Args):
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
        has_header_content = title is not None or len(self.data.categories) > 0

        if title is not None:
            print(f"# {title}\n")

        if len(self.data.categories) > 0:
            colors = self.args.get_arg("colors")

            for i in range(len(self.data.categories)):
                if colors is not None and isinstance(colors, list):
                    sys.stdout.write(
                        "\033[{color_i}m".format(color_i=colors[i])
                    )  # Start to write colorized.
                    sys.stdout.write(f"\033[{colors[i]}m")  # Start to write colorized.

                sys.stdout.write(TICK + " " + self.data.categories[i] + "  ")
                if colors:
                    sys.stdout.write("\033[0m")  # Back to original.

        if has_header_content:
            print("\n\n")

    def _normalize(self) -> list[list[float]]:
        """Normalize the data and return it."""
        width = self.args.get_arg("width")
        if not isinstance(width, int):
            width = 50  # Default width
        return normalize(self.data.data, width)


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
        value: Union[int, float],
        num_blocks: Union[int, float],
        val_min: Union[int, float],
        color: Union[int, None],
        label: str = "",
        tail: str = "",
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

        if doprint:
            print(label, tail, " ", end="")

        print_row_core(
            value=float(value),
            num_blocks=int(num_blocks),
            val_min=float(val_min),
            color=color,
            zero_as_small_tick=self.args.get_arg("label_before")
        )

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
            if self.args.get_arg("colors") is not None
            else [None] * (self.data.dims[1] if self.data.dims and len(self.data.dims) > 1 else 1)
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
                    val, deg = cvt_to_readable(values[j], self.args.get_arg("percentage"))
                    format_str = self.args.get_arg("format")
                    if isinstance(format_str, str):
                        formatted_val = format_str.format(val)
                    else:
                        formatted_val = "{:<5.2f}".format(val)  # Default format
                    tail = fmt.format(
                        formatted_val,
                        deg,
                        self.args.get_arg("suffix"),
                    )

                if colors and isinstance(colors, list) and j < len(colors):
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
                    str(tail) if tail is not None else "",
                )

                if not self.args.get_arg("label_before") and not self.args.get_arg(
                    "vertical"
                ):
                    print(tail)