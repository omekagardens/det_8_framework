"""QR-05T deletion-profile audit, capture, and read-only replay.

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
SCHEMA = "det8-qr05t-results-v1"
BASE_COMMIT = "814203ed6f386cc27e1351d0427ddfe89fadbc18"
SOURCES = (
    "README.md",
    "local_refinement.py",
    "reference_qr05t.py",
    "study.py",
    "test_qr05t.py",
    "test_capture.py",
)

PRIORS = {
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
    safely above every valid S schema, including evidence envelopes.
    """
    active, completed = set(), {}
    pending = [(value, 0, False)]
    while pending:
        item, depth, leaving = pending.pop()
        identity = id(item)
        if leaving:
            children = item if type(item) is list else item.values()
            nodes, height = 1, 1
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
        if item is None or type(item) in (bool, int, str):
            continue
        require(type(item) in (list, dict), "mathematical suite must use native exact JSON types")
        require(identity not in active, "cyclic wire container")
        require(depth <= 128, "wire exceeds bounded schema depth")
        if identity in completed:
            require(depth + completed[identity][1] - 1 <= 128, "wire exceeds bounded schema depth")
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
            atoms.append({"target_state": registry[key], "coefficients": [list(r) for r in table]})
        atoms.sort(key=lambda atom: atom["target_state"])
        total = zero()
        for atom in atoms:
            add_table(total, atom["coefficients"])
        require(total == [[1, 0, 0, 0], [0] * 4, [0] * 4, [0] * 4], "fine normalization")
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
    require(len(partitions["H"]["classes"]) <= 512, "H class cap")
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


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def rank_from_key(key):
    b = key[1]
    return [b[0][1][1][0], b[0][1][0][1]]


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


def edge_map(atoms):
    return {a["target_class"]: a["multiplicity"] for a in atoms}


def compose_word(classes, sid, word):
    mass = {sid: 1}
    for color in word:
        next_mass = {}
        for h, multiplicity in mass.items():
            for atom in classes[h][color]:
                g = atom["target_class"]
                next_mass[g] = next_mass.get(g, 0) + multiplicity * atom["multiplicity"]
        mass = next_mass
    return mass


def audit_local_profiles(classes, profiles):
    """Ground-truth profile audit: never derive its A values from local operators."""
    require(len(classes) == len(profiles), "profile/class count")
    k = len(classes)
    maps = [edge_map(row["transitions"]) for row in profiles]
    certificate = {
        "target_cells": k * k,
        "base_cells": 0,
        "recurrence_cells": 0,
        "normalization_cells": 16 * k,
        "max_abs_residual": 0,
    }
    operator_rows = []
    for s, row in enumerate(classes):
        O, E = row["parent_color_sizes"]
        for color, coordinate in (("odd", 0), ("even", 1)):
            require(sum(a["multiplicity"] for a in row[color]) == (O, E)[coordinate], "local mass")
            for atom in row[color]:
                target = classes[atom["target_class"]]
                expected_rank = [O, E]
                expected_rank[coordinate] -= 1
                require(
                    target["frame_id"] == row["frame_id"]
                    and target["parent_color_sizes"] == expected_rank,
                    "local edge frame/rank",
                )
        totals = zero()
        for g, target in enumerate(classes):
            m, n = target["parent_color_sizes"]
            count = maps[s].get(g, 0)
            compatible = target["frame_id"] == row["frame_id"] and m <= O and n <= E
            if not compatible:
                require(count == 0, "incompatible target zero")
                continue
            require(0 <= count <= choose(O, m) * choose(E, n), "bounded profile count")
            totals[m][n] += count
            if (m, n) == (O, E):
                certificate["base_cells"] += 1
                require(count == int(s == g), "full-rank delta")
            for color, divisor in (("odd", O - m), ("even", E - n)):
                if divisor > 0:
                    certificate["recurrence_cells"] += 1
                    numerator = sum(
                        a["multiplicity"] * maps[a["target_class"]].get(g, 0) for a in row[color]
                    )
                    require(
                        numerator % divisor == 0 and numerator == divisor * count,
                        "exact local recurrence",
                    )
        require(
            totals == [[choose(O, m) * choose(E, n) for n in range(4)] for m in range(4)],
            "all rank normalizations",
        )
        words = [
            compose_word(classes, s, word)
            for word in (("odd", "odd"), ("even", "even"), ("odd", "even"), ("even", "odd"))
        ]
        expected = []
        for m, n, factor in ((O - 2, E, 2), (O, E - 2, 2), (O - 1, E - 1, 1)):
            expected.append(
                {
                    g: factor * c
                    for g, c in maps[s].items()
                    if classes[g]["parent_color_sizes"] == [m, n]
                }
            )
        require(
            words == [expected[0], expected[1], expected[2], expected[2]], "complete operator maps"
        )
        require(
            [sum(w.values()) for w in words] == [O * (O - 1), E * (E - 1), O * E, O * E],
            "word row masses",
        )
        oo, ee, mixed = map(len, expected)
        operator_rows.append(
            {
                "class_id": s,
                "odd_odd_targets": oo,
                "even_even_targets": ee,
                "mixed_targets": mixed,
                "coefficient_cells": oo + ee + 2 * mixed,
                "odd_odd_pairs": O * (O - 1),
                "even_even_pairs": E * (E - 1),
                "mixed_pairs": O * E,
                "max_abs_residual": 0,
            }
        )
    totals = {
        key: sum(r[key] for r in operator_rows) for key in operator_rows[0] if key != "class_id"
    }
    return certificate, {"verified": True, "rows": operator_rows, "totals": totals}


