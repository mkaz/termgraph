"""Data class for termgraph - handles all data-related operations."""

from __future__ import annotations
from typing import Union


class Data:
    """Class representing the data for the chart."""

    def __init__(
        self,
        data: list,
        labels: list[str],
        categories: Union[list[str], None] = None,
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
        return min(value for sublist in self.data for value in sublist)

    def find_max(self) -> Union[int, float]:
        """Return the maximum value in sublist of list."""
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

    def normalize(self, width: int) -> list:
        """Normalize the data and return it."""
        # We offset by the minimum if there's a negative.
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


