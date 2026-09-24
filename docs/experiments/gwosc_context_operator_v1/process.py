"""Evaluate the eight RI-55 context rows after frozen synthetic qualification.

The only central scientific input is the pinned RI-53 REFERENCE.json export.
No envelope is inferred. This driver writes one complete sensitivity report to
a fresh directory outside Git checkouts; a computational failure is explicit,
has no accepted bound, and returns a failing exit status.
"""

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import stat
import sys


CHECK_PIN = {"bytes": 36039, "sha256": "f68a8f54629f61a2e1e3bf8315c978167074c454efa097e16150d1fb7b3f106e"}
INPUT_PIN = {"bytes": 1633767,
             "sha256": "24c291c9f4f160fe3cb7ca75926ccbed2ba1fe1559f8badc130f3d14dc3e407d"}
INPUT_ARRAY_SHA256 = "e34926cba71051771bdea7a75f26ac207dc45c59a16c9142edacc0b154efc52f"
DEPENDENCIES = {
    "ri53_processor": {"path": "gwosc_nr_comparison_v1/process.py", "bytes": 14909,
        "sha256": "374ff49a09c37aca4337631a275cef11a36e124e4bf56e2cdcb6c0d7988e34d4"},
    "ri53_qualifier": {"path": "gwosc_nr_comparison_v1/qualify.py", "bytes": 13916,
        "sha256": "e0d63265d812a02a2524c1f8f9a712465a45afec165859567859b4a5d5802823"},
    "ri53_qualification": {"path": "gwosc_nr_comparison_v1/QUALIFICATION_REPORT.json", "bytes": 15544,
        "sha256": "dab0822ae97639e16674bea6b059d4d67fae48dc725ce9c24576db0408339efe"},
    "ri53_processing": {"path": "gwosc_nr_comparison_v1/PROCESSING_REPORT.json", "bytes": 28405,
        "sha256": "6e3e2f85c2d05274e9919921b56be8a53bef41f01a81b1039e490925c4a3bb4f"},
    "ri50_inspector": {"path": "gwosc_nr_reference_v1/inspect_reference.py", "bytes": 11692,
        "sha256": "8e4d69e31d694431e798baaa7f567dbe1723a7dce13d7ed7ab8ecf9cabe81072"},
}
BOUNDARIES = {
    "exact_operator": "Exact rational coefficients and the prescribed finite odd-padding/startup operator; enclosures are conservative, not attained numeric extrema.",
    "rounded_production": "No uniform bound on rounded production filtering over an extension box is supplied.",
    "domain": "Eight named rows only; a finite L=4096 extension per side with artificial outer endpoints, not infinite physical continuation.",
    "envelope": "No physical M is inferred. A caller-supplied rational envelope, if present, is an externally declared assumption only.",
    "input": "Only unchanged RI-53 input_hex values enter the context dot products. Original printed time metadata and nominal index clock remain distinct.",
    "inference": "No calibrated uncertainty, waveform fit, timing estimate, significance, physical agreement, geometry or DET-versus-GR conclusion.",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(payload):
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def bound_bytes(path, pin, label):
    require(type(pin.get("bytes")) is int and pin["bytes"] > 0 and
            type(pin.get("sha256")) is str and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]),
            label + ": source or receipt pin not frozen")
    try:
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_size == pin["bytes"],
                label + ": expected pinned regular file")
        with path.open("rb") as stream:
            payload = stream.read(pin["bytes"] + 1)
    except OSError as error:
        raise ValueError(label + ": cannot read file") from error
    require(identity(payload) == {"bytes": pin["bytes"], "sha256": pin["sha256"]},
            label + ": snapshot identity mismatch")
    return payload


def load_check(payload, path):
    spec = importlib.util.spec_from_file_location("ri57_pinned_check", path)
    require(spec is not None and spec.loader is not None, "cannot specify checker source")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    exec(compile(payload, str(path), "exec"), module.__dict__)
    return module


