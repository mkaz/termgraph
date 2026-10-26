import pytest

from termgraph import termgraph as tg


def test_init_args():
    tg.init_args()


@pytest.mark.parametrize(
    "rows,options",
    [
        (1, ["--width", "10"]),
        (300, ["--width", "1000"]),
        (1, ["--version"]),
        (1, ["--help"]),
    ],
)
def test_cli_closed_stdout_pipe(tmp_path, rows, options):
    """Exercise interpreter shutdown too, not only errors raised inside draw."""
    import os
    import subprocess
    import sys

    # One small row fails at the final flush; many wide rows fail while drawing.
    data_file = tmp_path / f"pipe-{rows}.dat"
    data_file.write_text("item 1\n" * rows)
    read_fd, write_fd = os.pipe()
    os.close(read_fd)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "termgraph.termgraph", str(data_file), *options],
            check=False,
            stdout=write_fd,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
        )
    finally:
        os.close(write_fd)
    assert result.returncode == 1
    assert result.stderr == ""