S_PRIOR = "qr-05s-local-deletion-2026-09-06/results.json"


def fixtures():
    return [
        {
            "schema_version": "det8-qr05t-problem-v1",
            "family": "qr05t_local_refinement",
            "model": prior_json(S_PRIOR)["suite"]["problem"]["model"],
        }
    ]


def raw_counts(model, features, fine):
    registry = validate_model(model)
    local, full = [], []
    for state, feature, row in zip(model["states"], features, fine, strict=True):
        common = {
            "state_id": state["state_id"],
            "frame_id": state["frame_id"],
            "parent_color_sizes": feature["color_sizes"],
        }
        full.append(
            {
                **common,
                "transitions": [
                    {"target_state": a["target_state"], "multiplicity": 1}
                    for a in row["transitions"]
                ],
            }
        )
        colors = [[], []]
        eligible = model["frames"][state["frame_id"]]["eligible"]
        for v in state["kept"]:
            if v not in eligible:
                continue
            kept = [u for u in state["kept"] if u != v]
            target = registry[identity(state["frame_id"], kept, induced_past(state, kept))]
            colors[0 if v % 2 else 1].append({"target_state": target, "multiplicity": 1})
        local.append(
            {
                **common,
                **{
                    c: sorted(atoms, key=lambda a: a["target_state"])
                    for c, atoms in zip(("odd", "even"), colors, strict=True)
                },
            }
        )
    require(sum(sum(r["parent_color_sizes"]) for r in local) <= 26682, "fine local choice cap")
    for row in local:
        source = row["state_id"]
        for color, coordinate in (("odd", 0), ("even", 1)):
            rank = list(row["parent_color_sizes"])
            rank[coordinate] -= 1
            wanted = [
                a
                for a in full[source]["transitions"]
                if full[a["target_state"]]["parent_color_sizes"] == rank
            ]
            require_same_wire(wanted, row[color], "one-deletion slices of full raw subsets")
    return local, full


def ranked_groups(rows, vector):
    require(len(rows) == len(vector), "partition domain")
    groups = groups_from_vector(vector)
    require(1 <= len(groups) <= 512, "partition class cap")
    for group in groups:
        rep = rows[group["members"][0]]
        for sid in group["members"]:
            require(
                rows[sid]["frame_id"] == rep["frame_id"]
                and rows[sid]["parent_color_sizes"] == rep["parent_color_sizes"],
                "partition must fix rank and frame",
            )
    return groups


