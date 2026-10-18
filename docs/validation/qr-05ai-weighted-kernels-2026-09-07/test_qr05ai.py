"""Bounded independent checks for the private weighted-kernel diagnostic.

Only tests marked fixed consume authenticated AH cases. Collection and generic
hands use explicit synthetic data, never fixed fixture calculations.
"""

from __future__ import annotations

import builtins
import copy
import hashlib
import importlib.util
import json
import os
import sys
from fractions import Fraction as F
from itertools import combinations, pairwise
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
METHODS = ("raw", "joint_supported")
ALPHA = (F(1, 2), F(-1, 4), F(1, 8))
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
        load("_qr05ai_test_primary", "kernel.py"),
        load("_qr05ai_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05ai_test_runner", "study.py")


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


def independent_order(source):
    points = [tuple(map(fraction, c)) for c in source["coordinates"]]
    return [[j for j, (u, v) in enumerate(points) if u < x and v < y] for x, y in points]


def synthetic_source(four=False):
    if four:
        points = [
            (F(0), F(0)),
            *((F(2 * i + 1, 8), F(2 * i + 1, 8)) for i in range(4)),
            (F(1), F(1)),
        ]
        fixed, eligible = [0, 5], [1, 2, 3, 4]
        bounds = [(F(i, 4), F(i + 1, 4), F(0), F(1)) for i in range(4)]
        marks = [F(1, 8)] * 4
        probes = [{"name": "whole", "source": 0, "target": 5}]
    else:
        points = [
            (F(0), F(0)),
            (F(1, 4), F(1, 4)),
            (F(1, 2), F(1, 2)),
            (F(3, 4), F(3, 4)),
            (F(1), F(1)),
        ]
        fixed, eligible = [0, 2, 4], [1, 3]
        bounds = [(F(0), F(1, 2), F(0), F(1)), (F(1, 2), F(1), F(0), F(1))]
        marks = [F(1, 3), F(2, 3)]
        probes = [
            {"name": "whole", "source": 0, "target": 4},
            {"name": "left", "source": 0, "target": 2},
            {"name": "right", "source": 2, "target": 4},
        ]
    source = {
        "name": "synthetic",
        "coordinates": [rect(c) for c in points],
        "past": [],
        "fixed": fixed,
        "eligible": eligible,
        "probes": probes,
        "cells": [
            {
                "event": event,
                "bounds": rect(b),
                "geometric_mark": fw(area(b)),
                "supplied_mark": fw(w),
            }
            for event, b, w in zip(eligible, bounds, marks, strict=True)
        ],
        "mark_kind": "geometric_cell_volume" if four else "stale_base",
    }
    source["past"] = independent_order(source)
    return source


def design_of(m, name):
    if name == "identity":
        masses = [F(int(mask == (1 << m) - 1)) for mask in range(1 << m)]
    elif name == "iid_half":
        masses = [F(1, 1 << m)] * (1 << m)
    elif name == "singleton":
        masses = [F(1, m) if mask.bit_count() == 1 else F() for mask in range(1 << m)]
    else:
        assert name == "all_or_none"
        masses = [F(1, 2) if mask in (0, (1 << m) - 1) else F() for mask in range(1 << m)]
    return {"name": name, "mask_probabilities": list(map(fw, masses))}


def packet_of(source, design, mask):
    kept = sorted(
        source["fixed"] + [v for i, v in enumerate(source["eligible"]) if mask & (1 << i)]
    )
    return {
        "frame_size": len(source["past"]),
        "fixed": copy.deepcopy(source["fixed"]),
        "eligible": copy.deepcopy(source["eligible"]),
        "probes": copy.deepcopy(source["probes"]),
        "mask_probabilities": copy.deepcopy(design["mask_probabilities"]),
        "record": {
            "kept": kept,
            "past": [
                [j for j, v in enumerate(kept) if v in source["past"][event]] for event in kept
            ],
            "marks": [
                {"event": c["event"], "volume": copy.deepcopy(c["supplied_mark"])}
                for c in source["cells"]
                if c["event"] in kept
            ],
        },
    }


def inclusions(masses):
    return [
        sum((p for mask, p in enumerate(masses) if mask & support == support), F())
        for support in range(len(masses))
    ]


def chain_rows(packet):
    eligible = packet["eligible"]
    kept = packet["record"]["kept"]
    past = {
        v: {kept[i] for i in row} for v, row in zip(kept, packet["record"]["past"], strict=True)
    }
    weights = {c["event"]: fraction(c["volume"]) for c in packet["record"]["marks"]}
    pi = inclusions(list(map(fraction, packet["mask_probabilities"])))
    result = []
    for probe in packet["probes"]:
        a, b = probe["source"], probe["target"]
        interior = [v for v in eligible if v in weights and a in past[v] and v in past[b]]
        for degree in range(3):
            vertices = (
                [()]
                if degree == 0 and a in past[b]
                else (
                    [(v,) for v in interior]
                    if degree == 1
                    else [pair for pair in combinations(interior, 2) if pair[0] in past[pair[1]]]
                    if degree == 2
                    else []
                )
            )
            rows = []
            for vs in vertices:
                support = sum(1 << eligible.index(v) for v in vs)
                weight = F(1)
                for v in vs:
                    weight *= weights[v]
                rows.append(
                    {
                        "vertices": list(vs),
                        "eligible_mask": support,
                        "inclusion": fw(pi[support]),
                        "weight": fw(weight),
                    }
                )
            result.append({"probe": probe["name"], "degree": degree, "chains": rows})
    return result


