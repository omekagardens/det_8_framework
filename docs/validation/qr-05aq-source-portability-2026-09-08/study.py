"""QR-05AQ inherited coarse-map source portability orchestration."""

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
SCHEMA = "det8-qr05aq-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05aq.py")
AP = HERE.parent / "qr-05ap-measurement-stability-2026-09-08/results.json"
AP_ID = {
    "bytes": 361276,
    "sha256": "823d9f5a5511853fe3dbff800f1a6561db985021002c24ec2beb0c55199ba048",
}
AO = HERE.parent / "qr-05ao-field-measurements-2026-09-08/results.json"
AO_ID = {
    "bytes": 451698,
    "sha256": "55938309ba8ea8c205a9c6e127ce324e485b5e0bf5ff02bc5f513503e2f5fbf1",
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
    "old_generators",
    "new_generators",
    "observation_rows",
    "response_rows",
    "defined_response_rows",
    "undefined_response_rows",
    "coarse_moment_entries",
    "fine_moment_entries",
    "coarse_outgoing_entries",
    "source_coefficient_entries",
    "observation_entries",
    "target_entries",
    "generator_integral_entries",
    "constant_observation_entries",
    "constant_target_entries",
    "raw_decoder_entries",
    "prediction_entries",
    "residual_entries",
    "normalized_residual_entries",
    "nonzero_residual_entries",
    "failed_rows",
    "failed_generators",
    "row_bound_entries",
    "bound_attainer_indices",
    "witnesses",
    "witness_entries",
)
CHECK_FIELDS = (
    "old_response_identities",
    "geometric_policy_authenticated",
    "moment_additivity",
    "bernstein_partition",
    "generator_integrals",
    "constant_field_observations",
    "constant_field_responses",
    "geometric_portability",
    "witnesses_valid",
)
SCOPE = (
    "decoder_refitted",
    "old_convex_hull_inclusion_proved",
    "full_field_recovery_extended",
    "physical_sources_established",
    "empirical_noise_calibrated",
    "arbitrary_field_error_bound_proved",
    "unknown_geometry_reconstructed",
    "quantum_channel_constructed",
    "gravity_derived",
    "ret_integration_tested",
    "lean_verification_performed",
    "generic_production_API_hardened",
    "fixed_affine_families_run",
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
    require(ident(AP) == AP_ID, "AP artifact changed")
    return json.loads(plain_bytes(AP))


def identities():
    previous = prior_document()
    prior = {str(AP.relative_to(HERE.parent)): AP_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AP.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def project_inputs(ap_families, ao_families):
    for families, title in ((ap_families, "AP"), (ao_families, "AO")):
        require(type(families) is list and len(families) == 2, title + " family inventory")
        require(
            [f["problem"]["family"] for f in families] == list(FAMILIES), title + " family order"
        )
    problems = []
    for ap, ao in zip(ap_families, ao_families, strict=True):
        p, g, m = ao["problem"], ao["geometry"], ao["matrices"]
        require(p["probe"]["name"] == "whole", "AO whole probe")
        require(p["coarse"]["level"] == "l1" and p["fine"]["level"] == "l2", "AO selected levels")
        require(
            len(p["coarse"]["cells"]) == 7 and len(p["fine"]["cells"]) == 8, "AO cell inventory"
        )
        require(len(g["coarse_tiles"]) == 8 and len(g["fine_tiles"]) == 12, "AO tile inventory")
        require(
            [c["event"] for c in g["coarse_cells"]] == [c["event"] for c in p["coarse"]["cells"]],
            "AO coarse IDs",
        )
        require(
            [c["event"] for c in g["fine_cells"]] == [c["event"] for c in p["fine"]["cells"]],
            "AO fine IDs",
        )
        require(
            [o["name"] for o in m["observations"]] == ["integral", "weighted"],
            "AO observation inventory",
        )
        require(
            [q["name"] for q in m["targets"]] == ["coarse", "fine", "field"], "AO target inventory"
        )
        verify_suite(
            m["observations"][1]["rows"],
            [{"tile": t, "basis": j} for t in range(8) for j in range(4)],
        )
        coarse_ids = [c["event"] for c in g["coarse_cells"]]
        verify_suite(
            m["targets"][0]["rows"],
            [{"first": c, "second": d} for c in coarse_ids for d in coarse_ids],
        )
        certs = ao["certificates"]
        verify_suite(
            [{"observation": c["observation"], "target": c["target"]} for c in certs],
            [
                {"observation": o, "target": t}
                for o in ("integral", "weighted")
                for t in ("coarse", "fine", "field")
            ],
        )
        cert = certs[3]["certificate"]
        require(
            cert["recoverable"] is True and cert["collision"] is None, "AO frozen coarse recovery"
        )
        inherited = {
            "family": p["family"],
            "probe": p["probe"]["bounds"],
            "cells": [{"event": c["event"], "bounds": c["bounds"]} for c in g["coarse_cells"]],
            "tiles": [{"event": t["event"], "bounds": t["bounds"]} for t in g["coarse_tiles"]],
            "observations": m["observations"][1]["matrix"],
            "targets": m["targets"][0]["matrix"],
            "canonical": {key: cert[key] for key in ("row_basis", "decoder")},
            "geometric": m["coarse_decoder"],
        }
        verify_suite(ap["problem"], inherited)
        problem = {
            "family": inherited["family"],
            "probe": inherited["probe"],
            "coarse_cells": inherited["cells"],
            "fine_cells": [{"event": c["event"], "bounds": c["bounds"]} for c in g["fine_cells"]],
            "coarse_tiles": inherited["tiles"],
            "fine_tiles": [
                {key: t[key] for key in ("event", "bounds", "coarse_tile")} for t in g["fine_tiles"]
            ],
            "old_observations": inherited["observations"],
            "old_targets": inherited["targets"],
            "canonical": inherited["canonical"],
            "geometric": inherited["geometric"],
        }
        problems.append(copy.deepcopy(problem))
    return problems, (ap_families, ao_families)


def load_inputs():
    ap = prior_document()
    require(ap["prior_artifacts"].get(str(AO.relative_to(HERE.parent))) == AO_ID, "AO ancestry pin")
    require(ident(AO) == AO_ID, "AO artifact changed")
    ao = json.loads(plain_bytes(AO))
    return project_inputs(ap["suite"]["families"], ao["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05aq_" + name, HERE / filename)
    require(spec is not None and spec.loader is not None, "engine loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def controls(families):
    require(len(families) == 2, "complete fixed inventory")
    require([f["problem"]["family"] for f in families] == list(FAMILIES), "family order")
    for f in families:
        require(set(f["checks"]) == set(CHECK_FIELDS), "complete check fields")
        require(all(v is True for v in f["checks"].values()), "family check failed")
        require(
            [d["name"] for d in f["decoders"]] == ["canonical", "geometric"], "frozen policy order"
        )
        require(
            f["decoders"][1]["exact"] is True and f["decoders"][1]["witness"] is None,
            "geometric portability",
        )
    return dict.fromkeys(CHECK_FIELDS, True)


def historical_bridges(families, previous):
    ap_families, ao_families = previous
    expected, _ = project_inputs(ap_families, ao_families)
    verify_suite([f["problem"] for f in families], expected)
    controls(families)
    for family, ao in zip(families, ao_families, strict=True):
        for key in ("coarse_tiles", "fine_tiles"):
            new, old = family["geometry"][key], ao["geometry"][key]
            require(len(new) == len(old), "selected tile moment inventory")
            fields = (
                ("event", "bounds", "moments")
                if key == "coarse_tiles"
                else ("event", "bounds", "coarse_tile", "moments")
            )
            verify_suite(
                [{k: t[k] for k in fields} for t in new], [{k: t[k] for k in fields} for t in old]
            )
    return {
        "AP_selected_families": list(FAMILIES),
        "AP_frozen_inputs_equal": True,
        "AO_selected_fine_geometry_equal": True,
        "AO_selected_coarse_moments_equal": True,
        "AO_selected_fine_moments_equal": True,
        "old_maps_consumed": True,
        "old_response_identities_rechecked": True,
        "other_historical_mathematics_replayed": False,
        "older_executors_run": False,
    }


def payload_sizes(families):
    return [
        {
            "family": f["problem"]["family"],
            "input_bytes": len(canonical(f["problem"])),
            "geometry_bytes": len(canonical(f["geometry"])),
            "generator_bytes": len(canonical(f["generators"])),
            "measurement_bytes": len(
                canonical(
                    {
                        "rows": f["matrices"]["observation_rows"],
                        "matrix": f["matrices"]["observations"],
                    }
                )
            ),
            "target_bytes": len(
                canonical(
                    {"rows": f["matrices"]["response_rows"], "matrix": f["matrices"]["targets"]}
                )
            ),
            "decoder_bytes": len(canonical(f["decoders"])),
            "native_family_bytes": len(canonical(f)),
        }
        for f in families
    ]


def assemble_suite(families, previous):
    expected, consumed = load_inputs()
    verify_suite(list(previous), list(consumed))
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
