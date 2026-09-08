"""Independent rational Gram-Schmidt supplement, decoder and omission-witness checks.

Only test names containing fixed consume authenticated AR cases. Collection and generic
hands use explicit synthetic data, never fixed fixture calculations.
"""

from __future__ import annotations

import builtins
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
FAMILIES = ("grid", "warp")


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
        load("_qr05as_test_primary", "kernel.py"),
        load("_qr05as_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05as_test_runner", "study.py")


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


CHECKS = (
    "inherited_filter_identity",
    "base_certificate",
    "greedy_selection",
    "selected_filter_identity",
    "receiver_identity",
    "witness_constraints",
    "online_witness_recovery",
    "minimality_certificate",
)
SCOPE = (
    "source_dictionary_changed",
    "geometry_reintegrated",
    "old_collision_replayed",
    "full_field_recovery_tested",
    "individual_bank_minimality_proved",
    "sensor_cost_minimality_proved",
    "nonlinear_encoding_minimality_proved",
    "adaptive_readout_minimality_proved",
    "empirical_noise_calibrated",
    "physical_sources_established",
    "unknown_geometry_reconstructed",
    "quantum_channel_constructed",
    "gravity_derived",
    "ret_integration_tested",
    "lean_verification_performed",
    "generic_production_API_hardened",
    "fixed_affine_families_run",
    "older_executors_run",
)


def encode(value):
    if isinstance(value, F):
        return fw(value)
    if isinstance(value, list):
        return [encode(x) for x in value]
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    return value


def matrix(value):
    return [[fraction(x) for x in row] for row in value]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), F())


def mv(a, b):
    return [dot(row, b) for row in a]


def mm(a, b, width=None):
    if not b:
        assert width is not None
        return [[F()] * width for _ in a]
    return [[dot(row, col) for col in zip(*b, strict=True)] for row in a]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


class OrthogonalSpan:
    """Rational Gram-Schmidt with original-vector coordinates, without square roots."""

    def __init__(self, vectors=()):
        self.indices = []
        self.orthogonal = []
        self.combinations = []
        self.norms = []
        self.next_index = 0
        for vector in vectors:
            self.append(vector)

    def append(self, vector):
        index = self.next_index
        self.next_index += 1
        residual, projection = self.decompose(vector)
        if not any(residual):
            return False
        self.indices.append(index)
        self.orthogonal.append(residual)
        self.norms.append(dot(residual, residual))
        self.combinations.append({index: F(1), **{i: -v for i, v in projection.items() if v}})
        return True

    def decompose(self, vector):
        residual = list(vector)
        combination = {}
        for orth, norm, representation in zip(
            self.orthogonal, self.norms, self.combinations, strict=True
        ):
            scale = dot(vector, orth) / norm
            if scale:
                residual = [x - scale * y for x, y in zip(residual, orth, strict=True)]
                for i, v in representation.items():
                    combination[i] = combination.get(i, F()) + scale * v
        return residual, combination


def rank(rows):
    return len(OrthogonalSpan(rows).indices)


def columns(rows):
    return [list(x) for x in zip(*rows, strict=True)]