def aggregate_rows(rows, vector, mode):
    groups = ranked_groups(rows, vector)
    result = []
    for row in rows:
        common = {"state_id": row["state_id"], "parent_color_sizes": row["parent_color_sizes"]}
        if mode == "local":
            value = {**common, "frame_id": row["frame_id"]}
            for coordinate, color in enumerate(("odd", "even")):
                totals = {}
                for atom in row[color]:
                    target = atom["target_state"]
                    expected = list(row["parent_color_sizes"])
                    expected[coordinate] -= 1
                    require(
                        rows[target]["frame_id"] == row["frame_id"]
                        and rows[target]["parent_color_sizes"] == expected,
                        "fine local edge",
                    )
                    h = vector[target]
                    totals[h] = totals.get(h, 0) + atom["multiplicity"]
                require(sum(totals.values()) == row["parent_color_sizes"][coordinate], "local mass")
                value[color] = [
                    {"target_class": h, "multiplicity": totals[h]} for h in sorted(totals)
                ]
        else:
            totals, rank_totals = {}, zero()
            O, E = row["parent_color_sizes"]
            for atom in row["transitions"]:
                target = atom["target_state"]
                rank = rows[target]["parent_color_sizes"]
                require(
                    rows[target]["frame_id"] == row["frame_id"] and rank[0] <= O and rank[1] <= E,
                    "full fine target rank/frame",
                )
                require(rank != [O, E] or target == row["state_id"], "full-rank raw self delta")
                h = vector[target]
                totals[h] = totals.get(h, 0) + atom["multiplicity"]
                rank_totals[rank[0]][rank[1]] += atom["multiplicity"]
            require(
                rank_totals == [[choose(O, m) * choose(E, n) for n in range(4)] for m in range(4)],
                "full raw rank normalization",
            )
            value = {
                **common,
                "transitions": [
                    {
                        "target_class": h,
                        "retained_color_sizes": rows[groups[h]["members"][0]]["parent_color_sizes"],
                        "multiplicity": totals[h],
                    }
                    for h in sorted(totals)
                ],
            }
        result.append(value)
    return result


def signatures(rows, mode):
    return [canonical([r["odd"], r["even"]] if mode == "local" else r["transitions"]) for r in rows]


def trace_counts(rows, initial, mode):
    vector, rounds = list(initial), []
    bound = min(6, len(rows) - len(ranked_groups(rows, vector)))
    while True:
        groups = ranked_groups(rows, vector)
        aggregated = aggregate_rows(rows, vector, mode)
        sig = signatures(aggregated, mode)
        registry, following = {}, []
        for sid, value in enumerate(sig):
            key = (vector[sid], value)
            if key not in registry:
                registry[key] = len(registry)
            following.append(registry[key])
        new_groups = ranked_groups(rows, following)
        compared = 0
        all_equal = True
        for group in groups:
            left = group["members"][0]
            for right in group["members"][1:]:
                compared += 1
                equal = sig[left] == sig[right]
                all_equal = equal and all_equal
        stable = following == vector
        require(stable == all_equal, "all-member stability")
        separations = []
        for child in new_groups:
            right = child["members"][0]
            parent = vector[right]
            left = groups[parent]["members"][0]
            if right == left:
                continue
            base = {
                "parent_class_id": parent,
                "child_class_id": child["class_id"],
                "left_state": left,
                "right_state": right,
            }
            for color in ("odd", "even") if mode == "local" else ("transitions",):
                lhs, rhs = edge_map(aggregated[left][color]), edge_map(aggregated[right][color])
                differences = [
                    h for h in sorted(lhs.keys() | rhs.keys()) if lhs.get(h, 0) != rhs.get(h, 0)
                ]
                if differences:
                    h = differences[0]
                    if mode == "local":
                        base["color"] = color
                    else:
                        base["retained_color_sizes"] = rows[groups[h]["members"][0]][
                            "parent_color_sizes"
                        ]
                    base.update(
                        target_class=h,
                        left_multiplicity=lhs.get(h, 0),
                        right_multiplicity=rhs.get(h, 0),
                    )
                    separations.append(base)
                    break
            else:
                raise ValueError("split has no differing count")
        require(len(separations) == len(new_groups) - len(groups), "one witness per extra child")
        require(stable or len(new_groups) > len(groups), "strict splitting progress")
        atoms = sum(
            len(r[c])
            for r in aggregated
            for c in (("odd", "even") if mode == "local" else ("transitions",))
        )
        rounds.append(
            {
                "round_index": len(rounds),
                "state_classes": vector,
                "classes": groups,
                "rows_sha256": digest(canonical(aggregated)),
                "signature_atoms": atoms,
                "member_comparisons": compared,
                "stable": stable,
                "separations": separations,
            }
        )
        if stable:
            break
        require(len(rounds) <= bound, "rank-lowering strict-round bound")
        vector = following
    return {
        "mode": mode,
        "rounds": rounds,
        "strict_rounds": len(rounds) - 1,
        "state_classes": vector,
        "classes": groups,
        "counts": {
            "rounds": len(rounds),
            "signature_atoms": sum(r["signature_atoms"] for r in rounds),
            "member_comparisons": sum(r["member_comparisons"] for r in rounds),
            "separations": sum(len(r["separations"]) for r in rounds),
        },
    }


