"""Independent T local/full stable-refinement and terminal-profile tests.

Only pinned S JSON supplies the declared raw observation model; no previous
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
S_SHA = "8caa59a1921dc7fb46a38e44058bfe9f2ac5608c1f2ed05e5dc8ff063ab7e3b3"


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
def pinned_s():
    path = HERE.parent / "qr-05s-local-deletion-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 7128993 and hashlib.sha256(raw).hexdigest() == S_SHA
    envelope = json.loads(raw)
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


@pytest.fixture(scope="session")
def problem(pinned_s):
    return {
        "schema_version": "det8-qr05t-problem-v1",
        "family": "qr05t_local_refinement",
        "model": copy.deepcopy(pinned_s["problem"]["model"]),
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05t_test_direct", "local_refinement.py"),
        private_module("_qr05t_test_reference", "reference_qr05t.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors, problem):
    before = wire(problem)
    result = tuple(module.analyze(problem) for module in executors)
    assert wire(problem) == before
    return result


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05t_test_runner", "study.py")
    return runner, runner.run_suite()


def groups(vector):
    answer = []
    for sid, cid in enumerate(vector):
        if cid == len(answer):
            answer.append({"class_id": cid, "members": []})
        assert 0 <= cid < len(answer)
        answer[cid]["members"].append(sid)
    return answer


def refinement_map(source, target):
    result = []
    for group in groups(source):
        values = {target[sid] for sid in group["members"]}
        if len(values) != 1:
            return None
        result.append(values.pop())
    return result


def grouped_rows(raw, vector, mode):
    result = []
    for row in raw:
        sid = row["state_id"]
        if mode == "local":
            value = {
                key: copy.deepcopy(row[key])
                for key in ("state_id", "frame_id", "parent_color_sizes")
            }
            for color in ("odd", "even"):
                counts = {}
                for edge in row[color]:
                    cid = vector[edge["target_state"]]
                    counts[cid] = counts.get(cid, 0) + edge["multiplicity"]
                value[color] = [
                    {"target_class": cid, "multiplicity": count}
                    for cid, count in sorted(counts.items())
                ]
        else:
            counts, ranks = {}, {}
            for edge in row["transitions"]:
                target = edge["target_state"]
                cid = vector[target]
                rank = raw[target]["parent_color_sizes"]
                assert cid not in ranks or ranks[cid] == rank
                ranks[cid] = rank
                counts[cid] = counts.get(cid, 0) + edge["multiplicity"]
            value = {
                "state_id": sid,
                "parent_color_sizes": list(row["parent_color_sizes"]),
                "transitions": [
                    {
                        "target_class": cid,
                        "retained_color_sizes": list(ranks[cid]),
                        "multiplicity": count,
                    }
                    for cid, count in sorted(counts.items())
                ],
            }
        result.append(value)
    return result


def signature(row, mode):
    return [row["odd"], row["even"]] if mode == "local" else [row["transitions"]]


def separating_atom(left, right, mode):
    for color in ("odd", "even") if mode == "local" else ("transitions",):
        lhs = {edge["target_class"]: edge for edge in left[color]}
        rhs = {edge["target_class"]: edge for edge in right[color]}
        for cid in sorted(lhs.keys() | rhs.keys()):
            a = lhs[cid]["multiplicity"] if cid in lhs else 0
            b = rhs[cid]["multiplicity"] if cid in rhs else 0
            if a != b:
                extra = (
                    {"color": color}
                    if mode == "local"
                    else {
                        "retained_color_sizes": list(
                            (lhs.get(cid) or rhs[cid])["retained_color_sizes"]
                        )
                    }
                )
                return {
                    **extra,
                    "target_class": cid,
                    "left_multiplicity": a,
                    "right_multiplicity": b,
                }
    raise AssertionError("different signature lacks a separating atom")


def independent_trace(raw, initial, mode):
    current, rounds = list(initial), []
    bound = min(6, len(raw) - len(groups(initial)))
    while True:
        classes = groups(current)
        assert len(classes) <= 512
        for group in classes:
            assert (
                len(
                    {
                        (raw[sid]["frame_id"], tuple(raw[sid]["parent_color_sizes"]))
                        for sid in group["members"]
                    }
                )
                == 1
            )
        rows = grouped_rows(raw, current, mode)
        next_vector = partition(
            [[current[sid], *signature(row, mode)] for sid, row in enumerate(rows)]
        )["state_classes"]
        next_classes = groups(next_vector)
        comparisons = 0
        for group in classes:
            left = group["members"][0]
            for right in group["members"][1:]:
                comparisons += 1
                same = wire(signature(rows[left], mode)) == wire(signature(rows[right], mode))
                assert same == (next_vector[left] == next_vector[right])
        separations = []
        for child in next_classes:
            right = child["members"][0]
            parent = current[right]
            left = classes[parent]["members"][0]
            if next_vector[left] == child["class_id"]:
                continue
            separations.append(
                {
                    "parent_class_id": parent,
                    "child_class_id": child["class_id"],
                    "left_state": left,
                    "right_state": right,
                    **separating_atom(rows[left], rows[right], mode),
                }
            )
        atoms = sum(
            len(row[color])
            for row in rows
            for color in (("odd", "even") if mode == "local" else ("transitions",))
        )
        stable = next_vector == current
        rounds.append(
            {
                "round_index": len(rounds),
                "state_classes": current,
                "classes": classes,
                "rows_sha256": digest(rows),
                "signature_atoms": atoms,
                "member_comparisons": comparisons,
                "stable": stable,
                "separations": separations,
            }
        )
        assert comparisons == len(raw) - len(classes)
        assert len(separations) == len(next_classes) - len(classes)
        assert refinement_map(next_vector, current) is not None
        if stable:
            break
        current = next_vector
        assert len(rounds) <= bound
    return {
        "mode": mode,
        "rounds": rounds,
        "strict_rounds": len(rounds) - 1,
        "state_classes": current,
        "classes": groups(current),
        "counts": {
            "rounds": len(rounds),
            "signature_atoms": sum(r["signature_atoms"] for r in rounds),
            "member_comparisons": sum(r["member_comparisons"] for r in rounds),
            "separations": sum(len(r["separations"]) for r in rounds),
        },
    }


def bottom_up_partition(raw, initial):
    """Independent acyclic route: classify settled children before their parents."""
    labels, registry = {}, {}
    for sid in sorted(range(len(raw)), key=lambda sid: (sum(raw[sid]["parent_color_sizes"]), sid)):
        key = [initial[sid]]
        for color in ("odd", "even"):
            counts = {}
            for atom in raw[sid][color]:
                child = labels[atom["target_state"]]
                counts[child] = counts.get(child, 0) + atom["multiplicity"]
            key.append(sorted(counts.items()))
        encoded = json.dumps(key, separators=(",", ":"))
        labels[sid] = registry.setdefault(encoded, len(registry))
    return partition([labels[sid] for sid in range(len(raw))])["state_classes"]


@pytest.fixture(scope="session")
def independent(problem):
    model = problem["model"]
    states, frames = model["states"], model["frames"]
    fs = [observed_features(state, frames[state["frame_id"]]) for state in states]
    ckeys, hkeys = [], []
    for state, feature in zip(states, fs, strict=True):
        frame = frames[state["frame_id"]]
        key = [
            [frame["density"], list(frame["fixed"]), list(frame["eligible"])],
            feature["pair_graded"],
            feature["motif_count"],
        ]
        ckeys.append(key)
        hkeys.append(key + [feature["path_count"]])
        assert [feature["pair_graded"][0][1][1][0], feature["pair_graded"][0][1][0][1]] == feature[
            "color_sizes"
        ]
    cp, hp = partition(ckeys), partition(hkeys)
    registry = {state_key(s["frame_id"], s["kept"], s["past"]): s["state_id"] for s in states}
    fine, full, local = [], [], []
    for state, feature in zip(states, fs, strict=True):
        frame = frames[state["frame_id"]]
        present = sorted(set(state["kept"]) & set(frame["eligible"]))
        local_row = {
            "state_id": state["state_id"],
            "frame_id": state["frame_id"],
            "parent_color_sizes": list(feature["color_sizes"]),
        }
        for color, parity in (("odd", 1), ("even", 0)):
            counts = {}
            for vertex in present:
                if vertex % 2 == parity:
                    target = registry[induced_key(state, [v for v in state["kept"] if v != vertex])]
                    counts[target] = counts.get(target, 0) + 1
            local_row[color] = [
                {"target_state": sid, "multiplicity": count}
                for sid, count in sorted(counts.items())
            ]
            assert sum(counts.values()) == feature["color_sizes"][0 if parity else 1]
        local.append(local_row)
        fine_atoms, full_counts = [], {}
        for mask in range(1 << len(present)):
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(present) if mask & (1 << bit)]
            )
            target = registry[induced_key(state, kept)]
            odd, even = fs[target]["color_sizes"]
            fine_atoms.append(
                {
                    "target_state": target,
                    "coefficients": copy.deepcopy(kernel(*feature["color_sizes"], odd, even)),
                }
            )
            full_counts[target] = full_counts.get(target, 0) + 1
        fine.append(
            {
                "state_id": state["state_id"],
                "transitions": sorted(fine_atoms, key=lambda atom: atom["target_state"]),
            }
        )
        full.append(
            {
                **{key: local_row[key] for key in ("state_id", "frame_id", "parent_color_sizes")},
                "transitions": [
                    {"target_state": sid, "multiplicity": count}
                    for sid, count in sorted(full_counts.items())
                ],
            }
        )
    lt = independent_trace(local, cp["state_classes"], "local")
    ft = independent_trace(full, cp["state_classes"], "full")
    lv, fv = lt["state_classes"], ft["state_classes"]
    assert lv == fv == bottom_up_partition(local, cp["state_classes"])
    terminal_local = grouped_rows(local, lv, "local")
    profiles = grouped_rows(full, lv, "full")
    class_local, class_profiles = [], []
    for group in groups(lv):
        rep = group["members"][0]
        for sid in group["members"]:
            assert signature(terminal_local[sid], "local") == signature(
                terminal_local[rep], "local"
            )
            assert profiles[sid]["transitions"] == profiles[rep]["transitions"]
        class_local.append(
            {
                "class_id": group["class_id"],
                "representative_state": rep,
                **{
                    key: terminal_local[rep][key]
                    for key in ("frame_id", "parent_color_sizes", "odd", "even")
                },
            }
        )
        class_profiles.append(
            {
                "class_id": group["class_id"],
                "representative_state": rep,
                **{key: profiles[rep][key] for key in ("parent_color_sizes", "transitions")},
            }
        )
    cert, ops = certificates(class_local, class_profiles)
    powers = pushed(fine, lv)
    for parent, row, profile in zip(fs, powers, profiles, strict=True):
        expanded = []
        for atom in profile["transitions"]:
            table = [
                [atom["multiplicity"] * cell for cell in line]
                for line in kernel(*parent["color_sizes"], *atom["retained_color_sizes"])
            ]
            expanded.append({"target_class": atom["target_class"], "coefficients": table})
        assert row["transitions"] == expanded
    quotient = [
        {
            "class_id": g["class_id"],
            "representative_state": g["members"][0],
            "transitions": powers[g["members"][0]]["transitions"],
        }
        for g in groups(lv)
    ]
    named = {"C": cp["state_classes"], "L": lv, "F": fv, "H": hp["state_classes"]}
    maps = {
        name: refinement_map(named[name.split("_to_")[0]], named[name.split("_to_")[1]])
        for name in ("L_to_C", "F_to_C", "L_to_F", "F_to_L", "L_to_H", "H_to_L")
    }
    hrows = grouped_rows(local, named["H"], "local")
    hclosed = True
    for group in groups(named["H"]):
        for sid in group["members"]:
            equal = signature(hrows[sid], "local") == signature(hrows[group["members"][0]], "local")
            hclosed &= equal
    aligned = [
        refinement_map(
            ft["rounds"][min(i, len(ft["rounds"]) - 1)]["state_classes"],
            lt["rounds"][min(i, len(lt["rounds"]) - 1)]["state_classes"],
        )
        is not None
        for i in range(max(len(lt["rounds"]), len(ft["rounds"])))
    ]
    assert all(aligned) and (not hclosed or maps["H_to_L"] is not None)
    atoms = sum(len(row["transitions"]) for row in profiles)
    a = {
        "model_sha256": digest(model),
        "features": fs,
        "partitions": {"C": cp, "H": hp},
        "fine_kernel": {
            "sha256": digest(fine),
            "atoms": sum(len(row["transitions"]) for row in fine),
        },
        "fine_deletions": {
            "sha256": digest(local),
            "atoms": sum(len(row[color]) for row in local for color in ("odd", "even")),
            "choices": sum(sum(row["parent_color_sizes"]) for row in local),
        },
        "local_refinement": lt,
        "full_refinement": ft,
        "comparison": {
            "names": list(named),
            "refinement": [
                [refinement_map(left, right) is not None for right in named.values()]
                for left in named.values()
            ],
            "maps": maps,
            "same_terminal_memberships": lv == fv,
            "same_memberships_as_H": lv == named["H"],
            "H_local_closed": hclosed,
            "aligned_full_refines_local": aligned,
        },
        "terminal": {
            "local_rows": class_local,
            "class_profiles": class_profiles,
            "reconstruction": {"certificate": cert, "operator_checks": ops},
            "closure": {
                "local_closed": True,
                "full_closed": True,
                "classes_checked": len(class_local),
                "member_comparisons": len(states) - len(class_local),
            },
            "comparison": {
                "direct_profiles_sha256": digest(profiles),
                "reconstructed_profiles_sha256": digest(profiles),
                "pushed_rows_sha256": digest(powers),
                "quotient_rows_sha256": digest(quotient),
                "profile_cells": 16 * atoms,
                "power_cells": 16 * atoms,
                "max_abs_residual": 0,
            },
        },
        "minimality": {
            "verified": True,
            "initial_partition": "C",
            "terminal_partition": "L",
            "all_rounds_refine_C": True,
            "all_rounds_rank_frame_measurable": True,
            "local_full_terminals_equal": True,
            "H_used_in_construction": False,
            "strict_round_bound": min(6, len(states) - len(cp["classes"])),
            "relative_to_C": True,
            "arbitrary_partitions_enumerated": False,
        },
        "counts": {
            "states": len(states),
            "C_classes": len(cp["classes"]),
            "H_classes": len(hp["classes"]),
            "L_classes": len(lt["classes"]),
            "F_classes": len(ft["classes"]),
            "fine_atoms": sum(len(row["transitions"]) for row in fine),
            "fine_local_choices": sum(sum(row["parent_color_sizes"]) for row in local),
            "local_strict_rounds": lt["strict_rounds"],
            "full_strict_rounds": ft["strict_rounds"],
            "terminal_local_atoms": sum(
                len(row[color]) for row in class_local for color in ("odd", "even")
            ),
            "terminal_profile_atoms": sum(len(row["transitions"]) for row in class_profiles),
        },
    }
    return a, local, full, fine, profiles, quotient, hrows


def test_complete_outputs_equal_independent_raw_reconstruction(
    analyses, independent, problem, pinned_s
):
    expected, local, full, fine, _, _, hrows = independent
    assert wire(analyses[0]) == wire(analyses[1]) == wire(expected)
    assert wire(json.loads(wire(expected))) == wire(expected)
    assert len(wire(expected)) < 64 * 1024 * 1024
    assert wire(problem["model"]) == wire(pinned_s["problem"]["model"])
    prior = pinned_s["analysis"]
    assert wire(expected["features"]) == wire(prior["features"])
    assert wire(expected["partitions"]["H"]) == wire(prior["partition"])
    assert wire(hrows) == wire(prior["local_rows"])
    assert digest(fine) == prior["comparison"]["fine_kernel_sha256"]
    assert len(local) == len(full) == 4447
    assert expected["fine_kernel"]["atoms"] == 168388


def test_raw_one_deletion_rows_are_full_subset_slices_with_original_color_and_multiplicity(
    independent, problem
):
    a, local, full, _, _, _, _ = independent
    saw_reverse = saw_fixed = False
    for state, row, entire, feature in zip(
        problem["model"]["states"], local, full, a["features"], strict=True
    ):
        rank = row["parent_color_sizes"]
        atoms = entire["transitions"]
        totals = zero()
        for atom in atoms:
            target = atom["target_state"]
            child = full[target]
            assert child["frame_id"] == row["frame_id"]
            m, n = child["parent_color_sizes"]
            totals[m][n] += atom["multiplicity"]
            assert atom["multiplicity"] == 1
            if child["parent_color_sizes"] == rank:
                assert target == state["state_id"]
        assert totals == [
            [choose(rank[0], m) * choose(rank[1], n) for n in range(4)] for m in range(4)
        ]
        for color, decrement in (("odd", [1, 0]), ("even", [0, 1])):
            target_rank = [rank[i] - decrement[i] for i in range(2)]
            assert row[color] == [
                atom
                for atom in atoms
                if full[atom["target_state"]]["parent_color_sizes"] == target_rank
            ]
            for atom in row[color]:
                target = problem["model"]["states"][atom["target_state"]]
                removed = set(state["kept"]) - set(target["kept"])
                assert len(removed) == 1
                assert next(iter(removed)) % 2 == (1 if color == "odd" else 0)
        saw_reverse |= any(left > right for left, right in relation_of(state))
        if row["frame_id"] == 1:
            saw_fixed = True
            assert 3 in state["kept"] and feature["mean_graded"][1][0][0] == 1
    assert saw_reverse and saw_fixed


def test_full_trace_refines_local_at_aligned_rounds_without_assuming_equal_speeds(independent):
    a, local, full, _, _, _, _ = independent
    initial = a["partitions"]["C"]["state_classes"]
    for mode, raw in (("local", local), ("full", full)):
        trace = a[mode + "_refinement"]
        assert trace["strict_rounds"] <= min(6, len(raw) - len(groups(initial)))
        assert len(trace["rounds"]) == trace["strict_rounds"] + 1 <= 7
        assert sum(row["stable"] for row in trace["rounds"]) == 1 and trace["rounds"][-1]["stable"]
        assert trace["counts"]["separations"] == len(trace["classes"]) - len(groups(initial))
        for index, round_ in enumerate(trace["rounds"]):
            assert refinement_map(round_["state_classes"], initial) is not None
            assert round_["rows_sha256"] == digest(grouped_rows(raw, round_["state_classes"], mode))
            assert round_["member_comparisons"] == len(raw) - len(round_["classes"])
            children = [item["child_class_id"] for item in round_["separations"]]
            assert children == sorted(set(children))
            if index < trace["strict_rounds"]:
                assert len(round_["separations"]) == len(
                    trace["rounds"][index + 1]["classes"]
                ) - len(round_["classes"])
            else:
                assert round_["separations"] == []
    assert all(a["comparison"]["aligned_full_refines_local"])
    assert a["local_refinement"]["state_classes"] == bottom_up_partition(local, initial)


def test_terminal_constructors_use_only_local_rows_and_equal_independent_subsets(
    executors, independent
):
    a, local, _, _, _, _, _ = independent
    for module in executors:
        payload = {
            "schema_version": "det8-qr05t-local-v1",
            "state_classes": list(a["partitions"]["C"]["state_classes"]),
            "rows": local,
        }
        before = wire(payload)
        assert wire(module.refine_local(payload)) == wire(a["local_refinement"])
        assert wire(payload) == before
        rows = a["terminal"]["local_rows"]
        result = module.reconstruct_profiles(local_payload(rows))
        profiles = [
            {key: row[key] for key in ("class_id", "parent_color_sizes", "transitions")}
            for row in a["terminal"]["class_profiles"]
        ]
        assert wire(result) == wire({"profiles": profiles, **a["terminal"]["reconstruction"]})


def raw_local(ranks, odd, even=None, frames=None):
    even = even or [[] for _ in ranks]
    frames = frames or [0] * len(ranks)
    return [
        {
            "state_id": sid,
            "frame_id": frames[sid],
            "parent_color_sizes": list(rank),
            "odd": [{"target_state": target, "multiplicity": mult} for target, mult in odd[sid]],
            "even": [{"target_state": target, "multiplicity": mult} for target, mult in even[sid]],
        }
        for sid, rank in enumerate(ranks)
    ]


def synthetic(kind):
    if kind == "two_rounds":
        return raw_local(
            [[2, 0], [2, 0], [1, 0], [1, 0], [0, 0], [0, 0]],
            [[(2, 2)], [(3, 2)], [(4, 1)], [(5, 1)], [], []],
        ), [0, 0, 1, 1, 2, 3]
    if kind == "multiplicity":
        return raw_local(
            [[3, 0], [3, 0], [2, 0], [2, 0], [1, 0], [0, 0]],
            [[(2, 1), (3, 2)], [(2, 2), (3, 1)], [(4, 2)], [(4, 2)], [(5, 1)], []],
        ), [0, 0, 1, 2, 3, 4]
    if kind == "inherited":
        return raw_local([[0, 0], [0, 0]], [[], []]), [0, 1]
    if kind == "witness_order":
        return raw_local(
            [[1, 0], [1, 0], [0, 0], [1, 0], [1, 0], [0, 0]],
            [[(2, 1)], [(2, 1)], [], [(5, 1)], [(5, 1)], []],
        ), [0, 1, 2, 1, 0, 3]
    if kind == "both_colors":
        return raw_local(
            [[1, 1], [1, 1], [0, 0], [0, 1], [0, 1], [1, 0], [1, 0]],
            [[(3, 1)], [(4, 1)], [], [], [], [(2, 1)], [(2, 1)]],
            [[(5, 1)], [(6, 1)], [], [(2, 1)], [(2, 1)], [], []],
        ), [0, 0, 1, 2, 3, 4, 5]
    if kind == "six_rounds":
        labels = [(o, e, branch) for o, e in product(range(4), repeat=2) for branch in (0, 1)]
        ids = {label: sid for sid, label in enumerate(labels)}
        rows = raw_local(
            [[o, e] for o, e, _ in labels],
            [[(ids[o - 1, e, b], o)] if o else [] for o, e, b in labels],
            [[(ids[o, e - 1, b], e)] if e else [] for o, e, b in labels],
        )
        initial = partition([[o, e, b if o + e == 0 else -1] for o, e, b in labels])[
            "state_classes"
        ]
        return rows, initial
    raise AssertionError("unknown test-only algebraic control")


def full_from_words(local):
    class_rows = [
        {
            "class_id": row["state_id"],
            "frame_id": row["frame_id"],
            "parent_color_sizes": row["parent_color_sizes"],
            **{
                color: [
                    {"target_class": atom["target_state"], "multiplicity": atom["multiplicity"]}
                    for atom in row[color]
                ]
                for color in ("odd", "even")
            },
        }
        for row in local
    ]
    result = []
    for row in local:
        sid = row["state_id"]
        o, e = row["parent_color_sizes"]
        counts = {}
        for a, b in product(range(o + 1), range(e + 1)):
            divisor = factorial(a) * factorial(b)
            powers = word(class_rows, sid, ["odd"] * a + ["even"] * b)
            assert powers == word(class_rows, sid, ["even"] * b + ["odd"] * a)
            for target, numerator in powers.items():
                assert numerator % divisor == 0 and local[target]["parent_color_sizes"] == [
                    o - a,
                    e - b,
                ]
                counts[target] = numerator // divisor
        result.append(
            {
                **{key: row[key] for key in ("state_id", "frame_id", "parent_color_sizes")},
                "transitions": [
                    {"target_state": target, "multiplicity": count}
                    for target, count in sorted(counts.items())
                ],
            }
        )
    return result


@pytest.mark.parametrize(
    "kind",
    ["two_rounds", "multiplicity", "inherited", "witness_order", "both_colors", "six_rounds"],
)
def test_synthetic_refinement_equations_speeds_multiplicities_and_canonical_witnesses(
    executors, kind
):
    local, initial = synthetic(kind)
    full = full_from_words(local)
    expected_local, expected_full = (
        independent_trace(local, initial, "local"),
        independent_trace(full, initial, "full"),
    )
    assert (
        expected_local["state_classes"]
        == expected_full["state_classes"]
        == bottom_up_partition(local, initial)
    )
    before = wire([local, full, initial])
    for module in executors:
        assert wire(
            module.refine_local(
                {"schema_version": "det8-qr05t-local-v1", "rows": local, "state_classes": initial}
            )
        ) == wire(expected_local)
        assert wire(module._refine_full(full, initial)) == wire(expected_full)
    assert wire([local, full, initial]) == before
    if kind == "two_rounds":
        assert [len(r["classes"]) for r in expected_local["rounds"]] == [4, 5, 6]
        assert [len(r["classes"]) for r in expected_full["rounds"]] == [4, 6]
    elif kind == "six_rounds":
        assert expected_local["strict_rounds"] == 6 and expected_full["strict_rounds"] == 1
        assert len(expected_local["rounds"]) == 7
    elif kind == "multiplicity":
        assert {a["target_state"] for a in local[0]["odd"]} == {
            a["target_state"] for a in local[1]["odd"]
        }
        assert (
            sum(a["multiplicity"] for a in local[0]["odd"])
            == sum(a["multiplicity"] for a in local[1]["odd"])
            == 3
        )
        assert expected_local["rounds"][0]["separations"][0] == {
            "parent_class_id": 0,
            "child_class_id": 1,
            "left_state": 0,
            "right_state": 1,
            "color": "odd",
            "target_class": 1,
            "left_multiplicity": 1,
            "right_multiplicity": 2,
        }
    elif kind == "inherited":
        assert expected_local["strict_rounds"] == 0 and expected_local["state_classes"] == [0, 1]
        assert local[0]["odd"] == local[1]["odd"] == local[0]["even"] == local[1]["even"] == []
    elif kind == "witness_order":
        witnesses = expected_local["rounds"][0]["separations"]
        assert [w["child_class_id"] for w in witnesses] == [3, 4]
        assert [w["parent_class_id"] for w in witnesses] == [1, 0]
        assert all(
            w["target_class"] == 2 and w["left_multiplicity"] == 1 and w["right_multiplicity"] == 0
            for w in witnesses
        )
    else:
        witness = expected_local["rounds"][0]["separations"][0]
        assert witness["color"] == "odd" and witness["target_class"] == 2


def nonrealizable_local(kind):
    if kind == "fractional":
        return raw_local(
            [[3, 0], [2, 0], [2, 0], [1, 0], [1, 0], [0, 0]],
            [[(1, 1), (2, 2)], [(3, 1), (4, 1)], [(4, 2)], [(5, 1)], [(5, 1)], []],
        )
    return raw_local(
        [[1, 1], [0, 1], [1, 0], [0, 0], [0, 0]],
        [[(1, 1)], [], [(4, 1)], [], []],
        [[(2, 1)], [(3, 1)], [], [], []],
    )


@pytest.mark.parametrize("kind", ["fractional", "mixed"])
def test_local_stability_is_not_a_claim_of_full_subset_integrality_or_poset_realization(
    executors, kind
):
    rows = nonrealizable_local(kind)
    initial = list(range(len(rows)))
    expected = independent_trace(rows, initial, "local")
    classes = [
        {
            "class_id": row["state_id"],
            "frame_id": row["frame_id"],
            "parent_color_sizes": row["parent_color_sizes"],
            **{
                color: [
                    {"target_class": atom["target_state"], "multiplicity": atom["multiplicity"]}
                    for atom in row[color]
                ]
                for color in ("odd", "even")
            },
        }
        for row in rows
    ]
    for module in executors:
        assert wire(
            module.refine_local(
                {"schema_version": "det8-qr05t-local-v1", "state_classes": initial, "rows": rows}
            )
        ) == wire(expected)
        assert expected["strict_rounds"] == 0
        with pytest.raises(ValueError):
            module.reconstruct_profiles(
                {"schema_version": "det8-qr05s-local-v1", "classes": classes}
            )


class IntSubclass(int):
    pass


class StrSubclass(str):
    pass


class ListSubclass(list):
    pass


class DictSubclass(dict):
    pass


def micro_problem():
    return {
        "schema_version": "det8-qr05t-problem-v1",
        "family": "qr05t_local_refinement",
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
    first, second = (module.analyze(micro_problem()) for module in executors)
    assert wire(first) == wire(second)
    return first


def local_problem(kind="two_rounds"):
    rows, initial = synthetic(kind)
    return {"schema_version": "det8-qr05t-local-v1", "rows": rows, "state_classes": initial}


def simple_constructor():
    shared = []
    return {
        "schema_version": "det8-qr05s-local-v1",
        "classes": [
            {
                "class_id": 0,
                "frame_id": 0,
                "parent_color_sizes": [0, 0],
                "odd": shared,
                "even": shared,
            }
        ],
    }


def test_minimum_raw_model_has_one_stable_round_and_no_fake_strict_round(micro_analysis):
    for name in ("local_refinement", "full_refinement"):
        trace = micro_analysis[name]
        assert trace["strict_rounds"] == 0 and len(trace["rounds"]) == 1
        assert trace["rounds"][0]["state_classes"] == trace["state_classes"] == [0, 1]
        assert trace["rounds"][0]["stable"] is True and trace["rounds"][0]["separations"] == []
    assert micro_analysis["terminal"]["reconstruction"]["certificate"] == {
        "target_cells": 4,
        "base_cells": 2,
        "recurrence_cells": 0,
        "normalization_cells": 32,
        "max_abs_residual": 0,
    }
    assert micro_analysis["minimality"]["strict_round_bound"] == 0


LOCAL_CORRUPTIONS = [
    (("schema_version",), "det8-qr05s-local-v1"),
    (("extra",), 0),
    (("H",), []),
    (("full_profiles",), []),
    (("state_classes",), []),
    (("state_classes",), [0]),
    (("state_classes", 0), False),
    (("state_classes", 0), IntSubclass(0)),
    (("state_classes", 0), 1),
    (("state_classes", 2), 0),
    (("rows",), []),
    (("rows", 0, "state_id"), False),
    (("rows", 0, "state_id"), 1),
    (("rows", 0, "frame_id"), False),
    (("rows", 0, "frame_id"), 2),
    (("rows", 0, "parent_color_sizes"), [True, 0]),
    (("rows", 0, "parent_color_sizes"), [2.0, 0]),
    (("rows", 0, "parent_color_sizes"), [4, 0]),
    (("rows", 0, "parent_color_sizes"), [2]),
    (("rows", 0, "odd"), []),
    (("rows", 0, "even"), ()),
    (("rows", 0, "odd", 0, "target_state"), False),
    (("rows", 0, "odd", 0, "target_state"), 0),
    (("rows", 0, "odd", 0, "target_state"), 6),
    (("rows", 0, "odd", 0, "multiplicity"), True),
    (("rows", 0, "odd", 0, "multiplicity"), 0),
    (("rows", 0, "odd", 0, "multiplicity"), 1),
    (("rows", 0, "odd", 0, "multiplicity"), 4),
    (("rows", 0, "odd", 0, "multiplicity"), 1 << 4096),
    (("rows", 0, "odd", 0, "extra"), 0),
    (("rows", 2, "frame_id"), 1),
]


@pytest.mark.parametrize("path,value", LOCAL_CORRUPTIONS)
def test_local_refiner_requires_exact_schema_measurable_initial_partition_and_weighted_ranks(
    executors, path, value
):
    malformed = replaced(local_problem(), path, value)
    for module in executors:
        with pytest.raises(ValueError):
            module.refine_local(malformed)


@pytest.mark.parametrize("kind", ["duplicate", "unsorted", "color", "zero_color", "frame_fiber"])
def test_canonical_edge_premises_are_checked_on_otherwise_valid_control(executors, kind):
    value = local_problem("multiplicity")
    for module in executors:
        module.refine_local(value)
    if kind == "duplicate":
        value["rows"][0]["odd"] = [
            {"target_state": 2, "multiplicity": 1},
            {"target_state": 3, "multiplicity": 1},
            {"target_state": 3, "multiplicity": 1},
        ]
    elif kind == "unsorted":
        value["rows"][0]["odd"].reverse()
    elif kind == "color":
        value["rows"][0]["even"] = value["rows"][0]["odd"]
        value["rows"][0]["odd"] = []
    elif kind == "zero_color":
        value["rows"][5]["odd"] = [{"target_state": 5, "multiplicity": 1}]
    else:
        value = local_problem("inherited")
        value["state_classes"] = [0, 0]
        value["rows"][1]["frame_id"] = 1
    for module in executors:
        with pytest.raises(ValueError):
            module.refine_local(value)


@pytest.mark.parametrize(
    "kind",
    [
        "self_missing",
        "self_wrong",
        "same_rank_mass",
        "missing_rank",
        "rank_mass",
        "target_bool",
        "rank_bool",
        "frame",
        "duplicate",
        "unsorted",
        "cap",
        "extra",
    ],
)
def test_full_refiner_validates_native_counts_self_delta_all_ranks_and_canonical_atoms(
    executors, kind
):
    local, initial = synthetic("two_rounds")
    rows = full_from_words(local)
    if kind == "self_missing":
        rows[0]["transitions"] = rows[0]["transitions"][1:]
    elif kind == "self_wrong":
        rows[0]["transitions"][0]["target_state"] = 1
    elif kind == "same_rank_mass":
        rows[0]["transitions"][0]["multiplicity"] = 2
    elif kind == "missing_rank":
        rows[0]["transitions"] = [
            atom for atom in rows[0]["transitions"] if atom["target_state"] != 2
        ]
    elif kind == "rank_mass":
        rows[0]["transitions"][1]["multiplicity"] = 1
    elif kind == "target_bool":
        rows[0]["transitions"][0]["target_state"] = False
    elif kind == "rank_bool":
        rows[0]["parent_color_sizes"][1] = False
    elif kind == "frame":
        rows[4]["frame_id"] = 1
    elif kind == "duplicate":
        rows[0]["transitions"].append(rows[0]["transitions"][-1])
    elif kind == "unsorted":
        rows[0]["transitions"].reverse()
    elif kind == "cap":
        rows[0]["transitions"][0]["multiplicity"] = 1 << 4096
    else:
        rows[0]["extra"] = 0
    for module in executors:
        with pytest.raises(ValueError):
            module._refine_full(rows, initial)


def test_state_class_and_new_refinement_caps_fail_without_truncation(executors):
    rows = raw_local([[0, 0]] * 4447, [[] for _ in range(4447)])
    payload = {"schema_version": "det8-qr05t-local-v1", "rows": rows, "state_classes": [0] * 4447}
    for module in executors:
        result = module.refine_local(payload)
        assert result["strict_rounds"] == 0 and result["counts"]["member_comparisons"] == 4446
        assert result["classes"] == [{"class_id": 0, "members": list(range(4447))}]
        with pytest.raises(ValueError):
            module.refine_local(
                {
                    **payload,
                    "rows": rows + [{**rows[0], "state_id": 4447}],
                    "state_classes": [0] * 4448,
                }
            )
        identity_rows = rows[:512]
        assert (
            len(
                module.refine_local(
                    {**payload, "rows": identity_rows, "state_classes": list(range(512))}
                )["classes"]
            )
            == 512
        )
        with pytest.raises(ValueError):
            module.refine_local({**payload, "rows": rows[:513], "state_classes": list(range(513))})
        split_rows = raw_local(
            [[1, 0]] + [[0, 0]] * 511 + [[1, 0]], [[(1, 1)]] + [[] for _ in range(511)] + [[(2, 1)]]
        )
        with pytest.raises(ValueError):
            module.refine_local(
                {**payload, "rows": split_rows, "state_classes": list(range(512)) + [0]}
            )


RAW_CORRUPTIONS = [
    (("model", "states", 0, "state_id"), False),
    (("model", "states", 0, "frame_id"), False),
    (("model", "states", 0, "kept", 0), False),
    (("model", "states", 0, "past", 1, 0), False),
    (("model", "frames", 0, "fixed"), [0, 3, 7]),
    (("model", "frames", 0, "density"), "12/1"),
    (("model", "states", 0, "past", 0), [1]),
    (("model", "states", 0, "past", 1), []),
    (("model", "states", 0, "kept"), [7, 0]),
    (("model", "states", 0, "kept"), (0, 7)),
    (("model", "states", 1, "state_id"), 1 << 4096),
    (("model", "states", 1, "past", 2), [1, 0]),
    (("family",), "qr05s_local_deletion"),
    (("model", "extra"), 0),
]


@pytest.mark.parametrize("path,value", RAW_CORRUPTIONS)
def test_raw_analyzer_preserves_native_order_frame_and_schema_guards(executors, path, value):
    value = replaced(micro_problem(), path, value)
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(value)


def test_internal_transitivity_and_missing_single_deletion_successors_are_separate_premises(
    executors,
):
    value = micro_problem()
    present = [1, 2, 4]
    states = []
    for mask in range(8):
        kept = [0] + [v for bit, v in enumerate(present) if mask & (1 << bit)] + [7]
        relation = (
            {(1, 2), (2, 4)} | {(0, v) for v in kept if v != 0} | {(v, 7) for v in kept if v != 7}
        )
        states.append(
            {
                "state_id": mask,
                "frame_id": 0,
                "kept": kept,
                "past": [[i for i, a in enumerate(kept) if (a, b) in relation] for b in kept],
            }
        )
    states.append({**value["model"]["states"][1], "state_id": 8})
    value["model"]["states"] = states
    registry = {state_key(row["frame_id"], row["kept"], row["past"]) for row in states}
    for state in states[:8]:
        for removed in set(state["kept"]) & set(present):
            assert induced_key(state, [v for v in state["kept"] if v != removed]) in registry
    assert (1, 4) not in relation_of(states[7])
    missing = micro_problem()
    missing["model"]["states"][0] = {
        "state_id": 0,
        "frame_id": 0,
        "kept": [0, 1, 7],
        "past": [[], [0], [0, 1]],
    }
    for module in executors:
        for bad in (value, missing):
            with pytest.raises(ValueError):
                module.analyze(bad)


def mutable_ids(value):
    answer, stack = set(), [value]
    while stack:
        item = stack.pop()
        if type(item) not in (dict, list) or id(item) in answer:
            continue
        answer.add(id(item))
        stack.extend(item.values() if type(item) is dict else item)
    return answer


@pytest.mark.parametrize("method", ["analyze", "refine_local", "reconstruct_profiles"])
def test_complete_mutable_ownership_is_disjoint_both_directions_and_between_calls(
    executors, method
):
    for module in executors:
        value = {
            "analyze": micro_problem,
            "refine_local": local_problem,
            "reconstruct_profiles": simple_constructor,
        }[method]()
        call = getattr(module, method)
        before = wire(value)
        first, second = call(value), call(value)
        wanted = wire(first)
        assert mutable_ids(value).isdisjoint(mutable_ids(first))
        assert mutable_ids(value).isdisjoint(mutable_ids(second))
        assert mutable_ids(first).isdisjoint(mutable_ids(second))
        assert wire(second) == wanted and wire(value) == before
        if method == "analyze":
            first["partitions"]["C"]["classes"][0]["key"][0][1][0] = -99
            first["partitions"]["H"]["classes"][0]["key"][0][2][0] = -99
            value["model"]["frames"][0]["fixed"][0] = -88
        elif method == "refine_local":
            first["rounds"][0]["state_classes"][0] = -99
            value["state_classes"][0] = -88
        else:
            first["profiles"][0]["parent_color_sizes"][0] = -99
            value["classes"][0]["parent_color_sizes"][0] = -88
        assert wire(second) == wanted
        assert wire(call(json.loads(before))) == wanted
        with pytest.raises(ValueError):
            call(value)


def test_analyzer_dispatches_real_local_refiner_from_C_and_local_only_terminal_constructor(
    executors, micro_analysis, monkeypatch
):
    for module in executors:
        refine, construct = module.refine_local, module.reconstruct_profiles
        calls = []

        def local_spy(payload, refine=refine, calls=calls):
            assert set(payload) == {"schema_version", "rows", "state_classes"}
            assert payload["state_classes"] == micro_analysis["partitions"]["C"]["state_classes"]
            calls.append("local")
            return refine(payload)

        def constructor_spy(payload, construct=construct, calls=calls):
            assert set(payload) == {"schema_version", "classes"}
            assert all(
                set(row) == {"class_id", "frame_id", "parent_color_sizes", "odd", "even"}
                for row in payload["classes"]
            )
            calls.append("constructor")
            return construct(payload)

        with monkeypatch.context() as interception:
            interception.setattr(module, "refine_local", local_spy)
            interception.setattr(module, "reconstruct_profiles", constructor_spy)
            assert wire(module.analyze(micro_problem())) == wire(micro_analysis)
        assert calls == ["local", "constructor"]


@pytest.mark.parametrize("method", ["analyze", "refine_local", "reconstruct_profiles"])
@pytest.mark.parametrize(
    "kind", ["dict_subclass", "key_subclass", "value_subclass", "list_subclass", "cycle", "deep"]
)
def test_all_public_entries_reject_non_native_cycles_and_deep_malformed_trees(
    executors, method, kind
):
    value = {
        "analyze": micro_problem,
        "refine_local": local_problem,
        "reconstruct_profiles": simple_constructor,
    }[method]()
    if kind == "dict_subclass":
        value = DictSubclass(value)
    elif kind == "key_subclass":
        value[StrSubclass("schema_version")] = value.pop("schema_version")
    elif kind == "value_subclass":
        value["schema_version"] = StrSubclass(value["schema_version"])
    elif kind == "list_subclass":
        value["extra"] = ListSubclass()
    elif kind == "cycle":
        cycle = []
        cycle.append(cycle)
        value["extra"] = cycle
    else:
        deep = []
        for _ in range(1500):
            deep = [deep]
        value["extra"] = deep
    for module in executors:
        with pytest.raises(ValueError):
            getattr(module, method)(value)


@pytest.mark.parametrize("method", ["analyze", "refine_local", "reconstruct_profiles"])
def test_working_caps_are_enforced_before_return_without_allocating_large_payloads(
    executors, method, monkeypatch
):
    value = {
        "analyze": micro_problem,
        "refine_local": local_problem,
        "reconstruct_profiles": simple_constructor,
    }[method]()
    for module, constant in zip(executors, ("WORKING_CAP", "_MAX_WORK"), strict=True):
        wanted = wire(getattr(module, method)(value))
        with monkeypatch.context() as limited:
            limited.setattr(module, constant, 32)
            with pytest.raises(ValueError):
                getattr(module, method)(value)
        assert wire(getattr(module, method)(value)) == wanted


def test_aggregate_wire_audit_synthetic_controls_and_explicit_prior_projection(
    aggregate, independent, problem, pinned_s
):
    runner, suite = aggregate
    a, _, _, _, profiles, _, _ = independent
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
    assert wire(suite) == runner.canonical(suite) == wire(json.loads(wire(suite)))
    assert wire(suite["analysis"]) == wire(a) and wire(suite["problem"]) == wire(problem)
    assert suite["independent_route_equal"] is True
    assert suite["independent_audit"] == {
        "raw_model_reconstructed": True,
        "all_features_and_fibers_checked": True,
        "all_round_signatures_and_witnesses_reconstructed": True,
        "terminal_profiles_recurrences_and_operators_checked": True,
        "relative_minimality_premises_checked": True,
        "analysis_sha256": digest(a),
    }
    for control, (name, kind) in zip(
        suite["controls"],
        [("multiround", "two_rounds"), ("weighted", "multiplicity"), ("preserve", "inherited")],
        strict=True,
    ):
        local, initial = synthetic(kind)
        full = full_from_words(local)
        assert wire(control) == wire(
            {
                "name": name,
                "local_problem": {
                    "schema_version": "det8-qr05t-local-v1",
                    "rows": local,
                    "state_classes": initial,
                },
                "full_rows": full,
                "local_trace": independent_trace(local, initial, "local"),
                "full_trace": independent_trace(full, initial, "full"),
                "observed_C_realization": False,
            }
        )
    assert suite["public_controls"] == {
        "local_refiner_calls": 16,
        "private_full_control_calls": 6,
        "terminal_constructor_calls": 2,
        "invalid_local_calls_rejected": 14,
        "local_refiner_has_no_full_or_H_input": True,
        "terminal_constructor_has_no_raw_input": True,
    }
    assert suite["invalid_inputs_rejected"] == 14
    assert suite["prior_bridge"] == {
        "prior_artifact": "qr-05s-local-deletion-2026-09-06/results.json",
        "declared_raw_model_input_dependency": True,
        "source_alias_universe_regenerated": False,
        "matched_states": 4447,
        "all_features_equal": True,
        "actual_H_fibers_equal": True,
        "fine_kernel_equal": True,
        "H_local_rows_equal": True,
        "terminal_profiles_equal_after_H_map": True,
        "H_to_L_map_used": True,
        "H_equality_assumed": False,
        "P_minimality_or_consumer_replayed": False,
        "R_probability_helper_recomputed": False,
        "Q_four_variable_certificate_recomputed": False,
    }
    mapping = refinement_map(
        a["partitions"]["H"]["state_classes"], a["local_refinement"]["state_classes"]
    )
    assert mapping is not None
    projected = []
    prior = pinned_s["analysis"]
    for sid, h in enumerate(prior["partition"]["state_classes"]):
        old = prior["reconstruction"]["class_profiles"][h]
        counts, ranks = {}, {}
        for atom in old["transitions"]:
            target = mapping[atom["target_class"]]
            counts[target] = counts.get(target, 0) + atom["multiplicity"]
            ranks[target] = atom["retained_color_sizes"]
        projected.append(
            {
                "state_id": sid,
                "parent_color_sizes": old["parent_color_sizes"],
                "transitions": [
                    {
                        "target_class": target,
                        "retained_color_sizes": ranks[target],
                        "multiplicity": count,
                    }
                    for target, count in sorted(counts.items())
                ],
            }
        )
    assert wire(projected) == wire(profiles)
    assert suite["totals"] == {
        **a["counts"],
        "same_memberships_as_H": a["comparison"]["same_memberships_as_H"],
        "local_rounds": len(a["local_refinement"]["rounds"]),
        "full_rounds": len(a["full_refinement"]["rounds"]),
        "local_signature_atoms": a["local_refinement"]["counts"]["signature_atoms"],
        "full_signature_atoms": a["full_refinement"]["counts"]["signature_atoms"],
        "profile_cells": a["terminal"]["comparison"]["profile_cells"],
        "power_cells": a["terminal"]["comparison"]["power_cells"],
        "local_refiner_calls": 16,
        "terminal_constructor_calls": 2,
    }
    assert len(runner.SOURCES) == 6 and len(runner.PRIORS) == 24
    assert runner.PRIORS["qr-05s-local-deletion-2026-09-06/results.json"] == S_SHA


@pytest.mark.parametrize("mode", ["local", "full"])
@pytest.mark.parametrize(
    "kind",
    [
        "early_stop",
        "extra_round",
        "reordered_rounds",
        "old_vector",
        "fake_stable",
        "digest",
        "signature_count",
        "member_count",
        "omitted_witness",
        "extra_witness",
        "wrong_witness_target",
        "wrong_witness_zero",
    ],
)
def test_root_reconstructs_every_current_partition_next_split_and_first_witness(
    aggregate, mode, kind
):
    runner, suite = aggregate
    a = suite["analysis"]
    key = mode + "_refinement"
    trace = a[key]
    strict = next(index for index, row in enumerate(trace["rounds"]) if row["separations"])
    path = (key, "rounds", strict)
    if kind == "early_stop":
        bad = replaced(a, (key, "rounds"), trace["rounds"][:-1])
    elif kind == "extra_round":
        bad = replaced(a, (key, "rounds"), trace["rounds"] + [trace["rounds"][-1]])
    elif kind == "reordered_rounds":
        bad = replaced(a, (key, "rounds"), list(reversed(trace["rounds"])))
    elif kind == "old_vector":
        bad = replaced(
            a,
            (key, "rounds", strict + 1, "state_classes"),
            trace["rounds"][strict]["state_classes"],
        )
    elif kind == "fake_stable":
        bad = replaced(a, path + ("stable",), True)
    elif kind == "digest":
        bad = replaced(a, path + ("rows_sha256",), "0" * 64)
    elif kind == "signature_count":
        bad = replaced(
            a, path + ("signature_atoms",), trace["rounds"][strict]["signature_atoms"] - 1
        )
    elif kind == "member_count":
        bad = replaced(a, path + ("member_comparisons",), 0)
    elif kind == "omitted_witness":
        bad = replaced(a, path + ("separations",), [])
    elif kind == "extra_witness":
        bad = replaced(a, path + ("separations",), trace["rounds"][strict]["separations"] * 2)
    elif kind == "wrong_witness_target":
        bad = replaced(a, path + ("separations", 0, "target_class"), -1)
    else:
        bad = replaced(
            a,
            path + ("separations", 0, "right_multiplicity"),
            trace["rounds"][strict]["separations"][0]["right_multiplicity"] + 1,
        )
    assert wire(bad) != wire(a)
    with pytest.raises(ValueError):
        runner.check_analysis(bad, suite["problem"]["model"])


@pytest.mark.parametrize(
    "path,value",
    [
        (("features", 0, "chain_counts", 0), True),
        (("features", 0, "pair_graded", 0, 0, 0, 0), 2),
        (("comparison", "same_terminal_memberships"), 1),
        (("comparison", "same_memberships_as_H"), None),
        (("comparison", "maps", "H_to_L"), None),
        (("comparison", "maps", "L_to_C", 0), False),
        (("comparison", "aligned_full_refines_local", 0), False),
        (("minimality", "H_used_in_construction"), True),
        (("minimality", "strict_round_bound"), 7),
        (("minimality", "arbitrary_partitions_enumerated"), True),
        (("terminal", "class_profiles", 0, "transitions", 0, "multiplicity"), True),
        (("terminal", "reconstruction", "certificate", "base_cells"), 0),
        (("terminal", "reconstruction", "certificate", "recurrence_cells"), 0),
        (("terminal", "reconstruction", "operator_checks", "verified"), 1),
        (("terminal", "closure", "member_comparisons"), 0),
        (("terminal", "comparison", "max_abs_residual"), 1),
        (("fine_deletions", "choices"), 0),
    ],
)
def test_root_rejects_false_maps_claims_terminal_reconstruction_and_native_evidence(
    aggregate, path, value
):
    runner, suite = aggregate
    if path == ("comparison", "same_memberships_as_H"):
        value = not suite["analysis"]["comparison"]["same_memberships_as_H"]
    bad = replaced(suite["analysis"], path, value)
    assert wire(bad) != wire(suite["analysis"])
    with pytest.raises(ValueError):
        runner.check_analysis(bad, suite["problem"]["model"])


def test_same_cardinality_fiber_substitution_cannot_forge_terminal_membership(aggregate):
    runner, suite = aggregate
    a = suite["analysis"]
    classes = a["local_refinement"]["classes"]
    left, right = next(
        (left, right)
        for left, right in combinations(classes, 2)
        if len(left["members"]) > 1
        and len(right["members"]) > 1
        and min(left["members"][-1], right["members"][-1])
        > max(left["members"][0], right["members"][0])
    )
    lsid, rsid = left["members"][-1], right["members"][-1]
    bad = replaced(
        a,
        ("local_refinement", "classes", left["class_id"], "members"),
        sorted(left["members"][:-1] + [rsid]),
    )
    bad = replaced(
        bad,
        ("local_refinement", "classes", right["class_id"], "members"),
        sorted(right["members"][:-1] + [lsid]),
    )
    bad = replaced(bad, ("local_refinement", "state_classes", lsid), right["class_id"])
    bad = replaced(bad, ("local_refinement", "state_classes", rsid), left["class_id"])
    assert [len(row["members"]) for row in bad["local_refinement"]["classes"]] == [
        len(row["members"]) for row in classes
    ]
    assert [row["members"][0] for row in bad["local_refinement"]["classes"]] == [
        row["members"][0] for row in classes
    ]
    assert sorted(
        sid for row in bad["local_refinement"]["classes"] for sid in row["members"]
    ) == list(range(4447))
    with pytest.raises(ValueError):
        runner.check_analysis(bad, suite["problem"]["model"])


@pytest.mark.parametrize("kind", ["state_subclass", "key_subclass", "state_bool", "semantic"])
def test_cache_revalidates_native_raw_model_before_canonical_content_lookup(
    aggregate, micro_analysis, kind
):
    runner, _ = aggregate
    model = micro_problem()["model"]
    expected = runner.check_analysis(micro_analysis, model)
    if kind == "state_subclass":
        model["states"][0]["state_id"] = IntSubclass(0)
    elif kind == "key_subclass":
        model[StrSubclass("states")] = model.pop("states")
    elif kind == "state_bool":
        model["states"][0]["state_id"] = False
    else:
        model["states"][1]["past"][2] = [1]
    with pytest.raises(ValueError):
        runner.check_analysis(micro_analysis, model)
    assert runner.check_analysis(micro_analysis, micro_problem()["model"]) == expected


def identity_constructor(raw):
    return {
        "schema_version": "det8-qr05s-local-v1",
        "classes": [
            {
                "class_id": row["state_id"],
                "frame_id": row["frame_id"],
                "parent_color_sizes": list(row["parent_color_sizes"]),
                **{
                    color: [
                        {"target_class": edge["target_state"], "multiplicity": edge["multiplicity"]}
                        for edge in row[color]
                    ]
                    for color in ("odd", "even")
                },
            }
            for row in raw
        ],
    }


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_guards_dags_ownership_and_synthetic_controls_in_bounded_subprocess(
    tmp_path, optimized
):
    fixtures = {
        "micro": micro_problem(),
        "local": local_problem(),
        "constructor": simple_constructor(),
        "full": full_from_words(synthetic("two_rounds")[0]),
        "fractional": identity_constructor(nonrealizable_local("fractional")),
        "mixed": identity_constructor(nonrealizable_local("mixed")),
    }
    program = r"""