def independent_observe(packet):
    masses = list(map(fraction, packet["mask_probabilities"]))
    mask = sum(1 << j for j, v in enumerate(packet["eligible"]) if v in packet["record"]["kept"])
    questions = []
    for row in chain_rows(packet):
        alpha = ALPHA[row["degree"]]
        supported = [c for c in row["chains"] if fraction(c["inclusion"]) > 0]
        questions.append(
            {
                **row,
                "unsupported_observed_terms": len(row["chains"]) - len(supported),
                "estimates": {
                    "raw": fw(alpha * sum((fraction(c["weight"]) for c in row["chains"]), F())),
                    "joint_supported": fw(
                        alpha
                        * sum(
                            (fraction(c["weight"]) / fraction(c["inclusion"]) for c in supported),
                            F(),
                        )
                    ),
                },
            }
        )
    return {
        "mask": mask,
        "probability": fw(masses[mask]),
        "possible": bool(masses[mask]),
        "record": copy.deepcopy(packet["record"]),
        "packet_sha256": digest(packet),
        "questions": questions,
    }


def independent_geometry(source):
    points = [tuple(map(fraction, p)) for p in source["coordinates"]]
    cells = source["cells"]
    result = []
    for probe in source["probes"]:
        a, b = probe["source"], probe["target"]
        au, av = points[a]
        bu, bv = points[b]
        query = (au, bu, av, bv)
        v = area(query)
        clips = [clipped(tuple(map(fraction, c["bounds"])), query) for c in cells]
        hs = [area(c) for c in clips]
        assert sum(hs, F()) == v
        pair_rows = []
        pg = F()
        k = cross = diag = F()
        for i, ci in enumerate(cells):
            u, x = points[ci["event"]]
            in_i = au < u < bu and av < x < bv
            for j, cj in enumerate(cells):
                y, z = points[cj["event"]]
                precedes = u < y and x < z
                in_j = au < y < bu and av < z < bv
                hprod = hs[i] * hs[j]
                if hs[i] == 0 or hs[j] == 0:
                    integral = F()
                else:
                    ai, bi, ci0, di = clips[i]
                    aj, bj, cj0, dj = clips[j]
                    integral = (
                        directed_integral(ai, bi, aj, bj) * directed_integral(ci0, di, cj0, dj) / 4
                    )
                if i == j:
                    assert integral == hs[i] * hs[i] / 4
                    diag += integral
                else:
                    cross += integral
                    if precedes:
                        k += hprod
                if precedes and in_i and in_j:
                    pg += area(tuple(map(fraction, ci["bounds"]))) * area(
                        tuple(map(fraction, cj["bounds"]))
                    )
                pair_rows.append(
                    {
                        "first": ci["event"],
                        "second": cj["event"],
                        "representative_precedes": precedes,
                        "clipped_product": fw(hprod),
                        "causal_integral": fw(integral),
                    }
                )
        continuum = v * v / 4
        assert cross + diag == continuum
        errors = (pg - k, k - cross, -diag)
        assert sum(errors, F()) == pg - continuum
        result.append(
            {
                "probe": probe["name"],
                "volume": fw(v),
                "cell_clips": [
                    {"event": c["event"], "volume": fw(h)} for c, h in zip(cells, hs, strict=True)
                ],
                "pair_cells": pair_rows,
                "pair_discrepancy": {
                    "geometric_target": fw(pg),
                    "clipped_order_sum": fw(k),
                    "cross_cell_integral": fw(cross),
                    "within_cell_integral": fw(diag),
                    "continuum_pair": fw(continuum),
                    "boundary_error": fw(errors[0]),
                    "cross_order_error": fw(errors[1]),
                    "omission_error": fw(errors[2]),
                    "total_error": fw(pg - continuum),
                },
            }
        )
    return result


