"""Process the fixed public NR snapshot after admitted length-2769 qualification.

Write REFERENCE.json and PROCESSING_REPORT.json only to a new external directory.
The entire actual output receives the stricter input-scale-relative Decimal audit.
No amplitude adjustment, observed-data processing, fit or timing estimate occurs.
"""

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import stat
import sys


QUALIFIER = {"bytes": 13916,
             "sha256": "e0d63265d812a02a2524c1f8f9a712465a45afec165859567859b4a5d5802823"}
DEPENDENCIES = {
    "reference_inspector": {"path": "gwosc_nr_reference_v1/inspect_reference.py", "bytes": 11692,
                            "sha256": "8e4d69e31d694431e798baaa7f567dbe1723a7dce13d7ed7ab8ecf9cabe81072"},
    "reference_inspection": {"path": "gwosc_nr_reference_v1/REFERENCE_REPORT.json", "bytes": 1439846,
                             "sha256": "0a5ce388d722c185ce7de8fc81d36a69d9d98991ccba4235c9fb52817891de06"},
    "comparison_contract": {"path": "gwosc_nr_reference_v1/QUALIFICATION.md", "bytes": 12524,
                            "sha256": "cbc0d76415399b894794d6790692e57fac259117b19fe6ec1c93035278b70af2"},
    "observed_crop": {"path": "gwosc_nominal_result_v1/CROP.json", "bytes": 395470,
                      "sha256": "a580481b9f6ea8dbb90242f12023817709ee7ac208d504110966f01f353592e7"},
    "observed_processing": {"path": "gwosc_nominal_result_v1/PROCESSING_REPORT.json", "bytes": 159384,
                            "sha256": "98bf0c53d5b988d3bb2aaa5f60c0fbcd87512501dd1137175b25589cc4856820"},
}
INPUT_IDENTITY = {"bytes": 142345,
                  "sha256": "ed49c3e83f90e70ac85386f183031b7de3d3d6aa78e75a7d284e5a53a5cc0b76"}
OBSERVED_SHA256 = "79cc42fd39adc57b28323f0409def8ddbe17de6b136de43a39985d08b3691770"
PLACEMENT = {"offset_rational": "53/125", "time_origin_gps": 1126259462,
             "convention": "historical illustrative V1-to-V2 transfer; precise V2 alignment unresolved"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(payload):
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def bound_bytes(path, pin, label):
    try:
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode), label + ": expected regular file")
        require(info.st_size == pin["bytes"], label + ": byte count mismatch")
        with path.open("rb") as stream:
            payload = stream.read(pin["bytes"] + 1)
    except OSError as error:
        raise ValueError(label + ": cannot read file") from error
    require(identity(payload) == {"bytes": pin["bytes"], "sha256": pin["sha256"]},
            label + ": snapshot identity mismatch")
    return payload


def load_qualifier(path, payload):
    spec = importlib.util.spec_from_file_location("ri53_pinned_qualification", path)
    require(spec is not None and spec.loader is not None, "cannot specify qualifier source")
    module = importlib.util.module_from_spec(spec)
    exec(compile(payload, str(path), "exec"), module.__dict__)
    return module


def admission(qualification_path, expected_bytes, expected_sha256):
    require(type(expected_bytes) is int and 0 < expected_bytes <= 1024 * 1024,
            "qualification receipt byte count must be in [1, 1048576]")
    require(type(expected_sha256) is str and
            re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is not None,
            "qualification receipt requires lowercase SHA-256")
    base = Path(__file__).resolve().parent.parent
    qualifier_path = Path(__file__).resolve().parent / "qualify.py"
    qualifier_bytes = bound_bytes(qualifier_path, QUALIFIER, "qualifier source")
    # Bind all local publication bytes and the reviewed receipt before execution.
    payloads = {name: bound_bytes(base / pin["path"], pin, name)
                for name, pin in DEPENDENCIES.items()}
    qualification_bytes = bound_bytes(Path(qualification_path),
        {"bytes": expected_bytes, "sha256": expected_sha256}, "qualification receipt")
    qualifier = load_qualifier(qualifier_path, qualifier_bytes)
    admitted = qualifier.admission()
    qualification = json.loads(qualification_bytes)
    qualifier.validate_qualification(qualification, admitted)
    inspection = json.loads(payloads["reference_inspection"])
    require(inspection["schema_version"] == "gwosc-nr-reference-inspection-v1" and
            inspection["status"] == "snapshot_identity_and_numeric_structure_verified" and
            inspection["input_identity"] == INPUT_IDENTITY and
            inspection["source_identity"]["sha256"] == DEPENDENCIES["reference_inspector"]["sha256"] and
            inspection["text_structure"]["numeric_row_count"] == qualifier.LENGTH,
            "accepted reference inspection identity or length mismatch")
    crop = json.loads(payloads["observed_crop"])
    observed_report = json.loads(payloads["observed_processing"])
    require(observed_report["exported_crop_file"]["sha256"] == DEPENDENCIES["observed_crop"]["sha256"],
            "observed processing-to-crop identity mismatch")
    observed = {"crop_json_identity": identity(payloads["observed_crop"]),
                "grid": crop["grid"], "h1": crop["detectors"][0]}
    require(hashlib.sha256(qualifier.canonical(observed)).hexdigest() == OBSERVED_SHA256,
            "immutable observed H1 object mismatch")
    inspector = qualifier.load_module("nr_inspector", base / DEPENDENCIES["reference_inspector"]["path"],
                                      payloads["reference_inspector"])
    return {"qualifier": qualifier, "numeric": admitted, "inspector": inspector,
            "inspection": inspection, "observed": observed,
            "qualification": qualification,
            "qualification_identity": identity(qualification_bytes)}


