"""Data class for termgraph - handles all data-related operations."""

from __future__ import annotations
from typing import Union
import sys
import math
from .constants import DELIM


class Data:
    """Class representing the data for the chart."""

    def __init__(
        self,
        data: list,
        labels: list[str],
        categories: Union[list[str], None] = None,
    ):
        """Initialize data

        :data: The data to graph on the chart
        :labels: The labels of the data
        :categories: The categories of the data

        Can be called with positional or keyword arguments:
        - Data([10, 20, 40, 26], ["Q1", "Q2", "Q3", "Q4"])
        - Data(data=[10, 20, 40, 26], labels=["Q1", "Q2", "Q3", "Q4"])
        - Data(labels=["Q1", "Q2", "Q3", "Q4"], data=[10, 20, 40, 26])
        """

        if data is None or labels is None:
            raise Exception("Both 'data' and 'labels' parameters are required")

        if not labels:
            raise Exception("No labels provided")

        if not data:
            raise Exception("No data provided")

        if len(data) != len(labels):
            raise Exception("The dimensions of the data and labels must be the same")

        self.labels = labels
        self.data = data
        self.categories = categories or []
        self.dims = self._find_dims(data, labels)

    @classmethod
    def from_file(cls, filename: str, args: dict) -> Data:
        """Read data from a file or stdin and return a Data object.

        This method handles reading chart data from files or stdin (when filename is "-").
        The file format supports:
        - Comments: lines starting with #
        - Categories: lines starting with @ followed by category names
        - Data rows: label followed by numeric values

        Args:
            filename: Path to data file, or "-" for stdin
            args: Dictionary of arguments including optional "delim" and "verbose"

        Returns:
            Data object with parsed data, labels, and categories

        Example file format:
            @ Boys Girls
            2001 20.4 40.5
            2002 30.7 100.0
        """
        stdin = filename == "-"

        # Get delimiter from args or use default
        delim = args.get("delim") or DELIM

        if args.get("verbose"):
            print(f">> Reading data from {('stdin' if stdin else filename)}")

        categories: list[str] = []
        labels: list[str] = []
        data: list = []

        f = None

        try:
            f = sys.stdin if stdin else open(filename, "r")
            for line in f:
                line = line.strip()
                if line:
                    if not line.startswith("#"):
                        # Line contains categories.
                        if line.startswith("@"):
                            cols = line.split(delim)
                            cols[0] = cols[0].replace("@ ", "")
                            categories = cols

                        # Line contains label and values.
                        else:
                            if line.find(delim) > 0:
                                cols = line.split(delim)
                                row_delim = delim
                            else:
                                cols = line.split()
                                row_delim = " "
                            labeled_row = _label_row([col.strip() for col in cols], row_delim)
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

        return cls(data, labels, categories)

    def _find_dims(self, data, labels, dims=None) -> Union[tuple[int], None]:
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

    def find_min(self) -> Union[int, float]:
        """Return the minimum value in sublist of list."""
        # Check if data is flat (list of numbers) or nested (list of lists)
        is_flat = all(not isinstance(item, list) for item in self.data)

        if is_flat:
            return min(self.data)
        else:
            return min(value for sublist in self.data for value in sublist)

    def find_max(self) -> Union[int, float]:
        """Return the maximum value in sublist of list."""
        # Check if data is flat (list of numbers) or nested (list of lists)
        is_flat = all(not isinstance(item, list) for item in self.data)

        if is_flat:
            return max(self.data)
        else:
            return max(value for sublist in self.data for value in sublist)

    def find_min_label_length(self) -> int:
        """Return the minimum length for the labels."""
        return min(len(label) for label in self.labels)

    def find_max_label_length(self) -> int:
        """Return the maximum length for the labels."""
        return max(len(label) for label in self.labels)

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

    def normalize(self, width: int, scale: float | None = None) -> list:
        """Normalize data to width, or to a fixed number of units per tick.

        A fixed scale ignores width and rounds positive values up to a whole
        tick. It requires finite, non-negative data and does not offset values.
        """
        # Check if data is flat (list of numbers) or nested (list of lists)
        is_flat = all(not isinstance(item, list) for item in self.data)

        if scale is not None:
            if (
                isinstance(scale, bool)
                or not isinstance(scale, (int, float))
                or (isinstance(scale, float) and not math.isfinite(scale))
                or scale <= 0
            ):
                raise ValueError("scale must be a positive finite number")

            def scaled_value(value: float) -> int:
                if (isinstance(value, float) and not math.isfinite(value)) or value < 0:
                    raise ValueError("scale requires finite non-negative data")
                try:
                    blocks = value / scale
                except OverflowError:
                    raise ValueError("scaled value is too large") from None
                if not math.isfinite(blocks):
                    raise ValueError("scaled value is too large")
                return max(1, math.ceil(blocks)) if value > 0 else 0

            if is_flat:
                return [scaled_value(value) for value in self.data]
            return [[scaled_value(value) for value in row] for row in self.data]

        if is_flat:
            # Handle flat list data
            min_datum = min(self.data)
            if min_datum < 0:
                min_datum = abs(min_datum)
                data_offset = [d + min_datum for d in self.data]
            else:
                data_offset = self.data

            min_datum = min(data_offset)
            max_datum = max(data_offset)

            if min_datum == max_datum:
                return data_offset

            norm_factor = width / float(max_datum)
            return [v * norm_factor for v in data_offset]
        else:
            # Handle nested list data (original logic)
            data_offset = []
            min_datum = min(value for sublist in self.data for value in sublist)
            if min_datum < 0:
                min_datum = abs(min_datum)
                for datum in self.data:
                    data_offset.append([d + min_datum for d in datum])
            else:
                data_offset = self.data
            min_datum = min(value for sublist in data_offset for value in sublist)
            max_datum = max(value for sublist in data_offset for value in sublist)

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

    def __repr__(self):
        return f"Data(data={self.data if len(str(self.data)) < 25 else str(self.data)[:25] + '...'}, labels={self.labels}, categories={self.categories})"


class _LabeledRow:
    """Internal helper class for parsing data rows with labels."""
    def __init__(self, label: str, data: list[float]):
        self.label = label
        self.data = data


def _label_row(row: list[str], delim: str) -> _LabeledRow:
    """Parse a row of data, extracting label and numeric values."""
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
            raise ValueError(f"Multiple labels not allowed: {labels}, {text}")

    if labels:
        label = delim.join(labels)
    else:
        label = row[0]
        data.pop(0)

    return _LabeledRow(label=label, data=data)


def _maybe_float(text: str) -> float | None:
    """Try to convert text to float, return None if not possible."""
    try:
        return float(text)
    except ValueError:
        return None
