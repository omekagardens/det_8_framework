"""Offline clock chronology checks; all archive bytes are synthetic fixtures."""

from __future__ import annotations

import copy
import gzip
import hashlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from det8.applied_physics import ingest


def _record(epoch, bias=0.0, system="GPS"):
    return {"svn": "G01", "epoch": epoch, "bias_s": bias, "time_system": system}


def _header(system):
    return f"{system:>6}".ljust(65) + "TIME SYSTEM ID\n"


def _clock_text(day=1, *, system="GPS", end_day=None, end_hour=0):
    return (
        _header(system)
        + f"AS G01 2024 01 {day:02d} 00 00 00.000000 2 0.0 9.0E-9\n"
        + f"AS G01 2024 01 {end_day or day:02d} {end_hour:02d} 00 30.000000 2 3.0E-11 8.0E-9\n"
    )


def _gzip_fixture(path, text):
    path.write_bytes(gzip.compress(text.encode("ascii"), mtime=0))


def _legacy_fixtures(monkeypatch, contents):
    """Mock only decompression; hashing still reads each synthetic source file."""
    for path in contents:
        path.write_bytes(b"synthetic legacy archive: " + path.name.encode("ascii"))

    def decompress(command, **_kwargs):
        assert command[:2] == ["gzip", "-dc"]
        return SimpleNamespace(returncode=0, stdout=contents[Path(command[2])], stderr="")

    monkeypatch.setattr(ingest.subprocess, "run", decompress)


@pytest.mark.parametrize(
    "start,stop",
    [
        ("2016-12-31-23-59-30", "2017-01-01-00-00-30"),
        ("2017-01-01-02-59-30", "2017-01-01-03-00-30"),
    ],
)
def test_unknown_scale_refuses_both_possible_leap_boundaries(start, stop):
    first, last = _record(start, system=None), _record(stop, system=None)
    with pytest.raises(ValueError, match="without TIME SYSTEM ID"):
        ingest._elapsed_seconds(first, last)
    with pytest.raises(ValueError, match="without TIME SYSTEM ID"):
        ingest._elapsed_seconds(last, first)


@pytest.mark.parametrize(
    "system,start,stop",
    [
        ("UTC", "2016-12-31-23-59-30", "2017-01-01-00-00-30"),
        ("GLO", "2017-01-01-02-59-30", "2017-01-01-03-00-30"),
    ],
)
def test_declared_leap_scale_has_61_seconds_and_signed_reverse(system, start, stop):
    first, last = _record(start, system=system), _record(stop, 61e-12, system)
    assert ingest._elapsed_seconds(first, last) == 61
    assert ingest._elapsed_seconds(last, first) == -61
    assert ingest.daily_drift([last, first])["drift_s_per_s"] == pytest.approx(1e-12)
    assert ingest._elapsed_seconds({**first, "time_system": "GPS"}, {**last, "time_system": "GPS"}) == 60


@pytest.mark.parametrize(
    "system,lower,upper,before,after",
    [
        ("UTC", "1980-01-01-00-00-00", "2027-01-01-00-00-00", "1979-12-31-23-59-59", "2027-01-01-00-00-01"),
        ("GLO", "1980-01-01-03-00-00", "2027-01-01-03-00-00", "1980-01-01-02-59-59", "2027-01-01-03-00-01"),
        (None, "1980-01-01-03-00-00", "2027-01-01-00-00-00", "1980-01-01-02-59-59", "2027-01-01-00-00-01"),
    ],
)
def test_table_coverage_is_bounded_and_shifted_for_glo(system, lower, upper, before, after):
    for epoch in (lower, upper):
        record = _record(epoch, system=system)
        assert ingest._elapsed_seconds(record, record) == 0
    with pytest.raises(ValueError, match="supported from 1980-01-01"):
        ingest._elapsed_seconds(_record(before, system=system), _record(lower, system=system))
    with pytest.raises(ValueError, match="IERS Bulletin C 72"):
        ingest._elapsed_seconds(_record(after, system=system), _record(upper, system=system))


@pytest.mark.parametrize("system", ["GPS", "TAI", "BDS"])
def test_continuous_scales_do_not_use_the_utc_table_cutoff(system):
    for year in (1970, 2030):
        first = _record(f"{year}-01-01-00-00-00", system=system)
        last = _record(f"{year}-01-01-00-01-00", system=system)
        assert ingest._elapsed_seconds(first, last) == 60


@pytest.mark.parametrize("middle_system", ["UTC", None, "INVALID"])
def test_daily_drift_validates_interior_time_systems(middle_system):
    rows = [
        _record("2024-01-01-00-00-00"),
        _record("2024-01-01-00-00-30", 3e-11, middle_system),
        _record("2024-01-01-00-01-00", 6e-11),
    ]
    with pytest.raises(ValueError, match="time system"):
        ingest.daily_drift(rows)


def test_single_daily_record_still_checks_scale_and_coverage():
    with pytest.raises(ValueError, match="unsupported clock time system"):
        ingest.daily_drift([_record("2024-01-01-00-00-00", system="INVALID")])
    with pytest.raises(ValueError, match="supported from 1980-01-01"):
        ingest.daily_drift([_record("1979-12-31-00-00-00", system="UTC")])