def read_reference(path, admitted):
    inspector = admitted["inspector"]
    payload = inspector.verified_bytes(path, INPUT_IDENTITY["bytes"], INPUT_IDENTITY["sha256"])
    # Parse the same retained snapshot that passed the complete fixed identity.
    numeric = inspector.inspect_snapshot(payload)
    expected = {key: admitted["inspection"][key] for key in ("text_structure", "time_grid", "rows")}
    qualifier = admitted["qualifier"]
    require(qualifier.canonical(numeric) == qualifier.canonical(expected),
            "current reference rows differ from accepted complete inspection")
    rows = numeric["rows"]
    require(len(rows) == qualifier.LENGTH, "reference length differs from qualified length")
    # Each original strain token is converted to binary64 exactly once here.
    values = qualifier.np.array([float(row["strain_token"]) for row in rows],
                                dtype=qualifier.np.float64)
    qualifier.array_identity(values)
    return rows, values


def source_identity(admitted):
    return {"process": identity(Path(__file__).read_bytes()), "qualifier": QUALIFIER,
            "published_dependencies": DEPENDENCIES,
            "numerical_dependencies": admitted["qualifier"].DEPENDENCIES}


def build_outputs(rows, values, filtered, audit, admitted):
    qualifier = admitted["qualifier"]
    require(audit["passed"] is True and audit["criterion"] == "1e-9*maxabs(input)" and
            Fraction(audit["input_peak_exact"]) > 0 and
            Fraction(audit["threshold_exact"]) == Fraction(audit["input_peak_exact"]) / 10**9 and
            Fraction(audit["maximum_absolute_error_exact"]) <= Fraction(audit["threshold_exact"]),
            "actual scale-relative audit is not admitted")
    require(len(rows) == qualifier.LENGTH and audit["sample_count_compared"] == qualifier.LENGTH,
            "actual reference coverage mismatch")
    input_id, output_id = qualifier.array_identity(values), qualifier.array_identity(filtered)
    require(qualifier.canonical(input_id) == qualifier.canonical(audit["input_array_identity"]) and
            qualifier.canonical(output_id) == qualifier.canonical(audit["output_array_identity"]),
            "actual audit array identity mismatch")
    require(hashlib.sha256(qualifier.canonical(admitted["observed"])).hexdigest() == OBSERVED_SHA256,
            "observed H1 object changed")
    exported_rows = []
    for index, (row, before, after) in enumerate(zip(rows, values, filtered)):
        require(type(row["index"]) is int and row["index"] == index and
                Fraction(row["time_token"]) == Fraction(row["time_exact"]) and
                Fraction(row["strain_token"]) == Fraction(row["strain_exact"]),
                "reference row index or exact representation changed")
        exported_rows.append({key: row[key] for key in (
            "index", "line_number", "time_token", "time_exact", "strain_token", "strain_exact")})
        exported_rows[-1].update({"input_hex": float(before).hex(), "filtered_hex": float(after).hex(),
            "placed_time_exact": str(Fraction(row["time_exact"]) + Fraction(PLACEMENT["offset_rational"]))})
    provenance = source_identity(admitted)
    boundaries = {
        "reference": "Supplied data-informed scalar NR comparison, not a withheld prediction or refit.",
        "filtering": "Length-2769 stagewise odd-padding forward/backward operation on nominal 4096-Hz indices; no physical continuation or endpoint-error bound.",
        "timing": "Original printed times retained; exact 53/125-second historical placement is illustrative and precise V2 portability is unresolved.",
        "inference": "No calibrated agreement, arrival estimate, residual statistic, significance, parameter recovery, detection or DET-versus-GR result.",
    }
    reference = {
        "schema_version": "ri53-nominal-nr-reference-v1", "event": "GW150914",
        "quantity": "nominal dimensionless strain", "placement": PLACEMENT,
        "coefficient_manifest_sha256": qualifier.MANIFEST_SHA256,
        "recipe_sha256": qualifier.RECIPE_SHA256,
        "observed": admitted["observed"],
        "reference": {"sample_count": qualifier.LENGTH, "nominal_filter_rate_hz": 4096,
                      "input_identity": INPUT_IDENTITY, "input_array_identity": input_id,
                      "filtered_array_identity": output_id, "rows": exported_rows},
        "source_identity": provenance, "short_record_qualification_identity": admitted["qualification_identity"],
        "actual_scale_relative_audit": audit, "interpretation_boundary": boundaries,
    }
    reference_bytes = qualifier.export_json(reference)
    report = {
        "schema_version": "ri53-nr-processing-record-v1", "status": "nominal_reference_processed_and_audited",
        "source_identity": provenance, "input_identity": INPUT_IDENTITY,
        "short_record_qualification_identity": admitted["qualification_identity"],
        "short_record_qualification": admitted["qualification"],
        "current_processing_runtime": admitted["numeric"]["runtime"],
        "coefficient_manifest_sha256": qualifier.MANIFEST_SHA256, "recipe_sha256": qualifier.RECIPE_SHA256,
        "actual_scale_relative_audit": audit,
        "input_array_identity": input_id, "filtered_array_identity": output_id,
        "reference_time_grid": admitted["inspection"]["time_grid"], "placement": PLACEMENT,
        "observed_crop_identity": admitted["observed"]["crop_json_identity"],
        "observed_h1_identity": admitted["observed"]["h1"]["crop_identity"],
        "exported_reference_file": {"filename": "REFERENCE.json", **identity(reference_bytes)},
        "input_custody": "Qualification receipt and every source/report/manifest bound before reference access; one complete pinned snapshot supplied inspection and once-only strain-token conversion.",
        "interpretation_boundary": boundaries,
    }
    return reference_bytes, qualifier.export_json(report)


