"""Independent R subset-census, exact-basis and nested-subset tests.

The raw Q model is a declared byte-pinned input; prior executors are never
imported. Helpers are statically carried from this test author's P/Q lineage.
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
from itertools import combinations, product
from math import comb
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
F = Fraction
Q_SHA = "1e9b9443ee5d55cd888d5ea62e594fad197ca0baeecfee1f1efac34ada8125aa"
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


def replaced(tree, path, value):
    """Copy only ancestors of one changed cell; do not mutate shared fixtures."""
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = replaced(tree[path[0]], path[1:], value)
    return answer


@pytest.fixture(scope="session")
def pinned_q():
    path = HERE.parent / "qr-05q-three-layer-portability-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 13821257 and hashlib.sha256(raw).hexdigest() == Q_SHA
    envelope = json.loads(raw)
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


@pytest.fixture(scope="session")
def problem(pinned_q):
    domain = pinned_q["analysis"]["domain"]
    return {
        "schema_version": "det8-qr05r-problem-v1",
        "family": "qr05r_deletion_profile",
        "model": {
            "frames": copy.deepcopy(domain["frames"]),
            "states": copy.deepcopy(domain["states"]),
        },
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05r_test_direct", "deletion_profile.py"),
        private_module("_qr05r_test_reference", "reference_qr05r.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors, problem):
    return tuple(module.analyze(problem) for module in executors)


@pytest.fixture(scope="session")
def aggregate():
    module = private_module("_qr05r_test_aggregate", "study.py")
    return module, module.run_suite()


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


@cache
def basis_inverse(size):
    # Exact Gaussian elimination of the independently constructed expansion
    # matrix, not the production closed-form inverse or an interpolation grid.
    matrix = [
        [F(kernel(size, 0, rank, 0)[power][0]) for rank in range(size + 1)]
        + [F(int(power == col)) for col in range(size + 1)]
        for power in range(size + 1)
    ]
    for pivot in range(size + 1):
        assert matrix[pivot][pivot] != 0
        scale = matrix[pivot][pivot]
        matrix[pivot] = [v / scale for v in matrix[pivot]]
        for row in range(size + 1):
            if row != pivot:
                factor = matrix[row][pivot]
                matrix[row] = [
                    a - factor * b for a, b in zip(matrix[row], matrix[pivot], strict=True)
                ]
    assert [row[: size + 1] for row in matrix] == [
        [int(a == b) for b in range(size + 1)] for a in range(size + 1)
    ]
    result = tuple(tuple(row[size + 1 :]) for row in matrix)
    assert all(c.denominator == 1 for row in result for c in row)
    return result


@cache
def inverted_tuple(power, sizes):
    odd, even = sizes
    left = tuple(tuple(int(c) for c in row) for row in basis_inverse(odd))
    right = tuple(tuple(int(c) for c in row) for row in basis_inverse(even))
    result = zero()
    for o, e in product(range(odd + 1), range(even + 1)):
        result[o][e] = sum(
            left[o][i] * right[e][j] * power[i][j] for i, j in product(range(o + 1), range(e + 1))
        )
    return tuple(tuple(row) for row in result)


def invert(power, sizes):
    return [list(row) for row in inverted_tuple(tuple(tuple(row) for row in power), tuple(sizes))]


def expand(grades, sizes):
    result = zero()
    for o, e in product(range(sizes[0] + 1), range(sizes[1] + 1)):
        if not grades[o][e]:
            continue
        basis = kernel(*sizes, o, e)
        for i, j in product(range(4), repeat=2):
            result[i][j] += grades[o][e] * basis[i][j]
    return result


def integer_composition(rows):
    reports = []
    for row in rows:
        odd, even = row["parent_color_sizes"]
        direct = {atom["target_class"]: atom for atom in row["transitions"]}
        nested = {}
        for first in row["transitions"]:
            k, l = first["retained_color_sizes"]
            middle = rows[first["target_class"]]
            assert middle["parent_color_sizes"] == [k, l]
            for second in middle["transitions"]:
                target = second["target_class"]
                nested.setdefault(target, zero())[k][l] += (
                    first["multiplicity"] * second["multiplicity"]
                )
        assert set(nested) == set(direct)
        total = 0
        for target, table in nested.items():
            atom = direct[target]
            m, n = atom["retained_color_sizes"]
            expected = [
                [
                    atom["multiplicity"] * choose(odd - m, k - m) * choose(even - n, l - n)
                    for l in range(4)
                ]
                for k in range(4)
            ]
            assert table == expected
            total += sum(map(sum, table))
        assert total == 3 ** (odd + even)
        reports.append(
            {
                "class_id": row["class_id"],
                "final_targets": len(direct),
                "rank_cells": 16 * len(direct),
                "nested_pairs": total,
                "max_abs_residual": 0,
            }
        )
    return {
        "verified": True,
        "rows": reports,
        "totals": {
            key: sum(row[key] for row in reports)
            for key in ("final_targets", "rank_cells", "nested_pairs", "max_abs_residual")
        },
    }


@pytest.fixture(scope="session")
def independent(problem):
    model = problem["model"]
    frames, states = model["frames"], model["states"]
    fs = [observed_features(s, frames[s["frame_id"]]) for s in states]
    keys = []
    for state, feature in zip(states, fs, strict=True):
        frame = frames[state["frame_id"]]
        keys.append(
            [
                [frame["density"], frame["fixed"], frame["eligible"]],
                feature["pair_graded"],
                feature["motif_count"],
                feature["path_count"],
            ]
        )
    part = partition(keys)
    lookup = {state_key(s["frame_id"], s["kept"], s["past"]): s["state_id"] for s in states}
    fine, profiles = [], []
    for state, feature in zip(states, fs, strict=True):
        frame = frames[state["frame_id"]]
        eligible = sorted(set(state["kept"]) & set(frame["eligible"]))
        rel = relation_of(state)
        atoms, census = [], {}
        for mask in range(1 << len(eligible)):
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(eligible) if mask & (1 << bit)]
            )
            past = [[i for i, v in enumerate(kept) if (v, w) in rel] for w in kept]
            target = lookup[state_key(state["frame_id"], kept, past)]
            atoms.append(
                {
                    "target_state": target,
                    "coefficients": kernel(*feature["color_sizes"], *fs[target]["color_sizes"]),
                }
            )
            cid = part["state_classes"][target]
            rep = part["classes"][cid]["members"][0]
            assert fs[target]["color_sizes"] == fs[rep]["color_sizes"]
            census[cid] = census.get(cid, 0) + 1
        fine.append(
            {
                "state_id": state["state_id"],
                "transitions": sorted(atoms, key=lambda x: x["target_state"]),
            }
        )
        profiles.append(
            {
                "state_id": state["state_id"],
                "parent_color_sizes": feature["color_sizes"],
                "transitions": [
                    {
                        "target_class": cid,
                        "retained_color_sizes": fs[part["classes"][cid]["members"][0]][
                            "color_sizes"
                        ],
                        "multiplicity": count,
                    }
                    for cid, count in sorted(census.items())
                ],
            }
        )
    power_rows = pushed(fine, part["state_classes"])
    witness, comparisons = None, 0
    for group in part["classes"]:
        left = group["members"][0]
        left_map = {atom["target_class"]: atom for atom in profiles[left]["transitions"]}
        for right in group["members"][1:]:
            comparisons += 1
            assert profiles[right]["parent_color_sizes"] == profiles[left]["parent_color_sizes"]
            right_map = {atom["target_class"]: atom for atom in profiles[right]["transitions"]}
            unequal = [
                cid
                for cid in sorted(left_map.keys() | right_map.keys())
                if left_map.get(cid, {"multiplicity": 0})["multiplicity"]
                != right_map.get(cid, {"multiplicity": 0})["multiplicity"]
            ]
            if unequal and witness is None:
                cid = unequal[0]
                retained = (left_map.get(cid) or right_map[cid])["retained_color_sizes"]
                lm, rm = (
                    left_map.get(cid, {"multiplicity": 0})["multiplicity"],
                    right_map.get(cid, {"multiplicity": 0})["multiplicity"],
                )
                rates = next(
                    [str(x), str(y)]
                    for x, y in NODES
                    if direct_probability(*profiles[left]["parent_color_sizes"], *retained, x, y)
                    * (lm - rm)
                )
                witness = {
                    "class_id": group["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "target_class": cid,
                    "retained_color_sizes": retained,
                    "left_multiplicity": lm,
                    "right_multiplicity": rm,
                    "first_distinguishing_rates": rates,
                }
    cp = (
        []
        if witness
        else [
            {
                "class_id": group["class_id"],
                "representative_state": group["members"][0],
                "parent_color_sizes": profiles[group["members"][0]]["parent_color_sizes"],
                "transitions": profiles[group["members"][0]]["transitions"],
            }
            for group in part["classes"]
        ]
    )
    quotient = (
        []
        if witness
        else [
            {
                "class_id": group["class_id"],
                "representative_state": group["members"][0],
                "transitions": power_rows[group["members"][0]]["transitions"],
            }
            for group in part["classes"]
        ]
    )
    atoms = sum(len(row["transitions"]) for row in profiles)
    assert len(states) == 4447 and sum(len(row["transitions"]) for row in fine) == 168388
    a = {
        "model_sha256": digest(model),
        "features": fs,
        "partition": part,
        "profiles": profiles,
        "closure": {
            "closed": witness is None,
            "classes_checked": len(part["classes"]),
            "member_comparisons": comparisons,
            "witness": witness,
        },
        "class_profiles": cp,
        "conversion": {
            "fine_kernel_sha256": digest(fine),
            "pushed_rows_sha256": digest(power_rows),
            "quotient_rows_sha256": digest(quotient) if cp else None,
            "profile_cells": 16 * atoms,
            "power_cells": 16 * atoms,
            "normalization_cells": 16 * len(states),
            "max_abs_residual": 0,
        },
        "composition": integer_composition(cp) if cp else None,
        "evaluation": {
            "rate_points": 22,
            "profile_atoms": atoms,
            "probability_evaluations": 22 * atoms,
            "normalization_rows": 22 * len(states),
            "max_abs_residual": 0,
        },
        "counts": {
            "states": len(states),
            "classes": len(part["classes"]),
            "fine_atoms": 168388,
            "profile_atoms": atoms,
            "class_profile_atoms": sum(len(row["transitions"]) for row in cp),
        },
    }
    return a, fine, power_rows, quotient


def test_raw_model_dependency_and_complete_independent_result(
    analyses, independent, problem, pinned_q
):
    expected, fine, pushed_rows, quotient = independent
    assert set(problem["model"]) == {"frames", "states"}
    assert wire(problem["model"]) == wire(
        {key: pinned_q["analysis"]["domain"][key] for key in ("frames", "states")}
    )
    assert all(
        set(state) == {"state_id", "frame_id", "kept", "past"}
        for state in problem["model"]["states"]
    )
    assert wire(analyses[0]) == wire(analyses[1]) == wire(expected)
    assert wire(json.loads(wire(analyses[0]))) == wire(analyses[0])
    assert len(wire(analyses[0])) < 64 * 1024 * 1024
    assert set(analyses[0]) == {
        "model_sha256",
        "features",
        "partition",
        "profiles",
        "closure",
        "class_profiles",
        "conversion",
        "composition",
        "evaluation",
        "counts",
    }
    q = pinned_q["analysis"]
    assert wire(expected["features"]) == wire(q["features"])
    assert wire(expected["partition"]) == wire(q["partition"])
    assert digest(fine) == q["fine_kernel"]["sha256"]
    assert wire(pushed_rows) == wire(q["pushed_rows"])
    assert wire(quotient) == wire(q["quotient_rows"])
    assert expected["closure"]["closed"] is q["closure"]["closed"]


def test_H_fixes_parent_and_child_rank_with_fixed_three_excluded(independent, problem):
    a = independent[0]
    fs = a["features"]
    for state, feature, row in zip(problem["model"]["states"], fs, a["profiles"], strict=True):
        frame = problem["model"]["frames"][state["frame_id"]]
        raw = sorted(set(state["kept"]) & set(frame["eligible"]))
        assert feature["color_sizes"] == [sum(v % 2 for v in raw), sum(v % 2 == 0 for v in raw)]
        assert row["parent_color_sizes"] == [
            feature["pair_graded"][0][1][1][0],
            feature["pair_graded"][0][1][0][1],
        ]
        assert feature["mean_graded"][1][0][0] == int(state["frame_id"] == 1)
        for atom in row["transitions"]:
            group = a["partition"]["classes"][atom["target_class"]]
            assert atom["retained_color_sizes"] == [
                group["key"][1][0][1][1][0],
                group["key"][1][0][1][0][1],
            ]
            assert all(
                fs[sid]["color_sizes"] == atom["retained_color_sizes"] for sid in group["members"]
            )


def test_every_profile_is_a_positive_rankwise_subset_census(independent):
    a, fine, _, _ = independent
    for row, raw in zip(a["profiles"], fine, strict=True):
        odd, even = row["parent_color_sizes"]
        grades = zero()
        assert [atom["target_class"] for atom in row["transitions"]] == sorted(
            {atom["target_class"] for atom in row["transitions"]}
        )
        for atom in row["transitions"]:
            o, e = atom["retained_color_sizes"]
            count = atom["multiplicity"]
            assert type(count) is int and 1 <= count <= 9
            assert 0 <= o <= odd <= 3 and 0 <= e <= even <= 3
            assert count <= comb(odd, o) * comb(even, e)
            grades[o][e] += count
        assert grades == [[choose(odd, o) * choose(even, e) for e in range(4)] for o in range(4)]
        assert sum(map(sum, grades)) == len(raw["transitions"]) == 2 ** (odd + even)
        assert len(row["transitions"]) <= 64


def test_complete_grade_and_power_tables_are_bijective_at_fixed_parent_degree(independent):
    a, _, powers, _ = independent
    cells = 0
    for row, power_row in zip(a["profiles"], powers, strict=True):
        assert row["state_id"] == power_row["state_id"]
        assert [atom["target_class"] for atom in row["transitions"]] == [
            atom["target_class"] for atom in power_row["transitions"]
        ]
        for atom, power in zip(row["transitions"], power_row["transitions"], strict=True):
            grades = zero()
            o, e = atom["retained_color_sizes"]
            grades[o][e] = atom["multiplicity"]
            assert expand(grades, row["parent_color_sizes"]) == power["coefficients"]
            assert invert(power["coefficients"], row["parent_color_sizes"]) == grades
            cells += 16
    assert cells == a["conversion"]["profile_cells"] == a["conversion"]["power_cells"]


def test_complete_basis_unit_vectors_and_signed_tables_in_both_executors(executors):
    checked = 0
    for odd, even in product(range(4), repeat=2):
        sizes = [odd, even]
        for o, e in product(range(odd + 1), range(even + 1)):
            grades = zero()
            grades[o][e] = 1
            power = expand(grades, sizes)
            assert invert(power, sizes) == grades
            for module in executors:
                assert module.expand_grade_table(grades, sizes) == power
                assert module.inverse_basis(power, sizes) == grades
            checked += 1
        signed = [
            [(-1) ** (o + e) * (o + e + 1) if o <= odd and e <= even else 0 for e in range(4)]
            for o in range(4)
        ]
        expanded = expand(signed, sizes)
        for module in executors:
            assert module.expand_grade_table(signed, sizes) == expanded
            assert module.inverse_basis(expanded, sizes) == signed
    assert checked == 100
    for size in range(4):
        assert basis_inverse(size) == tuple(
            tuple(F(choose(size - i, o - i)) for i in range(size + 1)) for o in range(size + 1)
        )


def test_degree_elevation_is_not_profile_equality_without_common_parent_degree(executors):
    power = zero()
    power[1][0] = 1
    low, high = invert(power, [1, 0]), invert(power, [2, 0])
    assert low[1][0] == high[1][0] == high[2][0] == 1 and low != high
    assert expand(low, [1, 0]) == expand(high, [2, 0]) == power
    complement = zero()
    complement[0][0], complement[1][0] = 1, -1
    for size, grades in ((1, low), (2, high)):
        other = invert(complement, [size, 0])
        assert all(grades[o][0] + other[o][0] == choose(size, o) for o in range(4))
        for module in executors:
            assert module.inverse_basis(power, [size, 0]) == grades
    # The degree-2 event places the SAME label at two child ranks. It cannot
    # be a color-fixing H class, so this is a premise counterexample, not Q.
    assert sum(bool(high[o][0]) for o in range(4)) == 2


def test_integer_nested_subset_identity_and_missing_binomial_factor(independent):
    a = independent[0]
    assert a["closure"]["closed"] is True
    assert a["composition"] == integer_composition(a["class_profiles"])
    selected = next(row for row in a["class_profiles"] if row["parent_color_sizes"] == [2, 0])
    empty = next(atom for atom in selected["transitions"] if atom["retained_color_sizes"] == [0, 0])
    target = empty["target_class"]
    observed = 0
    for atom in selected["transitions"]:
        if atom["retained_color_sizes"] == [1, 0]:
            continuation = next(
                child["multiplicity"]
                for child in a["class_profiles"][atom["target_class"]]["transitions"]
                if child["target_class"] == target
            )
            observed += atom["multiplicity"] * continuation
    assert observed == empty["multiplicity"] * comb(2, 1) == 2
    assert observed != empty["multiplicity"]
    nested_pairs = a["composition"]["rows"][selected["class_id"]]["nested_pairs"]
    assert nested_pairs == 9
    assert nested_pairs != 4 ** sum(selected["parent_color_sizes"])


def payload(row):
    return {key: copy.deepcopy(row[key]) for key in ("parent_color_sizes", "transitions")}


def expected_evaluation(row, rates):
    x, y = map(F, rates)
    return {
        "rates": rates[:],
        "outcomes": [
            {
                "target_class": atom["target_class"],
                "probability": str(
                    atom["multiplicity"]
                    * direct_probability(
                        *row["parent_color_sizes"], *atom["retained_color_sizes"], x, y
                    )
                ),
            }
            for atom in row["transitions"]
        ],
    }


def test_all_profile_atoms_match_nonnegative_probabilities_at_all_22_rates(independent):
    a, _, power_rows, _ = independent
    evaluated = 0
    for row, power in zip(a["profiles"], power_rows, strict=True):
        for pair in POINTS:
            probabilities = []
            for atom, polynomial in zip(row["transitions"], power["transitions"], strict=True):
                p = atom["multiplicity"] * direct_probability(
                    *row["parent_color_sizes"], *atom["retained_color_sizes"], *pair
                )
                assert p == evaluate(polynomial["coefficients"], *pair) >= 0
                probabilities.append(p)
                evaluated += 1
            assert sum(probabilities) == 1
            if pair in ((F(0), F(0)), (F(1), F(1)), (F(0), F(1)), (F(1), F(0))):
                assert sum(p == 1 for p in probabilities) == 1 and all(
                    p in (0, 1) for p in probabilities
                )
    assert evaluated == a["evaluation"]["probability_evaluations"]


def test_every_summary_row_helper_matches_all_22_exact_rates_and_is_detached(
    executors, independent
):
    for row in independent[0]["class_profiles"]:
        public = json.loads(wire(payload(row)))
        before = wire(public)
        for pair in POINTS:
            rates = list(map(str, pair))
            expected = expected_evaluation(public, rates)
            for module in executors:
                assert wire(module.evaluate_row(public, rates)) == wire(expected)
        assert wire(public) == before
    assert set(public) == {"parent_color_sizes", "transitions"}


def rank_row(odd=2, even=0):
    return {
        "parent_color_sizes": [odd, even],
        "transitions": [
            {
                "target_class": index,
                "retained_color_sizes": [o, e],
                "multiplicity": comb(odd, o) * comb(even, e),
            }
            for index, (o, e) in enumerate(product(range(odd + 1), range(even + 1)))
        ],
    }


def test_binomial_factor_rankwise_normalization_and_zero_rate_controls(executors):
    public = rank_row()
    assert [atom["multiplicity"] for atom in public["transitions"]] == [1, 2, 1]
    expected = {
        "rates": ["1/2", "0"],
        "outcomes": [
            {"target_class": 0, "probability": "1/4"},
            {"target_class": 1, "probability": "1/2"},
            {"target_class": 2, "probability": "1/4"},
        ],
    }
    assert sum(direct_probability(2, 0, o, 0, F(1, 2), F(0)) for o in range(3)) == F(3, 4) != 1
    # Each atom individually respects its rank maximum, and the total is4,
    # but rank0 has2 and rank1 has1: total normalization alone is insufficient.
    wrong = {
        "parent_color_sizes": [2, 0],
        "transitions": [
            {"target_class": 0, "retained_color_sizes": [0, 0], "multiplicity": 1},
            {"target_class": 1, "retained_color_sizes": [0, 0], "multiplicity": 1},
            {"target_class": 2, "retained_color_sizes": [1, 0], "multiplicity": 1},
            {"target_class": 3, "retained_color_sizes": [2, 0], "multiplicity": 1},
        ],
    }
    assert sum(atom["multiplicity"] for atom in wrong["transitions"]) == 4
    for module in executors:
        assert module.evaluate_row(public, ["1/2", "0"]) == expected
        with pytest.raises(ValueError):
            module.evaluate_row(wrong, ["1/2", "0"])
        for rates in (["0", "0"], ["1", "1"]):
            out = module.evaluate_row(public, rates)
            assert (
                len(out["outcomes"]) == 3
                and sum(atom["probability"] == "0" for atom in out["outcomes"]) == 2
            )


def test_row_labels_are_not_authenticated_global_class_or_domain_membership(executors):
    public = {
        "parent_color_sizes": [0, 0],
        "transitions": [{"target_class": 4446, "retained_color_sizes": [0, 0], "multiplicity": 1}],
    }
    for module in executors:
        assert module.evaluate_row(public, ["1/3", "2/3"]) == {
            "rates": ["1/3", "2/3"],
            "outcomes": [{"target_class": 4446, "probability": "1"}],
        }


def synthetic_profiles(failing=True):
    groups = [
        {"class_id": 0, "key": [0], "members": [0, 1]},
        {"class_id": 1, "key": [1], "members": [2]},
        {"class_id": 2, "key": [2], "members": [3, 4]},
        {"class_id": 3, "key": [3], "members": [5]},
    ]
    part = {"state_classes": [0, 0, 1, 2, 2, 3], "classes": groups}

    def atom(target, odd, multiplicity=1):
        return {
            "target_class": target,
            "retained_color_sizes": [odd, 0],
            "multiplicity": multiplicity,
        }

    rows = [
        {
            "state_id": 0,
            "parent_color_sizes": [2, 0],
            "transitions": [atom(0, 2), atom(1, 0), atom(2, 1, 2)],
        },
        {
            "state_id": 1,
            "parent_color_sizes": [2, 0],
            "transitions": [atom(0, 2), atom(1, 0), atom(3 if failing else 2, 1, 2)],
        },
        {"state_id": 2, "parent_color_sizes": [0, 0], "transitions": [atom(1, 0)]},
        {"state_id": 3, "parent_color_sizes": [1, 0], "transitions": [atom(1, 0), atom(2, 1)]},
        {"state_id": 4, "parent_color_sizes": [1, 0], "transitions": [atom(1, 0), atom(2, 1)]},
        {"state_id": 5, "parent_color_sizes": [1, 0], "transitions": [atom(1, 0), atom(3, 1)]},
    ]
    witness = (
        {
            "class_id": 0,
            "left_state": 0,
            "right_state": 1,
            "target_class": 2,
            "retained_color_sizes": [1, 0],
            "left_multiplicity": 2,
            "right_multiplicity": 0,
            "first_distinguishing_rates": ["1/3", "0"],
        }
        if failing
        else None
    )
    return (
        part,
        rows,
        {"closed": not failing, "classes_checked": 4, "member_comparisons": 2, "witness": witness},
    )


@pytest.mark.parametrize("failing", [True, False])
def test_production_synthetic_profile_closure_preserves_failure_and_all_member_scan(
    executors, aggregate, failing
):
    part, rows, expected = synthetic_profiles(failing)
    before = wire([part, rows])
    for module in executors:
        assert module.closure_from_profiles(rows, part) == expected
        closure, classes, composition = module._closure(part, rows)
        assert closure == expected
        if failing:
            assert classes == [] and composition is None
        else:
            wanted = [
                {
                    "class_id": group["class_id"],
                    "representative_state": group["members"][0],
                    **payload(rows[group["members"][0]]),
                }
                for group in part["classes"]
            ]
            assert classes == wanted
            assert composition == integer_composition(wanted)
    root_closure, root_classes = aggregate[0].closure_profiles(part, rows)
    assert root_closure == expected
    if failing:
        assert root_classes == []
    assert wire([part, rows]) == before


def test_color_premise_failures_are_rejected_not_reported_as_law_equivalence(executors):
    part, rows, _ = synthetic_profiles()
    bad_parent = copy.deepcopy(rows)
    bad_parent[1] = {
        "state_id": 1,
        "parent_color_sizes": [1, 0],
        "transitions": copy.deepcopy(rows[3]["transitions"]),
    }
    wrong_target = copy.deepcopy(rows)
    wrong_target[3]["transitions"] = [
        {"target_class": 0, "retained_color_sizes": [1, 0], "multiplicity": 1},
        {"target_class": 1, "retained_color_sizes": [0, 0], "multiplicity": 1},
    ]
    for module in executors:
        # Row-only validation cannot authenticate the global target color.
        assert module.evaluate_row(payload(wrong_target[3]), ["1/2", "0"])["outcomes"]
        for changed in (bad_parent, wrong_target):
            with pytest.raises(ValueError):
                module.closure_from_profiles(changed, part)


def test_public_results_and_revalidation_do_not_alias_mutable_input(executors):
    for module in executors:
        row, rates = rank_row(), ["1/2", "0"]
        expected = module.evaluate_row(row, rates)
        before = wire(row)
        out = module.evaluate_row(row, rates)
        out["rates"][0] = "0"
        out["outcomes"][0]["probability"] = "99"
        assert rates == ["1/2", "0"] and wire(row) == before
        assert module.evaluate_row(row, rates) == expected
        row["transitions"][0]["multiplicity"] = True
        with pytest.raises(ValueError):
            module.evaluate_row(row, rates)
        row["transitions"][0]["multiplicity"] = 1
        assert module.evaluate_row(row, rates) == expected


def micro_problem():
    return {
        "schema_version": "det8-qr05r-problem-v1",
        "family": "qr05r_deletion_profile",
        "model": {
            "frames": [
                {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
                {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
            ],
            "states": [
                {"state_id": 0, "frame_id": 0, "kept": [0, 7], "past": [[], [0]]},
                {"state_id": 1, "frame_id": 1, "kept": [0, 3, 7], "past": [[], [0], [0, 1]]},
            ],
        },
    }


@pytest.fixture(scope="session")
def micro_analyses(executors):
    return tuple(module.analyze(micro_problem()) for module in executors)


def test_minimum_parser_case_is_not_automatically_the_certified_Q_domain(micro_analyses):
    assert wire(micro_analyses[0]) == wire(micro_analyses[1])
    a = micro_analyses[0]
    assert a["counts"] == {
        "states": 2,
        "classes": 2,
        "fine_atoms": 2,
        "profile_atoms": 2,
        "class_profile_atoms": 2,
    }
    assert a["features"][0]["chain_counts"] == [1, 0, 0, 0]
    assert a["features"][1]["chain_counts"] == [1, 1, 0, 0]
    assert all(row["parent_color_sizes"] == [0, 0] for row in a["profiles"])
    assert a["composition"]["totals"]["nested_pairs"] == 2


class IntSubclass(int):
    pass


class StringSubclass(str):
    pass


class ListSubclass(list):
    pass


class DictSubclass(dict):
    pass


def bad_problem(case):
    p = micro_problem()
    edits = {
        "schema": (["schema_version"], "other"),
        "family": (["family"], "other"),
        "schema-subclass": (["schema_version"], StringSubclass(p["schema_version"])),
        "family-bool": (["family"], True),
        "frames-tuple": (["model", "frames"], tuple(p["model"]["frames"])),
        "frame-bool": (["model", "frames", 0, "frame_id"], False),
        "fixed-mark": (["model", "frames", 1, "fixed"], [0, 7]),
        "eligible-mark": (["model", "frames", 1, "eligible"], [1, 2, 3, 4, 5, 6]),
        "density-float": (["model", "frames", 0, "density"], 12.0),
        "density-noncanonical": (["model", "frames", 0, "density"], "12/1"),
        "state-id-bool": (["model", "states", 0, "state_id"], False),
        "state-id-gap": (["model", "states", 1, "state_id"], 3),
        "state-frame-bool": (["model", "states", 0, "frame_id"], False),
        "kept-bool": (["model", "states", 1, "kept", 0], False),
        "kept-subclass": (["model", "states", 1, "kept", 0], IntSubclass(0)),
        "past-bool": (["model", "states", 1, "past", 1, 0], False),
        "past-float": (["model", "states", 1, "past", 1, 0], 0.0),
        "past-tuple": (["model", "states", 1, "past", 2], (0, 1)),
        "unsorted-past": (["model", "states", 1, "past", 2], [1, 0]),
        "duplicate-past": (["model", "states", 1, "past", 2], [0, 0, 1]),
        "out-of-range-past": (["model", "states", 1, "past", 2], [0, 3]),
        "self-loop": (["model", "states", 1, "past", 1], [0, 1]),
        "cycle": (["model", "states", 1, "past", 0], [1]),
        "nontransitive": (["model", "states", 1, "past", 2], [1]),
        "unsorted-kept": (["model", "states", 1, "kept"], [0, 7, 3]),
        "duplicate-kept": (["model", "states", 1, "kept"], [0, 3, 3]),
        "one-frame": (["model", "states", 1, "frame_id"], 0),
        "too-few": (["model", "states"], p["model"]["states"][:1]),
        "too-many": (
            ["model", "states"],
            [{**p["model"]["states"][0], "state_id": sid} for sid in range(4448)],
        ),
        "overflow": (["model", "states", 0, "state_id"], 1 << 4096),
    }
    if case in edits:
        path, value = edits[case]
        return replaced(p, path, value)
    if case == "extra":
        p["profiles"] = []
    elif case == "missing":
        del p["model"]
    elif case == "dict-subclass":
        return DictSubclass(p)
    elif case == "key-subclass":
        p[StringSubclass("family")] = p.pop("family")
    elif case == "states-subclass":
        p["model"]["states"] = ListSubclass(p["model"]["states"])
    elif case == "state-extra":
        p["model"]["states"][0]["H_class"] = 0
    elif case == "missing-endpoint":
        p["model"]["states"][0].update(kept=[0], past=[[]])
    elif case == "missing-fixed":
        p["model"]["states"][1].update(kept=[0, 7], past=[[], [0]])
    elif case == "duplicate-observation":
        p["model"]["states"].append({**copy.deepcopy(p["model"]["states"][0]), "state_id": 2})
    elif case == "missing-successors":
        p["model"]["states"].append(
            {"state_id": 2, "frame_id": 0, "kept": [0, 1, 2, 7], "past": [[], [0], [0], [0, 1, 2]]}
        )
    else:
        raise AssertionError(case)
    return p


@pytest.mark.parametrize(
    "case",
    [
        "schema",
        "family",
        "schema-subclass",
        "family-bool",
        "frames-tuple",
        "frame-bool",
        "fixed-mark",
        "eligible-mark",
        "density-float",
        "density-noncanonical",
        "state-id-bool",
        "state-id-gap",
        "state-frame-bool",
        "kept-bool",
        "kept-subclass",
        "past-bool",
        "past-float",
        "past-tuple",
        "unsorted-past",
        "duplicate-past",
        "out-of-range-past",
        "self-loop",
        "cycle",
        "nontransitive",
        "unsorted-kept",
        "duplicate-kept",
        "one-frame",
        "too-few",
        "too-many",
        "overflow",
        "extra",
        "missing",
        "dict-subclass",
        "key-subclass",
        "states-subclass",
        "state-extra",
        "missing-endpoint",
        "missing-fixed",
        "duplicate-observation",
        "missing-successors",
    ],
)
def test_analyze_rejects_malformed_small_models_without_full_domain_reconstruction(executors, case):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(bad_problem(case))


def bad_row(case):
    row = rank_row(2, 1)
    edits = {
        "parent-bool": (["parent_color_sizes", 0], True),
        "parent-high": (["parent_color_sizes", 0], 4),
        "parent-negative": (["parent_color_sizes", 0], -1),
        "parent-tuple": (["parent_color_sizes"], (2, 1)),
        "parent-length": (["parent_color_sizes"], [2, 1, 0]),
        "parent-subclass": (["parent_color_sizes"], ListSubclass([2, 1])),
        "target-bool": (["transitions", 0, "target_class"], False),
        "target-float": (["transitions", 0, "target_class"], 0.0),
        "target-subclass": (["transitions", 0, "target_class"], IntSubclass(0)),
        "target-range": (["transitions", 5, "target_class"], 4447),
        "rank-bool": (["transitions", 0, "retained_color_sizes", 0], False),
        "rank-negative": (["transitions", 0, "retained_color_sizes", 0], -1),
        "rank-high": (["transitions", 0, "retained_color_sizes", 0], 3),
        "rank-length": (["transitions", 0, "retained_color_sizes"], [0]),
        "rank-tuple": (["transitions", 0, "retained_color_sizes"], (0, 0)),
        "count-zero": (["transitions", 0, "multiplicity"], 0),
        "count-negative": (["transitions", 0, "multiplicity"], -1),
        "count-bool": (["transitions", 0, "multiplicity"], True),
        "count-float": (["transitions", 0, "multiplicity"], 1.0),
        "count-fraction": (["transitions", 0, "multiplicity"], F(1)),
        "count-subclass": (["transitions", 0, "multiplicity"], IntSubclass(1)),
        "count-high": (["transitions", 0, "multiplicity"], 10),
        "count-over-rank": (["transitions", 0, "multiplicity"], 2),
        "count-overflow": (["transitions", 0, "multiplicity"], 1 << 4096),
        "empty-atoms": (["transitions"], []),
        "atoms-tuple": (["transitions"], tuple(row["transitions"])),
    }
    if case in edits:
        return replaced(row, *edits[case])
    if case == "extra":
        row["state_id"] = 0
    elif case == "dict-subclass":
        return DictSubclass(row)
    elif case == "key-subclass":
        row[StringSubclass("transitions")] = row.pop("transitions")
    elif case == "atom-extra":
        row["transitions"][0]["probability"] = "1"
    elif case == "duplicate-target":
        row["transitions"][1]["target_class"] = 0
    elif case == "unsorted-targets":
        row["transitions"].reverse()
    elif case == "missing-atom":
        row["transitions"].pop()
    elif case == "too-many-atoms":
        row["transitions"] = row["transitions"] * 11
    else:
        raise AssertionError(case)
    return row


@pytest.mark.parametrize(
    "case",
    [
        "parent-bool",
        "parent-high",
        "parent-negative",
        "parent-tuple",
        "parent-length",
        "parent-subclass",
        "target-bool",
        "target-float",
        "target-subclass",
        "target-range",
        "rank-bool",
        "rank-negative",
        "rank-high",
        "rank-length",
        "rank-tuple",
        "count-zero",
        "count-negative",
        "count-bool",
        "count-float",
        "count-fraction",
        "count-subclass",
        "count-high",
        "count-over-rank",
        "count-overflow",
        "empty-atoms",
        "atoms-tuple",
        "extra",
        "dict-subclass",
        "key-subclass",
        "atom-extra",
        "duplicate-target",
        "unsorted-targets",
        "missing-atom",
        "too-many-atoms",
    ],
)
def test_public_row_rejects_native_and_rankwise_schema_errors(executors, case):
    for module in executors:
        with pytest.raises(ValueError):
            module.evaluate_row(bad_row(case), ["1/2", "1/2"])


@pytest.mark.parametrize(
    "rates",
    [
        None,
        [],
        ["1/2"],
        ["0", "0", "0"],
        ("0", "1"),
        ListSubclass(["0", "1"]),
        [0, "1"],
        [0.5, "1"],
        [True, "1"],
        [F(1, 2), "1"],
        [StringSubclass("1/2"), "1"],
        ["2/4", "1"],
        ["0.5", "1"],
        ["01", "1"],
        ["+1", "1"],
        ["-0", "1"],
        ["-1/2", "1"],
        ["3/2", "1"],
        ["1/0", "1"],
        ["1/" + str(1 << 4096), "1"],
    ],
)
def test_public_rates_are_bounded_canonical_unsigned_rationals(executors, rates):
    for module in executors:
        with pytest.raises(ValueError):
            module.evaluate_row(rank_row(), rates)


@pytest.mark.parametrize(
    "bad", ["1e-10000000", "1e999999999", "1e-1", "NaN", "1 /2", "١", "1" * 3001, "-1/2"]
)
def test_rate_grammar_rejects_before_fraction_constructor(executors, monkeypatch, bad):
    def forbidden(*args, **kwargs):
        raise AssertionError("unsafe syntax reached Fraction construction")

    for module in executors:
        with monkeypatch.context() as patch:
            patch.setattr(module, "Fraction", forbidden)
            if hasattr(module, "F"):
                patch.setattr(module, "F", forbidden)
            with pytest.raises(ValueError):
                module.evaluate_row(rank_row(), [bad, "0"])


def test_maximum_64_fine_atoms_and_multiplicity_nine_are_valid(executors):
    fine = {
        "parent_color_sizes": [3, 3],
        "transitions": [
            {
                "target_class": mask,
                "retained_color_sizes": [(mask & 7).bit_count(), (mask >> 3).bit_count()],
                "multiplicity": 1,
            }
            for mask in range(64)
        ],
    }
    ranked = rank_row(3, 3)
    assert max(atom["multiplicity"] for atom in ranked["transitions"]) == 9
    for module in executors:
        result = module.evaluate_row(fine, ["1/2", "1/2"])
        assert len(result["outcomes"]) == 64 and all(
            atom["probability"] == "1/64" for atom in result["outcomes"]
        )
        assert module.evaluate_row(ranked, ["2/5", "3/7"]) == expected_evaluation(
            ranked, ["2/5", "3/7"]
        )


def test_final_probability_component_cap_rejects_instead_of_rounding(executors):
    rate = "1/" + str((1 << 684) - 1)
    assert F(rate).denominator.bit_length() <= 4096 < (F(rate) ** 6).denominator.bit_length()
    for module in executors:
        with pytest.raises(ValueError):
            module.evaluate_row(rank_row(3, 3), [rate, rate])


def test_optimized_valid_small_case_and_native_guards_are_explicit(tmp_path):
    code = r"""
