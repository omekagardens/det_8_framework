"""Independent scalar and exhaustive-box checks of shared-bank errors.

Only test names containing fixed consume authenticated AU cases. Collection and generic
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
from itertools import product
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
        load("_qr05av_test_primary", "kernel.py"),
        load("_qr05av_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05av_test_runner", "study.py")


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


CHECKS = (
    "frozen_bank_identity",
    "error_map_identity",
    "normalized_error_identity",
    "primitive_box",
    "shared_pipeline",
    "shared_attainment",
    "enclosure_box",
    "enclosure_attainment",
    "complete_gain_partition",
)
SCOPE = (
    "source_dictionary_changed",
    "geometry_reintegrated",
    "decoder_refitted",
    "filters_reselected",
    "measurements_added",
    "normalization_row_added",
    "empirical_noise_calibrated",
    "stochastic_independence_assumed",
    "field_realizable_errors_required",
    "common_bank_feasibility_solved",
    "dimensionally_universal_noise_claimed",
    "full_field_stability_tested",
    "minimality_recomputed",
    "unknown_geometry_reconstructed",
    "physical_sensor_validated",
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


def scalar_product(left, right, width):
    # Indexed scalar contractions, independently authored rather than engine calls.
    return [
        [sum((left[i][h] * right[h][j] for h in range(len(right))), F()) for j in range(width)]
        for i in range(len(left))
    ]


def scalar_apply(a, values):
    return [sum((a[i][j] * values[j] for j in range(len(values))), F()) for i in range(len(a))]


def sign(value):
    return int(value > 0) - int(value < 0)


def expected(problem):
    b, g, d, w = (
        matrix(problem[key]) for key in ("interface", "geometric", "decoder", "primitive_map")
    )
    sigma = list(map(fraction, problem["target_scales"]))
    q, r, s, p = len(g), len(g[0]), len(b), len(w[0])
    k = scalar_product(d, b, r)
    assert k == g
    h = scalar_product(b, w, p)
    j = scalar_product(g, w, p)
    ell = scalar_product(d, h, p)
    assert ell == j
    normalized = [[x / sigma[i] for x in row] for i, row in enumerate(j)]
    beta = [sum(map(abs, row), F()) for row in h]
    enclosed = [[d[i][a] * beta[a] / sigma[i] for a in range(s)] for i in range(q)]
    alpha = [sum(map(abs, row), F()) for row in normalized]
    gamma = [sum(map(abs, row), F()) for row in enclosed]
    gap = [gamma[i] - alpha[i] for i in range(q)]
    assert all(x >= 0 for x in gap)
    shared_witnesses, enclosure_witnesses = [], []
    for i in range(q):
        signs = list(map(sign, normalized[i]))
        outer_signs = list(map(sign, enclosed[i]))
        inner, outer = {}, {}
        for label, direction in (("positive", 1), ("negative", -1)):
            primitive = [F(direction * x) for x in signs]
            bank = scalar_apply(w, primitive)
            observed = scalar_apply(b, bank)
            direct = scalar_apply(g, bank)
            decoded = scalar_apply(d, observed)
            result = [decoded[t] / sigma[t] for t in range(q)]
            assert direct == decoded
            assert observed == scalar_apply(h, primitive)
            assert result == scalar_apply(normalized, primitive)
            assert all(abs(result[t]) <= alpha[t] for t in range(q))
            assert all(abs(observed[a]) <= beta[a] for a in range(s))
            assert result[i] == direction * alpha[i]
            inner[label] = {
                "primitive": primitive,
                "bank_error": bank,
                "observed_error": observed,
                "direct_error": direct,
                "decoded_error": decoded,
                "normalized_error": result,
                "attained": result[i],
            }
            observed_outer = [direction * beta[a] * outer_signs[a] for a in range(s)]
            decoded_outer = scalar_apply(d, observed_outer)
            normalized_outer = [decoded_outer[t] / sigma[t] for t in range(q)]
            assert all(abs(normalized_outer[t]) <= gamma[t] for t in range(q))
            assert normalized_outer[i] == direction * gamma[i]
            outer[label] = {
                "observed_error": observed_outer,
                "decoded_error": decoded_outer,
                "normalized_error": normalized_outer,
                "attained": normalized_outer[i],
            }
        shared_witnesses.append({"target_row": i, "signs": signs, **inner})
        enclosure_witnesses.append({"target_row": i, "signs": outer_signs, **outer})
    max_alpha, max_gamma, max_gap = max(alpha), max(gamma), max(gap)
    a_rows = [i for i in range(q) if alpha[i] == max_alpha]
    g_rows = [i for i in range(q) if gamma[i] == max_gamma]
    gap_rows = [i for i in range(q) if gap[i] == max_gap]
    strict, tied = [i for i in range(q) if gap[i] > 0], [i for i in range(q) if gap[i] == 0]
    return encode(
        {
            "problem": copy.deepcopy(problem),
            "maps": {
                "decoder_bank": k,
                "bank_residual": [[F()] * r for _ in range(q)],
                "interface_error": h,
                "target_error": j,
                "decoded_error": ell,
                "error_residual": [[F()] * p for _ in range(q)],
                "normalized_target": normalized,
                "enclosure_target": enclosed,
            },
            "shared": {
                "row_gains": alpha,
                "witnesses": shared_witnesses,
                "max_gain": max_alpha,
                "max_rows": a_rows,
            },
            "enclosure": {
                "receiver_radii": beta,
                "row_gains": gamma,
                "witnesses": enclosure_witnesses,
                "max_gain": max_gamma,
                "max_rows": g_rows,
                "common_bank_feasibility_tested": False,
            },
            "comparison": {
                "gain_gap": gap,
                "strict_rows": strict,
                "tied_rows": tied,
                "max_gap": max_gap,
                "max_gap_rows": gap_rows,
            },
            "checks": dict.fromkeys(CHECKS, True),
            "counts": {
                "bank_values": r,
                "receiver_values": s,
                "primitive_values": p,
                "target_rows": q,
                "input_matrix_entries": s * r + q * r + q * s + r * p + q,
                "map_entries": 2 * q * r + s * p + 4 * q * p + q * s,
                "gain_entries": s + 3 * q + 3,
                "shared_witnesses": 2 * q,
                "shared_sign_entries": q * p,
                "shared_witness_entries": 2 * q * (p + r + s + 3 * q + 1),
                "enclosure_witnesses": 2 * q,
                "enclosure_sign_entries": q * s,
                "enclosure_witness_entries": 2 * q * (s + 2 * q + 1),
                "shared_maximizers": len(a_rows),
                "enclosure_maximizers": len(g_rows),
                "gap_maximizers": len(gap_rows),
                "strict_rows": len(strict),
                "tied_rows": len(tied),
            },
        }
    )


def make_problem(b, d, w, sigma=None, name="synthetic"):
    b, d, w = ([[F(x) for x in row] for row in a] for a in (b, d, w))
    r, q = len(w), len(d)
    if sigma is None:
        sigma = [F(1)] * q
    return encode(
        {
            "family": name,
            "target_labels": [{"first": i - 4, "second": -8} for i in range(q)],
            "interface": b,
            "geometric": scalar_product(d, b, r),
            "decoder": d,
            "primitive_map": w,
            "target_scales": list(map(F, sigma)),
        }
    )


def cancellation_problem():
    return make_problem([[1], [1]], [[1, -1]], [[1]], name="cancellation")


def strict_problem():
    return make_problem([[1, 1], [1, -1]], [[1, 1]], identity(2), name="strict")


def tied_unreachable_problem():
    return make_problem([[1], [1]], [[1, 0]], [[1]], name="tied-unreachable")


def opposite_problem():
    return make_problem([[1]], [[1], [-1], [1], [0]], [[1]], name="opposite")


def signed_problem():
    return make_problem(
        [[1, 2], [-1, 1]], [[1, -1], [0, 2], [-1, 1]], [[1, -1, 0], [2, -2, 0]], [2, 3, 5], "signed"
    )


def zero_beta_problem():
    return make_problem([[1, 0], [0, 0]], [[1, 77]], identity(2), name="zero-beta")


def empty_problem():
    return make_problem([], [[], []], [[], []], name="empty")


def no_primitive_problem():
    return make_problem([[1, -1]], [[2], [0]], [[], []], name="no-primitive")


@pytest.mark.parametrize(
    "factory",
    [
        cancellation_problem,
        strict_problem,
        tied_unreachable_problem,
        opposite_problem,
        signed_problem,
        zero_beta_problem,
        empty_problem,
        no_primitive_problem,
        lambda: make_problem([[0]], [[0], [0]], [[0, 0]], name="all-zero"),
    ],
)
def test_generic_full_scalar_wire_and_exhaustive_cube_extrema(engines, factory):
    p = factory()
    want = expected(p)
    b, d, w = (matrix(p[key]) for key in ("interface", "decoder", "primitive_map"))
    sigma = list(map(fraction, p["target_scales"]))
    gains = [fraction(x) for x in want["shared"]["row_gains"]]
    beta = [fraction(x) for x in want["enclosure"]["receiver_radii"]]
    outer = [fraction(x) for x in want["enclosure"]["row_gains"]]
    primitive_values = [
        [v / sigma[i] for i, v in enumerate(scalar_apply(d, scalar_apply(b, scalar_apply(w, xi))))]
        for xi in product((-1, 1), repeat=len(w[0]))
    ]
    enclosure_values = [
        [
            v / sigma[i]
            for i, v in enumerate(scalar_apply(d, [a * z for a, z in zip(beta, xi, strict=True)]))
        ]
        for xi in product((-1, 1), repeat=len(b))
    ]
    for i in range(len(d)):
        assert min(v[i] for v in primitive_values) == -gains[i]
        assert max(v[i] for v in primitive_values) == gains[i]
        assert min(v[i] for v in enclosure_values) == -outer[i]
        assert max(v[i] for v in enclosure_values) == outer[i]
    for engine in engines:
        before = wire(p)
        assert wire(engine.build_family(p)) == wire(want)
        assert wire(p) == before


def test_cancellation_zero_truth_and_strict_positive_enclosure_gap(engines):
    for engine in engines:
        zero = engine.build_family(cancellation_problem())
        assert zero["shared"]["row_gains"] == [fw(0)]
        assert zero["enclosure"]["row_gains"] == [fw(2)]
        assert zero["shared"]["witnesses"][0]["positive"]["primitive"] == [fw(0)]
        assert zero["shared"]["witnesses"][0]["negative"]["primitive"] == [fw(0)]
        strict = engine.build_family(strict_problem())
        assert strict["shared"]["row_gains"] == [fw(2)]
        assert strict["enclosure"]["receiver_radii"] == [fw(2), fw(2)]
        assert strict["enclosure"]["row_gains"] == [fw(4)]
        eta = strict["enclosure"]["witnesses"][0]["positive"]["observed_error"]
        assert eta == [fw(2), fw(2)]
        # The hand-computed inverse B requires primitive (2,0), outside the box.
        xi = [(fraction(eta[0]) + fraction(eta[1])) / 2, (fraction(eta[0]) - fraction(eta[1])) / 2]
        assert xi == [2, 0] and max(map(abs, xi)) > 1


def test_tied_bounds_do_not_make_canonical_enclosure_witness_reachable(engines):
    for engine in engines:
        a = engine.build_family(tied_unreachable_problem())
        assert a["shared"]["row_gains"] == a["enclosure"]["row_gains"] == [fw(1)]
        assert a["comparison"]["tied_rows"] == [0]
        eta = a["enclosure"]["witnesses"][0]["positive"]["observed_error"]
        assert eta == [fw(1), fw(0)]
        # Every shared observed vector is (xi,xi), so this canonical eta is not one.
        assert eta[0] != eta[1]
        assert a["enclosure"]["common_bank_feasibility_tested"] is False


def test_full_cross_target_witnesses_all_ties_and_zero_beta_signs(engines):
    for engine in engines:
        a = engine.build_family(opposite_problem())
        assert a["shared"]["max_rows"] == a["enclosure"]["max_rows"] == [0, 1, 2]
        assert a["comparison"]["max_gap_rows"] == [0, 1, 2, 3]
        assert a["shared"]["witnesses"][0]["positive"]["normalized_error"] == list(
            map(fw, [1, -1, 1, 0])
        )
        assert a["shared"]["witnesses"][1]["positive"]["normalized_error"] == list(
            map(fw, [-1, 1, -1, 0])
        )
        zero = a["shared"]["witnesses"][3]
        assert zero["signs"] == [0] and zero["positive"] == zero["negative"]
        z = engine.build_family(zero_beta_problem())
        assert z["enclosure"]["receiver_radii"] == [fw(1), fw(0)]
        assert z["enclosure"]["witnesses"][0]["signs"] == [1, 0]
        assert z["enclosure"]["row_gains"] == [fw(1)]
        e = engine.build_family(empty_problem())
        assert (
            e["shared"]["max_rows"]
            == e["enclosure"]["max_rows"]
            == e["comparison"]["max_gap_rows"]
            == [0, 1]
        )


def test_rank_deficient_error_map_cannot_hide_incorrect_bank_identity(engines):
    p = make_problem([[1, 0]], [[1]], [[1], [0]])
    bad = replaced(p, ["geometric", 0, 1], fw(7))
    assert scalar_product(matrix(bad["geometric"]), matrix(bad["primitive_map"]), 1) == [[F(1)]]
    for engine in engines:
        with pytest.raises(ValueError):
            engine.build_family(bad)
        # Zero-column errors similarly cannot excuse a wrong whole-bank map.
        bad_empty = replaced(no_primitive_problem(), ["geometric", 0, 0], fw(9))
        with pytest.raises(ValueError):
            engine.build_family(bad_empty)


def test_full_signed_transport_preserves_shared_domain_not_receiver_enclosure(engines):
    p = signed_problem()
    b, g, d, w = (matrix(p[k]) for k in ("interface", "geometric", "decoder", "primitive_map"))
    bank = [[F(2), F(1)], [F(0), F(-1)]]
    bank_inverse = [[F(1, 2), F(1, 2)], [F(0), F(-1)]]
    receiver = [[F(1), F(1)], [F(1), F(-1)]]
    receiver_inverse = [[F(1, 2), F(1, 2)], [F(1, 2), F(-1, 2)]]
    v = F(7, 3)
    moved = copy.deepcopy(p)
    moved["family"] = "transported"
    moved["interface"] = encode(mm(mm(receiver, b), bank_inverse))
    moved["geometric"] = encode([[v * x for x in row] for row in mm(g, bank_inverse)])
    moved["decoder"] = encode([[v * x for x in row] for row in mm(d, receiver_inverse)])
    moved["primitive_map"] = encode(mm(bank, w))
    moved["target_scales"] = [fw(v * fraction(x)) for x in p["target_scales"]]
    for engine in engines:
        old, new = engine.build_family(p), engine.build_family(moved)
        assert wire(new) == wire(expected(moved))
        assert new["maps"]["normalized_target"] == old["maps"]["normalized_target"]
        assert new["shared"]["row_gains"] == old["shared"]["row_gains"]
        assert new["shared"]["max_rows"] == old["shared"]["max_rows"]
        assert matrix(new["maps"]["interface_error"]) == mm(
            receiver, matrix(old["maps"]["interface_error"])
        )
        for first, second in zip(
            old["shared"]["witnesses"], new["shared"]["witnesses"], strict=True
        ):
            assert second["signs"] == first["signs"]
            for label in ("positive", "negative"):
                a, z = first[label], second[label]
                assert z["primitive"] == a["primitive"]
                assert (
                    z["normalized_error"] == a["normalized_error"]
                    and z["attained"] == a["attained"]
                )
                assert z["bank_error"] == encode(mv(bank, list(map(fraction, a["bank_error"]))))
                assert z["observed_error"] == encode(
                    mv(receiver, list(map(fraction, a["observed_error"])))
                )
                for key in ("direct_error", "decoded_error"):
                    assert z[key] == [fw(v * fraction(x)) for x in a[key]]
        # Correct target-scale transport prevents a change in arbitrary reference units.
        assert new["shared"]["max_gain"] == old["shared"]["max_gain"]


def test_receiver_mixing_changes_enclosure_but_monomial_rescaling_does_not(engines):
    p = strict_problem()
    t = [[F(1, 2), F(1, 2)], [F(1, 2), F(-1, 2)]]
    ti = [[F(1), F(1)], [F(1), F(-1)]]
    changed = copy.deepcopy(p)
    changed["interface"] = encode(mm(t, matrix(p["interface"])))
    changed["decoder"] = encode(mm(matrix(p["decoder"]), ti))
    mono = copy.deepcopy(p)
    mono["interface"] = encode(
        [
            [F(-3) * x for x in matrix(p["interface"])[1]],
            [F(2) * x for x in matrix(p["interface"])[0]],
        ]
    )
    mono["decoder"] = [[fw(F(-1, 3)), fw(F(1, 2))]]
    for engine in engines:
        original, mixed, monomial = [engine.build_family(x) for x in (p, changed, mono)]
        assert mixed["shared"]["row_gains"] == original["shared"]["row_gains"] == [fw(2)]
        assert mixed["enclosure"]["row_gains"] == [fw(2)]
        assert original["enclosure"]["row_gains"] == [fw(4)]
        assert monomial["enclosure"]["row_gains"] == original["enclosure"]["row_gains"]
        assert wire(mixed) == wire(expected(changed))
        assert wire(monomial) == wire(expected(mono))


def test_signed_primitive_permutations_and_epsilon_scaling(engines):
    p = signed_problem()
    moved = copy.deepcopy(p)
    permutation, signs = [2, 0, 1], [-1, 1, -1]
    moved["primitive_map"] = [
        [fw(signs[j] * fraction(row[permutation[j]])) for j in range(3)]
        for row in p["primitive_map"]
    ]
    for engine in engines:
        old, new = engine.build_family(p), engine.build_family(moved)
        assert wire(new) == wire(expected(moved))
        assert new["shared"]["row_gains"] == old["shared"]["row_gains"]
        assert new["enclosure"]["row_gains"] == old["enclosure"]["row_gains"]
        for a, z in zip(old["shared"]["witnesses"], new["shared"]["witnesses"], strict=True):
            assert z["signs"] == [signs[j] * a["signs"][permutation[j]] for j in range(3)]
            for side in ("positive", "negative"):
                for key in (
                    "bank_error",
                    "observed_error",
                    "direct_error",
                    "decoded_error",
                    "normalized_error",
                    "attained",
                ):
                    assert z[side][key] == a[side][key]
        for epsilon in (F(0), F(3, 2), F(7)):
            changed = replaced(
                p,
                ["primitive_map"],
                [[fw(epsilon * fraction(x)) for x in row] for row in p["primitive_map"]],
            )
            result = engine.build_family(changed)
            assert wire(result) == wire(expected(changed))
            for group in ("shared", "enclosure"):
                assert result[group]["row_gains"] == [
                    fw(epsilon * fraction(x)) for x in old[group]["row_gains"]
                ]
            if epsilon:
                for before, after in zip(
                    old["shared"]["witnesses"], result["shared"]["witnesses"], strict=True
                ):
                    assert after["signs"] == before["signs"]
                    for side in ("positive", "negative"):
                        for key in (
                            "bank_error",
                            "observed_error",
                            "direct_error",
                            "decoded_error",
                            "normalized_error",
                        ):
                            assert after[side][key] == [
                                fw(epsilon * fraction(x)) for x in before[side][key]
                            ]
            else:
                assert result["shared"]["max_rows"] == list(range(3))
                assert all(row["signs"] == [0] * 3 for row in result["shared"]["witnesses"])


def test_every_full_endpoint_uses_restricted_actual_pipeline(engines, monkeypatch):
    from collections import Counter

    for engine in engines:
        for factory in (cancellation_problem, signed_problem, empty_problem):
            p = factory()
            recorded = {"produce": [], "apply": []}
            originals = {name: getattr(engine, name) for name in recorded}
            for name, original in originals.items():

                def spy(a, x, name=name, original=original, recorded=recorded):
                    recorded[name].append(wire([a, x]))
                    return original(a, x)

                monkeypatch.setattr(engine, name, spy)
            a = engine.build_family(p)
            required = {"produce": [], "apply": []}
            for row in a["shared"]["witnesses"]:
                for side in ("positive", "negative"):
                    e = row[side]
                    for bank_map, values in (
                        (p["primitive_map"], e["primitive"]),
                        (p["interface"], e["bank_error"]),
                        (p["geometric"], e["bank_error"]),
                    ):
                        required["produce"].append(wire([bank_map, values]))
                    required["apply"].append(wire([p["decoder"], e["observed_error"]]))
            for row in a["enclosure"]["witnesses"]:
                for side in ("positive", "negative"):
                    required["apply"].append(wire([p["decoder"], row[side]["observed_error"]]))
            for name, original in originals.items():
                got, want = Counter(recorded[name]), Counter(required[name])
                assert all(got[key] >= count for key, count in want.items())
                monkeypatch.setattr(engine, name, original)


def test_raw_evaluators_no_intercept_or_file_access(engines, monkeypatch):
    def forbidden(*args, **kwargs):
        raise RuntimeError("restricted evaluator attempted file access")

    for engine in engines:
        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "read_bytes", forbidden)
            patch.setattr(Path, "read_text", forbidden)
            assert engine.produce([], [fw(99)]) == []
            assert engine.produce([[], []], []) == [fw(0), fw(0)]
            assert engine.apply([], []) == []
            assert engine.apply([[], []], []) == [fw(0), fw(0)]
            a, x = [[fw(2), fw(-3), fw(F(1, 2))]], list(map(fw, [-1, 7, 4]))
            assert engine.produce(a, x) == engine.apply(a, x) == [fw(-21)]
            with pytest.raises(TypeError):
                engine.apply([fw(9)], a, x)


def test_shared_aliases_and_output_detachment(engines):
    p = make_problem([[1], [1]], [[1, 0], [1, 0]], [[1]])
    p["interface"][1] = p["interface"][0]
    p["decoder"][1] = p["decoder"][0]
    before = wire(p)
    for engine in engines:
        a = engine.build_family(p)
        a["problem"]["decoder"][0][0][0] += 99
        a["shared"]["witnesses"][0]["positive"]["primitive"][0][0] += 77
        assert a["shared"]["witnesses"][1]["positive"]["primitive"] == [fw(1)]
        assert a["shared"]["witnesses"][0]["negative"]["primitive"] == [fw(-1)]
        assert wire(p) == before
        assert wire(engine.build_family(p)) == wire(expected(p))
        rows = [[fw(2)], [fw(2)]]
        rows[1] = rows[0]
        result = engine.apply(rows, [fw(3)])
        result[0][0] += 22
        assert result[1] == fw(6) and rows[0] == [fw(2)]


def test_admitted_cap_edges_in_separate_small_workloads(engines):
    cases = [
        make_problem([], [[]], [[] for _ in range(1024)]),
        make_problem([[0]] * 320, [[0] * 320], [[]]),
        make_problem([], [[] for _ in range(64)], [[]]),
        make_problem([[1]], [[1]], [[F(i, 257) for i in range(256)]]),
    ]
    for engine in engines:
        assert engine.produce([[]] * 1024, []) == [fw(0)] * 1024
        assert engine.produce([], [fw(0)] * 1024) == []
        assert engine.apply([[fw(0)] * 320] * 64, [fw(0)] * 320) == [fw(0)] * 64
        for p in cases:
            assert wire(engine.build_family(p)) == wire(expected(p))
        tiny = make_problem([[1]], [[1]], [[F(1, 1 << 3500)]])
        assert engine.build_family(tiny)["shared"]["row_gains"] == [fw(F(1, 1 << 3500))]


class NativeListSubclass(list):
    pass


class NativeDictSubclass(dict):
    pass


class NativeIntSubclass(int):
    pass


def malformed_families():
    p = signed_problem()
    yield None
    yield []
    yield NativeDictSubclass(p)
    yield {**p, "offset": [fw(0)] * 3}
    for key in p:
        yield {k: v for k, v in p.items() if k != key}
    for value in ("", False, 1):
        yield replaced(p, ["family"], value)
    for key in p.keys() - {"family"}:
        for value in (None, tuple(p[key]), NativeListSubclass(p[key])):
            yield replaced(p, [key], value)
    yield replaced(p, ["target_labels"], list(reversed(p["target_labels"])))
    yield replaced(p, ["target_labels", 1], p["target_labels"][0])
    yield replaced(p, ["target_labels", 0, "first"], True)
    yield replaced(p, ["target_labels", 0, "second"], NativeIntSubclass(-8))
    yield replaced(p, ["target_labels", 0, "extra"], 0)
    for key in ("interface", "geometric", "decoder", "primitive_map"):
        yield replaced(p, [key, -1], [])
        yield replaced(p, [key, -1], tuple(p[key][-1]))
    yield replaced(p, ["interface"], p["interface"] * 161)
    yield replaced(p, ["geometric"], p["geometric"] * 22)
    yield replaced(p, ["geometric"], [[fw(0)] * 1025] * 3)
    yield replaced(p, ["geometric"], [])
    yield replaced(p, ["primitive_map"], p["primitive_map"][:-1])
    yield replaced(p, ["primitive_map"], [[fw(0)] * 257] * 2)
    yield replaced(p, ["target_scales"], p["target_scales"][:-1])
    yield replaced(p, ["geometric", 0, 0], fw(99))
    for value in (fw(0), fw(-1)):
        yield replaced(p, ["target_scales", -1], value)
    for value in (
        True,
        0.0,
        F(0),
        (0, 1),
        [0],
        [0, 1, 2],
        [0, 0],
        [0, -1],
        [2, 2],
        [1 << 4096, 1],
        [0, True],
        [NativeIntSubclass(0), 1],
        NativeListSubclass([0, 1]),
    ):
        yield replaced(p, ["target_scales", -1], value)
        yield replaced(p, ["primitive_map", -1, -1], value)


def malformed_evaluators(row_cap, width_cap):
    a, x = [[fw(1), fw(-1), fw(2)]], list(map(fw, [3, 4, 5]))
    for value in (None, {}, (), NativeListSubclass(a), a * (row_cap + 1)):
        yield value, x
    for value in (None, {}, (), NativeListSubclass(x), x[:-1], [fw(0)] * (width_cap + 1)):
        yield a, value
    yield a + [[fw(0)] * 2], x
    for value in (True, 0.0, F(0), (0, 1), [0], [0, 0], [2, 2], [1 << 4096, 1]):
        yield replaced(a, [0, 2], value), x
        yield a, replaced(x, [2], value)
    yield [], [True]


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
    for name, rowcap, widthcap in (("produce", 1024, 1024), ("apply", 64, 320)):
        call = getattr(engine, name)
        for a, x in malformed_evaluators(rowcap, widthcap):
            require_rejection(lambda a=a, x=x, call=call: call(a, x))
            count += 1
    d = 1 << 4095
    for name in ("produce", "apply"):
        call = getattr(engine, name)
        if call([[fw(d), fw(-d)]], [fw(2), fw(2)]) != [fw(0)]:
            raise RuntimeError("canceled unretained products")
        require_rejection(lambda call=call: call([[fw(d), fw(d)]], [fw(1), fw(1)]))
    canceled = make_problem([[d], [d]], [[2, -2]], [[]])
    if engine.build_family(canceled)["maps"]["decoder_bank"] != [[fw(0)]]:
        raise RuntimeError("full-bank product cancellation")
    oversized = [
        make_problem([[1]], [[1]], [[d, d]]),
        make_problem([[1], [1]], [[d, -d]], [[1]]),
        make_problem([[1]], [[0]], [[d, d]]),
        make_problem([[1]], [[1]], [[d]], [F(1, d)]),
    ]
    for p in oversized:
        require_rejection(lambda p=p: engine.build_family(p))
    bad = replaced(make_problem([[1, 0]], [[1]], [[1], [0]]), ["geometric", 0, 1], fw(7))
    require_rejection(lambda: engine.build_family(bad))
    cyclic = signed_problem()
    cyclic["primitive_map"].append(cyclic["primitive_map"])
    require_rejection(lambda: engine.build_family(cyclic))
    cycle = []
    cycle.append(cycle)
    require_rejection(lambda: engine.produce(cycle, [fw(1)]))
    require_rejection(lambda: engine.apply([[fw(1)]], cycle))
    return count + 10


def pre_arithmetic_guards(engine):
    calls = []

    def forbidden(*args, **kwargs):
        calls.append(1)
        raise RuntimeError("arithmetic before complete admission")

    original = engine._fraction
    engine._fraction = forbidden
    try:
        for value in ([], [0]):
            require_rejection(
                lambda value=value: engine.build_family(
                    replaced(signed_problem(), ["target_scales", -1], value)
                )
            )
            require_rejection(lambda value=value: engine.produce([[fw(1)], [value]], [fw(2)]))
            require_rejection(lambda value=value: engine.apply([[fw(1)], [value]], [fw(2)]))
    finally:
        engine._fraction = original
    names = [
        n
        for n in ("_dot", "_mm", "_multiply", "_probe_maps", "_interval_radius")
        if hasattr(engine, n)
    ]
    originals = {name: getattr(engine, name) for name in names}
    for name in names:
        setattr(engine, name, forbidden)
    try:
        require_rejection(
            lambda: engine.build_family(replaced(signed_problem(), ["target_scales", -1], [1, 0]))
        )
        require_rejection(lambda: engine.produce([[fw(1)], [[1, 0]]], [fw(1)]))
        require_rejection(lambda: engine.apply([[fw(1)], [[1, 0]]], [fw(1)]))
    finally:
        for name, original in originals.items():
            setattr(engine, name, original)
    if calls:
        raise RuntimeError("late admission ordering")
    return 9


def test_native_shape_value_bank_identity_and_bit_guards(engines):
    counts = [explicit_guards(engine) for engine in engines]
    assert counts[0] == counts[1] and counts[0] > 100
    assert [pre_arithmetic_guards(engine) for engine in engines] == [9, 9]


@pytest.mark.parametrize("optimized", [False, True])
def test_isolated_explicit_normal_and_optimized_guards(tmp_path, optimized):
    script = r"""
