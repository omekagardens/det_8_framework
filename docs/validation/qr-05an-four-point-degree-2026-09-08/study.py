"""QR-05AN bounded degree-aware four-point orchestration; no historical executors."""

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
SCHEMA = "det8-qr05an-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05an.py")
AM = HERE.parent / "qr-05am-query-reuse-2026-09-07/results.json"
AM_ID = {
    "bytes": 4676696,
    "sha256": "46abc46e884b8e4bc472948b4c67b3f3dd4b6dd1e8d99ced1d778912dddc085e",
}
MAX_CAPTURE_BYTES = 128 * 1024 * 1024
MAX_WORKING_BYTES = 192 * 1024 * 1024
FAMILIES = ("grid", "warp")
AM_FAMILIES = ("grid", "warp", "warp_stale", "boost", "dilate")
LEVELS = ("l0", "l1", "l2")
COUNT_FIELDS = (
    "levels",
    "probes",
    "level_pairs",
    "level_triples",
    "level_quadruples",
    "middle_cells",
    "positive_middle_cells",
    "tiles",
    "breakpoint_entries",
    "middle_bound_entries",
    "tile_bound_entries",
    "middle_moment_entries",
    "tile_moment_entries",
    "propagated_vectors",
    "propagated_entries",
    "forced_vectors",
    "forced_entries",
    "outgoing_vectors",
    "outgoing_entries",
    "nonbilinear_propagated_vectors",
    "quadruple_tile_visits",
    "positive_quadruples",
    "undefined_quad_conditionals",
    "zero_third_quadruples",
    "forced_positive_errors",
    "forced_zero_errors",
    "forced_negative_errors",
    "mean_positive_errors",
    "mean_zero_errors",
    "mean_negative_errors",
    "nonbilinear_quadruples",
    "nonbilinear_forced_equalities",
    "coarsening_moment_blocks",
    "coarsening_moment_entries",
    "field_blocks",
    "field_pieces",
    "field_child_terms",
    "field_coefficient_entries",
    "blocks",
    "child_terms",
    "via_middle_blocks",
)
SCOPE = (
    "generic_production_API_hardened",
    "AM_moment_reuse_tested",
    "minimal_encoding_proved",
    "universal_fixed_degree_closure",
    "unknown_geometry_reconstructed",
    "arbitrary_dynamics_closure",
    "continuum_limit_established",
    "marks_authenticated",
    "stochastic_transition_constructed",
    "quantum_channel_constructed",
    "gravity_derived",
    "empirical_data_used",
    "ret_integration_tested",
    "lean_verification_performed",
    "fixed_affine_families_run",
)
MOMENT_EXPONENTS = tuple((i, j) for i in range(4) for j in range(4))
PROPAGATED_EXPONENTS = tuple((i, j) for i in range(3) for j in range(3))
BASIS_EXPONENTS = ((0, 0), (1, 0), (0, 1), (1, 1))


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
    require(ident(AM) == AM_ID, "AM artifact changed")
    return json.loads(plain_bytes(AM))


