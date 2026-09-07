"""QR-05L exact finite sampling capture and read-only replay."""

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
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05l-results-v1"
BASE_COMMIT = "2f232c8f795df3eaa5e73ed3c3125e231abdd80e"
SOURCES = (
    "README.md",
    "refinement.py",
    "reference_qr05l.py",
    "study.py",
    "test_qr05l.py",
    "test_capture.py",
)
PRIORS = {
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


PARTITIONS = ("mean_graded", "pair_graded", "color_order", "full_record")
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
        list(product(GRID, repeat=2))
        + [
            (F(1, 2), F(1, 2)),
            (F(2, 5), F(3, 7)),
            (F(1, 5), F(4, 5)),
            (F(1, 2), F(1, 3)),
            (F(0), F(2, 5)),
            (F(3, 7), F(1)),
        ]
    )
)
STAGE_PAIRS = (
    ((F(1, 2), F(1, 2)), (F(1, 2), F(1, 2))),
    ((F(1, 3), F(2, 3)), (F(2, 5), F(3, 7))),
    ((F(0), F(1, 2)), (F(2, 3), F(1))),
    ((F(1), F(1)), (F(1, 3), F(2, 3))),
)


def fixtures():
    return [{"schema_version": "det8-qr05l-problem-v1", "family": "qr05l_adversarial_iid"}]


def invalid_fixtures():
    good = fixtures()[0]
    return [
        None,
        [],
        True,
        {},
        {k: v for k, v in good.items() if k == "schema_version"},
        {"family": good["family"]},
        {**good, "extra": 1},
        *({**good, "family": v} for v in (None, True, 1, [], "wrong")),
        *({**good, "schema_version": v} for v in (None, True, 1, [], "wrong")),
        {**good, "profile": "ferrers6"},
        {**good, "design": "independent"},
    ]


def frame_value(frame):
    return [frame["density"], frame["fixed"], frame["eligible"]]


def state_key(a, state):
    return [frame_value(a["frames"][state["frame_id"]]), state["kept"], state["past"]]


def partition_key(a, state, name):
    frame = frame_value(a["frames"][state["frame_id"]])
    return (
        [frame, state["mean_graded"]]
        if name == "mean_graded"
        else (
            [frame, state["pair_graded"]]
            if name == "pair_graded"
            else [frame, state["color_order"]]
            if name == "color_order"
            else state_key(a, state)
        )
    )


def check_tensor(value, shape, nonnegative=False):
    if not shape:
        require(type(value) is int and (not nonnegative or value >= 0), "coefficient type/sign")
        return
    require(type(value) is list and len(value) == shape[0], "tensor shape")
    for item in value:
        check_tensor(item, shape[1:], nonnegative)


def induced_past(parent, kept):
    positions = {v: i for i, v in enumerate(kept)}
    old = {v: i for i, v in enumerate(parent["kept"])}
    return [
        [
            positions[parent["kept"][i]]
            for i in parent["past"][old[v]]
            if parent["kept"][i] in positions
        ]
        for v in kept
    ]


@memoize
def _evaluate(table, x, y):
    return sum(
        (c * x**i * y**j for i, row in enumerate(table) for j, c in enumerate(row) if c), F(0)
    )


def evaluate(table, x, y):
    return _evaluate(tuple(tuple(row) for row in table), x, y)


def zero():
    return [[0] * 4 for _ in range(4)]


def law_map(rows, target):
    return {r[target]: r["coefficients"] for r in rows}


def evaluated_row(rows, target, x, y):
    result = {}
    for atom in rows:
        p = evaluate(atom["coefficients"], x, y)
        require(p >= 0, "evaluated transition probability")
        if p:
            result[atom[target]] = p
    require(sum(result.values(), F(0)) == 1, "evaluated row normalization")
    return result


def probability(frame, state, target, x, y):
    p = F(1)
    for bit, v in enumerate(frame["eligible"]):
        if state["mask"] & (1 << bit):
            rate = x if v % 2 else y
            p *= rate if target["mask"] & (1 << bit) else 1 - rate
    return p


def first_collision(states, name):
    representatives = {}
    for state in states:
        cid = state["classes"][name]
        if cid not in representatives:
            representatives[cid] = state
            continue
        left = representatives[cid]
        a = law_map(left["summary_laws"][name], "target_class")
        b = law_map(state["summary_laws"][name], "target_class")
        for target in sorted(a.keys() | b.keys()):
            l, r = a.get(target, zero()), b.get(target, zero())
            if canonical(l) != canonical(r):
                return {
                    "class_id": cid,
                    "left_state": left["state_id"],
                    "right_state": state["state_id"],
                    "target_class": target,
                    "left_coefficients": l,
                    "right_coefficients": r,
                }
    return None


