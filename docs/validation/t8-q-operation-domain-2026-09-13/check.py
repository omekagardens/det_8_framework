"""Exact finite witnesses for OPERATION_DOMAIN.md, not a native operation law.

The universal complex-Hermitian argument belongs to the accompanying note.
These rational real-symmetric examples illustrate its hypotheses and boundary
cases; they do not establish universal coverage, select physical operations,
reconstruct quantum mechanics, or supply an executor. No DET8 modules, supplied
quantum instruments, floating-point tolerances, or external libraries are used.

Run directly with Python, including ``python -O check.py``. All substantive
checks use unittest assertions, which remain active under optimization.
"""

import unittest
from fractions import Fraction as F
from itertools import pairwise

Matrix = tuple[tuple[F, ...], ...]


def matrix(rows) -> Matrix:
    return tuple(tuple(F(value) for value in row) for row in rows)


def transpose(a: Matrix) -> Matrix:
    return tuple(zip(*a, strict=True))


def add(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(x + y for x, y in zip(ar, br, strict=True)) for ar, br in zip(a, b, strict=True)
    )


def scale(c: F, a: Matrix) -> Matrix:
    return tuple(tuple(c * x for x in row) for row in a)


def multiply(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum((x * y for x, y in zip(row, col, strict=True)), F(0)) for col in transpose(b))
        for row in a
    )


def outer(v: tuple[F, ...]) -> Matrix:
    return matrix(tuple(tuple(x * y for y in v) for x in v))


def tensor(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(x * y for x in ar for y in br) for ar in a for br in b)


def mass(a: Matrix) -> F:
    """DET total-entry mass e^T a e; emphatically not the trace."""
    return sum((sum(row, F(0)) for row in a), F(0))


def trace(a: Matrix) -> F:
    return sum((a[i][i] for i in range(len(a))), F(0))


def pairing(a: Matrix, b: Matrix) -> F:
    return trace(multiply(a, b))


def event_pair(a: Matrix, event: tuple[int, ...], other: tuple[int, ...]) -> F:
    return sum((a[i][j] for i in event for j in other), F(0))


def congruence(operator: Matrix, a: Matrix) -> Matrix:
    return multiply(multiply(operator, a), transpose(operator))


I2 = matrix(((1, 0), (0, 1)))
J2 = matrix(((1, 1), (1, 1)))
W2 = matrix(((1, -1), (-1, 1)))
D0 = scale(F(1, 4), J2)