def external_destination(path):
    path = Path(path)
    require(not path.exists() and not path.is_symlink(), "output destination must not exist")
    require(path.parent.is_dir(), "output parent must exist")
    resolved = path.parent.resolve() / path.name
    require(not any((parent / ".git").exists() for parent in (resolved.parent, *resolved.parent.parents)),
            "output destination must be outside Git checkouts")
    return resolved


def write_outputs(destination, reference_bytes, report_bytes):
    destination = external_destination(destination)
    try:
        destination.mkdir(mode=0o700)
        for name, payload in (("REFERENCE.json", reference_bytes), ("PROCESSING_REPORT.json", report_bytes)):
            with (destination / name).open("xb") as stream:
                stream.write(payload)
    except OSError as error:
        raise ValueError("output write failed; inspect the new destination for partial files") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qualification-report", type=Path, required=True)
    parser.add_argument("--expected-qualification-bytes", type=int, required=True)
    parser.add_argument("--expected-qualification-sha256", required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        destination = external_destination(arguments.output_dir)
        admitted = admission(arguments.qualification_report, arguments.expected_qualification_bytes,
                             arguments.expected_qualification_sha256)
        rows, values = read_reference(arguments.input, admitted)
        qualifier = admitted["qualifier"]
        filtered, audit = qualifier.filter_audit(values, admitted["numeric"], False)
        if not audit["passed"]:
            sys.stdout.buffer.write(qualifier.export_json({
                "schema_version": "ri53-nr-processing-failure-v1", "status": "actual_numeric_gate_failed",
                "actual_scale_relative_audit": audit, "input_identity": INPUT_IDENTITY,
                "source_identity": source_identity(admitted),
                "short_record_qualification_identity": admitted["qualification_identity"],
                "current_processing_runtime": admitted["numeric"]["runtime"],
                "exports_written": False}))
            return 1
        reference_bytes, report_bytes = build_outputs(rows, values, filtered, audit, admitted)
        write_outputs(destination, reference_bytes, report_bytes)
        sys.stdout.buffer.write(qualifier.export_json({"status": "nominal_reference_processed_and_audited",
            "outputs": {"REFERENCE.json": identity(reference_bytes), "PROCESSING_REPORT.json": identity(report_bytes)}}))
        return 0
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as error:
        parser.exit(1, "reference processing refused: " + str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
