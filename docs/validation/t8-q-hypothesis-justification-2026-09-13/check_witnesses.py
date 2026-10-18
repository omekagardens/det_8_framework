"""Exact mathematical witness checks for the accompanying non-entailment argument.

These are finite, stdlib-only Fraction/unittest controls, not Lean verification,
an axiom-independence proof for every proposed axiom, or a generative derivation
of quantum theory. Quantum matrices occur only as explicit countermodel data.
The accompanying argument must supply the quantified mathematical statements
and explain which weak DET premises each witness satisfies.

Run directly with Python, including ``python -O check_witnesses.py``. All checks
use unittest assertions, which remain active under optimization. No research
modules, numerical tolerances, experiment census, or executor are used.
"""

import unittest
from fractions import Fraction as F
from itertools import product

Matrix = tuple[tuple[F, ...], ...]


def matrix(rows) -> Matrix:
    """Convert the small explicit rational matrices below to immutable data."""
    return tuple(tuple(F(value) for value in row) for row in rows)


def identity(size: int) -> Matrix:
    return matrix(tuple(tuple(int(i == j) for j in range(size)) for i in range(size)))


def transpose(a: Matrix) -> Matrix:
    return tuple(zip(*a))


def add(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(x + y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def scale(c: F, a: Matrix) -> Matrix:
    return tuple(tuple(c * x for x in row) for row in a)


def multiply(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum((x * y for x, y in zip(row, col)), F(0)) for col in transpose(b)) for row in a
    )


def tensor(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(x * y for x in ar for y in br) for ar in a for br in b)


def trace(a: Matrix) -> F:
    return sum((a[i][i] for i in range(len(a))), F(0))


def expectation(rho: Matrix, effect: Matrix) -> F:
    return trace(multiply(rho, effect))


def diagonal(values: tuple[F, ...]) -> Matrix:
    return matrix(
        tuple(
            tuple(values[i] if i == j else 0 for j in range(len(values)))
            for i in range(len(values))
        )
    )


I2 = identity(2)
I4 = identity(4)
X = matrix(((0, 1), (1, 0)))
Z = matrix(((1, 0), (0, -1)))
J = matrix(((0, -1), (1, 0)))
W = tensor(J, J)
P_PLUS = scale(F(1, 2), add(I4, W))
P_MINUS = scale(F(1, 2), add(I4, scale(F(-1), W)))
RHO_PLUS = scale(F(1, 2), P_PLUS)
RHO_MINUS = scale(F(1, 2), P_MINUS)
U = scale(
    F(1, 2),
    matrix(((1, 1, 1, 1), (1, -1, 1, -1), (1, 1, -1, -1), (1, -1, -1, 1))),
)


def encode_compatible_d(rho: Matrix) -> Matrix:
    """J4 history order is (r, i); D_(r,i),(s,j) = delta_rs U_ir U_jr rho_ji."""
    return matrix(
        tuple(
            tuple(
                U[i][r] * U[j][r] * rho[j][i] if r == s else 0 for s in range(4) for j in range(4)
            )
            for r in range(4)
            for i in range(4)
        )
    )


class MathematicalWitnessChecks(unittest.TestCase):
    """Finite exact controls; the scope limitations in each check are substantive."""

    def assert_probability_vector(self, values: tuple[F, ...]) -> None:
        self.assertEqual(sum(values, F(0)), F(1))
        self.assertTrue(all(F(0) <= value <= F(1) for value in values))

    def test_two_rebits_fail_local_tomography_with_valid_states_and_effects(self):
        """The Sym2 basis spans every real local effect, not just sampled effects."""
        self.assertEqual(transpose(J), scale(F(-1), J))
        self.assertEqual(transpose(W), W)
        self.assertEqual(multiply(W, W), I4)
        self.assertEqual(add(P_PLUS, P_MINUS), I4)
        for projector, rho in ((P_PLUS, RHO_PLUS), (P_MINUS, RHO_MINUS)):
            self.assertEqual(transpose(projector), projector)
            # P = P P^T is an exact PSD certificate; rho = P / 2 is PSD too.
            self.assertEqual(multiply(projector, transpose(projector)), projector)
            self.assertEqual(rho, scale(F(1, 2), projector))
            self.assertEqual(trace(rho), F(1))
        self.assertNotEqual(RHO_PLUS, RHO_MINUS)

        # I, X, Z span Sym2(R); these nine products span all product-effect data.
        for a, b in product((I2, X, Z), repeat=2):
            probe = tensor(a, b)
            self.assertEqual(expectation(RHO_PLUS, probe), expectation(RHO_MINUS, probe))
            self.assertEqual(expectation(RHO_PLUS, probe), F(int(a == I2 and b == I2)))

        # The basis observables need not be effects. Check actual local effects
        # as well, with both each projector and its complement certified PSD.
        local_effects = (I2,) + tuple(
            scale(F(1, 2), add(I2, scale(F(sign), a))) for a in (X, Z) for sign in (-1, 1)
        )
        for effect in local_effects:
            for projector in (effect, add(I2, scale(F(-1), effect))):
                self.assertEqual(multiply(projector, transpose(projector)), projector)
        for a, b in product(local_effects, repeat=2):
            effect = tensor(a, b)
            p_plus, p_minus = (expectation(rho, effect) for rho in (RHO_PLUS, RHO_MINUS))
            self.assertEqual(p_plus, p_minus)
            self.assertTrue(F(0) <= p_plus <= F(1))
        # {P_PLUS, P_MINUS} is a valid global test that distinguishes the states.
        self.assertEqual(expectation(RHO_PLUS, P_PLUS), F(1))
        self.assertEqual(expectation(RHO_MINUS, P_PLUS), F(0))

    def test_rebit_witness_has_exact_compatible_kernel_encoding(self):
        """A compatible strongly positive D encoding, not a quantum reconstruction."""
        self.assertEqual(multiply(transpose(U), U), I4)
        root_kernel = (F(1, 4),) * 4
        next_kernel = ((F(1, 4),) * 4,) * 4
        self.assert_probability_vector(root_kernel)
        for row in next_kernel:
            self.assert_probability_vector(row)

        encoded = []
        for projector, rho in ((P_PLUS, RHO_PLUS), (P_MINUS, RHO_MINUS)):
            d = encode_compatible_d(rho)
            encoded.append(d)
            # B is block diagonal with blocks diag(U[:, r]) P.
            # D = B B^T / 2 proves PSD, hence strong positivity on all events.
            factor = matrix(
                tuple(
                    tuple(
                        U[i][r] * projector[i][j] if r == s else 0
                        for s in range(4)
                        for j in range(4)
                    )
                    for r in range(4)
                    for i in range(4)
                )
            )
            self.assertEqual(d, scale(F(1, 2), multiply(factor, transpose(factor))))
            self.assertEqual(transpose(d), d)
            self.assertEqual(sum((sum(row, F(0)) for row in d), F(0)), F(1))
            self.assertEqual(trace(d), F(1))
            for r, i in product(range(4), repeat=2):
                self.assertEqual(d[4 * r + i][4 * r + i], root_kernel[r] * next_kernel[r][i])
            # Coarsening either coordinate gives the compatible diagonal marginal.
            for r, s in product(range(4), repeat=2):
                self.assertEqual(
                    sum((d[4 * r + i][4 * s + j] for i, j in product(range(4), repeat=2)), F(0)),
                    root_kernel[r] if r == s else F(0),
                )
            for i, j in product(range(4), repeat=2):
                self.assertEqual(
                    sum((d[4 * r + i][4 * s + j] for r, s in product(range(4), repeat=2)), F(0)),
                    rho[j][i] if i == j else F(0),
                )
            # Column zero of U is nowhere zero, so this block recovers rho exactly.
            recovered = matrix(
                tuple(tuple(d[j][i] / (U[j][0] * U[i][0]) for j in range(4)) for i in range(4))
            )
            self.assertEqual(recovered, rho)
        self.assertNotEqual(encoded[0], encoded[1])

    def test_classical_pure_joint_marginals_finite_illustration(self):
        """Env sizes 2 and 3 illustrate, but do not prove, the all-size statement."""
        checked_point_masses = 0
        for environment_size in (2, 3):
            for atom in range(2 * environment_size):
                joint = tuple(F(int(k == atom)) for k in range(2 * environment_size))
                self.assert_probability_vector(joint)
                marginal = tuple(
                    sum(joint[a * environment_size : (a + 1) * environment_size], F(0))
                    for a in range(2)
                )
                self.assertIn(marginal, ((F(1), F(0)), (F(0), F(1))))
                self.assertNotEqual(marginal, (F(1, 2), F(1, 2)))
                checked_point_masses += 1
        self.assertEqual(checked_point_masses, 10)

        point_00 = (F(1), F(0), F(0), F(0))
        point_11 = (F(0), F(0), F(0), F(1))
        correlated = tuple((x + y) / 2 for x, y in zip(point_00, point_11))
        self.assertNotEqual(point_00, point_11)
        self.assertEqual(correlated, (F(1, 2), F(0), F(0), F(1, 2)))
        self.assert_probability_vector(correlated)
        self.assertEqual((sum(correlated[:2], F(0)), sum(correlated[2:], F(0))), (F(1, 2),) * 2)
        # This explicit nontrivial convex decomposition proves this joint is nonpure.
        self.assertNotIn(correlated, (point_00, point_11))
        self.assertEqual(sum(value > 0 for value in correlated), 2)

    def test_complete_future_tests_preserve_prefix_but_postselection_changes_it(self):
        """Exact row normalization controls forward marginals, not conditionals."""
        past = (F(1, 3), F(2, 3))
        future_tests = (
            ((F(1, 4), F(3, 4)), (F(3, 4), F(1, 4))),
            ((F(1, 2), F(1, 3), F(1, 6)), (F(1, 6), F(1, 3), F(1, 2))),
        )
        self.assert_probability_vector(past)
        conditionals = []
        for kernel in future_tests:
            for row in kernel:
                self.assert_probability_vector(row)
            joint = tuple(tuple(past[a] * p for p in kernel[a]) for a in range(2))
            flat = tuple(p for row in joint for p in row)
            self.assert_probability_vector(flat)
            # The diagonal D is PSD because its diagonal consists of probabilities.
            d = diagonal(flat)
            self.assertTrue(all(d[i][i] >= 0 for i in range(len(flat))))
            self.assertEqual(trace(d), F(1))
            self.assertEqual(tuple(sum(row, F(0)) for row in joint), past)
            selected_mass = sum((row[0] for row in joint), F(0))
            conditional = tuple(row[0] / selected_mass for row in joint)
            self.assert_probability_vector(conditional)
            self.assertNotEqual(conditional, past)
            conditionals.append(conditional)
        self.assertEqual(conditionals, [(F(1, 7), F(6, 7)), (F(3, 5), F(2, 5))])

    def test_unsharp_proper_kernel_does_not_supply_sharp_measurements(self):
        """Only a lack-of-measurement-richness witness, not a full GPT countertheory."""
        eta = F(1, 2)
        effects = tuple(eta / 2 + (1 - eta) * F(z) for z in (0, 1))
        self.assertEqual(effects, (F(1, 4), F(3, 4)))
        kernel = tuple((e, 1 - e) for e in effects)
        for row in kernel:
            self.assert_probability_vector(row)
            self.assertTrue(all(F(0) < p < F(1) for p in row))
        self.assertNotEqual(effects, (F(0), F(1)))
        initial = (F(1, 2), F(1, 2))
        joint = tuple(initial[z] * p for z in (0, 1) for p in kernel[z])
        self.assert_probability_vector(joint)
        self.assertEqual(joint, (F(1, 8), F(3, 8), F(3, 8), F(1, 8)))
        d = diagonal(joint)
        self.assertTrue(all(d[i][i] > 0 for i in range(4)))
        self.assertEqual(sum((sum(row, F(0)) for row in d), F(0)), F(1))


if __name__ == "__main__":
    unittest.main(verbosity=2)
