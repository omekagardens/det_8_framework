"""Source-bound BF tests: independent Boole/cofactor/scalar oracle.

No fixture evaluation or engine execution occurs at import. The complete
suite is held until the first source-bound release. Checks survive -O.
Only this gate's study driver is imported; no historical executor is used.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
import sys
import tempfile
import unittest
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

HERE = Path(__file__).resolve().parent
PROTOCOL_SHA256 = "0c874abb8290fc1d6e4d76c25c741bf778e5c721f8f7c0310693fcbf1804aa4e"


def load_module(name):
    spec = importlib.util.spec_from_file_location("qr05bf_test_" + name, HERE / (name + ".py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("BF source could not be loaded")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)
    return module


def exact_keys(test, value, names):
    test.assertIs(type(value), dict)
    test.assertEqual(set(value), set(names.split()))


@lru_cache(maxsize=1)
def boole_rule():
    nodes = tuple(Fraction(i, 4) for i in range(5))
    weights = tuple(Fraction(n, 90) for n in (7, 32, 12, 32, 7))
    for degree in range(6):
        if sum(w * x**degree for x, w in zip(nodes, weights, strict=True)) != Fraction(
            1, degree + 1
        ):
            raise ValueError("Independent quadrature certificate failed")
    return nodes, weights


def integrate(function):
    nodes, weights = boole_rule()
    return sum(
        (
            wu * wv * function(u, v)
            for u, wu in zip(nodes, weights, strict=True)
            for v, wv in zip(nodes, weights, strict=True)
        ),
        Fraction(0),
    )


def basis(u, v):
    return [(1 - u) * (1 - v), u * (1 - v), (1 - u) * v, u * v, u * (1 - u) * v * (1 - v)]


def functional(coefficients):
    return integrate(lambda u, v: dot(coefficients, basis(u, v)) * (1 - u) * (1 - v))


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), Fraction(0))


def multiply(a, b):
    return [[dot(row, list(column)) for column in zip(*b, strict=True)] for row in a]


def identity(n):
    return [[Fraction(i == j) for j in range(n)] for i in range(n)]


def determinant(matrix):
    """Permutation expansion, independent of either implementation's solver."""
    n = len(matrix)
    result = Fraction(0)
    for permutation in itertools.permutations(range(n)):
        inversions = sum(permutation[i] > permutation[j] for i in range(n) for j in range(i + 1, n))
        term = Fraction((-1) ** inversions)
        for i, j in enumerate(permutation):
            term *= matrix[i][j]
        result += term
    return result


def cofactor_inverse(matrix):
    denominator = determinant(matrix)
    if not denominator:
        raise ValueError("Singular independent test matrix")
    n = len(matrix)
    return [
        [
            Fraction((-1) ** (i + j))
            * determinant(
                [
                    [matrix[row][column] for column in range(n) if column != i]
                    for row in range(n)
                    if row != j
                ]
            )
            / denominator
            for j in range(n)
        ]
        for i in range(n)
    ]


def row_rank(matrix):
    """Exact rational Gram-Schmidt, not an echelon implementation."""
    vectors = []
    for row in matrix:
        residual = list(row)
        for vector in vectors:
            coefficient = dot(residual, vector) / dot(vector, vector)
            residual = [x - coefficient * y for x, y in zip(residual, vector, strict=True)]
        if any(residual):
            vectors.append(residual)
    return len(vectors)


def probability(means, outcomes):
    result = Fraction(1)
    for mean, outcome in zip(means, outcomes, strict=True):
        result *= (1 + mean * outcome) / 2
    return result


def branch_state(outcomes, mass):
    return [
        mass
        if all(outcome == 1 - 2 * bit for outcome, bit in zip(outcomes, bits, strict=True))
        else Fraction(0)
        for bits in itertools.product((0, 1), repeat=len(outcomes))
    ]


def trace_11(diagonal):
    """Insert both omitted bits into each desired retained bit string."""
    result = []
    for retained in itertools.product((0, 1), repeat=4):
        value = Fraction(0)
        for discarded in (0, 1):
            bits = (*retained[:3], discarded, retained[3])
            index = 0
            for bit in bits:
                index = 2 * index + bit
            value += diagonal[index]
        result.append(value)
    return result


def score(rows, estimate_key, target):
    mean = sum((r["probability"] * r[estimate_key] for r in rows), Fraction(0))
    variance = sum((r["probability"] * (r[estimate_key] - mean) ** 2 for r in rows), Fraction(0))
    bias = mean - target
    return {"mean": mean, "bias": bias, "variance": variance, "mse": variance + bias * bias}


