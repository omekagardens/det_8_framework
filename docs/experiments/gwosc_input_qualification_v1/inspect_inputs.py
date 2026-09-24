"""Read-only identity and structure check of two fixed GW150914 V2 products.

This is a reproducibility inspector for known files, not a general ingester or
a hostile-file security boundary. It performs no waveform analysis or fitting.
"""

import argparse
import hashlib
import io
import json
import stat
from fractions import Fraction
from pathlib import Path

import h5py
import numpy as np

GPS_START = 1126259446
DURATION = 32
RATE = 4096
NPOINTS = DURATION * RATE
MAX_FILE_BYTES = 2 * 1024 * 1024
FILES = (
    {
        "filename": "H-H1_LOSC_4_V2-1126259446-32.hdf5",
        "detector": "H1",
        "observatory": "H",
        "bytes": 1040592,
        "md5": "50441a42c13fc1f14e5c4ea5527f1515",
        "sha256": "6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6",
    },
    {
        "filename": "L-L1_LOSC_4_V2-1126259446-32.hdf5",
        "detector": "L1",
        "observatory": "L",
        "bytes": 1007420,
        "md5": "361ae6a040a9fef7897b1e0124d5b0a1",
        "sha256": "56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189",
    },
)
MASK_DESCRIPTION = (
    'A bitmask encoded as an integer-valued timeseries. The first "Bits" bits '
    'might be used, for each there is an entry in "Bits", "Shortnames", '
    '"Descriptions", one for each bit.'
)
DQ_NAMES = ("DATA", "CBC_CAT1", "CBC_CAT2", "CBC_CAT3", "BURST_CAT1", "BURST_CAT2", "BURST_CAT3")
DQ_DESCRIPTIONS = (
    "data present",
    "passes cbc CAT1 test",
    "passes cbc CAT2 test",
    "passes cbc CAT3 test",
    "passes burst CAT1 test",
    "passes burst CAT2 test",
    "passes burst CAT3 test",
)
INJECTION_NAMES = (
    "NO_CBC_HW_INJ",
    "NO_BURST_HW_INJ",
    "NO_DETCHAR_HW_INJ",
    "NO_CW_HW_INJ",
    "NO_STOCH_HW_INJ",
)
INJECTION_DESCRIPTIONS = (
    "no cbc injections",
    "no burst inejctions",
    "no detchar injections",
    "no continuous wave injections",
    "no stoch injection",
)
GROUPS = ("meta", "quality", "quality/detail", "quality/injections", "quality/simple", "strain")
DATASETS = (
    "meta/Description",
    "meta/DescriptionURL",
    "meta/Detector",
    "meta/Duration",
    "meta/GPSstart",
    "meta/Observatory",
    "meta/Type",
    "meta/UTCstart",
    "quality/injections/InjDescriptions",
    "quality/injections/InjShortnames",
    "quality/injections/Injmask",
    "quality/simple/DQDescriptions",
    "quality/simple/DQShortnames",
    "quality/simple/DQmask",
    "strain/Strain",
)


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _verified_bytes(directory, expected):
    path = directory / expected["filename"]
    try:
        information = path.lstat()
        _require(
            stat.S_ISREG(information.st_mode), f"{expected['filename']}: expected a regular file"
        )
        _require(
            information.st_size <= MAX_FILE_BYTES, f"{expected['filename']}: exceeds 2 MiB limit"
        )
        _require(
            information.st_size == expected["bytes"], f"{expected['filename']}: byte size mismatch"
        )
        with path.open("rb") as stream:
            payload = stream.read(MAX_FILE_BYTES)
    except OSError as error:
        raise ValueError(f"{expected['filename']}: file cannot be read") from error
    _require(len(payload) == expected["bytes"], f"{expected['filename']}: read byte size mismatch")
    actual_md5 = hashlib.md5(payload, usedforsecurity=False).hexdigest()
    actual_sha256 = hashlib.sha256(payload).hexdigest()
    _require(actual_md5 == expected["md5"], f"{expected['filename']}: publisher MD5 mismatch")
    _require(actual_sha256 == expected["sha256"], f"{expected['filename']}: local SHA-256 mismatch")
    return payload


def _text(value, label):
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8", errors="strict")
        except UnicodeDecodeError as error:
            raise ValueError(f"{label}: invalid UTF-8") from error
    _require(type(value) is str, f"{label}: expected scalar text")
    return value


def _scalar(value, expected, label):
    if type(expected) is str:
        actual = _text(value, label)
    elif type(expected) is int:
        _require(
            isinstance(value, (int, np.integer)) and not isinstance(value, (bool, np.bool_)),
            f"{label}: expected integer",
        )
        actual = int(value)
    else:
        _require(isinstance(value, (float, np.floating)), f"{label}: expected floating scalar")
        actual = float(value)
    _require(actual == expected, f"{label}: unexpected value")
    return actual


