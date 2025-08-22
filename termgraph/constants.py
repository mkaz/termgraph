"""Shared constants for termgraph."""

from __future__ import annotations

# Calendar days
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Units for human-readable numbers
UNITS = ["", "K", "M", "B", "T"]

# Default delimiter
DELIM = ","

# Graph characters
TICK = "▇"
SM_TICK = "▏"

# ANSI escape SGR Parameters color codes
AVAILABLE_COLORS = {
    "red": 91,
    "blue": 94,
    "green": 92,
    "magenta": 95,
    "yellow": 93,
    "black": 90,
    "cyan": 96,
}