import importlib.util,json,pathlib,sys
base=pathlib.Path(sys.argv[1]);problem,row,synthetic=json.loads(sys.argv[2])
class S(str):pass
class D(dict):pass
def rejected(fn):
 try:fn()
 except ValueError:return
 raise RuntimeError("optimized validation accepted an invalid value")
for i,filename in enumerate(("deletion_profile.py","reference_qr05r.py")):
 name="_qr05r_optimized_"+str(i);spec=importlib.util.spec_from_file_location(name,base/filename)
 m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
 a=m.analyze(problem)
 if a["counts"]["states"]!=2 or not a["closure"]["closed"]:raise RuntimeError("valid micro model failed")
 result=m.evaluate_row(row,["1/2","0"])
 if [o["probability"]for o in result["outcomes"]]!=["1/4","1/2","1/4"]:raise RuntimeError("binomial evaluation failed")
 part,profiles,expected=synthetic
 closed,classes,composition=m._closure(part,profiles)
 if closed!=expected or classes!=[] or composition is not None:raise RuntimeError("failure branch was repaired")
 bad=json.loads(json.dumps(problem));bad["model"]["states"][0]["frame_id"]=False
 rejected(lambda:m.analyze(bad));rejected(lambda:m.analyze(D(problem)))
 badkey=dict(problem);badkey[S("family")]=badkey.pop("family");rejected(lambda:m.analyze(badkey))
 badrow=json.loads(json.dumps(row));badrow["transitions"][0]["multiplicity"]=True
 rejected(lambda:m.evaluate_row(badrow,["1/2","0"]))
 rejected(lambda:m.evaluate_row(row,[S("1/2"),"0"]))
 rejected(lambda:m.evaluate_row(row,["2/4","0"]))
 def forbidden(*args,**kwargs):raise RuntimeError("scientific notation reached Fraction")
 original=m.Fraction;m.Fraction=forbidden
 if hasattr(m,"F"):original_f=m.F;m.F=forbidden
 rejected(lambda:m.evaluate_row(row,["1e-10000000","0"]))
 m.Fraction=original
 if hasattr(m,"F"):m.F=original_f