def expected(problem):
    o, r, q, g = (matrix(problem[key]) for key in ("observations", "bank", "targets", "filters"))
    m, b, n, t = len(o), len(r), len(q[0]), len(q)
    assert mm(g, r, n) == q
    a = [[F(1)] * n, *o]
    base_span = OrthogonalSpan(a)
    basis = [a[i] for i in base_span.indices]
    base_rank = len(basis)
    base_pivots = OrthogonalSpan(columns(a)).indices
    recoverable = [i for i, row in enumerate(q) if not any(base_span.decompose(row)[0])]
    failed = [i for i in range(t) if i not in recoverable]
    joint = rank([*a, *q])
    delta = joint - base_rank
    current = OrthogonalSpan(basis)
    selected = []
    decisions = []
    for index, row in enumerate(q):
        before = len(current.indices)
        residual, coefficients = current.decompose(row)
        if any(residual):
            decisions.append(
                {
                    "target_row": index,
                    "rank_before": before,
                    "rank_after": before + 1,
                    "selected": True,
                    "coefficients": None,
                }
            )
            selected.append(index)
            appended = current.append(row)
            assert appended
            basis.append(row)
        else:
            coefficient_row = [coefficients.get(i, F()) for i in range(before)]
            assert mv(columns(basis), coefficient_row) == row
            decisions.append(
                {
                    "target_row": index,
                    "rank_before": before,
                    "rank_after": before,
                    "selected": False,
                    "coefficients": coefficient_row,
                }
            )
    assert len(selected) == delta and len(current.indices) == joint
    filters = [g[i][:] for i in selected]
    h = mm(filters, r, n)
    assert h == [q[i] for i in selected]
    supports = [[i for i, v in enumerate(row) if v] for row in filters]
    x = [*o, *h]
    augmented = [[F(1)] * n, *x]
    full_span = OrthogonalSpan(augmented)
    full_basis = [augmented[i] for i in full_span.indices]
    assert full_span.indices == [*base_span.indices, *range(1 + m, 1 + m + delta)]
    full_columns = columns(full_basis)
    pivot_span = OrthogonalSpan(full_columns)
    pivots = pivot_span.indices
    assert len(pivots) == joint
    d = []
    intercept = []
    dense = []
    for row in q:
        residual, coefficients = full_span.decompose(row)
        assert not any(residual)
        compact = [coefficients.get(i, F()) for i in full_span.indices]
        assert mv(columns(full_basis), compact) == row
        d.append(compact)
        intercept.append(coefficients.get(0, F()))
        dense.append([coefficients.get(i + 1, F()) for i in range(m + delta)])
    predicted = [
        [offset + v for v in row] for offset, row in zip(intercept, mm(dense, x, n), strict=True)
    ]
    residuals = [
        [u - v for u, v in zip(actual, want, strict=True)]
        for actual, want in zip(predicted, q, strict=True)
    ]
    assert predicted == q and not any(any(row) for row in residuals)
    witnesses = []
    for j, target in enumerate(selected):
        e = [F(i == base_rank + j) for i in range(joint)]
        residual, coefficients = pivot_span.decompose(e)
        assert not any(residual)
        w = [coefficients.get(i, F()) for i in range(n)]
        assert mv(full_basis, w) == e
        assert all(w[i] == 0 for i in range(n) if i not in pivots)
        assert sum(w, F()) == 0 and mv(o, w) == [F()] * m
        assert mv(h, w) == [F(i == j) for i in range(delta)]
        mass = sum((max(F(), v) for v in w), F())
        assert mass > 0 and mass == sum((max(F(), -v) for v in w), F())
        plus = [max(F(), v) / mass for v in w]
        minus = [max(F(), -v) / mass for v in w]
        assert sum(plus, F()) == sum(minus, F()) == 1
        assert all(u * v == 0 for u, v in zip(plus, minus, strict=True))
        bp, bm = mv(r, plus), mv(r, minus)
        op, om = mv(o, plus), mv(o, minus)
        sp, sm = mv(filters, bp), mv(filters, bm)
        assert sp == mv(h, plus) and sm == mv(h, minus)
        available = [i for i in range(m + delta) if i != m + j]
        xp, xm = [*op, *sp], [*om, *sm]
        ap, am = [xp[i] for i in available], [xm[i] for i in available]
        tp, tm = mv(q, plus), mv(q, minus)
        pp = [offset + value for offset, value in zip(intercept, mv(dense, xp), strict=True)]
        pm = [offset + value for offset, value in zip(intercept, mv(dense, xm), strict=True)]
        difference = [u - v for u, v in zip(tp, tm, strict=True)]
        assert ap == am and pp == tp and pm == tm
        assert difference == [v / mass for v in mv(q, w)]
        assert difference[target] == sp[j] - sm[j] == 1 / mass > 0
        witnesses.append(
            {
                "omitted_index": j,
                "target_row": target,
                "available_rows": available,
                "null_vector": w,
                "positive_mass": mass,
                "weights_plus": plus,
                "weights_minus": minus,
                "bank_plus": bp,
                "bank_minus": bm,
                "coarse_plus": op,
                "coarse_minus": om,
                "supplement_plus": sp,
                "supplement_minus": sm,
                "available_plus": ap,
                "available_minus": am,
                "truth_plus": tp,
                "truth_minus": tm,
                "truth_difference": difference,
                "predicted_plus": pp,
                "predicted_minus": pm,
                "residual_plus": [F()] * t,
                "residual_minus": [F()] * t,
            }
        )
    counts = {
        "source_columns": n,
        "coarse_values": m,
        "bank_values": b,
        "target_rows": t,
        "supplement_values": delta,
        "receiver_values": m + delta,
        "input_matrix_entries": m * n + b * n + t * n + t * b,
        "selected_filter_entries": delta * b,
        "selected_filter_nonzero": sum(map(len, supports)),
        "selected_bank_rows": len({i for row in supports for i in row}),
        "supplement_entries": delta * n,
        "decision_coefficient_entries": sum(
            len(row["coefficients"]) for row in decisions if row["coefficients"] is not None
        ),
        "decoder_compact_entries": t * joint,
        "decoder_raw_entries": t * (1 + m + delta),
        "prediction_entries": t * n,
        "residual_entries": t * n,
        "witnesses": delta,
        "witness_entries": delta
        * (3 * n + 2 * b + 2 * m + 2 * delta + 2 * (m + delta - 1) + 7 * t + 1)
        if delta
        else 0,
    }
    for witness in witnesses:
        rational_fields = [
            value
            for key, value in witness.items()
            if key not in ("omitted_index", "target_row", "available_rows")
        ]
        assert sum(len(value) if isinstance(value, list) else 1 for value in rational_fields) == (
            3 * n + 2 * b + 2 * m + 2 * delta + 2 * (m + delta - 1) + 7 * t + 1
        )
    answer = encode(
        {
            "problem": copy.deepcopy(problem),
            "base": {
                "observation_rank": base_rank,
                "target_rank": rank(q),
                "joint_rank": joint,
                "delta": delta,
                "row_basis": base_span.indices,
                "pivot_columns": base_pivots,
                "free_columns": [i for i in range(n) if i not in base_pivots],
                "recoverable_rows": recoverable,
                "failed_rows": failed,
            },
            "selection": {
                "target_rows": selected,
                "target_labels": [copy.deepcopy(problem["target_labels"][i]) for i in selected],
                "decisions": decisions,
                "filters": filters,
                "bank_support": supports,
                "values": h,
            },
            "decoder": {
                "row_basis": full_span.indices,
                "pivot_columns": pivots,
                "free_columns": [i for i in range(n) if i not in pivots],
                "coefficients": d,
                "intercept": intercept,
                "matrix": dense,
                "predicted": predicted,
                "residuals": residuals,
                "exact": True,
            },
            "witnesses": witnesses,
            "checks": dict.fromkeys(CHECKS, True),
            "counts": counts,
        }
    )
    native(answer)
    return answer


def problem(o, r, q, g, name="synthetic"):
    q = [[F(x) for x in row] for row in q]
    return encode(
        {
            "family": name,
            "target_labels": [{"first": i - 3, "second": -8} for i in range(len(q))],
            "observations": o,
            "bank": r,
            "targets": q,
            "filters": g,
        }
    )


def normalization_problem():
    q = [[F(1)] * 3, *identity(3)]
    return problem([], identity(3), q, q, "normalization")


def redundant_problem():
    e = identity(4)
    coarse = [F(1), F(1), F(), F()]
    o = [coarse, [2 * x for x in coarse], [F()] * 4]
    q = [
        [F(1)] * 4,
        coarse,
        e[0],
        [2 * x + y for x, y in zip(e[0], coarse, strict=True)],
        e[2],
        e[3],
    ]
    return problem(o, identity(4), q, q, "redundant")


def no_supplement_problem():
    return problem(
        [],
        [[F(1)] * 3],
        [[F(1)] * 3, [F(2)] * 3, [F()] * 3],
        [[F(1)], [F(2)], [F()]],
        "known-offsets",
    )


def empty_bank_problem():
    return problem([[F(), F(1)]], [], [[F(), F()], [F(), F()]], [[], []], "empty-bank")


