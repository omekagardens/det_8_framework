"""Independent Q reachability, induced-order, unchanged-summary tests.

Raw sources, features and kernels are rebuilt; only pinned prior JSON is read.
Helper arithmetic is locally carried from this test author's P lineage.
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
O_SHA = "3364b36813f745a645d78d6d30caa292778da986cb6d1140f108a0fd4b945eb1"
P_SHA = "c43435c4916e5c15efb373ff70795ed733d7c4e360ebec4e9a1b32f4e050b048"
BASE_NAMES = ("ferrers6", "standard_example3", "chain6", "ferrers6_fixed", "path6", "cycle4_edge")
GENERATORS = ((1, 3), (1, 4), (2, 3), (2, 4), (3, 5), (3, 6), (4, 5), (4, 6))
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


def problem():
    return {"schema_version": "det8-qr05q-problem-v1", "family": "qr05q_three_layer"}


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05q_test_direct", "portability.py"),
        private_module("_qr05q_test_reference", "reference_qr05q.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors):
    return tuple(module.analyze(problem()) for module in executors)


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05q_test_aggregate", "study.py")
    return runner, runner.run_suite()


def prior_suite(directory, expected_sha, expected_bytes):
    path = HERE.parent / directory / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == expected_bytes and hashlib.sha256(raw).hexdigest() == expected_sha
    envelope = json.loads(raw)
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


@pytest.fixture(scope="session")
def pinned_o():
    return prior_suite("qr-05o-path-observable-2026-09-06", O_SHA, 27143093)


@pytest.fixture(scope="session")
def pinned_p():
    return prior_suite("qr-05p-minimal-summary-2026-09-06", P_SHA, 3882409)


@cache
def source(index):
    edges = {(0, v) for v in range(1, 8)} | {(v, 7) for v in range(7)}
    if index >= 1030:
        reverse = index >= 1286
        mask = index - (1286 if reverse else 1030)
        name = f"three_layer_{'reverse' if reverse else 'forward'}_{mask:03d}"
        edges |= {
            (b, a) if reverse else (a, b)
            for bit, (a, b) in enumerate(GENERATORS)
            if mask & (1 << bit)
        }
    elif index >= 6:
        reverse = index >= 518
        mask = index - (518 if reverse else 6)
        name = f"layered_{'eo' if reverse else 'oe'}_{mask:03d}"
        for i, j in product(range(3), repeat=2):
            if mask & (1 << (3 * i + j)):
                odd, even = 2 * i + 1, 2 * j + 2
                edges.add((even, odd) if reverse else (odd, even))
    else:
        name = BASE_NAMES[index]
        if index == 2:
            edges |= set(combinations(range(1, 7), 2))
        elif index == 4:
            edges |= {(1, 2), (1, 4), (3, 4), (3, 6), (5, 6)}
        elif index == 5:
            edges |= {(1, 4), (1, 6), (3, 4), (3, 6), (2, 5)}
        else:
            edges |= {
                (i + 1, j + 4)
                for i, j in product(range(3), repeat=2)
                if (i != j if index == 1 else i <= j)
            }
    reachable = [[(a, b) in edges for b in range(8)] for a in range(8)]
    for middle in range(8):
        for a, b in product(range(8), repeat=2):
            reachable[a][b] = reachable[a][b] or (reachable[a][middle] and reachable[middle][b])
    assert not any(reachable[a][a] for a in range(8))
    past = [[a for a in range(8) if reachable[a][b]] for b in range(8)]
    return name, past, int(index == 3)


@pytest.fixture(scope="session")
def independent_domain():
    frames = [
        {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
        {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
    ]
    profiles, states, aliases, registry = [], [], {}, {}
    for index in range(1542):
        name, original, fid = source(index)
        frame = frames[fid]
        ids = []
        for mask in range(1 << len(frame["eligible"])):
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(frame["eligible"]) if mask & (1 << bit)]
            )
            past = [[i for i, a in enumerate(kept) if a in original[b]] for b in kept]
            key = state_key(fid, kept, past)
            sid = registry.setdefault(key, len(registry))
            if sid == len(states):
                states.append({"state_id": sid, "frame_id": fid, "kept": kept, "past": past})
            ids.append(sid)
            aliases[index, mask] = sid
        profiles.append(
            {
                "profile_index": index,
                "name": name,
                "frame_id": fid,
                "past": original,
                "state_ids": ids,
            }
        )
    assert len(aliases) == 98656
    assert len(states) <= 35238
    return {"frames": frames, "profiles": profiles, "states": states}, aliases


@pytest.fixture(scope="session")
def independent(independent_domain):
    domain, aliases = independent_domain
    frames, states = domain["frames"], domain["states"]
    fs = [observed_features(state, frames[state["frame_id"]]) for state in states]
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
    lookup = {
        state_key(row["frame_id"], row["kept"], row["past"]): row["state_id"] for row in states
    }
    fine = []
    for state, feature in zip(states, fs, strict=True):
        frame = frames[state["frame_id"]]
        retained_eligible = sorted(set(state["kept"]) & set(frame["eligible"]))
        rel = relation_of(state)
        atoms = []
        for mask in range(1 << len(retained_eligible)):
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(retained_eligible) if mask & (1 << bit)]
            )
            past = [[i for i, a in enumerate(kept) if (a, b) in rel] for b in kept]
            target = lookup[state_key(state["frame_id"], kept, past)]
            atoms.append(
                {
                    "target_state": target,
                    "coefficients": kernel(*feature["color_sizes"], *fs[target]["color_sizes"]),
                }
            )
        fine.append(
            {
                "state_id": state["state_id"],
                "transitions": sorted(atoms, key=lambda atom: atom["target_state"]),
            }
        )
    rows = pushed(fine, part["state_classes"])
    witness = None
    comparisons = 0
    for group in part["classes"]:
        left = group["members"][0]
        for right in group["members"][1:]:
            comparisons += 1
            difference = first_difference(rows[left]["transitions"], rows[right]["transitions"])
            if difference is not None and witness is None:
                target, a, b = difference
                rates = next(
                    [str(x), str(y)] for x, y in NODES if evaluate(a, x, y) != evaluate(b, x, y)
                )
                witness = {
                    "class_id": group["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "target_class": target,
                    "left_coefficients": a,
                    "right_coefficients": b,
                    "first_distinguishing_rates": rates,
                }
    closed = witness is None
    quotient = (
        [
            {
                "class_id": group["class_id"],
                "representative_state": group["members"][0],
                "transitions": rows[group["members"][0]]["transitions"],
            }
            for group in part["classes"]
        ]
        if closed
        else []
    )
    atoms = sum(len(row["transitions"]) for row in fine)
    assert atoms <= 472428
    a = {
        "domain": domain,
        "features": fs,
        "partition": part,
        "fine_kernel": {
            "sha256": digest(fine),
            "transition_atoms": atoms,
            "coefficient_cells": 16 * atoms,
            "normalization_rows": len(states),
            "deterministic_corner_rows": 4 * len(states),
            "rate_points": 22,
            "evaluated_atoms": 22 * atoms,
        },
        "pushed_rows": rows,
        "closure": {
            "closed": closed,
            "classes_checked": len(part["classes"]),
            "member_comparisons": comparisons,
            "witness": witness,
        },
        "quotient_rows": quotient,
        "semigroup": composition(quotient) if closed else None,
        "expected_updates": {
            "motif_cells": 16 * len(states),
            "path_cells": 16 * len(states),
            "max_abs_residual": 0,
        },
        "counts": {
            "profiles": 1542,
            "aliases": 98656,
            "states": len(states),
            "classes": len(part["classes"]),
            "fine_atoms": atoms,
            "pushed_atoms": sum(len(row["transitions"]) for row in rows),
        },
    }
    return a, fine, aliases


def test_complete_dual_wire_agrees_with_independent_reconstruction(analyses, independent):
    expected = independent[0]
    assert wire(analyses[0]) == wire(analyses[1]) == wire(expected)
    assert wire(json.loads(wire(analyses[0]))) == wire(analyses[0])
    assert len(wire(analyses[0])) < 64 * 1024 * 1024
    assert set(analyses[0]) == {
        "domain",
        "features",
        "partition",
        "fine_kernel",
        "pushed_rows",
        "closure",
        "quotient_rows",
        "semigroup",
        "expected_updates",
        "counts",
    }
    for forbidden in ("stabilization", "refinement", "consumer", "trace_audit", "covariance_tower"):
        assert forbidden not in analyses[0]


def test_all_new_incidence_bits_have_exact_untransposed_reachability(independent_domain):
    profiles = independent_domain[0]["profiles"]
    for mask in range(256):
        forward = {edge for bit, edge in enumerate(GENERATORS) if mask & (1 << bit)}
        skips = {
            (a, b)
            for a in (1, 2)
            for b in (5, 6)
            if any((a, middle) in forward and (middle, b) in forward for middle in (3, 4))
        }
        expected = forward | skips
        for reverse in (False, True):
            pi = (1286 if reverse else 1030) + mask
            actual = {
                (a, b)
                for b, before in enumerate(profiles[pi]["past"])
                for a in before
                if a not in (0, 7) and b not in (0, 7)
            }
            wanted = {(b, a) for a, b in expected} if reverse else expected
            assert actual == wanted
            assert (
                profiles[pi]["name"]
                == f"three_layer_{'reverse' if reverse else 'forward'}_{mask:03d}"
            )
            assert profiles[pi]["frame_id"] == 0
            assert all(0 in profiles[pi]["past"][v] for v in range(1, 8))
            assert profiles[pi]["past"][0] == [] and profiles[pi]["past"][7] == list(range(7))
            assert all(
                a in profiles[pi]["past"][c]
                for b in range(8)
                for a in profiles[pi]["past"][b]
                for c in range(8)
                if b in profiles[pi]["past"][c]
            )
    for bit, (a, b) in enumerate(GENERATORS):
        assert a in profiles[1030 + (1 << bit)]["past"][b]
        assert b in profiles[1286 + (1 << bit)]["past"][a]
    assert 4 in profiles[1288]["past"][1] and 3 not in profiles[1288]["past"][2]


def test_mask17_keeps_transitive_comparison_after_intermediary_deletion(independent):
    a, _, aliases = independent
    states, fs = a["domain"]["states"], a["features"]
    for pi in (1047, 1303):
        full = aliases[pi, 63]
        reduced = aliases[pi, 17]  # Original eligible IDs1 and5, not the generator mask.
        assert states[reduced]["kept"] == [0, 1, 5, 7]
        relation = relation_of(states[reduced])
        assert ((1, 5) if pi == 1047 else (5, 1)) in relation
        assert fs[full]["chain_counts"] == [1, 6, 3, 1]
        assert fs[full]["mean_graded"][3][3][0] == 1
        assert sum(map(sum, fs[full]["mean_graded"][3])) == 1
        assert fs[full]["motif_count"] == fs[full]["path_count"] == 0
        assert fs[reduced]["chain_counts"] == [1, 2, 1, 0]
        assert fs[reduced]["color_sizes"] == [2, 0]
        # Keeping only surviving generators would lose this comparison.
        surviving_generators = [
            edge for bit, edge in enumerate(GENERATORS) if 17 & (1 << bit) and set(edge) <= {1, 5}
        ]
        assert surviving_generators == []


def test_complete_three_layers_count_comparabilities_and_three_chains(independent):
    a, _, aliases = independent
    for pi in (1285, 1541):
        sid = aliases[pi, 63]
        feature = a["features"][sid]
        assert feature["chain_counts"] == [1, 6, 12, 8]
        assert feature["mean_graded"][3] == [[0, 0, 0, 1], [0, 0, 3, 0], [0, 3, 0, 0], [1, 0, 0, 0]]
        assert (
            len(
                {
                    (u, v)
                    for u, v in relation_of(a["domain"]["states"][sid])
                    if u not in (0, 7) and v not in (0, 7)
                }
            )
            == 12
        )


def test_first_occurrence_aliases_raw_dedup_and_frame_marks_are_exact(independent):
    a, fine, aliases = independent
    domain = a["domain"]
    seen = {}
    for profile in domain["profiles"]:
        pi, fid = profile["profile_index"], profile["frame_id"]
        frame = domain["frames"][fid]
        assert len(profile["state_ids"]) == (32 if pi == 3 else 64)
        for mask, sid in enumerate(profile["state_ids"]):
            assert aliases[pi, mask] == sid
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(frame["eligible"]) if mask & (1 << bit)]
            )
            past = [[i for i, u in enumerate(kept) if u in profile["past"][v]] for v in kept]
            identity = state_key(fid, kept, past)
            if identity not in seen:
                assert sid == len(seen)
                seen[identity] = sid
            assert sid == seen[identity]
            assert domain["states"][sid] == {
                "state_id": sid,
                "frame_id": fid,
                "kept": kept,
                "past": past,
            }
    assert len(seen) == a["counts"]["states"]
    assert all(set(s) == {"state_id", "frame_id", "kept", "past"} for s in domain["states"])
    empty = aliases[0, 0]
    assert sum(sid == empty for sid in aliases.values()) == 1541
    assert fine[empty]["transitions"] == [
        {"target_state": empty, "coefficients": kernel(0, 0, 0, 0)}
    ]
    fixed = aliases[3, 0]
    assert domain["states"][fixed]["kept"] == [0, 3, 7]
    assert a["features"][fixed]["color_sizes"] == [0, 0]
    assert a["features"][fixed]["mean_graded"][1][0][0] == 1
    assert fixed != empty


def test_all_features_count_ordered_pairs_fixed_exclusion_and_disjoint_induced_supports(
    independent,
):
    a = independent[0]
    for state, feature in zip(a["domain"]["states"], a["features"], strict=True):
        d, b, n = feature["mean_graded"], feature["pair_graded"], feature["chain_counts"]
        assert b[0] == d
        for q, r in product(range(4), repeat=2):
            assert b[q][r] == b[r][q]
            assert sum(map(sum, b[q][r])) == n[q] * n[r]
        assert n == [sum(map(sum, row)) for row in d]
        assert n[0] == 1
        odd, even = feature["color_sizes"]
        assert feature["motif_count"] + feature["path_count"] <= comb(odd, 2) * comb(even, 2) <= 9
        motifs, paths = (
            {tuple(s) for s in feature[key]} for key in ("motif_supports", "path_supports")
        )
        assert not motifs & paths
        for support in motifs | paths:
            assert len(support) == len(set(support)) == 4
            assert sum(v % 2 for v in support) == 2
            assert set(support) <= set(a["domain"]["frames"][state["frame_id"]]["eligible"])
            if state["frame_id"] == 1:
                assert 3 not in support


@cache
def evaluated_at_audit_points(table):
    return tuple(evaluate_tuple(table, x, y) for x, y in POINTS)


@cache
def direct_at_audit_points(odd, even, o, e):
    return tuple(direct_probability(odd, even, o, e, x, y) for x, y in POINTS)


def test_all_fine_laws_are_normalized_nonnegative_and_corner_deterministic(independent):
    a, fine, _ = independent
    features, states = a["features"], a["domain"]["states"]
    atoms_checked = 0
    for state, feature, row in zip(states, features, fine, strict=True):
        assert row["state_id"] == state["state_id"]
        assert len(row["transitions"]) == 2 ** sum(feature["color_sizes"])
        assert [atom["target_state"] for atom in row["transitions"]] == sorted(
            {atom["target_state"] for atom in row["transitions"]}
        )
        assert all(
            sum(atom["coefficients"][i][j] for atom in row["transitions"]) == int(i == j == 0)
            for i, j in product(range(4), repeat=2)
        )
        for atom in row["transitions"]:
            target = atom["target_state"]
            assert states[target]["frame_id"] == state["frame_id"]
            assert set(states[target]["kept"]) <= set(state["kept"])
            table = tuple(tuple(line) for line in atom["coefficients"])
            values = evaluated_at_audit_points(table)
            assert values == direct_at_audit_points(
                *feature["color_sizes"], *features[target]["color_sizes"]
            )
            assert all(value >= 0 for value in values)
            assert all(type(c) is int for line in table for c in line)
            atoms_checked += 1
        for x, y in product((F(0), F(1)), repeat=2):
            positive = [
                (atom["target_state"], evaluate(atom["coefficients"], x, y))
                for atom in row["transitions"]
                if evaluate(atom["coefficients"], x, y)
            ]
            assert len(positive) == 1 and positive[0][1] == 1
            target = positive[0][0]
            if x == y == 1:
                assert target == state["state_id"]
            if x == y == 0:
                assert states[target]["kept"] == a["domain"]["frames"][state["frame_id"]]["fixed"]
        if len(row["transitions"]) > 1:
            assert any(
                evaluate(atom["coefficients"], F(1), F(1)) == 0 for atom in row["transitions"]
            )
    assert atoms_checked == a["counts"]["fine_atoms"]
    assert 22 * atoms_checked == a["fine_kernel"]["evaluated_atoms"]


def test_all_induced_successors_preserve_motif_supports_and_both_exact_expectations(independent):
    a, fine, _ = independent
    fs, states = a["features"], a["domain"]["states"]
    kept_masks = [sum(1 << v for v in state["kept"]) for state in states]
    support_masks = {
        name: [[sum(1 << v for v in support) for support in feature[name]] for feature in fs]
        for name in ("motif_supports", "path_supports")
    }
    checked = 0
    for feature, row in zip(fs, fine, strict=True):
        sid = row["state_id"]
        motif, path = zero(), zero()
        for atom in row["transitions"]:
            target = atom["target_state"]
            for name in support_masks:
                expected = [
                    support
                    for support in support_masks[name][sid]
                    if support & kept_masks[target] == support
                ]
                assert support_masks[name][target] == expected
            for i, j in product(range(4), repeat=2):
                motif[i][j] += atom["coefficients"][i][j] * fs[target]["motif_count"]
                path[i][j] += atom["coefficients"][i][j] * fs[target]["path_count"]
            checked += 1
        expected_motif, expected_path = zero(), zero()
        expected_motif[2][2], expected_path[2][2] = feature["motif_count"], feature["path_count"]
        assert motif == expected_motif and path == expected_path
    assert checked == a["counts"]["fine_atoms"]
    assert a["expected_updates"] == {
        "motif_cells": 16 * len(states),
        "path_cells": 16 * len(states),
        "max_abs_residual": 0,
    }


def test_expanded_H_is_only_the_unchanged_observed_key_with_actual_fibers(independent):
    a = independent[0]
    states, fs, part = a["domain"]["states"], a["features"], a["partition"]
    seen = set()
    assert sorted(sid for group in part["classes"] for sid in group["members"]) == list(
        range(len(states))
    )
    for group in part["classes"]:
        assert group["members"] == sorted(set(group["members"]))
        assert wire(group["key"]) not in seen
        seen.add(wire(group["key"]))
        for sid in group["members"]:
            frame = a["domain"]["frames"][states[sid]["frame_id"]]
            expected = [
                [frame["density"], frame["fixed"], frame["eligible"]],
                fs[sid]["pair_graded"],
                fs[sid]["motif_count"],
                fs[sid]["path_count"],
            ]
            assert group["key"] == expected
            assert part["state_classes"][sid] == group["class_id"]
    assert len(seen) == a["counts"]["classes"]


def test_every_member_is_checked_and_failure_never_gets_a_replacement_quotient(independent):
    a = independent[0]
    groups, rows, closure = a["partition"]["classes"], a["pushed_rows"], a["closure"]
    assert closure["classes_checked"] == len(groups)
    assert closure["member_comparisons"] == len(a["features"]) - len(groups)
    all_failures = []
    for group in groups:
        left = group["members"][0]
        for right in group["members"][1:]:
            difference = first_difference(rows[left]["transitions"], rows[right]["transitions"])
            if difference is not None:
                all_failures.append((group["class_id"], left, right, *difference))
    assert closure["closed"] is (not all_failures)
    if all_failures:
        cid, left, right, target, p, q = all_failures[0]
        witness = closure["witness"]
        assert [witness[k] for k in ("class_id", "left_state", "right_state", "target_class")] == [
            cid,
            left,
            right,
            target,
        ]
        assert witness["left_coefficients"] == p and witness["right_coefficients"] == q
        rates = tuple(map(F, witness["first_distinguishing_rates"]))
        assert rates == next(pair for pair in NODES if evaluate(p, *pair) != evaluate(q, *pair))
        assert a["quotient_rows"] == [] and a["semigroup"] is None
    else:
        assert closure["witness"] is None
        assert len(a["quotient_rows"]) == len(groups)
        assert a["semigroup"]["verified"] is True
        for group, row in zip(groups, a["quotient_rows"], strict=True):
            assert row["representative_state"] == group["members"][0]
            assert all(rows[sid]["transitions"] == row["transitions"] for sid in group["members"])


@pytest.fixture(scope="session")
def old_restriction(independent, pinned_o, pinned_p):
    a, fine, _ = independent
    old_o, old_p = pinned_o["analysis"], pinned_p["analysis"]
    domain = a["domain"]
    assert wire(domain["frames"]) == wire(old_o["frames"])
    assert wire(domain["profiles"][:1030]) == wire(old_o["profiles"])
    raw = [
        {key: state[key] for key in ("state_id", "frame_id", "kept", "past")}
        for state in old_o["states"]
    ]
    assert wire(domain["states"][:2470]) == wire(raw)
    assert digest({"frames": domain["frames"], "states": raw}) == old_p["model_sha256"]
    assert wire(a["features"][:2470]) == wire(old_p["features"])
    old_fine = [
        {"state_id": row["state_id"], "transitions": row["transitions"]} for row in old_o["states"]
    ]
    assert wire(fine[:2470]) == wire(old_fine)
    assert digest(old_fine) == old_p["fine_kernel"]["sha256"]
    assert all(atom["target_state"] < 2470 for row in fine[:2470] for atom in row["transitions"])
    vector = a["partition"]["state_classes"][:2470]
    old_ids = old_p["partitions"]["H"]["state_classes"]
    forward, backward = class_map(vector, old_ids), class_map(old_ids, vector)
    assert forward is not None and backward is not None
    groups = [
        {
            "class_id": group["class_id"],
            "key": group["key"],
            "members": [sid for sid in group["members"] if sid < 2470],
        }
        for group in a["partition"]["classes"]
        if group["members"][0] < 2470
    ]
    assert wire({"state_classes": vector, "classes": groups}) == wire(old_p["partitions"]["H"])
    rows = a["pushed_rows"][:2470]
    quotient = []
    for group in groups:
        first = group["members"][0]
        expected = rows[first]["transitions"]
        assert all(rows[sid]["transitions"] == expected for sid in group["members"])
        assert all(atom["target_class"] < len(groups) for atom in expected)
        quotient.append(
            {"class_id": group["class_id"], "representative_state": first, "transitions": expected}
        )
    assert wire(quotient) == wire(old_p["refinement"]["quotient_rows"])
    assert wire(quotient) == wire(old_o["path_observable"]["quotient_rows"])
    semigroup = composition(quotient)
    assert semigroup == old_p["refinement"]["semigroup"]
    return {
        "groups": groups,
        "quotient": quotient,
        "semigroup": semigroup,
        "fine_sha256": digest(old_fine),
        "class_maps": [forward, backward],
    }


def test_old_actual_domain_and_quotient_remain_valid_without_exporting_P_minimality(
    independent, old_restriction
):
    a = independent[0]
    assert len(old_restriction["groups"]) == 167
    assert old_restriction["semigroup"]["verified"] is True
    assert len(a["domain"]["profiles"][:1030]) == 1030
    assert sum(len(row["state_ids"]) for row in a["domain"]["profiles"][:1030]) == 65888
    if not a["closure"]["closed"]:
        assert a["quotient_rows"] == []
        assert old_restriction["quotient"]
    # Closure and minimality have not been inferred from a surviving key or
    # equality of class counts. There is no Q stabilization/repair certificate.
    assert "refinement" not in a and "coarsest" not in a


def synthetic_failure():
    part = {
        "state_classes": [0, 1, 1, 2, 0, 2],
        "classes": [
            {"class_id": 0, "key": [0], "members": [0, 4]},
            {"class_id": 1, "key": [1], "members": [1, 2]},
            {"class_id": 2, "key": [2], "members": [3, 5]},
        ],
    }
    one, xy, complement = zero(), zero(), zero()
    one[0][0], xy[1][1], complement[0][0], complement[1][1] = 1, 1, 1, -1
    rows = [
        {
            "state_id": 0,
            "transitions": [
                {"target_class": 0, "coefficients": xy},
                {"target_class": 1, "coefficients": complement},
            ],
        },
        {"state_id": 1, "transitions": [{"target_class": 2, "coefficients": one}]},
        {"state_id": 2, "transitions": [{"target_class": 1, "coefficients": one}]},
        {"state_id": 3, "transitions": [{"target_class": 2, "coefficients": one}]},
        {"state_id": 4, "transitions": [{"target_class": 1, "coefficients": one}]},
        {"state_id": 5, "transitions": [{"target_class": 2, "coefficients": one}]},
    ]
    expected = {
        "closed": False,
        "classes_checked": 3,
        "member_comparisons": 3,
        "witness": {
            "class_id": 0,
            "left_state": 0,
            "right_state": 4,
            "target_class": 0,
            "left_coefficients": xy,
            "right_coefficients": zero(),
            "first_distinguishing_rates": ["1/3", "1/3"],
        },
    }
    return part, rows, expected


def test_synthetic_failure_branch_preserves_first_class_member_target_and_full_scan(
    executors, aggregate
):
    part, rows, expected = synthetic_failure()
    before = wire([part, rows])
    for module in executors:
        result, quotient, semigroup = module._closure(part, rows)
        assert wire(result) == wire(expected)
        assert quotient == [] and semigroup is None
    runner, _ = aggregate
    assert wire(runner.closure_from_rows(rows, part)) == wire(expected)
    assert wire([part, rows]) == before
    # Class1 has its own failure and its first unequal member precedes class0's
    # unequal member in state order. The certificate still uses class order.
    assert first_difference(rows[1]["transitions"], rows[2]["transitions"]) is not None
    assert expected["witness"]["right_state"] == 4
    assert expected["witness"]["right_state"] > rows[2]["state_id"]


def test_selected_half_rate_and_corners_cannot_substitute_for_polynomial_closure(
    executors, aggregate
):
    x, smooth, one = zero(), zero(), zero()
    x[1][0], smooth[2][0], smooth[3][0], one[0][0] = 1, 3, -2, 1

    def row(sid, table):
        complement = [[one[i][j] - table[i][j] for j in range(4)] for i in range(4)]
        return {
            "state_id": sid,
            "transitions": [
                {"target_class": 0, "coefficients": table},
                {"target_class": 1, "coefficients": complement},
            ],
        }

    rows = [
        row(0, x),
        row(1, smooth),
        {"state_id": 2, "transitions": [{"target_class": 1, "coefficients": one}]},
    ]
    part = {
        "state_classes": [0, 0, 1],
        "classes": [
            {"class_id": 0, "key": [0], "members": [0, 1]},
            {"class_id": 1, "key": [1], "members": [2]},
        ],
    }
    assert all(
        evaluate(x, rate, F(0)) == evaluate(smooth, rate, F(0)) for rate in (F(0), F(1, 2), F(1))
    )
    assert evaluate(x, F(1, 3), F(0)) == F(1, 3) != F(7, 27) == evaluate(smooth, F(1, 3), F(0))
    expected = {
        "closed": False,
        "classes_checked": 2,
        "member_comparisons": 1,
        "witness": {
            "class_id": 0,
            "left_state": 0,
            "right_state": 1,
            "target_class": 0,
            "left_coefficients": x,
            "right_coefficients": smooth,
            "first_distinguishing_rates": ["1/3", "0"],
        },
    }
    for module in executors:
        result, quotient, semigroup = module._closure(part, rows)
        assert wire(result) == wire(expected)
        assert quotient == [] and semigroup is None
    assert aggregate[0].closure_from_rows(rows, part) == expected


def test_stable_synthetic_input_is_closed_without_merging_its_given_classes(executors):
    part, rows, _ = synthetic_failure()
    one = zero()
    one[0][0] = 1
    rows = [
        {"state_id": row["state_id"], "transitions": [{"target_class": 2, "coefficients": one}]}
        for row in rows
    ]
    expected_quotient = [
        {
            "class_id": group["class_id"],
            "representative_state": group["members"][0],
            "transitions": rows[group["members"][0]]["transitions"],
        }
        for group in part["classes"]
    ]
    for module in executors:
        result, quotient, semigroup = module._closure(part, rows)
        assert result == {
            "closed": True,
            "classes_checked": 3,
            "member_comparisons": 3,
            "witness": None,
        }
        assert quotient == expected_quotient
        assert semigroup == composition(expected_quotient)


class StringSubclass(str):
    pass


class DictSubclass(dict):
    pass


class ListSubclass(list):
    pass


def invalid_problem(case):
    p = problem()
    if case == "extra":
        p["closed"] = True
    elif case == "precomputed-domain":
        p["domain"] = {"states": []}
    elif case == "missing-schema":
        del p["schema_version"]
    elif case == "missing-family":
        del p["family"]
    elif case == "schema-value":
        p["schema_version"] = "det8-qr05p-problem-v1"
    elif case == "family-value":
        p["family"] = "qr05p_summary_contract"
    elif case == "schema-bool":
        p["schema_version"] = True
    elif case == "family-float":
        p["family"] = 1.0
    elif case == "family-null":
        p["family"] = None
    elif case == "family-subclass":
        p["family"] = StringSubclass(p["family"])
    elif case == "schema-subclass":
        p["schema_version"] = StringSubclass(p["schema_version"])
    elif case == "dict-subclass":
        return DictSubclass(p)
    elif case == "key-subclass":
        p[StringSubclass("family")] = p.pop("family")
    elif case == "key-nonstr":
        p[False] = p.pop("family")
    elif case == "list":
        return [p]
    elif case == "list-subclass":
        return ListSubclass([p])
    elif case == "tuple":
        return (p,)
    elif case == "null":
        return None
    elif case == "string":
        return "problem"
    else:
        raise AssertionError(case)
    return p


INVALID = (
    "extra",
    "precomputed-domain",
    "missing-schema",
    "missing-family",
    "schema-value",
    "family-value",
    "schema-bool",
    "family-float",
    "family-null",
    "family-subclass",
    "schema-subclass",
    "dict-subclass",
    "key-subclass",
    "key-nonstr",
    "list",
    "list-subclass",
    "tuple",
    "null",
    "string",
)


@pytest.mark.parametrize("case", INVALID)
def test_analyze_rejects_every_native_schema_coercion_with_valueerror(executors, case):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problem(case))


def test_optimized_schema_guards_and_valid_failure_branch_do_not_depend_on_assert(tmp_path):
    code = r"""
