"""Finite T5 transport regressions with fixed laws and independent ticket counts.

Loads this checkout's model directly, without importing the DET package.
"""
import math
from pathlib import Path
import sys
import unittest
from fractions import Fraction as F

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'models'))
import kernel_continuum as kc


class TransportTests(unittest.TestCase):
    def generator(self, n, drift):
        q = kc.make_nearest_neighbor_kernel(n, 1.0, 0.25, drift)
        return q, kc.graph_laplacian_generator(q, 0.25)["M"]

    def test_frozen_endpoint_laws_and_legacy_negative_control(self):
        q, m = self.generator(2, 0.25)
        self.assertEqual(q, [[11 / 16, 5 / 16], [3 / 16, 13 / 16]])
        self.assertEqual(kc.diffuse([1, 0], m, 0.25, 1), [11 / 16, 5 / 16])
        self.assertEqual(kc.diffuse([0, 1], m, 0.25, 1), [3 / 16, 13 / 16])
        legacy = [q[0][0], q[1][0]]
        self.assertEqual(sum(legacy), 7 / 8)
        self.assertNotEqual(legacy, kc.diffuse([1, 0], m, 0.25, 1))
        _, m = self.generator(3, 0.25)
        for start, expected in enumerate(([11 / 16, 5 / 16, 0],
                                          [3 / 16, 1 / 2, 5 / 16],
                                          [0, 3 / 16, 13 / 16])):
            p = [int(i == start) for i in range(3)]
            self.assertEqual(kc.diffuse(p, m, 0.25, 1), list(expected))

    def test_all_135_fixed_laws_against_ticket_counts(self):
        cells = 0
        # No matrix multiplication in the oracle. Each of 16 equiprobable
        # tickets moves right/left when that neighbour exists, else stays.
        for n in (2, 3):
            for drift, right, left in ((-0.25, 3, 5), (0.0, 4, 4), (0.25, 5, 3)):
                _, m = self.generator(n, drift)
                for start in range(n):
                    counts = [int(i == start) for i in range(n)]
                    p0 = counts[:]
                    for k in range(9):
                        with self.subTest(n=n, drift=drift, start=start, k=k):
                            expected = [float(F(v, 16 ** k)) for v in counts]
                            actual = kc.diffuse(p0, m, 0.25, k)
                            self.assertEqual(actual, expected)
                            self.assertEqual(sum(counts), 16 ** k)
                            self.assertEqual(sum(actual), 1.0)
                            self.assertGreaterEqual(min(actual), 0.0)
                            cells += 1
                        if k == 8:
                            break
                        next_counts = [0] * n
                        for site, count in enumerate(counts):
                            for ticket in range(16):
                                target = site
                                if ticket < right and site + 1 < n:
                                    target += 1
                                elif right <= ticket < right + left and site > 0:
                                    target -= 1
                                next_counts[target] += count
                        counts = next_counts
        self.assertEqual(cells, 135)

    def test_six_frozen_stationary_laws_and_balance(self):
        laws = {(2, -0.25): (F(5, 8), F(3, 8)),
                (2, 0.0): (F(1, 2), F(1, 2)),
                (2, 0.25): (F(3, 8), F(5, 8)),
                (3, -0.25): (F(25, 49), F(15, 49), F(9, 49)),
                (3, 0.0): (F(1, 3), F(1, 3), F(1, 3)),
                (3, 0.25): (F(9, 49), F(15, 49), F(25, 49))}
        for (n, drift), law in laws.items():
            with self.subTest(n=n, drift=drift):
                q, m = self.generator(n, drift)
                self.assertEqual(sum(law), 1)
                actual = kc.diffuse(list(law), m, 0.25, 8)
                for value, expected in zip(actual, law):
                    self.assertAlmostEqual(value, float(expected), delta=1e-14)
                for i in range(n - 1):
                    self.assertEqual(law[i] * F(q[i][i + 1]), law[i + 1] * F(q[i + 1][i]))
                uniform = [1.0 / n] * n
                after = kc.diffuse(uniform, m, 0.25, 1)
                if drift == 0:
                    for a, b in zip(after, uniform):
                        self.assertAlmostEqual(a, b, delta=1e-15)
                else:
                    self.assertGreater(max(abs(a - b) for a, b in zip(after, uniform)), 0.01)

    def test_signed_local_moments_including_all_endpoints(self):
        sites = 0
        for n in (2, 3):
            for drift, right, left in ((-0.25, 3, 5), (0.0, 4, 4), (0.25, 5, 3)):
                _, m = self.generator(n, drift)
                for source in range(n):
                    # Place each source at the fixed public reference index,
                    # retaining its actual coordinate and all outgoing targets.
                    order = [i for i in range(n) if i != source]
                    order.insert(n // 2, source)
                    permuted = [[m[i][j] for j in order] for i in order]
                    result = kc.continuum_coefficients(permuted, order)
                    r = right if source + 1 < n else 0
                    l = left if source > 0 else 0
                    self.assertEqual(result["drift"], (r - l) / 4)
                    self.assertEqual(result["diffusion"], (r + l) / 8)
                    p = [int(i == source) for i in range(n)]
                    law = kc.diffuse(p, m, 0.25, 1)
                    mean = sum((i - source) * law[i] for i in range(n))
                    raw_second = sum((i - source) ** 2 * law[i] for i in range(n))
                    self.assertEqual(mean, (r - l) / 16)
                    self.assertEqual(raw_second, (r + l) / 16)
                    sites += 1
        self.assertEqual(sites, 15)

    def test_symmetric_spectral_and_finite_discrete_fit(self):
        q = kc.make_nearest_neighbor_kernel(5, 1, 0.1)
        m = kc.graph_laplacian_generator(q, 0.1)["M"]
        self.assertAlmostEqual(kc.spectral_gap(m), 2 * (1 - math.cos(math.pi / 5)), delta=1e-9)
        m2 = [[-1.0, 1.0], [1.0, -1.0]]
        exact_discrete = -math.log(0.75) / 0.125
        fit = kc.measure_relaxation_rate(m2, 0.125, 12)
        self.assertAlmostEqual(fit, exact_discrete, delta=1e-10)
        self.assertGreater(abs(fit - kc.spectral_gap(m2)), 0.1)
        _, biased = self.generator(3, 0.25)
        for call in (lambda: kc.spectral_gap(biased),
                     lambda: kc.measure_relaxation_rate(biased, 0.25, 8)):
            with self.assertRaises(ValueError):
                call()
        disconnected = [[-1, 1, 0], [1, -1, 0], [0, 0, 0]]
        self.assertEqual(kc.spectral_gap(disconnected), 0.0)
        with self.assertRaises(ValueError):
            kc.measure_relaxation_rate(disconnected, 0.25, 8)
        with self.assertRaises(ValueError):
            kc.measure_relaxation_rate(m2, 0.5, 8)  # mode annihilated, no log fit
        self.assertAlmostEqual(kc.measure_relaxation_rate(m2, 1.0, 8), 0.0, delta=1e-15)

    def test_declared_degenerate_cases(self):
        self.assertEqual(kc.make_nearest_neighbor_kernel(1, 1, 8, 0.25), [[1.0]])
        self.assertEqual(kc.graph_laplacian_generator([[1]], 0.25)["M"], [[0.0]])
        self.assertEqual(kc.continuum_coefficients([[0]], [9])["diffusion"], 0.0)
        self.assertEqual(kc.diffuse([1], [[0]], 0, 8), [1.0])
        identity = [[1.0, 0.0], [0.0, 1.0]]
        self.assertEqual(kc.make_nearest_neighbor_kernel(2, 0, 0.25), identity)
        self.assertEqual(kc.make_nearest_neighbor_kernel(2, 1, 0, 0.25), identity)
        zero = [[0.0, 0.0], [0.0, 0.0]]
        self.assertEqual(kc.spectral_gap(zero), 0.0)
        self.assertEqual(kc.measure_relaxation_rate(zero, 0.25, 3), 0.0)
        self.assertEqual(kc.diffuse([0.25, 0.75], [[-1, 1], [1, -1]], 0, 8), [0.25, 0.75])
        with self.assertRaises(ValueError):
            kc.graph_laplacian_generator(identity, 0)
        with self.assertRaises(ValueError):
            kc.measure_relaxation_rate(zero, 0, 3)
        one_way = kc.make_nearest_neighbor_kernel(2, 1, 0.25, 1)
        self.assertEqual(one_way, [[0.5, 0.5], [0.0, 1.0]])
        periodic = kc.graph_laplacian_generator([[0, 1], [1, 0]], 1)["M"]
        self.assertEqual(kc.diffuse([1, 0], periodic, 1, 8), [1.0, 0.0])

    def test_constructor_and_extractor_reject_invalid_domains(self):
        cases = [(0, 1, 0.25, 0), (True, 1, 0.25, 0), (2.0, 1, 0.25, 0),
                 (2, -1, 0.25, 0), (2, 1, 0.25, 2), (2, math.inf, 0.25, 0),
                 (2, 1, math.nan, 0), (2, 1, -0.1, 0), (3, 1, 0.51, 0),
                 (2, 1, 0.81, 0.25)]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                kc.make_nearest_neighbor_kernel(*args)
        for q in ([], [[1, 0]], [[math.nan]], [[-0.1, 1.1], [0, 1]],
                  [[0.5, 0.25], [0.25, 0.75]], [[11 / 16, 3 / 16], [5 / 16, 13 / 16]]):
            with self.subTest(q=q), self.assertRaises(ValueError):
                kc.graph_laplacian_generator(q, 0.25)

    def test_evolution_and_helpers_reject_bad_shapes_values_steps(self):
        m = [[-1, 1], [1, -1]]
        for p in ([1], [-0.1, 1.1], [0.5, 0.25], [math.nan, 0], []):
            with self.subTest(p=p), self.assertRaises(ValueError):
                kc.diffuse(p, m, 0.25, 0)
        for bad in ([], [[0, 0]], [[math.inf]], [[1, -1], [0, 0]], [[-2, 1], [1, -1]]):
            with self.subTest(m=bad), self.assertRaises(ValueError):
                kc.diffuse([1, 0], bad, 0.25, 0)
        for steps in (-1, 0.5, True, math.inf):
            with self.subTest(steps=steps), self.assertRaises(ValueError):
                kc.diffuse([1, 0], m, 0.25, steps)
        for eps in (-1, math.nan, 1.01):
            with self.subTest(eps=eps), self.assertRaises(ValueError):
                kc.diffuse([1, 0], m, eps, 1)
        for positions in ([0], [0, math.inf]):
            with self.assertRaises(ValueError):
                kc.continuum_coefficients(m, positions)
        with self.assertRaises(ValueError):
            kc.measure_relaxation_rate(m, 0.25, 2)

    def test_tiny_one_way_rejection_and_scaled_symmetric_control(self):
        a = 2.0 ** -44
        one_way = [[-a, a], [0.0, 0.0]]
        eps = 2.0 ** 44
        with self.assertRaises(ValueError):
            kc.spectral_gap(one_way)
        with self.assertRaises(ValueError):
            kc.measure_relaxation_rate(one_way, eps, 8)
        q = kc.make_nearest_neighbor_kernel(2, a / 2, eps, a / 2)
        self.assertEqual(q, [[0.0, 1.0], [0.0, 1.0]])
        extracted = kc.graph_laplacian_generator(q, eps)
        self.assertEqual(extracted["M"], one_way)
        self.assertTrue(extracted["zero_row_sums"])
        self.assertFalse(extracted["symmetric"])
        self.assertFalse(extracted["is_laplacian"])

        symmetric = [[-a, a], [a, -a]]
        gap = kc.spectral_gap(symmetric)
        self.assertGreater(gap, 0.0)
        # Rescaled assertion: returning zero cannot pass just because a is tiny.
        self.assertAlmostEqual(gap / a, 2.0, delta=1e-12)
        small_step = 0.125 / a
        qs = kc.make_nearest_neighbor_kernel(2, a, small_step)
        gs = kc.graph_laplacian_generator(qs, small_step)
        self.assertEqual(gs["M"], symmetric)
        self.assertTrue(gs["symmetric"])
        self.assertTrue(gs["is_laplacian"])
        fit = kc.measure_relaxation_rate(symmetric, small_step, 12)
        self.assertAlmostEqual(fit / a, -math.log(0.75) / 0.125, delta=1e-10)
        zero = [[0.0, 0.0], [0.0, 0.0]]
        self.assertEqual(kc.spectral_gap(zero), 0.0)
        self.assertEqual(kc.measure_relaxation_rate(zero, eps, 8), 0.0)
        gz = kc.graph_laplacian_generator([[1, 0], [0, 1]], eps)
        self.assertTrue(gz["zero_row_sums"] and gz["symmetric"] and gz["is_laplacian"])

    def test_tiny_row_balance_has_no_absolute_rate_floor(self):
        a = 2.0 ** -44
        # A one-way edge is valid only when its source loses the same mass.
        for invalid in ([[0.0, a], [0.0, 0.0]], [[-a, 0.0], [0.0, 0.0]]):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                kc.diffuse([1.0, 0.0], invalid, 2.0 ** 44, 0)
            with self.assertRaises(ValueError):
                kc.spectral_gap(invalid)
            with self.assertRaises(ValueError):
                kc.measure_relaxation_rate(invalid, 2.0 ** 44, 8)
        # A dimensionless Q-row rounding tolerance must not hide the extracted
        # generator's entirely unbalanced tiny outgoing rate.
        with self.assertRaises(ValueError):
            kc.graph_laplacian_generator([[1.0, a], [0.0, 1.0]], 1.0)

    def test_run_t5_full_law_and_honest_separate_comparisons(self):
        result = kc.run_t5(n=3, w=1, eps=0.25, drift=0.25, n_steps=1)
        self.assertEqual(result["final_probabilities"], [3 / 16, 1 / 2, 5 / 16])
        self.assertEqual(result["final_probability_mass"], 1.0)
        self.assertTrue(result["final_nonnegative"])
        self.assertEqual(result["empirical_mean"], 1 / 8)
        self.assertEqual(result["empirical_variance"], 31 / 64)
        self.assertEqual(result["predicted_variance"], 31 / 64)
        self.assertEqual(result["relaxation_experiment"]["n"], 21)
        self.assertEqual(result["relaxation_experiment"]["drift"], 0.0)
        self.assertTrue(result["relaxation_experiment"]["separate_from_transport"])
        self.assertIn("synthetic", result["quantity_labels"]["empirical"])
        self.assertIn("not_derived_here", result["certificate"])
        zero = kc.run_t5(n=1, w=0, eps=0.25, n_steps=0)
        self.assertEqual(zero["final_probabilities"], [1.0])
        self.assertEqual(zero["spectral_gap_measured"], 0.0)
        for args in ({"eps": 0}, {"n": 2, "eps": 0.75}):
            with self.assertRaises(ValueError):
                kc.run_t5(**args)


if __name__ == "__main__":
    unittest.main()