def independent_case(case_id, level, source, design):
    assert source["past"] == independent_order(source)
    geometric = {c["event"]: area(tuple(map(fraction, c["bounds"]))) for c in source["cells"]}
    assert all(fw(geometric[c["event"]]) == c["geometric_mark"] for c in source["cells"])
    geometry = independent_geometry(source)
    masses = list(map(fraction, design["mask_probabilities"]))
    full = packet_of(source, design, len(masses) - 1)
    population = []
    for row in chain_rows(full):
        degree = row["degree"]
        alpha = ALPHA[degree]
        v = fraction(next(q["volume"] for q in geometry if q["probe"] == row["probe"]))
        supplied = sum((fraction(c["weight"]) for c in row["chains"]), F()) * alpha
        g = F()
        for c in row["chains"]:
            product = F(1)
            for event in c["vertices"]:
                product *= geometric[event]
            g += alpha * product
        continuum = (F(1, 2), -v / 4, v * v / 32)[degree]
        unsupported = [c["vertices"] for c in row["chains"] if fraction(c["inclusion"]) == 0]
        supported = alpha * sum(
            (fraction(c["weight"]) for c in row["chains"] if fraction(c["inclusion"]) > 0), F()
        )
        population.append(
            {
                **row,
                "scale": fw(alpha),
                "supplied_target": fw(supplied),
                "geometric_target": fw(g),
                "continuum_target": fw(continuum),
                "supported_target": fw(supported),
                "unsupported_chains": unsupported,
                "annotation_error": fw(supplied - g),
                "quadrature_error": fw(g - continuum),
                "full_target_supported": not unsupported,
            }
        )
    samples = [independent_observe(packet_of(source, design, mask)) for mask in range(len(masses))]
    moments = {}
    for method in METHODS:
        vectors = [[fraction(q["estimates"][method]) for q in s["questions"]] for s in samples]
        qn = len(population)
        means = [
            sum((p * r[i] for p, r in zip(masses, vectors, strict=True)), F()) for i in range(qn)
        ]
        covariance = [
            [
                sum(
                    (
                        p * (r[i] - means[i]) * (r[j] - means[j])
                        for p, r in zip(masses, vectors, strict=True)
                    ),
                    F(),
                )
                for j in range(qn)
            ]
            for i in range(qn)
        ]
        biases = [means[i] - fraction(q["supplied_target"]) for i, q in enumerate(population)]
        errors = []
        for i, q in enumerate(population):
            annotation = fraction(q["annotation_error"])
            quadrature = fraction(q["quadrature_error"])
            total = means[i] - fraction(q["continuum_target"])
            assert total == biases[i] + annotation + quadrature
            errors.append(
                {
                    "probe": q["probe"],
                    "degree": q["degree"],
                    "sampling_bias": fw(biases[i]),
                    "annotation_error": fw(annotation),
                    "quadrature_error": fw(quadrature),
                    "total_error": fw(total),
                }
            )
        moments[method] = {
            "mean": list(map(fw, means)),
            "bias": list(map(fw, biases)),
            "covariance": [list(map(fw, row)) for row in covariance],
            "errors": errors,
        }
    pi = inclusions(masses)
    supported = [[c for c in q["chains"] if fraction(c["inclusion"]) > 0] for q in population]
    union = []
    pairs = zeros = max_size = 0
    for i, left in enumerate(supported):
        matrixrow = []
        for j, right in enumerate(supported):
            value = F()
            for a in left:
                for b in right:
                    support = a["eligible_mask"] | b["eligible_mask"]
                    pairs += 1
                    zeros += pi[support] == 0
                    max_size = max(max_size, support.bit_count())
                    value += (
                        fraction(a["weight"])
                        * fraction(b["weight"])
                        * (pi[support] / (fraction(a["inclusion"]) * fraction(b["inclusion"])) - 1)
                    )
            matrixrow.append(
                fw(ALPHA[population[i]["degree"]] * ALPHA[population[j]["degree"]] * value)
            )
        union.append(matrixrow)
    assert union == moments["joint_supported"]["covariance"]
    assert moments["joint_supported"]["mean"] == [q["supported_target"] for q in population]
    return {
        "case_id": case_id,
        "level": level,
        "source": copy.deepcopy(source),
        "design": copy.deepcopy(design),
        "geometry": geometry,
        "population": population,
        "samples": samples,
        "moments": moments,
        "union_covariance": union,
        "counts": {
            "mask_rows": len(samples),
            "positive_rows": sum(s["possible"] for s in samples),
            "questions": len(population),
            "source_chain_terms": sum(len(q["chains"]) for q in population),
            "observed_chain_terms": sum(len(q["chains"]) for s in samples for q in s["questions"]),
            "ordered_supported_chain_pairs": pairs,
            "zero_union_pairs": zeros,
            "max_union_size": max_size,
        },
    }


@pytest.mark.parametrize(
    "bounds,expected",
    [
        ((0, 1, 2, 3), F(1)),
        ((2, 3, 0, 1), F(0)),
        ((0, 1, 0, 1), F(1, 2)),
        ((0, 2, 1, 3), F(7, 2)),
        ((1, 3, 0, 2), F(1, 2)),
        ((-2, 0, -1, 1), F(7, 2)),
        ((0, 1, 1, 2), F(1)),
        ((1, 2, 0, 1), F(0)),
        ((0, 0, 0, 1), F(0)),
        ((0, 1, 1, 1), F(0)),
        ((F(1, 3), F(2, 3), F(1, 2), F(5, 6)), F(7, 72)),
    ],
)
def test_directed_integral_exact_hands_and_complement_translation_scaling(
    engines, bounds, expected
):
    a, b, c, d = map(F, bounds)
    assert directed_integral(a, b, c, d) == expected
    for module in engines:
        actual = module.causal_area(a, b, c, d)
        assert actual == expected
        assert actual + module.causal_area(c, d, a, b) == (b - a) * (d - c)
        assert module.causal_area(a - 7, b - 7, c - 7, d - 7) == expected
        assert module.causal_area(3 * a, 3 * b, 3 * c, 3 * d) == 9 * expected