def partition_map(finer, coarser):
    require(len(finer) == len(coarser), "map domain")
    mapping = []
    for a, b in zip(finer, coarser, strict=True):
        if a == len(mapping):
            mapping.append(b)
        elif mapping[a] != b:
            return None
    return mapping


def constant_rows(rows, groups, mode):
    sig = signatures(rows, mode)
    closed, comparisons = True, 0
    for group in groups:
        left = group["members"][0]
        for right in group["members"][1:]:
            comparisons += 1
            equal = sig[left] == sig[right]
            closed = equal and closed
    return closed, comparisons


def expected_analysis(model):
    features, partitions, fine, _ = reconstruct_model(model)
    raw_local, raw_full = raw_counts(model, features, fine)
    C, H = partitions["C"], partitions["H"]
    local = trace_counts(raw_local, C["state_classes"], "local")
    full = trace_counts(raw_full, C["state_classes"], "full")
    vectors = [
        C["state_classes"],
        local["state_classes"],
        full["state_classes"],
        H["state_classes"],
    ]
    mappings = [[partition_map(a, b) for b in vectors] for a in vectors]
    require(local["state_classes"] == full["state_classes"], "local/full terminal fibers")
    aligned = []
    for index in range(max(len(local["rounds"]), len(full["rounds"]))):
        lv = local["rounds"][min(index, len(local["rounds"]) - 1)]["state_classes"]
        fv = full["rounds"][min(index, len(full["rounds"]) - 1)]["state_classes"]
        aligned.append(partition_map(fv, lv) is not None)
    require(all(aligned), "aligned full refinement dominates local")
    h_rows = aggregate_rows(raw_local, H["state_classes"], "local")
    h_closed, _ = constant_rows(h_rows, H["classes"], "local")
    require(not h_closed or mappings[3][1] is not None, "closed H must refine terminal")
    comparison = {
        "names": ["C", "L", "F", "H"],
        "refinement": [[m is not None for m in r] for r in mappings],
        "maps": {
            name: mappings[a][b]
            for name, a, b in [
                ("L_to_C", 1, 0),
                ("F_to_C", 2, 0),
                ("L_to_F", 1, 2),
                ("F_to_L", 2, 1),
                ("L_to_H", 1, 3),
                ("H_to_L", 3, 1),
            ]
        },
        "same_terminal_memberships": True,
        "same_memberships_as_H": mappings[1][3] is not None and mappings[3][1] is not None,
        "H_local_closed": h_closed,
        "aligned_full_refines_local": aligned,
    }
    groups, vector = local["classes"], local["state_classes"]
    local_rows = aggregate_rows(raw_local, vector, "local")
    profiles = aggregate_rows(raw_full, vector, "full")
    lc, comparisons = constant_rows(local_rows, groups, "local")
    fc, comparisons2 = constant_rows(profiles, groups, "full")
    require(lc and fc and comparisons == comparisons2, "terminal all-member closure")
    classes, class_profiles = [], []
    for group in groups:
        rep = group["members"][0]
        head = {"class_id": group["class_id"], "representative_state": rep}
        classes.append({**head, **{k: v for k, v in local_rows[rep].items() if k != "state_id"}})
        class_profiles.append(
            {**head, **{k: v for k, v in profiles[rep].items() if k != "state_id"}}
        )
    certificate, operators = audit_local_profiles(classes, class_profiles)
    reconstructed = [
        {"state_id": s, **{k: class_profiles[h][k] for k in ("parent_color_sizes", "transitions")}}
        for s, h in enumerate(vector)
    ]
    require_same_wire(reconstructed, profiles, "terminal reconstructed state profiles")
    pushed = push_rows(fine, vector)
    expanded = [{"state_id": r["state_id"], "transitions": expand_profile(r)} for r in profiles]
    require_same_wire(pushed, expanded, "terminal fine polynomial/profile expansion")
    quotient = [
        {
            "class_id": r["class_id"],
            "representative_state": r["representative_state"],
            "transitions": expand_profile(r),
        }
        for r in class_profiles
    ]
    atoms = sum(len(r["transitions"]) for r in profiles)
    for trace in (local, full):
        for round_ in trace["rounds"]:
            require(
                partition_map(round_["state_classes"], C["state_classes"]) is not None,
                "all rounds preserve C",
            )
            ranked_groups(raw_local, round_["state_classes"])
    return {
        "model_sha256": digest(canonical(model)),
        "features": features,
        "partitions": {"C": C, "H": H},
        "fine_kernel": {
            "sha256": digest(canonical(fine)),
            "atoms": sum(len(r["transitions"]) for r in fine),
        },
        "fine_deletions": {
            "sha256": digest(canonical(raw_local)),
            "atoms": sum(len(r[c]) for r in raw_local for c in ("odd", "even")),
            "choices": sum(sum(r["parent_color_sizes"]) for r in raw_local),
        },
        "local_refinement": local,
        "full_refinement": full,
        "comparison": comparison,
        "terminal": {
            "local_rows": classes,
            "class_profiles": class_profiles,
            "reconstruction": {"certificate": certificate, "operator_checks": operators},
            "closure": {
                "local_closed": lc,
                "full_closed": fc,
                "classes_checked": len(groups),
                "member_comparisons": comparisons,
            },
            "comparison": {
                "direct_profiles_sha256": digest(canonical(profiles)),
                "reconstructed_profiles_sha256": digest(canonical(reconstructed)),
                "pushed_rows_sha256": digest(canonical(pushed)),
                "quotient_rows_sha256": digest(canonical(quotient)),
                "profile_cells": 16 * atoms,
                "power_cells": 16 * atoms,
                "max_abs_residual": 0,
            },
        },
        "minimality": {
            "verified": True,
            "initial_partition": "C",
            "terminal_partition": "L",
            "all_rounds_refine_C": True,
            "all_rounds_rank_frame_measurable": True,
            "local_full_terminals_equal": True,
            "H_used_in_construction": False,
            "strict_round_bound": min(6, len(features) - len(C["classes"])),
            "relative_to_C": True,
            "arbitrary_partitions_enumerated": False,
        },
        "counts": {
            "states": len(features),
            "C_classes": len(C["classes"]),
            "H_classes": len(H["classes"]),
            "L_classes": len(local["classes"]),
            "F_classes": len(full["classes"]),
            "fine_atoms": sum(len(r["transitions"]) for r in fine),
            "fine_local_choices": sum(sum(r["parent_color_sizes"]) for r in raw_local),
            "local_strict_rounds": local["strict_rounds"],
            "full_strict_rounds": full["strict_rounds"],
            "terminal_local_atoms": sum(len(r[c]) for r in classes for c in ("odd", "even")),
            "terminal_profile_atoms": sum(len(r["transitions"]) for r in class_profiles),
        },
    }


