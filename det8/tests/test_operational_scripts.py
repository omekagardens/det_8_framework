"""Offline contracts for the two configured clock reporting scripts."""

from __future__ import annotations

import datetime
import gzip
from pathlib import Path

import pytest

from scripts import full_year_aging, g11_quadratic


def _write_daily_fixture(directory: Path, count: int = 10) -> None:
    start = datetime.date(2024, 1, 1)
    for index in range(count):
        day = start + datetime.timedelta(days=index)
        drift = (index + 1) ** 2 * 1e-12
        date_fields = f"{day.year} {day.month:02d} {day.day:02d}"
        text = (
            f"AS G01 {date_fields} 00 00 00.000000 1 0.0\n"
            f"AS G01 {date_fields} 00 00 30.000000 1 {drift * 30.0:.16E}\n"
        )
        with gzip.open(directory / f"day-{index:03d}.CLK.gz", "wt", encoding="ascii") as stream:
            stream.write(text)


def test_aging_scripts_use_the_selected_clock_directory(tmp_path: Path) -> None:
    _write_daily_fixture(tmp_path)

    aging = full_year_aging.analyze_clock_directory(tmp_path, ("G01",), min_days=3)
    quadratic = g11_quadratic.analyze_clock_directory(tmp_path, ("G01",), min_days=3)

    assert aging["n_files"] == 10
    assert aging["accepted_rows"] == 20
    assert aging["rejected_rows"] == 0
    assert aging["n_valid"] == 1
    assert quadratic["n_files"] == 10
    comparison = quadratic["rows"][0]
    assert comparison["best"] is None
    assert comparison["score_type"] == "descriptive_training_rss"
    assert set(comparison["fits"]) == {"exponential_offset_grid", "log_linear", "quadratic"}
    assert all(fit["rss"] >= 0 for fit in comparison["fits"].values())
    assert comparison["bic_available"] is False
    assert comparison["elapsed_days"] == list(range(10))
    assert comparison["span_days"] == 9


def test_aging_script_clis_are_configured_and_fail_closed(tmp_path: Path, capsys) -> None:
    assert full_year_aging.main(["--clock-dir", str(tmp_path), "--svns", "G01"]) == 1
    assert g11_quadratic.main(["--clock-dir", str(tmp_path), "--svns", "G01"]) == 1
    assert "no .CLK.gz files found" in capsys.readouterr().out

    corrupt = tmp_path / "corrupt.CLK.gz"
    corrupt.write_bytes(b"not-gzip")
    for script in (full_year_aging, g11_quadratic):
        assert script.main(["--clock-dir", str(tmp_path), "--svns", "G01"]) == 2
        assert "ERROR:" in capsys.readouterr().out


def test_clock_quadratic_refuses_nonzero_residual_square_underflow() -> None:
    with pytest.raises(ValueError, match="positive squared term underflows"):
        g11_quadratic._fit_quadratic([0, 1, 2, 3], [1e-200, 1, 4, 9])


def test_operational_scripts_contain_no_cross_checkout_root() -> None:
    for module in (full_year_aging, g11_quadratic):
        source = Path(module.__file__).read_text(encoding="utf-8")
        assert "/Volumes/" not in source
        assert "sys.path.insert" not in source
