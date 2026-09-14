"""Offline clock ingestion contracts; downloader and IBM contracts are separate."""

from __future__ import annotations

import datetime
import gzip
from pathlib import Path

import pytest

from det8.applied_physics.ingest import (
    collect_daily_clock_drifts, daily_drift, load,
    parse_igs_clock_report, read_igs_clock_archive,
)


def _clock_text(*, day: datetime.date | None = None, drift: float = 1e-12) -> str:
    selected = day or datetime.date(2024, 1, 1)
    date_fields = f"{selected.year} {selected.month:02d} {selected.day:02d}"
    return (
        f"AS G01 {date_fields} 00 00 00.000000 1 0.0D+00\n"
        f"AS G01 {date_fields} 00 00 30.000000 1 {drift * 30.0:.16E}\n"
    )


def _write_clock(path: Path, text: str | None = None) -> None:
    with gzip.open(path, "wt", encoding="ascii", newline="") as stream:
        stream.write(text or _clock_text())


def _time_system_header(system: str = "GPS") -> str:
    return f"{system:>6}".ljust(60) + "TIME SYSTEM ID\n"


def test_clock_parser_reports_rejections_and_accepts_fortran_exponents() -> None:
    report = parse_igs_clock_report(
        _clock_text()
        + "AS G02 2024 01 01 00 01 00.000000 2 1.0E-4\n"
        + "AS G03 2024 01 01 00 01 30.000000 1 NaN\n"
    )

    assert report["accepted_rows"] == 2
    assert report["rejected_rows"] == 2
    assert report["candidate_rows"] == 4
    assert report["records"][0]["bias_s"] == 0.0
    assert {item["line"] for item in report["rejections"]} == {3, 4}


def test_clock_parser_maps_complete_nvals_1_through_6_in_published_order() -> None:
    values = [1.0e-4, 2.0e-9, 3.0e-12, 4.0e-13, 5.0e-15, 6.0e-16]
    rows = [_time_system_header()]
    for n_values in range(1, 7):
        first_values = " ".join(f"{value:.12E}" for value in values[: min(n_values, 2)])
        rows.append(
            f"AS G0{n_values} 2024 02 {n_values:02d} 01 02 03.500000 "
            f"{n_values} {first_values}\n"
        )
        if n_values > 2:
            continuation = " ".join(f"{value:.12E}" for value in values[2:n_values])
            rows.append(f"   {continuation}\n")

    report = parse_igs_clock_report("".join(rows))

    assert report["accepted_rows"] == 6
    assert report["rejected_rows"] == 0
    assert report["continuation_rows"] == 4
    assert report["time_system"] == "GPS"
    first, second, third, *_, sixth = report["records"]
    assert first["bias_sigma_s"] is None
    assert first["drift_s_per_s"] is None
    assert second["bias_sigma_s"] == pytest.approx(values[1])
    assert second["drift_s_per_s"] is None
    assert third["drift_s_per_s"] == pytest.approx(values[2])
    assert sixth["drift_sigma_s_per_s"] == pytest.approx(values[3])
    assert sixth["acceleration_s_per_s2"] == pytest.approx(values[4])
    assert sixth["acceleration_sigma_s_per_s2"] == pytest.approx(values[5])


def test_clock_parser_rejects_incomplete_continuations_bad_calendar_and_uncertainty() -> None:
    text = (
        "AS G01 2024 01 01 00 00 00.000000 3 1.0E-4 2.0E-9\n"
        "ASDF G01 2024 01 01 00 00 00.000000 1 1.0E-4\n"
        "AS G02 2024 02 30 00 00 00.000000 1 1.0E-4\n"
        "AS G03 2024 01 01 00 00 00.000000 2 1.0E-4 -2.0E-9\n"
        "AS G04 2024 01 01 00 00 60.000000 1 1.0E-4\n"
        "AS G05 024 01 01 00 00 00.000000 1 1.0E-4\n"
        "AS G06 2024 01 01 00 00 00.0000001 1 1.0E-4\n"
    )

    report = parse_igs_clock_report(text)

    assert report["accepted_rows"] == 0
    assert report["candidate_rows"] == 6
    assert report["rejected_rows"] == 6
    assert report["ignored_rows"] == 1
    reasons = " ".join(item["reason"] for item in report["rejections"])
    assert "continuation" in reasons
    assert "invalid clock epoch" in reasons
    assert "nonnegative" in reasons
    assert "leap-second" in reasons
    assert "4-digit year" in reasons
    assert "six decimal places" in reasons


def test_daily_drift_sorts_records_and_rejects_ambiguous_series() -> None:
    later = {
        "svn": "G01",
        "epoch": "2024-01-01-00-01-00.000000",
        "bias_s": 6.0e-11,
        "time_system": "GPS",
    }
    earlier = {
        "svn": "G01",
        "epoch": "2024-01-01-00-00-00.000000",
        "bias_s": 0.0,
        "time_system": "GPS",
    }
    assert daily_drift([later, earlier])["drift_s_per_s"] == pytest.approx(1.0e-12)
    with pytest.raises(ValueError, match="duplicate epochs"):
        daily_drift([earlier, dict(earlier)])
    with pytest.raises(ValueError, match="one satellite"):
        daily_drift([earlier, {**later, "svn": "G02"}])