@pytest.mark.parametrize("values", [(1, 0, 0, 1), (0, 1, 1, 0), (0.0, 1, 0, 1), (False, 1, 0, 1)])
def test_directed_integral_basic_endpoint_consistency_fails_explicitly(engines, values):
    for module in engines:
        with pytest.raises(ValueError):
            module.causal_area(*values)


@pytest.mark.parametrize("four", [False, True])
@pytest.mark.parametrize("design_name", ["identity", "iid_half", "all_or_none", "singleton"])
def test_synthetic_complete_geometry_integrals_support_covariance_and_chain_wires(
    engines, four, design_name
):
    source = synthetic_source(four)
    design = design_of(len(source["eligible"]), design_name)
    expected = independent_case("synthetic", "test", source, design)
    for module in engines:
        before = wire([source, design])
        actual = module.build_case("synthetic", "test", source, design)
        assert wire(actual) == wire(expected) and wire([source, design]) == before
    if four and design_name == "iid_half":
        assert expected["counts"]["max_union_size"] == 4
    if design_name == "singleton":
        q = expected["population"][2]
        assert q["unsupported_chains"] and not q["full_target_supported"]
        assert expected["moments"]["joint_supported"]["mean"][2] == [0, 1]
        assert expected["moments"]["joint_supported"]["bias"][2] == fw(
            -fraction(q["supplied_target"])
        )
        assert expected["moments"]["joint_supported"]["covariance"][2][2] == [0, 1]


def test_nonzero_cross_order_and_omission_errors_cancel_without_becoming_same_mechanism(engines):
    s = synthetic_source()
    for module in engines:
        result = module.build_case("synthetic", "test", s, design_of(2, "identity"))
        d = result["geometry"][0]["pair_discrepancy"]
        assert d["cross_order_error"] == [1, 32] and d["omission_error"] == [-1, 32]
        assert d["total_error"] == [0, 1] and d["boundary_error"] == [0, 1]
        rows = result["geometry"][0]["pair_cells"]
        assert len(rows) == 4 and rows[0]["causal_integral"] == rows[3]["causal_integral"] == [
            1,
            64,
        ]
        assert rows[1]["causal_integral"] == [1, 32] and rows[2]["causal_integral"] == [0, 1]


def test_zero_marker_empty_chain_and_zero_probability_pair_omission_are_explicit(engines):
    source = synthetic_source()
    design = design_of(2, "singleton")
    packet = packet_of(source, design, 3)
    for module in engines:
        a = module.observe(packet)
        assert wire(a) == wire(independent_observe(packet))
        assert not a["possible"] and a["probability"] == [0, 1]
        assert a["questions"][0]["chains"] == [
            {"vertices": [], "eligible_mask": 0, "inclusion": [1, 1], "weight": [1, 1]}
        ]
        assert [c["vertices"] for c in a["questions"][1]["chains"]] == [[1], [3]]
        assert [c["vertices"] for c in a["questions"][2]["chains"]] == [[1, 3]]
        assert all(2 not in c["vertices"] for q in a["questions"] for c in q["chains"])
        assert a["questions"][2]["unsupported_observed_terms"] == 1
        assert a["questions"][2]["estimates"] == {"raw": [1, 36], "joint_supported": [0, 1]}


def test_observer_does_not_read_hidden_source_or_include_incomparable_pairs(engines, monkeypatch):
    source = synthetic_source()
    design = design_of(2, "iid_half")
    p = packet_of(source, design, 3)
    p["record"]["past"] = [[], [0], [0], [0], [0, 1, 2, 3]]
    expected = wire(independent_observe(p))
    assert not independent_observe(p)["questions"][2]["chains"]

    def forbidden(*args, **kwargs):
        raise RuntimeError("private mathematical engine read a hidden artifact")

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
            assert wire(module.observe(p)) == expected
            assert wire(module.build_case("synthetic", "test", source, design)) == wire(
                independent_case("synthetic", "test", source, design)
            )


def test_record_and_source_outputs_are_detached(engines):
    s = synthetic_source()
    d = design_of(2, "iid_half")
    p = packet_of(s, d, 3)
    for module in engines:
        before = wire(p)
        a, b = module.observe(p), module.observe(p)
        wanted = wire(b)
        a["record"]["marks"][0]["volume"][0] = -1
        a["questions"][1]["chains"][0]["weight"][0] = -1
        assert wire(p) == before and wire(b) == wanted and wire(module.observe(p)) == wanted
        case = module.build_case("synthetic", "test", s, d)
        case["source"]["cells"][0]["supplied_mark"][0] = -1
        assert s["cells"][0]["supplied_mark"] == [1, 3]


