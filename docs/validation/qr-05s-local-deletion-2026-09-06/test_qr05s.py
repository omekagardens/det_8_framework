"""Independent S one-deletion counts, recurrence and ordered-word tests.

Only pinned R JSON supplies the declared raw observation model; no previous
executor is imported. Elementary helpers are carried from our test lineage.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from functools import cache
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
R_SHA = "cfec27d60d605ec142af96f8931e0e90b3c5ca92c72389ce8e0d84ef8b444001"


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
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


@pytest.fixture(scope="session")
def pinned_r():
    path = HERE.parent / "qr-05r-deletion-profile-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 12028200 and hashlib.sha256(raw).hexdigest() == R_SHA
    envelope = json.loads(raw)
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


@pytest.fixture(scope="session")
def problem(pinned_r):
    return {
        "schema_version": "det8-qr05s-problem-v1",
        "family": "qr05s_local_deletion",
        "model": copy.deepcopy(pinned_r["problem"]["model"]),
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05s_test_direct", "local_deletion.py"),
        private_module("_qr05s_test_reference", "reference_qr05s.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors, problem):
    return tuple(module.analyze(problem) for module in executors)


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05s_test_aggregate", "study.py")
    return runner, runner.run_suite()


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def induced_key(state, kept):
    relation = relation_of(state)
    past = [[i for i, u in enumerate(kept) if (u, v) in relation] for v in kept]
    return state_key(state["frame_id"], kept, past)


def local_payload(classes):
    return {
        "schema_version": "det8-qr05s-local-v1",
        "classes": [
            {
                key: copy.deepcopy(row[key])
                for key in ("class_id", "frame_id", "parent_color_sizes", "odd", "even")
            }
            for row in classes
        ],
    }


def word(rows, sid, colors):
    values = {sid: 1}
    for color in colors:
        updated = {}
        for current, count in values.items():
            for atom in rows[current][color]:
                target = atom["target_class"]
                updated[target] = updated.get(target, 0) + count * atom["multiplicity"]
        values = updated
    return values


def certificates(rows, profiles):
    count = len(rows)
    maps = [
        {atom["target_class"]: atom["multiplicity"] for atom in row["transitions"]}
        for row in profiles
    ]
    base, recurrence, reports = 0, 0, []
    for source, parent in enumerate(rows):
        odd, even = parent["parent_color_sizes"]
        for target, final in enumerate(rows):
            m, n = final["parent_color_sizes"]
            value = maps[source].get(target, 0)
            if parent["frame_id"] != final["frame_id"] or m > odd or n > even:
                assert value == 0
                continue
            if (m, n) == (odd, even):
                base += 1
                assert value == int(source == target)
            for color, denominator in (("odd", odd - m), ("even", even - n)):
                if denominator > 0:
                    recurrence += 1
                    numerator = sum(
                        atom["multiplicity"] * maps[atom["target_class"]].get(target, 0)
                        for atom in parent[color]
                    )
                    assert numerator == denominator * value
                    assert numerator % denominator == 0
        rank_totals = zero()
        for atom in profiles[source]["transitions"]:
            m, n = atom["retained_color_sizes"]
            assert rows[atom["target_class"]]["parent_color_sizes"] == [m, n]
            rank_totals[m][n] += atom["multiplicity"]
        assert rank_totals == [
            [choose(odd, m) * choose(even, n) for n in range(4)] for m in range(4)
        ]
        oo, ee = word(rows, source, ["odd", "odd"]), word(rows, source, ["even", "even"])
        oe, eo = word(rows, source, ["odd", "even"]), word(rows, source, ["even", "odd"])

        def filtered(rank, factor, source=source):
            return {
                atom["target_class"]: factor * atom["multiplicity"]
                for atom in profiles[source]["transitions"]
                if atom["retained_color_sizes"] == list(rank)
            }

        assert oo == filtered((odd - 2, even), 2)
        assert ee == filtered((odd, even - 2), 2)
        assert oe == eo == filtered((odd - 1, even - 1), 1)
        assert sum(oo.values()) == odd * (odd - 1)
        assert sum(ee.values()) == even * (even - 1)
        assert sum(oe.values()) == odd * even
        reports.append(
            {
                "class_id": source,
                "odd_odd_targets": len(oo),
                "even_even_targets": len(ee),
                "mixed_targets": len(oe),
                "coefficient_cells": len(oo) + len(ee) + 2 * len(oe),
                "odd_odd_pairs": sum(oo.values()),
                "even_even_pairs": sum(ee.values()),
                "mixed_pairs": sum(oe.values()),
                "max_abs_residual": 0,
            }
        )
    return (
        {
            "target_cells": count * count,
            "base_cells": base,
            "recurrence_cells": recurrence,
            "normalization_cells": 16 * count,
            "max_abs_residual": 0,
        },
        {
            "verified": True,
            "rows": reports,
            "totals": {
                key: sum(row[key] for row in reports)
                for key in (
                    "odd_odd_targets",
                    "even_even_targets",
                    "mixed_targets",
                    "coefficient_cells",
                    "odd_odd_pairs",
                    "even_even_pairs",
                    "mixed_pairs",
                    "max_abs_residual",
                )
            },
        },
    )


@pytest.fixture(scope="session")
def independent(problem):
    model = problem["model"]
    frames, states = model["frames"], model["states"]
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
    registry = {state_key(s["frame_id"], s["kept"], s["past"]): s["state_id"] for s in states}
    local, fine, profiles = [], [], []
    choices = 0
    for state, feature in zip(states, fs, strict=True):
        frame = frames[state["frame_id"]]
        eligible = sorted(set(state["kept"]) & set(frame["eligible"]))
        counts = {"odd": {}, "even": {}}
        for v in eligible:
            target = registry[induced_key(state, [u for u in state["kept"] if u != v])]
            cid, color = part["state_classes"][target], "odd" if v % 2 else "even"
            counts[color][cid] = counts[color].get(cid, 0) + 1
            choices += 1
        local.append(
            {
                "state_id": state["state_id"],
                "frame_id": state["frame_id"],
                "parent_color_sizes": feature["color_sizes"],
                **{
                    color: [
                        {"target_class": cid, "multiplicity": value}
                        for cid, value in sorted(counts[color].items())
                    ]
                    for color in ("odd", "even")
                },
            }
        )
        atoms, census = [], {}
        for mask in range(1 << len(eligible)):
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(eligible) if mask & (1 << bit)]
            )
            target = registry[induced_key(state, kept)]
            atoms.append(
                {
                    "target_state": target,
                    "coefficients": kernel(*feature["color_sizes"], *fs[target]["color_sizes"]),
                }
            )
            cid = part["state_classes"][target]
            census[cid] = census.get(cid, 0) + 1
        fine.append(
            {
                "state_id": state["state_id"],
                "transitions": sorted(atoms, key=lambda atom: atom["target_state"]),
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
                        "multiplicity": value,
                    }
                    for cid, value in sorted(census.items())
                ],
            }
        )
    witness, comparisons, full_closed = None, 0, True
    for group in part["classes"]:
        left = group["members"][0]
        for right in group["members"][1:]:
            comparisons += 1
            full_closed &= profiles[left]["transitions"] == profiles[right]["transitions"]
            for color in ("odd", "even"):
                lhs = {atom["target_class"]: atom["multiplicity"] for atom in local[left][color]}
                rhs = {atom["target_class"]: atom["multiplicity"] for atom in local[right][color]}
                differing = [
                    target
                    for target in sorted(lhs.keys() | rhs.keys())
                    if lhs.get(target, 0) != rhs.get(target, 0)
                ]
                if differing and witness is None:
                    target = differing[0]
                    witness = {
                        "class_id": group["class_id"],
                        "left_state": left,
                        "right_state": right,
                        "color": color,
                        "target_class": target,
                        "left_multiplicity": lhs.get(target, 0),
                        "right_multiplicity": rhs.get(target, 0),
                    }
    assert (witness is None) == full_closed
    local_classes = (
        []
        if witness
        else [
            {
                "class_id": group["class_id"],
                "representative_state": group["members"][0],
                **{
                    key: local[group["members"][0]][key]
                    for key in ("frame_id", "parent_color_sizes", "odd", "even")
                },
            }
            for group in part["classes"]
        ]
    )
    cp = (
        []
        if witness
        else [
            {
                "class_id": group["class_id"],
                "representative_state": group["members"][0],
                **{
                    key: profiles[group["members"][0]][key]
                    for key in ("parent_color_sizes", "transitions")
                },
            }
            for group in part["classes"]
        ]
    )
    reconstruction = None
    if cp:
        certificate, operators = certificates(local_classes, cp)
        reconstruction = {
            "class_profiles": cp,
            "certificate": certificate,
            "operator_checks": operators,
        }
    power_rows = pushed(fine, part["state_classes"])
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
    direct_atoms = sum(len(row["transitions"]) for row in profiles)
    a = {
        "model_sha256": digest(model),
        "features": fs,
        "partition": part,
        "local_rows": local,
        "local_closure": {
            "closed": witness is None,
            "classes_checked": len(part["classes"]),
            "member_comparisons": comparisons,
            "witness": witness,
        },
        "local_classes": local_classes,
        "reconstruction": reconstruction,
        "comparison": {
            "direct_profiles_sha256": digest(profiles),
            "reconstructed_profiles_sha256": digest(profiles) if cp else None,
            "full_profile_closed": full_closed,
            "local_full_equivalent": True,
            "fine_kernel_sha256": digest(fine),
            "pushed_rows_sha256": digest(power_rows),
            "quotient_rows_sha256": digest(quotient) if cp else None,
            "profile_cells": 16 * direct_atoms if cp else 0,
            "power_cells": 16 * direct_atoms,
            "max_abs_residual": 0,
        },
        "counts": {
            "states": len(states),
            "classes": len(part["classes"]),
            "fine_atoms": sum(len(row["transitions"]) for row in fine),
            "fine_local_choices": choices,
            "local_atoms": sum(len(row[color]) for row in local for color in ("odd", "even")),
            "class_local_atoms": sum(
                len(row[color]) for row in local_classes for color in ("odd", "even")
            ),
            "direct_profile_atoms": direct_atoms,
            "class_profile_atoms": sum(len(row["transitions"]) for row in cp),
        },
    }
    return a, fine, profiles, power_rows, quotient


def test_complete_independent_raw_features_local_rows_and_profiles(
    analyses, independent, problem, pinned_r
):
    expected, fine, profiles, powers, quotient = independent
    assert wire(analyses[0]) == wire(analyses[1]) == wire(expected)
    assert wire(json.loads(wire(analyses[0]))) == wire(analyses[0])
    assert len(wire(analyses[0])) < 64 * 1024 * 1024
    assert set(analyses[0]) == {
        "model_sha256",
        "features",
        "partition",
        "local_rows",
        "local_closure",
        "local_classes",
        "reconstruction",
        "comparison",
        "counts",
    }
    assert wire(problem["model"]) == wire(pinned_r["problem"]["model"])
    r = pinned_r["analysis"]
    assert wire(expected["features"]) == wire(r["features"])
    assert wire(expected["partition"]) == wire(r["partition"])
    assert wire(profiles) == wire(r["profiles"])
    assert wire(expected["reconstruction"]["class_profiles"]) == wire(r["class_profiles"])
    assert digest(fine) == r["conversion"]["fine_kernel_sha256"]
    assert digest(powers) == r["conversion"]["pushed_rows_sha256"]
    assert digest(quotient) == r["conversion"]["quotient_rows_sha256"]


def test_single_deletions_preserve_colors_frame_multiplicity_and_full_induced_order(
    independent, problem
):
    a = independent[0]
    choices = 0
    assert set(problem["model"]) == {"frames", "states"}
    assert any(
        any(index > row for row, before in enumerate(s["past"]) for index in before)
        for s in problem["model"]["states"]
    )
    twin_rows = 0
    for state, feature, row in zip(
        problem["model"]["states"], a["features"], a["local_rows"], strict=True
    ):
        assert row["parent_color_sizes"] == [
            feature["pair_graded"][0][1][1][0],
            feature["pair_graded"][0][1][0][1],
        ]
        assert feature["mean_graded"][1][0][0] == int(state["frame_id"] == 1)
        for k, color in enumerate(("odd", "even")):
            assert sum(atom["multiplicity"] for atom in row[color]) == row["parent_color_sizes"][k]
            assert len(row[color]) <= 3
            if row["parent_color_sizes"][k] == 0:
                assert row[color] == []
            for atom in row[color]:
                rep = a["partition"]["classes"][atom["target_class"]]["members"][0]
                child = a["local_rows"][rep]
                desired = row["parent_color_sizes"][:]
                desired[k] -= 1
                assert (
                    child["frame_id"] == row["frame_id"] and child["parent_color_sizes"] == desired
                )
                assert 1 <= atom["multiplicity"] <= 3
                twin_rows += atom["multiplicity"] > 1
            choices += sum(atom["multiplicity"] for atom in row[color])
    assert choices == a["counts"]["fine_local_choices"] <= 26682
    assert twin_rows > 0 and a["counts"]["local_atoms"] < choices
    assert (
        a["counts"]["states"] == 4447
        and a["counts"]["fine_atoms"] == 168388
        and a["counts"]["classes"] <= 512
    )


def test_local_rows_are_exact_one_deletion_slices_of_independent_full_profiles(independent):
    a, _, profiles, _, _ = independent
    for local, profile in zip(a["local_rows"], profiles, strict=True):
        for index, color in enumerate(("odd", "even")):
            desired = local["parent_color_sizes"][:]
            desired[index] -= 1
            expected = [
                {"target_class": atom["target_class"], "multiplicity": atom["multiplicity"]}
                for atom in profile["transitions"]
                if atom["retained_color_sizes"] == desired
            ]
            assert local[color] == expected


def test_all_local_fibers_are_checked_and_no_reconstruction_is_substituted(independent):
    a = independent[0]
    classes = a["partition"]["classes"]
    assert a["local_closure"]["classes_checked"] == len(classes)
    assert a["local_closure"]["member_comparisons"] == a["counts"]["states"] - len(classes)
    for group in classes:
        rep = group["members"][0]
        for sid in group["members"]:
            assert a["local_rows"][sid]["frame_id"] == a["local_rows"][rep]["frame_id"]
            assert (
                a["local_rows"][sid]["parent_color_sizes"]
                == a["local_rows"][rep]["parent_color_sizes"]
            )
            if a["local_closure"]["closed"]:
                assert all(
                    a["local_rows"][sid][color] == a["local_rows"][rep][color]
                    for color in ("odd", "even")
                )
    assert a["local_closure"]["closed"] is a["comparison"]["full_profile_closed"]
    if not a["local_closure"]["closed"]:
        assert a["local_classes"] == [] and a["reconstruction"] is None
        assert (
            a["comparison"]["reconstructed_profiles_sha256"] is None
            and a["comparison"]["quotient_rows_sha256"] is None
        )


def test_public_local_only_constructor_matches_raw_subset_census(executors, independent):
    a = independent[0]
    local = json.loads(wire(local_payload(a["local_classes"])))
    assert set(local) == {"schema_version", "classes"}
    assert all(
        set(row) == {"class_id", "frame_id", "parent_color_sizes", "odd", "even"}
        for row in local["classes"]
    )
    expected = {
        "profiles": [
            {
                key: copy.deepcopy(row[key])
                for key in ("class_id", "parent_color_sizes", "transitions")
            }
            for row in a["reconstruction"]["class_profiles"]
        ],
        "certificate": a["reconstruction"]["certificate"],
        "operator_checks": a["reconstruction"]["operator_checks"],
    }
    before = wire(local)
    for module in executors:
        assert wire(module.reconstruct_profiles(local)) == wire(expected)
    assert wire(local) == before


def lattice(reverse=False):
    labels = list(product(range(2), range(4), range(3)))
    if reverse:
        labels.reverse()
    ids = {label: cid for cid, label in enumerate(labels)}
    rows = []
    for cid, (frame, odd, even) in enumerate(labels):
        rows.append(
            {
                "class_id": cid,
                "frame_id": frame,
                "parent_color_sizes": [odd, even],
                "odd": [{"target_class": ids[frame, odd - 1, even], "multiplicity": odd}]
                if odd
                else [],
                "even": [{"target_class": ids[frame, odd, even - 1], "multiplicity": even}]
                if even
                else [],
            }
        )
    return {"schema_version": "det8-qr05s-local-v1", "classes": rows}


def lattice_profiles(local):
    rows = local["classes"]
    return [
        {
            "class_id": source["class_id"],
            "parent_color_sizes": source["parent_color_sizes"],
            "transitions": [
                {
                    "target_class": target["class_id"],
                    "retained_color_sizes": target["parent_color_sizes"],
                    "multiplicity": comb(
                        source["parent_color_sizes"][0], target["parent_color_sizes"][0]
                    )
                    * comb(source["parent_color_sizes"][1], target["parent_color_sizes"][1]),
                }
                for target in rows
                if target["frame_id"] == source["frame_id"]
                and all(
                    b <= a
                    for a, b in zip(
                        source["parent_color_sizes"], target["parent_color_sizes"], strict=True
                    )
                )
            ],
        }
        for source in rows
    ]


def profiles_from_words(rows):
    result = []
    for sid, row in enumerate(rows):
        counts = {}
        odd, even = row["parent_color_sizes"]
        for a, b in product(range(odd + 1), range(even + 1)):
            paths = word(rows, sid, ["odd"] * a + ["even"] * b)
            divisor = factorial(a) * factorial(b)
            for target, numerator in paths.items():
                assert numerator % divisor == 0
                assert target not in counts
                assert rows[target]["parent_color_sizes"] == [odd - a, even - b]
                counts[target] = numerator // divisor
        result.append(
            {
                "class_id": sid,
                "parent_color_sizes": row["parent_color_sizes"],
                "transitions": [
                    {
                        "target_class": target,
                        "retained_color_sizes": rows[target]["parent_color_sizes"],
                        "multiplicity": m,
                    }
                    for target, m in sorted(counts.items())
                ],
            }
        )
    return result


@pytest.mark.parametrize("reverse", [False, True])
def test_public_constructor_analytic_rank_lattice_handles_arbitrary_id_topology(executors, reverse):
    model = lattice(reverse)
    profiles = lattice_profiles(model)
    assert profiles_from_words(model["classes"]) == profiles
    cert, operators = certificates(model["classes"], profiles)
    expected = {"profiles": profiles, "certificate": cert, "operator_checks": operators}
    before = wire(model)
    for module in executors:
        result = module.reconstruct_profiles(model)
        assert wire(result) == wire(expected)
    assert wire(model) == before
    if reverse:
        assert all(
            atom["target_class"] > row["class_id"]
            for row in model["classes"]
            for color in ("odd", "even")
            for atom in row[color]
        )
    assert cert["target_cells"] == 24**2 and cert["base_cells"] == 24
    assert cert["normalization_cells"] == 16 * 24


def test_every_ordered_word_has_correct_factorials_and_impossible_words_are_zero(independent):
    rows = independent[0]["local_classes"]
    profiles = independent[0]["reconstruction"]["class_profiles"]
    for sid, row in enumerate(rows):
        odd, even = row["parent_color_sizes"]
        assert word(rows, sid, []) == {sid: 1}
        assert word(rows, sid, ["odd"] * (odd + 1)) == {}
        assert word(rows, sid, ["even"] * (even + 1)) == {}
        for a, b in product(range(odd + 1), range(even + 1)):
            expected = {
                atom["target_class"]: atom["multiplicity"] * factorial(a) * factorial(b)
                for atom in profiles[sid]["transitions"]
                if atom["retained_color_sizes"] == [odd - a, even - b]
            }
            assert word(rows, sid, ["odd"] * a + ["even"] * b) == expected
            assert word(rows, sid, ["even"] * b + ["odd"] * a) == expected


def test_exact_divisor_is_number_removed_not_total_parent_count():
    rows = lattice()["classes"]
    profiles = lattice_profiles({"classes": rows})
    source = next(
        row["class_id"]
        for row in rows
        if row["frame_id"] == 0 and row["parent_color_sizes"] == [3, 1]
    )
    target = next(
        row["class_id"]
        for row in rows
        if row["frame_id"] == 0 and row["parent_color_sizes"] == [1, 0]
    )
    values = [
        {atom["target_class"]: atom["multiplicity"] for atom in row["transitions"]}
        for row in profiles
    ]
    odd_num = sum(
        atom["multiplicity"] * values[atom["target_class"]].get(target, 0)
        for atom in rows[source]["odd"]
    )
    even_num = sum(
        atom["multiplicity"] * values[atom["target_class"]].get(target, 0)
        for atom in rows[source]["even"]
    )
    assert odd_num == 6 and even_num == 3 and values[source][target] == 3
    assert odd_num // (3 - 1) == even_num // (1 - 0) == 3
    assert odd_num // 3 != values[source][target]


def test_twins_and_mixed_word_orders_have_distinct_multiplicity_factors():
    rows = lattice()["classes"]
    source = next(
        row["class_id"]
        for row in rows
        if row["frame_id"] == 0 and row["parent_color_sizes"] == [2, 1]
    )
    assert len(rows[source]["odd"]) == 1 and rows[source]["odd"][0]["multiplicity"] == 2
    oo = word(rows, source, ["odd", "odd"])
    oe, eo = word(rows, source, ["odd", "even"]), word(rows, source, ["even", "odd"])
    assert len(oo) == 1 and sum(oo.values()) == 2
    assert oe == eo and sum(oe.values()) == 2
    assert sum(oe.values()) + sum(eo.values()) == 4
    # Fixed-color order already counts each mixed subset; adding both orders
    # introduces another factor2, unlike a single same-color two-step word.
    assert sum(oo.values()) // factorial(2) == 1


def empty_model(count=2, shared=False):
    empty = []
    return {
        "schema_version": "det8-qr05s-local-v1",
        "classes": [
            {
                "class_id": cid,
                "frame_id": 0,
                "parent_color_sizes": [0, 0],
                "odd": empty if shared else [],
                "even": empty if shared else [],
            }
            for cid in range(count)
        ],
    }


def test_full_rank_delta_includes_distinct_equal_rank_labels_and_no_authentication(executors):
    local = empty_model(2, shared=True)
    for module in executors:
        result = module.reconstruct_profiles(local)
        assert result["profiles"] == [
            {
                "class_id": cid,
                "parent_color_sizes": [0, 0],
                "transitions": [
                    {"target_class": cid, "retained_color_sizes": [0, 0], "multiplicity": 1}
                ],
            }
            for cid in range(2)
        ]
        assert result["certificate"] == {
            "target_cells": 4,
            "base_cells": 4,
            "recurrence_cells": 0,
            "normalization_cells": 32,
            "max_abs_residual": 0,
        }
        assert result["operator_checks"]["totals"]["coefficient_cells"] == 0
    # Distinct same-frame empty labels are structurally/algebraically accepted;
    # this constructor does not authenticate them as actual H observations.
    assert local["classes"][0]["odd"] is local["classes"][1]["even"]


def fractional_model():
    targets = [[(1, 1), (2, 2)], [(3, 1), (4, 1)], [(4, 2)], [(5, 1)], [(5, 1)], []]
    ranks = [3, 2, 2, 1, 1, 0]
    return {
        "schema_version": "det8-qr05s-local-v1",
        "classes": [
            {
                "class_id": cid,
                "frame_id": 0,
                "parent_color_sizes": [rank, 0],
                "odd": [{"target_class": target, "multiplicity": m} for target, m in targets[cid]],
                "even": [],
            }
            for cid, rank in enumerate(ranks)
        ],
    }


def mixed_model():
    ranks = [[1, 1], [0, 1], [1, 0], [0, 0], [0, 0]]
    odd, even = [[(1, 1)], [], [(4, 1)], [], []], [[(2, 1)], [(3, 1)], [], [], []]
    return {
        "schema_version": "det8-qr05s-local-v1",
        "classes": [
            {
                "class_id": cid,
                "frame_id": 0,
                "parent_color_sizes": rank,
                "odd": [{"target_class": target, "multiplicity": m} for target, m in odd[cid]],
                "even": [{"target_class": target, "multiplicity": m} for target, m in even[cid]],
            }
            for cid, rank in enumerate(ranks)
        ],
    }


@pytest.mark.parametrize("kind", ["fractional", "mixed"])
def test_valid_local_totals_do_not_hide_fractional_reconstruction_or_mixed_failure(executors, kind):
    model = fractional_model() if kind == "fractional" else mixed_model()
    rows = model["classes"]
    for row in rows:
        for i, color in enumerate(("odd", "even")):
            assert sum(atom["multiplicity"] for atom in row[color]) == row["parent_color_sizes"][i]
            for atom in row[color]:
                target_rank = row["parent_color_sizes"][:]
                target_rank[i] -= 1
                assert rows[atom["target_class"]]["parent_color_sizes"] == target_rank
    if kind == "fractional":
        assert word(rows, 0, ["odd", "odd"])[3] == 1
        assert word(rows, 0, ["odd", "odd"])[3] % factorial(2) != 0
        assert all(
            word(rows, sid, ["odd", "even"]) == word(rows, sid, ["even", "odd"]) == {}
            for sid in range(len(rows))
        )
    else:
        assert word(rows, 0, ["odd", "even"]) == {3: 1}
        assert word(rows, 0, ["even", "odd"]) == {4: 1}
    for module in executors:
        with pytest.raises(ValueError):
            module.reconstruct_profiles(model)


def synthetic_local(mode="both"):
    vector = [0, 0, 1, 2, 3, 4, 5, 2]
    groups = [
        {
            "class_id": cid,
            "key": [cid],
            "members": [sid for sid, value in enumerate(vector) if value == cid],
        }
        for cid in range(6)
    ]
    ranks = [[1, 1], [1, 1], [0, 0], [0, 1], [0, 1], [1, 0], [1, 0], [0, 1]]

    def atoms(target):
        return [{"target_class": target, "multiplicity": 1}]

    rows = [
        {"state_id": sid, "frame_id": 0, "parent_color_sizes": rank, "odd": [], "even": []}
        for sid, rank in enumerate(ranks)
    ]
    rows[0].update(odd=atoms(2), even=atoms(4))
    rows[1].update(
        odd=atoms(3) if mode == "both" else atoms(2), even=atoms(4) if mode == "none" else atoms(5)
    )
    for sid in (3, 4, 7):
        rows[sid]["even"] = atoms(1)
    for sid in (5, 6):
        rows[sid]["odd"] = atoms(1)
    witness = (
        None
        if mode == "none"
        else {
            "class_id": 0,
            "left_state": 0,
            "right_state": 1,
            "color": "odd" if mode == "both" else "even",
            "target_class": 2 if mode == "both" else 4,
            "left_multiplicity": 1,
            "right_multiplicity": 0,
        }
    )
    return (
        {"state_classes": vector, "classes": groups},
        rows,
        {
            "closed": mode == "none",
            "classes_checked": 6,
            "member_comparisons": 2,
            "witness": witness,
        },
    )


@pytest.mark.parametrize("mode", ["both", "even", "none"])
def test_production_local_closure_scans_after_failure_and_uses_odd_before_even(executors, mode):
    part, rows, wanted = synthetic_local(mode)
    before = wire([part, rows])
    for module in executors:
        assert module.closure_from_local(rows, part) == wanted
        closure, classes, reconstruction = module._closure(part, rows)
        assert closure == wanted
        if mode != "none":
            assert classes == [] and reconstruction is None
        else:
            wanted_classes = [
                {
                    "class_id": g["class_id"],
                    "representative_state": g["members"][0],
                    **{
                        key: rows[g["members"][0]][key]
                        for key in ("frame_id", "parent_color_sizes", "odd", "even")
                    },
                }
                for g in part["classes"]
            ]
            assert classes == wanted_classes
            profiles = profiles_from_words(classes)
            cert, ops = certificates(classes, profiles)
            expected_profiles = [
                {"representative_state": classes[row["class_id"]]["representative_state"], **row}
                for row in profiles
            ]
            assert reconstruction == {
                "class_profiles": expected_profiles,
                "certificate": cert,
                "operator_checks": ops,
            }
    assert wire([part, rows]) == before


class NativeIntSubclass(int):
    pass


class NativeStrSubclass(str):
    pass


class NativeListSubclass(list):
    pass


class NativeDictSubclass(dict):
    pass


def micro_problem():
    return {
        "schema_version": "det8-qr05s-problem-v1",
        "family": "qr05s_local_deletion",
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
def micro_analysis(executors):
    value = micro_problem()
    first, second = (module.analyze(value) for module in executors)
    assert wire(first) == wire(second)
    return first


def test_minimum_raw_model_is_subset_closed_with_fixed_only_zero_deletions(micro_analysis):
    a = micro_analysis
    assert a["counts"] == {
        "states": 2,
        "classes": 2,
        "fine_atoms": 2,
        "fine_local_choices": 0,
        "local_atoms": 0,
        "class_local_atoms": 0,
        "direct_profile_atoms": 2,
        "class_profile_atoms": 2,
    }
    assert a["local_closure"] == {
        "closed": True,
        "classes_checked": 2,
        "member_comparisons": 0,
        "witness": None,
    }
    for index, feature in enumerate(a["features"]):
        assert feature["color_sizes"] == [0, 0]
        assert feature["chain_counts"] == [1, index, 0, 0]
    assert a["reconstruction"]["certificate"] == {
        "target_cells": 4,
        "base_cells": 2,
        "recurrence_cells": 0,
        "normalization_cells": 32,
        "max_abs_residual": 0,
    }


RAW_BAD_PATHS = [
    (("schema_version",), "det8-qr05r-problem-v1"),
    (("family",), "qr05r_deletion_profile"),
    (("extra",), 0),
    (("model", "extra"), []),
    (("model", "frames", 0, "density"), "12/1"),
    (("model", "frames", 0, "frame_id"), False),
    (("model", "frames", 0, "fixed"), [0, 3, 7]),
    (("model", "frames", 1, "eligible"), [1, 2, 3, 4, 5, 6]),
    (("model", "states"), []),
    (("model", "states", 0, "state_id"), False),
    (("model", "states", 0, "state_id"), NativeIntSubclass(0)),
    (("model", "states", 0, "frame_id"), False),
    (("model", "states", 0, "frame_id"), 2),
    (("model", "states", 0, "kept", 0), False),
    (("model", "states", 0, "kept"), [7, 0]),
    (("model", "states", 0, "kept"), [0, 0, 7]),
    (("model", "states", 0, "kept"), [0]),
    (("model", "states", 0, "kept"), (0, 7)),
    (("model", "states", 0, "past", 1, 0), False),
    (("model", "states", 0, "past", 1), [0, 0]),
    (("model", "states", 0, "past", 1), [2]),
    (("model", "states", 0, "past", 1), []),
    (("model", "states", 0, "past", 0), [0]),
    (("model", "states", 0, "past", 0), [1]),
    (("model", "states", 1, "past", 2), [1]),
    (("model", "states", 1, "past", 2), [1, 0]),
    (("model", "states", 1, "extra"), 0),
    (("model", "states", 1, "state_id"), 3),
    (("model", "states", 1, "state_id"), 1 << 4096),
]


@pytest.mark.parametrize("path,value", RAW_BAD_PATHS)
def test_raw_model_strict_schema_native_identity_order_marks_and_bounds(executors, path, value):
    malformed = replaced(micro_problem(), path, value)
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(malformed)


@pytest.mark.parametrize("kind", ["duplicate", "missing_successor", "single_frame", "state_cap"])
def test_raw_domain_requires_unique_observations_and_single_deletion_closure(executors, kind):
    malformed = micro_problem()
    states = malformed["model"]["states"]
    if kind == "duplicate":
        states.append({**states[0], "state_id": 2})
    elif kind == "missing_successor":
        states[0] = {"state_id": 0, "frame_id": 0, "kept": [0, 1, 7], "past": [[], [0], [0, 1]]}
    elif kind == "single_frame":
        states[1] = {"state_id": 1, "frame_id": 0, "kept": [0, 1, 7], "past": [[], [0], [0, 1]]}
    else:
        malformed["model"]["states"] = [states[0]] * 4448
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(malformed)


LOCAL_BAD_PATHS = [
    (("schema_version",), "det8-qr05r-profile-v1"),
    (("raw_model",), {}),
    (("profiles",), []),
    (("classes", 0, "extra"), 0),
    (("classes", 0, "representative_state"), 0),
    (("classes", 0, "class_id"), False),
    (("classes", 0, "class_id"), NativeIntSubclass(0)),
    (("classes", 0, "class_id"), 1),
    (("classes", 0, "frame_id"), False),
    (("classes", 0, "frame_id"), 2),
    (("classes", 0, "parent_color_sizes"), [False, 0]),
    (("classes", 0, "parent_color_sizes"), [0.0, 0]),
    (("classes", 0, "parent_color_sizes"), [0]),
    (("classes", 0, "parent_color_sizes"), [0, 0, 0]),
    (("classes", 0, "parent_color_sizes"), [4, 0]),
    (("classes", 0, "parent_color_sizes"), [-1, 0]),
    (("classes", 0, "parent_color_sizes"), (0, 0)),
    (("classes", 0, "even"), ()),
    (("classes", 0, "odd"), NativeListSubclass()),
    (("classes", 1, "even"), []),
    (("classes", 1, "even", 0, "target_class"), False),
    (("classes", 1, "even", 0, "target_class"), 24),
    (("classes", 1, "even", 0, "target_class"), 12),
    (("classes", 1, "even", 0, "target_class"), 1),
    (("classes", 1, "even", 0, "multiplicity"), True),
    (("classes", 1, "even", 0, "multiplicity"), 0),
    (("classes", 1, "even", 0, "multiplicity"), -1),
    (("classes", 1, "even", 0, "multiplicity"), 2),
    (("classes", 1, "even", 0, "multiplicity"), 4),
    (("classes", 1, "even", 0, "multiplicity"), 1.0),
    (("classes", 1, "even", 0, "multiplicity"), 1 << 4096),
    (("classes", 1, "even", 0, "extra"), 0),
]


@pytest.mark.parametrize("path,value", LOCAL_BAD_PATHS)
def test_local_constructor_exact_schema_ranks_frames_and_native_multiplicities(
    executors, path, value
):
    malformed = replaced(lattice(), path, value)
    for module in executors:
        with pytest.raises(ValueError):
            module.reconstruct_profiles(malformed)


@pytest.mark.parametrize("kind", ["duplicate", "unsorted", "too_many", "wrong_color"])
def test_local_edges_require_canonical_targets_and_color_specific_grade_loss(executors, kind):
    valid = fractional_model() if kind == "unsorted" else lattice()
    if kind == "unsorted":
        # Correcting the top weights makes every word count factorial-divisible.
        valid["classes"][0]["odd"][0]["multiplicity"] = 2
        valid["classes"][0]["odd"][1]["multiplicity"] = 1
    for module in executors:
        module.reconstruct_profiles(valid)
    malformed = copy.deepcopy(valid)
    if kind == "duplicate":
        # Merging the duplicate targets would exactly restore the valid row.
        malformed["classes"][6]["odd"] = [{"target_class": 3, "multiplicity": 1}] * 2
    elif kind == "unsorted":
        malformed["classes"][0]["odd"].reverse()
    elif kind == "too_many":
        # More than three positive atoms also necessarily violates the rank mass bound.
        malformed["classes"][9]["odd"] = [{"target_class": i, "multiplicity": 1} for i in range(4)]
    else:
        malformed["classes"][3]["even"] = malformed["classes"][3]["odd"]
        malformed["classes"][3]["odd"] = []
    for module in executors:
        with pytest.raises(ValueError):
            module.reconstruct_profiles(malformed)


def test_constructor_class_cap_counts_zero_base_cells_without_conflating_distinct_labels(executors):
    local = empty_model(512)
    for module in executors:
        result = module.reconstruct_profiles(local)
        assert len(result["profiles"]) == 512
        assert result["certificate"] == {
            "target_cells": 512**2,
            "base_cells": 512**2,
            "recurrence_cells": 0,
            "normalization_cells": 8192,
            "max_abs_residual": 0,
        }
        assert all(
            row["transitions"]
            == [
                {"target_class": row["class_id"], "retained_color_sizes": [0, 0], "multiplicity": 1}
            ]
            for row in result["profiles"]
        )
        for bad in (empty_model(0), empty_model(513)):
            with pytest.raises(ValueError):
                module.reconstruct_profiles(bad)


@pytest.mark.parametrize(
    "kind",
    [
        "dict_subclass",
        "list_subclass",
        "key_subclass",
        "value_subclass",
        "tuple",
        "float",
        "list_cycle",
        "dict_cycle",
        "deep",
    ],
)
@pytest.mark.parametrize("method", ["analyze", "reconstruct_profiles"])
def test_public_apis_reject_non_native_cyclic_and_deep_malformed_inputs(executors, kind, method):
    value = micro_problem() if method == "analyze" else empty_model()
    if kind == "dict_subclass":
        value = NativeDictSubclass(value)
    elif kind == "list_subclass":
        value["extra"] = NativeListSubclass()
    elif kind == "key_subclass":
        value[NativeStrSubclass("schema_version")] = value.pop("schema_version")
    elif kind == "value_subclass":
        value["schema_version"] = NativeStrSubclass(value["schema_version"])
    elif kind == "tuple":
        value["extra"] = ()
    elif kind == "float":
        value["extra"] = 0.0
    elif kind == "list_cycle":
        nested = []
        nested.append(nested)
        value["extra"] = nested
    elif kind == "dict_cycle":
        nested = {}
        nested["self"] = nested
        value["extra"] = nested
    else:
        nested = []
        for _ in range(1500):
            nested = [nested]
        value["extra"] = nested
    for module in executors:
        with pytest.raises(ValueError):
            getattr(module, method)(value)


def test_constructor_returns_detached_owned_results_and_revalidates_mutated_input(executors):
    for module in executors:
        value = lattice(True)
        before = wire(value)
        output = module.reconstruct_profiles(value)
        wanted = wire(output)
        output["profiles"][0]["parent_color_sizes"][0] = -99
        output["profiles"][0]["transitions"][0]["multiplicity"] = -99
        output["operator_checks"]["rows"][0]["class_id"] = -99
        assert wire(value) == before
        assert wire(module.reconstruct_profiles(value)) == wanted
        value["classes"][0]["odd"][0]["multiplicity"] = True
        with pytest.raises(ValueError):
            module.reconstruct_profiles(value)
        assert wire(module.reconstruct_profiles(json.loads(before))) == wanted


@pytest.mark.parametrize("method", ["analyze", "reconstruct_profiles"])
def test_public_resource_cap_can_be_exercised_without_large_allocations(
    executors, monkeypatch, method
):
    value = micro_problem() if method == "analyze" else empty_model()
    for module, constant in zip(executors, ("WORKING_CAP", "_MAX_WORK"), strict=True):
        before = wire(getattr(module, method)(value))
        with monkeypatch.context() as guarded:
            guarded.setattr(module, constant, 32)
            with pytest.raises(ValueError):
                getattr(module, method)(value)
        assert wire(getattr(module, method)(value)) == before


def test_analyze_routes_through_local_only_public_constructor(
    executors, micro_analysis, monkeypatch
):
    for module in executors:
        original = module.reconstruct_profiles
        received = []

        def observe(local, original=original, received=received):
            assert set(local) == {"schema_version", "classes"}
            assert local["schema_version"] == "det8-qr05s-local-v1"
            assert all(
                set(row) == {"class_id", "frame_id", "parent_color_sizes", "odd", "even"}
                for row in local["classes"]
            )
            received.append(wire(local))
            return original(local)

        with monkeypatch.context() as interception:
            interception.setattr(module, "reconstruct_profiles", observe)
            assert wire(module.analyze(micro_problem())) == wire(micro_analysis)
        assert len(received) == 1

        def constructor_failure(_):
            raise ValueError("test sentinel: local constructor was required")

        with monkeypatch.context() as interception:
            interception.setattr(module, "reconstruct_profiles", constructor_failure)
            with pytest.raises(ValueError, match="test sentinel"):
                module.analyze(micro_problem())


def test_analyze_results_do_not_alias_input_or_later_calls(executors, micro_analysis):
    wanted = wire(micro_analysis)
    for module in executors:
        value = micro_problem()
        before = wire(value)
        result = module.analyze(value)
        result["features"][0]["color_sizes"][0] = -99
        result["features"][0]["pair_graded"][0][0][0][0] = -99
        result["partition"]["classes"][0]["key"][0][1][0] = -99
        result["reconstruction"]["class_profiles"][0]["transitions"][0]["multiplicity"] = -99
        assert wire(value) == before
        assert wire(module.analyze(value)) == wanted


@pytest.mark.parametrize(
    "kind",
    ["parent_rank", "frame", "target_rank", "row_mass", "native", "missing_member", "wrong_label"],
)
def test_production_closure_requires_its_structural_local_premises(executors, kind):
    part, rows, _ = synthetic_local("none")
    if kind == "parent_rank":
        rows[1]["parent_color_sizes"] = [2, 1]
    elif kind == "frame":
        rows[1]["frame_id"] = 1
    elif kind == "target_rank":
        rows[0]["odd"][0]["target_class"] = 4
    elif kind == "row_mass":
        rows[0]["odd"][0]["multiplicity"] = 2
    elif kind == "native":
        rows[0]["state_id"] = False
    elif kind == "missing_member":
        part["classes"][0]["members"] = [0]
    else:
        part["state_classes"][1] = 1
    for module in executors:
        with pytest.raises(ValueError):
            module.closure_from_local(rows, part)


def test_aggregate_native_json_exact_independent_audit_and_declared_prior_bridge(
    aggregate, independent, problem
):
    runner, suite = aggregate
    expected, _, profiles, _, _ = independent
    assert set(suite) == {
        "problem",
        "analysis",
        "independent_route_equal",
        "independent_audit",
        "prior_bridge",
        "public_controls",
        "invalid_inputs_rejected",
        "totals",
    }
    assert wire(json.loads(wire(suite))) == wire(suite) == runner.canonical(suite)
    assert wire(suite["analysis"]) == wire(expected)
    assert wire(suite["problem"]) == wire(problem)
    assert suite["independent_route_equal"] is True
    assert suite["independent_audit"] == {
        "raw_observations_reconstructed": True,
        "all_features_and_H_fibers_checked": True,
        "all_single_deletions_and_multiplicities_checked": True,
        "all_subset_profiles_and_power_laws_checked": True,
        "all_local_recurrences_and_operator_maps_checked": True,
        "all_rank_normalizations_checked": True,
        "analysis_sha256": digest(expected),
    }
    assert suite["prior_bridge"] == {
        "prior_artifact": "qr-05r-deletion-profile-2026-09-06/results.json",
        "declared_raw_model_input_dependency": True,
        "source_alias_universe_regenerated": False,
        "matched_states": 4447,
        "all_features_equal": True,
        "actual_H_fibers_equal": True,
        "all_state_and_class_profiles_equal": True,
        "all_fine_pushed_quotient_laws_equal": True,
        "R_probability_helper_recomputed": False,
        "Q_four_variable_certificate_recomputed": False,
        "expanded_minimality_tested": False,
    }
    public = suite["public_controls"]
    # Each 32-class two-frame 0..3 lattice has 2*(1+2+3+4)^2 positive atoms.
    class_atoms = sum(
        len(row["transitions"]) for row in expected["reconstruction"]["class_profiles"]
    )
    assert public == {
        "calls": 12,
        "distinct_models": 3,
        "compared_profile_atoms": 2 * (class_atoms + 400),
        "invalid_calls_rejected": 16,
        "reverse_ID_topology_checked": True,
        "mixed_order_obstruction_rejected": True,
        "fractional_reconstruction_rejected": True,
        "hidden_raw_model_dependency": False,
        "detached_outputs_checked": True,
    }
    assert suite["invalid_inputs_rejected"] == 16
    assert suite["totals"] == {
        **expected["counts"],
        "local_closed": expected["local_closure"]["closed"],
        "member_comparisons": expected["local_closure"]["member_comparisons"],
        "profile_cells": 16 * sum(len(row["transitions"]) for row in profiles),
        "power_cells": 16 * sum(len(row["transitions"]) for row in profiles),
        **expected["reconstruction"]["certificate"],
        "operator_coefficient_cells": expected["reconstruction"]["operator_checks"]["totals"][
            "coefficient_cells"
        ],
        "public_calls": 12,
    }
    assert len(runner.SOURCES) == 6 and len(runner.PRIORS) == 23
    assert runner.PRIORS["qr-05r-deletion-profile-2026-09-06/results.json"] == R_SHA


AUDIT_CORRUPTIONS = [
    (("features", 0, "chain_counts", 0), True),
    (("features", 0, "pair_graded", 0, 0, 0, 0), 2),
    (("local_rows", 0, "state_id"), False),
    (("local_rows", 0, "frame_id"), False),
    (("local_rows", 0, "parent_color_sizes", 0), False),
    (("local_closure", "member_comparisons"), 0),
    (("local_closure", "closed"), 1),
    (("reconstruction", "class_profiles", 0, "transitions", 0, "multiplicity"), True),
    (("reconstruction", "certificate", "base_cells"), 0),
    (("reconstruction", "certificate", "recurrence_cells"), 0),
    (("reconstruction", "operator_checks", "verified"), 1),
    (("comparison", "direct_profiles_sha256"), "0" * 64),
    (("comparison", "local_full_equivalent"), False),
    (("comparison", "max_abs_residual"), 1),
    (("counts", "fine_local_choices"), 1),
]


@pytest.mark.parametrize("path,value", AUDIT_CORRUPTIONS)
def test_independent_full_audit_rejects_typed_and_mathematical_corruption(aggregate, path, value):
    runner, suite = aggregate
    corrupted = replaced(suite["analysis"], path, value)
    assert wire(corrupted) != wire(suite["analysis"])
    with pytest.raises(ValueError):
        runner.check_analysis(corrupted, suite["problem"]["model"])


def test_audit_detects_omitted_local_atoms_and_operator_multiplicity_not_just_support(aggregate):
    runner, suite = aggregate
    a, model = suite["analysis"], suite["problem"]["model"]
    sid, color = next(
        (row["state_id"], color)
        for row in a["local_rows"]
        for color in ("odd", "even")
        if row[color]
    )
    corrupted = replaced(a, ("local_rows", sid, color), a["local_rows"][sid][color][1:])
    with pytest.raises(ValueError):
        runner.check_analysis(corrupted, model)
    row = next(
        row
        for row in a["reconstruction"]["operator_checks"]["rows"]
        if row["odd_odd_pairs"] > row["odd_odd_targets"]
    )
    corrupted = replaced(
        a,
        ("reconstruction", "operator_checks", "rows", row["class_id"], "odd_odd_pairs"),
        row["odd_odd_targets"],
    )
    with pytest.raises(ValueError):
        runner.check_analysis(corrupted, model)


def test_audit_requires_actual_fibers_even_with_identical_class_counts_sizes_and_representatives(
    aggregate,
):
    runner, suite = aggregate
    a = suite["analysis"]
    classes = a["partition"]["classes"]
    left, right = next(
        (left, right)
        for left, right in combinations(classes, 2)
        if len(left["members"]) >= 2
        and len(right["members"]) >= 2
        and min(left["members"][-1], right["members"][-1])
        > max(left["members"][0], right["members"][0])
    )
    lsid, rsid = left["members"][-1], right["members"][-1]
    corrupted = replaced(
        a,
        ("partition", "classes", left["class_id"], "members"),
        sorted(left["members"][:-1] + [rsid]),
    )
    corrupted = replaced(
        corrupted,
        ("partition", "classes", right["class_id"], "members"),
        sorted(right["members"][:-1] + [lsid]),
    )
    corrupted = replaced(corrupted, ("partition", "state_classes", lsid), right["class_id"])
    corrupted = replaced(corrupted, ("partition", "state_classes", rsid), left["class_id"])
    assert [len(row["members"]) for row in corrupted["partition"]["classes"]] == [
        len(row["members"]) for row in classes
    ]
    assert [row["members"][0] for row in corrupted["partition"]["classes"]] == [
        row["members"][0] for row in classes
    ]
    assert sorted(
        sid for row in corrupted["partition"]["classes"] for sid in row["members"]
    ) == list(range(len(a["features"])))
    with pytest.raises(ValueError):
        runner.check_analysis(corrupted, suite["problem"]["model"])


@pytest.mark.parametrize("kind", ["state_subclass", "key_subclass", "bool_state", "semantic"])
def test_checker_cache_revalidates_native_input_and_exact_content(aggregate, micro_analysis, kind):
    runner, _ = aggregate
    model = micro_problem()["model"]
    valid = runner.check_analysis(micro_analysis, model)
    assert valid["all_single_deletions_and_multiplicities_checked"] is True
    if kind == "state_subclass":
        model["states"][0]["state_id"] = NativeIntSubclass(0)
    elif kind == "key_subclass":
        model[NativeStrSubclass("states")] = model.pop("states")
    elif kind == "bool_state":
        model["states"][0]["state_id"] = False
    else:
        model["states"][1]["past"][2] = [1]
    with pytest.raises(ValueError):
        runner.check_analysis(micro_analysis, model)
    assert runner.check_analysis(micro_analysis, micro_problem()["model"]) == valid


@pytest.mark.parametrize(
    "replacement", [True, 0.0, (0,), NativeIntSubclass(0), NativeListSubclass([0])]
)
def test_runner_native_guard_and_type_sensitive_comparison(aggregate, replacement):
    runner, _ = aggregate
    with pytest.raises(ValueError):
        runner.require_same_wire(
            {"nested": [0]}, {"nested": [replacement]}, "different native typed value"
        )
    assert runner.require_same_wire({"nested": [0]}, {"nested": [0]}, "equal") is None


def test_internal_transitivity_is_required_even_with_endpoints_and_deletion_successors(executors):
    malformed = micro_problem()
    interior = [1, 2, 4]
    relation = {(1, 2), (2, 4)}  # The omitted 1<4 is an internal comparison.
    states = []
    for mask in range(8):
        kept = [0] + [v for i, v in enumerate(interior) if mask & (1 << i)] + [7]
        edges = relation | {(0, v) for v in kept if v != 0} | {(v, 7) for v in kept if v != 7}
        past = [[i for i, left in enumerate(kept) if (left, right) in edges] for right in kept]
        states.append({"state_id": mask, "frame_id": 0, "kept": kept, "past": past})
    states.append({**malformed["model"]["states"][1], "state_id": 8})
    malformed["model"]["states"] = states
    registry = {state_key(s["frame_id"], s["kept"], s["past"]) for s in states}
    for state in states:
        edges = relation_of(state)
        assert all((0, v) in edges for v in state["kept"] if v != 0)
        assert all((v, 7) in edges for v in state["kept"] if v != 7)
        for removed in set(state["kept"]) & set(
            malformed["model"]["frames"][state["frame_id"]]["eligible"]
        ):
            assert induced_key(state, [v for v in state["kept"] if v != removed]) in registry
    assert {(1, 2), (2, 4)} <= relation_of(states[7]) and (1, 4) not in relation_of(states[7])
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(malformed)


def test_public_guards_and_constructive_controls_survive_optimized_python(tmp_path):
    fixtures = {
        "micro": micro_problem(),
        "lattice": lattice(True),
        "fractional": fractional_model(),
        "mixed": mixed_model(),
        "synthetic": synthetic_local("both")[:2],
    }
    program = r"""