def nonunique_filter_problem(changed=False):
    r = [[F(1), F()], [F(), F(1)], [F(1), F(1)]]
    g = [[F(1), F(), F()]] if not changed else [[F(4), F(3), F(-3)]]
    return problem([], r, [[F(1), F()]], g, "nonunique-filters")


def tiny_problem():
    tiny = F(1, 1 << 3500)
    q = [[tiny, F()]]
    return problem([], identity(2), q, q, "tiny-exact")


@pytest.mark.parametrize(
    "factory",
    [
        normalization_problem,
        redundant_problem,
        no_supplement_problem,
        empty_bank_problem,
        nonunique_filter_problem,
        lambda: nonunique_filter_problem(True),
        tiny_problem,
    ],
)
def test_generic_complete_independent_gram_schmidt_wire(engines, factory):
    p = factory()
    wanted = expected(p)
    before = wire(p)
    for engine in engines:
        assert wire(engine.build_family(p)) == wire(wanted)
        assert wire(p) == before


def test_normalization_avoids_a_spurious_readout_and_each_member_is_necessary(engines):
    for engine in engines:
        result = engine.build_family(normalization_problem())
        assert result["selection"]["target_rows"] == [1, 2]
        assert result["base"]["delta"] == 2
        assert result["decoder"]["intercept"] == encode([F(1), F(), F(), F(1)])
        assert result["decoder"]["matrix"] == encode(
            [[F(), F()], [F(1), F()], [F(), F(1)], [F(-1), F(-1)]]
        )
        assert [w["null_vector"] for w in result["witnesses"]] == encode(
            [[F(1), F(), F(-1)], [F(), F(1), F(-1)]]
        )
        for witness in result["witnesses"]:
            j = witness["omitted_index"]
            assert witness["available_plus"] == witness["available_minus"]
            assert fraction(witness["truth_difference"][witness["target_row"]]) > 0
            assert witness["available_rows"] == [1 - j]
            assert (
                engine.produce(result["selection"]["filters"], witness["bank_plus"])
                == witness["supplement_plus"]
            )
            assert (
                engine.apply(
                    result["decoder"]["intercept"],
                    result["decoder"]["matrix"],
                    witness["coarse_plus"] + witness["supplement_plus"],
                )
                == witness["truth_plus"]
            )


def test_original_order_not_reduced_rows_and_full_redundant_interfaces(engines):
    for engine in engines:
        result = engine.build_family(redundant_problem())
        assert result["base"]["row_basis"] == [0, 1]
        assert result["selection"]["target_rows"] == [2, 4]
        assert result["decoder"]["row_basis"] == [0, 1, 4, 5]
        assert result["base"]["recoverable_rows"] == [0, 1]
        assert result["base"]["failed_rows"] == [2, 3, 4, 5]
        assert [row["selected"] for row in result["selection"]["decisions"]] == [
            False,
            False,
            True,
            False,
            True,
            False,
        ]
        assert result["selection"]["decisions"][3]["coefficients"] == encode([F(), F(1), F(2)])
        assert result["selection"]["values"] == [redundant_problem()["targets"][i] for i in (2, 4)]


def test_zero_supplements_zero_bank_and_width_zero_receiver_are_distinct(engines):
    for engine in engines:
        for p in (no_supplement_problem(), empty_bank_problem()):
            result = engine.build_family(p)
            assert result["base"]["delta"] == 0
            assert (
                result["selection"]["target_rows"]
                == result["selection"]["filters"]
                == result["witnesses"]
                == []
            )
            assert result["counts"]["witness_entries"] == 0
        assert engine.produce([], []) == []
        assert engine.produce([[], []], []) == encode([F(), F()])
        assert engine.produce([], [fw(7), fw(-2), fw(4)]) == []
        assert engine.apply(encode([F(1), F(2), F()]), [[], [], []], []) == encode(
            [F(1), F(2), F()]
        )
        result = engine.build_family(no_supplement_problem())
        assert result["decoder"]["intercept"] == encode([F(1), F(2), F()])
        assert result["decoder"]["matrix"] == [[], [], []]


def test_declared_nonunique_filters_are_preserved_without_optimization(engines):
    for engine in engines:
        a = engine.build_family(nonunique_filter_problem())
        b = engine.build_family(nonunique_filter_problem(True))
        assert a["base"] == b["base"]
        assert a["decoder"] == b["decoder"]
        assert a["witnesses"] == b["witnesses"]
        assert a["selection"]["values"] == b["selection"]["values"]
        assert a["selection"]["filters"] != b["selection"]["filters"]
        assert a["selection"]["bank_support"] == [[0]]
        assert b["selection"]["bank_support"] == [[0, 1, 2]]
        assert a["counts"]["selected_filter_nonzero"] == 1
        assert b["counts"]["selected_filter_nonzero"] == 3


def inverse(a):
    span = OrthogonalSpan(columns(a))
    assert len(span.indices) == len(a)
    solution = []
    for e in identity(len(a)):
        residual, coordinates = span.decompose(e)
        assert not any(residual)
        solution.append([coordinates.get(i, F()) for i in range(len(a))])
    result = columns(solution)
    assert mm(a, result) == identity(len(a))
    return result


def coordinate_problem(p, p_map, s_map, v):
    o, r, q, g = (matrix(p[key]) for key in ("observations", "bank", "targets", "filters"))
    return {
        **copy.deepcopy(p),
        "observations": encode(mm(p_map, o)),
        "bank": encode(mm(s_map, r)),
        "targets": encode([[v * x for x in row] for row in q]),
        "filters": encode([[v * x for x in row] for row in mm(g, inverse(s_map))]),
    }