def admission(path, expected_bytes, expected_sha256):
    require(type(expected_bytes) is int and 0 < expected_bytes <= 128 * 1024 * 1024,
            "qualification receipt bytes must be in [1, 134217728]")
    require(type(expected_sha256) is str and re.fullmatch(r"[0-9a-f]{64}", expected_sha256),
            "qualification receipt requires lowercase SHA-256")
    check_path = Path(__file__).resolve().parent / "check.py"
    source = bound_bytes(check_path, CHECK_PIN, "checker source")
    receipt_bytes = bound_bytes(Path(path), {"bytes": expected_bytes, "sha256": expected_sha256},
                               "qualification receipt")
    check = load_check(source, check_path)
    admitted = check.admission()
    report = check.parse_json(receipt_bytes)
    check.validate_qualification(report, admitted)
    return {"check": check, "numeric": admitted, "qualification": report,
            "qualification_identity": identity(receipt_bytes)}


def reconstruct_rows(admitted):
    check = admitted["check"]
    rows = check.build_rows(admitted["numeric"])
    previous = {item["detail"]["row"]["row"]: item["detail"]["row"]
                for item in admitted["qualification"]["gates"] if item["id"].startswith("enclosure:")}
    require(set(previous) == set(check.ROWS), "receipt lacks fixed row certificates")
    for row in rows:
        require(check.canonical(check.row_summary(row)) == check.canonical(previous[row["row"]]),
                "reconstructed coefficient row differs from qualified receipt")
    return rows


def provenance(admitted):
    """Bind published RI-53 processing/source receipts without re-reading raw NR."""
    check = admitted["check"]
    base = Path(__file__).resolve().parent.parent
    payloads = {name: check.bound_bytes(base / pin["path"], pin, name)
                for name, pin in DEPENDENCIES.items()}
    prior = check.parse_json(payloads["ri53_processing"])
    qual = check.parse_json(payloads["ri53_qualification"])
    require(prior["schema_version"] == "ri53-nr-processing-record-v1" and
            prior["status"] == "nominal_reference_processed_and_audited" and
            prior["exported_reference_file"] == {"filename": "REFERENCE.json", **INPUT_PIN},
            "RI-53 processing does not bind this input export")
    require(prior["source_identity"]["process"] == {k: DEPENDENCIES["ri53_processor"][k] for k in ("bytes", "sha256")} and
            prior["source_identity"]["qualifier"] == {k: DEPENDENCIES["ri53_qualifier"][k] for k in ("bytes", "sha256")},
            "RI-53 source identities differ")
    require(prior["source_identity"]["published_dependencies"]["reference_inspector"] ==
            {"path": "gwosc_nr_reference_v1/inspect_reference.py", **{k: DEPENDENCIES["ri50_inspector"][k] for k in ("bytes", "sha256")}},
            "RI-50 inspection source identity differs")
    require(prior["short_record_qualification_identity"] == identity(payloads["ri53_qualification"]) and
            check.canonical(prior["short_record_qualification"]) == check.canonical(qual) and
            qual["status"] == "all_short_record_gates_passed" and
            check.canonical(prior["current_processing_runtime"]) == check.canonical(admitted["numeric"]["runtime"]) and
            prior["coefficient_manifest_sha256"] == check.MANIFEST_SHA256 and
            prior["recipe_sha256"] == check.RECIPE_SHA256,
            "RI-53 qualification/runtime/coefficient provenance differs")
    require(prior["input_array_identity"]["sha256"] == INPUT_ARRAY_SHA256 and
            prior["actual_scale_relative_audit"]["passed"] is True,
            "RI-53 input-array qualification differs")
    return prior


