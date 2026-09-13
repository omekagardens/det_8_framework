"""Prospective analytical-Q oracle, boundary controls and evidence lifecycle.

No mathematical execution is permitted before the complete first source
freeze. The explicit base-Q table is independent of both implementations.
Tests load fresh engine modules only from authenticated snapshot bytes.
"""

import copy
import hashlib
import importlib.util
import json
import signal
import tempfile
import types
import unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
VARIANTS = ["identity", "cyclic", "reversal", "rescale"]
RATIONAL_FIELDS = ["mu", "k", "x", "f", "g", "q"]


def load_study():
    spec = importlib.util.spec_from_file_location(
        "measure_divergence_test_study", HERE / "study.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load source-bound measure/divergence driver")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def context():
    """One genuine complete two-route mathematical analysis per suite."""
    study = load_study()
    snapshot = study.source_snapshot()
    protocol = study._protocol(snapshot)
    original_load = study.load_engine

    def guarded_load(blob, name):
        engine = original_load(blob, name)
        original_analyze = engine.analyze

        def guarded_analyze():
            with mock.patch("builtins.open", side_effect=AssertionError("pure analysis I/O")):
                return original_analyze()

        engine.analyze = guarded_analyze
        return engine

    with mock.patch.object(study, "load_engine", side_effect=guarded_load):
        report = study.analyze(snapshot)
    return study, snapshot, protocol, report


def exact(test, actual, expected, path="report"):
    test.assertIs(type(actual), type(expected), path)
    if type(expected) is dict:
        test.assertEqual(set(actual), set(expected), path)
        for key in expected:
            exact(test, actual[key], expected[key], f"{path}.{key}")
    elif type(expected) is list:
        test.assertEqual(len(actual), len(expected), path)
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            exact(test, left, right, f"{path}[{index}]")
    else:
        test.assertIn(type(expected), (str, int, bool, F), path)
        test.assertEqual(actual, expected, path)


def vector(values):
    return [F(value) for value in values]


def matrix(rows):
    return [vector(row) for row in rows]


def zeros(n):
    return [F(0) for _ in range(n)]


def diagonal(values):
    return [
        [value if i == j else F(0) for j in range(len(values))] for i, value in enumerate(values)
    ]


def action(A, v):
    return [sum((entry * value for entry, value in zip(row, v, strict=True)), F(0)) for row in A]


def cyclic_vector(values):
    return values[-1:] + values[:-1]


def cyclic_matrix(A):
    n = len(A)
    return [[A[(i - 1) % n][(j - 1) % n] for j in range(n)] for i in range(n)]


def scale_vector(v, factor):
    return [factor * value for value in v]


def scale_matrix(A, factor):
    return [scale_vector(row, factor) for row in A]


def mutable_ids(value):
    result = set()
    if type(value) in (list, dict):
        result.add(id(value))
        children = value.values() if type(value) is dict else value
        for child in children:
            result.update(mutable_ids(child))
    return result


def base_cases():
    """Explicit closed-form Q table, not an incidence or neighbor construction."""
    single = matrix([[0]])
    unequal = matrix([[-1, 1], [F(1, 2), F(-1, 2)]])
    disconnected = matrix([[-1, 1, 0], [F(1, 2), F(-1, 2), 0], [0, 0, 0]])
    arithmetic = matrix([[F(-3, 2), F(3, 2), 0], [F(3, 2), F(-5, 2), 1], [0, 1, -1]])
    pointwise = matrix([[-2, 2, 0], [1, -2, 1], [0, 1, -1]])
    specifications = [
        ("singleton_closed", [1], [], [0], "closed", [0], [], [2], [], [0], single),
        ("unequal_closed", [1, 2], [1], [0, 1], "closed", [0, 1], [], [0, 1], [], [0, 0], unequal),
        (
            "zero_edge_closed",
            [1, 2, 1],
            [1, 0],
            [0, 1, 2],
            "closed",
            [0, 1, 2],
            [],
            [0, 1, 2],
            [],
            [0, 0, 0],
            disconnected,
        ),
        (
            "arithmetic_face_closed",
            [1, 1, 1],
            [F(3, 2), 1],
            [-1, 0, 1],
            "closed",
            [0, 1, 2],
            [],
            [0, 1, 0],
            [],
            [0, 0, 0],
            arithmetic,
        ),
        (
            "pointwise_reweighted",
            [F(1, 2), 1, 1],
            [1, 1],
            [-1, 0, 1],
            "closed",
            [0, 1, 2],
            [],
            [0, 1, 0],
            [],
            [0, 0, 0],
            pointwise,
        ),
        ("prescribed_flux", [1, 2], [1], [0, 1], "flux", [0, 1], [], [1, 2], [], [2, -2], unequal),
        (
            "dirichlet_grounded",
            [1, 1, 1],
            [F(3, 2), 1],
            [-1, 0, 1],
            "dirichlet",
            [1],
            [0, 2],
            [1],
            [0, 0],
            [0, 0, 0],
            arithmetic,
        ),
        (
            "dirichlet_driven",
            [1, 1, 1],
            [F(3, 2), 1],
            [-1, 0, 1],
            "dirichlet",
            [1],
            [0, 2],
            [F(1, 2)],
            [1, 1],
            [0, 0, 0],
            arithmetic,
        ),
        (
            "dirichlet_unanchored",
            [1, 2, 1],
            [1, 0],
            [0, 1, 2],
            "dirichlet",
            [1, 2],
            [0],
            [1, 2],
            [0],
            [0, 0, 0],
            disconnected,
        ),
    ]
    result = []
    for name, mu, k, x, mode, I, D, f, g, q, Q in specifications:
        world = {
            "mu": vector(mu),
            "edges": [[i, i + 1] for i in range(len(mu) - 1)],
            "k": vector(k),
            "x": vector(x),
            "mode": mode,
            "I": list(I),
            "D": list(D),
            "f": vector(f),
            "g": vector(g),
            "q": vector(q),
        }
        result.append((name, world, copy.deepcopy(Q)))
    return result


