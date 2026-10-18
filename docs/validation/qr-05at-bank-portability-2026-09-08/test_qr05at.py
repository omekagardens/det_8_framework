"""Independent parent/basis scalar-sum structural portability checks.

Only test names containing fixed consume authenticated AS/AR cases. Collection and generic
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
        load("_qr05at_test_primary", "kernel.py"),
        load("_qr05at_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05at_test_runner", "study.py")


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


CHECKS = (
    "lineage_partition",
    "coarse_source_identity",
    "inherited_geometric_identity",
    "selected_filter_identity",
    "source_receiver_identity",
    "affine_probe_identity",
    "structural_classification",
)
SCOPE = (
    "source_dictionary_changed",
    "geometry_reintegrated",
    "old_collision_replayed",
    "decoder_refitted",
    "filters_reselected",
    "off_model_normalization_inferred",
    "physical_bank_controls_established",
    "full_field_recovery_tested",
    "measurement_interface_insufficiency_proved",
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


def area(bounds):
    u0, u1, v0, v1 = bounds
    return (u1 - u0) * (v1 - v0)


def overlap(a, b):
    return max(F(), min(a[1], b[1]) - max(a[0], b[0])) * max(F(), min(a[3], b[3]) - max(a[2], b[2]))


def partition_check(problem):
    coarse = [list(map(fraction, b)) for b in problem["coarse_tiles"]]
    bank = [list(map(fraction, row["bounds"])) for row in problem["bank_tiles"]]
    parents = [row["coarse_tile"] for row in problem["bank_tiles"]]
    for b in coarse + bank:
        assert b[0] < b[1] and b[2] < b[3]
    for rectangles in (coarse, bank):
        for i, b in enumerate(rectangles):
            assert all(overlap(b, c) == 0 for c in rectangles[:i])
    children = [[i for i, p in enumerate(parents) if p == j] for j in range(len(coarse))]
    for parent, indices in zip(coarse, children, strict=True):
        assert indices
        for index in indices:
            assert overlap(parent, bank[index]) == area(bank[index])
        assert sum((area(bank[i]) for i in indices), F()) == area(parent)
    return coarse, bank, parents, children


def expected(problem):
    coarse, bank, parents, children = partition_check(problem)
    o, r, q, g, f, l = (
        matrix(problem[key])
        for key in ("observations", "bank", "targets", "geometric", "filters", "receiver")
    )
    a = list(map(fraction, problem["intercept"]))
    c, b, n, t, k = len(coarse), len(bank), len(q[0]), len(q), len(f)
    m, rr = 4 * c, 4 * b
    selected = problem["selected_rows"]
    assert f == [g[i] for i in selected]
    # Direct indexed scalar construction: no C matrix multiplication and no
    # reconstruction of K from zero/unit controls.
    incidence = [
        [F(parents[col // 4] == row // 4 and col % 4 == row % 4) for col in range(rr)]
        for row in range(m)
    ]
    coarse_predicted = [
        [sum((r[4 * child + h][source] for child in children[parent]), F()) for source in range(n)]
        for parent in range(c)
        for h in range(4)
    ]
    assert coarse_predicted == o
    h = [
        [sum((f[j][i] * r[i][source] for i in range(rr)), F()) for source in range(n)]
        for j in range(k)
    ]
    geometric = [
        [sum((g[row][i] * r[i][source] for i in range(rr)), F()) for source in range(n)]
        for row in range(t)
    ]
    assert h == [q[i] for i in selected] and geometric == q
    effective = [
        [
            l[row][4 * parents[col // 4] + col % 4]
            + sum((l[row][m + j] * f[j][col] for j in range(k)), F())
            for col in range(rr)
        ]
        for row in range(t)
    ]
    defect = [[effective[row][col] - g[row][col] for col in range(rr)] for row in range(t)]
    defect_sources = [
        [sum((defect[row][i] * r[i][source] for i in range(rr)), F()) for source in range(n)]
        for row in range(t)
    ]
    residuals = [[a[row] + x for x in defect_sources[row]] for row in range(t)]
    receiver_source = [
        [
            a[row]
            + sum((l[row][i] * o[i][source] for i in range(m)), F())
            + sum((l[row][m + j] * h[j][source] for j in range(k)), F())
            for source in range(n)
        ]
        for row in range(t)
    ]
    assert receiver_source == q
    assert residuals == [[receiver_source[i][j] - q[i][j] for j in range(n)] for i in range(t)]
    assert not any(any(row) for row in residuals)
    structural = [row for row in range(t) if a[row] == 0 and not any(defect[row])]
    restricted = [row for row in range(t) if row not in structural]
    controls = []
    first = None
    for unit in [None, *range(rr)]:
        z = [F(i == unit) if unit is not None else F() for i in range(rr)]
        cv = [
            sum((z[4 * child + h] for child in children[parent]), F())
            for parent in range(c)
            for h in range(4)
        ]
        sv = [sum((coeff * z[i] for i, coeff in enumerate(row)), F()) for row in f]
        observed = cv + sv
        truth = [sum((coeff * z[i] for i, coeff in enumerate(row)), F()) for row in g]
        predicted = [
            offset + sum((coeff * observed[i] for i, coeff in enumerate(row)), F())
            for offset, row in zip(a, l, strict=True)
        ]
        difference = [u - v for u, v in zip(predicted, truth, strict=True)]
        affine = [a[row] + sum((defect[row][i] * z[i] for i in range(rr)), F()) for row in range(t)]
        assert difference == affine
        if first is None and any(difference):
            first = {
                "control_index": len(controls),
                "target_row": next(i for i, x in enumerate(difference) if x),
            }
        controls.append(
            {
                "bank_index": unit,
                "bank_values": z,
                "coarse_values": cv,
                "supplement_values": sv,
                "observed": observed,
                "truth": truth,
                "predicted": predicted,
                "residuals": difference,
                "affine_defect": affine,
            }
        )
    assert (first is None) == (not restricted)
    count_entries = sum(
        sum(len(row[key]) for key in row if key != "bank_index") for row in controls
    )
    assert count_entries == (rr + 1) * (rr + 2 * m + 2 * k + 4 * t)
    counts = {
        "coarse_tiles": c,
        "bank_tiles": b,
        "source_columns": n,
        "coarse_values": m,
        "bank_values": rr,
        "target_rows": t,
        "supplement_values": k,
        "receiver_values": m + k,
        "input_rational_entries": 4 * c
        + 4 * b
        + m * n
        + rr * n
        + t * n
        + t * rr
        + k * rr
        + t
        + t * (m + k),
        "coarse_map_entries": m * rr,
        "effective_map_entries": t * rr,
        "defect_entries": t * rr,
        "nonzero_defect_entries": sum(x != 0 for row in defect for x in row),
        "nonzero_intercept_entries": sum(x != 0 for x in a),
        "source_check_entries": 2 * m * n + k * n + 5 * t * n,
        "bank_controls": rr + 1,
        "bank_control_entries": count_entries,
        "structural_rows": len(structural),
        "restricted_only_rows": len(restricted),
    }
    result = encode(
        {
            "problem": copy.deepcopy(problem),
            "lineage": {
                "coarse_children": children,
                "coarse_map": incidence,
                "coarse_predicted": coarse_predicted,
                "coarse_residuals": [[F()] * n for _ in range(m)],
            },
            "composition": {
                "supplement_source": h,
                "geometric_source": geometric,
                "geometric_residuals": [[F()] * n for _ in range(t)],
                "receiver_source": receiver_source,
                "source_residuals": residuals,
                "effective_map": effective,
                "coefficient_defect": defect,
                "defect_on_sources": defect_sources,
            },
            "classification": {
                "structural_rows": structural,
                "restricted_only_rows": restricted,
                "nonzero_intercept_rows": [i for i, x in enumerate(a) if x],
                "nonzero_defect_rows": [i for i, row in enumerate(defect) if any(row)],
                "unrestricted_exact": not restricted,
                "first_failure": first,
            },
            "bank_controls": controls,
            "checks": dict.fromkeys(CHECKS, True),
            "counts": counts,
        }
    )
    native(result)
    return result


def make_problem(coarse, bank, r, g, selected, a, l, name):
    c, b = len(coarse), len(bank)
    parents = [row["coarse_tile"] for row in bank]
    n = len(r[0])
    o = [
        [
            sum((r[4 * j + h][source] for j, p in enumerate(parents) if p == i), F())
            for source in range(n)
        ]
        for i in range(c)
        for h in range(4)
    ]
    assert len(r) == 4 * b
    return encode(
        {
            "family": name,
            "coarse_tiles": coarse,
            "bank_tiles": bank,
            "target_labels": [{"first": i - 3, "second": -7} for i in range(len(g))],
            "observations": o,
            "bank": r,
            "targets": mm(g, r),
            "geometric": g,
            "selected_rows": selected,
            "filters": [g[i][:] for i in selected],
            "intercept": a,
            "receiver": l,
        }
    )


def single_geometry():
    return [[F(), F(1), F(), F(1)]], [
        {"bounds": [F(), F(1, 3), F(), F(1)], "coarse_tile": 0},
        {"bounds": [F(1, 3), F(1), F(), F(1)], "coarse_tile": 0},
    ]


def source_bank(duplicate=False):
    r = [[F(), F()] for _ in range(8)]
    r[0] = [F(1), F(1) if duplicate else F()]
    r[4] = [F(1) if duplicate else F(), F(1)]
    return r


def basis_row(index, size=8):
    return [F(i == index) for i in range(size)]


def structural_problem():
    coarse, bank = single_geometry()
    return make_problem(
        coarse,
        bank,
        source_bank(),
        [basis_row(4), basis_row(0)],
        [1],
        [F(), F()],
        [[F(1), F(), F(), F(), F(-1)], [F(), F(), F(), F(), F(1)]],
        "structural",
    )


def intercept_problem():
    coarse, bank = single_geometry()
    return make_problem(
        coarse,
        bank,
        source_bank(),
        [basis_row(0)],
        [0],
        [F(1)],
        [[F(-1)] * 4 + [F(1)]],
        "unit-only-trap",
    )


def linear_problem():
    coarse, bank = single_geometry()
    return make_problem(
        coarse,
        bank,
        source_bank(True),
        [basis_row(0)],
        [],
        [F()],
        [[F(1, 2), F(), F(), F()]],
        "hidden-linear-defect",
    )


def mixed_problem():
    coarse, bank = single_geometry()
    return make_problem(
        coarse,
        bank,
        source_bank(),
        [basis_row(4), basis_row(0), [F()] * 8],
        [1],
        [F(), F(1), F()],
        [[F(1), F(), F(), F(), F(-1)], [F(-1)] * 4 + [F(1)], [F()] * 5],
        "mixed",
    )


def two_parent_problem():
    coarse = [[F(), F(1), F(), F(1)], [F(2), F(4), F(-1), F(1)]]
    bank = [
        {"bounds": [F(), F(1, 3), F(), F(1)], "coarse_tile": 0},
        {"bounds": coarse[1][:], "coarse_tile": 1},
        {"bounds": [F(1, 3), F(1), F(), F(1)], "coarse_tile": 0},
    ]
    r = [[F(), F()] for _ in range(12)]
    r[0] = [F(1), F()]
    r[4] = [F(), F(1)]
    r[8] = [F(2), F()]
    g = [[F(i in (0, 8)) for i in range(12)], basis_row(4, 12)]
    return make_problem(
        coarse,
        bank,
        r,
        g,
        [],
        [F(), F()],
        [basis_row(0, 8), basis_row(4, 8)],
        "two-disjoint-parents",
    )


@pytest.mark.parametrize(
    "factory",
    [structural_problem, intercept_problem, linear_problem, mixed_problem, two_parent_problem],
)
def test_generic_complete_scalar_oracle(engines, factory):
    p = factory()
    wanted = expected(p)
    before = wire(p)
    for engine in engines:
        assert wire(engine.build_family(p)) == wire(wanted)
        assert wire(p) == before


def test_all_unit_controls_can_pass_while_zero_control_fails(engines):
    for engine in engines:
        result = engine.build_family(intercept_problem())
        assert result["composition"]["coefficient_defect"] == encode([[F(-1)] * 8])
        assert result["composition"]["defect_on_sources"] == encode([[F(-1), F(-1)]])
        assert result["composition"]["source_residuals"] == encode([[F(), F()]])
        assert result["classification"]["first_failure"] == {"control_index": 0, "target_row": 0}
        assert result["bank_controls"][0]["residuals"] == [fw(1)]
        assert all(row["residuals"] == [fw(0)] for row in result["bank_controls"][1:])


def test_linear_defect_and_mixed_classification_are_not_erased_by_source_agreement(engines):
    for engine in engines:
        result = engine.build_family(linear_problem())
        defect = [F(-1, 2) if i == 0 else F(1, 2) if i == 4 else F() for i in range(8)]
        assert result["composition"]["coefficient_defect"] == encode([defect])
        assert result["classification"]["nonzero_intercept_rows"] == []
        assert result["classification"]["first_failure"] == {"control_index": 1, "target_row": 0}
        assert result["bank_controls"][1]["residuals"] == [fw(F(-1, 2))]
        assert result["bank_controls"][5]["residuals"] == [fw(F(1, 2))]
        mixed = engine.build_family(mixed_problem())
        assert mixed["classification"]["structural_rows"] == [0, 2]
        assert mixed["classification"]["restricted_only_rows"] == [1]
        assert mixed["classification"]["first_failure"] == {"control_index": 0, "target_row": 1}


def test_raw_global_moments_sum_with_unit_not_area_weights(engines):
    for engine in engines:
        f = engine.build_family(structural_problem())
        c = matrix(f["lineage"]["coarse_map"])
        assert c == [[F(col % 4 == row) for col in range(8)] for row in range(4)]
        assert engine.produce(
            f["lineage"]["coarse_map"], encode([F(1), F(2), F(3), F(4), F(5), F(6), F(7), F(8)])
        ) == encode([F(6), F(8), F(10), F(12)])
        assert f["lineage"]["coarse_children"] == [[0, 1]]


def block_matrix(block, count):
    size = len(block)
    return [
        [block[i % size][j % size] if i // size == j // size else F() for j in range(size * count)]
        for i in range(size * count)
    ]


def transformed_problem(p, u, ui, v):
    c, b = len(p["coarse_tiles"]), len(p["bank_tiles"])
    pmap, smap = block_matrix(u, c), block_matrix(u, b)
    pinverse, sinverse = block_matrix(ui, c), block_matrix(ui, b)
    result = copy.deepcopy(p)
    for key, transform in (("observations", pmap), ("bank", smap)):
        result[key] = encode(mm(transform, matrix(p[key])))
    result["targets"] = encode([[v * x for x in row] for row in matrix(p["targets"])])
    for key in ("geometric", "filters"):
        result[key] = encode([[v * x for x in row] for row in mm(matrix(p[key]), sinverse)])
    result["intercept"] = encode([v * fraction(x) for x in p["intercept"]])
    result["receiver"] = encode(
        [
            [v * x for x in mm([row[: 4 * c]], pinverse)[0]] + row[4 * c :]
            for row in matrix(p["receiver"])
        ]
    )
    return result, pmap, smap, sinverse


@pytest.mark.parametrize("factory", [mixed_problem, two_parent_problem])
def test_shared_signed_basis_covariance_and_same_transported_probes(engines, factory):
    u = [
        [F(), F(1), F(), F()],
        [F(1), F(), F(), F()],
        [F(1), F(-2), F(3), F()],
        [F(), F(1), F(2), F(5)],
    ]
    ui = [
        [F(), F(1), F(), F()],
        [F(1), F(), F(), F()],
        [F(2, 3), F(-1, 3), F(1, 3), F()],
        [F(-7, 15), F(2, 15), F(-2, 15), F(1, 5)],
    ]
    assert mm(u, ui) == [[F(i == j) for j in range(4)] for i in range(4)]
    v = F(7, 3)
    p = factory()
    moved, pm, sm, si = transformed_problem(p, u, ui, v)
    a, b = expected(p), expected(moved)
    c = matrix(a["lineage"]["coarse_map"])
    assert mm(pm, c) == mm(c, sm)
    for key in ("effective_map", "coefficient_defect"):
        assert matrix(b["composition"][key]) == [
            [v * x for x in row] for row in mm(matrix(a["composition"][key]), si)
        ]
    assert a["classification"]["structural_rows"] == b["classification"]["structural_rows"]
    assert (
        a["classification"]["restricted_only_rows"] == b["classification"]["restricted_only_rows"]
    )
    for engine in engines:
        assert wire(engine.build_family(p)) == wire(a)
        assert wire(engine.build_family(moved)) == wire(b)
        for old in a["bank_controls"]:
            z = encode(mv(sm, list(map(fraction, old["bank_values"]))))
            coarse = engine.produce(b["lineage"]["coarse_map"], z)
            supplements = engine.produce(moved["filters"], z)
            predicted = engine.apply(moved["intercept"], moved["receiver"], coarse + supplements)
            truth = engine.produce(moved["geometric"], z)
            assert [fraction(x) - fraction(y) for x, y in zip(predicted, truth, strict=True)] == [
                v * fraction(x) for x in old["residuals"]
            ]


def permuted_problem(p, coarse_order, bank_order):
    result = copy.deepcopy(p)
    coarse_columns = [4 * i + h for i in coarse_order for h in range(4)]
    bank_columns = [4 * i + h for i in bank_order for h in range(4)]
    result["coarse_tiles"] = [copy.deepcopy(p["coarse_tiles"][i]) for i in coarse_order]
    result["bank_tiles"] = [
        {
            **copy.deepcopy(p["bank_tiles"][i]),
            "coarse_tile": coarse_order.index(p["bank_tiles"][i]["coarse_tile"]),
        }
        for i in bank_order
    ]
    result["observations"] = [copy.deepcopy(p["observations"][i]) for i in coarse_columns]
    result["bank"] = [copy.deepcopy(p["bank"][i]) for i in bank_columns]
    for key in ("filters", "geometric"):
        result[key] = [[copy.deepcopy(row[i]) for i in bank_columns] for row in p[key]]
    m = 4 * len(coarse_order)
    result["receiver"] = [
        [copy.deepcopy(row[i]) for i in coarse_columns] + copy.deepcopy(row[m:])
        for row in p["receiver"]
    ]
    return result, coarse_columns, bank_columns


def test_independent_tile_permutations_preserve_array_bound_coordinates(engines):
    p = two_parent_problem()
    moved, coarse_order, bank_order = permuted_problem(p, [1, 0], [2, 0, 1])
    wanted = expected(p)
    expected_moved = expected(moved)
    assert expected_moved["lineage"]["coarse_children"] == [[2], [0, 1]]
    for key in ("effective_map", "coefficient_defect"):
        assert expected_moved["composition"][key] == [
            [row[i] for i in bank_order] for row in wanted["composition"][key]
        ]
    assert expected_moved["lineage"]["coarse_predicted"] == [
        p["observations"][i] for i in coarse_order
    ]
    for engine in engines:
        assert wire(engine.build_family(moved)) == wire(expected_moved)


def test_every_control_calls_restricted_public_evaluators(engines, monkeypatch):
    from collections import Counter

    p = mixed_problem()
    wanted = expected(p)
    for engine in engines:
        applied = []
        produced = []
        original_apply, original_produce = engine.apply, engine.produce

        def applying(a, l, x, applied=applied, original_apply=original_apply):
            applied.append(wire([a, l, x]))
            return original_apply(a, l, x)

        def producing(h, z, produced=produced, original_produce=original_produce):
            produced.append(wire([h, z]))
            return original_produce(h, z)

        with monkeypatch.context() as m:
            m.setattr(engine, "apply", applying)
            m.setattr(engine, "produce", producing)
            result = engine.build_family(p)
        assert wire(result) == wire(wanted)
        need_a = Counter(
            wire([p["intercept"], p["receiver"], row["observed"]])
            for row in wanted["bank_controls"]
        )
        need_p = Counter(
            wire([h, row["bank_values"]])
            for row in wanted["bank_controls"]
            for h in (wanted["lineage"]["coarse_map"], p["filters"], p["geometric"])
        )
        assert not (need_a - Counter(applied))
        assert not (need_p - Counter(produced))


def test_raw_widths_empty_lists_and_file_blind_external_values(engines, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("raw evaluator attempted file access")

    with monkeypatch.context() as m:
        m.setattr(builtins, "open", forbidden)
        m.setattr(Path, "open", forbidden)
        m.setattr(Path, "read_bytes", forbidden)
        m.setattr(Path, "read_text", forbidden)
        for engine in engines:
            assert engine.produce([], []) == []
            assert engine.produce([[], []], []) == [fw(0), fw(0)]
            assert engine.produce([[fw(2), fw(-3), fw(4)]], [fw(-1), fw(7), fw(2)]) == [fw(-15)]
            assert engine.apply([fw(5)], [[]], []) == [fw(5)]
            assert engine.apply([fw(5)], [[fw(2), fw(-3), fw(4)]], [fw(-1), fw(7), fw(2)]) == [
                fw(-10)
            ]


def test_shared_inputs_are_accepted_and_outputs_detached(engines):
    p = structural_problem()
    p["filters"] = [p["geometric"][1]]
    frozen = wire(p)
    for engine in engines:
        result = engine.build_family(p)
        before = wire(result)
        assert wire(p) == frozen
        p["family"] = "changed"
        assert wire(result) == before
        p["family"] = "structural"
        result["lineage"]["coarse_map"][0][0][0] += 1
        assert wire(p) == frozen
        assert wire(engine.build_family(p)) == before


def test_accepted_dimension_edges_and_no_reselection(engines):
    p = structural_problem()
    for key in ("observations", "bank", "targets"):
        p[key] = [row * 288 for row in p[key]]
    zero = make_problem(
        [[F(), F(1), F(), F(1)]],
        [{"bounds": [F(), F(1), F(), F(1)], "coarse_tile": 0}],
        [[F()] for _ in range(4)],
        [[F()] * 4 for _ in range(64)],
        list(range(64)),
        [F()] * 64,
        [[F()] * 68 for _ in range(64)],
        "all-zero-supplements",
    )
    for engine in engines:
        for value in (p, zero):
            assert wire(engine.build_family(value)) == wire(expected(value))
        assert engine.produce([[fw(0)] * 1024 for _ in range(320)], [fw(1)] * 1024) == [fw(0)] * 320
        assert (
            engine.apply([fw(3)] * 64, [[fw(0)] * 320 for _ in range(64)], [fw(1)] * 320)
            == [fw(3)] * 64
        )


def cancellation_problem(overflow=False):
    d = F(1 << 4095)
    coarse = [[F(), F(1), F(), F(1)]]
    bank = [{"bounds": coarse[0][:], "coarse_tile": 0}]
    g = [[d] * 4]
    receiver = [[F() if overflow else -d] * 4 + [F(2)]]
    return make_problem(
        coarse, bank, [[F()] for _ in range(4)], g, [0], [F()], receiver, "cancellation"
    )


class NativeListSubclass(list):
    pass


def malformed_families():
    p = structural_problem()
    yield None
    yield []
    yield {**p, "normalized_bank": []}
    yield {k: v for k, v in p.items() if k != "receiver"}
    for value in ("", False, 1):
        yield replaced(p, ["family"], value)
    for key in (
        "coarse_tiles",
        "bank_tiles",
        "target_labels",
        "observations",
        "bank",
        "targets",
        "geometric",
        "selected_rows",
        "filters",
        "intercept",
        "receiver",
    ):
        yield replaced(p, [key], None)
        yield replaced(p, [key], tuple(p[key]))
    yield replaced(p, ["coarse_tiles"], [])
    yield replaced(p, ["bank_tiles"], [])
    yield replaced(p, ["coarse_tiles"], p["coarse_tiles"] * 65)
    yield replaced(p, ["bank_tiles"], p["bank_tiles"] * 129)
    yield replaced(p, ["targets"], [])
    yield replaced(p, ["targets"], [[]] * 2)
    yield replaced(p, ["targets"], [[fw(0)] * 577] * 2)
    yield replaced(p, ["target_labels"], p["target_labels"] * 33)
    yield replaced(p, ["target_labels"], list(reversed(p["target_labels"])))
    yield replaced(p, ["target_labels", 0, "first"], True)
    yield replaced(p, ["target_labels", 0, "extra"], 0)
    yield replaced(p, ["target_labels", 1], p["target_labels"][0])
    for value in (-1, True, 1):
        yield replaced(p, ["bank_tiles", 0, "coarse_tile"], value)
    yield replaced(p, ["bank_tiles", 0, "extra"], 0)
    for key in ("observations", "bank", "targets", "geometric", "filters", "receiver"):
        yield replaced(p, [key, -1], [])
    yield replaced(p, ["filters", 0, 0], fw(2))
    yield replaced(p, ["selected_rows"], [1, 1])
    yield replaced(p, ["selected_rows"], [2])
    yield replaced(p, ["selected_rows"], [True])
    yield replaced(p, ["selected_rows"], [1, 0])
    yield replaced(p, ["intercept"], [fw(0)])
    yield replaced(p, ["observations", 0, 0], fw(7))
    yield replaced(p, ["targets", 0, 0], fw(7))
    yield replaced(p, ["geometric", 0, 0], fw(7))
    yield replaced(p, ["intercept", 0], fw(7))
    for value in (True, 0.0, F(0), (0, 1), [0], [0, 0], [0, -1], [2, 2], [1 << 4096, 1]):
        yield replaced(p, ["receiver", -1, -1], value)
        yield replaced(p, ["coarse_tiles", 0, 0], value)
    yield replaced(p, ["bank_tiles", 1, "bounds"], p["bank_tiles"][0]["bounds"])
    yield replaced(p, ["bank_tiles", 1, "bounds", 0], fw(F(1, 2)))
    yield replaced(p, ["bank_tiles", 0, "bounds", 0], fw(-1))
    yield replaced(p, ["coarse_tiles", 0, 1], fw(0))
    yield NativeListSubclass()
    two = two_parent_problem()
    yield replaced(two, ["bank_tiles", 1, "coarse_tile"], 0)
    yield replaced(two, ["coarse_tiles", 1], two["coarse_tiles"][0])


def malformed_producers():
    h, x = [[fw(1)] * 3], [fw(1)] * 3
    for value in (None, {}, (), NativeListSubclass(h), h * 321, [[fw(0)] * 1025]):
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
        raise RuntimeError("producer cancellation")
    if engine.apply([fw(0)], [[fw(d), fw(-d)]], [fw(2), fw(2)]) != [fw(0)]:
        raise RuntimeError("receiver cancellation")
    require_rejection(lambda: engine.produce([[fw(d), fw(d)]], [fw(1), fw(1)]))
    require_rejection(lambda: engine.apply([fw(0)], [[fw(d), fw(d)]], [fw(1), fw(1)]))
    valid = cancellation_problem()
    if not engine.build_family(valid)["classification"]["unrestricted_exact"]:
        raise RuntimeError("effective-map cancellation")
    require_rejection(lambda: engine.build_family(cancellation_problem(True)))
    cyclic = structural_problem()
    cyclic["bank"].append(cyclic["bank"])
    require_rejection(lambda: engine.build_family(cyclic))
    cycle = []
    cycle.append(cycle)
    require_rejection(lambda: engine.produce(cycle, [fw(1)]))
    require_rejection(lambda: engine.apply([fw(1)], [[fw(1)]], cycle))
    return count + 6


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
                    replaced(structural_problem(), ["receiver", -1, -1], value)
                )
            )
            require_rejection(lambda value=value: engine.produce([[fw(1)], [value]], [fw(2)]))
            require_rejection(
                lambda value=value: engine.apply([fw(1), fw(2)], [[fw(1)], [value]], [fw(3)])
            )
    finally:
        engine._fraction = original
    original = engine._partition
    engine._partition = forbidden
    try:
        require_rejection(
            lambda: engine.build_family(
                replaced(structural_problem(), ["receiver", -1, -1], [1, 0])
            )
        )
    finally:
        engine._partition = original
    original = engine._dot
    engine._dot = forbidden
    try:
        p = structural_problem()
        p["bank_tiles"][1]["bounds"] = p["bank_tiles"][0]["bounds"]
        require_rejection(lambda: engine.build_family(p))
        require_rejection(lambda: engine.produce([[fw(1)], [[1, 0]]], [fw(1)]))
        require_rejection(lambda: engine.apply([fw(1), fw(2)], [[fw(1)], [[1, 0]]], [fw(1)]))
    finally:
        engine._dot = original
    if calls:
        raise RuntimeError("late admission ordering")
    return 10


def test_native_partition_identity_and_bit_guards(engines):
    inventory = [explicit_guards(e) for e in engines]
    assert inventory[0] == inventory[1] and inventory[0] > 100
    assert [pre_arithmetic_guards(e) for e in engines] == [10, 10]


@pytest.mark.parametrize("optimized", [False, True])
def test_isolated_explicit_normal_and_optimized_guards(tmp_path, optimized):
    script = r"""
