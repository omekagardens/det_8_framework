"""Independent N domain tests, carrying selected local M/L test utilities.

No previous executor is imported. Sources, observed chains, motifs, kernels,
and partition fibers are rebuilt before comparison with pinned M JSON.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from functools import cache
from itertools import combinations, product
from math import comb
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
F = Fraction
M_SHA = "79cb515022fdb3bb2c918a469c1ac5ffdf98a6dd18cdd289f8030fc7a38f1543"
BASE_NAMES = ("ferrers6", "standard_example3", "chain6", "ferrers6_fixed", "path6", "cycle4_edge")
QUESTIONS = ("pair_graded", "motif_pair")
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


def problem():
    return {"schema_version": "det8-qr05n-problem-v1", "family": "qr05n_layered_iid"}


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
        private_module("_qr05n_test_direct", "portability.py"),
        private_module("_qr05n_test_reference", "reference_qr05n.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors):
    return tuple(module.analyze(problem()) for module in executors)


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05n_test_aggregate", "study.py")
    return runner, runner.run_suite()


@pytest.fixture(scope="session")
def pinned_m():
    path = HERE.parent / "qr-05m-observable-realization-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == M_SHA
    artifact = json.loads(raw)
    assert (
        json.dumps(artifact, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(artifact["suite"])
    return artifact["suite"]


def native(value):
    if value is None or type(value) in (bool, int, str):
        if type(value) is int:
            assert abs(value).bit_length() <= 4096
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


def zero_table():
    return [[0] * 4 for _ in range(4)]


@cache
def kernel(odd, even, o, e):
    result = zero_table()
    for a in range(odd - o + 1):
        for b in range(even - e + 1):
            result[o + a][e + b] = (-1) ** (a + b) * comb(odd - o, a) * comb(even - e, b)
    return result


@cache
def evaluate_table(table, x, y):
    return sum(
        (F(c) * x**i * y**j for i, row in enumerate(table) for j, c in enumerate(row) if c), F(0)
    )


def evaluate(table, x, y):
    return evaluate_table(tuple(tuple(row) for row in table), x, y)


@cache
def direct_probability(odd, even, o, e, x, y):
    return x**o * (1 - x) ** (odd - o) * y**e * (1 - y) ** (even - e)


@cache
def submasks(mask):
    return [m for m in range(mask + 1) if m & mask == m]


@cache
def source(pi):
    edges = {(0, v) for v in range(1, 8)} | {(v, 7) for v in range(7)}
    if pi >= 6:
        reverse = pi >= 518
        incidence = pi - (518 if reverse else 6)
        name = f"layered_{'eo' if reverse else 'oe'}_{incidence:03d}"
        for i, j in product(range(3), repeat=2):
            if incidence & (1 << (3 * i + j)):
                odd, even = 2 * i + 1, 2 * j + 2
                edges.add((even, odd) if reverse else (odd, even))
    else:
        name = BASE_NAMES[pi]
        if pi == 2:
            edges |= set(combinations(range(1, 7), 2))
        elif pi == 4:
            edges |= {(1, 2), (1, 4), (3, 4), (3, 6), (5, 6)}
        elif pi == 5:
            edges |= {(1, 4), (1, 6), (3, 4), (3, 6), (2, 5)}
        else:
            edges |= {
                (i + 1, j + 4)
                for i, j in product(range(3), repeat=2)
                if (i != j if pi == 1 else i <= j)
            }
    fixed = [0, 3, 7] if pi == 3 else [0, 7]
    eligible = [v for v in range(1, 7) if v not in fixed]
    past = [[a for a in range(8) if (a, b) in edges] for b in range(8)]
    return name, past, fixed, eligible


def motif_supports(kept, past, eligible):
    relation = {(kept[i], b) for b, before in zip(kept, past, strict=True) for i in before}
    result = []
    for four in combinations(sorted(set(kept) & set(eligible)), 4):
        odd, even = [v for v in four if v % 2], [v for v in four if not v % 2]
        if len(odd) != 2 or len(even) != 2:
            continue
        induced = {(a, b) for a, b in relation if a in four and b in four}
        if induced == set(product(odd, even)) or induced == set(product(even, odd)):
            result.append(list(four))
    return result


def features(kept, past, eligible):
    relation = {(kept[i], b) for b, before in zip(kept, past, strict=True) for i in before}
    eligible = set(eligible)
    chains = [[] for _ in range(4)]
    d = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for q in range(4):
        for vertices in combinations([v for v in kept if v not in (0, 7)], q):
            if not all((0, v) in relation and (v, 7) in relation for v in vertices):
                continue
            if (0, 7) not in relation or not all(
                (a, b) in relation or (b, a) in relation for a, b in combinations(vertices, 2)
            ):
                continue
            support = frozenset(vertices) & eligible
            o = sum(v % 2 for v in support)
            d[q][o][len(support) - o] += 1
            chains[q].append(support)
    b = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for q, r in product(range(4), repeat=2):
        for left in chains[q]:
            for right in chains[r]:
                union = left | right
                o = sum(v % 2 for v in union)
                b[q][r][o][len(union) - o] += 1
    motifs = motif_supports(kept, past, eligible)
    odd = sum(v % 2 for v in kept if v in eligible)
    return {
        "chain_counts": list(map(len, chains)),
        "mean_graded": d,
        "pair_graded": b,
        "motif_supports": motifs,
        "motif_count": len(motifs),
        "color_sizes": [odd, sum(v in eligible for v in kept) - odd],
    }


@pytest.fixture(scope="session")
def independent():
    frames, profiles, states, aliases = [], [], [], {}
    frame_ids, state_ids = {}, {}
    for pi in range(1030):
        name, original, fixed, eligible = source(pi)
        frame = ["12", fixed, eligible]
        encoded = wire(frame)
        if encoded not in frame_ids:
            frame_ids[encoded] = len(frames)
            frames.append(
                {"frame_id": len(frames), "density": "12", "fixed": fixed, "eligible": eligible}
            )
        fi = frame_ids[encoded]
        profile_ids = []
        for mask in range(1 << len(eligible)):
            kept = sorted(fixed + [v for bit, v in enumerate(eligible) if mask & (1 << bit)])
            past = [[i for i, a in enumerate(kept) if a in original[b]] for b in kept]
            key = (fi, tuple(kept), tuple(tuple(row) for row in past))
            if key not in state_ids:
                sid = len(states)
                state_ids[key] = sid
                states.append(
                    {
                        "state_id": sid,
                        "frame_id": fi,
                        "mask": mask,
                        "kept": kept,
                        "past": past,
                        "aliases": [],
                        **features(kept, past, eligible),
                    }
                )
            sid = state_ids[key]
            states[sid]["aliases"].append({"profile_index": pi, "mask": mask})
            aliases[pi, mask] = sid
            profile_ids.append(sid)
        profiles.append(
            {
                "profile_index": pi,
                "name": name,
                "frame_id": fi,
                "past": original,
                "state_ids": profile_ids,
            }
        )
    partitions = {name: [] for name in QUESTIONS}
    registry = {name: {} for name in QUESTIONS}
    for state in states:
        frame = frames[state["frame_id"]]
        public = [frame["density"], frame["fixed"], frame["eligible"]]
        keys = {
            "pair_graded": [public, state["pair_graded"]],
            "motif_pair": [public, state["pair_graded"], state["motif_count"]],
        }
        state["classes"] = {}
        for name, key in keys.items():
            encoded = wire(key)
            cid = registry[name].setdefault(encoded, len(registry[name]))
            if cid == len(partitions[name]):
                partitions[name].append({"class_id": cid, "key": key, "members": []})
            partitions[name][cid]["members"].append(state["state_id"])
            state["classes"][name] = cid
    for state in states:
        pi = state["aliases"][0]["profile_index"]
        odd, even = state["color_sizes"]
        state["transitions"] = sorted(
            [
                {
                    "target_state": aliases[pi, mask],
                    "coefficients": kernel(odd, even, *states[aliases[pi, mask]]["color_sizes"]),
                }
                for mask in submasks(state["mask"])
            ],
            key=lambda row: row["target_state"],
        )
        state["summary_laws"] = {}
        for name in QUESTIONS:
            grouped = {}
            for atom in state["transitions"]:
                cid = states[atom["target_state"]]["classes"][name]
                table = grouped.setdefault(cid, zero_table())
                for i, j in product(range(4), repeat=2):
                    table[i][j] += atom["coefficients"][i][j]
            state["summary_laws"][name] = [
                {"target_class": cid, "coefficients": table}
                for cid, table in sorted(grouped.items())
            ]
    return {
        "frames": frames,
        "profiles": profiles,
        "states": states,
        "partitions": partitions,
    }, aliases


def first_difference(left, right):
    a = {row["target_class"]: row["coefficients"] for row in left}
    b = {row["target_class"]: row["coefficients"] for row in right}
    for target in sorted(a.keys() | b.keys()):
        x, y = a.get(target, zero_table()), b.get(target, zero_table())
        if x != y:
            return target, x, y
    return None


def composition(rows):
    reports = []
    sparse = {
        row["class_id"]: [
            (
                atom["target_class"],
                [
                    (4 * i + j, c)
                    for i, line in enumerate(atom["coefficients"])
                    for j, c in enumerate(line)
                    if c
                ],
            )
            for atom in row["transitions"]
        ]
        for row in rows
    }
    for first in rows:
        accumulated, paths = {}, 0
        for mid, left in sparse[first["class_id"]]:
            for target, right in sparse[mid]:
                paths += 1
                table = accumulated.setdefault(target, [0] * 256)
                for i, a in left:
                    for j, b in right:
                        table[16 * i + j] += a * b
        assert set(accumulated) == {atom["target_class"] for atom in first["transitions"]}
        for target, cells in sparse[first["class_id"]]:
            expected = [0] * 256
            for i, value in cells:
                expected[17 * i] = value
            assert accumulated[target] == expected
        reports.append(
            {
                "class_id": first["class_id"],
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
            key: sum(row[key] for row in reports)
            for key in (
                "transition_pairs",
                "intermediate_paths",
                "coefficient_cells",
                "max_abs_residual",
            )
        },
    }


@pytest.fixture(scope="session")
def expected_closure(independent):
    model = independent[0]
    result = {}
    for name in QUESTIONS:
        failure = None
        for group in model["partitions"][name]:
            first = group["members"][0]
            left = model["states"][first]["summary_laws"][name]
            for sid in group["members"][1:]:
                difference = first_difference(left, model["states"][sid]["summary_laws"][name])
                if difference is not None:
                    target, a, b = difference
                    failure = {
                        "class_id": group["class_id"],
                        "left_state": first,
                        "right_state": sid,
                        "target_class": target,
                        "left_coefficients": a,
                        "right_coefficients": b,
                    }
                    break
            if failure is not None:
                break
        quotient = (
            []
            if failure
            else [
                {
                    "class_id": group["class_id"],
                    "representative_state": group["members"][0],
                    "transitions": model["states"][group["members"][0]]["summary_laws"][name],
                }
                for group in model["partitions"][name]
            ]
        )
        result[name] = {
            "closed": failure is None,
            "first_collision": failure,
            "quotient_rows": quotient,
            "semigroup": None if failure else composition(quotient),
        }
    return result


def test_complete_exact_native_outputs_agree_and_remain_slim(analyses):
    assert wire(analyses[0]) == wire(analyses[1])
    encoded = wire(analyses[0])
    assert len(encoded.encode()) < 64 * 1024 * 1024
    assert wire(json.loads(encoded)) == encoded
    assert set(analyses[0]) == {
        "frames",
        "profiles",
        "states",
        "partitions",
        "closure",
        "expected_updates",
        "motif_expected_update",
        "counts",
    }
    for key in ("stabilization", "color_order", "trace_audit", "covariance_tower", "observable"):
        assert key not in analyses[0]


def test_independent_source_numbering_alias_registration_and_complete_state_features(
    analyses, independent
):
    expected, aliases = independent
    assert len(expected["profiles"]) == 1030 and len(expected["frames"]) == 2
    assert len(expected["states"]) == 2470 and len(expected["states"]) <= 2579
    assert len(aliases) == 65888 == 352 + 1024 * 64
    assert sum(len(state["aliases"]) for state in expected["states"]) == 65888
    for analysis in analyses:
        for key in ("frames", "profiles", "states", "partitions"):
            assert wire(analysis[key]) == wire(expected[key])
        assert set(analysis["partitions"]) == set(QUESTIONS)
        for groups in analysis["partitions"].values():
            assert sorted(sid for group in groups for sid in group["members"]) == list(range(2470))
            assert all(group["members"] == sorted(set(group["members"])) for group in groups)
    pure = {sid for profile in expected["profiles"][6:] for sid in profile["state_ids"]}
    count = sum(
        comb(3, o) * comb(3, e) * (2 * 2 ** (o * e) - 1) for o, e in product(range(4), repeat=2)
    )
    atoms = sum(
        comb(3, o) * comb(3, e) * (2 * 2 ** (o * e) - 1) * 2 ** (o + e)
        for o, e in product(range(4), repeat=2)
    )
    assert len(pure) == count == 2322
    assert sum(len(expected["states"][sid]["transitions"]) for sid in pure) == atoms == 96929
    assert len(set(range(2470)) - pure) == 148


def test_all_incidence_bits_are_reversed_without_transposition(analyses):
    for analysis in analyses:
        profiles = analysis["profiles"]
        for incidence in range(512):
            forward, reverse = profiles[6 + incidence], profiles[518 + incidence]
            assert forward["name"] == f"layered_oe_{incidence:03d}"
            assert reverse["name"] == f"layered_eo_{incidence:03d}"
            edges = {(a, b) for b in range(1, 7) for a in forward["past"][b] if 0 < a < 7}
            backwards = {(a, b) for b in range(1, 7) for a in reverse["past"][b] if 0 < a < 7}
            expected = {
                (2 * i + 1, 2 * j + 2)
                for i, j in product(range(3), repeat=2)
                if incidence & (1 << (3 * i + j))
            }
            assert edges == expected and backwards == {(b, a) for a, b in expected}
            assert len(edges) == incidence.bit_count()
            for profile in (forward, reverse):
                relation = {(a, b) for b, row in enumerate(profile["past"]) for a in row}
                assert all(a != b for a, b in relation)
                assert all((a, d) in relation for a, b in relation for c, d in relation if b == c)


def test_descending_ids_full_motif_multiplicity_empty_aliases_and_fixed_marks(
    analyses, independent
):
    _, aliases = independent
    for analysis in analyses:
        states = analysis["states"]
        for pi in (14, 526):
            full, edge = states[aliases[pi, 63]], states[aliases[pi, 6]]
            assert full["chain_counts"] == [1, 6, 1, 0]
            assert edge["chain_counts"] == [1, 2, 1, 0]
            assert edge["kept"] == [0, 2, 3, 7]
            assert full["mean_graded"][2][1][1] == 1
        descending = states[aliases[14, 6]]
        assert 2 in descending["past"][1]
        assert 1 not in descending["past"][2]
        for pi in (517, 1029):
            full = states[aliases[pi, 63]]
            supports = sorted(
                [
                    sorted((*o, *e))
                    for o in combinations((1, 3, 5), 2)
                    for e in combinations((2, 4, 6), 2)
                ]
            )
            assert full["chain_counts"] == [1, 6, 9, 0]
            assert full["motif_supports"] == supports and full["motif_count"] == 9
            expectation = analysis["motif_expected_update"]["rows"][full["state_id"]]
            target = zero_table()
            target[2][2] = 9
            assert expectation["coefficients"] == expectation["expected_coefficients"] == target
        assert analysis["profiles"][6]["state_ids"] == analysis["profiles"][518]["state_ids"]
        fixed0, fixed3 = states[aliases[0, 0]], states[aliases[3, 0]]
        assert fixed0["state_id"] != fixed3["state_id"]
        assert fixed0["chain_counts"] == [1, 0, 0, 0]
        assert fixed3["chain_counts"] == [1, 1, 0, 0]
        assert fixed3["mean_graded"][1][0][0] == 1
        assert fixed3["pair_graded"][1][1][0][0] == 1
        assert fixed3["color_sizes"] == [0, 0]
        assert len(fixed0["aliases"]) == 1029 and len(fixed0["transitions"]) == 1
        assert fixed0["transitions"][0]["coefficients"][0][0] == 1
        assert all(
            3 not in support
            for state in states
            if state["frame_id"] == 1
            for support in state["motif_supports"]
        )


def test_every_fine_kernel_coefficient_and_boundary_rate_is_explicit(independent):
    states = independent[0]["states"]
    unique = {
        wire(kernel(O, E, o, e))
        for O, E in product(range(4), repeat=2)
        for o in range(O + 1)
        for e in range(E + 1)
    }
    assert len(unique) == 100
    observed = set()
    for state in states:
        rows = state["transitions"]
        odd, even = state["color_sizes"]
        assert len(rows) == 2 ** state["mask"].bit_count()
        assert [row["target_state"] for row in rows] == sorted(
            {row["target_state"] for row in rows}
        )
        assert all(
            sum(row["coefficients"][i][j] for row in rows) == int(i == j == 0)
            for i, j in product(range(4), repeat=2)
        )
        for row in rows:
            target = states[row["target_state"]]
            o, e = target["color_sizes"]
            assert target["frame_id"] == state["frame_id"] and set(target["kept"]) <= set(
                state["kept"]
            )
            observed.add(wire(row["coefficients"]))
            assert all(
                c == 0
                for i, line in enumerate(row["coefficients"])
                for j, c in enumerate(line)
                if i > odd or j > even
            )
            for x, y in POINTS:
                assert evaluate(row["coefficients"], x, y) == direct_probability(
                    odd, even, o, e, x, y
                )
        for x, y in product((F(0), F(1)), repeat=2):
            positive = [row["target_state"] for row in rows if evaluate(row["coefficients"], x, y)]
            assert len(positive) == 1
            if x == y == 1:
                assert positive == [state["state_id"]]
            if x == y == 0:
                assert states[positive[0]]["mask"] == 0
    assert observed == unique


def feature_vector(state):
    return [v for table in state["mean_graded"] for row in table for v in row] + [
        v for matrix in state["pair_graded"] for table in matrix for row in table for v in row
    ]


@pytest.fixture(scope="session")
def expected_updates(independent):
    states = independent[0]["states"]
    vectors = [feature_vector(state) for state in states]
    sparse = [[(i, value) for i, value in enumerate(vector) if value] for vector in vectors]
    reports, motif_reports = [], []
    for state in states:
        actual = [[0] * 16 for _ in range(320)]
        motif = zero_table()
        for atom in state["transitions"]:
            cells = [
                (4 * i + j, c)
                for i, row in enumerate(atom["coefficients"])
                for j, c in enumerate(row)
                if c
            ]
            for index, value in sparse[atom["target_state"]]:
                for position, coefficient in cells:
                    actual[index][position] += value * coefficient
            for position, coefficient in cells:
                motif[position // 4][position % 4] += (
                    coefficient * states[atom["target_state"]]["motif_count"]
                )
        for index, value in enumerate(vectors[state["state_id"]]):
            expected = [0] * 16
            expected[index % 16] = value
            assert actual[index] == expected
        expected = zero_table()
        expected[2][2] = state["motif_count"]
        assert motif == expected
        reports.append(
            {
                "state_id": state["state_id"],
                "mean_features": 64,
                "pair_features": 256,
                "coefficient_cells": 5120,
                "max_abs_residual": 0,
            }
        )
        motif_reports.append(
            {
                "state_id": state["state_id"],
                "coefficients": motif,
                "expected_coefficients": expected,
                "max_abs_residual": 0,
            }
        )
    return (
        {"verified": True, "rows": reports, "coefficient_cells": 5120 * len(states)},
        {"verified": True, "rows": motif_reports, "coefficient_cells": 16 * len(states)},
    )


def test_all_mean_pair_and_motif_updates_coefficientwise(analyses, expected_updates):
    expected, motif = expected_updates
    for analysis in analyses:
        assert wire(analysis["expected_updates"]) == wire(expected)
        assert wire(analysis["motif_expected_update"]) == wire(motif)


def test_all_pair_moments_against_induced_count_outcome_polynomials(independent):
    states = independent[0]["states"]
    for state in states:
        raw = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        for atom in state["transitions"]:
            counts = states[atom["target_state"]]["chain_counts"]
            cells = [
                (i, j, c)
                for i, row in enumerate(atom["coefficients"])
                for j, c in enumerate(row)
                if c
            ]
            for q, r in product(range(4), repeat=2):
                value = counts[q] * counts[r]
                if value:
                    for i, j, coefficient in cells:
                        raw[q][r][i][j] += value * coefficient
        assert raw == state["pair_graded"]
        assert raw[0] == state["mean_graded"]


def test_complete_partition_laws_first_failure_order_and_conditional_quotients(
    analyses, independent, expected_closure
):
    states = independent[0]["states"]
    assert expected_closure["pair_graded"]["closed"] is False
    for analysis in analyses:
        assert wire(analysis["closure"]) == wire(expected_closure)
    for name, decision in expected_closure.items():
        if decision["closed"]:
            assert decision["first_collision"] is None
            assert decision["semigroup"]["verified"] is True
            for group, row in zip(
                independent[0]["partitions"][name], decision["quotient_rows"], strict=True
            ):
                assert row["representative_state"] == group["members"][0]
                assert all(
                    states[sid]["summary_laws"][name] == row["transitions"]
                    for sid in group["members"]
                )
        else:
            assert decision["quotient_rows"] == [] and decision["semigroup"] is None
            collision = decision["first_collision"]
            left, right = states[collision["left_state"]], states[collision["right_state"]]
            assert left["classes"][name] == right["classes"][name] == collision["class_id"]
            assert collision["left_coefficients"] != collision["right_coefficients"]
            assert any(
                evaluate(collision["left_coefficients"], x, y)
                != evaluate(collision["right_coefficients"], x, y)
                for x, y in POINTS[:16]
            )
        for state in states:
            assert all(
                sum(row["coefficients"][i][j] for row in state["summary_laws"][name])
                == int(i == j == 0)
                for i, j in product(range(4), repeat=2)
            )


def test_inventory_uses_only_retained_data_and_branch_appropriate_certificates(
    analyses, independent, expected_closure
):
    model, aliases = independent
    states = model["states"]
    fine = sum(len(state["transitions"]) for state in states)
    pushed = sum(len(row) for state in states for row in state["summary_laws"].values())
    closed = [decision for decision in expected_closure.values() if decision["closed"]]
    expected = {
        "frames": 2,
        "profiles": 1030,
        "aliases": len(aliases),
        "states": len(states),
        "partitions": 2,
        "fine_transition_atoms": fine,
        "summary_transition_atoms": pushed,
        "transition_coefficient_cells": 16 * (fine + pushed),
        "mean_feature_cells": len(states) * 64,
        "pair_feature_cells": len(states) * 256,
        "motif_support_occurrences": sum(state["motif_count"] for state in states),
        "motif_positive_states": sum(state["motif_count"] > 0 for state in states),
        "max_motif_count": max(state["motif_count"] for state in states),
        "expected_update_coefficient_cells": len(states) * 5120,
        "motif_expected_update_coefficient_cells": len(states) * 16,
        "closed_partitions": len(closed),
        "quotient_transition_atoms": sum(
            len(row["transitions"]) for decision in closed for row in decision["quotient_rows"]
        ),
        "semigroup_intermediate_paths": sum(
            decision["semigroup"]["totals"]["intermediate_paths"] for decision in closed
        ),
        "semigroup_coefficient_cells": sum(
            decision["semigroup"]["totals"]["coefficient_cells"] for decision in closed
        ),
    }
    assert len(expected) == 19 and fine == 99180 and fine <= 100393
    assert expected["max_motif_count"] == 9
    for analysis in analyses:
        assert wire(analysis["counts"]) == wire(expected)


@pytest.fixture(scope="session")
def restricted_m(independent, pinned_m):
    model = independent[0]
    old = pinned_m["analysis"]
    states = model["states"]
    old_candidate = old["observable"]
    maps = {}
    for name in QUESTIONS:
        groups = (
            old["partitions"]["pair_graded"] if name == "pair_graded" else old_candidate["classes"]
        )
        mapping = {}
        for group in groups:
            images = {states[sid]["classes"][name] for sid in group["members"]}
            assert len(images) == 1
            target = images.pop()
            mapping[group["class_id"]] = target
            assert [
                sid for sid in model["partitions"][name][target]["members"] if sid < 257
            ] == group["members"]
        assert len(set(mapping.values())) == len(mapping)
        maps[name] = mapping
    mapping = maps["motif_pair"]
    inverse = {new: old for old, new in mapping.items()}
    rows = []
    for group in old_candidate["classes"]:
        members = group["members"]
        representative = members[0]
        first = states[representative]["summary_laws"]["motif_pair"]
        assert all(states[sid]["summary_laws"]["motif_pair"] == first for sid in members)
        assert all(atom["target_class"] in inverse for atom in first)
        rows.append(
            {
                "class_id": group["class_id"],
                "representative_state": representative,
                "transitions": sorted(
                    [{**atom, "target_class": inverse[atom["target_class"]]} for atom in first],
                    key=lambda atom: atom["target_class"],
                ),
            }
        )
    assert wire(rows) == wire(old_candidate["quotient_rows"])
    semigroup = composition(rows)
    assert wire(semigroup) == wire(old_candidate["semigroup"])
    return {"maps": maps, "quotient_rows": rows, "semigroup": semigroup}


def test_exact_selected_m_prefix_and_motif_evidence_preserved(analyses, pinned_m):
    old = pinned_m["analysis"]
    old_fields = (
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
    for analysis in analyses:
        assert wire(analysis["frames"]) == wire(old["frames"])
        assert wire(analysis["profiles"][:6]) == wire(old["profiles"])
        for sid, (state, before) in enumerate(
            zip(analysis["states"][:257], old["states"], strict=True)
        ):
            for key in old_fields:
                assert wire(state[key]) == wire(before[key])
            aliases = [alias for alias in state["aliases"] if alias["profile_index"] < 6]
            assert wire(aliases) == wire(before["aliases"])
            assert all(atom["target_state"] < 257 for atom in state["transitions"])
            feature = old["observable"]["states"][sid]
            assert wire(state["motif_supports"]) == wire(feature["motif_supports"])
            assert state["motif_count"] == feature["motif_count"]
            assert state["classes"]["pair_graded"] == before["classes"]["pair_graded"]
            assert state["classes"]["motif_pair"] == old["observable"]["state_classes"][sid]
            assert wire(state["summary_laws"]["pair_graded"]) == wire(
                before["summary_laws"]["pair_graded"]
            )
            assert wire(state["summary_laws"]["motif_pair"]) == wire(
                old["observable"]["pushforward_rows"][sid]["transitions"]
            )
        assert wire(analysis["expected_updates"]["rows"][:257]) == wire(
            old["expected_updates"]["rows"]
        )
        assert wire(analysis["motif_expected_update"]["rows"][:257]) == wire(
            old["observable"]["expected_update"]["rows"]
        )
        assert (
            sum(
                alias["profile_index"] >= 6
                for state in analysis["states"][:257]
                for alias in state["aliases"]
            )
            > 0
        )


def test_m_actual_membership_maps_and_restricted_quotient_survive_any_global_outcome(
    analyses, pinned_m, restricted_m
):
    old = pinned_m["analysis"]
    for analysis in analyses:
        for name, mapping in restricted_m["maps"].items():
            old_groups = (
                old["partitions"]["pair_graded"]
                if name == "pair_graded"
                else old["observable"]["classes"]
            )
            for group in old_groups:
                new = analysis["partitions"][name][mapping[group["class_id"]]]
                assert [sid for sid in new["members"] if sid < 257] == group["members"]
                assert all(
                    analysis["states"][sid]["classes"][name] == new["class_id"]
                    for sid in group["members"]
                )
                if name == "pair_graded":
                    assert wire(new["key"]) == wire(group["key"])
                else:
                    before = old["states"][group["members"][0]]
                    frame = old["frames"][before["frame_id"]]
                    expected_key = [
                        [frame["density"], frame["fixed"], frame["eligible"]],
                        before["pair_graded"],
                        old["observable"]["states"][before["state_id"]]["motif_count"],
                    ]
                    assert wire(new["key"]) == wire(expected_key)
        assert len(restricted_m["quotient_rows"]) == 110
        global_decision = analysis["closure"]["motif_pair"]
        if not global_decision["closed"]:
            assert global_decision["first_collision"] is not None
            assert global_decision["quotient_rows"] == [] and global_decision["semigroup"] is None
        else:
            mapping = restricted_m["maps"]["motif_pair"]
            inverse = {new: before for before, new in mapping.items()}
            for before, new in mapping.items():
                row = global_decision["quotient_rows"][new]
                assert all(atom["target_class"] in inverse for atom in row["transitions"])
                transported = {
                    "class_id": before,
                    "representative_state": row["representative_state"],
                    "transitions": sorted(
                        [
                            {**atom, "target_class": inverse[atom["target_class"]]}
                            for atom in row["transitions"]
                        ],
                        key=lambda atom: atom["target_class"],
                    ),
                }
                assert wire(transported) == wire(restricted_m["quotient_rows"][before])


def selected_mass(state, predicate):
    total = zero_table()
    for atom in state["transitions"]:
        if predicate(atom["target_state"]):
            for i, j in product(range(4), repeat=2):
                total[i][j] += atom["coefficients"][i][j]
    return total


def test_selected_old_path_cycle_obstruction_not_hidden_by_new_aliases(analyses, independent):
    _, aliases = independent
    for analysis in analyses:
        states = analysis["states"]
        path, cycle = (states[aliases[pi, 63]] for pi in (4, 5))
        target = states[aliases[5, 45]]["classes"]["pair_graded"]
        assert path["pair_graded"] == cycle["pair_graded"]
        assert path["classes"]["pair_graded"] == cycle["classes"]["pair_graded"]
        assert path["classes"]["motif_pair"] != cycle["classes"]["motif_pair"]
        mass = [
            selected_mass(
                state,
                lambda sid, states=states, target=target: (
                    states[sid]["classes"]["pair_graded"] == target
                ),
            )
            for state in (path, cycle)
        ]
        expected = zero_table()
        expected[2][2], expected[3][2], expected[2][3], expected[3][3] = 1, -1, -1, 1
        assert mass == [zero_table(), expected]
        assert [evaluate(row, F(1, 2), F(1, 2)) for row in mass] == [F(0), F(1, 64)]


def test_all_pinned_m_recognizer_controls_remain_true_without_importing_old_executors(
    executors, pinned_m
):
    cases = pinned_m["observable_controls"]["recognizer_cases"]
    assert len(cases) == 14
    for case in cases:
        args = {name: case[name] for name in ("kept", "past", "eligible")}
        expected = motif_supports(**args)
        assert wire(expected) == wire(case["expected_supports"])
        for module in executors:
            assert wire(module.motif_supports(**args)) == wire(expected)


def test_whole_aggregate_has_native_exact_json_roundtrip_within_capture_cap(aggregate):
    runner, suite = aggregate
    encoded = wire(suite)
    assert wire(json.loads(encoded)) == encoded
    assert len(runner.canonical(suite)) < 64 * 1024 * 1024
    assert set(suite["analysis"]) == {
        "frames",
        "profiles",
        "states",
        "partitions",
        "closure",
        "expected_updates",
        "motif_expected_update",
        "counts",
    }


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


def test_optimized_assertion_free_schema_guards_and_valid_recognizer(tmp_path):
    # Full valid analyze() calls run in both normal and optimized suite runs.
    # This short subprocess independently guards rejection without duplicating
    # the entire 99,180-atom experiment another two times per suite run.
    script = r"""
import importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1])
valid = {"schema_version":"det8-qr05n-problem-v1","family":"qr05n_layered_iid"}
class Text(str):
    pass
class Mapping(dict):
    pass
class Sequence(list):
    pass
invalid = [True, {}, {**valid,"extra":1}, {**valid,"family":False}, {**valid,"schema_version":1},
           Mapping(valid), Sequence(), {**valid,"family":Text(valid["family"])},
           {**valid,"schema_version":Text(valid["schema_version"])},
           {Text("family"):valid["family"],"schema_version":valid["schema_version"]},
           {"family":valid["family"],Text("schema_version"):valid["schema_version"]}]
rejected = 0
for i, filename in enumerate(("portability.py","reference_qr05n.py")):
    name = "_qr05n_optimized_guards_" + str(i)
    spec = importlib.util.spec_from_file_location(name, root / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("missing executor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    actual = module.motif_supports([6,1,4,3],[[1,3],[],[1,3],[]],[1,3,4,6])
    if type(actual) is not list or actual != [[1,3,4,6]] or any(type(v) is not int for row in actual for v in row):
        raise RuntimeError("optimized marked-order recognition differs")
    for value in invalid:
        try:
            module.analyze(value)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError("optimized invalid input accepted")
print(json.dumps({"valid_recognizers":2,"explicit_rejections":rejected}))
"""
    result = subprocess.run(
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
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert json.loads(result.stdout) == {"valid_recognizers": 2, "explicit_rejections": 22}


@pytest.mark.parametrize(
    "kind",
    (
        "frame_bool",
        "state_bool",
        "alias_bool",
        "alias_loss",
        "alias_weight",
        "reverse_bit",
        "descending_chain",
        "missing_motif",
        "duplicate_motif",
        "coefficient",
        "motif_bool",
        "new_kept_bool",
        "new_past_bool",
    ),
)
def test_audit_rejects_label_alias_feature_and_native_coercion_mutations(aggregate, analyses, kind):
    runner, _ = aggregate
    changed = {
        **analyses[0],
        "states": list(analyses[0]["states"]),
        "profiles": list(analyses[0]["profiles"]),
    }
    sid = 0
    if kind == "descending_chain":
        sid = changed["profiles"][14]["state_ids"][63]
    elif kind in ("missing_motif", "duplicate_motif", "motif_bool"):
        sid = next(state["state_id"] for state in changed["states"] if state["motif_count"])
    elif kind in ("new_kept_bool", "new_past_bool"):
        sid = 257
    changed["states"][sid] = json.loads(wire(changed["states"][sid]))
    state = changed["states"][sid]
    if kind == "frame_bool":
        state["frame_id"] = False
    elif kind == "state_bool":
        state["state_id"] = False
    elif kind == "alias_bool":
        state["aliases"][0]["profile_index"] = False
    elif kind == "alias_loss":
        state["aliases"].pop()
    elif kind == "alias_weight":
        state["transitions"][0]["coefficients"][0][0] = len(state["aliases"])
    elif kind == "reverse_bit":
        changed["profiles"][526] = {
            **changed["profiles"][526],
            "past": changed["profiles"][520]["past"],
        }
    elif kind == "descending_chain":
        state["chain_counts"][2] = 0
    elif kind == "missing_motif":
        state["motif_supports"] = []
    elif kind == "duplicate_motif":
        state["motif_supports"].append(list(state["motif_supports"][0]))
    elif kind == "motif_bool":
        state["motif_count"] = True
    elif kind == "new_kept_bool":
        assert state["kept"][0] == 0
        state["kept"][0] = False
    elif kind == "new_past_bool":
        assert state["past"][1][0] == 0
        state["past"][1][0] = False
    else:
        state["transitions"][0]["coefficients"][0][0] += 1
    with pytest.raises(ValueError):
        runner.check_analysis(changed)


def test_equal_class_sizes_do_not_substitute_for_actual_candidate_fibers(aggregate, analyses):
    runner, _ = aggregate
    changed = {
        **analyses[0],
        "partitions": dict(analyses[0]["partitions"]),
        "states": list(analyses[0]["states"]),
    }
    changed["partitions"]["motif_pair"] = json.loads(wire(changed["partitions"]["motif_pair"]))
    groups = changed["partitions"]["motif_pair"]
    left, right = [group for group in groups if len(group["members"]) > 1][:2]
    a, b = left["members"][-1], right["members"][-1]
    left["members"] = sorted(b if sid == a else sid for sid in left["members"])
    right["members"] = sorted(a if sid == b else sid for sid in right["members"])
    for sid, cid in ((a, right["class_id"]), (b, left["class_id"])):
        changed["states"][sid] = {
            **changed["states"][sid],
            "classes": {**changed["states"][sid]["classes"], "motif_pair": cid},
        }
    assert [len(group["members"]) for group in groups] == [
        len(group["members"]) for group in analyses[0]["partitions"]["motif_pair"]
    ]
    assert changed["counts"] == analyses[0]["counts"]
    assert sorted(sid for group in groups for sid in group["members"]) == list(range(2470))
    with pytest.raises(ValueError):
        runner.check_analysis(changed)


@pytest.mark.parametrize("kind", ("flip_outcome", "omit_failure", "fabricate_failed_quotient"))
def test_failed_partition_evidence_cannot_be_hidden_or_replaced(aggregate, analyses, kind):
    runner, _ = aggregate
    changed = {**analyses[0], "closure": json.loads(wire(analyses[0]["closure"]))}
    failed = next(name for name in QUESTIONS if not changed["closure"][name]["closed"])
    if kind == "flip_outcome":
        changed["closure"][failed]["closed"] = True
    elif kind == "omit_failure":
        changed["closure"][failed]["first_collision"] = None
    else:
        changed["closure"][failed]["quotient_rows"] = [
            {"class_id": 0, "representative_state": 0, "transitions": []}
        ]
    with pytest.raises(ValueError):
        runner.check_analysis(changed)


def test_prior_restriction_requires_actual_candidate_class_map(aggregate, analyses):
    runner, _ = aggregate
    changed = {**analyses[0], "states": list(analyses[0]["states"])}
    state = changed["states"][0]
    changed["states"][0] = {**state, "classes": {**state["classes"], "motif_pair": 1}}
    with pytest.raises(ValueError):
        runner.prior_bridge(changed)


def full_count_law(states, state):
    table = {}
    for atom in state["transitions"]:
        target = tuple(states[atom["target_state"]]["chain_counts"])
        row = table.setdefault(target, zero_table())
        for i, j in product(range(4), repeat=2):
            row[i][j] += atom["coefficients"][i][j]
    return [
        {"chain_counts": list(counts), "coefficients": coefficients}
        for counts, coefficients in sorted(table.items())
    ]


def test_retained_counterexamples_include_complete_polynomials_and_measured_count_laws(
    aggregate, independent, expected_closure
):
    _, suite = aggregate
    model = independent[0]
    states = model["states"]
    for name in QUESTIONS:
        collision = expected_closure[name]["first_collision"]
        retained = suite["controls"]["counterexamples"][name]
        if collision is None:
            assert retained is None
            continue
        left, right = (states[collision[key]] for key in ("left_state", "right_state"))
        evaluations = []
        differing = []
        for index, (x, y) in enumerate(POINTS):
            a = evaluate(collision["left_coefficients"], x, y)
            b = evaluate(collision["right_coefficients"], x, y)
            evaluations.append(
                {"rates": [str(x), str(y)], "left_probability": str(a), "right_probability": str(b)}
            )
            if index < 16 and a != b:
                differing.append(index)
        assert differing
        laws = [full_count_law(states, state) for state in (left, right)]
        expected = {
            "partition": name,
            "witness": collision,
            "equal_current_key": model["partitions"][name][collision["class_id"]]["key"],
            "observations": [
                {
                    key: state[key]
                    for key in (
                        "state_id",
                        "frame_id",
                        "kept",
                        "past",
                        "chain_counts",
                        "motif_supports",
                        "motif_count",
                    )
                }
                for state in (left, right)
            ],
            "first_aliases": [state["aliases"][0] for state in (left, right)],
            "evaluations": evaluations,
            "first_distinguishing_grid_index": differing[0],
            "full_count_laws": laws,
            "full_count_laws_equal": wire(laws[0]) == wire(laws[1]),
        }
        assert wire(retained) == wire(expected)
        for law in laws:
            for x, y in POINTS:
                masses = [evaluate(atom["coefficients"], x, y) for atom in law]
                assert sum(masses) == 1 and all(p >= 0 for p in masses)


def test_retained_source_controls_match_independent_observations(
    aggregate, independent, expected_updates
):
    _, suite = aggregate
    model, aliases = independent
    states = model["states"]
    controls = suite["controls"]
    descending = [
        {
            "profile_index": pi,
            "mask": 63,
            "state_id": aliases[pi, 63],
            "chain_counts": states[aliases[pi, 63]]["chain_counts"],
            "past": states[aliases[pi, 63]]["past"],
        }
        for pi in (14, 526)
    ]
    assert wire(controls["descending_id_edges"]) == wire(descending)
    complete = []
    expected_b = zero_table()
    expected_b[1][1], expected_b[1][2], expected_b[2][1], expected_b[2][2] = 9, 18, 18, 36
    for pi in (517, 1029):
        state = states[aliases[pi, 63]]
        assert state["pair_graded"][2][2] == expected_b
        complete.append(
            {
                "profile_index": pi,
                "mask": 63,
                "state_id": state["state_id"],
                "chain_counts": state["chain_counts"],
                "motif_count": state["motif_count"],
                "motif_supports": state["motif_supports"],
                "pair_22": expected_b,
                "motif_expected_update": expected_updates[1]["rows"][state["state_id"]],
            }
        )
    assert wire(controls["complete_incidence"]) == wire(complete)
    assert wire(controls["empty_incidence"]) == wire(
        {
            "profile_indices": [6, 518],
            "state_ids": model["profiles"][6]["state_ids"],
            "duplicates_are_aliases": True,
        }
    )
    target = states[aliases[5, 45]]["classes"]["pair_graded"]
    coefficients = [
        selected_mass(
            states[aliases[pi, 63]], lambda sid: states[sid]["classes"]["pair_graded"] == target
        )
        for pi in (4, 5)
    ]
    assert wire(controls["old_adversary"]) == wire(
        {
            "path_state": aliases[4, 63],
            "cycle_state": aliases[5, 63],
            "target_state": aliases[5, 45],
            "target_pair_class": target,
            "coefficients": coefficients,
            "half_probabilities": ["0", "1/64"],
        }
    )
    assert wire(controls["fixed_only"]) == wire(
        [
            {
                "frame_id": states[aliases[pi, 0]]["frame_id"],
                "state_id": aliases[pi, 0],
                "kept": states[aliases[pi, 0]]["kept"],
            }
            for pi in (0, 3)
        ]
    )
    assert controls["feature_redefined"] is controls["stable_repair_executed"] is False


def test_retained_prior_bridge_records_actual_restricted_fibers_and_certificate(
    aggregate, independent, pinned_m, restricted_m
):
    _, suite = aggregate
    model = independent[0]
    old = pinned_m["analysis"]
    closed = suite["analysis"]["closure"]["motif_pair"]["closed"]
    expected = {
        "prior_artifact": "qr-05m-observable-realization-2026-09-06/results.json",
        "matched_states": 257,
        "matched_original_aliases": 352,
        "new_states": 2213,
        "added_aliases_on_old_states": sum(
            alias["profile_index"] >= 6
            for state in model["states"][:257]
            for alias in state["aliases"]
        ),
        "subset_closed_prefix": True,
        "class_maps": {
            name: [{"expanded_class": new, "old_class": before} for before, new in mapping.items()]
            for name, mapping in restricted_m["maps"].items()
        },
        "pulled_back_partitions": {
            "pair_graded": [
                {"class_id": group["class_id"], "members": group["members"]}
                for group in old["partitions"]["pair_graded"]
            ],
            "motif_pair": old["observable"]["classes"],
        },
        "old_state_polynomials_equal": True,
        "restricted_candidate_quotient": {
            "closed": True,
            "first_collision": None,
            "quotient_rows": restricted_m["quotient_rows"],
            "semigroup": restricted_m["semigroup"],
        },
        "global_candidate_closed": closed,
        "global_quotient_restriction_verified": True if closed else None,
        "whole_M_schema_reproduced": False,
    }
    assert wire(suite["prior_bridge"]) == wire(expected)


def test_retained_audit_inventory_and_claim_boundaries(aggregate, analyses, independent):
    _, suite = aggregate
    a = analyses[0]
    assert wire(suite["input"]) == wire(problem())
    assert wire(suite["analysis"]) == wire(a)
    counts = a["counts"]
    assert wire(suite["audit"]) == wire(
        {
            "verified": True,
            "rates": [[str(x), str(y)] for x, y in POINTS],
            "rate_points": 22,
            "evaluated_fine_atoms": 22 * counts["fine_transition_atoms"],
            "evaluated_summary_atoms": 22 * counts["summary_transition_atoms"],
            "deterministic_corner_rows": 4 * len(independent[0]["states"]),
            "expected_update_coefficient_cells": counts["expected_update_coefficient_cells"],
            "motif_expected_update_coefficient_cells": counts[
                "motif_expected_update_coefficient_cells"
            ],
            "semigroup_coefficient_cells": counts["semigroup_coefficient_cells"],
        }
    )
    assert suite["candidate_closed"] is a["closure"]["motif_pair"]["closed"]
    assert suite["candidate_failure_is_valid_investigative_outcome"] is True
    assert suite["old_domain_restriction_preserved"] is True
    for flag in (
        "source_labels_in_summary_keys",
        "aliases_used_as_weights",
        "selected_rate_zeros_discarded",
        "numeric_labels_assumed_topological",
        "expected_updates_imply_full_law",
        "feature_redefined_after_failure",
        "stable_refinement_executed",
        "expanded_trace_audit_executed",
        "unseen_domain_closure_claimed",
        "minimum_storage_or_runtime_claimed",
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
    assert suite["totals"]["restricted_prior_semigroup_coefficient_cells"] == 295424
    assert suite["bounds"]["artifact_bytes_max"] == 64 * 1024 * 1024