import importlib.util,json,pathlib,sys
base=pathlib.Path(sys.argv[1]);part,rows,wanted=json.loads(sys.argv[2])
class S(str):pass
class D(dict):pass
for i,filename in enumerate(("portability.py","reference_qr05q.py")):
 name="_qr05q_optimized_"+str(i);spec=importlib.util.spec_from_file_location(name,base/filename)
 module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
 valid={"schema_version":"det8-qr05q-problem-v1","family":"qr05q_three_layer"}
 badkey=dict(valid);badkey[S("family")]=badkey.pop("family")
 for bad in (None,[],(),D(valid),badkey,{**valid,"closed":True},{**valid,"family":S(valid["family"])},{**valid,"schema_version":True}):
  try:module.analyze(bad)
  except ValueError:pass
  else:raise RuntimeError("optimized native guard did not reject")
 result,quotient,semigroup=module._closure(part,rows)
 if result!=wanted or quotient!=[] or semigroup is not None:raise RuntimeError("optimized failure branch changed")
 if module.path_supports([0,1,3,5,7],[[],[0],[0,1],[0,1,2],[0,1,2,3]],[1,2,3,4,5,6])!=[]:raise RuntimeError("odd chain became a colored motif")
print("optimized strict guards and honest failure branch passed")
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
            json.dumps(synthetic_failure()),
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "optimized strict guards and honest failure branch passed"