def test_reverse_ID_integration_does_not_require_representative_comparability(engines):
    source = {
        "name": "synthetic_reverse",
        "coordinates": [
            rect(p) for p in ((0, 0), (F(3, 4), F(1, 10)), (F(1, 4), F(9, 10)), (1, 1))
        ],
        "past": [],
        "fixed": [0, 3],
        "eligible": [1, 2],
        "probes": [{"name": "whole", "source": 0, "target": 3}],
        "cells": [
            {
                "event": 1,
                "bounds": rect((F(1, 2), 1, 0, 1)),
                "geometric_mark": [1, 4],
                "supplied_mark": [1, 4],
            },
            {
                "event": 2,
                "bounds": rect((0, F(1, 2), 0, 1)),
                "geometric_mark": [1, 4],
                "supplied_mark": [1, 4],
            },
        ],
        "mark_kind": "geometric_cell_volume",
    }
    source["past"] = independent_order(source)
    design = design_of(2, "identity")
    expected = independent_case("reverse", "test", source, design)
    rows = expected["geometry"][0]["pair_cells"]
    assert [(r["first"], r["second"]) for r in rows] == [(1, 1), (1, 2), (2, 1), (2, 2)]
    assert rows[2]["causal_integral"] == [1, 32] and not rows[2]["representative_precedes"]
    assert (
        expected["population"][2]["chains"] == []
        and expected["population"][2]["full_target_supported"]
    )
    for module in engines:
        assert wire(module.build_case("reverse", "test", source, design)) == wire(expected)


def test_noncausal_record_has_no_empty_chain_or_fabricated_constant_coefficient(engines):
    packet = packet_of(synthetic_source(), design_of(2, "identity"), 3)
    packet["record"]["past"] = [[] for _ in packet["record"]["kept"]]
    for module in engines:
        actual = module.observe(packet)
        assert wire(actual) == wire(independent_observe(packet))
        assert all(
            not q["chains"] and q["estimates"] == {"raw": [0, 1], "joint_supported": [0, 1]}
            for q in actual["questions"]
        )


@pytest.mark.parametrize(
    "kind",
    [
        "extra",
        "coordinates",
        "normalization",
        "missing_fixed",
        "nontransitive",
        "missing_mark",
        "fixed_mark",
        "zero_mark",
    ],
)
def test_basic_private_packet_consistency_errors_fail_explicitly(engines, kind):
    p = packet_of(synthetic_source(), design_of(2, "identity"), 3)
    if kind in ("extra", "coordinates"):
        p[kind] = []
    elif kind == "normalization":
        p["mask_probabilities"][-1] = [1, 2]
    elif kind == "missing_fixed":
        p["record"]["kept"].pop(0)
    elif kind == "nontransitive":
        p["record"]["past"][-1] = [2, 3]
    elif kind == "missing_mark":
        p["record"]["marks"].pop()
    elif kind == "fixed_mark":
        p["record"]["marks"].insert(0, {"event": 0, "volume": [1, 1]})
    else:
        p["record"]["marks"][0]["volume"] = [0, 1]
    for module in engines:
        with pytest.raises(ValueError):
            module.observe(p)


@pytest.mark.parametrize("kind", ["order", "area", "interiority", "overlap", "zero_mark"])
def test_source_area_order_and_cell_consistency_are_recomputed(engines, kind):
    source = synthetic_source()
    if kind == "order":
        source["past"][-1] = [0]
    elif kind == "area":
        source["cells"][0]["geometric_mark"] = [1, 3]
    elif kind == "interiority":
        source["coordinates"][1] = rect((0, F(1, 4)))
        source["past"] = independent_order(source)
    elif kind == "overlap":
        source["cells"][0]["bounds"][1] = [3, 4]
        source["cells"][0]["geometric_mark"] = [3, 8]
    else:
        source["cells"][0]["supplied_mark"] = [0, 1]
    for module in engines:
        with pytest.raises(ValueError):
            module.build_case("bad", "test", source, design_of(2, "identity"))


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


@pytest.fixture(scope="session")
def ah_cases(runner):
    path = HERE.parent / "qr-05ah-boundary-refinement-2026-09-07" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert (
        len(raw) == 14297174
        and hashlib.sha256(raw).hexdigest()
        == "49b911c74a2e1428cb3b378ec2bf33c77feb80ab8cab213a26cd005531429bb8"
    )
    cases = json.loads(raw)["suite"]["cases"]
    assert len(cases) == 27 and sum(len(c["samples"]) for c in cases) == 4032
    assert wire(runner.load_inputs()) == wire(cases)
    return cases


