"""Shared utility functions for termgraph."""

from __future__ import annotations
import math
from .constants import UNITS


def cvt_to_readable(num, percentage=False):
    """Return the number in a human readable format.

    Examples:
        125000 -> (125.0, 'K')
        12550 -> (12.55, 'K')
        19561100 -> (19.561, 'M')
    """

    if percentage:
        return (num * 100, '%')

    if num >= 1 or num <= -1:
        neg = num < 0
        num = abs(num)

        # Find the degree of the number like if it is in thousands or millions, etc.
        index = math.floor(math.log(num) / math.log(1000))

        # Converts the number to the human readable format and returns it.
        newNum = round(num / (1000 ** index), 3)
        newNum *= -1 if neg else 1
        degree = UNITS[index]

    else:
        newNum = num
        degree = UNITS[0]

    return (newNum, degree)


def find_min(data: list) -> float:
    """Return the minimum value in sublist of list."""
    return min([min(sublist) for sublist in data])


def find_max(data: list) -> float:
    """Return the maximum value in sublist of list."""
    return max([max(sublist) for sublist in data])


def find_max_label_length(labels: list) -> int:
    """Return the maximum length for the labels."""
    return max([len(label) for label in labels])


def normalize(data: list, width: int) -> list:
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