def refines(states, left, right):
    seen = {}
    for state in states:
        a, b = state["classes"][left], state["classes"][right]
        if a in seen and seen[a] != b:
            return False
        seen[a] = b
    return True


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
            "partition_refinement",
            "closure",
            "expected_updates",
            "counts",
            "stabilization",
        },
        "analysis fields",
    )
    frames, profiles, states = a["frames"], a["profiles"], a["states"]
    require(len(frames) == 2 and len(profiles) == 6 and len(states) == 257, "domain sizes")
    for fid, frame in enumerate(frames):
        fixed = [0, 7] if fid == 0 else [0, 3, 7]
        require_same_wire(
            frame,
            {
                "frame_id": fid,
                "density": "12",
                "fixed": fixed,
                "eligible": [v for v in range(1, 7) if v not in fixed],
            },
            "frame",
        )
    lookup = {canonical(state_key(a, s)): s["state_id"] for s in states}
    require(len(lookup) == len(states), "state deduplication")
    aliases = [[] for _ in states]
    first_seen_states = set()
    for pid, profile in enumerate(profiles):
        require(
            set(profile) == {"profile_index", "name", "frame_id", "past", "state_ids"},
            "profile fields",
        )
        for field in ("profile_index", "frame_id"):
            check_tensor(profile[field], [], True)
        require(type(profile["past"]) is list and len(profile["past"]) == 8, "source past shape")
        for row in profile["past"]:
            require(type(row) is list, "source past row")
            check_tensor(row, [len(row)], True)
        require(
            profile["profile_index"] == pid
            and profile["name"] == PROFILE_NAMES[pid]
            and profile["frame_id"] == (1 if pid == 3 else 0),
            "profile identity",
        )
        frame = frames[profile["frame_id"]]
        if pid >= 4:
            edges = (
                {(1, 2), (1, 4), (3, 4), (3, 6), (5, 6)}
                if pid == 4
                else {(1, 4), (1, 6), (3, 4), (3, 6), (2, 5)}
            )
            expected_past = [
                [i for i in range(j) if i == 0 or j == 7 or (i, j) in edges] for j in range(8)
            ]
            require_same_wire(profile["past"], expected_past, "adversarial source relation")
        require(len(profile["state_ids"]) == 2 ** len(frame["eligible"]), "profile mask coverage")
        parent = {"kept": list(range(8)), "past": profile["past"]}
        for mask, sid in enumerate(profile["state_ids"]):
            require(type(sid) is int and 0 <= sid < len(states), "profile state id")
            if sid not in first_seen_states:
                require(sid == len(first_seen_states), "first-occurrence state registration")
                first_seen_states.add(sid)
            state = states[sid]
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(frame["eligible"]) if mask & (1 << bit)]
            )
            require(
                state["frame_id"] == profile["frame_id"]
                and state["mask"] == mask
                and state["kept"] == kept
                and state["past"] == induced_past(parent, kept),
                "alias induction",
            )
            aliases[sid].append({"profile_index": pid, "mask": mask})
    for sid, state in enumerate(states):
        require(
            set(state)
            == {
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
                "color_order",
                "classes",
                "transitions",
                "summary_laws",
            },
            "state fields",
        )
        for field in ("state_id", "frame_id", "mask"):
            check_tensor(state[field], [], True)
        check_tensor(state["kept"], [len(state["kept"])], True)
        require(
            type(state["past"]) is list and len(state["past"]) == len(state["kept"]),
            "observed past shape",
        )
        for row in state["past"]:
            require(type(row) is list, "observed past row")
            check_tensor(row, [len(row)], True)
        check_tensor(state["chain_counts"], [4], True)
        check_tensor(state["color_sizes"], [2], True)
        check_tensor(state["color_order"], [3], True)
        require(state["state_id"] == sid and aliases[sid], "state identity/aliases")
        require_same_wire(state["aliases"], aliases[sid], "state aliases native identity")
        frame = frames[state["frame_id"]]
        observed = [v for v in state["kept"] if v in frame["eligible"]]
        require(
            state["color_sizes"]
            == [sum(v % 2 for v in observed), sum(1 - v % 2 for v in observed)],
            "color sizes",
        )
        check_tensor(state["mean_graded"], [4, 4, 4], True)
        check_tensor(state["pair_graded"], [4, 4, 4, 4], True)
        require(state["pair_graded"][0] == state["mean_graded"], "D embedded in B")
        require(
            state["chain_counts"] == [sum(map(sum, table)) for table in state["mean_graded"]],
            "chain totals",
        )
        require(state["chain_counts"][0] == 1, "fixed probe zero-chain")
        require(
            set(state["classes"]) == set(PARTITIONS)
            and set(state["summary_laws"]) == set(PARTITIONS),
            "partition names",
        )
    require(
        set(a["partitions"]) == set(PARTITIONS) and set(a["closure"]) == set(PARTITIONS),
        "partition maps",
    )
    for name in PARTITIONS:
        groups = []
        ids = {}
        for state in states:
            key = partition_key(a, state, name)
            encoded = canonical(key)
            if encoded not in ids:
                ids[encoded] = len(groups)
                groups.append({"class_id": len(groups), "key": key, "members": []})
            cid = ids[encoded]
            groups[cid]["members"].append(state["state_id"])
            require(
                type(state["classes"][name]) is int and state["classes"][name] == cid,
                "class assignment",
            )
        require_same_wire(a["partitions"][name], groups, "first-occurrence partition")
    require_same_wire(
        a["partition_refinement"],
        [[refines(states, l, r) for r in PARTITIONS] for l in PARTITIONS],
        "refinement",
    )
    fine_atoms = 0
    pushed_atoms = 0
    evaluated_atoms = 0
    corner_rows = 0
    for state in states:
        frame = frames[state["frame_id"]]
        eligible = [v for v in frame["eligible"] if v in state["kept"]]
        expected_targets = []
        for mask in range(1 << len(eligible)):
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(eligible) if mask & (1 << bit)]
            )
            key = canonical([frame_value(frame), kept, induced_past(state, kept)])
            require(key in lookup, "subset-closed state domain")
            expected_targets.append(lookup[key])
        rows = state["transitions"]
        require(
            [r["target_state"] for r in rows] == sorted(expected_targets),
            "fine structural atom coverage",
        )
        fine_atoms += len(rows)
        normalization = zero()
        for atom in rows:
            require(set(atom) == {"target_state", "coefficients"}, "fine atom fields")
            check_tensor(atom["target_state"], [], True)
            table = atom["coefficients"]
            check_tensor(table, [4, 4])
            require(any(c for row in table for c in row), "structural atom nonzero")
            for i, j in product(range(4), repeat=2):
                require(
                    not table[i][j]
                    or (i <= state["color_sizes"][0] and j <= state["color_sizes"][1]),
                    "degree bound",
                )
                normalization[i][j] += table[i][j]
        unit = zero()
        unit[0][0] = 1
        require(normalization == unit, "coefficient row normalization")
        for x, y in AUDIT_POINTS:
            masses = evaluated_row(rows, "target_state", x, y)
            for atom in rows:
                target = states[atom["target_state"]]
                require(
                    evaluate(atom["coefficients"], x, y) == probability(frame, state, target, x, y),
                    "direct thinning evaluation",
                )
                evaluated_atoms += 1
            if x in (0, 1) and y in (0, 1):
                require(len(masses) == 1, "deterministic corner")
                corner_rows += 1
            if (x, y) == (F(1), F(1)):
                require(masses == {state["state_id"]: F(1)}, "identity endpoint")
            if (x, y) == (F(0), F(0)):
                require(all(states[t]["mask"] == 0 for t in masses), "fixed-only endpoint")
        for name in PARTITIONS:
            accumulated = {}
            for atom in rows:
                target = states[atom["target_state"]]["classes"][name]
                table = accumulated.setdefault(target, zero())
                for i, j in product(range(4), repeat=2):
                    table[i][j] += atom["coefficients"][i][j]
            expected = [
                {"target_class": t, "coefficients": accumulated[t]} for t in sorted(accumulated)
            ]
            require_same_wire(state["summary_laws"][name], expected, "coefficient pushforward")
            pushed_atoms += len(expected)
            for x, y in AUDIT_POINTS:
                masses = evaluated_row(expected, "target_class", x, y)
                direct = {}
                for atom in rows:
                    target = states[atom["target_state"]]
                    cid = target["classes"][name]
                    p = probability(frame, state, target, x, y)
                    if p:
                        direct[cid] = direct.get(cid, F(0)) + p
                require(masses == direct, "evaluated pushed row")
                evaluated_atoms += len(expected)

    # Weight every successor feature by every fine coefficient; padding zeros count.
    def feature_values(state):
        return [v for q in state["mean_graded"] for row in q for v in row] + [
            v for q in state["pair_graded"] for r in q for row in r for v in row
        ]

    features = [feature_values(s) for s in states]
    feature_rows = []
    for state in states:
        weighted = [[0] * 16 for _ in range(320)]
        for atom in state["transitions"]:
            coefficients = [
                (4 * i + j, c)
                for i, row in enumerate(atom["coefficients"])
                for j, c in enumerate(row)
                if c
            ]
            for feature, value in enumerate(features[atom["target_state"]]):
                if value:
                    for cell, coefficient in coefficients:
                        weighted[feature][cell] += coefficient * value
        for feature, value in enumerate(features[state["state_id"]]):
            expected = [0] * 16
            expected[feature % 16] = value
            require(weighted[feature] == expected, "diagonal expected feature update")
        feature_rows.append(
            {
                "state_id": state["state_id"],
                "mean_features": 64,
                "pair_features": 256,
                "coefficient_cells": 5120,
                "max_abs_residual": 0,
            }
        )
    require_same_wire(
        a["expected_updates"],
        {"verified": True, "rows": feature_rows, "coefficient_cells": len(states) * 5120},
        "expected update certificate",
    )
    closed = []
    quotient_atoms = 0
    paths = 0
    composition_cells = 0
    quotient_evaluations = 0
    for name in PARTITIONS:
        collision = first_collision(states, name)
        actual = a["closure"][name]
        require(
            set(actual) == {"closed", "first_collision", "quotient_rows", "semigroup"},
            "closure fields",
        )
        if collision is not None:
            require_same_wire(
                actual,
                {
                    "closed": False,
                    "first_collision": collision,
                    "quotient_rows": None,
                    "semigroup": None,
                },
                "failed partition has no quotient",
            )
            continue
        closed.append(name)
        rows = [
            {
                "class_id": group["class_id"],
                "representative_state": group["members"][0],
                "transitions": states[group["members"][0]]["summary_laws"][name],
            }
            for group in a["partitions"][name]
        ]
        semigroup = check_semigroup(rows)
        require_same_wire(
            actual,
            {
                "closed": True,
                "first_collision": None,
                "quotient_rows": rows,
                "semigroup": semigroup,
            },
            "quotient/composition",
        )
        quotient_atoms += sum(len(row["transitions"]) for row in rows)
        paths += semigroup["totals"]["intermediate_paths"]
        composition_cells += semigroup["totals"]["coefficient_cells"]
        for row in rows:
            for x, y in AUDIT_POINTS:
                evaluated_row(row["transitions"], "target_class", x, y)
                quotient_evaluations += len(row["transitions"])
    counts = {
        "frames": len(frames),
        "profiles": len(profiles),
        "aliases": sum(map(len, aliases)),
        "states": len(states),
        "partitions": len(PARTITIONS),
        "fine_transition_atoms": fine_atoms,
        "summary_transition_atoms": pushed_atoms,
        "transition_coefficient_cells": 16 * (fine_atoms + pushed_atoms),
        "mean_feature_cells": len(states) * 64,
        "pair_feature_cells": len(states) * 256,
        "expected_update_coefficient_cells": len(states) * 5120,
        "closed_partitions": len(closed),
        "quotient_transition_atoms": quotient_atoms,
        "semigroup_intermediate_paths": paths,
        "semigroup_coefficient_cells": composition_cells,
    }
    require_same_wire(a["counts"], counts, "exact work inventory")
    return {
        "verified": True,
        "rates": [[str(x), str(y)] for x, y in AUDIT_POINTS],
        "rate_points": len(AUDIT_POINTS),
        "evaluated_fine_and_pushed_atoms": evaluated_atoms,
        "evaluated_quotient_atoms": quotient_evaluations,
        "deterministic_corner_rows": corner_rows,
        "expected_feature_coefficient_cells": len(states) * 5120,
        "semigroup_coefficient_cells": composition_cells,
    }