def expected(protocol):
    """Literal entire native wire from independent integration and scalar laws."""
    q = [functional(row) for row in identity(5)]
    retained = protocol["retained_indices"]
    omitted = protocol["omitted_index"]
    stale = list(map(Fraction, protocol["stale_weights"]))
    volume = integrate(lambda _u, _v: Fraction(protocol["geometry"]["measure_factor"]))
    geometry = {
        "volume": volume,
        "sigma": volume**4,
        "coefficient_integrals": q,
        "stale_weights": stale,
        "equality_threshold": q[4] / q[3],
        "retained_indices": list(retained),
        "omitted_index": omitted,
    }
    placements = []
    for declared in protocol["placements"]:
        u, v = map(Fraction, declared["position"])
        last = basis(u, v)
        a = identity(5)[:4] + [last]
        decoder = cofactor_inverse(a)
        full_weights = multiply([q], decoder)[0]
        sa = [a[i] for i in retained]
        direction = [row[omitted] for row in decoder]
        candidate = [full_weights[i] for i in retained]
        candidate_residual = [x - y for x, y in zip(multiply([candidate], sa)[0], q, strict=True)]
        stale_residual = [x - y for x, y in zip(multiply([stale], sa)[0], q, strict=True)]
        target_null = dot(q, direction)
        delta = 1 / (2 * (1 + abs(direction[-1]) / 16))
        fixture_coefficients = [
            (p["id"], [*map(Fraction, p["corners"]), Fraction(p["theta"])])
            for p in protocol["profiles"]
        ]
        fixture_coefficients += [
            (name, [sign * delta * x for x in direction])
            for name, sign in zip(protocol["collision"]["ids"], (-1, 1), strict=True)
        ]
        profiles = []
        for name, coefficients in fixture_coefficients:
            means = [dot(row, coefficients) for row in a]
            target = functional(coefficients)
            reduced_rows = []
            for outcomes in itertools.product((-1, 1), repeat=4):
                mass = probability([means[i] for i in retained], outcomes)
                reduced_rows.append(
                    {
                        "outcomes": list(outcomes),
                        "probability": mass,
                        "state_diagonal": branch_state(outcomes, mass),
                        "stale_estimate": dot(stale, outcomes),
                        "candidate_estimate": dot(candidate, outcomes),
                    }
                )
            full_rows = []
            for outcomes in itertools.product((-1, 1), repeat=5):
                mass = probability(means, outcomes)
                full_rows.append(
                    {
                        "outcomes": list(outcomes),
                        "probability": mass,
                        "state_diagonal": branch_state(outcomes, mass),
                        "estimate": dot(full_weights, outcomes),
                    }
                )
            marginal_rows = []
            for reduced in reduced_rows:
                indices = [
                    i
                    for i, full in enumerate(full_rows)
                    if [full["outcomes"][j] for j in retained] == reduced["outcomes"]
                ]
                summed = [
                    sum((full_rows[i]["state_diagonal"][j] for i in indices), Fraction(0))
                    for j in range(32)
                ]
                marginal_rows.append(
                    {
                        "outcomes": list(reduced["outcomes"]),
                        "full_indices": indices,
                        "probability": sum(
                            (full_rows[i]["probability"] for i in indices), Fraction(0)
                        ),
                        "summed_full_state": summed,
                        "reduced_state": trace_11(summed),
                        "full_minus_candidate": [
                            full_rows[i]["estimate"] - reduced["candidate_estimate"]
                            for i in indices
                        ],
                    }
                )
            profiles.append(
                {
                    "id": name,
                    "coefficients": coefficients,
                    "admission_bound": max(map(abs, coefficients[:4])) + abs(coefficients[-1]) / 16,
                    "sample_means": means,
                    "recovered_coefficients": [dot(row, means) for row in decoder],
                    "target": target,
                    "reduced": {
                        "rows": reduced_rows,
                        "stale": score(reduced_rows, "stale_estimate", target),
                        "candidate": score(reduced_rows, "candidate_estimate", target),
                    },
                    "full": {"rows": full_rows, **score(full_rows, "estimate", target)},
                    "marginalization": {
                        "rows": marginal_rows,
                        "pathwise_nonzero_count": sum(
                            x != 0 for row in marginal_rows for x in row["full_minus_candidate"]
                        ),
                    },
                }
            )
        minus, plus = profiles[-2:]
        averaged = [
            [
                sum((row["state_diagonal"][j] for row in p["full"]["rows"]), Fraction(0))
                for j in range(32)
            ]
            for p in (minus, plus)
        ]
        collision = {
            "profiles": list(protocol["collision"]["ids"]),
            "coefficients_difference": [
                y - x for x, y in zip(minus["coefficients"], plus["coefficients"], strict=True)
            ],
            "full_means_difference": [
                y - x for x, y in zip(minus["sample_means"], plus["sample_means"], strict=True)
            ],
            "target_difference": plus["target"] - minus["target"],
            "predicted_target_difference": 2 * delta * target_null,
            "omitted_states": [
                [(1 + p["sample_means"][omitted]) / 2, (1 - p["sample_means"][omitted]) / 2]
                for p in (minus, plus)
            ],
            "full_averaged_states": averaged,
            "full_law_total_variation": sum(
                (
                    abs(y["probability"] - x["probability"])
                    for x, y in zip(minus["full"]["rows"], plus["full"]["rows"], strict=True)
                ),
                Fraction(0),
            )
            / 2,
            "retained_law_total_variation": sum(
                (
                    abs(y["probability"] - x["probability"])
                    for x, y in zip(minus["reduced"]["rows"], plus["reduced"]["rows"], strict=True)
                ),
                Fraction(0),
            )
            / 2,
        }
        placements.append(
            {
                "id": declared["id"],
                "position": [u, v],
                "basis": last,
                "evaluation_matrix": a,
                "coefficient_decoder": decoder,
                "left_inverse": multiply(decoder, a),
                "right_inverse": multiply(a, decoder),
                "full_weights": full_weights,
                "full_residual": [
                    x - y for x, y in zip(multiply([full_weights], a)[0], q, strict=True)
                ],
                "retained_evaluation_matrix": sa,
                "retained_rank": row_rank(sa),
                "omission_direction": direction,
                "retained_null_image": [dot(row, direction) for row in sa],
                "target_null_image": target_null,
                "locus_residual": (1 - u) * (1 - v) - q[4] / q[3],
                "stale_residual": stale_residual,
                "candidate_weights": candidate,
                "candidate_residual": candidate_residual,
                "recovery_status": "identified"
                if target_null == 0 and not any(candidate_residual)
                else "not_identified",
                "collision_scale": delta,
                "profiles": profiles,
                "collision": collision,
            }
        )
    return {"geometry": geometry, "placements": placements}


@lru_cache(maxsize=1)
def evaluated():
    study = load_module("study")
    protocol = study.load_protocol()
    return study, protocol, study.compare_routes()


class ProtocolTests(unittest.TestCase):
    def test_pinned_protocol_menu_and_no_observer_contract(self):
        data = (HERE / "protocol.json").read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), PROTOCOL_SHA256)
        p = json.loads(data)
        self.assertEqual(p["study"], "QR-05BF")
        self.assertEqual(
            [x["id"] for x in p["placements"]],
            ["center", "equality_u", "equality_v", "shift_low", "shift_high", "near_corner"],
        )
        self.assertEqual(len(p["profiles"]), 4)
        self.assertEqual(p["retained_indices"], [0, 1, 2, 4])
        self.assertEqual(p["omitted_index"], 3)
        self.assertNotIn("plans", p)
        self.assertNotIn("record_keys", p)
        for item in p["placements"]:
            for coordinate in item["position"]:
                self.assertGreater(Fraction(coordinate), 0)
                self.assertLess(Fraction(coordinate), 1)

    def test_boole_moment_certificate_before_integration(self):
        p = json.loads((HERE / "protocol.json").read_bytes())
        nodes, weights = boole_rule()
        self.assertEqual(nodes, tuple(map(Fraction, p["third_oracle"]["nodes"])))
        self.assertEqual(weights, tuple(map(Fraction, p["third_oracle"]["weights"])))
        self.assertEqual(p["third_oracle"]["verify_moments_through"], 5)
        for a, b in itertools.product(range(6), repeat=2):
            self.assertEqual(
                integrate(lambda u, v, a=a, b=b: u**a * v**b), Fraction(1, (a + 1) * (b + 1))
            )


class MathematicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        cls.oracle = expected(cls.protocol)

    def test_complete_native_report_against_independent_oracle(self):
        self.assertEqual(self.report, self.oracle)
        self.assertEqual(self.study.encode(self.report), self.study.encode(self.oracle))
        self.assertEqual(len(self.report["placements"]), 6)

    def test_exact_numeric_types_and_canonical_encoding(self):
        integer_keys = {"omitted_index", "retained_rank", "pathwise_nonzero_count"}
        integer_vectors = {"retained_indices", "full_indices", "outcomes"}

        def visit(value, path=()):
            if type(value) is dict:
                self.assertTrue(all(type(k) is str for k in value))
                for key, child in value.items():
                    visit(child, (*path, key))
            elif type(value) is list:
                for i, child in enumerate(value):
                    visit(child, (*path, i))
            elif path[-1] in {"id", "recovery_status"} or (
                "collision" in path and "profiles" == path[-2]
            ):
                self.assertIs(type(value), str, path)
            elif path[-1] in integer_keys or any(key in path for key in integer_vectors):
                self.assertIs(type(value), int, path)
            else:
                self.assertIs(type(value), Fraction, path)
                encoded = self.study.encode(value)
                self.assertIs(type(encoded), str)
                self.assertEqual(str(Fraction(encoded)), encoded)

        visit(self.report)

    def test_full_inverse_rank_null_and_equality_locus_identities(self):
        q = self.report["geometry"]["coefficient_integrals"]
        for p in self.report["placements"]:
            with self.subTest(placement=p["id"]):
                a, decoder = p["evaluation_matrix"], p["coefficient_decoder"]
                self.assertEqual(multiply(a, decoder), identity(5))
                self.assertEqual(multiply(decoder, a), identity(5))
                self.assertEqual(p["left_inverse"], identity(5))
                self.assertEqual(p["right_inverse"], identity(5))
                self.assertEqual(p["retained_rank"], 4)
                self.assertEqual(row_rank(p["retained_evaluation_matrix"]), 4)
                d = p["omission_direction"]
                self.assertEqual(d[:4], [0, 0, 0, 1])
                self.assertEqual([dot(row, d) for row in a], [0, 0, 0, 1, 0])
                u, v = p["position"]
                self.assertEqual(d[-1], -1 / ((1 - u) * (1 - v)))
                self.assertEqual(p["target_null_image"], q[3] - q[4] / ((1 - u) * (1 - v)))
                self.assertEqual(
                    p["locus_residual"],
                    (1 - u) * (1 - v) - self.report["geometry"]["equality_threshold"],
                )
                self.assertEqual(p["target_null_image"] == 0, p["locus_residual"] == 0)
                self.assertEqual(p["full_weights"][3], p["target_null_image"])
                self.assertEqual(p["candidate_residual"], [0, 0, 0, -p["target_null_image"], 0])
                self.assertEqual(p["full_residual"], [0] * 5)

    def test_stale_decoder_failure_is_not_reduced_access_failure(self):
        placements = {p["id"]: p for p in self.report["placements"]}
        self.assertEqual(placements["center"]["stale_residual"], [0] * 5)
        for name in ("center", "equality_u", "equality_v"):
            self.assertEqual(placements[name]["recovery_status"], "identified")
            self.assertEqual(placements[name]["candidate_residual"], [0] * 5)
        for name in ("equality_u", "equality_v"):
            self.assertTrue(any(placements[name]["stale_residual"]))
        for p in placements.values():
            identified = not any(p["candidate_residual"])
            self.assertEqual(p["recovery_status"], "identified" if identified else "not_identified")

    def test_complete_branch_accounting_and_analytic_score_biases(self):
        total = zeros = 0
        for p in self.report["placements"]:
            for f in p["profiles"]:
                self.assertLessEqual(f["admission_bound"], 1)
                self.assertEqual(f["recovered_coefficients"], f["coefficients"])
                self.assertTrue(all(-1 <= mean <= 1 for mean in f["sample_means"]))
                for system, n in (("reduced", 4), ("full", 5)):
                    rows = f[system]["rows"]
                    self.assertEqual(len(rows), 2**n)
                    self.assertEqual(sum(r["probability"] for r in rows), 1)
                    self.assertEqual(
                        [r["outcomes"] for r in rows],
                        [list(x) for x in itertools.product((-1, 1), repeat=n)],
                    )
                    for row in rows:
                        self.assertGreaterEqual(row["probability"], 0)
                        self.assertEqual(sum(row["state_diagonal"]), row["probability"])
                        self.assertTrue(all(x >= 0 for x in row["state_diagonal"]))
                        zeros += row["probability"] == 0
                    total += len(rows)
                for name, weights, residual in (
                    ("stale", self.report["geometry"]["stale_weights"], p["stale_residual"]),
                    ("candidate", p["candidate_weights"], p["candidate_residual"]),
                ):
                    scores = f["reduced"][name]
                    means = [f["sample_means"][i] for i in self.protocol["retained_indices"]]
                    self.assertEqual(scores["mean"], dot(weights, means))
                    self.assertEqual(scores["bias"], dot(residual, f["coefficients"]))
                    self.assertEqual(
                        scores["variance"],
                        sum(w * w * (1 - m * m) for w, m in zip(weights, means, strict=True)),
                    )
                    self.assertEqual(scores["mse"], scores["variance"] + scores["bias"] ** 2)
                self.assertEqual(f["full"]["bias"], 0)
                self.assertEqual(f["full"]["mean"], f["target"])
                self.assertEqual(
                    f["full"]["variance"],
                    sum(
                        w * w * (1 - m * m)
                        for w, m in zip(p["full_weights"], f["sample_means"], strict=True)
                    ),
                )
        self.assertEqual(total, 1728)
        self.assertGreater(zeros, 0)

    def test_marginalization_always_holds_but_pathwise_estimates_may_differ(self):
        nonidentifiable = 0
        for p in self.report["placements"]:
            coefficient = p["full_weights"][3]
            nonidentifiable += coefficient != 0
            for f in p["profiles"]:
                full = f["full"]["rows"]
                for reduced, marginal in zip(
                    f["reduced"]["rows"], f["marginalization"]["rows"], strict=True
                ):
                    self.assertEqual(marginal["probability"], reduced["probability"])
                    self.assertEqual(marginal["reduced_state"], reduced["state_diagonal"])
                    self.assertEqual(
                        trace_11(marginal["summed_full_state"]), reduced["state_diagonal"]
                    )
                    self.assertEqual(len(marginal["summed_full_state"]), 32)
                    for index, difference in zip(
                        marginal["full_indices"], marginal["full_minus_candidate"], strict=True
                    ):
                        self.assertEqual(difference, coefficient * full[index]["outcomes"][3])
                self.assertEqual(
                    f["marginalization"]["pathwise_nonzero_count"], 0 if coefficient == 0 else 32
                )
        self.assertGreater(nonidentifiable, 0)

    def test_admitted_collision_is_target_ambiguity_only_when_null_image_nonzero(self):
        for p in self.report["placements"]:
            minus, plus = p["profiles"][-2:]
            delta = p["collision_scale"]
            d = p["omission_direction"]
            collision = p["collision"]
            self.assertEqual(delta, 1 / (2 * (1 + abs(d[-1]) / 16)))
            self.assertGreater(delta, 0)
            for f, sign in ((minus, -1), (plus, 1)):
                self.assertEqual(f["coefficients"], [sign * delta * x for x in d])
                self.assertEqual(f["admission_bound"], Fraction(1, 2))
                self.assertEqual(
                    [f["sample_means"][i] for i in self.protocol["retained_indices"]], [0] * 4
                )
            self.assertEqual(minus["reduced"]["rows"], plus["reduced"]["rows"])
            self.assertNotEqual(minus["coefficients"], plus["coefficients"])
            self.assertNotEqual(collision["omitted_states"][0], collision["omitted_states"][1])
            self.assertNotEqual(
                collision["full_averaged_states"][0], collision["full_averaged_states"][1]
            )
            self.assertGreater(collision["full_law_total_variation"], 0)
            self.assertEqual(collision["retained_law_total_variation"], 0)
            self.assertEqual(collision["target_difference"], 2 * delta * p["target_null_image"])
            self.assertEqual(
                collision["target_difference"] == 0, p["recovery_status"] == "identified"
            )

    def test_coordinate_swap_preserves_geometric_certificates_not_profile_labels(self):
        placements = {p["id"]: p for p in self.report["placements"]}
        first, second = placements["equality_u"], placements["equality_v"]
        permutation = [0, 2, 1, 3, 4]
        self.assertEqual(first["position"], second["position"][::-1])
        for key in (
            "basis",
            "full_weights",
            "stale_residual",
            "candidate_residual",
            "omission_direction",
        ):
            self.assertEqual([first[key][i] for i in permutation], second[key])
        self.assertEqual(first["collision_scale"], second["collision_scale"])
        self.assertEqual(first["target_null_image"], second["target_null_image"])
        # The asymmetric base coefficients were not swapped: no assertion that
        # its station-labeled laws coincide under a geometry-only swap.


class RouteBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.study = load_module("study")
        self.protocol = {"public": [1, "contract"], "ratio": "1/3"}
        self.report = {
            "rational": Fraction(1, 3),
            "integer": 1,
            "rows": [Fraction(0)],
            "empty": None,
        }
        self.freeze = {
            "sources": {
                str((self.study.ROOT / (name + ".py")).relative_to(self.study.REPO)): {
                    "bytes": 1,
                    "sha256": "a" * 64,
                }
                for name in ("quantum", "reference")
            }
        }

    def compare(self, left, right):
        with (
            mock.patch.object(self.study, "_frozen", return_value=self.freeze),
            mock.patch.object(
                self.study, "load_protocol", return_value=copy.deepcopy(self.protocol)
            ),
            mock.patch.object(
                self.study,
                "_load_engine",
                side_effect=lambda name, _identity: SimpleNamespace(
                    analyze=left if name == "quantum" else right
                ),
            ),
        ):
            return self.study.compare_routes()

    def test_raw_report_numeric_type_and_extra_field_mutations(self):
        mutations = []
        for key, value in (
            ("rational", "1/3"),
            ("rational", Fraction(2, 3)),
            ("integer", True),
            ("integer", Fraction(1)),
            ("rows", [Fraction(1)]),
            ("rows", (Fraction(0),)),
            ("empty", "null"),
        ):
            changed = copy.deepcopy(self.report)
            changed[key] = value
            mutations.append(changed)
        changed = copy.deepcopy(self.report)
        changed["private"] = "unrecorded"
        mutations.append(changed)
        changed = copy.deepcopy(self.report)
        del changed["empty"]
        mutations.append(changed)
        for changed in mutations:
            with self.subTest(mutation=repr(changed)), self.assertRaises(ValueError):
                self.compare(
                    lambda _p: copy.deepcopy(self.report), lambda _p, changed=changed: changed
                )

    def test_equal_reports_and_input_copy_ownership(self):
        seen = []

        def analyzer(problem):
            seen.append(problem)
            return copy.deepcopy(self.report)

        self.assertEqual(self.compare(analyzer, analyzer), self.report)
        self.assertEqual(seen, [self.protocol, self.protocol])
        self.assertIsNot(seen[0], seen[1])
        self.assertIsNot(seen[0]["public"], seen[1]["public"])

    def test_mutating_either_engine_input_refused(self):
        def corrupt(problem):
            problem["public"].append("changed")
            return copy.deepcopy(self.report)

        def corrupt_type(problem):
            problem["ratio"] = Fraction(problem["ratio"])
            return copy.deepcopy(self.report)

        for corruption in (corrupt, corrupt_type):
            for left, right in (
                (corruption, lambda _p: copy.deepcopy(self.report)),
                (lambda _p: copy.deepcopy(self.report), corruption),
            ):
                with (
                    self.subTest(corruption=corruption.__name__, primary=left is corruption),
                    self.assertRaises(ValueError),
                ):
                    self.compare(left, right)

    def test_changed_freeze_after_route_refused(self):
        engine = SimpleNamespace(analyze=lambda _p: copy.deepcopy(self.report))
        changed = copy.deepcopy(self.freeze)
        changed["extra"] = "changed"
        with (
            mock.patch.object(self.study, "_frozen", side_effect=[self.freeze, changed]),
            mock.patch.object(self.study, "load_protocol", return_value=self.protocol),
            mock.patch.object(self.study, "_load_engine", return_value=engine),
            self.assertRaises(ValueError),
        ):
            self.study.compare_routes()

    def test_hashed_source_loader_ignores_import_caches_and_checks_bytes(self):
        with tempfile.TemporaryDirectory(prefix="det8-qr05bf-loader-") as temporary:
            root = Path(temporary)
            source = root / "quantum.py"
            source.write_bytes(
                b"def analyze(protocol):\n    return {'public': protocol['public']}\n"
            )
            identity = {
                "bytes": source.stat().st_size,
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            }
            poisoned = SimpleNamespace(analyze=lambda _p: "cached hidden answer")
            with (
                mock.patch.object(self.study, "ROOT", root),
                mock.patch.dict(sys.modules, {"quantum": poisoned}),
            ):
                first = self.study._load_engine("quantum", identity)
                second = self.study._load_engine("quantum", identity)
                self.assertIsNot(first, second)
                self.assertEqual(first.analyze({"public": "supplied"}), {"public": "supplied"})
                self.assertIs(sys.modules["quantum"], poisoned)
                source.write_bytes(source.read_bytes() + b"\n")
                with self.assertRaises(ValueError):
                    self.study._load_engine("quantum", identity)
                with self.assertRaises(ValueError):
                    self.study._load_engine("old_executor", identity)