def test_whole_aggregate_wire_and_exact_audit_bridge_contract(
    aggregate, analyses, independent, old_restriction
):
    runner, suite = aggregate
    a = analyses[0]
    assert wire(json.loads(wire(suite))) == wire(suite)
    assert runner.canonical(suite) == wire(suite)
    assert set(suite) == {
        "problem",
        "analysis",
        "independent_route_equal",
        "independent_audit",
        "prior_bridge",
        "controls",
        "invalid_inputs_rejected",
        "totals",
    }
    assert suite["problem"] == problem()
    assert wire(suite["analysis"]) == wire(a)
    assert suite["independent_route_equal"] is True
    assert suite["independent_audit"] == {
        "domain_regenerated": True,
        "all_features_reconstructed": True,
        "all_fine_rows_reconstructed": True,
        "all_H_rows_and_fibers_checked": True,
        "exact_fine_rate_points": 22,
        "motif_support_heredity_checked": True,
        "analysis_sha256": digest(a),
    }
    old_aliases = sum(
        sid < 2470 for profile in a["domain"]["profiles"][1030:] for sid in profile["state_ids"]
    )
    assert suite["prior_bridge"] == {
        "O_prior": "qr-05o-path-observable-2026-09-06/results.json",
        "P_prior": "qr-05p-minimal-summary-2026-09-06/results.json",
        "source_alias_universe_regenerated": True,
        "executor_prior_input_dependency": False,
        "old_profiles": 1030,
        "old_aliases": 65888,
        "old_states": 2470,
        "old_H_classes": 167,
        "raw_prefix_equal": True,
        "features_equal": True,
        "actual_H_restriction_equal": True,
        "fine_kernel_sha256": old_restriction["fine_sha256"],
        "old_quotient_equal": True,
        "old_semigroup": old_restriction["semigroup"],
        "new_states": a["counts"]["states"] - 2470,
        "new_profile_aliases_on_old_states": old_aliases,
    }
    assert suite["controls"] == {
        "single_bit_sources": 16,
        "full_mask_chain_controls": 2,
        "deleted_middle_comparison_controls": 2,
        "same_color_chain_controls": 2,
        "no_skip_edge_controls": 2,
        "fixed_frame_only_source3": True,
        "all_structural_atoms_retained": True,
        "expanded_closure": a["closure"]["closed"],
    }
    assert suite["invalid_inputs_rejected"] == 2 * len(runner.invalid_fixtures())
    assert suite["totals"] == {
        **a["counts"],
        "H_closed": a["closure"]["closed"],
        "H_member_comparisons": a["closure"]["member_comparisons"],
        "fine_coefficient_cells": a["fine_kernel"]["coefficient_cells"],
        "fine_rate_evaluations": a["fine_kernel"]["evaluated_atoms"],
        "motif_expectation_cells": a["expected_updates"]["motif_cells"],
        "path_expectation_cells": a["expected_updates"]["path_cells"],
        "new_states": a["counts"]["states"] - 2470,
        "old_H_classes_preserved": 167,
    }
    assert len(runner.SOURCES) == 6 and len(runner.PRIORS) == 21
    assert wire(independent[0]) == wire(a)


