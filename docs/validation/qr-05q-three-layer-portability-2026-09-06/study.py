"""QR-05Q three-layer portability audit, capture, and read-only replay.

Generic lifecycle, chain-support and matrix-coefficient audit utilities are
locally carried from the O/P runner lineage. Independent reconstruction
never imports either executor; run_suite dispatches them only for comparison.
The Q raw source universe is regenerated before any pinned-artifact comparison.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import re
import resource
import sys
import time
from fractions import Fraction as F
from functools import cache as memoize
from functools import lru_cache
from itertools import combinations, product
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05q-results-v1"
BASE_COMMIT = "493a9bf1014ceaa687dd3934a0cc9ddf55e50783"
SOURCES = (
    "README.md",
    "portability.py",
    "reference_qr05q.py",
    "study.py",
    "test_qr05q.py",
    "test_capture.py",
)

PRIORS = {
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

O_PRIOR = "qr-05o-path-observable-2026-09-06/results.json"
GRID = (F(0), F(1, 3), F(2, 3), F(1))
AUDIT_POINTS = tuple(
    dict.fromkeys(
        [
            *product(GRID, repeat=2),
            (F(1, 2), F(1, 2)),
            (F(2, 5), F(3, 7)),
            (F(1, 5), F(4, 5)),
            (F(1, 2), F(1, 3)),
            (F(0), F(2, 5)),
            (F(3, 7), F(1)),
        ]
    )
)
MAX_CAPTURE_BYTES = 64 * 1024 * 1024
MAX_WORKING_BYTES = 512 * 1024 * 1024


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


def zero():
    return [[0] * 4 for _ in range(4)]


def frame_value(frame):
    return [frame["density"], frame["fixed"], frame["eligible"]]


def identity(fid, kept, past):
    return fid, tuple(kept), tuple(tuple(row) for row in past)


def induced_past(parent, kept):
    old = {v: i for i, v in enumerate(parent["kept"])}
    new = {v: i for i, v in enumerate(kept)}
    return [
        sorted(new[parent["kept"][i]] for i in parent["past"][old[v]] if parent["kept"][i] in new)
        for v in kept
    ]


def observed_features(kept, past, eligible):
    relation = {(kept[i], kept[j]) for j, row in enumerate(past) for i in row}
    bits = {v: 1 << i for i, v in enumerate(eligible)}
    odds = sum(bit for v, bit in bits.items() if v % 2)
    interior = [v for v in kept if v not in (0, 7)]
    supports = [[] for _ in range(4)]
    for q in range(4):
        for vertices in combinations(interior, q):
            chain = all(
                (u, v) in relation or (v, u) in relation for u, v in combinations(vertices, 2)
            )
            endpoints = all((0, v) in relation and (v, 7) in relation for v in vertices)
            if chain and endpoints and (0, 7) in relation:
                supports[q].append(sum(bits.get(v, 0) for v in vertices))
    d = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    b = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for q in range(4):
        for support in supports[q]:
            d[q][(support & odds).bit_count()][(support & ~odds).bit_count()] += 1
        for r in range(4):
            for left in supports[q]:
                for right in supports[r]:
                    union = left | right
                    b[q][r][(union & odds).bit_count()][(union & ~odds).bit_count()] += 1
    motifs = []
    for support in combinations(sorted(set(kept) & set(eligible)), 4):
        odd = [v for v in support if v % 2]
        even = [v for v in support if not v % 2]
        if len(odd) != 2 or len(even) != 2:
            continue
        actual = {(u, v) for u, v in relation if u in support and v in support}
        if actual in ({(u, v) for u in odd for v in even}, {(v, u) for u in odd for v in even}):
            motifs.append(list(support))
    return [len(row) for row in supports], d, b, motifs


@memoize
def kernel(O, E, o, e):
    table = zero()
    for i in range(O - o + 1):
        for j in range(E - e + 1):
            table[o + i][e + j] = (-1) ** (i + j) * comb(O - o, i) * comb(E - e, j)
    return tuple(tuple(row) for row in table)


def add_table(target, source, scale=1):
    for i, row in enumerate(source):
        for j, value in enumerate(row):
            target[i][j] += scale * value


@memoize
def sparse(table):
    return tuple((4 * i + j, c) for i, row in enumerate(table) for j, c in enumerate(row) if c)


@memoize
def eval_rates(table):
    return tuple(
        sum((c * x**i * y**j for i, row in enumerate(table) for j, c in enumerate(row) if c), F(0))
        for x, y in AUDIT_POINTS
    )


@memoize
def direct_rates(O, E, o, e):
    return tuple(x**o * (1 - x) ** (O - o) * y**e * (1 - y) ** (E - e) for x, y in AUDIT_POINTS)


def evaluate(table, x, y):
    return sum(
        (c * x**i * y**j for i, row in enumerate(table) for j, c in enumerate(row) if c), F(0)
    )


def groups_from_vector(vector):
    groups = []
    for sid, cid in enumerate(vector):
        require(type(cid) is int and 0 <= cid <= len(groups), "canonical class vector")
        if cid == len(groups):
            groups.append({"class_id": cid, "members": []})
        groups[cid]["members"].append(sid)
    return groups


def check_semigroup(rows):
    # Independent matrix-coefficient multiplication: A_ij A_kl is zero
    # unless (i,j)==(k,l), when it must equal A_ij.
    blocks = {}
    for row in rows:
        cid = row["class_id"]
        for atom in row["transitions"]:
            target = atom["target_class"]
            for i in range(4):
                for j in range(4):
                    c = atom["coefficients"][i][j]
                    if c:
                        blocks.setdefault((i, j), {}).setdefault(cid, {})[target] = c
    exponents = list(product(range(4), repeat=2))
    for left in exponents:
        for right in exponents:
            result = {}
            for source, middles in blocks.get(left, {}).items():
                output = {}
                for middle, c in middles.items():
                    for target, d in blocks.get(right, {}).get(middle, {}).items():
                        output[target] = output.get(target, 0) + c * d
                output = {t: c for t, c in output.items() if c}
                if output:
                    result[source] = output
            expected = blocks.get(left, {}) if left == right else {}
            require(result == expected, "four-variable semigroup coefficient matrix")
    results = []
    for row in rows:
        reachable = set()
        paths = 0
        for edge in row["transitions"]:
            target_rows = rows[edge["target_class"]]["transitions"]
            paths += len(target_rows)
            reachable.update(r["target_class"] for r in target_rows)
        require(
            reachable == {r["target_class"] for r in row["transitions"]},
            "one/two-step structural reachability",
        )
        results.append(
            {
                "class_id": row["class_id"],
                "transition_pairs": len(reachable),
                "intermediate_paths": paths,
                "coefficient_cells": 256 * len(reachable),
                "max_abs_residual": 0,
            }
        )
    totals = {
        k: sum(row[k] for row in results)
        for k in ("transition_pairs", "intermediate_paths", "coefficient_cells")
    }
    return {"verified": True, "rows": results, "totals": {**totals, "max_abs_residual": 0}}


def observed_paths(kept, past, eligible):
    """Independent exact induced-relation audit; not a graph-edge path count."""
    relation = {(kept[i], kept[j]) for j, row in enumerate(past) for i in row}
    paths = []
    for support in combinations(sorted(set(kept) & set(eligible)), 4):
        odd = [v for v in support if v % 2]
        even = [v for v in support if not v % 2]
        if len(odd) != 2 or len(even) != 2:
            continue
        actual = {(u, v) for u, v in relation if u in support and v in support}
        forward = set(product(odd, even))
        backward = set(product(even, odd))
        if len(actual) == 3 and (actual < forward or actual < backward):
            paths.append(list(support))
    return paths


def vector_refines(finer, coarser):
    require(len(finer) == len(coarser), "refinement domain")
    images = {}
    for left, right in zip(finer, coarser, strict=True):
        if left in images and images[left] != right:
            return False
        images[left] = right
    return True


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
    """Reject implicit JSON coercions in the mathematical evidence tree."""
    if value is None or type(value) in (bool, int, str):
        return
    if type(value) is list:
        for item in value:
            require_wire(item)
        return
    if type(value) is dict:
        require(all(type(key) is str for key in value), "wire keys must be strings")
        for item in value.values():
            require_wire(item)
        return
    raise ValueError("mathematical suite must use native exact JSON types")


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


def validate_model(model):
    require_wire(model)
    require(retained_bits(model) <= 4096, "model exact component cap")
    require(type(model) is dict and set(model) == {"frames", "states"}, "model fields")
    expected_frames = [
        {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
        {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
    ]
    require_same_wire(model["frames"], expected_frames, "exact frames and marks")
    states = model["states"]
    require(type(states) is list and 2 <= len(states) <= 35238, "state bound")
    registry = {}
    for sid, state in enumerate(states):
        require(
            type(state) is dict and set(state) == {"state_id", "frame_id", "kept", "past"},
            "observation fields",
        )
        require(type(state["state_id"]) is int and state["state_id"] == sid, "native state ID")
        fid = state["frame_id"]
        require(type(fid) is int and fid in (0, 1), "native frame ID")
        kept, past = state["kept"], state["past"]
        frame = model["frames"][fid]
        require(
            type(kept) is list and all(type(v) is int and 0 <= v <= 7 for v in kept),
            "native kept IDs",
        )
        require(
            kept == sorted(set(kept))
            and set(frame["fixed"]) <= set(kept)
            and set(kept) <= set(frame["fixed"] + frame["eligible"]),
            "kept marks",
        )
        require(type(past) is list and len(past) == len(kept), "past length")
        for row in past:
            require(
                type(row) is list and all(type(i) is int and 0 <= i < len(kept) for i in row),
                "native predecessor indices",
            )
            require(row == sorted(set(row)), "predecessor ordering")
        relation = {(kept[i], kept[j]) for j, row in enumerate(past) for i in row}
        require(all(u != v for u, v in relation), "strict order")
        require(
            all((u, w) in relation for u, v in relation for z, w in relation if z == v),
            "transitive relation",
        )
        require(
            all((0, v) in relation for v in kept if v != 0)
            and all((v, 7) in relation for v in kept if v != 7),
            "fixed endpoints",
        )
        key = identity(fid, kept, past)
        require(key not in registry, "duplicate observation")
        registry[key] = sid
    require({s["frame_id"] for s in states} == {0, 1}, "both frames represented")
    return registry


def reconstruct_model(model):
    registry = validate_model(model)
    features, fine = [], []
    for state in model["states"]:
        frame = model["frames"][state["frame_id"]]
        counts, d, b, motifs = observed_features(state["kept"], state["past"], frame["eligible"])
        paths = observed_paths(state["kept"], state["past"], frame["eligible"])
        eligible = [v for v in state["kept"] if v in frame["eligible"]]
        odd = sum(v % 2 for v in eligible)
        even = len(eligible) - odd
        require(len(motifs) + len(paths) <= comb(odd, 2) * comb(even, 2), "motif bound")
        features.append(
            {
                "state_id": state["state_id"],
                "color_sizes": [odd, even],
                "chain_counts": counts,
                "mean_graded": d,
                "pair_graded": b,
                "motif_supports": motifs,
                "motif_count": len(motifs),
                "path_supports": paths,
                "path_count": len(paths),
            }
        )
        atoms = []
        for mask in range(1 << len(eligible)):
            retained = [v for bit, v in enumerate(eligible) if mask & (1 << bit)]
            kept = sorted(frame["fixed"] + retained)
            key = identity(state["frame_id"], kept, induced_past(state, kept))
            require(key in registry, "missing induced successor")
            o = sum(v % 2 for v in retained)
            e = len(retained) - o
            table = kernel(odd, even, o, e)
            require(eval_rates(table) == direct_rates(odd, even, o, e), "fine rate polynomial")
            atoms.append({"target_state": registry[key], "coefficients": [list(r) for r in table]})
        atoms.sort(key=lambda atom: atom["target_state"])
        total = zero()
        for atom in atoms:
            add_table(total, atom["coefficients"])
        require(total == [[1, 0, 0, 0], [0] * 4, [0] * 4, [0] * 4], "fine normalization")
        for x, y in product((F(0), F(1)), repeat=2):
            kept = sorted(frame["fixed"] + [v for v in eligible if (x if v % 2 else y) == 1])
            target = registry[identity(state["frame_id"], kept, induced_past(state, kept))]
            row = {a["target_state"]: evaluate(a["coefficients"], x, y) for a in atoms}
            require({sid: p for sid, p in row.items() if p} == {target: F(1)}, "fine corner")
        fine.append({"state_id": state["state_id"], "transitions": atoms})
    atoms = sum(len(row["transitions"]) for row in fine)
    require(atoms <= 472428, "fine atom cap")
    partitions = {}
    for name in ("C", "H"):
        ids, vector, groups = {}, [], []
        for state, feature in zip(model["states"], features, strict=True):
            key = [
                frame_value(model["frames"][state["frame_id"]]),
                feature["pair_graded"],
                feature["motif_count"],
            ]
            if name == "H":
                key.append(feature["path_count"])
            encoded = canonical(key)
            if encoded not in ids:
                ids[encoded] = len(groups)
                groups.append({"class_id": len(groups), "key": key, "members": []})
            cid = ids[encoded]
            vector.append(cid)
            groups[cid]["members"].append(state["state_id"])
        partitions[name] = {"state_classes": vector, "classes": groups}
    metadata = {
        "sha256": digest(canonical(fine)),
        "transition_atoms": atoms,
        "coefficient_cells": 16 * atoms,
        "normalization_rows": len(fine),
        "deterministic_corner_rows": 4 * len(fine),
        "rate_points": len(AUDIT_POINTS),
        "evaluated_atoms": len(AUDIT_POINTS) * atoms,
    }
    return features, partitions, fine, metadata


def push_rows(fine, vector):
    result = []
    for row in fine:
        tables = {}
        for atom in row["transitions"]:
            cid = vector[atom["target_state"]]
            add_table(tables.setdefault(cid, zero()), atom["coefficients"])
        result.append(
            {
                "state_id": row["state_id"],
                "transitions": [
                    {"target_class": cid, "coefficients": tables[cid]} for cid in sorted(tables)
                ],
            }
        )
    return result


def quotient_from_rows(rows, groups):
    quotient = []
    for group in groups:
        rep = group["members"][0]
        law = rows[rep]["transitions"]
        for sid in group["members"]:
            require_same_wire(rows[sid]["transitions"], law, "terminal fiber law")
        quotient.append(
            {"class_id": group["class_id"], "representative_state": rep, "transitions": law}
        )
    return quotient


P_PRIOR = "qr-05p-minimal-summary-2026-09-06/results.json"
BASE_NAMES = ("ferrers6", "standard_example3", "chain6", "ferrers6_fixed", "path6", "cycle4_edge")
ADJACENT_EDGES = ((1, 3), (1, 4), (2, 3), (2, 4), (3, 5), (3, 6), (4, 5), (4, 6))


def fixtures():
    return [{"schema_version": "det8-qr05q-problem-v1", "family": "qr05q_three_layer"}]


def invalid_fixtures():
    return [
        None,
        [],
        {},
        True,
        1,
        {"schema_version": "det8-qr05q-problem-v1"},
        {"schema_version": "det8-qr05q-problem-v1", "family": "other"},
        {**fixtures()[0], "extra": 0},
    ]


def profile_name(index):
    require(type(index) is int and 0 <= index < 1542, "profile index")
    if index < 6:
        return BASE_NAMES[index]
    if index < 1030:
        direction = "oe" if index < 518 else "eo"
        mask = index - (6 if index < 518 else 518)
        return f"layered_{direction}_{mask:03d}"
    direction = "forward" if index < 1286 else "reverse"
    return f"three_layer_{direction}_{index - (1030 if index < 1286 else 1286):03d}"


def source_spec(index):
    """Independently saturate original-ID comparisons, then expose local past."""
    profile_name(index)
    edges = {(0, v) for v in range(1, 8)} | {(v, 7) for v in range(1, 7)}
    if index in (0, 1, 3):
        edges |= {
            (i + 1, j + 4) for i in range(3) for j in range(3) if (i != j if index == 1 else i <= j)
        }
    elif index == 2:
        edges |= {(u, v) for u in range(1, 7) for v in range(u + 1, 7)}
    elif index == 4:
        edges |= {(1, 2), (1, 4), (3, 4), (3, 6), (5, 6)}
    elif index == 5:
        edges |= {(1, 4), (1, 6), (3, 4), (3, 6), (2, 5)}
    elif index < 1030:
        forward = index < 518
        mask = index - (6 if forward else 518)
        edges |= {
            (2 * i + 1, 2 * j + 2) if forward else (2 * j + 2, 2 * i + 1)
            for i in range(3)
            for j in range(3)
            if mask & (1 << (3 * i + j))
        }
    else:
        forward = index < 1286
        mask = index - (1030 if forward else 1286)
        edges |= {
            (u, v) if forward else (v, u)
            for bit, (u, v) in enumerate(ADJACENT_EDGES)
            if mask & (1 << bit)
        }
    while True:
        expanded = edges | {(u, w) for u, v in edges for z, w in edges if v == z}
        if expanded == edges:
            break
        edges = expanded
    require(all(u != v for u, v in edges), "source cycle")
    return [[u for u in range(8) if (u, v) in edges] for v in range(8)]


def reconstruct_domain():
    frames = [
        {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
        {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
    ]
    states, profiles, ids = [], [], {}
    for index in range(1542):
        frame = frames[int(index == 3)]
        source = {"kept": list(range(8)), "past": source_spec(index)}
        aliases = []
        for mask in range(1 << len(frame["eligible"])):
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(frame["eligible"]) if mask & (1 << bit)]
            )
            past = induced_past(source, kept)
            key = identity(frame["frame_id"], kept, past)
            if key not in ids:
                sid = len(states)
                ids[key] = sid
                states.append(
                    {"state_id": sid, "frame_id": frame["frame_id"], "kept": kept, "past": past}
                )
            aliases.append(ids[key])
        profiles.append(
            {
                "profile_index": index,
                "name": profile_name(index),
                "frame_id": frame["frame_id"],
                "past": source["past"],
                "state_ids": aliases,
            }
        )
        if index == 1029:
            require(len(states) == 2470, "old observation prefix")
    require(len(states) <= 35238, "domain state cap")
    require(sum(len(p["state_ids"]) for p in profiles) == 98656, "alias inventory")
    return {"frames": frames, "profiles": profiles, "states": states}


def closure_from_rows(rows, partition):
    witness = None
    comparisons = 0
    for group in partition["classes"]:
        left = group["members"][0]
        lrow = {a["target_class"]: a["coefficients"] for a in rows[left]["transitions"]}
        for right in group["members"][1:]:
            comparisons += 1
            rrow = {a["target_class"]: a["coefficients"] for a in rows[right]["transitions"]}
            if lrow == rrow:
                continue
            target = next(
                t
                for t in sorted(lrow.keys() | rrow.keys())
                if lrow.get(t, zero()) != rrow.get(t, zero())
            )
            lt, rt = lrow.get(target, zero()), rrow.get(target, zero())
            rates = next(
                (x, y)
                for x, y in product(GRID, repeat=2)
                if evaluate(lt, x, y) != evaluate(rt, x, y)
            )
            if witness is None:
                witness = {
                    "class_id": group["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "target_class": target,
                    "left_coefficients": lt,
                    "right_coefficients": rt,
                    "first_distinguishing_rates": [str(x) for x in rates],
                }
    return {
        "closed": witness is None,
        "classes_checked": len(partition["classes"]),
        "member_comparisons": comparisons,
        "witness": witness,
    }


def check_expected_updates(features, fine, domain):
    kept_sets = tuple(frozenset(s["kept"]) for s in domain["states"])
    for row, parent in zip(fine, features, strict=True):
        for name in ("motif", "path"):
            total = zero()
            for atom in row["transitions"]:
                child = features[atom["target_state"]]
                add_table(total, atom["coefficients"], child[f"{name}_count"])
                # An induced subset loses only supports involving deleted vertices.
                require(
                    child[f"{name}_supports"]
                    == [
                        support
                        for support in parent[f"{name}_supports"]
                        if all(v in kept_sets[atom["target_state"]] for v in support)
                    ],
                    "induced motif support heredity",
                )
            expected = zero()
            expected[2][2] = parent[f"{name}_count"]
            require(total == expected, "motif/path exact expectation")
    return {"motif_cells": 16 * len(fine), "path_cells": 16 * len(fine), "max_abs_residual": 0}


@lru_cache(maxsize=1)
def _reconstruction_bytes():
    """Owned immutable cache; no identity-only validation shortcut."""
    domain = reconstruct_domain()
    model = {k: domain[k] for k in ("frames", "states")}
    features, partitions, fine, metadata = reconstruct_model(model)
    updates = check_expected_updates(features, fine, domain)
    h = partitions["H"]
    pushed = push_rows(fine, h["state_classes"])
    closure = closure_from_rows(pushed, h)
    quotient = quotient_from_rows(pushed, h["classes"]) if closure["closed"] else []
    semigroup = check_semigroup(quotient) if closure["closed"] else None
    analysis = {
        "domain": domain,
        "features": features,
        "partition": h,
        "fine_kernel": metadata,
        "pushed_rows": pushed,
        "closure": closure,
        "quotient_rows": quotient,
        "semigroup": semigroup,
        "expected_updates": updates,
        "counts": {
            "profiles": len(domain["profiles"]),
            "aliases": sum(len(p["state_ids"]) for p in domain["profiles"]),
            "states": len(domain["states"]),
            "classes": len(h["classes"]),
            "fine_atoms": metadata["transition_atoms"],
            "pushed_atoms": sum(len(r["transitions"]) for r in pushed),
        },
    }
    return canonical(analysis), canonical(fine[:2470])


def expected_analysis_bytes():
    return _reconstruction_bytes()[0]


def expected_analysis():
    return json.loads(expected_analysis_bytes())


def check_analysis(a):
    require_wire(a)
    require(retained_bits(a) <= 4096, "exact component cap")
    raw = canonical(a)
    require(len(raw) <= MAX_WORKING_BYTES, "working output cap")
    require(raw == expected_analysis_bytes(), "independent full reconstruction differs")
    return {
        "domain_regenerated": True,
        "all_features_reconstructed": True,
        "all_fine_rows_reconstructed": True,
        "all_H_rows_and_fibers_checked": True,
        "exact_fine_rate_points": 22,
        "motif_support_heredity_checked": True,
        "analysis_sha256": digest(raw),
    }


def prior_bridge(a):
    old = prior_json(O_PRIOR)["suite"]["analysis"]
    p = prior_json(P_PRIOR)["suite"]["analysis"]
    domain = a["domain"]
    require_same_wire(domain["frames"], old["frames"], "old frames")
    require_same_wire(domain["profiles"][:1030], old["profiles"], "old source alias prefix")
    old_model = {
        "frames": old["frames"],
        "states": [
            {k: s[k] for k in ("state_id", "frame_id", "kept", "past")} for s in old["states"]
        ],
    }
    require_same_wire(
        {"frames": domain["frames"], "states": domain["states"][:2470]},
        old_model,
        "old raw state prefix",
    )
    require(digest(canonical(old_model)) == p["model_sha256"], "pinned P raw model")
    require_same_wire(a["features"][:2470], p["features"], "old full observed features")
    vector = a["partition"]["state_classes"][:2470]
    classes = [
        {
            "class_id": g["class_id"],
            "key": g["key"],
            "members": [sid for sid in g["members"] if sid < 2470],
        }
        for g in a["partition"]["classes"]
        if g["members"][0] < 2470
    ]
    require_same_wire(
        {"state_classes": vector, "classes": classes}, p["partitions"]["H"], "old actual H fibers"
    )
    fine_raw = _reconstruction_bytes()[1]
    old_fine = [{"state_id": s["state_id"], "transitions": s["transitions"]} for s in old["states"]]
    require(fine_raw == canonical(old_fine), "old full fine rows")
    require(digest(fine_raw) == p["fine_kernel"]["sha256"], "old P fine digest")
    restricted_rows = a["pushed_rows"][:2470]
    require(
        all(atom["target_class"] < 167 for row in restricted_rows for atom in row["transitions"]),
        "old successors stay old",
    )
    restricted_partition = {"state_classes": vector, "classes": classes}
    closure = closure_from_rows(restricted_rows, restricted_partition)
    require(closure["closed"], "old restricted H closure")
    quotient = quotient_from_rows(restricted_rows, classes)
    require_same_wire(quotient, p["refinement"]["quotient_rows"], "old restricted quotient")
    semigroup = check_semigroup(quotient)
    require_same_wire(semigroup, p["refinement"]["semigroup"], "old restricted semigroup")
    new_aliases_old = sum(
        sid < 2470 for profile in domain["profiles"][1030:] for sid in profile["state_ids"]
    )
    return {
        "O_prior": O_PRIOR,
        "P_prior": P_PRIOR,
        "source_alias_universe_regenerated": True,
        "executor_prior_input_dependency": False,
        "old_profiles": 1030,
        "old_aliases": 65888,
        "old_states": 2470,
        "old_H_classes": 167,
        "raw_prefix_equal": True,
        "features_equal": True,
        "actual_H_restriction_equal": True,
        "fine_kernel_sha256": digest(fine_raw),
        "old_quotient_equal": True,
        "old_semigroup": semigroup,
        "new_states": len(domain["states"]) - 2470,
        "new_profile_aliases_on_old_states": new_aliases_old,
    }


def controls(a):
    domain = a["domain"]
    states, profiles, features = domain["states"], domain["profiles"], a["features"]
    bit_checks = 0
    for reverse in (False, True):
        offset = 1286 if reverse else 1030
        for bit, (u, v) in enumerate(ADJACENT_EDGES):
            past = profiles[offset + (1 << bit)]["past"]
            actual = {(u, v) for v in range(1, 7) for u in past[v] if 1 <= u <= 6}
            require(actual == ({(v, u)} if reverse else {(u, v)}), "single-bit orientation")
            bit_checks += 1
        full = profiles[offset + 255]
        require(
            features[full["state_ids"][63]]["chain_counts"] == [1, 6, 12, 8],
            "full-mask chain counts",
        )
        chain = profiles[offset + 17]
        kept_15 = states[chain["state_ids"][17]]  # bits0,4 retain original1,5
        rel = {
            (kept_15["kept"][i], kept_15["kept"][j])
            for j, row in enumerate(kept_15["past"])
            for i in row
        }
        require(((5, 1) if reverse else (1, 5)) in rel, "deleted-middle comparison")
        selected = features[chain["state_ids"][21]]  # bits0,2,4 retain1,3,5
        require(selected["mean_graded"][3][3][0] == 1, "parity not layer color")
        empty = profiles[offset]["past"]
        require(
            all(not [u for u in empty[v] if 1 <= u <= 6] for v in range(1, 7)),
            "no free skip-layer edge",
        )
    return {
        "single_bit_sources": bit_checks,
        "full_mask_chain_controls": 2,
        "deleted_middle_comparison_controls": 2,
        "same_color_chain_controls": 2,
        "no_skip_edge_controls": 2,
        "fixed_frame_only_source3": all(
            p["frame_id"] == int(p["profile_index"] == 3) for p in profiles
        ),
        "all_structural_atoms_retained": True,
        "expanded_closure": a["closure"]["closed"],
    }


def run_suite():
    direct = load("_qr05q_direct", "portability.py")
    reference = load("_qr05q_reference", "reference_qr05q.py")
    problem = fixtures()[0]
    before = canonical(problem)
    a = direct.analyze(problem)
    require(canonical(problem) == before, "primary input mutation")
    require_wire(a)
    b = reference.analyze(problem)
    require(canonical(problem) == before, "reference input mutation")
    require_same_wire(a, b, "independent executor outputs differ")
    audit = check_analysis(a)
    bridge = prior_bridge(a)
    positive = controls(a)
    rejected = 0
    for route in (direct, reference):
        for invalid in invalid_fixtures():
            try:
                route.analyze(invalid)
            except ValueError:
                rejected += 1
            else:
                raise ValueError("invalid public input accepted")
    require_wire(a)
    return {
        "problem": problem,
        "analysis": a,
        "independent_route_equal": True,
        "independent_audit": audit,
        "prior_bridge": bridge,
        "controls": positive,
        "invalid_inputs_rejected": rejected,
        "totals": {
            **a["counts"],
            "H_closed": a["closure"]["closed"],
            "H_member_comparisons": a["closure"]["member_comparisons"],
            "fine_coefficient_cells": a["fine_kernel"]["coefficient_cells"],
            "fine_rate_evaluations": a["fine_kernel"]["evaluated_atoms"],
            "motif_expectation_cells": a["expected_updates"]["motif_cells"],
            "path_expectation_cells": a["expected_updates"]["path_cells"],
            "new_states": bridge["new_states"],
            "old_H_classes_preserved": 167,
        },
    }


if __name__ == "__main__":
    main()
