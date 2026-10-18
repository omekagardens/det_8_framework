"""QR-05K exact finite sampling capture and read-only replay."""

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
SCHEMA = "det8-qr05k-results-v1"
BASE_COMMIT = "a2d3b5f3ad7637939835140a9fe9acc6f66b28e2"
SOURCES = (
    "README.md",
    "closure.py",
    "reference_qr05k.py",
    "study.py",
    "test_qr05k.py",
    "test_capture.py",
)
PRIORS = {
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
PROFILE_NAMES = ("ferrers6", "standard_example3", "chain6", "ferrers6_fixed")
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
TOWER_PAIRS = (
    ((F(1, 2), F(1, 2)), (F(1, 2), F(1, 2))),
    ((F(1, 3), F(2, 3)), (F(2, 5), F(3, 7))),
    ((F(0), F(1, 2)), (F(2, 3), F(1))),
    ((F(1), F(1)), (F(1, 3), F(2, 3))),
)


def fixtures():
    return [{"schema_version": "det8-qr05k-problem-v1", "family": "qr05j_recursive_iid"}]


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
        },
        "analysis fields",
    )
    frames, profiles, states = a["frames"], a["profiles"], a["states"]
    require(len(frames) == 2 and len(profiles) == 4 and len(states) == 188, "domain sizes")
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


def prior_bridge(a):
    old_suite = prior_json("qr-05j-uncertainty-contract-2026-09-06/results.json")["suite"]
    old = old_suite["analysis"]
    mapping = (0, 0, 0, 0, 0, 1, 2, 2, 2, 3)
    require(len(old["cases"]) == len(mapping), "J case domain")
    matched = zeros = 0
    aliases = set()
    rows = []
    for ci, previous in enumerate(old["cases"]):
        pid = mapping[ci]
        profile = a["profiles"][pid]
        frame = a["frames"][profile["frame_id"]]
        require(
            previous["profile"] == profile["name"] and previous["past"] == profile["past"],
            "J source identity",
        )
        require(
            [previous[k] for k in ("density", "fixed", "eligible")] == frame_value(frame),
            "J frame identity",
        )
        for before in previous["states"]:
            state = a["states"][profile["state_ids"][before["mask"]]]
            require({"profile_index": pid, "mask": before["mask"]} in state["aliases"], "J alias")
            for field in (
                "mask",
                "kept",
                "past",
                "color_sizes",
                "chain_counts",
                "pair_graded",
                "color_order",
            ):
                require_same_wire(state[field], before[field], "J observed feature " + field)
            require_same_wire(state["mean_graded"], before["mean_polynomials"], "J mean polynomial")
            require_same_wire(state["mean_graded"], before["color_graded"], "J mean grading")
            aliases.add((pid, before["mask"]))
            matched += 1
            zeros += F(before["probability"]) == 0
            rows.append(
                {
                    "case_index": ci,
                    "profile_index": pid,
                    "mask": before["mask"],
                    "state_id": state["state_id"],
                }
            )
    require(
        matched == 608 and len(aliases) == 224 and zeros == 98,
        "complete J coverage including zero-mass aliases",
    )
    return {
        "verified": True,
        "source_gate": "QR-05J",
        "representative_cases": [0, 5, 6, 9],
        "matched_aliases": len(aliases),
        "matched_state_occurrences": matched,
        "zero_first_mass_occurrences_retained": zeros,
        "state_correspondence": rows,
        "old_history_partitions_reinterpreted": False,
        "old_design_masses_used": False,
        "earlier_bridge_retained": old_suite["prior_bridge"],
    }


