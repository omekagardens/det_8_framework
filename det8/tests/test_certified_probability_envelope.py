"""Deterministic invented rational envelopes only; no sampling or native data."""

from dataclasses import FrozenInstanceError
from decimal import Decimal
from fractions import Fraction as F
from itertools import permutations, product
import unittest
from unittest.mock import patch

from det8.models.certified_categorical_map import CategoricalMap
from det8.models.certified_probability_envelope import (
    EnvelopeResourceLimits, MAX_INTERMEDIATE_BITS, MAX_WORK_BITS,
    certify_probability_envelope,
)


class TestProbabilityEnvelope(unittest.TestCase):
    def make(self, lower, upper, **kwargs):
        return certify_probability_envelope(tuple(str(i) for i in range(len(lower))),
                                            lower, upper, **kwargs)

    def certificate(self, result):
        self.assertEqual(result.status, "CONDITIONAL_PROXY_CERTIFICATE")
        self.assertEqual(result.operational_admission, "ABSTAIN")
        self.assertIsNotNone(result.certificate)
        return result.certificate

    def test_documented_example_witnesses_and_map_interface(self):
        r = self.make([F(1, 5), F(1, 10), 0], [F(3, 5), F(1, 2), F(1, 5)],
                      proxy_budget=F(3, 16), provenance_reference="synthetic example; unverified")
        c = self.certificate(r)
        self.assertEqual(c.common_denominator, 10)
        self.assertEqual(c.original_lower_numerators, (2, 1, 0))
        self.assertEqual(c.original_upper_numerators, (6, 5, 2))
        self.assertEqual(c.lower_numerators, (3, 2, 0))
        self.assertEqual(c.upper_numerators, (6, 5, 2))
        self.assertEqual((c.lower_total, c.upper_total, c.lower_slack,
                          c.upper_slack, c.total_slack), (5, 13, 5, 3, 8))
        self.assertEqual(c.proxy_weights, (F(39, 80), F(31, 80), F(1, 8)))
        self.assertEqual(c.tv_bound, F(3, 16))
        self.assertEqual(c.budget_comparison_products, (48, 48))
        target = (F(3, 5), F(1, 5), F(1, 5))
        self.assertEqual(sum(abs(p - q) for p, q in zip(target, c.proxy_weights)) / 2,
                         c.tv_bound)
        mapping = CategoricalMap(c.proxy_weights, 3)
        self.assertEqual(mapping.cell_counts, (4, 3, 1))
        self.assertEqual(mapping.rounding_tv, F(1, 80))
        self.assertEqual(c.tv_bound + mapping.rounding_tv + F(1, 100), F(21, 100))
        self.assertEqual(r.provenance_reference, "synthetic example; unverified")

    def test_singletons_zero_width_and_forced_zero_outcomes(self):
        c = self.certificate(self.make([0, F(2, 5), F(3, 5)], [0, F(2, 5), F(3, 5)], proxy_budget=0))
        self.assertEqual(c.proxy_weights, (0, F(2, 5), F(3, 5)))
        self.assertEqual((c.total_slack, c.tv_bound), (0, 0))
        r = self.make([0, 1], [F(4, 5), 1], proxy_budget=0)
        c = self.certificate(r)
        self.assertEqual(r.outcomes, ("0", "1"))
        self.assertEqual(c.tightened_upper, (0, 1))
        self.assertEqual(c.proxy_weights, (0, 1))
        self.assertEqual(c.tv_bound, 0)
        c = self.certificate(self.make([0], [1]))
        self.assertEqual(c.proxy_weights, (1,))
        self.assertEqual(c.tv_bound, 0)
        self.assertIsNone(c.budget_comparison_products)

    def test_unnormalized_endpoints_are_allowed_without_rescaling(self):
        c = self.certificate(self.make([0, 0], [F(3, 4), F(3, 4)]))
        self.assertEqual(c.tightened_lower, (F(1, 4), F(1, 4)))
        self.assertEqual(c.proxy_weights, (F(1, 2), F(1, 2)))
        self.assertEqual(c.tv_bound, F(1, 4))

    def test_infeasible_lower_and_upper_totals(self):
        for lower, upper in [([F(3, 5)] * 2, [F(4, 5)] * 2),
                             ([0, 0], [F(2, 5)] * 2), ([0], [0])]:
            with self.subTest(lower=lower, upper=upper):
                r = self.make(lower, upper)
                self.assertEqual(r.status, "INFEASIBLE_ENVELOPE")
                self.assertIsNone(r.certificate)
                self.assertIsNone(r.compared_tv_bound)
                self.assertEqual(r.operational_admission, "ABSTAIN")

    def test_tiny_and_zero_budgets_are_exact(self):
        z = F(1, 10**6)
        lower, upper = [F(1, 2) - z] * 2, [F(1, 2) + z] * 2
        c = self.certificate(self.make(lower, upper, proxy_budget=z))
        self.assertEqual(c.tv_bound, z)
        self.assertEqual(c.proxy_weights, (F(1, 2), F(1, 2)))
        for budget in (z / 2, 0):
            r = self.make(lower, upper, proxy_budget=budget)
            self.assertEqual(r.status, "ABSTAIN_BUDGET")
            self.assertEqual(r.compared_tv_bound, z)
            self.assertIsNone(r.certificate)
            self.assertEqual(r.operational_admission, "ABSTAIN")
        c = self.certificate(self.make([F(1, 2)] * 2, [F(1, 2)] * 2, proxy_budget=0))
        self.assertEqual(c.tv_bound, 0)

    def test_budget_failure_does_not_claim_optimality(self):
        r = self.make([0, 0, 0], [F(1, 5), F(9, 10), F(9, 10)], proxy_budget=F(9, 20))
        self.assertEqual(r.status, "ABSTAIN_BUDGET")
        self.assertEqual(r.compared_tv_bound, F(1, 2))
        self.assertIsNone(r.certificate)
        c = self.certificate(self.make([0, 0, 0], [F(1, 5), F(9, 10), F(9, 10)]))
        self.assertEqual(c.proxy_weights, (F(1, 10), F(9, 20), F(9, 20)))
        # A finite witness exhibits a smaller realized distance, not a global
        # minimax claim or a reason to override the bound returned by the API.
        point = (F(1, 10), F(9, 10), 0)
        self.assertEqual(sum(abs(p-q) for p, q in zip(point, c.proxy_weights))/2, F(9, 20))

    def test_comparison_preflight_counterexample_before_lcm(self):
        lower, upper = [F(1, 3)] * 2, [F(2, 3)] * 2
        budget = F(1, 2**255 - 19)
        # C=21 alone is insufficient to admit the independent 255-bit budget.
        with patch("det8.models.certified_probability_envelope.gcd",
                   side_effect=AssertionError("LCM must not run before refusal")):
            r = self.make(lower, upper, proxy_budget=budget,
                          resource_limits=EnvelopeResourceLimits(max_intermediate_bits=21))
        self.assertEqual(r.status, "ABSTAIN_RESOURCE")
        self.assertEqual(r.resource_plan.construction_bits, 21)
        self.assertEqual(r.resource_plan.comparison_bits, 277)
        self.assertIsNone(r.certificate)
        accepted_precision = self.make(lower, upper, proxy_budget=budget,
                                       resource_limits=EnvelopeResourceLimits(max_intermediate_bits=277))
        self.assertEqual(accepted_precision.status, "ABSTAIN_BUDGET")
        self.assertEqual(accepted_precision.compared_tv_bound, F(1, 6))

    def test_resource_boundaries_and_storage_policy(self):
        base = self.make([F(1, 3)] * 2, [F(2, 3)] * 2)
        plan = base.resource_plan
        self.assertEqual(plan.comparison_bits, 0)
        self.assertEqual(plan.integer_slots, 128)
        self.assertEqual(plan.work_bits, 128 * 256)
        self.certificate(self.make([F(1, 3)] * 2, [F(2, 3)] * 2,
                                   resource_limits=EnvelopeResourceLimits(plan.construction_bits, plan.work_bits)))
        for limits in (EnvelopeResourceLimits(plan.construction_bits - 1, plan.work_bits),
                       EnvelopeResourceLimits(plan.construction_bits, plan.work_bits - 1),
                       EnvelopeResourceLimits(0, 0)):
            with self.subTest(limits=limits), patch("det8.models.certified_probability_envelope.gcd",
                     side_effect=AssertionError("large arithmetic must not run")):
                r = self.make([F(1, 3)] * 2, [F(2, 3)] * 2, resource_limits=limits)
                self.assertEqual(r.status, "ABSTAIN_RESOURCE")
                self.assertIsNone(r.certificate)

    def test_derived_consumer_precision_blowup_is_refused(self):
        p, q = 2**255 - 19, 2**255 - 31
        upper = (1 - F(1, p), 1 - F(1, q))
        independent_weight = (1 + F(1, q) - F(1, p)) / 2
        self.assertGreater(independent_weight.denominator.bit_length(), 256)
        r = self.make((0, 0), upper)
        self.assertEqual(r.status, "ABSTAIN_RESOURCE")
        self.assertIn("categorical-map weight precision", r.reason)
        self.assertIsNone(r.certificate)
        self.assertIsNone(r.compared_tv_bound)

    def test_permutation_equivariance(self):
        lower = (F(1, 5), F(1, 10), 0)
        upper = (F(3, 5), F(1, 2), F(1, 5))
        base = self.certificate(self.make(lower, upper))
        for order in permutations(range(3)):
            c = self.certificate(certify_probability_envelope(tuple(str(i) for i in order),
                tuple(lower[i] for i in order), tuple(upper[i] for i in order)))
            self.assertEqual(c.proxy_weights, tuple(base.proxy_weights[i] for i in order))
            self.assertEqual(c.tv_bound, base.tv_bound)

    def test_independent_finite_feasible_points_and_event_tv(self):
        # Six intervals on {0,1/2,1}, 216 boxes. Points are independently
        # enumerated quarter-grid normalized triples; all eight event errors
        # realize finite-space TV. This does not prove the all-real-P theorem.
        grid = (F(0), F(1, 2), F(1))
        intervals = [(lo, hi) for lo in grid for hi in grid if lo <= hi]
        points = [tuple(F(v, 4) for v in (i, j, 4-i-j))
                  for i in range(5) for j in range(5-i)]
        feasible_boxes = point_checks = 0
        for box in product(intervals, repeat=3):
            lower, upper = tuple(x[0] for x in box), tuple(x[1] for x in box)
            feasible = [p for p in points if all(lo <= v <= hi for lo, v, hi in zip(lower, p, upper))]
            r = self.make(lower, upper)
            if not feasible:
                self.assertEqual(r.status, "INFEASIBLE_ENVELOPE")
                continue
            feasible_boxes += 1
            c = self.certificate(r)
            self.assertEqual(sum(c.proxy_weights), 1)
            self.assertTrue(all(lo <= v <= hi for lo, v, hi in zip(lower, c.proxy_weights, upper)))
            for point in points:
                original = all(lo <= v <= hi for lo, v, hi in zip(lower, point, upper))
                tightened = all(lo <= v <= hi for lo, v, hi in zip(c.tightened_lower, point, c.tightened_upper))
                self.assertEqual(original, tightened)
                if not original:
                    continue
                point_checks += 1
                delta = tuple(p-q for p, q in zip(point, c.proxy_weights))
                event_supremum = max(abs(sum(delta[i] for i in range(3) if mask & (1 << i)))
                                     for mask in range(8))
                self.assertEqual(event_supremum, sum(abs(x) for x in delta)/2)
                self.assertLessEqual(event_supremum, c.tv_bound)
        self.assertGreater(feasible_boxes, 100)
        self.assertGreater(point_checks, 200)

    def test_immutable_outputs_input_copy_and_unverified_provenance(self):
        outcomes, lower, upper = ["a", "b"], [0, 0], [1, 1]
        r = certify_probability_envelope(outcomes, lower, upper, provenance_reference="not authenticated")
        c = self.certificate(r)
        outcomes[0], lower[0], upper[0] = "changed", 1, 0
        self.assertEqual(r.outcomes, ("a", "b"))
        self.assertEqual(r.lower, (0, 0))
        self.assertEqual(r.upper, (1, 1))
        self.assertEqual(r.provenance_reference, "not authenticated")
        with self.assertRaises(FrozenInstanceError):
            r.status = "PASS"
        with self.assertRaises(FrozenInstanceError):
            c.tv_bound = F(0)
        with self.assertRaises(FrozenInstanceError):
            r.resource_plan.work_bits = 0

    def test_strict_rational_inputs_and_reduced_pairs(self):
        c = self.certificate(self.make([(0, 1), (1, 1)], [(0, 1), (1, 1)], proxy_budget=(0, 1)))
        self.assertEqual(c.proxy_weights, (0, 1))
        for bad in (0.5, Decimal("0.5"), "1/2", True, None, [1, 2], (1,), (1, 2, 3), (True, 2)):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                self.make([bad], [1])
        for bad in (-1, 2, F(-1, 2), F(3, 2), (1, 0), (1, -2), (2, 4), (0, 2),
                    (1, 2**256), 2**256):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.make([bad], [1])
        for bad in (True, 0.5, Decimal("0.5"), "1", (1, 2, 3)):
            with self.subTest(budget=bad), self.assertRaises(TypeError):
                self.make([0], [1], proxy_budget=bad)
        for bad in (-1, 2, (2, 4), F(1, 2**256)):
            with self.subTest(budget=bad), self.assertRaises(ValueError):
                self.make([0], [1], proxy_budget=bad)
        with self.assertRaises(ValueError):
            self.make([F(3, 4)], [F(1, 2)])

    def test_no_implicit_numeric_container_or_identifier_adapters(self):
        class IntLike(int):
            pass
        class FractionLike(F):
            pass
        class ListLike(list):
            pass
        class StringLike(str):
            pass
        for bad in (IntLike(0), FractionLike(0)):
            with self.assertRaises(TypeError):
                self.make([bad], [1])
        for bad in (None, "0", iter((0,)), ListLike([0])):
            with self.assertRaises(TypeError):
                certify_probability_envelope(("a",), bad, (1,))
        for bad in ((1,), (True,), (StringLike("a"),)):
            with self.assertRaises(TypeError):
                certify_probability_envelope(bad, (0,), (1,))
        for bad in (("",), ("a" * 129,), ("a", "a"), ()):
            with self.assertRaises(ValueError):
                certify_probability_envelope(bad, (0,) * len(bad), (1,) * len(bad))
        with self.assertRaises(ValueError):
            certify_probability_envelope(("a",), (), (1,))
        for bad in (True, StringLike("ref"), 1):
            with self.assertRaises(TypeError):
                self.make([0], [1], provenance_reference=bad)
        for bad in ("", "r" * 1025):
            with self.assertRaises(ValueError):
                self.make([0], [1], provenance_reference=bad)

    def test_profile_boundaries(self):
        tiny = F(1, 2**256 - 1)
        c = self.certificate(self.make((tiny, 1-tiny), (tiny, 1-tiny), proxy_budget=tiny))
        self.assertEqual(c.proxy_weights, (tiny, 1-tiny))
        CategoricalMap(c.proxy_weights, 0)
        r = self.make((F(1, 256),) * 256, (F(1, 256),) * 256)
        c = self.certificate(r)
        self.assertEqual(len(c.proxy_weights), 256)
        self.assertEqual(c.tv_bound, 0)
        with self.assertRaises(ValueError):
            self.make((0,) * 257, (1,) * 257)
        for limits in ({}, True, (1, 2)):
            with self.assertRaises(TypeError):
                self.make([0], [1], resource_limits=limits)
        for value in (True, F(1), 1.0):
            with self.assertRaises(TypeError):
                EnvelopeResourceLimits(max_intermediate_bits=value)
        for kwargs in ({"max_intermediate_bits": -1}, {"max_intermediate_bits": MAX_INTERMEDIATE_BITS+1},
                       {"max_work_bits": -1}, {"max_work_bits": MAX_WORK_BITS+1}):
            with self.assertRaises(ValueError):
                EnvelopeResourceLimits(**kwargs)


if __name__ == "__main__":
    unittest.main()
