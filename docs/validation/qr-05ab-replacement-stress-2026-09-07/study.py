"""QR-05AB frozen-forecast replacement-mechanism stress and replay.

The runner carries its own nominal AA oracle and law checks. New actual laws
come from unnormalized clean N/future subjoint pushforwards; candidate risks
are projected quadratically then checked by literal coordinate loss.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import itertools
import json
import platform
import re
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05ab-results-v1"
BASE_COMMIT = "f486271e01de688be100ec0a7bfd256791ed0422"
SOURCES = (
    "README.md",
    "stress.py",
    "reference_qr05ab.py",
    "study.py",
    "test_qr05ab.py",
    "test_capture.py",
    "audit_json.py",
)
AA_PRIOR = "qr-05aa-uncertainty-decisions-2026-09-07/results.json"
AA_BYTES = 112206
AA_SHA = "bf5661984f9df4cb111fbe97061035967de9f7516a26154abefc7d1d3a49c424"
Z_PRIOR = "qr-05z-fixed-attenuation-2026-09-07/results.json"
Z_BYTES = 31075315
Z_SHA = "7828dafe766ae4cef9e2fd8dcc6181079fe936e8720a70367598aaf3bcbb8ccc"
Y_PRIOR = "qr-05y-explicit-fallback-2026-09-07/results.json"
Y_BYTES = 16474309
Y_SHA = "c4189b0f1bb0df4bb3e5f14c1969ede0ee754f59b4bc99e89aeac8d6b065891f"
X_PRIOR = "qr-05x-noise-misspecification-2026-09-07/results.json"
X_BYTES = 8842933
X_SHA = "1bf12e668ccaaeb20da78d849ae138ffcce2cc32e14be57f286169c74a4734c4"
W_PRIOR = "qr-05w-noisy-readouts-2026-09-07/results.json"
W_BYTES = 6756094
W_SHA = "05b20faf7feae7327113ace9168540d61db0e0e6bebae268819b2b84847cce8a"
LEVELS = [[0, 1], [1, 2], [3, 4], [1, 1]]
MAX_CAPTURE_BYTES = 64 * 1024 * 1024
MAX_WORKING_BYTES = 128 * 1024 * 1024

PRIORS = {
    AA_PRIOR: AA_SHA,
    Z_PRIOR: Z_SHA,
    Y_PRIOR: Y_SHA,
    X_PRIOR: X_SHA,
    W_PRIOR: W_SHA,
    "qr-05v-readout-value-2026-09-06/results.json": "eceb01f49624f3d5ebb5dc8041074aa04b62d8408d4a7117979fb1c6b9823ff7",
    "qr-05u-partial-observation-2026-09-06/results.json": "a2cf4ae0bb31934c3c1aeab7071fb6f675d90d9f0b1a5c2776282e926e3e5eee",
    "qr-05t-local-refinement-2026-09-06/results.json": "f7bf6db5dd822c27a3087c6ad48af3ae76fdce653536cff8d381bfae905a5fe8",
    "qr-05s-local-deletion-2026-09-06/results.json": "8caa59a1921dc7fb46a38e44058bfe9f2ac5608c1f2ed05e5dc8ff063ab7e3b3",
    "qr-05r-deletion-profile-2026-09-06/results.json": "cfec27d60d605ec142af96f8931e0e90b3c5ca92c72389ce8e0d84ef8b444001",
    "qr-05q-three-layer-portability-2026-09-06/results.json": "1e9b9443ee5d55cd888d5ea62e594fad197ca0baeecfee1f1efac34ada8125aa",
    "qr-05p-minimal-summary-2026-09-06/results.json": "c43435c4916e5c15efb373ff70795ed733d7c4e360ebec4e9a1b32f4e050b048",
    "qr-05o-path-observable-2026-09-06/results.json": "3364b36813f745a645d78d6d30caa292778da986cb6d1140f108a0fd4b945eb1",
    "qr-05n-domain-portability-2026-09-06/results.json": "f2d666285afef41cd8a7f977399d3626a620da39174967a38047714f5f26f93e",
    "qr-05m-observable-realization-2026-09-06/results.json": "79cb515022fdb3bb2c918a469c1ac5ffdf98a6dd18cdd289f8030fc7a38f1543",
    "qr-05l-adversarial-refinement-2026-09-06/results.json": "0df1b47e1219191783a9ec229540fd433e2129121ce2c5f6e5262e5f3c00e0ff",
    "qr-05k-recursive-closure-2026-09-06/results.json": "46d93f643c443b75ef425349cff11d7f3c437a79921e7e1ee94610998bd1a501",
    "qr-05j-uncertainty-contract-2026-09-06/results.json": "dc8f80f40861107dd7a5ee378c9813a90c1981a3c2e7e14ee343163e9d88c333",
    "qr-05i-analytic-portability-2026-09-06/results.json": "9742e602b037ce74611e7801256f86752f584438a80f9dac6c823acef671e798",
    "qr-05h-law-portability-2026-09-06/results.json": "e6d5f06d765ccca7a1da1cef15d12bc15a3287463ec3cce3732aab75af613b3a",
    "qr-05g-predictive-compression-2026-09-06/results.json": "62b13d1c46efcd5552596f37ba9ec5ab00f8e9708bab19f811cc0a0a357ffb74",
    "qr-01-quantum-records-2026-09-05/results.json": "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b",
    "qr-02-record-coarse-graining-2026-09-05/results.json": "b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c",
    "qr-03-predictive-histories-2026-09-05/results.json": "2b92b7bd42aa9cde29722269c1a31f339e37b217d1256e50d8ea0ee34d8188c2",
    "qr-04-adaptive-causal-records-2026-09-05/results.json": "a5dc5f5e96a189ae8fd5648334e630fd4c24f6cee2fa805a45d32522bc0bcd70",
    "qr-05a-quantum-births-2026-09-05/results.json": "e0c2676ae33b36dde3edb2697ac252330ad801006fe8420acd8cfb94b87c9479",
    "qr-05b-order-summaries-2026-09-05/results.json": "2fe3fd939dcc242ee2a6b8c4abc9d6904e32bf5072cf638f7d880daaeaf2e03b",
    "qr-05c-coarse-dynamics-2026-09-05/results.json": "4f7bb191e64db6bb24886cc1211cb83186d7e24f77599e56e25539c100f4dde1",
    "qr-05d-geometric-correspondence-2026-09-05/results.json": "ea3404f9401573c833965fc259b0f01dc28e3e3968ef79b4b3438e6535cd1238",
    "qr-05d-geometric-correspondence-2026-09-05/results-v2.json": "18499d8a126a3677fb0f0e54a98659df7934c7429c39cc0f531adfc063d40b32",
    "qr-05f-two-stage-2026-09-06/results.json": "0fffba7f9d8549b2e12d90551c82dc72e0ead7f4010923578af610e055683917",
    "qr-05e-sampling-aware-2026-09-06/results.json": "362e7f0c00f00491cd3820fd840faca63b244ed4a0c2156bcb3d0924baa52f41",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def plain_bytes(path):
    require(path.is_file() and not path.is_symlink(), "input must be a plain file")
    return path.read_bytes()


def ledger():
    result = {}
    for name in SOURCES:
        raw = plain_bytes(HERE / name)
        result[name] = {"bytes": len(raw), "sha256": digest(raw)}
    return result


def priors():
    result = {}
    for name, sha in PRIORS.items():
        raw = plain_bytes(HERE.parent / name)
        require(digest(raw) == sha, "prior artifact changed")
        result[name] = {"bytes": len(raw), "sha256": sha}
    return result


def prior_json(name):
    raw = plain_bytes(HERE.parent / name)
    require(digest(raw) == PRIORS[name], "prior artifact changed")
    return json.loads(raw)


def load(name, filename):
    require(name not in sys.modules, "private study module collision")
    path = HERE / filename
    raw = plain_bytes(path)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "cannot load executor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)  # noqa: S102
    return module


def retained_bits(value):
    if type(value) is dict:
        return max((retained_bits(v) for v in value.values()), default=0)
    if type(value) is list:
        return max((retained_bits(v) for v in value), default=0)
    if type(value) is int:
        return abs(value).bit_length()
    if type(value) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value):
        v = F(value)
        return max(abs(v.numerator).bit_length(), v.denominator.bit_length())
    return 0


def require_wire(value):
    """Native validation with per-call DAG accounting before serialization.

    Expanded value nodes lower-bound JSON bytes. Repeated references count
    each occurrence, but completed subtrees are walked only once. Depth is
    safely above valid AB schemas, including evidence envelopes.
    """
    active, completed = set(), {}
    pending = [(value, 0, False)]
    while pending:
        item, depth, leaving = pending.pop()
        identity = id(item)
        if leaving:
            children = item if type(item) is list else item.values()
            nodes, height = 1, 0
            for child in children:
                count, child_height = (
                    completed[id(child)] if type(child) in (list, dict) else (1, 0)
                )
                nodes += count
                height = max(height, child_height + 1)
                require(nodes <= MAX_WORKING_BYTES, "expanded wire exceeds working byte cap")
            completed[identity] = nodes, height
            active.remove(identity)
            continue
        require(depth <= 128, "wire exceeds bounded schema depth")
        if item is None or type(item) in (bool, int, str):
            continue
        require(type(item) in (list, dict), "mathematical suite must use native exact JSON types")
        require(identity not in active, "cyclic wire container")
        if identity in completed:
            require(depth + completed[identity][1] <= 128, "wire exceeds bounded schema depth")
            continue
        if type(item) is dict:
            require(all(type(key) is str for key in item), "wire keys must be strings")
        active.add(identity)
        pending.append((item, depth, True))
        children = item if type(item) is list else item.values()
        pending.extend((child, depth + 1, False) for child in children)


def canonical(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


def require_same_wire(left, right, message):
    require_wire(left)
    require_wire(right)
    require(canonical(left) == canonical(right), message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    require(
        sys.flags.isolated and sys.pycache_prefix, "run isolated with an external bytecode cache"
    )
    cache = Path(sys.pycache_prefix).resolve()
    require(
        cache != Path(cache.anchor) and not cache.is_relative_to(ROOT),
        "invalid bytecode cache boundary",
    )
    if not args.verify and (RESULT.exists() or RESULT.is_symlink()):
        raise FileExistsError("result exists; use --verify, never overwrite")
    frozen, previous = ledger(), priors()
    if args.verify:
        before = plain_bytes(RESULT)
        require(len(before) <= MAX_CAPTURE_BYTES, "artifact byte cap")
        existing = json.loads(before)
        require(
            type(existing) is dict
            and set(existing)
            == {"schema_version", "source_ledger", "prior_artifacts", "suite", "runtime"}
            and existing["schema_version"] == SCHEMA,
            "unrecognized result schema",
        )
        require(canonical(existing) == before, "result is not canonical")
        require_same_wire(existing["source_ledger"], frozen, "source identity changed")
        require_same_wire(existing["prior_artifacts"], previous, "prior identity changed")
    started = time.perf_counter()
    suite = run_suite()
    require_wire(suite)
    require(retained_bits(suite) <= 4096, "retained suite component bit bound")
    require_same_wire(suite, json.loads(canonical(suite)), "aggregate wire round trip differs")
    elapsed = time.perf_counter() - started
    require(ledger() == frozen and priors() == previous, "source/prior changed during execution")
    if args.verify:
        require_same_wire(existing["suite"], suite, "exact replay differs")
        require(plain_bytes(RESULT) == before, "result changed during replay")
        print(
            json.dumps(
                {
                    "status": "VERIFIED_EXACT_REPLAY",
                    "sha256": digest(before),
                    "seconds": elapsed,
                    "totals": suite["totals"],
                }
            )
        )
        return
    report = {
        "schema_version": SCHEMA,
        "source_ledger": frozen,
        "prior_artifacts": previous,
        "suite": suite,
        "runtime": {
            "python": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
            "isolated": bool(sys.flags.isolated),
            "optimized": sys.flags.optimize,
            "bytecode_cache": str(cache),
            "suite_seconds": elapsed,
            "rss_high_water_at_suite_end": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "rss_units": "bytes" if sys.platform == "darwin" else "KiB",
            "scope": "suite and internal exact JSON checks; excludes final report serialization; no application performance claim",
        },
    }
    raw = canonical(report)
    require(len(raw) <= MAX_CAPTURE_BYTES, "artifact byte cap")
    with RESULT.open("xb") as output:
        output.write(raw)
    require(plain_bytes(RESULT) == raw, "capture readback differs")
    print(
        json.dumps(
            {
                "status": "CREATED_EXACT_FINITE_RESULT",
                "path": str(RESULT),
                "bytes": len(raw),
                "sha256": digest(raw),
                "seconds": elapsed,
                "totals": suite["totals"],
            }
        )
    )


WEIGHTS = [[0, 1], [1, 2], [1, 1]]
CHECKS = (
    "coarse_zero",
    "nested_uncertainty",
    "complete_argmax",
    "complete_argmin",
    "minimax_nonpositive",
    "bound_extension_non_decrease",
)
AA_COUNTS = {
    "worlds": 4,
    "assumed_models": 4,
    "rules": 3,
    "decisions": 16,
    "world_rule_cells": 48,
    "excess_terms": 48,
    "candidate_world_visits": 120,
    "candidate_selection_visits": 48,
    "total_decision_work": 216,
}


def fraction(value):
    require(type(value) is list and len(value) == 2, "fraction pair")
    n, d = value
    require(type(n) is int and type(d) is int and d > 0, "fraction native components")
    result = F(n, d)
    require(
        -2 <= result <= 2 and [result.numerator, result.denominator] == value,
        "fraction range/reduction",
    )
    require(max(abs(n).bit_length(), d.bit_length()) <= 4096, "fraction bit cap")
    return result


def wire(value):
    require(type(value) is F and -2 <= value <= 2, "retained fraction range")
    require(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= 4096,
        "retained fraction bits",
    )
    return [value.numerator, value.denominator]


def nominal_problem(case):
    analysis = case["analysis"]
    require_same_wire(analysis["levels"], LEVELS, "four actual/assumed levels")
    require_same_wire(analysis["retained_weights"], WEIGHTS, "three fixed choices")
    worlds = []
    for actual in range(4):
        coarse = analysis["baseline"]["aggregate"]["pairs"][4 * actual]["coarse_forecast_risk"]
        models = []
        for assumed in range(4):
            index = 4 * actual + assumed
            require_same_wire(
                analysis["baseline"]["aggregate"]["pairs"][index]["coarse_forecast_risk"],
                coarse,
                "same-world common coarse risk",
            )
            pair = analysis["aggregate"]["pairs"][index]
            require(
                pair["actual_index"] == actual and pair["assumed_index"] == assumed,
                "ordered Z pair",
            )
            models.append(
                {
                    "assumed_index": assumed,
                    "forecast_risks": [
                        copy.deepcopy(blend["forecast_risk"]) for blend in pair["blends"]
                    ],
                }
            )
        worlds.append(
            {"actual_index": actual, "coarse_risk": copy.deepcopy(coarse), "models": models}
        )
    return {
        "schema_version": "det8-qr05aa-problem-v1",
        "family": "qr05aa_uncertainty_decision",
        "levels": copy.deepcopy(LEVELS),
        "retained_weights": copy.deepcopy(WEIGHTS),
        "worlds": worlds,
    }


def nominal_expected(problem):
    """Independent enumerate-all-extrema oracle, not an engine import."""
    worlds = copy.deepcopy(problem["worlds"])
    for world in worlds:
        coarse = fraction(world["coarse_risk"])
        for model in world["models"]:
            model["excess_risks"] = [wire(fraction(r) - coarse) for r in model["forecast_risks"]]
    decisions = []
    for assumed in range(4):
        previous = None
        for bound in range(4):
            indices = list(range(bound + 1))
            candidates, worst_values = [], []
            for rule, weight in enumerate(WEIGHTS):
                values = [
                    fraction(worlds[t]["models"][assumed]["excess_risks"][rule]) for t in indices
                ]
                worst = max(values)
                argmax = [t for t, v in zip(indices, values, strict=True) if v == worst]
                candidates.append(
                    {
                        "retained_weight": copy.deepcopy(weight),
                        "world_excesses": [wire(v) for v in values],
                        "worst_excess": wire(worst),
                        "worst_world_indices": argmax,
                    }
                )
                worst_values.append(worst)
            optimum = min(worst_values)
            argmin = [i for i, v in enumerate(worst_values) if v == optimum]
            require(worst_values[0] == 0 and optimum <= 0, "coarse option bound")
            if previous is not None:
                require(
                    all(a <= b for a, b in zip(previous[0], worst_values, strict=True))
                    and previous[1] <= optimum,
                    "nested uncertainty extrema",
                )
            previous = worst_values, optimum
            decisions.append(
                {
                    "assumed_index": assumed,
                    "bound_index": bound,
                    "world_indices": indices,
                    "candidates": candidates,
                    "minimax_excess": wire(optimum),
                    "minimizer_indices": argmin,
                    "minimizer_weights": [copy.deepcopy(WEIGHTS[i]) for i in argmin],
                    "checks": dict.fromkeys(CHECKS, True),
                }
            )
    return {
        "input_sha256": digest(canonical(problem)),
        "levels": copy.deepcopy(LEVELS),
        "retained_weights": copy.deepcopy(WEIGHTS),
        "worlds": worlds,
        "decisions": decisions,
        "counts": dict(AA_COUNTS),
    }


def prediction(rows):
    values = {tuple(row["value"]): fraction(row["probability"]) for row in rows}
    require(
        len(values) == len(rows)
        and sum(values.values(), F(0)) == 1
        and all(p > 0 for p in values.values()),
        "complete normalized positive law",
    )
    return values


def literal_loss(actual, forecast):
    coordinates = actual.keys() | forecast.keys()
    return sum(
        (
            mass
            * sum(
                (
                    (F(int(outcome == coordinate)) - forecast.get(coordinate, F(0))) ** 2
                    for coordinate in coordinates
                ),
                F(0),
            )
            for outcome, mass in actual.items()
        ),
        F(0),
    )


def joint(channel):
    return {
        (tuple(cell["value"]), future): fraction(cell["probability"]) * mass
        for cell in channel["cells"]
        for future, mass in prediction(cell["prediction"]).items()
    }


def verify_nominal_laws_and_risks(case, problem):
    """Original-law literal scorer plus family checks; no minimax oracle."""
    z = case["analysis"]
    experiment = case["problem"]["experiment"]
    require_same_wire(len(z["beliefs"]), len(experiment["beliefs"]), "history inventory")
    require(
        sum((fraction(b["weight"]) for b in experiment["beliefs"]), F(0)) == 1,
        "original history weights",
    )
    sums = [[[F(0) for _ in WEIGHTS] for _ in LEVELS] for _ in LEVELS]
    coarse_sums = [[F(0) for _ in LEVELS] for _ in LEVELS]
    seen = {}
    full_coincidence = [True] * 4
    for source, zb, yb in zip(
        experiment["beliefs"], z["beliefs"], z["baseline"]["beliefs"], strict=True
    ):
        bid = source["belief_id"]
        require_same_wire(source["weight"], zb["weight"], "Z original history likelihood")
        require_same_wire(source["weight"], yb["weight"], "Y original history likelihood")
        history_weight = fraction(source["weight"])
        channels = source["channels"]
        joints = [joint(c) for c in channels]
        atoms = set().union(*(j.keys() for j in joints))
        for t, level in enumerate(LEVELS):
            rate = fraction(level)
            for atom in atoms:
                require(
                    joints[t].get(atom, F(0))
                    == (1 - rate) * joints[0].get(atom, F(0)) + rate * joints[3].get(atom, F(0)),
                    "complete affine actual joint law",
                )
        fallbacks = {tuple(r["value"]): prediction(r["prediction"]) for r in source["fallbacks"]}
        # Authenticate true N fallback and invariant N mass for this pinned family.
        prefix_weights = []
        for j in joints:
            masses, laws = {}, {}
            for (report, future), mass in j.items():
                prefix = report[:5]
                masses[prefix] = masses.get(prefix, F(0)) + mass
                laws.setdefault(prefix, {})[future] = (
                    laws.setdefault(prefix, {}).get(future, F(0)) + mass
                )
            prefix_weights.append(masses)
            for prefix, mass in masses.items():
                require(
                    {v: p / mass for v, p in laws[prefix].items()} == fallbacks[prefix],
                    "true N conditional fallback",
                )
        require(all(v == prefix_weights[0] for v in prefix_weights), "N mass preservation")
        clean = {tuple(c["value"]): c for c in channels[0]["cells"]}
        assumed_cells = [{tuple(c["value"]): c for c in ch["cells"]} for ch in channels]
        for actual in range(4):
            for assumed in range(4):
                index = 4 * actual + assumed
                zpair, ypair = zb["pairs"][index], yb["pairs"][index]
                require_same_wire(len(zpair["cells"]), len(ypair["cells"]), "Z/Y report inventory")
                for cell, base in zip(zpair["cells"], ypair["cells"], strict=True):
                    require_same_wire(cell["value"], base["value"], "Z/Y report order")
                    report = tuple(cell["value"])
                    p = prediction(base["actual_prediction"])
                    f = prediction(base["forecast"])
                    g = prediction(base["coarse_forecast"])
                    require(g == fallbacks[report[:5]], "common coarse law")
                    if report in clean:
                        m0 = fraction(clean[report]["probability"])
                        ms = fraction(assumed_cells[assumed][report]["probability"])
                        beta = (1 - fraction(LEVELS[assumed])) * m0 / ms
                        require(0 <= beta <= 1, "clean forecast segment coefficient")
                        p0 = prediction(clean[report]["prediction"])
                        segment = {
                            v: (1 - beta) * g.get(v, F(0)) + beta * p0.get(v, F(0))
                            for v in g.keys() | p0.keys()
                        }
                        require(
                            {v: p for v, p in segment.items() if p} == f,
                            "complete clean forecast segment",
                        )
                    else:
                        require(f == g, "clean-zero replacement or explicit fallback")
                    report_weight = fraction(base["actual_probability"])
                    cg = literal_loss(p, g)
                    require_same_wire(wire(cg), base["coarse_risk"], "literal coarse score")
                    coarse_sums[actual][assumed] += history_weight * report_weight * cg
                    distance = sum(
                        ((f.get(v, F(0)) - g.get(v, F(0))) ** 2 for v in f.keys() | g.keys()), F(0)
                    )
                    require_same_wire(
                        wire(distance), cell["forecast_distance"], "complete endpoint distance"
                    )
                    if actual == 3:
                        require(p == g, "full replacement true coarse")
                        full_coincidence[assumed] &= f == g
                    for rule, blend in enumerate(cell["blends"]):
                        a = fraction(WEIGHTS[rule])
                        h = prediction(blend["forecast"])
                        expected = {
                            v: (1 - a) * g.get(v, F(0)) + a * f.get(v, F(0))
                            for v in f.keys() | g.keys()
                        }
                        require(
                            {v: p for v, p in expected.items() if p} == h, "full mixed forecast"
                        )
                        key = bid, assumed, rule, report
                        require(
                            key not in seen or seen[key] == h, "forecast depends on actual index"
                        )
                        seen[key] = h
                        risk = literal_loss(p, h)
                        require_same_wire(wire(risk), blend["forecast_risk"], "literal mixed score")
                        require_same_wire(
                            wire(cg - risk), blend["gain_over_coarse"], "cell signed gain"
                        )
                        sums[actual][assumed][rule] += history_weight * report_weight * risk
                        if actual == 0:
                            require(risk <= cg, "clean nonpositive excess")
                        if actual == 3:
                            require(
                                risk - cg == a * a * distance, "full replacement quadratic penalty"
                            )
    for actual in range(4):
        for assumed in range(4):
            require_same_wire(
                wire(coarse_sums[actual][assumed]),
                problem["worlds"][actual]["coarse_risk"],
                "original-weight coarse risk",
            )
            for rule in range(3):
                require_same_wire(
                    wire(sums[actual][assumed][rule]),
                    problem["worlds"][actual]["models"][assumed]["forecast_risks"][rule],
                    "original-weight complete risk",
                )
                require_same_wire(
                    wire(coarse_sums[actual][assumed] - sums[actual][assumed][rule]),
                    z["aggregate"]["pairs"][4 * actual + assumed]["blends"][rule][
                        "gain_over_coarse"
                    ],
                    "negative Z aggregate gain",
                )
    return full_coincidence


def nominal_producer_controls(analysis, case):
    problem = nominal_problem(case)
    require_same_wire(
        analysis["worlds"],
        nominal_expected(problem)["worlds"],
        "complete authenticated risk-table projection",
    )
    coincidence = verify_nominal_laws_and_risks(case, problem)
    for assumed in range(4):
        coarse = [fraction(w["coarse_risk"]) for w in problem["worlds"]]
        require(all(v == coarse[0] for v in coarse), "W constant coarse risk")
        for rule in range(3):
            risks = [
                fraction(w["models"][assumed]["forecast_risks"][rule]) for w in problem["worlds"]
            ]
            excesses = [r - g for r, g in zip(risks, coarse, strict=True)]
            for t, level in enumerate(LEVELS):
                a = fraction(level)
                require(risks[t] == (1 - a) * risks[0] + a * risks[3], "affine risk")
                require(coarse[t] == (1 - a) * coarse[0] + a * coarse[3], "affine coarse risk")
                require(
                    excesses[t] == (1 - a) * excesses[0] + a * excesses[3], "affine signed excess"
                )
            require(all(a <= b for a, b in itertools.pairwise(excesses)), "W nondecreasing excess")
            for bound in range(4):
                decision = analysis["decisions"][4 * assumed + bound]
                candidate = decision["candidates"][rule]
                require(
                    bound in candidate["worst_world_indices"]
                    and fraction(candidate["worst_excess"]) == excesses[bound],
                    "W upper endpoint among all worst worlds",
                )
        full = analysis["decisions"][4 * assumed + 3]
        require(
            0 in full["minimizer_indices"] and fraction(full["minimax_excess"]) == 0,
            "full bound includes coarse",
        )
        require(
            full["minimizer_indices"] == ([0, 1, 2] if coincidence[assumed] else [0]),
            "full-bound complete-law tie condition",
        )
    return {
        **dict.fromkeys(
            (
                "risk_table_matches_Z",
                "literal_forecast_risks_checked",
                "original_history_report_weights_preserved",
                "fixed_rule_forecasts_actual_index_independent",
                "W_affine_actual_joint_and_risk",
                "W_constant_coarse_risk",
                "W_clean_forecast_segment_and_excess",
                "W_full_replacement_quadratic_penalty",
                "W_excess_monotonicity_and_upper_endpoint",
                "W_full_bound_coarse_and_coincidence_ties",
            ),
            True,
        ),
        "origin_authenticated_by_generic_API": False,
        "raw_history_reconstruction_performed_by_this_runner": False,
    }


def nominal_check(analysis, case):
    problem = nominal_problem(case)
    require_same_wire(analysis, nominal_expected(problem), "independent complete AA output")
    return nominal_producer_controls(analysis, case)


MECHANISMS = ("forward", "reverse")
AB_CHECKS = (
    "nominal_selection_preserved",
    "complete_argmax",
    "all_any_quantifiers",
    "signed_bound_comparison",
    "coarse_zero",
    "nested_worlds",
    "world_witnesses_complete",
)


def wide(value):
    require(type(value) is F and -4 <= value <= 4, "wide retained difference range")
    require(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= 4096,
        "wide retained difference bits",
    )
    return [value.numerator, value.denominator]


def fixtures():
    aa, z, w = (prior_json(name) for name in (AA_PRIOR, Z_PRIOR, W_PRIOR))
    aa_raw = plain_bytes(HERE.parent / AA_PRIOR)
    require(len(aa_raw) == AA_BYTES and canonical(aa) == aa_raw, "pinned canonical AA envelope")
    require_same_wire(
        aa["prior_artifacts"],
        {k: v for k, v in priors().items() if k != AA_PRIOR},
        "AA 32-artifact lineage",
    )
    require_same_wire(
        [c["case_id"] for c in aa["suite"]["cases"]],
        [c["case_id"] for c in z["suite"]["cases"]],
        "AA/Z case order",
    )
    require_same_wire(
        [c["case_id"] for c in aa["suite"]["cases"]],
        [c["case_id"] for c in w["suite"]["cases"]],
        "AA/W case order",
    )
    return {"aa": aa["suite"], "z": z["suite"], "w": w["suite"]}


def replacement_laws(wsuite):
    alphabet = {}
    for row in wsuite["model"]["labels"]:
        n, value = tuple(row["observation"]), tuple(row["question"])
        require(value[:5] == n, "whole-model NMT prefix")
        alphabet.setdefault(n, set()).add(value)
    original = [
        {"N": list(n), "values": [list(v) for v in sorted(values)]}
        for n, values in sorted(alphabet.items())
    ]
    require(
        len(original) == 72 and sum(len(r["values"]) for r in original) == 93,
        "fixed whole-model alphabet inventory",
    )
    for case in wsuite["cases"]:
        require_same_wire(
            original,
            case["analysis"]["channel_model"]["alphabet"],
            "whole-model distinct labels including zero-prior labels",
        )
    answer = []
    for mechanism in MECHANISMS:
        rows = []
        for row in original:
            values = row["values"]
            m = len(values)
            probabilities = [
                F(2 * (r + 1 if mechanism == "forward" else m - r), m * (m + 1)) for r in range(m)
            ]
            require(
                sum(probabilities, F(0)) == 1 and all(p > 0 for p in probabilities),
                "positive normalized rank tilt",
            )
            rows.append(
                {
                    "N": copy.deepcopy(row["N"]),
                    "values": [
                        {"value": copy.deepcopy(value), "probability": wire(p)}
                        for value, p in zip(values, probabilities, strict=True)
                    ],
                }
            )
        answer.append({"mechanism_id": mechanism, "alphabet": rows})
    for left, right in zip(answer[0]["alphabet"], answer[1]["alphabet"], strict=True):
        m = len(left["values"])
        for a, b in zip(left["values"], right["values"], strict=True):
            require_same_wire(a["value"], b["value"], "opposite tilt support")
            require(
                (fraction(a["probability"]) + fraction(b["probability"])) / 2 == F(1, m),
                "opposite tilts average uniform",
            )
    return answer


def n_subjoints(clean):
    by_prefix = {}
    for (report, future), mass in clean.items():
        prefix = report[:5]
        row = by_prefix.setdefault(prefix, {})
        row[future] = row.get(future, F(0)) + mass
    return by_prefix


def pushed_channel(clean, n_joint, mu, rate):
    """Direct unnormalized N/future joint formula, not posterior averaging."""
    cells = []
    for prefix, subjoint in sorted(n_joint.items()):
        for report, tilt in sorted(mu[prefix].items()):
            law = {
                q: (1 - rate) * clean.get((report, q), F(0)) + rate * tilt * mass
                for q, mass in subjoint.items()
            }
            law = {q: p for q, p in law.items() if p}
            mass = sum(law.values(), F(0))
            if mass:
                cells.append(
                    {
                        "value": list(report),
                        "probability": wire(mass),
                        "prediction": [
                            {"value": list(q), "probability": wire(p / mass)}
                            for q, p in sorted(law.items())
                        ],
                    }
                )
    require(
        sum((fraction(c["probability"]) for c in cells), F(0)) == 1,
        "pushed actual report normalization",
    )
    return {"level": wire(rate), "cells": cells}


def build_stress_laws(zcase, laws):
    answer = []
    source = zcase["problem"]["experiment"]
    for mechanism in laws:
        mu = {
            tuple(r["N"]): {tuple(v["value"]): fraction(v["probability"]) for v in r["values"]}
            for r in mechanism["alphabet"]
        }
        beliefs = []
        for belief in source["beliefs"]:
            clean = joint(belief["channels"][0])
            n_joint = n_subjoints(clean)
            channels = [pushed_channel(clean, n_joint, mu, fraction(t)) for t in LEVELS]
            beliefs.append(
                {
                    "belief_id": belief["belief_id"],
                    "weight": copy.deepcopy(belief["weight"]),
                    "channels": channels,
                }
            )
        answer.append({"mechanism_id": mechanism["mechanism_id"], "beliefs": beliefs})
    return answer


def policy_maps(zcase):
    """Frozen full-support Z rules; no new assumed posterior is formed."""
    result = []
    for row, base in zip(
        zcase["analysis"]["beliefs"], zcase["analysis"]["baseline"]["beliefs"], strict=True
    ):
        models = []
        for assumed in range(4):
            mapping = {}
            for cell, old in zip(
                row["pairs"][12 + assumed]["cells"],
                base["pairs"][12 + assumed]["cells"],
                strict=True,
            ):
                require_same_wire(cell["value"], old["value"], "frozen full-support report order")
                g, f = prediction(old["coarse_forecast"]), prediction(old["forecast"])
                forecasts = [prediction(b["forecast"]) for b in cell["blends"]]
                require(forecasts[0] == g and forecasts[2] == f, "frozen endpoint forecasts")
                mapping[tuple(cell["value"])] = (g, f, forecasts)
            models.append(mapping)
        for report, (g, _, _) in models[0].items():
            require(
                all(report in m and m[report][0] == g for m in models),
                "shared coarse rule for all assumed models",
            )
        result.append(models)
    return result


def quadratic_loss(actual, forecast):
    return (
        F(1)
        - 2 * sum((mass * forecast.get(q, F(0)) for q, mass in actual.items()), F(0))
        + sum((p * p for p in forecast.values()), F(0))
    )


def score_stress(zcase, evidence, literal=False):
    policies = policy_maps(zcase)
    output = []
    for mechanism in evidence:
        sums = [[[F(0) for _ in WEIGHTS] for _ in LEVELS] for _ in LEVELS]
        coarse = [F(0) for _ in LEVELS]
        for source, original, models in zip(
            mechanism["beliefs"], zcase["problem"]["experiment"]["beliefs"], policies, strict=True
        ):
            require_same_wire(source["belief_id"], original["belief_id"], "original history IDs")
            require_same_wire(source["weight"], original["weight"], "original history likelihoods")
            weight = fraction(source["weight"])
            for actual, channel in enumerate(source["channels"]):
                require_same_wire(channel["level"], LEVELS[actual], "ordered stressed levels")
                for cell in channel["cells"]:
                    report = tuple(cell["value"])
                    p = prediction(cell["prediction"])
                    mass = fraction(cell["probability"])
                    score = literal_loss if literal else quadratic_loss
                    g0 = models[0][report][0]
                    cg = score(p, g0)
                    coarse[actual] += weight * mass * cg
                    if literal and actual == 3:
                        require(p == g0, "tilted full-replacement true N forecast")
                    for assumed, model in enumerate(models):
                        require(report in model, "frozen policy covers full tilted support")
                        g, f, forecasts = model[report]
                        require(g == g0, "frozen shared coarse law")
                        distance = sum(
                            ((f.get(q, F(0)) - g.get(q, F(0))) ** 2 for q in f.keys() | g.keys()),
                            F(0),
                        )
                        for rule, h in enumerate(forecasts):
                            risk = score(p, h)
                            sums[actual][assumed][rule] += weight * mass * risk
                            if literal and actual == 0:
                                require(risk <= cg, "unchanged clean nonpositive excess")
                            if literal and actual == 3:
                                require(
                                    risk - cg == fraction(WEIGHTS[rule]) ** 2 * distance,
                                    "tilted weighted quadratic penalty cell",
                                )
        worlds = []
        for actual in range(4):
            models = []
            for assumed in range(4):
                require(sums[actual][assumed][0] == coarse[actual], "same-actual coarse risk")
                models.append(
                    {
                        "assumed_index": assumed,
                        "forecast_risks": [wire(r) for r in sums[actual][assumed]],
                    }
                )
            worlds.append(
                {"actual_index": actual, "coarse_risk": wire(coarse[actual]), "models": models}
            )
        output.append({"mechanism_id": mechanism["mechanism_id"], "worlds": worlds})
    return output


def project_case(aacase, zcase, laws):
    require_same_wire(aacase["case_id"], zcase["case_id"], "nominal case identity")
    require_same_wire(aacase["problem"], nominal_problem(zcase), "nominal input from unchanged Z")
    evidence = build_stress_laws(zcase, laws)
    problem = {
        "schema_version": "det8-qr05ab-problem-v1",
        "family": "qr05ab_replacement_stress",
        "nominal": copy.deepcopy(aacase["problem"]),
        "mechanisms": score_stress(zcase, evidence),
    }
    return {"case_id": aacase["case_id"], "problem": problem, "stress_laws": evidence}


def expected_analysis(problem):
    """Independent all-world enumeration; never takes a stressed argmin."""
    baseline = nominal_expected(problem["nominal"])
    output = []
    old_evaluations = 0
    for source in problem["mechanisms"]:
        worlds = copy.deepcopy(source["worlds"])
        for world in worlds:
            coarse = fraction(world["coarse_risk"])
            for model in world["models"]:
                model["excess_risks"] = [
                    wire(fraction(r) - coarse) for r in model["forecast_risks"]
                ]
        certificates = []
        for assumed in range(4):
            for bound in range(4):
                previous = baseline["decisions"][4 * assumed + bound]
                old = previous["minimizer_indices"]
                original = fraction(previous["minimax_excess"])
                indices = list(range(bound + 1))
                candidates = []
                for rule, weight in enumerate(WEIGHTS):
                    values = [
                        fraction(worlds[t]["models"][assumed]["excess_risks"][rule])
                        for t in indices
                    ]
                    worst = max(values)
                    nominal = fraction(previous["candidates"][rule]["worst_excess"])
                    maximizers = [t for t, v in zip(indices, values, strict=True) if v == worst]
                    unsafe = [t for t, v in zip(indices, values, strict=True) if v > 0]
                    breaking = [t for t, v in zip(indices, values, strict=True) if v > original]
                    candidates.append(
                        {
                            "retained_weight": copy.deepcopy(weight),
                            "world_excesses": [wire(v) for v in values],
                            "worst_excess": wire(worst),
                            "worst_world_indices": maximizers,
                            "nominal_worst_excess": wire(nominal),
                            "worst_shift": wide(worst - nominal),
                            "bound_excess": wide(worst - original),
                            "nominal_minimizer": rule in old,
                            "coarse_safe": worst <= 0,
                            "strict_benefit": worst < 0,
                            "original_bound_preserved": worst <= original,
                            "unsafe_world_indices": unsafe,
                            "bound_breaking_world_indices": breaking,
                        }
                    )
                safe = [i for i in old if candidates[i]["coarse_safe"]]
                strict = [i for i in old if candidates[i]["strict_benefit"]]
                preserved = [i for i in old if candidates[i]["original_bound_preserved"]]
                unsafe = [i for i in old if not candidates[i]["coarse_safe"]]
                breaking = [i for i in old if not candidates[i]["original_bound_preserved"]]
                old_evaluations += len(old)
                require(
                    old and candidates[0]["worst_excess"] == [0, 1],
                    "frozen selection nonempty / coarse zero",
                )
                certificates.append(
                    {
                        "assumed_index": assumed,
                        "bound_index": bound,
                        "world_indices": indices,
                        "nominal_minimax_excess": copy.deepcopy(previous["minimax_excess"]),
                        "old_minimizer_indices": copy.deepcopy(old),
                        "old_minimizer_weights": copy.deepcopy(previous["minimizer_weights"]),
                        "candidates": candidates,
                        "safe_old_indices": safe,
                        "strictly_beneficial_old_indices": strict,
                        "bound_preserving_old_indices": preserved,
                        "unsafe_old_indices": unsafe,
                        "bound_breaking_old_indices": breaking,
                        "all_old_safe": len(safe) == len(old),
                        "any_old_safe": bool(safe),
                        "all_old_strict": len(strict) == len(old),
                        "any_old_strict": bool(strict),
                        "all_old_bound_preserved": len(preserved) == len(old),
                        "any_old_bound_preserved": bool(preserved),
                        "checks": dict.fromkeys(AB_CHECKS, True),
                    }
                )
        output.append(
            {"mechanism_id": source["mechanism_id"], "worlds": worlds, "certificates": certificates}
        )
    counts = {
        "mechanisms": 2,
        "worlds": 8,
        "assumed_models": 8,
        "rules": 6,
        "certificates": 32,
        "candidate_certificates": 96,
        "old_rule_evaluations": old_evaluations,
        "stress_risk_cells": 96,
        "baseline_decision_work": 216,
        "stress_excess_terms": 96,
        "candidate_world_visits": 240,
        "shift_terms": 192,
        "candidate_classification_visits": 96,
        "total_work_terms": 840,
    }
    return {
        "input_sha256": digest(canonical(problem)),
        "baseline": baseline,
        "mechanisms": output,
        "counts": counts,
    }


def verify_stress_family(analysis, aacase, zcase, laws, evidence):
    # Whole replacement-law origin is checked by fixtures/replacement_laws and
    # raw audit; here the full supplied law evidence must match that fixed map.
    require_same_wire(
        evidence, build_stress_laws(zcase, laws), "complete independently reconstructed tilted laws"
    )
    literal = score_stress(zcase, evidence, literal=True)
    for m, computed in zip(analysis["mechanisms"], literal, strict=True):
        for world, source in zip(m["worlds"], computed["worlds"], strict=True):
            require_same_wire(
                world["coarse_risk"], source["coarse_risk"], "literal coarse case risk"
            )
            for row, original in zip(world["models"], source["models"], strict=True):
                require_same_wire(
                    row["forecast_risks"],
                    original["forecast_risks"],
                    "literal original-weight frozen forecast risks",
                )
    nominal = analysis["baseline"]
    for bid, original in enumerate(zcase["problem"]["experiment"]["beliefs"]):
        old = [joint(ch) for ch in original["channels"]]
        actual = [[joint(ch) for ch in m["beliefs"][bid]["channels"]] for m in evidence]
        for mechanism in range(2):
            require(actual[mechanism][0] == old[0], "complete clean joint recovery")
            for t in range(4):
                require(
                    n_subjoints(actual[mechanism][t]) == n_subjoints(old[t]),
                    "complete N/future marginal preservation",
                )
                require(
                    {z for z, _ in actual[mechanism][t]} == {z for z, _ in old[t]},
                    "same positive report support",
                )
                atoms = (
                    actual[mechanism][0].keys()
                    | actual[mechanism][3].keys()
                    | actual[mechanism][t].keys()
                )
                rate = fraction(LEVELS[t])
                require(
                    all(
                        actual[mechanism][t].get(key, F(0))
                        == (1 - rate) * actual[mechanism][0].get(key, F(0))
                        + rate * actual[mechanism][3].get(key, F(0))
                        for key in atoms
                    ),
                    "affine full stressed joint",
                )
        for t in range(4):
            atoms = old[t].keys() | actual[0][t].keys() | actual[1][t].keys()
            require(
                all(
                    (actual[0][t].get(key, F(0)) + actual[1][t].get(key, F(0))) / 2
                    == old[t].get(key, F(0))
                    for key in atoms
                ),
                "opposite JOINT midpoint, not conditional posterior average",
            )
    for assumed in range(4):
        for rule in range(3):
            curves = []
            for mechanism in analysis["mechanisms"]:
                risks = [
                    fraction(w["models"][assumed]["forecast_risks"][rule])
                    for w in mechanism["worlds"]
                ]
                coarse = [fraction(w["coarse_risk"]) for w in mechanism["worlds"]]
                excess = [r - g for r, g in zip(risks, coarse, strict=True)]
                require_same_wire(
                    [wire(g) for g in coarse],
                    [w["coarse_risk"] for w in nominal["worlds"]],
                    "coarse risk unchanged",
                )
                for t, level in enumerate(LEVELS):
                    rate = fraction(level)
                    require(
                        risks[t] == (1 - rate) * risks[0] + rate * risks[3],
                        "affine original-law risk",
                    )
                require(
                    all(a <= b for a, b in itertools.pairwise(excess)),
                    "stressed excess nondecreasing",
                )
                for bound in range(4):
                    cert = mechanism["certificates"][4 * assumed + bound]
                    cand = cert["candidates"][rule]
                    require(
                        bound in cand["worst_world_indices"]
                        and fraction(cand["worst_excess"]) == excess[bound],
                        "upper endpoint remains worst",
                    )
                curves.append(risks)
            for t in range(4):
                require(
                    (curves[0][t] + curves[1][t]) / 2
                    == fraction(nominal["worlds"][t]["models"][assumed]["forecast_risks"][rule]),
                    "opposite risk midpoint nominal",
                )
            for bound in range(4):
                old = nominal["decisions"][4 * assumed + bound]
                one, two = [m["certificates"][4 * assumed + bound] for m in analysis["mechanisms"]]
                require(
                    (
                        fraction(one["candidates"][rule]["worst_excess"])
                        + fraction(two["candidates"][rule]["worst_excess"])
                    )
                    / 2
                    == fraction(old["candidates"][rule]["worst_excess"]),
                    "opposite worst-risk midpoint under upper-endpoint control",
                )
                if rule in old["minimizer_indices"]:
                    left, right = (F(*c["candidates"][rule]["bound_excess"]) for c in (one, two))
                    require(left + right == 0, "opposite old-bound deviations cancel")
                    require(
                        (left <= 0 and right <= 0) == (left == 0 and right == 0),
                        "both original bounds preserved iff exact",
                    )
    return literal


def producer_controls(analysis, aacase, zcase, laws, evidence):
    require_same_wire(
        aacase["analysis"], nominal_expected(aacase["problem"]), "complete nominal AA analysis"
    )
    require_same_wire(
        analysis["baseline"], aacase["analysis"], "entire nominal AA baseline retained"
    )
    nominal_check(analysis["baseline"], zcase)
    verify_stress_family(analysis, aacase, zcase, laws, evidence)
    return {
        **dict.fromkeys(
            (
                "nominal_AA_baseline_preserved",
                "whole_model_positive_rank_tilts",
                "complete_stressed_laws_and_support",
                "frozen_forecasts_and_weights",
                "literal_original_weight_risks",
                "clean_and_N_future_marginals_preserved",
                "affine_actual_joint_and_risk",
                "opposite_tilts_average_to_nominal",
                "full_replacement_tilted_quadratic_penalty",
                "upper_endpoint_and_opposite_bound_deviations",
                "all_original_ties_classified_without_reoptimization",
            ),
            True,
        ),
        "origin_authenticated_by_generic_API": False,
        "raw_history_reconstruction_performed_by_this_runner": False,
    }


def check_analysis(analysis, aacase, zcase, laws, evidence):
    projected = project_case(aacase, zcase, laws)
    require_same_wire(evidence, projected["stress_laws"], "entire retained actual-law evidence")
    require_same_wire(
        analysis,
        expected_analysis(projected["problem"]),
        "independent complete frozen-certificate output",
    )
    return producer_controls(analysis, aacase, zcase, laws, evidence)


def run_suite():
    data = fixtures()
    laws = replacement_laws(data["w"])
    primary = load("qr05ab_primary", "stress.py")
    reference = load("qr05ab_reference", "reference_qr05ab.py")
    cases = []
    for aa, z in zip(data["aa"]["cases"], data["z"]["cases"], strict=True):
        case = project_case(aa, z, laws)
        problem = case["problem"]
        before = canonical(problem)
        left = primary.analyze(problem)
        require(canonical(problem) == before, "primary input mutation")
        right = reference.analyze(problem)
        require(canonical(problem) == before, "reference input mutation")
        require_same_wire(left, right, "independent frozen-certificate engines")
        controls = check_analysis(left, aa, z, laws, case["stress_laws"])
        cases.append({**case, "analysis": left, "producer_controls": controls})
    bad = []
    p = copy.deepcopy(cases[0]["problem"])
    p["extra"] = 0
    bad.append(p)
    p = copy.deepcopy(cases[0]["problem"])
    p["nominal"]["worlds"].pop()
    bad.append(p)
    p = copy.deepcopy(cases[0]["problem"])
    p["mechanisms"].reverse()
    bad.append(p)
    p = copy.deepcopy(cases[0]["problem"])
    p["mechanisms"][0]["worlds"][0]["actual_index"] = False
    bad.append(p)
    p = copy.deepcopy(cases[0]["problem"])
    p["mechanisms"][0]["worlds"][0]["models"][0]["forecast_risks"][0] = [2, 1]
    bad.append(p)
    p = copy.deepcopy(cases[0]["problem"])
    p["mechanisms"][1]["worlds"][0]["coarse_risk"] = 0.5
    bad.append(p)
    p = copy.deepcopy(cases[0]["problem"])
    p["mechanisms"][0]["metadata"] = "unknown"
    bad.append(p)
    p = copy.deepcopy(cases[0]["problem"])
    p["nominal"]["levels"].reverse()
    bad.append(p)
    rejected = 0
    for engine in (primary, reference):
        for invalid in bad:
            try:
                engine.analyze(invalid)
            except ValueError:
                rejected += 1
            else:
                raise ValueError("malformed public wrapper accepted")
    require(rejected == 16, "all malformed public controls")
    totals = {
        "cases": len(cases),
        "analyze_calls": 2 * len(cases),
        "invalid_analyze_calls_rejected": rejected,
    }
    for key in cases[0]["analysis"]["counts"]:
        totals[key] = sum(c["analysis"]["counts"][key] for c in cases)
    return {
        "producer": {"artifact": AA_PRIOR, "bytes": AA_BYTES, "sha256": AA_SHA},
        "replacement_laws": laws,
        "cases": cases,
        "independent_route_equal": True,
        "public_controls": {
            "analyze_calls": 12,
            "invalid_analyze_calls_rejected": 16,
            "raw_laws_histories_or_artifacts_given_to_core": False,
            "forecasts_refitted": False,
            "stressed_rules_reoptimized": False,
            "old_ties_selected_retrospectively": False,
            "mechanisms_combined": False,
        },
        "totals": totals,
    }


if __name__ == "__main__":
    main()