def variant_world(world, variant):
    result = copy.deepcopy(world)
    n = len(world["mu"])
    if variant == "cyclic":
        for key in ("mu", "x", "q"):
            result[key] = cyclic_vector(world[key])
        result["edges"] = [[(tail + 1) % n, (head + 1) % n] for tail, head in world["edges"]]
        if world["mode"] == "dirichlet":
            for key in ("I", "D"):
                result[key] = [(node + 1) % n for node in world[key]]
        else:
            result["f"] = cyclic_vector(world["f"])
    elif variant == "reversal":
        result["edges"] = [[head, tail] for tail, head in world["edges"]]
    elif variant == "rescale":
        for key in ("mu", "k", "q"):
            result[key] = scale_vector(world[key], F(3, 2))
    return result


def components(Q, nodes):
    """Connectivity from the independently declared matrix, not supplied edges."""
    remaining = set(nodes)
    result = []
    while remaining:
        reached = {min(remaining)}
        frontier = set(reached)
        while frontier:
            adjacent = {
                j for i in frontier for j in remaining if Q[i][j] > 0 or Q[j][i] > 0
            } - reached
            reached.update(adjacent)
            frontier = adjacent
        result.append(sorted(reached))
        remaining.difference_update(reached)
    return result


def moment_data(Q, x):
    n = len(Q)
    return {
        "m0": [sum(row, F(0)) for row in Q],
        "m1": [sum((Q[i][j] * (x[j] - x[i]) for j in range(n)), F(0)) for i in range(n)],
        "m2": [sum((Q[i][j] * (x[j] - x[i]) ** 2 for j in range(n)), F(0)) / 2 for i in range(n)],
        "Q1": action(Q, [F(1)] * n),
        "Qx": action(Q, x),
        "Qx2": action(Q, [value**2 for value in x]),
    }


def adjoint_residual(Q, mu):
    return [[mu[i] * Q[i][j] - Q[j][i] * mu[j] for j in range(len(Q))] for i in range(len(Q))]


def oracle_row(world, Q):
    """Complete native expected report around a supplied analytical Q."""
    mu, edges, k, x = (world[key] for key in ("mu", "edges", "k", "x"))
    I, D, f, g, q = (world[key] for key in ("I", "D", "f", "g", "q"))
    n = len(mu)
    B = [[F(int(i == head) - int(i == tail)) for i in range(n)] for tail, head in edges]
    L = [[-mu[i] * Q[i][j] for j in range(n)] for i in range(n)]
    full = {
        **moment_data(Q, x),
        "counting_columns": [sum((Q[i][j] for i in range(n)), F(0)) for j in range(n)],
        "weighted_columns": [sum((mu[i] * Q[i][j] for i in range(n)), F(0)) for j in range(n)],
        "adjoint_residual": adjoint_residual(Q, mu),
        "energy_form": copy.deepcopy(L),
    }
    field = zeros(n)
    for node, value in zip(I, f, strict=True):
        field[node] = value
    for node, value in zip(D, g, strict=True):
        field[node] = value
    gradient = [field[head] - field[tail] for tail, head in edges]
    J = [-weight * difference for weight, difference in zip(k, gradient, strict=True)]
    influx = zeros(n)
    for (tail, head), flow in zip(edges, J, strict=True):
        influx[tail] -= flow
        influx[head] += flow
    outward = [sum((mu[i] * Q[i][a] * (field[i] - field[a]) for a in D), F(0)) for i in I]
    flux = {
        "field": field,
        "gradient": gradient,
        "J": J,
        "influx": influx,
        "Qf": action(Q, field),
        "dirichlet_outward": outward,
    }
    full_components = components(Q, range(n))
    kernel = [[F(int(i in group)) for i in range(n)] for group in full_components]
    anchors = {i: group[0] for group in full_components for i in group}
    # Independent expected values use the known supplied measures. The engine
    # must reconstruct them from Q; ratio identities are checked separately.
    normalized_mu = [mu[i] / mu[anchors[i]] for i in range(n)]
    normalized_k = [weight / mu[anchors[tail]] for (tail, _), weight in zip(edges, k, strict=True)]
    reconstruction = {
        "mu_normalized": normalized_mu,
        "k_normalized": normalized_k,
        "detailed_balance": adjoint_residual(Q, normalized_mu),
        "mu_residual": [normalized_mu[i] - mu[i] / mu[anchors[i]] for i in range(n)],
        "k_residual": [
            value - weight / mu[anchors[tail]]
            for value, (tail, _), weight in zip(normalized_k, edges, k, strict=True)
        ],
    }
    reduced_Q = [[Q[i][j] for j in I] for i in I]
    active_mu = [mu[i] for i in I]
    source = [sum((Q[i][a] * field[a] for a in D), F(0)) - q[i] / mu[i] for i in I]
    derivative = [
        value + forcing for value, forcing in zip(action(reduced_Q, f), source, strict=True)
    ]
    interior_components = components(Q, I)
    anchored = [any(Q[i][a] > 0 for i in group for a in D) for group in interior_components]
    reduced_kernel = [
        [F(int(i in group)) for i in I]
        for group, attached in zip(interior_components, anchored, strict=True)
        if not attached
    ]
    reduced = {
        "nodes": list(I),
        "W": diagonal(active_mu),
        "Q": reduced_Q,
        "adjoint_residual": adjoint_residual(reduced_Q, active_mu),
        **moment_data(reduced_Q, [x[i] for i in I]),
        "source": source,
        "fdot": derivative,
        "constant_balance": [
            sum((Q[i][j] for j in I), F(0)) + sum((Q[i][a] for a in D), F(0)) - q[i] / mu[i]
            for i in I
        ],
        "components": interior_components,
        "anchored": anchored,
        "kernel_basis": reduced_kernel,
        "kernel_images": [action(reduced_Q, v) for v in reduced_kernel],
        "invertible": all(anchored),
    }
    internal = sum(
        (
            weight * (field[head] - field[tail]) ** 2
            for (tail, head), weight in zip(edges, k, strict=True)
            if tail in I and head in I
        ),
        F(0),
    )
    external = sum((field[i] * q[i] for i in I), F(0))
    reservoir = sum((field[i] * flow for i, flow in zip(I, outward, strict=True)), F(0))
    balances = {
        "mass": sum((mu[i] * field[i] for i in I), F(0)),
        "energy": sum((mu[i] * field[i] ** 2 for i in I), F(0)) / 2,
        "mass_rate": sum((mu[i] * value for i, value in zip(I, derivative, strict=True)), F(0)),
        "energy_rate": sum(
            (mu[i] * field[i] * value for i, value in zip(I, derivative, strict=True)), F(0)
        ),
        "mass_rhs": -sum((q[i] for i in I), F(0)) - sum(outward, F(0)),
        "energy_rhs": -internal - external - reservoir,
        "internal_dissipation": internal,
        "external_work": external,
        "reservoir_work": reservoir,
        "ordinary_rate": sum(derivative, F(0)),
    }
    return {
        "world": copy.deepcopy(world),
        "B": B,
        "W": diagonal(mu),
        "K": diagonal(k),
        "L": L,
        "Q": copy.deepcopy(Q),
        "full": full,
        "flux": flux,
        "components": full_components,
        "kernel_basis": kernel,
        "kernel_images": [action(Q, v) for v in kernel],
        "reconstruction": reconstruction,
        "reduced": reduced,
        "balances": balances,
    }


