"""Shared utility functions for termgraph."""

from __future__ import annotations
import math
import sys
from .constants import UNITS, TICK, SM_TICK


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
        newNum = round(num / (1000**index), 3)
        newNum *= -1 if neg else 1
        degree = UNITS[index]

    else:
        newNum = num
        degree = UNITS[0]

    return (newNum, degree)


def normalize(data: list, width: int) -> list:
    """Normalize the data and return it."""
    # We offset by the minimum if there's a negative.
    data_offset = []
    min_datum = min(value for sublist in data for value in sublist)
    if min_datum < 0:
        min_datum = abs(min_datum)
        for datum in data:
            data_offset.append([d + min_datum for d in datum])
    else:
        data_offset = data
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


def print_row_core(
    value: float,
    num_blocks: int,
    val_min: float,
    color: int | None = None,
    label_before: bool = False,
    zero_as_small_tick: bool = False,
) -> None:
    """Core logic for printing a row of bars in horizontal graphs.

    Args:
        value: The data value being displayed
        num_blocks: Number of blocks/ticks to print
        val_min: Minimum value in dataset
        color: ANSI color code (optional)
        label_before: Whether to use small tick for zero values with label_before
        zero_as_small_tick: Additional condition for using small tick on zero
    """
    sys.stdout.write("\033[0m")  # no color

    if (num_blocks < 1 and (value > val_min or value > 0)) or (
        zero_as_small_tick and value == 0.0
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
