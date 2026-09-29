from termgraph import termgraph as tg
import sys


def test_init_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["termgraph", "input.dat"])
    args = tg.init_args()
    assert args["filename"] == "input.dat"
    assert args["width"] == 50
    assert args["scale"] is None
