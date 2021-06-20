import math

UNITS = ["", "K", "M", "B", "T"]


def cvt_to_readable(num):
    """Return the number in a human readable format

    Eg:
    125000 -> 125.0K
    12550 -> 12.55K
    19561100 -> 19.561M
    """

    # Find the degree of the number like if it is in thousands or millions, etc.
    index = int(math.log(num) / math.log(1000))

    # Converts the number to the human readable format and returns it.
    newNum = round(num / (1000 ** index), 3)
    degree = UNITS[index]

    return (newNum, degree)