def groups_from_vector(vector):
    groups = []
    for sid, cid in enumerate(vector):
        require(type(cid) is int and 0 <= cid <= len(groups), "native canonical class vector")
        if cid == len(groups):
            groups.append({"class_id": cid, "members": []})
        groups[cid]["members"].append(sid)
    return groups


def vector_refines(left, right):
    seen = {}
    for a, b in zip(left, right, strict=True):
        if a in seen and seen[a] != b:
            return False
        seen[a] = b
    return True


def push_to_vector(states, vector):
    rows = []
    for state in states:
        tables = {}
        for atom in state["transitions"]:
            target = vector[atom["target_state"]]
            table = tables.setdefault(target, zero())
            for i, j in product(range(4), repeat=2):
                table[i][j] += atom["coefficients"][i][j]
        rows.append(
            {
                "state_id": state["state_id"],
                "transitions": [
                    {"target_class": target, "coefficients": tables[target]}
                    for target in sorted(tables)
                ],
            }
        )
    return rows


def next_vector(vector, rows):
    identities = {}
    new = []
    for sid, cid in enumerate(vector):
        key = canonical([cid, rows[sid]["transitions"]])
        if key not in identities:
            identities[key] = len(identities)
        new.append(identities[key])
    return new


def split_witnesses(vector, groups, rows, new):
    answer = []
    maps = [law_map(row["transitions"], "target_class") for row in rows]
    for child in groups_from_vector(new):
        right = child["members"][0]
        parent = vector[right]
        left = groups[parent]["members"][0]
        if new[left] == child["class_id"]:
            continue
        a, b = maps[left], maps[right]
        target = next(
            t for t in sorted(a.keys() | b.keys()) if a.get(t, zero()) != b.get(t, zero())
        )
        answer.append(
            {
                "parent_class_id": parent,
                "child_class_id": child["class_id"],
                "left_state": left,
                "right_state": right,
                "target_class": target,
                "left_coefficients": a.get(target, zero()),
                "right_coefficients": b.get(target, zero()),
            }
        )
    return answer


