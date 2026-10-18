"""Independent O path-observable tests, carrying our N/M/L test lineage.

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
N_SHA = "f2d666285afef41cd8a7f977399d3626a620da39174967a38047714f5f26f93e"
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
    return {"schema_version": "det8-qr05o-problem-v1", "family": "qr05o_path_iid"}


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
        private_module("_qr05o_test_direct", "path_observable.py"),
        private_module("_qr05o_test_reference", "reference_qr05o.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors):
    return tuple(module.analyze(problem()) for module in executors)


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05o_test_aggregate", "study.py")
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


@pytest.fixture(scope="session")
def pinned_n():
    path = HERE.parent / "qr-05n-domain-portability-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == N_SHA
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


def independent_path_supports(kept, past, eligible):
    relation = {
        (kept[i], target) for target, before in zip(kept, past, strict=True) for i in before
    }
    answer = []
    for support in combinations(sorted(set(kept) & set(eligible)), 4):
        if sum(v % 2 for v in support) != 2:
            continue
        edges = [(u, v) for u, v in relation if u in support and v in support]
        if len(edges) != 3 or any(u % 2 == v % 2 for u, v in edges):
            continue
        if len({u % 2 for u, _ in edges}) != 1:
            continue
        degrees = sorted(sum(v in edge for edge in edges) for v in support)
        if degrees == [1, 1, 2, 2]:
            answer.append(list(support))
    return answer


def refines_ids(fine, coarse):
    image = {}
    for a, b in zip(fine, coarse, strict=True):
        image.setdefault(a, set()).add(b)
    return all(len(values) == 1 for values in image.values())


@pytest.fixture(scope="session")
def expected_path(independent):
    model = independent[0]
    states, frames = model["states"], model["frames"]
    features, classes, ids, registry = [], [], [], {}
    for state in states:
        frame = frames[state["frame_id"]]
        supports = independent_path_supports(state["kept"], state["past"], frame["eligible"])
        features.append(
            {"state_id": state["state_id"], "path_supports": supports, "path_count": len(supports)}
        )
        key = [
            [frame["density"], frame["fixed"], frame["eligible"]],
            state["pair_graded"],
            state["motif_count"],
            len(supports),
        ]
        encoded = wire(key)
        cid = registry.setdefault(encoded, len(registry))
        if cid == len(classes):
            classes.append({"class_id": cid, "key": key, "members": []})
        classes[cid]["members"].append(state["state_id"])
        ids.append(cid)
    pushed, expectations = [], []
    for state in states:
        tables, expectation = {}, zero_table()
        for atom in state["transitions"]:
            target = atom["target_state"]
            table = tables.setdefault(ids[target], zero_table())
            for i, j in product(range(4), repeat=2):
                table[i][j] += atom["coefficients"][i][j]
                expectation[i][j] += atom["coefficients"][i][j] * features[target]["path_count"]
        pushed.append(
            {
                "state_id": state["state_id"],
                "transitions": [
                    {"target_class": cid, "coefficients": table}
                    for cid, table in sorted(tables.items())
                ],
            }
        )
        expected = zero_table()
        expected[2][2] = features[state["state_id"]]["path_count"]
        assert expectation == expected
        expectations.append(
            {
                "state_id": state["state_id"],
                "coefficients": expectation,
                "expected_coefficients": expected,
                "max_abs_residual": 0,
            }
        )
    failure = None
    for group in classes:
        left = group["members"][0]
        for right in group["members"][1:]:
            difference = first_difference(pushed[left]["transitions"], pushed[right]["transitions"])
            if difference is not None:
                target, a, b = difference
                failure = {
                    "class_id": group["class_id"],
                    "left_state": left,
                    "right_state": right,
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
                "transitions": pushed[group["members"][0]]["transitions"],
            }
            for group in classes
        ]
    )
    semigroup = None if failure else composition(quotient)
    pair_ids = [state["classes"]["pair_graded"] for state in states]
    motif_ids = [state["classes"]["motif_pair"] for state in states]
    splitting = sum(
        len({ids[sid] for sid in group["members"]}) > 1
        for group in model["partitions"]["motif_pair"]
    )
    return {
        "definition": "eligible_color_layered_induced_p4",
        "states": features,
        "state_classes": ids,
        "classes": classes,
        "pushforward_rows": pushed,
        "closed": failure is None,
        "first_failure": failure,
        "quotient_rows": quotient,
        "semigroup": semigroup,
        "comparison": {
            "candidate_refines_pair": refines_ids(ids, pair_ids),
            "candidate_refines_motif_pair": refines_ids(ids, motif_ids),
            "motif_pair_refines_candidate": refines_ids(motif_ids, ids),
            "same_memberships_as_motif_pair": ids == motif_ids,
        },
        "expected_update": {
            "verified": True,
            "coefficient_cells": 16 * len(states),
            "rows": expectations,
        },
        "counts": {
            "states": len(states),
            "path_positive_states": sum(row["path_count"] > 0 for row in features),
            "path_support_occurrences": sum(row["path_count"] for row in features),
            "max_path_count": max(row["path_count"] for row in features),
            "classes": len(classes),
            "split_motif_pair_classes": splitting,
            "state_transition_atoms": sum(len(row["transitions"]) for row in pushed),
            "state_coefficient_cells": 16 * sum(len(row["transitions"]) for row in pushed),
            "expected_update_coefficient_cells": 16 * len(states),
            "quotient_transition_atoms": sum(len(row["transitions"]) for row in quotient),
            "semigroup_intermediate_paths": 0
            if semigroup is None
            else semigroup["totals"]["intermediate_paths"],
            "semigroup_coefficient_cells": 0
            if semigroup is None
            else semigroup["totals"]["coefficient_cells"],
        },
    }


def synthetic_order(kept, edges, eligible):
    relation = set(edges)
    while True:
        closure = relation | {(a, c) for a, b in relation for d, c in relation if b == d}
        if closure == relation:
            break
        relation = closure
    assert all(a != b and a in kept and b in kept for a, b in relation)
    return {
        "kept": list(kept),
        "past": [[i for i, a in enumerate(kept) if (a, b) in relation] for b in kept],
        "eligible": list(eligible),
    }


def restrict_observation(observation, kept):
    old = observation["kept"]
    relation = {
        (old[i], b) for b, before in zip(old, observation["past"], strict=True) for i in before
    }
    return {
        "kept": list(kept),
        "past": [[i for i, a in enumerate(kept) if (a, b) in relation] for b in kept],
        "eligible": list(observation["eligible"]),
    }


def path_cases():
    quad = [1, 3, 4, 6]
    full = set(product((1, 3), (4, 6)))
    rows = []
    for index, missing in enumerate(sorted(full)):
        for reverse in (False, True):
            edges = {(b, a) if reverse else (a, b) for a, b in full - {missing}}
            rows.append((f"missing_{index}_{reverse}", synthetic_order(quad, edges, quad), [quad]))
    path = full - {(3, 4)}
    rows += [
        ("two_disjoint_edges", synthetic_order(quad, [(1, 4), (3, 6)], quad), []),
        ("two_edge_wedge", synthetic_order(quad, [(1, 4), (1, 6)], quad), []),
        ("noninduced_paths_in_k22", synthetic_order(quad, full, quad), []),
        ("same_color_comparison", synthetic_order(quad, path | {(1, 3)}, quad), []),
        (
            "wrong_layer_colors",
            synthetic_order([1, 2, 3, 4], [(1, 3), (1, 4), (2, 4)], [1, 2, 3, 4]),
            [],
        ),
        (
            "wrong_cardinality",
            synthetic_order([1, 3, 5, 6], [(1, 5), (1, 6), (3, 6)], [1, 3, 5, 6]),
            [],
        ),
        ("directed_three_edge_chain", synthetic_order(quad, [(1, 4), (4, 3), (3, 6)], quad), []),
        ("fixed_original_three", synthetic_order(quad, path, [1, 4, 6]), []),
        ("reordered_local_positions", synthetic_order([6, 1, 4, 3], path, quad), [quad]),
        (
            "color_exchange",
            synthetic_order([2, 4, 5, 7], {(a + 1, b + 1) for a, b in path}, [2, 4, 5, 7]),
            [[2, 4, 5, 7]],
        ),
        (
            "harmless_outside",
            synthetic_order([0, *quad], path | {(0, v) for v in quad}, quad),
            [quad],
        ),
    ]
    rename = {1: 9, 3: 5, 4: 12, 6: 2}
    rows.append(
        (
            "parity_preserving_labels",
            synthetic_order(
                [12, 9, 2, 5], {(rename[a], rename[b]) for a, b in path}, [2, 5, 9, 12]
            ),
            [[2, 5, 9, 12]],
        )
    )
    intermediary = synthetic_order([1, 3, 4, 5, 6], path | {(3, 5), (5, 4)}, quad)
    rows.append(("intermediary_present", intermediary, []))
    rows.append(("intermediary_removed_induced", restrict_observation(intermediary, quad), []))
    overlap = [1, 2, 3, 4, 6]
    rows.append(
        (
            "overlapping_k23_missing_edge",
            synthetic_order(overlap, set(product((1, 3), (2, 4, 6))) - {(3, 6)}, overlap),
            [[1, 2, 3, 6], [1, 3, 4, 6]],
        )
    )
    return rows


@pytest.mark.parametrize(
    "name,observation,expected", path_cases(), ids=[row[0] for row in path_cases()]
)
def test_path_recognizer_uses_induced_marked_order_not_cover_graph_or_embeddings(
    executors, name, observation, expected
):
    assert independent_path_supports(**observation) == expected, name
    for module in executors:
        actual = module.path_supports(**observation)
        assert wire(actual) == wire(expected), name
        assert actual == sorted(actual) and len(actual) == len(
            {tuple(support) for support in actual}
        )
        assert all(support == sorted(set(support)) and len(support) == 4 for support in actual)
    if name in ("noninduced_paths_in_k22", "intermediary_present", "intermediary_removed_induced"):
        assert motif_supports(**observation) == [[1, 3, 4, 6]]


def test_every_path_feature_fiber_law_and_expectation_is_independently_reconstructed(
    analyses, expected_path
):
    for analysis in analyses:
        assert wire(analysis["path_observable"]) == wire(expected_path)
    assert expected_path["counts"]["states"] == 2470
    assert expected_path["counts"]["state_transition_atoms"] <= 99180
    assert expected_path["counts"]["expected_update_coefficient_cells"] == 39520
    assert expected_path["counts"]["semigroup_coefficient_cells"] <= 25390080


def test_all_induced_successors_preserve_supports_without_creation_and_m_t_are_disjoint(
    independent, expected_path
):
    states = independent[0]["states"]
    features = expected_path["states"]
    support_masks = [
        [sum(1 << v for v in support) for support in feature["path_supports"]]
        for feature in features
    ]
    kept_masks = [sum(1 << v for v in state["kept"]) for state in states]
    for state, feature in zip(states, features, strict=True):
        assert not (
            {tuple(support) for support in state["motif_supports"]}
            & {tuple(support) for support in feature["path_supports"]}
        )
        odd, even = state["color_sizes"]
        assert state["motif_count"] + feature["path_count"] <= comb(odd, 2) * comb(even, 2) <= 9
        for atom in state["transitions"]:
            sid = atom["target_state"]
            assert support_masks[sid] == [
                mask for mask in support_masks[state["state_id"]] if mask & kept_masks[sid] == mask
            ]


def test_path_partition_comparison_counts_split_fibers_not_cardinality_difference(
    independent, expected_path
):
    states = independent[0]["states"]
    ids = expected_path["state_classes"]
    b = [state["classes"]["pair_graded"] for state in states]
    c = [state["classes"]["motif_pair"] for state in states]
    assert refines_ids(ids, b) and refines_ids(ids, c)
    assert expected_path["comparison"] == {
        "candidate_refines_pair": True,
        "candidate_refines_motif_pair": True,
        "motif_pair_refines_candidate": refines_ids(c, ids),
        "same_memberships_as_motif_pair": ids == c,
    }
    split_groups = [
        group
        for group in independent[0]["partitions"]["motif_pair"]
        if len({ids[sid] for sid in group["members"]}) > 1
    ]
    assert expected_path["counts"]["split_motif_pair_classes"] == len(split_groups)
    assert sorted(sid for group in expected_path["classes"] for sid in group["members"]) == list(
        range(2470)
    )
    assert all(
        group["members"] == sorted(set(group["members"])) for group in expected_path["classes"]
    )


def test_closed_path_quotient_or_failure_is_verified_without_substitution(
    independent, expected_path
):
    candidate = expected_path
    states = independent[0]["states"]
    if not candidate["closed"]:
        assert candidate["quotient_rows"] == [] and candidate["semigroup"] is None
        failure = candidate["first_failure"]
        assert failure is not None
        assert (
            candidate["state_classes"][failure["left_state"]]
            == candidate["state_classes"][failure["right_state"]]
            == failure["class_id"]
        )
        assert any(
            evaluate(failure["left_coefficients"], x, y)
            != evaluate(failure["right_coefficients"], x, y)
            for x, y in POINTS[:16]
        )
    else:
        assert candidate["first_failure"] is None
        for group, row in zip(candidate["classes"], candidate["quotient_rows"], strict=True):
            assert row["representative_state"] == group["members"][0]
            assert all(
                candidate["pushforward_rows"][sid]["transitions"] == row["transitions"]
                for sid in group["members"]
            )
        assert candidate["semigroup"]["verified"] is True
    for state, row in zip(states, candidate["pushforward_rows"], strict=True):
        assert row["state_id"] == state["state_id"]
        assert all(
            sum(atom["coefficients"][i][j] for atom in row["transitions"]) == int(i == j == 0)
            for i, j in product(range(4), repeat=2)
        )
        for x, y in product((F(0), F(1)), repeat=2):
            positive = {
                atom["target_class"]: evaluate(atom["coefficients"], x, y)
                for atom in row["transitions"]
                if evaluate(atom["coefficients"], x, y)
            }
            assert len(positive) == 1 and sum(positive.values()) == 1
            if x == y == 1:
                assert positive == {candidate["state_classes"][state["state_id"]]: F(1)}


def test_prespecified_complete_almost_complete_and_old_obstruction_features(
    independent, expected_path
):
    states, aliases = independent[0]["states"], independent[1]
    for pi in (517, 1029):
        sid = aliases[pi, 63]
        assert states[sid]["motif_count"] == 9 and expected_path["states"][sid]["path_count"] == 0
    for pi in (516, 1028):
        sid = aliases[pi, 63]
        assert states[sid]["motif_count"] == 5 and expected_path["states"][sid]["path_count"] == 4
    star, path = (aliases[pi, 63] for pi in (84, 91))
    assert states[star]["classes"]["motif_pair"] == states[path]["classes"]["motif_pair"]
    assert [expected_path["states"][sid]["path_count"] for sid in (star, path)] == [0, 1]
    assert expected_path["state_classes"][star] != expected_path["state_classes"][path]


def test_overlapping_path_support_expectation_needs_no_support_independence(executors):
    _, source_case, supports = next(
        row for row in path_cases() if row[0] == "overlapping_k23_missing_edge"
    )
    assert len(supports) == 2 and motif_supports(**source_case) == [[1, 2, 3, 4]]
    eligible = source_case["eligible"]
    mean, joint = zero_table(), zero_table()
    for mask in range(32):
        kept = [v for bit, v in enumerate(eligible) if mask & (1 << bit)]
        observation = restrict_observation(source_case, kept)
        wanted = [support for support in supports if set(support) <= set(kept)]
        for module in executors:
            assert module.path_supports(**observation) == wanted
        odd = sum(v % 2 for v in kept)
        coefficients = kernel(2, 3, odd, len(kept) - odd)
        for i, j in product(range(4), repeat=2):
            mean[i][j] += len(wanted) * coefficients[i][j]
            joint[i][j] += int(len(wanted) == 2) * coefficients[i][j]
    expected_mean, expected_joint = zero_table(), zero_table()
    expected_mean[2][2], expected_joint[2][3] = 2, 1
    assert mean == expected_mean and joint == expected_joint
    assert evaluate(mean, F(1, 2), F(1, 2)) == F(1, 8)
    assert evaluate(joint, F(1, 2), F(1, 2)) == F(1, 32) != F(1, 16) ** 2


def test_empty_path_recognizer_recovers_exact_failed_n_candidate(executors, analyses, monkeypatch):
    for module, baseline in zip(executors, analyses, strict=True):
        with monkeypatch.context() as patch:
            patch.setattr(module, "path_supports", lambda kept, past, eligible: [])
            changed = module.analyze(problem())
        assert wire(
            {key: value for key, value in changed.items() if key != "path_observable"}
        ) == wire({key: value for key, value in baseline.items() if key != "path_observable"})
        path = changed["path_observable"]
        old = changed["closure"]["motif_pair"]
        assert path["closed"] is old["closed"] is False
        assert path["quotient_rows"] == [] and path["semigroup"] is None
        assert wire(path["first_failure"]) == wire(old["first_collision"])
        assert path["state_classes"] == [
            state["classes"]["motif_pair"] for state in changed["states"]
        ]
        assert all(row["path_count"] == 0 and row["path_supports"] == [] for row in path["states"])
        assert all(
            row["coefficients"] == row["expected_coefficients"] == zero_table()
            for row in path["expected_update"]["rows"]
        )
        assert path["counts"]["split_motif_pair_classes"] == 0
        for candidate, group in zip(
            path["classes"], changed["partitions"]["motif_pair"], strict=True
        ):
            assert candidate == {**group, "key": [*group["key"], 0]}
        assert path["comparison"] == {
            "candidate_refines_pair": True,
            "candidate_refines_motif_pair": True,
            "motif_pair_refines_candidate": True,
            "same_memberships_as_motif_pair": True,
        }


def test_whole_n_analysis_and_old_audits_are_preserved_not_reinterpreted(
    analyses, aggregate, pinned_n
):
    for analysis in analyses:
        assert wire(
            {key: value for key, value in analysis.items() if key != "path_observable"}
        ) == wire(pinned_n["analysis"])
    _, suite = aggregate
    for key in ("audit", "prior_bridge", "controls"):
        assert wire(suite[key]) == wire(pinned_n[key])
    assert suite["base_candidate_closed"] is pinned_n["candidate_closed"] is False
    assert suite["candidate_closed"] is suite["analysis"]["path_observable"]["closed"]


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
        "path_observable",
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
        "path_observable",
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
valid = {"schema_version":"det8-qr05o-problem-v1","family":"qr05o_path_iid"}
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
for i, filename in enumerate(("path_observable.py","reference_qr05o.py")):
    name = "_qr05o_optimized_guards_" + str(i)
    spec = importlib.util.spec_from_file_location(name, root / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("missing executor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    actual = module.motif_supports([6,1,4,3],[[1,3],[],[1,3],[]],[1,3,4,6])
    if type(actual) is not list or actual != [[1,3,4,6]] or any(type(v) is not int for row in actual for v in row):
        raise RuntimeError("optimized marked-order recognition differs")
    path = module.path_supports([6,1,4,3],[[1,3],[],[1],[]],[1,3,4,6])
    if type(path) is not list or path != [[1,3,4,6]] or any(type(v) is not int for row in path for v in row):
        raise RuntimeError("optimized induced-path recognition differs")
    for value in invalid:
        try:
            module.analyze(value)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError("optimized invalid input accepted")
print(json.dumps({"valid_recognizers":2,"valid_path_recognizers":2,"explicit_rejections":rejected}))
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
    assert json.loads(result.stdout) == {
        "valid_recognizers": 2,
        "valid_path_recognizers": 2,
        "explicit_rejections": 22,
    }


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
    assert suite["base_candidate_closed"] is a["closure"]["motif_pair"]["closed"]
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


@pytest.mark.parametrize(
    "kind",
    (
        "count_bool",
        "missing_support",
        "duplicate_support",
        "support_bool",
        "state_bool",
        "class_bool",
        "same_sizes_wrong_fibers",
        "expectation",
        "pushed_coefficient",
        "closure_flag",
        "failure_record",
        "invalid_quotient",
        "semigroup",
        "comparison_int",
        "split_count",
        "component_overflow",
    ),
)
def test_path_audit_rejects_feature_fiber_law_and_certificate_corruption(aggregate, analyses, kind):
    runner, _ = aggregate
    changed = {**analyses[0], "path_observable": json.loads(wire(analyses[0]["path_observable"]))}
    path = changed["path_observable"]
    positive = next(row for row in path["states"] if row["path_count"])
    if kind == "count_bool":
        path["states"][0]["path_count"] = False
    elif kind == "missing_support":
        positive["path_supports"] = []
    elif kind == "duplicate_support":
        positive["path_supports"].append(list(positive["path_supports"][0]))
    elif kind == "support_bool":
        first_one = next(
            row for row in path["states"] if any(1 in support for support in row["path_supports"])
        )
        support = next(support for support in first_one["path_supports"] if 1 in support)
        support[support.index(1)] = True
    elif kind == "state_bool":
        path["states"][0]["state_id"] = False
    elif kind == "class_bool":
        path["state_classes"][0] = False
    elif kind == "same_sizes_wrong_fibers":
        left, right = [group for group in path["classes"] if len(group["members"]) > 1][:2]
        a, b = left["members"][-1], right["members"][-1]
        left["members"] = sorted(b if sid == a else sid for sid in left["members"])
        right["members"] = sorted(a if sid == b else sid for sid in right["members"])
        path["state_classes"][a], path["state_classes"][b] = (
            path["state_classes"][b],
            path["state_classes"][a],
        )
        assert [len(group["members"]) for group in path["classes"]] == [
            len(group["members"]) for group in analyses[0]["path_observable"]["classes"]
        ]
        assert path["counts"] == analyses[0]["path_observable"]["counts"]
        assert sorted(sid for group in path["classes"] for sid in group["members"]) == list(
            range(2470)
        )
    elif kind == "expectation":
        path["expected_update"]["rows"][positive["state_id"]]["expected_coefficients"][2][2] += 1
    elif kind == "pushed_coefficient":
        path["pushforward_rows"][0]["transitions"][0]["coefficients"][0][0] = 2
    elif kind == "closure_flag":
        path["closed"] = not path["closed"]
    elif kind == "failure_record":
        path["first_failure"] = (
            {
                "class_id": 0,
                "left_state": 0,
                "right_state": 1,
                "target_class": 0,
                "left_coefficients": zero_table(),
                "right_coefficients": zero_table(),
            }
            if path["closed"]
            else None
        )
    elif kind == "invalid_quotient":
        if path["closed"]:
            path["quotient_rows"][0]["transitions"][0]["coefficients"][0][0] = 2
        else:
            path["quotient_rows"] = [{"class_id": 0, "representative_state": 0, "transitions": []}]
    elif kind == "semigroup":
        if path["closed"]:
            path["semigroup"]["totals"]["coefficient_cells"] += 1
        else:
            path["semigroup"] = {"verified": True, "rows": [], "totals": {}}
    elif kind == "comparison_int":
        path["comparison"]["candidate_refines_pair"] = 1
    elif kind == "split_count":
        path["counts"]["split_motif_pair_classes"] += 1
    else:
        path["states"][0]["path_count"] = 1 << 4096
    with pytest.raises(ValueError):
        runner.check_path_observable(changed)


@pytest.mark.parametrize("kind", ("old_count_bool", "old_closure", "old_audit"))
def test_n_bridge_rejects_changed_prior_projection_or_retained_base_evidence(
    aggregate, analyses, kind
):
    runner, suite = aggregate
    changed, changed_suite = dict(analyses[0]), dict(suite)
    if kind == "old_count_bool":
        changed["states"] = list(changed["states"])
        changed["states"][0] = {
            **changed["states"][0],
            "chain_counts": [True, *changed["states"][0]["chain_counts"][1:]],
        }
    elif kind == "old_closure":
        changed["closure"] = {
            **changed["closure"],
            "motif_pair": {**changed["closure"]["motif_pair"], "closed": True},
        }
    else:
        changed_suite["audit"] = {**changed_suite["audit"], "verified": 1}
    with pytest.raises(ValueError):
        runner.n_bridge(changed, changed_suite)


def test_retained_path_audit_and_n_bridge_distinguish_the_two_candidate_outcomes(
    aggregate, expected_path
):
    _, suite = aggregate
    counts = expected_path["counts"]
    assert wire(suite["path_audit"]) == wire(
        {
            "verified": True,
            "feature_rows": 2470,
            "expected_update_coefficient_cells": 39520,
            "pushed_coefficient_cells": counts["state_coefficient_cells"],
            "semigroup_coefficient_cells": counts["semigroup_coefficient_cells"],
            "rate_points": 22,
            "evaluated_atoms": 22 * counts["state_transition_atoms"],
            "deterministic_corner_rows": 9880,
            "closed": expected_path["closed"],
        }
    )
    assert wire(suite["n_bridge"]) == wire(
        {
            "prior_artifact": "qr-05n-domain-portability-2026-09-06/results.json",
            "matched_states": 2470,
            "matched_aliases": 65888,
            "whole_analysis_projection_equal": True,
            "retained_suite_fields": ["audit", "prior_bridge", "controls"],
            "base_candidate_closed": False,
            "new_candidate_required_to_equal_old_partition": False,
            "old_restricted_M_quotient_preserved": True,
        }
    )
    assert suite["candidate_closed"] is expected_path["closed"]
    assert suite["base_candidate_closed"] is False
    assert suite["coarsest_closed_refinement_claimed"] is False
    assert suite["path_is_directed_three_step_chain"] is False
    assert wire(suite["totals"]["path_observable"]) == wire(counts)
    assert suite["totals"]["all_checked_semigroup_coefficient_cells"] == (
        suite["analysis"]["counts"]["semigroup_coefficient_cells"]
        + counts["semigroup_coefficient_cells"]
        + suite["prior_bridge"]["restricted_candidate_quotient"]["semigroup"]["totals"][
            "coefficient_cells"
        ]
    )


def test_retained_path_recognizer_and_overlap_inventory(aggregate):
    _, suite = aggregate
    controls = suite["path_controls"]
    assert controls["recognizer_case_count"] == len(controls["recognizer_cases"]) == 22
    assert {row["name"] for row in controls["recognizer_cases"]} == {
        *(
            f"{direction}_missing_{index}"
            for direction in ("forward", "reverse")
            for index in range(4)
        ),
        "two_cross_edges",
        "complete_k22",
        "same_color_relation",
        "wrong_layer_colors",
        "wrong_color_cardinality",
        "total_order_not_cover_path",
        "fixed_corner_excluded",
        "reordered_local_positions",
        "color_preserving_relabel",
        "color_exchange",
        "outside_vertex",
        "intermediary_full",
        "intermediary_induced_removed",
        "overlapping_k23_minus_edge",
    }
    for row in controls["recognizer_cases"]:
        assert set(row) == {
            "name",
            "kept",
            "past",
            "eligible",
            "expected_paths",
            "expected_motifs",
            "primary_paths",
            "reference_paths",
            "primary_motifs",
            "reference_motifs",
            "verified",
        }
        args = {key: row[key] for key in ("kept", "past", "eligible")}
        expected = independent_path_supports(**args)
        motifs = motif_supports(**args)
        assert row["verified"] is True
        for key in ("expected_paths", "primary_paths", "reference_paths"):
            assert wire(row[key]) == wire(expected)
        for key in ("expected_motifs", "primary_motifs", "reference_motifs"):
            assert wire(row[key]) == wire(motifs)
    source = next(
        row for row in controls["recognizer_cases"] if row["name"] == "overlapping_k23_minus_edge"
    )
    assert source["expected_paths"] == [[1, 2, 3, 6], [1, 3, 4, 6]]
    atoms = []
    for mask in range(32):
        kept = [v for bit, v in enumerate(source["eligible"]) if mask & (1 << bit)]
        count = sum(set(support) <= set(kept) for support in source["expected_paths"])
        odd = sum(v % 2 for v in kept)
        atoms.append(
            {
                "mask": mask,
                "kept": kept,
                "path_count": count,
                "both_supports": count == 2,
                "coefficients": kernel(2, 3, odd, len(kept) - odd),
            }
        )
    expected_mean, expected_joint = zero_table(), zero_table()
    expected_mean[2][2], expected_joint[2][3] = 2, 1
    assert wire(controls["overlap_expectation"]) == wire(
        {
            "source_case": "overlapping_k23_minus_edge",
            "atoms": atoms,
            "coefficients": expected_mean,
            "expected_coefficients": expected_mean,
            "joint_support_coefficients": expected_joint,
            "expected_joint_support_coefficients": expected_joint,
            "product_marginal_powers": [4, 4],
            "half_probabilities": {"joint": "1/32", "product_marginals": "1/256"},
            "coefficient_cells": 32,
            "verified": True,
            "independent_support_survival_assumed": False,
        }
    )
    assert controls["synthetic_cases_in_certified_domain"] is False
    assert controls["feature_redefined_after_outcome"] is False
    assert suite["totals"]["path_recognizer_cases"] == 22


def test_retained_path_domain_controls_and_any_remaining_failure_are_measured(
    aggregate, independent, expected_path
):
    _, suite = aggregate
    states, aliases = independent[0]["states"], independent[1]
    controls = suite["path_controls"]
    domain = []
    for pi in (517, 1029, 516, 1028):
        sid = aliases[pi, 63]
        feature = expected_path["states"][sid]
        domain.append(
            {
                "profile_index": pi,
                "mask": 63,
                "state_id": sid,
                "path_count": feature["path_count"],
                "motif_count": states[sid]["motif_count"],
                "path_supports": feature["path_supports"],
                "expected_update": expected_path["expected_update"]["rows"][sid],
            }
        )
    assert wire(controls["domain_controls"]) == wire(domain)
    pair = [aliases[pi, 63] for pi in (84, 91)]
    assert wire(controls["old_obstruction"]) == wire(
        {
            "state_ids": pair,
            "base_classes": [states[sid]["classes"]["motif_pair"] for sid in pair],
            "path_counts": [0, 1],
            "new_classes": [expected_path["state_classes"][sid] for sid in pair],
            "distinguished": True,
        }
    )
    failure = expected_path["first_failure"]
    if failure is None:
        assert controls["candidate_counterexample"] is None
        return
    sides = [states[failure[key]] for key in ("left_state", "right_state")]
    evaluations = []
    distinguishing = []
    for index, (x, y) in enumerate(POINTS):
        a, b = (evaluate(failure[key], x, y) for key in ("left_coefficients", "right_coefficients"))
        evaluations.append(
            {"rates": [str(x), str(y)], "left_probability": str(a), "right_probability": str(b)}
        )
        if index < 16 and a != b:
            distinguishing.append(index)
    assert distinguishing
    laws = [full_count_law(states, state) for state in sides]
    assert wire(controls["candidate_counterexample"]) == wire(
        {
            "witness": failure,
            "equal_current_key": expected_path["classes"][failure["class_id"]]["key"],
            "observations": [
                {
                    key: state[key]
                    for key in (
                        "state_id",
                        "frame_id",
                        "kept",
                        "past",
                        "chain_counts",
                        "motif_count",
                    )
                }
                for state in sides
            ],
            "path_counts": [
                expected_path["states"][state["state_id"]]["path_count"] for state in sides
            ],
            "evaluations": evaluations,
            "first_distinguishing_grid_index": distinguishing[0],
            "full_count_laws": laws,
            "full_count_laws_equal": wire(laws[0]) == wire(laws[1]),
        }
    )