def identities():
    previous = prior_document()
    prior = {str(AM.relative_to(HERE.parent)): AM_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AM.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def project_inputs(previous):
    require(len(previous) == 5, "complete AM family inventory")
    require([f["problem"]["family"] for f in previous] == list(AM_FAMILIES), "AM family order")
    problems = []
    for old, name in zip(previous[:2], FAMILIES, strict=True):
        contexts = old["problem"]["contexts"]
        require(len(contexts) == 15, "AM full context inventory")
        chosen = [c for c in contexts if c["probe"] == "whole"]
        require(len(chosen) == 3, "three selected AM whole contexts")
        probe = copy.deepcopy(chosen[0]["probe_bounds"])
        levels = []
        for c, label, size in zip(chosen, LEVELS, (6, 7, 8), strict=True):
            require(
                c["level"] == label and len(c["middles"]) == size, "selected AM level inventory"
            )
            verify_suite(c["probe_bounds"], probe)
            require(all(m["bounds"] is not None for m in c["middles"]), "whole cells are positive")
            levels.append(
                {
                    "level": label,
                    "cells": [
                        {k: copy.deepcopy(m[k]) for k in ("event", "bounds")} for m in c["middles"]
                    ],
                }
            )
        problems.append(
            {"family": name, "probes": [{"name": "whole", "bounds": probe}], "levels": levels}
        )
    return problems, previous


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05an_" + name, HERE / filename)
    require(spec is not None and spec.loader is not None, "engine loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def affine_family(value, alpha, beta, du=F(0), dv=F(0)):
    """Complete global affine transport; input is an entire native family."""
    alpha, beta, du, dv = map(F, (alpha, beta, du, dv))
    require(alpha > 0 and beta > 0, "positive coordinate scales")
    k = alpha * beta

    def coefficients(items, exponents, power):
        require(type(items) is list and len(items) == len(exponents), "coefficient inventory")
        out = {e: F(0) for e in exponents}
        for x, (i, j) in zip(items, exponents, strict=True):
            for r in range(i + 1):
                for s in range(j + 1):
                    out[r, s] += (
                        frac(x)
                        * k**power
                        * math.comb(i, r)
                        * math.comb(j, s)
                        * (-du) ** (i - r)
                        * (-dv) ** (j - s)
                        / (alpha**i * beta**j)
                    )
        return [wire(out[e]) for e in exponents]

    def walk(item, field=None, degree=None):
        if item is None:
            return None
        if field == "bounds":
            require(type(item) is list and len(item) == 4, "four bounds")
            return [
                wire(frac(x) * a + d)
                for x, a, d in zip(item, (alpha, alpha, beta, beta), (du, du, dv, dv), strict=True)
            ]
        if field in ("u_breaks", "v_breaks"):
            a, d = (alpha, du) if field == "u_breaks" else (beta, dv)
            return [wire(frac(x) * a + d) for x in item]
        if field in ("moments", "coarse_moments", "child_moment_sum"):
            require(type(item) is list and len(item) == 16, "sixteen moments")
            old = dict(zip(MOMENT_EXPONENTS, map(frac, item), strict=True))
            return [
                wire(
                    k
                    * sum(
                        (
                            F(math.comb(i, r) * math.comb(j, s))
                            * alpha**r
                            * beta**s
                            * du ** (i - r)
                            * dv ** (j - s)
                            * old[r, s]
                            for r in range(i + 1)
                            for s in range(j + 1)
                        ),
                        F(0),
                    )
                )
                for i, j in MOMENT_EXPONENTS
            ]
        if field == "coefficients":
            return (
                coefficients(item, PROPAGATED_EXPONENTS, 2)
                if len(item) == 9
                else coefficients(item, BASIS_EXPONENTS, 1)
            )
        if field in ("coarse_coefficients", "child_coefficient_sum"):
            return coefficients(item, PROPAGATED_EXPONENTS, 2)
        if field == "forced_coefficients":
            return coefficients(item, BASIS_EXPONENTS, 2)
        if field in ("pairs", "triples", "quadruples", "blocks", "summary"):
            degree = {"pairs": 2, "triples": 3, "quadruples": 4, "blocks": 4, "summary": 4}[field]
        power = None
        if field in ("volume", "clipped_volume"):
            power = 1
        elif field in ("pair_integral", "pair_continuum_integral"):
            power = 2
        elif field in ("triple_integral", "triple_continuum_integral", "third_covariance"):
            power = 3
        elif field in (
            "quadruple_integral",
            "quadruple_continuum_integral",
            "mean_product",
            "mean_error",
            "centered_integral",
            "coarse_integral",
            "child_integral_sum",
            "via_middle_integral",
        ):
            power = 4
        elif field in ("volume_product", "causal_integral", "forced_integral", "forced_error"):
            require(degree in (2, 3, 4), "declared result degree")
            power = degree
        if power is not None:
            return wire(frac(item) * k**power)
        if type(item) is dict:
            return {key: walk(child, key, degree) for key, child in item.items()}
        if type(item) is list:
            return [walk(child, None, degree) for child in item]
        return item

    return walk(value)


def controls(families):
    require(len(families) == 2, "complete fixed family inventory")
    require([f["problem"]["family"] for f in families] == list(FAMILIES), "fixed family order")
    for family in families:
        for level in family["levels"]:
            for geometry in level["geometry"]:
                v = frac(geometry["volume"])
                summary = geometry["summary"]
                for name, power, denominator in (
                    ("pair", 2, 4),
                    ("triple", 3, 36),
                    ("quadruple", 4, 576),
                ):
                    wanted = wire(v**power / denominator)
                    verify_suite(summary[name + "_integral"], wanted)
                    verify_suite(summary[name + "_continuum_integral"], wanted)
    return {"pair_partition": True, "triple_partition": True, "quadruple_partition": True}


def am_bridges(families, previous):
    expected, _ = project_inputs(previous)
    verify_suite([f["problem"] for f in families], expected)
    return {
        "AM_selected_families": list(FAMILIES),
        "AM_selected_whole_bounds_ids_equal": True,
        "AM_selected_probe_bounds_equal": True,
        "AM_moments_consumed": False,
        "AM_query_answers_replayed": False,
        "older_math_replayed": False,
    }


def payload_sizes(families):
    out = []
    for family in families:
        contract = [
            {
                "level": level["level"],
                "geometry": [
                    {"probe": g["probe"], "middles": g["middles"]} for g in level["geometry"]
                ],
            }
            for level in family["levels"]
        ]
        out.append(
            {
                "family": family["problem"]["family"],
                "moment_contract_bytes": len(canonical(contract)),
                "coarsening_witness_bytes": len(canonical(family["coarsenings"])),
                "native_family_bytes": len(canonical(family)),
            }
        )
    return out


def assemble_suite(families, am_families):
    require(len(families) == 2, "complete fixed inventory")
    expected, consumed = load_inputs()
    verify_suite(am_families, consumed)
    verify_suite([f["problem"] for f in families], expected)
    for family in families:
        require(set(family["counts"]) == set(COUNT_FIELDS), "complete count inventory")
        require(
            all(type(v) is int and v >= 0 for v in family["counts"].values()),
            "native nonnegative counts",
        )
    return {
        "families": families,
        "controls": controls(families),
        "prior_bridges": am_bridges(families, am_families),
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