def replaced(tree, path, value):
    """Copy only ancestors of one changed cell; do not mutate shared fixtures."""
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = replaced(tree[path[0]], path[1:], value)
    return answer


def changed_analysis(a, case):
    if case == "new-state-id-bool":
        return replaced(a, ["domain", "states", 2470, "frame_id"], False)
    if case == "new-kept-bool":
        return replaced(a, ["domain", "states", 2470, "kept", 0], False)
    if case == "new-past-bool":
        return replaced(a, ["domain", "states", 2470, "past", 1, 0], False)
    if case == "new-profile-index-bool":
        return replaced(a, ["domain", "profiles", 1030, "frame_id"], False)
    if case == "reverse-transpose":
        return replaced(
            a, ["domain", "profiles", 1288, "past"], a["domain"]["profiles"][1290]["past"]
        )
    if case == "missing-transitive-source-edge":
        before = a["domain"]["profiles"][1047]["past"][5]
        assert 1 in before
        return replaced(a, ["domain", "profiles", 1047, "past", 5], [v for v in before if v != 1])
    if case == "wrong-alias":
        return replaced(a, ["domain", "profiles", 1047, "state_ids", 17], 0)
    if case == "feature-count-bool":
        return replaced(a, ["features", 2470, "chain_counts", 0], True)
    if case == "B-coefficient":
        return replaced(a, ["features", 2470, "pair_graded", 0, 0, 0, 0], 2)
    if case == "false-path-count":
        return replaced(a, ["features", 2470, "path_count"], a["features"][2470]["path_count"] + 1)
    if case == "fine-digest":
        return replaced(a, ["fine_kernel", "sha256"], "0" * 64)
    if case == "fine-count":
        return replaced(
            a, ["fine_kernel", "transition_atoms"], a["fine_kernel"]["transition_atoms"] - 1
        )
    if case == "pushed-coefficient":
        return replaced(
            a,
            ["pushed_rows", 2470, "transitions", 0, "coefficients", 0, 0],
            a["pushed_rows"][2470]["transitions"][0]["coefficients"][0][0] + 1,
        )
    if case == "omit-selected-zero":
        sid, index = next(
            (row["state_id"], index)
            for row in a["pushed_rows"]
            for index, atom in enumerate(row["transitions"])
            if evaluate(atom["coefficients"], F(1), F(1)) == 0
        )
        atoms = a["pushed_rows"][sid]["transitions"]
        assert any(c for line in atoms[index]["coefficients"] for c in line)
        return replaced(a, ["pushed_rows", sid, "transitions"], atoms[:index] + atoms[index + 1 :])
    if case == "class-id-bool":
        return replaced(a, ["partition", "state_classes", 0], False)
    if case == "false-closure":
        return replaced(a, ["closure", "closed"], not a["closure"]["closed"])
    if case == "closed-int":
        return replaced(a, ["closure", "closed"], int(a["closure"]["closed"]))
    if case == "incomplete-scan":
        return replaced(
            a, ["closure", "member_comparisons"], a["closure"]["member_comparisons"] - 1
        )
    if case == "fake-witness":
        return replaced(a, ["closure", "witness"], synthetic_failure()[2]["witness"])
    if case == "wrong-quotient":
        quotient = a["quotient_rows"]
        return replaced(
            a,
            ["quotient_rows"],
            quotient[:-1]
            if quotient
            else [{"class_id": 0, "representative_state": 0, "transitions": []}],
        )
    if case == "false-semigroup":
        if a["semigroup"] is None:
            return replaced(a, ["semigroup"], {"verified": True, "rows": [], "totals": {}})
        return replaced(a, ["semigroup", "rows", 0, "max_abs_residual"], 1)
    if case == "wrong-update":
        return replaced(
            a, ["expected_updates", "path_cells"], a["expected_updates"]["path_cells"] - 16
        )
    if case == "tuple-wire":
        return replaced(
            a, ["domain", "states", 2470, "kept"], tuple(a["domain"]["states"][2470]["kept"])
        )
    if case == "overflow":
        return replaced(a, ["counts", "states"], 1 << 4096)
    raise AssertionError(case)