def _attributes(dataset, expected):
    _require(set(dataset.attrs) == set(expected), f"{dataset.name}: unexpected attribute set")
    return {
        name: _scalar(dataset.attrs[name], value, f"{dataset.name}@{name}")
        for name, value in expected.items()
    }


def _dataset(handle, name, shape, dtype):
    dataset = handle[name]
    _require(isinstance(dataset, h5py.Dataset), f"{name}: expected dataset")
    _require(dataset.shape == shape, f"{name}: unexpected shape")
    _require(dataset.dtype == np.dtype(dtype), f"{name}: unexpected dtype")
    return dataset


def _metadata(handle, expected):
    values = {
        "Description": "Strain data time series from LIGO",
        "DescriptionURL": "http://losc.ligo.org/",
        "Detector": expected["detector"],
        "Duration": DURATION,
        "GPSstart": GPS_START,
        "Observatory": expected["observatory"],
        "Type": "StrainTimeSeries",
        "UTCstart": "2015-09-14T09:50:29",
    }
    output = {}
    for name, value in values.items():
        dtype = "int64" if type(value) is int else "object"
        dataset = _dataset(handle, "meta/" + name, (), dtype)
        _attributes(dataset, {})
        output[name] = _scalar(dataset[()], value, dataset.name)
    return output


def _text_vector(handle, name, expected, dtype):
    dataset = _dataset(handle, name, (len(expected),), dtype)
    _attributes(dataset, {})
    values = [_text(value, name) for value in dataset[()]]
    _require(values == list(expected), f"{name}: names/descriptions or order mismatch")
    return values


def _intervals(selected):
    """Coalesce exactly aligned one-second flags into half-open GPS intervals."""
    output = []
    start = None
    for index, active in enumerate(selected):
        if active and start is None:
            start = index
        elif not active and start is not None:
            output.append([GPS_START + start, GPS_START + index])
            start = None
    if start is not None:
        output.append([GPS_START + start, GPS_START + len(selected)])
    return output


def _mask(handle, prefix, stem, names, descriptions, names_dtype, descriptions_dtype):
    count = len(names)
    shortnames = _text_vector(handle, prefix + "/" + stem + "Shortnames", names, names_dtype)
    descriptions = _text_vector(
        handle, prefix + "/" + stem + "Descriptions", descriptions, descriptions_dtype
    )
    dataset = _dataset(handle, prefix + "/" + stem + "mask", (DURATION,), "uint32")
    attributes = _attributes(
        dataset,
        {
            "Bits": count,
            "Description": MASK_DESCRIPTION,
            "Npoints": DURATION,
            "Xlabel": "GPS time",
            "Xspacing": 1.0,
            "Xstart": GPS_START,
            "Xunits": "second",
            "Ylabel": stem + "mask",
        },
    )
    values = [int(value) for value in dataset[()]]
    _require(all(value >> count == 0 for value in values), f"{dataset.name}: undefined high bits")
    flags = []
    for bit, (name, description) in enumerate(zip(shortnames, descriptions, strict=True)):
        selected = [bool(value & (1 << bit)) for value in values]
        flags.append(
            {
                "bit": bit,
                "name": name,
                "description": description,
                "one_intervals_gps": _intervals(selected),
                "zero_intervals_gps": _intervals([not value for value in selected]),
                "seconds_one": sum(selected),
                "seconds_zero": DURATION - sum(selected),
            }
        )
    return {
        "dataset": dataset.name,
        "dtype": str(dataset.dtype),
        "shape": list(dataset.shape),
        "attributes": attributes,
        "raw_bitfields": values,
        "flags": flags,
        "interval_convention": "half-open GPS seconds [start,end)",
    }


