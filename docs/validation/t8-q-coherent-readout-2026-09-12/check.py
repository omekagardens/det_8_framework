"""Bounded exact checks of the conditional readout law; no growth census."""

import unittest
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product

import algebra as a
import reference as r


@dataclass(frozen=True, eq=False)
class Q:
    """Exact rational real and imaginary components, solely for test inputs."""

    real: F = F(0)
    imag: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "real", F(self.real))
        object.__setattr__(self, "imag", F(self.imag))

    @staticmethod
    def cast(value):
        return value if isinstance(value, Q) else Q(F(value))

    def __add__(self, other):
        other = Q.cast(other)
        return Q(self.real + other.real, self.imag + other.imag)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.real, -self.imag)

    def __sub__(self, other):
        return self + -Q.cast(other)

    def __mul__(self, other):
        other = Q.cast(other)
        return Q(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Q.cast(other)
        norm = other.real**2 + other.imag**2
        if norm == 0:
            raise ZeroDivisionError("Exact zero divisor")
        return self * Q(other.real / norm, -other.imag / norm)

    def conjugate(self):
        return Q(self.real, -self.imag)

    def __eq__(self, other):
        other = Q.cast(other)
        return self.real == other.real and self.imag == other.imag


BASIS = tuple(tuple(F(i == j) for j in range(16)) for i in range(16))
BRANCHES = tuple(product(("a", "b", "ab"), (0, 1), (0, 1)))


def fixture(coherence):
    """Local phi with diagonal1/2, tensored with uniform diagonal port b."""
    conjugate = coherence.conjugate() if isinstance(coherence, Q) else coherence
    local = ((F(1, 2), coherence), (conjugate, F(1, 2)))
    return tuple(
        local[i // 2][j // 2] * (F(1, 2) if i % 2 == j % 2 else 0)
        for i in range(4)
        for j in range(4)
    )


def weight(values):
    return sum((values[5 * i] for i in range(4)), F(0))


def mix(left, right, proportion=F(2, 5)):
    return tuple(proportion * x + (1 - proportion) * y for x, y in zip(left, right))


class ReadoutChecks(unittest.TestCase):
    def test_01_history_basis_and_unit_identities(self):
        self.assertEqual(a.add(*a.HISTORIES), a.ONE)
        self.assertEqual(a.add(*(a.mul(a.star(h), h) for h in a.HISTORIES)), a.ONE)
        for row, col in a.UNITS:
            ra, rb = divmod(row, 2)
            ca, cb = divmod(col, 2)
            reconstruction = a.add(
                *(
                    a.scale(h, (s if ra != ca else 1) * (t if rb != cb else 1))
                    for (i, s, j, t), h in zip(a.LABELS, a.HISTORIES)
                    if i == ca and j == cb
                )
            )
            self.assertEqual(reconstruction, {(row, col): F(1)})

    def test_02_derived_projector_identities(self):
        for action, context in product(("a", "b", "ab"), (0, 1)):
            p, q = (a.projector(action, context, x) for x in (0, 1))
            self.assertEqual(a.add(p, q), a.ONE)
            self.assertEqual(a.mul(p, q), {})
            for element in (p, q):
                self.assertEqual(a.star(element), element)
                self.assertEqual(a.mul(element, element), element)

    def test_03_full_history_embedding_and_reconstruction(self):
        self.assertEqual(a.LABELS, r.HISTORY_LABELS)
        for values in BASIS:
            kernel = a.history_kernel(values)
            self.assertEqual(kernel, r.history_kernel(values))
            self.assertEqual(a.coordinates_from_kernel(kernel), values)
            self.assertTrue(a.compatible(kernel))
            self.assertEqual(a.mass(kernel), weight(values))
            self.assertEqual(a.trace(kernel), a.mass(kernel))

    def test_04_all_complete_branch_coordinate_maps(self):
        # 16 basis inputs x12 maps: equality of linear maps, not just states.
        for values, branch in product(BASIS, BRANCHES):
            actual = a.branch_coordinates(values, *branch)
            self.assertEqual(actual, r.branch_coordinates(values, *branch))
            rebuilt = a.history_kernel(actual)
            self.assertTrue(a.compatible(rebuilt))
            self.assertEqual(a.coordinates_from_kernel(rebuilt), actual)

    def test_05_all_mass_functionals_and_action_marginals(self):
        for values in BASIS + (fixture(F(1, 4)), fixture(F(-1, 4))):
            for context in (0, 1):
                total = F(0)
                for action in ("a", "b", "ab"):
                    marginal = sum(
                        (weight(a.branch_coordinates(values, action, context, x)) for x in (0, 1)),
                        F(0),
                    )
                    self.assertEqual(marginal, weight(values) / 3)
                    total += marginal
                self.assertEqual(total, weight(values))

    def test_06_same_atomic_diagonal_different_readout(self):
        plus, minus = fixture(F(1, 4)), fixture(F(-1, 4))
        dp, dm = a.history_kernel(plus), a.history_kernel(minus)
        self.assertNotEqual(dp, dm)
        self.assertEqual(tuple(dp[i][i] for i in range(16)), (F(1, 16),) * 16)
        self.assertEqual(tuple(dm[i][i] for i in range(16)), (F(1, 16),) * 16)
        self.assertEqual(weight(a.branch_coordinates(plus, "a", 0, 0)), F(1, 4))
        self.assertEqual(weight(a.branch_coordinates(minus, "a", 0, 0)), F(1, 12))
        self.assertEqual(F(1, 2) ** 2 - F(1, 4) ** 2, F(3, 16))

    def test_07_complex_coherence_and_transpose_control(self):
        values = fixture(Q(F(1, 4), F(1, 4)))
        self.assertEqual(F(1, 4) - F(1, 16) - F(1, 16), F(1, 8))
        kernel = a.history_kernel(values)
        self.assertEqual(kernel, r.history_kernel(values))
        self.assertEqual(a.coordinates_from_kernel(kernel), values)
        self.assertEqual(a.mass(kernel), 1)
        self.assertTrue(any(isinstance(z, Q) and z.imag for row in kernel for z in row))
        for i, j in product(range(16), repeat=2):
            self.assertEqual(kernel[i][j], Q.cast(kernel[j][i]).conjugate())
        transposed = tuple(values[4 * j + i] for i in range(4) for j in range(4))
        self.assertNotEqual(kernel, r.history_kernel(transposed))
        for branch in BRANCHES:
            self.assertEqual(
                a.branch_coordinates(values, *branch), r.branch_coordinates(values, *branch)
            )

    def test_08_actual_and_formal_zero_branches(self):
        values = fixture(F(-1, 2))
        source = a.history_kernel(values)
        self.assertEqual(a.mass(source), 1)
        residual = a.branch_kernel(source, "a", 0, 0)
        self.assertEqual(residual, ((F(0),) * 16,) * 16)
        self.assertIsNone(a.normalized_or_none(residual))
        positive = a.branch_kernel(source, "a", 0, 1)
        self.assertEqual(a.mass(positive), F(1, 3))
        self.assertEqual(a.mass(a.normalized_or_none(positive)), 1)
        for action in ("a", "b", "ab"):
            self.assertEqual(a.branch_coordinates(values, action, 0, None), (F(0),) * 16)

    def test_09_raw_zero_mass_block_is_not_the_residual(self):
        source = a.history_kernel(fixture(F(-1, 2)))
        selected = [n for n, (_, s, _, _) in enumerate(a.LABELS) if s == 1]
        raw = tuple(tuple(source[i][j] for j in selected) for i in selected)
        self.assertEqual(a.mass(raw), 0)
        self.assertGreater(a.trace(raw), 0)
        with self.assertRaises(ValueError):
            a.normalized_or_none(raw)

    def test_10_mixtures_unnormalized_and_conditioned(self):
        left, right = fixture(F(1, 4)), fixture(F(-1, 4))
        p = F(2, 5)
        for branch in BRANCHES:
            bl, br = (a.branch_coordinates(v, *branch) for v in (left, right))
            bm = a.branch_coordinates(mix(left, right, p), *branch)
            self.assertEqual(bm, mix(bl, br, p))
            kl, kr, km = weight(bl), weight(br), weight(bm)
            posterior_weight = p * kl / km
            conditional = mix(
                tuple(v / kl for v in bl), tuple(v / kr for v in br), posterior_weight
            )
            self.assertEqual(tuple(v / km for v in bm), conditional)

    def test_11_complete_incomparable_compositions(self):
        # 16 basis x4 context pairs x4 outcomes =256 complete-map comparisons.
        for values, ca, cb, x, y in product(BASIS, (0, 1), (0, 1), (0, 1), (0, 1)):
            first = a.branch_coordinates(a.branch_coordinates(values, "a", ca, x), "b", cb, y)
            second = a.branch_coordinates(a.branch_coordinates(values, "b", cb, y), "a", ca, x)
            self.assertEqual(first, second)

    def test_12_correlated_input_not_product_assumption(self):
        # Positive rank-one Bell fixture, used only as an input/correspondence check.
        values = tuple(
            F(1, 2) if (i, j) in ((0, 0), (0, 3), (3, 0), (3, 3)) else F(0)
            for i in range(4)
            for j in range(4)
        )
        self.assertEqual(a.mass(a.history_kernel(values)), 1)
        for ca, cb, x, y in product((0, 1), repeat=4):
            first = a.branch_coordinates(a.branch_coordinates(values, "a", ca, x), "b", cb, y)
            second = a.branch_coordinates(a.branch_coordinates(values, "b", cb, y), "a", ca, x)
            self.assertEqual(first, second)
            self.assertGreaterEqual(weight(first), 0)
        impossible = a.branch_coordinates(a.branch_coordinates(values, "a", 0, 0), "b", 0, 1)
        self.assertEqual(impossible, (F(0),) * 16)

    def test_13_same_port_exchange_is_not_promised(self):
        values = tuple(F(1) if i == 0 else F(0) for i in range(16))
        uv = a.branch_coordinates(a.branch_coordinates(values, "a", 0, 0), "a", 1, 0)
        vu = a.branch_coordinates(a.branch_coordinates(values, "a", 1, 0), "a", 0, 0)
        self.assertNotEqual(uv, vu)

    def test_14_full_positive_kernel_cone_is_not_admitted(self):
        # PSD, mass1; incompatible with the declared history identities.
        raw = tuple(tuple(F(i == j == 0) for j in range(16)) for i in range(16))
        self.assertEqual(a.mass(raw), 1)
        self.assertFalse(a.compatible(raw))
        with self.assertRaises(ValueError):
            a.branch_kernel(raw, "a", 0, 0)

    def test_15_bad_shapes_and_exact_zero_guard(self):
        with self.assertRaises(ValueError):
            a.coordinates_from_kernel(((F(1),),))
        with self.assertRaises(ValueError):
            a.branch_coordinates((F(0),) * 15, "a", 0, 0)
        with self.assertRaises(ValueError):
            a.projector("c", 0, 0)
        with self.assertRaises(ZeroDivisionError):
            Q(1) / Q(0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