def check_stabilization(a):
    require_wire(a)
    require(retained_bits(a) <= 4096, "exact component cap")
    s = a["stabilization"]
    states = a["states"]
    n = len(states)
    require(
        set(s)
        == {
            "initial_partition",
            "rounds",
            "strict_rounds",
            "final_round",
            "state_classes",
            "classes",
            "quotient_rows",
            "semigroup",
            "comparison",
            "counts",
        },
        "stabilization fields",
    )
    require(s["initial_partition"] == "pair_graded", "initial refinement partition")
    vector = [state["classes"]["pair_graded"] for state in states]
    require(
        type(s["rounds"]) is list and 1 <= len(s["rounds"]) <= n - len(set(vector)) + 1,
        "finite refinement bound",
    )
    atoms = separations = 0
    known_refiner_checks = 0
    for ri, actual in enumerate(s["rounds"]):
        groups = groups_from_vector(vector)
        rows = push_to_vector(states, vector)
        new = next_vector(vector, rows)
        stable = new == vector
        witnesses = split_witnesses(vector, groups, rows, new)
        require_same_wire(
            actual,
            {
                "round_index": ri,
                "state_classes": vector,
                "classes": groups,
                "pushforward_rows": rows,
                "stable": stable,
                "separations": witnesses,
            },
            "exact refinement round",
        )
        require(vector_refines(new, vector), "refinement must not merge prior distinctions")
        require(
            stable == (ri == len(s["rounds"]) - 1),
            "refinement cannot stop early or append stable rounds",
        )
        if not stable:
            require(len(set(new)) > len(groups), "strict round must split")
        for name in PARTITIONS:
            other = [state["classes"][name] for state in states]
            if a["closure"][name]["closed"] and vector_refines(
                other, [t["classes"]["pair_graded"] for t in states]
            ):
                require(vector_refines(other, vector), "known closed B-refiner cannot be split")
                known_refiner_checks += 1
        atoms += sum(len(row["transitions"]) for row in rows)
        separations += len(witnesses)
        if not stable:
            vector = new
    classes = groups_from_vector(vector)
    quotient = []
    for group in classes:
        rep = group["members"][0]
        law = rows[rep]["transitions"]
        for sid in group["members"]:
            require_same_wire(rows[sid]["transitions"], law, "terminal class row constancy")
        quotient.append(
            {"class_id": group["class_id"], "representative_state": rep, "transitions": law}
        )
    semigroup = check_semigroup(quotient)
    names = ["mean_graded", "pair_graded", "stable_pair", "color_order", "full_record"]
    vectors = {name: [state["classes"][name] for state in states] for name in PARTITIONS}
    vectors["stable_pair"] = vector
    comparison = {
        "names": names,
        "refinement": [[vector_refines(vectors[l], vectors[r]) for r in names] for l in names],
    }
    counts = {
        "rounds": len(s["rounds"]),
        "strict_rounds": len(s["rounds"]) - 1,
        "classes": len(classes),
        "round_transition_atoms": atoms,
        "round_coefficient_cells": 16 * atoms,
        "separation_witnesses": separations,
        "quotient_transition_atoms": sum(len(row["transitions"]) for row in quotient),
        "semigroup_intermediate_paths": semigroup["totals"]["intermediate_paths"],
        "semigroup_coefficient_cells": semigroup["totals"]["coefficient_cells"],
    }
    for key, value in {
        "strict_rounds": len(s["rounds"]) - 1,
        "final_round": len(s["rounds"]) - 1,
        "state_classes": vector,
        "classes": classes,
        "quotient_rows": quotient,
        "semigroup": semigroup,
        "comparison": comparison,
        "counts": counts,
    }.items():
        require_same_wire(s[key], value, "terminal refinement " + key)
    evaluated = 0
    for row in quotient:
        for x, y in AUDIT_POINTS:
            evaluated_row(row["transitions"], "target_class", x, y)
            evaluated += len(row["transitions"])
    return {
        "verified": True,
        "rounds": len(s["rounds"]),
        "strict_rounds": len(s["rounds"]) - 1,
        "checked_round_atoms": atoms,
        "round_coefficient_cells": 16 * atoms,
        "known_closed_refiner_round_checks": known_refiner_checks,
        "evaluated_quotient_atoms": evaluated,
        "semigroup_coefficient_cells": semigroup["totals"]["coefficient_cells"],
        "coarsest_argument_premises_verified": True,
    }