import importlib.util,json,sys
from pathlib import Path
path=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("at_guard_tests",path)
t=importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
counts=[]
for name,file in (("primary","kernel.py"),("reference","reference.py")):
    engine=t.load("_qr05at_guard_"+name,file)
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
        + len(list(malformed_producers()))
        + len(list(malformed_receivers()))
        + 16
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


def changed_fraction(tree, path):
    current = tree
    for key in path:
        current = current[key]
    return replaced(tree, path, fw(fraction(current) + 1))


def family_mutations(family):
    for path in (
        ["problem", "coarse_tiles", 0, 0],
        ["problem", "bank_tiles", 0, "bounds", 0],
        ["problem", "intercept", 0],
        ["problem", "receiver", 0, 0],
        ["lineage", "coarse_map", 0, 0],
        ["lineage", "coarse_predicted", 0, 0],
        ["lineage", "coarse_residuals", 0, 0],
    ):
        yield changed_fraction(family, path)
    yield replaced(
        family, ["lineage", "coarse_children", 0], family["lineage"]["coarse_children"][0] + [-1]
    )
    for key in (
        "supplement_source",
        "geometric_source",
        "geometric_residuals",
        "receiver_source",
        "source_residuals",
        "effective_map",
        "coefficient_defect",
        "defect_on_sources",
    ):
        if family["composition"][key]:
            yield changed_fraction(family, ["composition", key, 0, 0])
        else:
            yield replaced(family, ["composition", key], [[]])
    for key in (
        "structural_rows",
        "restricted_only_rows",
        "nonzero_intercept_rows",
        "nonzero_defect_rows",
    ):
        yield replaced(family, ["classification", key], family["classification"][key] + [-1])
    yield replaced(
        family,
        ["classification", "unrestricted_exact"],
        not family["classification"]["unrestricted_exact"],
    )
    first = family["classification"]["first_failure"]
    if first is None:
        yield replaced(
            family, ["classification", "first_failure"], {"control_index": 0, "target_row": 0}
        )
    else:
        for key in ("control_index", "target_row"):
            yield replaced(family, ["classification", "first_failure", key], first[key] + 1)
    yield replaced(family, ["bank_controls"], family["bank_controls"][:-1])
    yield replaced(family, ["bank_controls", 0, "bank_index"], -1)
    for key in (
        "bank_values",
        "coarse_values",
        "supplement_values",
        "observed",
        "truth",
        "predicted",
        "residuals",
        "affine_defect",
    ):
        if family["bank_controls"][0][key]:
            yield changed_fraction(family, ["bank_controls", 0, key, 0])
        else:
            yield replaced(family, ["bank_controls", 0, key], [fw(1)])
    yield changed_fraction(family, ["bank_controls", 1, "residuals", 0])
    yield changed_fraction(family, ["bank_controls", -1, "affine_defect", 0])
    yield replaced(family, ["checks", "structural_classification"], False)
    for key in ("bank_control_entries", "source_check_entries", "nonzero_defect_entries"):
        yield replaced(family, ["counts", key], family["counts"][key] + 1)


