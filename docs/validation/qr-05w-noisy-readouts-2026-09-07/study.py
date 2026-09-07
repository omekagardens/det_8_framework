"""QR-05W noisy-readout audit, capture, and read-only replay.

Generic lifecycle, chain-support and matrix-coefficient audit utilities are
locally carried from the O/P runner lineage. Independent reconstruction
never imports either executor; run_suite dispatches them only for comparison.
U/V producer/raw inputs are declared dependencies; no prior executor is imported.
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
SCHEMA = "det8-qr05w-results-v1"
BASE_COMMIT = "971d2fd002d86bf6f13fd3d7888453cd23b44790"
SOURCES = (
    "README.md",
    "noisy_readout.py",
    "reference_qr05w.py",
    "study.py",
    "test_qr05w.py",
    "test_capture.py",
)

PRIORS = {
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


def expected_filtering(raw_model, case, domain=None):
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
def expected_filtering_bytes(raw_bytes, case_bytes):
    return canonical(expected_filtering(json.loads(raw_bytes), json.loads(case_bytes)))


def check_filtering(a, raw_model, case):
    require_wire(a)
    validate_model(raw_model)
    validate_case(case, raw_model)
    expected = expected_filtering_bytes(canonical(raw_model), canonical(case))
    require(canonical(a) == expected, "complete independent raw filtering audit differs")
    return {"analysis_sha256": digest(expected), "complete_native_output_equal": True}


U_PRIOR = "qr-05u-partial-observation-2026-09-06/results.json"
NAMES = ("N", "NMT", "H")
EDGES = (("baseline", "N"), ("N", "NMT"), ("NMT", "H"))


def v_fixtures():
    source = prior_json(U_PRIOR)["suite"]
    return {
        "raw_model": source["raw_model"],
        "model": source["model"],
        "cases": [
            {**{k: v for k, v in case.items() if k != "analysis"}, "u_analysis": case["analysis"]}
            for case in source["cases"]
        ],
    }


def original_case(case):
    return {k: case[k] for k in ("case_id", "raw_prior", "prior", "rates")}


def v_case_problem(model, case):
    return {
        "schema_version": "det8-qr05v-problem-v1",
        "family": "qr05v_readout_value",
        "model": model,
        "rate": case["rates"][2],
        "beliefs": [
            {"belief_id": i, "weight": row["likelihood"], "posterior": row["posterior"]}
            for i, row in enumerate(case["u_analysis"]["histories"])
        ],
    }


def validate_v_case(case, raw_model):
    require_wire(case)
    require(
        type(case) is dict
        and set(case) == {"case_id", "raw_prior", "prior", "rates", "u_analysis"},
        "V producer case schema",
    )
    validate_case(original_case(case), raw_model)
    require(type(case["u_analysis"]) is dict, "U evidence object")


def readout_maps(model):
    values = sorted({tuple(label["question"]) for label in model["labels"]})
    return {
        "NMT_to_N": [{"fine": list(q), "coarse": list(q[:5])} for q in values],
        "H_to_NMT": [
            {"fine": [label["class_id"]], "coarse": label["question"]} for label in model["labels"]
        ],
    }


def risk(law):
    require(sum(law.values(), F(0)) == 1, "risk law normalization")
    # Probability that two independent draws from this law disagree.
    value = sum((p * (1 - p) for p in law.values()), F(0))
    fq(value)
    return value


def weighted_distance(left, right, weight):
    return sum(
        (weight * ((left.get(q, F(0)) - right.get(q, F(0))) ** 2) for q in set(left) | set(right)),
        F(0),
    )


def raw_current_histories(domain, case):
    rates = case["rates"]
    cache = {}

    def row(sid, step):
        key = sid, step
        if key not in cache:
            cache[key] = raw_row(domain, sid, rates[step])
        return cache[key]

    result, paths = {}, 0
    for atom in case["raw_prior"]:
        prior_weight = fraction(atom["probability"], input_value=True)
        for first, p1 in row(atom["state_id"], 0).items():
            y1 = tuple(domain["raw_labels"][first]["observation"])
            for second, p2 in row(first, 1).items():
                y2 = tuple(domain["raw_labels"][second]["observation"])
                add_mass(result.setdefault((y1, y2), {}), second, prior_weight * p1 * p2)
                paths += 1
    require(
        sum(sum(m.values(), F(0)) for m in result.values()) == 1, "raw current histories normalize"
    )
    return result, paths


def raw_cell(domain, mass, value, future):
    weight = sum(mass.values(), F(0))
    require(weight > 0, "positive readout cell")
    posterior, joint = {}, {}
    for sid, probability in mass.items():
        add_mass(posterior, domain["H"]["state_classes"][sid], probability / weight)
        for q, conditional in future(sid).items():
            add_mass(joint, q, probability * conditional)
    require(sum(joint.values(), F(0)) == weight, "raw readout/future joint mass")
    prediction = {q: p / weight for q, p in joint.items() if p}
    conditional_risk = risk(prediction)
    pair_mass = sum((p * (weight - p) for p in joint.values()), F(0))
    require(
        pair_mass / weight == weight * conditional_risk,
        "raw within-cell disagreement normalization",
    )
    return {
        "value": value,
        "weight": weight,
        "posterior": posterior,
        "prediction": prediction,
        "risk": conditional_risk,
    }


def cell_wire(cell):
    return {
        "value": list(cell["value"]),
        "probability": fq(cell["weight"]),
        "posterior": belief(cell["posterior"]),
        "prediction": question_law(cell["prediction"]),
        "risk": fq(cell["risk"]),
    }


def merge_cells(children, parent_weight, key):
    result = {}
    for child in children:
        for target, probability in child[key].items():
            add_mass(result, target, child["weight"] / parent_weight * probability)
    return result


def make_refinement(coarse, fine, parents, children):
    checks, total_drop, total_variance = [], F(0), F(0)
    for parent in parents:
        if coarse == "baseline":
            selected = children
        elif coarse == "N":
            selected = [c for c in children if c["value"][:5] == parent["value"]]
        else:
            selected = [c for c in children if c["current_question"] == parent["value"]]
        require(bool(selected), "positive refinement parent has no children")
        require(sum(c["weight"] for c in selected) == parent["weight"], "refinement parent mass")
        posterior = merge_cells(selected, parent["weight"], "posterior")
        prediction = merge_cells(selected, parent["weight"], "prediction")
        require(posterior == parent["posterior"], "refinement posterior mixture")
        require(prediction == parent["prediction"], "refinement full question mixture")
        child_risk = sum((c["weight"] / parent["weight"] * c["risk"] for c in selected), F(0))
        drop = parent["risk"] - child_risk
        variance = sum(
            (
                weighted_distance(c["prediction"], prediction, c["weight"] / parent["weight"])
                for c in selected
            ),
            F(0),
        )
        predictions_match = [c["prediction"] == prediction for c in selected]
        equal = all(predictions_match)
        require(drop == variance and drop >= 0, "conditional risk/variance identity")
        require((drop == 0) == equal, "conditional zero gain iff equal future laws")
        checks.append(
            {
                "value": list(parent["value"]),
                "probability": fq(parent["weight"]),
                "fine_values": [list(c["value"]) for c in selected],
                "mixture_sha256": digest(canonical(question_law(prediction))),
                "conditional_risk_drop": fq(drop),
                "conditional_variance_gain": fq(variance),
                "predictions_equal": equal,
            }
        )
        total_drop += parent["weight"] * drop
        total_variance += parent["weight"] * variance
    require(total_drop == total_variance, "global refinement variance")
    require(
        (total_drop == 0) == all(p["predictions_equal"] for p in checks),
        "global zero gain iff equal",
    )
    return {
        "coarse": coarse,
        "fine": fine,
        "risk_drop": fq(total_drop),
        "variance_gain": fq(total_variance),
        "parent_checks": checks,
        "zero_gain_iff_equal": True,
    }


def analyze_raw_readout_belief(domain, entry, raw_posterior, rate, K, future):
    require(sum(raw_posterior.values(), F(0)) == 1, "raw current posterior")
    base = raw_cell(domain, raw_posterior, (), future)
    require_same_wire(belief(base["posterior"]), entry["posterior"], "current U/H posterior")
    groups = {name: {} for name in NAMES}
    for sid, weight in raw_posterior.items():
        labels = domain["raw_labels"][sid]
        values = (
            tuple(labels["observation"]),
            tuple(labels["question"]),
            (domain["H"]["state_classes"][sid],),
        )
        for name, value in zip(NAMES, values, strict=True):
            add_mass(groups[name].setdefault(value, {}), sid, weight)
    cells, readouts = {}, {}
    for name in NAMES:
        rows = [
            raw_cell(domain, mass, value, future) for value, mass in sorted(groups[name].items())
        ]
        if name == "H":
            for row in rows:
                row["current_question"] = tuple(
                    domain["summary_model"]["labels"][row["value"][0]]["question"]
                )
        require(sum(c["weight"] for c in rows) == 1, "readout cell probabilities")
        require(
            merge_cells(rows, F(1), "posterior") == base["posterior"], "readout posterior marginal"
        )
        require(
            merge_cells(rows, F(1), "prediction") == base["prediction"], "unchanged future marginal"
        )
        expected_risk = sum((c["weight"] * c["risk"] for c in rows), F(0))
        gain = base["risk"] - expected_risk
        variance = sum(
            (weighted_distance(c["prediction"], base["prediction"], c["weight"]) for c in rows),
            F(0),
        )
        require(gain == variance and gain >= 0, "readout Brier/variance gain")
        cells[name] = rows
        readouts[name] = {
            "cells": [cell_wire(c) for c in rows],
            "expected_risk": fq(expected_risk),
            "gain": fq(gain),
            "variance_gain": fq(variance),
        }
    refinements = [
        make_refinement(
            coarse, fine, [base] if coarse == "baseline" else cells[coarse], cells[fine]
        )
        for coarse, fine in EDGES
    ]
    for edge in refinements:
        parent_risk = (
            base["risk"]
            if edge["coarse"] == "baseline"
            else fraction(readouts[edge["coarse"]]["expected_risk"])
        )
        require(
            fraction(edge["risk_drop"])
            == parent_risk - fraction(readouts[edge["fine"]]["expected_risk"]),
            "adjacent risk drop",
        )
    labels = domain["summary_model"]["labels"]
    residual = sum(
        (p * risk(question_push(K[h], labels)) for h, p in base["posterior"].items()), F(0)
    )
    require(residual == fraction(readouts["H"]["expected_risk"]), "oracle residual from fixed K3")
    require(
        sum((fraction(edge["risk_drop"]) for edge in refinements), F(0)) == base["risk"] - residual,
        "gains telescope",
    )
    known_N = len(cells["N"]) == 1
    require(known_N and readouts["N"]["gain"] == [0, 1], "U history already fixes current N")
    return {
        "belief_id": entry["belief_id"],
        "weight": entry["weight"],
        "posterior": entry["posterior"],
        "baseline": {"prediction": question_law(base["prediction"]), "risk": fq(base["risk"])},
        "readouts": readouts,
        "refinements": refinements,
        "oracle_residual": fq(residual),
        "checks": {
            **{
                key: True
                for key in (
                    "probabilities_normalized",
                    "marginal_future_preserved",
                    "nested_mixtures",
                    "nested_risks",
                    "oracle_residual_identity",
                    "gains_telescope",
                )
            },
            "N_already_known": known_N,
        },
    }


def compile_readout_value(domain, problem, rows):
    weights = [fraction(row["weight"]) for row in rows]
    require(sum(weights, F(0)) == 1, "case history weights normalize")

    def average(values):
        return sum((w * value for w, value in zip(weights, values, strict=True)), F(0))

    aggregate_prediction = {}
    for weight, row in zip(weights, rows, strict=True):
        for atom in row["baseline"]["prediction"]:
            add_mass(
                aggregate_prediction, tuple(atom["value"]), weight * fraction(atom["probability"])
            )
    baseline = average([fraction(row["baseline"]["risk"]) for row in rows])
    expected_risk = {
        name: average([fraction(row["readouts"][name]["expected_risk"]) for row in rows])
        for name in NAMES
    }
    gain = {
        name: average([fraction(row["readouts"][name]["gain"]) for row in rows]) for name in NAMES
    }
    adjacent = [
        average([fraction(row["refinements"][i]["risk_drop"]) for row in rows]) for i in range(3)
    ]
    residual = average([fraction(row["oracle_residual"]) for row in rows])
    require(
        baseline >= expected_risk["N"] >= expected_risk["NMT"] >= expected_risk["H"] >= 0,
        "weighted risk nesting",
    )
    require(
        sum(adjacent, F(0)) == baseline - residual and residual == expected_risk["H"],
        "weighted oracle/telescoping",
    )
    require(
        all(gain[name] == baseline - expected_risk[name] for name in NAMES),
        "weighted gain identity",
    )
    aggregate = {
        "total_weight": [1, 1],
        "prediction": question_law(aggregate_prediction),
        "baseline_risk": fq(baseline),
        "expected_risk": {k: fq(v) for k, v in expected_risk.items()},
        "gain": {k: fq(v) for k, v in gain.items()},
        "adjacent_gain": [fq(v) for v in adjacent],
        "oracle_residual": fq(residual),
    }

    def first(predicate):
        return next((row["belief_id"] for row in rows if predicate(row)), None)

    witnesses = {
        "first_strict": [
            first(lambda row, i=i: fraction(row["refinements"][i]["risk_drop"]) > 0)
            for i in range(3)
        ],
        "first_zero": [
            first(lambda row, i=i: fraction(row["refinements"][i]["risk_drop"]) == 0)
            for i in range(3)
        ],
        "first_positive_oracle_residual": first(lambda row: fraction(row["oracle_residual"]) > 0),
        "first_zero_oracle_residual": first(lambda row: fraction(row["oracle_residual"]) == 0),
    }
    K = class_kernel(domain, problem["rate"])
    counts = {
        "classes": len(domain["summary_model"]["classes"]),
        "beliefs": len(rows),
        "profile_atoms": domain["reconstruction"]["profile_atoms"],
        "kernel_atoms": sum(map(len, K)),
        "posterior_atoms": sum(len(row["posterior"]) for row in rows),
        "readout_cells": {
            name: sum(len(row["readouts"][name]["cells"]) for row in rows) for name in NAMES
        },
        "readout_posterior_atoms": {
            name: sum(len(c["posterior"]) for row in rows for c in row["readouts"][name]["cells"])
            for name in NAMES
        },
        "readout_prediction_atoms": {
            name: sum(len(c["prediction"]) for row in rows for c in row["readouts"][name]["cells"])
            for name in NAMES
        },
        "refinement_parents": [
            sum(len(row["refinements"][i]["parent_checks"]) for row in rows) for i in range(3)
        ],
        "strict_gain_beliefs": {
            name: sum(fraction(row["readouts"][name]["gain"]) > 0 for row in rows) for name in NAMES
        },
        "no_gain_beliefs": {
            name: sum(fraction(row["readouts"][name]["gain"]) == 0 for row in rows)
            for name in NAMES
        },
        "positive_oracle_residual_beliefs": sum(
            fraction(row["oracle_residual"]) > 0 for row in rows
        ),
        "known_N_beliefs": sum(row["checks"]["N_already_known"] for row in rows),
    }
    require(
        sum(counts["readout_cells"].values()) <= 32768
        and sum(counts["readout_posterior_atoms"].values()) <= 786432
        and sum(counts["readout_prediction_atoms"].values()) <= 1048576,
        "retention resource caps",
    )
    return {
        "model_sha256": digest(canonical(domain["summary_model"])),
        "reconstruction": domain["reconstruction"],
        "rate": problem["rate"],
        "kernel_sha256": digest(canonical(kernel_wire(K))),
        "readout_maps": readout_maps(domain["summary_model"]),
        "beliefs": rows,
        "aggregate": aggregate,
        "witnesses": witnesses,
        "counts": counts,
    }


def expected_readout_value(raw_model, case, domain=None):
    validate_model(raw_model)
    validate_v_case(case, raw_model)
    if domain is None:
        domain = json.loads(independent_domain_bytes(canonical(raw_model)))
    source = expected_filtering(raw_model, original_case(case), domain)
    require_same_wire(source, case["u_analysis"], "complete U producer filtering evidence")
    problem = v_case_problem(domain["summary_model"], case)
    histories, _ = raw_current_histories(domain, case)
    require(len(histories) == len(problem["beliefs"]), "all U histories authenticated")
    K = class_kernel(domain, problem["rate"])
    future_cache = {}

    def future(sid):
        if sid not in future_cache:
            law = {}
            for target, probability in raw_row(domain, sid, problem["rate"]).items():
                add_mass(law, tuple(domain["raw_labels"][target]["question"]), probability)
            future_cache[sid] = law
        return future_cache[sid]

    rows = []
    for entry, received in zip(problem["beliefs"], source["histories"], strict=True):
        key = tuple(tuple(value) for value in received["observations"])
        raw_joint = histories[key]
        require(
            sum(raw_joint.values(), F(0)) == fraction(entry["weight"]),
            "U history likelihood from raw paths",
        )
        rows.append(
            analyze_raw_readout_belief(
                domain, entry, normalized(raw_joint), problem["rate"], K, future
            )
        )
    analysis = compile_readout_value(domain, problem, rows)
    require_same_wire(
        analysis["aggregate"]["prediction"],
        source["unconditional"]["next_prediction"],
        "U fixed marginal Q3",
    )
    mixed_current = {}
    for row in rows:
        for atom in row["posterior"]:
            add_mass(
                mixed_current,
                atom["class_id"],
                fraction(row["weight"]) * fraction(atom["probability"]),
            )
    require_same_wire(
        belief(mixed_current), source["unconditional"]["after_second"], "U current marginal"
    )
    residual = sum(
        (
            weight * risk(question_push(K[h], domain["summary_model"]["labels"]))
            for h, weight in mixed_current.items()
        ),
        F(0),
    )
    require(
        fq(residual) == analysis["aggregate"]["oracle_residual"],
        "aggregate oracle from unconditional H2",
    )
    return analysis


@lru_cache(maxsize=8)
def expected_readout_value_bytes(raw_bytes, case_bytes):
    return canonical(expected_readout_value(json.loads(raw_bytes), json.loads(case_bytes)))


def check_readout_value(a, raw_model, case):
    require_wire(a)
    validate_model(raw_model)
    validate_v_case(case, raw_model)
    expected = expected_readout_value_bytes(canonical(raw_model), canonical(case))
    require(canonical(a) == expected, "complete independent V raw readout audit differs")
    return {"analysis_sha256": digest(expected), "complete_native_output_equal": True}


def v_raw_bridge(data, domain):
    producer = prior_json(U_PRIOR)["suite"]
    require_same_wire(data["raw_model"], producer["raw_model"], "pinned U raw model")
    require_same_wire(
        data["model"], domain["summary_model"], "all-member U local/label input authentication"
    )
    before = producer["raw_bridge"]
    pairs = {
        "features_sha256": digest(canonical(domain["features"])),
        "H_sha256": digest(canonical(domain["H"])),
        "raw_local_sha256": digest(canonical(domain["raw_local"])),
        "fine_sha256": domain["fine_sha256"],
        "fine_atoms": domain["fine_atoms"],
        "profiles_sha256": domain["reconstruction"]["profiles_sha256"],
        "raw_deletion_choices": domain["local_choices"],
        "member_comparisons": domain["member_comparisons"],
    }
    for key, value in pairs.items():
        require_same_wire(value, before[key], "U bridge identity " + key)
    return {
        "prior_artifact": U_PRIOR,
        "raw_model_local_labels_and_beliefs_declared_dependencies": True,
        "states": len(domain["features"]),
        "classes": len(domain["H"]["classes"]),
        **pairs,
        "all_raw_members_authenticated": True,
        "U_complete_case_evidence_recomputed": True,
        "U_native_API_conditioning_calls_replayed": False,
        "source_aliases_regenerated": False,
        "T_minimality_P_consumer_R_helper_Q_certificate_replayed": False,
    }


def rate_audit(domain, cases):
    rates = sorted({rate_key(case["rates"][2]) for case in cases})
    ids = domain["H"]["state_classes"]
    reports = []
    for rate in rates:
        decoded = [list(pair) for pair in rate]
        K = class_kernel(domain, decoded)
        atoms = 0
        for sid in range(len(ids)):
            actual = {}
            for target, probability in raw_row(domain, sid, decoded).items():
                add_mass(actual, ids[target], probability)
                atoms += 1
            require(actual == K[ids[sid]], "every raw member fixed K3 law")
        reports.append(
            {
                "rate": decoded,
                "raw_rows_checked": len(ids),
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


V_PRIOR = "qr-05v-readout-value-2026-09-06/results.json"
LEVELS = (F(0), F(1, 2), F(3, 4), F(1))
GARBLING_LEVELS = (F(1, 2), F(1, 2), F(1))


def fixtures():
    source = prior_json(V_PRIOR)["suite"]
    return {
        "raw_model": source["raw_model"],
        "model": source["model"],
        "cases": [
            {**{k: v for k, v in case.items() if k != "analysis"}, "v_analysis": case["analysis"]}
            for case in source["cases"]
        ],
    }


def v_case(case):
    return {k: case[k] for k in ("case_id", "raw_prior", "prior", "rates", "u_analysis")}


def case_problem(model, case):
    return {
        "schema_version": "det8-qr05w-problem-v1",
        "family": "qr05w_noisy_readouts",
        "model": model,
        "rate": case["rates"][2],
        "beliefs": [
            {k: row[k] for k in ("belief_id", "weight", "posterior")}
            for row in case["v_analysis"]["beliefs"]
        ],
    }


def validate_w_case(case, raw_model):
    require_wire(case)
    require(
        type(case) is dict
        and set(case) == {"case_id", "raw_prior", "prior", "rates", "u_analysis", "v_analysis"},
        "W producer case schema",
    )
    validate_v_case(v_case(case), raw_model)
    require(type(case["v_analysis"]) is dict, "V evidence object")


def alphabet_of(domain):
    fibers = {}
    for label in domain["raw_labels"]:
        a = tuple(label["question"])
        n = tuple(label["observation"])
        require(a[:5] == n, "every raw current question refines N")
        fibers.setdefault(n, set()).add(a)
    return {n: tuple(sorted(values)) for n, values in sorted(fibers.items())}


def noise_probability(source, target, level, fibers):
    if source[:5] != target[:5]:
        return F(0)
    values = fibers[source[:5]]
    require(source in values and target in values, "channel symbols in fixed global fiber")
    # Expand the two mutually exclusive coin events, without observing them.
    return (1 - level if source == target else F(0)) + level * F(1, len(values))


def channel_rows_wire(rows):
    return [
        {
            "source": list(source),
            "transitions": [
                {"value": list(target), "probability": fq(probability)}
                for target, probability in sorted(row.items())
            ],
        }
        for source, row in sorted(rows.items())
    ]


def channel_model_from_raw(domain):
    fibers = alphabet_of(domain)
    require(1 <= sum(map(len, fibers.values())) <= 512, "global distinct alphabet cap")
    values = sorted(value for group in fibers.values() for value in group)
    channels, rows = [], []
    total_atoms = 0
    for level in LEVELS:
        current = {}
        for source in values:
            row = {
                target: noise_probability(source, target, level, fibers)
                for target in fibers[source[:5]]
            }
            row = {target: p for target, p in row.items() if p}
            require(sum(row.values(), F(0)) == 1, "global channel row mass")
            require(
                all(p > 0 and source[:5] == target[:5] for target, p in row.items()),
                "positive N-preserving channel row",
            )
            current[source] = row
            total_atoms += len(row)
            require(total_atoms <= 1048576, "global channel atom cap")
        rows.append(current)
        channels.append({"level": fq(level), "rows": channel_rows_wire(current)})
    planned = sum(len(group) ** 2 + 2 * len(group) ** 3 for group in fibers.values())
    require(planned <= 4194304, "planned composition work cap before products")
    actual_total, checks = 0, []
    for i, delta in enumerate(GARBLING_LEVELS):
        composed, terms = {}, 0
        for source in values:
            row = {}
            for middle, p in rows[i][source].items():
                for target in fibers[middle[:5]]:
                    g = noise_probability(middle, target, delta, fibers)
                    if g:
                        add_mass(row, target, p * g)
                        terms += 1
            require(row == rows[i + 1][source], "all-source stochastic channel composition")
            composed[source] = row
        encoded = channel_rows_wire(composed)
        require_same_wire(encoded, channels[i + 1]["rows"], "native complete composition rows")
        checks.append(
            {
                "from_index": i,
                "to_index": i + 1,
                "garbling_level": fq(delta),
                "row_comparisons": len(values),
                "product_terms": terms,
                "positive_composed_atoms": sum(map(len, composed.values())),
                "composed_sha256": digest(canonical(encoded)),
                "exact": True,
            }
        )
        actual_total += terms
    require(actual_total == planned, "actual composition product count")
    return {
        "alphabet": [
            {"N": list(n), "values": [list(a) for a in group]} for n, group in fibers.items()
        ],
        "channels": channels,
        "composition_checks": checks,
    }, fibers


def score_cells(cells, base):
    require(sum(c["weight"] for c in cells) == 1, "all positive cells have unit marginal mass")
    require(
        merge_cells(cells, F(1), "posterior") == base["posterior"],
        "channel leaves current belief unchanged",
    )
    require(
        merge_cells(cells, F(1), "prediction") == base["prediction"],
        "channel leaves future law unchanged",
    )
    expected = sum((c["weight"] * c["risk"] for c in cells), F(0))
    gain = base["risk"] - expected
    variance = sum(
        (weighted_distance(c["prediction"], base["prediction"], c["weight"]) for c in cells), F(0)
    )
    require(gain == variance and gain >= 0, "channel baseline risk/variance identity")
    return expected, gain, variance


def make_raw_garbling(domain, raw_current, rate_index, earlier, later, fibers, future):
    level, delta = LEVELS[rate_index], GARBLING_LEVELS[rate_index]
    earlier_map = {c["value"]: c for c in earlier}
    later_map = {c["value"]: c for c in later}
    # Independently enumerate current raw state and BOTH unobserved report
    # randomizations. No V deterministic-parent helper is used here.
    pair_raw = {}
    for sid, current_weight in raw_current.items():
        source = tuple(domain["raw_labels"][sid]["question"])
        for z in fibers[source[:5]]:
            pz = noise_probability(source, z, level, fibers)
            if not pz:
                continue
            for w in fibers[source[:5]]:
                pw = noise_probability(z, w, delta, fibers)
                if pw:
                    add_mass(pair_raw.setdefault((z, w), {}), sid, current_weight * pz * pw)
    require(len(pair_raw) <= 1048576, "single-belief report pair cap")
    pairs, incoming, left_mass, right_mass = [], {}, {}, {}
    for (z, w), mass in sorted(pair_raw.items()):
        pair = raw_cell(domain, mass, (), future)
        weight = pair["weight"]
        require(
            weight == earlier_map[z]["weight"] * noise_probability(z, w, delta, fibers),
            "raw Markov report-pair probability",
        )
        require(
            pair["posterior"] == earlier_map[z]["posterior"],
            "garbling coin does not reveal extra current information",
        )
        require(
            pair["prediction"] == earlier_map[z]["prediction"],
            "garbling coin does not reveal extra future information",
        )
        add_mass(left_mass, z, weight)
        add_mass(right_mass, w, weight)
        incoming.setdefault(w, []).append((z, weight))
        pairs.append({"earlier": list(z), "later": list(w), "probability": fq(weight)})
    require(
        left_mass == {z: c["weight"] for z, c in earlier_map.items()}, "earlier coupling marginal"
    )
    require(right_mass == {w: c["weight"] for w, c in later_map.items()}, "later coupling marginal")
    require(sum(left_mass.values(), F(0)) == 1, "joint report coupling mass")
    receiving, total_increase, total_variance = [], F(0), F(0)
    for w, receiver in sorted(later_map.items()):
        posterior, prediction = {}, {}
        earlier_risk, variance = F(0), F(0)
        equalities, sources = [], []
        for z, joint_weight in incoming[w]:
            cell = earlier_map[z]
            alpha = joint_weight / receiver["weight"]
            for h, p in cell["posterior"].items():
                add_mass(posterior, h, alpha * p)
            for q, p in cell["prediction"].items():
                add_mass(prediction, q, alpha * p)
            earlier_risk += alpha * cell["risk"]
            variance += weighted_distance(cell["prediction"], receiver["prediction"], alpha)
            equalities.append(cell["prediction"] == receiver["prediction"])
            sources.append(list(z))
        require(posterior == receiver["posterior"], "later complete current posterior mixture")
        require(prediction == receiver["prediction"], "later complete future law mixture")
        increase = receiver["risk"] - earlier_risk
        equal = all(equalities)
        require(increase == variance and increase >= 0, "conditional garbling variance loss")
        require((increase == 0) == equal, "conditional zero loss iff coupled laws agree")
        receiving.append(
            {
                "value": list(w),
                "probability": fq(receiver["weight"]),
                "earlier_values": sources,
                "posterior_mixture_sha256": digest(canonical(belief(posterior))),
                "prediction_mixture_sha256": digest(canonical(question_law(prediction))),
                "conditional_risk_increase": fq(increase),
                "conditional_variance_loss": fq(variance),
                "predictions_equal": equal,
            }
        )
        total_increase += receiver["weight"] * increase
        total_variance += receiver["weight"] * variance
    direct = sum((c["weight"] * c["risk"] for c in later), F(0)) - sum(
        (c["weight"] * c["risk"] for c in earlier), F(0)
    )
    require(total_increase == total_variance == direct >= 0, "global risk data processing")
    require(
        (direct == 0) == all(c["predictions_equal"] for c in receiving),
        "global zero loss iff all positive coupling laws agree",
    )
    return {
        "from_index": rate_index,
        "to_index": rate_index + 1,
        "garbling_level": fq(delta),
        "risk_increase": fq(total_increase),
        "variance_loss": fq(total_variance),
        "couplings": pairs,
        "receiving_checks": receiving,
        "zero_loss_iff_equal": True,
    }


def raw_noise_belief(domain, entry, raw_current, v_row, fibers, future):
    base = raw_cell(domain, raw_current, (), future)
    require_same_wire(
        belief(base["posterior"]), entry["posterior"], "V current belief authentication"
    )
    require_same_wire(
        {"prediction": question_law(base["prediction"]), "risk": fq(base["risk"])},
        v_row["baseline"],
        "V complete baseline authentication",
    )
    n_mass = {}
    for sid, weight in raw_current.items():
        n = tuple(domain["raw_labels"][sid]["observation"])
        add_mass(n_mass.setdefault(n, {}), sid, weight)
    n_cells = [raw_cell(domain, mass, n, future) for n, mass in sorted(n_mass.items())]
    n_risk, n_gain, _ = score_cells(n_cells, base)
    n_control = {
        "cells": [cell_wire(c) for c in n_cells],
        "expected_risk": fq(n_risk),
        "gain": fq(n_gain),
    }
    require_same_wire(
        n_control, {k: v_row["readouts"]["N"][k] for k in n_control}, "unchanged V deterministic N"
    )
    n_index = {c["value"]: c for c in n_cells}
    residual = sum((p * risk(future(sid)) for sid, p in raw_current.items()), F(0))
    h_control = {"expected_risk": fq(residual), "gain": fq(base["risk"] - residual)}
    require_same_wire(
        h_control,
        {k: v_row["readouts"]["H"][k] for k in h_control},
        "unchanged V full-H oracle residual",
    )
    all_cells, reports, risks = [], [], []
    for level in LEVELS:
        masses = {}
        for sid, p in raw_current.items():
            true_a = tuple(domain["raw_labels"][sid]["question"])
            for displayed in fibers[true_a[:5]]:
                coefficient = noise_probability(true_a, displayed, level, fibers)
                if coefficient:
                    add_mass(masses.setdefault(displayed, {}), sid, p * coefficient)
        cells = [raw_cell(domain, mass, a, future) for a, mass in sorted(masses.items())]
        expected, gain, variance = score_cells(cells, base)
        added = n_risk - expected
        require(added >= 0, "all noisy reports still contain exact N")
        all_cells.append(cells)
        risks.append(expected)
        reports.append(
            {
                "level": fq(level),
                "cells": [cell_wire(c) for c in cells],
                "expected_risk": fq(expected),
                "gain": fq(gain),
                "variance_gain": fq(variance),
                "gain_over_N": fq(added),
                "retained_gain_fraction": None,
            }
        )
    clean_gain = n_risk - risks[0]
    for i, report in enumerate(reports):
        added = fraction(report["gain_over_N"])
        report["retained_gain_fraction"] = fq(added / clean_gain) if clean_gain else None
        # Independently verify the preregistered family formula. Zero clean
        # symbol probabilities do not create nonexistent conditional laws.
        formula = F(0)
        t = LEVELS[i]
        for clean in all_cells[0]:
            parent = n_index[clean["value"][:5]]
            alpha = clean["weight"] / parent["weight"]
            w = (1 - t) * alpha + t / len(fibers[parent["value"]])
            term_weight = parent["weight"] * (1 - t) ** 2 * alpha**2 / w
            formula += weighted_distance(clean["prediction"], parent["prediction"], term_weight)
        require(added == formula, "family-specific quantitative gain formula")
        if t < 1:
            require((added > 0) == (clean_gain > 0), "family-implied strict added-gain survival")
    require_same_wire(
        reports[0]["cells"], v_row["readouts"]["NMT"]["cells"], "t=0 complete clean NMT cells"
    )
    require(reports[0]["expected_risk"] == v_row["readouts"]["NMT"]["expected_risk"], "t=0 V risk")
    endpoint_cells = {c["value"]: c for c in all_cells[-1]}
    for n, parent in n_index.items():
        for displayed in fibers[n]:
            cell = endpoint_cells[displayed]
            require(
                cell["weight"] == parent["weight"] / len(fibers[n]), "full-replacement output mass"
            )
            require(
                cell["posterior"] == parent["posterior"]
                and cell["prediction"] == parent["prediction"],
                "full replacement is N-information equivalent",
            )
    require(
        len(endpoint_cells) == sum(len(fibers[n]) for n in n_index), "full endpoint symbol coverage"
    )
    require(risks[-1] == n_risk, "full replacement expected risk equals N")
    require(
        residual <= risks[0] <= risks[1] <= risks[2] <= risks[3] <= base["risk"],
        "oracle/noise/N/baseline expected-risk order",
    )
    garblings = [
        make_raw_garbling(domain, raw_current, i, all_cells[i], all_cells[i + 1], fibers, future)
        for i in range(3)
    ]
    require(
        sum((fraction(g["risk_increase"]) for g in garblings), F(0)) == risks[-1] - risks[0],
        "adjacent losses telescope",
    )
    known_n = len(n_cells) == 1
    require(known_n and n_gain == 0, "actual U history already knows N")
    return {
        "belief_id": entry["belief_id"],
        "weight": entry["weight"],
        "posterior": entry["posterior"],
        "baseline": {"prediction": question_law(base["prediction"]), "risk": fq(base["risk"])},
        "controls": {"N": n_control, "H": h_control},
        "channels": reports,
        "garblings": garblings,
        "checks": {
            **{
                key: True
                for key in (
                    "probabilities_normalized",
                    "marginal_current_preserved",
                    "marginal_future_preserved",
                    "garbling_marginals",
                    "conditional_mixtures",
                    "risk_order",
                    "endpoint_information_equivalence",
                    "losses_telescope",
                )
            },
            "N_already_known": known_n,
        },
    }


def compile_noise_analysis(domain, problem, rows, channel_model):
    weights = [fraction(row["weight"]) for row in rows]
    require(sum(weights, F(0)) == 1, "case likelihood weights normalize")

    def average(values):
        return sum((p * x for p, x in zip(weights, values, strict=True)), F(0))

    baseline = average([fraction(row["baseline"]["risk"]) for row in rows])
    n_risk = average([fraction(row["controls"]["N"]["expected_risk"]) for row in rows])
    h_risk = average([fraction(row["controls"]["H"]["expected_risk"]) for row in rows])
    prediction = {}
    for weight, row in zip(weights, rows, strict=True):
        for atom in row["baseline"]["prediction"]:
            add_mass(prediction, tuple(atom["value"]), weight * fraction(atom["probability"]))
    channels = []
    for i, level in enumerate(LEVELS):
        expected = average([fraction(row["channels"][i]["expected_risk"]) for row in rows])
        gain = average([fraction(row["channels"][i]["gain"]) for row in rows])
        added = average([fraction(row["channels"][i]["gain_over_N"]) for row in rows])
        require(
            gain == baseline - expected and added == n_risk - expected,
            "weighted risk/gain identities",
        )
        channels.append(
            {
                "level": fq(level),
                "expected_risk": fq(expected),
                "gain": fq(gain),
                "gain_over_N": fq(added),
                "retained_gain_fraction": None,
            }
        )
    clean_gain = fraction(channels[0]["gain_over_N"])
    for row in channels:
        row["retained_gain_fraction"] = (
            fq(fraction(row["gain_over_N"]) / clean_gain) if clean_gain else None
        )
    adjacent = [
        average([fraction(row["garblings"][i]["risk_increase"]) for row in rows]) for i in range(3)
    ]
    risks = [fraction(c["expected_risk"]) for c in channels]
    require(
        h_risk <= risks[0] <= risks[1] <= risks[2] <= risks[3] == n_risk <= baseline,
        "case-weighted expected-risk order",
    )
    require(sum(adjacent, F(0)) == n_risk - risks[0], "case-weighted losses telescope")
    require(
        all(adjacent[i] == risks[i + 1] - risks[i] for i in range(3)),
        "case-weighted adjacent risk differences",
    )
    aggregate = {
        "total_weight": [1, 1],
        "prediction": question_law(prediction),
        "baseline_risk": fq(baseline),
        "N_risk": fq(n_risk),
        "H_risk": fq(h_risk),
        "channels": channels,
        "adjacent_risk_increase": [fq(x) for x in adjacent],
    }

    def first(predicate):
        return next((row["belief_id"] for row in rows if predicate(row)), None)

    witnesses = {
        "first_strict_gain": [
            first(lambda row, i=i: fraction(row["channels"][i]["gain_over_N"]) > 0)
            for i in range(4)
        ],
        "first_zero_gain": [
            first(lambda row, i=i: fraction(row["channels"][i]["gain_over_N"]) == 0)
            for i in range(4)
        ],
        "first_strict_loss": [
            first(lambda row, i=i: fraction(row["garblings"][i]["risk_increase"]) > 0)
            for i in range(3)
        ],
        "first_zero_loss": [
            first(lambda row, i=i: fraction(row["garblings"][i]["risk_increase"]) == 0)
            for i in range(3)
        ],
        "first_positive_oracle_residual": first(
            lambda row: fraction(row["controls"]["H"]["expected_risk"]) > 0
        ),
        "first_zero_oracle_residual": first(
            lambda row: fraction(row["controls"]["H"]["expected_risk"]) == 0
        ),
    }
    K = class_kernel(domain, problem["rate"])
    counts = {
        "classes": len(domain["summary_model"]["classes"]),
        "beliefs": len(rows),
        "profile_atoms": domain["reconstruction"]["profile_atoms"],
        "kernel_atoms": sum(map(len, K)),
        "alphabet_fibers": len(channel_model["alphabet"]),
        "alphabet_values": sum(len(f["values"]) for f in channel_model["alphabet"]),
        "global_channel_atoms": [
            sum(len(row["transitions"]) for row in c["rows"]) for c in channel_model["channels"]
        ],
        "posterior_atoms": sum(len(row["posterior"]) for row in rows),
        "channel_cells": [sum(len(row["channels"][i]["cells"]) for row in rows) for i in range(4)],
        "channel_posterior_atoms": [
            sum(len(c["posterior"]) for row in rows for c in row["channels"][i]["cells"])
            for i in range(4)
        ],
        "channel_prediction_atoms": [
            sum(len(c["prediction"]) for row in rows for c in row["channels"][i]["cells"])
            for i in range(4)
        ],
        "N_cells": sum(len(row["controls"]["N"]["cells"]) for row in rows),
        "N_posterior_atoms": sum(
            len(c["posterior"]) for row in rows for c in row["controls"]["N"]["cells"]
        ),
        "N_prediction_atoms": sum(
            len(c["prediction"]) for row in rows for c in row["controls"]["N"]["cells"]
        ),
        "coupling_atoms": [
            sum(len(row["garblings"][i]["couplings"]) for row in rows) for i in range(3)
        ],
        "receiving_checks": [
            sum(len(row["garblings"][i]["receiving_checks"]) for row in rows) for i in range(3)
        ],
        "strict_gain_beliefs": [
            sum(fraction(row["channels"][i]["gain_over_N"]) > 0 for row in rows) for i in range(4)
        ],
        "no_gain_beliefs": [
            sum(fraction(row["channels"][i]["gain_over_N"]) == 0 for row in rows) for i in range(4)
        ],
        "strict_loss_beliefs": [
            sum(fraction(row["garblings"][i]["risk_increase"]) > 0 for row in rows)
            for i in range(3)
        ],
        "no_loss_beliefs": [
            sum(fraction(row["garblings"][i]["risk_increase"]) == 0 for row in rows)
            for i in range(3)
        ],
        "positive_oracle_residual_beliefs": sum(
            fraction(row["controls"]["H"]["expected_risk"]) > 0 for row in rows
        ),
        "known_N_beliefs": sum(row["checks"]["N_already_known"] for row in rows),
    }
    require(counts["N_cells"] + sum(counts["channel_cells"]) <= 32768, "all retained cells cap")
    require(
        counts["N_posterior_atoms"] + sum(counts["channel_posterior_atoms"]) <= 1048576,
        "all retained posterior atoms cap",
    )
    require(
        counts["N_prediction_atoms"] + sum(counts["channel_prediction_atoms"]) <= 2097152,
        "all retained prediction atoms cap",
    )
    require(
        sum(counts["coupling_atoms"]) <= 1048576 and sum(counts["receiving_checks"]) <= 32768,
        "retained stochastic coupling/check caps",
    )
    return {
        "model_sha256": digest(canonical(domain["summary_model"])),
        "reconstruction": domain["reconstruction"],
        "rate": problem["rate"],
        "kernel_sha256": digest(canonical(kernel_wire(K))),
        "channel_model": channel_model,
        "beliefs": rows,
        "aggregate": aggregate,
        "witnesses": witnesses,
        "counts": counts,
    }


def expected_analysis(raw_model, case, domain=None):
    validate_model(raw_model)
    validate_w_case(case, raw_model)
    if domain is None:
        domain = json.loads(independent_domain_bytes(canonical(raw_model)))
    producer = expected_readout_value(raw_model, v_case(case), domain)
    require_same_wire(
        producer, case["v_analysis"], "complete V producer deterministic readout evidence"
    )
    problem = case_problem(domain["summary_model"], case)
    require_same_wire(
        problem["beliefs"],
        v_case_problem(domain["summary_model"], v_case(case))["beliefs"],
        "U/V complete current belief correspondence",
    )
    channel_model, fibers = channel_model_from_raw(domain)
    histories, _ = raw_current_histories(domain, case)
    future_cache = {}

    def future(sid):
        if sid not in future_cache:
            law = {}
            for target, probability in raw_row(domain, sid, problem["rate"]).items():
                add_mass(law, tuple(domain["raw_labels"][target]["question"]), probability)
            future_cache[sid] = law
        return future_cache[sid]

    rows = []
    for entry, received, v_row in zip(
        problem["beliefs"], case["u_analysis"]["histories"], producer["beliefs"], strict=True
    ):
        key = tuple(tuple(value) for value in received["observations"])
        raw_joint = histories[key]
        require(sum(raw_joint.values(), F(0)) == fraction(entry["weight"]), "raw W likelihood")
        rows.append(raw_noise_belief(domain, entry, normalized(raw_joint), v_row, fibers, future))
    analysis = compile_noise_analysis(domain, problem, rows, channel_model)
    require_same_wire(
        analysis["aggregate"]["prediction"],
        producer["aggregate"]["prediction"],
        "unchanged V aggregate future law",
    )
    require(
        analysis["aggregate"]["baseline_risk"] == producer["aggregate"]["baseline_risk"]
        and analysis["aggregate"]["N_risk"] == producer["aggregate"]["expected_risk"]["N"]
        and analysis["aggregate"]["H_risk"] == producer["aggregate"]["expected_risk"]["H"],
        "unchanged V aggregate controls",
    )
    return analysis


@lru_cache(maxsize=8)
def expected_analysis_bytes(raw_bytes, case_bytes):
    return canonical(expected_analysis(json.loads(raw_bytes), json.loads(case_bytes)))


def check_analysis(a, raw_model, case):
    require_wire(a)
    validate_model(raw_model)
    validate_w_case(case, raw_model)
    expected = expected_analysis_bytes(canonical(raw_model), canonical(case))
    require(canonical(a) == expected, "complete independent W raw noisy-readout audit differs")
    return {"analysis_sha256": digest(expected), "complete_native_output_equal": True}


def raw_bridge(data, domain):
    producer = prior_json(V_PRIOR)["suite"]
    require_same_wire(data["raw_model"], producer["raw_model"], "pinned V raw model")
    require_same_wire(
        data["model"], domain["summary_model"], "all-member V local/label authentication"
    )
    before = producer["raw_bridge"]
    pairs = {
        "features_sha256": digest(canonical(domain["features"])),
        "H_sha256": digest(canonical(domain["H"])),
        "raw_local_sha256": digest(canonical(domain["raw_local"])),
        "fine_sha256": domain["fine_sha256"],
        "fine_atoms": domain["fine_atoms"],
        "profiles_sha256": domain["reconstruction"]["profiles_sha256"],
        "raw_deletion_choices": domain["local_choices"],
        "member_comparisons": domain["member_comparisons"],
    }
    for key, value in pairs.items():
        require_same_wire(value, before[key], "V raw producer bridge identity " + key)
    return {
        "prior_artifact": V_PRIOR,
        "raw_model_local_labels_beliefs_and_V_readouts_declared_dependencies": True,
        "states": len(domain["features"]),
        "classes": len(domain["H"]["classes"]),
        **pairs,
        "all_raw_members_authenticated": True,
        "U_complete_case_evidence_recomputed": True,
        "V_complete_readout_evidence_recomputed": True,
        "U_V_native_API_calls_replayed": False,
        "source_aliases_regenerated": False,
        "T_minimality_P_consumer_R_helper_Q_certificate_replayed": False,
    }


def run_suite():
    direct = load("_qr05w_primary", "noisy_readout.py")
    reference = load("_qr05w_reference", "reference_qr05w.py")
    data = fixtures()
    domain = json.loads(independent_domain_bytes(canonical(data["raw_model"])))
    bridge = raw_bridge(data, domain)
    audit = rate_audit(domain, data["cases"])
    results, invalid = [], 0
    for case in data["cases"]:
        problem = case_problem(data["model"], case)
        before = canonical(problem)
        a = direct.analyze(problem)
        require(canonical(problem) == before, "primary mutated input")
        b = reference.analyze(problem)
        require(canonical(problem) == before, "reference mutated input")
        require_same_wire(a, b, "independent W routes differ")
        check_analysis(a, data["raw_model"], case)
        results.append({**case, "analysis": a})
    first = case_problem(data["model"], data["cases"][0])
    for route in (direct, reference):
        for bad in (
            None,
            {},
            [],
            {**first, "extra": 0},
            {**first, "schema_version": "bad"},
            {**first, "rate": []},
            {**first, "beliefs": []},
        ):
            try:
                route.analyze(bad)
            except ValueError:
                invalid += 1
            else:
                raise ValueError("malformed W public input accepted")
    totals = {
        "raw_states": len(data["raw_model"]["states"]),
        "classes": len(data["model"]["classes"]),
        "cases": len(results),
        "analyze_calls": 2 * len(results),
        "invalid_analyze_calls_rejected": invalid,
        "beliefs": sum(c["analysis"]["counts"]["beliefs"] for c in results),
        "posterior_atoms": sum(c["analysis"]["counts"]["posterior_atoms"] for c in results),
        "known_N_beliefs": sum(c["analysis"]["counts"]["known_N_beliefs"] for c in results),
        "raw_rate_rows_checked": audit["raw_row_comparisons"],
        "alphabet_fibers": results[0]["analysis"]["counts"]["alphabet_fibers"],
        "alphabet_values": results[0]["analysis"]["counts"]["alphabet_values"],
        "global_channel_atoms": results[0]["analysis"]["counts"]["global_channel_atoms"],
        "composition_product_terms": sum(
            c["product_terms"]
            for c in results[0]["analysis"]["channel_model"]["composition_checks"]
        ),
        **{
            key: [sum(c["analysis"]["counts"][key][i] for c in results) for i in range(4)]
            for key in ("channel_cells", "channel_prediction_atoms", "strict_gain_beliefs")
        },
        **{
            key: [sum(c["analysis"]["counts"][key][i] for c in results) for i in range(3)]
            for key in ("coupling_atoms", "receiving_checks", "strict_loss_beliefs")
        },
        "positive_oracle_residual_beliefs": sum(
            c["analysis"]["counts"]["positive_oracle_residual_beliefs"] for c in results
        ),
    }
    for c in results:
        require_same_wire(
            c["analysis"]["channel_model"],
            results[0]["analysis"]["channel_model"],
            "fixed global channel model across experiments",
        )
    require(invalid == 14, "invalid public call inventory")
    return {
        "raw_model": data["raw_model"],
        "model": data["model"],
        "cases": results,
        "independent_route_equal": True,
        "raw_bridge": bridge,
        "rate_audit": audit,
        "public_controls": {
            "analyze_calls": 12,
            "invalid_analyze_calls_rejected": invalid,
            "raw_orders_histories_or_artifacts_given_to_core": False,
            "intermediate_reports_or_noise_flags_given_to_forecaster": False,
        },
        "totals": totals,
    }


if __name__ == "__main__":
    main()
