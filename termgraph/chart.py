"""Chart classes for termgraph - handles chart rendering and display."""

from __future__ import annotations
import math
import sys
from typing import Union, List, Tuple
from itertools import zip_longest
import colorama
from .constants import TICK, SM_TICK, AVAILABLE_COLORS
from .utils import cvt_to_readable, print_row_core
from .data import Data
from .args import Args

colorama.init()


def format_value(
    value: Union[int, float], format_str_arg, percentage_arg, suffix_arg
) -> str:
    """Format a value consistently across chart types."""
    # Handle type conversions and defaults
    if format_str_arg is None or not isinstance(format_str_arg, str):
        format_str = "{:<5.2f}"
    else:
        format_str = format_str_arg

    if percentage_arg is None or not isinstance(percentage_arg, bool):
        percentage = False
    else:
        percentage = percentage_arg

    if suffix_arg is None or not isinstance(suffix_arg, str):
        suffix = ""
    else:
        suffix = suffix_arg

    formatted_val = format_str.format(value)

    if percentage and "%" not in formatted_val:
        try:
            # Convert to percentage
            numeric_value = float(formatted_val)
            formatted_val = f"{numeric_value * 100:.0f}%"
        except ValueError:
            # If conversion fails, just add % suffix
            formatted_val += "%"

    return f" {formatted_val}{suffix}"


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

        if title is not None:
            print(f"# {title}\n")

        if len(self.data.categories) > 0:
            colors = self.args.get_arg("colors")

            for i in range(len(self.data.categories)):
                if colors is not None and isinstance(colors, list):
                    sys.stdout.write(f"\033[{colors[i]}m")  # Start to write colorized.

                sys.stdout.write(TICK + " " + self.data.categories[i] + "  ")
                if colors:
                    sys.stdout.write("\033[0m")  # Back to original.

            print("\n")
        elif title is not None:
            print()

    def _normalize(self) -> list[list[float]]:
        """Normalize the data and return it."""
        width = self.args.get_arg("width")
        if not isinstance(width, int):
            width = 50  # Default width
        return self.data.normalize(width)


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
            zero_as_small_tick=bool(self.args.get_arg("label_before")),
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

    def _normalize(self) -> list[list[float]]:
        """Normalize the data and return it."""
        if self.args.get_arg("different_scale"):
            # Normalization per category
            normal_data: List[List[float]] = [[] for _ in range(len(self.data.data))]
            width = self.args.get_arg("width")
            if not isinstance(width, int):
                width = 50  # Default width

            if self.data.dims and len(self.data.dims) > 1:
                for i in range(self.data.dims[1]):
                    cat_data = [[dat[i]] for dat in self.data.data]
                    
                    # Create temporary Data object for category data
                    from .data import Data
                    temp_data = Data(cat_data, [f"cat_{j}" for j in range(len(cat_data))])
                    normal_cat_data = temp_data.normalize(width)

                    for row_idx, norm_val in enumerate(normal_cat_data):
                        normal_data[row_idx].append(norm_val[0])
            return normal_data
        else:
            return super()._normalize()

    def draw(self) -> None:
        """Draws the chart"""
        self._print_header()

        colors = (
            self.args.get_arg("colors")
            if self.args.get_arg("colors") is not None
            else [None]
            * (self.data.dims[1] if self.data.dims and len(self.data.dims) > 1 else 1)
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
                    val, deg = cvt_to_readable(
                        values[j], self.args.get_arg("percentage")
                    )
                    format_str = self.args.get_arg("format")
                    if isinstance(format_str, str):
                        formatted_val = format_str.format(val)
                    else:
                        formatted_val = f"{val:<5.2f}"  # Default format
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


class StackedChart(HorizontalChart):
    """Class representing a stacked bar chart"""

    def __init__(self, data: Data, args: Args = Args()):
        """Initialize the stacked chart

        :data: The data to be displayed on the chart
        :args: The arguments for the chart
        """
        super().__init__(data, args)

    def draw(self) -> None:
        """Draws the stacked chart"""
        self._print_header()

        colors_arg = self.args.get_arg("colors")
        if isinstance(colors_arg, list):
            colors = colors_arg
        else:
            colors = [None] * (
                self.data.dims[1] if self.data.dims and len(self.data.dims) > 1 else 1
            )

        val_min = self.data.find_min()
        normal_data = self._normalize()

        for i in range(len(self.data.labels)):
            if self.args.get_arg("no_labels"):
                # Hide the labels.
                label = ""
            else:
                label = f"{self.data.labels[i]:<{self.data.find_max_label_length()}}: "

            if self.args.get_arg("space_between") and i != 0:
                print()

            print(label, end="")

            values = self.data.data[i]
            num_blocks = normal_data[i]

            for j in range(len(values)):
                print_row_core(
                    value=values[j],
                    num_blocks=int(num_blocks[j]),
                    val_min=val_min,
                    color=colors[j] if j < len(colors) else None,
                    zero_as_small_tick=False,
                )

            if self.args.get_arg("no_values"):
                # Hide the values.
                tail = ""
            else:
                tail = format_value(
                    sum(values),
                    self.args.get_arg("format"),
                    self.args.get_arg("percentage"),
                    self.args.get_arg("suffix"),
                )

            print(tail)


class VerticalChart(Chart):
    """Class representing a vertical chart"""

    def __init__(self, data: Data, args: Args = Args()):
        """Initialize the vertical chart"""
        super().__init__(data, args)
        self.value_list: list[str] = []
        self.zipped_list: list[tuple[str, ...]] = []
        self.vertical_list: list[str] = []
        self.maxi = 0

    def _prepare_vertical(self, value: float, num_blocks: int):
        """Prepare the vertical graph data."""
        self.value_list.append(str(value))

        if self.maxi < num_blocks:
            self.maxi = num_blocks

        if num_blocks > 0:
            self.vertical_list.append((TICK * num_blocks))
        else:
            self.vertical_list.append(SM_TICK)

    def draw(self) -> None:
        """Draws the vertical chart"""
        self._print_header()

        colors = self.args.get_arg("colors")
        color = colors[0] if colors and isinstance(colors, list) else None

        for i in range(len(self.data.labels)):
            values = self.data.data[i]
            num_blocks = self.normal_data[i]
            for j in range(len(values)):
                self._prepare_vertical(values[j], int(num_blocks[j]))

        # Zip_longest method in order to turn them vertically.
        for row in zip_longest(*self.vertical_list, fillvalue=" "):
            self.zipped_list.append(row)

        result_list: List[Tuple[str, ...]] = []

        if self.zipped_list:
            counter = 0
            width = self.args.get_arg("width")
            if not isinstance(width, int):
                width = 50  # Default width

            # Combined with the maxi variable, escapes the appending method at
            # the correct point or the default one (width).
            for row in reversed(self.zipped_list):
                result_list.append(row)
                counter += 1

                if self.maxi == width:
                    if counter == width:
                        break
                else:
                    if counter == self.maxi:
                        break

        if color:
            sys.stdout.write(f"\033[{color}m")

        for row in result_list:
            print(*row)

        sys.stdout.write("\033[0m")

        if result_list and not self.args.get_arg("no_values"):
            print("-" * len(result_list[0]) * 2)
            print("  ".join(self.value_list))

        if result_list and not self.args.get_arg("no_labels"):
            print("-" * len(result_list[0]) * 2)
            # Print Labels
            labels = self.data.labels
            if labels:
                print("  ".join(labels))


class HistogramChart(Chart):
    """Class representing a histogram chart"""

    def __init__(self, data: Data, args: Args = Args()):
        """Initialize the histogram chart

        :data: The data to be displayed on the chart
        :args: The arguments for the chart
        """
        super().__init__(data, args)

    def draw(self) -> None:
        """Draws the histogram chart"""
        self._print_header()

        colors_arg = self.args.get_arg("colors")
        if isinstance(colors_arg, list):
            colors = colors_arg
        else:
            colors = [None]

        val_min = self.data.find_min()
        val_max = self.data.find_max()

        # Calculate borders
        class_min = math.floor(val_min)
        class_max = math.ceil(val_max)
        class_range = class_max - class_min
        bins_arg = self.args.get_arg("bins")
        if isinstance(bins_arg, int):
            bins_count = bins_arg
        else:
            bins_count = 5  # default
        class_width = class_range / bins_count

        border = float(class_min)
        borders = []
        max_len = len(str(border))

        for b in range(bins_count + 1):
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
            # Count values in this bin range
            for row in self.data.data:
                for v in row:  # Handle multi-dimensional data
                    if start <= v < end:
                        count += 1

            count_list.append([count])

        width_arg = self.args.get_arg("width")
        if isinstance(width_arg, int):
            width = width_arg
        else:
            width = 50  # default
        
        # Create temporary Data object for count data
        from .data import Data
        temp_data = Data(count_list, [f"bin_{i}" for i in range(len(count_list))])
        normal_counts = temp_data.normalize(width)

        for i, (start_border, end_border) in enumerate(zip(borders[:-1], borders[1:])):
            if colors and colors[0]:
                color = colors[0]
            else:
                color = None

            if not self.args.get_arg("no_labels"):
                print(f"{start_border:{max_len}} – {end_border:{max_len}}: ", end="")

            num_blocks = normal_counts[i]

            print_row_core(
                value=count_list[i][0],
                num_blocks=int(num_blocks[0]),
                val_min=0,  # Histogram always starts from 0
                color=color,
                zero_as_small_tick=False,
            )

            if self.args.get_arg("no_values"):
                tail = ""
            else:
                tail = format_value(
                    count_list[i][0],
                    self.args.get_arg("format"),
                    self.args.get_arg("percentage"),
                    self.args.get_arg("suffix"),
                )
            print(tail)
