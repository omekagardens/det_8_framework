"""Exact finite witnesses for CONTEXT_DOMAIN.md, not a physical operation law.

These rational real-symmetric examples check restricted record-context domains,
conditional cuts, and unresolved choices. They do not select physical states or
tests, derive their accessibility, supply an executor, or reconstruct QM. Matrix
positivity is certified by nonnegative outer-product decompositions or strict
diagonal dominance, never by a numerical eigenvalue tolerance.

Run directly with Python, including ``python -O check.py``. All substantive
checks use unittest assertions, which remain active under optimization. No DET8
modules, external libraries, or random sampling are used.
"""

import unittest
from fractions import Fraction as F

Matrix = tuple[tuple[F, ...], ...]
Event = tuple[int, ...]
Partition = tuple[Event, ...]


def matrix(rows) -> Matrix:
    return tuple(tuple(F(value) for value in row) for row in rows)


def zeros(n: int) -> Matrix:
    return matrix(((0,) * n,) * n)


def identity(n: int) -> Matrix:
    return matrix(tuple(tuple(int(i == j) for j in range(n)) for i in range(n)))


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


def congruence(operator: Matrix, a: Matrix) -> Matrix:
    return multiply(multiply(operator, a), transpose(operator))


def outer(v) -> Matrix:
    return matrix(tuple(tuple(x * y for y in v) for x in v))


def tensor(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(x * y for x in ar for y in br) for ar in a for br in b)


def event_pair(a: Matrix, event: Event, other: Event) -> F:
    return sum((a[i][j] for i in event for j in other), F(0))


def mass(a: Matrix) -> F:
    """The total-entry DET mass, not the matrix trace."""
    return sum((sum(row, F(0)) for row in a), F(0))


def weights(a: Matrix, partition: Partition) -> tuple[F, ...]:
    return tuple(event_pair(a, event, event) for event in partition)


def recordable(a: Matrix, partition: Partition) -> bool:
    return all(
        event_pair(a, event, other) == 0
        for i, event in enumerate(partition)
        for other in partition[i + 1 :]
    )


def cut(a: Matrix, event: Event) -> Matrix:
    """A supplied conditional-history cut, not a DET-selected update."""
    return tuple(
        tuple(value if i in event and j in event else F(0) for j, value in enumerate(row))
        for i, row in enumerate(a)
    )


def normalize_positive(a: Matrix) -> Matrix:
    probability = mass(a)
    if probability <= 0:
        raise ValueError("A conditional state requires strictly positive branch mass")
    return scale(1 / probability, a)


def canonical_partition(blocks) -> Partition:
    return tuple(sorted(tuple(sorted(block)) for block in blocks))


def set_partitions(n: int) -> tuple[Partition, ...]:
    """Enumerate the finite set partitions used only by the five-atom witness."""
    partitions: set[Partition] = {()}
    for atom in range(n):
        next_partitions: set[Partition] = set()
        for partition in partitions:
            next_partitions.add(canonical_partition((*partition, (atom,))))
            for k in range(len(partition)):
                blocks = list(partition)
                blocks[k] = (*blocks[k], atom)
                next_partitions.add(canonical_partition(blocks))
        partitions = next_partitions
    return tuple(sorted(partitions))


P: Partition = ((0, 1), (2, 3))
Q: Partition = ((0, 2), (1, 3))


def four_atom_kernel(c: F) -> Matrix:
    return matrix(
        ((F(1, 4), c, 0, 0), (c, F(1, 4), 0, 0), (0, 0, F(1, 4), -c), (0, 0, -c, F(1, 4)))
    )


def cycle_kernel() -> Matrix:
    return matrix(
        tuple(
            tuple(
                F(1, 5) if i == j else F(1, 40) * (1 if (i - j) % 5 in (1, 4) else -1)
                for j in range(5)
            )
            for i in range(5)
        )
    )