def test_generic_complete_wire_corruptions_are_nonvacuous(runner):
    counts = []
    for factory in (structural_problem, intercept_problem, linear_problem, mixed_problem):
        wanted = expected(factory())
        mutations = list(family_mutations(wanted))
        for bad in mutations:
            assert wire(bad) != wire(wanted)
            with pytest.raises(ValueError):
                runner.verify_suite(bad, wanted)
        counts.append(len(mutations))
    assert sum(counts) > 150


def test_selected_repair_link_bounds_equal_subrectangle_and_wrong_sibling(runner):
    parent = encode([F(), F(1, 2), F(), F(1)])
    child = encode([F(1, 4), F(1, 2), F(1, 3), F(2, 3)])
    sibling = encode([F(1, 2), F(1), F(), F(1)])
    assert runner.check_repair_link_bounds(parent, parent) is None
    assert runner.check_repair_link_bounds(child, parent) is None
    for wrong in (
        sibling,
        encode([F(), F(), F(), F(1)]),
        replaced(child, [3], []),
        replaced(child, [3], [0]),
        replaced(child, [3], [2, 2]),
        replaced(child, [0], [True, 1]),
        replaced(child, [0], [1 << 4096, 1]),
    ):
        with pytest.raises(ValueError):
            runner.check_repair_link_bounds(wrong, parent)


