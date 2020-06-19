"""
    Math functions for termgraph
"""


def find_min(data):
    """Return the minimum value in sublist of list."""
    return min([min(sublist) for sublist in data])


def find_max(data):
    """Return the maximum value in sublist of list."""
    return max([max(sublist) for sublist in data])


def normalize(data, width):
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

    # max_dat / width is the value for a single tick. norm_factor is the
    # inverse of this value
    # If you divide a number to the value of single tick, you will find how
    # many ticks it does contain basically.
    norm_factor = width / float(max_datum)
    normal_data = []
    for datum in data_offset:
        normal_data.append([v * norm_factor for v in datum])

    return normal_data
