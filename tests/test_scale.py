"""Fixed-scale normalization, rendering, and command-line regression tests."""

import math
import os
import re
import subprocess
import sys
from copy import deepcopy

import pytest

from termgraph import Args, BarChart, Data, HistogramChart, StackedChart, VerticalChart


def plain_output(text):
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def run_cli(*options, data="A 6\nB 12\n"):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, "-m", "termgraph.termgraph", *options],
        input=data,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        timeout=15,
        check=False,
    )


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([0, 1, 4, 5, 8], [0, 1, 1, 2, 2]),
        ([[0, 1], [4, 5], [8, 12]], [[0, 1], [1, 2], [2, 3]]),
        ([[4], [4]], [[1], [1]]),
        ([[0], [0]], [[0], [0]]),
    ],
)
def test_fixed_scale_normalization(values, expected):
    original = deepcopy(values)
    data = Data(values, [str(i) for i in range(len(values))])
    assert data.normalize(50, scale=4) == expected
    assert data.data == original


def test_fixed_scale_does_not_depend_on_width_or_other_values():
    first = Data([[26], [37], [6]], ["A", "B", "C"])
    second = Data([[12], [70], [6]], ["A", "B", "C"])
    assert first.normalize(1, scale=4) == [[7], [10], [2]]
    assert second.normalize(100, scale=4) == [[3], [18], [2]]


def test_fractional_scale():
    data = Data([[0.1], [0.5], [0.75]], ["A", "B", "C"])
    assert data.normalize(50, scale=0.25) == [[1], [2], [3]]


@pytest.mark.parametrize("scale", [0, -1, math.nan, math.inf, -math.inf, True, "4"])
def test_invalid_api_scale(scale):
    data = Data([[1]], ["A"])
    with pytest.raises(ValueError, match="scale must be a positive finite number"):
        data.normalize(50, scale=scale)


@pytest.mark.parametrize("value", [-1, math.nan, math.inf, -math.inf])
def test_fixed_scale_rejects_negative_or_nonfinite_values(value):
    data = Data([[value]], ["A"])
    with pytest.raises(ValueError, match="finite non-negative data"):
        data.normalize(50, scale=4)


def test_fixed_scale_rejects_overflow():
    data = Data([[1e308]], ["A"])
    with pytest.raises(ValueError, match="scaled value is too large"):
        data.normalize(50, scale=1e-308)


def test_very_large_integers_do_not_raise_overflow_error():
    large = 10**400
    data = Data([[large]], ["A"])
    assert data.normalize(50, scale=large) == [[1]]
    with pytest.raises(ValueError, match="scaled value is too large"):
        data.normalize(50, scale=4)


@pytest.mark.parametrize("values", [[0, 1, 4, 5], [[0], [1], [4], [5]]])
def test_fixed_scale_bar_rendering(values, capsys):
    chart = BarChart(
        Data(values, ["A", "B", "C", "D"]),
        Args(scale=4, width=1, custom_tick="#", format="{:g}", suffix=" units"),
    )
    chart.draw()
    assert plain_output(capsys.readouterr().out).splitlines() == [
        "A:  0 units",
        "B: # 1 units",
        "C: # 4 units",
        "D: ## 5 units",
    ]


def test_fixed_scale_stacked_rendering(capsys):
    chart = StackedChart(
        Data([[4, 8], [8, 12]], ["A", "B"]),
        Args(scale=4, custom_tick="#", format="{:g}"),
    )
    chart.draw()
    assert plain_output(capsys.readouterr().out).splitlines() == [
        "A: ### 12",
        "B: ##### 20",
    ]


def test_fixed_scale_vertical_rendering(capsys):
    chart = VerticalChart(
        Data([[4], [12]], ["A", "B"]),
        Args(scale=4, width=1, custom_tick="#", no_values=True, no_labels=True),
    )
    chart.draw()
    assert plain_output(capsys.readouterr().out).splitlines() == ["  #", "  #", "# #"]


@pytest.mark.parametrize("chart_type", [BarChart, StackedChart, VerticalChart])
def test_fixed_scale_rejects_different_scale_api(chart_type):
    with pytest.raises(ValueError, match="different_scale"):
        chart_type(Data([[1, 2]], ["A"]), Args(scale=4, different_scale=True))


def test_fixed_scale_rejects_histogram_api():
    with pytest.raises(ValueError, match="histogram"):
        HistogramChart(Data([[1], [2]], ["A", "B"]), Args(scale=4))


def test_cli_fixed_scale():
    result = run_cli(
        "--scale", "4", "--width", "1", "--custom-tick", "#", "--format", "{:g}"
    )
    assert result.returncode == 0, result.stderr
    assert plain_output(result.stdout).splitlines() == ["A: ## 6", "B: ### 12"]


@pytest.mark.parametrize("option", ["--stacked", "--vertical"])
def test_cli_fixed_scale_other_bar_charts(option):
    result = run_cli("--scale", "4", option, "--custom-tick", "#")
    assert result.returncode == 0, result.stderr
    assert "#" in result.stdout


@pytest.mark.parametrize("scale", ["0", "-1", "nan", "inf", "-inf", "text"])
def test_cli_rejects_invalid_scale(scale):
    result = run_cli(f"--scale={scale}")
    assert result.returncode == 2
    assert "positive finite number" in result.stderr
    assert "Traceback" not in result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize("option", ["--different-scale", "--histogram", "--calendar"])
def test_cli_rejects_incompatible_modes(option):
    result = run_cli("--scale", "4", option)
    assert result.returncode == 2
    assert f"--scale cannot be used with {option}" in result.stderr
    assert "Traceback" not in result.stderr
    assert result.stdout == ""


def test_cli_rejects_negative_data_without_traceback():
    result = run_cli("--scale", "4", data="A -1\nB 2\n")
    assert result.returncode == 2
    assert "finite non-negative data" in result.stderr
    assert "Traceback" not in result.stderr
    assert result.stdout == ""


def test_scale_none_preserves_automatic_normalization():
    data = Data([[1], [2]], ["A", "B"])
    assert data.normalize(50, scale=None) == data.normalize(50)
    assert BarChart(data, Args()).normal_data == data.normalize(50)


def test_automatic_scaling_preserves_legacy_normalize_override():
    class CustomData(Data):
        def normalize(self, width):
            return [[width]]

    assert BarChart(CustomData([[1]], ["A"]), Args(width=3)).normal_data == [[3]]


def test_positive_values_remain_visible_after_division_underflow():
    assert Data([[1e-300]], ["A"]).normalize(50, scale=1e300) == [[1]]


def test_args_scale_can_be_updated():
    args = Args()
    args.update_args(scale=4)
    assert BarChart(Data([[6]], ["A"]), args).normal_data == [[2]]
