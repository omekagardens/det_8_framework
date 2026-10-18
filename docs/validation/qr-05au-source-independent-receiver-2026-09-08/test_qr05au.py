"""Independent rational Gram-Schmidt source-independent receiver checks.

Only test names containing fixed consume authenticated AT cases. Collection and generic
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
        load("_qr05au_test_primary", "kernel.py"),
        load("_qr05au_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05au_test_runner", "study.py")


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


CHECKS = (
    "selected_filter_identity",
    "source_inputs_consistent",
    "source_independent_certificate",
    "decoder_bank_identity",
    "decoder_source_identity",
    "restricted_application",
    "collision_valid",
    "complete_classification",
)
SCOPE = (
    "source_dictionary_changed",
    "geometry_reintegrated",
    "old_collision_replayed",
    "old_decoder_modified",
    "filters_reselected",
    "measurements_added",
    "normalization_row_added",
    "source_dependent_fit_performed",
    "physical_bank_controls_established",
    "full_field_recovery_tested",
    "physical_interface_insufficiency_proved",
    "minimality_recomputed",
    "empirical_noise_calibrated",
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


def expected_certificate(interface, targets):
    """Orthogonal row projections and an independent column-span null construction."""
    b, g = matrix(interface), matrix(targets)
    r = len(g[0])
    span = OrthogonalSpan(b)
    basis = [b[i] for i in span.indices]
    # Original full columns rather than a Gaussian/RREF reduction.
    column_span = OrthogonalSpan(columns(b) if b else [[] for _ in range(r)])
    pivots = column_span.indices
    free = [i for i in range(r) if i not in pivots]
    recovered, failed, coefficients = [], [], []
    for i, row in enumerate(g):
        residual, representation = span.decompose(row)
        if any(residual):
            failed.append(i)
            coefficients.append(None)
        else:
            recovered.append(i)
            compact = [representation.get(j, F()) for j in span.indices]
            assert [dot(compact, col) for col in columns(basis)] == row if basis else not any(row)
            coefficients.append(compact)
    collision = None
    for j in free:
        if not failed:
            break
        residual, representation = column_span.decompose([row[j] for row in b])
        assert not any(residual)
        w = [-representation.get(i, F()) for i in range(r)]
        w[j] = F(1)
        difference = mv(g, w)
        if any(difference):
            assert mv(b, w) == [F()] * len(b)
            assert all(w[i] == F(i == j) for i in free)
            collision = {
                "free_column": j,
                "separating_row": next(i for i, x in enumerate(difference) if x),
                "null_vector": w,
                "bank_a": [F()] * r,
                "bank_b": w[:],
                "observed_a": [F()] * len(b),
                "observed_b": mv(b, w),
                "truth_a": [F()] * len(g),
                "truth_b": difference[:],
                "truth_difference": difference,
            }
            break
    assert bool(failed) == (collision is not None)
    return encode(
        {
            "interface_rank": len(span.indices),
            "target_rank": rank(g),
            "joint_rank": rank([*b, *g]),
            "row_basis": span.indices,
            "pivot_columns": pivots,
            "free_columns": free,
            "recoverable_rows": recovered,
            "failed_rows": failed,
            "row_coefficients": coefficients,
            "recoverable": not failed,
            "collision": collision,
        }
    )


def expected(problem):
    c, f, g, r, o, q = (
        matrix(problem[k])
        for k in ("coarse_map", "filters", "geometric", "bank", "observations", "targets")
    )
    m, k, t, b, n = len(c), len(f), len(g), len(g[0]), len(q[0])
    s = m + k
    interface = [*c, *f]
    assert mm(c, r, n) == o and mm(g, r, n) == q
    assert f == [g[i] for i in problem["selected_rows"]]
    cert = expected_certificate(encode(interface), encode(g))
    recovered = cert["recoverable_rows"]
    v = len(recovered)
    dense = []
    for i in recovered:
        row = [F()] * s
        for index, value in zip(cert["row_basis"], cert["row_coefficients"][i], strict=True):
            row[index] = fraction(value)
        dense.append(row)
    source = mm(interface, r, n)
    prediction = mm(dense, interface, b)
    assert prediction == [g[i] for i in recovered]
    assert mm(dense, source, n) == [q[i] for i in recovered]
    controls = []
    for i in [None, *range(b)]:
        z = [F(j == i) for j in range(b)]
        coarse, supplement = mv(c, z), mv(f, z)
        observed = [*coarse, *supplement]
        truth = mv([g[j] for j in recovered], z)
        predicted = mv(dense, observed)
        assert predicted == truth
        controls.append(
            {
                "bank_index": i,
                "bank_values": z,
                "coarse_values": coarse,
                "supplement_values": supplement,
                "observed": observed,
                "truth": truth,
                "predicted": predicted,
                "residuals": [F()] * v,
            }
        )
    counts = {
        "coarse_values": m,
        "bank_values": b,
        "source_columns": n,
        "target_rows": t,
        "supplement_values": k,
        "receiver_values": s,
        "input_matrix_entries": m * b + k * b + t * b + b * n + m * n + t * n,
        "interface_entries": s * b,
        "source_check_entries": (s + m + 2 * t) * n,
        "compact_decoder_entries": v * cert["interface_rank"],
        "raw_decoder_entries": v * s,
        "bank_prediction_entries": v * b,
        "bank_residual_entries": v * b,
        "source_prediction_entries": v * n,
        "source_residual_entries": v * n,
        "bank_controls": b + 1,
        "bank_control_entries": (b + 1) * (b + 2 * s + 3 * v),
        "collisions": int(bool(cert["failed_rows"])),
        "collision_entries": 3 * b + 2 * s + 3 * t if cert["failed_rows"] else 0,
        "recovered_rows": v,
        "failed_rows": t - v,
    }
    return encode(
        {
            "problem": copy.deepcopy(problem),
            "interface": interface,
            "source": {
                "interface_values": source,
                "geometric_values": mm(g, r, n),
                "coarse_residuals": [[F()] * n for _ in range(m)],
                "target_residuals": [[F()] * n for _ in range(t)],
            },
            "certificate": cert,
            "decoder": {
                "target_rows": recovered[:],
                "matrix": dense,
                "bank_predicted": prediction,
                "bank_residuals": [[F()] * b for _ in range(v)],
                "source_predicted": mm(dense, source, n),
                "source_residuals": [[F()] * n for _ in range(v)],
                "complete": v == t,
            },
            "bank_controls": controls,
            "checks": dict.fromkeys(CHECKS, True),
            "counts": counts,
        }
    )


def make_problem(c, g, selected=(), r=None, name="synthetic"):
    c, g = ([[F(x) for x in row] for row in a] for a in (c, g))
    if r is None:
        r = identity(len(g[0]))
    else:
        r = [[F(x) for x in row] for row in r]
    n = len(r[0])
    return encode(
        {
            "family": name,
            "target_labels": [{"first": i - 5, "second": -9} for i in range(len(g))],
            "coarse_map": c,
            "filters": [g[i][:] for i in selected],
            "geometric": g,
            "selected_rows": list(selected),
            "bank": r,
            "observations": mm(c, r, n),
            "targets": mm(g, r, n),
        }
    )


def trap_problem():
    # The old normalized source has equal coordinates, but the new domain is all z.
    return make_problem([[1, -1]], [[1, 1]], r=[[F(1, 2)], [F(1, 2)]], name="trap")


def partial_problem():
    return make_problem(
        [[0, 0, 0, 0], [1, 1, 0, 0], [2, 2, 0, 0]],
        [[0, 0, 0, 0], [3, 3, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]],
        [2],
        name="partial",
    )


def complete_problem():
    return make_problem(
        [[0, 0, 0], [2, 0, 0], [4, 0, 0]],
        [[1, 0, 0], [0, 1, -1], [3, 2, -2], [0, 0, 0]],
        [1],
        name="complete",
    )


def free_first_problem():
    return make_problem(
        [[1, 1, 0, 0], [0, 0, 1, 1]],
        [[0, 0, 0, 1], [0, 1, 0, 0]],
        name="free-first",
    )


def invisible_first_problem():
    return make_problem([[1, 0, 0]], [[2, 0, 0], [0, 0, 3]], name="invisible-first")


@pytest.mark.parametrize(
    "factory",
    [
        trap_problem,
        partial_problem,
        complete_problem,
        free_first_problem,
        invisible_first_problem,
        lambda: make_problem([], [[0, 0], [0, 0]]),
        lambda: make_problem([], [[1, 0], [0, 1]]),
        lambda: make_problem([[0, 0]], [[0, 0], [1, 1]]),
    ],
)
def test_generic_complete_orthogonal_oracle(engines, factory):
    p = factory()
    want = expected(p)
    for engine in engines:
        before = wire(p)
        actual = engine.build_family(p)
        assert wire(actual) == wire(want)
        assert wire(p) == before
        assert wire(engine.certify(want["interface"], p["geometric"])) == wire(want["certificate"])


def test_no_normalization_or_mass_rescaling_and_source_fit_is_insufficient(engines):
    p = trap_problem()
    for engine in engines:
        a = engine.build_family(p)
        cert = a["certificate"]
        assert cert["row_basis"] == [0] and cert["interface_rank"] == 1
        assert cert["failed_rows"] == [0] and cert["row_coefficients"] == [None]
        assert a["decoder"] == {
            "target_rows": [],
            "matrix": [],
            "bank_predicted": [],
            "bank_residuals": [],
            "source_predicted": [],
            "source_residuals": [],
            "complete": False,
        }
        w = cert["collision"]
        assert w["null_vector"] == [fw(1), fw(1)] and w["truth_difference"] == [fw(2)]
        assert w["bank_a"] == [fw(0), fw(0)] and w["bank_b"] == [fw(1), fw(1)]
        assert w["observed_a"] == w["observed_b"] == [fw(0)]
        assert all(
            row["truth"] == row["predicted"] == row["residuals"] == [] for row in a["bank_controls"]
        )
        # Appending a constant would change this unrestricted problem, not repair it.
        altered = engine.certify([*p["coarse_map"], [fw(1), fw(1)]], p["geometric"])
        assert altered["recoverable"]


def test_canonical_witness_is_free_column_first_and_skips_invisible_columns(engines):
    for engine in engines:
        a = engine.build_family(free_first_problem())["certificate"]["collision"]
        assert a["free_column"] == 1 and a["separating_row"] == 1
        assert a["null_vector"] == list(map(fw, [-1, 1, 0, 0]))
        assert a["truth_difference"] == [fw(0), fw(1)]
        b = engine.build_family(invisible_first_problem())["certificate"]["collision"]
        assert b["free_column"] == 2 and b["separating_row"] == 1
        assert b["null_vector"] == list(map(fw, [0, 0, 1]))


def test_source_dictionary_changes_cannot_change_certificate_or_receiver(engines, monkeypatch):
    p = partial_problem()
    c, g = matrix(p["coarse_map"]), matrix(p["geometric"])
    banks = [
        [[0] for _ in range(4)],
        [[1, -2, 7] for _ in range(4)],
        identity(4),
        [[F(i - j, 7) for j in range(5)] for i in range(4)],
    ]
    for engine in engines:
        original = engine.certify
        calls = []

        def spy(b, g, original=original, calls=calls):
            calls.append((copy.deepcopy(b), copy.deepcopy(g)))
            return original(b, g)

        monkeypatch.setattr(engine, "certify", spy)
        outputs = []
        for bank in banks:
            altered = make_problem(c, g, p["selected_rows"], bank)
            a = engine.build_family(altered)
            assert wire(a) == wire(expected(altered))
            outputs.append((a["certificate"], a["decoder"]["target_rows"], a["decoder"]["matrix"]))
        assert all(wire(list(x)) == wire(list(outputs[0])) for x in outputs)
        b = [*p["coarse_map"], *p["filters"]]
        assert calls == [(b, p["geometric"])] * len(banks)
        monkeypatch.setattr(engine, "certify", original)


def test_recovery_does_not_require_identifiable_bank_and_zero_interface(engines):
    for engine in engines:
        p = make_problem([[1, 1]], [[2, 2], [0, 0]])
        a = engine.build_family(p)
        assert a["certificate"]["interface_rank"] == 1
        assert a["certificate"]["interface_rank"] < len(p["bank"])
        assert a["decoder"]["matrix"] == [[fw(2)], [fw(0)]]
        assert a["decoder"]["complete"]
        zero = engine.build_family(make_problem([], [[0], [0]]))
        assert zero["decoder"]["matrix"] == [[], []]
        assert zero["certificate"]["row_coefficients"] == [[], []]
        assert zero["certificate"]["row_basis"] == zero["certificate"]["pivot_columns"] == []
        assert zero["certificate"]["free_columns"] == [0]
        assert zero["decoder"]["complete"]


def inverse(a):
    span = OrthogonalSpan(columns(a))
    assert len(span.indices) == len(a)
    result = []
    for e in identity(len(a)):
        residual, representation = span.decompose(e)
        assert not any(residual)
        result.append([representation.get(i, F()) for i in range(len(a))])
    return columns(result)


def transformed_problem(p, coarse_change, bank_change, scale):
    c, g, r = (matrix(p[key]) for key in ("coarse_map", "geometric", "bank"))
    ci, bi = inverse(coarse_change), inverse(bank_change)
    moved = make_problem(
        mm(mm(coarse_change, c), bi),
        [[scale * x for x in row] for row in mm(g, bi)],
        p["selected_rows"],
        mm(bank_change, r),
        "transported",
    )
    return moved, ci, bi


@pytest.mark.parametrize("factory", [complete_problem, partial_problem, free_first_problem])
def test_signed_coordinate_transport_and_changed_canonical_basis(engines, factory):
    p = factory()
    m, r, k = len(p["coarse_map"]), len(p["geometric"][0]), len(p["filters"])
    pc = identity(m)
    pc[0], pc[-1] = pc[-1], pc[0]
    if m > 1:
        pc[0] = [x + 2 * y for x, y in zip(pc[0], pc[1], strict=True)]
    bs = identity(r)
    bs[0], bs[-1] = bs[-1], bs[0]
    bs[0] = [3 * x - y for x, y in zip(bs[0], bs[1], strict=True)]
    scale = F(5, 3)
    moved, pci, _ = transformed_problem(p, pc, bs, scale)
    want = expected(moved)
    for engine in engines:
        old = engine.build_family(p)
        new = engine.build_family(moved)
        assert wire(new) == wire(want)
        for key in (
            "interface_rank",
            "target_rank",
            "joint_rank",
            "recoverable_rows",
            "failed_rows",
        ):
            assert new["certificate"][key] == old["certificate"][key]
        old_d = matrix(old["decoder"]["matrix"])
        # Transport the SAME dense map, not the recanonicalized representation.
        transported = []
        for row in old_d:
            transported.append([scale * x for x in mm([row[:m]], pci)[0]] + row[m:])
        assert mm(transported, matrix(new["interface"]), r) == [
            matrix(moved["geometric"])[i] for i in old["decoder"]["target_rows"]
        ]
        for control in old["bank_controls"]:
            z = mv(bs, [fraction(v) for v in control["bank_values"]])
            observed = mv(matrix(new["interface"]), z)
            got = engine.apply(encode(transported), encode(observed))
            assert got == [fw(scale * fraction(x)) for x in control["truth"]]
        if old["certificate"]["collision"] is not None:
            w = [fraction(x) for x in old["certificate"]["collision"]["null_vector"]]
            sw = mv(bs, w)
            assert mv(matrix(new["interface"]), sw) == [F()] * (m + k)
            assert mv(matrix(moved["geometric"]), sw) == [
                scale * fraction(x) for x in old["certificate"]["collision"]["truth_difference"]
            ]
        if factory is complete_problem:
            assert new["certificate"]["row_basis"] != old["certificate"]["row_basis"]
            assert new["decoder"]["matrix"] != encode(transported)
        if factory is free_first_problem:
            assert new["certificate"]["pivot_columns"] != old["certificate"]["pivot_columns"]


def test_every_retained_control_calls_public_evaluators_without_failed_zero_rows(
    engines, monkeypatch
):
    from collections import Counter

    for engine in engines:
        for factory in (trap_problem, partial_problem, complete_problem):
            p = factory()
            got_calls = {"produce": [], "apply": []}
            originals = {name: getattr(engine, name) for name in got_calls}
            for name, original in originals.items():

                def spy(a, x, original=original, name=name, got_calls=got_calls):
                    got_calls[name].append(wire([a, x]))
                    return original(a, x)

                monkeypatch.setattr(engine, name, spy)
            a = engine.build_family(p)
            want_calls = {"produce": [], "apply": []}
            recovered_g = [p["geometric"][i] for i in a["decoder"]["target_rows"]]
            for row in a["bank_controls"]:
                z = row["bank_values"]
                for bank_map in (p["coarse_map"], p["filters"], recovered_g):
                    want_calls["produce"].append(wire([bank_map, z]))
                want_calls["apply"].append(wire([a["decoder"]["matrix"], row["observed"]]))
            collision = a["certificate"]["collision"]
            if collision is not None:
                for z in (collision["bank_a"], collision["bank_b"]):
                    for bank_map in (a["interface"], p["geometric"]):
                        want_calls["produce"].append(wire([bank_map, z]))
            for name, original in originals.items():
                actual, wanted = Counter(got_calls[name]), Counter(want_calls[name])
                assert all(actual[key] >= count for key, count in wanted.items())
                monkeypatch.setattr(engine, name, original)


def test_restricted_file_blind_apis_zero_widths_and_non_multiple_of_four(engines, monkeypatch):
    def forbidden(*args, **kwargs):
        raise RuntimeError("restricted evaluator accessed a file")

    for engine in engines:
        # All modules are loaded before disabling file reads.
        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "read_bytes", forbidden)
            patch.setattr(Path, "read_text", forbidden)
            assert engine.certify([], [[fw(0)]]) == expected_certificate([], [[fw(0)]])
            assert engine.produce([], [fw(-3)]) == []
            assert engine.produce([[], []], []) == [fw(0), fw(0)]
            assert engine.apply([], []) == []
            assert engine.apply([[], []], []) == [fw(0), fw(0)]
            assert engine.apply([[fw(2), fw(-3), fw(F(1, 2))]], list(map(fw, [-1, 7, 4]))) == [
                fw(-21)
            ]
            assert engine.produce([[fw(2), fw(-3), fw(F(1, 2))]], list(map(fw, [-1, 7, 4]))) == [
                fw(-21)
            ]
            # A third argument is not an accepted hidden/intercept API.
            with pytest.raises(TypeError):
                engine.apply([fw(9)], [[fw(1)]], [fw(2)])


def test_shared_children_and_detached_repeated_outputs(engines):
    p = make_problem([[1, 1], [1, 1]], [[1, 1], [1, 1]], [1])
    p["coarse_map"][1] = p["coarse_map"][0]
    p["filters"][0] = p["geometric"][1]
    before = wire(p)
    for engine in engines:
        a = engine.build_family(p)
        cert = engine.certify(a["interface"], p["geometric"])
        a["problem"]["geometric"][0][0][0] += 99
        a["decoder"]["matrix"][0][0][0] += 77
        cert["row_coefficients"][0][0][0] += 66
        assert wire(p) == before
        assert wire(engine.build_family(p)) == wire(expected(p))
        x, matrix_input = [fw(2)], [[fw(3)], [fw(3)]]
        matrix_input[1] = matrix_input[0]
        output = engine.apply(matrix_input, x)
        output[0][0] = 999
        assert output[1] == fw(6) and x == [fw(2)] and matrix_input[0] == [fw(3)]


def test_accepted_cap_edges_and_tiny_exact_nonzero_pivot(engines):
    for engine in engines:
        assert engine.produce([[]] * 320, []) == [fw(0)] * 320
        assert engine.produce([], [fw(0)] * 1024) == []
        assert engine.apply([[fw(0)] * 320] * 64, [fw(7)] * 320) == [fw(0)] * 64
        a = engine.certify([[fw(0)]] * 320, [[fw(0)]] * 64)
        assert a["recoverable_rows"] == list(range(64)) and a["interface_rank"] == 0
        a = engine.certify([], [[fw(0)] * 1024])
        assert a["free_columns"] == list(range(1024)) and a["recoverable"]
        p = make_problem([[0]] * 256, [[0]] * 64, range(64), [[0]])
        a = engine.build_family(p)
        assert wire(a) == wire(expected(p))
        p = make_problem([[1]], [[2]], r=[[F(i, 577) for i in range(576)]])
        assert wire(engine.build_family(p)) == wire(expected(p))
        d = 1 << 3500
        b, g = [[fw(F(1, d)), fw(0)]], [[fw(1), fw(0)], [fw(0), fw(1)]]
        cert = engine.certify(b, g)
        assert cert["row_coefficients"] == [[fw(d)], None]
        assert cert["interface_rank"] == 1 and cert["failed_rows"] == [1]


class NativeListSubclass(list):
    pass


class NativeDictSubclass(dict):
    pass


class NativeIntSubclass(int):
    pass


def malformed_families():
    p = partial_problem()
    yield None
    yield []
    yield NativeDictSubclass(p)
    yield {**p, "normalization": [fw(1)]}
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
    yield replaced(p, ["target_labels", 0, "second"], NativeIntSubclass(-9))
    yield replaced(p, ["target_labels", 0, "extra"], 0)
    for value in ([True], [-1], [4], [2, 2], [2, 1]):
        yield replaced(p, ["selected_rows"], value)
    for key in ("coarse_map", "filters", "geometric", "bank", "observations", "targets"):
        yield replaced(p, [key, -1], [])
        yield replaced(p, [key, -1], tuple(p[key][-1]))
    yield replaced(p, ["coarse_map"], p["coarse_map"] * 86)
    yield replaced(p, ["geometric"], [p["geometric"][0]] * 65)
    yield replaced(p, ["geometric"], [[fw(0)] * 1025] * 4)
    yield replaced(p, ["geometric"], [])
    yield replaced(p, ["bank"], p["bank"][:-1])
    yield replaced(p, ["targets"], [[fw(0)] * 577] * 4)
    for path in (["filters", 0, 0], ["observations", 0, 0], ["targets", 0, 0]):
        yield replaced(p, path, fw(11))
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
        yield replaced(p, ["targets", -1, -1], value)


def malformed_certificates():
    b, g = [[fw(1), fw(-1)]], [[fw(1), fw(1)]]
    for value in (None, {}, (), NativeListSubclass(b), b * 321):
        yield value, g
    for value in (None, {}, (), [], NativeListSubclass(g), g * 65, [[]], [[fw(0)] * 1025]):
        yield b, value
    yield b + [[fw(1)]], g
    for value in (True, 0.0, F(0), (0, 1), [0], [0, 0], [2, 2], [1 << 4096, 1]):
        yield replaced(b, [0, 1], value), g
        yield b, replaced(g, [0, 1], value)
    yield [], [[True]]


def malformed_evaluators(row_cap, width_cap):
    a, x = [[fw(1), fw(-1), fw(2)]], [fw(3), fw(4), fw(5)]
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
    for b, g in malformed_certificates():
        require_rejection(lambda b=b, g=g: engine.certify(b, g))
        count += 1
    for name, rowcap, widthcap in (("produce", 320, 1024), ("apply", 64, 320)):
        call = getattr(engine, name)
        for a, x in malformed_evaluators(rowcap, widthcap):
            require_rejection(lambda a=a, x=x, call=call: call(a, x))
            count += 1
    d = 1 << 4095
    for name in ("produce", "apply"):
        call = getattr(engine, name)
        if call([[fw(d), fw(-d)]], [fw(2), fw(2)]) != [fw(0)]:
            raise RuntimeError("internal cancellation rejected")
        require_rejection(lambda call=call: call([[fw(d), fw(d)]], [fw(1), fw(1)]))
    p = make_problem([[d, d]], [[d, d]], r=[[2], [-2]])
    if engine.build_family(p)["source"]["geometric_values"] != [[fw(0)]]:
        raise RuntimeError("source product cancellation")
    require_rejection(lambda: engine.certify([[fw(F(1, d)), fw(0)]], [[fw(d), fw(0)]]))
    require_rejection(lambda: engine.certify([[fw(F(1, d)), fw(d)]], [[fw(0), fw(1)]]))
    cyclic = partial_problem()
    cyclic["targets"].append(cyclic["targets"])
    require_rejection(lambda: engine.build_family(cyclic))
    cycle = []
    cycle.append(cycle)
    require_rejection(lambda: engine.certify(cycle, [[fw(0)]]))
    require_rejection(lambda: engine.produce(cycle, [fw(1)]))
    require_rejection(lambda: engine.apply([[fw(1)]], cycle))
    return count + 8


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
                    replaced(partial_problem(), ["targets", -1, -1], value)
                )
            )
            require_rejection(lambda value=value: engine.certify([[fw(1)]], [[fw(0)], [value]]))
            require_rejection(lambda value=value: engine.produce([[fw(1)], [value]], [fw(2)]))
            require_rejection(lambda value=value: engine.apply([[fw(1)], [value]], [fw(2)]))
    finally:
        engine._fraction = original
    names = [
        name for name in ("_dot", "_row_basis", "_echelon", "_multiply") if hasattr(engine, name)
    ]
    originals = {name: getattr(engine, name) for name in names}
    for name in names:
        setattr(engine, name, forbidden)
    try:
        require_rejection(
            lambda: engine.build_family(replaced(partial_problem(), ["targets", -1, -1], [1, 0]))
        )
        require_rejection(lambda: engine.certify([[fw(1)]], [[fw(0)], [[1, 0]]]))
        require_rejection(lambda: engine.produce([[fw(1)], [[1, 0]]], [fw(1)]))
        require_rejection(lambda: engine.apply([[fw(1)], [[1, 0]]], [fw(1)]))
    finally:
        for name, original in originals.items():
            setattr(engine, name, original)
    if calls:
        raise RuntimeError("late admission ordering")
    return 12


def test_native_shape_value_identity_and_bit_guards(engines):
    a, b = [explicit_guards(engine) for engine in engines]
    assert a == b and a > 100
    assert [pre_arithmetic_guards(engine) for engine in engines] == [12, 12]


@pytest.mark.parametrize("optimized", [False, True])
def test_isolated_explicit_normal_and_optimized_guards(tmp_path, optimized):
    script = r"""
