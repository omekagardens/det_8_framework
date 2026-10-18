"""QR-05AL bounded moment-contract orchestration; no historical engine imports."""

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
SCHEMA = "det8-qr05al-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05al.py")
AK = HERE.parent / "qr-05ak-shared-middle-2026-09-07/results.json"
AK_ID = {
    "bytes": 16462744,
    "sha256": "15fce56375af7e44bfc2f955559c55628c77338d11a1911161c4e3bb6f038db4",
}
MAX_CAPTURE_BYTES = 128 * 1024 * 1024
MAX_WORKING_BYTES = 192 * 1024 * 1024
FAMILIES = ("grid", "warp", "warp_stale", "boost", "dilate")
LEVELS = ("l0", "l1", "l2")
SCOPE = (
    "generic_production_API_hardened",
    "unknown_geometry_reconstructed",
    "minimal_encoding_proved",
    "universal_query_closure",
    "arbitrary_dynamics_closure",
    "continuum_limit_established",
    "marks_authenticated",
    "stochastic_transition_constructed",
    "quantum_channel_constructed",
    "gravity_derived",
    "empirical_data_used",
    "ret_integration_tested",
    "lean_verification_performed",
)
COUNT_FIELDS = (
    "levels",
    "probes",
    "level_pairs",
    "level_triples",
    "blocks",
    "child_terms",
    "middle_cells",
    "positive_middle_cells",
    "tiles",
    "breakpoint_entries",
    "middle_bound_entries",
    "tile_bound_entries",
    "middle_moment_entries",
    "tile_moment_entries",
    "coefficient_vectors",
    "coefficient_entries",
    "coarsening_moment_blocks",
    "coarsening_moment_entries",
    "zero_middle_level_triples",
    "undefined_level_conditionals",
    "positive_triples",
    "original_positive_errors",
    "original_zero_errors",
    "original_negative_errors",
    "tile_positive_errors",
    "tile_zero_errors",
    "tile_negative_errors",
    "between_positive_errors",
    "between_zero_errors",
    "between_negative_errors",
)
AK_TRIPLE_FIELDS = (
    "first",
    "middle",
    "last",
    "volume_product",
    "causal_integral",
    "pair_product",
    "product_error",
    "conditional",
    "product_conditional",
    "middle_covariance",
)
AK_BLOCK_FIELDS = (
    "first",
    "middle",
    "last",
    "children",
    "coarse_integral",
    "child_integral_sum",
    "via_middle_integral",
)
MOMENT_EXPONENTS = tuple((i, j) for i in range(3) for j in range(3))
BASIS_EXPONENTS = ((0, 0), (1, 0), (0, 1), (1, 1))
VOLUME_FIELDS = {"volume", "clipped_volume"}
PAIR_FIELDS = {"clipped_product", "middle_covariance"}
TRIPLE_FIELDS = {
    "volume_product",
    "pair_product",
    "product_error",
    "tile_pair_product",
    "tile_product_error",
    "between_tile_error",
    "centered_integral",
    "within_tile_centered_integral",
    "true_integral",
    "continuum_integral",
    "original_product_sum",
    "tile_product_sum",
    "original_error",
    "tile_error",
    "between_error",
    "coarse_integral",
    "child_integral_sum",
    "via_middle_integral",
}


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
    require(ident(AK) == AK_ID, "AK artifact changed")
    return json.loads(plain_bytes(AK))