@pytest.mark.parametrize("prefix", [False, True])
def test_readout_coordinate_changes_scale_witness_direction_not_mixture(engines, prefix):
    p = redundant_problem()
    p_map = (
        [[F(2), F(), F()], [F(1), F(3), F()], [F(-2), F(4), F(5)]]
        if prefix
        else [[F(), F(), F(1)], [F(), F(1), F()], [F(1), F(), F()]]
    )
    s_map = [
        [F(2), F(), F(), F()],
        [F(-1), F(3), F(), F()],
        [F(2), F(1), F(5), F()],
        [F(), F(-2), F(1), F(7)],
    ]
    v = F(7, 3)
    moved = coordinate_problem(p, p_map, s_map, v)
    want, want_moved = expected(p), expected(moved)
    for key in (
        "observation_rank",
        "target_rank",
        "joint_rank",
        "delta",
        "pivot_columns",
        "free_columns",
        "recoverable_rows",
        "failed_rows",
    ):
        assert want["base"][key] == want_moved["base"][key]
    assert (want["base"]["row_basis"] == want_moved["base"]["row_basis"]) is prefix
    for key in ("target_rows", "target_labels"):
        assert want["selection"][key] == want_moved["selection"][key]
    assert matrix(want_moved["selection"]["filters"]) == [
        [v * x for x in row] for row in mm(matrix(want["selection"]["filters"]), inverse(s_map))
    ]
    assert matrix(want_moved["selection"]["values"]) == [
        [v * x for x in row] for row in matrix(want["selection"]["values"])
    ]
    for a, b in zip(want["witnesses"], want_moved["witnesses"], strict=True):
        for key in (
            "omitted_index",
            "target_row",
            "available_rows",
            "weights_plus",
            "weights_minus",
        ):
            assert a[key] == b[key]
        assert list(map(fraction, b["null_vector"])) == [fraction(x) / v for x in a["null_vector"]]
        assert fraction(b["positive_mass"]) == fraction(a["positive_mass"]) / v
        for key in (
            "truth_plus",
            "truth_minus",
            "truth_difference",
            "predicted_plus",
            "predicted_minus",
        ):
            assert list(map(fraction, b[key])) == [v * fraction(x) for x in a[key]]
        for sign in ("plus", "minus"):
            assert list(map(fraction, b["bank_" + sign])) == mv(
                s_map, list(map(fraction, a["bank_" + sign]))
            )
            assert list(map(fraction, b["coarse_" + sign])) == mv(
                p_map, list(map(fraction, a["coarse_" + sign]))
            )
    old = want["decoder"]
    a = [v * fraction(x) for x in old["intercept"]]
    pi = inverse(p_map)
    transported = []
    for row in matrix(old["matrix"]):
        transported.append([v * x for x in mm([row[:3]], pi)[0]] + row[3:])
    values = [F(-2), F(5), F(7), F(3, 2), F(-4)]
    changed = mv(p_map, values[:3]) + [v * x for x in values[3:]]
    for engine in engines:
        assert wire(engine.build_family(p)) == wire(want)
        assert wire(engine.build_family(moved)) == wire(want_moved)
        left = engine.apply(encode(a), encode(transported), encode(changed))
        right = engine.apply(old["intercept"], old["matrix"], encode(values))
        assert list(map(fraction, left)) == [v * fraction(x) for x in right]


