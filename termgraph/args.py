"""Args class for termgraph - handles chart configuration options."""

from __future__ import annotations
from typing import Union


class Args:
    """Class representing the arguments to modify the graph."""

    default = {
        "filename": "-",
        "title": None,
        "width": 50,
        "format": "{:<5.2f}",
        "suffix": "",
        "no_labels": False,
        "no_values": False,
        "space_between": False,
        "colors": None,
        "vertical": False,
        "stacked": False,
        "histogram": False,
        "bins": 5,
        "different_scale": False,
        "calendar": False,
        "start_dt": None,
        "custom_tick": "",
        "delim": "",
        "verbose": False,
        "label_before": False,
        "percentage": False,
        "no_readable": False,
    }

    def __init__(self, **kwargs):
        """Initialize the Args object."""

        self.args = dict(self.default)

        for arg, value in list(kwargs.items()):
            if arg in self.args:
                self.args[arg] = value
            else:
                raise Exception(f"Invalid Argument: {arg}")

    def get_arg(self, arg: str) -> Union[int, str, bool, None]:
        """Returns the value for the argument given.

        :arg: The name of the argument.
        :returns: The value of the argument.

        """

        if arg in self.args:
            return self.args[arg]
        else:
            raise Exception(f"Invalid Argument: {arg}")

    def update_args(self, **kwargs) -> None:
        """Updates the arguments"""

        for arg, value in list(kwargs.items()):
            if arg in self.args:
                self.args[arg] = value
            else:
                raise Exception(f"Invalid Argument: {arg}")