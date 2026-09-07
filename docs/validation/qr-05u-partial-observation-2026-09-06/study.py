"""QR-05U partial-observation audit, capture, and read-only replay.

Generic lifecycle, chain-support and matrix-coefficient audit utilities are
locally carried from the O/P runner lineage. Independent reconstruction
never imports either executor; run_suite dispatches them only for comparison.
T raw/local/label inputs are declared dependencies; no prior executor is imported.
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
SCHEMA = "det8-qr05u-results-v1"
BASE_COMMIT = "9dd30b3c25d77afd10b0827409cba36992c5fe18"
SOURCES = (
    "README.md",
    "filtering.py",
    "reference_qr05u.py",
    "study.py",
    "test_qr05u.py",
    "test_capture.py",
)

PRIORS = {
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


T_PRIOR = "qr-05t-local-refinement-2026-09-06/results.json"


def fraction(value, *, input_value=False):
    require(type(value) is list and len(value) == 2, "fraction pair")
    n, d = value
    require(type(n) is int and type(d) is int and 0 <= n <= d and d > 0, "native probability")
    limit = 64 if input_value else 4096
    require(max(n.bit_length(), d.bit_length()) <= limit, "fraction component cap")
    result = F(n, d)
    require([result.numerator, result.denominator] == value, "reduced fraction")
    return result


def fq(value):
    require(0 <= value <= 1, "probability interval")
    require(
        max(value.numerator.bit_length(), value.denominator.bit_length()) <= 4096,
        "derived fraction cap",
    )
    return [value.numerator, value.denominator]


def belief(values):
    return [{"class_id": h, "probability": fq(p)} for h, p in sorted(values.items()) if p]


def question_law(values):
    return [{"value": list(q), "probability": fq(p)} for q, p in sorted(values.items()) if p]


def normalized(values):
    total = sum(values.values(), F(0))
    require(total > 0, "positive normalization")
    return {key: val / total for key, val in values.items() if val}


def add_mass(target, key, value):
    if value:
        target[key] = target.get(key, F(0)) + value


def push(mass, kernel_rows):
    out = {}
    for i, weight in mass.items():
        for j, prob in kernel_rows[i].items():
            add_mass(out, j, weight * prob)
    return out


def question_push(mass, labels):
    out = {}
    for i, prob in mass.items():
        add_mass(out, tuple(labels[i]["question"]), prob)
    return out


def observation_groups(mass, labels):
    out = {}
    for i, prob in mass.items():
        add_mass(out.setdefault(tuple(labels[i]["observation"]), {}), i, prob)
    return out


def case_problem(model, case):
    return {
        "schema_version": "det8-qr05u-problem-v1",
        "family": "qr05u_partial_observation",
        "model": model,
        "prior": case["prior"],
        "rates": case["rates"],
    }


def fixtures():
    source = prior_json(T_PRIOR)["suite"]
    raw = source["problem"]["model"]
    a = source["analysis"]
    classes = [
        {k: v for k, v in row.items() if k != "representative_state"}
        for row in a["terminal"]["local_rows"]
    ]
    labels = []
    for row in a["terminal"]["local_rows"]:
        feature = a["features"][row["representative_state"]]
        obs = [row["frame_id"], *feature["chain_counts"]]
        labels.append(
            {
                "class_id": row["class_id"],
                "observation": obs,
                "question": obs + [feature["motif_count"], feature["path_count"]],
            }
        )
    schedules = {
        "balanced": [[[1, 2], [1, 2]], [[2, 3], [1, 3]], [[1, 2], [1, 2]]],
        "biased": [[[2, 3], [1, 3]], [[1, 3], [2, 3]], [[2, 3], [2, 3]]],
    }
    priors = {
        "left": [(612, F(1))],
        "right": [(625, F(1))],
        "mixture": [(612, F(1, 2)), (625, F(1, 2))],
    }
    cases = []
    for name, raw_prior in priors.items():
        mass = {}
        for sid, weight in raw_prior:
            add_mass(mass, a["partitions"]["H"]["state_classes"][sid], weight)
        for schedule, rates in schedules.items():
            cases.append(
                {
                    "case_id": name + "_" + schedule,
                    "raw_prior": [{"state_id": sid, "probability": fq(p)} for sid, p in raw_prior],
                    "prior": belief(mass),
                    "rates": rates,
                }
            )
    return {"raw_model": raw, "model": {"classes": classes, "labels": labels}, "cases": cases}


def independent_domain(model):
    features, parts, fine, _ = reconstruct_model(model)
    partition = parts["H"]
    ids = partition["state_classes"]
    local, full = raw_counts(model, features, fine)
    state_profiles = profile_census(model, features, fine, partition)
    closed, class_profiles = closure_profiles(partition, state_profiles)
    require(closed["closed"], "raw H full closure")
    classes, labels, raw_labels = [], [], []
    for state, feature in zip(model["states"], features, strict=True):
        obs = [state["frame_id"], *feature["chain_counts"]]
        raw_labels.append(
            {"observation": obs, "question": obs + [feature["motif_count"], feature["path_count"]]}
        )
    for group in partition["classes"]:
        h, rep = group["class_id"], group["members"][0]
        rows = []
        for sid in group["members"]:
            source = local[sid]
            row = {
                "class_id": h,
                "frame_id": source["frame_id"],
                "parent_color_sizes": source["parent_color_sizes"],
            }
            for color in ("odd", "even"):
                counts = {}
                for edge in source[color]:
                    target = ids[edge["target_state"]]
                    counts[target] = counts.get(target, 0) + edge["multiplicity"]
                row[color] = [
                    {"target_class": g, "multiplicity": n} for g, n in sorted(counts.items())
                ]
            require_same_wire(raw_labels[sid], raw_labels[rep], "all-member label constancy")
            rows.append(row)
        for row in rows[1:]:
            require_same_wire(row, rows[0], "all-member local constancy")
        classes.append(rows[0])
        labels.append({"class_id": h, **raw_labels[rep]})
    profiles = [
        {k: v for k, v in row.items() if k != "representative_state"} for row in class_profiles
    ]
    certificate, operators = audit_local_profiles(classes, profiles)
    return {
        "features": features,
        "H": partition,
        "raw_local": local,
        "raw_full": full,
        "raw_labels": raw_labels,
        "profiles": profiles,
        "summary_model": {"classes": classes, "labels": labels},
        "reconstruction": {
            "profiles_sha256": digest(canonical(profiles)),
            "profile_atoms": sum(len(r["transitions"]) for r in profiles),
            "certificate": certificate,
            "operator_checks": operators,
        },
        "fine_sha256": digest(canonical(fine)),
        "fine_atoms": sum(len(r["transitions"]) for r in fine),
        "state_profiles_sha256": digest(canonical(state_profiles)),
        "local_choices": sum(sum(r["parent_color_sizes"]) for r in local),
        "member_comparisons": len(features) - len(classes),
    }


@lru_cache(maxsize=1)
def independent_domain_bytes(model_bytes):
    return canonical(independent_domain(json.loads(model_bytes)))


@memoize
def subset_probability(O, E, m, n, rate):
    x, y = (F(*v) for v in rate)
    return x**m * (1 - x) ** (O - m) * y**n * (1 - y) ** (E - n)


def rate_key(rate):
    return tuple(tuple(pair) for pair in rate)


def product_rate(rates):
    values = [F(1), F(1)]
    for rate in rates:
        for c in (0, 1):
            values[c] *= fraction(rate[c], input_value=True)
    return [fq(value) for value in values]


def class_kernel(domain, rate):
    out = []
    for row in domain["profiles"]:
        O, E = row["parent_color_sizes"]
        values = {}
        for edge in row["transitions"]:
            prob = edge["multiplicity"] * subset_probability(
                O, E, *edge["retained_color_sizes"], rate_key(rate)
            )
            add_mass(values, edge["target_class"], prob)
        require(sum(values.values(), F(0)) == 1, "class kernel normalization")
        out.append(values)
    return out


def kernel_wire(rows):
    return [
        {
            "class_id": h,
            "transitions": [
                {"target_class": g, "probability": fq(p)} for g, p in sorted(row.items()) if p
            ],
        }
        for h, row in enumerate(rows)
    ]


def raw_row(domain, sid, rate):
    source = domain["raw_full"][sid]
    O, E = source["parent_color_sizes"]
    out = {}
    for atom in source["transitions"]:
        target = atom["target_state"]
        m, n = domain["raw_full"][target]["parent_color_sizes"]
        prob = atom["multiplicity"] * subset_probability(O, E, m, n, rate_key(rate))
        add_mass(out, target, prob)
    require(sum(out.values(), F(0)) == 1, "raw kernel normalization")
    return out


def validate_case(case, raw_model):
    require_wire(case)
    require(
        type(case) is dict and set(case) == {"case_id", "raw_prior", "prior", "rates"},
        "case schema",
    )
    require(type(case["case_id"]) is str and 1 <= len(case["case_id"]) <= 64, "case ID")
    for key, target_key, upper in (
        ("raw_prior", "state_id", len(raw_model["states"])),
        ("prior", "class_id", 512),
    ):
        values = case[key]
        require(type(values) is list and 1 <= len(values) <= 16, "sparse prior support")
        previous, total = -1, F(0)
        for atom in values:
            require(type(atom) is dict and set(atom) == {target_key, "probability"}, "prior atom")
            target = atom[target_key]
            require(type(target) is int and previous < target < upper, "ordered prior ID")
            weight = fraction(atom["probability"], input_value=True)
            require(weight > 0, "positive prior atom")
            previous, total = target, total + weight
        require(total == 1, "prior unit mass")
    require(type(case["rates"]) is list and len(case["rates"]) == 3, "three stages")
    for rate in case["rates"]:
        require(type(rate) is list and len(rate) == 2, "two-color rate")
        for value in rate:
            fraction(value, input_value=True)


def first_difference(left, right):
    for q in sorted(set(left) | set(right)):
        if left.get(q, F(0)) != right.get(q, F(0)):
            return q, left.get(q, F(0)), right.get(q, F(0))
    return None


def summarize_controls(history_data, latest, K3, labels):
    histories = sorted(history_data)
    controls = {"history_witness": None, "forgetting_witness": None, "map_witness": None}
    counts = {
        k: 0
        for k in (
            "history_pairs_compared",
            "history_pairs_different",
            "forgetting_comparisons",
            "forgetting_differences",
            "map_comparisons",
            "map_differences",
        )
    }
    for index, h in enumerate(histories):
        posterior, prediction = history_data[h]
        for other in histories[index + 1 :]:
            if other[1] != h[1]:
                continue
            counts["history_pairs_compared"] += 1
            diff = first_difference(prediction, history_data[other][1])
            if diff is not None:
                counts["history_pairs_different"] += 1
                if controls["history_witness"] is None:
                    q, a, b = diff
                    controls["history_witness"] = {
                        "left": [list(v) for v in h],
                        "right": [list(v) for v in other],
                        "question": list(q),
                        "left_probability": fq(a),
                        "right_probability": fq(b),
                    }
        counts["forgetting_comparisons"] += 1
        diff = first_difference(prediction, latest[h[1]][1])
        if diff is not None:
            counts["forgetting_differences"] += 1
            if controls["forgetting_witness"] is None:
                q, a, b = diff
                controls["forgetting_witness"] = {
                    "observations": [list(v) for v in h],
                    "question": list(q),
                    "history_probability": fq(a),
                    "latest_only_probability": fq(b),
                }
        winner = min(posterior, key=lambda g: (-posterior[g], g))
        point_prediction = question_push(K3[winner], labels)
        counts["map_comparisons"] += 1
        diff = first_difference(prediction, point_prediction)
        if diff is not None:
            counts["map_differences"] += 1
            if controls["map_witness"] is None:
                q, a, b = diff
                controls["map_witness"] = {
                    "observations": [list(v) for v in h],
                    "map_class_id": winner,
                    "question": list(q),
                    "mixture_probability": fq(a),
                    "map_probability": fq(b),
                }
    return controls, counts


def expected_analysis(raw_model, case, domain=None):
    validate_model(raw_model)
    validate_case(case, raw_model)
    if domain is None:
        domain = json.loads(independent_domain_bytes(canonical(raw_model)))
    ids, labels = domain["H"]["state_classes"], domain["summary_model"]["labels"]
    rates = case["rates"]
    initial = {}
    for atom in case["raw_prior"]:
        add_mass(initial, ids[atom["state_id"]], fraction(atom["probability"], input_value=True))
    require_same_wire(belief(initial), case["prior"], "raw prior pushforward")
    class_rows = [class_kernel(domain, rate) for rate in rates]
    raw_cache = {}

    def step(sid, stage):
        key = sid, stage
        if key not in raw_cache:
            raw_cache[key] = raw_row(domain, sid, rates[stage])
        return raw_cache[key]

    first_joint, joint, future = {}, {}, {}
    after1, after2, after3 = {}, {}, {}
    for atom in case["raw_prior"]:
        s, p0 = atom["state_id"], fraction(atom["probability"], input_value=True)
        for t, p1 in step(s, 0).items():
            w1 = p0 * p1
            y1 = tuple(domain["raw_labels"][t]["observation"])
            add_mass(first_joint.setdefault(y1, {}), ids[t], w1)
            add_mass(after1, ids[t], w1)
            for u, p2 in step(t, 1).items():
                w2 = w1 * p2
                y2 = tuple(domain["raw_labels"][u]["observation"])
                history = y1, y2
                add_mass(joint.setdefault(history, {}), ids[u], w2)
                add_mass(after2, ids[u], w2)
                for v, p3 in step(u, 2).items():
                    w3 = w2 * p3
                    add_mass(
                        future.setdefault(history, {}),
                        tuple(domain["raw_labels"][v]["question"]),
                        w3,
                    )
                    add_mass(after3, ids[v], w3)
    require(after1 == push(initial, class_rows[0]), "raw/class first law")
    require(after2 == push(after1, class_rows[1]), "raw/class second law")
    require(after3 == push(after2, class_rows[2]), "raw/class third law")
    require(
        after3 == push(initial, class_kernel(domain, product_rate(rates))),
        "direct product-rate class law",
    )
    require(
        all(sum(v.values(), F(0)) == 1 for v in (initial, after1, after2, after3)),
        "unit unconditional laws",
    )
    first, first_post = [], {}
    for y, mass in sorted(first_joint.items()):
        posterior = normalized(mass)
        first_post[y] = posterior
        first.append(
            {
                "observation": list(y),
                "likelihood": fq(sum(mass.values(), F(0))),
                "posterior": belief(posterior),
            }
        )
    latest_only, latest = [], {}
    for y, mass in sorted(observation_groups(after2, labels).items()):
        posterior = normalized(mass)
        prediction = question_push(push(posterior, class_rows[2]), labels)
        latest[y] = posterior, prediction
        latest_only.append(
            {
                "observation": list(y),
                "likelihood": fq(sum(mass.values(), F(0))),
                "posterior": belief(posterior),
                "prediction": question_law(prediction),
            }
        )
    histories, history_data = [], {}
    tower_first, tower_latest = {}, {}
    first_evidence = {y: sum(mass.values(), F(0)) for y, mass in first_joint.items()}
    latest_evidence = {
        tuple(row["observation"]): fraction(row["likelihood"]) for row in latest_only
    }
    for h, mass in sorted(joint.items()):
        evidence = sum(mass.values(), F(0))
        posterior = normalized(mass)
        require(
            all(tuple(labels[g]["observation"]) == h[1] for g in posterior),
            "posterior emission support",
        )
        require(sum(posterior.values(), F(0)) == 1, "posterior unit mass")
        require(sum(future[h].values(), F(0)) == evidence, "raw future joint normalization")
        prediction = {q: w / evidence for q, w in future[h].items()}
        require(
            prediction == question_push(push(posterior, class_rows[2]), labels),
            "raw future/class mixture",
        )
        conditional = evidence / first_evidence[h[0]]
        require(
            sum(
                v
                for g, v in push(first_post[h[0]], class_rows[1]).items()
                if tuple(labels[g]["observation"]) == h[1]
            )
            == conditional,
            "conditional evidence",
        )
        histories.append(
            {
                "observations": [list(v) for v in h],
                "likelihood": fq(evidence),
                "conditional_likelihood": fq(conditional),
                "posterior": belief(posterior),
                "prediction": question_law(prediction),
            }
        )
        history_data[h] = posterior, prediction
        for q, p in prediction.items():
            add_mass(tower_first.setdefault(h[0], {}), q, conditional * p)
            add_mass(tower_latest.setdefault(h[1], {}), q, evidence / latest_evidence[h[1]] * p)
    require(sum(first_evidence.values(), F(0)) == 1, "first likelihood normalization")
    require(
        sum(sum(row.values(), F(0)) for row in joint.values()) == 1,
        "joint likelihood normalization",
    )
    for y, posterior in first_post.items():
        require(
            tower_first[y]
            == question_push(push(push(posterior, class_rows[1]), class_rows[2]), labels),
            "first tower law",
        )
    for y, (_, prediction) in latest.items():
        require(tower_latest[y] == prediction, "latest tower law")
    controls, comparisons = summarize_controls(history_data, latest, class_rows[2], labels)
    counts = {
        "classes": len(labels),
        "profile_atoms": domain["reconstruction"]["profile_atoms"],
        "kernel_atoms": [sum(len(row) for row in K) for K in class_rows],
        "first_histories": len(first),
        "histories": len(histories),
        "first_posterior_atoms": sum(len(row["posterior"]) for row in first),
        "history_posterior_atoms": sum(len(row["posterior"]) for row in histories),
        "history_prediction_atoms": sum(len(row["prediction"]) for row in histories),
        "latest_observations": len(latest_only),
        "latest_posterior_atoms": sum(len(row["posterior"]) for row in latest_only),
        "latest_prediction_atoms": sum(len(row["prediction"]) for row in latest_only),
        **comparisons,
    }
    require(
        counts["histories"] <= 16384
        and counts["history_posterior_atoms"] <= 262144
        and counts["history_prediction_atoms"] <= 262144,
        "history retention caps",
    )
    return {
        "model_sha256": digest(canonical(domain["summary_model"])),
        "reconstruction": domain["reconstruction"],
        "prior": case["prior"],
        "rates": rates,
        "kernel_sha256": [digest(canonical(kernel_wire(K))) for K in class_rows],
        "first": first,
        "histories": histories,
        "latest_only": latest_only,
        "unconditional": {
            "after_first": belief(after1),
            "after_second": belief(after2),
            "after_third": belief(after3),
            "next_prediction": question_law(question_push(after3, labels)),
        },
        "controls": controls,
        "checks": {
            **{
                key: True
                for key in (
                    "first_normalization",
                    "joint_normalization",
                    "posterior_normalization",
                    "posterior_support",
                    "tower_first",
                    "tower_latest",
                    "three_step_composition",
                )
            },
            "max_abs_residual": [0, 1],
        },
        "counts": counts,
    }


@lru_cache(maxsize=8)
def expected_analysis_bytes(raw_bytes, case_bytes):
    return canonical(expected_analysis(json.loads(raw_bytes), json.loads(case_bytes)))


def check_analysis(a, raw_model, case):
    require_wire(a)
    validate_model(raw_model)
    validate_case(case, raw_model)
    expected = expected_analysis_bytes(canonical(raw_model), canonical(case))
    require(canonical(a) == expected, "complete independent raw filtering audit differs")
    return {"analysis_sha256": digest(expected), "complete_native_output_equal": True}


def raw_bridge(data, domain):
    producer = prior_json(T_PRIOR)["suite"]
    previous = producer["analysis"]
    require_same_wire(data["raw_model"], producer["problem"]["model"], "T raw dependency")
    require_same_wire(data["model"], domain["summary_model"], "producer local/label model vs raw")
    require_same_wire(domain["features"], previous["features"], "T raw features")
    require_same_wire(domain["H"], previous["partitions"]["H"], "T actual H fibers")
    require(domain["fine_sha256"] == previous["fine_kernel"]["sha256"], "T fine polynomial law")
    require(
        domain["state_profiles_sha256"]
        == previous["terminal"]["comparison"]["direct_profiles_sha256"],
        "T complete state profiles",
    )
    require_same_wire(
        domain["reconstruction"]["certificate"],
        previous["terminal"]["reconstruction"]["certificate"],
        "T recurrence certificate",
    )
    require_same_wire(
        domain["reconstruction"]["operator_checks"],
        previous["terminal"]["reconstruction"]["operator_checks"],
        "T local operators",
    )
    return {
        "prior_artifact": T_PRIOR,
        "raw_local_labels_declared_input_dependencies": True,
        "states": len(domain["features"]),
        "classes": len(domain["H"]["classes"]),
        "member_comparisons": domain["member_comparisons"],
        "features_sha256": digest(canonical(domain["features"])),
        "H_sha256": digest(canonical(domain["H"])),
        "raw_local_sha256": digest(canonical(domain["raw_local"])),
        "fine_sha256": domain["fine_sha256"],
        "fine_atoms": domain["fine_atoms"],
        "raw_deletion_choices": domain["local_choices"],
        "profiles_sha256": domain["reconstruction"]["profiles_sha256"],
        "all_members_labels_local_and_profiles_equal": True,
        "T_refinement_or_minimality_replayed": False,
        "source_aliases_regenerated": False,
        "P_consumer_R_helper_Q_certificate_replayed": False,
    }


def rate_audit(domain, cases):
    rates = {rate_key(rate) for case in cases for rate in case["rates"]}
    rates.update(rate_key(product_rate(case["rates"])) for case in cases)
    ids = domain["H"]["state_classes"]
    reports = []
    for rate in sorted(rates):
        decoded = [list(pair) for pair in rate]
        K = class_kernel(domain, decoded)
        comparisons = atoms = 0
        for sid in range(len(ids)):
            observed = {}
            for target, prob in raw_row(domain, sid, decoded).items():
                add_mass(observed, ids[target], prob)
                atoms += 1
            require(observed == K[ids[sid]], "every raw member rate law")
            comparisons += 1
        reports.append(
            {
                "rates": decoded,
                "raw_rows_checked": comparisons,
                "raw_positive_atoms": atoms,
                "class_positive_atoms": sum(map(len, K)),
                "kernel_sha256": digest(canonical(kernel_wire(K))),
                "max_abs_residual": [0, 1],
            }
        )
    return {
        "rates": reports,
        "raw_row_comparisons": sum(r["raw_rows_checked"] for r in reports),
        "raw_positive_atoms": sum(r["raw_positive_atoms"] for r in reports),
        "all_raw_members_checked": True,
    }


def named_id_control(domain, raw_model):
    for group in domain["H"]["classes"]:
        for i, left in enumerate(group["members"]):
            for right in group["members"][i + 1 :]:
                a = int(1 in raw_model["states"][left]["kept"])
                b = int(1 in raw_model["states"][right]["kept"])
                if a != b:
                    return {
                        "predicate": "original_vertex_1_present",
                        "H_measurable": False,
                        "witness": {
                            "class_id": group["class_id"],
                            "left_state": left,
                            "right_state": right,
                            "left_value": a,
                            "right_value": b,
                        },
                        "public_custom_predicate_supported": False,
                    }
    return {
        "predicate": "original_vertex_1_present",
        "H_measurable": True,
        "witness": None,
        "public_custom_predicate_supported": False,
    }


def conditioning_expected(analysis, records):
    first = next((row for row in analysis["first"] if row["observation"] == records[0]), None)
    found = next((row for row in analysis["histories"] if row["observations"] == records), None)
    if found is None:
        return {
            "status": "impossible",
            "failed_stage": 1 if first is None else 2,
            "likelihood": [0, 1],
            "posterior": None,
            "prediction": None,
        }
    return {
        "status": "possible",
        "failed_stage": None,
        **{key: found[key] for key in ("likelihood", "posterior", "prediction")},
    }


def public_controls(routes, data, analyses):
    calls, impossible, invalid = 0, 0, 0
    other = min(row["observation"] for row in data["model"]["labels"] if row["observation"][0] == 1)
    for route in routes:
        for index, (case, a) in enumerate(zip(data["cases"], analyses, strict=True)):
            p = case_problem(data["model"], case)
            records_menu = [a["histories"][0]["observations"]]
            if index == 0:
                records_menu.extend(
                    [
                        a["histories"][-1]["observations"],
                        [other, other],
                        [a["histories"][0]["observations"][0], other],
                    ]
                )
            for records in records_menu:
                before = canonical([p, records])
                output = route.filter_history(p, records)
                require_same_wire(
                    output, conditioning_expected(a, records), "actual public conditioning"
                )
                require(canonical([p, records]) == before, "conditioning input mutation")
                calls += 1
                impossible += int(output["status"] == "impossible")
        p = case_problem(data["model"], data["cases"][0])
        for bad in (
            None,
            {},
            [],
            {**p, "extra": 0},
            {**p, "schema_version": "bad"},
            {**p, "rates": []},
            {**p, "prior": []},
        ):
            try:
                route.analyze(bad)
            except ValueError:
                invalid += 1
            else:
                raise ValueError("malformed public analysis accepted")
    require(calls == 18 and impossible == 4 and invalid == 14, "public control inventory")
    return {
        "conditioning_calls": calls,
        "impossible_conditioning_calls": impossible,
        "invalid_analyze_calls_rejected": invalid,
        "raw_orders_or_artifacts_given_to_core": False,
    }


def run_suite():
    direct = load("_qr05u_primary", "filtering.py")
    reference = load("_qr05u_reference", "reference_qr05u.py")
    data = fixtures()
    domain = json.loads(independent_domain_bytes(canonical(data["raw_model"])))
    bridge = raw_bridge(data, domain)
    laws = rate_audit(domain, data["cases"])
    analyses, retained, lifts = [], [], []
    for case in data["cases"]:
        problem = case_problem(data["model"], case)
        before = canonical(problem)
        a, b = direct.analyze(problem), reference.analyze(problem)
        require(canonical(problem) == before, "analysis input mutation")
        require_same_wire(a, b, "independent summary routes differ")
        check_analysis(a, data["raw_model"], case)
        analyses.append(a)
        retained.append({**case, "analysis": a})
        variants = {}
        for kind, position in (("first", 0), ("last", -1)):
            raw_prior = {}
            for atom in case["prior"]:
                sid = domain["H"]["classes"][atom["class_id"]]["members"][position]
                add_mass(raw_prior, sid, fraction(atom["probability"], input_value=True))
            lifted = {
                **case,
                "raw_prior": [
                    {"state_id": sid, "probability": fq(p)} for sid, p in sorted(raw_prior.items())
                ],
            }
            value = expected_analysis(data["raw_model"], lifted, domain)
            require_same_wire(value, a, "within-H raw prior redistribution")
            variants[kind] = {
                "raw_prior": lifted["raw_prior"],
                "analysis_sha256": digest(canonical(value)),
                "H_filtering_equal": True,
                "raw_posterior_equality_claimed": False,
            }
        lifts.append({"case_id": case["case_id"], **variants})
    public = public_controls((direct, reference), data, analyses)
    totals = {
        "raw_states": len(data["raw_model"]["states"]),
        "classes": len(data["model"]["classes"]),
        "cases": len(analyses),
        "analyze_calls": 2 * len(analyses),
        "conditioning_calls": public["conditioning_calls"],
        "prior_lift_comparisons": 2 * len(lifts),
        "histories": sum(a["counts"]["histories"] for a in analyses),
        "history_posterior_atoms": sum(a["counts"]["history_posterior_atoms"] for a in analyses),
        "history_prediction_atoms": sum(a["counts"]["history_prediction_atoms"] for a in analyses),
        "history_witness_cases": sum(
            a["controls"]["history_witness"] is not None for a in analyses
        ),
        "forgetting_witness_cases": sum(
            a["controls"]["forgetting_witness"] is not None for a in analyses
        ),
        "map_witness_cases": sum(a["controls"]["map_witness"] is not None for a in analyses),
        "raw_rate_rows_checked": laws["raw_row_comparisons"],
    }
    return {
        "raw_model": data["raw_model"],
        "model": data["model"],
        "cases": retained,
        "independent_route_equal": True,
        "raw_bridge": bridge,
        "rate_audit": laws,
        "prior_lifts": lifts,
        "unsupported_observation": named_id_control(domain, data["raw_model"]),
        "public_controls": public,
        "totals": totals,
    }


if __name__ == "__main__":
    main()