def read_reference(path, admitted, prior):
    check = admitted["check"]
    payload = check.bound_bytes(Path(path), INPUT_PIN, "RI-53 central export")
    exported = check.parse_json(payload)
    require(exported["schema_version"] == "ri53-nominal-nr-reference-v1" and
            exported["coefficient_manifest_sha256"] == check.MANIFEST_SHA256 and
            exported["recipe_sha256"] == check.RECIPE_SHA256 and
            check.canonical(exported["source_identity"]) == check.canonical(prior["source_identity"]) and
            exported["short_record_qualification_identity"] == prior["short_record_qualification_identity"],
            "RI-53 central export source binding differs")
    reference = exported["reference"]
    require(type(reference["sample_count"]) is int and reference["sample_count"] == check.N and
            type(reference["nominal_filter_rate_hz"]) is int and reference["nominal_filter_rate_hz"] == 4096,
            "RI-53 central dimensions or nominal clock differ")
    rows = reference["rows"]
    require(type(rows) is list and len(rows) == check.N, "incomplete central export")
    values, time_metadata, hex_values = [], [], []
    for index, row in enumerate(rows):
        require(type(row) is dict and type(row["index"]) is int and row["index"] == index and
                type(row["input_hex"]) is str, "central row index or input representation differs")
        value = float.fromhex(row["input_hex"])
        require(math.isfinite(value) and value.hex() == row["input_hex"], "noncanonical/nonfinite input_hex")
        values.append(value)
        hex_values.append(row["input_hex"])
        time_metadata.append({key: row[key] for key in ("index", "line_number", "time_token", "time_exact", "placed_time_exact")})
    array_id = check.array_identity(values, check.N)
    require(array_id["sha256"] == INPUT_ARRAY_SHA256 and
            check.canonical(array_id) == check.canonical(reference["input_array_identity"]) and
            check.canonical(array_id) == check.canonical(prior["input_array_identity"]),
            "unchanged binary64 input array binding failed")
    return tuple(Fraction.from_float(value) for value in values), {
        "export_identity": identity(payload), "input_array_identity": array_id,
        "input_hex_identity": identity(check.canonical(hex_values)),
        "original_time_metadata_identity": identity(check.canonical(time_metadata)),
        "original_placement": exported["placement"], "nominal_filter_rate_hz": 4096,
        "conversion": "Each unchanged canonical input_hex parsed once as binary64, then converted exactly to Fraction; strain tokens and filtered_hex are not used.",
    }


def source_identity(admitted):
    check = admitted["check"]
    return {"process": identity(Path(__file__).read_bytes()), "check": CHECK_PIN,
            "engine": check.ENGINE_PIN, "oracle": check.ORACLE_PIN,
            "published_numeric_dependencies": check.DEPENDENCIES, "published_input_dependencies": DEPENDENCIES}


def base_report(admitted):
    check = admitted["check"]
    return {"schema_version": "ri57-context-sensitivity-v1", "dimensions": {"N": check.N, "L": check.L, "T": check.T},
        "selected_rows": list(check.ROWS), "source_identity": source_identity(admitted),
        "qualification_identity": admitted["qualification_identity"],
        "qualification_status": admitted["qualification"]["status"],
        "runtime": admitted["numeric"]["runtime"], "arithmetic_contract": admitted["numeric"]["arithmetic"],
        "coefficient_manifest_sha256": check.MANIFEST_SHA256, "design_sha256": check.DESIGN_SHA256,
        "interpretation_boundary": BOUNDARIES,
        "rounded_production_status": "not_bounded_by_this_exact_operator_report"}