BRIDGES = {
    "AS_selected_families": ["grid", "warp"],
    "AS_frozen_maps_equal": True,
    "AS_source_inputs_equal": True,
    "AR_source_inputs_equal": True,
    "AR_lineage_inputs_equal": True,
    "AR_observation_labels_checked": True,
    "AR_repair_links_checked": True,
    "AR_zero_repair_intercept": True,
    "other_historical_mathematics_replayed": False,
    "older_executors_run": False,
}


def projected_problem(current, old):
    sp = current["problem"]
    return {
        "family": sp["family"],
        "coarse_tiles": [copy.deepcopy(row["bounds"]) for row in old["geometry"]["coarse_tiles"]],
        "bank_tiles": [
            {key: copy.deepcopy(row[key]) for key in ("bounds", "coarse_tile")}
            for row in old["geometry"]["repair_tiles"]
        ],
        "target_labels": copy.deepcopy(sp["target_labels"]),
        "observations": copy.deepcopy(sp["observations"]),
        "bank": copy.deepcopy(sp["bank"]),
        "targets": copy.deepcopy(sp["targets"]),
        "geometric": copy.deepcopy(sp["filters"]),
        "selected_rows": copy.deepcopy(current["selection"]["target_rows"]),
        "filters": copy.deepcopy(current["selection"]["filters"]),
        "intercept": copy.deepcopy(current["decoder"]["intercept"]),
        "receiver": copy.deepcopy(current["decoder"]["matrix"]),
    }