def prior_bridge(a):
    old_suite = prior_json("qr-05k-recursive-closure-2026-09-06/results.json")["suite"]
    old = old_suite["analysis"]
    size = len(old["states"])
    require(size == 188, "prior state domain")
    require_same_wire(a["frames"], old["frames"], "K frames")
    require_same_wire(a["profiles"][:4], old["profiles"], "K source profile maps")
    prefix = []
    extra_aliases = 0
    for before, state in zip(old["states"], a["states"][:size], strict=True):
        aliases = [alias for alias in state["aliases"] if alias["profile_index"] < 4]
        extra_aliases += len(state["aliases"]) - len(aliases)
        restricted = {**state, "aliases": aliases}
        require_same_wire(restricted, before, "complete K observed state restriction")
        require(
            all(atom["target_state"] < size for atom in state["transitions"]),
            "K fine kernel must not leave prefix",
        )
        prefix.append(restricted)
    for name in PARTITIONS:
        pulled = []
        for group in a["partitions"][name]:
            members = [sid for sid in group["members"] if sid < size]
            if members:
                pulled.append({**group, "members": members})
        require_same_wire(pulled, old["partitions"][name], "K basic partition pullback")
        collision = first_collision(prefix, name)
        quotient = semigroup = None
        if collision is None:
            quotient = [
                {
                    "class_id": group["class_id"],
                    "representative_state": group["members"][0],
                    "transitions": prefix[group["members"][0]]["summary_laws"][name],
                }
                for group in pulled
            ]
            semigroup = check_semigroup(quotient)
        require_same_wire(
            {
                "closed": collision is None,
                "first_collision": collision,
                "quotient_rows": quotient,
                "semigroup": semigroup,
            },
            old["closure"][name],
            "K basic closure certificate",
        )
    require_same_wire(
        a["expected_updates"]["rows"][:size],
        old["expected_updates"]["rows"],
        "K expected-update rows",
    )
    stable = a["stabilization"]
    vector = stable["state_classes"]
    mapping = {}
    for group in old["partitions"]["pair_graded"]:
        new_id = vector[group["members"][0]]
        members = [sid for sid in stable["classes"][new_id]["members"] if sid < size]
        require_same_wire(members, group["members"], "K stable class membership restriction")
        mapping[group["class_id"]] = new_id
    require(len(set(mapping.values())) == len(mapping), "injective K class image")
    reverse = {new: before for before, new in mapping.items()}
    quotient = []
    for before, new in mapping.items():
        row = stable["quotient_rows"][new]
        require(
            all(atom["target_class"] in reverse for atom in row["transitions"]),
            "K quotient must not leave class image",
        )
        quotient.append(
            {
                "class_id": before,
                "representative_state": row["representative_state"],
                "transitions": sorted(
                    [
                        {
                            "target_class": reverse[atom["target_class"]],
                            "coefficients": atom["coefficients"],
                        }
                        for atom in row["transitions"]
                    ],
                    key=lambda atom: atom["target_class"],
                ),
            }
        )
    require_same_wire(
        quotient,
        old["closure"]["pair_graded"]["quotient_rows"],
        "K pair quotient polynomial restriction",
    )
    require_same_wire(
        check_semigroup(quotient),
        old["closure"]["pair_graded"]["semigroup"],
        "K pair quotient composition restriction",
    )
    return {
        "verified": True,
        "source_gate": "QR-05K",
        "matched_states": size,
        "matched_original_aliases": 224,
        "additional_aliases_on_old_states": extra_aliases,
        "matched_profiles": 4,
        "basic_partition_memberships_matched": 4,
        "stable_restriction": {
            "class_map": [
                {"old_pair_class": old_id, "stable_class": new_id}
                for old_id, new_id in mapping.items()
            ],
            "classes": len(mapping),
            "memberships_verified": True,
            "quotient_polynomials_verified": True,
            "semigroup_verified": True,
            "fine_rows_leave_old_states": False,
            "quotient_rows_leave_class_image": False,
        },
        "old_mass_filters_used": False,
        "earlier_bridge_retained": old_suite["prior_bridge"],
    }


