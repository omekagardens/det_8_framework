"""Independent raw-order, refinement, and summary-only consumer tests for P.

Only the byte-pinned O JSON is read; no earlier executor or test is imported.
Observed features and every fine polynomial are reconstructed before using
any P executor output. Synthetic Markov controls are not certified O inputs.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from functools import cache
from itertools import combinations, pairwise, product
from math import comb
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
F = Fraction
O_SHA = "3364b36813f745a645d78d6d30caa292778da986cb6d1140f108a0fd4b945eb1"
QUESTIONS = (
    "chain_counts",
    "motif_count",
    "path_count",
    "counts_motif_path",
    "named_relation_1_7",
)
NODES = tuple(product((F(0), F(1, 3), F(2, 3), F(1)), repeat=2))
POINTS = NODES + (
    (F(1, 2), F(1, 2)),
    (F(2, 5), F(3, 7)),
    (F(1, 5), F(4, 5)),
    (F(1, 2), F(1, 3)),
    (F(0), F(2, 5)),
    (F(3, 7), F(1)),
)


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
    raise AssertionError(f"non-native mathematical wire type: {type(value)}")


def wire(value):
    native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


def digest(value):
    return hashlib.sha256(wire(value)).hexdigest()


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("private test module name is already in use")
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("required module unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def pinned_o():
    path = HERE.parent / "qr-05o-path-observable-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 27143093 and hashlib.sha256(raw).hexdigest() == O_SHA
    envelope = json.loads(raw)
    # The envelope has runtime floats. Only the mathematical suite is native.
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


@pytest.fixture(scope="session")
def problem(pinned_o):
    a = pinned_o["analysis"]
    return {
        "schema_version": "det8-qr05p-problem-v1",
        "family": "qr05p_summary_contract",
        "model": {
            "frames": copy.deepcopy(a["frames"]),
            "states": [
                {key: copy.deepcopy(row[key]) for key in ("state_id", "frame_id", "kept", "past")}
                for row in a["states"]
            ],
        },
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05p_test_direct", "closure.py"),
        private_module("_qr05p_test_reference", "reference_qr05p.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors, problem):
    return tuple(module.analyze(problem) for module in executors)


@pytest.fixture(scope="session")
def aggregate():
    module = private_module("_qr05p_test_aggregate", "study.py")
    return module, module.run_suite()


def zero():
    return [[0] * 4 for _ in range(4)]


@cache
def kernel(odd, even, o, e):
    result = zero()
    for a in range(odd - o + 1):
        for b in range(even - e + 1):
            result[o + a][e + b] = (-1) ** (a + b) * comb(odd - o, a) * comb(even - e, b)
    return result


@cache
def evaluate_tuple(table, x, y):
    return sum(
        (c * x**i * y**j for i, row in enumerate(table) for j, c in enumerate(row) if c), F(0)
    )


def evaluate(table, x, y):
    return evaluate_tuple(tuple(tuple(row) for row in table), x, y)


@cache
def direct_probability(odd, even, o, e, x, y):
    return x**o * (1 - x) ** (odd - o) * y**e * (1 - y) ** (even - e)


def add_into(left, right):
    for i, j in product(range(4), repeat=2):
        left[i][j] += right[i][j]


def relation_of(state):
    return {
        (state["kept"][i], b)
        for b, before in zip(state["kept"], state["past"], strict=True)
        for i in before
    }


def state_key(frame_id, kept, past):
    return frame_id, tuple(kept), tuple(tuple(row) for row in past)


def observed_features(state, frame):
    kept, relation = state["kept"], relation_of(state)
    eligible = set(frame["eligible"])
    chains = [[] for _ in range(4)]
    d = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for q in range(4):
        for vertices in combinations([v for v in kept if v not in (0, 7)], q):
            if not all(
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
    motifs, paths = [], []
    for four in combinations(sorted(set(kept) & eligible), 4):
        if sum(v % 2 for v in four) != 2:
            continue
        edges = [(a, z) for a, z in relation if a in four and z in four]
        if any(a % 2 == z % 2 for a, z in edges) or len({a % 2 for a, _ in edges}) != 1:
            continue
        if len(edges) == 4:
            motifs.append(list(four))
        if len(edges) == 3 and sorted(sum(v in edge for edge in edges) for v in four) == [
            1,
            1,
            2,
            2,
        ]:
            paths.append(list(four))
    odd = sum(v % 2 for v in kept if v in eligible)
    return {
        "state_id": state["state_id"],
        "color_sizes": [odd, len(set(kept) & eligible) - odd],
        "chain_counts": list(map(len, chains)),
        "mean_graded": d,
        "pair_graded": b,
        "motif_supports": motifs,
        "motif_count": len(motifs),
        "path_supports": paths,
        "path_count": len(paths),
    }


def partition(keys):
    ids, classes, registry = [], [], {}
    for sid, key in enumerate(keys):
        encoded = wire(key)
        cid = registry.setdefault(encoded, len(registry))
        if cid == len(classes):
            classes.append({"class_id": cid, "key": key, "members": []})
        ids.append(cid)
        classes[cid]["members"].append(sid)
    return {"state_classes": ids, "classes": classes}


def fibers(ids):
    answer = []
    for sid, cid in enumerate(ids):
        assert 0 <= cid <= len(answer)
        if cid == len(answer):
            answer.append({"class_id": cid, "members": []})
        answer[cid]["members"].append(sid)
    return answer


def class_map(fine, coarse):
    answer = []
    for a, b in zip(fine, coarse, strict=True):
        if a == len(answer):
            answer.append(b)
        elif answer[a] != b:
            return None
    return answer


def pushed(fine, ids):
    answer = []
    for row in fine:
        accumulated = {}
        for atom in row["transitions"]:
            add_into(
                accumulated.setdefault(ids[atom["target_state"]], zero()), atom["coefficients"]
            )
        answer.append(
            {
                "state_id": row["state_id"],
                "transitions": [
                    {"target_class": target, "coefficients": table}
                    for target, table in sorted(accumulated.items())
                ],
            }
        )
    return answer


def first_difference(left, right):
    a = {row["target_class"]: row["coefficients"] for row in left}
    b = {row["target_class"]: row["coefficients"] for row in right}
    for target in sorted(a.keys() | b.keys()):
        p, q = a.get(target, zero()), b.get(target, zero())
        if p != q:
            return target, p, q
    return None


def refine(fine, initial):
    current, rounds = initial[:], []
    while True:
        rows = pushed(fine, current)
        next_ids = partition(
            [[cid, row["transitions"]] for cid, row in zip(current, rows, strict=True)]
        )["state_classes"]
        splits = []
        for group in fibers(next_ids):
            right = group["members"][0]
            parent = current[right]
            left = current.index(parent)
            if next_ids[left] == group["class_id"]:
                continue
            target, a, b = first_difference(rows[left]["transitions"], rows[right]["transitions"])
            rates = next(
                [str(x), str(y)] for x, y in NODES if evaluate(a, x, y) != evaluate(b, x, y)
            )
            splits.append(
                {
                    "parent_class_id": parent,
                    "child_class_id": group["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "target_class": target,
                    "left_coefficients": a,
                    "right_coefficients": b,
                    "first_distinguishing_rates": rates,
                }
            )
        rounds.append(
            {
                "round_index": len(rounds),
                "state_classes": current,
                "classes": fibers(current),
                "pushed_rows_sha256": digest(rows),
                "pushed_atoms": sum(len(row["transitions"]) for row in rows),
                "stable": next_ids == current,
                "separations": splits,
            }
        )
        if next_ids == current:
            return rounds, rows
        assert len(fibers(next_ids)) > len(fibers(current))
        current = next_ids
        assert len(rounds) <= len(current) - len(fibers(initial))


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
                cells = accumulated.setdefault(target, [0] * 256)
                for i, a in left:
                    for j, b in right:
                        cells[16 * i + j] += a * b
        assert set(accumulated) == {atom["target_class"] for atom in first["transitions"]}
        for target, table in sparse[first["class_id"]]:
            expected = [0] * 256
            for i, value in table:
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
def independent(problem):
    model = problem["model"]
    states, frames = model["states"], model["frames"]
    fs = [observed_features(state, frames[state["frame_id"]]) for state in states]
    registry = {state_key(s["frame_id"], s["kept"], s["past"]): s["state_id"] for s in states}
    assert len(registry) == len(states) == 2470
    fine = []
    for state, feature in zip(states, fs, strict=True):
        frame = frames[state["frame_id"]]
        eligible = sorted(set(state["kept"]) & set(frame["eligible"]))
        relation = relation_of(state)
        atoms = []
        for mask in range(1 << len(eligible)):
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(eligible) if mask & (1 << bit)]
            )
            past = [[i for i, a in enumerate(kept) if (a, b) in relation] for b in kept]
            sid = registry[state_key(state["frame_id"], kept, past)]
            atoms.append(
                {
                    "target_state": sid,
                    "coefficients": kernel(*feature["color_sizes"], *fs[sid]["color_sizes"]),
                }
            )
        fine.append(
            {
                "state_id": state["state_id"],
                "transitions": sorted(atoms, key=lambda a: a["target_state"]),
            }
        )
    keys_c, keys_h = [], []
    for state, feature in zip(states, fs, strict=True):
        frame = frames[state["frame_id"]]
        public = [frame["density"], frame["fixed"], frame["eligible"]]
        key = [public, feature["pair_graded"], feature["motif_count"]]
        keys_c.append(key)
        keys_h.append([*key, feature["path_count"]])
    partitions = {"C": partition(keys_c), "H": partition(keys_h)}
    rounds, rows = refine(fine, partitions["C"]["state_classes"])
    ids, classes = rounds[-1]["state_classes"], rounds[-1]["classes"]
    quotient = [
        {
            "class_id": group["class_id"],
            "representative_state": group["members"][0],
            "transitions": rows[group["members"][0]]["transitions"],
        }
        for group in classes
    ]
    return {
        "features": fs,
        "partitions": partitions,
        "fine": fine,
        "rounds": rounds,
        "pushed": rows,
        "ids": ids,
        "classes": classes,
        "quotient": quotient,
        "semigroup": composition(quotient),
    }


def observable_values(model, fs, name):
    if name == "chain_counts":
        return [row["chain_counts"] for row in fs]
    if name in ("motif_count", "path_count"):
        return [row[name] for row in fs]
    if name == "counts_motif_path":
        return [[*row["chain_counts"], row["motif_count"], row["path_count"]] for row in fs]
    assert name == "named_relation_1_7"
    return [int((1, 7) in relation_of(state)) for state in model["states"]]


def marginal(atoms, values, target_key):
    groups, lookup = {}, {}
    for atom in atoms:
        value = values[atom[target_key]]
        key = wire(value)
        lookup[key] = value
        add_into(groups.setdefault(key, zero()), atom["coefficients"])
    return [{"value": lookup[key], "coefficients": groups[key]} for key in sorted(groups)]


@pytest.fixture(scope="session")
def expected_consumer(problem, independent):
    classes, quotient = independent["classes"], independent["quotient"]
    observables, marginals = [], []
    for name in QUESTIONS:
        values = observable_values(problem["model"], independent["features"], name)
        failure = None
        for group in classes:
            left = group["members"][0]
            for right in group["members"][1:]:
                if wire(values[left]) != wire(values[right]):
                    failure = {
                        "class_id": group["class_id"],
                        "left_state": left,
                        "right_state": right,
                        "left_value": values[left],
                        "right_value": values[right],
                    }
                    break
            if failure is not None:
                break
        class_values = None if failure else [values[group["members"][0]] for group in classes]
        observables.append(
            {
                "name": name,
                "measurable": failure is None,
                "class_values": class_values,
                "first_failure": failure,
            }
        )
        if failure:
            continue
        rows = [
            {
                "class_id": row["class_id"],
                "outcomes": marginal(row["transitions"], class_values, "target_class"),
            }
            for row in quotient
        ]
        cells = 0
        for fine in independent["fine"]:
            expected = rows[independent["ids"][fine["state_id"]]]["outcomes"]
            actual = marginal(fine["transitions"], values, "target_state")
            assert actual == expected
            cells += 16 * len(actual)
        marginals.append({"name": name, "rows": rows, "fine_coefficient_cells": cells})
    consumer = {
        "schema_version": "det8-qr05p-consumer-v1",
        "model_sha256": digest(problem["model"]),
        "state_classes_sha256": digest(independent["ids"]),
        "class_count": len(classes),
        "quotient_rows": quotient,
        "observables": observables,
    }
    return consumer, marginals


def test_raw_projection_is_byte_bound_and_has_no_precomputed_evidence(problem, pinned_o):
    assert set(problem) == {"schema_version", "family", "model"}
    assert set(problem["model"]) == {"frames", "states"}
    assert len(problem["model"]["states"]) == 2470
    assert problem["model"]["frames"] == [
        {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
        {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
    ]
    for state, previous in zip(
        problem["model"]["states"], pinned_o["analysis"]["states"], strict=True
    ):
        assert set(state) == {"state_id", "frame_id", "kept", "past"}
        assert all(wire(state[key]) == wire(previous[key]) for key in state)


def test_complete_native_analysis_and_independent_features(
    analyses, independent, problem, pinned_o
):
    assert wire(analyses[0]) == wire(analyses[1])
    assert len(wire(analyses[0])) < 64 * 1024 * 1024
    assert wire(json.loads(wire(analyses[0]))) == wire(analyses[0])
    assert set(analyses[0]) == {
        "model_sha256",
        "features",
        "partitions",
        "fine_kernel",
        "refinement",
        "consumer",
        "consumer_audit",
        "counts",
    }
    for a in analyses:
        assert a["model_sha256"] == digest(problem["model"])
        assert wire(a["features"]) == wire(independent["features"])
        assert wire(a["partitions"]) == wire(independent["partitions"])
    for feature, old, path in zip(
        independent["features"],
        pinned_o["analysis"]["states"],
        pinned_o["analysis"]["path_observable"]["states"],
        strict=True,
    ):
        assert all(
            feature[key] == old[key]
            for key in feature
            if key not in ("path_count", "path_supports")
        )
        assert (
            feature["path_count"] == path["path_count"]
            and feature["path_supports"] == path["path_supports"]
        )


def test_all_fine_laws_are_induced_normalized_corner_exact_and_pinned(
    analyses, independent, pinned_o
):
    fine, features = independent["fine"], independent["features"]
    assert fine == [
        {"state_id": row["state_id"], "transitions": row["transitions"]}
        for row in pinned_o["analysis"]["states"]
    ]
    atoms = sum(len(row["transitions"]) for row in fine)
    assert atoms == 99180
    for row, feature in zip(fine, features, strict=True):
        assert len(row["transitions"]) == 2 ** sum(feature["color_sizes"])
        assert all(
            sum(a["coefficients"][i][j] for a in row["transitions"]) == int(i == j == 0)
            for i, j in product(range(4), repeat=2)
        )
        odd, even = feature["color_sizes"]
        for atom in row["transitions"]:
            o, e = features[atom["target_state"]]["color_sizes"]
            for x, y in POINTS:
                assert (
                    evaluate(atom["coefficients"], x, y)
                    == direct_probability(odd, even, o, e, x, y)
                    >= 0
                )
        for x, y in product((F(0), F(1)), repeat=2):
            positive = [atom for atom in row["transitions"] if evaluate(atom["coefficients"], x, y)]
            assert len(positive) == 1 and evaluate(positive[0]["coefficients"], x, y) == 1
            if x == y == 1:
                assert positive[0]["target_state"] == row["state_id"]
    for a in analyses:
        assert a["fine_kernel"] == {
            "sha256": digest(fine),
            "transition_atoms": atoms,
            "coefficient_cells": 16 * atoms,
            "normalization_rows": 2470,
            "deterministic_corner_rows": 9880,
            "rate_points": 22,
            "evaluated_atoms": 22 * atoms,
        }


def test_chain_pairs_count_both_orders_self_pairs_fixed_vertices_and_induced_motifs(independent):
    for feature in independent["features"]:
        d, b, n = feature["mean_graded"], feature["pair_graded"], feature["chain_counts"]
        assert b[0] == d
        for q, r in product(range(4), repeat=2):
            assert b[q][r] == b[r][q]
            assert sum(map(sum, b[q][r])) == n[q] * n[r]
        assert not (
            {tuple(row) for row in feature["motif_supports"]}
            & {tuple(row) for row in feature["path_supports"]}
        )
        odd, even = feature["color_sizes"]
        assert feature["motif_count"] + feature["path_count"] <= comb(odd, 2) * comb(even, 2)


def test_every_refinement_signature_witness_and_terminal_fiber_is_recomputed(analyses, independent):
    rounds, ids = independent["rounds"], independent["ids"]
    c, h = (independent["partitions"][name]["state_classes"] for name in ("C", "H"))
    for a in analyses:
        r = a["refinement"]
        assert r["initial_partition"] == "C"
        assert wire(r["rounds"]) == wire(rounds)
        assert r["strict_rounds"] == r["final_round"] == len(rounds) - 1
        assert r["state_classes"] == ids and r["classes"] == independent["classes"]
        assert wire(r["quotient_rows"]) == wire(independent["quotient"])
        assert r["semigroup"] == independent["semigroup"]
        vectors = (c, ids, h)
        assert r["comparison"] == {
            "names": ["C", "R", "H"],
            "refinement": [
                [class_map(left, right) is not None for right in vectors] for left in vectors
            ],
            "same_memberships_as_H": ids == h,
            "R_to_C": class_map(ids, c),
            "R_to_H": class_map(ids, h),
            "H_to_R": class_map(h, ids),
        }
        atoms = sum(row["pushed_atoms"] for row in rounds)
        assert r["counts"] == {
            "rounds": len(rounds),
            "strict_rounds": len(rounds) - 1,
            "classes": len(independent["classes"]),
            "round_transition_atoms": atoms,
            "round_coefficient_cells": 16 * atoms,
            "separation_witnesses": sum(len(row["separations"]) for row in rounds),
            "quotient_transition_atoms": sum(
                len(row["transitions"]) for row in independent["quotient"]
            ),
            "semigroup_intermediate_paths": independent["semigroup"]["totals"][
                "intermediate_paths"
            ],
            "semigroup_coefficient_cells": independent["semigroup"]["totals"]["coefficient_cells"],
        }
    assert rounds[0]["state_classes"] == c and rounds[-1]["stable"] is True
    assert all(row["stable"] is False for row in rounds[:-1])
    assert len(rounds) - 1 <= len(ids) - len(fibers(c))
    for earlier, later in pairwise(rounds):
        assert class_map(later["state_classes"], earlier["state_classes"]) is not None
        assert len(later["classes"]) > len(earlier["classes"])
    for group, row in zip(independent["classes"], independent["quotient"], strict=True):
        assert all(
            independent["pushed"][sid]["transitions"] == row["transitions"]
            for sid in group["members"]
        )


def test_bottom_up_proper_successor_types_give_same_partition_without_synchronous_rounds(
    independent,
):
    c = independent["partitions"]["C"]["state_classes"]
    provisional, registry = {}, {}
    order = sorted(
        range(len(c)), key=lambda sid: (sum(independent["features"][sid]["color_sizes"]), sid)
    )
    for sid in order:
        targets, self_loop = {}, None
        size = sum(independent["features"][sid]["color_sizes"])
        for atom in independent["fine"][sid]["transitions"]:
            target = atom["target_state"]
            if target == sid:
                self_loop = atom["coefficients"]
                continue
            assert sum(independent["features"][target]["color_sizes"]) < size
            add_into(targets.setdefault(provisional[target], zero()), atom["coefficients"])
        assert self_loop is not None
        key = wire([c[sid], self_loop, [[target, p] for target, p in sorted(targets.items())]])
        provisional[sid] = registry.setdefault(key, len(registry))
    actual = partition([provisional[sid] for sid in range(len(c))])["state_classes"]
    assert actual == independent["ids"]
    # These are concrete admissible refiners; coarseness over all admissible Q
    # follows from the stated induction, not exhaustive partition enumeration.
    h = independent["partitions"]["H"]["state_classes"]
    for row in independent["rounds"]:
        assert class_map(h, row["state_classes"]) is not None
        assert class_map(list(range(len(c))), row["state_classes"]) is not None


def constant_fine(successors):
    one = zero()
    one[0][0] = 1
    return [
        {
            "state_id": sid,
            "transitions": [{"target_state": target, "coefficients": copy.deepcopy(one)}],
        }
        for sid, target in enumerate(successors)
    ]


@pytest.mark.parametrize(
    "successors,initial,expected_vectors",
    [
        ([1, 2, 3, 3], [0, 0, 0, 1], [[0, 0, 0, 1], [0, 0, 1, 2], [0, 1, 2, 3]]),
        ([0, 0, 2], [0, 0, 1], [[0, 0, 1]]),
        ([0, 0], [0, 1], [[0, 1]]),
    ],
    ids=["two-strict-rounds", "already-stable", "old-class-must-prevent-merge"],
)
def test_synthetic_production_refinement_is_not_a_one_round_or_merging_shortcut(
    executors, successors, initial, expected_vectors
):
    fine = constant_fine(successors)
    rounds, _ = refine(fine, initial)
    assert [row["state_classes"] for row in rounds] == expected_vectors
    for module in executors:
        assert wire(module.refine(fine, initial)) == wire(rounds)
    if len(initial) == 2:
        rows = pushed(fine, initial)
        illegally_merged = partition([row["transitions"] for row in rows])["state_classes"]
        assert illegally_merged == [0, 0] != initial


def test_exact_consumer_measurability_and_all_fine_marginal_polynomials(
    analyses, expected_consumer, independent
):
    consumer, marginals = expected_consumer
    for a in analyses:
        assert wire(a["consumer"]) == wire(consumer)
        audit = a["consumer_audit"]
        assert set(audit) == {
            "marginals",
            "prediction_checks",
            "nonmeasurable_questions",
            "named_singleton_control",
            "verified",
        }
        assert wire(audit["marginals"]) == wire(marginals)
        assert audit["verified"] is True
        assert audit["prediction_checks"] == 22 * len(independent["classes"]) * len(marginals)
        assert audit["nonmeasurable_questions"] == [
            row["name"] for row in consumer["observables"] if not row["measurable"]
        ]
    assert [row["name"] for row in consumer["observables"]] == list(QUESTIONS)
    assert consumer["observables"][-1]["measurable"] is False
    # No raw state, initial aliases, representative value fallback, or prior
    # probability distribution is available to the consumer payload.
    assert set(consumer) == {
        "schema_version",
        "model_sha256",
        "state_classes_sha256",
        "class_count",
        "quotient_rows",
        "observables",
    }


def test_named_singleton_is_a_real_class_relative_query_exclusion(analyses, problem, independent):
    states = problem["model"]["states"]
    chosen = []
    for vertex in (1, 3):
        chosen.append(
            next(
                s["state_id"]
                for s in states
                if s["frame_id"] == 0
                and s["kept"] == [0, vertex, 7]
                and s["past"] == [[], [0], [0, 1]]
            )
        )
    values = observable_values(problem["model"], independent["features"], QUESTIONS[-1])
    polynomials = []
    for sid in chosen:
        result = zero()
        for atom in independent["fine"][sid]["transitions"]:
            if values[atom["target_state"]]:
                add_into(result, atom["coefficients"])
        polynomials.append(result)
    x = zero()
    x[1][0] = 1
    assert polynomials == [x, zero()]
    c, h = (independent["partitions"][name]["state_classes"] for name in ("C", "H"))
    expected = {
        "state_ids": chosen,
        "C_classes": [c[s] for s in chosen],
        "H_classes": [h[s] for s in chosen],
        "R_classes": [independent["ids"][s] for s in chosen],
        "current_values": [1, 0],
        "next_coefficients": polynomials,
        "half_probabilities": ["1/2", "0"],
        "same_R_class": True,
    }
    assert (
        len(set(expected["C_classes"]))
        == len(set(expected["H_classes"]))
        == len(set(expected["R_classes"]))
        == 1
    )
    for a in analyses:
        assert wire(a["consumer_audit"]["named_singleton_control"]) == wire(expected)


def test_top_counts_are_derived_not_claims_about_memory_or_unrestricted_minimality(
    analyses, independent, expected_consumer
):
    _, marginals = expected_consumer
    expected = {
        "states": 2470,
        "features": 2470,
        "C_classes": len(independent["partitions"]["C"]["classes"]),
        "H_classes": len(independent["partitions"]["H"]["classes"]),
        "R_classes": len(independent["classes"]),
        "fine_atoms": 99180,
        "refinement_rounds": len(independent["rounds"]),
        "strict_rounds": len(independent["rounds"]) - 1,
        "measurable_questions": len(marginals),
        "consumer_prediction_checks": 22 * len(independent["classes"]) * len(marginals),
        "consumer_fine_coefficient_cells": sum(row["fine_coefficient_cells"] for row in marginals),
    }
    for a in analyses:
        assert a["counts"] == expected


def micro_problem():
    """Closed four-observation helper case with both named singleton witnesses."""
    return {
        "schema_version": "det8-qr05p-problem-v1",
        "family": "qr05p_summary_contract",
        "model": {
            "frames": [
                {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
                {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
            ],
            "states": [
                {"state_id": 0, "frame_id": 0, "kept": [0, 7], "past": [[], [0]]},
                {"state_id": 1, "frame_id": 0, "kept": [0, 1, 7], "past": [[], [0], [0, 1]]},
                {"state_id": 2, "frame_id": 0, "kept": [0, 3, 7], "past": [[], [0], [0, 1]]},
                {"state_id": 3, "frame_id": 1, "kept": [0, 3, 7], "past": [[], [0], [0, 1]]},
            ],
        },
    }


@pytest.fixture(scope="session")
def micro_analyses(executors):
    return tuple(module.analyze(micro_problem()) for module in executors)


def prediction_expected(name, cid, rates, marginal_rows):
    x, y = map(F, rates)
    return {
        "question": name,
        "class_id": cid,
        "rates": rates,
        "outcomes": [
            {"value": atom["value"], "probability": str(evaluate(atom["coefficients"], x, y))}
            for atom in marginal_rows[cid]["outcomes"]
        ],
    }


def test_predict_uses_only_detached_payload_and_preserves_all_structural_outcomes(
    executors, expected_consumer
):
    consumer, marginals = expected_consumer
    # Deep JSON detachment excludes fine records, live registries, and private
    # in-process construction objects. Cover every class and every audit rate,
    # without multiplying expensive public payload validation by their product.
    detached = json.loads(wire(consumer))
    for item in marginals:
        name, rows = item["name"], item["rows"]
        probes = {(cid, POINTS[cid % len(POINTS)]) for cid in range(consumer["class_count"])}
        probes |= {(consumer["class_count"] - 1, rates) for rates in POINTS}
        for cid, pair in sorted(probes):
            rates = list(map(str, pair))
            expected = prediction_expected(name, cid, rates, rows)
            for module in executors:
                actual = module.predict(detached, name, cid, rates)
                assert wire(actual) == wire(expected)
                assert sum(F(atom["probability"]) for atom in actual["outcomes"]) == 1
                assert all(F(atom["probability"]) >= 0 for atom in actual["outcomes"])
        # All 22 x class marginal evaluations are independently checked; no
        # sampled-rate evidence substitutes for the complete coefficients.
        for row, pair in product(rows, POINTS):
            expected = prediction_expected(name, row["class_id"], list(map(str, pair)), rows)
            assert sum(F(atom["probability"]) for atom in expected["outcomes"]) == 1
            assert all(F(atom["probability"]) >= 0 for atom in expected["outcomes"])
    assert wire(detached) == wire(consumer)


def test_fixed_independent_stage_marginals_equal_product_rates(expected_consumer):
    consumer, marginals = expected_consumer
    quotient = consumer["quotient_rows"]
    schedules = (
        ((F(1), F(1)), (F(1), F(1))),
        ((F(1, 2), F(1, 2)), (F(1, 3), F(2, 3))),
        ((F(0), F(2, 5)), (F(3, 7), F(1))),
    )
    for first, second in schedules:
        combined = first[0] * second[0], first[1] * second[1]
        for item in marginals:
            rows = item["rows"]
            for row in quotient:
                accumulated = {}
                for atom in row["transitions"]:
                    weight = evaluate(atom["coefficients"], *first)
                    for outcome in rows[atom["target_class"]]["outcomes"]:
                        key = wire(outcome["value"])
                        accumulated[key] = accumulated.get(key, F(0)) + weight * evaluate(
                            outcome["coefficients"], *second
                        )
                direct = {
                    wire(atom["value"]): evaluate(atom["coefficients"], *combined)
                    for atom in rows[row["class_id"]]["outcomes"]
                }
                assert accumulated == direct


def test_small_closed_helper_case_and_named_rejection_do_not_authenticate_other_domains(
    executors, micro_analyses
):
    assert wire(micro_analyses[0]) == wire(micro_analyses[1])
    for module, a in zip(executors, micro_analyses, strict=True):
        assert a["counts"]["states"] == 4
        consumer = json.loads(wire(a["consumer"]))
        assert a["consumer_audit"]["named_singleton_control"]["same_R_class"] is True
        for cid in range(consumer["class_count"]):
            for rates in (["0", "0"], ["1/2", "1/2"], ["1", "1"]):
                with pytest.raises(ValueError):
                    module.predict(consumer, "named_relation_1_7", cid, rates)
        singleton = a["refinement"]["state_classes"][1]
        out = module.predict(consumer, "chain_counts", singleton, ["0", "0"])
        assert any(atom["probability"] == "0" for atom in out["outcomes"])
        assert len(out["outcomes"]) == 2


def test_predict_result_vectors_are_detached_from_payload_and_later_calls(
    executors, micro_analyses
):
    for module, a in zip(executors, micro_analyses, strict=True):
        consumer = json.loads(wire(a["consumer"]))
        before = wire(consumer)
        first = module.predict(consumer, "counts_motif_path", 0, ["1/2", "1/2"])
        expected = copy.deepcopy(first)
        first["outcomes"][0]["value"][0] = 999
        first["rates"][0] = "0"
        assert wire(consumer) == before
        assert wire(module.predict(consumer, "counts_motif_path", 0, ["1/2", "1/2"])) == wire(
            expected
        )


def test_consumer_validation_is_not_a_fine_domain_encoder_or_artifact_authenticator(
    executors, micro_analyses
):
    for module, a in zip(executors, micro_analyses, strict=True):
        consumer = json.loads(wire(a["consumer"]))
        original = module.predict(consumer, "chain_counts", 0, ["1/2", "1/2"])
        consumer["model_sha256"] = "a" * 64
        consumer["state_classes_sha256"] = "b" * 64
        # A structurally valid different digest is not authenticated by predict.
        # The application, not this mathematical API, pins the trusted payload.
        assert module.predict(consumer, "chain_counts", 0, ["1/2", "1/2"]) == original


class IntSubclass(int):
    pass


class StringSubclass(str):
    pass


class ListSubclass(list):
    pass


class DictSubclass(dict):
    pass


def invalid_problem(case):
    p = micro_problem()
    states, frames = p["model"]["states"], p["model"]["frames"]
    if case == "extra":
        p["outcome"] = True
    elif case == "missing":
        del p["family"]
    elif case == "schema":
        p["schema_version"] = "det8-qr05o-problem-v1"
    elif case == "family":
        p["family"] = "different"
    elif case == "dict-subclass":
        return DictSubclass(p)
    elif case == "key-subclass":
        p[StringSubclass("family")] = p.pop("family")
    elif case == "value-subclass":
        p["family"] = StringSubclass(p["family"])
    elif case == "tuple-states":
        p["model"]["states"] = tuple(states)
    elif case == "list-subclass":
        p["model"]["states"] = ListSubclass(states)
    elif case == "model-extra":
        p["model"]["classes"] = []
    elif case == "frame-extra":
        frames[0]["aliases"] = []
    elif case == "state-extra":
        states[0]["motif_count"] = 0
    elif case == "state-id-bool":
        states[0]["state_id"] = False
    elif case == "state-id-gap":
        states[1]["state_id"] = 8
    elif case == "frame-id-bool":
        states[0]["frame_id"] = False
    elif case == "frame-bool":
        frames[0]["frame_id"] = False
    elif case == "kept-bool":
        states[1]["kept"][0] = False
    elif case == "past-bool":
        states[1]["past"][1][0] = False
    elif case == "past-subclass":
        states[1]["past"][1][0] = IntSubclass(0)
    elif case == "past-float":
        states[1]["past"][1][0] = 0.0
    elif case == "density-float":
        frames[0]["density"] = 12.0
    elif case == "density-noncanonical":
        frames[0]["density"] = "12/1"
    elif case == "fixed-mark":
        frames[1]["fixed"] = [0, 7]
    elif case == "eligible-mark":
        frames[1]["eligible"] = [1, 2, 3, 4, 5, 6]
    elif case == "missing-endpoint":
        states[0]["kept"] = [0]
        states[0]["past"] = [[]]
    elif case == "duplicate-kept":
        states[1]["kept"] = [0, 1, 1]
    elif case == "unsorted-kept":
        states[1]["kept"] = [0, 7, 1]
    elif case == "duplicate-past":
        states[1]["past"][2] = [0, 0, 1]
    elif case == "unsorted-past":
        states[1]["past"][2] = [1, 0]
    elif case == "invalid-past":
        states[1]["past"][2] = [0, 3]
    elif case == "self-loop":
        states[1]["past"][1] = [0, 1]
    elif case == "cycle":
        states[1]["past"][0] = [1]
    elif case == "nontransitive":
        states[1]["past"][2] = [1]
    elif case == "missing-fixed":
        states[3]["kept"], states[3]["past"] = [0, 7], [[], [0]]
    elif case == "duplicate-observation":
        states[2] = {**copy.deepcopy(states[1]), "state_id": 2}
    elif case == "missing-successor":
        states.append(
            {"state_id": 4, "frame_id": 0, "kept": [0, 1, 2, 7], "past": [[], [0], [0], [0, 1, 2]]}
        )
    elif case == "one-frame":
        states[3]["frame_id"] = 0
    elif case == "too-few":
        p["model"]["states"] = states[:1]
    elif case == "too-many":
        p["model"]["states"] = [{**states[0], "state_id": sid} for sid in range(2471)]
    elif case == "overflow":
        states[0]["state_id"] = 1 << 4096
    elif case == "missing-singleton-control":
        p["model"]["states"] = [states[0], {**states[3], "state_id": 1}]
    else:
        raise AssertionError(case)
    return p


INVALID_PROBLEMS = (
    "extra",
    "missing",
    "schema",
    "family",
    "dict-subclass",
    "key-subclass",
    "value-subclass",
    "tuple-states",
    "list-subclass",
    "model-extra",
    "frame-extra",
    "state-extra",
    "state-id-bool",
    "state-id-gap",
    "frame-id-bool",
    "frame-bool",
    "kept-bool",
    "past-bool",
    "past-subclass",
    "past-float",
    "density-float",
    "density-noncanonical",
    "fixed-mark",
    "eligible-mark",
    "missing-endpoint",
    "duplicate-kept",
    "unsorted-kept",
    "duplicate-past",
    "unsorted-past",
    "invalid-past",
    "self-loop",
    "cycle",
    "nontransitive",
    "missing-fixed",
    "duplicate-observation",
    "missing-successor",
    "one-frame",
    "too-few",
    "too-many",
    "overflow",
    "missing-singleton-control",
)


@pytest.mark.parametrize("case", INVALID_PROBLEMS)
def test_analyze_rejects_malformed_native_coercing_and_open_models(executors, case):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problem(case))


@pytest.mark.parametrize(
    "question,cid,rates",
    [
        ("unknown", 0, ["1/2", "1/2"]),
        (StringSubclass("chain_counts"), 0, ["1/2", "1/2"]),
        ("chain_counts", False, ["1/2", "1/2"]),
        ("chain_counts", IntSubclass(0), ["1/2", "1/2"]),
        ("chain_counts", -1, ["1/2", "1/2"]),
        ("chain_counts", 9999, ["1/2", "1/2"]),
        ("chain_counts", 0.0, ["1/2", "1/2"]),
        ("chain_counts", 0, ("1/2", "1/2")),
        ("chain_counts", 0, ListSubclass(["1/2", "1/2"])),
        ("chain_counts", 0, ["1/2"]),
        ("chain_counts", 0, ["1/2", "1/2", "0"]),
        ("chain_counts", 0, [F(1, 2), "1/2"]),
        ("chain_counts", 0, [0.5, "1/2"]),
        ("chain_counts", 0, [True, "1/2"]),
        ("chain_counts", 0, [StringSubclass("1/2"), "1/2"]),
        ("chain_counts", 0, ["2/4", "1/2"]),
        ("chain_counts", 0, ["0.5", "1/2"]),
        ("chain_counts", 0, ["-0", "1/2"]),
        ("chain_counts", 0, ["-1/2", "1/2"]),
        ("chain_counts", 0, ["3/2", "1/2"]),
        ("chain_counts", 0, ["1/0", "1/2"]),
        ("chain_counts", 0, [str(1 << 4096), "1/2"]),
    ],
)
def test_predict_rejects_invalid_question_class_and_exact_rates(
    executors, micro_analyses, question, cid, rates
):
    for module, a in zip(executors, micro_analyses, strict=True):
        with pytest.raises(ValueError):
            module.predict(a["consumer"], question, cid, rates)


def invalid_consumer(consumer, case):
    c = copy.deepcopy(consumer)
    if case == "subclass":
        return DictSubclass(c)
    if case == "key-subclass":
        c[StringSubclass("schema_version")] = c.pop("schema_version")
    elif case == "extra":
        c["raw_states"] = []
    elif case == "schema":
        c["schema_version"] = "other"
    elif case == "model-digest":
        c["model_sha256"] = "bad"
    elif case == "class-digest":
        c["state_classes_sha256"] = "bad"
    elif case == "count-bool":
        c["class_count"] = True
    elif case == "row-missing":
        c["quotient_rows"].pop()
    elif case == "row-id-bool":
        c["quotient_rows"][0]["class_id"] = False
    elif case == "representative-bool":
        c["quotient_rows"][0]["representative_state"] = False
    elif case == "representative-not-zero":
        for row in c["quotient_rows"]:
            row["representative_state"] += 1
    elif case == "representative-order":
        rows = c["quotient_rows"]
        rows[1]["representative_state"], rows[2]["representative_state"] = (
            rows[2]["representative_state"],
            rows[1]["representative_state"],
        )
    elif case == "target-bool":
        c["quotient_rows"][0]["transitions"][0]["target_class"] = False
    elif case == "target-range":
        c["quotient_rows"][0]["transitions"][0]["target_class"] = c["class_count"]
    elif case == "coefficient-bool":
        c["quotient_rows"][0]["transitions"][0]["coefficients"][0][0] = True
    elif case == "coefficient-float":
        c["quotient_rows"][0]["transitions"][0]["coefficients"][0][0] = 1.0
    elif case == "coefficient-overflow":
        c["quotient_rows"][0]["transitions"][0]["coefficients"][0][0] = 1 << 4096
    elif case == "table-shape":
        c["quotient_rows"][0]["transitions"][0]["coefficients"].pop()
    elif case == "row-normalization":
        c["quotient_rows"][0]["transitions"][0]["coefficients"][0][0] += 1
    elif case == "duplicate-atom":
        c["quotient_rows"][0]["transitions"] *= 2
    elif case == "negative-selected":
        row = c["quotient_rows"][0]
        positive, negative = zero(), zero()
        positive[0][0], negative[0][0] = 2, -1
        row["transitions"] = [
            {"target_class": 0, "coefficients": positive},
            {"target_class": 1, "coefficients": negative},
        ]
    elif case == "missing-observable":
        c["observables"].pop()
    elif case == "duplicate-observable":
        c["observables"][1] = copy.deepcopy(c["observables"][0])
    elif case == "measurable-int":
        c["observables"][0]["measurable"] = 1
    elif case == "value-count":
        c["observables"][0]["class_values"].pop()
    elif case == "value-bool":
        c["observables"][0]["class_values"][0][0] = True
    elif case == "value-n0":
        c["observables"][0]["class_values"][0][0] = 0
    elif case == "value-n1":
        c["observables"][0]["class_values"][0][1] = 7
    elif case == "value-n2":
        c["observables"][0]["class_values"][0][2] = 16
    elif case == "value-n3":
        c["observables"][0]["class_values"][0][3] = 21
    elif case == "value-m":
        c["observables"][1]["class_values"][0] = 10
    elif case == "value-t":
        c["observables"][2]["class_values"][0] = 10
    elif case == "value-tuple":
        c["observables"][0]["class_values"][0] = tuple(c["observables"][0]["class_values"][0])
    elif case == "failure-inconsistent":
        c["observables"][0]["first_failure"] = {
            "class_id": 0,
            "left_state": 0,
            "right_state": 1,
            "left_value": 0,
            "right_value": 1,
        }
    else:
        raise AssertionError(case)
    return c


@pytest.mark.parametrize(
    "case",
    [
        "subclass",
        "key-subclass",
        "extra",
        "schema",
        "model-digest",
        "class-digest",
        "count-bool",
        "row-missing",
        "row-id-bool",
        "representative-bool",
        "representative-not-zero",
        "representative-order",
        "target-bool",
        "target-range",
        "coefficient-bool",
        "coefficient-float",
        "coefficient-overflow",
        "table-shape",
        "row-normalization",
        "duplicate-atom",
        "negative-selected",
        "missing-observable",
        "duplicate-observable",
        "measurable-int",
        "value-count",
        "value-bool",
        "value-n0",
        "value-n1",
        "value-n2",
        "value-n3",
        "value-m",
        "value-t",
        "value-tuple",
        "failure-inconsistent",
    ],
)
def test_predict_rejects_malformed_payload_without_claiming_artifact_authentication(
    executors, micro_analyses, case
):
    for module, a in zip(executors, micro_analyses, strict=True):
        with pytest.raises(ValueError):
            module.predict(invalid_consumer(a["consumer"], case), "chain_counts", 0, ["1/2", "1/2"])


def test_optimized_guards_and_valid_summary_prediction_execute_without_assertions(tmp_path):
    code = r"""