import copy, importlib.util, json, sys
from pathlib import Path
base = Path(sys.argv[1])
fixtures = json.loads(sys.argv[2])
count = 0
def require(condition, message):
    if not condition:
        raise RuntimeError(message)
def reject(call, value):
    global count
    try:
        call(value)
    except ValueError:
        count += 1
    else:
        raise RuntimeError("invalid input accepted with assertions disabled")
class I(int): pass
class S(str): pass
class L(list): pass
class D(dict): pass
for index, filename in enumerate(("local_deletion.py", "reference_qr05s.py")):
    name = "_qr05s_optimized_" + str(index)
    spec = importlib.util.spec_from_file_location(name, base / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    a = module.analyze(fixtures["micro"])
    require(a["counts"]["fine_local_choices"] == 0 and a["local_closure"]["closed"] is True, "minimum raw model")
    value = module.reconstruct_profiles(fixtures["lattice"])
    require(value["certificate"]["target_cells"] == 24**2 and value["certificate"]["normalization_cells"] == 384, "lattice certificate")
    require(value["profiles"][0]["transitions"][-1]["multiplicity"] == 1, "reversed target topology")
    reject(module.reconstruct_profiles, fixtures["fractional"])
    reject(module.reconstruct_profiles, fixtures["mixed"])
    part, rows = fixtures["synthetic"]
    closure, classes, result = module._closure(part, rows)
    require(closure["member_comparisons"] == 2 and closure["witness"]["color"] == "odd", "failure traversal")
    require(classes == [] and result is None, "failed construction suppression")
    empty = []
    shared = {"schema_version": "det8-qr05s-local-v1", "classes": [{"class_id": 0, "frame_id": 0, "parent_color_sizes": [0, 0], "odd": empty, "even": empty}]}
    require(module.reconstruct_profiles(shared)["certificate"]["base_cells"] == 1, "shared container rejected")
    for method, source in (("analyze", fixtures["micro"]), ("reconstruct_profiles", fixtures["lattice"])):
        call = getattr(module, method)
        for kind in ("dict", "key", "string", "integer", "boolean", "list", "tuple", "float", "cycle", "dictcycle", "deep"):
            bad = copy.deepcopy(source)
            if kind == "dict": bad = D(bad)
            elif kind == "key": bad[S("schema_version")] = bad.pop("schema_version")
            elif kind == "string": bad["schema_version"] = S(bad["schema_version"])
            elif kind in ("integer", "boolean"):
                if method == "analyze": bad["model"]["states"][0]["state_id"] = I(0) if kind == "integer" else False
                else: bad["classes"][0]["class_id"] = I(0) if kind == "integer" else False
            elif kind == "list": bad["extra"] = L()
            elif kind == "tuple": bad["extra"] = ()
            elif kind == "float": bad["extra"] = 0.0
            elif kind == "cycle":
                child = []; child.append(child); bad["extra"] = child
            elif kind == "dictcycle":
                child = {}; child["self"] = child; bad["extra"] = child
            else:
                child = []
                for _ in range(1500): child = [child]
                bad["extra"] = child
            reject(call, bad)
        cap = "WORKING_CAP" if index == 0 else "_MAX_WORK"
        saved = getattr(module, cap)
        setattr(module, cap, 32)
        try: reject(call, source)
        finally: setattr(module, cap, saved)
    result = module.reconstruct_profiles(shared)
    result["profiles"][0]["parent_color_sizes"][0] = -99
    require(module.reconstruct_profiles(shared)["profiles"][0]["parent_color_sizes"] == [0, 0], "cached result alias")
print("optimized rejection controls:", count)
"""
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-X",
            f"pycache_prefix={tmp_path / 'external-bytecode'}",
            "-O",
            "-c",
            program,
            str(HERE),
            json.dumps(fixtures),
        ],
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "optimized rejection controls: 52"


@pytest.mark.parametrize("optimized", [False, True])
def test_compact_shared_dags_fail_before_expanded_traversal_or_serialization(tmp_path, optimized):
    # Forty shared containers describe trillions of expanded nodes. Construct
    # this only inside a bounded subprocess; never serialize it in pytest.
    program = r"""
import copy, importlib.util, json, resource, sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (8, 8))
base = Path(sys.argv[1])
micro = json.loads(sys.argv[2])
count = 0
def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, base / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
def dag():
    value = []
    for _ in range(40):
        value = [value, value]
    return value
