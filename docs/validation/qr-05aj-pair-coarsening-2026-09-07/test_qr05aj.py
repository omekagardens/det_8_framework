"""Bounded independent checks for the private pair-coarsening diagnostic.

Only tests marked fixed consume authenticated AI cases. Collection and generic
hands use explicit synthetic data, never fixed fixture calculations.
"""

from __future__ import annotations

import builtins
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from fractions import Fraction as F
from itertools import combinations, pairwise
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
FAMILIES = ("grid", "warp", "warp_stale", "boost", "dilate")


def fw(value):
    value = F(value)
    return [value.numerator, value.denominator]


def fraction(value):
    assert type(value) is list and len(value) == 2
    n, d = value
    assert type(n) is int and type(d) is int and d > 0
    answer = F(n, d)
    assert [answer.numerator, answer.denominator] == value
    assert max(abs(n).bit_length(), d.bit_length()) <= 4096
    return answer


def native(value):
    if value is None or type(value) in (bool, int, str):
        if type(value) is int:
            assert abs(value).bit_length() <= 4096
        return
    if type(value) is list:
        for child in value:
            native(child)
        return
    if type(value) is dict:
        assert all(type(k) is str for k in value)
        for child in value.values():
            native(child)
        return
    raise AssertionError(f"non-native mathematical type {type(value)}")


def wire(value):
    native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode()