@pytest.mark.parametrize(
    "case",
    [
        "new-state-id-bool",
        "new-kept-bool",
        "new-past-bool",
        "new-profile-index-bool",
        "reverse-transpose",
        "missing-transitive-source-edge",
        "wrong-alias",
        "feature-count-bool",
        "B-coefficient",
        "false-path-count",
        "fine-digest",
        "fine-count",
        "pushed-coefficient",
        "omit-selected-zero",
        "class-id-bool",
        "false-closure",
        "closed-int",
        "incomplete-scan",
        "fake-witness",
        "wrong-quotient",
        "false-semigroup",
        "wrong-update",
        "tuple-wire",
        "overflow",
    ],
)
def test_independent_audit_rejects_changed_evidence_not_just_reported_counts(
    aggregate, analyses, case
):
    runner, _ = aggregate
    changed = changed_analysis(analyses[0], case)
    with pytest.raises(ValueError):
        runner.check_analysis(changed)


def test_same_size_wrong_fibers_do_not_hide_behind_equal_cardinality(aggregate, analyses):
    a = analyses[0]
    groups = [group for group in a["partition"]["classes"] if len(group["members"]) > 1]
    left, right = next(
        (x, y) for x, y in combinations(groups, 2) if len(x["members"]) == len(y["members"])
    )
    u, v = left["members"][-1], right["members"][-1]
    lm = sorted([sid for sid in left["members"] if sid != u] + [v])
    rm = sorted([sid for sid in right["members"] if sid != v] + [u])
    assert lm[0] == left["members"][0] and rm[0] == right["members"][0]
    changed = replaced(a, ["partition", "classes", left["class_id"], "members"], lm)
    changed = replaced(changed, ["partition", "classes", right["class_id"], "members"], rm)
    changed = replaced(changed, ["partition", "state_classes", u], right["class_id"])
    changed = replaced(changed, ["partition", "state_classes", v], left["class_id"])
    assert changed["counts"] == a["counts"]
    assert sorted(
        sid for group in changed["partition"]["classes"] for sid in group["members"]
    ) == list(range(a["counts"]["states"]))
    with pytest.raises(ValueError):
        aggregate[0].check_analysis(changed)