import copy, importlib.util, json, resource, sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (12, 12))
base, fixtures = Path(sys.argv[1]), json.loads(sys.argv[2])
checks = 0
def require(condition, message):
    if not condition: raise RuntimeError(message)
def reject(call, value):
    global checks
    try: call(value)
    except ValueError: checks += 1
    else: raise RuntimeError("malformed input accepted with assertions disabled")
def load(name, file):
    spec = importlib.util.spec_from_file_location(name, base / file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
def dag():
    value = []
    for _ in range(40): value = [value, value]
    return value
def mutable_ids(value):
    result, stack = set(), [value]
    while stack:
        item = stack.pop()
        if type(item) not in (dict, list) or id(item) in result: continue
        result.add(id(item)); stack.extend(item.values() if type(item) is dict else item)
    return result
class I(int): pass
class S(str): pass
class L(list): pass
class D(dict): pass
for index, filename in enumerate(("local_refinement.py", "reference_qr05t.py")):
    module = load("_qr05t_guard_" + str(index), filename)
    local = module.refine_local(fixtures["local"])
    full = module._refine_full(fixtures["full"], fixtures["local"]["state_classes"])
    require(local["strict_rounds"] == 2 and full["strict_rounds"] == 1, "different-speed control")
    require(local["state_classes"] == full["state_classes"], "synthetic terminal equality")
    reject(module.reconstruct_profiles, fixtures["fractional"])
    reject(module.reconstruct_profiles, fixtures["mixed"])
    for method, source in (("analyze", fixtures["micro"]), ("refine_local", fixtures["local"]), ("reconstruct_profiles", fixtures["constructor"])):
        call = getattr(module, method)
        first, second = call(source), call(source)
        require(mutable_ids(source).isdisjoint(mutable_ids(first)), "input/output alias")
        require(mutable_ids(first).isdisjoint(mutable_ids(second)), "cross-call alias")
        for kind in ("dict", "key", "string", "integer", "boolean", "list", "tuple", "float", "cycle", "deep", "dag"):
            bad = copy.deepcopy(source)
            if kind == "dict": bad = D(bad)
            elif kind == "key": bad[S("schema_version")] = bad.pop("schema_version")
            elif kind == "string": bad["schema_version"] = S(bad["schema_version"])
            elif kind in ("integer", "boolean"):
                wrong = I(0) if kind == "integer" else False
                if method == "analyze": bad["model"]["states"][0]["state_id"] = wrong
                elif method == "refine_local": bad["state_classes"][0] = wrong
                else: bad["classes"][0]["class_id"] = wrong
            elif kind == "list": bad["extra"] = L()
            elif kind == "tuple": bad["extra"] = ()
            elif kind == "float": bad["extra"] = 0.0
            elif kind == "cycle":
                value = []; value.append(value); bad["extra"] = value
            elif kind == "deep":
                value = []
                for _ in range(1500): value = [value]
                bad["extra"] = value
            else: bad["extra"] = dag()
            reject(call, bad)
        limit = "WORKING_CAP" if index == 0 else "_MAX_WORK"
        saved = getattr(module, limit)
        setattr(module, limit, 32)
        try: reject(call, source)
        finally: setattr(module, limit, saved)
    for field in ("frames", "states"):
        bad = copy.deepcopy(fixtures["micro"])
        bad["model"][field] = [dag()]
        reject(module.analyze, bad)
    for field in ("rows", "state_classes"):
        bad = copy.deepcopy(fixtures["local"])
        bad[field] = [dag()]
        reject(module.refine_local, bad)
    bad = copy.deepcopy(fixtures["full"])
    bad[0]["transitions"][0]["target_state"] = False
    reject(lambda value: module._refine_full(value, fixtures["local"]["state_classes"]), bad)
    bad = copy.deepcopy(fixtures["full"])
    bad[0]["transitions"].pop(0)
    reject(lambda value: module._refine_full(value, fixtures["local"]["state_classes"]), bad)
    empty = []
    shared = {"schema_version": "det8-qr05t-local-v1", "state_classes": [0], "rows": [{"state_id": 0, "frame_id": 0, "parent_color_sizes": [0, 0], "odd": empty, "even": empty}]}
    require(module.refine_local(shared)["strict_rounds"] == 0, "shared valid containers")
runner = load("_qr05t_guard_runner", "study.py")
reject(runner.require_wire, {"extra": dag()})
reject(lambda value: runner.require_same_wire({"zero": 0}, value, "typed"), {"zero": False})
print("explicit bounded rejection checks:", checks)
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE), json.dumps(fixtures)])
    result = subprocess.run(arguments, text=True, capture_output=True, timeout=20, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "explicit bounded rejection checks: 90"