def check_traces(a):
    states = a["states"]
    s = a["stabilization"]
    vector = s["state_classes"]
    projection = [states[group["members"][0]]["classes"]["pair_graded"] for group in s["classes"]]
    fine_cache = {}
    coarse_cache = {}
    trace_cache = {}

    def fine(sid, rates):
        key = (sid, *rates)
        if key not in fine_cache:
            fine_cache[key] = [
                (atom["target_state"], evaluate(atom["coefficients"], *rates))
                for atom in states[sid]["transitions"]
            ]
        return fine_cache[key]

    def coarse(cid, rates):
        key = (cid, *rates)
        if key not in coarse_cache:
            coarse_cache[key] = [
                (atom["target_class"], evaluate(atom["coefficients"], *rates))
                for atom in s["quotient_rows"][cid]["transitions"]
            ]
        return coarse_cache[key]

    def projected(cid, pair_index):
        key = (cid, pair_index)
        if key not in trace_cache:
            first, second = STAGE_PAIRS[pair_index]
            trace = {}
            for middle, p in coarse(cid, first):
                for target, q in coarse(middle, second):
                    pair = (projection[middle], projection[target])
                    trace[pair] = trace.get(pair, F(0)) + p * q
            trace_cache[key] = trace
        return trace_cache[key]

    rows = []
    for state in states:
        for pi, (first, second) in enumerate(STAGE_PAIRS):
            trace = {}
            for middle, p in fine(state["state_id"], first):
                for target, q in fine(middle, second):
                    pair = (
                        states[middle]["classes"]["pair_graded"],
                        states[target]["classes"]["pair_graded"],
                    )
                    trace[pair] = trace.get(pair, F(0)) + p * q
            coarse_trace = projected(vector[state["state_id"]], pi)
            require(trace.keys() == coarse_trace.keys(), "two-step B trace structural support")
            require(trace == coarse_trace, "fine/projected quotient joint B trace")
            require(
                all(p >= 0 for p in trace.values()) and sum(trace.values(), F(0)) == 1,
                "joint trace probability",
            )
            rows.append(
                {
                    "state_id": state["state_id"],
                    "rate_pair_index": pi,
                    "atoms": [
                        {
                            "first_pair_class": first_id,
                            "last_pair_class": last_id,
                            "probability": str(trace[first_id, last_id]),
                        }
                        for first_id, last_id in sorted(trace)
                    ],
                    "probability_sum": "1",
                    "max_abs_residual": "0",
                }
            )
    return {
        "stage_rate_pairs": [[[str(v) for v in rate] for rate in pair] for pair in STAGE_PAIRS],
        "rows": rows,
        "checked_rows": len(rows),
        "structural_trace_atoms": sum(len(row["atoms"]) for row in rows),
        "verified": True,
    }