import importlib.util,json,sys
from pathlib import Path
path=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("au_guard_tests",path)
t=importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
counts=[]
for name,file in (("primary","kernel.py"),("reference","reference.py")):
    engine=t.load("_qr05au_guard_"+name,file)
    counts.append(t.explicit_guards(engine)+t.pre_arithmetic_guards(engine))
print(json.dumps(counts))
"""
    args = [sys.executable, "-I", "-X", "pycache_prefix=" + str(tmp_path / "cache")]
    if optimized:
        args.append("-O")
    completed = subprocess.run(
        [*args, "-c", script, str(Path(__file__).resolve())],
        capture_output=True,
        text=True,
        check=True,
        timeout=120,
    )
    count = (
        len(list(malformed_families()))
        + len(list(malformed_certificates()))
        + len(list(malformed_evaluators(320, 1024)))
        + len(list(malformed_evaluators(64, 320)))
        + 20
    )
    assert json.loads(completed.stdout) == [count, count]


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
    "AT_selected_families": list(FAMILIES),
    "AT_interface_inputs_equal": True,
    "AT_target_inputs_equal": True,
    "AT_source_inputs_equal": True,
    "old_affine_decoder_replayed": False,
    "old_bank_defect_replayed": False,
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
    if f["interface"]:
        yield changed_fraction(f, ["interface", 0, 0])
    for key, value in f["source"].items():
        if value:
            yield changed_fraction(f, ["source", key, 0, 0])
        else:
            yield replaced(f, ["source", key], [[fw(0)]])
    cert = f["certificate"]
    for key in ("interface_rank", "target_rank", "joint_rank"):
        yield replaced(f, ["certificate", key], cert[key] + 1)
    for key in ("row_basis", "pivot_columns", "free_columns", "recoverable_rows", "failed_rows"):
        yield replaced(f, ["certificate", key], [*cert[key], -1])
    yield replaced(f, ["certificate", "recoverable"], not cert["recoverable"])
    yield replaced(f, ["certificate", "row_coefficients"], cert["row_coefficients"][:-1])
    if cert["failed_rows"]:
        yield replaced(f, ["certificate", "row_coefficients", cert["failed_rows"][0]], [])
    if cert["recoverable_rows"]:
        i = cert["recoverable_rows"][0]
        row = cert["row_coefficients"][i]
        if row:
            yield changed_fraction(f, ["certificate", "row_coefficients", i, 0])
        else:
            yield replaced(f, ["certificate", "row_coefficients", i], None)
    collision = cert["collision"]
    if collision is None:
        yield replaced(f, ["certificate", "collision"], {})
    else:
        yield replaced(f, ["certificate", "collision"], None)
        for key in ("free_column", "separating_row"):
            yield replaced(f, ["certificate", "collision", key], collision[key] + 1)
        for key in (
            "null_vector",
            "bank_a",
            "bank_b",
            "observed_a",
            "observed_b",
            "truth_a",
            "truth_b",
            "truth_difference",
        ):
            if collision[key]:
                yield changed_fraction(f, ["certificate", "collision", key, 0])
            else:
                yield replaced(f, ["certificate", "collision", key], [fw(0)])
    decoder = f["decoder"]
    yield replaced(f, ["decoder", "complete"], not decoder["complete"])
    yield replaced(f, ["decoder", "target_rows"], [*decoder["target_rows"], -1])
    for key in (
        "matrix",
        "bank_predicted",
        "bank_residuals",
        "source_predicted",
        "source_residuals",
    ):
        if decoder[key] and decoder[key][0]:
            yield changed_fraction(f, ["decoder", key, 0, 0])
        else:
            yield replaced(f, ["decoder", key], [[fw(0)]])
    yield replaced(f, ["bank_controls"], f["bank_controls"][:-1])
    yield replaced(f, ["bank_controls", 0, "bank_index"], 0)
    for key in (
        "bank_values",
        "coarse_values",
        "supplement_values",
        "observed",
        "truth",
        "predicted",
        "residuals",
    ):
        if f["bank_controls"][0][key]:
            yield changed_fraction(f, ["bank_controls", 0, key, 0])
        else:
            yield replaced(f, ["bank_controls", 0, key], [fw(0)])
    for key in CHECKS:
        yield replaced(f, ["checks", key], False)
    for key in (
        "compact_decoder_entries",
        "bank_control_entries",
        "collision_entries",
        "source_check_entries",
        "recovered_rows",
        "failed_rows",
    ):
        yield replaced(f, ["counts", key], f["counts"][key] + 1)


def literal_count_checks(f):
    p, d, cert, counts = f["problem"], f["decoder"], f["certificate"], f["counts"]
    assert counts["input_matrix_entries"] == sum(
        len(row)
        for key in ("coarse_map", "filters", "geometric", "bank", "observations", "targets")
        for row in p[key]
    )
    assert counts["interface_entries"] == sum(map(len, f["interface"]))
    assert counts["source_check_entries"] == sum(
        len(row) for value in f["source"].values() for row in value
    )
    assert counts["compact_decoder_entries"] == sum(
        len(row) for row in cert["row_coefficients"] if row is not None
    )
    for key, field in (
        ("raw_decoder_entries", "matrix"),
        ("bank_prediction_entries", "bank_predicted"),
        ("bank_residual_entries", "bank_residuals"),
        ("source_prediction_entries", "source_predicted"),
        ("source_residual_entries", "source_residuals"),
    ):
        assert counts[key] == sum(map(len, d[field]))
    assert counts["bank_control_entries"] == sum(
        len(value)
        for row in f["bank_controls"]
        for key, value in row.items()
        if key != "bank_index"
    )
    w = cert["collision"]
    assert counts["collision_entries"] == (
        sum(len(value) for key, value in w.items() if key not in ("free_column", "separating_row"))
        if w is not None
        else 0
    )


def test_generic_complete_wire_mutations_and_literal_counts(runner):
    for factory in (
        trap_problem,
        partial_problem,
        complete_problem,
        lambda: make_problem([], [[0], [1]]),
    ):
        f = expected(factory())
        literal_count_checks(f)
        for bad in family_mutations(f):
            assert wire(bad) != wire(f)
            with pytest.raises(ValueError):
                runner.verify_suite(bad, f)


def projected_problem(old):
    p = old["problem"]
    return {
        "family": p["family"],
        "target_labels": copy.deepcopy(p["target_labels"]),
        "coarse_map": copy.deepcopy(old["lineage"]["coarse_map"]),
        **{
            key: copy.deepcopy(p[key])
            for key in ("filters", "geometric", "selected_rows", "bank", "observations", "targets")
        },
    }


def independent_history_checks(families, previous):
    assert [f["problem"]["family"] for f in families] == list(FAMILIES)
    assert [old["problem"]["family"] for old in previous] == list(FAMILIES)
    for family, old in zip(families, previous, strict=True):
        assert wire(family["problem"]) == wire(projected_problem(old))
        p = family["problem"]
        assert p["filters"] == [p["geometric"][i] for i in p["selected_rows"]]
        literal_count_checks(family)


def payload(families):
    return [
        {
            "family": f["problem"]["family"],
            "input_bytes": len(wire(f["problem"])),
            "interface_bytes": len(wire(f["interface"])),
            "source_bytes": len(wire(f["source"])),
            "certificate_bytes": len(wire(f["certificate"])),
            "decoder_bytes": len(wire(f["decoder"])),
            "bank_controls_bytes": len(wire(f["bank_controls"])),
            "receiver_map_bytes": len(
                wire({k: f["decoder"][k] for k in ("target_rows", "matrix")})
            ),
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
            **copy.deepcopy(p),
            "intercept": [fw(999)],
            "receiver": [[fw(111)]],
            "coarse_tiles": "not read",
        },
        "lineage": {"coarse_map": copy.deepcopy(p["coarse_map"])},
        "composition": {"coefficient_defect": [[fw(222)]]},
        "classification": {"unrestricted_exact": False},
        "bank_controls": [],
    }


def test_synthetic_history_full_suite_and_all_cached_routes(runner, monkeypatch):
    problems = []
    for name, factory in zip(FAMILIES, (partial_problem, trap_problem), strict=True):
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
    bad = changed_fraction(previous, [0, "problem", "intercept", 0])
    with pytest.raises(ValueError):
        runner.assemble_suite(families, bad)
    # Selective projection ignores the old model; full assembly pins the consumed record.
    assert runner.historical_bridges(families, bad) == BRIDGES

    def changing(p):
        answer = copy.deepcopy(lookup[p["family"]])
        p["family"] = "changed"
        return answer

    monkeypatch.setattr(runner, "load_engine", lambda name: SimpleNamespace(build_family=changing))
    with pytest.raises(ValueError):
        runner.run_suite("primary")


def test_synthetic_projection_inventory_detachment_and_selected_boundaries(runner):
    # Explicit synthetic zero data at declared historical dimensions, not historical math.
    p = make_problem([[0] * 48] * 32, [[0] * 48] * 64, range(5), [[0] * 108] * 48)
    previous = []
    for name in FAMILIES:
        supplied = copy.deepcopy(p)
        supplied["family"] = name
        previous.append(synthetic_history(supplied))
    before = wire(previous)
    projected, consumed = runner.project_inputs(previous)
    assert consumed is previous
    assert projected == [projected_problem(old) for old in previous]
    projected[0]["bank"][0][0][0] = 999
    assert wire(previous) == before
    for bad in (
        tuple(previous),
        list(reversed(previous)),
        previous[:1],
        replaced(previous, [0, "problem", "selected_rows"], []),
        replaced(previous, [0, "lineage", "coarse_map", -1], []),
        replaced(previous, [0, "problem", "bank", -1], []),
        replaced(previous, [0, "problem", "target_labels"], []),
    ):
        with pytest.raises(ValueError):
            runner.project_inputs(bad)


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
def test_fixed_complete_orthogonal_oracle_and_actual_bank_controls(engines, fixed_data, index):
    problems, _, wanted, _ = fixed_data
    for engine in engines:
        p = copy.deepcopy(problems[index])
        before = wire(p)
        a = engine.build_family(p)
        assert wire(p) == before
        assert wire(a) == wire(wanted[index])
        assert wire(engine.certify(a["interface"], p["geometric"])) == wire(a["certificate"])
        g = [p["geometric"][i] for i in a["decoder"]["target_rows"]]
        for control in a["bank_controls"]:
            z = control["bank_values"]
            c, f = engine.produce(p["coarse_map"], z), engine.produce(p["filters"], z)
            assert c + f == control["observed"]
            assert engine.produce(g, z) == control["truth"]
            assert engine.apply(a["decoder"]["matrix"], c + f) == control["predicted"]
        collision = a["certificate"]["collision"]
        if collision is not None:
            for suffix in ("a", "b"):
                z = collision["bank_" + suffix]
                assert engine.produce(a["interface"], z) == collision["observed_" + suffix]
                assert engine.produce(p["geometric"], z) == collision["truth_" + suffix]


def test_fixed_full_suite_payload_and_source_restriction(runner, fixed_data):
    problems, previous, families, wanted = fixed_data
    assert wire(runner.assemble_suite(families, previous)) == wire(wanted)
    assert runner.historical_bridges(families, previous) == BRIDGES
    assert runner.payload_sizes(families) == payload(families)
    for p, f in zip(problems, families, strict=True):
        assert len(p["coarse_map"]) == 32 and len(p["bank"]) == 48
        assert len(p["geometric"]) == 64 and len(p["targets"][0]) == 108
        assert len(p["selected_rows"]) == 5 and len(f["bank_controls"]) == 49
        recovered = f["certificate"]["recoverable_rows"]
        assert f["counts"]["bank_control_entries"] == 49 * (48 + 74 + 3 * len(recovered))
        assert f["counts"]["source_check_entries"] == (37 + 32 + 128) * 108
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
        replaced(wanted, ["prior_bridges", "AT_interface_inputs_equal"], False),
        replaced(wanted, ["prior_bridges", "old_affine_decoder_replayed"], True),
        replaced(
            wanted,
            ["payload_sizes", 0, "certificate_bytes"],
            wanted["payload_sizes"][0]["certificate_bytes"] + 1,
        ),
        replaced(wanted, ["totals", "collisions"], wanted["totals"]["collisions"] + 1),
        replaced(wanted, ["scope", "normalization_row_added"], True),
        replaced(wanted, ["scope", "physical_interface_insufficiency_proved"], True),
        {**wanted, "extra": 0},
    ]
    for bad in changes:
        assert wire(bad) != wire(wanted)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, wanted)


def test_fixed_selected_producer_changes_are_nonvacuous(runner, fixed_data):
    _, previous, families, _ = fixed_data
    paths = [
        [0, "lineage", "coarse_map", 0, 0],
        *[
            [0, "problem", key, 0, 0]
            for key in ("filters", "geometric", "bank", "observations", "targets")
        ],
    ]
    changed = [changed_fraction(previous, path) for path in paths]
    for path, value in (
        ([0, "problem", "selected_rows", 0], -1),
        ([0, "problem", "target_labels", 0, "first"], False),
        ([0, "problem", "family"], "changed"),
    ):
        changed.append(replaced(previous, path, value))
    for bad in changed:
        assert wire(bad) != wire(previous)
        with pytest.raises(ValueError):
            runner.historical_bridges(families, bad)


def test_fixed_unselected_historical_mathematics_is_not_replayed(runner, fixed_data):
    problems, previous, families, _ = fixed_data
    changes = [
        changed_fraction(previous, [0, "problem", "intercept", 0]),
        changed_fraction(previous, [0, "problem", "receiver", 0, 0]),
        changed_fraction(previous, [0, "composition", "effective_map", 0, 0]),
        changed_fraction(previous, [0, "composition", "coefficient_defect", 0, 0]),
        replaced(
            previous,
            [0, "classification", "unrestricted_exact"],
            not previous[0]["classification"]["unrestricted_exact"],
        ),
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
        "prior_artifacts": 51,
        "ancestor_sources": 74,
    }
    assert set(current["source_ledger"]) == set(runner.SOURCES)
    raw = runner.AT.read_bytes()
    assert len(raw) == 1147189
    assert (
        hashlib.sha256(raw).hexdigest()
        == "3fe96ced94f7b4d45feec43d0415a908d656825e21f04a6796329825de4d651a"
    )
    for name, want in current["source_ledger"].items():
        raw = (HERE / name).read_bytes()
        assert len(raw) == want["bytes"] and hashlib.sha256(raw).hexdigest() == want["sha256"]
