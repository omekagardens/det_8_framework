"""Independent exact certificates for a supplied maximal recordability cone.

The tests use rational real/imaginary pairs for independent matrix algebra.
They check finite identities and counterexamples, not the general theorem by
sampling and not physical preparation/operation availability. Run normally or
with -O: unittest assertions remain enabled in either case.
"""

import unittest
from fractions import Fraction as F

import model as m

P = m.Partition(((0,), (1, 2), (3, 4, 5)))
Q = m.Partition(((0, 1), (2, 3)))
Z = (F(0), F(0))


def pair(value):
    if isinstance(value, m.G):
        return value.real, value.imag
    if isinstance(value, tuple):
        return value
    return F(value), F(0)


def plus(left, right):
    a, b = pair(left)
    c, d = pair(right)
    return a + c, b + d


def times(left, right):
    a, b = pair(left)
    c, d = pair(right)
    return a * c - b * d, a * d + b * c


def conjugate(value):
    a, b = pair(value)
    return a, -b


def total(values):
    result = Z
    for value in values:
        result = plus(result, value)
    return result


def convert(rows):
    return m.matrix(tuple(m.G(*pair(value)) for value in row) for row in rows)


def add(left, right):
    return convert(
        tuple(plus(a, b) for a, b in zip(x, y, strict=True))
        for x, y in zip(left, right, strict=True)
    )


def scale(value, operator):
    return convert(tuple(times(value, entry) for entry in row) for row in operator)