def check_tower(a):
    states = a["states"]
    cache = {}

    def moments(sid, rates):
        key = (sid, *rates)
        if key not in cache:
            weights = evaluated_row(states[sid]["transitions"], "target_state", *rates)
            mean = [
                sum((p * states[t]["chain_counts"][q] for t, p in weights.items()), F(0))
                for q in range(4)
            ]
            covariance = [
                [
                    sum(
                        (
                            p
                            * (states[t]["chain_counts"][q] - mean[q])
                            * (states[t]["chain_counts"][r] - mean[r])
                            for t, p in weights.items()
                        ),
                        F(0),
                    )
                    for r in range(4)
                ]
                for q in range(4)
            ]
            cache[key] = (mean, covariance)
        return cache[key]

    rows = []
    encode = lambda matrix: [[str(v) for v in row] for row in matrix]
    for state in states:
        for pair_index, (first, second) in enumerate(TOWER_PAIRS):
            weights = evaluated_row(state["transitions"], "target_state", *first)
            children = {sid: moments(sid, second) for sid in weights}
            mean = [
                sum((weights[sid] * values[0][q] for sid, values in children.items()), F(0))
                for q in range(4)
            ]
            within = [
                [
                    sum((weights[sid] * values[1][q][r] for sid, values in children.items()), F(0))
                    for r in range(4)
                ]
                for q in range(4)
            ]
            between = [
                [
                    sum(
                        (
                            weights[sid] * (values[0][q] - mean[q]) * (values[0][r] - mean[r])
                            for sid, values in children.items()
                        ),
                        F(0),
                    )
                    for r in range(4)
                ]
                for q in range(4)
            ]
            total = [[within[q][r] + between[q][r] for r in range(4)] for q in range(4)]
            direct_mean, direct_covariance = moments(
                state["state_id"], (first[0] * second[0], first[1] * second[1])
            )
            require(
                mean == direct_mean and total == direct_covariance,
                "total covariance tower/product-rate law",
            )
            require(
                all(
                    matrix[q][r] == matrix[r][q]
                    for matrix in (within, between, total)
                    for q, r in product(range(4), repeat=2)
                ),
                "covariance symmetry",
            )
            rows.append(
                {
                    "state_id": state["state_id"],
                    "pair_index": pair_index,
                    "final_mean": [str(v) for v in mean],
                    "within_covariance": encode(within),
                    "between_covariance": encode(between),
                    "final_covariance": encode(total),
                }
            )
    return {
        "stage_rate_pairs": [[[str(v) for v in rate] for rate in pair] for pair in TOWER_PAIRS],
        "rows": rows,
        "row_count": len(rows),
        "verified": True,
    }


def controls(a, tower):
    ids = a["profiles"][0]["state_ids"]
    states = a["states"]
    star, path = states[ids[57]], states[ids[27]]
    target = states[ids[41]]["classes"]["mean_graded"]
    require_same_wire(star["mean_graded"], path["mean_graded"], "selected equal D witness")
    left = law_map(star["summary_laws"]["mean_graded"], "target_class").get(target, zero())
    right = law_map(path["summary_laws"]["mean_graded"], "target_class").get(target, zero())
    expected = zero()
    expected[1][2] = 1
    expected[2][2] = -1
    require(left == expected and right == zero(), "selected star/path successor law")
    half = [str(evaluate(t, F(1, 2), F(1, 2))) for t in (left, right)]
    require(half == ["1/16", "0"], "selected star/path half-rate witness")
    require(not a["closure"]["mean_graded"]["closed"], "negative closure control")
    require(
        all(a["closure"][name]["closed"] for name in ("color_order", "full_record")),
        "positive closure controls",
    )
    absorbing = []
    for frame in a["frames"]:
        fixed = [s for s in states if s["frame_id"] == frame["frame_id"] and s["mask"] == 0]
        require(len(fixed) == 1, "unique frame fixed state")
        unit = zero()
        unit[0][0] = 1
        require_same_wire(
            fixed[0]["transitions"],
            [{"target_state": fixed[0]["state_id"], "coefficients": unit}],
            "absorbing fixed observation",
        )
        absorbing.append({"frame_id": frame["frame_id"], "state_id": fixed[0]["state_id"]})
    singleton = ids[1]
    row = next(
        row for row in tower["rows"] if row["state_id"] == singleton and row["pair_index"] == 0
    )
    within, between, final = (
        row[key][1][1] for key in ("within_covariance", "between_covariance", "final_covariance")
    )
    require(
        [within, between, final] == ["1/8", "1/16", "3/16"], "singleton covariance decomposition"
    )
    independent_retention = sum((F(a * b, 4) for a, b in product((0, 1), repeat=2)), F(0))
    reused_retention = sum((F(coin * coin, 2) for coin in (0, 1)), F(0))
    require(
        independent_retention == F(1, 4) and reused_retention == F(1, 2),
        "fresh versus reused coin diagnostic",
    )
    return {
        "star_path": {
            "profile_index": 0,
            "left_mask": 57,
            "right_mask": 27,
            "left_state": star["state_id"],
            "right_state": path["state_id"],
            "target_mask": 41,
            "target_class": target,
            "equal_mean_summary": True,
            "left_coefficients": left,
            "right_coefficients": right,
            "half_probabilities": half,
        },
        "positive_closure_partitions": ["color_order", "full_record"],
        "mean_closure": a["closure"]["mean_graded"]["closed"],
        "measured_pair_closure": a["closure"]["pair_graded"]["closed"],
        "fixed_absorbing": absorbing,
        "singleton_tower": {
            "state_id": singleton,
            "pair_index": 0,
            "within_variance": within,
            "between_variance": between,
            "final_variance": final,
        },
        "reused_coin": {
            "per_stage_rate": "1/2",
            "independent_two_stage_retention": str(independent_retention),
            "reused_coin_two_stage_retention": str(reused_retention),
            "fresh_independence_premise_satisfied": False,
            "is_counterexample_to_declared_semigroup": False,
        },
    }


