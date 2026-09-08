"""Bounded independent checks for the private query-reuse diagnostic.

Only tests marked fixed consume authenticated AL cases. Collection and generic
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
from math import comb
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
        load("_qr05am_test_primary", "kernel.py"),
        load("_qr05am_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05am_test_runner", "study.py")


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


def affine_length(a, b, left, right, predecessor):
    def value(y):
        return max(F(), min(b - a, y - a if predecessor else b - y))

    slope = (value(right) - value(left)) / (right - left)
    return value(left) - slope * left, slope


def integral_polynomial(coefficients, left, right):
    return sum(
        (
            c * (right ** (power + 1) - left ** (power + 1)) / (power + 1)
            for power, c in enumerate(coefficients)
        ),
        F(),
    )


def triple_integral(a, b, c, d, e, f):
    # Direct shared-middle polynomial integration is independent of the AM
    # primary's Gram contractions and the reference's Simpson evaluations.
    assert a <= b and c <= d and e <= f
    total = F()
    for left, right in pairwise(sorted({a, b, c, d, e, f})):
        if c <= left < right <= d:
            l0, l1 = affine_length(a, b, left, right, True)
            r0, r1 = affine_length(e, f, left, right, False)
            total += integral_polynomial((l0 * r0, l0 * r1 + l1 * r0, l1 * r1), left, right)
    return total


def ratio(n, d):
    return n / d if d else None


def nullable(value):
    return fw(value) if value is not None else None


POWERS = tuple((i, j) for i in range(3) for j in range(3))
BASIS = ((0, 0), (1, 0), (0, 1), (1, 1))


def power_integral(a, b, p):
    # Factored endpoint-power sum: independent of subtracting antiderivatives
    # and of the reference's tensor-Simpson evaluations.
    return (b - a) * sum((a**i * b ** (p - i) for i in range(p + 1)), F()) / (p + 1)


def raw_moments(bounds):
    a, b, c, d = bounds
    return [power_integral(a, b, i) * power_integral(c, d, j) / 2 for i, j in POWERS]


def gram(moments):
    return [[moments[3 * (i + k) + j + l] for k, l in BASIS] for i, j in BASIS]


def coefficients(endpoint, tile, incoming):
    if area(endpoint) == 0:
        return [F()] * 4
    lines = []
    for axis in (0, 2):
        a, b = endpoint[axis : axis + 2]
        left, right = tile[axis : axis + 2]
        # Two strict interior nodes, not the engine's endpoint/corner recipe.
        x, y = (2 * left + right) / 3, (left + 2 * right) / 3

        def length(z, a=a, b=b):
            return max(F(), min(b - a, z - a if incoming else b - z))

        slope = (length(y) - length(x)) / (y - x)
        lines.append((length(x) - slope * x, slope))
    return [lines[0][i] * lines[1][j] / 2 for i, j in BASIS]


def mean_integral(coeff, moments):
    return sum((x * moments[3 * i + j] for x, (i, j) in zip(coeff, BASIS, strict=True)), F())


def product_integral(left, right, moments):
    # Convolve the two bivariate polynomials first, then integrate the nine
    # monomials. No flattened 4x4 production contraction is reused.
    poly = {(i, j): F() for i, j in POWERS}
    for x, (i, j) in zip(left, BASIS, strict=True):
        for y, (k, l) in zip(right, BASIS, strict=True):
            poly[i + k, j + l] += x * y
    return sum((poly[key] * value for key, value in zip(POWERS, moments, strict=True)), F())


def centered(left, right, mean_left, mean_right, moments):
    a, b = left.copy(), right.copy()
    a[0] -= mean_left
    b[0] -= mean_right
    return product_integral(a, b, moments)


def transported_moments(values, alpha, beta, du=F(), dv=F()):
    moments = dict(zip(POWERS, values, strict=True))
    return [
        alpha
        * beta
        * sum(
            (
                F(comb(i, r) * comb(j, s))
                * alpha**r
                * du ** (i - r)
                * beta**s
                * dv ** (j - s)
                * moments[r, s]
                for r in range(i + 1)
                for s in range(j + 1)
            ),
            F(),
        )
        for i, j in POWERS
    ]


def transported_coefficients(values, alpha, beta, du=F(), dv=F()):
    result = {key: F() for key in BASIS}
    for value, (i, j) in zip(values, BASIS, strict=True):
        for r in range(i + 1):
            for s in range(j + 1):
                result[r, s] += (
                    value
                    * alpha
                    * beta
                    * comb(i, r)
                    * comb(j, s)
                    * (-du) ** (i - r)
                    * (-dv) ** (j - s)
                    / alpha**i
                    / beta**j
                )
    return [result[key] for key in BASIS]


def endpoint(value):
    return tuple(map(fraction, value)) if value is not None else None


def split_bounds(tile, endpoints):
    cuts = []
    for axis in (0, 2):
        lo, hi = tile[axis : axis + 2]
        cuts.append(
            sorted(
                {
                    lo,
                    hi,
                    *(
                        x
                        for e in endpoints
                        if e is not None
                        for x in e[axis : axis + 2]
                        if lo < x < hi
                    ),
                }
            )
        )
    return [(a, b, c, d) for a, b in pairwise(cuts[0]) for c, d in pairwise(cuts[1])]


def forced_coefficients(e, tile, incoming):
    if e is None:
        return [F()] * 4
    u = affine_length(*e[:2], *tile[:2], incoming)
    v = affine_length(*e[2:], *tile[2:], incoming)
    return [u[i] * v[j] / 2 for i, j in BASIS]


def admits(e, tile, incoming):
    forced = forced_coefficients(e, tile, incoming)
    if e is None:
        return True
    # Every endpoint-cut subrectangle has one exact bilinear polynomial.
    # Compare its coefficients with the old forced fit, not any integrated error.
    return all(coefficients(e, p, incoming) == forced for p in split_bounds(tile, [e]))


def fixed_queries(middle, probe):
    bounds = middle["bounds"]
    if bounds is None:
        incoming = outgoing = None
    else:
        b = endpoint(bounds)
        first = endpoint(middle["tiles"][0]["bounds"])
        k = (first[0] + first[1]) / 2
        incoming = rect((b[0], k, b[2], b[3]))
        outgoing = rect((k, b[1], b[2], b[3]))
    return [
        {"name": "whole_probe", "incoming": copy.deepcopy(probe), "outgoing": copy.deepcopy(probe)},
        {
            "name": "middle_self",
            "incoming": copy.deepcopy(bounds),
            "outgoing": copy.deepcopy(bounds),
        },
        {"name": "incoming_kink", "incoming": incoming, "outgoing": copy.deepcopy(bounds)},
        {"name": "outgoing_kink", "incoming": copy.deepcopy(bounds), "outgoing": outgoing},
        {"name": "zero_endpoint", "incoming": None, "outgoing": copy.deepcopy(bounds)},
    ]


def snapshot_problem(ucuts=(F(0), F(1)), vcuts=(F(0), F(1)), queries=None, empty=False):
    bounds = (ucuts[0], ucuts[-1], vcuts[0], vcuts[-1])
    middle = {
        "event": 9,
        "bounds": rect(bounds),
        "u_breaks": list(map(fw, ucuts)),
        "v_breaks": list(map(fw, vcuts)),
        "moments": list(map(fw, raw_moments(bounds))),
        "tiles": [
            {"bounds": rect((a, b, c, d)), "moments": list(map(fw, raw_moments((a, b, c, d))))}
            for a, b in pairwise(ucuts)
            for c, d in pairwise(vcuts)
        ],
    }
    middle["queries"] = (
        copy.deepcopy(queries) if queries is not None else fixed_queries(middle, rect(bounds))
    )
    middles = [middle]
    if empty:
        none = {
            "event": -2,
            "bounds": None,
            "u_breaks": [],
            "v_breaks": [],
            "moments": [[0, 1] for _ in range(9)],
            "tiles": [],
        }
        none["queries"] = fixed_queries(none, rect(bounds))
        middles.insert(0, none)
    return {
        "family": "synthetic",
        "contexts": [
            {"level": "level", "probe": "whole", "probe_bounds": rect(bounds), "middles": middles}
        ],
    }


def query(name, incoming, outgoing):
    return {
        "name": name,
        "incoming": rect(incoming) if incoming is not None else None,
        "outgoing": rect(outgoing) if outgoing is not None else None,
    }


def independent_query(middle, query, geometric=True):
    a, c = endpoint(query["incoming"]), endpoint(query["outgoing"])
    b = endpoint(middle["bounds"])
    h = area(b) if b is not None else F()
    oldrows, pieces, blocks, raw = [], [], [], []
    forced_left = forced_right = forced_true = F()
    for ti, tile in enumerate(middle["tiles"]):
        bounds, moments = endpoint(tile["bounds"]), list(map(fraction, tile["moments"]))
        if geometric:
            assert moments == raw_moments(bounds)
        left, right = forced_coefficients(a, bounds, True), forced_coefficients(c, bounds, False)
        ia, oa = admits(a, bounds, True), admits(c, bounds, False)
        oldrows.append(
            {
                "tile": ti,
                "incoming_admissible": ia,
                "outgoing_admissible": oa,
                "forced_incoming": list(map(fw, left)),
                "forced_outgoing": list(map(fw, right)),
            }
        )
        forced_left += mean_integral(left, moments)
        forced_right += mean_integral(right, moments)
        forced_true += product_integral(left, right, moments)
        indices = []
        children = [bounds] if ia and oa else split_bounds(bounds, [a, c])
        for box in children:
            retained = ia and oa
            m = moments.copy() if retained else raw_moments(box)
            inc, out = forced_coefficients(a, box, True), forced_coefficients(c, box, False)
            assert admits(a, box, True) and admits(c, box, False)
            indices.append(len(pieces))
            pieces.append(
                {
                    "parent": ti,
                    "bounds": copy.deepcopy(tile["bounds"]) if retained else rect(box),
                    "moments": copy.deepcopy(tile["moments"]) if retained else list(map(fw, m)),
                    "moment_source": "retained" if retained else "derived",
                    "incoming_coefficients": list(map(fw, inc)),
                    "outgoing_coefficients": list(map(fw, out)),
                }
            )
            raw.append((m, inc, out))
        summed = [sum((raw[i][0][j] for i in indices), F()) for j in range(9)]
        assert summed == moments
        blocks.append(
            {
                "parent": ti,
                "children": indices,
                "old_moments": copy.deepcopy(tile["moments"]),
                "piece_moment_sum": list(map(fw, summed)),
            }
        )
    status = (
        "empty_middle"
        if not h
        else "reuse"
        if all(r["incoming_admissible"] and r["outgoing_admissible"] for r in oldrows)
        else "refine"
    )
    jin = sum((mean_integral(inc, m) for m, inc, _ in raw), F())
    jout = sum((mean_integral(out, m) for m, _, out in raw), F())
    true = sum((product_integral(inc, out, m) for m, inc, out in raw), F())
    if geometric and h:
        direct_in = (
            directed_integral(*a[:2], *b[:2]) * directed_integral(*a[2:], *b[2:]) / 4
            if a is not None
            else F()
        )
        direct_out = (
            directed_integral(*b[:2], *c[:2]) * directed_integral(*b[2:], *c[2:]) / 4
            if c is not None
            else F()
        )
        direct_true = (
            triple_integral(*a[:2], *b[:2], *c[:2]) * triple_integral(*a[2:], *b[2:], *c[2:]) / 8
            if a is not None and c is not None
            else F()
        )
        assert (jin, jout, true) == (direct_in, direct_out, direct_true)
    p, fp = ratio(jin * jout, h), ratio(forced_left * forced_right, h)
    cent = (
        sum((centered(inc, out, jin / h, jout / h, m) for m, inc, out in raw), F()) if h else None
    )
    assert cent is None or cent == true - p
    va, vc = area(a) if a is not None else F(), area(c) if c is not None else F()
    volume = va * h * vc
    result = {
        "middle_volume": fw(h),
        "incoming_volume": fw(va),
        "outgoing_volume": fw(vc),
        "volume_product": fw(volume),
        "incoming_pair": fw(jin),
        "outgoing_pair": fw(jout),
        "causal_integral": fw(true),
        "pair_product": nullable(p),
        "conditional": nullable(ratio(true, volume)),
        "product_conditional": nullable(p / volume if volume else None),
        "middle_covariance": nullable(cent / h if h else None),
        "centered_integral": nullable(cent),
        "forced_incoming_pair": fw(forced_left),
        "forced_outgoing_pair": fw(forced_right),
        "forced_integral": fw(forced_true),
        "forced_pair_product": nullable(fp),
        "forced_conditional": nullable(ratio(forced_true, volume)),
        "forced_product_conditional": nullable(fp / volume if volume else None),
        "incoming_pair_error": fw(forced_left - jin),
        "outgoing_pair_error": fw(forced_right - jout),
        "forced_error": fw(forced_true - true),
        "reuse_incoming_pair": fw(jin) if status == "reuse" else None,
        "reuse_outgoing_pair": fw(jout) if status == "reuse" else None,
        "reuse_integral": fw(true) if status == "reuse" else None,
    }
    derived = sum(p["moment_source"] == "derived" for p in pieces)
    supported = sum(r["incoming_admissible"] and r["outgoing_admissible"] for r in oldrows)
    counts = {
        "old_tiles": len(oldrows),
        "admissible_old_tiles": supported,
        "unsupported_old_tiles": len(oldrows) - supported,
        "retained_pieces": len(pieces) - derived,
        "derived_pieces": derived,
        "replaced_old_tiles": len(oldrows) - supported,
        "moment_derivation_calls": derived,
        "forced_coefficient_vectors": 2 * len(oldrows),
        "forced_coefficient_entries": 8 * len(oldrows),
        "exact_coefficient_vectors": 2 * len(pieces),
        "exact_coefficient_entries": 8 * len(pieces),
        "new_moment_entries": 9 * derived,
        "retained_moment_entries": 9 * (len(pieces) - derived),
        "piece_bound_entries": 4 * len(pieces),
        "moment_blocks": len(blocks),
        "moment_block_entries": 18 * len(blocks),
    }
    return {
        "name": query["name"],
        "admission": status,
        "old_tiles": oldrows,
        "pieces": pieces,
        "moment_blocks": blocks,
        "result": result,
        "counts": counts,
    }


def independent_family(problem, geometric=True):
    contexts = []
    for context in problem["contexts"]:
        positives = [endpoint(m["bounds"]) for m in context["middles"] if m["bounds"] is not None]
        assert sum(map(area, positives), F()) == area(endpoint(context["probe_bounds"]))
        assert all(area(clipped(a, b)) == 0 for a, b in combinations(positives, 2))
        contexts.append(
            {
                "level": context["level"],
                "probe": context["probe"],
                "middles": [
                    {
                        "event": middle["event"],
                        "queries": [
                            independent_query(middle, q, geometric) for q in middle["queries"]
                        ],
                    }
                    for middle in context["middles"]
                ],
            }
        )
    mids = [m for context in problem["contexts"] for m in context["middles"]]
    queries = [
        q for context in contexts for middle in context["middles"] for q in middle["queries"]
    ]
    counts = {key: sum(q["counts"][key] for q in queries) for key in queries[0]["counts"]}
    positive = [q for q in queries if q["admission"] != "empty_middle"]
    counts.update(
        {
            "contexts": len(contexts),
            "middle_rows": len(mids),
            "positive_middle_rows": sum(m["bounds"] is not None for m in mids),
            "snapshot_tiles": sum(len(m["tiles"]) for m in mids),
            "snapshot_moment_entries": sum(
                len(m["moments"]) + sum(len(t["moments"]) for t in m["tiles"]) for m in mids
            ),
            "snapshot_bound_entries": sum(
                (len(m["bounds"]) if m["bounds"] is not None else 0)
                + len(m["u_breaks"])
                + len(m["v_breaks"])
                + sum(len(t["bounds"]) for t in m["tiles"])
                for m in mids
            ),
            "endpoint_bound_entries": sum(
                len(q[key])
                for m in mids
                for q in m["queries"]
                for key in ("incoming", "outgoing")
                if q[key] is not None
            ),
            "queries": len(queries),
            "empty_middle_queries": len(queries) - len(positive),
            "reuse_queries": sum(q["admission"] == "reuse" for q in queries),
            "refinement_queries": sum(q["admission"] == "refine" for q in queries),
            "positive_exact_queries": sum(
                fraction(q["result"]["causal_integral"]) > 0 for q in queries
            ),
            "forced_positive_errors": sum(
                fraction(q["result"]["forced_error"]) > 0 for q in positive
            ),
            "forced_zero_errors": sum(fraction(q["result"]["forced_error"]) == 0 for q in positive),
            "forced_negative_errors": sum(
                fraction(q["result"]["forced_error"]) < 0 for q in positive
            ),
            "refinement_forced_equalities": sum(
                q["admission"] == "refine" and q["result"]["forced_error"] == [0, 1]
                for q in queries
            ),
            "incoming_pair_disagreements": sum(
                q["result"]["incoming_pair_error"] != [0, 1] for q in positive
            ),
            "outgoing_pair_disagreements": sum(
                q["result"]["outgoing_pair_error"] != [0, 1] for q in positive
            ),
        }
    )
    return {"problem": copy.deepcopy(problem), "contexts": contexts, "counts": counts}


UNIT = (F(0), F(1), F(0), F(1))


def mixed_problem():
    kink = query("kink", (0, F(1, 4), 0, 1), UNIT)
    return snapshot_problem(
        (F(0), F(1, 2), F(1)),
        queries=[kink, {**kink, "name": "repeat"}, query("aligned", (0, F(1, 2), 0, 1), UNIT)],
    )


def failing_problem():
    return snapshot_problem(queries=[query("failing", (0, F(1, 2), 0, 1), UNIT)])


def accidental_problem():
    return snapshot_problem(queries=[query("accidental", (F(1, 4), F(3, 4), 0, 1), (2, 3, 2, 3))])


def result_query(family, index=0, middle=0):
    return family["contexts"][0]["middles"][middle]["queries"][index]


@pytest.mark.parametrize(
    "factory",
    [snapshot_problem, mixed_problem, failing_problem, accidental_problem],
    ids=["five_queries", "mixed_repeated", "failing", "accidental"],
)
def test_generic_complete_independent_family_wire(engines, factory):
    problem = factory()
    expected, before = independent_family(problem), wire(problem)
    for module in engines:
        assert wire(module.build_family(problem)) == wire(expected) and wire(problem) == before


def test_forced_old_corner_fit_fails_and_true_refinement_recovers_integral(engines):
    p = failing_problem()
    for module in engines:
        q = result_query(module.build_family(p))
        r = q["result"]
        assert q["admission"] == "refine" and q["counts"]["derived_pieces"] == 2
        assert r["incoming_pair"] == [3, 64] and r["forced_incoming_pair"] == [1, 32]
        assert r["causal_integral"] == [7, 2304] and r["forced_integral"] == [1, 576]
        assert r["forced_error"] == [-1, 768] and r["reuse_integral"] is None
        assert q["moment_blocks"][0]["old_moments"] == q["moment_blocks"][0]["piece_moment_sum"]
        assert q["old_tiles"][0]["incoming_admissible"] is False


def test_accidental_integral_equality_does_not_certify_bilinear_reuse(engines):
    p = accidental_problem()
    for module in engines:
        family = module.build_family(p)
        q = result_query(family)
        assert q["admission"] == "refine" and q["counts"]["derived_pieces"] == 3
        assert q["result"]["incoming_pair"] == q["result"]["forced_incoming_pair"] == [1, 32]
        assert q["result"]["causal_integral"] == q["result"]["forced_integral"] == [1, 64]
        assert q["result"]["forced_error"] == [0, 1] and q["result"]["reuse_integral"] is None
        assert family["counts"]["refinement_forced_equalities"] == 1


def test_reuse_runs_with_new_moment_hook_disabled_and_shared_native_inputs(engines, monkeypatch):
    p = snapshot_problem(
        (F(0), F(1, 2), F(1)),
        queries=[query("aligned", (0, F(1, 2), 0, 1), UNIT), query("self", UNIT, UNIT)],
    )
    middle = p["contexts"][0]["middles"][0]
    # Native aliases are allowed; outputs must detach rather than reject them.
    middle["queries"][1]["incoming"] = middle["bounds"]
    middle["queries"][1]["outgoing"] = middle["bounds"]
    expected, before = wire(independent_family(p)), wire(p)

    def forbidden(*args):
        raise RuntimeError("reuse secretly derived moments")

    for module in engines:
        with monkeypatch.context() as patch:
            patch.setattr(module, "derive_moments", forbidden)
            result = module.build_family(p)
        assert wire(result) == expected and wire(p) == before
        assert (
            result["counts"]["moment_derivation_calls"] == result["counts"]["derived_pieces"] == 0
        )
        assert result["counts"]["reuse_queries"] == 2


def test_only_new_children_call_hook_once_per_query_and_retained_pieces_are_unchanged(
    engines, monkeypatch
):
    p = mixed_problem()
    original = wire(p)
    expected = independent_family(p)
    for module in engines:
        calls = []
        derive = module.derive_moments

        def count(bounds, derive=derive, calls=calls):
            calls.append(copy.deepcopy(bounds))
            return derive(bounds)

        with monkeypatch.context() as patch:
            patch.setattr(module, "derive_moments", count)
            actual = module.build_family(p)
        assert wire(actual) == wire(expected) and wire(p) == original
        expected_calls = [
            piece["bounds"]
            for q in expected["contexts"][0]["middles"][0]["queries"]
            for piece in q["pieces"]
            if piece["moment_source"] == "derived"
        ]
        assert (
            calls == expected_calls
            and len(calls) == actual["counts"]["moment_derivation_calls"] == 4
        )
        for q in actual["contexts"][0]["middles"][0]["queries"]:
            for piece in q["pieces"]:
                if piece["moment_source"] == "retained":
                    old = p["contexts"][0]["middles"][0]["tiles"][piece["parent"]]
                    assert piece["bounds"] == old["bounds"] and piece["moments"] == old["moments"]
        for index, q in enumerate(p["contexts"][0]["middles"][0]["queries"]):
            one = replaced(p, ("contexts", 0, "middles", 0, "queries"), [q])
            assert wire(result_query(module.build_family(one))) == wire(result_query(actual, index))


def test_coherent_wrong_higher_old_moment_is_not_silently_regenerated(engines, monkeypatch):
    p = snapshot_problem(queries=[query("self", UNIT, UNIT)])
    bad = copy.deepcopy(p)
    delta = F(1, 100)
    middle = bad["contexts"][0]["middles"][0]
    middle["moments"][8] = middle["tiles"][0]["moments"][8] = fw(
        fraction(middle["moments"][8]) + delta
    )
    primary, reference = engines

    def forbidden(*args):
        raise RuntimeError("unexpected old moment regeneration through new-moment hook")

    with monkeypatch.context() as patch:
        patch.setattr(primary, "derive_moments", forbidden)
        actual = primary.build_family(bad)
    assert wire(actual) == wire(independent_family(bad, geometric=False))
    assert fraction(result_query(actual)["result"]["causal_integral"]) == F(1, 288) + delta / 4
    assert actual["problem"]["contexts"][0]["middles"][0]["moments"] == middle["moments"]
    with monkeypatch.context() as patch:
        patch.setattr(reference, "derive_moments", forbidden)
        with pytest.raises(ValueError):
            reference.build_family(bad)


@pytest.mark.parametrize(
    "incoming,outgoing,status",
    [
        ((F(1, 4), F(3, 4), 1, 2), UNIT, "reuse"),
        ((0, F(1, 2), 0, 1), None, "refine"),
        (None, (F(1, 2), 1, 0, 1), "refine"),
        ((-1, 0, 0, 1), UNIT, "reuse"),
        (UNIT, (1, 2, 0, 1), "reuse"),
    ],
)
def test_inactive_and_boundary_factors_do_not_mask_other_function_kinks(
    engines, incoming, outgoing, status
):
    p = snapshot_problem(queries=[query("function_test", incoming, outgoing)])
    expected = independent_family(p)
    for module in engines:
        actual = module.build_family(p)
        assert wire(actual) == wire(expected)
        assert result_query(actual)["admission"] == status
    if incoming is None or outgoing is None:
        assert result_query(expected)["result"]["forced_error"] == [0, 1]
        assert result_query(expected)["admission"] == "refine"


def test_empty_middle_keeps_raw_zero_but_divided_and_reuse_fields_null(engines):
    p = snapshot_problem(empty=True)
    expected = independent_family(p)
    for module in engines:
        actual = module.build_family(p)
        assert wire(actual) == wire(expected)
        for q in actual["contexts"][0]["middles"][0]["queries"]:
            assert (
                q["admission"] == "empty_middle"
                and q["old_tiles"] == q["pieces"] == q["moment_blocks"] == []
            )
            r = q["result"]
            for key in (
                "incoming_pair",
                "outgoing_pair",
                "causal_integral",
                "forced_integral",
                "forced_error",
            ):
                assert r[key] == [0, 1]
            for key in (
                "pair_product",
                "forced_pair_product",
                "middle_covariance",
                "centered_integral",
                "reuse_integral",
            ):
                assert r[key] is None


def affine_family(value, alpha, beta, du=F(), dv=F(), path=()):
    if value is None:
        return None
    key = path[-1] if path else None
    if key in ("bounds", "probe_bounds", "incoming", "outgoing"):
        return [
            fw(fraction(x) * s + d)
            for x, s, d in zip(value, (alpha, alpha, beta, beta), (du, du, dv, dv), strict=True)
        ]
    if key in ("u_breaks", "v_breaks"):
        scale, shift = (alpha, du) if key == "u_breaks" else (beta, dv)
        return [fw(fraction(x) * scale + shift) for x in value]
    if key in ("moments", "old_moments", "piece_moment_sum"):
        return list(map(fw, transported_moments(list(map(fraction, value)), alpha, beta, du, dv)))
    if key in (
        "forced_incoming",
        "forced_outgoing",
        "incoming_coefficients",
        "outgoing_coefficients",
    ):
        return list(
            map(fw, transported_coefficients(list(map(fraction, value)), alpha, beta, du, dv))
        )
    powers = {
        **dict.fromkeys(("middle_volume", "incoming_volume", "outgoing_volume"), 1),
        **dict.fromkeys(
            (
                "incoming_pair",
                "outgoing_pair",
                "forced_incoming_pair",
                "forced_outgoing_pair",
                "incoming_pair_error",
                "outgoing_pair_error",
                "reuse_incoming_pair",
                "reuse_outgoing_pair",
                "middle_covariance",
            ),
            2,
        ),
        **dict.fromkeys(
            (
                "volume_product",
                "causal_integral",
                "pair_product",
                "centered_integral",
                "forced_integral",
                "forced_pair_product",
                "forced_error",
                "reuse_integral",
            ),
            3,
        ),
    }
    if key in powers:
        return fw(fraction(value) * (alpha * beta) ** powers[key])
    if type(value) is dict:
        return {k: affine_family(v, alpha, beta, du, dv, (*path, k)) for k, v in value.items()}
    if type(value) is list:
        return [affine_family(v, alpha, beta, du, dv, (*path, i)) for i, v in enumerate(value)]
    return value


def test_full_signed_affine_transport_preserves_reuse_and_refinement_decisions(engines):
    expected = affine_family(independent_family(mixed_problem()), F(2), F(3), F(3), F(-5))
    assert wire(expected) == wire(independent_family(expected["problem"]))
    for module in engines:
        assert wire(module.build_family(expected["problem"])) == wire(expected)


def test_no_hidden_file_reads_and_detached_moment_payloads(engines, monkeypatch):
    p = mixed_problem()
    before, expected = wire(p), wire(independent_family(p))

    def forbidden(*args, **kwargs):
        raise RuntimeError("read hidden artifact")

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
            first, second = module.build_family(p), module.build_family(p)
            assert wire(first) == wire(second) == expected and wire(p) == before
            first["problem"]["contexts"][0]["middles"][0]["moments"][0][0] = -1
            result_query(first)["pieces"][-1]["moments"][0][0] = -1
            assert (
                wire(second) == expected
                and wire(p) == before
                and wire(module.build_family(p)) == expected
            )


MALFORMED = (
    "extra",
    "duplicate_context",
    "bool_id",
    "subclass_id",
    "duplicate_query",
    "endpoint_type",
    "missing_tile",
    "reverse_breaks",
    "tile_bounds",
    "wrong_mass",
    "incoherent_higher",
    "degenerate_endpoint",
    "float_coordinate",
    "tuple_queries",
    "unknown_middle",
    "coverage_hole",
)


def malformed_problem(kind):
    p = snapshot_problem()
    context = p["contexts"][0]
    m = context["middles"][0]
    if kind == "extra":
        p["new_answers"] = []
    elif kind == "duplicate_context":
        p["contexts"].append(copy.deepcopy(context))
    elif kind == "bool_id":
        m["event"] = True
    elif kind == "subclass_id":

        class NonNativeInt(int):
            pass

        m["event"] = NonNativeInt(9)
    elif kind == "duplicate_query":
        m["queries"][1]["name"] = m["queries"][0]["name"]
    elif kind == "endpoint_type":
        m["queries"][0]["incoming"] = {"bounds": rect(UNIT)}
    elif kind == "missing_tile":
        m["tiles"] = []
    elif kind == "reverse_breaks":
        m["u_breaks"].reverse()
    elif kind == "tile_bounds":
        m["tiles"][0]["bounds"][1] = [2, 1]
    elif kind == "wrong_mass":
        m["moments"][0] = m["tiles"][0]["moments"][0] = [1, 1]
    elif kind == "incoherent_higher":
        m["moments"][8] = [1, 1]
    elif kind == "degenerate_endpoint":
        m["queries"][0]["incoming"] = rect((0, 0, 0, 1))
    elif kind == "float_coordinate":
        m["queries"][0]["incoming"][0][0] = 0.0
    elif kind == "tuple_queries":
        m["queries"] = tuple(m["queries"])
    elif kind == "unknown_middle":
        m["incoming_coefficients"] = []
    elif kind == "coverage_hole":
        p = snapshot_problem((F(0), F(1, 2)))
        p["contexts"][0]["probe_bounds"] = rect(UNIT)
    else:
        raise AssertionError(kind)
    return p


@pytest.mark.parametrize("kind", MALFORMED)
def test_basic_structural_native_grid_and_moment_consistency(engines, kind):
    for module in engines:
        with pytest.raises(ValueError):
            module.build_family(malformed_problem(kind))


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


def test_snapshot_payload_is_counted_once_and_updates_count_repeated_queries(engines):
    p = mixed_problem()
    for module in engines:
        counts = module.build_family(p)["counts"]
        expected = {
            "snapshot_tiles": 2,
            "old_tiles": 6,
            "snapshot_moment_entries": 27,
            "snapshot_bound_entries": 17,
            "endpoint_bound_entries": 24,
            "derived_pieces": 4,
            "retained_pieces": 4,
            "moment_derivation_calls": 4,
            "forced_coefficient_vectors": 12,
            "forced_coefficient_entries": 48,
            "exact_coefficient_vectors": 16,
            "exact_coefficient_entries": 64,
            "new_moment_entries": 36,
            "retained_moment_entries": 36,
            "moment_block_entries": 108,
        }
        assert {key: counts[key] for key in expected} == expected


def test_full_twenty_five_child_grid_preserves_hook_order_and_all_nine_moments(
    engines, monkeypatch
):
    fifth = F(1, 5)
    p = snapshot_problem(
        queries=[
            query(
                "four_cuts",
                (fifth, 2 * fifth, fifth, 2 * fifth),
                (3 * fifth, 4 * fifth, 3 * fifth, 4 * fifth),
            )
        ]
    )
    expected = independent_family(p)
    assert result_query(expected)["counts"]["derived_pieces"] == 25
    for module in engines:
        calls = []
        derive = module.derive_moments

        def count(bounds, derive=derive, calls=calls):
            calls.append(copy.deepcopy(bounds))
            return derive(bounds)

        with monkeypatch.context() as patch:
            patch.setattr(module, "derive_moments", count)
            actual = module.build_family(p)
        assert wire(actual) == wire(expected)
        q = result_query(actual)
        assert (
            calls == [piece["bounds"] for piece in result_query(expected)["pieces"]]
            and len(calls) == 25
        )
        assert q["moment_blocks"][0]["old_moments"] == q["moment_blocks"][0]["piece_moment_sum"]


def invalid_rectangles():
    bounds = rect(UNIT)
    return [
        tuple(bounds),
        replaced(bounds, (0, 0), False),
        replaced(bounds, (0, 1), 0),
        replaced(bounds, (1,), [2, 2]),
        replaced(bounds, (0, 0), 0.0),
        rect((0, 0, 0, 1)),
        rect((1, 0, 0, 1)),
        bounds[:-1],
    ]


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_guard_hook_and_trust_controls_survive_optimization(tmp_path, optimized):
    program = r"""