def count_law(a, sid):
    tables = {}
    for atom in a["states"][sid]["transitions"]:
        counts = tuple(a["states"][atom["target_state"]]["chain_counts"])
        table = tables.setdefault(counts, zero())
        for i, j in product(range(4), repeat=2):
            table[i][j] += atom["coefficients"][i][j]
    return [{"counts": list(counts), "coefficients": tables[counts]} for counts in sorted(tables)]


def controls(a):
    states = a["states"]
    stable = a["stabilization"]
    path = states[a["profiles"][4]["state_ids"][63]]
    cycle = states[a["profiles"][5]["state_ids"][63]]
    target_state = states[a["profiles"][5]["state_ids"][45]]
    target = target_state["classes"]["pair_graded"]
    require_same_wire(path["mean_graded"], cycle["mean_graded"], "adversary equal D")
    require_same_wire(path["pair_graded"], cycle["pair_graded"], "adversary equal B")
    require(path["chain_counts"] == cycle["chain_counts"] == [1, 6, 5, 0], "adversary full counts")
    require(target_state["chain_counts"] == [1, 4, 4, 0], "four-cycle count atom")
    r22 = zero()
    r22[1][1] = 5
    r22[2][1] = 4
    r22[1][2] = 4
    r22[2][2] = 12
    require(path["pair_graded"][2][2] == r22, "adversary shared R22")
    left = law_map(path["summary_laws"]["pair_graded"], "target_class").get(target, zero())
    right = law_map(cycle["summary_laws"]["pair_graded"], "target_class").get(target, zero())
    polynomial = zero()
    polynomial[2][2] = 1
    polynomial[3][2] = -1
    polynomial[2][3] = -1
    polynomial[3][3] = 1
    require(left == zero() and right == polynomial, "selected next B cycle witness")
    path_law = count_law(a, path["state_id"])
    cycle_law = count_law(a, cycle["state_id"])

    def atom_at(law):
        return next((row["coefficients"] for row in law if row["counts"] == [1, 4, 4, 0]), zero())

    require(
        atom_at(path_law) == left and atom_at(cycle_law) == right, "realized full count-law failure"
    )
    evaluations = []
    for x, y, expected in ((F(1, 2), F(1, 2), F(1, 64)), (F(1, 3), F(2, 3), F(8, 729))):
        probabilities = [str(evaluate(table, x, y)) for table in (left, right)]
        require(probabilities == ["0", str(expected)], "adversary selected rate witness")
        evaluations.append(
            {
                "rates": [str(x), str(y)],
                "path_probability": probabilities[0],
                "cycle_probability": probabilities[1],
            }
        )
    left_class = stable["state_classes"][path["state_id"]]
    right_class = stable["state_classes"][cycle["state_id"]]
    require(left_class != right_class, "refinement must distinguish adversary")
    require(
        not a["closure"]["pair_graded"]["closed"] and not a["closure"]["mean_graded"]["closed"],
        "negative basic closure controls",
    )
    require(
        all(a["closure"][name]["closed"] for name in ("color_order", "full_record")),
        "positive basic closure controls",
    )
    ids = a["profiles"][0]["state_ids"]
    star, path_old = states[ids[57]], states[ids[27]]
    target_old = states[ids[41]]["classes"]["mean_graded"]
    l = law_map(star["summary_laws"]["mean_graded"], "target_class").get(target_old, zero())
    r = law_map(path_old["summary_laws"]["mean_graded"], "target_class").get(target_old, zero())
    expected = zero()
    expected[1][2] = 1
    expected[2][2] = -1
    require(
        star["mean_graded"] == path_old["mean_graded"] and l == expected and r == zero(),
        "K star/path mean witness",
    )
    absorbing = []
    for frame in a["frames"]:
        fixed = [
            state
            for state in states
            if state["frame_id"] == frame["frame_id"] and state["mask"] == 0
        ]
        require(len(fixed) == 1, "unique fixed-only state")
        unit = zero()
        unit[0][0] = 1
        require_same_wire(
            fixed[0]["transitions"],
            [{"target_state": fixed[0]["state_id"], "coefficients": unit}],
            "fixed absorbing row",
        )
        absorbing.append({"frame_id": frame["frame_id"], "state_id": fixed[0]["state_id"]})
    compression = None
    for group in stable["classes"]:
        left_id = group["members"][0]
        for right_id in group["members"][1:]:
            if states[left_id]["color_order"] != states[right_id]["color_order"]:
                compression = {
                    "stable_class": group["class_id"],
                    "left_state": left_id,
                    "right_state": right_id,
                    "left_color_order": states[left_id]["color_order"],
                    "right_color_order": states[right_id]["color_order"],
                    "equal_stable_pushed_rows": True,
                }
                rows = stable["rounds"][-1]["pushforward_rows"]
                require_same_wire(
                    rows[left_id]["transitions"],
                    rows[right_id]["transitions"],
                    "retained nonisomorphic compression",
                )
                break
        if compression is not None:
            break
    independent = sum((F(c * d, 4) for c, d in product((0, 1), repeat=2)), F(0))
    reused = sum((F(coin * coin, 2) for coin in (0, 1)), F(0))
    require(independent == F(1, 4) and reused == F(1, 2), "fresh/reused coin diagnostic")
    return {
        "adversary": {
            "path_state": path["state_id"],
            "cycle_state": cycle["state_id"],
            "full_mask": 63,
            "cycle_target_mask": 45,
            "target_state": target_state["state_id"],
            "target_pair_class": target,
            "counts": [1, 6, 5, 0],
            "target_counts": [1, 4, 4, 0],
            "equal_D": True,
            "equal_B": True,
            "shared_R22": r22,
            "path_coefficients": left,
            "cycle_coefficients": right,
            "evaluations": evaluations,
            "path_count_law": path_law,
            "cycle_count_law": cycle_law,
            "path_stable_class": left_class,
            "cycle_stable_class": right_class,
        },
        "old_mean_witness": {
            "star_state": star["state_id"],
            "path_state": path_old["state_id"],
            "target_mean_class": target_old,
            "star_coefficients": l,
            "path_coefficients": r,
            "half_probabilities": ["1/16", "0"],
        },
        "positive_basic_closure_partitions": ["color_order", "full_record"],
        "failed_basic_partitions": ["mean_graded", "pair_graded"],
        "fixed_absorbing": absorbing,
        "compression_witness": compression,
        "reused_coin": {
            "per_stage_rate": "1/2",
            "independent_retention": str(independent),
            "reused_retention": str(reused),
            "fresh_independence_premise_satisfied": False,
            "is_counterexample_to_declared_semigroup": False,
        },
    }


