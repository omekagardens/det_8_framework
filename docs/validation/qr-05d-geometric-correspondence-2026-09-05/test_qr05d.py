"""Independent exact tests of the bounded scalar order/geometry diagnostic.

The scalar coefficient matrices are not quantum channels or probabilities.
No prior QR executor, DET model, RET source, or numerical tolerance is used.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from itertools import permutations
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CASES = (
    "mesh3",
    "mesh5",
    "mesh7",
    "mesh5_boost",
    "mesh5_dilate",
    "mesh5_dilate_wrong_density",
    "mesh5_warp",
    "ferrers6",
    "standard_example3",
)
F = Fraction


def problem(case="mesh3"):
    return {"schema_version": "det8-qr05d-problem-v1", "case": case}


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("test-private module name already occupied")
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load research executor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05d_test_primary", "geometry.py"),
        private_module("_qr05d_test_reference", "reference_qr05d.py"),
    )


@pytest.fixture(scope="session")
def results(executors):
    return {case: tuple(module.analyze(problem(case)) for module in executors) for case in CASES}


def rational_matrix(wire):
    return [[F(value) for value in row] for row in wire]


def pair_row(result, source, target):
    return next(
        row
        for row in result["geometry"]["pairs"]
        if row["source"] == source and row["target"] == target
    )


def probe_pair(result, name):
    probe = next(row for row in result["probes"] if row["name"] == name)
    return pair_row(result, probe["source"], probe["target"])


def supplied_points(case):
    if case == "standard_example3":
        return None
    if case == "ferrers6":
        return [
            (F(0), F(0)),
            *(
                (F(u, 16), F(v, 16))
                for u, v in ((2, 6), (4, 4), (6, 2), (3, 14), (5, 12), (14, 10))
            ),
            (F(1), F(1)),
        ]
    m = 3 if case == "mesh3" else 7 if case == "mesh7" else 5
    epsilon = F(1, 4 * m)
    denominator = (m + 1) * (1 + epsilon)
    points = [(F(0), F(0))]
    points.extend(
        ((F(i) + epsilon * j) / denominator, (F(j) + epsilon * i) / denominator)
        for i in range(1, m + 1)
        for j in range(1, m + 1)
    )
    points.append((F(1), F(1)))
    if case == "mesh5_boost":
        return [(2 * u, v / 2) for u, v in points]
    if case in ("mesh5_dilate", "mesh5_dilate_wrong_density"):
        return [(2 * u, 2 * v) for u, v in points]
    if case == "mesh5_warp":
        return [(u * u, v * v) for u, v in points]
    return points


def endpoint_chains(relation):
    n = len(relation)
    paths = [1] + [0] * (n - 1)
    counts = []
    for _ in range(1, n):
        paths = [sum(paths[i] for i in range(n) if relation[i][j]) for j in range(n)]
        counts.append(paths[-1])
    return counts


def independently_check_order(order, density):
    n, relation = order["n"], order["relation"]
    assert len(relation) == n
    assert all(
        len(row) == n and all(type(x) is int and x in (0, 1) for x in row) for row in relation
    )
    assert all(not relation[i][j] for i in range(n) for j in range(i + 1))
    intervals = [
        [sum(relation[i][k] and relation[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]
    chain_pairs = [
        [
            sum(
                relation[i][a] and relation[a][b] and relation[b][j]
                for a in range(n)
                for b in range(a + 1, n)
            )
            for j in range(n)
        ]
        for i in range(n)
    ]
    assert order["interval_cardinality"] == intervals
    assert order["chain_pairs"] == chain_pairs
    assert all(not intervals[i][j] or relation[i][j] for i in range(n) for j in range(n))
    links = [
        [int(bool(relation[i][j]) and intervals[i][j] == 0) for j in range(n)] for i in range(n)
    ]
    assert order["links"] == links
    longest = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if relation[i][j]:
                longest[i][j] = 1 + max(
                    (longest[i][k] for k in range(i + 1, j) if relation[i][k] and relation[k][j]),
                    default=0,
                )
    assert order["longest_chain_edges"] == longest
    relations, link_count = sum(map(sum, relation)), sum(map(sum, links))
    assert order["summary"] == {
        "events": n,
        "relations": relations,
        "links": link_count,
        "incomparable": n * (n - 1) // 2 - relations,
        "minimal": sum(not any(relation[i][j] for i in range(n)) for j in range(n)),
        "maximal": sum(not any(row) for row in relation),
        "height": max(map(max, longest)) + 1,
    }
    expected = [
        [[F(relation[i][j], 2) for j in range(n)] for i in range(n)],
        [[-F(intervals[i][j], 4) / density for j in range(n)] for i in range(n)],
        [[F(chain_pairs[i][j], 8) / density**2 for j in range(n)] for i in range(n)],
    ]
    assert [rational_matrix(matrix) for matrix in order["kernel_coefficients"]] == expected
    counts = endpoint_chains(relation)
    assert order["endpoint"]["chain_counts"] == counts
    coefficients = [
        F((-1) ** (k - 1) * count, 2**k) / density ** (k - 1) for k, count in enumerate(counts, 1)
    ]
    assert list(map(F, order["endpoint"]["coefficients"])) == coefficients
    assert len(coefficients) == n - 1


@pytest.mark.parametrize("case", CASES)
def test_complete_dual_executor_outputs_agree(results, case):
    direct, reference = results[case]
    assert direct == reference
    assert json.loads(json.dumps(direct, allow_nan=False)) == direct


@pytest.mark.parametrize("case", CASES)
def test_all_pair_integer_counts_coefficient_matrices_and_chain_series(results, case):
    for result in results[case]:
        assert result["case"] == case
        assert str(F(result["density"])) == result["density"]
        assert F(result["density"]) > 0
        independently_check_order(result["order"], F(result["density"]))
        for matrix in result["order"]["kernel_coefficients"]:
            assert all(
                type(value) is str and str(F(value)) == value for row in matrix for value in row
            )
        assert all(str(F(value)) == value for value in result["order"]["endpoint"]["coefficients"])


@pytest.mark.parametrize("case", CASES)
def test_supplied_coordinates_and_exact_signed_geometry_errors(results, case):
    points = supplied_points(case)
    for result in results[case]:
        if points is None:
            assert result["coordinates"] is None and result["geometry"] is None
            continue
        assert result["coordinates"] == [[str(u), str(v)] for u, v in points]
        n = len(points)
        assert len({u for u, _ in points}) == len({v for _, v in points}) == n
        relation = [[int(a < c and b < d) for c, d in points] for a, b in points]
        assert result["order"]["relation"] == relation
        rows = result["geometry"]["pairs"]
        assert [(row["source"], row["target"]) for row in rows] == [
            (i, j) for i in range(n) for j in range(n) if relation[i][j]
        ]
        volume_errors, coefficient_errors = [], []
        rho = F(result["density"])
        for row in rows:
            i, j = row["source"], row["target"]
            du, dv = points[j][0] - points[i][0], points[j][1] - points[i][1]
            tau = du * dv
            assert tau > 0
            volume = tau / 2
            count_volume = F(result["order"]["interval_cardinality"][i][j]) / rho
            assert F(row["tau_squared"]) == tau
            assert F(row["volume"]) == volume
            assert F(row["count_volume"]) == count_volume
            assert F(row["volume_error"]) == count_volume - volume
            continuum = [F(1, 2), -tau / 8, tau**2 / 128]
            assert list(map(F, row["continuum_coefficients"])) == continuum
            actual = [F(matrix[i][j]) for matrix in result["order"]["kernel_coefficients"]]
            errors = [a - b for a, b in zip(actual, continuum)]
            assert list(map(F, row["coefficient_errors"])) == errors
            volume_errors.append(abs(count_volume - volume))
            coefficient_errors.append([abs(value) for value in errors])
        metrics = result["geometry"]["metrics"]
        assert metrics["timelike_pairs"] == len(rows)
        assert metrics["exact_volume_pairs"] == volume_errors.count(F(0))
        assert F(metrics["max_abs_volume_error"]) == max(volume_errors)
        assert F(metrics["mean_abs_volume_error"]) == sum(volume_errors) / len(rows)
        assert list(map(F, metrics["max_abs_coefficient_errors"])) == [
            max(row[k] for row in coefficient_errors) for k in range(3)
        ]


@pytest.mark.parametrize("m", (3, 5, 7))
def test_mesh_analytical_counts_and_calibration_are_not_local_reconstruction(results, m):
    for result in results[f"mesh{m}"]:
        assert result["order"]["n"] == m * m + 2
        assert F(result["density"]) == 2 * m * m
        counts = result["order"]["endpoint"]["chain_counts"]
        assert counts[:3] == [1, m * m, m * m * (m * m + 2 * m - 3) // 4]
        assert result["order"]["summary"]["height"] == 2 * m + 1
        assert list(map(F, result["order"]["endpoint"]["coefficients"][:3])) == [
            F(1, 2),
            -F(1, 8),
            F(m * m + 2 * m - 3, 128 * m * m),
        ]
        whole = probe_pair(result, "whole")
        assert F(whole["count_volume"]) == F(whole["volume"]) == F(1, 2)
        assert F(whole["volume_error"]) == 0
        assert F(whole["coefficient_errors"][2]) == F(2 * m - 3, 128 * m * m) > 0
        middle = probe_pair(result, "bottom_to_middle")
        assert F(middle["tau_squared"]) == F(1, 4)
        expected_count = ((m + 1) // 2) ** 2 - 1
        assert F(middle["count_volume"]) == F(expected_count, 2 * m * m)
        assert F(middle["volume_error"]) == F(expected_count, 2 * m * m) - F(1, 8) != 0


def test_mesh_third_coefficient_discrepancies_decrease_but_do_not_disappear(results):
    errors = [
        F(probe_pair(results[f"mesh{m}"][0], "whole")["coefficient_errors"][2]) for m in (3, 5, 7)
    ]
    assert errors[0] > errors[1] > errors[2] > 0


def test_boost_preserves_all_interval_and_order_diagnostics(results):
    for base, boost in zip(results["mesh5"], results["mesh5_boost"]):
        assert base["coordinates"] != boost["coordinates"]
        for key in ("density", "order", "geometry", "probes", "two_order"):
            assert base[key] == boost[key]


def test_correct_dilation_scales_geometry_density_and_coefficients_consistently(results):
    for base, dilated in zip(results["mesh5"], results["mesh5_dilate"]):
        assert F(dilated["density"]) == F(base["density"]) / 4
        for key in (
            "relation",
            "links",
            "interval_cardinality",
            "chain_pairs",
            "longest_chain_edges",
            "summary",
        ):
            assert base["order"][key] == dilated["order"][key]
        for power, (left, right) in enumerate(
            zip(base["order"]["kernel_coefficients"], dilated["order"]["kernel_coefficients"])
        ):
            assert rational_matrix(right) == [
                [4**power * value for value in row] for row in rational_matrix(left)
            ]
        for power, (left, right) in enumerate(
            zip(
                base["order"]["endpoint"]["coefficients"],
                dilated["order"]["endpoint"]["coefficients"],
            )
        ):
            assert F(right) == 4**power * F(left)
        for left, right in zip(base["geometry"]["pairs"], dilated["geometry"]["pairs"]):
            for key in ("tau_squared", "volume", "count_volume", "volume_error"):
                assert F(right[key]) == 4 * F(left[key])
            for key in ("continuum_coefficients", "coefficient_errors"):
                assert list(map(F, right[key])) == [
                    4**k * F(value) for k, value in enumerate(left[key])
                ]


def test_wrong_density_remains_a_calibration_error_not_an_automatic_correction(results):
    for base, wrong, dilated in zip(
        results["mesh5"], results["mesh5_dilate_wrong_density"], results["mesh5_dilate"]
    ):
        assert wrong["coordinates"] == dilated["coordinates"]
        assert wrong["density"] == base["density"] == "50"
        assert wrong["order"] == base["order"]
        whole = probe_pair(wrong, "whole")
        assert F(whole["count_volume"]) == F(1, 2)
        assert F(whole["volume"]) == 2
        assert F(whole["volume_error"]) == -F(3, 2)
        assert F(whole["coefficient_errors"][1]) == F(3, 8)
        assert wrong["geometry"] != dilated["geometry"]


def test_order_preserving_warp_changes_local_comparison_not_order_data(results):
    for base, warped in zip(results["mesh5"], results["mesh5_warp"]):
        assert warped["order"] == base["order"] and warped["density"] == base["density"]
        assert probe_pair(warped, "whole") == probe_pair(base, "whole")
        assert warped["geometry"]["pairs"] != base["geometry"]["pairs"]
        lower, upper = probe_pair(warped, "bottom_to_middle"), probe_pair(warped, "middle_to_top")
        assert F(lower["volume"]) == F(1, 32) and F(upper["volume"]) == F(9, 32)
        assert F(lower["count_volume"]) == F(upper["count_volume"]) == F(4, 25)
        assert F(lower["volume_error"]) == F(103, 800)
        assert F(upper["volume_error"]) == -F(97, 800)


def interior_relation(result):
    relation = result["order"]["relation"]
    return [[relation[i + 1][j + 1] for j in range(6)] for i in range(6)]


def linear_extensions_and_realizers(relation):
    n = len(relation)
    extensions, positions = [], []
    for perm in permutations(range(n)):
        rank = [perm.index(i) for i in range(n)]
        if all(not relation[i][j] or rank[i] < rank[j] for i in range(n) for j in range(n)):
            extensions.append(list(perm))
            positions.append(rank)
    realizers = []
    for left, left_rank in enumerate(positions):
        for right, right_rank in enumerate(positions):
            if all(
                bool(relation[i][j])
                == (left_rank[i] < left_rank[j] and right_rank[i] < right_rank[j])
                for i in range(n)
                for j in range(n)
            ):
                realizers.append([extensions[left], extensions[right]])
    return extensions, realizers


def test_endpoint_collision_does_not_certify_the_supplied_flat_geometry(results):
    for ferrers, standard in zip(results["ferrers6"], results["standard_example3"]):
        assert (
            ferrers["order"]["summary"]
            == standard["order"]["summary"]
            == {
                "events": 8,
                "relations": 19,
                "links": 12,
                "incomparable": 9,
                "minimal": 1,
                "maximal": 1,
                "height": 4,
            }
        )
        assert ferrers["order"]["endpoint"] == standard["order"]["endpoint"]
        assert ferrers["order"]["endpoint"]["chain_counts"] == [1, 6, 6, 0, 0, 0, 0]
        assert list(map(F, ferrers["order"]["endpoint"]["coefficients"])) == [
            F(1, 2),
            -F(1, 8),
            F(1, 192),
            F(0),
            F(0),
            F(0),
            F(0),
        ]
        assert ferrers["order"]["interval_cardinality"] != standard["order"]["interval_cardinality"]
        assert ferrers["geometry"] is not None
        assert standard["geometry"] is None and standard["coordinates"] is None


@pytest.mark.parametrize("case", ("ferrers6", "standard_example3"))
def test_exhaustive_two_order_realizers_match_independent_enumeration(results, case):
    for result in results[case]:
        relation = interior_relation(result)
        expected = [
            [
                int(i < 3 <= j and (i <= j - 3 if case == "ferrers6" else i != j - 3))
                for j in range(6)
            ]
            for i in range(6)
        ]
        assert relation == expected
        extensions, realizers = linear_extensions_and_realizers(relation)
        assert result["two_order"]["linear_extensions"] == extensions
        assert result["two_order"]["realizer_count"] == len(realizers)
        assert result["two_order"]["first_realizer"] == (realizers[0] if realizers else None)
        assert bool(realizers) is (case == "ferrers6")
        if case == "standard_example3":
            # Each order can reverse at most one missing matched a_i,b_i pair;
            # two orders therefore cannot reverse all three incomparable pairs.
            for extension in extensions:
                assert sum(extension.index(i + 3) < extension.index(i) for i in range(3)) <= 1


@pytest.mark.parametrize("case", ("ferrers6", "standard_example3"))
def test_six_interior_summaries_agree_without_probe_endpoint_counts(executors, results, case):
    relation = interior_relation(results[case][0])
    past = [[i for i in range(6) if relation[i][j]] for j in range(6)]
    for module in executors:
        order = module.order_analysis(past, F(12))
        assert order["summary"] == {
            "events": 6,
            "relations": 6,
            "links": 6,
            "incomparable": 9,
            "minimal": 3,
            "maximal": 3,
            "height": 2,
        }
        assert not any(any(row) for row in order["interval_cardinality"])


@pytest.mark.parametrize("case", CASES)
def test_designated_probes_and_absence_of_unrequested_realizer_search(results, case):
    for result in results[case]:
        n = result["order"]["n"]
        assert result["probes"][0] == {"name": "whole", "source": 0, "target": n - 1}
        if case.startswith("mesh"):
            assert [row["name"] for row in result["probes"]] == [
                "whole",
                "bottom_to_middle",
                "middle_to_top",
            ]
            assert result["two_order"] is None
        else:
            assert len(result["probes"]) == 1


VALID_HELPERS = [
    ([[]], F(1)),
    ([[], []], F(3, 2)),
    ([[], [0]], F(2)),
    ([[], [0], [0, 1]], F(1, 3)),
    ([[], [0], [0]], F(6)),
    ([[], [], [0, 1]], F(6)),
    ([[] for _ in range(51)], F(1)),
]


@pytest.mark.parametrize("past,density", VALID_HELPERS)
def test_bounded_helper_handles_singletons_zeros_chains_and_nonunique_endpoints(
    executors, past, density
):
    outputs = [module.order_analysis(copy.deepcopy(past), density) for module in executors]
    assert outputs[0] == outputs[1]
    for order in outputs:
        independently_check_order(order, density)
        assert order["relation"] == [
            [int(i in past[j]) for j in range(len(past))] for i in range(len(past))
        ]


def malformed_inputs():
    base = problem()
    return [
        None,
        [],
        True,
        False,
        "mesh3",
        {},
        {"case": "mesh3"},
        {"schema_version": base["schema_version"]},
        {**base, "density": "18"},
        {**base, "extra": 1},
        *({**base, "schema_version": value} for value in (None, True, False, 1, [], "wrong")),
        *(
            {**base, "case": value}
            for value in (None, True, False, 1, [], {}, "unknown", "mesh9", "")
        ),
    ]


@pytest.mark.parametrize("wire", malformed_inputs())
def test_strict_fixture_schema(executors, wire):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(copy.deepcopy(wire))


BAD_PASTS = [
    None,
    (),
    {},
    [],
    [0],
    [()],
    [None],
    [True],
    [[0]],
    [[-1]],
    [[], [1]],
    [[], [True]],
    [[], [False]],
    [[], [0.0]],
    [[], ["0"]],
    [[], [0, 0]],
    [[], [], [1, 0]],
    [[], [0], [1]],
    [[] for _ in range(52)],
]


@pytest.mark.parametrize("past", BAD_PASTS)
def test_helper_rejects_noncanonical_nontransitive_and_out_of_bound_orders(executors, past):
    for module in executors:
        with pytest.raises(ValueError):
            module.order_analysis(copy.deepcopy(past), F(1))


@pytest.mark.parametrize("density", (None, True, False, 1, 0, 0.5, "1", [], F(0), -F(1, 2)))
def test_helper_density_requires_a_positive_fraction(executors, density):
    for module in executors:
        with pytest.raises(ValueError):
            module.order_analysis([[], [0]], density)


@pytest.mark.parametrize(
    "density", (F(1 << 4097), F(1, 1 << 4097)), ids=("large_numerator", "large_denominator")
)
def test_retained_rational_component_guard_rejects_exact_overflow(executors, density):
    for module in executors:
        with pytest.raises(ValueError):
            module.order_analysis([[], [0], [0, 1], [0, 1, 2]], density)


def test_optimized_valid_execution_and_explicit_rejections(tmp_path):
    script = r"""