import importlib.util,json,pathlib,sys
directory = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("am_guard_tests",directory / "test_qr05am.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
rejections,hooks = 0,[]
def reject(fn,*args):
    global rejections
    try:
        fn(*args)
    except ValueError:
        rejections += 1
    else:
        raise RuntimeError("invalid input accepted")
def forbidden(*args):
    raise RuntimeError("reuse called new-moment hook")
for name,filename in (("primary","kernel.py"),("reference","reference.py")):
    module = t.load("am_guard_"+name,filename)
    for kind in t.MALFORMED:
        reject(module.build_family,t.malformed_problem(kind))
    for bounds in t.invalid_rectangles():
        reject(module.derive_moments,bounds)
    p = t.snapshot_problem(queries=[t.query("self",t.UNIT,t.UNIT)])
    old = module.derive_moments
    module.derive_moments = forbidden
    try:
        answer = module.build_family(p)
        if t.wire(answer) != t.wire(t.independent_family(p)):
            raise RuntimeError("reuse complete wire differs")
        bad = t.copy.deepcopy(p)
        m = bad["contexts"][0]["middles"][0]
        m["moments"][8] = m["tiles"][0]["moments"][8] = t.fw(t.fraction(m["moments"][8])+t.F(1,100))
        if name == "primary":
            altered = module.build_family(bad)
            if t.wire(altered) != t.wire(t.independent_family(bad,geometric=False)):
                raise RuntimeError("supplied moment replaced")
            if t.result_query(altered)["result"]["causal_integral"] == t.result_query(answer)["result"]["causal_integral"]:
                raise RuntimeError("wrong supplied moment silently ignored")
        else:
            reject(module.build_family,bad)
    finally:
        module.derive_moments = old
    calls = []
    def counted(bounds):
        calls.append(t.copy.deepcopy(bounds))
        return old(bounds)
    module.derive_moments = counted
    try:
        p = t.mixed_problem()
        before = t.wire(p)
        answer = module.build_family(p)
        if t.wire(answer) != t.wire(t.independent_family(p)) or t.wire(p) != before:
            raise RuntimeError("refinement complete wire or input differs")
        if len(calls) != answer["counts"]["moment_derivation_calls"] or len(calls) != 4:
            raise RuntimeError("derivation hook count differs")
        hooks.append(len(calls))
    finally:
        module.derive_moments = old
if rejections != 49 or hooks != [4,4]:
    raise RuntimeError("guard inventory changed")
print(json.dumps({"rejections":rejections,"new_moment_calls":hooks}))
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
    assert json.loads(result.stdout) == {"rejections": 49, "new_moment_calls": [4, 4]}


def snapshot_projection(problem):
    return {
        "family": problem["family"],
        "contexts": [
            {
                **{key: context[key] for key in ("level", "probe", "probe_bounds")},
                "middles": [
                    {
                        key: middle[key]
                        for key in ("event", "bounds", "u_breaks", "v_breaks", "moments", "tiles")
                    }
                    for middle in context["middles"]
                ],
            }
            for context in problem["contexts"]
        ],
    }


def query_projection(problem):
    return [
        {
            "level": c["level"],
            "probe": c["probe"],
            "middles": [{"event": m["event"], "queries": m["queries"]} for m in c["middles"]],
        }
        for c in problem["contexts"]
    ]


def independent_inputs(previous):
    assert [f["problem"]["family"] for f in previous] == list(FAMILIES)
    problems = []
    for family in previous:
        probes = {p["name"]: p["bounds"] for p in family["problem"]["probes"]}
        assert len(probes) == 5 and len(family["levels"]) == 3
        contexts = []
        for level in family["levels"]:
            assert len(level["geometry"]) == 5
            for geometry in level["geometry"]:
                q = copy.deepcopy(probes[geometry["probe"]])
                middles = []
                for old in geometry["middles"]:
                    middle = {
                        key: copy.deepcopy(old[key])
                        for key in ("event", "bounds", "u_breaks", "v_breaks", "moments")
                    }
                    middle["tiles"] = [
                        {key: copy.deepcopy(t[key]) for key in ("bounds", "moments")}
                        for t in old["tiles"]
                    ]
                    middle["queries"] = fixed_queries(middle, q)
                    middles.append(middle)
                contexts.append(
                    {
                        "level": level["level"],
                        "probe": geometry["probe"],
                        "probe_bounds": q,
                        "middles": middles,
                    }
                )
        problems.append({"family": family["problem"]["family"], "contexts": contexts})
    return problems, previous


@pytest.fixture(scope="session")
def fixed_inputs(runner):
    # No fixture work or fixed mathematics executes at import/collection.
    path = HERE.parent / "qr-05al-middle-moments-2026-09-07/results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 13515233
    assert (
        hashlib.sha256(raw).hexdigest()
        == "1e0f3ac8822afcd4407a176e1bfa4a2c3f5e45c43724e4e70bf3f66f01580a52"
    )
    previous = json.loads(raw)["suite"]["families"]
    expected, previous = independent_inputs(previous)
    actual, consumed = runner.load_inputs()
    assert wire(actual) == wire(expected) and wire(consumed) == wire(previous)
    return expected, previous


@pytest.fixture(scope="session")
def expected_families(fixed_inputs):
    return [independent_family(p) for p in fixed_inputs[0]]


@pytest.fixture(scope="session")
def actual_families(fixed_inputs, engines):
    outputs = []
    for p in fixed_inputs[0]:
        pair = []
        for module in engines:
            supplied = copy.deepcopy(p)
            before = wire(supplied)
            pair.append(module.build_family(supplied))
            assert wire(supplied) == before
        outputs.append(pair)
    return outputs


@pytest.mark.fixed
@pytest.mark.parametrize("index", range(5), ids=FAMILIES)
def test_fixed_all_five_complete_literal_family_comparisons(
    actual_families, expected_families, index
):
    expected = wire(expected_families[index])
    assert all(wire(actual) == expected for actual in actual_families[index])


def without_family(family):
    return {**family, "problem": {k: v for k, v in family["problem"].items() if k != "family"}}


def independent_controls(families):
    by = {f["problem"]["family"]: f for f in families}
    base = without_family(by["grid"])
    assert wire(without_family(by["boost"])) == wire(affine_family(base, F(2), F(1, 2)))
    assert wire(without_family(by["dilate"])) == wire(affine_family(base, F(2), F(2)))
    assert wire(without_family(by["warp_stale"])) == wire(without_family(by["warp"]))
    return {"boost": True, "dilation": True, "stale_geometric": True}


def independent_bridges(families, previous):
    expected, _ = independent_inputs(previous)
    assert wire([f["problem"] for f in families]) == wire(expected)
    assert wire([snapshot_projection(f["problem"]) for f in families]) == wire(
        [snapshot_projection(p) for p in expected]
    )
    return {
        "AL_family_names": list(FAMILIES),
        "AL_geometry_moment_projection_equal": True,
        "AL_probe_bounds_equal": True,
        "AL_other_math_replayed": False,
        "older_math_replayed": False,
    }


def independent_payload_sizes(families):
    out = []
    for family in families:
        update = [
            {
                "level": c["level"],
                "probe": c["probe"],
                "middles": [
                    {
                        "event": m["event"],
                        "queries": [
                            {key: q[key] for key in ("name", "admission", "pieces")}
                            for q in m["queries"]
                        ],
                    }
                    for m in c["middles"]
                ],
            }
            for c in family["contexts"]
        ]
        out.append(
            {
                "family": family["problem"]["family"],
                "snapshot_bytes": len(wire(snapshot_projection(family["problem"]))),
                "query_bytes": len(wire(query_projection(family["problem"]))),
                "exact_update_bytes": len(wire(update)),
                "native_family_bytes": len(wire(family)),
            }
        )
    return out


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
        "payload_sizes": independent_payload_sizes(expected_families),
        "totals": totals,
        "scope": dict.fromkeys(
            (
                "generic_production_API_hardened",
                "untrusted_primary_moments_geometrically_authenticated",
                "minimal_grid_proved",
                "universal_query_interface",
                "unknown_geometry_reconstructed",
                "arbitrary_dynamics_closure",
                "continuum_limit_established",
                "marks_authenticated",
                "stochastic_transition_constructed",
                "quantum_channel_constructed",
                "gravity_derived",
                "empirical_data_used",
                "ret_integration_tested",
                "lean_verification_performed",
            ),
            False,
        ),
    }