def run_suite():
    direct = load("qr05k_capture_direct", "closure.py")
    reference = load("qr05k_capture_reference", "reference_qr05k.py")
    problem = fixtures()[0]
    a, b = direct.analyze(problem), reference.analyze(problem)
    require_same_wire(a, b, "independent complete K outputs differ")
    audit = check_analysis(a)
    tower = check_tower(a)
    rejections = []
    for index, invalid in enumerate(invalid_fixtures()):
        rejected = []
        for name, module in (
            ("observed_chain_pairs_binomial", direct),
            ("full_count_moments_interpolation", reference),
        ):
            try:
                module.analyze(invalid)
            except (TypeError, ValueError):
                rejected.append(name)
            else:
                raise ValueError("malformed K problem accepted")
        rejections.append({"fixture_index": index, "input": invalid, "rejected_by": rejected})
    suite = {
        "input": problem,
        "analysis": a,
        "audit": audit,
        "covariance_tower": tower,
        "controls": controls(a, tower),
        "prior_bridge": prior_bridge(a),
        "rejections": rejections,
        "research_base_commit": BASE_COMMIT,
        "claim": "Exact finite recursive summary closure under independent two-color thinning; expected feature updates do not suffice for next-summary-law closure.",
        "bounds": {
            "events_per_source": 8,
            "eligible_per_source_max": 6,
            "chain_order_max": 3,
            "transition_bidegree_max": [3, 3],
            "composition_four_variable_degree_max": [3, 3, 3, 3],
            "exact_component_bits": 4096,
        },
        "parameter_domain": "[0,1]^2 per independent stage",
        "new_subset_closed_observed_state_domain": True,
        "source_aliases_used_as_weights": False,
        "old_current_design_tokens_in_summary_keys": False,
        "selected_rate_zeros_discarded_from_structural_rows": False,
        "expected_update_implies_stochastic_closure": False,
        "failed_partition_has_quotient": False,
        "finite_pair_summary_closure_established": a["closure"]["pair_graded"]["closed"],
        "general_pair_summary_closure_established": False,
        "deterministic_mask_update_established": False,
        "adaptive_rate_composition_tested": False,
        "correlated_stage_composition_claimed": False,
        "minimal_summary_established": False,
        "observation_composition_is_physical_time": False,
        "positive_definiteness_required": False,
        "covariance_regularization_added": False,
        "application_speedup_measured": False,
        "empirical_data_used": False,
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
        "class_counts": {n: len(a["partitions"][n]) for n in PARTITIONS},
        "closed_partition_names": [n for n in PARTITIONS if a["closure"][n]["closed"]],
        "audit_rate_points": len(AUDIT_POINTS),
        "covariance_tower_rows": tower["row_count"],
        "prior_aliases": suite["prior_bridge"]["matched_aliases"],
        "prior_state_occurrences": suite["prior_bridge"]["matched_state_occurrences"],
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