@pytest.fixture(scope="session")
def expected_cases(ah_cases):
    return [independent_case(c["case_id"], c["level"], c["source"], c["design"]) for c in ah_cases]


@pytest.mark.fixed
@pytest.mark.parametrize("index", range(27))
def test_fixed_all_twenty_seven_complete_private_engine_cases(
    index, engines, ah_cases, expected_cases
):
    old = ah_cases[index]
    for module in engines:
        before = wire([old["source"], old["design"]])
        actual = module.build_case(old["case_id"], old["level"], old["source"], old["design"])
        assert wire(actual) == wire(expected_cases[index])
        assert wire([old["source"], old["design"]]) == before


def scale_geometry(geometry, factor):
    result = copy.deepcopy(geometry)
    for q in result:
        q["volume"] = fw(fraction(q["volume"]) * factor)
        for c in q["cell_clips"]:
            c["volume"] = fw(fraction(c["volume"]) * factor)
        for pair in q["pair_cells"]:
            for key in ("clipped_product", "causal_integral"):
                pair[key] = fw(fraction(pair[key]) * factor**2)
        q["pair_discrepancy"] = {
            k: fw(fraction(v) * factor**2) for k, v in q["pair_discrepancy"].items()
        }
    return result


def scale_questions(questions, factor, population=False):
    result = copy.deepcopy(questions)
    for q in result:
        f = factor ** q["degree"]
        for c in q["chains"]:
            c["weight"] = fw(fraction(c["weight"]) * f)
        if population:
            for key in (
                "supplied_target",
                "geometric_target",
                "continuum_target",
                "supported_target",
                "annotation_error",
                "quadrature_error",
            ):
                q[key] = fw(fraction(q[key]) * f)
        else:
            q["estimates"] = {k: fw(fraction(v) * f) for k, v in q["estimates"].items()}
    return result


def scale_moments(moments, factor):
    result = copy.deepcopy(moments)
    for m in result.values():
        degrees = [q["degree"] for q in m["errors"]]
        for key in ("mean", "bias"):
            m[key] = [fw(fraction(v) * factor**d) for v, d in zip(m[key], degrees, strict=True)]
        m["covariance"] = [
            [fw(fraction(v) * factor ** (a + b)) for v, b in zip(row, degrees, strict=True)]
            for row, a in zip(m["covariance"], degrees, strict=True)
        ]
        for row in m["errors"]:
            for key in ("sampling_bias", "annotation_error", "quadrature_error", "total_error"):
                row[key] = fw(fraction(row[key]) * factor ** row["degree"])
    return result


def scaled_samples(case, factor):
    result = copy.deepcopy(case["samples"])
    for sample in result:
        p = packet_of(case["source"], case["design"], sample["mask"])
        for c in p["record"]["marks"]:
            c["volume"] = fw(fraction(c["volume"]) * factor)
        sample["record"] = p["record"]
        sample["packet_sha256"] = digest(p)
        sample["questions"] = scale_questions(sample["questions"], factor)
    return result


def independent_controls(cases):
    by = {(c["source"]["name"], c["level"], c["design"]["name"]): c for c in cases}
    result = {"refinement": [], "boost": [], "dilation": [], "stale_marks": []}
    for source in FAMILIES:
        for level in range(2):
            a, b = (by[source, f"l{k}", "identity"] for k in (level, level + 1))
            for i, (left, right) in enumerate(zip(a["geometry"], b["geometry"], strict=True)):
                p, q = a["population"][3 * i + 2], b["population"][3 * i + 2]
                result["refinement"].append(
                    {
                        "source": source,
                        "coarse": a["level"],
                        "fine": b["level"],
                        "probe": left["probe"],
                        "geometric_coefficient_change": fw(
                            fraction(q["geometric_target"]) - fraction(p["geometric_target"])
                        ),
                        "signed_error_change": fw(
                            fraction(q["quadrature_error"]) - fraction(p["quadrature_error"])
                        ),
                        "absolute_error_change": fw(
                            abs(fraction(q["quadrature_error"]))
                            - abs(fraction(p["quadrature_error"]))
                        ),
                        "within_cell_change": fw(
                            fraction(right["pair_discrepancy"]["within_cell_integral"])
                            - fraction(left["pair_discrepancy"]["within_cell_integral"])
                        ),
                    }
                )
    for level in ("l0", "l1", "l2"):
        base = by["grid", level, "identity"]
        for key, name, factor in (("boost", "boost", F(1)), ("dilation", "dilate", F(4))):
            moved = by[name, level, "identity"]
            assert wire(base["design"]) == wire(moved["design"]) and wire(
                base["source"]["past"]
            ) == wire(moved["source"]["past"])
            result[key].append(
                {
                    "level": level,
                    "volume_factor": fw(factor),
                    "full_geometry_scaling": wire(scale_geometry(base["geometry"], factor))
                    == wire(moved["geometry"]),
                    "full_population_scaling": wire(
                        scale_questions(base["population"], factor, True)
                    )
                    == wire(moved["population"]),
                    "sample_coefficients_scaling": wire(scaled_samples(base, factor))
                    == wire(moved["samples"]),
                    "full_moment_scaling": wire(scale_moments(base["moments"], factor))
                    == wire(moved["moments"]),
                }
            )
        stale = by["warp_stale", level, "identity"]
        result["stale_marks"].append(
            {
                "level": level,
                "public_samples_equal_grid": wire(stale["samples"]) == wire(base["samples"]),
                "geometric_pair_data_equal_warp": wire(stale["geometry"])
                == wire(by["warp", level, "identity"]["geometry"]),
            }
        )
    return result