def set_path(value, path, replacement):
    current = value
    for component in path[:-1]:
        current = current[component]
    current[path[-1]] = replacement


def get_path(value, path):
    for component in path:
        value = value[component]
    return value


def analysis_mutations(original):
    """Stream representative fields, late branch values and shape/type changes."""
    leaves = []

    def collect(value, path=()):
        if type(value) is dict:
            for key, child in value.items():
                collect(child, (*path, key))
        elif type(value) is list:
            if value:
                collect(value[0], (*path, 0))
        else:
            leaves.append((path, value))

    collect(original)
    for path, value in leaves:
        if type(value) is str:
            try:
                replacement = str(Fraction(value) + 1)
            except ValueError:
                replacement = value + "-changed"
        elif type(value) is int:
            replacement = value + 1
        else:
            replacement = "changed"
        changed = copy.deepcopy(original)
        set_path(changed, path, replacement)
        yield "scalar " + repr(path), changed
    late = ("mathematics", "placements", -1, "profiles", -1)
    paths = [(*late, "full", "rows", -1, key) for key in ("probability", "estimate")]
    paths += [
        (*late, "reduced", "rows", -1, key)
        for key in ("probability", "stale_estimate", "candidate_estimate")
    ]
    paths += [
        (*late, "full", "rows", -1, "state_diagonal", -1),
        (*late, "reduced", "rows", -1, "state_diagonal", -1),
        (*late, "marginalization", "rows", -1, "full_minus_candidate", -1),
        (*late, "marginalization", "rows", -1, "summed_full_state", -1),
        (*late, "marginalization", "rows", -1, "reduced_state", -1),
    ]
    for path in paths:
        changed = copy.deepcopy(original)
        set_path(changed, path, str(Fraction(get_path(changed, path)) + 1))
        yield "late " + repr(path), changed
    for path in [
        ("mathematics", "placements"),
        ("mathematics", "placements", 0, "coefficient_decoder", 0),
        (*late, "full", "rows"),
        (*late, "marginalization", "rows", -1, "summed_full_state"),
    ]:
        changed = copy.deepcopy(original)
        set_path(changed, path, get_path(changed, path)[:-1])
        yield "truncated " + repr(path), changed
    for path in [
        ("mathematics", "geometry", "retained_indices", 1),
        ("mathematics", "placements", 0, "retained_rank"),
        ("be_restriction", "placements"),
    ]:
        changed = copy.deepcopy(original)
        set_path(changed, path, True)
        yield "native type " + repr(path), changed
    for key in original:
        changed = copy.deepcopy(original)
        del changed[key]
        yield "missing " + key, changed
    changed = copy.deepcopy(original)
    changed["private"] = "hidden"
    yield "extra private field", changed


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.study = load_module("study")
        self.directory = tempfile.TemporaryDirectory(prefix="det8-qr05bf-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.freeze = self.root / "freeze.json"
        self.capture_path = self.root / "capture.json"
        self.sources = {"synthetic/source.py": {"bytes": 1, "sha256": "a" * 64}}
        self.small = {
            "mathematics": {"exact": "1/3", "count": 1},
            "be_restriction": {"branches": 1},
        }
        source_mock = mock.patch.object(
            self.study, "source_identities", side_effect=lambda: copy.deepcopy(self.sources)
        )
        source_mock.start()
        self.addCleanup(source_mock.stop)
        self.study.freeze_source(self.freeze)

    def write_json(self, path, value):
        path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")

    def capture_small(self):
        with mock.patch.object(self.study, "analysis", return_value=copy.deepcopy(self.small)):
            return self.study.capture(self.capture_path, self.freeze)

    def replay_small(self, path=None):
        with mock.patch.object(self.study, "analysis", return_value=copy.deepcopy(self.small)):
            return self.study.replay(path or self.capture_path, self.freeze)

    def test_create_replay_and_readonly_identity(self):
        evidence = self.capture_small()
        exact_keys(self, evidence, "schema freeze sources analysis")
        self.assertEqual(evidence["schema"], "QR-05BF-evidence-v1")
        self.assertEqual(evidence["sources"], self.sources)
        self.assertEqual(evidence["analysis"], self.small)
        self.assertEqual(evidence["freeze"], self.study.identity(self.freeze))
        before = self.capture_path.read_bytes(), self.freeze.read_bytes()
        self.assertEqual(self.replay_small(), evidence)
        self.assertEqual((self.capture_path.read_bytes(), self.freeze.read_bytes()), before)

    def test_create_only_existing_paths_and_symlinks(self):
        self.capture_small()
        saved = self.capture_path.read_bytes(), self.freeze.read_bytes()
        for operation, path in (
            (self.study.capture, self.capture_path),
            (self.study.freeze_source, self.freeze),
        ):
            with (
                self.subTest(operation=operation.__name__),
                self.assertRaises((ValueError, FileExistsError)),
            ):
                operation(path)
        target = self.root / "absent.json"
        link = self.root / "dangling.json"
        link.symlink_to(target)
        with mock.patch.object(self.study, "analysis", return_value=self.small):
            with self.assertRaises((ValueError, FileExistsError)):
                self.study.capture(link, self.freeze)
            with self.assertRaises((ValueError, FileExistsError)):
                self.study.freeze_source(link)
        self.assertFalse(target.exists())
        self.assertTrue(link.is_symlink())
        self.assertEqual((self.capture_path.read_bytes(), self.freeze.read_bytes()), saved)

    def test_malformed_json_duplicates_nonfinite_and_size_limits(self):
        invalid = [
            b"",
            b"{",
            b"\xff",
            b'{"x":1,"x":2}',
            b'{"nested":{"x":1,"x":2}}',
            b"1.0",
            b"1e0",
            b"NaN",
            b"Infinity",
            b"-Infinity",
        ]
        for index, data in enumerate(invalid):
            path = self.root / ("bad-" + str(index) + ".json")
            path.write_bytes(data)
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.study.read_json(path)
            self.assertEqual(path.read_bytes(), data)
        with self.assertRaises(ValueError):
            self.study.read_json(self.root / "missing.json")
        with self.assertRaises(ValueError):
            self.study.read_json(self.root)
        link = self.root / "read-link.json"
        link.symlink_to(self.freeze)
        with self.assertRaises(ValueError):
            self.study.read_json(link)
        path = self.root / "sized.json"
        path.write_bytes(b"[0]")
        with mock.patch.object(self.study, "MAX_JSON_BYTES", 3):
            self.assertEqual(self.study.read_json(path), [0])
        with mock.patch.object(self.study, "MAX_JSON_BYTES", 2), self.assertRaises(ValueError):
            self.study.read_json(path)

    def test_freeze_schema_runtime_and_source_mutations(self):
        base = self.study.read_json(self.freeze)
        candidates = [None, [], {}, {**base, "extra": 0}, {**base, "schema": "wrong"}]
        for key, replacement in (
            ("python", ""),
            ("python", 3),
            ("implementation", None),
            ("optimized", True),
            ("optimized", -1),
            ("optimized", 3),
        ):
            changed = copy.deepcopy(base)
            changed["runtime_at_source_freeze"][key] = replacement
            candidates.append(changed)
        for key in ("schema", "sources", "runtime_at_source_freeze"):
            changed = copy.deepcopy(base)
            del changed[key]
            candidates.append(changed)
        changed = copy.deepcopy(base)
        changed["sources"]["synthetic/source.py"]["bytes"] = True
        candidates.append(changed)
        changed = copy.deepcopy(base)
        changed["sources"]["synthetic/source.py"]["sha256"] = "b" * 64
        candidates.append(changed)
        for index, changed in enumerate(candidates):
            path = self.root / ("bad-freeze-" + str(index) + ".json")
            self.write_json(path, changed)
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.study.capture(self.root / ("unused-" + str(index)), path)

    def test_evidence_header_and_complete_identity_mutations(self):
        base = self.capture_small()
        changes = [None, [], {}, {**base, "schema": "wrong"}, {**base, "extra": 0}]
        for key in base:
            changed = copy.deepcopy(base)
            del changed[key]
            changes.append(changed)
        for path, replacement in (
            (("freeze", "bytes"), True),
            (("freeze", "sha256"), "b" * 64),
            (("sources", "synthetic/source.py", "bytes"), True),
            (("sources", "synthetic/source.py", "sha256"), "b" * 64),
            (("analysis", "mathematics", "exact"), "2/6"),
            (("analysis", "mathematics", "count"), True),
            (("analysis", "be_restriction", "branches"), True),
        ):
            changed = copy.deepcopy(base)
            set_path(changed, path, replacement)
            changes.append(changed)
        for index, changed in enumerate(changes):
            path = self.root / ("bad-capture-" + str(index) + ".json")
            self.write_json(path, changed)
            before = path.read_bytes()
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.replay_small(path)
            self.assertEqual(path.read_bytes(), before)

    def test_changed_sources_before_and_during_creation_refused(self):
        self.sources["synthetic/source.py"]["bytes"] = 2
        with self.assertRaises(ValueError):
            self.capture_small()
        self.assertFalse(self.capture_path.exists())
        self.sources["synthetic/source.py"]["bytes"] = 1

        def change(_freeze):
            self.sources["synthetic/source.py"]["bytes"] = 2
            return copy.deepcopy(self.small)

        with (
            mock.patch.object(self.study, "analysis", side_effect=change),
            self.assertRaises(ValueError),
        ):
            self.study.capture(self.capture_path, self.freeze)
        self.assertFalse(self.capture_path.exists())

    def test_source_changes_during_freeze_refused(self):
        changed = copy.deepcopy(self.sources)
        changed["synthetic/source.py"]["bytes"] += 1
        path = self.root / "new-freeze.json"
        with (
            mock.patch.object(self.study, "source_identities", side_effect=[self.sources, changed]),
            self.assertRaises(ValueError),
        ):
            self.study.freeze_source(path)
        self.assertFalse(path.exists())

    def test_freeze_byte_changes_during_capture_and_replay_refused(self):
        before = self.freeze.read_bytes()

        def change(_freeze):
            self.freeze.write_bytes(before + b"\n")
            return copy.deepcopy(self.small)

        with (
            mock.patch.object(self.study, "analysis", side_effect=change),
            self.assertRaises(ValueError),
        ):
            self.study.capture(self.capture_path, self.freeze)
        self.assertFalse(self.capture_path.exists())
        self.freeze.write_bytes(before)
        self.capture_small()
        evidence_before = self.capture_path.read_bytes()
        with (
            mock.patch.object(self.study, "analysis", side_effect=change),
            self.assertRaises(ValueError),
        ):
            self.study.replay(self.capture_path, self.freeze)
        self.assertEqual(self.capture_path.read_bytes(), evidence_before)

    def test_failed_analysis_does_not_publish_or_replace_evidence(self):
        with (
            mock.patch.object(
                self.study, "analysis", side_effect=ValueError("declared failed comparison")
            ),
            self.assertRaises(ValueError),
        ):
            self.study.capture(self.capture_path, self.freeze)
        self.assertFalse(self.capture_path.exists())
        self.capture_small()
        before = self.capture_path.read_bytes()
        with (
            mock.patch.object(
                self.study, "analysis", side_effect=ValueError("declared failed replay")
            ),
            self.assertRaises(ValueError),
        ):
            self.study.replay(self.capture_path, self.freeze)
        self.assertEqual(self.capture_path.read_bytes(), before)

    def test_changed_published_bytes_are_rejected_and_retained(self):
        original_create = self.study._create_json

        def corrupt(path, value):
            identity = original_create(path, value)
            path.write_bytes(path.read_bytes() + b"\n")
            return identity

        with (
            mock.patch.object(self.study, "analysis", return_value=self.small),
            mock.patch.object(self.study, "_create_json", side_effect=corrupt),
            self.assertRaises(ValueError),
        ):
            self.study.capture(self.capture_path, self.freeze)
        self.assertTrue(self.capture_path.is_file())
        before = self.capture_path.read_bytes()
        with self.assertRaises((ValueError, FileExistsError)):
            self.study.capture(self.capture_path, self.freeze)
        self.assertEqual(self.capture_path.read_bytes(), before)

    def test_artifact_byte_change_during_replay_refused(self):
        self.capture_small()
        before = self.capture_path.read_bytes()

        def corrupt(_freeze):
            self.capture_path.write_bytes(before + b"\n")
            return copy.deepcopy(self.small)

        with (
            mock.patch.object(self.study, "analysis", side_effect=corrupt),
            self.assertRaises(ValueError),
        ):
            self.study.replay(self.capture_path, self.freeze)
        self.assertEqual(self.capture_path.read_bytes(), before + b"\n")

    def test_output_byte_cap_precedes_creation(self):
        path = self.root / "capped.json"
        with mock.patch.object(self.study, "MAX_JSON_BYTES", 1), self.assertRaises(ValueError):
            self.study._create_json(path, {"larger": "value"})
        self.assertFalse(path.exists())

    def test_complete_report_and_restriction_non_noop_mutations(self):
        study, _protocol, report = evaluated()
        with mock.patch.object(study, "compare_routes", return_value=report):
            expected = study.analysis()
        with mock.patch.object(self.study, "analysis", return_value=expected):
            evidence = self.study.capture(self.capture_path, self.freeze)
            before = self.capture_path.read_bytes()
            original_parse = self.study._parse_json
            count = 0
            for name, changed in analysis_mutations(expected):
                with self.subTest(case=name):
                    self.assertNotEqual(
                        self.study.canonical(changed), self.study.canonical(expected)
                    )
                    bad = copy.deepcopy(evidence)
                    bad["analysis"] = changed

                    # Inject only this parsed artifact; freeze/source reads use
                    # the real parser. Keep large field corruptions in memory.
                    def parse(data, mutation=bad):
                        return mutation if data == before else original_parse(data)

                    with (
                        mock.patch.object(self.study, "_parse_json", side_effect=parse),
                        self.assertRaises(ValueError),
                    ):
                        self.study.replay(self.capture_path, self.freeze)
                    self.assertEqual(self.capture_path.read_bytes(), before)
                    count += 1
            self.assertGreater(count, 50)

    def test_encoding_rejects_unsupported_native_types(self):
        for value in (0.0, float("nan"), float("inf"), (), {1: "bad"}, {"set": {1}}, b"bytes"):
            with self.subTest(value=repr(value)), self.assertRaises(ValueError):
                self.study.encode(value)
        self.assertFalse(self.study.same({"integer": 1}, {"integer": True}))
        self.assertEqual(self.study.encode(Fraction(2, 6)), "1/3")


def selected_be_fixture(study, report):
    """Create only selected BE-shaped data, not an old executor or oracle."""
    g = report["geometry"]
    center = next(p for p in report["placements"] if p["id"] == "center")
    previous = {
        "geometry": {
            "volume": g["volume"],
            "sigma": g["sigma"],
            "corner_weights": g["coefficient_integrals"][:4],
            "bubble_target": g["coefficient_integrals"][4],
            "evaluation_matrix": center["evaluation_matrix"],
            "coefficient_decoder": center["coefficient_decoder"],
            "repair_weights": center["full_weights"],
            "center_basis": center["basis"][:4],
            "bubble_at_center": center["basis"][4],
        },
        "reduction": {
            "target_weights": g["stale_weights"],
            "retained_indices": g["retained_indices"],
            "omitted_index": g["omitted_index"],
            **{
                key: center[key]
                for key in (
                    "retained_evaluation_matrix",
                    "retained_rank",
                    "omission_direction",
                    "retained_null_image",
                    "target_null_image",
                )
            },
        },
        "profiles": [],
        "operators": "not selected",
        "collision": "not selected",
        "off_model": "not selected",
        "observer": "not selected",
    }
    for current in center["profiles"][:4]:
        reduced = current["reduced"]
        target4 = {
            "rows": [
                {
                    "outcomes": row["outcomes"],
                    "probability": row["probability"],
                    "state_diagonal": row["state_diagonal"],
                    "estimate": row["candidate_estimate"],
                }
                for row in reduced["rows"]
            ],
            **reduced["candidate"],
        }
        previous["profiles"].append(
            {
                "id": current["id"],
                "corners": current["coefficients"][:4],
                "theta": current["coefficients"][4],
                **{
                    key: current[key]
                    for key in (
                        "admission_bound",
                        "sample_means",
                        "recovered_coefficients",
                        "target",
                    )
                },
                "plans": {
                    "repair5": current["full"],
                    "target4": target4,
                    "repeatcc5": "not selected",
                },
                "mse_differences": "not selected",
            }
        )
    return study.encode({"analysis": {"mathematics": previous}})


class HistoricalBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()

    def restriction(self, document, current=None):
        data = json.dumps(document, sort_keys=True).encode()
        identities = dict(self.study.BE_IDENTITIES)
        identities["results.json"] = hashlib.sha256(data).hexdigest()
        with (
            mock.patch.object(self.study, "_read_bounded", return_value=data),
            mock.patch.object(self.study, "BE_IDENTITIES", identities),
            mock.patch.object(
                self.study, "_load_engine", side_effect=AssertionError("historical executor")
            ),
        ):
            return self.study._be_restriction(self.report if current is None else current)

    def test_selected_be_overlap_excludes_old_observer_replication_and_off_model(self):
        document = selected_be_fixture(self.study, self.report)
        summary = {"status": "matched", "placements": 1, "profiles": 4, "plans": 2, "branches": 192}
        self.assertEqual(self.restriction(document), summary)
        changed = copy.deepcopy(document)
        old = changed["analysis"]["mathematics"]
        for key in ("operators", "collision", "off_model", "observer"):
            old[key] = None
        old["profiles"][0]["plans"]["repeatcc5"] = None
        old["profiles"][0]["mse_differences"] = None
        self.assertNotEqual(self.study.canonical(changed), self.study.canonical(document))
        self.assertEqual(self.restriction(changed), summary)

    def test_semantic_selected_history_mutations_are_wire_non_noops(self):
        document = selected_be_fixture(self.study, self.report)
        paths = [
            ("geometry", key) for key in ("volume", "sigma", "bubble_target", "bubble_at_center")
        ]
        paths += [
            ("geometry", key, 0) for key in ("corner_weights", "repair_weights", "center_basis")
        ]
        paths += [("geometry", key, -1, -1) for key in ("evaluation_matrix", "coefficient_decoder")]
        paths += [
            ("reduction", key, -1)
            for key in (
                "target_weights",
                "omission_direction",
                "retained_null_image",
            )
        ]
        paths += [
            ("reduction", "retained_evaluation_matrix", -1, -1),
            ("reduction", "target_null_image"),
        ]
        paths += [("profiles", -1, key) for key in ("theta", "admission_bound", "target")]
        paths += [
            ("profiles", -1, key, -1)
            for key in (
                "corners",
                "sample_means",
                "recovered_coefficients",
            )
        ]
        for plan in ("repair5", "target4"):
            prefix = ("profiles", -1, "plans", plan)
            paths += [(*prefix, key) for key in ("mean", "bias", "variance", "mse")]
            paths += [(*prefix, "rows", -1, key) for key in ("probability", "estimate")]
            paths += [(*prefix, "rows", -1, "state_diagonal", -1)]
        for path in paths:
            changed = copy.deepcopy(document)
            full = ("analysis", "mathematics", *path)
            set_path(changed, full, str(Fraction(get_path(changed, full)) + 1))
            self.assertNotEqual(self.study.canonical(changed), self.study.canonical(document))
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(changed)
        for path, value in (
            (("reduction", "retained_indices", 1), True),
            (("reduction", "omitted_index"), True),
            (("reduction", "retained_rank"), True),
            (("profiles", -1, "plans", "target4", "rows", -1, "outcomes", 0), True),
            (("profiles", -1, "plans", "repair5", "rows"), []),
        ):
            changed = copy.deepcopy(document)
            set_path(changed, ("analysis", "mathematics", *path), value)
            self.assertNotEqual(self.study.canonical(changed), self.study.canonical(document))
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(changed)

    def test_current_center_identity_and_both_reduced_estimators_are_checked(self):
        document = selected_be_fixture(self.study, self.report)
        center_index = next(
            i for i, p in enumerate(self.report["placements"]) if p["id"] == "center"
        )
        for path, value in (
            (("placements", center_index, "position", 0), Fraction(1, 3)),
            (("placements", center_index, "id"), "absent"),
            (("placements", center_index, "profiles", 0, "id"), "reordered"),
            (
                (
                    "placements",
                    center_index,
                    "profiles",
                    0,
                    "reduced",
                    "rows",
                    -1,
                    "stale_estimate",
                ),
                Fraction(7),
            ),
            (
                ("placements", center_index, "profiles", 0, "reduced", "candidate", "bias"),
                Fraction(7),
            ),
        ):
            current = copy.deepcopy(self.report)
            set_path(current, path, value)
            self.assertNotEqual(self.study.canonical(current), self.study.canonical(self.report))
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(document, current)
        duplicated = copy.deepcopy(self.report)
        duplicated["placements"].append(copy.deepcopy(duplicated["placements"][center_index]))
        with self.assertRaises(ValueError):
            self.restriction(document, duplicated)

    def test_historical_hash_precedes_semantic_parsing(self):
        with (
            mock.patch.object(self.study, "_read_bounded", return_value=b"{}"),
            mock.patch.object(
                self.study, "_parse_json", side_effect=AssertionError("unverified data")
            ),
            self.assertRaises(ValueError),
        ):
            self.study._be_restriction(self.report)

    def test_analysis_has_only_mathematics_and_selected_restriction(self):
        with mock.patch.object(self.study, "compare_routes", return_value=self.report):
            result = self.study.analysis()
        exact_keys(self, result, "mathematics be_restriction")
        self.assertEqual(result["mathematics"], self.study.encode(self.report))
        self.assertEqual(
            result["be_restriction"],
            {"status": "matched", "placements": 1, "profiles": 4, "plans": 2, "branches": 192},
        )


class SourceIdentityTests(unittest.TestCase):
    def test_exact_eleven_current_and_be_source_identities(self):
        study = load_module("study")
        actual = study.source_identities()
        current = [
            HERE / name
            for name in (
                "README.md",
                "protocol.json",
                "quantum.py",
                "reference.py",
                "study.py",
                "test_qr05bf.py",
            )
        ]
        previous = [
            HERE.parent / "qr-05be-target-specific-measurement-reduction-2026-09-08" / name
            for name in (
                "README.md",
                "RESULTS.md",
                "protocol.json",
                "source-freeze.json",
                "results.json",
            )
        ]
        self.assertEqual(len(actual), 11)
        self.assertEqual(set(actual), {str(p.relative_to(study.REPO)) for p in current + previous})
        for path in current + previous:
            data = path.read_bytes()
            self.assertEqual(
                actual[str(path.relative_to(study.REPO))],
                {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()},
            )
        self.assertEqual(study.read_json(study.FREEZE_PATH)["sources"], actual)

    def test_protocol_hash_and_parse_share_one_snapshot(self):
        study = load_module("study")
        data = (HERE / "protocol.json").read_bytes()
        with (
            mock.patch.object(study, "_read_bounded", return_value=data) as read,
            mock.patch.object(study, "_bytes_identity", wraps=study._bytes_identity) as hashed,
            mock.patch.object(study, "_parse_json", wraps=study._parse_json) as parsed,
        ):
            self.assertEqual(study.load_protocol(), json.loads(data))
        self.assertEqual(read.call_count, 1)
        self.assertEqual(hashed.call_count, 1)
        self.assertEqual(parsed.call_count, 1)
        self.assertIs(hashed.call_args.args[0], data)
        self.assertIs(parsed.call_args.args[0], data)
        with (
            mock.patch.object(study, "_read_bounded", return_value=b"{}"),
            mock.patch.object(
                study, "_parse_json", side_effect=AssertionError("unverified protocol")
            ),
            self.assertRaises(ValueError),
        ):
            study.load_protocol()

    def test_authenticated_protocol_native_selection_and_menu_checks(self):
        study = load_module("study")
        protocol = json.loads((HERE / "protocol.json").read_bytes())
        for path, value in (
            (("retained_indices", 1), True),
            (("omitted_index",), True),
            (("stations", 4), "unknown"),
            (("placements",), []),
            (("profiles",), []),
        ):
            changed = copy.deepcopy(protocol)
            set_path(changed, path, value)
            data = json.dumps(changed).encode()
            with (
                self.subTest(path=path),
                mock.patch.object(study, "_read_bounded", return_value=data),
                mock.patch.object(
                    study, "_bytes_identity", return_value={"sha256": PROTOCOL_SHA256}
                ),
                self.assertRaises(ValueError),
            ):
                study.load_protocol()


if __name__ == "__main__":
    unittest.main()