class RecordContextDomainWitnessChecks(unittest.TestCase):
    def assert_normalized(self, a: Matrix) -> None:
        self.assertEqual(transpose(a), a)
        self.assertEqual(mass(a), F(1))

    def assert_four_atom_psd(self, d: Matrix, c: F) -> None:
        vectors = ((1, 1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 1), (0, 0, 1, -1))
        coefficients = (
            (F(1, 4) + c) / 2,
            (F(1, 4) - c) / 2,
            (F(1, 4) - c) / 2,
            (F(1, 4) + c) / 2,
        )
        certificate = zeros(4)
        for coefficient, vector in zip(coefficients, vectors, strict=True):
            self.assertGreater(coefficient, F(0))
            certificate = add(certificate, scale(coefficient, outer(vector)))
        self.assertEqual(certificate, d)

    def test_two_recordable_contexts_do_not_survive_each_others_cut(self):
        for c in (F(1, 8), F(-1, 8)):
            d = four_atom_kernel(c)
            self.assert_four_atom_psd(d, c)
            self.assert_normalized(d)
            self.assertTrue(recordable(d, P))
            self.assertTrue(recordable(d, Q))
            self.assertEqual(weights(d, P), (F(1, 2) + 2 * c, F(1, 2) - 2 * c))
            self.assertEqual(weights(d, Q), (F(1, 2), F(1, 2)))
            mu = weights(d, P)[0]
            conditional = normalize_positive(cut(d, P[0]))
            self.assertEqual(event_pair(conditional, *Q), c / mu)
            self.assertFalse(recordable(conditional, Q))
            self.assertEqual(sum(weights(conditional, Q), F(0)), 1 / (2 * mu))
            self.assertEqual(1 / (2 * mu), F(2, 3) if c > 0 else F(2))
            finest = tuple((i,) for i in range(4))
            self.assertFalse(recordable(d, finest))

    def test_positive_conditional_cuts_are_normalized_psd_and_repeatable(self):
        for c in (F(1, 8), F(-1, 8)):
            d = four_atom_kernel(c)
            self.assert_four_atom_psd(d, c)
            for k, event in enumerate(P):
                projector = matrix(
                    tuple(tuple(int(i == j and i in event) for j in range(4)) for i in range(4))
                )
                branch = cut(d, event)
                # Projection congruence of the certified PSD input proves branch PSD.
                self.assertEqual(branch, congruence(projector, d))
                mu = weights(d, P)[k]
                self.assertGreater(mu, F(0))
                conditional = normalize_positive(branch)
                self.assertEqual(conditional, scale(1 / mu, branch))
                self.assert_normalized(conditional)
                self.assertTrue(recordable(conditional, P))
                self.assertEqual(weights(conditional, P), (F(1 - k), F(k)))
                self.assertEqual(normalize_positive(cut(conditional, event)), conditional)

    def test_zero_mass_nonzero_branch_has_no_normalized_conditional_state(self):
        d = matrix(((1, -1, 0), (-1, 1, 0), (0, 0, 1)))
        self.assertEqual(d, add(outer((1, -1, 0)), outer((0, 0, 1))))
        self.assert_normalized(d)
        partition = ((0, 1), (2,))
        self.assertTrue(recordable(d, partition))
        self.assertEqual(weights(d, partition), (F(0), F(1)))
        zero_mass_branch = cut(d, partition[0])
        self.assertEqual(zero_mass_branch, outer((1, -1, 0)))
        self.assertNotEqual(zero_mass_branch, zeros(3))
        self.assertEqual(mass(zero_mass_branch), F(0))
        with self.assertRaisesRegex(ValueError, "strictly positive"):
            normalize_positive(zero_mass_branch)

    def test_fixed_context_convex_mixtures_and_coarsenings_keep_weights(self):
        kernels = tuple(four_atom_kernel(c) for c in (F(1, 8), F(-1, 8), F(0)))
        coefficients = (F(1, 2), F(1, 3), F(1, 6))
        mixture = zeros(4)
        expected_weights = [F(0), F(0)]
        for coefficient, c, d in zip(coefficients, (F(1, 8), F(-1, 8), F(0)), kernels, strict=True):
            self.assertGreaterEqual(coefficient, F(0))
            self.assert_four_atom_psd(d, c)
            self.assertTrue(recordable(d, P))
            mixture = add(mixture, scale(coefficient, d))
            expected_weights = [
                old + coefficient * weight
                for old, weight in zip(expected_weights, weights(d, P), strict=True)
            ]
        self.assertEqual(sum(coefficients, F(0)), F(1))
        self.assert_normalized(mixture)
        self.assertTrue(recordable(mixture, P))
        self.assertEqual(weights(mixture, P), tuple(expected_weights))
        coarse = ((0, 1, 2, 3),)
        self.assertTrue(recordable(mixture, coarse))
        self.assertEqual(weights(mixture, coarse), (sum(expected_weights, F(0)),))
        self.assertEqual(weights(mixture, coarse), (F(1),))

    def test_product_partition_closure_multiplies_exact_weights(self):
        d, e = four_atom_kernel(F(1, 8)), four_atom_kernel(F(-1, 8))
        self.assert_four_atom_psd(d, F(1, 8))
        self.assert_four_atom_psd(e, F(-1, 8))
        joint = tensor(d, e)
        # Tensor products of the checked nonnegative outer-product decompositions
        # give a nonnegative outer-product decomposition of the joint kernel.
        partition = tuple(tuple(4 * i + j for i in a for j in b) for a in P for b in Q)
        self.assert_normalized(joint)
        self.assertTrue(recordable(joint, partition))
        self.assertEqual(
            weights(joint, partition), tuple(x * y for x in weights(d, P) for y in weights(e, Q))
        )
        for a in P:
            for b in Q:
                for aa in P:
                    for bb in Q:
                        self.assertEqual(
                            event_pair(
                                joint,
                                tuple(4 * i + j for i in a for j in b),
                                tuple(4 * i + j for i in aa for j in bb),
                            ),
                            event_pair(d, a, aa) * event_pair(e, b, bb),
                        )

    def test_coarse_history_cut_differs_from_discarding_fine_outcomes(self):
        d = scale(F(1, 3), matrix(((1, 0, F(1, 2)), (0, 1, F(-1, 2)), (F(1, 2), F(-1, 2), 1))))
        certificate = zeros(3)
        for vector in ((1, 0, 1), (0, 1, -1), (1, 0, 0), (0, 1, 0)):
            certificate = add(certificate, scale(F(1, 6), outer(vector)))
        self.assertEqual(d, certificate)
        self.assert_normalized(d)
        partition = ((0, 1), (2,))
        self.assertTrue(recordable(d, partition))
        self.assertEqual(weights(d, partition), (F(2, 3), F(1, 3)))
        coarse_cut = cut(d, (0, 1, 2))
        discarded_fine = add(cut(d, partition[0]), cut(d, partition[1]))
        self.assertEqual(coarse_cut, d)
        self.assertNotEqual(coarse_cut, discarded_fine)
        self.assertEqual(discarded_fine, scale(F(1, 3), identity(3)))
        self.assertEqual(mass(coarse_cut), mass(discarded_fine))
        self.assertEqual(weights(coarse_cut, partition), weights(discarded_fine, partition))

    def test_same_record_probabilities_and_repeatability_do_not_select_reset(self):
        d = four_atom_kernel(F(1, 8))
        mu = weights(d, P)[0]
        cut_state = normalize_positive(cut(d, P[0]))
        alternatives = (outer((1, 0, 0, 0)), outer((0, 1, 0, 0)))
        for state in alternatives:
            # Supplied maps B_r(d)=mu_r(d) state_r are positive: mu_r is
            # nonnegative on PSD inputs and each output is a rank-one PSD kernel.
            branch = scale(mu, state)
            self.assertEqual(mass(branch), mu)
            self.assertEqual(normalize_positive(branch), state)
            self.assert_normalized(state)
            self.assertTrue(recordable(state, P))
            self.assertEqual(weights(state, P), (F(1), F(0)))
            self.assertNotEqual(state, cut_state)
        self.assertNotEqual(*alternatives)
        # Completing the second outcome with atom 2 gives the same full P law.
        for state in alternatives:
            branches = (scale(mu, state), scale(1 - mu, outer((0, 0, 1, 0))))
            self.assertEqual(tuple(mass(branch) for branch in branches), weights(d, P))

    def test_cyclic_kernel_has_five_recordable_binary_contexts_not_finest(self):
        d = cycle_kernel()
        self.assert_normalized(d)
        # Real symmetry plus positive strict diagonal dominance certifies positive
        # definiteness by the exact quadratic-form bound (or Gershgorin).
        for i, row in enumerate(d):
            self.assertGreater(row[i], sum((abs(x) for j, x in enumerate(row) if j != i), F(0)))
            self.assertEqual(sum((x for j, x in enumerate(row) if j != i), F(0)), F(0))
            partition = ((i,), tuple(j for j in range(5) if j != i))
            self.assertTrue(recordable(d, partition))
            self.assertEqual(weights(d, partition), (F(1, 5), F(4, 5)))
        self.assertFalse(recordable(d, tuple((i,) for i in range(5))))
        rotated = tuple(tuple(d[(i + 1) % 5][(j + 1) % 5] for j in range(5)) for i in range(5))
        self.assertEqual(rotated, d)

    def test_cyclic_symmetry_selects_no_invariant_nontrivial_recordable_partition(self):
        def rotate(partition: Partition) -> Partition:
            return canonical_partition(
                tuple(tuple((i + 1) % 5 for i in block) for block in partition)
            )

        contexts = tuple(
            canonical_partition(((i,), tuple(j for j in range(5) if j != i))) for i in range(5)
        )
        self.assertEqual(len(set(contexts)), 5)
        self.assertEqual({rotate(context) for context in contexts}, set(contexts))
        for context in contexts:
            self.assertNotEqual(rotate(context), context)
        partitions = set_partitions(5)
        self.assertEqual(len(partitions), 52)
        fixed = {partition for partition in partitions if rotate(partition) == partition}
        trivial = ((0, 1, 2, 3, 4),)
        finest = tuple((i,) for i in range(5))
        self.assertEqual(fixed, {trivial, finest})
        self.assertEqual(
            {partition for partition in fixed if recordable(cycle_kernel(), partition)}, {trivial}
        )

    def test_nonunitary_silent_congruence_preserves_a_declared_context(self):
        j = matrix(((1, 1), (1, 1)))
        w = outer((1, -1))
        local = scale(F(1, 2), add(j, scale(F(2), w)))
        local_inverse = scale(F(1, 2), add(j, scale(F(1, 2), w)))

        def block_diagonal(a: Matrix) -> Matrix:
            return tuple(
                tuple(a[i % 2][k % 2] if i // 2 == k // 2 else F(0) for k in range(4))
                for i in range(4)
            )

        operator, inverse = block_diagonal(local), block_diagonal(local_inverse)
        self.assertEqual(multiply(operator, inverse), identity(4))
        self.assertEqual(multiply(inverse, operator), identity(4))
        self.assertNotEqual(multiply(transpose(operator), operator), identity(4))
        for event in P:
            indicator = matrix(tuple((int(i in event),) for i in range(4)))
            self.assertEqual(multiply(transpose(operator), indicator), indicator)
        for c in (F(1, 8), F(-1, 8)):
            d = four_atom_kernel(c)
            self.assert_four_atom_psd(d, c)
            changed = congruence(operator, d)
            # Congruence of a PSD matrix is PSD; inverse congruence is also positive.
            self.assert_normalized(changed)
            self.assertTrue(recordable(changed, P))
            self.assertEqual(weights(changed, P), weights(d, P))
            for event in P:
                for other in P:
                    self.assertEqual(event_pair(changed, event, other), event_pair(d, event, other))
            self.assertNotEqual(changed, d)
            self.assertEqual(congruence(inverse, changed), d)


if __name__ == "__main__":
    unittest.main(verbosity=2)