def independent_bridges(cases, previous):
    for c, old in zip(cases, previous, strict=True):
        assert c["case_id"] == old["case_id"] and c["level"] == old["level"]
        assert wire(c["source"]) == wire(old["source"]) and wire(c["design"]) == wire(old["design"])
        for s, t in zip(c["samples"], old["samples"], strict=True):
            assert wire(s["record"]) == wire(t["problem"]["record"])
            assert all(s[k] == t["analysis"][k] for k in ("mask", "probability", "possible"))
            p = {
                k: t["problem"][k]
                for k in (
                    "frame_size",
                    "fixed",
                    "eligible",
                    "probes",
                    "mask_probabilities",
                    "record",
                )
            }
            assert s["packet_sha256"] == digest(p)
            for i, oldq in enumerate(t["analysis"]["questions"]):
                q = s["questions"][3 * i + 1]
                assert q["probe"] == oldq["probe"]
                assert [
                    {
                        "event": ch["vertices"][0],
                        "volume": ch["weight"],
                        "inclusion": ch["inclusion"],
                    }
                    for ch in q["chains"]
                ] == oldq["observed_cells"]
                for method, oldmethod in (("raw", "raw"), ("joint_supported", "inclusion")):
                    assert q["estimates"][method] == fw(-fraction(oldq["estimates"][oldmethod]) / 4)
        for i, pop in enumerate(old["population"]):
            q, g = c["population"][3 * i + 1], c["geometry"][i]
            projected = {
                "probe": q["probe"],
                "members": [ch["vertices"][0] for ch in q["chains"]],
                "overlaps": g["cell_clips"],
            }
            projected.update(
                {
                    target: fw(-4 * fraction(q[current]))
                    for target, current in (
                        ("supplied_target", "supplied_target"),
                        ("geometric_target", "geometric_target"),
                        ("continuum_volume", "continuum_target"),
                        ("annotation_error", "annotation_error"),
                        ("quadrature_error", "quadrature_error"),
                    )
                }
            )
            assert wire(projected) == wire(pop)
        for method, oldmethod in (("raw", "raw"), ("joint_supported", "inclusion")):
            a, b = c["moments"][method], old["moments"][oldmethod]
            for key in ("mean", "bias"):
                assert [a[key][3 * i + 1] for i in range(5)] == [
                    fw(-fraction(v) / 4) for v in b[key]
                ]
            assert [
                [a["covariance"][3 * i + 1][3 * j + 1] for j in range(5)] for i in range(5)
            ] == [[fw(fraction(v) / 16) for v in row] for row in b["covariance"]]
    return {
        "AH_case_ids": [c["case_id"] for c in cases],
        "AH_sources_designs_equal": True,
        "AH_sample_records_equal": True,
        "AH_linear_populations_equal": True,
        "AH_raw_inclusion_means_covariances_equal": True,
        "AF_math_replayed": False,
        "other_prior_math_replayed": False,
    }


@pytest.fixture(scope="session")
def expected_suite(expected_cases, ah_cases):
    counts = {"cases": len(expected_cases)}
    for key in expected_cases[0]["counts"]:
        values = [c["counts"][key] for c in expected_cases]
        counts[key] = max(values) if key == "max_union_size" else sum(values)
    return {
        "cases": expected_cases,
        "controls": independent_controls(expected_cases),
        "prior_bridges": independent_bridges(expected_cases, ah_cases),
        "totals": counts,
        "scope": dict.fromkeys(
            (
                "generic_production_API_hardened",
                "unknown_geometry_reconstructed",
                "marks_authenticated",
                "kernel_error_bound_established",
                "continuum_limit_established",
                "cross_level_observation_transport_proved",
                "quantum_channel_constructed",
                "gravity_derived",
                "empirical_data_used",
                "ret_integration_tested",
            ),
            False,
        ),
    }


@pytest.mark.fixed
def test_fixed_complete_suite_controls_and_all_AH_projections(runner, expected_suite, ah_cases):
    actual = runner.assemble_suite(expected_suite["cases"], ah_cases)
    assert wire(actual) == wire(expected_suite)
    runner.verify_suite(actual, expected_suite)


