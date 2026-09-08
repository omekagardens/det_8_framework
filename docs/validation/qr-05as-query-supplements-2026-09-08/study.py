"""QR-05AS query-specific minimal linear readout orchestration."""

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
SCHEMA = "det8-qr05as-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05as.py")
AR = HERE.parent / "qr-05ar-fine-response-sufficiency-2026-09-08/results.json"
AR_ID = {
    "bytes": 704842,
    "sha256": "c9ed0e299c057eb6503238a3bc5ce18352abe81bc111615464afaa6ed264e4f8",
}
MAX_CAPTURE_BYTES = 128 * 1024 * 1024
MAX_WORKING_BYTES = 192 * 1024 * 1024
FAMILIES = ("grid", "warp")
COUNT_FIELDS = (
    "source_columns",
    "coarse_values",
    "bank_values",
    "target_rows",
    "supplement_values",
    "receiver_values",
    "input_matrix_entries",
    "selected_filter_entries",
    "selected_filter_nonzero",
    "selected_bank_rows",
    "supplement_entries",
    "decision_coefficient_entries",
    "decoder_compact_entries",
    "decoder_raw_entries",
    "prediction_entries",
    "residual_entries",
    "witnesses",
    "witness_entries",
)


CHECK_FIELDS = (
    "inherited_filter_identity",
    "base_certificate",
    "greedy_selection",
    "selected_filter_identity",
    "receiver_identity",
    "witness_constraints",
    "online_witness_recovery",
    "minimality_certificate",
)


SCOPE = (
    "source_dictionary_changed",
    "geometry_reintegrated",
    "old_collision_replayed",
    "full_field_recovery_tested",
    "individual_bank_minimality_proved",
    "sensor_cost_minimality_proved",
    "nonlinear_encoding_minimality_proved",
    "adaptive_readout_minimality_proved",
    "empirical_noise_calibrated",
    "physical_sources_established",
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
    require(ident(AR) == AR_ID, "AR artifact changed")
    return json.loads(plain_bytes(AR))


def identities():
    previous = prior_document()
    prior = {str(AR.relative_to(HERE.parent)): AR_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AR.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def project_inputs(ar_families):
    require(type(ar_families) is list and len(ar_families) == 2, "AR family inventory")
    require([f["problem"]["family"] for f in ar_families] == list(FAMILIES), "AR family order")
    problems = []
    for family in ar_families:
        matrices, repair = family["matrices"], family["repair"]
        labels = matrices["fine_response_rows"]
        require(len(labels) == 64, "AR target inventory")
        verify_suite(repair["intercept"], [[0, 1] for _ in labels])
        p = {
            "family": family["problem"]["family"],
            "target_labels": labels,
            "observations": matrices["coarse_observations"],
            "bank": matrices["repair_observations"],
            "targets": matrices["fine_targets"],
            "filters": repair["matrix"],
        }
        for key, rows, width in (
            ("observations", 32, 108),
            ("bank", 48, 108),
            ("targets", 64, 108),
            ("filters", 64, 48),
        ):
            require(
                len(p[key]) == rows and all(len(row) == width for row in p[key]),
                "AR matrix inventory",
            )
        problems.append(copy.deepcopy(p))
    return problems, ar_families


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05as_" + name, HERE / filename)
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
        base, selected, decoder = family["base"], family["selection"], family["decoder"]
        require(type(base["delta"]) is int and base["delta"] >= 0, "native supplement count")
        require(base["delta"] == base["joint_rank"] - base["observation_rank"], "rank increment")
        require(len(selected["target_rows"]) == base["delta"], "selection count")
        require(len(family["witnesses"]) == base["delta"], "complete witness inventory")
        require(decoder["exact"] is True, "full receiver identity")
        require(len(decoder["row_basis"]) == base["joint_rank"], "completed basis count")
    return dict.fromkeys(CHECK_FIELDS, True)


def historical_bridges(families, previous):
    expected, _ = project_inputs(previous)
    verify_suite([f["problem"] for f in families], expected)
    controls(families)
    keys = (
        "observation_rank",
        "target_rank",
        "joint_rank",
        "row_basis",
        "pivot_columns",
        "free_columns",
        "recoverable_rows",
        "failed_rows",
    )
    for current, old in zip(families, previous, strict=True):
        verify_suite(
            {k: current["base"][k] for k in keys}, {k: old["certificate"][k] for k in keys}
        )
    return {
        "AR_selected_families": list(FAMILIES),
        "AR_selected_inputs_equal": True,
        "AR_zero_repair_intercept": True,
        "AR_base_certificate_equal": True,
        "AR_filter_identity_rechecked": True,
        "other_historical_mathematics_replayed": False,
        "older_executors_run": False,
    }


def payload_sizes(families):
    return [
        {
            "family": f["problem"]["family"],
            "input_bytes": len(canonical(f["problem"])),
            "base_bytes": len(canonical(f["base"])),
            "selection_bytes": len(canonical(f["selection"])),
            "decoder_bytes": len(canonical(f["decoder"])),
            "witness_bytes": len(canonical(f["witnesses"])),
            "producer_map_bytes": len(canonical(f["selection"]["filters"])),
            "receiver_map_bytes": len(
                canonical({k: f["decoder"][k] for k in ("intercept", "matrix")})
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