import importlib.util,json,pathlib,sys
base=pathlib.Path(sys.argv[1]); problem=json.loads(sys.argv[2])
class S(str): pass
class I(int): pass
class L(list): pass
class D(dict): pass
def rejected(fn):
    try: fn()
    except ValueError: return
    raise RuntimeError("optimized guard accepted an invalid input")
for index, filename in enumerate(("closure.py","reference_qr05p.py")):
    name="_qr05p_optimized_"+str(index)
    spec=importlib.util.spec_from_file_location(name,base/filename)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    a=module.analyze(problem)
    if a["counts"]["states"]!=4: raise RuntimeError("valid helper failed")
    p=module.predict(a["consumer"],"chain_counts",0,["1/2","1/2"])
    if p["outcomes"]!=[{"value":[1,0,0,0],"probability":"1"}]: raise RuntimeError("valid prediction failed")
    bad=json.loads(json.dumps(problem));bad["model"]["states"][0]["frame_id"]=False
    rejected(lambda:module.analyze(bad))
    badkey=dict(problem);badkey[S("family")]=badkey.pop("family")
    rejected(lambda:module.analyze(badkey))
    rejected(lambda:module.analyze(D(problem)))
    rejected(lambda:module.predict(a["consumer"],"chain_counts",False,["1/2","1/2"]))
    rejected(lambda:module.predict(a["consumer"],S("chain_counts"),0,["1/2","1/2"]))
    rejected(lambda:module.predict(a["consumer"],"chain_counts",I(0),["1/2","1/2"]))
    rejected(lambda:module.predict(a["consumer"],"chain_counts",0,L(["1/2","1/2"])))
    rejected(lambda:module.predict(a["consumer"],"chain_counts",0,[S("1/2"),"1/2"]))
    rejected(lambda:module.predict(a["consumer"],"chain_counts",0,["2/4","1/2"]))
    rejected(lambda:module.predict(a["consumer"],"named_relation_1_7",0,["1/2","1/2"]))
    badc=json.loads(json.dumps(a["consumer"]));badc["quotient_rows"][0]["transitions"][0]["coefficients"][0][0]=True
    rejected(lambda:module.predict(badc,"chain_counts",0,["1/2","1/2"]))