def malformed(where):
    value = copy.deepcopy(micro)
    if where == "extra":
        value["extra"] = dag()
    else:
        value["model"][where] = [dag()]
    return value
def reject(call, value):
    global count
    try:
        call(value)
    except ValueError:
        count += 1
    else:
        raise RuntimeError("compact exponentially expanded DAG accepted")
for index, filename in enumerate(("local_deletion.py", "reference_qr05s.py")):
    module = load("_qr05s_dag_" + str(index), filename)
    for where in ("extra", "frames", "states"):
        reject(module.analyze, malformed(where))
    shared = []
    valid = {"schema_version": "det8-qr05s-local-v1", "classes": [{"class_id": 0, "frame_id": 0, "parent_color_sizes": [0, 0], "odd": shared, "even": shared}]}
    reject(module.reconstruct_profiles, {**valid, "extra": dag()})
    # Memoization must be local to each validation call, not a permanent cache
    # of containers or a prohibition against harmless repeated references.
    answer = module.reconstruct_profiles(valid)
    if answer["certificate"]["base_cells"] != 1:
        raise RuntimeError("valid shared-container input rejected after DAG")
runner = load("_qr05s_dag_runner", "study.py")
for where in ("extra", "frames", "states"):
    reject(runner.require_wire, malformed(where))
print("bounded shared-DAG rejections:", count)
"""
    arguments = [
        sys.executable,
        "-I",
        "-X",
        f"pycache_prefix={tmp_path / 'dag-external-bytecode'}",
    ]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE), json.dumps(micro_problem())])
    result = subprocess.run(arguments, text=True, capture_output=True, timeout=15, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "bounded shared-DAG rejections: 11"