def _inspect(payload, expected):
    with h5py.File(io.BytesIO(payload), "r") as handle:
        members = []
        handle.visit(members.append)
        _require(set(members) == set(GROUPS) | set(DATASETS), "unexpected fixed-release member set")
        for name in GROUPS:
            _require(isinstance(handle[name], h5py.Group), f"{name}: expected group")
            _require(not handle[name].attrs, f"{name}: unexpected group attributes")
        metadata = _metadata(handle, expected)
        dq = _mask(handle, "quality/simple", "DQ", DQ_NAMES, DQ_DESCRIPTIONS, "S10", "S22")
        injection = _mask(
            handle,
            "quality/injections",
            "Inj",
            INJECTION_NAMES,
            INJECTION_DESCRIPTIONS,
            "S17",
            "S29",
        )
        dataset = _dataset(handle, "strain/Strain", (NPOINTS,), "float64")
        attributes = _attributes(
            dataset,
            {
                "Npoints": NPOINTS,
                "Xlabel": "GPS time",
                "Xspacing": 1.0 / RATE,
                "Xstart": GPS_START,
                "Xunits": "second",
                "Ylabel": "Strain",
                "Yunits": "",
            },
        )
        strain = dataset[()]
        _require(not np.isinf(strain).any(), "strain contains infinite samples")
        per_second = []
        for second, bitfield in enumerate(dq["raw_bitfields"]):
            block = strain[second * RATE : (second + 1) * RATE]
            finite, missing = int(np.isfinite(block).sum()), int(np.isnan(block).sum())
            present = bool(bitfield & 1)
            _require(
                (present and finite == RATE and missing == 0)
                or (not present and finite == 0 and missing == RATE),
                f"DATA/strain consistency failure in GPS second {GPS_START + second}",
            )
            per_second.append(
                {
                    "gps_start": GPS_START + second,
                    "gps_end_exclusive": GPS_START + second + 1,
                    "DATA": present,
                    "finite_samples": finite,
                    "nan_samples": missing,
                }
            )
        strain_report = {
            "dataset": dataset.name,
            "dtype": str(dataset.dtype),
            "shape": list(dataset.shape),
            "attributes": attributes,
            "sample_grid": {
                "representation": "implicit index grid; no separate time array",
                "time_scale": "GPS",
                "unit": "second",
                "rate_hz": RATE,
                "first_sample": str(Fraction(GPS_START)),
                "spacing": str(Fraction(1, RATE)),
                "last_sample": str(Fraction(GPS_START) + Fraction(NPOINTS - 1, RATE)),
                "end_exclusive": str(Fraction(GPS_START + DURATION)),
            },
            "finite_samples": int(np.isfinite(strain).sum()),
            "nan_samples": int(np.isnan(strain).sum()),
            "infinite_samples": 0,
            "per_second_DATA_consistency": per_second,
        }
    warnings = [
        {
            "code": "NO_INJECTION_FLAG_NOT_SET",
            "flag": flag["name"],
            "zero_intervals_gps": flag["zero_intervals_gps"],
            "meaning": "This no-injection flag is not asserted. No scientific exclusion is applied here.",
        }
        for flag in injection["flags"]
        if flag["zero_intervals_gps"]
    ]
    missing_intervals = [
        {
            "gps_start": start,
            "gps_end_exclusive": end,
            "reason": "DATA bit zero; corresponding strain samples are NaN",
        }
        for start, end in dq["flags"][0]["zero_intervals_gps"]
    ]
    return {
        "filename": expected["filename"],
        "status": "identity_and_structure_verified",
        "identity": {key: expected[key] for key in ("bytes", "md5", "sha256")},
        "metadata": metadata,
        "strain": strain_report,
        "data_quality": dq,
        "hardware_injection_flags": injection,
        "warnings": warnings,
        "missing_and_excluded_by_DATA": missing_intervals,
        "analysis_selection": {
            "rule": "Only DATA-bit absence is recorded as exclusion in this qualification step.",
            "other_quality_and_injection_flags": "retained in full; no science-specific mask selected",
        },
    }


def inspect_pair(input_dir):
    """Return the fixed-pair qualification report; write nothing and fetch nothing."""
    directory = Path(input_dir)
    # Bind both complete byte strings before any HDF5 parser sees either file.
    payloads = [_verified_bytes(directory, expected) for expected in FILES]
    try:
        detectors = [
            _inspect(payload, expected) for payload, expected in zip(payloads, FILES, strict=True)
        ]
    except (OSError, KeyError, TypeError, OverflowError) as error:
        raise ValueError("verified input failed fixed-release HDF5 inspection") from error
    return {
        "schema_version": "gwosc-fixed-pair-qualification-v1",
        "status": "identity_and_structure_verified",
        "event": "GW150914",
        "strain_product_version": "V2",
        "detectors": detectors,
        "interpretation_boundary": {
            "dimensionless_strain": "publisher interpretation; the literal strain Yunits attribute is empty",
            "C02_calibration": "external publisher release identification, not a literal calibration header",
            "calibration_uncertainty": "applicable artifact values, interpolation and correlations remain unqualified",
            "scientific_fit_readiness": "not established by identity, structure, finite samples or quality flags",
            "prior_access": "known public reference event; not blind evaluation data",
            "native_gravity_comparison": "no native forward law or DET-versus-GR inference supplied",
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        report = inspect_pair(arguments.input_dir)
    except ValueError as error:
        parser.exit(1, f"input qualification refused: {error}\n")
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
