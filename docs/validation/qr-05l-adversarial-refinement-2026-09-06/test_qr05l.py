"""Independent L refinement tests adapted from the earlier K test lineage.

No earlier executor is imported. New graph features and kernels are rebuilt
from observed subset outcomes; prior evidence is read only as pinned JSON.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from functools import cache
from itertools import combinations, pairwise, permutations, product
from math import comb
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
F = Fraction
K_SHA = "46d93f643c443b75ef425349cff11d7f3c437a79921e7e1ee94610998bd1a501"
PROFILES = ("ferrers6", "standard_example3", "chain6", "ferrers6_fixed", "path6", "cycle4_edge")
QUESTIONS = ("mean_graded", "pair_graded", "color_order", "full_record")
POINTS = tuple(
    dict.fromkeys(
        (
            *product((F(0), F(1, 3), F(2, 3), F(1)), repeat=2),
            (F(1, 2), F(1, 2)),
            (F(2, 5), F(3, 7)),
            (F(1, 5), F(4, 5)),
            (F(1, 2), F(1, 3)),
            (F(0), F(2, 5)),
            (F(3, 7), F(1)),
        )
    )
)
STAGES = (
    ((F(1, 2), F(1, 2)), (F(1, 2), F(1, 2))),
    ((F(1, 3), F(2, 3)), (F(2, 5), F(3, 7))),
    ((F(0), F(1, 2)), (F(2, 3), F(1))),
    ((F(1), F(1)), (F(1, 3), F(2, 3))),
)


def problem():
    return {"schema_version": "det8-qr05l-problem-v1", "family": "qr05l_adversarial_iid"}


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("test-private module already occupied")
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("executor unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05l_test_direct", "refinement.py"),
        private_module("_qr05l_test_reference", "reference_qr05l.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors):
    return tuple(module.analyze(problem()) for module in executors)


@pytest.fixture(scope="session")
def pinned_k():
    path = HERE.parent / "qr-05k-recursive-closure-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == K_SHA
    artifact = json.loads(raw)
    assert (
        json.dumps(artifact, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(artifact["suite"])
    return artifact["suite"]["analysis"]


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05l_test_aggregate", "study.py")
    return runner, runner.run_suite()


def native(value):
    if value is None or type(value) in (bool, int, str):
        return
    if type(value) is list:
        for item in value:
            native(item)
        return
    if type(value) is dict:
        assert all(type(key) is str for key in value)
        for item in value.values():
            native(item)
        return
    raise AssertionError(f"non-native exact mathematical type {type(value)}")


def wire(value):
    native(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


@cache
def source(profile):
    past = [[]]
    for j in range(6):
        if profile == "path6":
            before = [a for a, b in ((1, 2), (1, 4), (3, 4), (3, 6), (5, 6)) if b == j + 1]
        elif profile == "cycle4_edge":
            before = [a for a, b in ((1, 4), (1, 6), (3, 4), (3, 6), (2, 5)) if b == j + 1]
        elif profile == "chain6":
            before = list(range(1, j + 1))
        elif j < 3:
            before = []
        else:
            before = [
                i + 1
                for i in range(3)
                if (i != j - 3 if profile == "standard_example3" else i <= j - 3)
            ]
        past.append([0, *before])
    past.append(list(range(7)))
    fixed = [0, 3, 7] if profile == "ferrers6_fixed" else [0, 7]
    eligible = [v for v in range(1, 7) if v not in fixed]
    return past, fixed, eligible


@cache
def observed(profile, mask):
    original, fixed, eligible = source(profile)
    kept = sorted(fixed + [v for j, v in enumerate(eligible) if mask & (1 << j)])
    past = [[i for i, v in enumerate(kept) if v in original[target]] for target in kept]
    local = {v: i for i, v in enumerate(kept)}
    d = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    counts = []
    for q in range(4):
        number = 0
        for vertices in combinations([v for v in kept if 0 < v < 7], q):
            if all(local[a] in past[local[b]] for a, b in pairwise([0, *vertices, 7])):
                support = [v for v in vertices if v in eligible]
                o = sum(v % 2 for v in support)
                d[q][o][len(support) - o] += 1
                number += 1
        counts.append(number)
    o = sum(v % 2 for v in kept if v in eligible)
    return {
        "mask": mask,
        "kept": kept,
        "past": past,
        "chain_counts": counts,
        "mean_graded": d,
        "color_sizes": [o, mask.bit_count() - o],
    }


@cache
def submasks(s):
    return [u for u in range(s + 1) if u & s == u]


@cache
def pairs_from_outcomes(profile, s):
    odd, even = observed(profile, s)["color_sizes"]
    values = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for u in submasks(s):
        observation = observed(profile, u)
        o, e = observation["color_sizes"]
        for q in range(4):
            for r in range(4):
                values[q][r][o][e] += (
                    observation["chain_counts"][q] * observation["chain_counts"][r]
                )
    b = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for q in range(4):
        for r in range(4):
            for a in range(odd + 1):
                for c in range(even + 1):
                    b[q][r][a][c] = sum(
                        values[q][r][o][e]
                        * (-1) ** (a - o + c - e)
                        * comb(odd - o, a - o)
                        * comb(even - e, c - e)
                        for o in range(a + 1)
                        for e in range(c + 1)
                    )
    return b


@cache
def color_code(profile, s):
    state = observed(profile, s)
    fixed = source(profile)[1]
    kept, past = state["kept"], state["past"]
    local, n = {v: i for i, v in enumerate(kept)}, len(kept)
    codes = []
    for perm in permutations([v for v in kept if v not in fixed]):
        arrangement = [*fixed, *perm]
        relation = sum(
            1 << (i * n + j)
            for i, a in enumerate(arrangement)
            for j, b in enumerate(arrangement)
            if local[a] in past[local[b]]
        )
        color = sum(1 << i for i, v in enumerate(arrangement) if v not in fixed and v % 2)
        codes.append((relation, color))
    return [n, *min(codes)]


def zero_table():
    return [[0] * 4 for _ in range(4)]


@cache
def transition_coefficients(odd, even, o, e):
    table = zero_table()
    for a in range(odd - o + 1):
        for b in range(even - e + 1):
            table[o + a][e + b] = (-1) ** (a + b) * comb(odd - o, a) * comb(even - e, b)
    return table


@cache
def evaluate_immutable(table, x, y):
    return sum(
        (F(c) * x**a * y**b for a, row in enumerate(table) for b, c in enumerate(row) if c),
        start=F(0),
    )


def evaluate(table, x, y):
    return evaluate_immutable(tuple(tuple(row) for row in table), x, y)


@pytest.fixture(scope="session")
def independent():
    frames, profiles, states = [], [], []
    frame_index, state_index, aliases = {}, {}, {}
    for pi, profile in enumerate(PROFILES):
        past, fixed, eligible = source(profile)
        frame = ["12", fixed, eligible]
        encoded = wire(frame)
        if encoded not in frame_index:
            fi = len(frames)
            frame_index[encoded] = fi
            frames.append({"frame_id": fi, "density": "12", "fixed": fixed, "eligible": eligible})
        fi = frame_index[encoded]
        state_ids = []
        for s in range(1 << len(eligible)):
            observation = observed(profile, s)
            encoded = wire([frame, observation["kept"], observation["past"]])
            if encoded not in state_index:
                sid = len(states)
                state_index[encoded] = sid
                states.append(
                    {
                        "state_id": sid,
                        "frame_id": fi,
                        **observation,
                        "pair_graded": pairs_from_outcomes(profile, s),
                        "color_order": color_code(profile, s),
                        "aliases": [],
                    }
                )
            sid = state_index[encoded]
            states[sid]["aliases"].append({"profile_index": pi, "mask": s})
            state_ids.append(sid)
            aliases[pi, s] = sid
        profiles.append(
            {
                "profile_index": pi,
                "name": profile,
                "frame_id": fi,
                "past": past,
                "state_ids": state_ids,
            }
        )
    partitions, lookup = {q: [] for q in QUESTIONS}, {q: {} for q in QUESTIONS}
    for state in states:
        frame = frames[state["frame_id"]]
        public = [frame["density"], frame["fixed"], frame["eligible"]]
        keys = {
            "mean_graded": [public, state["mean_graded"]],
            "pair_graded": [public, state["pair_graded"]],
            "color_order": [public, state["color_order"]],
            "full_record": [public, state["kept"], state["past"]],
        }
        state["classes"] = {}
        for q, key in keys.items():
            encoded = wire(key)
            if encoded not in lookup[q]:
                cid = len(partitions[q])
                lookup[q][encoded] = cid
                partitions[q].append({"class_id": cid, "key": key, "members": []})
            cid = lookup[q][encoded]
            state["classes"][q] = cid
            partitions[q][cid]["members"].append(state["state_id"])
    for state in states:
        pi = state["aliases"][0]["profile_index"]
        odd, even = state["color_sizes"]
        transitions = []
        for u in submasks(state["mask"]):
            tid = aliases[pi, u]
            o, e = states[tid]["color_sizes"]
            transitions.append(
                {"target_state": tid, "coefficients": transition_coefficients(odd, even, o, e)}
            )
        state["transitions"] = sorted(transitions, key=lambda row: row["target_state"])
        state["summary_laws"] = {}
        for q in QUESTIONS:
            grouped = {}
            for row in transitions:
                target = states[row["target_state"]]["classes"][q]
                table = grouped.setdefault(target, zero_table())
                for i in range(4):
                    for j in range(4):
                        table[i][j] += row["coefficients"][i][j]
            state["summary_laws"][q] = [
                {"target_class": target, "coefficients": table}
                for target, table in sorted(grouped.items())
            ]
    return {
        "frames": frames,
        "profiles": profiles,
        "states": states,
        "partitions": partitions,
    }, aliases


def refinement(states, left, right):
    images = {}
    for state in states:
        images.setdefault(state["classes"][left], set()).add(state["classes"][right])
    return all(len(targets) == 1 for targets in images.values())


def composition(rows):
    reports = []
    for first in rows:
        source = first["class_id"]
        accumulated = {}
        paths = 0
        for hop in first["transitions"]:
            left = [
                (4 * i + j, c)
                for i, row in enumerate(hop["coefficients"])
                for j, c in enumerate(row)
                if c
            ]
            second = rows[hop["target_class"]]
            for final in second["transitions"]:
                paths += 1
                coefficients = accumulated.setdefault(final["target_class"], [0] * 256)
                right = [
                    (4 * i + j, c)
                    for i, row in enumerate(final["coefficients"])
                    for j, c in enumerate(row)
                    if c
                ]
                for i, a in left:
                    for j, b in right:
                        coefficients[16 * i + j] += a * b
        assert set(accumulated) == {row["target_class"] for row in first["transitions"]}
        for final in first["transitions"]:
            embedded = [0] * 256
            for i, row in enumerate(final["coefficients"]):
                for j, c in enumerate(row):
                    index = 4 * i + j
                    embedded[16 * index + index] = c
            assert accumulated[final["target_class"]] == embedded
        reports.append(
            {
                "class_id": source,
                "transition_pairs": len(accumulated),
                "intermediate_paths": paths,
                "coefficient_cells": 256 * len(accumulated),
                "max_abs_residual": 0,
            }
        )
    return {
        "verified": True,
        "rows": reports,
        "totals": {
            name: sum(row[name] for row in reports)
            for name in (
                "transition_pairs",
                "intermediate_paths",
                "coefficient_cells",
                "max_abs_residual",
            )
        },
    }


@pytest.fixture(scope="session")
def expected_closure(independent):
    model, _ = independent
    states, partitions = model["states"], model["partitions"]
    result = {}
    for q in QUESTIONS:
        collision = None
        for state in states:
            cid = state["classes"][q]
            first = partitions[q][cid]["members"][0]
            left = {
                row["target_class"]: row["coefficients"] for row in states[first]["summary_laws"][q]
            }
            right = {row["target_class"]: row["coefficients"] for row in state["summary_laws"][q]}
            for target in sorted(left.keys() | right.keys()):
                a, b = left.get(target, zero_table()), right.get(target, zero_table())
                if a != b:
                    collision = {
                        "class_id": cid,
                        "left_state": first,
                        "right_state": state["state_id"],
                        "target_class": target,
                        "left_coefficients": a,
                        "right_coefficients": b,
                    }
                    break
            if collision is not None:
                break
        rows = (
            None
            if collision
            else [
                {
                    "class_id": group["class_id"],
                    "representative_state": group["members"][0],
                    "transitions": states[group["members"][0]]["summary_laws"][q],
                }
                for group in partitions[q]
            ]
        )
        result[q] = {
            "closed": collision is None,
            "first_collision": collision,
            "quotient_rows": rows,
            "semigroup": None if rows is None else composition(rows),
        }
    return result


def classes_of(ids):
    classes = []
    for sid, cid in enumerate(ids):
        if cid == len(classes):
            classes.append({"class_id": cid, "members": []})
        assert 0 <= cid < len(classes)
        classes[cid]["members"].append(sid)
    return classes


def pushed_rows(states, ids):
    rows = []
    for state in states:
        accumulated = {}
        for transition in state["transitions"]:
            table = accumulated.setdefault(ids[transition["target_state"]], zero_table())
            for i, coefficients in enumerate(transition["coefficients"]):
                for j, coefficient in enumerate(coefficients):
                    table[i][j] += coefficient
        rows.append(
            {
                "state_id": state["state_id"],
                "transitions": [
                    {"target_class": target, "coefficients": table}
                    for target, table in sorted(accumulated.items())
                ],
            }
        )
    return rows


def first_difference(left, right):
    a = {row["target_class"]: row["coefficients"] for row in left}
    b = {row["target_class"]: row["coefficients"] for row in right}
    for target in sorted(a.keys() | b.keys()):
        lhs, rhs = a.get(target, zero_table()), b.get(target, zero_table())
        if lhs != rhs:
            return target, lhs, rhs
    return None


def refines_ids(fine, coarse):
    image = {}
    for a, b in zip(fine, coarse, strict=True):
        image.setdefault(a, set()).add(b)
    return all(len(values) == 1 for values in image.values())


@pytest.fixture(scope="session")
def expected_stabilization(independent):
    states = independent[0]["states"]
    ids = [state["classes"]["pair_graded"] for state in states]
    rounds = []
    while True:
        classes = classes_of(ids)
        pushed = pushed_rows(states, ids)
        labels = {}
        next_ids = []
        for sid, row in enumerate(pushed):
            key = wire([ids[sid], row["transitions"]])
            next_ids.append(labels.setdefault(key, len(labels)))
        assert refines_ids(next_ids, ids)
        stable = ids == next_ids
        separations = []
        for child in classes_of(next_ids):
            right = child["members"][0]
            parent = ids[right]
            left = classes[parent]["members"][0]
            if next_ids[left] == child["class_id"]:
                continue
            difference = first_difference(pushed[left]["transitions"], pushed[right]["transitions"])
            assert difference is not None
            target, lhs, rhs = difference
            separations.append(
                {
                    "parent_class_id": parent,
                    "child_class_id": child["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "target_class": target,
                    "left_coefficients": lhs,
                    "right_coefficients": rhs,
                }
            )
        rounds.append(
            {
                "round_index": len(rounds),
                "state_classes": ids,
                "classes": classes,
                "pushforward_rows": pushed,
                "stable": stable,
                "separations": separations,
            }
        )
        if stable:
            break
        assert len(labels) > len(classes)
        assert len(rounds) <= len(states) - len(rounds[0]["classes"])
        ids = next_ids
    rows = [
        {
            "class_id": group["class_id"],
            "representative_state": group["members"][0],
            "transitions": pushed[group["members"][0]]["transitions"],
        }
        for group in classes
    ]
    semigroup = composition(rows)
    names = ["mean_graded", "pair_graded", "stable_pair", "color_order", "full_record"]
    vectors = {
        q: ids if q == "stable_pair" else [state["classes"][q] for state in states] for q in names
    }
    atoms = sum(len(row["transitions"]) for item in rounds for row in item["pushforward_rows"])
    return {
        "initial_partition": "pair_graded",
        "rounds": rounds,
        "strict_rounds": len(rounds) - 1,
        "final_round": len(rounds) - 1,
        "state_classes": ids,
        "classes": classes,
        "quotient_rows": rows,
        "semigroup": semigroup,
        "comparison": {
            "names": names,
            "refinement": [[refines_ids(vectors[a], vectors[b]) for b in names] for a in names],
        },
        "counts": {
            "rounds": len(rounds),
            "strict_rounds": len(rounds) - 1,
            "classes": len(classes),
            "round_transition_atoms": atoms,
            "round_coefficient_cells": 16 * atoms,
            "separation_witnesses": sum(len(item["separations"]) for item in rounds),
            "quotient_transition_atoms": sum(len(row["transitions"]) for row in rows),
            "semigroup_intermediate_paths": semigroup["totals"]["intermediate_paths"],
            "semigroup_coefficient_cells": semigroup["totals"]["coefficient_cells"],
        },
    }


@pytest.fixture(scope="session")
def expected_trace(independent, expected_stabilization):
    states = independent[0]["states"]
    stable = expected_stabilization
    quotient = stable["quotient_rows"]
    pair_ids = [state["classes"]["pair_graded"] for state in states]
    stable_to_pair = [pair_ids[group["members"][0]] for group in stable["classes"]]

    @cache
    def quotient_trace(cid, pair_index):
        first_rates, second_rates = STAGES[pair_index]
        law = {}
        for first in quotient[cid]["transitions"]:
            mid = first["target_class"]
            p = evaluate(first["coefficients"], *first_rates)
            for second in quotient[mid]["transitions"]:
                key = (stable_to_pair[mid], stable_to_pair[second["target_class"]])
                law[key] = law.get(key, F(0)) + p * evaluate(second["coefficients"], *second_rates)
        return law

    rows = []
    for state in states:
        for index, (first_rates, second_rates) in enumerate(STAGES):
            law = {}
            for first in state["transitions"]:
                mid = first["target_state"]
                p = evaluate(first["coefficients"], *first_rates)
                for second in states[mid]["transitions"]:
                    key = (pair_ids[mid], pair_ids[second["target_state"]])
                    law[key] = law.get(key, F(0)) + p * evaluate(
                        second["coefficients"], *second_rates
                    )
            assert law == quotient_trace(stable["state_classes"][state["state_id"]], index)
            assert all(p >= 0 for p in law.values()) and sum(law.values()) == 1
            rows.append(
                {
                    "state_id": state["state_id"],
                    "rate_pair_index": index,
                    "atoms": [
                        {"first_pair_class": first, "last_pair_class": last, "probability": str(p)}
                        for (first, last), p in sorted(law.items())
                    ],
                    "probability_sum": "1",
                    "max_abs_residual": "0",
                }
            )
    return {
        "stage_rate_pairs": [[list(map(str, a)), list(map(str, b))] for a, b in STAGES],
        "rows": rows,
        "checked_rows": 4 * len(states),
        "structural_trace_atoms": sum(len(row["atoms"]) for row in rows),
        "verified": True,
    }


def test_exact_outputs_have_complete_native_schema_and_agree(analyses):
    assert wire(analyses[0]) == wire(analyses[1])
    assert wire(json.loads(wire(analyses[0]))) == wire(analyses[0])
    assert set(analyses[0]) == {
        "frames",
        "profiles",
        "states",
        "partitions",
        "partition_refinement",
        "closure",
        "expected_updates",
        "counts",
        "stabilization",
    }


def test_all_frames_aliases_deduplicated_states_and_partitions_are_independent(
    analyses, independent
):
    expected, aliases = independent
    assert len(expected["frames"]) == 2 and len(expected["profiles"]) == 6
    assert 188 < len(expected["states"]) <= 316 and len(aliases) == 352
    assert sum(len(state["aliases"]) for state in expected["states"]) == 352
    for analysis in analyses:
        for key in ("frames", "profiles", "states", "partitions"):
            assert wire(analysis[key]) == wire(expected[key])
        refinement_matrix = [
            [refinement(expected["states"], a, b) for b in QUESTIONS] for a in QUESTIONS
        ]
        assert wire(analysis["partition_refinement"]) == wire(refinement_matrix)
        for classes in analysis["partitions"].values():
            assert sorted(sid for group in classes for sid in group["members"]) == list(
                range(len(expected["states"]))
            )
            assert all(set(group) == {"class_id", "key", "members"} for group in classes)
            assert all(group["members"] == sorted(set(group["members"])) for group in classes)
        assert len(analysis["partitions"]["full_record"]) == len(expected["states"])
        assert all(
            state["classes"]["full_record"] == state["state_id"] for state in analysis["states"]
        )


def test_transition_support_coefficients_normalization_corners_and_boundary_rates(
    analyses, independent
):
    _, aliases = independent
    assert len(POINTS) == 22
    for analysis in analyses:
        states = analysis["states"]
        for state in states:
            odd, even = state["color_sizes"]
            rows = state["transitions"]
            assert [row["target_state"] for row in rows] == sorted(
                {row["target_state"] for row in rows}
            )
            assert len(rows) == 2 ** state["mask"].bit_count()
            assert all(
                sum(row["coefficients"][i][j] for row in rows) == int(i == j == 0)
                for i in range(4)
                for j in range(4)
            )
            for row in rows:
                successor = states[row["target_state"]]
                assert successor["frame_id"] == state["frame_id"]
                assert set(successor["kept"]) <= set(state["kept"])
                assert any(c for values in row["coefficients"] for c in values)
                assert all(
                    type(c) is int and abs(c).bit_length() <= 4096
                    for values in row["coefficients"]
                    for c in values
                )
                for x, y in POINTS:
                    o, e = successor["color_sizes"]
                    assert evaluate(row["coefficients"], x, y) == x**o * (1 - x) ** (
                        odd - o
                    ) * y**e * (1 - y) ** (even - e)
            pi = state["aliases"][0]["profile_index"]
            for x, y in product((F(0), F(1)), repeat=2):
                support = [
                    row["target_state"] for row in rows if evaluate(row["coefficients"], x, y)
                ]
                assert len(support) == 1
                if x == y == 1:
                    assert support == [state["state_id"]]
                if x == y == 0:
                    assert support == [aliases[pi, 0]]
            for q in QUESTIONS:
                law = state["summary_laws"][q]
                for x, y in POINTS:
                    expected = {}
                    for row in rows:
                        cid = states[row["target_state"]]["classes"][q]
                        expected[cid] = expected.get(cid, F(0)) + evaluate(
                            row["coefficients"], x, y
                        )
                    assert {
                        row["target_class"]: evaluate(row["coefficients"], x, y) for row in law
                    } == expected
                    assert sum(expected.values()) == 1
        fixed = [state for state in states if state["mask"] == 0]
        assert len(fixed) == 2
        for state in fixed:
            assert (
                len(state["transitions"]) == 1
                and state["transitions"][0]["target_state"] == state["state_id"]
            )


def feature_vector(state):
    return [v for table in state["mean_graded"] for row in table for v in row] + [
        v for matrix in state["pair_graded"] for table in matrix for row in table for v in row
    ]


def test_all_expected_feature_updates_are_diagonal_coefficientwise(analyses, independent):
    states = independent[0]["states"]
    feature_vectors = [feature_vector(state) for state in states]
    reports = []
    for state in states:
        actual = [[0] * 16 for _ in range(320)]
        for transition in state["transitions"]:
            coefficients = [
                (4 * i + j, c)
                for i, row in enumerate(transition["coefficients"])
                for j, c in enumerate(row)
                if c
            ]
            for f, value in enumerate(feature_vectors[transition["target_state"]]):
                if value:
                    for position, coefficient in coefficients:
                        actual[f][position] += value * coefficient
        for f, value in enumerate(feature_vectors[state["state_id"]]):
            expected = [0] * 16
            expected[f % 16] = value
            assert actual[f] == expected
        reports.append(
            {
                "state_id": state["state_id"],
                "mean_features": 64,
                "pair_features": 256,
                "coefficient_cells": 5120,
                "max_abs_residual": 0,
            }
        )
    expected = {"verified": True, "rows": reports, "coefficient_cells": 5120 * len(states)}
    for analysis in analyses:
        assert wire(analysis["expected_updates"]) == wire(expected)


def test_strong_closure_first_missing_target_witness_and_exact_quotients(
    analyses, independent, expected_closure
):
    states = independent[0]["states"]
    for analysis in analyses:
        assert wire(analysis["closure"]) == wire(expected_closure)
        assert analysis["closure"]["mean_graded"]["closed"] is False
        assert analysis["closure"]["mean_graded"]["quotient_rows"] is None
        assert analysis["closure"]["mean_graded"]["semigroup"] is None
        assert analysis["closure"]["pair_graded"]["closed"] is False
        assert analysis["closure"]["pair_graded"]["quotient_rows"] is None
        assert analysis["closure"]["pair_graded"]["semigroup"] is None
        for q in ("full_record", "color_order"):
            assert analysis["closure"][q]["closed"] is True
        for q, closure in analysis["closure"].items():
            if not closure["closed"]:
                collision = closure["first_collision"]
                a, b, target = (
                    collision["left_state"],
                    collision["right_state"],
                    collision["target_class"],
                )
                assert states[a]["classes"][q] == states[b]["classes"][q] == collision["class_id"]
                assert collision["left_coefficients"] != collision["right_coefficients"]
                for side, sid in (("left", a), ("right", b)):
                    expected = next(
                        (
                            row["coefficients"]
                            for row in states[sid]["summary_laws"][q]
                            if row["target_class"] == target
                        ),
                        zero_table(),
                    )
                    assert wire(collision[side + "_coefficients"]) == wire(expected)
            else:
                rows = closure["quotient_rows"]
                assert closure["first_collision"] is None
                for group, row in zip(analysis["partitions"][q], rows):
                    assert row["representative_state"] == group["members"][0]
                    assert all(
                        wire(states[sid]["summary_laws"][q]) == wire(row["transitions"])
                        for sid in group["members"]
                    )


def test_four_variable_semigroup_counts_and_measured_inventory(
    analyses, independent, expected_closure
):
    model, aliases = independent
    states = model["states"]
    fine = sum(len(state["transitions"]) for state in states)
    pushed = sum(len(row) for state in states for row in state["summary_laws"].values())
    closed = [item for item in expected_closure.values() if item["closed"]]
    expected = {
        "frames": 2,
        "profiles": 6,
        "aliases": len(aliases),
        "states": len(states),
        "partitions": 4,
        "fine_transition_atoms": fine,
        "summary_transition_atoms": pushed,
        "transition_coefficient_cells": 16 * (fine + pushed),
        "mean_feature_cells": len(states) * 64,
        "pair_feature_cells": len(states) * 256,
        "expected_update_coefficient_cells": len(states) * 320 * 16,
        "closed_partitions": len(closed),
        "quotient_transition_atoms": sum(
            len(row["transitions"]) for item in closed for row in item["quotient_rows"]
        ),
        "semigroup_intermediate_paths": sum(
            item["semigroup"]["totals"]["intermediate_paths"] for item in closed
        ),
        "semigroup_coefficient_cells": sum(
            item["semigroup"]["totals"]["coefficient_cells"] for item in closed
        ),
    }
    assert len(expected) == 15
    for analysis in analyses:
        assert wire(analysis["counts"]) == wire(expected)
        for q, item in analysis["closure"].items():
            if item["closed"]:
                assert wire(item["semigroup"]) == wire(expected_closure[q]["semigroup"])
                for row in item["semigroup"]["rows"]:
                    assert row["coefficient_cells"] == 256 * row["transition_pairs"]
                    assert row["max_abs_residual"] == 0


def test_selected_star_path_failure_is_not_hidden_by_expected_mean_updates(analyses, independent):
    _, aliases = independent
    for analysis in analyses:
        star, path = (analysis["states"][aliases[0, s]] for s in (57, 27))
        target = analysis["states"][aliases[0, 41]]["classes"]["mean_graded"]
        assert star["mean_graded"] == path["mean_graded"]
        assert star["summary_laws"]["mean_graded"] != path["summary_laws"]["mean_graded"]
        coefficient_rows = [
            next(
                (
                    row["coefficients"]
                    for row in state["summary_laws"]["mean_graded"]
                    if row["target_class"] == target
                ),
                zero_table(),
            )
            for state in (star, path)
        ]
        expected = zero_table()
        expected[1][2], expected[2][2] = 1, -1
        assert coefficient_rows == [expected, zero_table()]
        assert [evaluate(table, F(1, 2), F(1, 2)) for table in coefficient_rows] == [F(1, 16), F(0)]
        assert analysis["expected_updates"]["verified"] is True


def test_independent_stage_variables_and_reused_coin_are_different_contracts(independent):
    model, aliases = independent
    triple = model["states"][aliases[2, 21]]
    self_poly = next(
        row["coefficients"]
        for row in triple["transitions"]
        if row["target_state"] == triple["state_id"]
    )
    expected = zero_table()
    expected[3][0] = 1
    assert self_poly == expected
    # x^3 a^3 is valid in independent stage variables; identifying a=x
    # produces degree six, not a bidegree-three interpolation problem.
    for x, a in ((F(1, 2), F(1, 3)), (F(2, 3), F(2, 5))):
        assert evaluate(self_poly, x, F(1)) * evaluate(self_poly, a, F(1)) == (x * a) ** 3
    assert F(1, 2) ** 6 != F(1, 2) ** 3
    independent_final = sum(
        F(1, 4) for first, second in product((0, 1), repeat=2) if first and second
    )
    reused_final = sum(F(1, 2) for coin in (0, 1) if coin and coin)
    assert independent_final == F(1, 4) and reused_final == F(1, 2)


def test_whole_aggregate_native_exact_round_trip(aggregate):
    _, suite = aggregate
    assert wire(json.loads(wire(suite))) == wire(suite)


def test_canonical_refinement_every_round_and_coarseness_premises(
    analyses, independent, expected_stabilization
):
    states = independent[0]["states"]
    expected = expected_stabilization
    assert expected["strict_rounds"] > 0
    assert expected["strict_rounds"] <= len(states) - len(expected["rounds"][0]["classes"])
    for analysis in analyses:
        assert wire(analysis["stabilization"]) == wire(expected)
    for index, round_ in enumerate(expected["rounds"]):
        ids = round_["state_classes"]
        assert refines_ids(ids, [state["classes"]["pair_graded"] for state in states])
        assert sorted(sid for group in round_["classes"] for sid in group["members"]) == list(
            range(len(states))
        )
        # Both independently closed structural baselines must refine every
        # intermediate partition: each current block is their block union.
        for baseline in ("color_order", "full_record"):
            fine_ids = [state["classes"][baseline] for state in states]
            assert refines_ids(fine_ids, ids)
            for group in independent[0]["partitions"][baseline]:
                rows = [round_["pushforward_rows"][sid]["transitions"] for sid in group["members"]]
                assert all(row == rows[0] for row in rows)
        if round_["stable"]:
            assert index == len(expected["rounds"]) - 1
            assert round_["separations"] == []
            for group in round_["classes"]:
                rows = [round_["pushforward_rows"][sid]["transitions"] for sid in group["members"]]
                assert all(row == rows[0] for row in rows)
        else:
            following = expected["rounds"][index + 1]
            assert refines_ids(following["state_classes"], ids)
            assert len(following["classes"]) > len(round_["classes"])
            assert len(round_["separations"]) == len(following["classes"]) - len(round_["classes"])
            assert [row["child_class_id"] for row in round_["separations"]] == sorted(
                row["child_class_id"] for row in round_["separations"]
            )


def test_bottom_up_proper_successor_classification_independently_finds_same_fixed_point(
    independent, expected_stabilization
):
    states = independent[0]["states"]
    assigned, registry = {}, {}
    for state in sorted(states, key=lambda s: (s["mask"].bit_count(), s["state_id"])):
        proper = {}
        self_probability = None
        for atom in state["transitions"]:
            target = atom["target_state"]
            if target == state["state_id"]:
                self_probability = atom["coefficients"]
                continue
            assert states[target]["mask"].bit_count() < state["mask"].bit_count()
            table = proper.setdefault(assigned[target], zero_table())
            for i in range(4):
                for j in range(4):
                    table[i][j] += atom["coefficients"][i][j]
        assert self_probability is not None
        # All proper successors have already been classified. Equal B fixes
        # both color sizes and therefore the self-loop polynomial. Its class
        # does not need to be guessed or iterated in this triangular route.
        key = wire(
            [
                state["classes"]["pair_graded"],
                self_probability,
                [[target, table] for target, table in sorted(proper.items())],
            ]
        )
        assigned[state["state_id"]] = registry.setdefault(key, len(registry))
    canonical = {}
    ids = [canonical.setdefault(assigned[sid], len(canonical)) for sid in range(len(states))]
    assert ids == expected_stabilization["state_classes"]


def test_entire_k_prefix_retained_with_provenance_alias_filter(analyses, pinned_k):
    old_count = len(pinned_k["states"])
    assert old_count == 188
    for analysis in analyses:
        assert wire(analysis["frames"]) == wire(pinned_k["frames"])
        assert wire(analysis["profiles"][:4]) == wire(pinned_k["profiles"])
        additional_aliases = 0
        for old, state in zip(pinned_k["states"], analysis["states"][:old_count], strict=True):
            filtered = {
                **state,
                "aliases": [alias for alias in state["aliases"] if alias["profile_index"] < 4],
            }
            additional_aliases += len(state["aliases"]) - len(filtered["aliases"])
            assert wire(filtered) == wire(old)
            assert all(atom["target_state"] < old_count for atom in state["transitions"])
        assert additional_aliases > 0
        for q in QUESTIONS:
            pulled_back = []
            for group in analysis["partitions"][q]:
                members = [sid for sid in group["members"] if sid < old_count]
                if members:
                    pulled_back.append({**group, "members": members})
            assert wire(pulled_back) == wire(pinned_k["partitions"][q])
        assert wire(analysis["expected_updates"]["rows"][:old_count]) == wire(
            pinned_k["expected_updates"]["rows"]
        )
        assert pinned_k["closure"]["pair_graded"]["closed"] is True
        assert analysis["closure"]["pair_graded"]["closed"] is False
        # The closed old domain is unchanged; a global flag must not replace
        # the restriction evidence or retroactively negate K's scoped result.
        assert analysis["closure"]["pair_graded"]["quotient_rows"] is None


def test_stable_quotient_restricted_to_k_is_exact_original_pair_quotient(analyses, pinned_k):
    old_count = len(pinned_k["states"])
    for analysis in analyses:
        stable = analysis["stabilization"]
        mapping = {}
        for group in pinned_k["partitions"]["pair_graded"]:
            images = {stable["state_classes"][sid] for sid in group["members"]}
            assert len(images) == 1
            target = images.pop()
            mapping[group["class_id"]] = target
            restricted = [sid for sid in stable["classes"][target]["members"] if sid < old_count]
            assert restricted == group["members"]
        assert len(set(mapping.values())) == len(mapping)
        inverse = {new: old for old, new in mapping.items()}
        for old_row in pinned_k["closure"]["pair_graded"]["quotient_rows"]:
            row = stable["quotient_rows"][mapping[old_row["class_id"]]]
            assert all(atom["target_class"] in inverse for atom in row["transitions"])
            transported = sorted(
                (
                    {**atom, "target_class": inverse[atom["target_class"]]}
                    for atom in row["transitions"]
                ),
                key=lambda atom: atom["target_class"],
            )
            assert wire(transported) == wire(old_row["transitions"])
            assert row["representative_state"] == old_row["representative_state"]


def polynomial(terms):
    table = zero_table()
    for (i, j), coefficient in terms.items():
        table[i][j] = coefficient
    return table


def selected_mass(state, predicate):
    result = zero_table()
    for atom in state["transitions"]:
        if predicate(atom["target_state"]):
            for i in range(4):
                for j in range(4):
                    result[i][j] += atom["coefficients"][i][j]
    return result


def test_prespecified_adversary_has_equal_all_means_raw_pairs_but_unequal_full_laws(
    analyses, independent
):
    _, aliases = independent
    expected_raw = [
        polynomial({(1, 0): 3, (0, 1): 3, (2, 0): 6, (1, 1): 18, (0, 2): 6}),
        polynomial({(1, 1): 10, (2, 1): 10, (1, 2): 10}),
        polynomial({(1, 1): 5, (2, 1): 4, (1, 2): 4, (2, 2): 12}),
    ]
    witness = polynomial({(2, 2): 1, (3, 2): -1, (2, 3): -1, (3, 3): 1})
    for analysis in analyses:
        states = analysis["states"]
        left, right = (states[aliases[pi, 63]] for pi in (4, 5))
        target_state = states[aliases[5, 45]]
        target = target_state["classes"]["pair_graded"]
        assert target_state["kept"] == [0, 1, 3, 4, 6, 7]
        assert target_state["chain_counts"] == [1, 4, 4, 0]
        assert left["mean_graded"] == right["mean_graded"]
        assert left["pair_graded"] == right["pair_graded"]
        assert left["chain_counts"] == right["chain_counts"] == [1, 6, 5, 0]
        for state in (left, right):
            assert state["mean_graded"][1] == polynomial({(1, 0): 3, (0, 1): 3})
            assert state["mean_graded"][2] == polynomial({(1, 1): 5})
            assert state["mean_graded"][3] == zero_table()
            assert [state["pair_graded"][q][r] for q, r in ((1, 1), (1, 2), (2, 2))] == expected_raw
            assert all(
                state["pair_graded"][3][q] == state["pair_graded"][q][3] == zero_table()
                for q in range(4)
            )
        supported_masks = [
            [s for s in range(64) if states[aliases[pi, s]]["classes"]["pair_graded"] == target]
            for pi in (4, 5)
        ]
        assert supported_masks == [[], [45]]
        b_laws = [
            selected_mass(
                state,
                lambda sid, states=states, target=target: (
                    states[sid]["classes"]["pair_graded"] == target
                ),
            )
            for state in (left, right)
        ]
        count_laws = [
            selected_mass(
                state, lambda sid, states=states: states[sid]["chain_counts"] == [1, 4, 4, 0]
            )
            for state in (left, right)
        ]
        assert b_laws == count_laws == [zero_table(), witness]
        assert [evaluate(table, F(1, 2), F(1, 2)) for table in b_laws] == [F(0), F(1, 64)]
        assert [evaluate(table, F(1, 3), F(2, 3)) for table in b_laws] == [F(0), F(8, 729)]
        stable_ids = analysis["stabilization"]["state_classes"]
        assert left["classes"]["pair_graded"] == right["classes"]["pair_graded"]
        assert stable_ids[left["state_id"]] != stable_ids[right["state_id"]]
        assert left["color_order"] != right["color_order"]


def test_trace_audit_is_complete_fine_path_law_not_only_a_final_marginal(
    aggregate, expected_trace, independent
):
    _, suite = aggregate
    states, aliases = independent[0]["states"], independent[1]
    assert wire(suite["trace_audit"]) == wire(expected_trace)
    assert len(expected_trace["rows"]) == 4 * len(states)
    assert any(
        atom["probability"] == "0" for row in expected_trace["rows"] for atom in row["atoms"]
    )
    alive = states[aliases[0, 1]]["classes"]["pair_graded"]
    dead = states[aliases[0, 0]]["classes"]["pair_graded"]
    row = expected_trace["rows"][4 * aliases[0, 1]]
    actual = {
        (atom["first_pair_class"], atom["last_pair_class"]): F(atom["probability"])
        for atom in row["atoms"]
    }
    assert actual == {(alive, alive): F(1, 4), (alive, dead): F(1, 4), (dead, dead): F(1, 2)}
    assert (dead, alive) not in actual
    # The terminal alive mass is 1/4, but a trace also distinguishes survival
    # at the first observation followed by loss at the second observation.
    assert sum(p for (first, _), p in actual.items() if first == alive) == F(1, 2)


def test_retained_controls_include_full_count_laws_and_actual_remaining_compression(
    aggregate, independent, expected_stabilization
):
    _, suite = aggregate
    states, aliases = independent[0]["states"], independent[1]
    controls = suite["controls"]
    stable = expected_stabilization
    path, cycle, target = (states[aliases[pi, mask]] for pi, mask in ((4, 63), (5, 63), (5, 45)))

    def count_law(state):
        targets = sorted(
            {tuple(states[row["target_state"]]["chain_counts"]) for row in state["transitions"]}
        )
        return [
            {
                "counts": list(counts),
                "coefficients": selected_mass(
                    state, lambda sid, counts=counts: tuple(states[sid]["chain_counts"]) == counts
                ),
            }
            for counts in targets
        ]

    assert wire(controls["adversary"]) == wire(
        {
            "path_state": path["state_id"],
            "cycle_state": cycle["state_id"],
            "full_mask": 63,
            "cycle_target_mask": 45,
            "target_state": target["state_id"],
            "target_pair_class": target["classes"]["pair_graded"],
            "counts": [1, 6, 5, 0],
            "target_counts": [1, 4, 4, 0],
            "equal_D": True,
            "equal_B": True,
            "shared_R22": polynomial({(1, 1): 5, (2, 1): 4, (1, 2): 4, (2, 2): 12}),
            "path_coefficients": zero_table(),
            "cycle_coefficients": polynomial({(2, 2): 1, (3, 2): -1, (2, 3): -1, (3, 3): 1}),
            "evaluations": [
                {"rates": ["1/2", "1/2"], "path_probability": "0", "cycle_probability": "1/64"},
                {"rates": ["1/3", "2/3"], "path_probability": "0", "cycle_probability": "8/729"},
            ],
            "path_count_law": count_law(path),
            "cycle_count_law": count_law(cycle),
            "path_stable_class": stable["state_classes"][path["state_id"]],
            "cycle_stable_class": stable["state_classes"][cycle["state_id"]],
        }
    )
    assert wire(controls["old_mean_witness"]) == wire(
        {
            "star_state": aliases[0, 57],
            "path_state": aliases[0, 27],
            "target_mean_class": states[aliases[0, 41]]["classes"]["mean_graded"],
            "star_coefficients": polynomial({(1, 2): 1, (2, 2): -1}),
            "path_coefficients": zero_table(),
            "half_probabilities": ["1/16", "0"],
        }
    )
    assert controls["positive_basic_closure_partitions"] == ["color_order", "full_record"]
    assert controls["failed_basic_partitions"] == ["mean_graded", "pair_graded"]
    assert controls["fixed_absorbing"] == [
        {"frame_id": 0, "state_id": aliases[0, 0]},
        {"frame_id": 1, "state_id": aliases[3, 0]},
    ]
    compression = None
    for group in stable["classes"]:
        left = group["members"][0]
        for right in group["members"][1:]:
            if states[left]["color_order"] != states[right]["color_order"]:
                compression = {
                    "stable_class": group["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "left_color_order": states[left]["color_order"],
                    "right_color_order": states[right]["color_order"],
                    "equal_stable_pushed_rows": True,
                }
                break
        if compression is not None:
            break
    assert wire(controls["compression_witness"]) == wire(compression)
    assert wire(controls["reused_coin"]) == wire(
        {
            "per_stage_rate": "1/2",
            "independent_retention": "1/4",
            "reused_retention": "1/2",
            "fresh_independence_premise_satisfied": False,
            "is_counterexample_to_declared_semigroup": False,
        }
    )


def test_retained_audits_bridge_and_claim_boundaries(
    aggregate, analyses, independent, pinned_k, expected_stabilization
):
    _, suite = aggregate
    analysis = analyses[0]
    states, aliases = independent[0]["states"], independent[1]
    assert wire(suite["input"]) == wire(problem())
    assert wire(suite["analysis"]) == wire(analysis)
    counts = analysis["counts"]
    s = expected_stabilization
    assert wire(suite["audit"]) == wire(
        {
            "verified": True,
            "rates": [[str(x), str(y)] for x, y in POINTS],
            "rate_points": 22,
            "evaluated_fine_and_pushed_atoms": 22
            * (counts["fine_transition_atoms"] + counts["summary_transition_atoms"]),
            "evaluated_quotient_atoms": 22 * counts["quotient_transition_atoms"],
            "deterministic_corner_rows": 4 * len(states),
            "expected_feature_coefficient_cells": 5120 * len(states),
            "semigroup_coefficient_cells": counts["semigroup_coefficient_cells"],
        }
    )
    assert wire(suite["refinement_audit"]) == wire(
        {
            "verified": True,
            "rounds": len(s["rounds"]),
            "strict_rounds": s["strict_rounds"],
            "checked_round_atoms": s["counts"]["round_transition_atoms"],
            "round_coefficient_cells": s["counts"]["round_coefficient_cells"],
            "known_closed_refiner_round_checks": 2 * len(s["rounds"]),
            "evaluated_quotient_atoms": 22 * s["counts"]["quotient_transition_atoms"],
            "semigroup_coefficient_cells": s["counts"]["semigroup_coefficient_cells"],
            "coarsest_argument_premises_verified": True,
        }
    )
    bridge = suite["prior_bridge"]
    old_size = len(pinned_k["states"])
    assert wire(
        {
            key: value
            for key, value in bridge.items()
            if key not in ("stable_restriction", "earlier_bridge_retained")
        }
    ) == wire(
        {
            "verified": True,
            "source_gate": "QR-05K",
            "matched_states": old_size,
            "matched_original_aliases": 224,
            "additional_aliases_on_old_states": sum(
                alias["profile_index"] >= 4
                for state in states[:old_size]
                for alias in state["aliases"]
            ),
            "matched_profiles": 4,
            "basic_partition_memberships_matched": 4,
            "old_mass_filters_used": False,
        }
    )
    mapping = [
        {
            "old_pair_class": group["class_id"],
            "stable_class": s["state_classes"][group["members"][0]],
        }
        for group in pinned_k["partitions"]["pair_graded"]
    ]
    assert wire(bridge["stable_restriction"]) == wire(
        {
            "class_map": mapping,
            "classes": len(mapping),
            "memberships_verified": True,
            "quotient_polynomials_verified": True,
            "semigroup_verified": True,
            "fine_rows_leave_old_states": False,
            "quotient_rows_leave_class_image": False,
        }
    )
    prior_suite = json.loads(
        (HERE.parent / "qr-05k-recursive-closure-2026-09-06" / "results.json").read_bytes()
    )["suite"]
    assert wire(bridge["earlier_bridge_retained"]) == wire(prior_suite["prior_bridge"])
    assert len(aliases) == 352
    for flag in (
        "expanded_domain_subset_closed",
        "original_K_domain_preserved",
        "original_K_pair_quotient_restriction_verified",
        "initial_pair_partition_retained",
        "previous_class_preserved_in_refinement_key",
        "finite_coarsest_B_refinement_established",
    ):
        assert suite[flag] is True
    for flag in (
        "failed_B_has_quotient",
        "source_labels_in_summary_keys",
        "aliases_used_as_weights",
        "selected_rate_zeros_discarded",
        "expected_updates_imply_full_law",
        "general_pair_closure_claimed",
        "refinement_depth_is_trace_horizon",
        "terminal_marginal_substituted_for_trace",
        "trace_minimality_claimed",
        "minimum_storage_or_runtime_claimed",
        "deterministic_mask_update_established",
        "adaptive_rate_composition_tested",
        "correlated_stage_composition_claimed",
        "observation_composition_is_physical_time",
        "empirical_data_used",
        "empirical_noise_calibration_tested",
        "ret_integration_tested",
        "quantum_channel_constructed",
        "event_growth_constructed",
        "gravity_derived",
        "continuum_limit_established",
        "lean_proof_completed",
    ):
        assert suite[flag] is False
    assert "covariance_tower" not in suite


@pytest.mark.parametrize(
    "kind",
    (
        "early_stop",
        "extra_stable_round",
        "improper_merge",
        "replace_initial_partition",
        "missing_separation",
        "separation_child",
        "separation_target",
        "separation_coefficients",
        "round_class_bool",
        "final_class_bool",
        "quotient_coefficient",
        "composition_residual",
    ),
)
def test_refinement_audit_rejects_mutated_certificate(aggregate, analyses, kind):
    runner, _ = aggregate
    changed = {**analyses[0], "stabilization": json.loads(wire(analyses[0]["stabilization"]))}
    stable = changed["stabilization"]
    if kind == "early_stop":
        stable["rounds"] = stable["rounds"][:1]
        stable["rounds"][0]["stable"] = True
        stable["rounds"][0]["separations"] = []
    elif kind == "extra_stable_round":
        stable["rounds"].append(json.loads(wire(stable["rounds"][-1])))
        stable["rounds"][-1]["round_index"] += 1
    elif kind == "improper_merge":
        # A row-only merge is forbidden even if it preserved some rows:
        # the full previous B distinction must survive every next key.
        stable["rounds"][1]["state_classes"][1] = 0
    elif kind == "replace_initial_partition":
        stable["initial_partition"] = "color_order"
    elif kind == "missing_separation":
        stable["rounds"][0]["separations"] = []
    elif kind.startswith("separation_"):
        witness = stable["rounds"][0]["separations"][0]
        if kind == "separation_child":
            witness["child_class_id"] += 1
        elif kind == "separation_target":
            witness["target_class"] += 1
        else:
            witness["left_coefficients"][0][0] += 1
    elif kind == "round_class_bool":
        stable["rounds"][0]["state_classes"][0] = False
    elif kind == "final_class_bool":
        stable["state_classes"][0] = False
    elif kind == "quotient_coefficient":
        stable["quotient_rows"][0]["transitions"][0]["coefficients"][0][0] = 2
    else:
        stable["semigroup"]["rows"][0]["max_abs_residual"] = 1
    with pytest.raises(ValueError):
        runner.check_stabilization(changed)


@pytest.mark.parametrize(
    "kind",
    (
        "state_frame_bool",
        "alias_profile_bool",
        "profile_bool",
        "chain_count_bool",
        "coefficient_bool",
        "coefficient_value",
        "coefficient_shape",
        "pair_bool",
        "basic_class_bool",
        "source_identity",
        "kept_bool",
        "alias_missing",
    ),
)
def test_basic_audit_rejects_type_coercions_and_source_or_calculus_mutations(
    aggregate, analyses, kind
):
    runner, _ = aggregate
    changed = {
        **analyses[0],
        "states": list(analyses[0]["states"]),
        "profiles": list(analyses[0]["profiles"]),
    }
    changed["states"][0] = json.loads(wire(changed["states"][0]))
    changed["profiles"][0] = json.loads(wire(changed["profiles"][0]))
    state = changed["states"][0]
    if kind == "state_frame_bool":
        state["frame_id"] = False
    elif kind == "alias_profile_bool":
        state["aliases"][0]["profile_index"] = False
    elif kind == "profile_bool":
        changed["profiles"][0]["profile_index"] = False
    elif kind == "chain_count_bool":
        state["chain_counts"][0] = True
    elif kind == "coefficient_bool":
        state["transitions"][0]["coefficients"][0][0] = True
    elif kind == "coefficient_value":
        state["transitions"][0]["coefficients"][0][0] = 2
    elif kind == "coefficient_shape":
        state["transitions"][0]["coefficients"].pop()
    elif kind == "pair_bool":
        state["pair_graded"][0][0][0][0] = True
    elif kind == "basic_class_bool":
        state["classes"]["pair_graded"] = False
    elif kind == "source_identity":
        changed["profiles"][0]["name"] = "path6"
    elif kind == "kept_bool":
        state["kept"][0] = False
    else:
        state["aliases"].pop()
    with pytest.raises(ValueError):
        runner.check_analysis(changed)


@pytest.mark.parametrize("name", ("mean_graded", "pair_graded"))
def test_failed_basic_partition_cannot_be_given_a_quotient(aggregate, analyses, name):
    runner, _ = aggregate
    changed = {**analyses[0], "closure": dict(analyses[0]["closure"])}
    changed["closure"][name] = {**changed["closure"][name], "quotient_rows": []}
    with pytest.raises(ValueError):
        runner.check_analysis(changed)


@pytest.mark.parametrize("kind", ("fine_row", "stable_members", "stable_quotient"))
def test_k_restriction_audit_rejects_tampered_old_domain(aggregate, analyses, kind):
    runner, _ = aggregate
    changed = dict(analyses[0])
    if kind == "fine_row":
        changed["states"] = list(changed["states"])
        changed["states"][0] = json.loads(wire(changed["states"][0]))
        changed["states"][0]["transitions"][0]["coefficients"][0][0] = 2
    else:
        changed["stabilization"] = json.loads(wire(changed["stabilization"]))
        stable = changed["stabilization"]
        if kind == "stable_members":
            stable["classes"][0]["members"].append(1)
        else:
            stable["quotient_rows"][0]["transitions"][0]["target_class"] = (
                len(stable["classes"]) - 1
            )
    with pytest.raises(ValueError):
        runner.prior_bridge(changed)


def invalid_inputs():
    class Text(str):
        pass

    class Mapping(dict):
        pass

    class Sequence(list):
        pass

    base = problem()
    return [
        None,
        [],
        True,
        False,
        {},
        {"schema_version": base["schema_version"]},
        {"family": base["family"]},
        {**base, "extra": 1},
        {**base, "profile": "ferrers6"},
        Mapping(base),
        Sequence(),
        {**base, "schema_version": Text(base["schema_version"])},
        {**base, "family": Text(base["family"])},
        {Text("schema_version"): base["schema_version"], "family": base["family"]},
        {"schema_version": base["schema_version"], Text("family"): base["family"]},
        *({**base, "schema_version": v} for v in (None, True, False, 1, [], "wrong")),
        *(
            {**base, "family": v}
            for v in (None, True, False, 1, [], {}, "unknown", "qr05i_chain_pairs")
        ),
    ]


@pytest.mark.parametrize("value", invalid_inputs())
def test_strict_input_rejects_types_values_and_subclasses(executors, value):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(value)


def test_optimized_valid_outputs_and_assertion_free_schema_guards(tmp_path):
    script = r"""
