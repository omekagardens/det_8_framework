"""QR-05AR fine-response sufficiency and explicit measurement repair orchestration."""

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
SCHEMA = "det8-qr05ar-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05ar.py")
AQ = HERE.parent / "qr-05aq-source-portability-2026-09-08/results.json"
AQ_ID = {
    "bytes": 934498,
    "sha256": "c9c0bb0b20cd3646217e6ad97eaf2f41ca40406fc94d8fac975b67267eec6a08",
}
MAX_CAPTURE_BYTES = 128 * 1024 * 1024
MAX_WORKING_BYTES = 192 * 1024 * 1024
FAMILIES = ("grid", "warp")
COUNT_FIELDS = (
    "coarse_cells",
    "fine_cells",
    "positive_coarse_cells",
    "positive_fine_cells",
    "coarse_tiles",
    "fine_tiles",
    "repair_tiles",
    "added_repair_tiles",
    "generators",
    "coarse_observation_rows",
    "fine_observation_rows",
    "repair_observation_rows",
    "coarse_response_rows",
    "fine_response_rows",
    "defined_fine_response_rows",
    "undefined_fine_response_rows",
    "coarse_moment_entries",
    "fine_moment_entries",
    "repair_moment_entries",
    "outgoing_entries",
    "source_coefficient_entries",
    "observation_entries",
    "target_entries",
    "constant_observation_entries",
    "constant_target_entries",
    "generator_integral_entries",
    "raw_geometric_entries",
    "certificate_decoder_entries",
    "recoverable_rows",
    "failed_rows",
    "collisions",
    "collision_entries",
    "repair_prediction_entries",
    "repair_residual_entries",
    "repair_collision_entries",
)
CHECK_FIELDS = (
    "geometry_partitions",
    "bernstein_partition",
    "generator_integrals",
    "moment_additivity",
    "observation_additivity",
    "response_additivity",
    "geometric_coarse_identity",
    "geometric_fine_identity",
    "coarse_certificate_valid",
    "collision_valid",
    "repair_collision_valid",
    "constant_field_sums",
)
SCOPE = (
    "source_dictionary_changed",
    "old_convex_hull_inclusion_proved",
    "full_field_recovery_tested",
    "repair_minimality_proved",
    "fine_measurements_recovered_from_coarse",
    "physical_sources_established",
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
    require(ident(AQ) == AQ_ID, "AQ artifact changed")
    return json.loads(plain_bytes(AQ))


def identities():
    previous = prior_document()
    prior = {str(AQ.relative_to(HERE.parent)): AQ_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AQ.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def project_inputs(aq_families):
    require(type(aq_families) is list and len(aq_families) == 2, "AQ family inventory")
    require([f["problem"]["family"] for f in aq_families] == list(FAMILIES), "AQ family order")
    fields = ("family", "probe", "coarse_cells", "fine_cells", "coarse_tiles", "fine_tiles")
    problems = []
    for family in aq_families:
        p = family["problem"]
        require(len(p["coarse_cells"]) == 7 and len(p["fine_cells"]) == 8, "AQ cell inventory")
        require(len(p["coarse_tiles"]) == 8 and len(p["fine_tiles"]) == 12, "AQ tile inventory")
        problems.append(copy.deepcopy({key: p[key] for key in fields}))
    return problems, aq_families


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05ar_" + name, HERE / filename)
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
        cert, repair = family["certificate"], family["repair"]
        require(type(cert["recoverable"]) is bool, "native recoverability")
        require(cert["recoverable"] == (len(cert["failed_rows"]) == 0), "recovery classification")
        require((cert["collision"] is None) == cert["recoverable"], "collision presence")
        require((cert["decoder"] is not None) == cert["recoverable"], "complete decoder presence")
        require(repair["exact"] is True, "structural repair")
        require(
            (repair["collision"] is None) == (cert["collision"] is None),
            "repair collision presence",
        )
    return dict.fromkeys(CHECK_FIELDS, True)


def historical_bridges(families, previous):
    expected, _ = project_inputs(previous)
    verify_suite([f["problem"] for f in families], expected)
    controls(families)
    for new, old in zip(families, previous, strict=True):
        g, h = new["geometry"], old["geometry"]
        fields = ("volume", "coarse_cells", "fine_cells", "parents", "coarse_tiles", "fine_tiles")
        verify_suite({k: g[k] for k in fields}, {k: h[k] for k in fields})
        verify_suite(g["coarse_response_scales"], h["response_scales"])
        verify_suite(new["generators"], old["generators"])
        m, n = new["matrices"], old["matrices"]
        for current, previous_key in (
            ("coarse_observation_rows", "observation_rows"),
            ("coarse_response_rows", "response_rows"),
            ("coarse_observations", "observations"),
            ("coarse_targets", "targets"),
            ("generator_integrals", "generator_integrals"),
            ("constant_coarse_observations", "constant_observations"),
            ("constant_coarse_targets", "constant_targets"),
        ):
            verify_suite(m[current], n[previous_key])
        verify_suite(m["coarse_geometric"], old["problem"]["geometric"])
    return {
        "AQ_selected_families": list(FAMILIES),
        "AQ_geometry_inputs_equal": True,
        "AQ_selected_geometry_equal": True,
        "AQ_sources_equal": True,
        "AQ_coarse_measurements_equal": True,
        "AQ_coarse_targets_equal": True,
        "AQ_geometric_map_equal": True,
        "AQ_source_sums_equal": True,
        "other_historical_mathematics_replayed": False,
        "older_executors_run": False,
    }


def payload_sizes(families):
    observation_fields = (
        "coarse_observation_rows",
        "fine_observation_rows",
        "repair_observation_rows",
        "coarse_observations",
        "fine_observations",
        "repair_observations",
    )
    target_fields = ("coarse_response_rows", "fine_response_rows", "coarse_targets", "fine_targets")
    return [
        {
            "family": f["problem"]["family"],
            "input_bytes": len(canonical(f["problem"])),
            "geometry_bytes": len(canonical(f["geometry"])),
            "generator_bytes": len(canonical(f["generators"])),
            "measurement_bytes": len(canonical({k: f["matrices"][k] for k in observation_fields})),
            "target_bytes": len(canonical({k: f["matrices"][k] for k in target_fields})),
            "certificate_bytes": len(canonical(f["certificate"])),
            "repair_bytes": len(canonical(f["repair"])),
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
