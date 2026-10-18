"""QR-05R deletion-profile audit, capture, and read-only replay.

Generic lifecycle, chain-support and matrix-coefficient audit utilities are
locally carried from the O/P runner lineage. Independent reconstruction
never imports either executor; run_suite dispatches them only for comparison.
The raw Q model is an explicit input dependency; source aliases are not regenerated.
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
SCHEMA = "det8-qr05r-results-v1"
BASE_COMMIT = "7598cdfbf3b4a17ad27c1187973108ba74fea525"
SOURCES = (
    "README.md",
    "deletion_profile.py",
    "reference_qr05r.py",
    "study.py",
    "test_qr05r.py",
    "test_capture.py",
)

PRIORS = {
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
    require(type(states) is list and 2 <= len(states) <= 4447, "state bound")
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
    require(atoms <= 168388, "fine atom cap")
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


Q_PRIOR = "qr-05q-three-layer-portability-2026-09-06/results.json"


def fixtures():
    q = prior_json(Q_PRIOR)["suite"]["analysis"]
    model = {key: q["domain"][key] for key in ("frames", "states")}
    return [
        {
            "schema_version": "det8-qr05r-problem-v1",
            "family": "qr05r_deletion_profile",
            "model": model,
        }
    ]


def invalid_fixtures():
    return [
        None,
        [],
        {},
        True,
        1,
        {"schema_version": "det8-qr05r-problem-v1", "family": "other"},
        {
            "schema_version": "det8-qr05r-problem-v1",
            "family": "qr05r_deletion_profile",
            "model": {},
        },
        {**fixtures()[0], "extra": 0},
    ]


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def rank_from_key(key):
    b = key[1]
    return [b[0][1][1][0], b[0][1][0][1]]


@memoize
def inverse_counts(O, E, table):
    result = zero()
    for o in range(O + 1):
        for e in range(E + 1):
            result[o][e] = sum(
                table[i][j] * comb(O - i, o - i) * comb(E - j, e - j)
                for i in range(o + 1)
                for j in range(e + 1)
            )
    return tuple(tuple(row) for row in result)


def profile_census(model, features, fine, partition):
    result = []
    for state, feature, row in zip(model["states"], features, fine, strict=True):
        counts = {}
        for atom in row["transitions"]:
            sid = atom["target_state"]
            h = partition["state_classes"][sid]
            sizes = features[sid]["color_sizes"]
            require(sizes == rank_from_key(partition["classes"][h]["key"]), "H successor colors")
            if h not in counts:
                counts[h] = {"target_class": h, "retained_color_sizes": sizes, "multiplicity": 0}
            require(
                counts[h]["retained_color_sizes"] == sizes, "target has more than one color rank"
            )
            counts[h]["multiplicity"] += 1
        parent = feature["color_sizes"]
        h = partition["state_classes"][state["state_id"]]
        require(parent == rank_from_key(partition["classes"][h]["key"]), "H parent colors")
        rank_totals = zero()
        for atom in counts.values():
            o, e = atom["retained_color_sizes"]
            require(
                0 < atom["multiplicity"] <= choose(parent[0], o) * choose(parent[1], e) <= 9,
                "positive bounded subset multiplicity",
            )
            rank_totals[o][e] += atom["multiplicity"]
        require(
            rank_totals
            == [[choose(parent[0], o) * choose(parent[1], e) for e in range(4)] for o in range(4)],
            "rankwise binomial normalization",
        )
        require(sum(map(sum, rank_totals)) == 2 ** sum(parent), "total subset count")
        result.append(
            {
                "state_id": state["state_id"],
                "parent_color_sizes": parent,
                "transitions": [counts[h] for h in sorted(counts)],
            }
        )
    return result


def expand_profile(row):
    O, E = row["parent_color_sizes"]
    return [
        {
            "target_class": atom["target_class"],
            "coefficients": [
                [atom["multiplicity"] * c for c in line]
                for line in kernel(O, E, *atom["retained_color_sizes"])
            ],
        }
        for atom in row["transitions"]
    ]


def closure_profiles(partition, profiles):
    witness, comparisons = None, 0
    for group in partition["classes"]:
        left = group["members"][0]
        lhs = profiles[left]
        counts = {a["target_class"]: a for a in lhs["transitions"]}
        for right in group["members"][1:]:
            comparisons += 1
            rhs = profiles[right]
            require(
                lhs["parent_color_sizes"] == rhs["parent_color_sizes"],
                "closure requires equal parent colors",
            )
            other = {a["target_class"]: a for a in rhs["transitions"]}
            unequal = [
                h for h in sorted(counts.keys() | other.keys()) if counts.get(h) != other.get(h)
            ]
            if unequal and witness is None:
                h = unequal[0]
                la, ra = counts.get(h), other.get(h)
                sizes = (la or ra)["retained_color_sizes"]
                require(
                    all(a is None or a["retained_color_sizes"] == sizes for a in (la, ra)),
                    "one target class must have a fixed rank",
                )
                lc, rc = la["multiplicity"] if la else 0, ra["multiplicity"] if ra else 0
                table = kernel(*lhs["parent_color_sizes"], *sizes)
                point = next(
                    pair for pair in product(GRID, repeat=2) if evaluate(table, *pair) * (lc - rc)
                )
                witness = {
                    "class_id": group["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "target_class": h,
                    "retained_color_sizes": sizes,
                    "left_multiplicity": lc,
                    "right_multiplicity": rc,
                    "first_distinguishing_rates": [str(x) for x in point],
                }
    closure = {
        "closed": witness is None,
        "classes_checked": len(partition["classes"]),
        "member_comparisons": comparisons,
        "witness": witness,
    }
    classes = []
    if witness is None:
        for group in partition["classes"]:
            row = profiles[group["members"][0]]
            classes.append(
                {
                    "class_id": group["class_id"],
                    "representative_state": row["state_id"],
                    "parent_color_sizes": row["parent_color_sizes"],
                    "transitions": row["transitions"],
                }
            )
    return closure, classes


def count_composition(classes):
    maps = [{a["target_class"]: a for a in row["transitions"]} for row in classes]
    rows = []
    for row in classes:
        O, E = row["parent_color_sizes"]
        pairs = {}
        reachable = set()
        for middle in row["transitions"]:
            h = middle["target_class"]
            k, l = middle["retained_color_sizes"]
            require(classes[h]["parent_color_sizes"] == [k, l], "intermediate class colors")
            for final in classes[h]["transitions"]:
                g = final["target_class"]
                reachable.add(g)
                grade = (g, k, l)
                pairs[grade] = pairs.get(grade, 0) + middle["multiplicity"] * final["multiplicity"]
        direct = maps[row["class_id"]]
        require(reachable == set(direct), "nested/direct structural targets")
        nested = 0
        for g in sorted(reachable):
            m, n = direct[g]["retained_color_sizes"]
            require(classes[g]["parent_color_sizes"] == [m, n], "final class colors")
            for k, l in product(range(4), repeat=2):
                actual = pairs.get((g, k, l), 0)
                expected = direct[g]["multiplicity"] * choose(O - m, k - m) * choose(E - n, l - n)
                require(actual == expected, "nested subset counting identity")
                nested += actual
        require(nested == 3 ** (O + E), "three choices per eligible nested vertex")
        rows.append(
            {
                "class_id": row["class_id"],
                "final_targets": len(direct),
                "rank_cells": 16 * len(direct),
                "nested_pairs": nested,
                "max_abs_residual": 0,
            }
        )
    return {
        "verified": True,
        "rows": rows,
        "totals": {
            key: sum(row[key] for row in rows)
            for key in ("final_targets", "rank_cells", "nested_pairs", "max_abs_residual")
        },
    }


def convert_and_evaluate(features, fine, pushed, profiles, classes):
    atoms, rate_evaluations = 0, 0
    for profile, law in zip(profiles, pushed, strict=True):
        expanded = expand_profile(profile)
        require_same_wire(expanded, law["transitions"], "profile-to-power exact expansion")
        O, E = profile["parent_color_sizes"]
        totals = [F(0)] * len(AUDIT_POINTS)
        for atom, edge in zip(profile["transitions"], expanded, strict=True):
            o, e = atom["retained_color_sizes"]
            coefficients = tuple(tuple(line) for line in edge["coefficients"])
            count_table = inverse_counts(O, E, coefficients)
            expected_counts = zero()
            expected_counts[o][e] = atom["multiplicity"]
            require(
                count_table == tuple(tuple(line) for line in expected_counts),
                "complete inverse basis",
            )
            direct = tuple(atom["multiplicity"] * p for p in direct_rates(O, E, o, e))
            require(eval_rates(coefficients) == direct, "positive expression/power evaluation")
            require(all(p >= 0 for p in direct), "negative positive-basis probability")
            for point, value in enumerate(direct):
                totals[point] += value
            atoms += 1
            rate_evaluations += len(direct)
        require(all(p == 1 for p in totals), "profile rate normalization")
    quotient = [
        {
            "class_id": row["class_id"],
            "representative_state": row["representative_state"],
            "transitions": expand_profile(row),
        }
        for row in classes
    ]
    conversion = {
        "fine_kernel_sha256": digest(canonical(fine)),
        "pushed_rows_sha256": digest(canonical(pushed)),
        "quotient_rows_sha256": digest(canonical(quotient)) if classes else None,
        "profile_cells": 16 * atoms,
        "power_cells": 16 * atoms,
        "normalization_cells": 16 * len(features),
        "max_abs_residual": 0,
    }
    evaluation = {
        "rate_points": len(AUDIT_POINTS),
        "profile_atoms": atoms,
        "probability_evaluations": rate_evaluations,
        "normalization_rows": len(AUDIT_POINTS) * len(profiles),
        "max_abs_residual": 0,
    }
    return conversion, evaluation


def expected_analysis(model):
    features, partitions, fine, _ = reconstruct_model(model)
    h = partitions["H"]
    profiles = profile_census(model, features, fine, h)
    closure, classes = closure_profiles(h, profiles)
    pushed = push_rows(fine, h["state_classes"])
    conversion, evaluation = convert_and_evaluate(features, fine, pushed, profiles, classes)
    composition = count_composition(classes) if closure["closed"] else None
    return {
        "model_sha256": digest(canonical(model)),
        "features": features,
        "partition": h,
        "profiles": profiles,
        "closure": closure,
        "class_profiles": classes,
        "conversion": conversion,
        "composition": composition,
        "evaluation": evaluation,
        "counts": {
            "states": len(features),
            "classes": len(h["classes"]),
            "fine_atoms": sum(len(r["transitions"]) for r in fine),
            "profile_atoms": sum(len(r["transitions"]) for r in profiles),
            "class_profile_atoms": sum(len(r["transitions"]) for r in classes),
        },
    }


@lru_cache(maxsize=2)
def expected_analysis_bytes(model_bytes):
    return canonical(expected_analysis(json.loads(model_bytes)))


def check_analysis(a, model):
    require_wire(model)
    validate_model(model)
    require_wire(a)
    require(retained_bits(a) <= 4096, "exact component cap")
    raw = canonical(a)
    require(len(raw) <= MAX_WORKING_BYTES, "working output cap")
    require(
        raw == expected_analysis_bytes(canonical(model)), "independent full reconstruction differs"
    )
    return {
        "raw_observations_reconstructed": True,
        "all_features_and_H_fibers_checked": True,
        "all_subset_profiles_and_power_laws_checked": True,
        "all_rank_normalizations_checked": True,
        "all_nested_counts_checked": True,
        "analysis_sha256": digest(raw),
    }


def prior_bridge(a, model):
    q = prior_json(Q_PRIOR)["suite"]["analysis"]
    require_same_wire(
        model, {k: q["domain"][k] for k in ("frames", "states")}, "exact Q raw projection"
    )
    require_same_wire(a["features"], q["features"], "Q features")
    require_same_wire(a["partition"], q["partition"], "Q actual H fibers")
    require(
        a["conversion"]["fine_kernel_sha256"] == q["fine_kernel"]["sha256"], "Q full fine digest"
    )
    pushed = [
        {"state_id": row["state_id"], "transitions": expand_profile(row)} for row in a["profiles"]
    ]
    require_same_wire(pushed, q["pushed_rows"], "all Q pushed coefficients")
    require(digest(canonical(pushed)) == a["conversion"]["pushed_rows_sha256"], "Q pushed digest")
    require_same_wire(
        {k: a["closure"][k] for k in ("closed", "classes_checked", "member_comparisons")},
        {k: q["closure"][k] for k in ("closed", "classes_checked", "member_comparisons")},
        "Q closure comparisons",
    )
    require(
        a["closure"]["witness"] is None and q["closure"]["witness"] is None, "certified Q closure"
    )
    quotient = [
        {
            "class_id": row["class_id"],
            "representative_state": row["representative_state"],
            "transitions": expand_profile(row),
        }
        for row in a["class_profiles"]
    ]
    require_same_wire(quotient, q["quotient_rows"], "complete Q quotient")
    require(
        a["conversion"]["quotient_rows_sha256"] == digest(canonical(quotient)), "Q quotient digest"
    )
    return {
        "prior_artifact": Q_PRIOR,
        "declared_raw_model_input_dependency": True,
        "source_alias_universe_regenerated": False,
        "matched_states": len(model["states"]),
        "all_features_equal": True,
        "actual_H_fibers_equal": True,
        "all_fine_pushed_quotient_laws_equal": True,
        "Q_four_variable_certificate_recomputed": False,
        "expanded_minimality_tested": False,
    }


def mathematical_controls(a):
    monomials = 0
    for O, E in product(range(4), repeat=2):
        for i in range(O + 1):
            for j in range(E + 1):
                power = zero()
                power[i][j] = 1
                counts = inverse_counts(O, E, tuple(tuple(r) for r in power))
                expanded = zero()
                for o in range(O + 1):
                    for e in range(E + 1):
                        add_table(expanded, kernel(O, E, o, e), counts[o][e])
                require(expanded == power, "full bounded basis inverse")
                monomials += 1
    event_one, event_two = zero(), zero()
    add_table(event_one, kernel(1, 0, 1, 0))
    add_table(event_two, kernel(2, 0, 1, 0))
    add_table(event_two, kernel(2, 0, 2, 0))
    require(event_one == event_two, "degree-elevation law")
    require(
        inverse_counts(1, 0, tuple(tuple(r) for r in event_one))
        != inverse_counts(2, 0, tuple(tuple(r) for r in event_two)),
        "degree-elevation profiles differ",
    )
    return {
        "basis_monomials": monomials,
        "basis_coefficient_cells": 16 * monomials,
        "degree_elevation_equal_laws_different_profiles": True,
        "degree_elevation_control_is_outside_H_premises": True,
        "parent_successor_colors_checked": len(a["features"]),
        "all_structural_zero_rate_atoms_retained": True,
    }


def payload(row):
    return {k: row[k] for k in ("parent_color_sizes", "transitions")}


def public_controls(direct, reference, a):
    calls = 0
    for row in a["class_profiles"]:
        p = payload(row)
        coefficients = expand_profile(row)
        before = canonical(p)
        for index, (x, y) in enumerate(AUDIT_POINTS):
            rates = [str(x), str(y)]
            expected = {
                "rates": rates,
                "outcomes": [
                    {
                        "target_class": edge["target_class"],
                        "probability": str(
                            eval_rates(tuple(tuple(r) for r in edge["coefficients"]))[index]
                        ),
                    }
                    for edge in coefficients
                ],
            }
            for route in (direct, reference):
                result = route.evaluate_row(p, rates)
                require_wire(result)
                require_same_wire(
                    result, expected, "public positive row differs from independent power law"
                )
                require(canonical(p) == before, "public profile mutated")
                calls += 1
    single = {
        "parent_color_sizes": [1, 0],
        "transitions": [
            {"target_class": 0, "retained_color_sizes": [0, 0], "multiplicity": 1},
            {"target_class": 1, "retained_color_sizes": [1, 0], "multiplicity": 1},
        ],
    }
    bad_rates = [
        None,
        [],
        [0, "1"],
        ["1.0", "1"],
        ["1/0", "1"],
        ["2/2", "1"],
        ["-1/2", "1"],
        ["3/2", "1"],
        ["1e999999999", "1"],
        ["1" * 3001, "1"],
    ]
    bad_payloads = [
        None,
        {},
        {**single, "extra": 1},
        {"parent_color_sizes": [True, 0], "transitions": single["transitions"]},
        {"parent_color_sizes": [1, 0], "transitions": single["transitions"][:1]},
        {"parent_color_sizes": [1, 0], "transitions": list(reversed(single["transitions"]))},
    ]
    rejected = 0
    for route in (direct, reference):
        for p, rates in [(single, r) for r in bad_rates] + [
            (p, ["1/2", "0"]) for p in bad_payloads
        ]:
            try:
                route.evaluate_row(p, rates)
            except ValueError:
                rejected += 1
            else:
                raise ValueError("invalid probability-row input accepted")
    return {
        "calls": calls,
        "classes": len(a["class_profiles"]),
        "rate_points": 22,
        "invalid_calls_rejected": rejected,
        "hidden_model_dependency": False,
        "structural_zero_outcomes_retained": True,
    }


def run_suite():
    direct = load("_qr05r_direct", "deletion_profile.py")
    reference = load("_qr05r_reference", "reference_qr05r.py")
    problem = fixtures()[0]
    before = canonical(problem)
    a = direct.analyze(problem)
    require(canonical(problem) == before, "primary input mutation")
    b = reference.analyze(problem)
    require(canonical(problem) == before, "reference input mutation")
    require_same_wire(a, b, "independent executor outputs differ")
    audit = check_analysis(a, problem["model"])
    bridge = prior_bridge(a, problem["model"])
    controls = mathematical_controls(a)
    public = public_controls(direct, reference, a)
    rejected = 0
    for route in (direct, reference):
        for bad in invalid_fixtures():
            try:
                route.analyze(bad)
            except ValueError:
                rejected += 1
            else:
                raise ValueError("invalid analyze input accepted")
    return {
        "problem": problem,
        "analysis": a,
        "independent_route_equal": True,
        "independent_audit": audit,
        "prior_bridge": bridge,
        "controls": controls,
        "public_controls": public,
        "invalid_inputs_rejected": rejected,
        "totals": {
            **a["counts"],
            "profile_closed": a["closure"]["closed"],
            "member_comparisons": a["closure"]["member_comparisons"],
            "profile_cells": a["conversion"]["profile_cells"],
            "power_cells": a["conversion"]["power_cells"],
            "normalization_cells": a["conversion"]["normalization_cells"],
            "composition_rank_cells": a["composition"]["totals"]["rank_cells"]
            if a["composition"]
            else 0,
            "nested_pairs": a["composition"]["totals"]["nested_pairs"] if a["composition"] else 0,
            "probability_evaluations": a["evaluation"]["probability_evaluations"],
            "public_calls": public["calls"],
        },
    }


if __name__ == "__main__":
    main()