@lru_cache(maxsize=2)
def expected_analysis_bytes(model_bytes):
    return canonical(expected_analysis(json.loads(model_bytes)))


def check_analysis(a, model):
    validate_model(model)  # Never allow canonical-content caching to hide native substitutions.
    require_wire(a)
    require(retained_bits(a) <= 4096, "component cap")
    raw = canonical(a)
    require(len(raw) <= MAX_WORKING_BYTES, "working cap")
    require(
        raw == expected_analysis_bytes(canonical(model)),
        "independent full T reconstruction differs",
    )
    return {
        "raw_model_reconstructed": True,
        "all_features_and_fibers_checked": True,
        "all_round_signatures_and_witnesses_reconstructed": True,
        "terminal_profiles_recurrences_and_operators_checked": True,
        "relative_minimality_premises_checked": True,
        "analysis_sha256": digest(raw),
    }


def prior_bridge(a, model):
    previous = prior_json(S_PRIOR)["suite"]
    s = previous["analysis"]
    require_same_wire(model, previous["problem"]["model"], "exact S raw input")
    require_same_wire(a["features"], s["features"], "S features")
    require_same_wire(a["partitions"]["H"], s["partition"], "actual S H fibers")
    require(a["fine_kernel"]["sha256"] == s["comparison"]["fine_kernel_sha256"], "S fine law")
    features, _, fine, _ = reconstruct_model(model)
    raw_local, raw_full = raw_counts(model, features, fine)
    require_same_wire(
        aggregate_rows(raw_local, s["partition"]["state_classes"], "local"),
        s["local_rows"],
        "S H local rows",
    )
    require(a["comparison"]["H_local_closed"] == s["local_closure"]["closed"], "S H closure")
    mapping = a["comparison"]["maps"]["H_to_L"]
    require(mapping is not None, "pinned closed H must refine L")
    projected = []
    h_vector = s["partition"]["state_classes"]
    for state, h in enumerate(h_vector):
        old = s["reconstruction"]["class_profiles"][h]
        counts = {}
        ranks = {}
        for atom in old["transitions"]:
            target = mapping[atom["target_class"]]
            counts[target] = counts.get(target, 0) + atom["multiplicity"]
            ranks[target] = atom["retained_color_sizes"]
        projected.append(
            {
                "state_id": state,
                "parent_color_sizes": old["parent_color_sizes"],
                "transitions": [
                    {"target_class": g, "retained_color_sizes": ranks[g], "multiplicity": counts[g]}
                    for g in sorted(counts)
                ],
            }
        )
    require_same_wire(
        projected,
        aggregate_rows(raw_full, a["local_refinement"]["state_classes"], "full"),
        "all S profiles projected through verified H-to-L map",
    )
    require(
        digest(canonical(projected)) == a["terminal"]["comparison"]["direct_profiles_sha256"],
        "projected S complete profile digest",
    )
    return {
        "prior_artifact": S_PRIOR,
        "declared_raw_model_input_dependency": True,
        "source_alias_universe_regenerated": False,
        "matched_states": len(features),
        "all_features_equal": True,
        "actual_H_fibers_equal": True,
        "fine_kernel_equal": True,
        "H_local_rows_equal": True,
        "terminal_profiles_equal_after_H_map": True,
        "H_to_L_map_used": True,
        "H_equality_assumed": False,
        "P_minimality_or_consumer_replayed": False,
        "R_probability_helper_recomputed": False,
        "Q_four_variable_certificate_recomputed": False,
    }


