"""Independent retained-order observer and exact local sampling diagnostics.

Generic controls do not load any producer artifacts. Fixed tests are separately
named and consume pinned JSON only after the coordinated release.
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
from itertools import pairwise
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent


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


def fraction(value):
    assert type(value) is list and len(value) == 2
    n, d = value
    assert type(n) is int and type(d) is int and d > 0
    result = F(n, d)
    assert [result.numerator, result.denominator] == value
    assert max(abs(result.numerator).bit_length(), result.denominator.bit_length()) <= 4096
    return result


def fw(value):
    value = F(value)
    return [value.numerator, value.denominator]


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("private test module name already in use")
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("required module unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


CAPS = (
    "MAX_BITS",
    "MAX_DEPTH",
    "MAX_NODES",
    "MAX_BYTES",
    "MAX_LEVELS",
    "MAX_CELLS",
    "MAX_PROBES",
    "MAX_TILE_CHECKS",
    "MAX_PAIR_CHECKS",
    "MAX_QUERY_CELL_TERMS",
    "MAX_TOTAL_WORK",
)
HOOKS = ("_partition", "_refinement", "_questions")
SCOPE = dict.fromkeys(
    (
        "observer_has_geometry",
        "marks_authenticated",
        "unknown_geometry_reconstructed",
        "monotone_absolute_error_guaranteed",
        "continuum_limit_established",
        "gravity_derived",
    ),
    False,
)
METHODS = ("raw", "uniform_rate", "inclusion")


def rect(values):
    return list(map(fw, values))


def cell(name, bounds, representative, volume, parent=None):
    return {
        "name": name,
        "parent": parent,
        "bounds": rect(bounds),
        "representative": rect(representative),
        "volume": fw(volume),
    }


def problem_of():
    return {
        "schema_version": "det8-qr05ah-problem-v1",
        "family": "qr05ah_partition_bounds",
        "domain": rect((0, 1, 0, 1)),
        "probes": [{"name": "q", "bounds": rect((0, F(1, 5), 0, 1))}],
        "levels": [
            {"name": "a", "cells": [cell("c", (0, 1, 0, 1), (F(3, 4), F(1, 2)), F(1, 2))]},
            {
                "name": "b",
                "cells": [
                    cell("c_l", (0, F(1, 2), 0, 1), (F(1, 10), F(1, 2)), F(1, 4), "c"),
                    cell("c_r", (F(1, 2), 1, 0, 1), (F(3, 4), F(1, 2)), F(1, 4), "c"),
                ],
            },
        ],
    }


def fixed_internal_problem():
    return problem_of()


def rectangle(bounds):
    return tuple(map(fraction, bounds))


def area(bounds):
    a, b, c, d = bounds
    return (b - a) * (d - c) / 2


def contained(inner, outer):
    a, b, c, d = inner
    x, y, z, t = outer
    return x <= a < b <= y and z <= c < d <= t


def clip_area(left, right):
    a, b, c, d = left
    x, y, z, t = right
    return max(F(), min(b, y) - max(a, x)) * max(F(), min(d, t) - max(c, z)) / 2


def arrangement_partition(domain, rectangles):
    us = sorted({domain[0], domain[1], *(x for r in rectangles for x in r[:2])})
    vs = sorted({domain[2], domain[3], *(x for r in rectangles for x in r[2:])})
    assert all(contained(r, domain) for r in rectangles)
    total = F()
    for a, b in pairwise(us):
        for c, d in pairwise(vs):
            u, v = (a + b) / 2, (c + d) / 2
            if domain[0] < u < domain[1] and domain[2] < v < domain[3]:
                assert sum(x < u < y and z < v < t for x, y, z, t in rectangles) == 1
                total += (b - a) * (d - c) / 2
    assert total == area(domain)


def independent_analysis(p):
    domain = rectangle(p["domain"])
    questions = [(q["name"], rectangle(q["bounds"])) for q in p["probes"]]
    levels = []
    for level in p["levels"]:
        cells = level["cells"]
        bounds = {c["name"]: rectangle(c["bounds"]) for c in cells}
        weights = {c["name"]: fraction(c["volume"]) for c in cells}
        points = {c["name"]: tuple(map(fraction, c["representative"])) for c in cells}
        geometry = {name: area(b) for name, b in bounds.items()}
        arrangement_partition(domain, list(bounds.values()))
        rows = []
        for name, q in questions:
            inner = [n for n, b in bounds.items() if contained(b, q)]
            outer = [n for n, b in bounds.items() if clip_area(b, q) > 0]
            representative = [
                n for n, (u, v) in points.items() if q[0] < u < q[1] and q[2] < v < q[3]
            ]
            lower, upper, g = (
                sum((geometry[n] for n in names), F()) for names in (inner, outer, representative)
            )
            t = sum((weights[n] for n in representative), F())
            v = area(q)
            assert lower <= g <= upper and lower <= v <= upper
            assert g - upper <= g - v <= g - lower and abs(g - v) <= upper - lower
            rows.append(
                {
                    "probe": name,
                    "inner_cells": inner,
                    "outer_cells": outer,
                    "representative_cells": representative,
                    "lower_bound": fw(lower),
                    "upper_bound": fw(upper),
                    "boundary_gap": fw(upper - lower),
                    "geometric_target": fw(g),
                    "supplied_target": fw(t),
                    "continuum_volume": fw(v),
                    "annotation_error": fw(t - g),
                    "quadrature_error": fw(g - v),
                    "total_error": fw(t - v),
                    "error_lower": fw(g - upper),
                    "error_upper": fw(g - lower),
                }
            )
        levels.append(
            {
                "name": level["name"],
                "cells": [
                    {
                        "name": c["name"],
                        "geometric_volume": fw(geometry[c["name"]]),
                        "annotation_error": fw(weights[c["name"]] - geometry[c["name"]]),
                    }
                    for c in cells
                ],
                "questions": rows,
            }
        )
    refinements = []
    for i, (coarse, fine) in enumerate(pairwise(p["levels"])):
        parents = []
        for parent in coarse["cells"]:
            children = [c for c in fine["cells"] if c["parent"] == parent["name"]]
            assert children
            arrangement_partition(
                rectangle(parent["bounds"]), [rectangle(c["bounds"]) for c in children]
            )
            total = sum((fraction(c["volume"]) for c in children), F())
            assert total == fraction(parent["volume"])
            parents.append(
                {
                    "parent": parent["name"],
                    "children": [c["name"] for c in children],
                    "geometric_volume": fw(area(rectangle(parent["bounds"]))),
                    "supplied_volume": fw(total),
                }
            )
        rows = []
        for cq, fq in zip(levels[i]["questions"], levels[i + 1]["questions"], strict=True):
            names = ("lower_bound", "upper_bound", "boundary_gap", "quadrature_error")
            l, u, g, e = (fraction(fq[n]) - fraction(cq[n]) for n in names)
            assert l >= 0 and u <= 0 and g <= 0
            rows.append(
                {
                    "probe": cq["probe"],
                    "lower_gain": fw(l),
                    "upper_drop": fw(-u),
                    "gap_drop": fw(-g),
                    "quadrature_error_change": fw(e),
                    "absolute_error_change": fw(
                        abs(fraction(fq["quadrature_error"]))
                        - abs(fraction(cq["quadrature_error"]))
                    ),
                }
            )
        refinements.append(
            {"coarse": coarse["name"], "fine": fine["name"], "parents": parents, "questions": rows}
        )
    sizes = [len(level["cells"]) for level in p["levels"]]
    tile = sum(c * (2 * c + 1) ** 2 for c in sizes)
    pairs = sum(c * (c - 1) // 2 for c in sizes)
    terms = len(p["probes"]) * sum(sizes)
    links = sum(sizes[1:])
    return {
        "input_sha256": digest(p),
        "domain_volume": fw(area(domain)),
        "levels": levels,
        "refinements": refinements,
        "counts": {
            "levels": len(sizes),
            "cells": sum(sizes),
            "probes": len(p["probes"]),
            "tile_checks": tile,
            "pair_checks": pairs,
            "query_cell_terms": terms,
            "refinement_links": links,
            "total_work": tile + pairs + 3 * terms + links,
        },
        "scope": dict(SCOPE),
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05ah_test_primary", "certificate.py"),
        private_module("_qr05ah_test_reference", "reference_qr05ah.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return private_module("_qr05ah_test_runner", "study.py")


def test_explicit_nonmonotone_counterexample_complete_wire_and_signed_error(executors):
    p = problem_of()
    expected = independent_analysis(p)
    a, b = (level["questions"][0] for level in expected["levels"])
    assert a["lower_bound"] == b["lower_bound"] == [0, 1]
    assert a["upper_bound"] == [1, 2] and b["upper_bound"] == [1, 4]
    assert a["quadrature_error"] == [-1, 10] and b["quadrature_error"] == [3, 20]
    assert expected["refinements"][0]["questions"][0]["absolute_error_change"] == [1, 20]
    for module in executors:
        before = wire(p)
        assert wire(module.certify(p)) == wire(expected) and wire(p) == before


def test_equal_probe_rectangles_are_allowed_but_zero_area_touch_is_not_outer(executors):
    p = problem_of()
    p["probes"] = [
        {"name": "whole", "bounds": p["domain"]},
        {"name": "left", "bounds": rect((0, F(1, 2), 0, 1))},
        {"name": "left_again", "bounds": rect((0, F(1, 2), 0, 1))},
    ]
    expected = independent_analysis(p)
    fine = expected["levels"][1]["questions"]
    assert (
        fine[1]["inner_cells"]
        == fine[1]["outer_cells"]
        == fine[1]["representative_cells"]
        == ["c_l"]
    )
    assert (
        fine[1]["lower_bound"]
        == fine[1]["upper_bound"]
        == fine[1]["geometric_target"]
        == fine[1]["continuum_volume"]
    )
    assert {k: v for k, v in fine[1].items() if k != "probe"} == {
        k: v for k, v in fine[2].items() if k != "probe"
    }
    for module in executors:
        assert wire(module.certify(p)) == wire(expected)


@pytest.mark.parametrize("scale", [F(1, 100), F(10)])
def test_additive_stale_annotations_may_lie_outside_geometric_enclosure(executors, scale):
    p = problem_of()
    p["probes"] = [{"name": "whole", "bounds": p["domain"]}]
    for level in p["levels"]:
        for c in level["cells"]:
            c["volume"] = fw(fraction(c["volume"]) * scale)
    expected = independent_analysis(p)
    for level in expected["levels"]:
        q = level["questions"][0]
        t, l, u = map(fraction, (q["supplied_target"], q["lower_bound"], q["upper_bound"]))
        assert t < l or t > u
    for module in executors:
        assert wire(module.certify(p)) == wire(expected)
        assert module.certify(p)["scope"] == SCOPE


def test_single_child_may_rename_and_move_representative_inside_unchanged_geometry(executors):
    p = problem_of()
    renamed = copy.deepcopy(p["levels"][0]["cells"][0])
    renamed.update(name="renamed", parent="c", representative=rect((F(1, 10), F(1, 2))))
    p["levels"][1]["cells"] = [renamed]
    expected = independent_analysis(p)
    assert expected["refinements"][0]["parents"][0]["children"] == ["renamed"]
    assert (
        expected["levels"][0]["questions"][0]["geometric_target"]
        != expected["levels"][1]["questions"][0]["geometric_target"]
    )
    for module in executors:
        assert wire(module.certify(p)) == wire(expected)


def test_signed_coordinates_translation_and_anisotropic_scale_are_native_geometry(executors):
    p = problem_of()

    def transformed_pair(values):
        u, v = map(fraction, values)
        return rect((2 * u - 3, v / 2 - 2))

    def transformed_bounds(values):
        a, b, c, d = rectangle(values)
        return rect((2 * a - 3, 2 * b - 3, c / 2 - 2, d / 2 - 2))

    q = copy.deepcopy(p)
    q["domain"] = transformed_bounds(q["domain"])
    for probe in q["probes"]:
        probe["bounds"] = transformed_bounds(probe["bounds"])
    for level in q["levels"]:
        for c in level["cells"]:
            c["bounds"] = transformed_bounds(c["bounds"])
            c["representative"] = transformed_pair(c["representative"])
    a, b = independent_analysis(p), independent_analysis(q)
    assert {k: v for k, v in a.items() if k != "input_sha256"} == {
        k: v for k, v in b.items() if k != "input_sha256"
    }
    for module in executors:
        assert wire(module.certify(q)) == wire(b)


def test_large_internal_area_product_can_cancel_but_retained_domain_area_overflow_rejects(
    executors,
):
    p = problem_of()
    size = F(1 << 2048)
    p["domain"] = rect((0, size, 0, size))
    p["probes"] = [{"name": "whole", "bounds": p["domain"]}]
    p["levels"] = [
        {"name": "large", "cells": [cell("c", (0, size, 0, size), (size / 2, size / 2), F(1))]}
    ]
    expected = independent_analysis(p)
    assert expected["domain_volume"] == [1 << 4095, 1]
    for module in executors:
        assert wire(module.certify(p)) == wire(expected)
        bad = copy.deepcopy(p)
        bad["domain"][1] = fw(2 * size)
        bad["probes"][0]["bounds"] = copy.deepcopy(bad["domain"])
        bad["levels"][0]["cells"][0]["bounds"] = copy.deepcopy(bad["domain"])
        with pytest.raises(ValueError):
            module.certify(bad)


def test_certifier_reads_no_artifacts_and_does_not_authenticate_supplied_marks(
    executors, monkeypatch
):
    p = problem_of()
    expected = wire(independent_analysis(p))

    def forbidden(*args, **kwargs):
        raise RuntimeError("certificate tried to read external geometry")

    with monkeypatch.context() as patch:
        for host, name in (
            (builtins, "open"),
            (os, "open"),
            (Path, "open"),
            (Path, "read_bytes"),
            (Path, "read_text"),
        ):
            patch.setattr(host, name, forbidden)
        for module in executors:
            assert wire(module.certify(p)) == expected


class IntChild(int):
    pass


class StrChild(str):
    pass


class ListChild(list):
    pass


class DictChild(dict):
    pass


def partition_counter(kind):
    p = problem_of()
    left, right = p["levels"][1]["cells"]
    if kind == "equal_area_overlap_hole":
        left["bounds"] = rect((0, F(3, 4), 0, 1))
        right["bounds"] = rect((F(1, 2), F(3, 4), 0, 1))
        right["representative"] = rect((F(5, 8), F(1, 2)))
    elif kind == "hole":
        left["bounds"] = rect((0, F(2, 5), 0, 1))
    elif kind == "overlap":
        left["bounds"] = rect((0, F(3, 5), 0, 1))
    elif kind == "nonadditive":
        left["volume"] = fw(F(1, 3))
    elif kind == "false_parent":
        p["levels"][0]["cells"] = copy.deepcopy(p["levels"][1]["cells"])
        for c in p["levels"][0]["cells"]:
            c["parent"] = None
        left["parent"], right["parent"] = "c_r", "c_l"
    else:
        raise AssertionError(kind)
    return p


def invalid_problems():
    p = problem_of()
    bad = [None, [], (), DictChild(p), {**p, 1: 0}]
    bad += [
        {**p, key: []}
        for key in ("extra", "coordinates", "source", "unknown_marks", "estimator", "metric_fit")
    ]
    bad += [{k: v for k, v in p.items() if k != key} for key in p]
    for key in ("schema_version", "family"):
        bad += [replaced(p, (key,), v) for v in (None, True, StrChild(p[key]), "wrong")]
    for path in (("domain",), ("probes", 0, "bounds"), ("levels", 1, "cells", 1, "bounds")):
        old = p
        for key in path:
            old = old[key]
        bad += [
            replaced(p, path, v)
            for v in (
                None,
                tuple(old),
                ListChild(old),
                [],
                old[:-1],
                old + old[:1],
                rect((1, 0, 0, 1)),
                rect((0, 0, 0, 1)),
                rect((0, 1, 1, 0)),
            )
        ]
    for path in (
        ("domain", 0),
        ("levels", 1, "cells", 1, "volume"),
        ("levels", 1, "cells", 1, "representative", 0),
    ):
        bad += [
            replaced(p, path, v)
            for v in (
                None,
                (),
                ListChild([0, 1]),
                [],
                [1],
                [0, 1, 2],
                [False, 1],
                [0, True],
                [IntChild(0), 1],
                [0, IntChild(1)],
                [0.0, 1],
                [0, 1.0],
                ["0", 1],
                [0, 0],
                [0, -1],
                [0, 2],
                [2, 4],
                [1, 1 << 4096],
                [1 << 4096, 1],
            )
        ]
    for path in (("probes",), ("levels",), ("levels", 1, "cells")):
        old = p
        for key in path:
            old = old[key]
        bad += [replaced(p, path, v) for v in (None, tuple(old), ListChild(old), [], old * 2)]
    bad += [
        replaced(p, ("levels",), [p["levels"][0]] * 5),
        replaced(p, ("levels", 1, "cells"), p["levels"][1]["cells"][::-1]),
    ]
    for path in (("probes", 0), ("levels", 1), ("levels", 1, "cells", 1)):
        old = p
        for key in path:
            old = old[key]
        bad += [replaced(p, path, v) for v in (None, [], DictChild(old), {**old, "extra": 0})]
        bad += [replaced(p, path, {k: v for k, v in old.items() if k != key}) for key in old]
    for path in (("probes", 0, "name"), ("levels", 1, "name"), ("levels", 1, "cells", 1, "name")):
        bad += [
            replaced(p, path, v)
            for v in (None, True, StrChild("name"), "", "A", "9a", "a-b", "a b", "é", "a" * 41)
        ]
    bad += [
        replaced(p, ("levels", 1, "name"), "a"),
        replaced(p, ("levels", 1, "cells", 1, "name"), "c_l"),
    ]
    for v in (None, False, 0, StrChild("c"), "", "unknown", "c_l"):
        bad.append(replaced(p, ("levels", 1, "cells", 1, "parent"), v))
    bad += [replaced(p, ("levels", 0, "cells", 0, "parent"), v) for v in ("c", False, 0)]
    for v in (
        None,
        (),
        ListChild([[1, 2], [1, 2]]),
        [],
        [[1, 2]],
        [[1, 2]] * 3,
        rect((F(1, 2), F(1, 2))),
        rect((1, F(1, 2))),
    ):
        bad.append(replaced(p, ("levels", 1, "cells", 1, "representative"), v))
    bad += [replaced(p, ("levels", 1, "cells", 1, "volume"), v) for v in ([0, 1], [-1, 1])]
    bad += [
        replaced(p, ("probes", 0, "bounds"), rect((-1, F(1, 5), 0, 1))),
        replaced(p, ("levels", 1, "cells", 1, "bounds"), rect((F(1, 2), 2, 0, 1))),
        replaced(p, ("levels", 1, "cells"), [p["levels"][1]["cells"][0]]),
    ]
    bad += [
        partition_counter(kind)
        for kind in ("equal_area_overlap_hole", "hole", "overlap", "nonadditive", "false_parent")
    ]
    return bad


@pytest.mark.parametrize("index", range(len(invalid_problems())))
def test_invalid_native_geometry_partition_and_lineage_are_not_repaired(executors, index):
    for module in executors:
        with pytest.raises(ValueError):
            module.certify(invalid_problems()[index])


def planned_caps(p):
    sizes = [len(l["cells"]) for l in p["levels"]]
    t = sum(c * (2 * c + 1) ** 2 for c in sizes)
    d = sum(c * (c - 1) // 2 for c in sizes)
    q = len(p["probes"]) * sum(sizes)
    r = sum(sizes[1:])
    return {
        "MAX_LEVELS": len(sizes),
        "MAX_CELLS": max(sizes),
        "MAX_PROBES": len(p["probes"]),
        "MAX_TILE_CHECKS": t,
        "MAX_PAIR_CHECKS": d,
        "MAX_QUERY_CELL_TERMS": q,
        "MAX_TOTAL_WORK": t + d + 3 * q + r,
    }


def test_all_reservations_late_schema_and_validated_partitions_precede_questions(
    executors, monkeypatch
):
    p = problem_of()
    for module in executors:
        calls = dict.fromkeys(HOOKS, 0)
        with monkeypatch.context() as patch:
            for name in HOOKS:
                original = getattr(module, name)

                def counted(*args, _name=name, _original=original, _calls=calls):
                    _calls[_name] += 1
                    return _original(*args)

                patch.setattr(module, name, counted)
            assert wire(module.certify(p)) == wire(independent_analysis(p))
        assert calls == {"_partition": 2, "_refinement": 1, "_questions": 2}

        def forbidden(*args):
            raise RuntimeError("hook executed before complete admission")

        for constant, limit in planned_caps(p).items():
            with monkeypatch.context() as patch:
                patch.setattr(module, constant, limit - 1)
                for name in HOOKS:
                    patch.setattr(module, name, forbidden)
                with pytest.raises(ValueError):
                    module.certify(p)
        for bad in (
            replaced(p, ("levels", 1, "cells", 1, "volume"), [0, 1]),
            replaced(p, ("levels", 1, "cells", 1, "parent"), "unknown"),
            replaced(p, ("levels", 1, "cells", 1, "representative"), rect((1, F(1, 2)))),
        ):
            with monkeypatch.context() as patch:
                for name in HOOKS:
                    patch.setattr(module, name, forbidden)
                with pytest.raises(ValueError):
                    module.certify(bad)
        for kind in ("equal_area_overlap_hole", "hole", "overlap", "nonadditive", "false_parent"):
            bad = partition_counter(kind)
            if kind == "equal_area_overlap_hole":
                assert sum(
                    (area(rectangle(c["bounds"])) for c in bad["levels"][1]["cells"]), F()
                ) == area(rectangle(bad["domain"]))
            with monkeypatch.context() as patch:
                patch.setattr(module, "_questions", forbidden)
                with pytest.raises(ValueError):
                    module.certify(bad)


@pytest.mark.parametrize("constant", CAPS)
def test_live_caps_restore_and_do_not_reuse_cached_admission(executors, monkeypatch, constant):
    p = problem_of()
    p["probes"].append({"name": "whole", "bounds": p["domain"]})
    for module in executors:
        with monkeypatch.context() as patch:
            patch.setattr(module, constant, 0)
            with pytest.raises(ValueError):
                module.certify(p)
        assert wire(module.certify(p)) == wire(independent_analysis(p))


def maximal_problem():
    cells = [
        cell(f"c{i}", (F(i, 8), F(i + 1, 8), 0, 1), (F(2 * i + 1, 16), F(1, 2)), F(1, 16))
        for i in range(8)
    ]
    levels = [{"name": "l0", "cells": cells}]
    for i in range(1, 4):
        next_cells = [{**copy.deepcopy(c), "parent": c["name"]} for c in cells]
        levels.append({"name": f"l{i}", "cells": next_cells})
    return {
        "schema_version": "det8-qr05ah-problem-v1",
        "family": "qr05ah_partition_bounds",
        "domain": rect((0, 1, 0, 1)),
        "probes": [{"name": f"q{i}", "bounds": rect((0, 1, 0, 1))} for i in range(8)],
        "levels": levels,
    }


def test_exact_maximum_levels_cells_probes_and_all_structural_work_counts(executors):
    p = maximal_problem()
    expected = independent_analysis(p)
    assert expected["counts"] == {
        "levels": 4,
        "cells": 32,
        "probes": 8,
        "tile_checks": 9248,
        "pair_checks": 112,
        "query_cell_terms": 256,
        "refinement_links": 24,
        "total_work": 10152,
    }
    for module in executors:
        assert wire(module.certify(p)) == wire(expected)


def mutable_ids(value):
    if type(value) not in (dict, list):
        return set()
    answer = {id(value)}
    for child in value.values() if type(value) is dict else value:
        answer |= mutable_ids(child)
    return answer


def nested(value, wrappers):
    for _ in range(wrappers):
        value = [value]
    return value


def tree_resources(value, depth=0):
    nodes, maximum = 1, depth
    if type(value) in (dict, list):
        for child in value.values() if type(value) is dict else value:
            count, height = tree_resources(child, depth + 1)
            nodes += count
            maximum = max(maximum, height)
    return nodes, maximum


def shared_problem():
    p = problem_of()
    p["levels"][0]["cells"][0]["bounds"] = p["domain"]
    p["probes"].append({"name": "whole", "bounds": p["domain"]})
    return p


def graph_inputs(p):
    cycle = []
    cycle.append(cycle)
    cycle_dict = {}
    cycle_dict["cycle"] = cycle_dict
    dag = []
    for _ in range(40):
        dag = [dag, dag]
    for value in (cycle, cycle_dict, nested([], 1500), dag):
        yield {**p, "extra": value}
    for path in (
        ("domain",),
        ("domain", 0),
        ("probes",),
        ("probes", 0),
        ("probes", 0, "bounds"),
        ("levels",),
        ("levels", 1),
        ("levels", 1, "cells"),
        ("levels", 1, "cells", 1),
        ("levels", 1, "cells", 1, "bounds"),
        ("levels", 1, "cells", 1, "representative"),
        ("levels", 1, "cells", 1, "representative", 0),
        ("levels", 1, "cells", 1, "volume"),
        ("levels", 1, "cells", 1, "parent"),
    ):
        yield replaced(p, path, dag)


def test_native_scalar_empty_shared_depth_exact_ASCII_node_and_output_boundaries(
    executors, monkeypatch
):
    value = {'"\\\b\f\n\r\t\x00\x1f é 🐈 \ud800': ["é", "🐈", "\udfff", -123, False, None]}
    for module in executors:
        for x in (nested(0, 64), nested([], 64)):
            module._native(x)
        for x in (nested(0, 65), nested([], 65)):
            with pytest.raises(ValueError):
                module._native(x)
        shared = [0]
        module._native([shared, nested(shared, 62)])
        with pytest.raises(ValueError):
            module._native([shared, nested(shared, 63)])
        for constant, limit in (
            ("MAX_NODES", 8),
            ("MAX_DEPTH", 2),
            ("MAX_BYTES", len(wire(value))),
        ):
            with monkeypatch.context() as patch:
                patch.setattr(module, constant, limit)
                module._native(value)
                patch.setattr(module, constant, limit - 1)
                with pytest.raises(ValueError):
                    module._native(value)
        p = shared_problem()
        nodes, depth = tree_resources(p)
        for constant, limit in (
            ("MAX_NODES", nodes - 1),
            ("MAX_DEPTH", depth - 1),
            ("MAX_BYTES", len(wire(p)) - 1),
        ):

            def forbidden(*args, **kwargs):
                raise RuntimeError("unsafe tree serialized")

            with monkeypatch.context() as patch:
                patch.setattr(module, constant, limit)
                patch.setattr(json, "dumps", forbidden)
                with pytest.raises(ValueError):
                    module.certify(p)
        expected = wire(module.certify(p))
        assert len(expected) > len(wire(p))
        with monkeypatch.context() as patch:
            patch.setattr(module, "MAX_BYTES", len(expected) - 1)
            with pytest.raises(ValueError):
                module.certify(p)
            patch.setattr(module, "MAX_BYTES", len(expected))
            assert wire(module.certify(p)) == expected


def test_certificate_outputs_are_detached_across_input_levels_and_calls(executors):
    p = shared_problem()
    before = wire(p)
    for module in executors:
        a, b = module.certify(p), module.certify(p)
        expected = wire(b)
        assert not (mutable_ids(a) & (mutable_ids(p) | mutable_ids(b)))
        a["domain_volume"][0] = 10
        a["levels"][0]["questions"][0]["supplied_target"][0] = -1
        assert wire(p) == before and wire(b) == expected
        assert wire(module.certify(p)) == expected
        changed = copy.deepcopy(p)
        detached = module.certify(changed)
        changed["levels"][0]["cells"][0]["representative"] = rect((F(1, 10), F(1, 2)))
        assert wire(detached) == expected and wire(module.certify(changed)) != expected


def wide_cancellation_problem():
    b = F(1 << 4095)
    bounds = (-b, b, 0, 3 / b)
    return {
        "schema_version": "det8-qr05ah-problem-v1",
        "family": "qr05ah_partition_bounds",
        "domain": rect(bounds),
        "probes": [{"name": "whole", "bounds": rect(bounds)}],
        "levels": [{"name": "wide", "cells": [cell("c", bounds, (0, 1 / b), 3)]}],
    }


def test_4097_bit_unretained_width_cancels_but_retained_supplied_sum_overflow_rejects(executors):
    p = wide_cancellation_problem()
    expected = independent_analysis(p)
    assert expected["domain_volume"] == [3, 1]
    overflowing = problem_of()
    overflowing["levels"] = [overflowing["levels"][1]]
    for c in overflowing["levels"][0]["cells"]:
        c["parent"] = None
        c["volume"] = [1 << 4095, 1]
    overflowing["probes"] = [{"name": "whole", "bounds": overflowing["domain"]}]
    for module in executors:
        assert wire(module.certify(p)) == wire(expected)
        with pytest.raises(ValueError):
            module.certify(overflowing)


def test_generic_auditor_complete_certificate_wire():
    audit = private_module("_qr05ah_test_generic_audit", "audit_json.py")
    for p in (problem_of(), shared_problem(), wide_cancellation_problem()):
        assert wire(audit.expected_certificate(p)) == wire(independent_analysis(p))


OBS_SCOPE = dict.fromkeys(
    (
        "missing_marks_inferred",
        "source_moments_inferred",
        "geometry_inferred",
        "mark_origin_authenticated",
        "observation_origin_authenticated",
    ),
    False,
)
FAMILIES = ("grid", "warp", "warp_stale", "boost", "dilate")
SPECIFICATIONS = [
    (name, level, design)
    for name in FAMILIES
    for level in range(3)
    for design in (
        ("identity", "iid_half", "singleton") if name in ("grid", "warp") else ("identity",)
    )
]


def base_partition_levels():
    first = {
        f"c_{i}_{j}": (F(i, 3), F(i + 1, 3), F(j, 2), F(j + 1, 2))
        for i in range(3)
        for j in range(2)
    }
    levels = [first]
    second = {n: b for n, b in first.items() if n != "c_1_0"}
    second["c_1_0_l"] = (F(1, 3), F(1, 2), F(0), F(1, 2))
    second["c_1_0_r"] = (F(1, 2), F(2, 3), F(0), F(1, 2))
    levels.append(second)
    third = {n: b for n, b in second.items() if n != "c_1_0_l"}
    third["c_1_0_lb"] = (F(1, 3), F(1, 2), F(0), F(1, 4))
    third["c_1_0_lt"] = (F(1, 3), F(1, 2), F(1, 4), F(1, 2))
    levels.append(third)
    return [{n: level[n] for n in sorted(level)} for level in levels]


def transformed_point(name, u, v):
    if name in ("warp", "warp_stale"):
        return u * u, v * v
    if name == "boost":
        return 2 * u, v / 2
    if name == "dilate":
        return 2 * u, 2 * v
    assert name == "grid"
    return u, v


def transformed_rectangle(name, bounds):
    a, b, c, d = bounds
    u, v = transformed_point(name, a, c)
    x, y = transformed_point(name, b, d)
    return u, x, v, y


def marker_points():
    return {
        "bottom": (F(0), F(0)),
        "aligned": (F(2, 3), F(1, 2)),
        "unaligned": (F(3, 5), F(2, 5)),
        "top": (F(1), F(1)),
    }


PROBE_LABELS = (
    ("whole", "bottom", "top"),
    ("lower_aligned", "bottom", "aligned"),
    ("upper_aligned", "aligned", "top"),
    ("lower_unaligned", "bottom", "unaligned"),
    ("upper_unaligned", "unaligned", "top"),
)


def base_label_map(level):
    points = marker_points()
    for name, (a, b, c, d) in base_partition_levels()[level].items():
        points[name] = ((a + b) / 2, (c + d) / 2)
    labels = sorted(points, key=lambda n: (sum(points[n]), *points[n], n))
    return {name: i for i, name in enumerate(labels)}, points


def independent_certificate_problem(name):
    levels = []
    old = {}
    for index, partition in enumerate(base_partition_levels()):
        cells = []
        for label, b in partition.items():
            if index == 0:
                parent = None
            elif label in old:
                parent = label
            elif index == 1:
                parent = "c_1_0"
            else:
                parent = "c_1_0_l"
            a, z, c, d = b
            target = transformed_rectangle(name, b)
            point = transformed_point(name, (a + z) / 2, (c + d) / 2)
            mark = area(b if name == "warp_stale" else target)
            cells.append(cell(label, target, point, mark, parent))
        levels.append({"name": f"l{index}", "cells": cells})
        old = partition
    markers = marker_points()
    probes = []
    for probe, a, b in PROBE_LABELS:
        au, av = markers[a]
        bu, bv = markers[b]
        probes.append(
            {"name": probe, "bounds": rect(transformed_rectangle(name, (au, bu, av, bv)))}
        )
    return {
        "schema_version": "det8-qr05ah-problem-v1",
        "family": "qr05ah_partition_bounds",
        "domain": rect(transformed_rectangle(name, (F(0), F(1), F(0), F(1)))),
        "probes": probes,
        "levels": levels,
    }


def independent_source(name, level=0):
    ids, base = base_label_map(level)
    coords = [transformed_point(name, *base[n]) for n in sorted(base, key=ids.__getitem__)]
    past = [[i for i, (u, v) in enumerate(coords) if u < x and v < y] for x, y in coords]
    assert all(all(i < j for i in row) for j, row in enumerate(past))
    cells = []
    for label, b in sorted(base_partition_levels()[level].items(), key=lambda pair: ids[pair[0]]):
        transformed = transformed_rectangle(name, b)
        cells.append(
            {
                "event": ids[label],
                "bounds": rect(transformed),
                "geometric_mark": fw(area(transformed)),
                "supplied_mark": fw(area(b if name == "warp_stale" else transformed)),
            }
        )
    return {
        "name": name,
        "coordinates": [rect(p) for p in coords],
        "past": past,
        "fixed": sorted(ids[n] for n in marker_points()),
        "eligible": [c["event"] for c in cells],
        "probes": [{"name": p, "source": ids[a], "target": ids[b]} for p, a, b in PROBE_LABELS],
        "cells": cells,
        "mark_kind": "stale_base" if name == "warp_stale" else "geometric_cell_volume",
    }


def independent_design(name, m):
    if name == "identity":
        masses = [F(int(mask == (1 << m) - 1)) for mask in range(1 << m)]
    elif name == "iid_half":
        masses = [F(1, 1 << m)] * (1 << m)
    else:
        assert name == "singleton"
        masses = [F(1, m) if mask.bit_count() == 1 else F() for mask in range(1 << m)]
    assert sum(masses, F()) == 1
    return {"name": name, "mask_probabilities": list(map(fw, masses))}


def independent_case(name, level, design_name):
    source = independent_source(name, level)
    design = independent_design(design_name, len(source["cells"]))
    population = independent_population(source)
    samples = []
    for mask in range(len(design["mask_probabilities"])):
        p = independent_packet(source, design, mask)
        samples.append({"problem": p, "analysis": observer_analysis(p)})
    masses = list(map(fraction, design["mask_probabilities"]))
    moments = independent_moments(population, samples, masses)
    cov, pairs, zeros = independent_covariance(source, population, masses)
    assert cov == moments["inclusion"]["covariance"]
    assert moments["inclusion"]["mean"] == [q["supplied_target"] for q in population]
    return {
        "case_id": name + f"__l{level}__" + design_name,
        "level": f"l{level}",
        "source": source,
        "design": design,
        "population": population,
        "samples": samples,
        "moments": moments,
        "joint_covariance": cov,
        "counts": {
            "events": len(source["past"]),
            "eligible_events": len(source["eligible"]),
            "mask_rows": len(samples),
            "positive_rows": sum(x["analysis"]["possible"] for x in samples),
            "questions": len(population),
            "source_member_terms": sum(len(q["members"]) for q in population),
            "observed_member_terms": sum(
                x["analysis"]["counts"]["observed_member_terms"] for x in samples
            ),
            "ordered_cell_pairs": pairs,
            "zero_joint_pairs": zeros,
            "packet_calls": 2 * len(samples),
        },
    }


@pytest.fixture(scope="session")
def pinned_ag():
    path = HERE.parent / "qr-05ag-local-volume-2026-09-07" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert (
        len(raw) == 3027867
        and hashlib.sha256(raw).hexdigest()
        == "5af957be534af3096c7f61ec444349ec49c739ebf70364146b7f4568a8832f91"
    )
    envelope = json.loads(raw)
    for name, identity in envelope["source_ledger"].items():
        source = path.parent / name
        assert source.is_file() and not source.is_symlink()
        evidence = source.read_bytes()
        assert (
            len(evidence) == identity["bytes"]
            and hashlib.sha256(evidence).hexdigest() == identity["sha256"]
        )
    native(envelope["suite"])
    return envelope


@pytest.fixture(scope="session")
def observers(pinned_ag):
    result = []
    for i, filename in enumerate(("volume.py", "reference_qr05ag.py")):
        path = HERE.parent / "qr-05ag-local-volume-2026-09-07" / filename
        assert (
            hashlib.sha256(path.read_bytes()).hexdigest()
            == pinned_ag["source_ledger"][filename]["sha256"]
        )
        spec = importlib.util.spec_from_file_location(f"_qr05ah_test_pinned_observer_{i}", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        result.append(module)
    return tuple(result)


@pytest.fixture(scope="session")
def expected_certificates():
    result = []
    for name in FAMILIES:
        p = independent_certificate_problem(name)
        result.append({"source": name, "problem": p, "analysis": independent_analysis(p)})
    return result


@pytest.fixture(scope="session")
def expected_cases():
    return [independent_case(*spec) for spec in SPECIFICATIONS]


@pytest.mark.parametrize("index", range(5))
def test_fixed_five_complete_family_certificates(index, expected_certificates, runner, executors):
    expected = expected_certificates[index]
    assert wire(runner.certificate_problem(FAMILIES[index])) == wire(expected["problem"])
    assert wire(runner.certificate_oracle(expected["problem"])) == wire(expected["analysis"])
    before = wire(expected["problem"])
    for module in executors:
        assert wire(module.certify(expected["problem"])) == wire(expected["analysis"])
        assert wire(expected["problem"]) == before


@pytest.mark.parametrize("index", range(27))
def test_fixed_all_twenty_seven_case_source_packet_moment_and_certificate_bridges(
    index, expected_cases, expected_certificates, runner, observers
):
    name, level, design = SPECIFICATIONS[index]
    expected = expected_cases[index]
    assert wire(runner.build_case(name, level, design)) == wire(expected)
    for sample in expected["samples"]:
        p = sample["problem"]
        assert set(p) == {
            "schema_version",
            "family",
            "frame_size",
            "fixed",
            "eligible",
            "probes",
            "mask_probabilities",
            "record",
        }
        assert set(p["record"]) == {"kept", "past", "marks"}
        assert len(p["eligible"]) <= 8 and p["frame_size"] <= 12
        before = wire(p)
        for module in observers:
            assert wire(module.analyze(p)) == wire(sample["analysis"]) and wire(p) == before
    certificate = expected_certificates[FAMILIES.index(name)]["analysis"]["levels"][level]
    ids, _ = base_label_map(level)
    for pop, q in zip(expected["population"], certificate["questions"], strict=True):
        assert pop["members"] == sorted(ids[n] for n in q["representative_cells"])
        for key, certkey in (
            ("supplied_target", "supplied_target"),
            ("geometric_target", "geometric_target"),
            ("continuum_volume", "continuum_volume"),
            ("annotation_error", "annotation_error"),
            ("quadrature_error", "quadrature_error"),
        ):
            assert pop[key] == q[certkey]


def observer_problem(mask=3, masses=None, marks=None, past=None, fixed=None, probes=None):
    past = [list(range(i)) for i in range(4)] if past is None else past
    n = len(past)
    fixed = [0, n - 1] if fixed is None else fixed
    eligible = [i for i in range(n) if i not in fixed]
    masses = [F(1, 1 << len(eligible))] * (1 << len(eligible)) if masses is None else masses
    marks = (
        [F(1), F(3)]
        if marks is None and len(eligible) == 2
        else ([F(i + 1) for i in range(len(eligible))] if marks is None else marks)
    )
    probes = [{"name": "whole", "source": 0, "target": n - 1}] if probes is None else probes
    kept = sorted(fixed + [v for j, v in enumerate(eligible) if mask & (1 << j)])
    return {
        "schema_version": "det8-qr05ag-problem-v1",
        "family": "qr05ag_local_volume",
        "frame_size": n,
        "fixed": copy.deepcopy(fixed),
        "eligible": eligible,
        "probes": copy.deepcopy(probes),
        "mask_probabilities": list(map(fw, masses)),
        "record": {
            "kept": kept,
            "past": [[j for j, v in enumerate(kept) if v in past[event]] for event in kept],
            "marks": [
                {"event": event, "volume": fw(marks[j])}
                for j, event in enumerate(eligible)
                if event in kept
            ],
        },
    }


def observer_analysis(p):
    eligible = p["eligible"]
    masses = list(map(fraction, p["mask_probabilities"]))
    pi = [
        sum((mass for mask, mass in enumerate(masses) if mask & (1 << j)), F())
        for j in range(len(eligible))
    ]
    pbar = sum(pi, F()) / len(pi)
    kept, past = p["record"]["kept"], p["record"]["past"]
    rows = dict(zip(kept, ({kept[j] for j in row} for row in past), strict=True))
    mark = {row["event"]: fraction(row["volume"]) for row in p["record"]["marks"]}
    inclusion = dict(zip(eligible, pi, strict=True))
    mask = sum(1 << j for j, v in enumerate(eligible) if v in kept)
    questions = []
    for probe in p["probes"]:
        a, b = probe["source"], probe["target"]
        members = [v for v in eligible if v in mark and a in rows[v] and v in rows[b]]
        questions.append(
            {
                "probe": probe["name"],
                "observed_cells": [
                    {"event": v, "volume": fw(mark[v]), "inclusion": fw(inclusion[v])}
                    for v in members
                ],
                "estimates": {
                    "raw": fw(sum((mark[v] for v in members), F())),
                    "uniform_rate": fw(sum((mark[v] / pbar for v in members), F())),
                    "inclusion": fw(sum((mark[v] / inclusion[v] for v in members), F())),
                },
            }
        )
    m, k, pn = len(eligible), len(mark), len(questions)
    l, i, c = 1 << m, m * (1 << (m - 1)), pn * k
    a = sum(len(q["observed_cells"]) for q in questions)
    return {
        "input_sha256": digest(p),
        "mask": mask,
        "probability": fw(masses[mask]),
        "possible": bool(masses[mask]),
        "marginals": list(map(fw, pi)),
        "questions": questions,
        "counts": {
            "events": p["frame_size"],
            "eligible_events": m,
            "kept_events": len(kept),
            "retained_cells": k,
            "mask_rows": l,
            "questions": pn,
            "inclusion_terms": i,
            "member_candidates": c,
            "observed_member_terms": a,
            "estimator_terms": 3 * a,
            "reserved_estimator_terms": 3 * c,
            "reserved_total_work": l + i + 4 * c + 3 * pn,
            "total_work": l + i + c + 3 * a + 3 * pn,
        },
        "scope": dict(OBS_SCOPE),
    }


def design_moments(analyses, masses, method):
    vectors = [[fraction(q["estimates"][method]) for q in a["questions"]] for a in analyses]
    qn = len(vectors[0])
    mean = [sum((p * v[i] for p, v in zip(masses, vectors, strict=True)), F()) for i in range(qn)]
    covariance = [
        [
            sum(
                (
                    p * (v[i] - mean[i]) * (v[j] - mean[j])
                    for p, v in zip(masses, vectors, strict=True)
                ),
                F(),
            )
            for j in range(qn)
        ]
        for i in range(qn)
    ]
    second = [
        [
            sum((p * v[i] * v[j] for p, v in zip(masses, vectors, strict=True)), F())
            - mean[i] * mean[j]
            for j in range(qn)
        ]
        for i in range(qn)
    ]
    assert covariance == second
    return mean, covariance


def independent_packet(source, design, mask):
    return observer_problem(
        mask,
        masses=list(map(fraction, design["mask_probabilities"])),
        marks=[fraction(c["supplied_mark"]) for c in source["cells"]],
        past=source["past"],
        fixed=source["fixed"],
        probes=source["probes"],
    )


def overlap_length(a, b, c, d):
    # Independent partition-by-endpoints route instead of directly clipping
    # a single interval with min/max endpoints.
    points = sorted({a, b, c, d})
    length = F()
    for left, right in pairwise(points):
        mid = (left + right) / 2
        if a < mid < b and c < mid < d:
            length += right - left
    return length


def independent_population(source):
    coords = [tuple(map(fraction, p)) for p in source["coordinates"]]
    result = []
    for probe in source["probes"]:
        a, b = probe["source"], probe["target"]
        au, av = coords[a]
        bu, bv = coords[b]
        members = [
            c["event"]
            for c in source["cells"]
            if au < coords[c["event"]][0] < bu and av < coords[c["event"]][1] < bv
        ]
        assert members == [
            i for i in source["eligible"] if a in source["past"][i] and i in source["past"][b]
        ]
        supplied = sum(
            (fraction(c["supplied_mark"]) for c in source["cells"] if c["event"] in members), F()
        )
        geometric = sum(
            (fraction(c["geometric_mark"]) for c in source["cells"] if c["event"] in members), F()
        )
        continuum = (bu - au) * (bv - av) / 2
        overlaps = []
        for c in source["cells"]:
            ul, uh, vl, vh = map(fraction, c["bounds"])
            value = overlap_length(ul, uh, au, bu) * overlap_length(vl, vh, av, bv) / 2
            overlaps.append({"event": c["event"], "volume": fw(value)})
        assert sum((fraction(c["volume"]) for c in overlaps), F()) == continuum
        result.append(
            {
                "probe": probe["name"],
                "members": members,
                "supplied_target": fw(supplied),
                "geometric_target": fw(geometric),
                "continuum_volume": fw(continuum),
                "annotation_error": fw(supplied - geometric),
                "quadrature_error": fw(geometric - continuum),
                "overlaps": overlaps,
            }
        )
    return result


def independent_moments(population, samples, masses):
    result = {}
    for method in METHODS:
        mean, cov = design_moments([x["analysis"] for x in samples], masses, method)
        bias, rows = [], []
        for q, average in zip(population, mean, strict=True):
            t, g, v = map(
                fraction, (q["supplied_target"], q["geometric_target"], q["continuum_volume"])
            )
            components = (average - t, t - g, g - v)
            assert sum(components, F()) == average - v
            bias.append(fw(components[0]))
            rows.append(
                {
                    "probe": q["probe"],
                    "mean": fw(average),
                    "finite_target": fw(t),
                    "true_finite_target": fw(g),
                    "continuum": fw(v),
                    "sampling_bias": fw(components[0]),
                    "annotation_error": fw(components[1]),
                    "quadrature_error": fw(components[2]),
                    "total_error": fw(average - v),
                }
            )
        result[method] = {
            "mean": list(map(fw, mean)),
            "bias": bias,
            "covariance": [list(map(fw, row)) for row in cov],
            "decompositions": rows,
        }
    return result


def independent_covariance(source, population, masses):
    cells = source["cells"]
    n = len(cells)
    pi = [sum((p for mask, p in enumerate(masses) if mask & (1 << i)), F()) for i in range(n)]
    pair = [
        [
            sum((p for mask, p in enumerate(masses) if mask & (1 << i) and mask & (1 << j)), F())
            for j in range(n)
        ]
        for i in range(n)
    ]
    kernel = [
        [
            fraction(cells[i]["supplied_mark"])
            * fraction(cells[j]["supplied_mark"])
            * (pair[i][j] / (pi[i] * pi[j]) - 1)
            for j in range(n)
        ]
        for i in range(n)
    ]
    memberships = [
        [i for i, c in enumerate(cells) if c["event"] in q["members"]] for q in population
    ]
    matrix = [
        [fw(sum((kernel[i][j] for i in left for j in right), F())) for right in memberships]
        for left in memberships
    ]
    pairs = sum(len(left) * len(right) for left in memberships for right in memberships)
    zeros = sum(
        pair[i][j] == 0
        for left in memberships
        for right in memberships
        for i in left
        for j in right
    )
    return matrix, pairs, zeros


def scaled_population(population, factor):
    answer = copy.deepcopy(population)
    for q in answer:
        for key in (
            "supplied_target",
            "geometric_target",
            "continuum_volume",
            "annotation_error",
            "quadrature_error",
        ):
            q[key] = fw(fraction(q[key]) * factor)
        for row in q["overlaps"]:
            row["volume"] = fw(fraction(row["volume"]) * factor)
    return answer


def scaled_moments(moments, factor):
    answer = copy.deepcopy(moments)
    for method in METHODS:
        for key in ("mean", "bias"):
            answer[method][key] = [fw(fraction(v) * factor) for v in answer[method][key]]
        answer[method]["covariance"] = [
            [fw(fraction(v) * factor * factor) for v in row] for row in answer[method]["covariance"]
        ]
        for row in answer[method]["decompositions"]:
            for key in row:
                if key != "probe":
                    row[key] = fw(fraction(row[key]) * factor)
    return answer


def assert_psd(matrix):
    a = [list(map(fraction, row)) for row in matrix]
    assert a == list(map(list, zip(*a, strict=True)))
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot >= 0
        if pivot == 0:
            assert all(a[k][j] == 0 for j in range(k + 1, len(a)))
        else:
            for i in range(k + 1, len(a)):
                for j in range(k + 1, len(a)):
                    a[i][j] -= a[i][k] * a[k][j] / pivot


def geometric_projection(analysis):
    result = copy.deepcopy(analysis)
    result.pop("input_sha256")
    for level in result["levels"]:
        for c in level["cells"]:
            c.pop("annotation_error")
        for q in level["questions"]:
            for name in ("supplied_target", "annotation_error", "total_error"):
                q.pop(name)
    for ref in result["refinements"]:
        for parent in ref["parents"]:
            parent.pop("supplied_volume")
    return result


def scale_certificate(analysis, factor, new_hash):
    answer = copy.deepcopy(analysis)
    answer["input_sha256"] = new_hash
    answer["domain_volume"] = fw(fraction(answer["domain_volume"]) * factor)
    for level in answer["levels"]:
        for c in level["cells"]:
            for key in ("geometric_volume", "annotation_error"):
                c[key] = fw(fraction(c[key]) * factor)
        for q in level["questions"]:
            for key in q:
                if key not in ("probe", "inner_cells", "outer_cells", "representative_cells"):
                    q[key] = fw(fraction(q[key]) * factor)
    for ref in answer["refinements"]:
        for parent in ref["parents"]:
            for key in ("geometric_volume", "supplied_volume"):
                parent[key] = fw(fraction(parent[key]) * factor)
        for q in ref["questions"]:
            for key in q:
                if key != "probe":
                    q[key] = fw(fraction(q[key]) * factor)
    return answer


def scale_observation(sample, factor):
    result = copy.deepcopy(sample)
    for mark in result["problem"]["record"]["marks"]:
        mark["volume"] = fw(fraction(mark["volume"]) * factor)
    result["analysis"]["input_sha256"] = digest(result["problem"])
    for question in result["analysis"]["questions"]:
        for mark in question["observed_cells"]:
            mark["volume"] = fw(fraction(mark["volume"]) * factor)
        for method in METHODS:
            question["estimates"][method] = fw(fraction(question["estimates"][method]) * factor)
    return result


def independent_controls(certificates, cases, counter):
    cb = {c["source"]: c["analysis"] for c in certificates}
    by = {c["case_id"]: c for c in cases}
    result = {"enclosures": [], "refinement": [], "stale_marks": []}
    for name in FAMILIES:
        cert = cb[name]
        qs = [q for level in cert["levels"] for q in level["questions"]]
        changes = [q for ref in cert["refinements"] for q in ref["questions"]]
        identities = True
        for q in qs:
            t, g, v = map(
                fraction, (q["supplied_target"], q["geometric_target"], q["continuum_volume"])
            )
            identities &= (
                fraction(q["annotation_error"]) == t - g
                and fraction(q["quadrature_error"]) == g - v
                and fraction(q["total_error"]) == t - v
                and fraction(q["annotation_error"]) + fraction(q["quadrature_error"])
                == fraction(q["total_error"])
            )
        result["enclosures"].append(
            {
                "source": name,
                "sandwiches_hold": all(
                    fraction(q["lower_bound"]) <= fraction(q[k]) <= fraction(q["upper_bound"])
                    for q in qs
                    for k in ("geometric_target", "continuum_volume")
                ),
                "annotation_separate": identities,
                "aligned_exact": all(
                    q["lower_bound"]
                    == q["upper_bound"]
                    == q["geometric_target"]
                    == q["continuum_volume"]
                    for level in cert["levels"]
                    for q in level["questions"][:3]
                ),
            }
        )
        result["refinement"].append(
            {
                "source": name,
                "lower_nondecreasing": all(fraction(q["lower_gain"]) >= 0 for q in changes),
                "upper_nonincreasing": all(fraction(q["upper_drop"]) >= 0 for q in changes),
                "gap_nonincreasing": all(fraction(q["gap_drop"]) >= 0 for q in changes),
                "all_absolute_errors_nonincreasing": all(
                    fraction(q["absolute_error_change"]) <= 0 for q in changes
                ),
                "absolute_error_changes": [q["absolute_error_change"] for q in changes],
            }
        )
    for level in range(3):
        a = by[f"grid__l{level}__identity"]
        c = by[f"warp_stale__l{level}__identity"]
        result["stale_marks"].append(
            {
                "level": f"l{level}",
                "geometric_certificate_equal_warp": wire(geometric_projection(cb["warp"]))
                == wire(geometric_projection(cb["warp_stale"])),
                "public_samples_equal_base": wire(a["samples"]) == wire(c["samples"]),
                "annotation_errors": [q["annotation_error"] for q in c["population"]],
            }
        )
    for name, key, factor in (("boost", "boost", F(1)), ("dilate", "dilation", F(4))):
        result[key] = {
            "volume_factor": fw(factor),
            "complete_certificate_scaling": wire(
                scale_certificate(cb["grid"], factor, cb[name]["input_sha256"])
            )
            == wire(cb[name]),
            "complete_observer_scaling": all(
                wire(
                    [
                        scale_observation(s, factor)
                        for s in by[f"grid__l{level}__identity"]["samples"]
                    ]
                )
                == wire(by[f"{name}__l{level}__identity"]["samples"])
                for level in range(3)
            ),
            "complete_moment_scaling": all(
                wire(scaled_moments(by[f"grid__l{level}__identity"]["moments"], factor))
                == wire(by[f"{name}__l{level}__identity"]["moments"])
                for level in range(3)
            ),
        }
    q = counter["analysis"]["refinements"][0]["questions"][0]
    result["counterexample"] = {
        **counter,
        "bounds_tightened": fraction(q["gap_drop"]) > 0,
        "absolute_error_increased": fraction(q["absolute_error_change"]) > 0,
    }
    return result


@pytest.fixture(scope="session")
def expected_suite(expected_certificates, expected_cases, pinned_ag):
    old = {c["case_id"]: c for c in pinned_ag["suite"]["cases"]}
    ids = []
    for case in expected_cases:
        if case["level"] == "l0":
            reduced = {k: v for k, v in case.items() if k != "level"}
            reduced["case_id"] = case["source"]["name"] + "__" + case["design"]["name"]
            assert wire(reduced) == wire(old[reduced["case_id"]])
            ids.append(reduced["case_id"])
    assert len(ids) == 9
    counts = {
        "cases": len(expected_cases),
        **{k: sum(c["counts"][k] for c in expected_cases) for k in expected_cases[0]["counts"]},
    }
    counter = {"problem": problem_of(), "analysis": independent_analysis(problem_of())}
    return {
        "certificates": expected_certificates,
        "cases": expected_cases,
        "controls": independent_controls(expected_certificates, expected_cases, counter),
        "prior_bridges": {
            "AG_level0_case_ids": ids,
            "AG_level0_complete_cases_equal": True,
            "AG_other_math_replayed": False,
        },
        "public_controls": {
            "certificate_calls": 12,
            "observer_calls": counts["packet_calls"],
            "independent_certificate_routes_equal": True,
            "independent_observer_routes_equal": True,
            "invalid_certificate_calls_rejected": 16,
        },
        "totals": counts,
        "scope": dict.fromkeys(
            (
                "unknown_geometry_reconstructed",
                "continuum_limit_established",
                "marks_authenticated",
                "observer_bounds_inferred",
                "monotone_absolute_error_guaranteed",
                "cross_level_observation_transport_proved",
                "quantum_channel_constructed",
                "gravity_derived",
                "empirical_data_used",
                "ret_integration_tested",
            ),
            False,
        ),
    }


def test_fixed_full_suite_controls_counterexample_and_nine_AG_level_zero_case_bridges(
    runner, expected_suite
):
    assert wire(runner.run_suite()) == wire(expected_suite)
    counter = {k: expected_suite["controls"]["counterexample"][k] for k in ("problem", "analysis")}
    assert wire(
        runner.assemble_suite(expected_suite["certificates"], expected_suite["cases"], counter)
    ) == wire(expected_suite)


def test_fixed_covariance_three_errors_and_geometric_enclosure_keep_access_layers_separate(
    expected_cases, expected_certificates
):
    for case in expected_cases:
        for method in METHODS:
            assert_psd(case["moments"][method]["covariance"])
            for row in case["moments"][method]["decompositions"]:
                assert sum(
                    (
                        fraction(row[k])
                        for k in ("sampling_bias", "annotation_error", "quadrature_error")
                    ),
                    F(),
                ) == fraction(row["total_error"])
        assert case["moments"]["inclusion"]["covariance"] == case["joint_covariance"]
        assert all(x == [0, 1] for x in case["moments"]["inclusion"]["bias"])
        if case["design"]["name"] == "singleton":
            assert case["counts"]["zero_joint_pairs"] > 0
    for cert in expected_certificates:
        for level in cert["analysis"]["levels"]:
            for q in level["questions"]:
                g, v, l, u = map(
                    fraction,
                    (
                        q["geometric_target"],
                        q["continuum_volume"],
                        q["lower_bound"],
                        q["upper_bound"],
                    ),
                )
                assert l <= g <= u and l <= v <= u
                assert fraction(q["error_lower"]) <= g - v <= fraction(q["error_upper"])
                assert abs(g - v) <= fraction(q["boundary_gap"])
        for ref in cert["analysis"]["refinements"]:
            assert all(
                fraction(q[k]) >= 0
                for q in ref["questions"]
                for k in ("lower_gain", "upper_drop", "gap_drop")
            )


def at_path(tree, path):
    for key in path:
        tree = tree[key]
    return tree


def add_fraction(tree, path):
    return replaced(tree, path, fw(fraction(at_path(tree, path)) + 1))


def test_fixed_certificate_output_corruptions_are_nonvacuous_complete_wire_checks(
    runner, expected_certificates
):
    original = expected_certificates[0]["analysis"]
    q = original["levels"][0]["questions"][3]
    changes = [
        replaced(original, ("input_sha256",), "0" * 64),
        add_fraction(original, ("domain_volume",)),
        add_fraction(original, ("levels", 0, "cells", 0, "geometric_volume")),
        add_fraction(original, ("levels", 0, "cells", 0, "annotation_error")),
        *(
            replaced(original, ("levels", 0, "questions", 3, key), q[key] + ["not_a_cell"])
            for key in ("inner_cells", "outer_cells", "representative_cells")
        ),
        *(
            add_fraction(original, ("levels", 0, "questions", 3, key))
            for key in (
                "lower_bound",
                "upper_bound",
                "boundary_gap",
                "geometric_target",
                "supplied_target",
                "continuum_volume",
                "annotation_error",
                "quadrature_error",
                "total_error",
                "error_lower",
                "error_upper",
            )
        ),
        replaced(original, ("refinements", 0, "parents", 0, "children"), ["false_child"]),
        add_fraction(original, ("refinements", 0, "parents", 0, "supplied_volume")),
        add_fraction(original, ("refinements", 0, "questions", 3, "lower_gain")),
        add_fraction(original, ("refinements", 0, "questions", 3, "absolute_error_change")),
        replaced(original, ("counts", "total_work"), original["counts"]["total_work"] + 1),
        replaced(original, ("scope", "observer_has_geometry"), True),
    ]
    assert len(changes) == 24
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.require_same_wire(
                bad, original, "complete independently reconstructed certificate"
            )
    assert wire(original) == before


def test_fixed_observer_case_corruptions_cannot_leak_bounds_or_hide_sampling_geometry(
    runner, expected_cases
):
    original = expected_cases[3]
    changes = [
        replaced(original, ("level",), "l0"),
        add_fraction(original, ("source", "cells", 0, "bounds", 1)),
        add_fraction(original, ("source", "cells", 0, "supplied_mark")),
        replaced(
            original,
            ("samples", 0, "problem", "record"),
            {**original["samples"][0]["problem"]["record"], "bounds": []},
        ),
        add_fraction(
            original, ("samples", 0, "analysis", "questions", 0, "estimates", "inclusion")
        ),
        replaced(original, ("samples", 0, "analysis", "scope", "geometry_inferred"), True),
        add_fraction(original, ("population", 3, "quadrature_error")),
        add_fraction(original, ("population", 3, "overlaps", 0, "volume")),
        add_fraction(original, ("moments", "inclusion", "covariance", 1, 2)),
        add_fraction(original, ("moments", "inclusion", "decompositions", 3, "sampling_bias")),
        add_fraction(original, ("joint_covariance", 1, 2)),
        replaced(original, ("counts", "packet_calls"), original["counts"]["packet_calls"] + 1),
    ]
    assert len(changes) == 12
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.check_case(bad, original)
    assert wire(original) == before


def test_fixed_complete_suite_controls_bridges_and_claim_scope_reject_nonvacuous_changes(
    runner, expected_suite
):
    original = expected_suite
    changes = [
        replaced(original, ("controls", "counterexample", "absolute_error_increased"), False),
        replaced(
            original,
            ("controls", "refinement", 0, "all_absolute_errors_nonincreasing"),
            not original["controls"]["refinement"][0]["all_absolute_errors_nonincreasing"],
        ),
        add_fraction(original, ("controls", "stale_marks", 0, "annotation_errors", 0)),
        replaced(
            original,
            ("prior_bridges", "AG_level0_case_ids"),
            original["prior_bridges"]["AG_level0_case_ids"][:-1],
        ),
        replaced(original, ("public_controls", "invalid_certificate_calls_rejected"), 17),
        replaced(original, ("scope", "cross_level_observation_transport_proved"), True),
        replaced(original, ("cases",), list(reversed(original["cases"]))),
        {**original, "only_favorable_refinements": True},
    ]
    assert len(changes) == 8
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.check_suite(bad, original)
    assert wire(original) == before


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_guard_subprocess_without_assertions(tmp_path, optimized):
    program = r"""