print("optimized valid mathematics and explicit native guards passed")
"""
    data = [micro_problem(), rank_row(), synthetic_profiles()]
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
            json.dumps(data),
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "optimized valid mathematics and explicit native guards passed"


def test_raw_Q_transitivity_and_fixed_marks_are_not_recomputed_from_generator_edges(
    problem, pinned_q, independent
):
    raw, fs = problem["model"]["states"], independent[0]["features"]
    profiles = pinned_q["analysis"]["domain"]["profiles"]
    for pi in (1047, 1303):
        full, reduced = profiles[pi]["state_ids"][63], profiles[pi]["state_ids"][17]
        assert raw[reduced]["kept"] == [0, 1, 5, 7]
        assert ((1, 5) if pi == 1047 else (5, 1)) in relation_of(raw[reduced])
        assert fs[full]["mean_graded"][3][3][0] == 1
        assert fs[reduced]["chain_counts"] == [1, 2, 1, 0]
    assert all("profiles" not in row and "aliases" not in row for row in raw)


def test_full_aggregate_native_wire_and_declared_input_dependency(aggregate, analyses, problem):
    runner, suite = aggregate
    a = analyses[0]
    assert runner.canonical(suite) == wire(suite) == wire(json.loads(wire(suite)))
    assert set(suite) == {
        "problem",
        "analysis",
        "independent_route_equal",
        "independent_audit",
        "prior_bridge",
        "controls",
        "public_controls",
        "invalid_inputs_rejected",
        "totals",
    }
    assert wire(suite["problem"]) == wire(problem)
    assert wire(suite["analysis"]) == wire(a)
    assert suite["independent_route_equal"] is True
    assert suite["independent_audit"] == {
        "raw_observations_reconstructed": True,
        "all_features_and_H_fibers_checked": True,
        "all_subset_profiles_and_power_laws_checked": True,
        "all_rank_normalizations_checked": True,
        "all_nested_counts_checked": True,
        "analysis_sha256": digest(a),
    }
    assert suite["prior_bridge"] == {
        "prior_artifact": "qr-05q-three-layer-portability-2026-09-06/results.json",
        "declared_raw_model_input_dependency": True,
        "source_alias_universe_regenerated": False,
        "matched_states": 4447,
        "all_features_equal": True,
        "actual_H_fibers_equal": True,
        "all_fine_pushed_quotient_laws_equal": True,
        "Q_four_variable_certificate_recomputed": False,
        "expanded_minimality_tested": False,
    }
    assert suite["controls"] == {
        "basis_monomials": 100,
        "basis_coefficient_cells": 1600,
        "degree_elevation_equal_laws_different_profiles": True,
        "degree_elevation_control_is_outside_H_premises": True,
        "parent_successor_colors_checked": 4447,
        "all_structural_zero_rate_atoms_retained": True,
    }
    assert suite["public_controls"] == {
        "calls": 2 * 22 * len(a["class_profiles"]),
        "classes": len(a["class_profiles"]),
        "rate_points": 22,
        "invalid_calls_rejected": 32,
        "hidden_model_dependency": False,
        "structural_zero_outcomes_retained": True,
    }
    assert suite["invalid_inputs_rejected"] == 2 * len(runner.invalid_fixtures())
    assert suite["totals"] == {
        **a["counts"],
        "profile_closed": a["closure"]["closed"],
        "member_comparisons": a["closure"]["member_comparisons"],
        "profile_cells": a["conversion"]["profile_cells"],
        "power_cells": a["conversion"]["power_cells"],
        "normalization_cells": a["conversion"]["normalization_cells"],
        "composition_rank_cells": a["composition"]["totals"]["rank_cells"]
        if a["composition"]
        else 0,
        "nested_pairs": a["composition"]["totals"]["nested_pairs"] if a["composition"] else 0,
        "probability_evaluations": a["evaluation"]["probability_evaluations"],
        "public_calls": suite["public_controls"]["calls"],
    }
    assert len(runner.SOURCES) == 6 and len(runner.PRIORS) == 22


def changed_analysis(a, case):
    changes = {
        "model-digest": (["model_sha256"], "0" * 64),
        "feature-id-bool": (["features", 0, "state_id"], False),
        "feature-N0-bool": (["features", 0, "chain_counts", 0], True),
        "feature-B": (["features", 0, "pair_graded", 0, 0, 0, 0], 2),
        "parent-rank-bool": (["profiles", 0, "parent_color_sizes", 0], False),
        "child-rank-bool": (["profiles", 0, "transitions", 0, "retained_color_sizes", 0], False),
        "target-class-bool": (["profiles", 0, "transitions", 0, "target_class"], False),
        "multiplicity-bool": (["profiles", 0, "transitions", 0, "multiplicity"], True),
        "alias-weighted-count": (["profiles", 0, "transitions", 0, "multiplicity"], 2),
        "rank-target-confusion": (
            ["profiles", 0, "transitions", 0, "retained_color_sizes"],
            [1, 0],
        ),
        "fine-digest": (["conversion", "fine_kernel_sha256"], "0" * 64),
        "pushed-digest": (["conversion", "pushed_rows_sha256"], "0" * 64),
        "quotient-digest": (["conversion", "quotient_rows_sha256"], "0" * 64),
        "profile-cells": (["conversion", "profile_cells"], a["conversion"]["profile_cells"] - 16),
        "closed-int": (["closure", "closed"], int(a["closure"]["closed"])),
        "closure-flip": (["closure", "closed"], not a["closure"]["closed"]),
        "member-scan": (["closure", "member_comparisons"], a["closure"]["member_comparisons"] + 1),
        "fake-witness": (["closure", "witness"], synthetic_profiles()[2]["witness"]),
        "class-profile-count": (["class_profiles", 0, "transitions", 0, "multiplicity"], 2),
        "nested-pairs": (["composition", "rows", 0, "nested_pairs"], 2),
        "composition-ranks": (["composition", "rows", 0, "rank_cells"], 0),
        "evaluation-count": (
            ["evaluation", "probability_evaluations"],
            a["evaluation"]["probability_evaluations"] - 1,
        ),
        "profile-tuple": (["profiles", 0, "parent_color_sizes"], (0, 0)),
        "overflow": (["counts", "states"], 1 << 4096),
    }
    if case in changes:
        return replaced(a, *changes[case])
    if case == "omit-selected-zero":
        sid, idx = next(
            (row["state_id"], i)
            for row in a["profiles"]
            for i, atom in enumerate(row["transitions"])
            if atom["retained_color_sizes"] != row["parent_color_sizes"]
        )
        atoms = a["profiles"][sid]["transitions"]
        assert atoms[idx]["multiplicity"] > 0
        assert (
            direct_probability(
                *a["profiles"][sid]["parent_color_sizes"],
                *atoms[idx]["retained_color_sizes"],
                F(1),
                F(1),
            )
            == 0
        )
        return replaced(a, ["profiles", sid, "transitions"], atoms[:idx] + atoms[idx + 1 :])
    raise AssertionError(case)


@pytest.mark.parametrize(
    "case",
    [
        "model-digest",
        "feature-id-bool",
        "feature-N0-bool",
        "feature-B",
        "parent-rank-bool",
        "child-rank-bool",
        "target-class-bool",
        "multiplicity-bool",
        "alias-weighted-count",
        "rank-target-confusion",
        "fine-digest",
        "pushed-digest",
        "quotient-digest",
        "profile-cells",
        "closed-int",
        "closure-flip",
        "member-scan",
        "fake-witness",
        "class-profile-count",
        "nested-pairs",
        "composition-ranks",
        "evaluation-count",
        "profile-tuple",
        "overflow",
        "omit-selected-zero",
    ],
)
def test_independent_audit_rejects_exact_evidence_corruption(aggregate, analyses, problem, case):
    runner, _ = aggregate
    with pytest.raises(ValueError):
        runner.check_analysis(changed_analysis(analyses[0], case), problem["model"])


def test_same_cardinality_wrong_fibers_cannot_substitute_for_actual_partition(
    aggregate, analyses, problem
):
    a = analyses[0]
    groups = [g for g in a["partition"]["classes"] if len(g["members"]) > 1]
    left, right = next(
        (x, y) for x, y in combinations(groups, 2) if len(x["members"]) == len(y["members"])
    )
    u, v = left["members"][-1], right["members"][-1]
    lm, rm = (
        sorted([sid for sid in left["members"] if sid != u] + [v]),
        sorted([sid for sid in right["members"] if sid != v] + [u]),
    )
    assert lm[0] == left["members"][0] and rm[0] == right["members"][0]
    changed = replaced(a, ["partition", "classes", left["class_id"], "members"], lm)
    changed = replaced(changed, ["partition", "classes", right["class_id"], "members"], rm)
    changed = replaced(changed, ["partition", "state_classes", u], right["class_id"])
    changed = replaced(changed, ["partition", "state_classes", v], left["class_id"])
    assert changed["counts"] == a["counts"]
    assert sorted(
        sid for group in changed["partition"]["classes"] for sid in group["members"]
    ) == list(range(4447))
    with pytest.raises(ValueError):
        aggregate[0].check_analysis(changed, problem["model"])


def test_model_cache_is_content_keyed_and_mutated_inputs_are_revalidated(aggregate, micro_analyses):
    runner, _ = aggregate
    model, a = micro_problem()["model"], copy.deepcopy(micro_analyses[0])
    expected = runner.check_analysis(a, model)
    model["states"][0]["frame_id"] = False
    with pytest.raises(ValueError):
        runner.check_analysis(a, model)
    model["states"][0]["frame_id"] = 0
    model["states"][1]["past"][2] = [1]
    with pytest.raises(ValueError):
        runner.check_analysis(a, model)
    model["states"][1]["past"][2] = [0, 1]
    a["profiles"][0]["transitions"][0]["multiplicity"] = True
    with pytest.raises(ValueError):
        runner.check_analysis(a, model)
    a["profiles"][0]["transitions"][0]["multiplicity"] = 1
    assert runner.check_analysis(a, model) == expected


@pytest.mark.parametrize(
    "bad", [(1,), {"x": 1.0}, {False: 0}, {StringSubclass("x"): 0}, {"x": ListSubclass([1])}]
)
def test_runner_native_wire_guard(aggregate, bad):
    with pytest.raises(ValueError):
        aggregate[0].require_wire(bad)


@pytest.mark.parametrize("left,right", [({"a": [True]}, {"a": [1]}), ({"a": [False]}, {"a": [0]})])
def test_runner_equality_does_not_coerce_bool_to_int(aggregate, left, right):
    assert left == right
    with pytest.raises(ValueError):
        aggregate[0].require_same_wire(left, right, "native bool/int distinction")
