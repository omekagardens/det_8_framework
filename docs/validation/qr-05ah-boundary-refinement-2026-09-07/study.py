"""QR-05AH private supplied-geometry producer and exact record-local comparison.

Coordinates/full orders remain private to the producer and independent auditor.
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
SCHEMA = "det8-qr05ah-results-v1"
BASE_COMMIT = "f603b02ffba1d6965695eb13e572ad554f7d1827"
SOURCES = (
    "README.md",
    "certificate.py",
    "reference_qr05ah.py",
    "study.py",
    "test_qr05ah.py",
    "test_capture.py",
    "audit_json.py",
)
AD_PRIOR = "qr-05ad-continuous-retention-2026-09-07/results.json"
AD_BYTES = 5003206
AD_SHA = "099c9df18db91545fdd3a08a383e2e4ed96bf5734f6b80a9e492c3bc954c611a"
AC_PRIOR = "qr-05ac-replacement-envelope-2026-09-07/results.json"
AC_BYTES = 1783649
AC_SHA = "3fc5a502c214ba408e5f539133156b0ad81a2ef243545645dc980e7936932c18"
AB_PRIOR = "qr-05ab-replacement-stress-2026-09-07/results.json"
AB_BYTES = 1805554
AB_SHA = "7cbe2668d5b022f73207502bab214078b911e25d25a3826918b916e967643009"
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

AE_PRIOR = "qr-05ae-history-safety-2026-09-07/results.json"
AE_SHA = "5b7946512ea77e076387a25d5cf46c30d25a42d37fdd66ae39a4edadb179bbde"

AF_PRIOR = "qr-05af-local-geometry-2026-09-07/results.json"
AF_SHA = "8a823b6253d4862bcea8f774f7d46278b288186a0361f38b39cdefd18974d7a3"

AG_PRIOR = "qr-05ag-local-volume-2026-09-07/results.json"
AG_SHA = "5af957be534af3096c7f61ec444349ec49c739ebf70364146b7f4568a8832f91"
AGDIR = HERE.parent / "qr-05ag-local-volume-2026-09-07"

PRIORS = {
    AG_PRIOR: AG_SHA,
    AF_PRIOR: AF_SHA,
    AE_PRIOR: AE_SHA,
    AD_PRIOR: AD_SHA,
    AC_PRIOR: AC_SHA,
    AB_PRIOR: AB_SHA,
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
    require(path.stat().st_size <= MAX_CAPTURE_BYTES, "input artifact byte cap")
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
    ag_sources()
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
    safely above valid AF schemas, including evidence envelopes.
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
        if type(item) is str:
            require(len(item) <= MAX_WORKING_BYTES, "wire string exceeds working byte cap")
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
    raw = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()
    require(len(raw) <= MAX_WORKING_BYTES, "serialized wire exceeds working byte cap")
    return raw


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


METHODS = ("raw", "uniform_rate", "inclusion")
PACKET_SCOPE = (
    "missing_marks_inferred",
    "source_moments_inferred",
    "geometry_inferred",
    "mark_origin_authenticated",
    "observation_origin_authenticated",
)
CERT_SCOPE = (
    "observer_has_geometry",
    "marks_authenticated",
    "unknown_geometry_reconstructed",
    "monotone_absolute_error_guaranteed",
    "continuum_limit_established",
    "gravity_derived",
)
SUITE_SCOPE = (
    "unknown_geometry_reconstructed",
    "continuum_limit_established",
    "marks_authenticated",
    "observer_bounds_inferred",
    "monotone_absolute_error_guaranteed",
    "cross_level_observation_transport_proved",
    "quantum_channel_constructed",
    "gravity_derived",
    "empirical_data_used",
    "ret_integration_tested",
)
FAMILIES = ("grid", "warp", "warp_stale", "boost", "dilate")
LEVELS = ("l0", "l1", "l2")


def fraction(value):
    require(type(value) is list and len(value) == 2, "fraction pair")
    a, b = value
    require(type(a) is int and type(b) is int and b > 0, "exact rational components")
    result = F(a, b)
    require([result.numerator, result.denominator] == value, "reduced rational")
    return result


def wire(value):
    result = F(value)
    require(
        max(abs(result.numerator).bit_length(), result.denominator.bit_length()) <= 4096,
        "retained rational component bound",
    )
    return [result.numerator, result.denominator]


def vector(values):
    return [wire(x) for x in values]


def matrix(values):
    return [vector(row) for row in values]


def marginals(masses, m):
    return [sum((p for s, p in enumerate(masses) if s & (1 << i)), F(0)) for i in range(m)]


def packet_oracle(problem):
    """Literal retained-record oracle: no source geometry or absent marks."""
    eligible = problem["eligible"]
    kept = problem["record"]["kept"]
    past = problem["record"]["past"]
    lookup = {event: pos for pos, event in enumerate(kept)}
    m = len(eligible)
    masses = [fraction(p) for p in problem["mask_probabilities"]]
    pi = marginals(masses, m)
    pbar = sum(pi, F(0)) / m
    require(all(p > 0 for p in pi), "positive marginals")
    marks = {row["event"]: fraction(row["volume"]) for row in problem["record"]["marks"]}
    mask = sum(1 << i for i, event in enumerate(eligible) if event in kept)
    questions = []
    for probe in problem["probes"]:
        a, b = lookup[probe["source"]], lookup[probe["target"]]
        members = [
            event
            for event in eligible
            if event in marks and a in past[lookup[event]] and lookup[event] in past[b]
        ]
        estimates = {}
        for method in METHODS:
            value = sum(
                (
                    marks[event]
                    * (
                        1
                        if method == "raw"
                        else 1 / pbar
                        if method == "uniform_rate"
                        else 1 / pi[eligible.index(event)]
                    )
                    for event in members
                ),
                F(0),
            )
            estimates[method] = wire(value)
        questions.append(
            {
                "probe": probe["name"],
                "observed_cells": [
                    {
                        "event": event,
                        "volume": wire(marks[event]),
                        "inclusion": wire(pi[eligible.index(event)]),
                    }
                    for event in members
                ],
                "estimates": estimates,
            }
        )
    L = 1 << m
    I = m * (1 << (m - 1))
    P = len(questions)
    K = len(marks)
    C = P * K
    A = sum(len(q["observed_cells"]) for q in questions)
    return {
        "input_sha256": digest(canonical(problem)),
        "mask": mask,
        "probability": wire(masses[mask]),
        "possible": masses[mask] > 0,
        "marginals": vector(pi),
        "questions": questions,
        "counts": {
            "events": problem["frame_size"],
            "eligible_events": m,
            "kept_events": len(kept),
            "retained_cells": K,
            "mask_rows": L,
            "questions": P,
            "inclusion_terms": I,
            "member_candidates": C,
            "observed_member_terms": A,
            "estimator_terms": 3 * A,
            "reserved_estimator_terms": 3 * C,
            "reserved_total_work": L + I + 4 * C + 3 * P,
            "total_work": L + I + C + 3 * A + 3 * P,
        },
        "scope": dict.fromkeys(PACKET_SCOPE, False),
    }


def make_packet(source, design, mask):
    kept = sorted(
        source["fixed"] + [v for i, v in enumerate(source["eligible"]) if mask & (1 << i)]
    )
    lookup = {event: i for i, event in enumerate(kept)}
    return {
        "schema_version": "det8-qr05ag-problem-v1",
        "family": "qr05ag_local_volume",
        "frame_size": len(source["past"]),
        "fixed": copy.deepcopy(source["fixed"]),
        "eligible": copy.deepcopy(source["eligible"]),
        "probes": copy.deepcopy(source["probes"]),
        "mask_probabilities": copy.deepcopy(design["mask_probabilities"]),
        "record": {
            "kept": kept,
            "past": [[lookup[p] for p in source["past"][event] if p in lookup] for event in kept],
            "marks": [
                {"event": c["event"], "volume": copy.deepcopy(c["supplied_mark"])}
                for c in source["cells"]
                if c["event"] in lookup
            ],
        },
    }


def population(source):
    result = []
    coords = [[fraction(x) for x in p] for p in source["coordinates"]]
    for probe in source["probes"]:
        a, b = probe["source"], probe["target"]
        members = [
            c["event"]
            for c in source["cells"]
            if a in source["past"][c["event"]] and c["event"] in source["past"][b]
        ]
        T = sum(
            (fraction(c["supplied_mark"]) for c in source["cells"] if c["event"] in members), F(0)
        )
        G = sum(
            (fraction(c["geometric_mark"]) for c in source["cells"] if c["event"] in members), F(0)
        )
        au, av = coords[a]
        bu, bv = coords[b]
        V = (bu - au) * (bv - av) / 2
        overlaps = []
        for cell in source["cells"]:
            ul, uh, vl, vh = map(fraction, cell["bounds"])
            area = max(F(0), min(uh, bu) - max(ul, au)) * max(F(0), min(vh, bv) - max(vl, av)) / 2
            overlaps.append({"event": cell["event"], "volume": wire(area)})
        require(
            sum((fraction(x["volume"]) for x in overlaps), F(0)) == V,
            "partition clips recover continuum",
        )
        result.append(
            {
                "probe": probe["name"],
                "members": members,
                "supplied_target": wire(T),
                "geometric_target": wire(G),
                "continuum_volume": wire(V),
                "annotation_error": wire(T - G),
                "quadrature_error": wire(G - V),
                "overlaps": overlaps,
            }
        )
    return result


def moments(pop, samples):
    P = len(pop)
    probabilities = [fraction(s["analysis"]["probability"]) for s in samples]
    result = {}
    for method in METHODS:
        rows = [
            [fraction(q["estimates"][method]) for q in s["analysis"]["questions"]] for s in samples
        ]
        means = [
            sum((p * row[i] for p, row in zip(probabilities, rows, strict=True)), F(0))
            for i in range(P)
        ]
        cov = [
            [
                sum(
                    (
                        p * (row[i] - means[i]) * (row[j] - means[j])
                        for p, row in zip(probabilities, rows, strict=True)
                    ),
                    F(0),
                )
                for j in range(P)
            ]
            for i in range(P)
        ]
        second = [
            [
                sum((p * row[i] * row[j] for p, row in zip(probabilities, rows, strict=True)), F(0))
                - means[i] * means[j]
                for j in range(P)
            ]
            for i in range(P)
        ]
        require(cov == second, "centered and second moments agree")
        biases = []
        decompositions = []
        for q, mean in zip(pop, means, strict=True):
            T, G, V = map(
                fraction, [q["supplied_target"], q["geometric_target"], q["continuum_volume"]]
            )
            bias = mean - T
            annotation = T - G
            quadrature = G - V
            total = mean - V
            require(total == bias + annotation + quadrature, "three signed errors")
            biases.append(bias)
            decompositions.append(
                {
                    "probe": q["probe"],
                    "mean": wire(mean),
                    "finite_target": wire(T),
                    "true_finite_target": wire(G),
                    "continuum": wire(V),
                    "sampling_bias": wire(bias),
                    "annotation_error": wire(annotation),
                    "quadrature_error": wire(quadrature),
                    "total_error": wire(total),
                }
            )
        result[method] = {
            "mean": vector(means),
            "bias": vector(biases),
            "covariance": matrix(cov),
            "decompositions": decompositions,
        }
    return result


def covariance_oracle(source, pop, design):
    masses = list(map(fraction, design["mask_probabilities"]))
    eligible = source["eligible"]
    pi = marginals(masses, len(eligible))
    idx = {event: i for i, event in enumerate(eligible)}
    weights = {c["event"]: fraction(c["supplied_mark"]) for c in source["cells"]}
    pair = zero = 0
    matrix_out = []
    for q in pop:
        row = []
        for r in pop:
            value = F(0)
            for i, j in itertools.product(q["members"], r["members"]):
                pair += 1
                support = (1 << idx[i]) | (1 << idx[j])
                joint = sum((p for mask, p in enumerate(masses) if mask & support == support), F(0))
                zero += joint == 0
                value += weights[i] * weights[j] * (joint / (pi[idx[i]] * pi[idx[j]]) - 1)
            row.append(value)
        matrix_out.append(row)
    return matrix(matrix_out), pair, zero


def area(bounds):
    ul, uh, vl, vh = bounds
    return (uh - ul) * (vh - vl) / 2


def contains(outer, inner):
    return (
        outer[0] <= inner[0] < inner[1] <= outer[1] and outer[2] <= inner[2] < inner[3] <= outer[3]
    )


def overlap(a, b):
    return (
        max(F(0), min(a[1], b[1]) - max(a[0], b[0]))
        * max(F(0), min(a[3], b[3]) - max(a[2], b[2]))
        / 2
    )


def certificate_oracle(problem):
    """Literal supplied-geometry oracle; never called with observer-only access."""
    domain = list(map(fraction, problem["domain"]))
    P = len(problem["probes"])
    output = []
    refinements = []
    previous = None
    for lev in problem["levels"]:
        cells = [
            {
                **c,
                "bounds": list(map(fraction, c["bounds"])),
                "representative": list(map(fraction, c["representative"])),
                "volume": fraction(c["volume"]),
            }
            for c in lev["cells"]
        ]
        require(all(contains(domain, c["bounds"]) for c in cells), "contained partition")
        require(
            all(
                overlap(a["bounds"], b["bounds"]) == 0 for a, b in itertools.combinations(cells, 2)
            ),
            "disjoint partition",
        )
        require(sum((area(c["bounds"]) for c in cells), F(0)) == area(domain), "complete partition")
        questions = []
        for probe in problem["probes"]:
            q = list(map(fraction, probe["bounds"]))
            inner = [c for c in cells if contains(q, c["bounds"])]
            outer = [c for c in cells if overlap(q, c["bounds"]) > 0]
            selected = [
                c
                for c in cells
                if q[0] < c["representative"][0] < q[1] and q[2] < c["representative"][1] < q[3]
            ]
            L = sum((area(c["bounds"]) for c in inner), F(0))
            U = sum((area(c["bounds"]) for c in outer), F(0))
            G = sum((area(c["bounds"]) for c in selected), F(0))
            T = sum((c["volume"] for c in selected), F(0))
            V = area(q)
            require(L <= G <= U and L <= V <= U, "two geometric sandwiches")
            questions.append(
                {
                    "probe": probe["name"],
                    "inner_cells": [c["name"] for c in inner],
                    "outer_cells": [c["name"] for c in outer],
                    "representative_cells": [c["name"] for c in selected],
                    **{
                        k: wire(v)
                        for k, v in {
                            "lower_bound": L,
                            "upper_bound": U,
                            "boundary_gap": U - L,
                            "geometric_target": G,
                            "supplied_target": T,
                            "continuum_volume": V,
                            "annotation_error": T - G,
                            "quadrature_error": G - V,
                            "total_error": T - V,
                            "error_lower": G - U,
                            "error_upper": G - L,
                        }.items()
                    },
                }
            )
        level_out = {
            "name": lev["name"],
            "cells": [
                {
                    "name": c["name"],
                    "geometric_volume": wire(area(c["bounds"])),
                    "annotation_error": wire(c["volume"] - area(c["bounds"])),
                }
                for c in cells
            ],
            "questions": questions,
        }
        if previous is not None:
            parent_cells, prior_level = previous
            parents = []
            for parent in parent_cells:
                children = [c for c in cells if c["parent"] == parent["name"]]
                require(
                    children and all(contains(parent["bounds"], c["bounds"]) for c in children),
                    "parent containment",
                )
                require(
                    sum((area(c["bounds"]) for c in children), F(0)) == area(parent["bounds"]),
                    "parent geometric coverage",
                )
                require(
                    sum((c["volume"] for c in children), F(0)) == parent["volume"],
                    "parent mark additivity",
                )
                parents.append(
                    {
                        "parent": parent["name"],
                        "children": [c["name"] for c in children],
                        "geometric_volume": wire(area(parent["bounds"])),
                        "supplied_volume": wire(parent["volume"]),
                    }
                )
            changes = []
            for q, r in zip(prior_level["questions"], questions, strict=True):
                gains = {
                    k: value
                    for k, value in (
                        ("lower_gain", fraction(r["lower_bound"]) - fraction(q["lower_bound"])),
                        ("upper_drop", fraction(q["upper_bound"]) - fraction(r["upper_bound"])),
                        ("gap_drop", fraction(q["boundary_gap"]) - fraction(r["boundary_gap"])),
                    )
                }
                require(all(v >= 0 for v in gains.values()), "nested enclosure")
                gains["quadrature_error_change"] = fraction(r["quadrature_error"]) - fraction(
                    q["quadrature_error"]
                )
                gains["absolute_error_change"] = abs(fraction(r["quadrature_error"])) - abs(
                    fraction(q["quadrature_error"])
                )
                changes.append({"probe": q["probe"], **{k: wire(v) for k, v in gains.items()}})
            refinements.append(
                {
                    "coarse": prior_level["name"],
                    "fine": lev["name"],
                    "parents": parents,
                    "questions": changes,
                }
            )
        output.append(level_out)
        previous = cells, level_out
    Cs = [len(l["cells"]) for l in problem["levels"]]
    T = sum(c * (2 * c + 1) ** 2 for c in Cs)
    D = sum(c * (c - 1) // 2 for c in Cs)
    Q = P * sum(Cs)
    R = sum(Cs[1:])
    return {
        "input_sha256": digest(canonical(problem)),
        "domain_volume": wire(area(domain)),
        "levels": output,
        "refinements": refinements,
        "counts": {
            "levels": len(Cs),
            "cells": sum(Cs),
            "probes": P,
            "tile_checks": T,
            "pair_checks": D,
            "query_cell_terms": Q,
            "refinement_links": R,
            "total_work": T + D + 3 * Q + R,
        },
        "scope": dict.fromkeys(CERT_SCOPE, False),
    }


def base_levels():
    cells = {
        f"c_{i}_{j}": (F(i, 3), F(i + 1, 3), F(j, 2), F(j + 1, 2))
        for i, j in itertools.product(range(3), range(2))
    }
    levels = [[(name, None, b) for name, b in sorted(cells.items())]]
    del cells["c_1_0"]
    cells.update(
        {"c_1_0_l": (F(1, 3), F(1, 2), F(0), F(1, 2)), "c_1_0_r": (F(1, 2), F(2, 3), F(0), F(1, 2))}
    )
    levels.append(
        [
            (name, "c_1_0" if name in ("c_1_0_l", "c_1_0_r") else name, b)
            for name, b in sorted(cells.items())
        ]
    )
    del cells["c_1_0_l"]
    cells.update(
        {
            "c_1_0_lb": (F(1, 3), F(1, 2), F(0), F(1, 4)),
            "c_1_0_lt": (F(1, 3), F(1, 2), F(1, 4), F(1, 2)),
        }
    )
    levels.append(
        [
            (name, "c_1_0_l" if name in ("c_1_0_lb", "c_1_0_lt") else name, b)
            for name, b in sorted(cells.items())
        ]
    )
    return levels


def transform(name, u, v):
    if name in ("warp", "warp_stale"):
        return u * u, v * v
    if name == "boost":
        return 2 * u, v / 2
    if name == "dilate":
        return 2 * u, 2 * v
    require(name == "grid", "fixed source")
    return u, v


def base_markers():
    return {
        "bottom": (F(0), F(0)),
        "aligned": (F(2, 3), F(1, 2)),
        "unaligned": (F(3, 5), F(2, 5)),
        "top": (F(1), F(1)),
    }


PROBE_LABELS = (
    ("whole", "bottom", "top"),
    ("lower_aligned", "bottom", "aligned"),
    ("upper_aligned", "aligned", "top"),
    ("lower_unaligned", "bottom", "unaligned"),
    ("upper_unaligned", "unaligned", "top"),
)


def certificate_problem(name):
    levels = []
    for level, rows in zip(LEVELS, base_levels(), strict=True):
        cells = []
        for label, parent, b in rows:
            ul, vl = transform(name, b[0], b[2])
            uh, vh = transform(name, b[1], b[3])
            bounds = [ul, uh, vl, vh]
            rep = transform(name, (b[0] + b[1]) / 2, (b[2] + b[3]) / 2)
            cells.append(
                {
                    "name": label,
                    "parent": parent,
                    "bounds": vector(bounds),
                    "representative": vector(rep),
                    "volume": wire(area(b) if name == "warp_stale" else area(bounds)),
                }
            )
        levels.append({"name": level, "cells": cells})
    markers = {label: transform(name, *point) for label, point in base_markers().items()}
    probes = []
    for label, a, b in PROBE_LABELS:
        probes.append(
            {
                "name": label,
                "bounds": vector([markers[a][0], markers[b][0], markers[a][1], markers[b][1]]),
            }
        )
    domain = probes[0]["bounds"]
    return {
        "schema_version": "det8-qr05ah-problem-v1",
        "family": "qr05ah_partition_bounds",
        "domain": copy.deepcopy(domain),
        "probes": probes,
        "levels": levels,
    }


def label_ids(level):
    points = base_markers()
    for name, _parent, b in base_levels()[level]:
        points[name] = ((b[0] + b[1]) / 2, (b[2] + b[3]) / 2)
    labels = sorted(points, key=lambda label: (sum(points[label]), *points[label], label))
    return {label: i for i, label in enumerate(labels)}


def make_source(name, level=0):
    require(type(level) is int and 0 <= level < 3, "fixed level")
    problem = certificate_problem(name)
    ids = label_ids(level)
    points = {label: transform(name, *p) for label, p in base_markers().items()}
    cells = []
    for cell in problem["levels"][level]["cells"]:
        label = cell["name"]
        b = list(map(fraction, cell["bounds"]))
        points[label] = tuple(map(fraction, cell["representative"]))
        cells.append(
            {
                "event": ids[label],
                "bounds": copy.deepcopy(cell["bounds"]),
                "geometric_mark": wire(area(b)),
                "supplied_mark": copy.deepcopy(cell["volume"]),
            }
        )
    coordinates = [None] * len(ids)
    for label, p in points.items():
        coordinates[ids[label]] = p
    tx = [((u + v) / 2, (u - v) / 2) for u, v in coordinates]
    past = [
        [i for i in range(j) if tx[j][0] - tx[i][0] > abs(tx[j][1] - tx[i][1])]
        for j in range(len(tx))
    ]
    return {
        "name": name,
        "coordinates": [vector(p) for p in coordinates],
        "past": past,
        "fixed": sorted(ids[x] for x in base_markers()),
        "eligible": sorted(c["event"] for c in cells),
        "probes": [{"name": q, "source": ids[a], "target": ids[b]} for q, a, b in PROBE_LABELS],
        "cells": sorted(cells, key=lambda c: c["event"]),
        "mark_kind": "stale_base" if name == "warp_stale" else "geometric_cell_volume",
    }


def design_law(name, m):
    require(
        1 <= m <= 8 and name in ("identity", "iid_half", "singleton"), "declared observation law"
    )
    masses = [
        F(mask == (1 << m) - 1)
        if name == "identity"
        else F(1, 1 << m)
        if name == "iid_half"
        else F(1, m)
        if mask.bit_count() == 1
        else F(0)
        for mask in range(1 << m)
    ]
    require(sum(masses, F(0)) == 1, "normalized observation law")
    return {"name": name, "mask_probabilities": vector(masses)}


def build_case(name, level, design_name, engines=None):
    source = make_source(name, level)
    design = design_law(design_name, len(source["eligible"]))
    pop = population(source)
    samples = []
    for mask in range(1 << len(source["eligible"])):
        packet = make_packet(source, design, mask)
        expected = packet_oracle(packet)
        if engines is not None:
            for engine in engines:
                engine_input = copy.deepcopy(packet)
                before_input = canonical(engine_input)
                actual = engine.analyze(engine_input)
                require(canonical(engine_input) == before_input, "public input mutated")
                require_same_wire(actual, expected, "complete public marked-volume output")
        samples.append({"problem": packet, "analysis": expected})
    mm = moments(pop, samples)
    cov, pairs, zero = covariance_oracle(source, pop, design)
    require_same_wire(cov, mm["inclusion"]["covariance"], "source inclusion covariance")
    require(all(x == [0, 1] for x in mm["inclusion"]["bias"]), "supported linear means")
    return {
        "case_id": name + "__" + LEVELS[level] + "__" + design_name,
        "level": LEVELS[level],
        "source": source,
        "design": design,
        "population": pop,
        "samples": samples,
        "moments": mm,
        "joint_covariance": cov,
        "counts": {
            "events": len(source["past"]),
            "eligible_events": len(source["eligible"]),
            "mask_rows": len(samples),
            "positive_rows": sum(s["analysis"]["possible"] for s in samples),
            "questions": len(pop),
            "source_member_terms": sum(len(q["members"]) for q in pop),
            "observed_member_terms": sum(
                s["analysis"]["counts"]["observed_member_terms"] for s in samples
            ),
            "ordered_cell_pairs": pairs,
            "zero_joint_pairs": zero,
            "packet_calls": 2 * len(samples),
        },
    }


def same(a, b):
    require_wire(a)
    require_wire(b)
    return canonical(a) == canonical(b)


def positive_packet_law(case):
    return [
        {"problem": s["problem"], "probability": s["analysis"]["probability"]}
        for s in case["samples"]
        if s["analysis"]["possible"]
    ]


def unmarked_packets(case):
    result = []
    for sample in case["samples"]:
        packet = copy.deepcopy(sample["problem"])
        del packet["record"]["marks"]
        result.append(packet)
    return result


def field_vector(case, field):
    return [q[field] for q in case["population"]]


def scaled_population(pop, factor):
    result = copy.deepcopy(pop)
    for q in result:
        for key in (
            "supplied_target",
            "geometric_target",
            "continuum_volume",
            "annotation_error",
            "quadrature_error",
        ):
            q[key] = wire(fraction(q[key]) * factor)
        for c in q["overlaps"]:
            c["volume"] = wire(fraction(c["volume"]) * factor)
    return result


def scaled_moments(mm, factor):
    result = copy.deepcopy(mm)
    for method in METHODS:
        for key in ("mean", "bias"):
            result[method][key] = vector(fraction(x) * factor for x in mm[method][key])
        result[method]["covariance"] = [
            vector(fraction(x) * factor * factor for x in row) for row in mm[method]["covariance"]
        ]
        for q in result[method]["decompositions"]:
            for key in q:
                if key != "probe":
                    q[key] = wire(fraction(q[key]) * factor)
    return result


def packet_scaling(base, other, factor):
    for s, t in zip(base["samples"], other["samples"], strict=True):
        packet = copy.deepcopy(s["problem"])
        for c in packet["record"]["marks"]:
            c["volume"] = wire(fraction(c["volume"]) * factor)
        if not same(packet, t["problem"]):
            return False
        expected = copy.deepcopy(s["analysis"])
        expected["input_sha256"] = digest(canonical(packet))
        for q in expected["questions"]:
            for c in q["observed_cells"]:
                c["volume"] = wire(fraction(c["volume"]) * factor)
            for method in METHODS:
                q["estimates"][method] = wire(fraction(q["estimates"][method]) * factor)
        if not same(expected, t["analysis"]):
            return False
    return True


def specifications():
    return [
        (name, level, design)
        for name in FAMILIES
        for level in range(3)
        for design in (
            ("identity", "iid_half", "singleton") if name in ("grid", "warp") else ("identity",)
        )
    ]


def ag_sources():
    doc = prior_json(AG_PRIOR)
    require(
        set(doc["source_ledger"])
        == {
            "README.md",
            "volume.py",
            "reference_qr05ag.py",
            "study.py",
            "test_qr05ag.py",
            "test_capture.py",
            "audit_json.py",
        },
        "AG ledger names",
    )
    for name, want in doc["source_ledger"].items():
        raw = plain_bytes(AGDIR / name)
        require_same_wire({"bytes": len(raw), "sha256": digest(raw)}, want, "AG source identity")
    return doc["source_ledger"]


def load_observers():
    ag_sources()
    modules = []
    for module_name, filename in (
        ("qr05ah_ag_primary", "volume.py"),
        ("qr05ah_ag_reference", "reference_qr05ag.py"),
    ):
        require(module_name not in sys.modules, "private observer collision")
        path = AGDIR / filename
        raw = plain_bytes(path)
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        exec(compile(raw, str(path), "exec"), module.__dict__)  # noqa: S102
        modules.append(module)
    return tuple(modules)


def counter_problem():
    def cell(name, parent, b, rep, w):
        return {
            "name": name,
            "parent": parent,
            "bounds": vector(b),
            "representative": vector(rep),
            "volume": wire(w),
        }

    return {
        "schema_version": "det8-qr05ah-problem-v1",
        "family": "qr05ah_partition_bounds",
        "domain": vector([0, 1, 0, 1]),
        "probes": [{"name": "q", "bounds": vector([0, F(1, 5), 0, 1])}],
        "levels": [
            {"name": "a", "cells": [cell("c", None, [0, 1, 0, 1], [F(3, 4), F(1, 2)], F(1, 2))]},
            {
                "name": "b",
                "cells": [
                    cell("c_l", "c", [0, F(1, 2), 0, 1], [F(1, 10), F(1, 2)], F(1, 4)),
                    cell("c_r", "c", [F(1, 2), 1, 0, 1], [F(3, 4), F(1, 2)], F(1, 4)),
                ],
            },
        ],
    }


def analyze_certificate(problem, engines=None):
    expected = certificate_oracle(problem)
    if engines is not None:
        for engine in engines:
            given = copy.deepcopy(problem)
            before = canonical(given)
            actual = engine.certify(given)
            require(canonical(given) == before, "certificate input mutated")
            require_same_wire(actual, expected, "complete source-aware certificate")
    return expected


def geometric_projection(analysis):
    out = copy.deepcopy(analysis)
    del out["input_sha256"]
    for level in out["levels"]:
        for cell in level["cells"]:
            del cell["annotation_error"]
        for q in level["questions"]:
            for key in ("supplied_target", "annotation_error", "total_error"):
                del q[key]
    for ref in out["refinements"]:
        for parent in ref["parents"]:
            del parent["supplied_volume"]
    return out


def scale_certificate(analysis, factor, input_hash):
    out = copy.deepcopy(analysis)
    out["input_sha256"] = input_hash
    out["domain_volume"] = wire(fraction(out["domain_volume"]) * factor)
    for level in out["levels"]:
        for cell in level["cells"]:
            for key in ("geometric_volume", "annotation_error"):
                cell[key] = wire(fraction(cell[key]) * factor)
        for q in level["questions"]:
            for key in q:
                if key not in ("probe", "inner_cells", "outer_cells", "representative_cells"):
                    q[key] = wire(fraction(q[key]) * factor)
    for ref in out["refinements"]:
        for parent in ref["parents"]:
            for key in ("geometric_volume", "supplied_volume"):
                parent[key] = wire(fraction(parent[key]) * factor)
        for q in ref["questions"]:
            for key in q:
                if key != "probe":
                    q[key] = wire(fraction(q[key]) * factor)
    return out


def case_certificate_bridge(case, certificate):
    level = LEVELS.index(case["level"])
    ids = label_ids(level)
    for pop, q in zip(case["population"], certificate["levels"][level]["questions"], strict=True):
        require_same_wire(
            pop["members"],
            sorted(ids[n] for n in q["representative_cells"]),
            "source labels to observed IDs",
        )
        for key in (
            "supplied_target",
            "geometric_target",
            "continuum_volume",
            "annotation_error",
            "quadrature_error",
        ):
            require_same_wire(pop[key], q[key], "source-aware geometric bridge " + key)


def controls(certificates, cases, counter):
    cb = {c["source"]: c["analysis"] for c in certificates}
    by = {c["case_id"]: c for c in cases}
    result = {"enclosures": [], "refinement": [], "stale_marks": []}
    for name in FAMILIES:
        cert = cb[name]
        qs = [q for level in cert["levels"] for q in level["questions"]]
        changes = [q for ref in cert["refinements"] for q in ref["questions"]]
        result["enclosures"].append(
            {
                "source": name,
                "sandwiches_hold": all(
                    fraction(q["lower_bound"]) <= fraction(q[k]) <= fraction(q["upper_bound"])
                    for q in qs
                    for k in ("geometric_target", "continuum_volume")
                ),
                "annotation_separate": all(
                    fraction(q["total_error"])
                    == fraction(q["annotation_error"]) + fraction(q["quadrature_error"])
                    and fraction(q["annotation_error"])
                    == fraction(q["supplied_target"]) - fraction(q["geometric_target"])
                    and fraction(q["quadrature_error"])
                    == fraction(q["geometric_target"]) - fraction(q["continuum_volume"])
                    and fraction(q["total_error"])
                    == fraction(q["supplied_target"]) - fraction(q["continuum_volume"])
                    for q in qs
                ),
                "aligned_exact": all(
                    q["lower_bound"]
                    == q["upper_bound"]
                    == q["geometric_target"]
                    == q["continuum_volume"]
                    for lev in cert["levels"]
                    for q in lev["questions"][:3]
                ),
            }
        )
        result["refinement"].append(
            {
                "source": name,
                "lower_nondecreasing": all(fraction(q["lower_gain"]) >= 0 for q in changes),
                "upper_nonincreasing": all(fraction(q["upper_drop"]) >= 0 for q in changes),
                "gap_nonincreasing": all(fraction(q["gap_drop"]) >= 0 for q in changes),
                "all_absolute_errors_nonincreasing": all(
                    fraction(q["absolute_error_change"]) <= 0 for q in changes
                ),
                "absolute_error_changes": [q["absolute_error_change"] for q in changes],
            }
        )
    for level in LEVELS:
        c = by["warp_stale__" + level + "__identity"]
        a = by["grid__" + level + "__identity"]
        result["stale_marks"].append(
            {
                "level": level,
                "geometric_certificate_equal_warp": same(
                    geometric_projection(cb["warp_stale"]), geometric_projection(cb["warp"])
                ),
                "public_samples_equal_base": same(a["samples"], c["samples"]),
                "annotation_errors": [q["annotation_error"] for q in c["population"]],
            }
        )
    for name, key, factor in (("boost", "boost", F(1)), ("dilate", "dilation", F(4))):
        result[key] = {
            "volume_factor": wire(factor),
            "complete_certificate_scaling": same(
                scale_certificate(cb["grid"], factor, cb[name]["input_sha256"]), cb[name]
            ),
            "complete_observer_scaling": all(
                packet_scaling(
                    by["grid__" + lev + "__identity"], by[name + "__" + lev + "__identity"], factor
                )
                for lev in LEVELS
            ),
            "complete_moment_scaling": all(
                same(
                    scaled_moments(by["grid__" + lev + "__identity"]["moments"], factor),
                    by[name + "__" + lev + "__identity"]["moments"],
                )
                for lev in LEVELS
            ),
        }
    ref = counter["analysis"]["refinements"][0]["questions"][0]
    result["counterexample"] = {
        **counter,
        "bounds_tightened": fraction(ref["gap_drop"]) > 0,
        "absolute_error_increased": fraction(ref["absolute_error_change"]) > 0,
    }
    return result


def prior_bridges(cases):
    ag = prior_json(AG_PRIOR)
    old = {c["case_id"]: c for c in ag["suite"]["cases"]}
    ids = []
    for case in cases:
        if case["level"] != "l0":
            continue
        key = case["source"]["name"] + "__" + case["design"]["name"]
        expected = copy.deepcopy(case)
        del expected["level"]
        expected["case_id"] = key
        require_same_wire(expected, old[key], "complete consumed AG level0 case")
        ids.append(key)
    require(len(ids) == 9, "nine AG bridges")
    return {
        "AG_level0_case_ids": ids,
        "AG_level0_complete_cases_equal": True,
        "AG_other_math_replayed": False,
    }


def malformed_certificates(problem):
    rows = []
    x = copy.deepcopy(problem)
    x["extra"] = 0
    rows.append(x)
    x = copy.deepcopy(problem)
    w = x["levels"][0]["cells"][0]["volume"]
    w[0] *= 2
    w[1] *= 2
    rows.append(x)
    x = copy.deepcopy(problem)
    c = x["levels"][0]["cells"][0]
    c["representative"][0] = c["bounds"][0]
    rows.append(x)
    x = copy.deepcopy(problem)
    x["levels"][0]["cells"].pop()
    rows.append(x)
    x = copy.deepcopy(problem)
    a, b = x["levels"][0]["cells"][:2]
    b["bounds"] = copy.deepcopy(a["bounds"])
    b["representative"] = copy.deepcopy(a["representative"])
    rows.append(x)
    x = copy.deepcopy(problem)
    x["levels"][1]["cells"][0]["parent"] = "missing"
    rows.append(x)
    x = copy.deepcopy(problem)
    c = x["levels"][1]["cells"][0]
    c["volume"] = wire(fraction(c["volume"]) * 2)
    rows.append(x)
    x = copy.deepcopy(problem)
    x["probes"][0]["bounds"][0] = [-1, 1]
    rows.append(x)
    return rows


def assemble_suite(certificates, cases, counter, rejected=16):
    require(len(certificates) == 5 and len(cases) == 27, "frozen family sizes")
    for c, (name, level, design) in zip(cases, specifications(), strict=True):
        require(c["case_id"] == name + "__" + LEVELS[level] + "__" + design, "case ordering")
        case_certificate_bridge(c, certificates[FAMILIES.index(name)]["analysis"])
    totals = {"cases": len(cases)}
    totals.update({key: sum(c["counts"][key] for c in cases) for key in cases[0]["counts"]})
    require(totals["mask_rows"] == 4032, "complete mask enumeration")
    return {
        "certificates": certificates,
        "cases": cases,
        "controls": controls(certificates, cases, counter),
        "prior_bridges": prior_bridges(cases),
        "public_controls": {
            "certificate_calls": 12,
            "observer_calls": totals["packet_calls"],
            "independent_certificate_routes_equal": True,
            "independent_observer_routes_equal": True,
            "invalid_certificate_calls_rejected": rejected,
        },
        "totals": totals,
        "scope": dict.fromkeys(SUITE_SCOPE, False),
    }


def check_case(case, expected):
    require_same_wire(case, expected, "complete AH observation case")


def check_suite(suite, expected):
    require_same_wire(suite, expected, "complete AH certificates and observations")


def run_suite():
    engines = (
        load("qr05ah_primary", "certificate.py"),
        load("qr05ah_reference", "reference_qr05ah.py"),
    )
    observers = load_observers()
    certs = []
    for name in FAMILIES:
        problem = certificate_problem(name)
        certs.append(
            {"source": name, "problem": problem, "analysis": analyze_certificate(problem, engines)}
        )
    problem = counter_problem()
    counter = {"problem": problem, "analysis": analyze_certificate(problem, engines)}
    cases = [build_case(name, level, design, observers) for name, level, design in specifications()]
    rejected = 0
    for engine in engines:
        for problem in malformed_certificates(certs[0]["problem"]):
            try:
                engine.certify(problem)
            except ValueError:
                rejected += 1
            else:
                raise ValueError("malformed certificate accepted")
    require(rejected == 16, "all invalid certificates rejected")
    return assemble_suite(certs, cases, counter, rejected)


if __name__ == "__main__":
    main()
