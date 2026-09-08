"""QR-05AG private supplied-geometry producer and exact record-local comparison.

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
SCHEMA = "det8-qr05ag-results-v1"
BASE_COMMIT = "39921dff4fc9e9bbc02817659473c87bda1bb430"
SOURCES = (
    "README.md",
    "volume.py",
    "reference_qr05ag.py",
    "study.py",
    "test_qr05ag.py",
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

PRIORS = {
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
SUITE_SCOPE = (
    "unknown_geometry_reconstructed",
    "annotations_proved_necessary_or_minimal",
    "continuum_limit_established",
    "poisson_ensemble_validated",
    "quantum_channel_constructed",
    "gravity_derived",
    "empirical_data_used",
    "ret_integration_tested",
    "unknown_sampling_law_inferred",
)
DESIGNS = ("identity", "iid_half", "heterogeneous", "all_or_none", "fixed_size2", "singleton")


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


def make_source(name):
    require(name in ("grid", "warp", "warp_stale", "boost", "dilate"), "known source")
    base = {
        "bottom": (F(0), F(0)),
        "aligned": (F(2, 3), F(1, 2)),
        "unaligned": (F(3, 5), F(2, 5)),
        "top": (F(1), F(1)),
    }
    bounds = {}
    for i, j in itertools.product(range(3), range(2)):
        label = f"c_{i}_{j}"
        base[label] = (F(2 * i + 1, 6), F(2 * j + 1, 4))
        bounds[label] = (F(i, 3), F(i + 1, 3), F(j, 2), F(j + 1, 2))
    labels = sorted(base, key=lambda label: (sum(base[label]), *base[label], label))
    ids = {label: i for i, label in enumerate(labels)}

    def transform(u, v):
        if name in ("warp", "warp_stale"):
            return u * u, v * v
        if name == "boost":
            return 2 * u, v / 2
        if name == "dilate":
            return 2 * u, 2 * v
        return u, v

    coords = [transform(*base[label]) for label in labels]
    tx = [((u + v) / 2, (u - v) / 2) for u, v in coords]
    past = [
        [i for i in range(j) if tx[j][0] - tx[i][0] > abs(tx[j][1] - tx[i][1])]
        for j in range(len(coords))
    ]
    cells = []
    for label in labels:
        if label not in bounds:
            continue
        ul, uh, vl, vh = bounds[label]
        newul, newvl = transform(ul, vl)
        newuh, newvh = transform(uh, vh)
        g = (newuh - newul) * (newvh - newvl) / 2
        w = (uh - ul) * (vh - vl) / 2 if name == "warp_stale" else g
        cells.append(
            {
                "event": ids[label],
                "bounds": vector([newul, newuh, newvl, newvh]),
                "geometric_mark": wire(g),
                "supplied_mark": wire(w),
            }
        )
    probes = [
        {"name": q, "source": ids[a], "target": ids[b]}
        for q, a, b in (
            ("whole", "bottom", "top"),
            ("lower_aligned", "bottom", "aligned"),
            ("upper_aligned", "aligned", "top"),
            ("lower_unaligned", "bottom", "unaligned"),
            ("upper_unaligned", "unaligned", "top"),
        )
    ]
    return {
        "name": name,
        "coordinates": [vector(c) for c in coords],
        "past": past,
        "fixed": sorted(ids[label] for label in base if label not in bounds),
        "eligible": [c["event"] for c in cells],
        "probes": probes,
        "cells": cells,
        "mark_kind": "stale_base" if name == "warp_stale" else "geometric_cell_volume",
    }


def design_law(name, m):
    require(m == 6, "frozen design frame")
    masses = []
    for mask in range(1 << m):
        count = mask.bit_count()
        if name == "identity":
            p = F(mask == (1 << m) - 1)
        elif name == "iid_half":
            p = F(1, 1 << m)
        elif name == "heterogeneous":
            p = F(1)
            for i in range(m):
                rate = F(1 if i % 2 == 0 else 2, 3)
                p *= rate if mask & (1 << i) else 1 - rate
        elif name == "all_or_none":
            p = F(1, 2) if mask in (0, (1 << m) - 1) else F(0)
        elif name == "fixed_size2":
            p = F(1, 15) if count == 2 else F(0)
        elif name == "singleton":
            p = F(1, 6) if count == 1 else F(0)
        else:
            raise ValueError("known design")
        masses.append(p)
    require(sum(masses, F(0)) == 1, "design normalization")
    return {"name": name, "mask_probabilities": vector(masses)}


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


def specifications():
    return [(name, design) for name in ("grid", "warp") for design in DESIGNS] + [
        (name, design)
        for name in ("warp_stale", "boost", "dilate")
        for design in ("identity", "iid_half")
    ]


def build_case(name, design_name, engines=None):
    source = make_source(name)
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
        "case_id": name + "__" + design_name,
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


def controls(cases):
    by = {c["case_id"]: c for c in cases}
    result = {
        "warp": [],
        "stale_marks": [],
        "boost": [],
        "dilation": [],
        "boundaries": [],
        "sampling": [],
    }
    for design in DESIGNS:
        a, b = by["grid__" + design], by["warp__" + design]
        result["warp"].append(
            {
                "design": design,
                "unmarked_packets_equal": same(unmarked_packets(a), unmarked_packets(b)),
                "marked_positive_laws_equal": same(positive_packet_law(a), positive_packet_law(b)),
                "base_targets": field_vector(a, "supplied_target"),
                "warped_targets": field_vector(b, "supplied_target"),
                "base_volumes": field_vector(a, "continuum_volume"),
                "warped_volumes": field_vector(b, "continuum_volume"),
            }
        )
    for design in ("identity", "iid_half"):
        a, b, c = (by[name + "__" + design] for name in ("grid", "warp", "warp_stale"))
        result["stale_marks"].append(
            {
                "design": design,
                "packets_equal_base": same(a["samples"], c["samples"]),
                "geometric_targets_equal_warp": same(
                    field_vector(b, "geometric_target"), field_vector(c, "geometric_target")
                ),
                "supplied_targets": field_vector(c, "supplied_target"),
                "geometric_targets": field_vector(c, "geometric_target"),
                "annotation_errors": field_vector(c, "annotation_error"),
            }
        )
        for name, key, factor in (("boost", "boost", F(1)), ("dilate", "dilation", F(4))):
            t = by[name + "__" + design]
            result[key].append(
                {
                    "design": design,
                    "order_equal": same(a["source"]["past"], t["source"]["past"]),
                    "packet_estimate_scaling": packet_scaling(a, t, factor),
                    "moment_scaling": same(scaled_moments(a["moments"], factor), t["moments"]),
                    "population_scaling": same(
                        scaled_population(a["population"], factor), t["population"]
                    ),
                    "volume_factor": wire(factor),
                }
            )
    for name in ("grid", "warp", "warp_stale", "boost", "dilate"):
        c = by[name + "__identity"]
        result["boundaries"].append(
            {
                "source": name,
                "overlaps_sum_to_volume": all(
                    sum((fraction(x["volume"]) for x in q["overlaps"]), F(0))
                    == fraction(q["continuum_volume"])
                    for q in c["population"]
                ),
                "aligned_geometric_exact": all(
                    q["geometric_target"] == q["continuum_volume"] for q in c["population"][:3]
                ),
                "unaligned_quadrature_errors": field_vector(c, "quadrature_error")[3:],
            }
        )
    for name in ("grid", "warp"):
        for design in DESIGNS:
            c = by[name + "__" + design]
            result["sampling"].append(
                {
                    "case_id": c["case_id"],
                    "inclusion_unbiased": all(
                        x == [0, 1] for x in c["moments"]["inclusion"]["bias"]
                    ),
                    "uniform_bias": c["moments"]["uniform_rate"]["bias"],
                    "raw_bias": c["moments"]["raw"]["bias"],
                    "covariance_formula_equal": same(
                        c["moments"]["inclusion"]["covariance"], c["joint_covariance"]
                    ),
                }
            )
    return result


def malformed_packets(packet):
    rows = []
    x = copy.deepcopy(packet)
    x["extra"] = 0
    rows.append(x)
    x = copy.deepcopy(packet)
    x["coordinates"] = []
    rows.append(x)
    x = copy.deepcopy(packet)
    x["record"]["kept"][0] = False
    rows.append(x)
    x = copy.deepcopy(packet)
    x["mask_probabilities"][-1] = [1, 2]
    rows.append(x)
    x = copy.deepcopy(packet)
    x["record"]["kept"].pop(0)
    rows.append(x)
    x = copy.deepcopy(packet)
    removed = False
    for k, row in enumerate(x["record"]["past"]):
        for j in row:
            for i in x["record"]["past"][j]:
                if i in row:
                    row.remove(i)
                    removed = True
                    break
            if removed:
                break
        if removed:
            break
    require(removed, "nonvacuous transitivity corruption")
    rows.append(x)
    x = copy.deepcopy(packet)
    x["record"]["marks"].pop()
    rows.append(x)
    x = copy.deepcopy(packet)
    x["record"]["marks"].insert(0, {"event": x["fixed"][0], "volume": [1, 1]})
    rows.append(x)
    return rows


def assemble_suite(cases, rejected=16):
    require(len(cases) == 18, "frozen case count")
    for c, (name, design) in zip(cases, specifications(), strict=True):
        require(c["case_id"] == name + "__" + design, "frozen case order")
    totals = {"cases": len(cases)}
    totals.update({k: sum(c["counts"][k] for c in cases) for k in cases[0]["counts"]})
    require(totals["mask_rows"] == 1152, "all frozen mask rows")
    return {
        "cases": cases,
        "controls": controls(cases),
        "public_controls": {
            "ordinary_packet_calls": totals["packet_calls"],
            "independent_route_equal": True,
            "invalid_calls_rejected": rejected,
        },
        "totals": totals,
        "scope": dict.fromkeys(SUITE_SCOPE, False),
    }


def check_case(case, expected):
    require_same_wire(case, expected, "complete marked-volume private case")


def check_suite(suite, expected):
    require_same_wire(suite, expected, "complete native AG suite including controls and scope")


def run_suite():
    engines = (load("qr05ag_primary", "volume.py"), load("qr05ag_reference", "reference_qr05ag.py"))
    cases = [build_case(name, design, engines) for name, design in specifications()]
    rejected = 0
    for engine in engines:
        for packet in malformed_packets(cases[0]["samples"][-1]["problem"]):
            try:
                engine.analyze(packet)
            except ValueError:
                rejected += 1
            else:
                raise ValueError("malformed AG input accepted")
    require(rejected == 16, "all malformed public controls rejected")
    return assemble_suite(cases, rejected)


if __name__ == "__main__":
    main()