@pytest.mark.fixed
def test_fixed_complete_suite_payloads_and_all_consumed_AL_fields(
    runner, actual_families, expected_suite, fixed_inputs
):
    actual = runner.assemble_suite([pair[0] for pair in actual_families], fixed_inputs[1])
    assert wire(actual) == wire(expected_suite)
    runner.verify_suite(actual, expected_suite)


@pytest.mark.fixed
@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_cached_orchestration_preserves_inputs_and_declared_routes(
    runner, fixed_inputs, expected_suite, monkeypatch, route
):
    # Complete real two-engine arithmetic is verified for all five families;
    # this test uses cached oracle outputs to isolate route orchestration only.
    by = {f["problem"]["family"]: f for f in expected_suite["families"]}
    calls = []

    def loader(name):
        def build(problem):
            wanted = by[problem["family"]]
            assert wire(problem) == wire(wanted["problem"])
            calls.append((name, problem["family"]))
            return copy.deepcopy(wanted)

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
def test_fixed_nonvacuous_reuse_refinement_and_supplied_payload_corruptions(
    runner, expected_families
):
    original = expected_families[0]
    old = ("problem", "contexts", 0, "middles", 0)
    q = ("contexts", 0, "middles", 0, "queries", 2)
    reuse = ("contexts", 0, "middles", 0, "queries", 1)
    assert (
        at_path(original, (*q, "admission")) == "refine"
        and at_path(original, (*reuse, "admission")) == "reuse"
    )
    changes = [
        add_fraction(original, ("problem", "contexts", 0, "probe_bounds", 0)),
        add_fraction(original, (*old, "moments", 8)),
        add_fraction(original, (*old, "tiles", 0, "moments", 8)),
        add_fraction(original, (*old, "queries", 2, "incoming", 1)),
        replaced(original, (*q, "admission"), "reuse"),
        replaced(original, (*q, "old_tiles", 0, "incoming_admissible"), True),
        add_fraction(original, (*q, "old_tiles", 0, "forced_incoming", 3)),
        add_fraction(original, (*q, "old_tiles", 0, "forced_outgoing", 0)),
        add_fraction(original, (*q, "pieces", 0, "bounds", 0)),
        add_fraction(original, (*q, "pieces", 0, "moments", 8)),
        replaced(original, (*q, "pieces", 0, "moment_source"), "retained"),
        replaced(original, (*q, "pieces", 0, "parent"), 1),
        add_fraction(original, (*q, "pieces", 0, "outgoing_coefficients", 0)),
        replaced(original, (*q, "pieces"), at_path(original, (*q, "pieces"))[:-1]),
        replaced(original, (*q, "moment_blocks", 0, "children"), []),
        add_fraction(original, (*q, "moment_blocks", 0, "old_moments", 8)),
        add_fraction(original, (*q, "moment_blocks", 0, "piece_moment_sum", 8)),
        add_fraction(original, (*q, "result", "incoming_pair")),
        add_fraction(original, (*q, "result", "outgoing_pair")),
        add_fraction(original, (*q, "result", "causal_integral")),
        add_fraction(original, (*q, "result", "forced_incoming_pair")),
        add_fraction(original, (*q, "result", "forced_integral")),
        add_fraction(original, (*q, "result", "forced_error")),
        add_fraction(original, (*q, "result", "middle_covariance")),
        add_fraction(original, (*q, "result", "centered_integral")),
        add_fraction(original, (*q, "result", "conditional")),
        replaced(original, (*q, "result", "reuse_integral"), [0, 1]),
        replaced(original, (*reuse, "result", "reuse_integral"), None),
        replaced(
            original,
            (*q, "counts", "moment_derivation_calls"),
            at_path(original, (*q, "counts", "moment_derivation_calls")) + 1,
        ),
        replaced(
            original,
            ("counts", "retained_moment_entries"),
            original["counts"]["retained_moment_entries"] + 1,
        ),
    ]
    assert len(changes) == 30
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.verify_suite(bad, original)
    assert wire(original) == before


