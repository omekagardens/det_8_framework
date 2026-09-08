"""QR-05AO bounded coarse-field observation orchestration; no historical executors."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import platform
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05ao-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05ao.py")
AN = HERE.parent / "qr-05an-four-point-degree-2026-09-08/results.json"
AN_ID = {
    "bytes": 8378531,
    "sha256": "a455f43f65dea9da33692cd256fad942e2d21d0bfed9f54a0deed163ff5bd9c1",
}
MAX_CAPTURE_BYTES = 128 * 1024 * 1024
MAX_WORKING_BYTES = 192 * 1024 * 1024
FAMILIES = ("grid", "warp")
AN_FAMILIES = FAMILIES
LEVELS = ("l0", "l1", "l2")
COUNT_FIELDS = (
    "coarse_cells",
    "fine_cells",
    "positive_coarse_cells",
    "positive_fine_cells",
    "generators",
    "coarse_tiles",
    "fine_tiles",
    "input_bound_entries",
    "clipped_bound_entries",
    "tile_bound_entries",
    "coarse_moment_entries",
    "fine_moment_entries",
    "coarse_outgoing_vectors",
    "coarse_outgoing_entries",
    "fine_outgoing_vectors",
    "fine_outgoing_entries",
    "observation_rows",
    "observation_entries",
    "fine_weighted_rows",
    "fine_weighted_entries",
    "coarse_response_rows",
    "fine_response_rows",
    "field_rows",
    "target_entries",
    "geometric_decoder_entries",
    "certificates",
    "recoverable",
    "failed",
    "row_basis_entries",
    "pivot_column_entries",
    "canonical_decoder_entries",
    "collision_entries",
)
SCOPE = (
    "generic_production_API_hardened",
    "unknown_geometry_reconstructed",
    "minimal_encoding_proved",
    "universal_compression_proved",
    "mixture_weights_recovered",
    "physical_mixture_preparation_established",
    "empirical_measurements_used",
    "noisy_measurement_robustness_tested",
    "quantum_channel_constructed",
    "gravity_derived",
    "continuum_limit_established",
    "ret_integration_tested",
    "lean_verification_performed",
    "fixed_affine_families_run",
    "full_retained_artifact_information_lost",
)
FIELD_POWERS = tuple((i, j) for i in range(3) for j in range(3))
CHECK_FIELDS = (
    "weighted_contains_integral",
    "coarse_decoder_exact",
    "coarse_refinement_exact",
    "response_partition_exact",
    "measurement_refinement_exact",
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


def frac(value):
    require(
        type(value) is list and len(value) == 2 and all(type(x) is int for x in value),
        "fraction pair",
    )
    n, d = value
    require(d > 0 and math.gcd(n, d) == 1, "reduced fraction")
    return F(n, d)


def wire(value):
    value = F(value)
    return [value.numerator, value.denominator]


def prior_document():
    require(ident(AN) == AN_ID, "AN artifact changed")
    return json.loads(plain_bytes(AN))


def identities():
    previous = prior_document()
    prior = {str(AN.relative_to(HERE.parent)): AN_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AN.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def project_inputs(previous):
    require(type(previous) is list and len(previous) == 2, "complete AN family inventory")
    require([f["problem"]["family"] for f in previous] == list(FAMILIES), "AN family order")
    problems = []
    for old, name in zip(previous, FAMILIES, strict=True):
        p = old["problem"]
        require(set(p) == {"family", "probes", "levels"}, "AN original input fields")
        require(len(p["probes"]) == 1 and p["probes"][0]["name"] == "whole", "AN whole probe")
        require(set(p["probes"][0]) == {"name", "bounds"}, "AN probe fields")
        require(len(p["levels"]) == 3, "AN level inventory")
        require([l["level"] for l in p["levels"]] == list(LEVELS), "AN level order")
        for level, size in zip(p["levels"], (6, 7, 8), strict=True):
            require(set(level) == {"level", "cells"}, "AN level fields")
            require(len(level["cells"]) == size, "AN level cell inventory")
            require(all(set(c) == {"event", "bounds"} for c in level["cells"]), "AN cell fields")
        problems.append(
            {
                "family": name,
                "probe": copy.deepcopy(p["probes"][0]),
                "coarse": copy.deepcopy(p["levels"][1]),
                "fine": copy.deepcopy(p["levels"][2]),
            }
        )
    return problems, previous


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05ao_" + name, HERE / filename)
    require(spec is not None and spec.loader is not None, "engine loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def affine_problem(problem, alpha, beta, du=F(0), dv=F(0)):
    """Transport only geometry input; certificate transport is independently tested."""
    alpha, beta, du, dv = map(F, (alpha, beta, du, dv))
    require(alpha > 0 and beta > 0, "positive coordinate scales")
    result = copy.deepcopy(problem)
    rows = [result["probe"], *result["coarse"]["cells"], *result["fine"]["cells"]]
    for row in rows:
        row["bounds"] = [
            wire(frac(x) * a + d)
            for x, a, d in zip(
                row["bounds"], (alpha, alpha, beta, beta), (du, du, dv, dv), strict=True
            )
        ]
    return result


def controls(families):
    require(len(families) == 2, "complete fixed family inventory")
    require([f["problem"]["family"] for f in families] == list(FAMILIES), "fixed family order")
    for family in families:
        require(set(family["checks"]) == set(CHECK_FIELDS), "complete geometric checks")
        require(all(v is True for v in family["checks"].values()), "geometric check failed")
    return dict.fromkeys(CHECK_FIELDS, True)


def an_bridges(families, previous):
    expected, _ = project_inputs(previous)
    verify_suite([f["problem"] for f in families], expected)
    for family, old in zip(families, previous, strict=True):
        require(len(old["levels"]) == 3, "AN output level inventory")
        require([l["level"] for l in old["levels"]] == list(LEVELS), "AN output level order")
        geometries = old["levels"][2]["geometry"]
        require(
            len(geometries) == 1 and geometries[0]["probe"] == "whole", "selected AN output probe"
        )
        geometry = geometries[0]
        ids = [c["event"] for c in family["problem"]["fine"]["cells"]]
        verify_suite([m["event"] for m in geometry["middles"]], ids)
        generators = [{"first": a, "second": b} for a in ids for b in ids]
        verify_suite(family["matrices"]["generators"], generators)
        old_tiles = [(m["event"], t) for m in geometry["middles"] for t in m["tiles"]]
        new_tiles = family["geometry"]["fine_tiles"]
        require(len(old_tiles) == len(new_tiles), "selected AN flattened tile inventory")
        field_rows, field_matrix = [], []
        for ti, ((event, tile), new) in enumerate(zip(old_tiles, new_tiles, strict=True)):
            verify_suite(
                {"event": new["event"], "bounds": new["bounds"]},
                {"event": event, "bounds": tile["bounds"]},
            )
            propagated = tile["propagated"]
            verify_suite(
                [{"first": p["first"], "second": p["second"]} for p in propagated], generators
            )
            require(all(len(p["coefficients"]) == 9 for p in propagated), "AN coefficient arity")
            for pi, power in enumerate(FIELD_POWERS):
                field_rows.append({"tile": ti, "power": list(power)})
                field_matrix.append([p["coefficients"][pi] for p in propagated])
        targets = family["matrices"]["targets"]
        require(
            [t["name"] for t in targets] == ["coarse", "fine", "field"], "complete target order"
        )
        verify_suite(targets[2], {"name": "field", "rows": field_rows, "matrix": field_matrix})
        old_quads = geometry["quadruples"]
        require(len(old_quads) == len(ids) ** 4, "AN selected quadruple inventory")
        quad_map = {
            (q["first"], q["second"], q["third"], q["last"]): q["causal_integral"]
            for q in old_quads
        }
        require(len(quad_map) == len(ids) ** 4, "AN quadruple unique tuples")
        rows = [{"first": c, "second": d} for c in ids for d in ids]
        matrix = [
            [quad_map[a, b, row["first"], row["second"]] for a in ids for b in ids] for row in rows
        ]
        verify_suite(targets[1], {"name": "fine", "rows": rows, "matrix": matrix})
    return {
        "AN_selected_families": list(FAMILIES),
        "AN_selected_input_geometry_equal": True,
        "AN_selected_fine_coefficients_equal": True,
        "AN_selected_fine_quadruples_equal": True,
        "AN_answers_consumed_by_engines": False,
        "AN_other_mathematics_replayed": False,
        "older_executors_run": False,
    }


def payload_sizes(families):
    out = []
    for family in families:
        matrices = family["matrices"]
        out.append(
            {
                "family": family["problem"]["family"],
                "geometry_bytes": len(canonical(family["geometry"])),
                "measurement_map_bytes": len(
                    canonical(
                        {
                            "generators": matrices["generators"],
                            "observations": matrices["observations"],
                        }
                    )
                ),
                "target_map_bytes": len(canonical(matrices["targets"])),
                "geometric_decoder_bytes": len(canonical(matrices["coarse_decoder"])),
                "certificate_bytes": len(canonical(family["certificates"])),
                "native_family_bytes": len(canonical(family)),
            }
        )
    return out


def assemble_suite(families, an_families):
    require(len(families) == 2, "complete fixed inventory")
    expected, consumed = load_inputs()
    verify_suite(an_families, consumed)
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
        "prior_bridges": an_bridges(families, an_families),
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
