#!/usr/bin/env python3
"""Inspect fixed public DCC v3 O1 calibration inputs without extracting files.

This is an identity/table qualification tool, not a general archive ingester,
a hostile-file security boundary, or a calibration-error inference model.
It reads three specified files, writes JSON to stdout, and fetches nothing.
"""

import argparse
import hashlib
import io
import json
import re
import stat
import tarfile
from decimal import Decimal, InvalidOperation
from pathlib import Path


GPS_START = 1126259446
GPS_END = 1126259478
GPS_MIDPOINT = 1126259462
INPUTS = {
    "LIGO_O1_cal_uncertainty.tgz": {
        "bytes": 12841275,
        "sha256": "426c3e46242566351272d8b8a14044c1e97e8bd292ca2df74b0fee261bbc4d5c",
    },
    "README": {
        "bytes": 7585,
        "sha256": "fb4650601da797badc8bf9e068f798788842667a5bc27ae035ae5ffd0d311d7e",
    },
    "makeSamplePlot.py": {
        "bytes": 6147,
        "sha256": "548783b3010288c94430d54d4ac393a412f6c6afa8dbb3c3da8b41489fa80c7a",
    },
}
DETECTORS = {
    "H1": {"site": "LHO", "count": 2022, "bracket": (1126256791, 1126260391),
           "nearest": 1126260391},
    "L1": {"site": "LLO", "count": 1757, "bracket": (1126257729, 1126261329),
           "nearest": 1126257729},
}
SELECTED_SHA256 = {
    ("H1", 1126256791): "daaaf31118ec76dafa69973e9db4e75fe9dff210859b0bcec5129e026e7d0832",
    ("H1", 1126260391): "10e24d7b9d95c8eba55599a909cd052b1108fe924241ee9b2c52f5e1f1bec820",
    ("L1", 1126257729): "53ea55a36ca4a593d9bc7c3890c428c8544878b6ea88bc1b9bd958fcd628aa0a",
    ("L1", 1126261329): "430f4818af5f27183b92d50f368eb414b376d27f6d45a01f9fddce485fbd3733",
}
FINAL_NAME = re.compile(
    r"(H1|L1)/Jun-28-2017_O1_(LHO|LLO)_GPSTime_([0-9]{10})_"
    r"C02_RelativeResponseUncertainty_FinalResults\.txt"
)
DIRECTORIES = {"H1", "L1", "statisticalsummaries"}
SUMMARIES = {
    "statisticalsummaries/O1_C02_H1_150912-160119_percentile.txt",
    "statisticalsummaries/O1_C02_L1_150912-160119_percentile.txt",
}
HEADER = (
    "# Frequency    Median Mag     Phase (Rad)    -1 Sigma Mag   "
    "-1 Sigma Phase +1 Sigma Mag   +1 Sigma Phase"
)
COLUMNS = (
    "frequency_hz", "median_magnitude", "median_phase_radians",
    "lower_1sigma_magnitude", "lower_1sigma_phase_radians",
    "upper_1sigma_magnitude", "upper_1sigma_phase_radians",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verified_bytes(directory, filename, pin):
    path = directory / filename
    try:
        information = path.lstat()
        require(stat.S_ISREG(information.st_mode), f"{filename}: expected regular file")
        require(information.st_size == pin["bytes"], f"{filename}: byte size mismatch")
        with path.open("rb") as stream:
            payload = stream.read(pin["bytes"] + 1)
    except OSError as error:
        raise ValueError(f"{filename}: file cannot be read") from error
    require(len(payload) == pin["bytes"], f"{filename}: read byte size mismatch")
    require(hashlib.sha256(payload).hexdigest() == pin["sha256"],
            f"{filename}: SHA-256 mismatch")
    return payload


def archive_inventory(archive):
    members = archive.getmembers()
    require(len(members) == 3784, "archive entry count mismatch")
    require(len({member.name for member in members}) == len(members),
            "archive contains duplicate names")
    epochs = {detector: {} for detector in DETECTORS}
    directories, summaries, canonical = set(), set(), []
    for member in members:
        if member.isdir():
            require(member.name in DIRECTORIES and member.size == 0,
                    "unexpected archive directory")
            directories.add(member.name)
            kind = "directory"
        else:
            require(member.isfile(), "archive contains a nonregular member")
            kind = "regular_file"
            if member.name in SUMMARIES:
                require(member.size == 22730, "statistical summary size mismatch")
                summaries.add(member.name)
            else:
                match = FINAL_NAME.fullmatch(member.name)
                require(match is not None, "unexpected FinalResults filename")
                detector, site, epoch_text = match.groups()
                epoch = int(epoch_text)
                require(site == DETECTORS[detector]["site"], "detector/site mismatch")
                require(member.size == 10605, "FinalResults size mismatch")
                require(epoch not in epochs[detector], "duplicate detector/GPS epoch")
                epochs[detector][epoch] = member
        canonical.append({"name": member.name, "bytes": member.size, "type": kind})
    require(directories == DIRECTORIES and summaries == SUMMARIES,
            "directory/statistical summary inventory mismatch")
    for detector, expected in DETECTORS.items():
        require(len(epochs[detector]) == expected["count"],
                f"{detector}: FinalResults count mismatch")
    canonical.sort(key=lambda item: item["name"])
    inventory_bytes = json.dumps(canonical, sort_keys=True, separators=(",", ":"),
                                 ensure_ascii=True).encode("ascii")
    report = {
        "entries": len(members),
        "regular_files": sum(member.isfile() for member in members),
        "directories": sorted(directories),
        "statistical_summary_members_not_parsed": sorted(summaries),
        "canonical_inventory_sha256": hashlib.sha256(inventory_bytes).hexdigest(),
        "inventory_digest_convention": (
            "SHA-256 of ASCII JSON list sorted by member name; each object has name, "
            "bytes, type; sorted object keys, ensure_ascii=True, separators=(',',':'); "
            "type is directory or regular_file; no trailing newline"
        ),
        "detectors": {
            detector: {"FinalResults_files": len(table),
                       "first_epoch_gps": min(table), "last_epoch_gps": max(table)}
            for detector, table in epochs.items()
        },
    }
    require(report["regular_files"] == 3781, "regular-file count mismatch")
    return epochs, report


def nearest_at(epochs, gps):
    ranked = sorted((abs(epoch - gps), epoch) for epoch in epochs)
    require(len(ranked) >= 2 and ranked[0][0] < ranked[1][0],
            f"no unique nearest epoch at GPS {gps}")
    return {
        "target_gps": gps,
        "nearest_epoch_gps": ranked[0][1],
        "nearest_distance_seconds": ranked[0][0],
        "runner_up_epoch_gps": ranked[1][1],
        "runner_up_distance_seconds": ranked[1][0],
    }


def select_epochs(detector, epochs):
    earlier = [epoch for epoch in epochs if epoch < GPS_MIDPOINT]
    later = [epoch for epoch in epochs if epoch > GPS_MIDPOINT]
    require(earlier and later, f"{detector}: no bracketing epochs")
    bracket = (max(earlier), min(later))
    require(bracket == DETECTORS[detector]["bracket"], f"{detector}: bracket changed")
    require(bracket[0] < GPS_START < GPS_END < bracket[1],
            f"{detector}: epochs do not bracket the complete interval")
    midpoint = nearest_at(epochs, GPS_MIDPOINT)
    start, end = nearest_at(epochs, GPS_START), nearest_at(epochs, GPS_END)
    selected = midpoint["nearest_epoch_gps"]
    require(selected == DETECTORS[detector]["nearest"], f"{detector}: nearest changed")
    require(start["nearest_epoch_gps"] == selected == end["nearest_epoch_gps"],
            f"{detector}: nearest epoch changes within interval")
    return bracket, {
        "bracketing_epoch_gps": list(bracket),
        "nearest_epoch_gps": selected,
        "nearest_member": epochs[selected].name,
        "nearest_offset_from_midpoint_seconds": selected - GPS_MIDPOINT,
        "midpoint_check": midpoint,
        "interval_start_check": start,
        "interval_end_exclusive_checked_as_closed_endpoint": end,
        "same_unique_nearest_throughout_interval": True,
        "interval_proof": (
            "Every detector epoch was compared at both enclosing endpoints. "
            "The same unique minimizer at both endpoints remains unique throughout: "
            "for each competitor, its squared-distance difference from the selected "
            "epoch is affine in target time and positive at both endpoints."
        ),
        "selection_interpretation": (
            "Nearest available epoch follows the publisher example as an approximation; "
            "constancy of that choice is not a bound on calibration variation or error."
        ),
    }


def inspect_table(archive, detector, epoch, member):
    stream = archive.extractfile(member)
    require(stream is not None, f"{member.name}: regular-member stream missing")
    with stream:
        payload = stream.read(member.size + 1)
    require(len(payload) == member.size, f"{member.name}: member byte size mismatch")
    digest = hashlib.sha256(payload).hexdigest()
    require(digest == SELECTED_SHA256[(detector, epoch)],
            f"{member.name}: selected-member SHA-256 mismatch")
    try:
        lines = payload.decode("ascii", errors="strict").splitlines()
    except UnicodeDecodeError as error:
        raise ValueError(f"{member.name}: non-ASCII table") from error
    require(len(lines) == 101 and lines[0] == HEADER,
            f"{member.name}: header/row count mismatch")
    raw_rows, frequencies = [], []
    previous = Decimal(0)
    for line_number, line in enumerate(lines[1:], 2):
        tokens = line.split()
        require(len(tokens) == 7, f"{member.name}:{line_number}: expected seven columns")
        try:
            values = [Decimal(token) for token in tokens]
        except InvalidOperation as error:
            raise ValueError(f"{member.name}:{line_number}: invalid decimal") from error
        require(all(value.is_finite() for value in values),
                f"{member.name}:{line_number}: nonfinite decimal")
        frequency, median_mag, median_phase, lower_mag, lower_phase, upper_mag, upper_phase = values
        require(frequency > previous, f"{member.name}:{line_number}: frequency not increasing/positive")
        require(0 < lower_mag <= median_mag <= upper_mag,
                f"{member.name}:{line_number}: magnitude positivity/order failure")
        require(lower_phase <= median_phase <= upper_phase,
                f"{member.name}:{line_number}: phase order failure")
        previous = frequency
        frequencies.append(frequency)
        raw_rows.append(tokens)
    counts = (sum(f < 10 for f in frequencies),
              sum(10 <= f < 2048 for f in frequencies),
              sum(f >= 2048 for f in frequencies))
    require(counts == (10, 77, 13) and frequencies[0] == 5 and frequencies[-1] == 5000,
            f"{member.name}: fixed frequency inventory mismatch")
    return {
        "member": member.name,
        "detector": detector,
        "calibration_version_from_filename": "C02",
        "epoch_gps": epoch,
        "offset_from_midpoint_seconds": epoch - GPS_MIDPOINT,
        "bytes": len(payload), "sha256": digest,
        "header": lines[0], "row_count": len(raw_rows), "columns": list(COLUMNS),
        "frequency_first_hz": raw_rows[0][0], "frequency_last_hz": raw_rows[-1][0],
        "frequency_partition_counts": {
            "below_10_hz_invalid_for_analysis": counts[0],
            "at_least_10_hz_and_strictly_below_2048_hz": counts[1],
            "at_least_2048_hz_not_used_for_this_4096_hz_product": counts[2],
        },
        "frequency_partition_interpretation": (
            "The middle partition only satisfies the stated frequency restrictions; "
            "it is not a chosen analysis band or an inference-validity certification."
        ),
        "numeric_representation": "Original numeric tokens, checked with exact Decimal comparisons",
        "numeric_rows": raw_rows,
    }


def inspect_calibration(input_dir):
    directory = Path(input_dir)
    # Verify ALL immutable payloads before decoding text or opening the archive.
    payloads = {name: verified_bytes(directory, name, pin) for name, pin in INPUTS.items()}
    # These files are bound as documentation, never executed or imported.
    for filename in ("README", "makeSamplePlot.py"):
        try:
            payloads[filename].decode("utf-8", errors="strict")
        except UnicodeDecodeError as error:
            raise ValueError(f"{filename}: invalid UTF-8") from error
    try:
        with tarfile.open(fileobj=io.BytesIO(payloads["LIGO_O1_cal_uncertainty.tgz"]),
                          mode="r:gz") as archive:
            epochs, inventory = archive_inventory(archive)
            detectors = {}
            for detector, table in epochs.items():
                bracket, selection = select_epochs(detector, table)
                detectors[detector] = {
                    "selection": selection,
                    "bracketing_tables": [inspect_table(archive, detector, epoch, table[epoch])
                                          for epoch in bracket],
                }
    except (tarfile.TarError, OSError, EOFError) as error:
        raise ValueError("verified archive could not be inspected") from error
    return {
        "schema_version": "gwosc-fixed-o1-calibration-qualification-v1",
        "status": "fixed_input_identity_inventory_and_selected_tables_verified",
        "input_identities": INPUTS,
        "publisher_release": "DCC T2100313 version 3; LIGO O1 C02",
        "target_strain_product": {
            "event": "GW150914", "release": "GWOSC V2", "sample_rate_hz": 4096,
            "interval_gps": [GPS_START, GPS_END], "interval_convention": "[start,end)",
            "midpoint_gps": GPS_MIDPOINT,
            "relationship": "External release association; strain bytes are not read by this inspector",
        },
        "archive_inventory": inventory,
        "detectors": detectors,
        "interpretation_boundary": {
            "response_ratio": "Publisher definition eta = R_true / R_model",
            "phase_unit": "radians",
            "uncertainty": (
                "Per-frequency median and +/-1 sigma statistical boundaries; "
                "not deterministic or simultaneous error bounds"
            ),
            "nearest_epoch": "Documented approximation, not within-interval calibration assurance",
            "correlations": "No joint frequency, time, magnitude/phase or detector error law supplied here",
            "operations": "No interpolation, independent error draws, correction, filter, plot or fit",
            "scientific_readiness": "Not established by these identity and table checks",
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        report = inspect_calibration(arguments.input_dir)
    except ValueError as error:
        parser.exit(1, f"calibration qualification refused: {error}\n")
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False))


if __name__ == "__main__":
    main()