def independent_history_checks(families, previous):
    as_families, ar_families = previous
    for f, current, old in zip(families, as_families, ar_families, strict=True):
        assert f["problem"] == projected_problem(current, old)
        p = f["problem"]
        for key, oldkey in (
            ("observations", "coarse_observations"),
            ("bank", "repair_observations"),
            ("targets", "fine_targets"),
            ("target_labels", "fine_response_rows"),
        ):
            assert p[key] == old["matrices"][oldkey]
        assert p["geometric"] == old["repair"]["matrix"]
        assert old["repair"]["intercept"] == [fw(0)] * len(p["targets"])
        geo = old["geometry"]
        for key, tiles in (
            ("coarse_observation_rows", geo["coarse_tiles"]),
            ("repair_observation_rows", geo["repair_tiles"]),
        ):
            assert old["matrices"][key] == [
                {"tile": i, "basis": h} for i in range(len(tiles)) for h in range(4)
            ]
        assert [
            {key: row[key] for key in ("event", "bounds")} for row in geo["coarse_tiles"]
        ] == old["problem"]["coarse_tiles"]
        assert [
            {key: row[key] for key in ("event", "bounds", "coarse_tile")}
            for row in geo["fine_tiles"]
        ] == old["problem"]["fine_tiles"]
        for row in geo["repair_tiles"]:
            index = row["fine_tile"]
            parent = geo["fine_tiles"][index]
            assert type(index) is int and type(row["coarse_tile"]) is int
            assert wire(row["event"]) == wire(parent["event"])
            assert row["coarse_tile"] == parent["coarse_tile"]
            child_bounds = list(map(fraction, row["bounds"]))
            parent_bounds = list(map(fraction, parent["bounds"]))
            assert overlap(child_bounds, parent_bounds) == area(child_bounds) > 0