def run_suite():
    direct = load("qr05l_capture_direct", "refinement.py")
    reference = load("qr05l_capture_reference", "reference_qr05l.py")
    problem = fixtures()[0]
    a, b = direct.analyze(problem), reference.analyze(problem)
    require_same_wire(a, b, "independent complete L outputs differ")
    audit = check_analysis(a)
    refinement_audit = check_stabilization(a)
    trace = check_traces(a)
    rejections = []
    for index, invalid in enumerate(invalid_fixtures()):
        rejected = []
        for name, module in (
            ("observed_pairs_coefficient_refinement", direct),
            ("source_moments_grid_worklist", reference),
        ):
            try:
                module.analyze(invalid)
            except (TypeError, ValueError):
                rejected.append(name)
            else:
                raise ValueError("malformed L problem accepted")
        rejections.append({"fixture_index": index, "input": invalid, "rejected_by": rejected})
    suite = {
        "input": problem,
        "analysis": a,
        "audit": audit,
        "refinement_audit": refinement_audit,
        "trace_audit": trace,
        "controls": controls(a),
        "prior_bridge": prior_bridge(a),
        "rejections": rejections,
        "research_base_commit": BASE_COMMIT,
        "claim": "A realized equal-pair-summary counterexample defeats expanded-domain closure; exact partition refinement constructs the coarsest strongly closed B-refinement on the declared finite state and rate family.",
        "bounds": {
            "events_per_source": 8,
            "eligible_per_source_max": 6,
            "chain_order_max": 3,
            "transition_bidegree_max": [3, 3],
            "composition_four_variable_degree_max": [3, 3, 3, 3],
            "strict_round_bound": len(a["states"]) - len(a["partitions"]["pair_graded"]),
            "exact_component_bits": 4096,
        },
        "parameter_domain": "[0,1]^2 per fresh independent stage",
        "expanded_domain_subset_closed": True,
        "original_K_domain_preserved": True,
        "original_K_pair_quotient_restriction_verified": True,
        "initial_pair_partition_retained": True,
        "failed_B_has_quotient": False,
        "previous_class_preserved_in_refinement_key": True,
        "finite_coarsest_B_refinement_established": True,
        "coarseness_basis": "Recorded induction plus exact initialization, refinement-step and terminal-closure checks; not exhaustive partition search or Lean.",
        "source_labels_in_summary_keys": False,
        "aliases_used_as_weights": False,
        "selected_rate_zeros_discarded": False,
        "expected_updates_imply_full_law": False,
        "general_pair_closure_claimed": False,
        "refinement_depth_is_trace_horizon": False,
        "terminal_marginal_substituted_for_trace": False,
        "trace_minimality_claimed": False,
        "minimum_storage_or_runtime_claimed": False,
        "deterministic_mask_update_established": False,
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
        "basic_class_counts": {n: len(a["partitions"][n]) for n in PARTITIONS},
        "closed_basic_partition_names": [n for n in PARTITIONS if a["closure"][n]["closed"]],
        "stabilization": a["stabilization"]["counts"],
        "all_semigroup_coefficient_cells": a["counts"]["semigroup_coefficient_cells"]
        + a["stabilization"]["counts"]["semigroup_coefficient_cells"],
        "audit_rate_points": len(AUDIT_POINTS),
        "trace_rows": trace["checked_rows"],
        "trace_atoms": trace["structural_trace_atoms"],
        "prior_states": suite["prior_bridge"]["matched_states"],
        "prior_aliases": suite["prior_bridge"]["matched_original_aliases"],
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
