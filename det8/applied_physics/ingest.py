"""
DET v8.0 — Applied Physics: Real-Data Ingest Pipelines

The five applied datasets have source metadata, format-specific parsers,
synthetic record generators and a legacy mapping to DET proxy inputs. Generated
records bypass file parsing; synthetic execution does not validate a parser.
The generic clock mapping uses sample-index time, concatenated satellite
series and synthetic thermal/radiation forcing. Dated clock comparisons use
the separate daily-record interface; neither path validates a physical model.

Real datasets are not bundled and may require registration or API access.
File hashes assume stable inputs during parsing and later hashing, rather
than immutable capture. No download or credential access occurs on import.
"""

from __future__ import annotations

import csv
import datetime
import gzip
import hashlib
import json
import math
import os
import random
import re
import subprocess
from collections.abc import Iterable
from pathlib import Path

# ── Dataset metadata (source + format) ──────────────────────────────────────

DATA_SOURCES = {
    "igs_clock": {
        "name": "GNSS clock aging (IGS)",
        "url": (
            "https://cddis.nasa.gov/archive/gnss/products/<GPSweek>/"
            "igs<GPSweek><DoW>.clk.Z  (final; igr=rapid, igu=ultra-rapid). "
            "Earthdata login required. Files are RINEX 3.04 clock (.clk), "
            "Unix-compressed (.Z → `uncompress`). Contains `AS` satellite records "
            "and `AR` receiver records."
        ),
        "local_path": "det8/data/igs/",
        "format": (
            "RINEX 3.04 clock (.clk): AS epoch row with bias and optional bias sigma; "
            "a continuation row carries optional rate, rate sigma, acceleration, and "
            "acceleration sigma"
        ),
        "observable": "clock bias / drift (Δf/f)",
        "thermal": "satellite internal temperature T(t)",
        "radiation": "orbital radiation flux Φ(t) (AP-8/AE-8)",
    },
    "ibm_qubit": {
        "name": "Superconducting-qubit decoherence drift (IBM/Google)",
        "url": "IBM Quantum backend.properties() JSON; Google calibration logs",
        "format": "JSON: {qubits: [[{name: T1/T2, value, unit, date}, ...], ...]}",
        "observable": "T1 / T2 coherence times",
        "thermal": "chip temperature",
        "radiation": "none (TLS spectral diffusion, not radiation)",
    },
    "cavity_drift": {
        "name": "Ultra-stable cavity creep (NIST/PTB/LIGO)",
        "url": "NIST/PTB cavity-stability datasets; LIGO calibration archives",
        "format": "CSV: date, dL_over_L (fractional length drift), T (K)",
        "observable": "fractional length drift ΔL/L",
        "thermal": "cavity temperature",
        "radiation": "none",
    },
    "space_telemetry": {
        "name": "Spacecraft solar-cell / sensor degradation (NASA/ESA)",
        "url": "NASA/ESA open-data portals (telemetry CSV + orbital ephemeris)",
        "format": "CSV: timestamp, power_fraction, T (K), radiation_flux",
        "observable": "solar-array power fraction",
        "thermal": "component temperature T(t) (eclipse cycles)",
        "radiation": "radiation flux Φ(t)",
    },
    "gauge_blocks": {
        "name": "Gauge-block metallurgy (metrology archives)",
        "url": "National metrology institute calibration databases",
        "format": "CSV: block_id, material, mfg_date, quench_rate, dL_over_L, T",
        "observable": "fractional length drift ΔL/L",
        "thermal": "ambient temperature",
        "radiation": "none",
    },
}


# ── Generic loaders ─────────────────────────────────────────────────────────