def payload(families):
    return [
        {
            "family": f["problem"]["family"],
            "input_bytes": len(wire(f["problem"])),
            "lineage_bytes": len(wire(f["lineage"])),
            "composition_bytes": len(wire(f["composition"])),
            "classification_bytes": len(wire(f["classification"])),
            "bank_controls_bytes": len(wire(f["bank_controls"])),
            "receiver_map_bytes": len(
                wire({"intercept": f["problem"]["intercept"], "matrix": f["problem"]["receiver"]})
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


def synthetic_histories(family):
    p = family["problem"]
    current = {
        "problem": {
            "family": p["family"],
            "observations": copy.deepcopy(p["observations"]),
            "bank": copy.deepcopy(p["bank"]),
            "targets": copy.deepcopy(p["targets"]),
            "filters": copy.deepcopy(p["geometric"]),
            "target_labels": copy.deepcopy(p["target_labels"]),
        },
        "selection": {
            "target_rows": copy.deepcopy(p["selected_rows"]),
            "filters": copy.deepcopy(p["filters"]),
        },
        "decoder": {
            "intercept": copy.deepcopy(p["intercept"]),
            "matrix": copy.deepcopy(p["receiver"]),
        },
    }
    coarse = [
        {"event": i, "bounds": copy.deepcopy(bounds)} for i, bounds in enumerate(p["coarse_tiles"])
    ]
    fine = [
        {"event": i, "bounds": copy.deepcopy(row["bounds"]), "coarse_tile": row["coarse_tile"]}
        for i, row in enumerate(p["bank_tiles"])
    ]
    repair = [{**copy.deepcopy(row), "fine_tile": i} for i, row in enumerate(fine)]
    old = {
        "problem": {
            "family": p["family"],
            "coarse_tiles": copy.deepcopy(coarse),
            "fine_tiles": copy.deepcopy(fine),
        },
        "geometry": {"coarse_tiles": coarse, "fine_tiles": fine, "repair_tiles": repair},
        "matrices": {
            "coarse_observations": copy.deepcopy(p["observations"]),
            "repair_observations": copy.deepcopy(p["bank"]),
            "fine_targets": copy.deepcopy(p["targets"]),
            "fine_response_rows": copy.deepcopy(p["target_labels"]),
            "coarse_observation_rows": [
                {"tile": i, "basis": h} for i in range(len(coarse)) for h in range(4)
            ],
            "repair_observation_rows": [
                {"tile": i, "basis": h} for i in range(len(repair)) for h in range(4)
            ],
        },
        "repair": {
            "intercept": [fw(0)] * len(p["targets"]),
            "matrix": copy.deepcopy(p["geometric"]),
        },
    }
    return current, old


def test_synthetic_tuple_history_full_suite_and_all_cached_routes(runner, monkeypatch):
    problems = []
    for name, factory in zip(FAMILIES, (structural_problem, mixed_problem), strict=True):
        p = factory()
        p["family"] = name
        problems.append(p)
    families = list(map(expected, problems))
    histories = list(map(synthetic_histories, families))
    previous = ([h[0] for h in histories], [h[1] for h in histories])
    independent_history_checks(families, previous)
    wanted = expected_suite(families)
    lookup = {f["problem"]["family"]: f for f in families}

    def projection(current, old):
        return [projected_problem(a, b) for a, b in zip(current, old, strict=True)], (current, old)

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
    bad = copy.deepcopy(previous)
    bad[0][0]["decoder"]["intercept"][0] = fw(7)
    with pytest.raises(ValueError):
        runner.assemble_suite(families, bad)

    def changing(p):
        answer = copy.deepcopy(lookup[p["family"]])
        p["family"] = "changed"
        return answer

    monkeypatch.setattr(runner, "load_engine", lambda name: SimpleNamespace(build_family=changing))
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
def test_fixed_complete_scalar_oracle_and_restricted_bank_controls(engines, fixed_data, index):
    problems, _, wanted, _ = fixed_data
    for engine in engines:
        p = copy.deepcopy(problems[index])
        before = wire(p)
        actual = engine.build_family(p)
        assert wire(p) == before
        assert wire(actual) == wire(wanted[index])
        for control in actual["bank_controls"]:
            z = control["bank_values"]
            coarse = engine.produce(actual["lineage"]["coarse_map"], z)
            supplement = engine.produce(p["filters"], z)
            assert coarse + supplement == control["observed"]
            assert engine.produce(p["geometric"], z) == control["truth"]
            assert (
                engine.apply(p["intercept"], p["receiver"], coarse + supplement)
                == control["predicted"]
            )


def test_fixed_full_suite_payload_and_source_restriction(runner, fixed_data):
    problems, previous, families, wanted = fixed_data
    assert wire(runner.assemble_suite(families, previous)) == wire(wanted)
    assert runner.historical_bridges(families, previous) == BRIDGES
    assert runner.payload_sizes(families) == payload(families)
    for p, f in zip(problems, families, strict=True):
        assert len(p["coarse_tiles"]) == 8 and len(p["bank_tiles"]) == 12
        assert len(p["observations"]) == 32 and len(p["bank"]) == 48
        assert len(p["targets"]) == 64 and len(p["targets"][0]) == 108
        assert len(p["selected_rows"]) == 5 and len(f["bank_controls"]) == 49
        assert f["counts"]["bank_control_entries"] == 49 * (48 + 2 * 32 + 2 * 5 + 4 * 64)
        assert f["counts"]["source_check_entries"] == 2 * 32 * 108 + 5 * 108 + 5 * 64 * 108
        assert all(
            not any(fraction(x) for x in row) for row in f["composition"]["source_residuals"]
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


def test_fixed_full_family_and_suite_corruptions_are_nonvacuous(runner, fixed_data):
    _, _, families, wanted = fixed_data
    for f in families:
        for bad in family_mutations(f):
            assert wire(bad) != wire(f)
            with pytest.raises(ValueError):
                runner.verify_suite(bad, f)
    changes = [
        replaced(wanted, ["families"], list(reversed(families))),
        replaced(wanted, ["prior_bridges", "AS_frozen_maps_equal"], False),
        replaced(wanted, ["prior_bridges", "older_executors_run"], True),
        replaced(
            wanted,
            ["payload_sizes", 0, "composition_bytes"],
            wanted["payload_sizes"][0]["composition_bytes"] + 1,
        ),
        replaced(
            wanted,
            ["totals", "nonzero_defect_entries"],
            wanted["totals"]["nonzero_defect_entries"] + 1,
        ),
        replaced(wanted, ["scope", "measurement_interface_insufficiency_proved"], True),
        replaced(wanted, ["scope", "off_model_normalization_inferred"], True),
        {**wanted, "extra": 0},
    ]
    for bad in changes:
        assert wire(bad) != wire(wanted)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, wanted)


def test_fixed_selected_producer_changes_and_original_tile_link(runner, fixed_data):
    _, previous, families, _ = fixed_data
    # The outer tuple is orchestration, not part of the mathematical wire.
    original = list(previous)
    paths = [
        [0, 0, "decoder", "intercept", 0],
        [0, 0, "decoder", "matrix", 0, 0],
        [0, 0, "selection", "filters", 0, 0],
        [0, 0, "problem", "observations", 0, 0],
        [0, 0, "problem", "bank", 0, 0],
        [0, 0, "problem", "targets", 0, 0],
        [0, 0, "problem", "filters", 0, 0],
        [1, 0, "repair", "intercept", 0],
        [1, 0, "matrices", "coarse_observations", 0, 0],
        [1, 0, "matrices", "repair_observations", 0, 0],
        [1, 0, "matrices", "fine_targets", 0, 0],
        [1, 0, "repair", "matrix", 0, 0],
        [1, 0, "geometry", "coarse_tiles", 0, "bounds", 0],
        [1, 0, "geometry", "repair_tiles", 0, "bounds", 0],
    ]
    changed = [changed_fraction(original, path) for path in paths]
    for path, value in (
        ([0, 0, "selection", "target_rows", 0], -1),
        ([1, 0, "matrices", "coarse_observation_rows", 0, "basis"], 3),
        ([1, 0, "matrices", "repair_observation_rows", 0, "tile"], -1),
        ([1, 0, "geometry", "repair_tiles", 0, "coarse_tile"], False),
        ([1, 0, "geometry", "repair_tiles", 0, "event"], True),
    ):
        changed.append(replaced(original, path, value))
    geo = previous[1][0]["geometry"]
    choice = next(
        (
            (i, j)
            for i, row in enumerate(geo["repair_tiles"])
            for j, origin in enumerate(geo["fine_tiles"])
            if j != row["fine_tile"]
            and origin["event"] == row["event"]
            and origin["coarse_tile"] == row["coarse_tile"]
            and origin["bounds"] != row["bounds"]
        ),
        None,
    )
    if choice is None:
        # Same-parent siblings are covered synthetically; fixed inventories need
        # only supply a distinct, incorrect original-tile reference.
        choice = (0, (geo["repair_tiles"][0]["fine_tile"] + 1) % len(geo["fine_tiles"]))
    changed.append(
        replaced(original, [1, 0, "geometry", "repair_tiles", choice[0], "fine_tile"], choice[1])
    )
    for bad in changed:
        assert wire(bad) != wire(original)
        with pytest.raises(ValueError):
            runner.historical_bridges(families, tuple(bad))


def test_fixed_unselected_historical_mathematics_is_not_replayed(runner, fixed_data):
    problems, previous, families, _ = fixed_data
    original = list(previous)
    changes = [
        replaced(original, [0, 0, "base", "delta"], previous[0][0]["base"]["delta"] + 1),
        replaced(original, [0, 0, "witnesses"], []),
        replaced(original, [1, 0, "certificate", "collision"], None),
    ]
    for bad in changes:
        assert wire(bad) != wire(original)
        assert runner.project_inputs(*bad)[0] == problems
        assert runner.historical_bridges(families, tuple(bad)) == BRIDGES


def test_fixed_source_and_ancestor_identity_inventory(runner):
    identity = runner.identities()
    assert {k: len(identity[k]) for k in identity} == {
        "source_ledger": 5,
        "prior_artifacts": 50,
        "ancestor_sources": 69,
    }
    assert set(identity["source_ledger"]) == set(runner.SOURCES)
    for path, count, sha in (
        (runner.AS, 614211, "901c7e1a7c53be35be5654fbb01e5bbde4044f6a50184dd80014df155129e366"),
        (runner.AR, 704842, "c9ed0e299c057eb6503238a3bc5ce18352abe81bc111615464afaa6ed264e4f8"),
    ):
        raw = runner.plain_bytes(path)
        assert len(raw) == count and hashlib.sha256(raw).hexdigest() == sha
        document = json.loads(raw)
        assert runner.canonical(document) == raw
        native(document["suite"])
    for key, base in (
        ("source_ledger", HERE),
        ("prior_artifacts", HERE.parent),
        ("ancestor_sources", HERE.parent),
    ):
        for path, want in identity[key].items():
            raw = runner.plain_bytes(base / path)
            assert len(raw) == want["bytes"] and hashlib.sha256(raw).hexdigest() == want["sha256"]