@pytest.mark.fixed
def test_fixed_nonvacuous_byte_scope_trust_and_complete_transform_claims(runner, expected_suite):
    original = expected_suite
    changes = [
        replaced(original, ("controls", key), False)
        for key in ("boost", "dilation", "stale_geometric")
    ]
    changes += [
        replaced(
            original, ("scope", "untrusted_primary_moments_geometrically_authenticated"), True
        ),
        replaced(original, ("scope", "minimal_grid_proved"), True),
        replaced(original, ("prior_bridges", "AL_other_math_replayed"), True),
        replaced(
            original, ("totals", "new_moment_entries"), original["totals"]["new_moment_entries"] + 1
        ),
    ]
    changes += [
        replaced(original, ("payload_sizes", 0, key), original["payload_sizes"][0][key] + 1)
        for key in ("snapshot_bytes", "query_bytes", "exact_update_bytes", "native_family_bytes")
    ]
    assert len(changes) == 11
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.verify_suite(bad, original)
    for path in (
        (3, "contexts", 0, "middles", 0, "queries", 2, "pieces", 0, "moments", 8),
        (2, "problem", "contexts", 0, "probe_bounds", 0),
    ):
        bad = add_fraction(original["families"], path)
        assert wire(bad) != wire(original["families"])
        with pytest.raises(ValueError):
            runner.controls(bad)
    assert wire(original) == before


@pytest.mark.fixed
def test_fixed_AL_projection_changes_cannot_hide_in_old_payloads(
    runner, expected_families, fixed_inputs
):
    original = fixed_inputs[1][0]
    m = ("levels", 0, "geometry", 0, "middles", 0)
    coherent = add_fraction(
        add_fraction(original, (*m, "moments", 8)), (*m, "tiles", 0, "moments", 8)
    )
    changes = [
        add_fraction(original, ("problem", "probes", 0, "bounds", 0)),
        add_fraction(original, (*m, "bounds", 0)),
        add_fraction(original, (*m, "u_breaks", 0)),
        add_fraction(original, (*m, "moments", 8)),
        add_fraction(original, (*m, "tiles", 0, "bounds", 0)),
        coherent,
        replaced(original, (*m, "tiles"), at_path(original, (*m, "tiles"))[:-1]),
        replaced(original, (*m, "event"), at_path(original, (*m, "event")) + 100),
    ]
    assert len(changes) == 8
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.al_bridges(expected_families, [bad, *fixed_inputs[1][1:]])
    assert wire(original) == before
