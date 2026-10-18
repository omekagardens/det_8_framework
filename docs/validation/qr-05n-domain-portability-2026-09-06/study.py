"""QR-05N finite domain-portability capture and read-only replay.

Lifecycle and sparse quotient audit utilities are carried locally from the
M runner; expanded domain/features/restriction checks are reconstructed here.
Prior JSON is comparison evidence, never input to either executor.
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
from itertools import combinations, product
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05n-results-v1"
BASE_COMMIT = "c991bc2fba906d88824e337e41c28d651f9c7674"
SOURCES = (
    "README.md",
    "portability.py",
    "reference_qr05n.py",
    "study.py",
    "test_qr05n.py",
    "test_capture.py",
)
PRIORS = {
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


PARTITIONS = ("pair_graded", "motif_pair")
PROFILE_NAMES = (
    "ferrers6",
    "standard_example3",
    "chain6",
    "ferrers6_fixed",
    "path6",
    "cycle4_edge",
)
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
M_PRIOR = "qr-05m-observable-realization-2026-09-06/results.json"


def fixtures():
    return [{"schema_version": "det8-qr05n-problem-v1", "family": "qr05n_layered_iid"}]


def invalid_fixtures():
    good = fixtures()[0]
    return [
        None,
        [],
        True,
        {},
        {"schema_version": good["schema_version"]},
        {"family": good["family"]},
        {**good, "extra": 1},
        *({**good, "family": v} for v in (None, True, 1, [], "wrong")),
        *({**good, "schema_version": v} for v in (None, True, 1, [], "wrong")),
        {**good, "profile": "ferrers6"},
        {**good, "design": "independent"},
    ]


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


def source_spec(index):
    if index < 6:
        name = PROFILE_NAMES[index]
    else:
        name = f"layered_{'oe' if index < 518 else 'eo'}_{(index - 6) % 512:03d}"
    edges = {(0, j) for j in range(1, 8)} | {(i, 7) for i in range(1, 7)}
    if index in (0, 1, 3):
        edges |= {
            (i + 1, j + 4) for i in range(3) for j in range(3) if (i != j if index == 1 else i <= j)
        }
    elif index == 2:
        edges |= {(i, j) for i in range(1, 7) for j in range(i + 1, 7)}
    elif index == 4:
        edges |= {(1, 2), (1, 4), (3, 4), (3, 6), (5, 6)}
    elif index == 5:
        edges |= {(1, 4), (1, 6), (3, 4), (3, 6), (2, 5)}
    else:
        h = (index - 6) % 512
        for i, j in product(range(3), repeat=2):
            if h & (1 << (3 * i + j)):
                odd, even = 2 * i + 1, 2 * j + 2
                edges.add((odd, even) if index < 518 else (even, odd))
    return name, [[i for i in range(8) if (i, j) in edges] for j in range(8)]


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


def flatten_features(state):
    return [c for table in state["mean_graded"] for row in table for c in row] + [
        c for tensor in state["pair_graded"] for table in tensor for row in table for c in row
    ]


def groups_from_vector(vector):
    groups = []
    for sid, cid in enumerate(vector):
        require(type(cid) is int and 0 <= cid <= len(groups), "canonical class vector")
        if cid == len(groups):
            groups.append({"class_id": cid, "members": []})
        groups[cid]["members"].append(sid)
    return groups


def closure_from_rows(states, groups, name):
    failure = None
    for group in groups:
        left = group["members"][0]
        lhs = {a["target_class"]: a["coefficients"] for a in states[left]["summary_laws"][name]}
        for right in group["members"][1:]:
            rhs = {
                a["target_class"]: a["coefficients"] for a in states[right]["summary_laws"][name]
            }
            different = [
                t
                for t in sorted(lhs.keys() | rhs.keys())
                if lhs.get(t, zero()) != rhs.get(t, zero())
            ]
            if different:
                t = different[0]
                failure = {
                    "class_id": group["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "target_class": t,
                    "left_coefficients": lhs.get(t, zero()),
                    "right_coefficients": rhs.get(t, zero()),
                }
                break
        if failure is not None:
            break
    rows = (
        []
        if failure is not None
        else [
            {
                "class_id": g["class_id"],
                "representative_state": g["members"][0],
                "transitions": states[g["members"][0]]["summary_laws"][name],
            }
            for g in groups
        ]
    )
    return {
        "closed": failure is None,
        "first_collision": failure,
        "quotient_rows": rows,
        "semigroup": None if failure is not None else check_semigroup(rows),
    }


def check_analysis(a):
    require_wire(a)
    require(retained_bits(a) <= 4096, "exact component cap")
    require(
        set(a)
        == {
            "frames",
            "profiles",
            "states",
            "partitions",
            "closure",
            "expected_updates",
            "motif_expected_update",
            "counts",
        },
        "analysis fields",
    )
    frames, profiles, states = a["frames"], a["profiles"], a["states"]
    require(
        len(frames) == 2 and len(profiles) == 1030 and len(states) == 2470,
        "declared domain inventory",
    )
    require(len(states) <= 2579, "state cap")
    expected_frames = [
        {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
        {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
    ]
    require_same_wire(frames, expected_frames, "frames")
    for sid, state in enumerate(states):
        require(
            type(state.get("state_id")) is int
            and state["state_id"] == sid
            and type(state.get("frame_id")) is int
            and 0 <= state["frame_id"] < len(frames),
            "native state/frame identity",
        )
        kept, past = state.get("kept"), state.get("past")
        require(
            type(kept) is list
            and all(type(v) is int and 0 <= v < 8 for v in kept)
            and kept == sorted(set(kept)),
            "native observed vertex IDs",
        )
        require(
            type(past) is list
            and len(past) == len(kept)
            and all(
                type(row) is list
                and all(type(i) is int and 0 <= i < len(kept) for i in row)
                and row == sorted(set(row))
                and j not in row
                for j, row in enumerate(past)
            ),
            "native observed predecessor indices",
        )
    lookup = {identity(s["frame_id"], s["kept"], s["past"]): s["state_id"] for s in states}
    require(len(lookup) == len(states), "deduplicated observations")
    aliases = [[] for _ in states]
    visited = set()
    for pid, profile in enumerate(profiles):
        name, past = source_spec(pid)
        frame = frames[int(pid == 3)]
        parent = {"kept": list(range(8)), "past": past}
        ids = []
        for mask in range(1 << len(frame["eligible"])):
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(frame["eligible"]) if mask & (1 << bit)]
            )
            restricted = induced_past(parent, kept)
            observed_key = identity(frame["frame_id"], kept, restricted)
            require(observed_key in lookup, "missing supplied observation")
            sid = lookup[observed_key]
            require(type(sid) is int and 0 <= sid < len(states), "state ID")
            if sid not in visited:
                require(sid == len(visited), "first-observation numbering")
                require_same_wire(
                    {k: states[sid][k] for k in ("frame_id", "kept", "past")},
                    {"frame_id": frame["frame_id"], "kept": kept, "past": restricted},
                    "first-alias observed record",
                )
                visited.add(sid)
            ids.append(sid)
            aliases[sid].append({"profile_index": pid, "mask": mask})
        require_same_wire(
            profile,
            {
                "profile_index": pid,
                "name": name,
                "frame_id": frame["frame_id"],
                "past": past,
                "state_ids": ids,
            },
            "source incidence/alias enumeration",
        )
    require(
        len(visited) == len(states) and sum(map(len, aliases)) == 65888, "complete alias universe"
    )
    partitions = {name: [] for name in PARTITIONS}
    registries = {name: {} for name in PARTITIONS}
    fields = {
        "state_id",
        "frame_id",
        "mask",
        "kept",
        "past",
        "aliases",
        "color_sizes",
        "chain_counts",
        "mean_graded",
        "pair_graded",
        "motif_supports",
        "motif_count",
        "classes",
        "transitions",
        "summary_laws",
    }
    for sid, state in enumerate(states):
        require(set(state) == fields, "state fields")
        frame = frames[state["frame_id"]]
        mask = sum(1 << bit for bit, v in enumerate(frame["eligible"]) if v in state["kept"])
        count, d, b, motifs = observed_features(state["kept"], state["past"], frame["eligible"])
        require_same_wire(
            {
                k: state[k]
                for k in (
                    "state_id",
                    "frame_id",
                    "mask",
                    "aliases",
                    "color_sizes",
                    "chain_counts",
                    "mean_graded",
                    "pair_graded",
                    "motif_supports",
                    "motif_count",
                )
            },
            {
                "state_id": sid,
                "frame_id": frame["frame_id"],
                "mask": mask,
                "aliases": aliases[sid],
                "color_sizes": [
                    sum(v % 2 for v in state["kept"] if v in frame["eligible"]),
                    sum(not v % 2 for v in state["kept"] if v in frame["eligible"]),
                ],
                "chain_counts": count,
                "mean_graded": d,
                "pair_graded": b,
                "motif_supports": motifs,
                "motif_count": len(motifs),
            },
            "observed chain/pair/motif features",
        )
        require(0 <= len(motifs) <= 9, "motif cap")
        assignments = {}
        for name in PARTITIONS:
            key = [frame_value(frame), b] + ([len(motifs)] if name == "motif_pair" else [])
            encoded = canonical(key)
            if encoded not in registries[name]:
                cid = len(registries[name])
                registries[name][encoded] = cid
                partitions[name].append({"class_id": cid, "key": key, "members": []})
            cid = registries[name][encoded]
            partitions[name][cid]["members"].append(sid)
            assignments[name] = cid
        require_same_wire(state["classes"], assignments, "candidate computed keys")
    require_same_wire(a["partitions"], partitions, "actual partition fibers and keys")
    feature_rows = [flatten_features(s) for s in states]
    feature_nonzero = [[(i, v) for i, v in enumerate(row) if v] for row in feature_rows]
    updates, motif_updates = [], []
    fine_atoms = pushed_atoms = fine_evaluations = pushed_evaluations = corners = 0
    for state in states:
        frame = frames[state["frame_id"]]
        O, E = state["color_sizes"]
        expected_fine, children = [], {}
        for mask in range(1 << len(frame["eligible"])):
            if mask & ~state["mask"]:
                continue
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(frame["eligible"]) if mask & (1 << bit)]
            )
            past = induced_past(state, kept)
            child_key = identity(state["frame_id"], kept, past)
            require(child_key in lookup, "missing induced successor")
            target = lookup[child_key]
            children[mask] = target
            o, e = states[target]["color_sizes"]
            expected_fine.append(
                {"target_state": target, "coefficients": [list(row) for row in kernel(O, E, o, e)]}
            )
        expected_fine.sort(key=lambda atom: atom["target_state"])
        require_same_wire(state["transitions"], expected_fine, "complete fine polynomial row")
        expected_pushed = {}
        for name in PARTITIONS:
            tables = {}
            for atom in expected_fine:
                cid = states[atom["target_state"]]["classes"][name]
                add_table(tables.setdefault(cid, zero()), atom["coefficients"])
            expected_pushed[name] = [
                {"target_class": cid, "coefficients": tables[cid]} for cid in sorted(tables)
            ]
        require_same_wire(state["summary_laws"], expected_pushed, "complete pushed polynomial rows")
        fine_atoms += len(expected_fine)
        pushed_atoms += sum(len(row) for row in expected_pushed.values())
        actual = [[0] * 16 for _ in range(320)]
        motif_actual = zero()
        for atom in expected_fine:
            target = states[atom["target_state"]]
            table = tuple(tuple(row) for row in atom["coefficients"])
            for f, value in feature_nonzero[target["state_id"]]:
                for degree, c in sparse(table):
                    actual[f][degree] += value * c
            add_table(motif_actual, table, target["motif_count"])
            require(
                eval_rates(table) == direct_rates(O, E, *target["color_sizes"]),
                "fine rational-grid law",
            )
            fine_evaluations += len(AUDIT_POINTS)
        for f, row in enumerate(actual):
            value = feature_rows[state["state_id"]][f]
            require(
                row == [value if d == f % 16 else 0 for d in range(16)],
                "support expected update cells",
            )
        updates.append(
            {
                "state_id": state["state_id"],
                "mean_features": 64,
                "pair_features": 256,
                "coefficient_cells": 5120,
                "max_abs_residual": 0,
            }
        )
        motif_expected = zero()
        motif_expected[2][2] = state["motif_count"]
        require_same_wire(motif_actual, motif_expected, "motif expectation cells")
        motif_updates.append(
            {
                "state_id": state["state_id"],
                "coefficients": motif_actual,
                "expected_coefficients": motif_expected,
                "max_abs_residual": 0,
            }
        )
        for row in [expected_fine, *expected_pushed.values()]:
            total = zero()
            evaluated = [F(0)] * len(AUDIT_POINTS)
            for atom in row:
                add_table(total, atom["coefficients"])
                values = eval_rates(tuple(tuple(r) for r in atom["coefficients"]))
                require(all(v >= 0 for v in values), "rate atom sign")
                for n, v in enumerate(values):
                    evaluated[n] += v
            require_same_wire(
                total,
                [[int(i == 0 and j == 0) for j in range(4)] for i in range(4)],
                "coefficient normalization",
            )
            require(all(v == 1 for v in evaluated), "rate normalization")
        pushed_evaluations += len(AUDIT_POINTS) * sum(len(row) for row in expected_pushed.values())
        for n, (x, y) in enumerate(AUDIT_POINTS):
            if x not in (0, 1) or y not in (0, 1):
                continue
            mask = sum(
                1 << bit
                for bit, v in enumerate(frame["eligible"])
                if state["mask"] & (1 << bit) and (x if v % 2 else y) == 1
            )
            target = children[mask]
            for name, row, target_field, wanted in [
                ("fine", expected_fine, "target_state", target),
                *[
                    (name, expected_pushed[name], "target_class", states[target]["classes"][name])
                    for name in PARTITIONS
                ],
            ]:
                positive = {
                    atom[target_field]: eval_rates(tuple(tuple(r) for r in atom["coefficients"]))[n]
                    for atom in row
                    if eval_rates(tuple(tuple(r) for r in atom["coefficients"]))[n]
                }
                require(positive == {wanted: F(1)}, "deterministic corner " + name)
            corners += 1
    require(fine_atoms == 99180 and fine_atoms <= 100393, "fine atom count/cap")
    expected_updates = {"verified": True, "rows": updates, "coefficient_cells": 5120 * len(states)}
    motif_expected_update = {
        "verified": True,
        "rows": motif_updates,
        "coefficient_cells": 16 * len(states),
    }
    require_same_wire(a["expected_updates"], expected_updates, "expected update inventory")
    require_same_wire(a["motif_expected_update"], motif_expected_update, "motif update inventory")
    closures = {name: closure_from_rows(states, partitions[name], name) for name in PARTITIONS}
    require_same_wire(a["closure"], closures, "closure decision/witness/quotient")
    closed = [r for r in closures.values() if r["closed"]]
    counts = {
        "frames": 2,
        "profiles": 1030,
        "aliases": 65888,
        "states": len(states),
        "partitions": 2,
        "fine_transition_atoms": fine_atoms,
        "summary_transition_atoms": pushed_atoms,
        "transition_coefficient_cells": 16 * (fine_atoms + pushed_atoms),
        "mean_feature_cells": 64 * len(states),
        "pair_feature_cells": 256 * len(states),
        "motif_support_occurrences": sum(s["motif_count"] for s in states),
        "motif_positive_states": sum(s["motif_count"] > 0 for s in states),
        "max_motif_count": max(s["motif_count"] for s in states),
        "expected_update_coefficient_cells": 5120 * len(states),
        "motif_expected_update_coefficient_cells": 16 * len(states),
        "closed_partitions": len(closed),
        "quotient_transition_atoms": sum(
            len(row["transitions"]) for c in closed for row in c["quotient_rows"]
        ),
        "semigroup_intermediate_paths": sum(
            c["semigroup"]["totals"]["intermediate_paths"] for c in closed
        ),
        "semigroup_coefficient_cells": sum(
            c["semigroup"]["totals"]["coefficient_cells"] for c in closed
        ),
    }
    require_same_wire(a["counts"], counts, "exact counters")
    return {
        "verified": True,
        "rates": [[str(x), str(y)] for x, y in AUDIT_POINTS],
        "rate_points": len(AUDIT_POINTS),
        "evaluated_fine_atoms": fine_evaluations,
        "evaluated_summary_atoms": pushed_evaluations,
        "deterministic_corner_rows": corners,
        "expected_update_coefficient_cells": 5120 * len(states),
        "motif_expected_update_coefficient_cells": 16 * len(states),
        "semigroup_coefficient_cells": counts["semigroup_coefficient_cells"],
    }


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


def prior_bridge(a):
    require_wire(a)
    old = prior_json(M_PRIOR)["suite"]["analysis"]
    n = len(old["states"])
    require(n == 257, "pinned M domain")
    require_same_wire(a["frames"], old["frames"], "old frames")
    require_same_wire(a["profiles"][:6], old["profiles"], "old profile maps")
    shared = (
        "state_id",
        "frame_id",
        "mask",
        "kept",
        "past",
        "color_sizes",
        "chain_counts",
        "mean_graded",
        "pair_graded",
        "transitions",
    )
    for sid in range(n):
        state, previous = a["states"][sid], old["states"][sid]
        require_same_wire(
            {k: state[k] for k in shared},
            {k: previous[k] for k in shared},
            "old retained state fields",
        )
        require_same_wire(
            [alias for alias in state["aliases"] if alias["profile_index"] < 6],
            previous["aliases"],
            "old filtered aliases",
        )
        require_same_wire(
            {
                "state_id": sid,
                "motif_count": state["motif_count"],
                "motif_supports": state["motif_supports"],
            },
            old["observable"]["states"][sid],
            "old observed motif",
        )
        require_same_wire(
            state["classes"],
            {
                "pair_graded": previous["classes"]["pair_graded"],
                "motif_pair": old["observable"]["state_classes"][sid],
            },
            "old class assignments",
        )
        require_same_wire(
            state["summary_laws"],
            {
                "pair_graded": previous["summary_laws"]["pair_graded"],
                "motif_pair": old["observable"]["pushforward_rows"][sid]["transitions"],
            },
            "old state pushed laws",
        )
        require(
            all(atom["target_state"] < n for atom in state["transitions"]),
            "old subset-closed prefix",
        )
    require_same_wire(
        a["expected_updates"]["rows"][:n], old["expected_updates"]["rows"], "old D/B updates"
    )
    require_same_wire(
        a["motif_expected_update"]["rows"][:n],
        old["observable"]["expected_update"]["rows"],
        "old motif updates",
    )
    restrictions = {}
    maps = {}
    for name in PARTITIONS:
        vector = [s["classes"][name] for s in a["states"][:n]]
        groups = groups_from_vector(vector)
        pulled = [
            {"class_id": g["class_id"], "members": [sid for sid in g["members"] if sid < n]}
            for g in a["partitions"][name]
            if any(sid < n for sid in g["members"])
        ]
        require_same_wire(groups, pulled, "actual pulled-back memberships")
        expected = (
            old["partitions"]["pair_graded"]
            if name == "pair_graded"
            else old["observable"]["classes"]
        )
        require_same_wire(
            groups,
            [{"class_id": g["class_id"], "members": g["members"]} for g in expected],
            "M fibers",
        )
        maps[name] = [{"expanded_class": g["class_id"], "old_class": g["class_id"]} for g in groups]
        restrictions[name] = groups
    restricted = closure_from_rows(a["states"][:n], restrictions["motif_pair"], "motif_pair")
    require(restricted["closed"], "old candidate remains closed")
    require_same_wire(
        restricted["quotient_rows"], old["observable"]["quotient_rows"], "old quotient coefficients"
    )
    require_same_wire(
        restricted["semigroup"], old["observable"]["semigroup"], "old quotient composition"
    )
    global_closed = a["closure"]["motif_pair"]["closed"]
    global_verified = None
    if global_closed:
        image = {item["expanded_class"] for item in maps["motif_pair"]}
        rows = [
            row for row in a["closure"]["motif_pair"]["quotient_rows"] if row["class_id"] in image
        ]
        require(
            all(atom["target_class"] in image for row in rows for atom in row["transitions"]),
            "old global quotient image closed",
        )
        require_same_wire(rows, restricted["quotient_rows"], "actual global quotient restriction")
        global_verified = True
    else:
        require_same_wire(
            a["closure"]["motif_pair"]["quotient_rows"],
            [],
            "failed global candidate has no quotient",
        )
        require(
            a["closure"]["motif_pair"]["semigroup"] is None,
            "failed global candidate has no semigroup",
        )
    return {
        "prior_artifact": M_PRIOR,
        "matched_states": n,
        "matched_original_aliases": 352,
        "new_states": len(a["states"]) - n,
        "added_aliases_on_old_states": sum(
            alias["profile_index"] >= 6 for s in a["states"][:n] for alias in s["aliases"]
        ),
        "subset_closed_prefix": True,
        "class_maps": maps,
        "pulled_back_partitions": restrictions,
        "old_state_polynomials_equal": True,
        "restricted_candidate_quotient": restricted,
        "global_candidate_closed": global_closed,
        "global_quotient_restriction_verified": global_verified,
        "whole_M_schema_reproduced": False,
    }


def count_law(a, sid):
    result = {}
    for atom in a["states"][sid]["transitions"]:
        key = tuple(a["states"][atom["target_state"]]["chain_counts"])
        add_table(result.setdefault(key, zero()), atom["coefficients"])
    return [{"chain_counts": list(key), "coefficients": result[key]} for key in sorted(result)]


def counterexample(a, name):
    failure = a["closure"][name]["first_collision"]
    if failure is None:
        return None
    left, right = (a["states"][failure[k]] for k in ("left_state", "right_state"))
    require(
        left["classes"][name] == right["classes"][name] == failure["class_id"],
        "counterexample same current class",
    )
    key = a["partitions"][name][failure["class_id"]]["key"]
    evaluations = []
    first_grid_difference = None
    for index, (x, y) in enumerate(AUDIT_POINTS):
        lhs = evaluate(failure["left_coefficients"], x, y)
        rhs = evaluate(failure["right_coefficients"], x, y)
        evaluations.append(
            {"rates": [str(x), str(y)], "left_probability": str(lhs), "right_probability": str(rhs)}
        )
        if index < 16 and lhs != rhs and first_grid_difference is None:
            first_grid_difference = index
    require(first_grid_difference is not None, "nonzero bounded polynomial distinguished on grid")
    laws = [count_law(a, s["state_id"]) for s in (left, right)]
    return {
        "partition": name,
        "witness": failure,
        "equal_current_key": key,
        "observations": [
            {
                k: s[k]
                for k in (
                    "state_id",
                    "frame_id",
                    "kept",
                    "past",
                    "chain_counts",
                    "motif_supports",
                    "motif_count",
                )
            }
            for s in (left, right)
        ],
        "first_aliases": [s["aliases"][0] for s in (left, right)],
        "evaluations": evaluations,
        "first_distinguishing_grid_index": first_grid_difference,
        "full_count_laws": laws,
        "full_count_laws_equal": canonical(laws[0]) == canonical(laws[1]),
    }


def controls(a):
    def state(pid, mask=63):
        return a["states"][a["profiles"][pid]["state_ids"][mask]]

    descending = []
    for pid in (14, 526):
        s = state(pid)
        require_same_wire(s["chain_counts"], [1, 6, 1, 0], "descending-edge chain count")
        require(s["motif_count"] == 0, "single-edge motif count")
        descending.append(
            {
                "profile_index": pid,
                "mask": 63,
                "state_id": s["state_id"],
                "chain_counts": s["chain_counts"],
                "past": s["past"],
            }
        )
    complete = []
    expected_b = zero()
    for i, j, v in ((1, 1, 9), (1, 2, 18), (2, 1, 18), (2, 2, 36)):
        expected_b[i][j] = v
    for pid in (517, 1029):
        s = state(pid)
        require_same_wire(s["chain_counts"], [1, 6, 9, 0], "complete incidence chain counts")
        require(s["motif_count"] == 9 and len(s["motif_supports"]) == 9, "nine overlapping motifs")
        require_same_wire(
            s["pair_graded"][2][2], expected_b, "complete incidence ordered edge pairs"
        )
        row = a["motif_expected_update"]["rows"][s["state_id"]]
        complete.append(
            {
                "profile_index": pid,
                "mask": 63,
                "state_id": s["state_id"],
                "chain_counts": s["chain_counts"],
                "motif_count": s["motif_count"],
                "motif_supports": s["motif_supports"],
                "pair_22": s["pair_graded"][2][2],
                "motif_expected_update": row,
            }
        )
    require_same_wire(
        a["profiles"][6]["state_ids"], a["profiles"][518]["state_ids"], "empty incidence aliases"
    )
    path, cycle = state(4), state(5)
    require_same_wire(path["pair_graded"], cycle["pair_graded"], "retained old equal-B adversary")
    require(
        path["motif_count"] == 0 and cycle["motif_count"] == 1, "retained old distinguishing motif"
    )
    selected = state(5, 45)
    target_class = selected["classes"]["pair_graded"]
    rows = []
    for s in (path, cycle):
        table = next(
            (
                atom["coefficients"]
                for atom in s["summary_laws"]["pair_graded"]
                if atom["target_class"] == target_class
            ),
            zero(),
        )
        rows.append(table)
    require_same_wire(
        rows, [zero(), [list(r) for r in kernel(3, 3, 2, 2)]], "old selected next-B witness"
    )
    fixed = []
    for pid in (0, 3):
        s = state(pid, 0)
        require(
            len(s["transitions"]) == 1 and s["transitions"][0]["target_state"] == s["state_id"],
            "fixed-only absorbing",
        )
        require(s["motif_count"] == 0, "fixed-only motif")
        fixed.append({"frame_id": s["frame_id"], "state_id": s["state_id"], "kept": s["kept"]})
    return {
        "descending_id_edges": descending,
        "complete_incidence": complete,
        "empty_incidence": {
            "profile_indices": [6, 518],
            "state_ids": a["profiles"][6]["state_ids"],
            "duplicates_are_aliases": True,
        },
        "old_adversary": {
            "path_state": path["state_id"],
            "cycle_state": cycle["state_id"],
            "target_state": selected["state_id"],
            "target_pair_class": target_class,
            "coefficients": rows,
            "half_probabilities": [str(evaluate(t, F(1, 2), F(1, 2))) for t in rows],
        },
        "fixed_only": fixed,
        "counterexamples": {name: counterexample(a, name) for name in PARTITIONS},
        "feature_redefined": False,
        "stable_repair_executed": False,
    }


def run_suite():
    direct = load("qr05n_capture_direct", "portability.py")
    reference = load("qr05n_capture_reference", "reference_qr05n.py")
    problem = fixtures()[0]
    a, b = direct.analyze(problem), reference.analyze(problem)
    require_same_wire(a, b, "independent complete N outputs differ")
    del b
    audit = check_analysis(a)
    bridge = prior_bridge(a)
    checks = controls(a)
    rejections = []
    for index, invalid in enumerate(invalid_fixtures()):
        rejected = []
        for name, module in (
            ("observed_pairs_binomial", direct),
            ("source_count_law_interpolation", reference),
        ):
            try:
                module.analyze(invalid)
            except (TypeError, ValueError):
                rejected.append(name)
            else:
                raise ValueError("malformed N problem accepted")
        rejections.append({"fixture_index": index, "input": invalid, "rejected_by": rejected})
    suite = {
        "input": problem,
        "analysis": a,
        "audit": audit,
        "prior_bridge": bridge,
        "controls": checks,
        "rejections": rejections,
        "research_base_commit": BASE_COMMIT,
        "claim": "Test unchanged (frame,B,M) closure on the prespecified append-only two-orientation layered family; retain failures without an automatic repair.",
        "candidate_closed": a["closure"]["motif_pair"]["closed"],
        "candidate_failure_is_valid_investigative_outcome": True,
        "parameter_domain": "[0,1]^2 per fresh independent stage",
        "bounds": {
            "states_max": 2579,
            "fine_atoms_max": 100393,
            "eligible_max": 6,
            "colors_max": [3, 3],
            "chain_order_max": 3,
            "transition_degree": [3, 3],
            "composition_degree": [3, 3, 3, 3],
            "motif_max": 9,
            "exact_component_bits": 4096,
            "artifact_bytes_max": MAX_CAPTURE_BYTES,
        },
        "old_domain_restriction_preserved": True,
        "source_labels_in_summary_keys": False,
        "aliases_used_as_weights": False,
        "selected_rate_zeros_discarded": False,
        "numeric_labels_assumed_topological": False,
        "expected_updates_imply_full_law": False,
        "feature_redefined_after_failure": False,
        "stable_refinement_executed": False,
        "expanded_trace_audit_executed": False,
        "unseen_domain_closure_claimed": False,
        "minimum_storage_or_runtime_claimed": False,
        "adaptive_rate_composition_tested": False,
        "correlated_stage_composition_claimed": False,
        "observation_composition_is_physical_time": False,
        "empirical_data_used": False,
        "empirical_noise_calibration_tested": False,
        "ret_integration_tested": False,
        "quantum_channel_constructed": False,
        "event_growth_constructed": False,
        "gravity_derived": False,
        "continuum_limit_established": False,
        "lean_proof_completed": False,
    }
    bits = retained_bits(suite)
    require(bits <= 4096, "exact component cap")
    suite["totals"] = {
        **a["counts"],
        "class_counts": {name: len(a["partitions"][name]) for name in PARTITIONS},
        "closed_partition_names": [name for name in PARTITIONS if a["closure"][name]["closed"]],
        "audit_rate_points": len(AUDIT_POINTS),
        "prior_states": bridge["matched_states"],
        "prior_aliases": bridge["matched_original_aliases"],
        "new_states": bridge["new_states"],
        "added_aliases_on_old_states": bridge["added_aliases_on_old_states"],
        "restricted_prior_semigroup_coefficient_cells": bridge["restricted_candidate_quotient"][
            "semigroup"
        ]["totals"]["coefficient_cells"],
        "rejected_fixtures": len(rejections),
        "max_retained_component_bits": bits,
    }
    require_wire(suite)
    return suite


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


if __name__ == "__main__":
    main()