@pytest.mark.parametrize("function", [ingest.daily_drift, ingest.derive_drift])
@pytest.mark.parametrize(
    "first_bias,last_bias,stop",
    [
        (-1e308, 1e308, "2024-01-01-00-00-01"),
        (0.0, 1e308, "2024-01-01-00-00-00.000001"),
        (0.0, float.fromhex("0x0.0000000000001p-1022"), "2024-01-01-00-00-02"),
        (float("nan"), 0.0, "2024-01-01-00-00-01"),
    ],
)
def test_unrepresentable_bias_arithmetic_refuses(function, first_bias, last_bias, stop):
    with pytest.raises(ValueError, match="bias|drift"):
        function([_record("2024-01-01-00-00-00", first_bias), _record(stop, last_bias)])


def test_finite_endpoint_drift_sorts_without_mutating_and_preserves_true_zero():
    rows = [_record("2024-01-01-00-01-00", 6e-11), _record("2024-01-01-00-00-00")]
    original = copy.deepcopy(rows)
    result = ingest.daily_drift(rows)
    assert result["drift_s_per_s"] == pytest.approx(1e-12)
    assert result["dt_s"] == 60
    assert result["start_epoch"] == rows[1]["epoch"]
    assert result["end_epoch"] == rows[0]["epoch"]
    assert rows == original
    zero_rows = [{**r, "bias_s": 1e308} for r in reversed(rows)]
    assert ingest.daily_drift(zero_rows)["drift_s_per_s"] == 0
    assert ingest.derive_drift(zero_rows)[0]["drift_s_per_s"] == 0


@pytest.mark.parametrize("additional_header", ["UTC", "INVALID"])
@pytest.mark.parametrize("format_name", ["plain", "gzip", "legacy"])
def test_all_file_paths_refuse_invalid_time_headers(tmp_path, monkeypatch, additional_header, format_name):
    text = _header("GPS") + _header(additional_header) + _clock_text()
    if format_name == "legacy":
        path = tmp_path / "fixture.clk.Z"
        _legacy_fixtures(monkeypatch, {path: text})
        operation = lambda: ingest.run_clock_aging(tmp_path, "G01", ".clk.Z")
    elif format_name == "gzip":
        path = tmp_path / "fixture.CLK.gz"
        _gzip_fixture(path, text)
        operation = lambda: ingest.load("igs_clock", path)
    else:
        path = tmp_path / "fixture.clk"
        path.write_text(text, encoding="ascii")
        operation = lambda: ingest.load("igs_clock", path)
    with pytest.raises(ValueError, match="time-system header"):
        operation()


def test_merged_legacy_modern_rows_have_exact_source_association_and_chronology(tmp_path, monkeypatch):
    early = tmp_path / "z-first.clk.Z"
    later = tmp_path / "a-second.CLK.gz"
    _legacy_fixtures(monkeypatch, {early: _clock_text(day=1)})
    _gzip_fixture(later, _clock_text(day=3))
    rows = ingest.run_clock_aging(tmp_path, "G01")
    assert [r["file"] for r in rows] == [early.name, later.name]
    assert [r["start_epoch"] for r in rows] == ["2024-01-01-00-00-00.000000", "2024-01-03-00-00-00.000000"]
    for row, path in zip(rows, (early, later), strict=True):
        assert row["source_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert row["end_epoch"].endswith("00-00-30.000000")
        assert row["time_system"] == "GPS"
        assert row["drift_s_per_s"] == pytest.approx(1e-12)
    elapsed = ingest._elapsed_seconds(
        {"epoch": rows[0]["start_epoch"], "time_system": "GPS"},
        {"epoch": rows[1]["start_epoch"], "time_system": "GPS"},
    )
    assert elapsed == 172800  # The missing civil day remains a real gap.


@pytest.mark.parametrize("second_format", ["legacy", "modern"])
def test_duplicate_day_is_rejected_across_all_archive_combinations(tmp_path, monkeypatch, second_format):
    first = tmp_path / "first.clk.Z"
    texts = {first: _clock_text()}
    if second_format == "legacy":
        texts[tmp_path / "alias.clk.Z"] = _clock_text()
    else:
        _gzip_fixture(tmp_path / "alias.CLK.gz", _clock_text())
    _legacy_fixtures(monkeypatch, texts)
    with pytest.raises(ValueError, match="duplicate G01 civil day"):
        ingest.run_clock_aging(tmp_path, "G01")


@pytest.mark.parametrize("format_name", ["legacy", "modern"])
def test_multiday_intervals_are_refused_by_both_paths(tmp_path, monkeypatch, format_name):
    text = _clock_text(day=1, end_day=2)
    if format_name == "legacy":
        _legacy_fixtures(monkeypatch, {tmp_path / "multiday.clk.Z": text})
    else:
        _gzip_fixture(tmp_path / "multiday.CLK.gz", text)
    with pytest.raises(ValueError, match="more than one civil day"):
        ingest.run_clock_aging(tmp_path, "G01")


def test_merged_days_refuse_inconsistent_declared_scales(tmp_path, monkeypatch):
    _legacy_fixtures(monkeypatch, {tmp_path / "first.clk.Z": _clock_text(day=1, system="UTC")})
    _gzip_fixture(tmp_path / "second.CLK.gz", _clock_text(day=2, system="GPS"))
    with pytest.raises(ValueError, match="inconsistent time systems"):
        ingest.run_clock_aging(tmp_path, "G01")