def digest(value):
    return hashlib.sha256(wire(value)).hexdigest()


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def engines():
    return (
        load("_qr05aj_test_primary", "kernel.py"),
        load("_qr05aj_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05aj_test_runner", "study.py")


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


def rect(values):
    return list(map(fw, values))


def area(bounds):
    a, b, c, d = bounds
    return max(F(), b - a) * max(F(), d - c) / 2


def clipped(bounds, query):
    a, b, c, d = bounds
    u, v, x, y = query
    return max(a, u), min(b, v), max(c, x), min(d, y)


def directed_integral(a, b, c, d):
    assert a <= b and c <= d
    points = sorted({a, b, c, d})
    result = F()
    for left, right in pairwise(points):
        if a <= left < right <= b:
            heights = [max(F(), d - max(c, x)) for x in (left, right)]
            result += (right - left) * sum(heights, F()) / 2
    return result


LINKS = ((0, 1), (1, 2), (0, 2))


def problem_of(annotated=False):
    def c(event, bounds, mark=None):
        return {
            "event": event,
            "bounds": rect(bounds),
            "supplied_mark": fw(area(bounds) if mark is None else mark),
        }

    return {
        "family": "synthetic",
        "probes": [
            {"name": "whole", "bounds": rect((0, 1, 0, 1))},
            {"name": "partial", "bounds": rect((0, F(3, 8), 0, F(3, 4)))},
            {"name": "small", "bounds": rect((0, F(1, 8), 0, F(1, 4)))},
        ],
        "levels": [
            {"level": "coarse", "cells": [c(-2, (0, F(1, 2), 0, 1)), c(9, (F(1, 2), 1, 0, 1))]},
            {
                "level": "middle",
                "cells": [
                    c(1, (F(1, 2), 1, 0, 1)),
                    c(3, (0, F(1, 4), 0, 1)),
                    c(9, (F(1, 4), F(1, 2), 0, 1)),
                ],
            },
            {
                "level": "fine",
                "cells": [
                    c(-2, (F(1, 4), F(1, 2), 0, 1), 3 if annotated else None),
                    c(3, (0, F(1, 4), F(1, 2), 1), 2 if annotated else None),
                    c(8, (F(1, 2), 1, 0, 1), 5 if annotated else None),
                    c(9, (0, F(1, 4), 0, F(1, 2)), 1 if annotated else None),
                ],
            },
        ],
    }


def contained(inner, outer):
    a, b, c, d = inner
    x, y, z, t = outer
    return x <= a < b <= y and z <= c < d <= t


def partition_of(parent, children):
    assert all(contained(c, parent) for c in children)
    us = sorted({parent[0], parent[1], *(x for c in children for x in c[:2])})
    vs = sorted({parent[2], parent[3], *(x for c in children for x in c[2:])})
    for a, b in pairwise(us):
        for c, d in pairwise(vs):
            u, v = (a + b) / 2, (c + d) / 2
            if parent[0] < u < parent[1] and parent[2] < v < parent[3]:
                assert sum(x < u < y and z < v < t for x, y, z, t in children) == 1


def fraction_or_none(numerator, denominator):
    return fw(numerator / denominator) if denominator else None


def independent_family(problem):
    rawlevels = problem["levels"]
    cells = [level["cells"] for level in rawlevels]
    boxes = [{c["event"]: tuple(map(fraction, c["bounds"])) for c in level} for level in cells]
    volumes = [{event: area(b) for event, b in level.items()} for level in boxes]
    assert all(
        area(clipped(a, b)) == 0 for level in boxes for a, b in combinations(level.values(), 2)
    )
    maps = {}
    for coarse, fine in LINKS:
        mapping = {}
        for child, bounds in boxes[fine].items():
            parents = [
                parent for parent, outer in boxes[coarse].items() if contained(bounds, outer)
            ]
            assert len(parents) == 1
            mapping[child] = parents[0]
        for parent, bounds in boxes[coarse].items():
            partition_of(
                bounds, [boxes[fine][child] for child in mapping if mapping[child] == parent]
            )
        maps[coarse, fine] = mapping
    assert all(maps[0, 2][child] == maps[0, 1][maps[1, 2][child]] for child in boxes[2])
    levels = []
    internal = []
    for li, raw in enumerate(rawlevels):
        geometry = []
        data = []
        for probe in problem["probes"]:
            query = tuple(map(fraction, probe["bounds"]))
            clips = {event: clipped(bounds, query) for event, bounds in boxes[li].items()}
            hs = {event: area(bounds) for event, bounds in clips.items()}
            assert sum(hs.values(), F()) == area(query)
            js = {}
            for first, a in clips.items():
                for second, b in clips.items():
                    js[first, second] = (
                        directed_integral(a[0], a[1], b[0], b[1])
                        * directed_integral(a[2], a[3], b[2], b[3])
                        / 4
                        if hs[first] and hs[second]
                        else F()
                    )
            assert sum(js.values(), F()) == area(query) ** 2 / 4
            for event, h in hs.items():
                assert js[event, event] == h * h / 4
            geometry.append(
                {
                    "probe": probe["name"],
                    "volume": fw(area(query)),
                    "cells": [{"event": event, "clipped_volume": fw(h)} for event, h in hs.items()],
                    "pairs": [
                        {
                            "first": a,
                            "second": b,
                            "clipped_product": fw(hs[a] * hs[b]),
                            "causal_integral": fw(value),
                            "conditional": fraction_or_none(value, hs[a] * hs[b]),
                        }
                        for (a, b), value in js.items()
                    ],
                }
            )
            data.append((hs, js))
        levels.append({"level": raw["level"], "geometry": geometry})
        internal.append(data)
    coarsenings = []
    for coarse, fine in LINKS:
        mapping = maps[coarse, fine]
        children = {
            parent: [child for child in boxes[fine] if mapping[child] == parent]
            for parent in boxes[coarse]
        }
        geometry = []
        for qi, probe in enumerate(problem["probes"]):
            hc, jc = internal[coarse][qi]
            hf, jf = internal[fine][qi]
            weights = {
                c["event"]: fraction(c["supplied_mark"])
                * hf[c["event"]]
                / volumes[fine][c["event"]]
                for c in cells[fine]
            }
            blockrows = []
            for a, aa in children.items():
                for b, bb in children.items():
                    denominator = hc[a] * hc[b]
                    annotation_den = sum((weights[x] * weights[y] for x in aa for y in bb), F())
                    rawsum = sum((jf[x, y] for x in aa for y in bb), F())
                    diagonal = sum((jf[x, y] for x in aa for y in bb if x == y), F())
                    assert rawsum == jc[a, b]
                    defined = [(x, y) for x in aa for y in bb if hf[x] * hf[y] > 0]
                    conditional = rawsum / denominator if denominator else None
                    weighted = (
                        sum(
                            (
                                (hf[x] * hf[y] / denominator) * (jf[x, y] / (hf[x] * hf[y]))
                                for x, y in defined
                            ),
                            F(),
                        )
                        if denominator
                        else None
                    )
                    unweighted = (
                        sum((jf[x, y] / (hf[x] * hf[y]) for x, y in defined), F()) / len(defined)
                        if defined
                        else None
                    )
                    annotation = (
                        sum(
                            (
                                (weights[x] * weights[y] / annotation_den)
                                * (jf[x, y] / (hf[x] * hf[y]))
                                for x, y in defined
                            ),
                            F(),
                        )
                        if annotation_den
                        else None
                    )
                    assert weighted == conditional
                    via_integral = via_conditional = None
                    if (coarse, fine) == (0, 2):
                        ma = [m for m in boxes[1] if maps[0, 1][m] == a]
                        mb = [m for m in boxes[1] if maps[0, 1][m] == b]
                        descendants = {
                            m: [c for c in boxes[2] if maps[1, 2][c] == m] for m in boxes[1]
                        }
                        hm = {m: sum((hf[c] for c in descendants[m]), F()) for m in boxes[1]}
                        jmiddle = {
                            (x, y): sum(
                                (jf[i, j] for i in descendants[x] for j in descendants[y]), F()
                            )
                            for x in ma
                            for y in mb
                        }
                        via_integral = sum(jmiddle.values(), F())
                        den_middle = sum((hm[x] for x in ma), F()) * sum((hm[y] for y in mb), F())
                        via_conditional = (
                            sum(
                                (
                                    (hm[x] * hm[y] / den_middle) * (value / (hm[x] * hm[y]))
                                    for (x, y), value in jmiddle.items()
                                    if hm[x] * hm[y] > 0
                                ),
                                F(),
                            )
                            if den_middle
                            else None
                        )
                        assert via_integral == rawsum and via_conditional == conditional
                    blockrows.append(
                        {
                            "first": a,
                            "second": b,
                            "children": [
                                {
                                    "first": x,
                                    "second": y,
                                    "geometric_weight": fraction_or_none(
                                        hf[x] * hf[y], denominator
                                    ),
                                    "annotation_weight": fraction_or_none(
                                        weights[x] * weights[y], annotation_den
                                    ),
                                }
                                for x in aa
                                for y in bb
                            ],
                            "coarse_integral": fw(jc[a, b]),
                            "child_integral_sum": fw(rawsum),
                            "child_diagonal_integral": fw(diagonal),
                            "child_offdiagonal_integral": fw(rawsum - diagonal),
                            "coarse_conditional": fw(conditional)
                            if conditional is not None
                            else None,
                            "weighted_child_conditional": fw(weighted)
                            if weighted is not None
                            else None,
                            "unweighted_child_conditional": fw(unweighted)
                            if unweighted is not None
                            else None,
                            "annotation_weighted_child_conditional": fw(annotation)
                            if annotation is not None
                            else None,
                            "via_middle_integral": fw(via_integral)
                            if via_integral is not None
                            else None,
                            "via_middle_conditional": fw(via_conditional)
                            if via_conditional is not None
                            else None,
                        }
                    )
            for parent, cs in children.items():
                assert hc[parent] == sum((hf[c] for c in cs), F())
            geometry.append(
                {
                    "probe": probe["name"],
                    "volumes": [
                        {
                            "parent": parent,
                            "coarse_volume": fw(hc[parent]),
                            "child_volume_sum": fw(sum((hf[c] for c in cs), F())),
                        }
                        for parent, cs in children.items()
                    ],
                    "blocks": blockrows,
                }
            )
        coarsenings.append(
            {
                "coarse": rawlevels[coarse]["level"],
                "fine": rawlevels[fine]["level"],
                "parents": [{"parent": p, "children": cs} for p, cs in children.items()],
                "geometry": geometry,
            }
        )
    lp = [pair for level in levels for q in level["geometry"] for pair in q["pairs"]]
    blocks = [b for link in coarsenings for q in link["geometry"] for b in q["blocks"]]
    counts = {
        "levels": len(levels),
        "probes": len(problem["probes"]),
        "level_pairs": len(lp),
        "blocks": len(blocks),
        "child_terms": sum(len(b["children"]) for b in blocks),
        "undefined_level_pairs": sum(p["conditional"] is None for p in lp),
        "undefined_blocks": sum(b["coarse_conditional"] is None for b in blocks),
        "unweighted_mismatches": sum(
            b["unweighted_child_conditional"] != b["coarse_conditional"] for b in blocks
        ),
        "annotation_mismatches": sum(
            b["annotation_weighted_child_conditional"] != b["coarse_conditional"] for b in blocks
        ),
        "diagonal_omission_mismatches": sum(
            b["child_offdiagonal_integral"] != b["coarse_integral"] for b in blocks
        ),
        "cross_child_omission_mismatches": sum(
            b["child_diagonal_integral"] != b["coarse_integral"] for b in blocks
        ),
    }
    return {
        "problem": copy.deepcopy(problem),
        "levels": levels,
        "coarsenings": coarsenings,
        "counts": counts,
    }


@pytest.mark.parametrize("annotated", [False, True])
def test_generic_complete_family_has_full_blocks_actual_weights_and_direct_middle_equality(
    engines, annotated
):
    p = problem_of(annotated)
    expected = independent_family(p)
    assert (
        expected["counts"]["undefined_blocks"] > 0
        and expected["counts"]["unweighted_mismatches"] > 0
    )
    assert (
        expected["counts"]["diagonal_omission_mismatches"] > 0
        and expected["counts"]["cross_child_omission_mismatches"] > 0
    )
    assert (expected["counts"]["annotation_mismatches"] > 0) == annotated
    for module in engines:
        before = wire(p)
        assert wire(module.build_family(p)) == wire(expected) and wire(p) == before


def test_parent_diagonal_keeps_cross_child_terms_and_zero_products_stay_explicit(engines):
    p = problem_of()
    expected = independent_family(p)
    whole = expected["coarsenings"][0]["geometry"][0]["blocks"][0]
    assert whole["first"] == whole["second"] == -2
    assert whole["coarse_integral"] == [1, 64]
    assert whole["child_diagonal_integral"] == whole["child_offdiagonal_integral"] == [1, 128]
    small = expected["coarsenings"][2]["geometry"][2]["blocks"]
    positive = small[0]
    assert positive["coarse_conditional"] == [1, 4]
    assert any(c["geometric_weight"] == [0, 1] for c in positive["children"])
    assert any(c["geometric_weight"] == [1, 1] for c in positive["children"])
    undefined = small[-1]
    for key in (
        "coarse_conditional",
        "weighted_child_conditional",
        "unweighted_child_conditional",
        "annotation_weighted_child_conditional",
        "via_middle_conditional",
    ):
        assert undefined[key] is None
    assert (
        undefined["coarse_integral"]
        == undefined["child_integral_sum"]
        == undefined["via_middle_integral"]
        == [0, 1]
    )
    assert all(
        c["geometric_weight"] is None and c["annotation_weight"] is None
        for c in undefined["children"]
    )
    # Event9 is a right parent at level0, but the lower-left child at level2.
    assert expected["coarsenings"][2]["parents"][0]["children"] == [-2, 3, 9]
    for module in engines:
        assert wire(module.build_family(p)) == wire(expected)


def test_nonadditive_positive_marks_change_only_annotation_candidate_not_geometry(engines):
    a, b = problem_of(False), problem_of(True)
    assert sum((fraction(c["supplied_mark"]) for c in b["levels"][2]["cells"]), F()) != sum(
        (fraction(c["supplied_mark"]) for c in b["levels"][0]["cells"]), F()
    )
    for module in engines:
        left, right = module.build_family(a), module.build_family(b)
        assert wire(left["levels"]) == wire(right["levels"])
        for l, r in zip(left["coarsenings"], right["coarsenings"], strict=True):
            for q, t in zip(l["geometry"], r["geometry"], strict=True):
                for x, y in zip(q["blocks"], t["blocks"], strict=True):
                    assert x["coarse_integral"] == y["coarse_integral"]
                    assert x["weighted_child_conditional"] == y["weighted_child_conditional"]
        assert right["counts"]["annotation_mismatches"] > 0


@pytest.mark.parametrize(
    "bounds",
    [
        (0, 1, 0, 1),
        (0, 2, 1, 3),
        (1, 3, 0, 2),
        (-2, 0, -1, 1),
        (0, 1, 1, 2),
        (1, 2, 0, 1),
        (0, 0, 0, 1),
        (0, 1, 1, 1),
    ],
)
def test_directed_integral_hands_preserve_direction_and_boundary_measure(engines, bounds):
    a, b, c, d = map(F, bounds)
    expected = directed_integral(a, b, c, d)
    for module in engines:
        assert module.causal_area(a, b, c, d) == expected
        assert module.causal_area(c, d, a, b) + expected == (b - a) * (d - c)
        assert module.causal_area(2 * a - 5, 2 * b - 5, 2 * c - 5, 2 * d - 5) == 4 * expected


def expected_composition():
    h = F(1, 2)
    # Integral_0^1 u(1-u)du from exact polynomial coefficients.
    one_dimensional = sum((c / F(i + 1) for i, c in enumerate((0, 1, -1))), F())
    shared = one_dimensional**2
    pair = F(1, 4)
    j = h * h * pair
    return {
        "h": fw(h),
        "pair_fraction": fw(pair),
        "squared_pair_fraction": fw(pair * pair),
        "shared_middle_fraction": fw(shared),
        "pair_measure": fw(j),
        "block_product_measure": fw(j * j / h),
        "shared_middle_measure": fw(h**3 * shared),
        "signed_product_error": fw(j * j / h - h**3 * shared),
    }


def test_composition_boundary_uses_one_shared_middle_point_not_matrix_powers(runner):
    expected = expected_composition()
    assert expected["shared_middle_fraction"] == [1, 36] and expected["squared_pair_fraction"] == [
        1,
        16,
    ]
    assert expected["signed_product_error"] == [5, 1152] and expected["pair_fraction"] != [1, 1]
    assert wire(runner.composition_witness()) == wire(expected)


def malformed_problem(kind):
    p = problem_of()
    if kind == "extra":
        p["geometry_answers"] = []
    elif kind == "level_count":
        p["levels"].pop()
    elif kind == "duplicate_level":
        p["levels"][1]["level"] = p["levels"][0]["level"]
    elif kind == "duplicate_id":
        p["levels"][0]["cells"][1]["event"] = -2
    elif kind == "bool_id":
        p["levels"][0]["cells"][0]["event"] = False
    elif kind == "unsorted_id":
        p["levels"][2]["cells"].reverse()
    elif kind == "zero_mark":
        p["levels"][2]["cells"][0]["supplied_mark"] = [0, 1]
    elif kind == "unreduced":
        p["levels"][2]["cells"][0]["supplied_mark"] = [2, 4]
    elif kind == "outside_query":
        p["probes"][0]["bounds"] = rect((0, 2, 0, 1))
    elif kind == "degenerate":
        p["levels"][2]["cells"][0]["bounds"] = rect((0, 0, 0, 1))
    elif kind == "overlap_hole":
        p["levels"][0]["cells"][0]["bounds"] = rect((0, F(3, 4), 0, 1))
        p["levels"][0]["cells"][1]["bounds"] = rect((F(1, 2), F(3, 4), 0, 1))
    elif kind == "nonnested":
        for c, bounds in zip(
            p["levels"][1]["cells"],
            ((F(3, 5), 1, 0, 1), (0, F(2, 5), 0, 1), (F(2, 5), F(3, 5), 0, 1)),
            strict=True,
        ):
            c["bounds"] = rect(bounds)
    elif kind == "hidden_hole":
        p["probes"] = p["probes"][-1:]
        p["levels"][2]["cells"][2]["bounds"] = rect((F(1, 2), F(9, 10), 0, 1))
    else:
        raise AssertionError(kind)
    return p


@pytest.mark.parametrize(
    "kind",
    [
        "extra",
        "level_count",
        "duplicate_level",
        "duplicate_id",
        "bool_id",
        "unsorted_id",
        "zero_mark",
        "unreduced",
        "outside_query",
        "degenerate",
        "overlap_hole",
        "nonnested",
        "hidden_hole",
    ],
)
def test_malformed_geometry_and_full_lineage_fail_explicitly(engines, kind):
    p = malformed_problem(kind)
    for module in engines:
        with pytest.raises(ValueError):
            module.build_family(p)


def test_family_reads_no_hidden_artifacts_and_outputs_are_detached(engines, monkeypatch):
    p = problem_of(True)
    before = wire(p)
    expected = wire(independent_family(p))

    def forbidden(*args, **kwargs):
        raise RuntimeError("mathematical engine read hidden artifact")

    with monkeypatch.context() as patch:
        for host, name in (
            (builtins, "open"),
            (os, "open"),
            (Path, "open"),
            (Path, "read_bytes"),
            (Path, "read_text"),
        ):
            patch.setattr(host, name, forbidden)
        for module in engines:
            a, b = module.build_family(p), module.build_family(p)
            assert wire(a) == wire(b) == expected and wire(p) == before
            a["problem"]["levels"][0]["cells"][0]["supplied_mark"][0] = -1
            a["levels"][0]["geometry"][0]["pairs"][0]["causal_integral"][0] = -1
            assert (
                wire(p) == before
                and wire(b) == expected
                and wire(module.build_family(p)) == expected
            )


@pytest.fixture
def lifecycle(runner, tmp_path, monkeypatch):
    identity = {
        "source_ledger": {"source": {"bytes": 1, "sha256": "fixed"}},
        "prior_artifacts": {"prior": {"bytes": 1, "sha256": "fixed"}},
        "ancestor_sources": {"ancestor": {"bytes": 1, "sha256": "fixed"}},
    }
    monkeypatch.setattr(runner, "identities", lambda: copy.deepcopy(identity))
    monkeypatch.setattr(runner, "run_suite", lambda route="compare": {"totals": {"stub": 1}})
    monkeypatch.setattr(runner.platform, "platform", lambda: "lifecycle-test-platform")
    monkeypatch.setattr(sys, "flags", SimpleNamespace(isolated=1, optimize=0))
    monkeypatch.setattr(sys, "pycache_prefix", str(tmp_path / "external-cache"))
    return runner, tmp_path / "capture.json"


def test_capture_create_only_and_both_readonly_routes_preserve_runtime(lifecycle):
    runner, path = lifecycle
    created = runner.capture(path)
    before = path.read_bytes()
    assert created["status"] == "CREATED_EXACT_FINITE_RESULT"
    with pytest.raises(FileExistsError):
        runner.capture(path)
    for route in ("primary", "reference"):
        replay = runner.capture(path, route=route, verify=True)
        assert replay["status"] == "VERIFIED_EXACT_REPLAY" and replay["sha256"] == created["sha256"]
        assert path.read_bytes() == before


@pytest.mark.parametrize(
    "field", ["schema_version", "source_ledger", "prior_artifacts", "ancestor_sources", "suite"]
)
def test_capture_replay_rejects_changed_evidence_without_overwriting(lifecycle, field):
    runner, path = lifecycle
    runner.capture(path)
    envelope = json.loads(path.read_bytes())
    envelope[field] = "changed"
    raw = runner.canonical(envelope)
    path.write_bytes(raw)
    with pytest.raises(ValueError):
        runner.capture(path, verify=True)
    assert path.read_bytes() == raw


@pytest.mark.parametrize("kind", ["extra", "noncanonical", "wrong_type"])
def test_capture_requires_known_canonical_envelope(lifecycle, kind):
    runner, path = lifecycle
    runner.capture(path)
    raw = path.read_bytes()
    if kind == "noncanonical":
        changed = b" " + raw
    elif kind == "extra":
        changed = runner.canonical({**json.loads(raw), "extra": 0})
    else:
        changed = runner.canonical([])
    path.write_bytes(changed)
    with pytest.raises(ValueError):
        runner.capture(path, verify=True)
    assert path.read_bytes() == changed


@pytest.mark.parametrize("verify", [False, True])
def test_capture_never_follows_result_symlink(lifecycle, verify):
    runner, path = lifecycle
    target = path.with_name("untouched.json")
    target.write_bytes(b"original")
    path.symlink_to(target)
    with pytest.raises(ValueError if verify else FileExistsError):
        runner.capture(path, verify=verify)
    assert target.read_bytes() == b"original"


def test_capture_identity_change_midrun_prevents_write(lifecycle, monkeypatch):
    runner, path = lifecycle

    def changed(route="compare"):
        monkeypatch.setattr(runner, "identities", lambda: {"changed": True})
        return {"totals": {"stub": 1}}

    monkeypatch.setattr(runner, "run_suite", changed)
    with pytest.raises(ValueError):
        runner.capture(path)
    assert not path.exists()


def test_capture_replay_detects_concurrent_artifact_change(lifecycle, monkeypatch):
    runner, path = lifecycle
    runner.capture(path)

    def changed(route="compare"):
        path.write_bytes(b"concurrent")
        return {"totals": {"stub": 1}}

    monkeypatch.setattr(runner, "run_suite", changed)
    with pytest.raises(ValueError):
        runner.capture(path, verify=True)
    assert path.read_bytes() == b"concurrent"


@pytest.mark.parametrize("kind", ["not_isolated", "no_cache", "root_cache", "checkout_cache"])
def test_capture_runtime_boundary(lifecycle, monkeypatch, kind):
    runner, path = lifecycle
    if kind == "not_isolated":
        monkeypatch.setattr(sys, "flags", SimpleNamespace(isolated=0, optimize=0))
    elif kind == "no_cache":
        monkeypatch.setattr(sys, "pycache_prefix", None)
    elif kind == "root_cache":
        monkeypatch.setattr(sys, "pycache_prefix", runner.ROOT.anchor)
    else:
        monkeypatch.setattr(sys, "pycache_prefix", str(runner.ROOT / "local-cache"))
    with pytest.raises(ValueError):
        runner.capture(path)
    assert not path.exists()


@pytest.mark.parametrize("verify", [False, True])
def test_capture_size_caps_are_live_without_overwrite(lifecycle, monkeypatch, verify):
    runner, path = lifecycle
    if verify:
        runner.capture(path)
        before = path.read_bytes()
    monkeypatch.setattr(runner, "MAX_CAPTURE_BYTES", 2)
    with pytest.raises(ValueError):
        runner.capture(path, verify=verify)
    if verify:
        assert path.read_bytes() == before
    else:
        assert not path.exists()


def test_working_suite_byte_cap_prevents_capture(lifecycle, monkeypatch):
    runner, path = lifecycle
    monkeypatch.setattr(runner, "MAX_WORKING_BYTES", 2)
    with pytest.raises(ValueError):
        runner.capture(path)
    assert not path.exists()


@pytest.mark.parametrize(
    "value",
    [
        {"totals": (1,)},
        {"totals": {"value": F(1, 2)}},
        {"totals": {"value": 1.0}},
        {"totals": {"value": 1 << 4096}},
    ],
)
def test_mathematical_suite_requires_native_bounded_integer_components(
    lifecycle, monkeypatch, value
):
    runner, path = lifecycle
    monkeypatch.setattr(runner, "run_suite", lambda route="compare": value)
    with pytest.raises(ValueError):
        runner.capture(path)
    assert not path.exists()


def test_readonly_mathematical_comparison_distinguishes_bool_from_integer(runner):
    with pytest.raises(ValueError):
        runner.verify_suite({"value": True}, {"value": 1})


@pytest.mark.parametrize("optimized", [False, True])
def test_bounded_explicit_guards_survive_optimization(tmp_path, optimized):
    # Explicit conditions, rather than assert statements, remain active under -O.
    program = r"""
import importlib.util, json, pathlib, sys
p = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("aj_guard_tests", p / "test_qr05aj.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
kinds = ("extra", "level_count", "duplicate_level", "duplicate_id", "bool_id",
         "unsorted_id", "zero_mark", "unreduced", "outside_query", "degenerate",
         "overlap_hole", "nonnested", "hidden_hole")
count = 0
def reject(fn, *args):
    global count
    try:
        fn(*args)
    except ValueError:
        count += 1
    else:
        raise RuntimeError("invalid input accepted")
for name, filename in (("primary", "kernel.py"), ("reference", "reference.py")):
    m = t.load("aj_guard_" + name, filename)
    for kind in kinds:
        reject(m.build_family, t.malformed_problem(kind))
    for args in ((True,1,0,1), (0.0,1,0,1), (1,0,0,1), (0,1,1,0), ("0",1,0,1)):
        reject(m.causal_area, *args)
    p = t.problem_of(True)
    before = t.wire(p)
    expected = t.wire(t.independent_family(p))
    first, second = m.build_family(p), m.build_family(p)
    if t.wire(first) != expected or t.wire(second) != expected or t.wire(p) != before:
        raise RuntimeError("generic complete wire or input changed")
    first["problem"]["levels"][0]["cells"][0]["supplied_mark"][0] = -1
    if t.wire(second) != expected or t.wire(p) != before:
        raise RuntimeError("output alias leaked")
if count != 36:
    raise RuntimeError("guard inventory changed")
print(json.dumps({"rejections": count, "engines": 2}))
"""
    args = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'cache'}"]
    if optimized:
        args.append("-O")
    result = subprocess.run(
        [*args, "-c", program, str(HERE)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    assert json.loads(result.stdout) == {"rejections": 36, "engines": 2}


def independent_inputs(cases):
    by = {case["case_id"]: case for case in cases}
    assert len(by) == len(cases) == 27
    problems, consumed = [], []
    for name in FAMILIES:
        levels, queries = [], []
        for level in ("l0", "l1", "l2"):
            case = by[f"{name}__{level}__identity"]
            assert case["design"]["name"] == "identity" and case["level"] == level
            source = case["source"]
            assert source["name"] == name
            current = []
            for probe in source["probes"]:
                start, end = [source["coordinates"][probe[key]] for key in ("source", "target")]
                current.append(
                    {
                        "name": probe["name"],
                        "bounds": copy.deepcopy([start[0], end[0], start[1], end[1]]),
                    }
                )
            queries.append(current)
            levels.append(
                {
                    "level": level,
                    "cells": [
                        {
                            key: copy.deepcopy(cell[key])
                            for key in ("event", "bounds", "supplied_mark")
                        }
                        for cell in source["cells"]
                    ],
                }
            )
            assert source["eligible"] == [cell["event"] for cell in levels[-1]["cells"]]
            consumed.append(case)
        assert wire(queries[0]) == wire(queries[1]) == wire(queries[2])
        problems.append({"family": name, "probes": queries[0], "levels": levels})
    return problems, consumed


@pytest.fixture(scope="session")
def fixed_inputs(runner):
    # This fixture is lazy and used exclusively by tests marked fixed.
    path = HERE.parent / "qr-05ai-weighted-kernels-2026-09-07/results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 14980342
    assert (
        hashlib.sha256(raw).hexdigest()
        == "17dbb103c56b6489d5aef75f4eda77108fea12bfc475fc65ffcfd82710bf6786"
    )
    old = json.loads(raw)["suite"]["cases"]
    problems, consumed = independent_inputs(old)
    actual_problems, actual_consumed = runner.load_inputs()
    assert wire(problems) == wire(actual_problems) and wire(consumed) == wire(actual_consumed)
    return problems, consumed


@pytest.fixture(scope="session")
def expected_families(fixed_inputs):
    return [independent_family(p) for p in fixed_inputs[0]]


@pytest.fixture(scope="session")
def actual_families(fixed_inputs, engines):
    outputs = []
    for problem in fixed_inputs[0]:
        pair = []
        for module in engines:
            supplied = copy.deepcopy(problem)
            before = wire(supplied)
            pair.append(module.build_family(supplied))
            assert wire(supplied) == before
        outputs.append(pair)
    return outputs


@pytest.mark.fixed
@pytest.mark.parametrize("index", range(5), ids=FAMILIES)
def test_fixed_all_five_complete_engine_wires(actual_families, expected_families, index):
    expected = wire(expected_families[index])
    assert all(wire(actual) == expected for actual in actual_families[index])


def geometry_projection(family, scale=F(1), annotations=True):
    volume_keys = {"volume", "clipped_volume", "coarse_volume", "child_volume_sum"}
    pair_keys = {
        "clipped_product",
        "causal_integral",
        "coarse_integral",
        "child_integral_sum",
        "child_diagonal_integral",
        "child_offdiagonal_integral",
        "via_middle_integral",
    }
    excluded = {
        "annotation_weight",
        "annotation_weighted_child_conditional",
        "annotation_mismatches",
    }

    def visit(value, key=None):
        if value is None:
            return None
        if key in volume_keys | pair_keys:
            return fw(fraction(value) * scale ** (2 if key in pair_keys else 1))
        if type(value) is dict:
            return {k: visit(v, k) for k, v in value.items() if annotations or k not in excluded}
        if type(value) is list:
            return [visit(v) for v in value]
        return value

    return visit({k: family[k] for k in ("levels", "coarsenings", "counts")})


def independent_controls(families):
    by = {family["problem"]["family"]: family for family in families}
    assert wire(geometry_projection(by["boost"])) == wire(geometry_projection(by["grid"]))
    assert wire(geometry_projection(by["dilate"])) == wire(geometry_projection(by["grid"], F(4)))
    assert wire(geometry_projection(by["warp_stale"], annotations=False)) == wire(
        geometry_projection(by["warp"], annotations=False)
    )
    return {"boost": True, "dilation": True, "stale_geometric": True}


def independent_bridges(families, consumed):
    ids = []
    for family in families:
        for li, level in enumerate(family["levels"]):
            old = consumed[len(ids)]
            source = old["source"]
            expected_id = family["problem"]["family"] + "__" + level["level"] + "__identity"
            assert old["case_id"] == expected_id
            ids.append(expected_id)
            assert wire(family["problem"]["levels"][li]["cells"]) == wire(
                [
                    {key: c[key] for key in ("event", "bounds", "supplied_mark")}
                    for c in source["cells"]
                ]
            )
            assert len(level["geometry"]) == len(old["geometry"])
            for now, previous in zip(level["geometry"], old["geometry"], strict=True):
                assert now["probe"] == previous["probe"] and now["volume"] == previous["volume"]
                assert wire(now["cells"]) == wire(
                    [
                        {"event": c["event"], "clipped_volume": c["volume"]}
                        for c in previous["cell_clips"]
                    ]
                )
                pairs = []
                for pair in previous["pair_cells"]:
                    product = fraction(pair["clipped_product"])
                    pairs.append(
                        {
                            **{
                                k: pair[k]
                                for k in ("first", "second", "clipped_product", "causal_integral")
                            },
                            "conditional": fraction_or_none(
                                fraction(pair["causal_integral"]), product
                            ),
                        }
                    )
                assert wire(now["pairs"]) == wire(pairs)
    return {
        "AI_identity_case_ids": ids,
        "AI_projected_inputs_equal": True,
        "AI_complete_clipped_volumes_and_pairs_equal": True,
        "AI_sampling_math_replayed": False,
        "other_prior_math_replayed": False,
    }


@pytest.fixture(scope="session")
def expected_suite(expected_families, fixed_inputs):
    totals = {"families": len(expected_families)}
    totals.update(
        {
            key: sum(f["counts"][key] for f in expected_families)
            for key in expected_families[0]["counts"]
        }
    )
    return {
        "families": expected_families,
        "controls": independent_controls(expected_families),
        "prior_bridges": independent_bridges(expected_families, fixed_inputs[1]),
        "composition_witness": expected_composition(),
        "totals": totals,
        "scope": dict.fromkeys(
            (
                "generic_production_API_hardened",
                "unknown_geometry_reconstructed",
                "marks_authenticated",
                "continuum_limit_established",
                "cross_level_observation_transport_proved",
                "higher_chain_composition_closed",
                "stochastic_transition_constructed",
                "quantum_channel_constructed",
                "gravity_derived",
                "empirical_data_used",
                "ret_integration_tested",
            ),
            False,
        ),
    }


@pytest.mark.fixed
def test_fixed_complete_suite_and_all_fifteen_AI_geometry_projections(
    runner, actual_families, expected_suite, fixed_inputs
):
    actual = runner.assemble_suite([pair[0] for pair in actual_families], fixed_inputs[1])
    assert wire(actual) == wire(expected_suite)
    runner.verify_suite(actual, expected_suite)


@pytest.mark.fixed
@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_route_orchestration_selects_only_declared_engines(
    runner, fixed_inputs, expected_suite, monkeypatch, route
):
    # Five real complete engine pairs are tested separately; cached oracle values
    # isolate orchestration here, without another execution of the mathematics.
    calls = []
    by = {f["problem"]["family"]: f for f in expected_suite["families"]}

    def loader(name):
        def build(problem):
            target = by[problem["family"]]
            assert wire(problem) == wire(target["problem"])
            calls.append((name, problem["family"]))
            return copy.deepcopy(target)

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    monkeypatch.setattr(runner, "load_inputs", lambda: fixed_inputs)
    assert wire(runner.run_suite(route)) == wire(expected_suite)
    names = ("primary", "reference") if route == "compare" else (route,)
    assert calls == [(name, family) for family in FAMILIES for name in names]


def at_path(tree, path):
    for key in path:
        tree = tree[key]
    return tree


def add_fraction(tree, path):
    return replaced(tree, path, fw(fraction(at_path(tree, path)) + 1))


@pytest.mark.fixed
def test_fixed_nonvacuous_complete_family_corruptions(runner, expected_families):
    original = expected_families[0]
    g = ("levels", 0, "geometry", 0)
    block = ("coarsenings", 2, "geometry", 0, "blocks", 0)
    pair = at_path(original, (*g, "pairs", 1))
    undefined = next(
        ("levels", li, "geometry", qi, "pairs", pi, "conditional")
        for li, level in enumerate(original["levels"])
        for qi, query in enumerate(level["geometry"])
        for pi, row in enumerate(query["pairs"])
        if row["conditional"] is None
    )
    changes = [
        add_fraction(original, ("problem", "levels", 0, "cells", 0, "bounds", 0)),
        add_fraction(original, ("problem", "levels", 2, "cells", 0, "supplied_mark")),
        add_fraction(original, (*g, "volume")),
        add_fraction(original, (*g, "cells", 0, "clipped_volume")),
        add_fraction(original, (*g, "pairs", 0, "causal_integral")),
        replaced(
            original, (*g, "pairs", 1), {**pair, "first": pair["second"], "second": pair["first"]}
        ),
        replaced(original, undefined, [0, 1]),
        replaced(original, ("coarsenings", 2, "parents", 0, "children"), []),
        replaced(original, (*block, "children"), at_path(original, (*block, "children"))[:-1]),
        add_fraction(original, (*block, "children", 0, "geometric_weight")),
        add_fraction(original, (*block, "children", 0, "annotation_weight")),
        add_fraction(original, (*block, "child_integral_sum")),
        add_fraction(original, (*block, "child_diagonal_integral")),
        add_fraction(original, (*block, "child_offdiagonal_integral")),
        add_fraction(original, (*block, "weighted_child_conditional")),
        add_fraction(original, (*block, "unweighted_child_conditional")),
        add_fraction(original, (*block, "annotation_weighted_child_conditional")),
        add_fraction(original, (*block, "via_middle_integral")),
        add_fraction(original, (*block, "via_middle_conditional")),
        replaced(original, ("counts", "child_terms"), original["counts"]["child_terms"] + 1),
    ]
    assert len(changes) == 20
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.verify_suite(bad, original)
    assert wire(original) == before


@pytest.mark.fixed
def test_fixed_nonvacuous_suite_claim_and_aggregate_corruptions(runner, expected_suite):
    original = expected_suite
    changes = [
        replaced(original, ("controls", "boost"), False),
        replaced(original, ("controls", "dilation"), False),
        replaced(original, ("controls", "stale_geometric"), False),
        replaced(original, ("prior_bridges", "AI_sampling_math_replayed"), True),
        add_fraction(original, ("composition_witness", "shared_middle_measure")),
        replaced(original, ("scope", "higher_chain_composition_closed"), True),
        replaced(original, ("totals", "blocks"), original["totals"]["blocks"] + 1),
        replaced(original, ("prior_bridges", "AI_identity_case_ids"), []),
    ]
    assert len(changes) == 8
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.verify_suite(bad, original)
    assert wire(original) == before


@pytest.mark.fixed
def test_fixed_consumed_AI_pair_projection_corruptions_are_not_merely_flagged(
    runner, expected_families, fixed_inputs
):
    original = fixed_inputs[1][0]
    pair = original["geometry"][0]["pair_cells"][1]
    changes = [
        add_fraction(original, ("geometry", 0, "volume")),
        add_fraction(original, ("geometry", 0, "cell_clips", 0, "volume")),
        add_fraction(original, ("geometry", 0, "pair_cells", 0, "clipped_product")),
        add_fraction(original, ("geometry", 0, "pair_cells", 0, "causal_integral")),
        replaced(
            original,
            ("geometry", 0, "pair_cells", 1),
            {**pair, "first": pair["second"], "second": pair["first"]},
        ),
        replaced(
            original, ("geometry", 0, "pair_cells"), original["geometry"][0]["pair_cells"][:-1]
        ),
    ]
    assert len(changes) == 6
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.ai_bridges(expected_families, [bad, *fixed_inputs[1][1:]])
    assert wire(original) == before
