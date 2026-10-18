"""Independent finite-state transition, quotient, and composition checks."""

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
J_SHA = "dc8f80f40861107dd7a5ee378c9813a90c1981a3c2e7e14ee343163e9d88c333"
PROFILES = ("ferrers6", "standard_example3", "chain6", "ferrers6_fixed")
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
    return {"schema_version": "det8-qr05k-problem-v1", "family": "qr05j_recursive_iid"}


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
        private_module("_qr05k_test_direct", "closure.py"),
        private_module("_qr05k_test_reference", "reference_qr05k.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors):
    return tuple(module.analyze(problem()) for module in executors)


@pytest.fixture(scope="session")
def pinned_j():
    path = HERE.parent / "qr-05j-uncertainty-contract-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == J_SHA
    artifact = json.loads(raw)
    assert (
        json.dumps(artifact, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(artifact["suite"])
    return artifact["suite"]["analysis"]


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05k_test_aggregate", "study.py")
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
        if profile == "chain6":
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


def moments(counts, probabilities):
    assert sum(probabilities) == 1 and all(p >= 0 for p in probabilities)
    mean = [sum(p * z[q] for z, p in zip(counts, probabilities)) for q in range(4)]
    cov = [
        [
            sum(p * (z[q] - mean[q]) * (z[r] - mean[r]) for z, p in zip(counts, probabilities))
            for r in range(4)
        ]
        for q in range(4)
    ]
    return mean, cov


@pytest.fixture(scope="session")
def tower(independent):
    model, _ = independent
    states = model["states"]

    @cache
    def conditional(sid, x, y):
        state = states[sid]
        counts = [states[row["target_state"]]["chain_counts"] for row in state["transitions"]]
        probabilities = [evaluate(row["coefficients"], x, y) for row in state["transitions"]]
        return moments(counts, probabilities)

    expected = []
    for state in states:
        for rates1, rates2 in STAGES:
            direct_mean, direct_cov = conditional(
                state["state_id"], rates1[0] * rates2[0], rates1[1] * rates2[1]
            )
            probabilities = [evaluate(row["coefficients"], *rates1) for row in state["transitions"]]
            futures = [conditional(row["target_state"], *rates2) for row in state["transitions"]]
            mean = [
                sum(p * values[0][q] for p, values in zip(probabilities, futures)) for q in range(4)
            ]
            within = [
                [
                    sum(p * values[1][q][r] for p, values in zip(probabilities, futures))
                    for r in range(4)
                ]
                for q in range(4)
            ]
            between = [
                [
                    sum(
                        p * (values[0][q] - mean[q]) * (values[0][r] - mean[r])
                        for p, values in zip(probabilities, futures)
                    )
                    for r in range(4)
                ]
                for q in range(4)
            ]
            total = [[within[q][r] + between[q][r] for r in range(4)] for q in range(4)]
            assert mean == direct_mean and total == direct_cov
            expected.append((state["state_id"], rates1, rates2, mean, within, between, total))
    return expected


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
    }


def test_all_frames_aliases_deduplicated_states_and_partitions_are_independent(
    analyses, independent
):
    expected, aliases = independent
    assert len(expected["frames"]) == 2 and len(expected["profiles"]) == 4
    assert len(expected["states"]) == 188 and len(aliases) == 224
    assert sum(len(state["aliases"]) for state in expected["states"]) == 224
    for analysis in analyses:
        for key in ("frames", "profiles", "states", "partitions"):
            assert wire(analysis[key]) == wire(expected[key])
        refinement_matrix = [
            [refinement(expected["states"], a, b) for b in QUESTIONS] for a in QUESTIONS
        ]
        assert wire(analysis["partition_refinement"]) == wire(refinement_matrix)
        for classes in analysis["partitions"].values():
            assert sorted(sid for group in classes for sid in group["members"]) == list(range(188))
            assert all(set(group) == {"class_id", "key", "members"} for group in classes)
            assert all(group["members"] == sorted(set(group["members"])) for group in classes)
        assert len(analysis["partitions"]["full_record"]) == 188
        assert all(
            state["classes"]["full_record"] == state["state_id"] for state in analysis["states"]
        )


def test_all_224_aliases_and_608_prior_state_occurrences_match_without_old_mass_filter(
    analyses, pinned_j, independent
):
    _, aliases = independent
    case_profiles = (0, 0, 0, 0, 0, 1, 2, 2, 2, 3)
    for analysis in analyses:
        matched = zeros = 0
        alias_pairs = set()
        for ci, previous in enumerate(pinned_j["cases"]):
            pi = case_profiles[ci]
            profile = analysis["profiles"][pi]
            frame = analysis["frames"][profile["frame_id"]]
            assert previous["profile"] == profile["name"] and previous["past"] == profile["past"]
            assert previous["fixed"] == frame["fixed"] and previous["eligible"] == frame["eligible"]
            assert previous["density"] == frame["density"]
            for old in previous["states"]:
                matched += 1
                zeros += F(old["probability"]) == 0
                alias_pairs.add((pi, old["mask"]))
                state = analysis["states"][aliases[pi, old["mask"]]]
                assert profile["state_ids"][old["mask"]] == state["state_id"]
                assert {"profile_index": pi, "mask": old["mask"]} in state["aliases"]
                for field in (
                    "mask",
                    "kept",
                    "past",
                    "color_sizes",
                    "chain_counts",
                    "pair_graded",
                    "color_order",
                ):
                    assert wire(state[field]) == wire(old[field])
                assert wire(state["mean_graded"]) == wire(old["mean_polynomials"])
        assert matched == 608 and zeros == 98 and len(alias_pairs) == 224


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
    expected = {"verified": True, "rows": reports, "coefficient_cells": 962560}
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
        "profiles": 4,
        "aliases": len(aliases),
        "states": 188,
        "partitions": 4,
        "fine_transition_atoms": fine,
        "summary_transition_atoms": pushed,
        "transition_coefficient_cells": 16 * (fine + pushed),
        "mean_feature_cells": 188 * 64,
        "pair_feature_cells": 188 * 256,
        "expected_update_coefficient_cells": 188 * 320 * 16,
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


def determinant(matrix):
    result = F(0)
    n = len(matrix)
    for perm in permutations(range(n)):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = F(sign)
        for i, j in enumerate(perm):
            term *= matrix[i][j]
        result += term
    return result


def psd(matrix):
    assert all(matrix[0][q] == matrix[q][0] == 0 for q in range(4))
    assert all(matrix[q][r] == matrix[r][q] for q in range(4) for r in range(4))
    for size in (1, 2, 3):
        for ids in combinations((1, 2, 3), size):
            assert determinant([[matrix[q][r] for r in ids] for q in ids]) >= 0


def test_all_752_fresh_stage_covariance_towers_include_between_record_variation(tower, independent):
    assert len(tower) == 752
    _, aliases = independent
    for _, _, _, _, within, between, total in tower:
        for covariance in (within, between, total):
            psd(covariance)
        assert total == [[within[q][r] + between[q][r] for r in range(4)] for q in range(4)]
    singleton = next(row for row in tower if row[0] == aliases[0, 1] and row[1:3] == STAGES[0])
    _, _, _, mean, within, between, total = singleton
    assert mean[1] == F(1, 4)
    assert within[1][1] == F(1, 8) and between[1][1] == F(1, 16)
    assert total[1][1] == F(3, 16)
    fixed_ids = {aliases[0, 0], aliases[3, 0]}
    assert all(
        c == 0 for sid, _, _, _, _, _, cov in tower if sid in fixed_ids for row in cov for c in row
    )


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


def test_all_retained_tower_rows_match_independent_fresh_stage_outcomes(aggregate, tower):
    _, suite = aggregate
    rows = []
    for sid, rates1, rates2, mean, within, between, total in tower:
        rows.append(
            {
                "state_id": sid,
                "pair_index": STAGES.index((rates1, rates2)),
                "final_mean": list(map(str, mean)),
                "within_covariance": [list(map(str, row)) for row in within],
                "between_covariance": [list(map(str, row)) for row in between],
                "final_covariance": [list(map(str, row)) for row in total],
            }
        )
    expected = {
        "stage_rate_pairs": [
            [list(map(str, first)), list(map(str, second))] for first, second in STAGES
        ],
        "rows": rows,
        "row_count": 752,
        "verified": True,
    }
    assert wire(suite["covariance_tower"]) == wire(expected)


def test_retained_controls_audit_and_all_prior_correspondences(aggregate, independent, pinned_j):
    _, suite = aggregate
    model, aliases = independent
    controls = suite["controls"]
    star, path = (model["states"][aliases[0, s]] for s in (57, 27))
    target = model["states"][aliases[0, 41]]["classes"]["mean_graded"]
    polynomial = zero_table()
    polynomial[1][2], polynomial[2][2] = 1, -1
    assert wire(controls["star_path"]) == wire(
        {
            "profile_index": 0,
            "left_mask": 57,
            "right_mask": 27,
            "left_state": star["state_id"],
            "right_state": path["state_id"],
            "target_mask": 41,
            "target_class": target,
            "equal_mean_summary": True,
            "left_coefficients": polynomial,
            "right_coefficients": zero_table(),
            "half_probabilities": ["1/16", "0"],
        }
    )
    assert controls["positive_closure_partitions"] == ["color_order", "full_record"]
    assert controls["mean_closure"] is False
    assert (
        controls["measured_pair_closure"] is suite["analysis"]["closure"]["pair_graded"]["closed"]
    )
    assert controls["fixed_absorbing"] == [
        {"frame_id": 0, "state_id": aliases[0, 0]},
        {"frame_id": 1, "state_id": aliases[3, 0]},
    ]
    assert controls["singleton_tower"] == {
        "state_id": aliases[0, 1],
        "pair_index": 0,
        "within_variance": "1/8",
        "between_variance": "1/16",
        "final_variance": "3/16",
    }
    assert wire(controls["reused_coin"]) == wire(
        {
            "per_stage_rate": "1/2",
            "independent_two_stage_retention": "1/4",
            "reused_coin_two_stage_retention": "1/2",
            "fresh_independence_premise_satisfied": False,
            "is_counterexample_to_declared_semigroup": False,
        }
    )
    bridge = suite["prior_bridge"]
    mapping = (0, 0, 0, 0, 0, 1, 2, 2, 2, 3)
    expected = [
        {
            "case_index": ci,
            "profile_index": mapping[ci],
            "mask": state["mask"],
            "state_id": aliases[mapping[ci], state["mask"]],
        }
        for ci, case in enumerate(pinned_j["cases"])
        for state in case["states"]
    ]
    assert wire(bridge["state_correspondence"]) == wire(expected)
    assert bridge["verified"] is True and bridge["source_gate"] == "QR-05J"
    assert bridge["representative_cases"] == [0, 5, 6, 9]
    assert bridge["matched_aliases"] == 224 and bridge["matched_state_occurrences"] == 608
    assert bridge["zero_first_mass_occurrences_retained"] == 98
    assert (
        bridge["old_history_partitions_reinterpreted"] is bridge["old_design_masses_used"] is False
    )
    counts = suite["analysis"]["counts"]
    assert wire(suite["audit"]) == wire(
        {
            "verified": True,
            "rates": [[str(x), str(y)] for x, y in POINTS],
            "rate_points": 22,
            "evaluated_fine_and_pushed_atoms": 22
            * (counts["fine_transition_atoms"] + counts["summary_transition_atoms"]),
            "evaluated_quotient_atoms": 22 * counts["quotient_transition_atoms"],
            "deterministic_corner_rows": 188 * 4,
            "expected_feature_coefficient_cells": 962560,
            "semigroup_coefficient_cells": counts["semigroup_coefficient_cells"],
        }
    )
    for flag in (
        "source_aliases_used_as_weights",
        "old_current_design_tokens_in_summary_keys",
        "expected_update_implies_stochastic_closure",
        "failed_partition_has_quotient",
        "general_pair_summary_closure_established",
        "deterministic_mask_update_established",
        "adaptive_rate_composition_tested",
        "correlated_stage_composition_claimed",
        "observation_composition_is_physical_time",
        "positive_definiteness_required",
        "covariance_regularization_added",
        "minimal_summary_established",
    ):
        assert suite[flag] is False


@pytest.mark.parametrize(
    "kind",
    (
        "coefficient_bool",
        "coefficient_value",
        "coefficient_shape",
        "transition_target",
        "pushed_coefficient",
        "pair_type",
        "alias",
    ),
)
def test_runner_rejects_copied_state_and_transition_corruption(aggregate, analyses, kind):
    runner, _ = aggregate
    changed = dict(analyses[0])
    changed["states"] = list(changed["states"])
    first = json.loads(wire(changed["states"][0]))
    changed["states"][0] = first
    if kind == "coefficient_bool":
        first["transitions"][0]["coefficients"][0][0] = True
    elif kind == "coefficient_value":
        first["transitions"][0]["coefficients"][0][0] = 2
    elif kind == "coefficient_shape":
        first["transitions"][0]["coefficients"].pop()
    elif kind == "transition_target":
        first["transitions"][0]["target_state"] = 1
    elif kind == "pushed_coefficient":
        first["summary_laws"]["mean_graded"][0]["coefficients"][0][0] = 2
    elif kind == "pair_type":
        first["pair_graded"][0][0][0][0] = True
    else:
        first["aliases"].pop()
    with pytest.raises(ValueError):
        runner.check_analysis(changed)


@pytest.mark.parametrize(
    "field,value", (("quotient_rows", []), ("semigroup", {"verified": True}), ("closed", True))
)
def test_failed_partition_cannot_be_given_a_fabricated_quotient(aggregate, analyses, field, value):
    runner, _ = aggregate
    changed = dict(analyses[0])
    changed["closure"] = dict(changed["closure"])
    changed["closure"]["mean_graded"] = dict(changed["closure"]["mean_graded"])
    changed["closure"]["mean_graded"][field] = value
    with pytest.raises(ValueError, match="failed partition"):
        runner.check_analysis(changed)


def test_semigroup_certificate_corruption_is_rejected(aggregate, analyses):
    runner, _ = aggregate
    changed = dict(analyses[0])
    changed["closure"] = dict(changed["closure"])
    full = json.loads(wire(changed["closure"]["full_record"]))
    changed["closure"]["full_record"] = full
    full["semigroup"]["totals"]["max_abs_residual"] = 1
    with pytest.raises(ValueError, match="quotient/composition"):
        runner.check_analysis(changed)


@pytest.mark.parametrize(
    "component", ("within_covariance", "between_covariance", "final_covariance")
)
def test_singleton_tower_component_corruption_cannot_pass_controls(
    aggregate, analyses, independent, component
):
    runner, suite = aggregate
    _, aliases = independent
    changed = dict(suite["covariance_tower"])
    changed["rows"] = list(changed["rows"])
    index = next(
        i
        for i, row in enumerate(changed["rows"])
        if row["state_id"] == aliases[0, 1] and row["pair_index"] == 0
    )
    row = json.loads(wire(changed["rows"][index]))
    row[component][1][1] = "0"
    changed["rows"][index] = row
    with pytest.raises(ValueError, match="singleton covariance"):
        runner.controls(analyses[0], changed)


def test_prior_bridge_rejects_corrupted_source_identity(aggregate, analyses):
    runner, _ = aggregate
    changed = dict(analyses[0])
    changed["profiles"] = list(changed["profiles"])
    changed["profiles"][0] = dict(changed["profiles"][0])
    changed["profiles"][0]["name"] = "not_the_recorded_source"
    with pytest.raises(ValueError, match="J source identity"):
        runner.prior_bridge(changed)


def test_consistent_fine_state_id_permutation_violates_first_registration(aggregate, analyses):
    runner, _ = aggregate
    changed = json.loads(wire(analyses[0]))

    def renamed(sid):
        return 1 - sid if sid in (0, 1) else sid

    for profile in changed["profiles"]:
        profile["state_ids"] = [renamed(sid) for sid in profile["state_ids"]]
    for state in changed["states"]:
        state["state_id"] = renamed(state["state_id"])
        for row in state["transitions"]:
            row["target_state"] = renamed(row["target_state"])
        state["transitions"].sort(key=lambda row: row["target_state"])
    changed["states"].sort(key=lambda state: state["state_id"])
    for groups in changed["partitions"].values():
        for group in groups:
            group["members"] = sorted(renamed(sid) for sid in group["members"])
    for item in changed["closure"].values():
        if item["first_collision"] is not None:
            for field in ("left_state", "right_state"):
                item["first_collision"][field] = renamed(item["first_collision"][field])
        if item["quotient_rows"] is not None:
            for row in item["quotient_rows"]:
                row["representative_state"] = renamed(row["representative_state"])
    for row in changed["expected_updates"]["rows"]:
        row["state_id"] = renamed(row["state_id"])
    changed["expected_updates"]["rows"].sort(key=lambda row: row["state_id"])
    # Fine-state references remain consistent; class IDs are separate labels.
    for profile in changed["profiles"]:
        for mask, sid in enumerate(profile["state_ids"]):
            assert changed["states"][sid]["mask"] == mask
            assert {"profile_index": profile["profile_index"], "mask": mask} in changed["states"][
                sid
            ]["aliases"]
    with pytest.raises(ValueError, match="first-occurrence state registration"):
        runner.check_analysis(changed)


@pytest.mark.parametrize("field", ("state_frame", "alias_profile", "chain_count", "profile_index"))
def test_audit_rejects_boolean_substitutions_for_native_integer_metadata(
    aggregate, analyses, field
):
    runner, _ = aggregate
    changed = dict(analyses[0])
    changed["states"] = list(changed["states"])
    changed["states"][0] = json.loads(wire(changed["states"][0]))
    changed["profiles"] = list(changed["profiles"])
    changed["profiles"][0] = dict(changed["profiles"][0])
    if field == "state_frame":
        changed["states"][0]["frame_id"] = False
    elif field == "alias_profile":
        changed["states"][0]["aliases"][0]["profile_index"] = False
    elif field == "chain_count":
        changed["states"][0]["chain_counts"][0] = True
    else:
        changed["profiles"][0]["profile_index"] = False
    with pytest.raises(ValueError):
        runner.check_analysis(changed)


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
valid = {"schema_version":"det8-qr05k-problem-v1", "family":"qr05j_recursive_iid"}
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
for number, filename in enumerate(("closure.py", "reference_qr05k.py")):
    name = "_qr05k_optimized_test_" + str(number)
    spec = importlib.util.spec_from_file_location(name, root / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("executor unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    result = module.analyze(valid)
    native(result)
    if result["counts"]["states"] != 188 or result["counts"]["aliases"] != 224:
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
