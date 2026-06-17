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

# ANSI color codes for 256-color mode
AVAILABLE_COLORS = {
    "red": 9,
    "blue": 12,
    "green": 10,
    "magenta": 13,
    "yellow": 11,
    "black": 0,
    "cyan": 14,
}