def mm(left, right):
    return convert(
        tuple(
            total(times(left[i][k], right[k][j]) for k in range(len(right)))
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def outer(left, right=None):
    right = left if right is None else right
    return convert(tuple(times(a, conjugate(b)) for b in right) for a in left)


def vector_sum(left, right, coefficient=1):
    return tuple(plus(a, times(coefficient, b)) for a, b in zip(left, right, strict=True))


def trace_pair(left, right):
    return total(times(left[i][j], right[j][i]) for i in range(len(left)) for j in range(len(left)))


def direct_weights(operator, partition):
    return tuple(total(operator[i][j] for i in cell for j in cell) for cell in partition.cells)


def flatten(operator):
    return tuple(component for row in operator for entry in row for component in pair(entry))


def rank(rows):
    """Independent exact real Gaussian elimination, with no model rank helper."""
    rows = [list(map(F, row)) for row in rows]
    if not rows:
        return 0
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(pivot_row, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        divisor = rows[pivot_row][column]
        rows[pivot_row] = [entry / divisor for entry in rows[pivot_row]]
        for i in range(len(rows)):
            if i != pivot_row:
                coefficient = rows[i][column]
                rows[i] = [
                    a - coefficient * b for a, b in zip(rows[i], rows[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def direct_visible(partition):
    return tuple(
        tuple(F(int(i in cell), len(cell)) for i in range(partition.n)) for cell in partition.cells
    )


def direct_dark(partition):
    return tuple(
        tuple(F(int(i == atom) - int(i == cell[0])) for i in range(partition.n))
        for cell in partition.cells
        for atom in cell[1:]
    )


def real_product(left, right):
    return tuple(
        tuple(
            sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


class MaximalDomainChecks(unittest.TestCase):
    def test_gaussian_rationals_match_independent_pair_arithmetic(self):
        scalars = (m.G(), m.G(2, -3), m.G(F(1, 3), F(2, 5)), m.I)
        for a in scalars:
            self.assertEqual(pair(a.conjugate()), conjugate(a))
            self.assertEqual(a.norm_squared(), a.real**2 + a.imag**2)
            for b in scalars:
                self.assertEqual(pair(a + b), plus(a, b))
                self.assertEqual(pair(a * b), times(a, b))
                if b != 0:
                    self.assertEqual((a / b) * b, a)
        for value in (0.5, True, complex(0, 1)):
            with self.assertRaises(TypeError):
                m.G(value)
        with self.assertRaises(ZeroDivisionError):
            m.I / 0

    def test_partition_validation_unequal_cells_and_exact_coverage(self):
        self.assertEqual((P.n, P.k), (6, 3))
        self.assertEqual(tuple(map(len, P.cells)), (1, 2, 3))
        for cells in ((), ((),), ((0, 1), (1, 2)), ((0,), (2,)), ((-1,),), ((True,),), ((F(0),),)):
            with self.assertRaises(ValueError):
                m.Partition(cells)
        with self.assertRaises(ValueError):
            m.Partition(((0, 1),), n=3)
        with self.assertRaises(ValueError):
            m.Partition(((0,),), n=True)

    def test_visible_dark_duality_uses_cell_size_not_equal_cell_assumption(self):
        visible, dark = direct_visible(P), direct_dark(P)
        self.assertEqual(m.visible_vectors(P), visible)
        self.assertEqual(m.dark_basis(P), dark)
        for r, cell in enumerate(P.cells):
            for s, v in enumerate(visible):
                self.assertEqual(sum((v[i] for i in cell), F(0)), int(r == s))
            for w in dark:
                self.assertEqual(sum((w[i] for i in cell), F(0)), 0)
        self.assertEqual(rank(visible + dark), P.n)

    def test_real_rank_one_dark_families_keep_exact_records_and_unit_mass(self):
        for r, v in enumerate(direct_visible(P)):
            expected = tuple(F(int(r == s)) for s in range(P.k))
            for w in direct_dark(P):
                for t in (F(-3), F(-1, 2), F(0), F(2, 3), F(5)):
                    d = outer(vector_sum(v, w, t))
                    self.assertEqual(m.kernel(d, P, normalized=True), d)
                    self.assertEqual(m.q(d, P), expected)
                    self.assertEqual(direct_weights(d, P), tuple((x, F(0)) for x in expected))
                    self.assertEqual(m.mass(d), 1)

    def test_imaginary_rank_one_dark_families_keep_exact_records_and_unit_mass(self):
        for r, v in enumerate(direct_visible(P)):
            expected = tuple(F(int(r == s)) for s in range(P.k))
            for w in direct_dark(P):
                for t in (F(-2), F(-1, 3), F(1, 2), F(4)):
                    d = outer(vector_sum(v, w, (F(0), t)))
                    self.assertTrue(m.is_psd(d))
                    self.assertTrue(m.in_span(d, P))
                    self.assertEqual(m.q(d, P), expected)
                    self.assertEqual(m.mass(d), 1)

    def test_nonzero_positive_dark_directions_have_zero_mass_and_records(self):
        dark = direct_dark(P)
        vectors = (*dark, vector_sum(dark[0], dark[1], (0, 1)))
        for w in vectors:
            d = outer(w)
            self.assertNotEqual(d, m.zeros(P.n))
            self.assertEqual(m.kernel(d, P), d)
            self.assertEqual(m.q(d, P), (0, 0, 0))
            self.assertEqual(m.mass(d), 0)
            with self.assertRaises(ValueError):
                m.kernel(d, P, normalized=True)

    def test_full_real_span_dimension_and_quotient_kernel_rank_are_exact(self):
        basis = m.span_basis(P)
        expected = P.n**2 - P.k * (P.k - 1)
        self.assertEqual(len(basis), expected)
        self.assertEqual(m.span_dimension(P), expected)
        self.assertEqual(rank(tuple(flatten(d) for d in basis)), expected)
        self.assertTrue(all(m.in_span(d, P) for d in basis))
        quotient_rows = tuple(m.q(d, P) for d in basis)
        self.assertEqual(rank(quotient_rows), P.k)
        invisible = tuple(d for d in basis if m.q(d, P) == (0,) * P.k)
        self.assertEqual(rank(tuple(flatten(d) for d in invisible)), P.n**2 - P.k**2)
        self.assertTrue(any(entry.imag for d in invisible for row in d for entry in row))

    def test_visible_dark_polarizations_are_differences_of_recordable_psd_inputs(self):
        for v in direct_visible(P):
            for w in direct_dark(P):
                base = add(outer(v), outer(w))
                forward, backward = outer(v, w), outer(w, v)
                real_cross = add(forward, backward)
                imag_cross = add(scale((0, 1), forward), scale((0, -1), backward))
                real_positive = outer(vector_sum(v, w))
                imag_positive = outer(vector_sum(v, w, (0, -1)))
                self.assertEqual(add(real_positive, scale(-1, base)), real_cross)
                self.assertEqual(add(imag_positive, scale(-1, base)), imag_cross)
                for d in (outer(v), outer(w), real_positive, imag_positive):
                    self.assertEqual(m.kernel(d, P), d)
                for d in (real_cross, imag_cross):
                    self.assertEqual(m.q(d, P), (0, 0, 0))

    def test_dark_polarizations_span_the_entire_dark_hermitian_block(self):
        dark = direct_dark(P)
        basis = [outer(w) for w in dark]
        for i, w in enumerate(dark):
            for z in dark[i + 1 :]:
                base = add(outer(w), outer(z))
                for coefficient in (1, (0, -1)):
                    positive = outer(vector_sum(w, z, coefficient))
                    cross = add(positive, scale(-1, base))
                    self.assertTrue(m.is_psd(positive))
                    self.assertEqual(m.q(positive, P), (0, 0, 0))
                    basis.append(cross)
        self.assertEqual(rank(tuple(flatten(d) for d in basis)), (P.n - P.k) ** 2)

    def test_positive_section_is_surjective_and_its_linear_extension_is_signed(self):
        for weights in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (F(1, 6), F(1, 3), F(1, 2)), (2, 3, 7)):
            d = m.section(weights, P)
            self.assertEqual(m.q(d, P), weights)
            self.assertEqual(m.mass(d), sum(weights))
            self.assertEqual(m.kernel(d, P), d)
        signed = m.section((1, -2, 3), P)
        self.assertTrue(m.in_span(signed, P))
        self.assertFalse(m.is_psd(signed))
        self.assertEqual(m.q(signed, P), (1, -2, 3))
        with self.assertRaises(ValueError):
            m.section((1, 2), P)

    def test_one_cell_boundary_is_the_full_hermitian_space(self):
        one = m.Partition(((0, 1, 2),))
        basis = m.span_basis(one)
        self.assertEqual(len(basis), 9)
        self.assertEqual(rank(tuple(flatten(d) for d in basis)), 9)
        d = convert(((1, (0, 2), -3), ((0, -2), 4, (1, -1)), (-3, (1, 1), -2)))
        self.assertTrue(m.in_span(d, one))
        self.assertFalse(m.is_psd(d))
        self.assertEqual(m.q(d, one), (m.mass(d),))

    def test_singleton_boundary_has_only_diagonal_recordable_kernels(self):
        singletons = m.Partition(((0,), (1,), (2,)))
        basis = m.span_basis(singletons)
        self.assertEqual(m.dark_basis(singletons), ())
        self.assertEqual(rank(tuple(flatten(d) for d in basis)), 3)
        self.assertEqual(m.q(m.section((1, 2, 3), singletons), singletons), (1, 2, 3))
        for coefficient in (1, (0, 1)):
            coherent = outer((1, coefficient, 0))
            self.assertTrue(m.is_psd(coherent))
            self.assertFalse(m.in_span(coherent, singletons))
            with self.assertRaises(ValueError):
                m.kernel(coherent, singletons)

    def test_bounded_cell_effects_and_invalid_coefficients(self):
        coefficients = (F(1, 4), F(1), F(0))
        for r, v in enumerate(direct_visible(P)):
            for w in direct_dark(P):
                for t in (-3, 0, 2):
                    d = outer(vector_sum(v, w, (0, t)))
                    effect = m.bounded_effect(d, P, coefficients)
                    self.assertEqual(effect, coefficients[r])
                    self.assertGreaterEqual(effect, 0)
                    self.assertLessEqual(effect, m.mass(d))
        for coefficients in ((-1, 0, 0), (0, 2, 0), (0, 1), (True, 0, 0)):
            with self.assertRaises((ValueError, TypeError)):
                m.bounded_effect(m.section((1, 0, 0), P), P, coefficients)

    def test_ambient_off_visible_representers_restrict_to_the_zero_functional(self):
        b0, b1, _ = m.indicator_vectors(P)
        forward, backward = outer(b0, b1), outer(b1, b0)
        for representer in (
            add(forward, backward),
            add(scale((0, 1), forward), scale((0, -1), backward)),
        ):
            self.assertNotEqual(representer, m.zeros(P.n))
            for d in m.span_basis(P):
                self.assertEqual(trace_pair(representer, d), Z)
        # An ambient matrix representative is not uniquely determined by its
        # restriction to the recordability span.

    def test_measure_prepare_factors_arbitrary_substochastic_transition(self):
        transition = ((F(1, 4), F(1, 3), 0), (F(1, 2), 0, 1))
        self.assertEqual(m.substochastic(transition, P, Q), transition)
        for d in m.span_basis(P):
            output = m.measure_prepare(d, P, Q, transition)
            expected = tuple(
                sum((a * x for a, x in zip(row, m.q(d, P), strict=True)), F(0))
                for row in transition
            )
            self.assertEqual(m.q(output, Q), expected)
            self.assertEqual(output, m.section(expected, Q))
        for weights in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (F(1, 3), F(1, 3), F(1, 3))):
            d = add(m.section(weights, P), outer(direct_dark(P)[0]))
            output = m.measure_prepare(d, P, Q, transition)
            self.assertEqual(m.kernel(output, Q), output)
            self.assertLessEqual(m.mass(output), m.mass(d))

    def test_complete_labeled_family_keeps_each_mass_and_residual_separate(self):
        first = ((F(1, 4), F(1, 3), 0), (F(1, 2), 0, F(1, 2)))
        second = ((F(1, 4), F(2, 3), F(1, 2)), (0, 0, 0))
        family = ((("P", "prepare", "a", "Q"), first), (("P", "prepare", "b", "Q"), second))
        d = add(m.section((F(1, 5), F(3, 10), F(1, 2)), P), outer(direct_dark(P)[0]))
        outputs = tuple(
            (label, m.measure_prepare(d, P, Q, transition)) for label, transition in family
        )
        self.assertEqual(tuple(label for label, _ in outputs), tuple(label for label, _ in family))
        self.assertEqual(sum((m.mass(output) for _, output in outputs), F(0)), 1)
        self.assertNotEqual(outputs[0][1], outputs[1][1])
        for _, output in outputs:
            probability = m.mass(output)
            self.assertGreater(probability, 0)
            self.assertEqual(
                m.kernel(scale(1 / probability, output), Q, normalized=True),
                scale(1 / probability, output),
            )

    def test_measure_prepare_composition_matches_classical_matrix_composition(self):
        target = m.Partition(((0,), (1,), (2,)))
        first = ((F(1, 4), F(1, 3), 0), (F(1, 2), 0, 1))
        second = ((F(1, 2), 0), (0, F(1, 3)), (F(1, 4), F(1, 2)))
        composite = real_product(second, first)
        for d in m.span_basis(P):
            sequential = m.measure_prepare(m.measure_prepare(d, P, Q, first), Q, target, second)
            direct = m.measure_prepare(d, P, target, composite)
            self.assertEqual(sequential, direct)

    def test_one_shot_rows_and_signed_span_extensions_are_not_consumed_twice(self):
        transition = ((F(1, 4), F(1, 3), 0), (F(1, 2), 0, 1))
        coefficients = (F(1, 4), F(1, 2), F(3, 4))
        positive = m.section((1, 0, 2), P)
        negative = m.section((0, 3, 0), P)
        signed = add(positive, scale(-1, negative))
        self.assertTrue(m.in_span(signed, P))
        self.assertFalse(m.is_psd(signed))

        def one_shot(d):
            return ((entry for entry in row) for row in d)

        self.assertEqual(
            m.measure_prepare(one_shot(signed), P, Q, transition),
            m.measure_prepare(signed, P, Q, transition),
        )
        self.assertEqual(
            m.bounded_effect(one_shot(signed), P, coefficients),
            m.bounded_effect(signed, P, coefficients),
        )
        self.assertEqual(
            m.measure_prepare(signed, P, Q, transition),
            add(
                m.measure_prepare(positive, P, Q, transition),
                scale(-1, m.measure_prepare(negative, P, Q, transition)),
            ),
        )
        self.assertEqual(
            m.bounded_effect(signed, P, coefficients),
            m.bounded_effect(positive, P, coefficients)
            - m.bounded_effect(negative, P, coefficients),
        )

    def test_identity_and_reset_have_same_cell_law_but_different_dark_residuals(self):
        transition = tuple(tuple(F(int(i == j)) for j in range(P.k)) for i in range(P.k))
        d = add(m.section((1, 0, 0), P), outer(direct_dark(P)[0]))
        reset = m.measure_prepare(d, P, P, transition)
        self.assertEqual(m.q(reset, P), m.q(d, P))
        self.assertNotEqual(reset, d)
        self.assertEqual(m.mass(reset), m.mass(d))
        dark = outer(direct_dark(P)[0])
        self.assertNotEqual(dark, m.zeros(P.n))
        self.assertEqual(m.mass(dark), 0)
        self.assertEqual(m.measure_prepare(dark, P, P, transition), m.zeros(P.n))
        with self.assertRaises(ValueError):
            m.kernel(dark, P, normalized=True)

    def test_old_selected_shape_effect_is_not_bounded_on_the_maximal_cone(self):
        one = m.Partition(((0, 1),))
        a = convert(((F(1, 3), F(1, 6)), (F(1, 6), F(1, 3))))
        b = convert(((1, F(-1, 2)), (F(-1, 2), 1)))

        def selected_shape_effect(d):
            return F(3, 4) * (d[0][0].real + d[1][1].real) + 3 * d[0][1].real

        self.assertEqual(m.q(a, one), m.q(b, one))
        self.assertEqual(m.mass(a), 1)
        self.assertEqual(m.mass(b), 1)
        self.assertEqual(selected_shape_effect(a), 1)
        self.assertEqual(selected_shape_effect(b), 0)
        for t, expected in ((0, F(9, 8)), (1, F(-3, 8))):
            d = outer(vector_sum((F(1, 2), F(1, 2)), (1, -1), t))
            self.assertEqual(m.kernel(d, one, normalized=True), d)
            self.assertEqual(selected_shape_effect(d), expected)
        # Thus separation on the selected a/b cone is not a counterexample
        # to the bounded-effect theorem on the entire maximal cone.

    def test_full_cone_silent_map_and_commit_have_complete_mass(self):
        visible_projector = m.zeros(P.n)
        for b, cell in zip(m.indicator_vectors(P), P.cells, strict=True):
            visible_projector = add(visible_projector, scale(F(1, len(cell)), outer(b)))
        dark_projector = add(m.identity(P.n), scale(-1, visible_projector))
        operator = add(scale(F(1, 2), visible_projector), scale(2, dark_projector))
        self.assertEqual(mm(visible_projector, visible_projector), visible_projector)
        self.assertEqual(mm(dark_projector, dark_projector), dark_projector)
        self.assertEqual(mm(visible_projector, dark_projector), m.zeros(P.n))
        for d in m.span_basis(P):
            silent = mm(mm(operator, d), operator)
            commit = scale(F(3, 4), d)
            self.assertTrue(m.in_span(silent, P))
            self.assertEqual(m.q(silent, P), tuple(weight / 4 for weight in m.q(d, P)))
            self.assertEqual(m.mass(silent) + m.mass(commit), m.mass(d))

    def test_full_kernel_first_commit_series_diverges_while_quotient_converges(self):
        v, w = direct_visible(P)[0], direct_dark(P)[0]
        h, dark = outer(v), outer(w)
        silent_residual = add(h, dark)
        partial = m.zeros(P.n)
        for count in range(1, 9):
            partial = add(partial, scale(F(3, 4), silent_residual))
            silent_residual = add(scale(F(1, 4**count), h), scale(4**count, dark))
            expected = add(scale(1 - F(1, 4**count), h), scale(F(4**count - 1, 4), dark))
            self.assertEqual(partial, expected)
            self.assertEqual(m.kernel(partial, P), partial)
            self.assertEqual(m.q(partial, P), (1 - F(1, 4**count), 0, 0))
            self.assertEqual(m.mass(silent_residual), F(1, 4**count))
            self.assertEqual(m.mass(partial) + m.mass(silent_residual), 1)
            self.assertEqual(partial[1][1], F(4**count - 1, 4))
        # The displayed formula proves a divergent matrix entry and vanishing
        # remaining mass; no convergence of the full residual is asserted.

    def test_malformed_and_indefinite_kernels_are_rejected_without_repair(self):
        nonhermitian = convert(((1, (0, 1)), ((0, 1), 1)))
        indefinite = convert(((1, 2), (2, 1)))
        zero_diagonal_cross = convert(((0, (0, 1)), ((0, -1), 0)))
        one = m.Partition(((0, 1),))
        for d in (nonhermitian, indefinite, zero_diagonal_cross):
            self.assertFalse(m.is_psd(d))
            with self.assertRaises(ValueError):
                m.kernel(d, one)
        with self.assertRaises(ValueError):
            m.q(nonhermitian, one)
        with self.assertRaises(ValueError):
            m.matrix(((1, 2), (3,)))
        for transition in (((1, 1, 1),), ((-1, 0, 0), (0, 0, 0)), ((1, 0, 0), (1, 0, 0))):
            with self.assertRaises(ValueError):
                m.substochastic(transition, P, Q)


if __name__ == "__main__":
    unittest.main(verbosity=2)
