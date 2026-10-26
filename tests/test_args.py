import pytest

from termgraph.args import Args


def test_unknown_constructor_arg_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Invalid Argument: unknown"):
        Args(unknown=True)


def test_unknown_get_arg_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Invalid Argument: unknown"):
        Args().get_arg("unknown")


def test_unknown_update_arg_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Invalid Argument: unknown"):
        Args().update_args(unknown=True)