def test_elapsed_time_does_not_assume_headerless_epochs_are_utc_at_leap_boundary() -> None:
    before = {"svn": "G01", "epoch": "2016-12-31-23-59-30.000000", "bias_s": 0.0}
    after = {"svn": "G01", "epoch": "2017-01-01-00-00-30.000000", "bias_s": 6e-11}
    with pytest.raises(ValueError, match="without TIME SYSTEM ID"):
        daily_drift([before, after])

    gps = daily_drift([
        {**before, "time_system": "GPS"},
        {**after, "time_system": "GPS"},
    ])
    utc = daily_drift([
        {**before, "time_system": "UTC"},
        {**after, "time_system": "UTC"},
    ])
    assert gps["dt_s"] == 60.0
    assert utc["dt_s"] == 61.0


def test_utc_elapsed_time_refuses_dates_beyond_the_pinned_iers_table() -> None:
    before = {
        "svn": "G01",
        "epoch": "2027-06-30-23-59-30.000000",
        "bias_s": 0.0,
        "time_system": "UTC",
    }
    after = {
        "svn": "G01",
        "epoch": "2027-07-01-00-00-30.000000",
        "bias_s": 6e-11,
        "time_system": "UTC",
    }
    with pytest.raises(ValueError, match="IERS Bulletin C 72"):
        daily_drift([before, after])


def test_load_derives_rate_from_biases_instead_of_using_bias_sigma(tmp_path: Path) -> None:
    archive = tmp_path / "sigma.CLK.gz"
    _write_clock(
        archive,
        _time_system_header()
        + "AS G01 2024 01 01 00 00 00.000000 2 0.0 9.0E-9\n"
        + "AS G01 2024 01 01 00 00 30.000000 2 3.0E-11 8.0E-9\n",
    )

    result = load("igs_clock", path=str(archive))

    assert [record["drift_s_per_s"] for record in result["records"]] == [None, None]
    assert result["inputs"]["observable"] == pytest.approx([1.0e-12])


def test_archive_validation_hashes_source_and_can_expose_rejected_rows(tmp_path: Path) -> None:
    archive = tmp_path / "fixture.CLK.gz"
    _write_clock(
        archive,
        _clock_text() + "AS G02 2024 01 01 00 01 00.000000 2 1.0E-4\n",
    )

    report = read_igs_clock_archive(archive, strict=False)
    assert report["accepted_rows"] == 2
    assert report["rejected_rows"] == 1
    assert len(report["source_sha256"]) == 64
    assert report["compressed_bytes"] == archive.stat().st_size
    with pytest.raises(ValueError, match="malformed AS row"):
        read_igs_clock_archive(archive, strict=True)


def test_compressed_file_load_reports_hash_and_row_counts(tmp_path: Path) -> None:
    archive = tmp_path / "fixture.CLK.gz"
    _write_clock(archive)
    result = load("igs_clock", path=str(archive))

    assert result["source"] == "file"
    assert len(result["source_sha256"]) == 64
    assert result["n_records"] == 2
    assert result["ingest_report"]["accepted_rows"] == 2
    assert result["ingest_report"]["rejected_rows"] == 0


def test_daily_collection_keeps_source_file_association(tmp_path: Path) -> None:
    first = tmp_path / "a.CLK.gz"
    second = tmp_path / "b.CLK.gz"
    _write_clock(first, _clock_text(drift=1e-12))
    _write_clock(second, "AS G02 2024 01 02 00 00 00.000000 1 0.0\n")

    result = collect_daily_clock_drifts(tmp_path, ["G01"])
    assert result["daily"]["G01"] == pytest.approx([1e-12])
    assert result["daily_records"]["G01"][0]["file"] == first.name
    assert result["daily_records"]["G01"][0]["start_epoch"].startswith("2024-01-01")
    assert result["daily_records"]["G01"][0]["time_system"] is None
    assert len(result["daily_records"]["G01"][0]["source_sha256"]) == 64
    assert result["n_files"] == 2


def test_daily_collection_orders_by_parsed_epoch_not_filename(tmp_path: Path) -> None:
    early = tmp_path / "z-late-name.CLK.gz"
    late = tmp_path / "a-early-name.CLK.gz"
    _write_clock(early, _time_system_header() + _clock_text(day=datetime.date(2024, 1, 1)))
    _write_clock(
        late,
        _time_system_header() + _clock_text(day=datetime.date(2024, 1, 2), drift=2e-12),
    )

    result = collect_daily_clock_drifts(tmp_path, ["G01"])

    assert result["daily"]["G01"] == pytest.approx([1e-12, 2e-12])
    assert [record["file"] for record in result["daily_records"]["G01"]] == [
        early.name,
        late.name,
    ]
    assert all(record["time_system"] == "GPS" for record in result["daily_records"]["G01"])


def test_daily_collection_rejects_duplicate_satellite_day_under_an_alias(
    tmp_path: Path,
) -> None:
    _write_clock(tmp_path / "first.CLK.gz", _clock_text(day=datetime.date(2024, 1, 1)))
    _write_clock(tmp_path / "renamed-copy.CLK.gz", _clock_text(day=datetime.date(2024, 1, 1)))

    with pytest.raises(ValueError, match="duplicate G01 civil day"):
        collect_daily_clock_drifts(tmp_path, ["G01"])