import importlib.util,json,sys
from pathlib import Path
path=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("av_guard_tests",path)
t=importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
counts=[]
for name,file in (("primary","kernel.py"),("reference","reference.py")):
    engine=t.load("_qr05av_guard_"+name,file)
    counts.append(t.explicit_guards(engine)+t.pre_arithmetic_guards(engine))
print(json.dumps(counts))
"""
    args = [sys.executable, "-I", "-X", "pycache_prefix=" + str(tmp_path / "cache")]
    if optimized:
        args.append("-O")
    result = subprocess.run(
        [*args, "-c", script, str(Path(__file__).resolve())],
        capture_output=True,
        text=True,
        check=True,
        timeout=120,
    )
    total = (
        len(list(malformed_families()))
        + len(list(malformed_evaluators(1024, 1024)))
        + len(list(malformed_evaluators(64, 320)))
        + 19
    )
    assert json.loads(result.stdout) == [total, total]


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


BRIDGES = {
    "AU_selected_families": list(FAMILIES),
    "AU_interface_inputs_equal": True,
    "AU_target_inputs_equal": True,
    "AU_decoder_inputs_equal": True,
    "AU_complete_target_indexing": True,
    "fixed_raw_unit_box": True,
    "frozen_bank_identity_rechecked": True,
    "other_historical_mathematics_replayed": False,
    "older_executors_run": False,
}


def changed_fraction(tree, path):
    value = tree
    for key in path:
        value = value[key]
    return replaced(tree, path, fw(fraction(value) + 1))


def family_mutations(f):
    for key in f:
        yield {k: v for k, v in f.items() if k != key}
    yield {**f, "extra": 0}
    yield replaced(f, ["problem", "family"], f["problem"]["family"] + "-wrong")
    yield changed_fraction(f, ["problem", "target_scales", 0])
    for key, value in f["maps"].items():
        if value and value[0]:
            yield changed_fraction(f, ["maps", key, 0, 0])
        else:
            yield replaced(f, ["maps", key], [[fw(0)]])
    for group in ("shared", "enclosure"):
        part = f[group]
        yield changed_fraction(f, [group, "row_gains", 0])
        yield changed_fraction(f, [group, "max_gain"])
        yield replaced(f, [group, "max_rows"], [*part["max_rows"], -1])
        yield replaced(f, [group, "witnesses"], part["witnesses"][:-1])
        row = part["witnesses"][0]
        yield replaced(f, [group, "witnesses", 0, "target_row"], 1)
        if row["signs"]:
            yield replaced(f, [group, "witnesses", 0, "signs", 0], 2)
            yield replaced(f, [group, "witnesses", 0, "signs", 0], False)
        else:
            yield replaced(f, [group, "witnesses", 0, "signs"], [0])
        for side in ("positive", "negative"):
            endpoint = row[side]
            for key, value in endpoint.items():
                if key == "attained":
                    yield changed_fraction(f, [group, "witnesses", 0, side, key])
                elif value:
                    yield changed_fraction(f, [group, "witnesses", 0, side, key, 0])
                else:
                    yield replaced(f, [group, "witnesses", 0, side, key], [fw(0)])
    yield replaced(f, ["enclosure", "common_bank_feasibility_tested"], True)
    yield replaced(f, ["enclosure", "witnesses", 0, "positive", "primitive"], [])
    if f["enclosure"]["receiver_radii"]:
        yield changed_fraction(f, ["enclosure", "receiver_radii", 0])
    else:
        yield replaced(f, ["enclosure", "receiver_radii"], [fw(0)])
    yield changed_fraction(f, ["comparison", "gain_gap", 0])
    yield changed_fraction(f, ["comparison", "max_gap"])
    for key in ("strict_rows", "tied_rows", "max_gap_rows"):
        yield replaced(f, ["comparison", key], [*f["comparison"][key], -1])
    for key in CHECKS:
        yield replaced(f, ["checks", key], False)
    for key in (
        "map_entries",
        "gain_entries",
        "shared_witness_entries",
        "enclosure_witness_entries",
        "shared_maximizers",
        "gap_maximizers",
    ):
        yield replaced(f, ["counts", key], f["counts"][key] + 1)


def literal_count_checks(f):
    p, c = f["problem"], f["counts"]
    assert c["input_matrix_entries"] == sum(
        len(row) for key in ("interface", "geometric", "decoder", "primitive_map") for row in p[key]
    ) + len(p["target_scales"])
    assert c["map_entries"] == sum(len(row) for a in f["maps"].values() for row in a)
    assert c["gain_entries"] == (
        len(f["enclosure"]["receiver_radii"])
        + len(f["shared"]["row_gains"])
        + len(f["enclosure"]["row_gains"])
        + len(f["comparison"]["gain_gap"])
        + 3
    )
    for group in ("shared", "enclosure"):
        witnesses = f[group]["witnesses"]
        assert c[group + "_witnesses"] == 2 * len(witnesses)
        assert c[group + "_sign_entries"] == sum(len(w["signs"]) for w in witnesses)
        assert c[group + "_witness_entries"] == sum(
            1 if key == "attained" else len(value)
            for witness in witnesses
            for side in ("positive", "negative")
            for key, value in witness[side].items()
        )
        assert c[group + "_maximizers"] == len(f[group]["max_rows"])
    assert c["gap_maximizers"] == len(f["comparison"]["max_gap_rows"])
    assert c["strict_rows"] == len(f["comparison"]["strict_rows"])
    assert c["tied_rows"] == len(f["comparison"]["tied_rows"])


def test_generic_full_wire_mutations_and_literal_payload_counts(runner):
    for factory in (cancellation_problem, strict_problem, signed_problem, empty_problem):
        f = expected(factory())
        literal_count_checks(f)
        for bad in family_mutations(f):
            assert wire(bad) != wire(f)
            with pytest.raises(ValueError):
                runner.verify_suite(bad, f)


def projected_problem(old):
    p = old["problem"]
    r, q = len(p["geometric"][0]), len(p["geometric"])
    return {
        "family": p["family"],
        "target_labels": copy.deepcopy(p["target_labels"]),
        "interface": copy.deepcopy(old["interface"]),
        "geometric": copy.deepcopy(p["geometric"]),
        "decoder": copy.deepcopy(old["decoder"]["matrix"]),
        "primitive_map": encode(identity(r)),
        "target_scales": [fw(1)] * q,
    }


def independent_history_checks(families, previous):
    assert [f["problem"]["family"] for f in families] == list(FAMILIES)
    assert [old["problem"]["family"] for old in previous] == list(FAMILIES)
    for f, old in zip(families, previous, strict=True):
        assert wire(f["problem"]) == wire(projected_problem(old))
        assert old["decoder"]["target_rows"] == list(range(len(f["problem"]["geometric"])))
        literal_count_checks(f)


def payload(families):
    return [
        {
            "family": f["problem"]["family"],
            "input_bytes": len(wire(f["problem"])),
            "map_bytes": len(wire(f["maps"])),
            "shared_bytes": len(wire(f["shared"])),
            "enclosure_bytes": len(wire(f["enclosure"])),
            "comparison_bytes": len(wire(f["comparison"])),
            "native_family_bytes": len(wire(f)),
        }
        for f in families
    ]


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


def synthetic_history(p):
    return {
        "problem": {
            "family": p["family"],
            "target_labels": copy.deepcopy(p["target_labels"]),
            "geometric": copy.deepcopy(p["geometric"]),
            "bank": "not read",
        },
        "interface": copy.deepcopy(p["interface"]),
        "decoder": {
            "matrix": copy.deepcopy(p["decoder"]),
            "target_rows": list(range(len(p["geometric"]))),
            "complete": False,
        },
        "certificate": {"interface_rank": 999, "collision": "not read"},
        "source": {"geometric_values": "not read"},
        "bank_controls": [],
    }


def test_synthetic_history_full_suite_and_all_cached_routes(runner, monkeypatch):
    problems = []
    for name, factory in zip(FAMILIES, (cancellation_problem, strict_problem), strict=True):
        p = factory()
        p["family"] = name
        problems.append(p)
    families = list(map(expected, problems))
    previous = list(map(synthetic_history, problems))
    independent_history_checks(families, previous)
    wanted = expected_suite(families)
    lookup = {f["problem"]["family"]: f for f in families}

    def projection(prior):
        return [projected_problem(old) for old in prior], prior

    monkeypatch.setattr(runner, "project_inputs", projection)
    monkeypatch.setattr(
        runner, "load_inputs", lambda: (copy.deepcopy(problems), copy.deepcopy(previous))
    )
    calls = []

    def loader(name):
        def build(p):
            assert set(p) == set(problems[0])
            calls.append(name)
            return copy.deepcopy(lookup[p["family"]])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    assert wire(runner.assemble_suite(families, previous)) == wire(wanted)
    for route, count in (("primary", 2), ("reference", 2), ("compare", 4)):
        calls.clear()
        assert wire(runner.run_suite(route)) == wire(wanted)
        assert len(calls) == count
    with pytest.raises(ValueError):
        runner.run_suite("unknown")
    bad = replaced(previous, [0, "certificate", "interface_rank"], 777)
    with pytest.raises(ValueError):
        runner.assemble_suite(families, bad)
    assert runner.historical_bridges(families, bad) == BRIDGES

    def changing(p):
        result = copy.deepcopy(lookup[p["family"]])
        p["family"] = "changed"
        return result

    monkeypatch.setattr(runner, "load_engine", lambda name: SimpleNamespace(build_family=changing))
    with pytest.raises(ValueError):
        runner.run_suite("primary")


def test_synthetic_selected_indexing_projection_inventory_and_detachment(runner):
    # Newly written synthetic zeros at selected historical dimensions: no prior data.
    p = make_problem([[0] * 48] * 37, [[0] * 37] * 64, identity(48))
    previous = []
    for name in FAMILIES:
        supplied = copy.deepcopy(p)
        supplied["family"] = name
        previous.append(synthetic_history(supplied))
    before = wire(previous)
    projected, consumed = runner.project_inputs(previous)
    assert consumed is previous
    assert projected == [projected_problem(old) for old in previous]
    projected[0]["decoder"][0][0][0] = 999
    assert wire(previous) == before
    changes = [
        tuple(previous),
        list(reversed(previous)),
        previous[:1],
        replaced(previous, [0, "decoder", "target_rows"], []),
        replaced(previous, [0, "decoder", "target_rows", 0], False),
        replaced(previous, [0, "decoder", "target_rows"], list(reversed(range(64)))),
        replaced(previous, [0, "interface", -1], []),
        replaced(previous, [0, "decoder", "matrix", -1], []),
        replaced(previous, [0, "problem", "target_labels"], []),
    ]
    for bad in changes:
        with pytest.raises(ValueError):
            runner.project_inputs(bad)
    # Complete booleans and old rank/collision/source results are deliberately unselected.
    bad = replaced(previous, [0, "decoder", "complete"], True)
    assert runner.project_inputs(bad)[0] == [projected_problem(old) for old in previous]


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
def test_fixed_full_scalar_oracle_and_actual_signed_endpoint_calls(engines, fixed_data, index):
    problems, _, wanted, _ = fixed_data
    for engine in engines:
        p = copy.deepcopy(problems[index])
        before = wire(p)
        a = engine.build_family(p)
        assert wire(p) == before
        assert wire(a) == wire(wanted[index])
        for row in a["shared"]["witnesses"]:
            for side in ("positive", "negative"):
                endpoint = row[side]
                bank = engine.produce(p["primitive_map"], endpoint["primitive"])
                observed = engine.produce(p["interface"], bank)
                direct = engine.produce(p["geometric"], bank)
                decoded = engine.apply(p["decoder"], observed)
                assert bank == endpoint["bank_error"]
                assert observed == endpoint["observed_error"]
                assert direct == decoded == endpoint["direct_error"] == endpoint["decoded_error"]
                assert [
                    fw(fraction(x) / fraction(s))
                    for x, s in zip(decoded, p["target_scales"], strict=True)
                ] == endpoint["normalized_error"]
        for row in a["enclosure"]["witnesses"]:
            for side in ("positive", "negative"):
                endpoint = row[side]
                assert (
                    engine.apply(p["decoder"], endpoint["observed_error"])
                    == endpoint["decoded_error"]
                )


def test_fixed_full_suite_payload_and_selected_identity(runner, fixed_data):
    problems, previous, families, wanted = fixed_data
    assert wire(runner.assemble_suite(families, previous)) == wire(wanted)
    assert runner.historical_bridges(families, previous) == BRIDGES
    assert runner.payload_sizes(families) == payload(families)
    for p, f in zip(problems, families, strict=True):
        assert len(p["interface"]) == 37 and len(p["geometric"][0]) == 48
        assert len(p["geometric"]) == 64 and len(p["primitive_map"][0]) == 48
        assert p["primitive_map"] == encode(identity(48))
        assert p["target_scales"] == [fw(1)] * 64
        assert f["counts"]["shared_witness_entries"] == 128 * (48 + 48 + 37 + 192 + 1)
        assert f["counts"]["enclosure_witness_entries"] == 128 * (37 + 128 + 1)
        literal_count_checks(f)
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


def test_fixed_full_family_and_suite_corruptions_are_nonvacuous(runner, fixed_data):
    _, _, families, wanted = fixed_data
    for f in families:
        for bad in family_mutations(f):
            assert wire(bad) != wire(f)
            with pytest.raises(ValueError):
                runner.verify_suite(bad, f)
    changes = [
        replaced(wanted, ["families"], list(reversed(families))),
        replaced(wanted, ["prior_bridges", "AU_decoder_inputs_equal"], False),
        replaced(wanted, ["prior_bridges", "fixed_raw_unit_box"], False),
        replaced(
            wanted,
            ["payload_sizes", 0, "shared_bytes"],
            wanted["payload_sizes"][0]["shared_bytes"] + 1,
        ),
        replaced(wanted, ["totals", "strict_rows"], wanted["totals"]["strict_rows"] + 1),
        replaced(wanted, ["scope", "stochastic_independence_assumed"], True),
        replaced(wanted, ["scope", "common_bank_feasibility_solved"], True),
        {**wanted, "extra": 0},
    ]
    for bad in changes:
        assert wire(bad) != wire(wanted)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, wanted)


def test_fixed_selected_producer_changes_are_nonvacuous(runner, fixed_data):
    _, previous, families, _ = fixed_data
    changes = [
        changed_fraction(previous, [0, "interface", 0, 0]),
        changed_fraction(previous, [0, "problem", "geometric", 0, 0]),
        changed_fraction(previous, [0, "decoder", "matrix", 0, 0]),
        replaced(previous, [0, "problem", "target_labels", 0, "first"], False),
        replaced(previous, [0, "decoder", "target_rows", 0], False),
        replaced(previous, [0, "decoder", "target_rows"], list(reversed(range(64)))),
        replaced(previous, [0, "problem", "family"], "changed"),
    ]
    for bad in changes:
        assert wire(bad) != wire(previous)
        with pytest.raises(ValueError):
            runner.historical_bridges(families, bad)


def test_fixed_unselected_historical_mathematics_is_not_replayed(runner, fixed_data):
    problems, previous, families, _ = fixed_data
    changes = [
        replaced(
            previous,
            [0, "certificate", "interface_rank"],
            previous[0]["certificate"]["interface_rank"] + 1,
        ),
        replaced(previous, [0, "certificate", "collision"], {"not": "read"}),
        replaced(previous, [0, "decoder", "complete"], not previous[0]["decoder"]["complete"]),
        changed_fraction(previous, [0, "source", "geometric_values", 0, 0]),
        changed_fraction(previous, [0, "problem", "bank", 0, 0]),
        replaced(previous, [0, "bank_controls"], []),
    ]
    for bad in changes:
        assert wire(bad) != wire(previous)
        assert runner.project_inputs(bad)[0] == problems
        assert runner.historical_bridges(families, bad) == BRIDGES


def test_fixed_source_and_ancestor_identity_inventory(runner):
    current = runner.identities()
    assert {k: len(current[k]) for k in current} == {
        "source_ledger": 5,
        "prior_artifacts": 52,
        "ancestor_sources": 79,
    }
    assert set(current["source_ledger"]) == set(runner.SOURCES)
    raw = runner.AU.read_bytes()
    assert len(raw) == 1073452
    assert (
        hashlib.sha256(raw).hexdigest()
        == "25e2fabfcf9e18df3ee3bf41fcac15a8b18cf3be1c4e14858be87316b48257ad"
    )
    for name, want in current["source_ledger"].items():
        raw = (HERE / name).read_bytes()
        assert len(raw) == want["bytes"] and hashlib.sha256(raw).hexdigest() == want["sha256"]