def identities():
    previous = prior_document()
    prior = {str(AK.relative_to(HERE.parent)): AK_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AK.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def project_inputs(previous):
    require(len(previous) == 5, "complete AK family inventory")
    problems = []
    for old, family in zip(previous, FAMILIES, strict=True):
        source = old["problem"]
        require(source["family"] == family, "AK family order")
        levels = []
        require(len(source["levels"]) == 3 and len(source["probes"]) == 5, "bounded AK input")
        for lev, name, size in zip(source["levels"], LEVELS, (6, 7, 8), strict=True):
            require(lev["level"] == name and len(lev["cells"]) == size, "fixed level inventory")
            levels.append(
                {
                    "level": name,
                    "cells": [
                        {key: copy.deepcopy(cell[key]) for key in ("event", "bounds")}
                        for cell in lev["cells"]
                    ],
                }
            )
        problems.append(
            {"family": family, "probes": copy.deepcopy(source["probes"]), "levels": levels}
        )
    return problems, previous


def load_inputs():
    return project_inputs(prior_document()["suite"]["families"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05al_" + name, HERE / filename)
    require(spec is not None and spec.loader is not None, "engine loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scale_family(value, alpha, beta):
    """Complete zero-translation affine transport, including contract payload."""
    alpha, beta = F(alpha), F(beta)
    require(alpha > 0 and beta > 0, "positive coordinate scales")
    k = alpha * beta

    def walk(item, field=None, context=None):
        if item is None:
            return None
        if field == "bounds":
            require(type(item) is list and len(item) == 4, "bounds shape")
            return [
                wire(frac(x) * factor)
                for x, factor in zip(item, (alpha, alpha, beta, beta), strict=True)
            ]
        if field in ("u_breaks", "v_breaks"):
            factor = alpha if field == "u_breaks" else beta
            return [wire(frac(x) * factor) for x in item]
        if field in ("moments", "coarse_moments", "child_moment_sum"):
            require(type(item) is list and len(item) == 9, "nine moments")
            return [
                wire(frac(x) * k * alpha**i * beta**j)
                for x, (i, j) in zip(item, MOMENT_EXPONENTS, strict=True)
            ]
        if field == "coefficients":
            require(type(item) is list and len(item) == 4, "four coefficients")
            return [
                wire(frac(x) * k / (alpha**i * beta**j))
                for x, (i, j) in zip(item, BASIS_EXPONENTS, strict=True)
            ]
        if field in VOLUME_FIELDS:
            return wire(frac(item) * k)
        if field in PAIR_FIELDS or (field == "causal_integral" and context == "pairs"):
            return wire(frac(item) * k**2)
        if field in TRIPLE_FIELDS or field == "causal_integral":
            return wire(frac(item) * k**3)
        if type(item) is dict:
            return {
                key: walk(child, key, key if key in ("pairs", "triples") else context)
                for key, child in item.items()
            }
        if type(item) is list:
            return [walk(child, context=context) for child in item]
        return item

    return walk(value)


def comparison_projection(family):
    answer = copy.deepcopy(family)
    del answer["problem"]["family"]
    return answer


def controls(families):
    require(len(families) == 5, "complete control inventory")
    require(
        [f["problem"]["family"] for f in families] == list(FAMILIES),
        "complete control order",
    )
    by_name = {f["problem"]["family"]: f for f in families}
    base = comparison_projection(by_name["grid"])
    verify_suite(comparison_projection(by_name["boost"]), scale_family(base, F(2), F(1, 2)))
    verify_suite(comparison_projection(by_name["dilate"]), scale_family(base, F(2), F(2)))
    verify_suite(
        comparison_projection(by_name["warp_stale"]),
        comparison_projection(by_name["warp"]),
    )
    return {"boost": True, "dilation": True, "stale_geometric": True}


def ak_level_projection(family):
    return [
        {
            "level": level["level"],
            "geometry": [
                {
                    **{key: copy.deepcopy(g[key]) for key in ("probe", "volume", "cells", "pairs")},
                    "triples": [
                        {key: copy.deepcopy(row[key]) for key in AK_TRIPLE_FIELDS}
                        for row in g["triples"]
                    ],
                }
                for g in level["geometry"]
            ],
        }
        for level in family["levels"]
    ]


def ak_coarsening_projection(family):
    return [
        {
            **{key: copy.deepcopy(link[key]) for key in ("coarse", "fine", "parents")},
            "geometry": [
                {
                    "probe": g["probe"],
                    "blocks": [
                        {key: copy.deepcopy(row[key]) for key in AK_BLOCK_FIELDS}
                        for row in g["blocks"]
                    ],
                }
                for g in link["geometry"]
            ],
        }
        for link in family["coarsenings"]
    ]


def ak_bridges(families, old):
    require(len(families) == len(old) == 5, "complete consumed AK families")
    require(
        [f["problem"]["family"] for f in families]
        == [f["problem"]["family"] for f in old]
        == list(FAMILIES),
        "AK family order",
    )
    for current, previous in zip(families, old, strict=True):
        verify_suite(current["problem"], previous["problem"])
        verify_suite(ak_level_projection(current), ak_level_projection(previous))
        verify_suite(ak_coarsening_projection(current), ak_coarsening_projection(previous))
    return {
        "AK_family_names": list(FAMILIES),
        "AK_projected_inputs_equal": True,
        "AK_complete_clipped_volumes_pairs_triples_equal": True,
        "AK_true_coarsening_equal": True,
        "other_AK_math_replayed": False,
        "other_prior_math_replayed": False,
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
                "native_family_bytes": len(canonical(family)),
                "moment_contract_bytes": len(canonical(contract)),
            }
        )
    return out


def assemble_suite(families, ak_families):
    require(len(families) == 5, "complete family inventory")
    expected, consumed = load_inputs()
    verify_suite(ak_families, consumed)
    verify_suite([f["problem"] for f in families], expected)
    totals = {"families": len(families)}
    for family in families:
        require(set(family["counts"]) == set(COUNT_FIELDS), "complete count inventory")
        require(
            all(type(v) is int and v >= 0 for v in family["counts"].values()),
            "nonnegative native counts",
        )
    for key in COUNT_FIELDS:
        totals[key] = sum(f["counts"][key] for f in families)
    return {
        "families": families,
        "controls": controls(families),
        "prior_bridges": ak_bridges(families, ak_families),
        "payload_sizes": payload_sizes(families),
        "totals": totals,
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