import importlib.util,json,resource,sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
spec=importlib.util.spec_from_file_location("_qr05ah_guards",Path(sys.argv[1]))
if spec is None or spec.loader is None:raise RuntimeError("missing helpers")
h=importlib.util.module_from_spec(spec);sys.modules[spec.name]=h;spec.loader.exec_module(h)
rejections=pre=0
def require(value,message):
    if not value:raise RuntimeError(message)
def reject(call,value):
    global rejections
    try:call(value)
    except ValueError:rejections+=1
    else:raise RuntimeError("invalid input accepted")
def before_dump(call,value):
    global pre
    original=json.dumps
    def forbidden(*args,**kwargs):raise RuntimeError("unsafe tree serialized")
    json.dumps=forbidden
    try:reject(call,value);pre+=1
    finally:json.dumps=original
valid=h.problem_of();shared_valid=h.shared_problem();invalid=h.invalid_problems()
require(len(list(h.graph_inputs(valid)))==18,"graph fixture inventory")
for i,filename in enumerate(("certificate.py","reference_qr05ah.py")):
    module=h.private_module("_qr05ah_guard_core"+str(i),filename)
    for p in (valid,shared_valid,h.wide_cancellation_problem()):
        require(h.wire(module.certify(p))==h.wire(h.independent_analysis(p)),"complete generic certificate")
    counts=dict.fromkeys(h.HOOKS,0);hooks={n:getattr(module,n) for n in h.HOOKS}
    for name in hooks:
        def counted(*args,_name=name,**kw):counts[_name]+=1;return hooks[_name](*args,**kw)
        setattr(module,name,counted)
    try:module.certify(valid)
    finally:
        for name,value in hooks.items():setattr(module,name,value)
    require(counts=={"_partition":2,"_refinement":1,"_questions":2},"complete hook inventory")
    for bad in invalid:reject(module.certify,bad)
    for bad in h.graph_inputs(valid):before_dump(module.certify,bad)
    def forbidden(*args):raise RuntimeError("work preceded complete reservation")
    planned=h.planned_caps(valid)
    require(len(planned)==7 and len(h.CAPS)==11,"live-cap fixture inventory")
    for constant,limit in planned.items():
        old=getattr(module,constant);hooks={n:getattr(module,n) for n in h.HOOKS}
        setattr(module,constant,limit-1)
        for n in hooks:setattr(module,n,forbidden)
        try:reject(module.certify,valid)
        finally:
            setattr(module,constant,old)
            for n,v in hooks.items():setattr(module,n,v)
    for constant in h.CAPS:
        old=getattr(module,constant);setattr(module,constant,min(1,planned.get(constant,2)-1))
        try:reject(module.certify,valid)
        finally:setattr(module,constant,old)
    hooks={n:getattr(module,n) for n in h.HOOKS}
    for n in hooks:setattr(module,n,forbidden)
    try:
        reject(module.certify,h.replaced(valid,("levels",1,"cells",1,"volume"),[0,1]))
        reject(module.certify,h.replaced(valid,("levels",1,"cells",1,"parent"),"unknown"))
        reject(module.certify,h.replaced(valid,("levels",1,"cells",1,"representative"),h.rect((1,h.F(1,2)))))
    finally:
        for n,v in hooks.items():setattr(module,n,v)
    original=module._questions;module._questions=forbidden
    try:
        for kind in ("equal_area_overlap_hole","hole","overlap","nonadditive","false_parent"):
            reject(module.certify,h.partition_counter(kind))
    finally:module._questions=original
    for v in (h.nested(0,64),h.nested([],64)):module._native(v)
    for v in (h.nested(0,65),h.nested([],65)):reject(module._native,v)
    shared=[0];module._native([shared,h.nested(shared,62)]);reject(module._native,[shared,h.nested(shared,63)])
    size=h.F(1<<2048);big=h.problem_of()
    big["domain"]=h.rect((0,size,0,size));big["probes"]=[{"name":"whole","bounds":big["domain"]}]
    big["levels"]=[{"name":"large","cells":[h.cell("c",(0,size,0,size),(size/2,size/2),1)]}]
    require(h.wire(module.certify(big))==h.wire(h.independent_analysis(big)),"unretained product cancellation")
    too=h.replaced(big,("domain",1),h.fw(2*size))
    too["probes"][0]["bounds"]=too["domain"]
    too["levels"][0]["cells"][0]["bounds"]=too["domain"]
    reject(module.certify,too)
    too=h.problem_of();too["levels"]=too["levels"][1:];too["levels"][0]["name"]="single"
    for cell in too["levels"][0]["cells"]:cell["parent"]=None;cell["volume"]=h.fw(h.F(1<<4095))
    too["probes"][0]["bounds"]=too["domain"]
    reject(module.certify,too)
    scalar={'"\\\\\b\f\n\r\t\x00\x1f é 🐈 \ud800':["é","🐈","\udfff",-123,False,None]}
    for constant,limit in (("MAX_NODES",8),("MAX_DEPTH",2),("MAX_BYTES",len(h.wire(scalar)))):
        old=getattr(module,constant);setattr(module,constant,limit)
        try:
            module._native(scalar)
            setattr(module,constant,limit-1);reject(module._native,scalar)
        finally:setattr(module,constant,old)
    wanted=h.wire(module.certify(shared_valid));old=module.MAX_BYTES
    require(len(wanted)>len(h.wire(shared_valid)),"output-byte fixture nonvacuous")
    module.MAX_BYTES=len(wanted)-1
    try:reject(module.certify,shared_valid)
    finally:module.MAX_BYTES=old
    nodes,depth=h.tree_resources(shared_valid)
    for constant,limit in (("MAX_NODES",nodes-1),("MAX_DEPTH",depth-1),("MAX_BYTES",len(h.wire(shared_valid))-1)):
        old=getattr(module,constant);setattr(module,constant,limit)
        try:before_dump(module.certify,shared_valid)
        finally:setattr(module,constant,old)
    input_before=h.wire(shared_valid);result=module.certify(shared_valid)
    result["levels"][0]["questions"][0]["supplied_target"][0]=-1
    result["domain_volume"][0]=2
    require(h.wire(shared_valid)==input_before,"input mutation")
    require(h.wire(module.certify(shared_valid))==h.wire(h.independent_analysis(shared_valid)),"ownership and restored caps")
runner=h.private_module("_qr05ah_guard_runner","study.py")
for bad in h.graph_inputs(valid):before_dump(runner.require_wire,bad)
for v in (h.nested(0,128),h.nested([],128)):runner.require_wire(v)
for v in (h.nested(0,129),h.nested([],129)):reject(runner.require_wire,v)
shared=[0];runner.require_wire([shared,h.nested(shared,126)]);reject(runner.require_wire,[shared,h.nested(shared,127)])
reject(lambda v:runner.require_same_wire({"x":0},v,"typed regression"),{"x":False})
require(pre==60,"pre-serialization rejection inventory")
require(rejections==2*(len(invalid)+56)+22,"explicit rejection inventory")
print(json.dumps({"rejections":rejections,"pre_serialization_rejections":pre,"invalid_fixture_cases":len(invalid),"optimized":bool(sys.flags.optimize)}))

"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05ah.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "rejections": 2 * (len(invalid_problems()) + 56) + 22,
        "pre_serialization_rejections": 60,
        "invalid_fixture_cases": len(invalid_problems()),
        "optimized": optimized,
    }