@pytest.mark.fixed
@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_route_orchestration_uses_declared_engines_and_preserves_inputs(
    runner, expected_suite, ah_cases, monkeypatch, route
):
    # Real build_case mathematics is independently compared for all27 cases above.
    # Here cached exact outputs isolate orchestration without repeating that work.
    calls = []
    by = {c["case_id"]: c for c in expected_suite["cases"]}

    def loader(name):
        def build(case_id, level, source, design):
            assert name in ("primary", "reference")
            old = next(c for c in ah_cases if c["case_id"] == case_id)
            assert (
                level == old["level"]
                and wire(source) == wire(old["source"])
                and wire(design) == wire(old["design"])
            )
            calls.append((name, case_id))
            return copy.deepcopy(by[case_id])

        return SimpleNamespace(build_case=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    monkeypatch.setattr(runner, "load_inputs", lambda: ah_cases)
    assert wire(runner.run_suite(route)) == wire(expected_suite)
    names = ("primary", "reference") if route == "compare" else (route,)
    assert calls == [(name, c["case_id"]) for c in ah_cases for name in names]


def at_path(tree, path):
    for key in path:
        tree = tree[key]
    return tree


def add_fraction(tree, path):
    return replaced(tree, path, fw(fraction(at_path(tree, path)) + 1))


@pytest.mark.fixed
def test_fixed_finite_result_corruptions_cover_geometry_directions_support_and_covariance(
    runner, expected_cases
):
    original = expected_cases[2]
    pair = original["geometry"][0]["pair_cells"][1]
    changes = [
        add_fraction(original, ("source", "coordinates", 0, 0)),
        add_fraction(original, ("source", "cells", 0, "geometric_mark")),
        add_fraction(original, ("geometry", 0, "volume")),
        add_fraction(original, ("geometry", 0, "cell_clips", 0, "volume")),
        replaced(
            original,
            ("geometry", 0, "pair_cells", 1),
            {**pair, "first": pair["second"], "second": pair["first"]},
        ),
        replaced(
            original,
            ("geometry", 0, "pair_cells", 1, "representative_precedes"),
            not pair["representative_precedes"],
        ),
        add_fraction(original, ("geometry", 0, "pair_cells", 0, "causal_integral")),
        add_fraction(original, ("geometry", 0, "pair_discrepancy", "omission_error")),
        add_fraction(original, ("population", 2, "supported_target")),
        replaced(
            original,
            ("population", 2, "unsupported_chains"),
            original["population"][2]["unsupported_chains"] + [[]],
        ),
        replaced(
            original,
            ("population", 2, "full_target_supported"),
            not original["population"][2]["full_target_supported"],
        ),
        add_fraction(original, ("population", 2, "annotation_error")),
        add_fraction(original, ("moments", "joint_supported", "bias", 2)),
        add_fraction(original, ("moments", "joint_supported", "covariance", 1, 2)),
        add_fraction(original, ("union_covariance", 1, 2)),
        replaced(
            original,
            ("samples", -1, "questions", 2, "unsupported_observed_terms"),
            original["samples"][-1]["questions"][2]["unsupported_observed_terms"] + 1,
        ),
        replaced(original, ("samples", -1, "packet_sha256"), "0" * 64),
        replaced(original, ("counts", "max_union_size"), original["counts"]["max_union_size"] + 1),
    ]
    assert len(changes) == 18
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.verify_suite(bad, original)
    assert wire(original) == before


@pytest.mark.fixed
def test_fixed_suite_control_scope_and_aggregate_corruptions_are_nonvacuous(runner, expected_suite):
    original = expected_suite
    changes = [
        add_fraction(original, ("controls", "refinement", 0, "signed_error_change")),
        replaced(original, ("controls", "dilation", 0, "full_geometry_scaling"), False),
        replaced(original, ("controls", "stale_marks", 0, "geometric_pair_data_equal_warp"), False),
        replaced(original, ("prior_bridges", "AH_linear_populations_equal"), False),
        replaced(original, ("scope", "kernel_error_bound_established"), True),
        replaced(original, ("totals", "max_union_size"), original["totals"]["max_union_size"] + 1),
    ]
    assert len(changes) == 6
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.verify_suite(bad, original)
    assert wire(original) == before


@pytest.mark.fixed
def test_fixed_historical_projection_corruptions_are_checked_not_merely_flagged(
    runner, expected_cases, ah_cases
):
    original = ah_cases[0]
    changes = [
        add_fraction(original, ("source", "coordinates", 0, 0)),
        add_fraction(original, ("samples", -1, "analysis", "probability")),
        add_fraction(
            original, ("samples", -1, "analysis", "questions", 0, "observed_cells", 0, "volume")
        ),
        add_fraction(original, ("population", 0, "overlaps", 0, "volume")),
        add_fraction(original, ("moments", "inclusion", "covariance", 0, 1)),
        add_fraction(original, ("moments", "raw", "bias", 0)),
    ]
    assert len(changes) == 6
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.ah_bridges(expected_cases, [bad, *ah_cases[1:]])
    assert wire(original) == before