def test_audit_cached_bytes_are_immutable_and_working_cap_is_explicit(
    aggregate, analyses, monkeypatch
):
    runner, _ = aggregate
    detached = runner.expected_analysis()
    detached["features"][0]["chain_counts"][0] = True
    with pytest.raises(ValueError):
        runner.check_analysis(detached)
    assert runner.expected_analysis()["features"][0]["chain_counts"][0] is not True
    assert runner.check_analysis(analyses[0])["all_H_rows_and_fibers_checked"] is True
    with monkeypatch.context() as patch:
        patch.setattr(runner, "MAX_WORKING_BYTES", 32)
        with pytest.raises(ValueError):
            runner.check_analysis(analyses[0])


@pytest.mark.parametrize(
    "value",
    [(0,), {"nested": 1.0}, {False: 1}, {StringSubclass("key"): 0}, {"nested": ListSubclass([1])}],
)
def test_runner_rejects_non_native_wire(aggregate, value):
    with pytest.raises(ValueError):
        aggregate[0].require_wire(value)


@pytest.mark.parametrize("left,right", [({"a": [True]}, {"a": [1]}), ({"a": [False]}, {"a": [0]})])
def test_runner_equality_is_canonical_not_bool_int_coercing(aggregate, left, right):
    assert left == right
    with pytest.raises(ValueError):
        aggregate[0].require_same_wire(left, right, "typed wire regression")
