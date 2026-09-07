"""QR-05P exact refinement/consumer audit, capture, and read-only replay.

Generic lifecycle, chain-support and matrix-coefficient audit utilities are
locally carried from O; P reconstruction never imports either executor.
The pinned O raw observation table is a declared model input dependency.
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
SCHEMA = "det8-qr05p-results-v1"
BASE_COMMIT = "35831db06b3f5089fdb36d066cfb741b1c2984cb"
SOURCES = (
    "README.md",
    "closure.py",
    "reference_qr05p.py",
    "study.py",
    "test_qr05p.py",
    "test_capture.py",
)

PRIORS = {
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
QUESTIONS = ("chain_counts", "motif_count", "path_count", "counts_motif_path", "named_relation_1_7")
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


def fixtures():
    old = prior_json(O_PRIOR)["suite"]["analysis"]
    model = {
        "frames": old["frames"],
        "states": [
            {key: state[key] for key in ("state_id", "frame_id", "kept", "past")}
            for state in old["states"]
        ],
    }
    return [
        {
            "schema_version": "det8-qr05p-problem-v1",
            "family": "qr05p_summary_contract",
            "model": model,
        }
    ]


def invalid_fixtures():
    good = fixtures()[0]
    return [
        None,
        [],
        True,
        {},
        {**good, "extra": 1},
        {k: v for k, v in good.items() if k != "model"},
        *({**good, "schema_version": v} for v in (None, 1, True, [], "wrong")),
        *({**good, "family": v} for v in (None, 1, True, [], "wrong")),
        *({**good, "model": v} for v in (None, 1, True, [], {})),
    ]


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
    require(type(states) is list and 2 <= len(states) <= 2470, "state bound")
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
    require(atoms <= 99180, "fine atom cap")
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


def class_map(left, right):
    if not vector_refines(left, right):
        return None
    groups = groups_from_vector(left)
    return [right[g["members"][0]] for g in groups]


def refinement_rounds(fine, initial):
    vector = list(initial)
    rounds = []
    limit = len(vector) - len(groups_from_vector(vector)) + 1
    for ri in range(limit):
        groups = groups_from_vector(vector)
        rows = push_rows(fine, vector)
        registry, new = {}, []
        for sid, row in enumerate(rows):
            signature = canonical([vector[sid], row["transitions"]])
            if signature not in registry:
                registry[signature] = len(registry)
            new.append(registry[signature])
        require(vector_refines(new, vector), "refinement cannot merge")
        separations = []
        for child in groups_from_vector(new):
            right = child["members"][0]
            parent = vector[right]
            left = groups[parent]["members"][0]
            if new[left] == child["class_id"]:
                continue
            l = {a["target_class"]: a["coefficients"] for a in rows[left]["transitions"]}
            r = {a["target_class"]: a["coefficients"] for a in rows[right]["transitions"]}
            target = next(
                t for t in sorted(l.keys() | r.keys()) if l.get(t, zero()) != r.get(t, zero())
            )
            a, b = l.get(target, zero()), r.get(target, zero())
            rates = next(
                [str(x), str(y)]
                for x, y in product(GRID, repeat=2)
                if evaluate(a, x, y) != evaluate(b, x, y)
            )
            separations.append(
                {
                    "parent_class_id": parent,
                    "child_class_id": child["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "target_class": target,
                    "left_coefficients": a,
                    "right_coefficients": b,
                    "first_distinguishing_rates": rates,
                }
            )
        stable = vector == new
        rounds.append(
            {
                "round_index": ri,
                "state_classes": vector,
                "classes": groups,
                "pushed_rows_sha256": digest(canonical(rows)),
                "pushed_atoms": sum(len(row["transitions"]) for row in rows),
                "stable": stable,
                "separations": separations,
            }
        )
        require(len(canonical(rounds)) <= MAX_WORKING_BYTES, "working output cap")
        if stable:
            return rounds, rows
        require(len(set(new)) > len(groups), "strict refinement must split")
        vector = new
    raise ValueError("refinement exceeded finite bound")


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


def question_values(model, features):
    values = {name: [] for name in QUESTIONS}
    for state, feature in zip(model["states"], features, strict=True):
        relation = {
            (state["kept"][i], state["kept"][j]) for j, row in enumerate(state["past"]) for i in row
        }
        values["chain_counts"].append(feature["chain_counts"])
        values["motif_count"].append(feature["motif_count"])
        values["path_count"].append(feature["path_count"])
        values["counts_motif_path"].append(
            [*feature["chain_counts"], feature["motif_count"], feature["path_count"]]
        )
        values["named_relation_1_7"].append(int((1, 7) in relation))
    return values


def marginal(transitions, values, target_field):
    tables, originals = {}, {}
    for atom in transitions:
        value = values[atom[target_field]]
        key = canonical(value)
        originals[key] = value
        add_table(tables.setdefault(key, zero()), atom["coefficients"])
    return [{"value": originals[key], "coefficients": tables[key]} for key in sorted(tables)]


def consumer_certificate(model, features, fine, vector, quotient):
    groups = groups_from_vector(vector)
    all_values = question_values(model, features)
    observables, marginals, nonmeasurable = [], [], []
    prediction_checks = 0
    for name in QUESTIONS:
        values = all_values[name]
        failure = None
        for group in groups:
            left = group["members"][0]
            for right in group["members"][1:]:
                if canonical(values[left]) != canonical(values[right]):
                    failure = {
                        "class_id": group["class_id"],
                        "left_state": left,
                        "right_state": right,
                        "left_value": values[left],
                        "right_value": values[right],
                    }
                    break
            if failure is not None:
                break
        class_values = None if failure else [values[g["members"][0]] for g in groups]
        observables.append(
            {
                "name": name,
                "measurable": failure is None,
                "class_values": class_values,
                "first_failure": failure,
            }
        )
        if failure:
            nonmeasurable.append(name)
            continue
        rows = [
            {
                "class_id": row["class_id"],
                "outcomes": marginal(row["transitions"], class_values, "target_class"),
            }
            for row in quotient
        ]
        cells = 0
        for state in fine:
            actual = marginal(state["transitions"], values, "target_state")
            require_same_wire(
                actual, rows[vector[state["state_id"]]]["outcomes"], "consumer full marginal law"
            )
            cells += 16 * len(actual)
        for row in rows:
            for index, _ in enumerate(AUDIT_POINTS):
                probabilities = [
                    eval_rates(tuple(tuple(r) for r in atom["coefficients"]))[index]
                    for atom in row["outcomes"]
                ]
                require(
                    all(p >= 0 for p in probabilities) and sum(probabilities) == 1,
                    "consumer rate distribution",
                )
                prediction_checks += 1
        marginals.append({"name": name, "rows": rows, "fine_coefficient_cells": cells})
    consumer = {
        "schema_version": "det8-qr05p-consumer-v1",
        "model_sha256": digest(canonical(model)),
        "state_classes_sha256": digest(canonical(vector)),
        "class_count": len(groups),
        "quotient_rows": quotient,
        "observables": observables,
    }
    keys = {identity(s["frame_id"], s["kept"], s["past"]): s["state_id"] for s in model["states"]}
    pair = [keys[identity(0, [0, v, 7], [[], [0], [0, 1]])] for v in (1, 3)]
    tables = []
    for sid in pair:
        table = zero()
        for atom in fine[sid]["transitions"]:
            add_table(
                table, atom["coefficients"], all_values["named_relation_1_7"][atom["target_state"]]
            )
        tables.append(table)
    expected = zero()
    expected[1][0] = 1
    require_same_wire(tables, [expected, zero()], "named singleton x/zero exclusion")
    require(vector[pair[0]] == vector[pair[1]], "same summary named singleton")
    return consumer, {
        "marginals": marginals,
        "prediction_checks": prediction_checks,
        "nonmeasurable_questions": nonmeasurable,
        "named_singleton_control": {
            "state_ids": pair,
            "R_classes": [vector[sid] for sid in pair],
            "current_values": [all_values["named_relation_1_7"][sid] for sid in pair],
            "next_coefficients": tables,
            "half_probabilities": [str(evaluate(t, F(1, 2), F(1, 2))) for t in tables],
            "same_R_class": True,
        },
        "verified": True,
    }


def expected_analysis(model):
    features, partitions, fine, metadata = reconstruct_model(model)
    rounds, rows = refinement_rounds(fine, partitions["C"]["state_classes"])
    final = rounds[-1]
    vector, groups = final["state_classes"], final["classes"]
    quotient = quotient_from_rows(rows, groups)
    semigroup = check_semigroup(quotient)
    # Recheck H's closure from this supplied model; H is never the refinement seed.
    h_rows = push_rows(fine, partitions["H"]["state_classes"])
    quotient_from_rows(h_rows, partitions["H"]["classes"])
    vectors = {
        "C": partitions["C"]["state_classes"],
        "R": vector,
        "H": partitions["H"]["state_classes"],
    }
    comparison = {
        "names": ["C", "R", "H"],
        "refinement": [
            [vector_refines(vectors[x], vectors[y]) for y in ("C", "R", "H")]
            for x in ("C", "R", "H")
        ],
        "same_memberships_as_H": vector == vectors["H"],
        "R_to_C": class_map(vector, vectors["C"]),
        "R_to_H": class_map(vector, vectors["H"]),
        "H_to_R": class_map(vectors["H"], vector),
    }
    require(
        comparison["R_to_C"] is not None and comparison["H_to_R"] is not None,
        "coarseness premise: closed H/C refinement",
    )
    round_atoms = sum(r["pushed_atoms"] for r in rounds)
    refinement_counts = {
        "rounds": len(rounds),
        "strict_rounds": len(rounds) - 1,
        "classes": len(groups),
        "round_transition_atoms": round_atoms,
        "round_coefficient_cells": 16 * round_atoms,
        "separation_witnesses": sum(len(r["separations"]) for r in rounds),
        "quotient_transition_atoms": sum(len(r["transitions"]) for r in quotient),
        "semigroup_intermediate_paths": semigroup["totals"]["intermediate_paths"],
        "semigroup_coefficient_cells": semigroup["totals"]["coefficient_cells"],
    }
    refinement = {
        "initial_partition": "C",
        "rounds": rounds,
        "strict_rounds": len(rounds) - 1,
        "final_round": len(rounds) - 1,
        "state_classes": vector,
        "classes": groups,
        "quotient_rows": quotient,
        "semigroup": semigroup,
        "comparison": comparison,
        "counts": refinement_counts,
    }
    consumer, audit = consumer_certificate(model, features, fine, vector, quotient)
    pair = audit["named_singleton_control"]["state_ids"]
    for name in ("C", "H"):
        audit["named_singleton_control"][name + "_classes"] = [vectors[name][sid] for sid in pair]
    counts = {
        "states": len(model["states"]),
        "features": len(features),
        "C_classes": len(partitions["C"]["classes"]),
        "H_classes": len(partitions["H"]["classes"]),
        "R_classes": len(groups),
        "fine_atoms": metadata["transition_atoms"],
        "refinement_rounds": len(rounds),
        "strict_rounds": len(rounds) - 1,
        "measurable_questions": sum(o["measurable"] for o in consumer["observables"]),
        "consumer_prediction_checks": audit["prediction_checks"],
        "consumer_fine_coefficient_cells": sum(
            m["fine_coefficient_cells"] for m in audit["marginals"]
        ),
    }
    result = {
        "model_sha256": digest(canonical(model)),
        "features": features,
        "partitions": partitions,
        "fine_kernel": metadata,
        "refinement": refinement,
        "consumer": consumer,
        "consumer_audit": audit,
        "counts": counts,
    }
    require(len(canonical(result)) <= MAX_WORKING_BYTES, "working output cap")
    return result


@lru_cache(maxsize=2)
def expected_analysis_bytes(model_bytes):
    """Cache immutable evidence by exact native model content, never object identity."""
    return canonical(expected_analysis(json.loads(model_bytes)))


def check_analysis(a, model):
    require_wire(a)
    require_wire(model)
    require(retained_bits(a) <= 4096, "exact component cap")
    require(retained_bits(model) <= 4096, "model exact component cap")
    require(
        canonical(a) == expected_analysis_bytes(canonical(model)),
        "complete independent P reconstruction",
    )
    return {
        "verified": True,
        "model_states": len(model["states"]),
        "fine_coefficient_cells": a["fine_kernel"]["coefficient_cells"],
        "refinement_rounds": len(a["refinement"]["rounds"]),
        "round_coefficient_cells": a["refinement"]["counts"]["round_coefficient_cells"],
        "semigroup_coefficient_cells": a["refinement"]["counts"]["semigroup_coefficient_cells"],
        "consumer_fine_coefficient_cells": a["counts"]["consumer_fine_coefficient_cells"],
        "consumer_prediction_checks": a["consumer_audit"]["prediction_checks"],
        "coarsest_argument_premises_verified": True,
        "earlier_O_certificates_recomputed": False,
    }


def prior_bridge(a, model):
    old = prior_json(O_PRIOR)["suite"]["analysis"]
    expected_model = {
        "frames": old["frames"],
        "states": [
            {k: s[k] for k in ("state_id", "frame_id", "kept", "past")} for s in old["states"]
        ],
    }
    require_same_wire(model, expected_model, "raw model is exact pinned O projection")
    expected_features = [
        {
            **{
                k: state[k]
                for k in (
                    "state_id",
                    "color_sizes",
                    "chain_counts",
                    "mean_graded",
                    "pair_graded",
                    "motif_supports",
                    "motif_count",
                )
            },
            "path_supports": path["path_supports"],
            "path_count": path["path_count"],
        }
        for state, path in zip(old["states"], old["path_observable"]["states"], strict=True)
    ]
    require_same_wire(a["features"], expected_features, "all O features preserved")
    fine = [{"state_id": s["state_id"], "transitions": s["transitions"]} for s in old["states"]]
    require_same_wire(
        a["fine_kernel"]["sha256"], digest(canonical(fine)), "all O fine kernel digest"
    )
    require_same_wire(
        a["partitions"]["C"],
        {
            "state_classes": [s["classes"]["motif_pair"] for s in old["states"]],
            "classes": old["partitions"]["motif_pair"],
        },
        "C fibers preserved",
    )
    require_same_wire(
        a["partitions"]["H"],
        {
            "state_classes": old["path_observable"]["state_classes"],
            "classes": old["path_observable"]["classes"],
        },
        "H fibers preserved",
    )
    return {
        "prior_artifact": O_PRIOR,
        "matched_states": len(fine),
        "model_projection_equal": True,
        "all_features_equal": True,
        "C_H_memberships_equal": True,
        "fine_kernel_sha256": digest(canonical(fine)),
        "declared_observation_input_dependency": True,
        "source_alias_universe_regenerated": False,
        "whole_O_analysis_reproduced": False,
        "earlier_O_expectation_certificates_recomputed": False,
    }


def public_controls(direct, reference, a):
    consumer = a["consumer"]
    ids = sorted({0, consumer["class_count"] // 2, consumer["class_count"] - 1})
    checks = 0
    for marginal_case in a["consumer_audit"]["marginals"]:
        for cid in ids:
            for x, y in AUDIT_POINTS:
                rates = [str(x), str(y)]
                expected = {
                    "question": marginal_case["name"],
                    "class_id": cid,
                    "rates": rates,
                    "outcomes": [
                        {
                            "value": atom["value"],
                            "probability": str(evaluate(atom["coefficients"], x, y)),
                        }
                        for atom in marginal_case["rows"][cid]["outcomes"]
                    ],
                }
                for module in (direct, reference):
                    require_same_wire(
                        module.predict(consumer, marginal_case["name"], cid, rates),
                        expected,
                        "public summary-only prediction",
                    )
                    checks += 1
    rejected = []
    for name in a["consumer_audit"]["nonmeasurable_questions"]:
        for module in (direct, reference):
            try:
                module.predict(consumer, name, 0, ["1/2", "1/2"])
            except (TypeError, ValueError):
                pass
            else:
                raise ValueError("nonmeasurable observable accepted")
        rejected.append(name)
    return {
        "public_class_ids": ids,
        "public_rate_points": len(AUDIT_POINTS),
        "public_prediction_calls": checks,
        "nonmeasurable_questions_rejected": rejected,
        "fine_records_supplied_to_predict": False,
        "verified": True,
    }


def run_suite():
    direct = load("qr05p_capture_direct", "closure.py")
    reference = load("qr05p_capture_reference", "reference_qr05p.py")
    problem = fixtures()[0]
    a, b = direct.analyze(problem), reference.analyze(problem)
    require_wire(a)
    require_wire(b)
    require(
        len(canonical(a)) <= MAX_WORKING_BYTES and len(canonical(b)) <= MAX_WORKING_BYTES,
        "working output cap",
    )
    require_same_wire(a, b, "independent complete P outputs differ")
    del b
    audit = check_analysis(a, problem["model"])
    bridge = prior_bridge(a, problem["model"])
    controls = public_controls(direct, reference, a)
    rejected = []
    for index, invalid in enumerate(invalid_fixtures()):
        for module in (direct, reference):
            try:
                module.analyze(invalid)
            except (TypeError, ValueError):
                pass
            else:
                raise ValueError("invalid P problem accepted")
        rejected.append(index)
    suite = {
        "input": problem,
        "analysis": a,
        "audit": audit,
        "prior_bridge": bridge,
        "controls": controls,
        "rejected_fixture_indices": rejected,
        "research_base_commit": BASE_COMMIT,
        "claim": "Coarsest strongly closed C-refinement on the supplied pinned O domain and polynomial law; certify only measurable summary-consumer questions.",
        "coarsest_closed_C_refinement_verified": True,
        "H_equal_to_coarsest_refinement": a["refinement"]["comparison"]["same_memberships_as_H"],
        "input_is_declared_prior_observation_projection": True,
        "unrestricted_minimality_claimed": False,
        "minimum_memory_or_runtime_claimed": False,
        "unseen_domain_membership_from_matching_H_key": False,
        "all_labeled_graph_queries_supported": False,
        "adaptive_or_correlated_stages_tested": False,
        "empirical_data_used": False,
        "ret_integration_tested": False,
        "lean_proof_completed": False,
        "gravity_derived": False,
        "physical_time_identified_with_thinning": False,
        "prior_source_alias_universe_regenerated": False,
        "entire_O_suite_replayed": False,
        "bounds": {
            "states": 2470,
            "fine_atoms": 99180,
            "transition_degree": [3, 3],
            "composition_degree": [3, 3, 3, 3],
            "exact_component_bits": 4096,
            "working_output_bytes": MAX_WORKING_BYTES,
            "artifact_bytes": MAX_CAPTURE_BYTES,
        },
        "totals": {
            **a["counts"],
            "rejected_fixtures": len(rejected),
            "public_prediction_calls": controls["public_prediction_calls"],
        },
    }
    require(retained_bits(suite) <= 4096, "retained exact component cap")
    require_wire(suite)
    return suite


if __name__ == "__main__":
    main()