class OperationDomainWitnessChecks(unittest.TestCase):
    def assert_normalized(self, a: Matrix) -> None:
        self.assertEqual(transpose(a), a)
        self.assertEqual(mass(a), F(1))

    def test_atom_diagonals_are_not_an_unrestricted_commit_distribution(self):
        # Outer-product equality is the PSD certificate, not a numerical eigentest.
        d = outer((F(2), F(-1)))
        self.assertEqual(d, matrix(((4, -2), (-2, 1))))
        self.assert_normalized(d)
        self.assertEqual((d[0][0], d[1][1]), (F(4), F(1)))
        self.assertEqual(trace(d), F(5))
        self.assertNotEqual(event_pair(d, (0,), (1,)), F(0))
        self.assertNotEqual(d[0][0] + d[1][1], mass(d))

    def test_informative_singletons_work_on_the_restricted_diagonal_cone(self):
        p0 = matrix(((1, 0), (0, 0)))
        p1 = matrix(((0, 0), (0, 1)))
        outcomes = []
        for x in (F(1, 4), F(3, 4)):
            # Convex combination of rank-one PSD matrices certifies positivity.
            d = add(scale(x, p0), scale(1 - x, p1))
            self.assert_normalized(d)
            self.assertEqual(event_pair(d, (0,), (1,)), F(0))
            branches = (congruence(p0, d), congruence(p1, d))
            self.assertEqual(add(*branches), d)
            probabilities = tuple(mass(branch) for branch in branches)
            self.assertEqual(probabilities, (x, 1 - x))
            self.assertEqual(sum(probabilities, F(0)), F(1))
            outcomes.append(probabilities)
        self.assertNotEqual(*outcomes)
        # The same branch effects are not dominated by J2 on the full PSD cone.
        self.assertEqual(mass(W2), F(0))
        self.assertEqual(pairing(p0, W2), F(1))
        self.assertLess(pairing(add(J2, scale(F(-1), p0)), W2), F(0))

    def test_four_atom_recordable_partition_resolves_equal_diagonals(self):
        distributions = []
        kernels = []
        for c in (F(1, 8), F(-1, 8)):
            d = matrix(
                ((F(1, 4), c, 0, 0), (c, F(1, 4), 0, 0), (0, 0, F(1, 4), -c), (0, 0, -c, F(1, 4)))
            )
            # Exact positive weighted sum of four outer products: a PSD certificate.
            eigenvectors = ((1, 1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 1), (0, 0, 1, -1))
            eigenvalues = (F(1, 4) + c, F(1, 4) - c, F(1, 4) - c, F(1, 4) + c)
            reconstructed = matrix(((0,) * 4,) * 4)
            for value, vector in zip(eigenvalues, eigenvectors, strict=True):
                self.assertGreater(value, F(0))
                reconstructed = add(reconstructed, scale(value / 2, outer(vector)))
            self.assertEqual(reconstructed, d)
            self.assert_normalized(d)
            self.assertEqual(tuple(d[i][i] for i in range(4)), (F(1, 4),) * 4)
            self.assertEqual(event_pair(d, (0, 1), (2, 3)), F(0))
            probabilities = (event_pair(d, (0, 1), (0, 1)), event_pair(d, (2, 3), (2, 3)))
            self.assertEqual(sum(probabilities, F(0)), F(1))
            distributions.append(probabilities)
            kernels.append(d)
        self.assertNotEqual(*kernels)
        self.assertEqual(distributions, [(F(3, 4), F(1, 4)), (F(1, 4), F(3, 4))])

    def test_mass_preserving_congruence_need_not_be_unitary(self):
        # This algebraic cone map is explicitly supplied, not selected as physical.
        operator = scale(F(1, 2), add(J2, scale(F(2), W2)))
        inverse = scale(F(1, 2), add(J2, scale(F(1, 2), W2)))
        self.assertEqual(multiply(operator, inverse), I2)
        self.assertEqual(multiply(inverse, operator), I2)
        self.assertNotEqual(multiply(transpose(operator), operator), I2)
        self.assertEqual(multiply(transpose(operator), matrix(((1,), (1,)))), matrix(((1,), (1,))))
        d = outer((F(1), F(0)))
        transformed = congruence(operator, d)
        self.assertEqual(transformed, outer((F(3, 2), F(-1, 2))))
        self.assert_normalized(transformed)
        self.assertEqual(trace(d), F(1))
        self.assertEqual(trace(transformed), F(5, 2))
        self.assertEqual(congruence(inverse, transformed), d)
        # Local congruence remains positive on this explicit tensor-product input.
        ancillary = outer((F(2), F(-1)))
        joint = tensor(d, ancillary)
        joint_transformed = congruence(tensor(operator, I2), joint)
        self.assertEqual(joint_transformed, tensor(transformed, ancillary))
        self.assert_normalized(joint_transformed)
        self.assertEqual(congruence(tensor(inverse, I2), joint_transformed), joint)

    def test_normalized_slice_contains_unbounded_zero_mass_direction(self):
        self.assertEqual(W2, outer((F(1), F(-1))))
        self.assertEqual(mass(W2), F(0))
        self.assertNotEqual(W2, scale(F(0), I2))
        for t in (F(0), F(1), F(8)):
            # A nonnegative sum of the displayed outer products is PSD.
            d = add(D0, scale(t, W2))
            self.assert_normalized(d)
            self.assertEqual(trace(d), F(1, 2) + 2 * t)
            self.assertEqual(d[0][0], F(1, 4) + t)

    def test_rank_one_mass_effects_cannot_distinguish_normalized_kernels(self):
        probabilities = (F(1, 2), F(1, 3), F(1, 6))  # silent, commit A, commit B
        self.assertEqual(sum(probabilities, F(0)), F(1))
        effects = tuple(scale(p, J2) for p in probabilities)
        self.assertEqual(add(add(effects[0], effects[1]), effects[2]), J2)
        states = (D0, outer((F(2), F(-1))), add(D0, scale(F(7), W2)))
        for d in states:
            self.assert_normalized(d)
            self.assertEqual(tuple(pairing(effect, d) for effect in effects), probabilities)
            # T_r(d)=p_r d is a supplied positive instrument realizing these effects.
            branches = tuple(scale(p, d) for p in probabilities)
            self.assertEqual(tuple(mass(branch) for branch in branches), probabilities)
            self.assertEqual(add(add(branches[0], branches[1]), branches[2]), d)

    def test_first_commit_prefixes_and_finite_tail_balance_exactly(self):
        q, p_a, p_b = F(2, 3), F(1, 9), F(2, 9)
        self.assertEqual(q + p_a + p_b, F(1))
        for d in (D0, outer((F(2), F(-1)))):
            for horizon in (1, 2, 8):
                totals = [F(0), F(0)]
                for n in range(horizon):
                    residual = scale(q**n, d)
                    prefix = tuple(mass(scale(p, residual)) for p in (p_a, p_b))
                    self.assertEqual(prefix, (q**n * p_a, q**n * p_b))
                    totals = [x + y for x, y in zip(totals, prefix, strict=True)]
                tail = mass(scale(q**horizon, d))
                self.assertEqual(tail, q**horizon)
                self.assertEqual(sum(totals, F(0)) + tail, F(1))
                self.assertEqual(totals[1], 2 * totals[0])
        # If q=1 and all commit weights vanish, no finite prefix ever commits.
        for horizon in (1, 8):
            self.assertEqual(F(1) ** horizon, F(1))
            self.assertEqual(sum((F(1) ** n * F(0) for n in range(horizon)), F(0)), F(0))

    def test_zero_mass_branch_can_be_a_nonzero_positive_map(self):
        def branch(d: Matrix) -> Matrix:
            return scale(mass(d), W2)

        # B(d)=m(d) W2 is positive because m(d)>=0 for PSD d and W2 is PSD.
        # Its effect is zero, but its output matrix need not be zero. This is not
        # a normalized conditional state and cannot license a positive-probability commit.
        for d in (D0, outer((F(2), F(-1)))):
            output = branch(d)
            self.assertEqual(output, W2)
            self.assertNotEqual(output, scale(F(0), I2))
            self.assertEqual(mass(output), F(0))
            self.assertEqual(mass(add(d, output)), mass(d))
        self.assertEqual(branch(W2), scale(F(0), I2))
        self.assertEqual(branch(add(D0, W2)), add(branch(D0), branch(W2)))

    def test_first_commit_mass_convergence_does_not_bound_the_full_kernel(self):
        plus, minus = scale(F(1, 2), J2), scale(F(1, 2), W2)
        self.assertEqual(add(plus, minus), I2)
        self.assertEqual(multiply(plus, minus), scale(F(0), I2))
        operator = add(scale(F(1, 2), plus), scale(F(2), minus))
        self.assertEqual(operator, matrix(((F(5, 4), F(-3, 4)), (F(-3, 4), F(5, 4)))))
        initial = add(scale(F(1, 2), plus), minus)
        self.assertEqual(initial, matrix(((F(3, 4), F(-1, 4)), (F(-1, 4), F(3, 4)))))
        self.assert_normalized(initial)
        dark_coefficients = []
        for horizon in (1, 2, 3, 5):
            residual, accumulated = initial, scale(F(0), I2)
            for n in range(horizon):
                committed = scale(F(3, 4), residual)
                self.assertEqual(mass(committed), F(3, 4) * F(1, 4) ** n)
                accumulated = add(accumulated, committed)
                residual = congruence(operator, residual)
            bright_coefficient = F(1, 2) * (1 - F(1, 4) ** horizon)
            dark_coefficient = F(1, 4) * (F(4) ** horizon - 1)
            expected = add(scale(bright_coefficient, plus), scale(dark_coefficient, minus))
            self.assertEqual(accumulated, expected)
            self.assertEqual(mass(accumulated), 1 - F(1, 4) ** horizon)
            self.assertEqual(mass(accumulated) + mass(residual), F(1))
            self.assertEqual(trace(accumulated), bright_coefficient + dark_coefficient)
            dark_coefficients.append(dark_coefficient)
        self.assertTrue(all(x < y for x, y in pairwise(dark_coefficients)))
        # Divergence as N grows follows from the proved formula, not finite tests.
        self.assertGreater(dark_coefficients[-1], F(255))


if __name__ == "__main__":
    unittest.main(verbosity=2)