def load_csv(path: str) -> list[dict]:
    """Load a CSV file into a list of row dicts (string values)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ── Format-specific parsers (target the published format) ───────────────────


def _rinex_float(value: str) -> float:
    """Parse a finite RINEX number, including Fortran ``D`` exponents."""
    parsed = float(value.replace("D", "E").replace("d", "e"))
    if not math.isfinite(parsed):
        raise ValueError("non-finite RINEX value")
    return parsed


_SATELLITE_CLOCK_NAME = re.compile(r"^[GRECJIS][0-9]{2}$")
_CLOCK_SECONDS = re.compile(r"^[0-9]{1,2}(?:\.[0-9]{1,6})?$")
_TIME_SYSTEMS = {"GPS", "GLO", "GAL", "QZS", "IRN", "BDS", "UTC", "TAI"}
# Civil instants immediately after every UTC leap second in the GNSS era.  A
# fixed offset between a continuous GNSS time scale and UTC does not affect an
# elapsed-time difference; UTC and GLO, however, need the inserted second.
# Provenance: IERS Bulletin C 72 (2026-07-06), which confirms UTC-TAI=-37 s
# since 2017-01-01 and no leap second at the end of December 2026:
# https://datacenter.iers.org/data/16/bulletinc-072.txt
# Historical transitions: https://hpiers.obspm.fr/iers/bul/bulc/Leap_Second.dat
# The omitted 1980-01-01 transition is at the start of the supported interval;
# no supported elapsed-time calculation crosses it.
_UTC_LEAP_TRANSITIONS = tuple(
    datetime.datetime(year, month, day, tzinfo=datetime.UTC)
    for year, month, day in (
        (1981, 7, 1),
        (1982, 7, 1),
        (1983, 7, 1),
        (1985, 7, 1),
        (1988, 1, 1),
        (1990, 1, 1),
        (1991, 1, 1),
        (1992, 7, 1),
        (1993, 7, 1),
        (1994, 7, 1),
        (1996, 1, 1),
        (1997, 7, 1),
        (1999, 1, 1),
        (2006, 1, 1),
        (2009, 1, 1),
        (2012, 7, 1),
        (2015, 7, 1),
        (2017, 1, 1),
    )
)
_UTC_LEAP_TABLE_VALID_FROM = datetime.datetime(1980, 1, 1, tzinfo=datetime.UTC)
_UTC_LEAP_TABLE_VALID_UNTIL = datetime.datetime(2027, 1, 1, tzinfo=datetime.UTC)


def _clock_epoch(fields: list[str]) -> tuple[str, datetime.datetime]:
    """Validate a six-field RINEX epoch and return its civil-time coordinate."""
    if len(fields) != 6:
        raise ValueError("clock epoch must contain six fields")
    if len(fields[0]) != 4 or not all(value.isdigit() for value in fields[:5]):
        raise ValueError("clock epoch calendar fields must be unsigned integers with a 4-digit year")
    if not _CLOCK_SECONDS.fullmatch(fields[5]):
        raise ValueError("clock epoch seconds must have at most six decimal places")
    year, month, day, hour, minute = (int(value) for value in fields[:5])
    second_value = _rinex_float(fields[5])
    if not 0.0 <= second_value < 60.0:
        raise ValueError("leap-second or out-of-range epoch seconds are unsupported")
    second = int(second_value)
    microsecond = round((second_value - second) * 1_000_000)
    if microsecond >= 1_000_000:
        raise ValueError("epoch seconds exceed supported six-digit precision")
    try:
        coordinate = datetime.datetime(
            year,
            month,
            day,
            hour,
            minute,
            second,
            microsecond,
            tzinfo=datetime.UTC,
        )
    except ValueError as exc:
        raise ValueError(f"invalid clock epoch: {exc}") from exc
    return "-".join(fields), coordinate


def _parse_igs_clock_lines(lines: Iterable[str]) -> tuple[list[dict], dict]:
    """Parse satellite clock rows and return records plus auditable row counts.

    RINEX 3.04 orders values as bias, bias sigma, rate, rate sigma,
    acceleration, acceleration sigma.  More than two values require one
    continuation line; treating the second value as rate is a serious schema
    error because operational IGS products commonly publish bias plus sigma.
    """
    records = []
    rejected = []
    rejected_rows = 0
    candidate_rows = 0
    ignored_rows = 0
    continuation_rows = 0
    header_errors = []
    time_system = None
    pending = None

    def reject(line_number: int, reason: str) -> None:
        nonlocal rejected_rows
        rejected_rows += 1
        if len(rejected) < 100:
            rejected.append({"line": line_number, "reason": reason})

    def finish(candidate: dict) -> None:
        values = candidate["values"]
        if len(values) != candidate["n_values"]:
            raise ValueError(
                f"NVALS={candidate['n_values']} but {len(values)} values were supplied"
            )
        for index in (1, 3, 5):
            if index < len(values) and values[index] < 0.0:
                raise ValueError("clock uncertainty values must be nonnegative")
        records.append({
            "svn": candidate["svn"],
            "epoch": candidate["epoch"],
            "time_system": candidate["time_system"],
            "n_values": candidate["n_values"],
            "bias_s": values[0],
            "bias_sigma_s": values[1] if len(values) >= 2 else None,
            "drift_s_per_s": values[2] if len(values) >= 3 else None,
            "drift_sigma_s_per_s": values[3] if len(values) >= 4 else None,
            "acceleration_s_per_s2": values[4] if len(values) >= 5 else None,
            "acceleration_sigma_s_per_s2": values[5] if len(values) >= 6 else None,
        })

    for line_number, raw_line in enumerate(lines, start=1):
        raw_line = raw_line.rstrip("\r\n")
        line = raw_line.strip()

        if raw_line.rstrip().endswith("TIME SYSTEM ID"):
            prefix = raw_line[: raw_line.rfind("TIME SYSTEM ID")].strip()
            declared = prefix.split()[0].upper() if prefix else ""
            if declared not in _TIME_SYSTEMS:
                header_errors.append({
                    "line": line_number,
                    "reason": f"unsupported TIME SYSTEM ID {declared!r}",
                })
            elif time_system is not None and declared != time_system:
                header_errors.append({
                    "line": line_number,
                    "reason": f"conflicting TIME SYSTEM ID {declared!r}",
                })
            else:
                time_system = declared

        fields = line.split()
        is_satellite_record = bool(fields and fields[0] == "AS")

        if pending is not None:
            if is_satellite_record or not line or not raw_line[:1].isspace():
                reject(
                    pending["line"],
                    f"NVALS={pending['n_values']} record has no complete continuation line",
                )
                pending = None
            else:
                continuation_rows += 1
                try:
                    remaining = pending["n_values"] - len(pending["values"])
                    if len(fields) != remaining:
                        raise ValueError(
                            f"continuation supplies {len(fields)} values; expected {remaining}"
                        )
                    pending["values"].extend(_rinex_float(value) for value in fields)
                    finish(pending)
                except (ValueError, IndexError) as exc:
                    reject(pending["line"], str(exc))
                pending = None
                continue

        if not line or line.startswith(("#", ">")):
            ignored_rows += 1
            continue
        if not is_satellite_record:
            ignored_rows += 1
            continue

        candidate_rows += 1
        try:
            if len(fields) < 10:
                raise ValueError("fewer than 10 fields")
            nvals = int(fields[8])
            if not 1 <= nvals <= 6:
                raise ValueError("NVALS must be between 1 and 6")
            if not _SATELLITE_CLOCK_NAME.fullmatch(fields[1]):
                raise ValueError(f"invalid satellite clock name {fields[1]!r}")
            epoch, _coordinate = _clock_epoch(fields[2:8])
            first_line_values = fields[9:]
            expected_first_line = min(nvals, 2)
            if len(first_line_values) != expected_first_line:
                raise ValueError(
                    f"data row supplies {len(first_line_values)} values; "
                    f"expected {expected_first_line} before continuation"
                )
            candidate = {
                "line": line_number,
                "svn": fields[1],
                "epoch": epoch,
                "time_system": time_system,
                "n_values": nvals,
                "values": [_rinex_float(value) for value in first_line_values],
            }
            if nvals > 2:
                pending = candidate
            else:
                finish(candidate)
        except (ValueError, IndexError) as exc:
            reject(line_number, str(exc))

    if pending is not None:
        reject(
            pending["line"],
            f"NVALS={pending['n_values']} record has no complete continuation line",
        )

    return records, {
        "candidate_rows": candidate_rows,
        "accepted_rows": len(records),
        "rejected_rows": rejected_rows,
        "ignored_rows": ignored_rows,
        "continuation_rows": continuation_rows,
        "time_system": time_system,
        "header_errors": header_errors,
        "rejections": rejected,
        "rejections_truncated": rejected_rows > len(rejected),
    }


def parse_igs_clock_report(text: str) -> dict:
    """Parse RINEX clock text and retain accepted/rejected row diagnostics."""
    records, report = _parse_igs_clock_lines(text.splitlines())
    return {"records": records, **report}


def parse_igs_clock(text: str) -> list[dict]:
    """Parse RINEX clock text, preserving the historical list-only API."""
    return parse_igs_clock_report(text)["records"]


def _sha256_file(path: str | os.PathLike[str]) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_igs_clock_archive(
    path: str | os.PathLike[str],
    *,
    strict: bool = True,
    max_uncompressed_bytes: int = 512 * 1024 * 1024,
    max_line_bytes: int = 1024 * 1024,
) -> dict:
    """Read and validate a gzip clock product without trusting its extension.

    Validation proves that the stream decompresses, contains at least one valid
    satellite clock row, and (in strict mode) contains no malformed ``AS`` rows.
    The source must remain unchanged during this call: its hash is read from
    the path after parsing, not from an immutable captured input. This validates
    an AS-row subset, not every mandatory RINEX header or scientific premise.
    """
    source = Path(path)
    if max_uncompressed_bytes <= 0:
        raise ValueError("max_uncompressed_bytes must be positive")
    if max_line_bytes <= 0:
        raise ValueError("max_line_bytes must be positive")

    total_bytes = 0
    with gzip.open(source, "rt", encoding="ascii", errors="strict", newline="") as stream:
        def bounded_lines():
            nonlocal total_bytes
            while True:
                line = stream.readline(max_line_bytes + 1)
                if not line:
                    break
                if len(line) > max_line_bytes:
                    raise ValueError(f"clock product line exceeds {max_line_bytes} bytes")
                total_bytes += len(line.encode("ascii"))
                if total_bytes > max_uncompressed_bytes:
                    raise ValueError(
                        f"decompressed clock product exceeds {max_uncompressed_bytes} bytes"
                    )
                yield line

        records, report = _parse_igs_clock_lines(bounded_lines())

    if not records:
        raise ValueError("clock product contains no valid AS rows")
    if strict and report["header_errors"]:
        raise ValueError(
            f"clock product contains {len(report['header_errors'])} invalid time-system header(s)"
        )
    if strict and report["rejected_rows"]:
        raise ValueError(
            f"clock product contains {report['rejected_rows']} malformed AS row(s)"
        )
    return {
        "records": records,
        **report,
        "compressed_bytes": source.stat().st_size,
        "uncompressed_bytes": total_bytes,
        "source_sha256": _sha256_file(source),
    }


def _ordered_daily_records(candidates: list[dict], svn: str) -> list[dict]:
    """Apply one chronology contract to modern, legacy and merged daily rows."""
    systems = {record["time_system"] for record in candidates}
    if len(systems) > 1:
        raise ValueError(f"{svn} daily products use inconsistent time systems")
    ordered = sorted(
        candidates,
        key=lambda record: _epoch_coordinate(record["start_epoch"]),
    )
    previous = None
    for record in ordered:
        start = _epoch_coordinate(record["start_epoch"])
        end = _epoch_coordinate(record["end_epoch"])
        if start.date() != end.date():
            raise ValueError(f"{svn} product {record['file']} spans more than one civil day")
        first = {"epoch": record["start_epoch"], "time_system": record["time_system"]}
        last = {"epoch": record["end_epoch"], "time_system": record["time_system"]}
        if _elapsed_seconds(first, last) <= 0:
            raise ValueError(f"{svn} product {record['file']} has a nonpositive interval")
        if previous is not None:
            previous_start = _epoch_coordinate(previous["start_epoch"])
            previous_end = _epoch_coordinate(previous["end_epoch"])
            if start.date() == previous_start.date():
                raise ValueError(
                    f"duplicate {svn} civil day in {previous['file']} and {record['file']}"
                )
            if start <= previous_end:
                raise ValueError(
                    f"overlapping {svn} clock intervals in {previous['file']} and {record['file']}"
                )
        previous = record
    return ordered


def collect_daily_clock_drifts(
    clk_dir: str | os.PathLike[str],
    svns: Iterable[str],
    *,
    pattern: str = "*.CLK.gz",
    strict: bool = True,
) -> dict:
    """Collect dated per-satellite drift rows from stable local gzip products.

    Source hashes require files unchanged during ingestion; they do not certify
    an immutable capture. Chronology validation does not validate clock noise,
    interval averaging, physical forcing or an aging model.
    """
    requested = tuple(dict.fromkeys(svns))
    files = sorted(Path(clk_dir).glob(pattern))
    daily_candidates = {svn: [] for svn in requested}
    file_reports = []
    accepted_rows = 0
    rejected_rows = 0

    for path in files:
        report = read_igs_clock_archive(path, strict=strict)
        accepted_rows += report["accepted_rows"]
        rejected_rows += report["rejected_rows"]
        file_reports.append({
            "file": path.name,
            "source_sha256": report["source_sha256"],
            "accepted_rows": report["accepted_rows"],
            "rejected_rows": report["rejected_rows"],
        })
        by_svn = {svn: [] for svn in requested}
        for record in report["records"]:
            if record["svn"] in by_svn:
                by_svn[record["svn"]].append(record)
        for svn in requested:
            drift = daily_drift(by_svn[svn])
            if drift["drift_s_per_s"] is not None:
                daily_candidates[svn].append({
                    "file": path.name,
                    "source_sha256": report["source_sha256"],
                    "drift_s_per_s": drift["drift_s_per_s"],
                    "start_epoch": drift["start_epoch"],
                    "end_epoch": drift["end_epoch"],
                    "time_system": drift["time_system"],
                })

    daily = {svn: [] for svn in requested}
    daily_records = {svn: [] for svn in requested}
    for svn, candidates in daily_candidates.items():
        ordered = _ordered_daily_records(candidates, svn)
        daily_records[svn] = ordered
        daily[svn] = [record["drift_s_per_s"] for record in ordered]

    return {
        "daily": daily,
        "daily_records": daily_records,
        "files": file_reports,
        "n_files": len(files),
        "accepted_rows": accepted_rows,
        "rejected_rows": rejected_rows,
    }


def parse_ibm_properties(obj: dict) -> list[dict]:
    """Parse an IBM Qiskit BackendProperties JSON into per-qubit records.

    obj["qubits"][i] is a list of {name, value, unit, date} for qubit i.
    """
    records = []
    qubits = obj.get("qubits", [])
    for i, props in enumerate(qubits):
        rec = {"qubit": i, "date": obj.get("last_update_date", "")}
        for p in props:
            if p.get("name") in ("T1", "T2"):
                rec[p["name"]] = float(p.get("value", 0.0))
        if "T1" in rec and "T2" in rec:
            records.append(rec)
    return records


def parse_cavity_csv(rows: list[dict]) -> list[dict]:
    """Parse a cavity-drift CSV: date, dL_over_L, T."""
    return [
        {"date": r.get("date", ""),
         "dL_over_L": float(r["dL_over_L"]),
         "T": float(r.get("T", 300.0))}
        for r in rows
    ]


def parse_space_csv(rows: list[dict]) -> list[dict]:
    """Parse a space-telemetry CSV: timestamp, power_fraction, T, radiation_flux."""
    return [
        {"timestamp": r.get("timestamp", ""),
         "power_fraction": float(r["power_fraction"]),
         "T": float(r["T"]),
         "radiation_flux": float(r["radiation_flux"])}
        for r in rows
    ]


def parse_gauge_csv(rows: list[dict]) -> list[dict]:
    """Parse a gauge-block CSV: block_id, material, mfg_date, quench_rate, dL_over_L, T."""
    return [
        {"block_id": r.get("block_id", ""),
         "material": r.get("material", ""),
         "quench_rate": float(r.get("quench_rate", 0.0)),
         "dL_over_L": float(r["dL_over_L"]),
         "T": float(r.get("T", 300.0))}
        for r in rows
    ]


def parse_broadcast_nav(text: str) -> list[dict]:
    """Parse a RINEX 3 broadcast-ephemeris (BRDC) file into clock-polynomial records.

    Each navigation block opens with a line like:
        G01 2024 01 01 00 00 00 <a_f0> <a_f1> <a_f2> ...
    where a_f0 = SV clock bias (s), a_f1 = clock drift (s/s), a_f2 = drift rate
    (s/s²). Only the opening line of each block starts with a constellation
    letter (G/R/E/C/J); the continuation lines (orbital elements) do not.
    """
    records = []
    for line in text.splitlines():
        f = line.split()
        if len(f) >= 9 and f[0] and f[0][0] in "GRECJ":
            try:
                records.append({
                    "svn": f[0],
                    "epoch": "-".join(f[1:7]),
                    "a_f0_s": float(f[7]),
                    "a_f1_s_per_s": float(f[8]),
                    "a_f2_s_per_s2": float(f[9]) if len(f) > 9 else 0.0,
                })
            except (ValueError, IndexError):
                continue
    return records


def clock_aging_series(records: list[dict], svn: str) -> list[dict]:
    """Extract the clock-drift (a_f1) aging series for one satellite, sorted by epoch.

    The aging test: does the κ-recovery model predict the a_f1 drift trajectory
    better than IEEE log-aging?
    """
    sel = [r for r in records if r["svn"] == svn]
    sel.sort(key=lambda r: r["epoch"])
    return sel


def _epoch_coordinate(epoch: str) -> datetime.datetime:
    """Parse an epoch as a civil coordinate without claiming it is UTC."""
    _canonical, coordinate = _clock_epoch(epoch.split("-"))
    return coordinate


def _epoch_seconds(epoch: str) -> float:
    """Return a sortable civil-time coordinate; this does not convert GPS to UTC."""
    return _epoch_coordinate(epoch).timestamp()


def _elapsed_seconds(first: dict, last: dict) -> float:
    """Compute elapsed seconds on a declared scale within table coverage.

    Unknown scales are allowed only where both UTC and UTC+3 GLO coordinates
    are covered and neither permits a leap-second ambiguity. Calendar labels
    are coordinates, not a conversion between distinct time scales.
    """
    start = _epoch_coordinate(first["epoch"])
    stop = _epoch_coordinate(last["epoch"])
    system = first.get("time_system")
    if last.get("time_system") != system:
        raise ValueError("clock records use inconsistent time systems")
    if system is not None and (not isinstance(system, str) or system not in _TIME_SYSTEMS):
        raise ValueError(f"unsupported clock time system {system!r}")

    earlier, later = min(start, stop), max(start, stop)
    offsets = (0, 3) if system is None else ((3,) if system == "GLO" else (0,))
    leap_count = 0
    if system in {None, "UTC", "GLO"}:
        for hours in offsets:
            shift = datetime.timedelta(hours=hours)
            if earlier < _UTC_LEAP_TABLE_VALID_FROM + shift:
                raise ValueError("UTC leap-second table is only supported from 1980-01-01 (GLO +3h)")
            if later > _UTC_LEAP_TABLE_VALID_UNTIL + shift:
                raise ValueError(
                    "UTC leap-second table is only validated through 2027-01-01 "
                    "(GLO +3h) by IERS Bulletin C 72"
                )
            leap_count += sum(earlier < transition + shift <= later for transition in _UTC_LEAP_TRANSITIONS)
    if leap_count and system is None:
        raise ValueError(
            "cannot derive elapsed time across a leap-second boundary without TIME SYSTEM ID"
        )
    elapsed = (stop - start).total_seconds()
    if system in {"UTC", "GLO"}:
        elapsed += leap_count if stop >= start else -leap_count
    return elapsed


def _finite_clock_bias(record: dict) -> float:
    try:
        bias = float(record["bias_s"])
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("clock series contains an invalid bias") from exc
    if not math.isfinite(bias):
        raise ValueError("clock series contains a non-finite bias")
    return bias


def _bias_drift(first: dict, last: dict, elapsed: float) -> float:
    difference = _finite_clock_bias(last) - _finite_clock_bias(first)
    if not math.isfinite(difference):
        raise ValueError("clock bias difference is not finite")
    drift = difference / elapsed
    if not math.isfinite(drift) or (difference != 0 and drift == 0):
        raise ValueError("derived clock drift is not representable")
    return drift


def derive_drift(series: list[dict]) -> list[dict]:
    """Derive clock drift (s/s) from a bias-only .clk series by differencing.

    The IGS .clk products are bias-only (NVALS=1); the drift/aging is the
    numerical time derivative dbias/dt. Returns records augmented with
    `drift_s_per_s`.
    """
    out = []
    for i in range(1, len(series)):
        prev, cur = series[i - 1], series[i]
        dt = _elapsed_seconds(prev, cur)
        if dt > 0:
            rec = dict(cur)
            rec["drift_s_per_s"] = _bias_drift(prev, cur, dt)
            out.append(rec)
    return out


def daily_drift(series: list[dict]) -> dict:
    """Average clock drift over a day, from a bias-only .clk series.

    drift = (bias_last − bias_first) / (t_last − t_first), in s/s. This is the
    daily aging datum; the multi-day trajectory of this value is the aging
    curve the κ-model vs IEEE log-aging test operates on.
    """
    if not series:
        return {
            "svn": None,
            "drift_s_per_s": None,
            "n": 0,
            "start_epoch": None,
            "end_epoch": None,
            "time_system": None,
        }
    svns = {record["svn"] for record in series}
    if len(svns) != 1:
        raise ValueError("daily clock series must contain exactly one satellite")
    ordered = sorted(series, key=lambda record: _epoch_coordinate(record["epoch"]))
    coordinates = [_epoch_coordinate(record["epoch"]) for record in ordered]
    if len(set(coordinates)) != len(coordinates):
        raise ValueError("daily clock series contains duplicate epochs")
    for record in ordered:
        _elapsed_seconds(record, record)
        _finite_clock_bias(record)
    if any(record.get("time_system") != ordered[0].get("time_system") for record in ordered):
        raise ValueError("daily clock series uses inconsistent time systems")
    if len(ordered) < 2:
        return {
            "svn": ordered[0]["svn"],
            "drift_s_per_s": None,
            "n": 1,
            "start_epoch": ordered[0]["epoch"],
            "end_epoch": ordered[0]["epoch"],
            "time_system": ordered[0].get("time_system"),
        }
    first, last = ordered[0], ordered[-1]
    dt = _elapsed_seconds(first, last)
    if dt <= 0:
        return {
            "svn": first["svn"],
            "drift_s_per_s": None,
            "n": len(series),
            "start_epoch": first["epoch"],
            "end_epoch": last["epoch"],
            "time_system": first.get("time_system"),
        }
    return {
        "svn": first["svn"],
        "drift_s_per_s": _bias_drift(first, last, dt),
        "n": len(series),
        "dt_s": dt,
        "start_epoch": first["epoch"],
        "end_epoch": last["epoch"],
        "time_system": first.get("time_system"),
    }


def run_clock_aging(clk_dir: str, svn: str, ext: str | None = None) -> list[dict]:
    """Build a satellite's multi-day drift (aging) curve from a directory of clock files.

    Handles BOTH the legacy short-named `.clk.Z` and the modern `.CLK.gz`
    products (auto-detected). Each file is a daily clock product; for each,
    extract the endpoint drift (Δf/f) for `svn`. Both paths retain source hashes,
    dates and time systems, and reject duplicate or overlapping civil days.
    Hashes assume stable files during parsing and hashing, not immutable input
    capture. Dated rows do not validate a noise model or a physical aging law.
    """
    if ext in (None, ".CLK.gz"):
        modern = collect_daily_clock_drifts(
            clk_dir,
            [svn],
            pattern="*.CLK.gz" if ext is None else f"*{ext}",
        )
        series = modern["daily_records"][svn]
        if ext == ".CLK.gz":
            return series
    else:
        series = []

    legacy_pattern = "*.clk.Z" if ext is None else f"*{ext}"
    files = sorted(Path(clk_dir).glob(legacy_pattern))

    for path in files:
        completed = subprocess.run(
            ["gzip", "-dc", os.fspath(path)],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        if completed.returncode != 0:
            raise ValueError(f"could not decompress {path.name}: {completed.stderr.strip()}")
        report = parse_igs_clock_report(completed.stdout)
        if report["header_errors"]:
            raise ValueError(f"invalid time-system header in clock product {path.name}")
        if not report["records"] or report["rejected_rows"]:
            raise ValueError(
                f"invalid clock product {path.name}: "
                f"{report['accepted_rows']} accepted, {report['rejected_rows']} rejected"
            )
        recs = report["records"]
        sat = [r for r in recs if r["svn"] == svn]
        d = daily_drift(sat)
        if d["drift_s_per_s"] is not None:
            series.append({
                "file": path.name,
                "source_sha256": _sha256_file(path),
                "drift_s_per_s": d["drift_s_per_s"],
                "start_epoch": d["start_epoch"],
                "end_epoch": d["end_epoch"],
                "time_system": d["time_system"],
            })
    return _ordered_daily_records(series, svn)


def generate_broadcast_nav(seed: int = 42) -> list[dict]:
    """Synthetic BRDC-like record: a_f0/a_f1 with slow aging + a damage event."""
    rng = random.Random(seed)
    records = []
    drift = 1e-13
    bias = 0.0
    for i in range(200):
        if i == 100:
            drift += 5e-12            # radiation/damage event spikes the drift.
        drift += -(drift - 1e-13) * 0.02 + rng.gauss(0, 1e-14)  # aging recovery.
        bias += drift
        records.append({
            "svn": "G01",
            "epoch": f"2024-{1 + i // 12:03d}-{i:05d}",
            "a_f0_s": bias + rng.gauss(0, 1e-13),
            "a_f1_s_per_s": drift,
            "a_f2_s_per_s2": 0.0,
        })
    return records


# ── Synthetic generators (format-identical surrogates) ─────────────────────


def generate_igs_clock(seed: int = 42) -> list[dict]:
    """Synthetic IGS-like clock record: bias/drift with a proton-event walk."""
    rng = random.Random(seed)
    records = []
    bias = 0.0
    drift = 1e-13
    start = datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC)
    for epoch in range(200):
        # Solar-proton event at epoch 100 spikes the drift (damage).
        if epoch == 100:
            drift += 5e-12
        # Drift relaxes back (recovery) + noise.
        drift += -(drift - 1e-13) * 0.02 + rng.gauss(0, 1e-14)
        bias += drift
        timestamp = start + datetime.timedelta(seconds=epoch)
        records.append({"svn": "G01",
                        "epoch": timestamp.strftime("%Y-%m-%d-%H-%M-%S.%f"),
                        "time_system": "GPS",
                        "bias_s": bias + rng.gauss(0, 1e-13),
                        "drift_s_per_s": drift})
    return records


def generate_ibm_qubit(seed: int = 42) -> list[dict]:
    """Synthetic IBM-like calibration: T1/T2 with spatially-correlated drift."""
    rng = random.Random(seed)
    n = 20
    # κ-diffusion on a chain → correlated T1 drift (one hot defect at qubit 5).
    kappa = [0.2 if i != 5 else 0.8 for i in range(n)]
    for _ in range(50):
        new = list(kappa)
        for i in range(1, n - 1):
            new[i] += 0.05 * (kappa[i - 1] - 2 * kappa[i] + kappa[i + 1]) - (kappa[i] - 0.1) / 1000.0
        kappa = [max(0.0, min(1.0, k)) for k in new]
    records = []
    for i in range(n):
        t1 = 100.0 / (1.0 + kappa[i]) + rng.gauss(0, 0.5)   # µs
        records.append({"qubit": i, "date": "2024-001", "T1": t1, "T2": t1 * 0.6})
    return records


def generate_cavity_drift(seed: int = 42) -> list[dict]:
    """Synthetic NIST/LIGO-like cavity drift: single-exponential creep + noise."""
    rng = random.Random(seed)
    records = []
    for month in range(0, 240, 4):
        dL = 5e-9 * math.exp(-month / 60.0) + rng.gauss(0, 2e-11)
        records.append({"date": f"m{month:03d}", "dL_over_L": dL, "T": 300.0 + rng.gauss(0, 0.01)})
    return records


def generate_space_telemetry(seed: int = 42) -> list[dict]:
    """Synthetic NASA/ESA-like telemetry: sawtooth power + eclipse cycles."""
    rng = random.Random(seed)
    records = []
    power = 1.0
    for step in range(200):
        hot = (step % 20) < 10
        T = 400.0 if hot else 200.0
        flux = 1.0
        # Damage accumulates; recovery only in the hot phase.
        damage = 2e-4 * flux
        recovery = -power * 0.01 if hot else 0.0
        power = max(0.5, min(1.0, power + damage + recovery + rng.gauss(0, 2e-4)))
        records.append({"timestamp": f"t{step:03d}", "power_fraction": power,
                        "T": T, "radiation_flux": flux})
    return records


def generate_gauge_blocks(seed: int = 42) -> list[dict]:
    """Synthetic gauge-block archive: drift set by quench rate (κ₀)."""
    rng = random.Random(seed)
    records = []
    for i in range(30):
        quench = rng.uniform(0.0, 1.0)   # quench rate → κ₀
        tau = 20.0 + 40.0 * quench        # faster quench → longer recovery
        dL = (0.2 * quench) * math.exp(-60.0 / tau) + rng.gauss(0, 1e-9)
        records.append({"block_id": f"GB{i:04d}", "material": "steel",
                        "quench_rate": quench, "dL_over_L": dL, "T": 300.0})
    return records


_GENERATORS = {
    "igs_clock": generate_igs_clock,
    "ibm_qubit": generate_ibm_qubit,
    "cavity_drift": generate_cavity_drift,
    "space_telemetry": generate_space_telemetry,
    "gauge_blocks": generate_gauge_blocks,
}


# ── Mapping to DET inputs ───────────────────────────────────────────────────


def to_kappa_inputs(dataset: str, records: list[dict]) -> dict:
    """Map parsed records to (t, T_t, flux_t, observable) for the κ-model.

    observable is the drift/coherence/power/length series that the structural
    proxy maps to κ(t); T_t drives τ_rec; flux_t drives κ̇_damage.

    This legacy generic mapping uses sample-index time, concatenates satellite
    series, and supplies synthetic thermal/radiation forcing for clocks. Those
    choices are not measured chronology or scientific validation; dated clock
    comparisons use the separate daily-record interface.
    """
    if dataset == "igs_clock":
        observable = []
        by_satellite = {}
        for record in records:
            by_satellite.setdefault(record["svn"], []).append(record)
        for satellite_records in by_satellite.values():
            ordered = sorted(
                satellite_records,
                key=lambda record: _epoch_coordinate(record["epoch"]),
            )
            previous = None
            for record in ordered:
                rate = record.get("drift_s_per_s")
                if rate is None and previous is not None:
                    elapsed = _elapsed_seconds(previous, record)
                    if elapsed <= 0.0:
                        raise ValueError("clock records must have strictly increasing epochs")
                    rate = (record["bias_s"] - previous["bias_s"]) / elapsed
                if rate is not None:
                    observable.append(rate)
                previous = record
        t = list(range(len(observable)))
        T_t = [300.0] * len(observable)                 # satellite thermal (approx).
        flux_t = [1.0 if i == 100 else 0.0 for i in t]  # solar-proton-event pulse.
    elif dataset == "ibm_qubit":
        t = [r["qubit"] for r in records]
        T_t = [300.0] * len(records)
        flux_t = [0.0] * len(records)                # no radiation.
        observable = [r["T1"] for r in records]
    elif dataset == "cavity_drift":
        t = list(range(len(records)))
        T_t = [r["T"] for r in records]
        flux_t = [0.0] * len(records)
        observable = [r["dL_over_L"] for r in records]
    elif dataset == "space_telemetry":
        t = list(range(len(records)))
        T_t = [r["T"] for r in records]
        flux_t = [r["radiation_flux"] for r in records]
        observable = [r["power_fraction"] for r in records]
    elif dataset == "gauge_blocks":
        t = list(range(len(records)))
        T_t = [r["T"] for r in records]
        flux_t = [0.0] * len(records)
        observable = [r["dL_over_L"] for r in records]
    else:
        raise KeyError(f"unknown dataset: {dataset}")

    return {"t": t, "T_t": T_t, "flux_t": flux_t, "observable": observable}


# ── End-to-end ingest ───────────────────────────────────────────────────────


def load(dataset: str, path: str | None = None, seed: int = 42) -> dict:
    """Load a dataset: parse a real file if `path` is given, else synthesize.

    Returns parsed records, legacy proxy inputs, and source metadata. Files
    must remain stable during reading and later hashing; a source hash is not
    an immutable capture or a replay certificate. The generic mapping retains
    its sample-index and synthetic-forcing limits described in to_kappa_inputs.
    """
    if dataset not in DATA_SOURCES:
        raise KeyError(f"unknown dataset: {dataset}")

    ingest_report = None
    source_sha256 = None
    if path is not None:
        # Parse the REAL file with the same parser used for the surrogate.
        if dataset == "igs_clock":
            if str(path).endswith(".gz"):
                parsed = read_igs_clock_archive(path)
            else:
                with open(path, encoding="ascii") as f:
                    parsed = parse_igs_clock_report(f.read())
                if not parsed["records"]:
                    raise ValueError("clock product contains no valid AS rows")
                if parsed["rejected_rows"]:
                    raise ValueError(
                        f"clock product contains {parsed['rejected_rows']} malformed AS row(s)"
                    )
                if parsed["header_errors"]:
                    raise ValueError("clock product contains invalid time-system header(s)")
            records = parsed["records"]
            ingest_report = {key: value for key, value in parsed.items() if key != "records"}
        elif dataset == "ibm_qubit":
            with open(path, encoding="utf-8") as f:
                records = parse_ibm_properties(json.load(f))
        elif dataset == "cavity_drift":
            records = parse_cavity_csv(load_csv(path))
        elif dataset == "space_telemetry":
            records = parse_space_csv(load_csv(path))
        elif dataset == "gauge_blocks":
            records = parse_gauge_csv(load_csv(path))
        else:
            records = []
        source = "file"
        source_sha256 = _sha256_file(path)
        if ingest_report is None:
            ingest_report = {"accepted_rows": len(records), "rejected_rows": 0}
    else:
        records = _GENERATORS[dataset](seed=seed)
        source = "synthetic"

    inputs = to_kappa_inputs(dataset, records)
    return {
        "dataset": dataset,
        "metadata": DATA_SOURCES[dataset],
        "source": source,
        "source_sha256": source_sha256,
        "ingest_report": ingest_report,
        "n_records": len(records),
        "records": records,
        "inputs": inputs,
    }


def run_all_ingests(seed: int = 42) -> dict:
    """Run every ingest pipeline end-to-end (synthetic fallback)."""
    rows = []
    for dataset in DATA_SOURCES:
        r = load(dataset, seed=seed)
        obs = r["inputs"]["observable"]
        rows.append({
            "dataset": dataset,
            "source": r["source"],
            "n_records": r["n_records"],
            "observable_min": f"{min(obs):.3e}" if obs else None,
            "observable_max": f"{max(obs):.3e}" if obs else None,
        })
    return {"rows": rows, "n_datasets": len(rows)}