def evaluate(rows, values, envelope_value, admitted, input_record):
    check = admitted["check"]
    peak = max(map(abs, values))
    threshold = peak / 10**12
    results, failures = [], []
    for row in rows:
        context = check.context_interval(row["a"], values)
        try:
            check.require_width(context, threshold, "actual scale-relative context", peak == 0)
            check.require_width(row["gain"], max(Fraction(1), row["gain"][1]) / 10**12, "gain")
            check.validate_row_status(row["operator_status"], row["b"])
        except ValueError as error:
            failures.append({"row": row["row"], "error": str(error),
                             "valid_context_interval": check.encoded_interval(context)})
            continue
        result = {**check.row_summary(row), "rigorous_status": "certified_with_pilot_widths",
                  "context_interval": check.encoded_interval(context),
                  "context_width_exact": str(context[1] - context[0]),
                  "context_width_limit_exact": str(threshold)}
        if envelope_value is not None:
            amplitude = envelope_value["value"]
            absolute = check.abs_interval(context)
            bound = (absolute[0] + amplitude * row["gain"][0],
                     absolute[1] + amplitude * row["gain"][1])
            result["conditional_bound_interval"] = check.encoded_interval(bound)
            result["bound_interpretation"] = "Enclosure of the exact rowwise supremum; upper endpoint is a conservative bound, not a numerically demonstrated attaining value."
        results.append(result)
    report = {**base_report(admitted), "input": input_record, "input_peak_exact": str(peak),
        "actual_context_width_rule": "1e-12*maxabs(input), without a unit floor; exactly [0,0] at zero input",
        "failures": failures, "status": "sensitivity_certified" if not failures else "sensitivity_failed",
        "rigorous_status": "all_eight_selected_rows_certified" if not failures else "no_accepted_pilot_bound",
        # A failed pilot retains diagnostics separately, never partially accepted rows.
        "rows": results if not failures else [], "unaccepted_row_diagnostics": results if failures else []}
    if envelope_value is not None:
        report["declared_envelope"] = {key: envelope_value[key] for key in ("numerator", "denominator", "label")}
    return report


def external_destination(path):
    path = Path(path)
    require(path.name not in ("", ".", "..") and not path.exists() and not path.is_symlink(),
            "output destination must be a fresh leaf")
    require(path.parent.is_dir(), "output parent must exist")
    resolved = path.parent.resolve() / path.name
    require(not any((parent / ".git").exists() for parent in (resolved.parent, *resolved.parent.parents)),
            "output destination must be outside Git checkouts")
    return resolved


def write_report(destination, payload):
    destination = external_destination(destination)
    try:
        destination.mkdir(mode=0o700)
        with (destination / "SENSITIVITY_REPORT.json").open("xb") as stream:
            stream.write(payload)
    except OSError as error:
        raise ValueError("report write failed; inspect the new destination for an incomplete file") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qualification-report", type=Path, required=True)
    parser.add_argument("--expected-qualification-bytes", type=int, required=True)
    parser.add_argument("--expected-qualification-sha256", required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--envelope-numerator")
    parser.add_argument("--envelope-denominator")
    parser.add_argument("--envelope-label")
    args = parser.parse_args(argv)
    admitted = None
    phase = "qualification_admission"
    try:
        destination = external_destination(args.output_dir)
        admitted = admission(args.qualification_report, args.expected_qualification_bytes,
                             args.expected_qualification_sha256)
        check = admitted["check"]
        supplied_envelope = check.envelope(args.envelope_numerator, args.envelope_denominator, args.envelope_label)
        # Qualification, runtime and all reconstructed enclosure identities/widths
        # pass before opening any actual central sample or its processing summary.
        phase = "reconstruct_qualified_enclosures_before_actual_input"
        rows = reconstruct_rows(admitted)
        phase = "verify_published_provenance_before_actual_input"
        prior = provenance(admitted)
        phase = "read_verified_central_export"
        values, input_record = read_reference(args.input, admitted, prior)
        phase = "actual_scale_relative_context_audit"
        report = evaluate(rows, values, supplied_envelope, admitted, input_record)
        check.check_coefficients(admitted["numeric"])
    except (ValueError, TypeError, KeyError, OSError, ArithmeticError, RuntimeError, MemoryError) as error:
        if admitted is None:
            parser.exit(1, "context processing refused before admission: " + str(error) + "\n")
        check = admitted["check"]
        report = {**base_report(admitted), "status": "sensitivity_failed", "rigorous_status": "no_accepted_pilot_bound",
                  "rows": [], "failures": [{"phase": phase, "error_type": type(error).__name__, "error": str(error)}]}
    try:
        payload = check.export_json(report)
        write_report(destination, payload)
        sys.stdout.buffer.write(check.export_json({"status": report["status"],
            "output": {"filename": "SENSITIVITY_REPORT.json", **identity(payload)}}))
        return 0 if report["status"] == "sensitivity_certified" else 1
    except (ValueError, OSError) as error:
        parser.exit(1, "context report publication refused: " + str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