def local_payload(rows, vector):
    return {"schema_version": "det8-qr05t-local-v1", "rows": rows, "state_classes": vector}


def constructor_payload(rows):
    return {
        "schema_version": "det8-qr05s-local-v1",
        "classes": [
            {k: r[k] for k in ("class_id", "frame_id", "parent_color_sizes", "odd", "even")}
            for r in rows
        ],
    }


def constructor_output(terminal):
    return {
        "profiles": [
            {k: r[k] for k in ("class_id", "parent_color_sizes", "transitions")}
            for r in terminal["class_profiles"]
        ],
        **terminal["reconstruction"],
    }


def synthetic_controls():
    def row(i, rank, edges):
        return {
            "state_id": i,
            "frame_id": 0,
            "parent_color_sizes": [rank, 0],
            "odd": [{"target_state": j, "multiplicity": n} for j, n in edges],
            "even": [],
        }

    multiround = [
        row(0, 2, [(2, 2)]),
        row(1, 2, [(3, 2)]),
        row(2, 1, [(4, 1)]),
        row(3, 1, [(5, 1)]),
        row(4, 0, []),
        row(5, 0, []),
    ]
    weighted = [
        row(0, 3, [(2, 1), (3, 2)]),
        row(1, 3, [(2, 2), (3, 1)]),
        row(2, 2, [(4, 2)]),
        row(3, 2, [(4, 2)]),
        row(4, 1, [(5, 1)]),
        row(5, 0, []),
    ]
    preserve = [row(0, 0, []), row(1, 0, [])]
    result = []
    for name, rows, initial in [
        ("multiround", multiround, [0, 0, 1, 1, 2, 3]),
        ("weighted", weighted, [0, 0, 1, 2, 3, 4]),
        ("preserve", preserve, [0, 1]),
    ]:
        full = []
        for source, row_ in enumerate(rows):
            current, counts, factorial = {source: 1}, {source: 1}, 1
            for depth in range(1, row_["parent_color_sizes"][0] + 1):
                following = {}
                for j, weight in current.items():
                    for edge in rows[j]["odd"]:
                        h = edge["target_state"]
                        following[h] = following.get(h, 0) + weight * edge["multiplicity"]
                factorial *= depth
                for j, count in following.items():
                    require(count % factorial == 0, "synthetic ordered-word integrality")
                    counts[j] = count // factorial
                current = following
            full.append(
                {k: v for k, v in row_.items() if k not in ("odd", "even")}
                | {
                    "transitions": [
                        {"target_state": j, "multiplicity": counts[j]} for j in sorted(counts)
                    ]
                }
            )
        local_trace, full_trace = (
            trace_counts(rows, initial, "local"),
            trace_counts(full, initial, "full"),
        )
        require(local_trace["state_classes"] == full_trace["state_classes"], "synthetic terminals")
        expected = {"multiround": (2, 1), "weighted": (1, 1), "preserve": (0, 0)}[name]
        require(
            (local_trace["strict_rounds"], full_trace["strict_rounds"]) == expected,
            "prespecified synthetic strict rounds",
        )
        result.append(
            {
                "name": name,
                "local_problem": local_payload(rows, initial),
                "full_rows": full,
                "local_trace": local_trace,
                "full_trace": full_trace,
                "observed_C_realization": False,
            }
        )
    return result