print("optimized valid and explicit guards passed")
"""
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-O",
            "-X",
            f"pycache_prefix={tmp_path / 'external-pycache'}",
            "-c",
            code,
            str(HERE),
            json.dumps(micro_problem()),
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "optimized valid and explicit guards passed"


def test_whole_aggregate_native_roundtrip_and_exact_dependency_boundaries(
    aggregate, analyses, independent, problem
):
    runner, suite = aggregate
    assert wire(json.loads(wire(suite))) == wire(suite)
    assert runner.canonical(suite) == wire(suite)
    assert wire(suite["input"]) == wire(problem)
    assert wire(suite["analysis"]) == wire(analyses[0])
    assert set(suite) == {
        "input",
        "analysis",
        "audit",
        "prior_bridge",
        "controls",
        "rejected_fixture_indices",
        "research_base_commit",
        "claim",
        "coarsest_closed_C_refinement_verified",
        "H_equal_to_coarsest_refinement",
        "input_is_declared_prior_observation_projection",
        "unrestricted_minimality_claimed",
        "minimum_memory_or_runtime_claimed",
        "unseen_domain_membership_from_matching_H_key",
        "all_labeled_graph_queries_supported",
        "adaptive_or_correlated_stages_tested",
        "empirical_data_used",
        "ret_integration_tested",
        "lean_proof_completed",
        "gravity_derived",
        "physical_time_identified_with_thinning",
        "prior_source_alias_universe_regenerated",
        "entire_O_suite_replayed",
        "bounds",
        "totals",
    }
    assert suite["research_base_commit"] == "35831db06b3f5089fdb36d066cfb741b1c2984cb"
    assert suite["coarsest_closed_C_refinement_verified"] is True
    assert (
        suite["H_equal_to_coarsest_refinement"]
        is analyses[0]["refinement"]["comparison"]["same_memberships_as_H"]
    )
    assert suite["input_is_declared_prior_observation_projection"] is True
    for key in (
        "unrestricted_minimality_claimed",
        "minimum_memory_or_runtime_claimed",
        "unseen_domain_membership_from_matching_H_key",
        "all_labeled_graph_queries_supported",
        "adaptive_or_correlated_stages_tested",
        "empirical_data_used",
        "ret_integration_tested",
        "lean_proof_completed",
        "gravity_derived",
        "physical_time_identified_with_thinning",
        "prior_source_alias_universe_regenerated",
        "entire_O_suite_replayed",
    ):
        assert suite[key] is False
    a = analyses[0]
    assert suite["audit"] == {
        "verified": True,
        "model_states": 2470,
        "fine_coefficient_cells": 16 * 99180,
        "refinement_rounds": len(independent["rounds"]),
        "round_coefficient_cells": a["refinement"]["counts"]["round_coefficient_cells"],
        "semigroup_coefficient_cells": independent["semigroup"]["totals"]["coefficient_cells"],
        "consumer_fine_coefficient_cells": a["counts"]["consumer_fine_coefficient_cells"],
        "consumer_prediction_checks": a["consumer_audit"]["prediction_checks"],
        "coarsest_argument_premises_verified": True,
        "earlier_O_certificates_recomputed": False,
    }
    assert suite["prior_bridge"] == {
        "prior_artifact": "qr-05o-path-observable-2026-09-06/results.json",
        "matched_states": 2470,
        "model_projection_equal": True,
        "all_features_equal": True,
        "C_H_memberships_equal": True,
        "fine_kernel_sha256": digest(independent["fine"]),
        "declared_observation_input_dependency": True,
        "source_alias_universe_regenerated": False,
        "whole_O_analysis_reproduced": False,
        "earlier_O_expectation_certificates_recomputed": False,
    }
    chosen = sorted({0, a["consumer"]["class_count"] // 2, a["consumer"]["class_count"] - 1})
    assert suite["controls"] == {
        "public_class_ids": chosen,
        "public_rate_points": 22,
        "public_prediction_calls": 2 * len(chosen) * 22 * a["counts"]["measurable_questions"],
        "nonmeasurable_questions_rejected": a["consumer_audit"]["nonmeasurable_questions"],
        "fine_records_supplied_to_predict": False,
        "verified": True,
    }
    assert suite["bounds"] == {
        "states": 2470,
        "fine_atoms": 99180,
        "transition_degree": [3, 3],
        "composition_degree": [3, 3, 3, 3],
        "exact_component_bits": 4096,
        "working_output_bytes": 512 * 1024 * 1024,
        "artifact_bytes": 64 * 1024 * 1024,
    }
    assert suite["rejected_fixture_indices"] == list(range(len(runner.invalid_fixtures())))
    assert suite["totals"] == {
        **a["counts"],
        "rejected_fixtures": len(runner.invalid_fixtures()),
        "public_prediction_calls": suite["controls"]["public_prediction_calls"],
    }
    assert len(runner.SOURCES) == 6 and len(runner.PRIORS) == 20


@pytest.mark.parametrize(
    "bad",
    [
        (1,),
        {"nested": {"value": 1.0}},
        {False: 1},
        {"nested": [StringSubclass("1")]},
        {StringSubclass("key"): 1},
    ],
)
def test_runner_native_wire_rejects_tuples_floats_and_subclasses(aggregate, bad):
    runner, _ = aggregate
    with pytest.raises(ValueError):
        runner.require_wire(bad)


@pytest.mark.parametrize(
    "left,right", [({"nested": [True]}, {"nested": [1]}), ([0, {"a": False}], [0, {"a": 0}])]
)
def test_runner_wire_equality_is_type_exact(aggregate, left, right):
    runner, _ = aggregate
    assert left == right
    with pytest.raises(ValueError):
        runner.require_same_wire(left, right, "bool/int substitution")


def mutate_analysis(a, case):
    if case == "model-digest":
        a["model_sha256"] = "0" * 64
    elif case == "feature-state-bool":
        a["features"][0]["state_id"] = False
    elif case == "feature-count-bool":
        a["features"][0]["chain_counts"][0] = True
    elif case == "feature-pair":
        a["features"][0]["pair_graded"][0][0][0][0] += 1
    elif case == "fine-digest":
        a["fine_kernel"]["sha256"] = "0" * 64
    elif case == "round-digest":
        a["refinement"]["rounds"][0]["pushed_rows_sha256"] = "0" * 64
    elif case == "round-missing":
        a["refinement"]["rounds"].pop()
    elif case == "round-extra-stable":
        a["refinement"]["rounds"].append(copy.deepcopy(a["refinement"]["rounds"][-1]))
    elif case == "round-noncanonical-id":
        a["refinement"]["rounds"][0]["state_classes"][0] = 1
    elif case == "old-class-merge":
        a["refinement"]["rounds"][0]["state_classes"] = [0] * len(a["features"])
    elif case == "stable-int":
        a["refinement"]["rounds"][-1]["stable"] = 1
    elif case == "fake-separation":
        a["refinement"]["rounds"][-1]["separations"] = [
            {
                "parent_class_id": 0,
                "child_class_id": 1,
                "left_state": 0,
                "right_state": 1,
                "target_class": 0,
                "left_coefficients": zero(),
                "right_coefficients": zero(),
                "first_distinguishing_rates": ["0", "0"],
            }
        ]
    elif case == "comparison-bool-int":
        a["refinement"]["comparison"]["same_memberships_as_H"] = 1
    elif case == "comparison-false-H":
        a["refinement"]["comparison"]["same_memberships_as_H"] = not a["refinement"]["comparison"][
            "same_memberships_as_H"
        ]
    elif case == "comparison-class-map":
        a["refinement"]["comparison"]["R_to_C"][0] = 1
    elif case == "quotient":
        a["refinement"]["quotient_rows"][0]["transitions"][0]["coefficients"][0][0] += 1
    elif case == "semigroup":
        a["refinement"]["semigroup"]["rows"][0]["max_abs_residual"] = 1
    elif case == "false-measurability":
        a["consumer"]["observables"][-1].update(
            measurable=True, class_values=[0] * a["consumer"]["class_count"], first_failure=None
        )
    elif case == "measurable-class-value":
        a["consumer"]["observables"][0]["class_values"][0][0] += 1
    elif case == "marginal-law":
        a["consumer_audit"]["marginals"][0]["rows"][0]["outcomes"][0]["coefficients"][0][0] += 1
    elif case == "marginal-cells":
        a["consumer_audit"]["marginals"][0]["fine_coefficient_cells"] += 16
    elif case == "named-control":
        a["consumer_audit"]["named_singleton_control"]["half_probabilities"][0] = "0"
    elif case == "prediction-checks":
        a["consumer_audit"]["prediction_checks"] += 1
    elif case == "extra":
        a["general_minimality"] = True
    elif case == "overflow":
        a["counts"]["states"] = 1 << 4096
    else:
        raise AssertionError(case)


@pytest.mark.parametrize(
    "case",
    [
        "model-digest",
        "feature-state-bool",
        "feature-count-bool",
        "feature-pair",
        "fine-digest",
        "round-digest",
        "round-missing",
        "round-extra-stable",
        "round-noncanonical-id",
        "old-class-merge",
        "stable-int",
        "fake-separation",
        "comparison-bool-int",
        "comparison-false-H",
        "comparison-class-map",
        "quotient",
        "semigroup",
        "false-measurability",
        "measurable-class-value",
        "marginal-law",
        "marginal-cells",
        "named-control",
        "prediction-checks",
        "extra",
        "overflow",
    ],
)
def test_independent_runner_audit_rejects_corrupt_evidence_on_small_closed_case(
    aggregate, micro_analyses, case
):
    runner, _ = aggregate
    changed = copy.deepcopy(micro_analyses[0])
    mutate_analysis(changed, case)
    with pytest.raises(ValueError):
        runner.check_analysis(changed, micro_problem()["model"])


@pytest.mark.parametrize(
    "case", ["early-stop", "missing-separation", "reordered-rounds", "same-size-wrong-fibers"]
)
def test_real_domain_audit_rejects_false_refinement_certificates(
    aggregate, analyses, problem, case
):
    runner, _ = aggregate
    a = copy.deepcopy(analyses[0])
    r = a["refinement"]
    assert len(r["rounds"]) >= 2 and r["rounds"][0]["separations"]
    if case == "early-stop":
        r["rounds"] = r["rounds"][:1]
        r["rounds"][0]["stable"] = True
        r["strict_rounds"] = r["final_round"] = 0
    elif case == "missing-separation":
        r["rounds"][0]["separations"].pop()
    elif case == "reordered-rounds":
        r["rounds"][0], r["rounds"][1] = r["rounds"][1], r["rounds"][0]
    else:
        groups = [group for group in r["classes"] if len(group["members"]) > 1]
        left, right = next(
            (a, b) for a, b in combinations(groups, 2) if len(a["members"]) == len(b["members"])
        )
        u, v = left["members"][-1], right["members"][-1]
        left["members"].remove(u)
        left["members"].append(v)
        right["members"].remove(v)
        right["members"].append(u)
        left["members"].sort()
        right["members"].sort()
        r["state_classes"][u], r["state_classes"][v] = r["state_classes"][v], r["state_classes"][u]
        assert all(
            group["members"][0]
            == analyses[0]["refinement"]["classes"][group["class_id"]]["members"][0]
            for group in (left, right)
        )
        assert sorted(sid for group in r["classes"] for sid in group["members"]) == list(
            range(2470)
        )
    with pytest.raises(ValueError):
        runner.check_analysis(a, problem["model"])


@pytest.mark.parametrize(
    "case",
    [
        "raw-frame-bool",
        "raw-past-bool",
        "feature-bool",
        "fine-digest",
        "C-membership",
        "H-membership",
    ],
)
def test_prior_bridge_rejects_type_coercion_or_changed_observation_evidence(
    aggregate, analyses, problem, case
):
    runner, _ = aggregate
    a, model = copy.deepcopy(analyses[0]), copy.deepcopy(problem["model"])
    if case == "raw-frame-bool":
        model["states"][0]["frame_id"] = False
    elif case == "raw-past-bool":
        model["states"][0]["past"][1][0] = False
    elif case == "feature-bool":
        a["features"][0]["chain_counts"][0] = True
    elif case == "fine-digest":
        a["fine_kernel"]["sha256"] = "0" * 64
    elif case == "C-membership":
        a["partitions"]["C"]["state_classes"][0] = 1
    elif case == "H-membership":
        a["partitions"]["H"]["state_classes"][0] = 1
    with pytest.raises(ValueError):
        runner.prior_bridge(a, model)


def test_audit_cache_is_exact_model_content_not_mutable_identity(aggregate, micro_analyses):
    runner, _ = aggregate
    model = micro_problem()["model"]
    a = copy.deepcopy(micro_analyses[0])
    expected = runner.check_analysis(a, model)
    assert expected["verified"] is True
    model["states"][0]["frame_id"] = False
    with pytest.raises(ValueError):
        runner.check_analysis(a, model)
    model["states"][0]["frame_id"] = 0
    model["states"][1]["past"][2] = [1]
    with pytest.raises(ValueError):
        runner.check_analysis(a, model)
    model["states"][1]["past"][2] = [0, 1]
    assert runner.check_analysis(a, model) == expected
    a["features"][0]["chain_counts"][0] = True
    with pytest.raises(ValueError):
        runner.check_analysis(a, model)
    a["features"][0]["chain_counts"][0] = 1
    assert runner.check_analysis(a, model) == expected


def test_predict_revalidates_mutated_payload_after_success(executors, micro_analyses):
    for module, a in zip(executors, micro_analyses, strict=True):
        payload = copy.deepcopy(a["consumer"])
        expected = module.predict(payload, "chain_counts", 0, ["1/2", "1/2"])
        payload["quotient_rows"][0]["transitions"][0]["coefficients"][0][0] = True
        with pytest.raises(ValueError):
            module.predict(payload, "chain_counts", 0, ["1/2", "1/2"])
        payload["quotient_rows"][0]["transitions"][0]["coefficients"][0][0] = 1
        assert module.predict(payload, "chain_counts", 0, ["1/2", "1/2"]) == expected


@pytest.mark.parametrize(
    "text", ["1e-10000000", "1e999999999", "1e-1", "NaN", "1 /2", "١", "1" * 3001]
)
def test_rate_grammar_and_length_reject_before_fraction_construction(
    executors, micro_analyses, monkeypatch, text
):
    def forbidden(*args, **kwargs):
        raise AssertionError("unsafe/noncanonical rate reached rational construction")

    for module, a in zip(executors, micro_analyses, strict=True):
        consumer = copy.deepcopy(a["consumer"])
        module.predict(consumer, "chain_counts", 0, ["1/2", "1/2"])
        with monkeypatch.context() as patch:
            patch.setattr(module, "Fraction", forbidden)
            if hasattr(module, "F"):
                patch.setattr(module, "F", forbidden)
            with pytest.raises(ValueError):
                module.predict(consumer, "chain_counts", 0, [text, "1/2"])


def test_consumer_fine_atom_cap_is_enforced_without_duplicate_target_shortcuts(
    executors, micro_analyses
):
    count = 316
    assert count**2 > 99180
    one, nil = zero(), zero()
    one[0][0] = 1
    payload = copy.deepcopy(micro_analyses[0]["consumer"])
    payload["class_count"] = count
    payload["quotient_rows"] = [
        {
            "class_id": cid,
            "representative_state": cid,
            "transitions": [
                {"target_class": target, "coefficients": one if target == cid else nil}
                for target in range(count)
            ],
        }
        for cid in range(count)
    ]
    for item in payload["observables"]:
        if item["measurable"]:
            item["class_values"] = [copy.deepcopy(item["class_values"][0]) for _ in range(count)]
    for module in executors:
        with pytest.raises(ValueError):
            module.predict(payload, "chain_counts", 0, ["1/2", "1/2"])


def test_prediction_rational_output_respects_exact_component_bound(executors, micro_analyses):
    rate = "1/" + str((1 << 1366) - 1)
    assert F(rate).denominator.bit_length() <= 4096 < (F(rate) ** 3).denominator.bit_length()
    p, q = zero(), zero()
    p[3][0], q[0][0], q[3][0] = 1, 1, -1
    for module, a in zip(executors, micro_analyses, strict=True):
        consumer = copy.deepcopy(a["consumer"])
        consumer["quotient_rows"][1]["transitions"] = [
            {"target_class": 0, "coefficients": q},
            {"target_class": 1, "coefficients": p},
        ]
        with pytest.raises(ValueError):
            module.predict(consumer, "chain_counts", 1, [rate, "1"])
