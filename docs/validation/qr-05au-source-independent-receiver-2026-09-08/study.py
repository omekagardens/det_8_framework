"""QR-05AU source-independent zero-intercept receiver orchestration."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import platform
import resource
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05au-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05au.py")
AT = HERE.parent / "qr-05at-bank-portability-2026-09-08/results.json"
AT_ID = {
    "bytes": 1147189,
    "sha256": "3fe96ced94f7b4d45feec43d0415a908d656825e21f04a6796329825de4d651a",
}
MAX_CAPTURE_BYTES = 128 * 1024 * 1024
MAX_WORKING_BYTES = 192 * 1024 * 1024
FAMILIES = ("grid", "warp")
COUNT_FIELDS = (
    "coarse_values",
    "bank_values",
    "source_columns",
    "target_rows",
    "supplement_values",
    "receiver_values",
    "input_matrix_entries",
    "interface_entries",
    "source_check_entries",
    "compact_decoder_entries",
    "raw_decoder_entries",
    "bank_prediction_entries",
    "bank_residual_entries",
    "source_prediction_entries",
    "source_residual_entries",
    "bank_controls",
    "bank_control_entries",
    "collisions",
    "collision_entries",
    "recovered_rows",
    "failed_rows",
)
CHECK_FIELDS = (
    "selected_filter_identity",
    "source_inputs_consistent",
    "source_independent_certificate",
    "decoder_bank_identity",
    "decoder_source_identity",
    "restricted_application",
    "collision_valid",
    "complete_classification",
)
SCOPE = (
    "source_dictionary_changed",
    "geometry_reintegrated",
    "old_collision_replayed",
    "old_decoder_modified",
    "filters_reselected",
    "measurements_added",
    "normalization_row_added",
    "source_dependent_fit_performed",
    "physical_bank_controls_established",
    "full_field_recovery_tested",
    "physical_interface_insufficiency_proved",
    "minimality_recomputed",
    "empirical_noise_calibrated",
    "unknown_geometry_reconstructed",
    "quantum_channel_constructed",
    "gravity_derived",
    "ret_integration_tested",
    "lean_verification_performed",
    "generic_production_API_hardened",
    "fixed_affine_families_run",
    "older_executors_run",
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def plain_bytes(path):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), "not a plain evidence file")
    require(path.stat().st_size <= MAX_CAPTURE_BYTES, "capture byte cap")
    raw = path.read_bytes()
    require(len(raw) <= MAX_CAPTURE_BYTES, "capture byte cap")
    return raw


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def ident(path):
    raw = plain_bytes(path)
    return {"bytes": len(raw), "sha256": digest(raw)}


def native(value, depth=0):
    require(depth <= 128, "native depth")
    kind = type(value)
    if value is None or kind in (bool, str):
        return
    if kind is int:
        require(abs(value).bit_length() <= 4096, "retained component bits")
        return
    require(kind in (list, dict), "native mathematical data required")
    if kind is dict:
        require(all(type(k) is str for k in value), "native keys")
    for child in value.values() if kind is dict else value:
        native(child, depth + 1)


def canonical(value):
    raw = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")
    require(len(raw) <= MAX_WORKING_BYTES, "working byte cap")
    return raw


def verify_suite(actual, expected):
    native(actual)
    native(expected)
    require(canonical(actual) == canonical(expected), "complete mathematical wire differs")


def prior_document():
    require(ident(AT) == AT_ID, "AT artifact changed")
    return json.loads(plain_bytes(AT))


def identities():
    previous = prior_document()
    prior = {str(AT.relative_to(HERE.parent)): AT_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AT.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def project_inputs(at_families):
    require(type(at_families) is list and len(at_families) == 2, "AT family inventory")
    require([f["problem"]["family"] for f in at_families] == list(FAMILIES), "AT family order")
    problems = []
    for family in at_families:
        old = family["problem"]
        p = {
            "family": old["family"],
            "target_labels": old["target_labels"],
            "coarse_map": family["lineage"]["coarse_map"],
            "filters": old["filters"],
            "geometric": old["geometric"],
            "selected_rows": old["selected_rows"],
            "bank": old["bank"],
            "observations": old["observations"],
            "targets": old["targets"],
        }
        require(
            type(p["selected_rows"]) is list and len(p["selected_rows"]) == 5,
            "AT selection inventory",
        )
        require(
            type(p["target_labels"]) is list and len(p["target_labels"]) == 64,
            "AT target inventory",
        )
        for key, rows, width in (
            ("coarse_map", 32, 48),
            ("filters", 5, 48),
            ("geometric", 64, 48),
            ("bank", 48, 108),
            ("observations", 32, 108),
            ("targets", 64, 108),
        ):
            require(
                type(p[key]) is list
                and len(p[key]) == rows
                and all(type(row) is list and len(row) == width for row in p[key]),
                "AT matrix inventory",
            )
        problems.append(copy.deepcopy(p))
    return problems, at_families


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05au_" + name, HERE / filename)
    require(spec is not None and spec.loader is not None, "engine loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def controls(families):
    require(type(families) is list and len(families) == 2, "complete fixed inventory")
    require([f["problem"]["family"] for f in families] == list(FAMILIES), "family order")
    for family in families:
        require(set(family["checks"]) == set(CHECK_FIELDS), "complete check fields")
        require(all(v is True for v in family["checks"].values()), "family check failed")
        cert, decoder = family["certificate"], family["decoder"]
        q = len(family["problem"]["geometric"])
        require(
            type(cert["recoverable"]) is bool and type(decoder["complete"]) is bool,
            "native completeness",
        )
        require(cert["recoverable"] == (not cert["failed_rows"]), "certificate completeness")
        require(decoder["complete"] == cert["recoverable"], "decoder completeness")
        require((cert["collision"] is None) == cert["recoverable"], "collision presence")
        require(
            sorted(cert["recoverable_rows"] + cert["failed_rows"]) == list(range(q)),
            "complete response inventory",
        )
        verify_suite(decoder["target_rows"], cert["recoverable_rows"])
        require(len(cert["row_coefficients"]) == q, "row coefficient inventory")
        for i, row in enumerate(cert["row_coefficients"]):
            require((row is None) == (i in cert["failed_rows"]), "failed rows must be null")
        require(len(decoder["matrix"]) == len(cert["recoverable_rows"]), "recovered decoder rows")
        require(
            len(family["bank_controls"]) == len(family["problem"]["bank"]) + 1,
            "complete zero/unit controls",
        )
    return dict.fromkeys(CHECK_FIELDS, True)


def historical_bridges(families, previous):
    expected, _ = project_inputs(previous)
    verify_suite([f["problem"] for f in families], expected)
    controls(families)
    return {
        "AT_selected_families": list(FAMILIES),
        "AT_interface_inputs_equal": True,
        "AT_target_inputs_equal": True,
        "AT_source_inputs_equal": True,
        "old_affine_decoder_replayed": False,
        "old_bank_defect_replayed": False,
        "other_historical_mathematics_replayed": False,
        "older_executors_run": False,
    }


def payload_sizes(families):
    return [
        {
            "family": f["problem"]["family"],
            "input_bytes": len(canonical(f["problem"])),
            "interface_bytes": len(canonical(f["interface"])),
            "source_bytes": len(canonical(f["source"])),
            "certificate_bytes": len(canonical(f["certificate"])),
            "decoder_bytes": len(canonical(f["decoder"])),
            "bank_controls_bytes": len(canonical(f["bank_controls"])),
            "receiver_map_bytes": len(
                canonical({k: f["decoder"][k] for k in ("target_rows", "matrix")})
            ),
            "native_family_bytes": len(canonical(f)),
        }
        for f in families
    ]


def assemble_suite(families, previous):
    expected, consumed = load_inputs()
    verify_suite(previous, consumed)
    verify_suite([f["problem"] for f in families], expected)
    controls(families)
    for family in families:
        require(set(family["counts"]) == set(COUNT_FIELDS), "complete count inventory")
        require(
            all(type(v) is int and v >= 0 for v in family["counts"].values()),
            "native nonnegative counts",
        )
    return {
        "families": families,
        "prior_bridges": historical_bridges(families, previous),
        "payload_sizes": payload_sizes(families),
        "totals": {
            "families": 2,
            **{key: sum(f["counts"][key] for f in families) for key in COUNT_FIELDS},
        },
        "scope": dict.fromkeys(SCOPE, False),
    }


def run_suite(route="compare"):
    require(route in ("compare", "primary", "reference"), "unknown route")
    problems, previous = load_inputs()
    names = ("primary", "reference") if route == "compare" else (route,)
    engines = [load_engine(name) for name in names]
    families = []
    for problem in problems:
        outputs = []
        for engine in engines:
            supplied = copy.deepcopy(problem)
            outputs.append(engine.build_family(supplied))
            verify_suite(supplied, problem)
        if len(outputs) == 2:
            verify_suite(outputs[0], outputs[1])
        families.append(outputs[0])
    suite = assemble_suite(families, previous)
    native(suite)
    canonical(suite)
    return suite


def capture(path=None, route="compare", verify=False):
    path = Path(RESULT if path is None else path)
    require(
        sys.flags.isolated and sys.pycache_prefix,
        "isolated Python/external bytecode cache required",
    )
    cache = Path(sys.pycache_prefix).resolve()
    require(
        cache != Path(cache.anchor) and not cache.is_relative_to(ROOT), "external bytecode cache"
    )
    if not verify and (path.exists() or path.is_symlink()):
        raise FileExistsError("evidence exists; never overwrite")
    before = identities()
    raw_before = plain_bytes(path) if verify else None
    if verify:
        existing = json.loads(raw_before)
        require(
            type(existing) is dict
            and set(existing)
            == {
                "schema_version",
                "source_ledger",
                "prior_artifacts",
                "ancestor_sources",
                "suite",
                "runtime",
            },
            "capture fields",
        )
        require(existing["schema_version"] == SCHEMA, "capture schema")
        require(canonical(existing) == raw_before, "noncanonical capture")
        for key, value in before.items():
            verify_suite(existing[key], value)
    start = time.perf_counter()
    suite = run_suite(route)
    native(suite)
    suite_raw = canonical(suite)
    seconds = time.perf_counter() - start
    verify_suite(before, identities())
    if verify:
        verify_suite(suite, existing["suite"])
        require(plain_bytes(path) == raw_before, "capture changed during replay")
        raw = raw_before
    else:
        report = {
            "schema_version": SCHEMA,
            **before,
            "suite": suite,
            "runtime": {
                "route": route,
                "python": sys.version,
                "platform": platform.platform(),
                "executable": sys.executable,
                "isolated": bool(sys.flags.isolated),
                "optimized": sys.flags.optimize,
                "bytecode_cache": str(cache),
                "suite_seconds": seconds,
                "rss_high_water_at_suite_end": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "rss_units": "bytes" if sys.platform == "darwin" else "KiB",
                "scope": "verification timing; excludes final serialization; not application benchmark",
            },
        }
        raw = canonical(report)
        require(len(raw) <= MAX_CAPTURE_BYTES, "capture byte cap")
        with path.open("xb") as stream:
            stream.write(raw)
        require(plain_bytes(path) == raw, "capture readback")
    verify_suite(before, identities())
    return {
        "status": "VERIFIED_EXACT_REPLAY" if verify else "CREATED_EXACT_FINITE_RESULT",
        "route": route,
        "path": str(path),
        "bytes": len(raw),
        "sha256": digest(raw),
        "suite_bytes": len(suite_raw),
        "suite_sha256": digest(suite_raw),
        "seconds": seconds,
        "totals": suite["totals"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--route", choices=("compare", "primary", "reference"), default="compare")
    parser.add_argument("--artifact", type=Path, default=RESULT)
    args = parser.parse_args()
    print(json.dumps(capture(args.artifact, args.route, args.verify)))


if __name__ == "__main__":
    main()