def test_restricted_producer_receiver_external_values_and_file_blindness(engines, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("restricted evaluator attempted file access")

    p = nonunique_filter_problem(True)
    f = expected(p)
    with monkeypatch.context() as m:
        m.setattr(builtins, "open", forbidden)
        m.setattr(Path, "open", forbidden)
        m.setattr(Path, "read_bytes", forbidden)
        m.setattr(Path, "read_text", forbidden)
        for engine in engines:
            # This arbitrary signed bank vector need not arise from any source mixture.
            assert engine.produce(p["filters"], encode([F(3), F(-2), F(7)])) == [fw(-15)]
            assert engine.apply([fw(5)], [[fw(2), fw(-3), fw(4)]], encode([F(-1), F(7), F(2)])) == [
                fw(-10)
            ]
            for witness in f["witnesses"]:
                supplied = engine.produce(f["selection"]["filters"], witness["bank_plus"])
                assert (
                    engine.apply(f["decoder"]["intercept"], f["decoder"]["matrix"], supplied)
                    == witness["truth_plus"]
                )


def test_shared_native_inputs_and_detached_outputs(engines):
    p = normalization_problem()
    p["filters"] = p["targets"]
    frozen = wire(p)
    for engine in engines:
        answer = engine.build_family(p)
        before = wire(answer)
        assert wire(p) == frozen
        p["family"] = "changed"
        assert wire(answer) == before
        p["family"] = "normalization"
        answer["selection"]["filters"][0][0][0] += 1
        assert wire(p) == frozen
        assert wire(engine.build_family(p)) == before
        values = encode([F(2), F(3)])
        result = engine.produce([[fw(1), fw(2)]], values)
        values[0] = fw(9)
        assert result == [fw(8)]
        result[0][0] = 91
        assert engine.produce([[fw(1), fw(2)]], encode([F(2), F(3)])) == [fw(8)]


def test_accepted_matrix_and_raw_interface_edges(engines):
    wide = problem([], [], [[F()] * 576], [[]], "wide-zero")
    many = problem(
        [[F()]] * 256, [[F()]] * 1024, [[F()]] * 64, [[F()] * 1024 for _ in range(64)], "many-zero"
    )
    for engine in engines:
        for p in (wide, many):
            assert wire(engine.build_family(p)) == wire(expected(p))
        assert engine.produce([[fw(0)] * 1024 for _ in range(64)], [fw(1)] * 1024) == [fw(0)] * 64
        assert (
            engine.apply([fw(3)] * 64, [[fw(0)] * 320 for _ in range(64)], [fw(1)] * 320)
            == [fw(3)] * 64
        )


def test_family_product_cancellation_and_retained_omission_direction_bits(engines):
    d = 1 << 4095
    valid = problem([], [[F(2)], [F(2)]], [[F()]], [[F(d), F(-d)]], "cancellation")
    wanted = expected(valid)
    # Both individual product terms are 4097-bit, but no such term is retained.
    assert (2 * d).bit_length() == 4097
    q = [[F(1, d), F(1, d - 1)]]
    oversized = problem([], identity(2), q, q, "retained-direction-overflow")
    assert mm(matrix(oversized["filters"]), matrix(oversized["bank"])) == q
    # Unit omitted response requires mass d(d-1), a genuinely retained value.
    assert (d * (d - 1)).bit_length() > 4096
    for engine in engines:
        assert wire(engine.build_family(valid)) == wire(wanted)
        with pytest.raises(ValueError):
            engine.build_family(oversized)


class NativeListSubclass(list):
    pass


class NativeIntSubclass(int):
    pass


def malformed_families():
    p = normalization_problem()
    yield None
    yield []
    yield {**p, "geometry": []}
    yield {key: value for key, value in p.items() if key != "bank"}
    for value in ("", False, 1):
        yield replaced(p, ["family"], value)
    for value in ([], (), p["target_labels"][:-1], p["target_labels"] * 17):
        yield replaced(p, ["target_labels"], value)
    yield replaced(p, ["target_labels", 0, "first"], True)
    yield replaced(p, ["target_labels", 0, "second"], 1.0)
    yield replaced(p, ["target_labels", 0, "extra"], 0)
    yield replaced(p, ["target_labels", 1], p["target_labels"][0])
    yield replaced(p, ["target_labels"], list(reversed(p["target_labels"])))
    for key in ("observations", "bank", "targets", "filters"):
        yield replaced(p, [key], None)
        yield replaced(p, [key], tuple(p[key]))
        yield replaced(p, [key], NativeListSubclass(p[key]))
    yield replaced(p, ["targets"], [])
    yield replaced(p, ["targets"], [[]] * 4)
    yield replaced(p, ["targets"], [[fw(0)] * 577] * 4)
    yield replaced(p, ["observations"], [[fw(0)] * 3] * 257)
    yield replaced(p, ["bank"], [[fw(0)] * 3] * 1025)
    yield replaced(p, ["bank", 2], [fw(0)])
    yield replaced(p, ["targets", 3], [fw(0)])
    yield replaced(p, ["filters", 3], [fw(0)])
    yield replaced(p, ["filters"], p["filters"][:-1])
    yield replaced(p, ["filters", 3, 2], fw(2))
    for value in (
        True,
        0.0,
        F(0),
        NativeIntSubclass(0),
        (0, 1),
        [0],
        [0, 0],
        [0, -1],
        [2, 2],
        [1 << 4096, 1],
    ):
        yield replaced(p, ["targets", 3, 2], value)
        yield replaced(p, ["filters", 3, 2], value)
    yield replaced(empty_bank_problem(), ["targets", 0, 0], fw(1))


def malformed_producers():
    h, x = [[fw(1), fw(2), fw(3)]], [fw(1)] * 3
    for value in (None, {}, (), NativeListSubclass(h), h * 65, [[fw(0)] * 1025]):
        yield value, x
    for value in (None, {}, (), NativeListSubclass(x), x[:-1], x * 342):
        yield h, value
    yield [[fw(1)] * 3, [fw(1)] * 2], x
    for value in (True, 0.0, F(0), (0, 1), [0], [0, 0], [2, 2], [1 << 4096, 1]):
        yield replaced(h, [0, 2], value), x
        yield h, replaced(x, [2], value)
    yield [], [True]


def malformed_receivers():
    a, l, x = [fw(1)], [[fw(1)] * 3], [fw(1)] * 3
    for value in (None, [], (), [fw(1)] * 65, [True]):
        yield value, l, x
    for value in (None, [], (), [[fw(1)] * 2], [[fw(1)] * 321], [[fw(1)] * 3] * 2):
        yield a, value, x
    for value in (None, (), x[:-1], [True] * 3):
        yield a, l, value
    for value in (True, 0.0, F(0), (0, 1), [0], [0, 0], [2, 2], [1 << 4096, 1]):
        yield a, replaced(l, [0, 2], value), x
        yield a, l, replaced(x, [2], value)


def require_rejection(call):
    try:
        call()
    except ValueError:
        return
    raise RuntimeError("expected explicit ValueError")


def explicit_guards(engine):
    count = 0
    for p in malformed_families():
        require_rejection(lambda p=p: engine.build_family(p))
        count += 1
    for h, x in malformed_producers():
        require_rejection(lambda h=h, x=x: engine.produce(h, x))
        count += 1
    for a, l, x in malformed_receivers():
        require_rejection(lambda a=a, l=l, x=x: engine.apply(a, l, x))
        count += 1
    d = 1 << 4095
    if engine.produce([[fw(d), fw(-d)]], [fw(2), fw(2)]) != [fw(0)]:
        raise RuntimeError("producer internal cancellation")
    if engine.apply([fw(0)], [[fw(d), fw(-d)]], [fw(2), fw(2)]) != [fw(0)]:
        raise RuntimeError("receiver internal cancellation")
    require_rejection(lambda: engine.produce([[fw(d), fw(d)]], [fw(1), fw(1)]))
    require_rejection(lambda: engine.apply([fw(0)], [[fw(d), fw(d)]], [fw(1), fw(1)]))
    cyclic = normalization_problem()
    cyclic["observations"].append(cyclic["observations"])
    require_rejection(lambda: engine.build_family(cyclic))
    cycle = []
    cycle.append(cycle)
    require_rejection(lambda: engine.produce(cycle, [fw(1)]))
    require_rejection(lambda: engine.apply([fw(1)], [[fw(1)]], cycle))
    return count + 5


def pre_arithmetic_guards(engine):
    calls = []

    def forbidden(*args, **kwargs):
        calls.append(1)
        raise RuntimeError("arithmetic reached before complete admission")

    original = engine._fraction
    engine._fraction = forbidden
    try:
        for value in ([], [0]):
            require_rejection(
                lambda value=value: engine.build_family(
                    replaced(normalization_problem(), ["filters", 3, 2], value)
                )
            )
            require_rejection(lambda value=value: engine.produce([[fw(1)], [value]], [fw(2)]))
            require_rejection(
                lambda value=value: engine.apply([fw(1), fw(2)], [[fw(1)], [value]], [fw(3)])
            )
    finally:
        engine._fraction = original
    hook = "_multiply" if hasattr(engine, "_multiply") else "_dot"
    original = getattr(engine, hook)
    setattr(engine, hook, forbidden)
    try:
        require_rejection(
            lambda: engine.build_family(
                replaced(normalization_problem(), ["filters", 3, 2], [1, 0])
            )
        )
    finally:
        setattr(engine, hook, original)
    original = engine._dot
    engine._dot = forbidden
    try:
        require_rejection(lambda: engine.produce([[fw(1)], [[1, 0]]], [fw(1)]))
        require_rejection(lambda: engine.apply([fw(1), fw(2)], [[fw(1)], [[1, 0]]], [fw(1)]))
    finally:
        engine._dot = original
    if calls:
        raise RuntimeError("late shape/value admission ordering")
    return 9


def test_explicit_native_dimension_identity_and_bit_guards(engines):
    counts = [explicit_guards(engine) for engine in engines]
    assert counts[0] == counts[1] and counts[0] > 90
    assert [pre_arithmetic_guards(engine) for engine in engines] == [9, 9]


@pytest.mark.parametrize("optimized", [False, True])
def test_isolated_explicit_normal_and_optimized_guards(tmp_path, optimized):
    script = r"""
import importlib.util,json,sys
from pathlib import Path
path=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("as_guards",path)
t=importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
counts=[]
for name,file in (("primary","kernel.py"),("reference","reference.py")):
    engine=t.load("_qr05as_guard_"+name,file)
    counts.append(t.explicit_guards(engine)+t.pre_arithmetic_guards(engine))
print(json.dumps(counts))
"""
    args = [sys.executable, "-I", "-X", "pycache_prefix=" + str(tmp_path / "cache")]
    if optimized:
        args.append("-O")
    done = subprocess.run(
        [*args, "-c", script, str(Path(__file__).resolve())],
        capture_output=True,
        text=True,
        check=True,
        timeout=90,
    )
    count = (
        len(list(malformed_families()))
        + len(list(malformed_producers()))
        + len(list(malformed_receivers()))
        + 14
    )
    assert json.loads(done.stdout) == [count, count]


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


def changed_fraction(tree, path):
    current = tree
    for key in path:
        current = current[key]
    return replaced(tree, path, fw(fraction(current) + 1))


def family_mutations(family):
    for key in ("observation_rank", "target_rank", "joint_rank", "delta"):
        yield replaced(family, ["base", key], family["base"][key] + 1)
    for key in ("row_basis", "pivot_columns", "free_columns", "recoverable_rows", "failed_rows"):
        yield replaced(family, ["base", key], family["base"][key] + [-1])
    selected = family["selection"]
    yield replaced(family, ["selection", "target_rows"], selected["target_rows"] + [-1])
    yield replaced(
        family,
        ["selection", "target_labels"],
        selected["target_labels"] + [{"first": 999, "second": 999}],
    )
    first = selected["decisions"][0]
    for key in ("target_row", "rank_before", "rank_after"):
        yield replaced(family, ["selection", "decisions", 0, key], first[key] + 1)
    yield replaced(family, ["selection", "decisions", 0, "selected"], not first["selected"])
    for flag in (False, True):
        index = next(
            (i for i, row in enumerate(selected["decisions"]) if row["selected"] is flag), None
        )
        if index is not None:
            if flag:
                yield replaced(family, ["selection", "decisions", index, "coefficients"], [])
            else:
                yield changed_fraction(family, ["selection", "decisions", index, "coefficients", 0])
    if selected["target_rows"]:
        yield changed_fraction(family, ["selection", "filters", 0, 0])
        yield replaced(family, ["selection", "bank_support", 0], selected["bank_support"][0] + [-1])
        yield changed_fraction(family, ["selection", "values", 0, 0])
    else:
        for key in ("filters", "bank_support", "values"):
            yield replaced(family, ["selection", key], [[]])
    for key in ("row_basis", "pivot_columns", "free_columns"):
        yield replaced(family, ["decoder", key], family["decoder"][key] + [-1])
    yield changed_fraction(family, ["decoder", "coefficients", 0, 0])
    yield changed_fraction(family, ["decoder", "intercept", 0])
    if family["decoder"]["matrix"][0]:
        yield changed_fraction(family, ["decoder", "matrix", 0, 0])
    else:
        yield replaced(family, ["decoder", "matrix", 0], [fw(1)])
    yield changed_fraction(family, ["decoder", "predicted", 0, 0])
    yield changed_fraction(family, ["decoder", "residuals", 0, 0])
    yield replaced(family, ["decoder", "exact"], False)
    if family["witnesses"]:
        for i, _witness in enumerate(family["witnesses"]):
            yield changed_fraction(family, ["witnesses", i, "positive_mass"])
        witness = family["witnesses"][0]
        for key in ("omitted_index", "target_row"):
            yield replaced(family, ["witnesses", 0, key], witness[key] + 1)
        yield replaced(family, ["witnesses", 0, "available_rows"], witness["available_rows"] + [-1])
        for key in (
            "null_vector",
            "weights_plus",
            "weights_minus",
            "bank_plus",
            "bank_minus",
            "coarse_plus",
            "coarse_minus",
            "supplement_plus",
            "supplement_minus",
            "available_plus",
            "available_minus",
            "truth_plus",
            "truth_minus",
            "truth_difference",
            "predicted_plus",
            "predicted_minus",
            "residual_plus",
            "residual_minus",
        ):
            if witness[key]:
                yield changed_fraction(family, ["witnesses", 0, key, 0])
            else:
                yield replaced(family, ["witnesses", 0, key], [fw(1)])
        yield replaced(family, ["witnesses"], family["witnesses"][:-1])
    else:
        yield replaced(family, ["witnesses"], [{}])
    yield replaced(family, ["checks", "minimality_certificate"], False)
    yield replaced(family, ["counts", "witness_entries"], family["counts"]["witness_entries"] + 1)
    yield replaced(
        family, ["counts", "selected_bank_rows"], family["counts"]["selected_bank_rows"] + 1
    )
    yield changed_fraction(family, ["problem", "targets", 0, 0])
    yield replaced(family, ["problem", "target_labels", 0, "second"], 999)


def test_complete_generic_wire_and_witness_corruptions_are_nonvacuous(runner):
    count = 0
    for factory in (
        normalization_problem,
        redundant_problem,
        no_supplement_problem,
        empty_bank_problem,
    ):
        wanted = expected(factory())
        for bad in family_mutations(wanted):
            assert wire(bad) != wire(wanted)
            with pytest.raises(ValueError):
                runner.verify_suite(bad, wanted)
            count += 1
    assert count > 150


BRIDGES = {
    "AR_selected_families": ["grid", "warp"],
    "AR_selected_inputs_equal": True,
    "AR_zero_repair_intercept": True,
    "AR_base_certificate_equal": True,
    "AR_filter_identity_rechecked": True,
    "other_historical_mathematics_replayed": False,
    "older_executors_run": False,
}
BASE_FIELDS = (
    "observation_rank",
    "target_rank",
    "joint_rank",
    "row_basis",
    "pivot_columns",
    "free_columns",
    "recoverable_rows",
    "failed_rows",
)


def projected_problem(old):
    return {
        "family": old["problem"]["family"],
        "target_labels": copy.deepcopy(old["matrices"]["fine_response_rows"]),
        "observations": copy.deepcopy(old["matrices"]["coarse_observations"]),
        "bank": copy.deepcopy(old["matrices"]["repair_observations"]),
        "targets": copy.deepcopy(old["matrices"]["fine_targets"]),
        "filters": copy.deepcopy(old["repair"]["matrix"]),
    }


def payload(families):
    result = []
    for f in families:
        result.append(
            {
                "family": f["problem"]["family"],
                "input_bytes": len(wire(f["problem"])),
                "base_bytes": len(wire(f["base"])),
                "selection_bytes": len(wire(f["selection"])),
                "decoder_bytes": len(wire(f["decoder"])),
                "witness_bytes": len(wire(f["witnesses"])),
                "producer_map_bytes": len(wire(f["selection"]["filters"])),
                "receiver_map_bytes": len(
                    wire({k: f["decoder"][k] for k in ("intercept", "matrix")})
                ),
                "native_family_bytes": len(wire(f)),
            }
        )
    return result


def expected_suite(families):
    return {
        "families": families,
        "prior_bridges": copy.deepcopy(BRIDGES),
        "payload_sizes": payload(families),
        "totals": {
            "families": 2,
            **{key: sum(f["counts"][key] for f in families) for key in families[0]["counts"]},
        },
        "scope": dict.fromkeys(SCOPE, False),
    }


def synthetic_history(family):
    p = family["problem"]
    return {
        "problem": {"family": p["family"]},
        "matrices": {
            "fine_response_rows": copy.deepcopy(p["target_labels"]),
            "coarse_observations": copy.deepcopy(p["observations"]),
            "repair_observations": copy.deepcopy(p["bank"]),
            "fine_targets": copy.deepcopy(p["targets"]),
        },
        "repair": {"intercept": [fw(0)] * len(p["targets"]), "matrix": copy.deepcopy(p["filters"])},
        "certificate": {
            **{key: copy.deepcopy(family["base"][key]) for key in BASE_FIELDS},
            "decoder": None,
            "collision": {"unselected": True},
        },
    }


def independent_history_checks(families, previous):
    for f, old in zip(families, previous, strict=True):
        assert f["problem"] == projected_problem(old)
        assert old["repair"]["intercept"] == [fw(0)] * len(f["problem"]["targets"])
        assert {key: f["base"][key] for key in BASE_FIELDS} == {
            key: old["certificate"][key] for key in BASE_FIELDS
        }


def test_synthetic_history_full_suite_and_all_cached_routes(runner, monkeypatch):
    problems = []
    for name, factory in zip(FAMILIES, (normalization_problem, empty_bank_problem), strict=True):
        p = factory()
        p["family"] = name
        problems.append(p)
    families = list(map(expected, problems))
    previous = list(map(synthetic_history, families))
    independent_history_checks(families, previous)
    wanted = expected_suite(families)
    lookup = {f["problem"]["family"]: f for f in families}

    def projection(old):
        for family in old:
            assert family["repair"]["intercept"] == [fw(0)] * len(
                family["matrices"]["fine_targets"]
            )
        return [projected_problem(f) for f in old], old

    monkeypatch.setattr(runner, "project_inputs", projection)
    monkeypatch.setattr(
        runner, "load_inputs", lambda: (copy.deepcopy(problems), copy.deepcopy(previous))
    )
    calls = []

    def loader(name):
        def build(p):
            assert set(p) == set(problems[0])
            calls.append((name, p["family"]))
            return copy.deepcopy(lookup[p["family"]])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    assert wire(runner.assemble_suite(families, previous)) == wire(wanted)
    for route, count in (("primary", 2), ("reference", 2), ("compare", 4)):
        calls.clear()
        assert wire(runner.run_suite(route)) == wire(wanted)
        assert len(calls) == count
    with pytest.raises(ValueError):
        runner.assemble_suite(families, tuple(previous))
    with pytest.raises(ValueError):
        runner.run_suite("unknown")

    def corrupts(p):
        result = copy.deepcopy(lookup[p["family"]])
        p["family"] = "changed"
        return result

    monkeypatch.setattr(runner, "load_engine", lambda name: SimpleNamespace(build_family=corrupts))
    with pytest.raises(ValueError):
        runner.run_suite("primary")


def test_missing_and_broken_symlink_replay_are_readonly(lifecycle):
    runner, path = lifecycle
    with pytest.raises(ValueError):
        runner.capture(path, verify=True)
    target = path.with_name("missing.json")
    path.symlink_to(target)
    with pytest.raises(FileExistsError):
        runner.capture(path)
    with pytest.raises(ValueError):
        runner.capture(path, verify=True)
    assert path.is_symlink() and not target.exists()


@pytest.fixture(scope="session")
def fixed_data(runner):
    problems, previous = runner.load_inputs()
    before = wire(problems)
    families = list(map(expected, problems))
    assert wire(problems) == before
    independent_history_checks(families, previous)
    return problems, previous, families, expected_suite(families)


@pytest.mark.parametrize("index", [0, 1])
def test_fixed_complete_engine_wires_and_online_witnesses(engines, fixed_data, index):
    problems, _, wanted, _ = fixed_data
    for engine in engines:
        p = copy.deepcopy(problems[index])
        frozen = wire(p)
        actual = engine.build_family(p)
        assert wire(p) == frozen
        assert wire(actual) == wire(wanted[index])
        for witness in actual["witnesses"]:
            assert witness["available_plus"] == witness["available_minus"]
            for sign in ("plus", "minus"):
                supplements = engine.produce(
                    actual["selection"]["filters"], witness["bank_" + sign]
                )
                assert supplements == witness["supplement_" + sign]
                assert (
                    engine.apply(
                        actual["decoder"]["intercept"],
                        actual["decoder"]["matrix"],
                        witness["coarse_" + sign] + supplements,
                    )
                    == witness["truth_" + sign]
                )


def test_fixed_complete_suite_counts_payload_and_selected_bridge(runner, fixed_data):
    problems, previous, families, wanted = fixed_data
    assert [p["family"] for p in problems] == list(FAMILIES)
    assert wire(runner.assemble_suite(families, previous)) == wire(wanted)
    assert runner.historical_bridges(families, previous) == BRIDGES
    assert runner.payload_sizes(families) == payload(families)
    for p, f in zip(problems, families, strict=True):
        assert len(p["observations"]) == 32 and len(p["bank"]) == 48
        assert len(p["targets"]) == 64 and len(p["targets"][0]) == 108
        assert f["base"]["delta"] == f["base"]["joint_rank"] - f["base"]["observation_rank"]
        assert f["selection"]["filters"] == [p["filters"][i] for i in f["selection"]["target_rows"]]
        assert len(f["witnesses"]) == len(f["selection"]["target_rows"]) == f["base"]["delta"]
        assert f["counts"]["selected_filter_nonzero"] == sum(
            fraction(x) != 0 for row in f["selection"]["filters"] for x in row
        )
        assert f["counts"]["selected_bank_rows"] == len(
            {i for row in f["selection"]["bank_support"] for i in row}
        )
    assert set(wanted["scope"]) == set(SCOPE) and not any(wanted["scope"].values())


@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_cached_orchestration_routes(runner, fixed_data, monkeypatch, route):
    _, _, families, wanted = fixed_data
    lookup = {f["problem"]["family"]: f for f in families}
    seen = []

    def loader(name):
        def build(p):
            assert p == lookup[p["family"]]["problem"]
            seen.append(name)
            return copy.deepcopy(lookup[p["family"]])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    assert wire(runner.run_suite(route)) == wire(wanted)
    assert seen == (["primary", "reference"] * 2 if route == "compare" else [route] * 2)


def test_fixed_full_output_and_suite_corruptions_are_nonvacuous(runner, fixed_data):
    _, _, families, wanted = fixed_data
    count = 0
    for family in families:
        for bad in family_mutations(family):
            assert wire(bad) != wire(family)
            with pytest.raises(ValueError):
                runner.verify_suite(bad, family)
            count += 1
    changes = [
        replaced(wanted, ["families"], list(reversed(families))),
        replaced(wanted, ["prior_bridges", "AR_filter_identity_rechecked"], False),
        replaced(wanted, ["prior_bridges", "older_executors_run"], True),
        replaced(
            wanted,
            ["payload_sizes", 0, "producer_map_bytes"],
            wanted["payload_sizes"][0]["producer_map_bytes"] + 1,
        ),
        replaced(
            wanted, ["totals", "supplement_values"], wanted["totals"]["supplement_values"] + 1
        ),
        replaced(wanted, ["scope", "individual_bank_minimality_proved"], True),
        replaced(wanted, ["scope", "nonlinear_encoding_minimality_proved"], True),
        {**wanted, "extra": 0},
    ]
    for bad in changes:
        assert wire(bad) != wire(wanted)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, wanted)
    assert count >= 100 and len(changes) == 8


