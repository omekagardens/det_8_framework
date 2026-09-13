"""Eight exact finite witnesses for the conditional pair-kernel derivation.

Standard library only. This file neither imports old model implementations
nor generates histories, searches fixtures or writes captures. Operators in
the completion witness are constructed from the supplied D-inner product.
"""

import itertools
import unittest
from fractions import Fraction as F


def matrix(rows):
    return [[F(value) for value in row] for row in rows]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def transpose(a):
    return [list(column) for column in zip(*a, strict=True)]


def multiply(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def add(a, b):
    return [
        [x + y for x, y in zip(arow, brow, strict=True)] for arow, brow in zip(a, b, strict=True)
    ]


def scale(value, a):
    return [[F(value) * entry for entry in row] for row in a]


def apply(a, vector):
    return [
        sum((entry * value for entry, value in zip(row, vector, strict=True)), F(0)) for row in a
    ]


def inner(d, u, v):
    return sum((left * right for left, right in zip(u, apply(d, v), strict=True)), F(0))


def event(n, indices):
    return [F(i in indices) for i in range(n)]


def pair(d, a, b):
    return sum((d[i][j] for i in a for j in b), F(0))


def mass(d):
    return sum((sum(row, F(0)) for row in d), F(0))


def restrict(d, indices):
    """Retain the raw branch on the original history algebra, including zeros."""
    return [
        [entry if i in indices and j in indices else F(0) for j, entry in enumerate(row)]
        for i, row in enumerate(d)
    ]


def normalize(d):
    total = mass(d)
    if total <= 0:
        raise ValueError("only strictly positive total mass can be conditioned")
    return scale(1 / total, d)


def determinant(a):
    """Exact cofactor formula; used only for the fixed matrices of size <= 4."""
    if not a:
        return F(1)
    if len(a) == 1:
        return a[0][0]
    return sum(
        (
            (-1) ** column
            * a[0][column]
            * determinant([[entry for j, entry in enumerate(row) if j != column] for row in a[1:]])
            for column in range(len(a))
        ),
        F(0),
    )


def projector(d, vector):
    """D-orthogonal line projection, derived by its defining inner product."""
    norm = inner(d, vector, vector)
    if norm <= 0:
        raise ValueError("projection vector must have positive D norm")
    dual = apply(d, vector)
    return [[left * right / norm for right in dual] for left in vector]


class StrictDerivationWitnesses(unittest.TestCase):
    def test_1_fixed_diagonal_coherence_sensitive_recordable_partition(self):
        witnesses = []
        for c in (F(1, 8), F(-1, 8)):
            d = matrix(
                [[F(1, 4), c, 0, 0], [c, F(1, 4), 0, 0], [0, 0, F(1, 4), -c], [0, 0, -c, F(1, 4)]]
            )
            self.assertEqual(mass(d), F(1))
            self.assertEqual(d, transpose(d))
            a, b = {0, 1}, {2, 3}
            self.assertEqual(pair(d, a, b), F(0))
            self.assertEqual(pair(d, b, a), F(0))
            weights = [pair(d, a, a), pair(d, b, b)]
            self.assertEqual(weights, [F(1, 2) + 2 * c, F(1, 2) - 2 * c])
            self.assertEqual(sum(weights), F(1))
            # Fixed complete eigenbasis, without introducing an amplitude input.
            for vector, eigenvalue in (
                ([1, 1, 0, 0], F(1, 4) + c),
                ([1, -1, 0, 0], F(1, 4) - c),
                ([0, 0, 1, 1], F(1, 4) - c),
                ([0, 0, 1, -1], F(1, 4) + c),
            ):
                self.assertGreater(eigenvalue, 0)
                self.assertEqual(apply(d, vector), [eigenvalue * entry for entry in vector])
            mu = lambda indices, d=d: pair(d, indices, indices)
            i3 = mu({0, 1, 2}) - mu({0, 1}) - mu({0, 2}) - mu({1, 2}) + mu({0}) + mu({1}) + mu({2})
            self.assertEqual(i3, F(0))
            witnesses.append((d, weights))
        self.assertEqual(
            [witnesses[0][0][i][i] for i in range(4)], [witnesses[1][0][i][i] for i in range(4)]
        )
        self.assertEqual(witnesses[0][1], [F(3, 4), F(1, 4)])
        self.assertEqual(witnesses[1][1], [F(1, 4), F(3, 4)])

    def test_2_nested_history_conditioning_and_nonzero_impossible_block(self):
        d = matrix(
            [
                [F(1, 4), F(1, 8), 0, 0],
                [F(1, 8), F(1, 4), 0, 0],
                [0, 0, F(1, 4), F(-1, 8)],
                [0, 0, F(-1, 8), F(1, 4)],
            ]
        )
        a, b = {0, 1}, {0}
        da, db = restrict(d, a), restrict(d, b)
        self.assertEqual(restrict(da, b), restrict(d, a & b))
        self.assertEqual(mass(da), F(3, 4))
        self.assertEqual(mass(db), F(1, 4))
        conditional_a = normalize(da)
        raw_second = restrict(conditional_a, b)
        self.assertEqual(mass(raw_second), F(1, 3))
        self.assertEqual(mass(da) * mass(raw_second), mass(db))
        self.assertEqual(normalize(raw_second), normalize(db))

        dz = matrix([[1, -1, 0], [-1, 1, 0], [0, 0, 1]])
        self.assertEqual(mass(dz), F(1))
        # The fixed block has eigenvalues 2, 0; the remaining one is 1.
        for vector, eigenvalue in (([1, -1, 0], F(2)), ([1, 1, 0], F(0)), ([0, 0, 1], F(1))):
            self.assertEqual(apply(dz, vector), [eigenvalue * entry for entry in vector])
        impossible = restrict(dz, {0, 1})
        self.assertEqual(pair(dz, {0, 1}, {2}), F(0))
        self.assertEqual(mass(impossible), F(0))
        self.assertNotEqual(impossible, zero(3))
        self.assertEqual(mass(restrict(dz, {2})), F(1))
        with self.assertRaises(ValueError):
            normalize(impossible)
        self.assertEqual(impossible, matrix([[1, -1, 0], [-1, 1, 0], [0, 0, 0]]))

    def test_3_coarse_decoherence_does_not_select_a_unique_operator_completion(self):
        d = scale(F(1, 3), matrix([[1, 0, F(1, 2)], [0, 1, F(-1, 2)], [F(1, 2), F(-1, 2), 1]]))
        expected_minors = {
            (0,): F(1, 3),
            (1,): F(1, 3),
            (2,): F(1, 3),
            (0, 1): F(1, 9),
            (0, 2): F(1, 12),
            (1, 2): F(1, 12),
            (0, 1, 2): F(1, 54),
        }
        for size in (1, 2, 3):
            for indices in itertools.combinations(range(3), size):
                minor = determinant([[d[i][j] for j in indices] for i in indices])
                self.assertEqual(minor, expected_minors[indices])
                self.assertGreater(minor, 0)
        self.assertEqual(mass(d), F(1))
        a, b, w = event(3, {0, 1}), event(3, {2}), [F(1), F(-1), F(-1)]
        self.assertEqual(
            [inner(d, vector, vector) for vector in (a, b, w)], [F(2, 3), F(1, 3), F(1, 3)]
        )
        for u, v in itertools.combinations((a, b, w), 2):
            self.assertEqual(inner(d, u, v), F(0))
        boolean_cut = matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
        self.assertNotEqual(multiply(transpose(boolean_cut), d), multiply(d, boolean_cut))
        pa, pb, pw = (projector(d, vector) for vector in (a, b, w))
        self.assertEqual(add(add(pa, pb), pw), identity(3))
        completions = ((add(pa, pw), pb), (pa, add(pb, pw)))
        prepared = [F(1)] * 3
        for first, second in completions:
            self.assertEqual(add(first, second), identity(3))
            self.assertEqual(multiply(first, second), zero(3))
            self.assertEqual(multiply(second, first), zero(3))
            for projection in (first, second):
                self.assertEqual(multiply(projection, projection), projection)
                self.assertEqual(multiply(transpose(projection), d), multiply(d, projection))
            self.assertEqual(apply(first, prepared), a)
            self.assertEqual(apply(second, prepared), b)
            self.assertEqual(
                [
                    inner(d, apply(projection, prepared), apply(projection, prepared))
                    for projection in (first, second)
                ],
                [F(2, 3), F(1, 3)],
            )
        self.assertEqual(apply(completions[0][0], w), w)
        self.assertEqual(apply(completions[1][0], w), [F(0)] * 3)
        self.assertNotEqual(completions[0], completions[1])

    def test_4_boolean_cut_does_not_descend_through_a_gram_nullspace(self):
        d = scale(F(1, 4), matrix([[1, 1], [1, 1]]))
        n = [F(1), F(-1)]
        cut = matrix([[1, 0], [0, 0]])
        self.assertEqual(mass(d), F(1))
        self.assertEqual(apply(d, n), [F(0), F(0)])
        self.assertEqual(inner(d, n, n), F(0))
        self.assertEqual(inner(d, apply(cut, n), apply(cut, n)), F(1, 4))

    def test_5_real_pair_kernel_can_interfere(self):
        d = scale(F(1, 6), matrix([[2, 1], [1, 2]]))
        self.assertEqual(mass(d), F(1))
        self.assertGreater(d[0][0], 0)
        self.assertEqual(determinant(d), F(1, 12))
        self.assertEqual(pair(d, {0, 1}, {0, 1}) - pair(d, {0}, {0}) - pair(d, {1}, {1}), F(1, 3))

    def test_6_reversibility_does_not_force_G_inverse_Omega_squared_minus_identity(self):
        # D = G + i Omega. Complex arithmetic is checked through exact real
        # and imaginary components; no floating complex numbers are used.
        t = F(1, 2)
        j0 = matrix([[0, -1], [1, 0]])
        g = scale(F(1, 2), identity(2))
        omega = scale(t / 2, j0)
        self.assertEqual(g, transpose(g))
        self.assertEqual(transpose(omega), scale(-1, omega))
        self.assertEqual((mass(g), mass(omega)), (F(1), F(0)))
        eigenvalues = [F(1, 4), F(3, 4)]
        # Hermitian 2x2 positivity follows from the positive diagonal and
        # determinant; characteristic roots are verified exactly as well.
        determinant_d = g[0][0] * g[1][1] - omega[0][1] ** 2
        self.assertEqual(determinant_d, F(3, 16))
        for eigenvalue in eigenvalues:
            self.assertGreater(eigenvalue, 0)
            self.assertEqual(eigenvalue**2 - eigenvalue + determinant_d, F(0))
        j = multiply(scale(2, identity(2)), omega)
        self.assertEqual(j, scale(t, j0))
        self.assertEqual(multiply(j, j), scale(F(-1, 4), identity(2)))
        self.assertNotEqual(multiply(j, j), scale(-1, identity(2)))
        rotation = matrix([[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]])
        self.assertEqual(multiply(transpose(rotation), rotation), identity(2))
        self.assertEqual(determinant(rotation), F(1))
        self.assertEqual(multiply(multiply(transpose(rotation), g), rotation), g)
        self.assertEqual(multiply(multiply(transpose(rotation), omega), rotation), omega)

    def test_7_equal_readout_and_repeatability_do_not_fix_reset_residuals(self):
        groups = ({0, 1}, {2, 3})

        def reset(d, record, right):
            weight = pair(d, groups[record], groups[record])
            output = zero(4)
            target = 2 * record + int(right)
            output[target][target] = weight
            return output

        d = scale(F(1, 4), identity(4))
        outputs = []
        for right in (False, True):
            branches = [reset(d, record, right) for record in (0, 1)]
            self.assertEqual([mass(branch) for branch in branches], [F(1, 2)] * 2)
            self.assertEqual(sum(mass(branch) for branch in branches), F(1))
            for record, branch in enumerate(branches):
                self.assertEqual(restrict(branch, groups[record]), branch)
                self.assertEqual(reset(branch, record, right), branch)
                self.assertEqual(reset(branch, 1 - record, right), zero(4))
                self.assertEqual(mass(normalize(branch)), F(1))
            outputs.append(branches)
        self.assertNotEqual(normalize(outputs[0][0]), normalize(outputs[1][0]))
        self.assertEqual(
            normalize(outputs[0][0]),
            matrix([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        )
        self.assertEqual(
            normalize(outputs[1][0]),
            matrix([[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        )
        supported_only_in_a = matrix([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        for right in (False, True):
            impossible = reset(supported_only_in_a, 1, right)
            self.assertEqual(impossible, zero(4))
            with self.assertRaises(ValueError):
                normalize(impossible)

    def test_8_bare_extensions_preserve_the_old_kernel_but_not_next_weights(self):
        d = scale(F(1, 6), matrix([[2, 1], [1, 2]]))
        next_weights = []
        for q in ((F(1), F(0)), (F(1, 2), F(1, 2))):
            extended = [
                [
                    d[row // 2][column // 2] * q[row % 2] if row % 2 == column % 2 else F(0)
                    for column in range(4)
                ]
                for row in range(4)
            ]
            self.assertEqual(extended, transpose(extended))
            self.assertEqual(mass(extended), F(1))
            for size in (1, 2, 3, 4):
                for indices in itertools.combinations(range(4), size):
                    self.assertGreaterEqual(
                        determinant([[extended[i][j] for j in indices] for i in indices]), F(0)
                    )
            old_blocks = ({0, 1}, {2, 3})
            coarse = [[pair(extended, a, b) for b in old_blocks] for a in old_blocks]
            self.assertEqual(coarse, d)
            new_blocks = ({0, 2}, {1, 3})
            self.assertEqual(pair(extended, *new_blocks), F(0))
            weights = [pair(extended, block, block) for block in new_blocks]
            self.assertEqual(weights, list(q))
            next_weights.append(weights)
        self.assertNotEqual(next_weights[0], next_weights[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
