"""QR-05AJ bounded pair-measure orchestration; no historical engine imports."""

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
SCHEMA = "det8-qr05aj-results-v1"
SOURCES = ("README.md", "kernel.py", "reference.py", "study.py", "test_qr05aj.py")
AI = HERE.parent / "qr-05ai-weighted-kernels-2026-09-07/results.json"
AI_ID = {
    "bytes": 14980342,
    "sha256": "17dbb103c56b6489d5aef75f4eda77108fea12bfc475fc65ffcfd82710bf6786",
}
MAX_CAPTURE_BYTES = 64 * 1024 * 1024
MAX_WORKING_BYTES = 96 * 1024 * 1024
FAMILIES = ("grid", "warp", "warp_stale", "boost", "dilate")
LEVELS = ("l0", "l1", "l2")
SCOPE = (
    "generic_production_API_hardened",
    "unknown_geometry_reconstructed",
    "marks_authenticated",
    "continuum_limit_established",
    "cross_level_observation_transport_proved",
    "higher_chain_composition_closed",
    "stochastic_transition_constructed",
    "quantum_channel_constructed",
    "gravity_derived",
    "empirical_data_used",
    "ret_integration_tested",
)
VOLUME_FIELDS = {"volume", "clipped_volume", "coarse_volume", "child_volume_sum"}
PAIR_FIELDS = {
    "clipped_product",
    "causal_integral",
    "coarse_integral",
    "child_integral_sum",
    "child_diagonal_integral",
    "child_offdiagonal_integral",
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
    require(ident(AI) == AI_ID, "AI artifact changed")
    return json.loads(plain_bytes(AI))


def identities():
    previous = prior_document()
    prior = {str(AI.relative_to(HERE.parent)): AI_ID}
    for name, want in previous["prior_artifacts"].items():
        require(ident(HERE.parent / name) == want, "prior artifact changed: " + name)
        prior[name] = want
    ancestors = dict(previous["ancestor_sources"])
    for name, want in previous["source_ledger"].items():
        ancestors[str((AI.parent / name).relative_to(HERE.parent))] = want
    for name, want in ancestors.items():
        require(ident(HERE.parent / name) == want, "ancestor source changed: " + name)
    return {
        "source_ledger": {name: ident(HERE / name) for name in SOURCES},
        "prior_artifacts": prior,
        "ancestor_sources": ancestors,
    }


def project_inputs(previous):
    require(len(previous) == 27, "complete AI case inventory")
    by_id = {c["case_id"]: c for c in previous}
    require(len(by_id) == 27, "unique AI case IDs")
    problems, consumed = [], []
    for family in FAMILIES:
        levels, probes = [], None
        for level, size in zip(LEVELS, (6, 7, 8), strict=True):
            case = by_id[family + "__" + level + "__identity"]
            source = case["source"]
            require(
                case["level"] == level
                and source["name"] == family
                and case["design"]["name"] == "identity",
                "identity source selection",
            )
            current_probes = []
            for p in source["probes"]:
                a, b = source["coordinates"][p["source"]], source["coordinates"][p["target"]]
                current_probes.append(
                    {"name": p["name"], "bounds": copy.deepcopy([a[0], b[0], a[1], b[1]])}
                )
            require(len(current_probes) == 5, "five fixed probes")
            if probes is None:
                probes = current_probes
            else:
                verify_suite(current_probes, probes)
            cells = [
                {k: copy.deepcopy(c[k]) for k in ("event", "bounds", "supplied_mark")}
                for c in source["cells"]
            ]
            require(len(cells) == size, "fixed cell inventory")
            verify_suite([c["event"] for c in cells], source["eligible"])
            levels.append({"level": level, "cells": cells})
            consumed.append(case)
        problems.append({"family": family, "probes": probes, "levels": levels})
    return problems, consumed


def load_inputs():
    return project_inputs(prior_document()["suite"]["cases"])


def load_engine(name):
    require(name in ("primary", "reference"), "unknown route")
    filename = "kernel.py" if name == "primary" else "reference.py"
    spec = importlib.util.spec_from_file_location("qr05aj_" + name, HERE / filename)
    require(spec is not None and spec.loader is not None, "engine loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measure_projection(family):
    return {k: copy.deepcopy(family[k]) for k in ("levels", "coarsenings", "counts")}


def scale_geometry(value, factor, field=None):
    if value is None:
        return None
    if field in VOLUME_FIELDS:
        return wire(frac(value) * factor)
    if field in PAIR_FIELDS:
        return wire(frac(value) * factor**2)
    if type(value) is dict:
        return {k: scale_geometry(v, factor, k) for k, v in value.items()}
    if type(value) is list:
        return [scale_geometry(v, factor) for v in value]
    return value


def omit_annotation_candidate(value):
    excluded = {
        "annotation_weight",
        "annotation_weighted_child_conditional",
        "annotation_mismatches",
    }
    if type(value) is dict:
        return {k: omit_annotation_candidate(v) for k, v in value.items() if k not in excluded}
    if type(value) is list:
        return [omit_annotation_candidate(v) for v in value]
    return value


def controls(families):
    by_name = {f["problem"]["family"]: f for f in families}
    base = measure_projection(by_name["grid"])
    verify_suite(measure_projection(by_name["boost"]), base)
    verify_suite(measure_projection(by_name["dilate"]), scale_geometry(base, F(4)))
    verify_suite(
        omit_annotation_candidate(measure_projection(by_name["warp_stale"])),
        omit_annotation_candidate(measure_projection(by_name["warp"])),
    )
    return {"boost": True, "dilation": True, "stale_geometric": True}


def ai_bridges(families, old):
    require(len(old) == 15, "complete consumed AI case count")
    ids = []
    for f in families:
        for level in f["levels"]:
            case_id = f["problem"]["family"] + "__" + level["level"] + "__identity"
            previous = old[len(ids)]
            require(previous["case_id"] == case_id, "AI case order")
            ids.append(case_id)
            require(len(level["geometry"]) == len(previous["geometry"]), "AI probe count")
            for g, p in zip(level["geometry"], previous["geometry"], strict=True):
                verify_suite(
                    {"probe": g["probe"], "volume": g["volume"]},
                    {"probe": p["probe"], "volume": p["volume"]},
                )
                verify_suite(
                    [{"event": c["event"], "volume": c["clipped_volume"]} for c in g["cells"]],
                    p["cell_clips"],
                )
                fields = ("first", "second", "clipped_product", "causal_integral")
                verify_suite(
                    [{k: pair[k] for k in fields} for pair in g["pairs"]],
                    [{k: pair[k] for k in fields} for pair in p["pair_cells"]],
                )
    return {
        "AI_identity_case_ids": ids,
        "AI_projected_inputs_equal": True,
        "AI_complete_clipped_volumes_and_pairs_equal": True,
        "AI_sampling_math_replayed": False,
        "other_prior_math_replayed": False,
    }


def composition_witness():
    h = F(1, 2)
    pair, shared = F(1, 4), F(1, 36)
    product = pair**2
    return {
        "h": wire(h),
        "pair_fraction": wire(pair),
        "squared_pair_fraction": wire(product),
        "shared_middle_fraction": wire(shared),
        "pair_measure": wire(h**2 * pair),
        "block_product_measure": wire(h**3 * product),
        "shared_middle_measure": wire(h**3 * shared),
        "signed_product_error": wire(h**3 * (product - shared)),
    }


def assemble_suite(families, ai_cases):
    require(len(families) == 5, "complete family inventory")
    expected, consumed = load_inputs()
    verify_suite(ai_cases, consumed)
    verify_suite([f["problem"] for f in families], expected)
    totals = {"families": len(families)}
    for key in families[0]["counts"]:
        totals[key] = sum(f["counts"][key] for f in families)
    return {
        "families": families,
        "controls": controls(families),
        "prior_bridges": ai_bridges(families, ai_cases),
        "composition_witness": composition_witness(),
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