import importlib.util, json, sys
from fractions import Fraction
from pathlib import Path
root = Path(sys.argv[1])
valid = {"schema_version":"det8-qr05d-problem-v1", "case":"standard_example3"}
outputs = []
for number, filename in enumerate(("geometry.py", "reference_qr05d.py")):
    name = "_qr05d_optimized_test_" + str(number)
    spec = importlib.util.spec_from_file_location(name, root / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("executor unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    output = module.analyze(valid)
    if output["order"]["endpoint"]["chain_counts"] != [1,6,6,0,0,0,0]:
        raise RuntimeError("valid optimized scalar analysis differs")
    if output["two_order"]["realizer_count"] != 0 or output["geometry"] is not None:
        raise RuntimeError("abstract obstruction boundary differs")
    outputs.append(output)
    for bad in (True, {**valid,"extra":1}, {**valid,"case":True},
                {**valid,"schema_version":False}, {**valid,"case":"unknown"}):
        try:
            module.analyze(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("optimized fixture validation accepted invalid input")
    for past, density in (([],Fraction(1)), ([[],[False]],Fraction(1)),
                          ([[],[0],[1]],Fraction(1)), ([[],[0]],True),
                          ([[],[0]],Fraction(0))):
        try:
            module.order_analysis(past, density)
        except ValueError:
            pass
        else:
            raise RuntimeError("optimized helper validation accepted invalid input")
if outputs[0] != outputs[1]:
    raise RuntimeError("optimized implementations disagree")
print(json.dumps({"valid_routes":2,"explicit_rejections":20}))
"""
    completed = subprocess.run(
        [
            sys.executable,
            "-I",
            "-O",
            "-X",
            f"pycache_prefix={tmp_path / 'bytecode'}",
            "-c",
            script,
            str(HERE),
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
    )
    assert json.loads(completed.stdout) == {"valid_routes": 2, "explicit_rejections": 20}