def public_controls(direct, reference, a, model, controls):
    features, _, fine, _ = reconstruct_model(model)
    rows, _ = raw_counts(model, features, fine)
    problem = local_payload(rows, a["partitions"]["C"]["state_classes"])
    local_calls = full_calls = constructor_calls = rejected = 0
    for route in (direct, reference):
        for p, expected in [(problem, a["local_refinement"])] + [
            (c["local_problem"], c["local_trace"]) for c in controls
        ]:
            before = canonical(p)
            value = route.refine_local(p)
            require_same_wire(value, expected, "actual public local refinement")
            require(canonical(p) == before, "local-refinement input mutated")
            value["state_classes"][0] = -99
            require(canonical(p) == before, "local-refinement output aliases input")
            require_same_wire(
                route.refine_local(p), expected, "detached local-refinement later call"
            )
            local_calls += 2
        for c in controls:
            value = route._refine_full(c["full_rows"], c["local_problem"]["state_classes"])
            require_same_wire(value, c["full_trace"], "private full-profile synthetic trace")
            full_calls += 1
        p = constructor_payload(a["terminal"]["local_rows"])
        before = canonical(p)
        value = route.reconstruct_profiles(p)
        require_same_wire(
            value, constructor_output(a["terminal"]), "actual terminal local-only reconstruction"
        )
        require(canonical(p) == before, "terminal constructor input mutated")
        constructor_calls += 1
        for bad in (
            None,
            {},
            [],
            {**problem, "extra": 0},
            {**problem, "schema_version": "bad"},
            {**problem, "state_classes": [True]},
            {**problem, "rows": []},
        ):
            try:
                route.refine_local(bad)
            except ValueError:
                rejected += 1
            else:
                raise ValueError("invalid local refinement accepted")
    return {
        "local_refiner_calls": local_calls,
        "private_full_control_calls": full_calls,
        "terminal_constructor_calls": constructor_calls,
        "invalid_local_calls_rejected": rejected,
        "local_refiner_has_no_full_or_H_input": True,
        "terminal_constructor_has_no_raw_input": True,
    }


def run_suite():
    direct = load("_qr05t_direct", "local_refinement.py")
    reference = load("_qr05t_reference", "reference_qr05t.py")
    problem = fixtures()[0]
    before = canonical(problem)
    a = direct.analyze(problem)
    require(canonical(problem) == before, "primary input mutation")
    b = reference.analyze(problem)
    require(canonical(problem) == before, "reference input mutation")
    require_same_wire(a, b, "independent T outputs differ")
    audit = check_analysis(a, problem["model"])
    bridge = prior_bridge(a, problem["model"])
    controls = synthetic_controls()
    public = public_controls(direct, reference, a, problem["model"], controls)
    rejected = 0
    for route in (direct, reference):
        for bad in (
            None,
            [],
            {},
            True,
            {**problem, "extra": 0},
            {**problem, "model": {}},
            {**problem, "family": "bad"},
        ):
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
            "same_memberships_as_H": a["comparison"]["same_memberships_as_H"],
            "local_rounds": len(a["local_refinement"]["rounds"]),
            "full_rounds": len(a["full_refinement"]["rounds"]),
            "local_signature_atoms": a["local_refinement"]["counts"]["signature_atoms"],
            "full_signature_atoms": a["full_refinement"]["counts"]["signature_atoms"],
            "profile_cells": a["terminal"]["comparison"]["profile_cells"],
            "power_cells": a["terminal"]["comparison"]["power_cells"],
            "local_refiner_calls": public["local_refiner_calls"],
            "terminal_constructor_calls": public["terminal_constructor_calls"],
        },
    }


if __name__ == "__main__":
    main()