def test_fixed_selected_producer_changes_and_unselected_collision_boundary(runner, fixed_data):
    problems, previous, families, _ = fixed_data
    changed = []
    for path in (
        [0, "matrices", "coarse_observations", 0, 0],
        [0, "matrices", "repair_observations", 0, 0],
        [0, "matrices", "fine_targets", 0, 0],
        [0, "repair", "matrix", 0, 0],
        [0, "repair", "intercept", 0],
    ):
        changed.append(changed_fraction(previous, path))
    changed.append(replaced(previous, [0, "matrices", "fine_response_rows", 0, "first"], 999))
    for key in BASE_FIELDS:
        current = previous[0]["certificate"][key]
        value = current + [-1] if type(current) is list else current + 1
        changed.append(replaced(previous, [0, "certificate", key], value))
    for bad in changed:
        assert wire(bad) != wire(previous)
        with pytest.raises(ValueError):
            runner.historical_bridges(families, bad)
    for key, value in (("decoder", []), ("collision", None)):
        bad = copy.deepcopy(previous)
        bad[0]["certificate"][key] = value
        assert wire(bad) != wire(previous)
        assert runner.project_inputs(bad)[0] == problems
        assert runner.historical_bridges(families, bad) == BRIDGES


def test_fixed_capture_source_and_ancestor_identity_inventory(runner):
    identity = runner.identities()
    assert {k: len(identity[k]) for k in identity} == {
        "source_ledger": 5,
        "prior_artifacts": 49,
        "ancestor_sources": 64,
    }
    assert set(identity["source_ledger"]) == set(runner.SOURCES)
    raw = runner.plain_bytes(runner.AR)
    assert len(raw) == 704842 and hashlib.sha256(raw).hexdigest() == (
        "c9ed0e299c057eb6503238a3bc5ce18352abe81bc111615464afaa6ed264e4f8"
    )
    envelope = json.loads(raw)
    assert runner.canonical(envelope) == raw
    native(envelope["suite"])
    for name, base in (
        ("source_ledger", HERE),
        ("prior_artifacts", HERE.parent),
        ("ancestor_sources", HERE.parent),
    ):
        for path, want in identity[name].items():
            data = runner.plain_bytes(base / path)
            assert len(data) == want["bytes"] and hashlib.sha256(data).hexdigest() == want["sha256"]