import hashlib, importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1])
valid = {"schema_version":"det8-qr05l-problem-v1", "family":"qr05l_adversarial_iid"}
class Text(str):
    pass
class Mapping(dict):
    pass
class Sequence(list):
    pass
invalid = (
    True, {**valid,"extra":1}, {**valid,"family":False}, {**valid,"family":"unknown"},
    {**valid,"schema_version":1}, Mapping(valid), Sequence(),
    {**valid,"schema_version":Text(valid["schema_version"])}, {**valid,"family":Text(valid["family"])},
    {Text("schema_version"):valid["schema_version"], "family":valid["family"]},
    {"schema_version":valid["schema_version"], Text("family"):valid["family"]},
)
def native(value):
    if value is None or type(value) in (bool,int,str):
        return
    if type(value) is list:
        for item in value:
            native(item)
        return
    if type(value) is dict and all(type(key) is str for key in value):
        for item in value.values():
            native(item)
        return
    raise RuntimeError("non-native exact output")
digests = []
for number, filename in enumerate(("refinement.py", "reference_qr05l.py")):
    name = "_qr05l_optimized_test_" + str(number)
    spec = importlib.util.spec_from_file_location(name, root / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("executor unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    result = module.analyze(valid)
    native(result)
    if not 188 < result["counts"]["states"] <= 316 or result["counts"]["aliases"] != 352:
        raise RuntimeError("optimized universe differs")
    digests.append(hashlib.sha256(json.dumps(result,sort_keys=True,separators=(",", ":"),allow_nan=False).encode()).hexdigest())
    del result
    for bad in invalid:
        try:
            module.analyze(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("optimized malformed input accepted")
if digests[0] != digests[1]:
    raise RuntimeError("optimized exact outputs differ")
print(json.dumps({"valid_routes":2,"explicit_rejections":2*len(invalid)}))
"""
    completed = subprocess.run(
        [
            sys.executable,
            "-I",
            "-O",
            "-X",
            f"pycache_prefix={tmp_path / 'bytecode'}",
            "-c",
            script,
            str(HERE),
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
    )
    assert json.loads(completed.stdout) == {"valid_routes": 2, "explicit_rejections": 22}