@lru_cache(maxsize=1)
def full_oracle():
    rows = []
    witnesses = []
    for name, world, Q in base_cases():
        for variant in VARIANTS:
            rows.append(
                {
                    "id": name + ":" + variant,
                    "base": name,
                    "variant": variant,
                    **oracle_row(
                        variant_world(world, variant),
                        cyclic_matrix(Q) if variant == "cyclic" else Q,
                    ),
                }
            )
        witnesses.append(
            {
                "base": name,
                "rows": [name + ":identity", name + ":rescale"],
                "Q": copy.deepcopy(Q),
                "measures": [list(world["mu"]), scale_vector(world["mu"], F(3, 2))],
                "conductances": [list(world["k"]), scale_vector(world["k"], F(3, 2))],
            }
        )
    return {"schema": "qr05-measure-divergence-report-v1", "rows": rows, "witnesses": witnesses}


def exact_rank(A):
    """Small exact elimination independently checks the reported kernel size."""
    rows = copy.deepcopy(A)
    position = 0
    for column in range(len(A)):
        pivot = next((i for i in range(position, len(A)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[position], rows[pivot] = rows[pivot], rows[position]
        divisor = rows[position][column]
        rows[position] = [value / divisor for value in rows[position]]
        for i in range(position + 1, len(A)):
            coefficient = rows[i][column]
            rows[i] = [
                left - coefficient * right
                for left, right in zip(rows[i], rows[position], strict=True)
            ]
        position += 1
    return position


class MeasureDivergenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.snapshot, cls.protocol, cls.report = context()

    def engines(self):
        for name in ("primary.py", "reference.py"):
            yield name, self.study.load_engine(self.snapshot[name], name)

    def test_complete_independent_native_report_and_codec(self):
        exact(self, self.report, full_oracle())
        exact(
            self,
            self.study.decode(
                self.study.strict_loads(self.study.canonical(self.study.encode(self.report)))
            ),
            self.report,
        )

    def test_literal_case_worlds_protocol_and_fixed_order(self):
        cases = base_cases()
        self.assertEqual(len(self.protocol["cases"]), 9)
        exact(self, self.protocol["variants"], VARIANTS)
        exact(self, self.protocol["scale_multiplier"], [3, 2])
        for supplied, (name, world, _) in zip(self.protocol["cases"], cases, strict=True):
            raw = copy.deepcopy(world)
            for key in RATIONAL_FIELDS:
                raw[key] = [[value.numerator, value.denominator] for value in world[key]]
            exact(self, supplied, {"id": name, "world": raw})
        self.assertEqual(
            [row["id"] for row in self.report["rows"]],
            [name + ":" + variant for name, _, _ in cases for variant in VARIANTS],
        )

    def test_full_and_effective_census_without_boundary_control_rows(self):
        rows = self.report["rows"]
        actual = {
            "rows": len(rows),
            "event_occurrences": sum(len(row["Q"]) for row in rows),
            "edges": sum(len(row["world"]["edges"]) for row in rows),
            "matrix_cells": sum(len(row["Q"]) ** 2 for row in rows),
            "dynamic_occurrences": sum(len(row["reduced"]["nodes"]) for row in rows),
            "effective_matrix_cells": sum(len(row["reduced"]["Q"]) ** 2 for row in rows),
            "witnesses": len(self.report["witnesses"]),
        }
        expected = {
            "rows": 36,
            "event_occurrences": 92,
            "edges": 56,
            "matrix_cells": 252,
            "dynamic_occurrences": 72,
            "effective_matrix_cells": 168,
            "witnesses": 9,
        }
        exact(self, actual, expected)
        exact(self, self.protocol["coverage"], expected)

    def test_weighted_incidence_adjoint_conservation_and_energy_form(self):
        for row in self.report["rows"]:
            world, Q = row["world"], row["Q"]
            n, B, k, mu = len(Q), row["B"], world["k"], world["mu"]
            outer_sum = [
                [
                    sum(
                        (weight * edge[i] * edge[j] for weight, edge in zip(k, B, strict=True)),
                        F(0),
                    )
                    for j in range(n)
                ]
                for i in range(n)
            ]
            exact(self, row["L"], outer_sum)
            exact(self, row["full"]["energy_form"], outer_sum)
            exact(self, row["full"]["weighted_columns"], zeros(n))
            exact(self, row["full"]["Q1"], zeros(n))
            exact(self, row["full"]["adjoint_residual"], [zeros(n) for _ in range(n)])
            self.assertTrue(all(Q[i][j] >= 0 for i in range(n) for j in range(n) if i != j))
            u, v = world["x"], row["flux"]["field"]
            lhs = sum((u[i] * mu[i] * value for i, value in enumerate(action(Q, v))), F(0))
            rhs = -sum(
                (
                    weight * left * right
                    for weight, left, right in zip(k, action(B, u), action(B, v), strict=True)
                ),
                F(0),
            )
            exact(self, lhs, rhs)

    def test_full_and_reduced_half_moment_polynomial_identities(self):
        for row in self.report["rows"]:
            for data, Q, x in (
                (row["full"], row["Q"], row["world"]["x"]),
                (
                    row["reduced"],
                    row["reduced"]["Q"],
                    [row["world"]["x"][i] for i in row["reduced"]["nodes"]],
                ),
            ):
                for key, value in moment_data(Q, x).items():
                    exact(self, data[key], value)
                exact(
                    self,
                    data["Qx"],
                    [xi * m0 + m1 for xi, m0, m1 in zip(x, data["m0"], data["m1"], strict=True)],
                )
                exact(
                    self,
                    data["Qx2"],
                    [
                        xi**2 * m0 + 2 * xi * m1 + 2 * m2
                        for xi, m0, m1, m2 in zip(
                            x, data["m0"], data["m1"], data["m2"], strict=True
                        )
                    ],
                )
                polynomial = [F(2) - xi + F(3) * xi**2 for xi in x]
                expected = [
                    m0 * p + m1 * (-1 + 6 * xi) + 6 * m2
                    for xi, p, m0, m1, m2 in zip(
                        x, polynomial, data["m0"], data["m1"], data["m2"], strict=True
                    )
                ]
                exact(self, action(Q, polynomial), expected)

    def test_actual_arithmetic_moments_and_different_pointwise_measure(self):
        rows = {row["id"]: row for row in self.report["rows"]}
        arithmetic, pointwise = (
            rows["arithmetic_face_closed:identity"],
            rows["pointwise_reweighted:identity"],
        )
        exact(self, arithmetic["full"]["m1"], vector([F(3, 2), F(-1, 2), -1]))
        exact(self, arithmetic["full"]["m2"], vector([F(3, 4), F(5, 4), F(1, 2)]))
        exact(self, pointwise["full"]["m1"], vector([2, 0, -1]))
        exact(self, pointwise["full"]["m2"], vector([1, 1, F(1, 2)]))
        exact(self, pointwise["full"]["counting_columns"], vector([-1, 1, 0]))
        exact(self, pointwise["full"]["weighted_columns"], zeros(3))
        self.assertNotEqual(arithmetic["W"], pointwise["W"])
        self.assertNotEqual(arithmetic["Q"], pointwise["Q"])
        self.assertNotEqual(arithmetic["full"]["m2"][1], F(1))

    def test_all_nine_analytical_boundary_derivatives(self):
        expected = [
            ([0], 0, 0),
            ([1, F(-1, 2)], 0, -1),
            ([1, F(-1, 2), 0], 0, -1),
            ([F(3, 2), F(-5, 2), 1], 0, F(-5, 2)),
            ([2, -2, 1], 0, -2),
            ([-1, F(1, 2)], 0, 1),
            ([F(-5, 2)], F(-5, 2), F(-5, 2)),
            ([F(5, 4)], F(5, 4), F(5, 8)),
            ([F(-1, 2), 0], -1, -1),
        ]
        rows = {row["id"]: row for row in self.report["rows"]}
        for (name, _, _), (derivative, mass, energy) in zip(base_cases(), expected, strict=True):
            row = rows[name + ":identity"]
            exact(self, row["reduced"]["fdot"], vector(derivative))
            exact(self, row["balances"]["mass_rate"], F(mass))
            exact(self, row["balances"]["energy_rate"], F(energy))

    def test_all_flux_and_mass_energy_balances(self):
        for row in self.report["rows"]:
            world, flux, reduced, balances = (
                row["world"],
                row["flux"],
                row["reduced"],
                row["balances"],
            )
            exact(self, flux["Qf"], action(row["Q"], flux["field"]))
            exact(
                self,
                flux["influx"],
                [mu * value for mu, value in zip(world["mu"], flux["Qf"], strict=True)],
            )
            exact(
                self,
                reduced["fdot"],
                [flux["Qf"][i] - world["q"][i] / world["mu"][i] for i in world["I"]],
            )
            exact(self, balances["mass_rate"], balances["mass_rhs"])
            exact(self, balances["energy_rate"], balances["energy_rhs"])
            self.assertGreaterEqual(balances["internal_dissipation"], 0)
            if world["mode"] == "closed":
                exact(self, balances["mass_rate"], F(0))
                self.assertLessEqual(balances["energy_rate"], 0)
            elif world["mode"] == "flux":
                self.assertGreater(balances["energy_rate"], 0)
                self.assertNotEqual(reduced["constant_balance"], zeros(len(world["I"])))
        unequal = next(row for row in self.report["rows"] if row["id"] == "unequal_closed:identity")
        exact(self, unequal["balances"]["ordinary_rate"], F(1, 2))
        exact(self, unequal["balances"]["mass_rate"], F(0))

    def test_component_kernel_grounding_and_reduced_zeroth_moments(self):
        for row in self.report["rows"]:
            n = len(row["Q"])
            self.assertEqual(len(row["kernel_basis"]), n - exact_rank(row["Q"]))
            for basis, value in zip(row["kernel_basis"], row["kernel_images"], strict=True):
                exact(self, value, action(row["Q"], basis))
                exact(self, value, zeros(n))
            reduced = row["reduced"]
            size = len(reduced["nodes"])
            rank = exact_rank(reduced["Q"])
            self.assertEqual(len(reduced["kernel_basis"]), size - rank)
            self.assertIs(reduced["invertible"], rank == size)
            self.assertIs(reduced["invertible"], all(reduced["anchored"]))
            for basis, value in zip(reduced["kernel_basis"], reduced["kernel_images"], strict=True):
                exact(self, value, action(reduced["Q"], basis))
                exact(self, value, zeros(size))
            if row["world"]["mode"] == "dirichlet":
                self.assertNotEqual(reduced["m0"], zeros(size))
                exact(self, reduced["constant_balance"], zeros(size))
        rows = {row["id"]: row for row in self.report["rows"]}
        exact(
            self,
            rows["dirichlet_unanchored:identity"]["reduced"]["Q"],
            matrix([[F(-1, 2), 0], [0, 0]]),
        )
        exact(self, rows["dirichlet_grounded:identity"]["reduced"]["m0"], vector([F(-5, 2)]))
        exact(self, rows["zero_edge_closed:identity"]["components"], [[0, 1], [2]])

    def test_relative_measure_ratios_conductances_and_component_anchors(self):
        for row in self.report["rows"]:
            Q, reconstruction = row["Q"], row["reconstruction"]
            muhat = reconstruction["mu_normalized"]
            for group in row["components"]:
                exact(self, muhat[group[0]], F(1))
                for i in group:
                    for j in group:
                        if i != j and Q[i][j] > 0:
                            exact(self, muhat[j] / muhat[i], Q[i][j] / Q[j][i])
            exact(
                self,
                reconstruction["k_normalized"],
                [muhat[tail] * Q[tail][head] for tail, head in row["world"]["edges"]],
            )
            exact(self, reconstruction["detailed_balance"], [zeros(len(Q)) for _ in Q])
            exact(self, reconstruction["mu_residual"], zeros(len(Q)))
            exact(self, reconstruction["k_residual"], zeros(len(row["world"]["edges"])))
        rows = {row["id"]: row for row in self.report["rows"]}
        exact(
            self,
            rows["unequal_closed:cyclic"]["reconstruction"]["mu_normalized"],
            vector([1, F(1, 2)]),
        )
        exact(
            self,
            rows["pointwise_reweighted:identity"]["reconstruction"]["k_normalized"],
            vector([2, 2]),
        )
        exact(
            self,
            rows["pointwise_reweighted:cyclic"]["reconstruction"]["k_normalized"],
            vector([1, 1]),
        )

    def test_cyclic_full_and_transport_order_and_anchor_renormalization(self):
        rows = {row["id"]: row for row in self.report["rows"]}
        for base, _, _ in base_cases():
            old, new = rows[base + ":identity"], rows[base + ":cyclic"]
            n = len(old["Q"])
            exact(self, new["world"], variant_world(old["world"], "cyclic"))
            for key in ("W", "L", "Q"):
                exact(self, new[key], cyclic_matrix(old[key]))
            exact(self, new["B"], [cyclic_vector(row) for row in old["B"]])
            exact(self, new["K"], old["K"])
            for key in (
                "m0",
                "m1",
                "m2",
                "Q1",
                "Qx",
                "Qx2",
                "counting_columns",
                "weighted_columns",
            ):
                exact(self, new["full"][key], cyclic_vector(old["full"][key]))
            for key in ("adjoint_residual", "energy_form"):
                exact(self, new["full"][key], cyclic_matrix(old["full"][key]))
            for key in ("field", "influx", "Qf"):
                exact(self, new["flux"][key], cyclic_vector(old["flux"][key]))
            for key in ("gradient", "J"):
                exact(self, new["flux"][key], old["flux"][key])
            is_dirichlet = old["world"]["mode"] == "dirichlet"
            for key in ("W", "Q", "adjoint_residual"):
                exact(
                    self,
                    new["reduced"][key],
                    old["reduced"][key] if is_dirichlet else cyclic_matrix(old["reduced"][key]),
                )
            for key in ("m0", "m1", "m2", "Q1", "Qx", "Qx2", "source", "fdot", "constant_balance"):
                exact(
                    self,
                    new["reduced"][key],
                    old["reduced"][key] if is_dirichlet else cyclic_vector(old["reduced"][key]),
                )
            exact(self, new["balances"], old["balances"])
            oldhat, newhat = (
                old["reconstruction"]["mu_normalized"],
                new["reconstruction"]["mu_normalized"],
            )
            for group in old["components"]:
                old_anchor_after = min(group, key=lambda node: (node + 1) % n)
                factor = oldhat[old_anchor_after]
                for i in group:
                    exact(self, newhat[(i + 1) % n], oldhat[i] / factor)
                for edge_index, (tail, _) in enumerate(old["world"]["edges"]):
                    if tail in group:
                        exact(
                            self,
                            new["reconstruction"]["k_normalized"][edge_index],
                            old["reconstruction"]["k_normalized"][edge_index] / factor,
                        )

    def test_edge_orientation_is_gauge_not_causal_reversal(self):
        rows = {row["id"]: row for row in self.report["rows"]}
        for base, _, _ in base_cases():
            old, new = rows[base + ":identity"], rows[base + ":reversal"]
            exact(self, new["world"], variant_world(old["world"], "reversal"))
            exact(self, new["B"], scale_matrix(old["B"], F(-1)))
            for key in ("gradient", "J"):
                exact(self, new["flux"][key], scale_vector(old["flux"][key], F(-1)))
            for key in ("field", "influx", "Qf", "dirichlet_outward"):
                exact(self, new["flux"][key], old["flux"][key])
            for key in (
                "W",
                "K",
                "L",
                "Q",
                "full",
                "components",
                "kernel_basis",
                "kernel_images",
                "reconstruction",
                "reduced",
                "balances",
            ):
                exact(self, new[key], old[key])

    def test_joint_scaling_includes_outward_flux_and_affine_boundary_terms(self):
        rows = {row["id"]: row for row in self.report["rows"]}
        factor = F(3, 2)
        for base, _, _ in base_cases():
            old, new = rows[base + ":identity"], rows[base + ":rescale"]
            exact(self, new["world"], variant_world(old["world"], "rescale"))
            for key in ("W", "K", "L"):
                exact(self, new[key], scale_matrix(old[key], factor))
            for key in ("B", "Q", "components", "kernel_basis", "kernel_images", "reconstruction"):
                exact(self, new[key], old[key])
            for key in ("J", "influx", "dirichlet_outward"):
                exact(self, new["flux"][key], scale_vector(old["flux"][key], factor))
            for key in ("field", "gradient", "Qf"):
                exact(self, new["flux"][key], old["flux"][key])
            for key, value in old["full"].items():
                wanted = (
                    scale_matrix(value, factor)
                    if key in ("adjoint_residual", "energy_form")
                    else scale_vector(value, factor)
                    if key == "weighted_columns"
                    else value
                )
                exact(self, new["full"][key], wanted)
            for key, value in old["reduced"].items():
                exact(
                    self,
                    new["reduced"][key],
                    scale_matrix(value, factor) if key in ("W", "adjoint_residual") else value,
                )
            for key, value in old["balances"].items():
                exact(
                    self, new["balances"][key], value if key == "ordinary_rate" else factor * value
                )

    def test_all_nine_same_Q_different_measure_witnesses(self):
        exact(self, self.report["witnesses"], full_oracle()["witnesses"])
        rows = {row["id"]: row for row in self.report["rows"]}
        for witness in self.report["witnesses"]:
            left, right = [rows[name] for name in witness["rows"]]
            exact(self, witness["Q"], left["Q"])
            exact(self, witness["Q"], right["Q"])
            exact(self, witness["measures"], [left["world"]["mu"], right["world"]["mu"]])
            exact(self, witness["conductances"], [left["world"]["k"], right["world"]["k"]])
            self.assertNotEqual(witness["measures"][0], witness["measures"][1])

    def test_fresh_pure_evaluate_all_fixed_worlds(self):
        for name, engine in self.engines():
            for expected in full_oracle()["rows"]:
                supplied = copy.deepcopy(expected["world"])
                original = copy.deepcopy(supplied)
                with self.subTest(engine=name, row=expected["id"]):
                    with mock.patch(
                        "builtins.open", side_effect=AssertionError("pure evaluator I/O")
                    ):
                        actual = engine.evaluate(supplied)
                    exact(
                        self,
                        actual,
                        {
                            key: value
                            for key, value in expected.items()
                            if key not in ("id", "base", "variant")
                        },
                    )
                    exact(self, supplied, original)
                    self.assertFalse(mutable_ids(supplied) & mutable_ids(actual))

    def test_named_triangle_constant_reservoir_and_net_outflow_controls(self):
        triangle = copy.deepcopy(base_cases()[3][1])
        triangle.update(
            {
                "mu": vector([1, 1, 1]),
                "edges": [[0, 1], [1, 2], [2, 0]],
                "k": vector([1, 1, 1]),
                "x": vector([0, 1, 2]),
                "f": vector([0, 1, 0]),
            }
        )
        triangle_Q = matrix([[-2, 1, 1], [1, -2, 1], [1, 1, -2]])
        constant = copy.deepcopy(base_cases()[6][1])
        constant["f"], constant["g"] = vector([1]), vector([1, 1])
        outflow = copy.deepcopy(base_cases()[5][1])
        outflow["q"] = vector([1, 0])
        for name, engine in self.engines():
            with self.subTest(engine=name):
                exact(self, engine.evaluate(triangle), oracle_row(triangle, triangle_Q))
                held = engine.evaluate(constant)
                exact(self, held, oracle_row(constant, base_cases()[6][2]))
                exact(self, held["reduced"]["fdot"], vector([0]))
                exact(self, held["reduced"]["m0"], vector([F(-5, 2)]))
                flowing = engine.evaluate(outflow)
                exact(self, flowing, oracle_row(outflow, base_cases()[5][2]))
                exact(self, flowing["reduced"]["fdot"], vector([0, F(-1, 2)]))
                exact(self, flowing["balances"]["mass_rate"], F(-1))
                exact(self, flowing["balances"]["energy_rate"], F(-2))

    def test_strict_container_and_rational_input_refusals(self):
        class DictSubclass(dict):
            pass

        class ListSubclass(list):
            pass

        class FractionSubclass(F):
            pass

        class StringSubclass(str):
            pass

        world = copy.deepcopy(base_cases()[1][1])
        bad = [None, [], DictSubclass(world), {**world, "extra": 0}]
        bad.extend(
            {key: value for key, value in world.items() if key != omitted} for omitted in world
        )
        for key, value in world.items():
            if type(value) is list:
                for changed in (None, tuple(value), ListSubclass(value)):
                    bad.append({**world, key: changed})
        for key in RATIONAL_FIELDS:
            source = copy.deepcopy(base_cases()[6][1] if key == "g" else world)
            for value in (0, True, 0.0, FractionSubclass(0), F(2**128), F(-(2**128)), F(1, 2**128)):
                changed = copy.deepcopy(source)
                changed[key][0] = value
                bad.append(changed)
        for value in (None, True, 1, "unknown", StringSubclass("closed")):
            bad.append({**world, "mode": value})
        for key, values in (("mu", (F(0), F(-1))), ("k", (F(-1),))):
            for value in values:
                changed = copy.deepcopy(world)
                changed[key][0] = value
                bad.append(changed)
        for key in RATIONAL_FIELDS:
            bad.append({**world, key: world[key] + [F(0)]})
        bad.append({**world, "mu": []})
        bad.append({**world, "mu": [F(1)] * 4})
        for name, engine in self.engines():
            for changed in bad:
                with (
                    self.subTest(engine=name, value=repr(changed)[:160]),
                    self.assertRaises(ValueError),
                ):
                    engine.evaluate(changed)

    def test_edge_labels_undirected_duplicates_and_partition_refusals(self):
        class IntSubclass(int):
            pass

        class ListSubclass(list):
            pass

        pair = copy.deepcopy(base_cases()[1][1])
        bad = []
        for edges in (
            [()],
            [[0]],
            [[0, 1, 0]],
            [ListSubclass([0, 1])],
            [[0, 0]],
            [[-1, 1]],
            [[0, 2]],
            [[True, 1]],
            [[F(0), 1]],
            [[0.0, 1]],
            [[IntSubclass(0), 1]],
            [[0, 1], [0, 1]],
            [[0, 1], [1, 0]],
        ):
            bad.append({**pair, "edges": edges, "k": [F(1)] * len(edges)})
        for I, D in (
            ([0, 0], []),
            ([0], []),
            ([0, 1], [1]),
            ([0, 2], []),
            ([1, 0], []),
            ([True, 1], []),
            ([F(0), 1], []),
            ([IntSubclass(0), 1], []),
            ([0], [1]),
        ):
            bad.append({**pair, "I": I, "D": D, "f": [F(1)] * len(I), "g": [F(1)] * len(D)})
        bad.append({**pair, "q": vector([1, 0])})
        held = copy.deepcopy(base_cases()[6][1])
        for I, D in (
            ([], [0, 1, 2]),
            ([0, 1, 2], []),
            ([1], [0, 0]),
            ([1], [0]),
            ([1], [0, 1]),
            ([1], [True, 2]),
            ([1], [0, 3]),
        ):
            bad.append({**held, "I": I, "D": D, "f": [F(1)] * len(I), "g": [F(1)] * len(D)})
        bad.append({**held, "q": vector([1, 0, 0])})
        bad.append({**held, "f": []})
        bad.append({**held, "g": vector([0])})
        bad.append({**pair, "mode": "flux", "I": [1, 0]})
        for name, engine in self.engines():
            for changed in bad:
                original = copy.deepcopy(changed)
                with (
                    self.subTest(engine=name, value=repr(changed)[:160]),
                    self.assertRaises(ValueError),
                ):
                    engine.evaluate(changed)
                self.assertEqual(changed, original)

    def test_inclusive_128_bit_inputs_signed_values_and_no_output_cutoff(self):
        for name, engine in self.engines():
            for key in RATIONAL_FIELDS:
                index = 6 if key == "g" else 5 if key == "q" else 1
                _, prototype, base_Q = base_cases()[index]
                for boundary in (F(2**127), F(1, 2**127)):
                    world, Q = copy.deepcopy(prototype), copy.deepcopy(base_Q)
                    old = world[key][0]
                    world[key][0] = boundary
                    if key == "mu":
                        Q[0] = scale_vector(Q[0], old / boundary)
                    elif key == "k":
                        Q = scale_matrix(Q, boundary / old)
                    with self.subTest(engine=name, field=key, boundary=boundary):
                        row = engine.evaluate(world)
                        exact(self, row, oracle_row(world, Q))
                        if key == "f" and boundary == F(2**127):
                            self.assertGreater(
                                row["balances"]["energy"].numerator.bit_length(), 128
                            )
                if key in ("x", "f", "g", "q"):
                    signed = copy.deepcopy(prototype)
                    signed[key][0] = F(-(2**127))
                    exact(self, engine.evaluate(signed), oracle_row(signed, base_Q))

    def test_shared_valid_containers_and_fresh_cross_call_outputs(self):
        for name, engine in self.engines():
            shared_positive, shared_zero, shared_empty = vector([1]), vector([0]), []
            world = {
                "mu": shared_positive,
                "edges": shared_empty,
                "k": shared_empty,
                "x": shared_zero,
                "mode": "closed",
                "I": [0],
                "D": shared_empty,
                "f": shared_positive,
                "g": shared_empty,
                "q": shared_zero,
            }
            original = copy.deepcopy(world)
            expected = oracle_row(original, matrix([[0]]))
            first, second = engine.evaluate(world), engine.evaluate(copy.deepcopy(original))
            with self.subTest(engine=name):
                exact(self, first, expected)
                exact(self, second, expected)
                self.assertFalse(mutable_ids(world) & mutable_ids(first))
                self.assertFalse(mutable_ids(first) & mutable_ids(second))
                self.assertIs(world["mu"], world["f"])
                self.assertIs(world["x"], world["q"])
                first["world"]["mu"][0] = F(999)
                first["Q"][0][0] = F(999)
                first["reduced"]["nodes"].append(999)
                exact(self, world, original)
                exact(self, second, expected)
                exact(self, engine.evaluate(copy.deepcopy(original)), expected)


class EvidenceTests(unittest.TestCase):
    def test_nine_sources_and_pins_checked_before_protocol_parse(self):
        study = load_study()
        snapshot = study.source_snapshot()
        self.assertEqual(len(study.SOURCE_PATHS), 9)
        self.assertEqual(set(snapshot), set(study.SOURCE_PATHS))
        for name, blob in snapshot.items():
            self.assertIs(type(blob), bytes, name)
            self.assertLessEqual(len(blob), 262144, name)
        for name in ["protocol.json", *study.DEPENDENCY_PINS]:
            changed = {**snapshot, name: snapshot[name] + b"\n"}
            with (
                self.subTest(source=name),
                mock.patch.object(study, "strict_loads", side_effect=AssertionError("early parse")),
                self.assertRaises(ValueError),
            ):
                study._protocol(changed)

    def test_utility_authentication_regular_file_and_size_refusals(self):
        study = load_study()
        with tempfile.TemporaryDirectory(prefix="qr05-measure-utility-") as directory:
            root = Path(directory)
            untrusted = root / "probe.py"
            untrusted.write_bytes(b"raise AssertionError('untrusted execution')\n")
            oversize = root / "oversize.py"
            oversize.write_bytes(b" " * (study.SOURCE_LIMIT + 1))
            link = root / "link.py"
            link.symlink_to(untrusted)
            for path in (untrusted, oversize, link, root, root / "missing.py"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    study._load_utilities(path)

    def test_native_codec_and_strict_json_refusals(self):
        study = load_study()
        value = {"fraction": F(1), "integer": 1, "flag": True, "rows": []}
        exact(self, study.decode(study.strict_loads(study.canonical(study.encode(value)))), value)
        for left, right in ((F(1), 1), (True, 1), ([], ()), ({"x": 1}, {"x": 1, "extra": 0})):
            with self.assertRaises(ValueError):
                study.require_equal(left, right)
        for blob in (b'{"x":1,"x":2}', b'{"x":1.0}', b'{"x":NaN}'):
            with self.assertRaises(ValueError):
                study.strict_loads(blob)

    def test_authenticated_synthetic_roundtrip_and_exclusive_publication(self):
        study = load_study()
        synthetic = {"value": F(1, 3), "integer": 1, "flag": True}
        with tempfile.TemporaryDirectory(prefix="qr05-measure-evidence-") as directory:
            freeze, capture = Path(directory) / "freeze.json", Path(directory) / "capture.json"
            with mock.patch.object(study, "analyze", return_value=synthetic):
                artifact = study.freeze(freeze)
                self.assertEqual(artifact["schema"], "qr05-measure-divergence-source-freeze-v1")
                self.assertEqual(len(artifact["sources"]), 9)
                exact(self, study.capture(capture, freeze), synthetic)
                exact(self, study.replay(capture, freeze), synthetic)
                with self.assertRaises(FileExistsError):
                    study.freeze(freeze)
                with self.assertRaises(FileExistsError):
                    study.capture(capture, freeze)
                original = capture.read_bytes()
                decoded = json.loads(original)
                self.assertEqual(decoded["schema"], "qr05-measure-divergence-capture-v1")
                decoded["report"]["integer"] = True
                capture.write_bytes(study.canonical(decoded))
                with self.assertRaises(ValueError):
                    study.replay(capture, freeze)
                capture.write_bytes(original)
                frozen = freeze.read_bytes()
                freeze.write_bytes(frozen + b"\n")
                with self.assertRaises(ValueError):
                    study.replay(capture, freeze)
                freeze.write_bytes(frozen)
                decoded = json.loads(original)
                decoded["freeze_sha256"] = "0" * 64
                capture.write_bytes(study.canonical(decoded))
                with self.assertRaises(ValueError):
                    study.replay(capture, freeze)

    def test_freeze_schema_identity_runtime_and_canonical_refusals(self):
        study = load_study()
        snapshot = study.source_snapshot()
        with tempfile.TemporaryDirectory(prefix="qr05-measure-freeze-") as directory:
            path = Path(directory) / "freeze.json"
            study.freeze(path)
            original = json.loads(path.read_bytes())
            bad = [
                {**original, field: value}
                for field, value in (("schema", "wrong"), ("sources", {}), ("extra", 1))
            ]
            for field, value in (
                ("optimization", True),
                ("optimization", 3),
                ("version", ""),
                ("implementation", []),
            ):
                bad.append({**original, "runtime": {**original["runtime"], field: value}})
            for value in bad:
                path.write_bytes(study.canonical(value))
                with self.subTest(value=value), self.assertRaises(ValueError):
                    study._checked_freeze(path, snapshot)
            path.write_bytes(study.canonical(original) + b"\n")
            with self.assertRaises(ValueError):
                study._checked_freeze(path, snapshot)

    def test_capture_schema_sources_and_tampering_refuse_before_analysis(self):
        study = load_study()
        with tempfile.TemporaryDirectory(prefix="qr05-measure-capture-") as directory:
            freeze, capture = Path(directory) / "freeze.json", Path(directory) / "capture.json"
            study.freeze(freeze)
            with mock.patch.object(study, "analyze", return_value={"value": F(1)}):
                study.capture(capture, freeze)
            original = json.loads(capture.read_bytes())
            for field, value in (
                ("schema", "wrong"),
                ("sources", {}),
                ("extra", 1),
                ("freeze_sha256", "0" * 64),
            ):
                capture.write_bytes(study.canonical({**original, field: value}))
                with (
                    self.subTest(field=field),
                    mock.patch.object(
                        study, "analyze", side_effect=AssertionError("early analysis")
                    ),
                    self.assertRaises(ValueError),
                ):
                    study.replay(capture, freeze)

    def test_first_capture_full_native_binding_without_another_analysis(self):
        study, snapshot, _, report = context()
        freeze = study._checked_freeze(HERE / "source-freeze.json", snapshot)
        data = study.read_bounded(HERE / "results.json")
        artifact = study.strict_loads(data)
        self.assertEqual(set(artifact), {"schema", "sources", "freeze_sha256", "report"})
        self.assertEqual(artifact["schema"], "qr05-measure-divergence-capture-v1")
        self.assertEqual(study.canonical(artifact), data)
        study.require_equal(artifact["sources"], study.identities(snapshot))
        self.assertEqual(artifact["freeze_sha256"], hashlib.sha256(freeze).hexdigest())
        exact(self, study.decode(artifact["report"]), report)

    def test_complete_route_type_mismatch_and_late_source_drift_refuse(self):
        study, snapshot, _, report = context()
        changed = copy.deepcopy(report)
        changed["rows"][0]["Q"][0][0] = 0
        left = types.SimpleNamespace(analyze=lambda: copy.deepcopy(report))
        right = types.SimpleNamespace(analyze=lambda: copy.deepcopy(changed))
        with (
            mock.patch.object(study, "load_engine", side_effect=[left, right]),
            self.assertRaises(ValueError),
        ):
            study.analyze(snapshot)
        drifted = {**snapshot, "primary.py": snapshot["primary.py"] + b"\n"}
        with (
            mock.patch.object(study, "load_engine", side_effect=[left, left]),
            mock.patch.object(study, "source_snapshot", return_value=drifted),
            self.assertRaises(ValueError),
        ):
            study.analyze(snapshot)

    def test_freeze_and_source_rechecks_around_capture(self):
        study = load_study()
        snapshot = study.source_snapshot()
        with tempfile.TemporaryDirectory(prefix="qr05-measure-races-") as directory:
            freeze, capture = Path(directory) / "freeze.json", Path(directory) / "capture.json"
            study.freeze(freeze)
            original = freeze.read_bytes()

            def mutate_freeze(_snapshot):
                freeze.write_bytes(original + b"\n")
                return {"value": F(1)}

            with (
                mock.patch.object(study, "analyze", side_effect=mutate_freeze),
                self.assertRaises(ValueError),
            ):
                study.capture(capture, freeze)
            self.assertFalse(capture.exists())
            freeze.write_bytes(original)
            drifted = {**snapshot, "reference.py": snapshot["reference.py"] + b"\n"}
            with (
                mock.patch.object(study, "source_snapshot", side_effect=[snapshot, drifted]),
                mock.patch.object(study, "analyze", return_value={"value": F(1)}),
                self.assertRaises(ValueError),
            ):
                study.capture(capture, freeze)
            self.assertFalse(capture.exists())

    def test_publication_readback_and_replay_input_stability(self):
        study = load_study()
        with tempfile.TemporaryDirectory(prefix="qr05-measure-publish-") as directory:
            freeze, capture = Path(directory) / "freeze.json", Path(directory) / "capture.json"
            study.freeze(freeze)
            actual_write = study._write_new

            def altered_write(path, blob):
                actual_write(path, blob)
                Path(path).write_bytes(blob + b"\n")

            with (
                mock.patch.object(study, "_write_new", side_effect=altered_write),
                mock.patch.object(study, "analyze", return_value={"value": F(1)}),
                self.assertRaises(ValueError),
            ):
                study.capture(capture, freeze)
            capture.unlink()
            with mock.patch.object(study, "analyze", return_value={"value": F(1)}):
                study.capture(capture, freeze)
            original = capture.read_bytes()

            def alter_capture(_snapshot):
                capture.write_bytes(original + b"\n")
                return {"value": F(1)}

            with (
                mock.patch.object(study, "analyze", side_effect=alter_capture),
                self.assertRaises(ValueError),
            ):
                study.replay(capture, freeze)


if __name__ == "__main__":

    def expired(_signum, _frame):
        raise KeyboardInterrupt("60-second measure/divergence suite deadline")

    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, 60)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
