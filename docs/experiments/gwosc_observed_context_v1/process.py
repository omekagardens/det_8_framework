"""Fixed RI64 observed-context driver; no envelope, fitting or renderer.

A caller-pinned new qualification receipt and the published RI60 receipt admit
the run. All sixteen coefficient certificates must reconcile before either
observed file or the published crop is opened. The shared context module owns
the numerical reductions and same-snapshot custody. This driver publishes two
deterministic files only after every detector gate passes.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import stat
import sys


CHECK_PIN = {"bytes": 34640, "sha256": "f76bab65b4f3a4d8cde5efe292d2bfe3a5d8792048feace55308884757f38241"}
BOUNDARIES = {
    "comparison": "Three finite boundary conditions applied to identical central observed samples; the published rounded 32-second result is a baseline, not physical ground truth.",
    "selected_rows": "Actual-specific exact-operator and rounded-output bounds apply only to the eight fixed coordinates per detector.",
    "whole_vectors": "Complete production-versus-Decimal comparisons are numerical diagnostics; they are not exact-operator certificates for unexamined rows.",
    "context": "The retained recorded context is known released data. No envelope M, missing continuation, fitted alignment or model is inferred.",
    "interpretation": "No detection, residual statistic, noise estimate, calibration interval, confidence claim, DET-versus-GR test, native forward map or gravity proof.",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(payload):
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def export_json(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True,
                       allow_nan=False) + "\n").encode("ascii")


def bound_bytes(path, pin, label):
    require(type(pin.get("bytes")) is int and pin["bytes"] > 0 and
            type(pin.get("sha256")) is str and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]),
            label + ": source or receipt pin is not frozen")
    try:
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_size == pin["bytes"], label + ": expected pinned regular file")
        with path.open("rb") as stream:
            payload = stream.read(pin["bytes"] + 1)
    except OSError as error:
        raise ValueError(label + ": cannot read pinned file") from error
    require(identity(payload) == {"bytes": pin["bytes"], "sha256": pin["sha256"]}, label + ": identity changed")
    return payload


def admission(qualification_path, expected_bytes, expected_sha256):
    require(type(expected_bytes) is int and 0 < expected_bytes <= 128 * 1024 * 1024,
            "qualification byte count outside [1,134217728]")
    require(type(expected_sha256) is str and re.fullmatch(r"[0-9a-f]{64}", expected_sha256),
            "qualification receipt requires lowercase SHA-256")
    path = Path(__file__).resolve().parent / "check.py"
    source = bound_bytes(path, CHECK_PIN, "new qualifier")
    receipt = bound_bytes(Path(qualification_path), {"bytes": expected_bytes, "sha256": expected_sha256},
                          "new qualification receipt")
    spec = importlib.util.spec_from_file_location("ri64_pinned_check", path)
    require(spec is not None and spec.loader is not None, "cannot load pinned qualifier")
    check = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = check
    exec(compile(source, str(path), "exec"), check.__dict__)
    admitted = check.admission()
    qualification = check.parse_json(receipt)
    check.validate_qualification(qualification, admitted)
    return {"check": check, "admitted": admitted, "qualification": qualification,
            "qualification_identity": identity(receipt)}


def external_destination(path):
    path = Path(path)
    require(not path.exists() and not path.is_symlink() and path.name not in ("", ".", ".."),
            "output leaf must be new")
    require(path.parent.is_dir(), "output parent must exist")
    resolved = path.parent.resolve() / path.name
    require(not any((parent / ".git").exists() for parent in (resolved.parent, *resolved.parent.parents)),
            "output must be outside Git checkouts")
    return resolved


def source_identity(ready):
    check = ready["check"]
    admitted = ready["admitted"]
    return {"process": identity(Path(__file__).read_bytes()), "check": CHECK_PIN,
            "context": check.CONTEXT_PIN, "published_dependencies": admitted["shared"]["dependency_identities"],
            "design": admitted["shared"]["design_identity"]}


def build_outputs(detectors, observed, ready):
    check = ready["check"]
    shared = ready["admitted"]["shared"]
    require(type(detectors) is list and len(detectors) == 2 and
            [record["detector"] for record in detectors] == ["H1", "L1"] and
            all(record["passed"] is True for record in detectors), "both complete detector results must pass")
    common = {"event": "GW150914", "strain_product_version": "V2",
        "source_identity": source_identity(ready), "runtime": shared["runtime"],
        "qualification_identity": ready["qualification_identity"],
        "ri60_qualification_identity": shared["qualification60_identity"],
        "dimensions": {"source_count": 131072, "N": 2769, "L": 4096, "T": 10961},
        "selected_rows": list(check.ROWS), "crop_identity": observed["crop_identity"],
        "published_processing_identity": observed["processing_identity"],
        "input_custody": observed["input_custody"], "interpretation_boundary": BOUNDARIES}
    exported = {"schema_version": "ri64-observed-context-v1", **common, "detectors": detectors}
    export_bytes = export_json(exported)
    report = {"schema_version": "ri64-observed-context-processing-v1", **common,
        "status": "all_observed_context_gates_passed", "failures": [],
        "new_qualification": ready["qualification"],
        "detectors": [{"detector": record["detector"], "passed": record["passed"],
                       "complete_result_identity": identity(canonical(record))} for record in detectors],
        "complete_values_location": "All source-indexed input/output arrays, complete Decimal diagnostics and exact reductions, every maximizing index, full annotations and all selected-row interval/endpoint gates are retained in the bound OBSERVED_CONTEXT.json detector records.",
        "exported_observed_context": {"filename": "OBSERVED_CONTEXT.json", **identity(export_bytes)}}
    return export_bytes, export_json(report)


def write_outputs(destination, observed_bytes, report_bytes, validate_destination=external_destination):
    destination = validate_destination(destination)
    created = []
    made_directory = False
    try:
        destination.mkdir(mode=0o700)
        made_directory = True
        for name, payload in (("OBSERVED_CONTEXT.json", observed_bytes), ("PROCESSING_REPORT.json", report_bytes)):
            path = destination / name
            with path.open("xb") as stream:
                created.append(path)
                stream.write(payload)
    except OSError as error:
        # Remove only this call's newly created files; never an existing target.
        for path in created:
            try:
                path.unlink()
            except OSError:
                pass
        if made_directory:
            try:
                destination.rmdir()
            except OSError:
                pass
        raise ValueError("output write failed; no complete accepted two-file export was published") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qualification-report", type=Path, required=True)
    parser.add_argument("--expected-qualification-bytes", type=int, required=True)
    parser.add_argument("--expected-qualification-sha256", required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    ready = None
    phase = "source_and_current_qualification_admission"
    try:
        destination = external_destination(args.output_dir)
        ready = admission(args.qualification_report, args.expected_qualification_bytes,
                          args.expected_qualification_sha256)
        context, shared = ready["admitted"]["context"], ready["admitted"]["shared"]
        phase = "reconcile_all_sixteen_coefficients_before_observed_access"
        rows = context.reconcile_coefficients(shared)
        phase = "bind_both_snapshots_and_complete_published_crop"
        observed = context.read_verified_inputs(args.input_dir, shared)
        phase = "all_detector_numeric_and_interval_gates"
        require([record["detector"] for record in observed["detectors"]] == ["H1", "L1"], "detector order changed")
        detectors = [context.evaluate_detector(record, rows, shared) for record in observed["detectors"]]
        phase = "assemble_complete_deterministic_exports"
        export_bytes, report_bytes = build_outputs(detectors, observed, ready)
        phase = "exclusive_external_publication"
        write_outputs(destination, export_bytes, report_bytes, ready["check"].external_destination)
        sys.stdout.buffer.write(export_json({"status": "all_observed_context_gates_passed",
            "outputs": {"OBSERVED_CONTEXT.json": identity(export_bytes), "PROCESSING_REPORT.json": identity(report_bytes)}}))
        return 0
    except (ValueError, TypeError, KeyError, OSError, ArithmeticError, RuntimeError, MemoryError) as error:
        failure = {"schema_version": "ri64-observed-context-failure-v1", "status": "observed_context_failed",
                   "phase": phase, "error_type": type(error).__name__, "error": str(error), "accepted_outputs": False}
        if ready is not None:
            failure["qualification_identity"] = ready["qualification_identity"]
            failure["source_identity"] = source_identity(ready)
        sys.stdout.buffer.write(export_json(failure))
        print("observed-context processing refused at " + phase + ": " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
