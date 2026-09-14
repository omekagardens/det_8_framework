"""Exact independent certificates for the fixed-image joint-repeatability result.

The native sixteen-label image, reference and extra same-image return rule are
declared separately from physical availability. Fine records always retain
both (a,b). Coarse b probabilities are analytic sums, not erased records or
classical-memory rereads. Relative and input-mass-normalized defects differ.
"""

import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F
from itertools import combinations, product

import model as m

ZERO = (F(0), F(0))


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


def conj(value):
    a, b = pair(value)
    return a, -b


def total(values):
    result = ZERO
    for value in values:
        result = plus(result, value)
    return result


def matrix(rows):
    return tuple(tuple(m.G(*pair(entry)) for entry in row) for row in rows)


def add(left, right):
    return matrix(
        tuple(plus(a, b) for a, b in zip(x, y, strict=True))
        for x, y in zip(left, right, strict=True)
    )


def scale(coefficient, operator):
    return matrix(tuple(times(coefficient, entry) for entry in row) for row in operator)


def transpose(operator):
    return matrix(
        tuple(operator[i][j] for i in range(len(operator))) for j in range(len(operator[0]))
    )


def dagger(operator):
    return matrix(
        tuple(conj(operator[i][j]) for i in range(len(operator))) for j in range(len(operator[0]))
    )


def mm(left, right):
    return matrix(
        tuple(
            total(
                times(left[i][k], right[k][j])
                for k in range(len(right))
                if pair(left[i][k]) != ZERO and pair(right[k][j]) != ZERO
            )
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def tensor(left, right):
    return matrix(
        tuple(
            times(left[a][b], right[i][j])
            for b in range(len(left[0]))
            for j in range(len(right[0]))
        )
        for a in range(len(left))
        for i in range(len(right))
    )


def eye(size):
    return matrix(tuple(int(i == j) for j in range(size)) for i in range(size))


def zeros(size):
    return matrix((0,) * size for _ in range(size))


def trace(operator):
    return total(operator[i][i] for i in range(len(operator)))


def flatten(operator):
    return tuple(component for row in operator for entry in row for component in pair(entry))


def rank(rows):
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
        rows[pivot_row] = [value / divisor for value in rows[pivot_row]]
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


Z = matrix(((1, 0), (0, -1)))
X = matrix(((0, 1), (1, 0)))
Y = matrix(((0, (0, -1)), ((0, 1), 0)))
H0 = matrix(((1, 1), (1, -1)))
CNOT = matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)))
U0 = mm(tensor(eye(2), H0), CNOT)
CELLS = tuple(product((0, 1), repeat=2))
BITS = tuple(product((0, 1), repeat=4))
PARAMETERS = (F(-1), F(-2, 3), F(-1, 2), F(0), F(1, 3), F(1, 2), F(1))
RHO = matrix(((F(3, 5), (F(1, 10), F(1, 5))), ((F(1, 10), F(-1, 5)), F(2, 5))))
CENTER = scale(F(1, 2), eye(2))
RHO_BASIS = (matrix(((1, 0), (0, 0))), matrix(((0, 0), (0, 1))), X, Y)


def native(a, i, b, j):
    return 8 * a + 4 * i + 2 * b + j


def grouped(a, b, i, j):
    return 8 * a + 4 * b + 2 * i + j


def retwist(operator):
    output = [[ZERO for _ in range(16)] for _ in range(16)]
    for a, i, b, j in BITS:
        for c, k, d, ell in BITS:
            sign = (-1) ** (a * i + b * j + c * k + d * ell)
            output[native(a, i, b, j)][native(c, k, d, ell)] = times(
                sign, operator[grouped(a, b, i, j)][grouped(c, d, k, ell)]
            )
    return matrix(output)


def untwist(operator):
    output = [[ZERO for _ in range(16)] for _ in range(16)]
    for a, i, b, j in BITS:
        for c, k, d, ell in BITS:
            sign = (-1) ** (a * i + b * j + c * k + d * ell)
            output[grouped(a, b, i, j)][grouped(c, d, k, ell)] = times(
                sign, operator[native(a, i, b, j)][native(c, k, d, ell)]
            )
    return matrix(output)


def block(operator, row, column):
    return matrix(operator[4 * row + i][4 * column : 4 * column + 4] for i in range(4))


def local_from(rho, c=0):
    a = scale(F(1, 2), transpose(rho))
    f, b = scale(c, Z), mm(mm(Z, a), Z)
    adjoint = dagger(f)
    return tuple(tuple(a[i]) + tuple(f[i]) for i in range(2)) + tuple(
        tuple(adjoint[i]) + tuple(b[i]) for i in range(2)
    )


def image(rho, t):
    a = scale(F(1, 2), transpose(rho))
    b = scale(F(1, 4), add(eye(2), scale(t, Z)))
    common = scale(F(1, 2), mm(mm(U0, tensor(a, b)), dagger(U0)))
    return retwist(tensor(eye(4), common))


def independent_inverse(operator):
    common = block(untwist(operator), 0, 0)
    product_block = scale(F(1, 2), mm(mm(dagger(U0), common), U0))
    reduced = matrix(
        tuple(total(product_block[2 * i + j][2 * k + j] for j in range(2)) for k in range(2))
        for i in range(2)
    )
    return scale(4, transpose(reduced))


def cell_indices(outcome):
    a, b = outcome
    return tuple(native(a, i, b, j) for i, j in product((0, 1), repeat=2))


def cell_form(operator, left, right):
    return total(operator[i][j] for i in cell_indices(left) for j in cell_indices(right))


def weights(operator):
    return tuple(cell_form(operator, cell, cell)[0] for cell in CELLS)


def raw_mass(operator):
    return total(entry for row in operator for entry in row)[0]


def pulled_effect(t, outcome):
    return scale(F(1, 4), add(eye(2), scale((-1) ** outcome[1] * t, Z)))


def fine_effect(rho, t, outcome):
    return trace(mm(rho, pulled_effect(t, outcome)))[0]


def coarse_effect(rho, t, b):
    return fine_effect(rho, t, (0, b)) + fine_effect(rho, t, (1, b))


def aligned_rho(t, outcome):
    if t == 0:
        return CENTER
    sign = 1 if ((-1) ** outcome[1]) * t > 0 else -1
    return scale(F(1, 2), add(eye(2), scale(sign, Z)))


def exact_optimal_branch(rho, t, outcome):
    return scale(fine_effect(rho, t, outcome), image(aligned_rho(t, outcome), t))


def prepared(t=F(1, 2), rho=RHO, setting_id="return-A"):
    local_records = (
        m.InputRecord(0, "prepare", "beam-ready", ("H", "P_inv"), (("sample", "L"),)),
        m.InputRecord(1, "calibrate", "pass", ("Z",), (("phase", "retained"),), (0,)),
    )
    reference_records = (m.InputRecord(0, "prepare", "probe-ready", ("Z",), (("sample", "R"),)),)
    local = m.LocalInput(local_from(rho), "beam", local_records)
    reference = m.ReferenceInput(t, "probe", reference_records)
    return m.prepare_state(
        local,
        reference,
        m.Independence(("beam", "probe")),
        joint_origin="joint-run",
        setting_id=setting_id,
    )


class JointRepeatabilityChecks(unittest.TestCase):
    def test_full_native_image_matches_independent_signed_permutation_and_congruence(self):
        for t in PARAMETERS:
            actual = m.image_span(RHO, t)
            expected = image(RHO, t)
            self.assertEqual(actual, expected)
            self.assertEqual(m.to_untwisted(actual), untwist(expected))
            self.assertEqual(m.from_untwisted(untwist(expected)), expected)
            self.assertEqual(m.inverse_span(actual, t), RHO)
            self.assertEqual(independent_inverse(actual), RHO)

    def test_native_and_grouped_labels_cover_all_sixteen_atoms(self):
        self.assertEqual({native(*bits) for bits in BITS}, set(range(16)))
        self.assertEqual({grouped(a, b, i, j) for a, i, b, j in BITS}, set(range(16)))
        for a, i, b, j in BITS:
            self.assertEqual(m.index_native(a, i, b, j), native(a, i, b, j))
            self.assertEqual(m.index_joint(a, b, i, j), grouped(a, b, i, j))
        self.assertEqual(
            tuple(cell_indices(cell) for cell in CELLS),
            ((0, 1, 4, 5), (2, 3, 6, 7), (8, 9, 12, 13), (10, 11, 14, 15)),
        )

    def test_pulled_fine_effects_are_derived_on_the_entire_hermitian_span(self):
        for t in PARAMETERS:
            for rho in RHO_BASIS:
                native_image = image(rho, t)
                for index, outcome in enumerate(CELLS):
                    effect = pulled_effect(t, outcome)
                    self.assertEqual(m.pulled_effect(t, outcome), effect)
                    self.assertEqual(weights(native_image)[index], fine_effect(rho, t, outcome))
                    self.assertEqual(
                        m.raw_cell_weights(native_image)[index], fine_effect(rho, t, outcome)
                    )
                for left, right in combinations(CELLS, 2):
                    self.assertEqual(cell_form(native_image, left, right), ZERO)
            self.assertEqual(rank(tuple(flatten(image(rho, t)) for rho in RHO_BASIS)), 4)
            self.assertEqual(
                rank(tuple(flatten(pulled_effect(t, cell)) for cell in CELLS)), 1 if t == 0 else 2
            )
        # Equality on four independent Hermitian directions is a full linear
        # certificate, including complex off-diagonal input, not PSD sampling.

    def test_joint_quotient_keeps_transpose_and_shared_conjugation_convention(self):
        self.assertEqual(scale(F(1, 2), mm(U0, dagger(U0))), eye(4))
        for t in PARAMETERS:
            raw = image(RHO, t)
            common = block(untwist(raw), 0, 0)
            quotient = scale(4, transpose(common))
            reference_rho = scale(F(1, 2), add(eye(2), scale(t, Z)))
            expected = scale(F(1, 2), mm(mm(U0, tensor(RHO, reference_rho)), transpose(U0)))
            self.assertEqual(quotient, expected)
            self.assertEqual(m.quotient_on_span(raw, t), expected)
            self.assertTrue(any(entry.imag for row in quotient for entry in row))

    def test_image_positive_mass_and_inverse_include_singular_endpoints(self):
        for t in PARAMETERS:
            for rho in (RHO, CENTER, *RHO_BASIS[:2]):
                raw = m.image(rho, t, normalized=True)
                self.assertEqual(raw, image(rho, t))
                self.assertTrue(m.is_psd(raw))
                self.assertEqual(m.inverse_image(raw, t, normalized=True), rho)
                self.assertEqual(raw_mass(raw), trace(rho)[0])
                self.assertEqual(m.raw_mass(raw), 1)
                self.assertEqual(sum(m.raw_cell_weights(raw)), 1)
                self.assertEqual(tuple(pair(value) for value in m.raw_crossforms(raw)), (ZERO,) * 6)

    def test_zero_unnormalized_and_signed_spans_are_distinguished(self):
        for t in (F(-1), F(0), F(1, 2), F(1)):
            for rho in (zeros(2), scale(3, RHO)):
                raw = m.image(rho, t)
                self.assertEqual(m.inverse_image(raw, t), rho)
                self.assertEqual(raw_mass(raw), trace(rho)[0])
                with self.assertRaises(ValueError):
                    m.image(rho, t, normalized=True)
            signed = add(RHO_BASIS[0], scale(-2, RHO_BASIS[1]))
            raw_signed = m.image_span(signed, t)
            self.assertEqual(m.inverse_span(raw_signed, t), signed)
            with self.assertRaises(ValueError):
                m.image(signed, t)
            with self.assertRaises(ValueError):
                m.inverse_image(raw_signed, t)

    def test_same_image_membership_checks_the_reference_and_all_raw_blocks(self):
        raw = image(RHO, F(1, 2))
        with self.assertRaises(ValueError):
            m.inverse_span(raw, F(-1, 2))
        altered_grouped = [list(row) for row in untwist(raw)]
        altered_grouped[4][4] += F(1, 100)
        altered = m.from_untwisted(matrix(altered_grouped))
        self.assertTrue(m.is_psd(altered))
        with self.assertRaises(ValueError):
            m.inverse_span(altered, F(1, 2))
        self.assertEqual(m.inverse_span(zeros(16), 0), zeros(2))
        self.assertEqual(m.inverse_span(zeros(16), 1), zeros(2))

    def test_t_zero_is_a_chosen_c_zero_image_not_the_prior_full_cone_exclusion(self):
        local = local_from(CENTER, F(1, 8))
        reference = local_from(CENTER)
        product_raw = tensor(local, reference)
        grouped_input = untwist(product_raw)
        lifted = tensor(eye(4), U0)
        coupled = retwist(scale(F(1, 2), mm(mm(lifted, grouped_input), dagger(lifted))))
        self.assertTrue(m.is_psd(coupled))
        self.assertEqual(raw_mass(coupled), 1)
        self.assertTrue(
            all(cell_form(coupled, left, right) == ZERO for left, right in combinations(CELLS, 2))
        )
        with self.assertRaises(ValueError):
            m.inverse_span(coupled, 0)
        self.assertNotEqual(coupled, image(CENTER, 0))

    def test_fine_effect_spectral_ceiling_and_relative_floor_are_exact(self):
        for t in PARAMETERS:
            ceiling = (1 + abs(t)) / 4
            self.assertEqual(m.fine_relative_floor(t), 1 - ceiling)
            for outcome in CELLS:
                effect = pulled_effect(t, outcome)
                self.assertTrue(m.is_psd(effect))
                self.assertTrue(m.is_psd(add(scale(ceiling, eye(2)), scale(-1, effect))))
                self.assertEqual(fine_effect(aligned_rho(t, outcome), t, outcome), ceiling)
                self.assertEqual(1 - ceiling, (3 - abs(t)) / 4)
                self.assertGreaterEqual(1 - ceiling, F(1, 2))

    def test_coarse_next_b_effect_has_a_different_spectral_ceiling(self):
        for t in PARAMETERS:
            ceiling = (1 + abs(t)) / 2
            self.assertEqual(m.b_relative_floor(t), 1 - ceiling)
            for b in (0, 1):
                expected = add(pulled_effect(t, (0, b)), pulled_effect(t, (1, b)))
                self.assertEqual(m.pulled_b_effect(t, b), expected)
                self.assertTrue(m.is_psd(add(scale(ceiling, eye(2)), scale(-1, expected))))
                self.assertEqual(coarse_effect(aligned_rho(t, (0, b)), t, b), ceiling)
                self.assertEqual(1 - ceiling, (1 - abs(t)) / 2)

    def test_algebraic_optimal_resets_are_positive_calibrated_and_complete(self):
        for t in PARAMETERS:
            device = m.optimal_instrument(t)
            for rho in (RHO, CENTER, *RHO_BASIS[:2]):
                raw = image(rho, t)
                outputs = tuple(device.branch(raw, outcome) for outcome in CELLS)
                for outcome, output in zip(CELLS, outputs, strict=True):
                    self.assertEqual(output, exact_optimal_branch(rho, t, outcome))
                    self.assertTrue(m.is_psd(output))
                    self.assertEqual(raw_mass(output), fine_effect(rho, t, outcome))
                    self.assertEqual(m.image_span(m.inverse_span(output, t), t), output)
                self.assertEqual(sum(raw_mass(output) for output in outputs), raw_mass(raw))

    def test_relative_optimality_is_simultaneous_for_all_four_full_branches(self):
        for t in PARAMETERS:
            device = m.optimal_instrument(t)
            fine_ceiling, coarse_ceiling = (1 + abs(t)) / 4, (1 + abs(t)) / 2
            for rho in RHO_BASIS:
                raw = image(rho, t)
                for outcome in CELLS:
                    output = device.branch_on_span(raw, outcome)
                    success_fine = weights(output)[CELLS.index(outcome)]
                    success_b = sum(
                        weight
                        for cell, weight in zip(CELLS, weights(output), strict=True)
                        if cell[1] == outcome[1]
                    )
                    self.assertEqual(success_fine, fine_ceiling * fine_effect(rho, t, outcome))
                    self.assertEqual(success_b, coarse_ceiling * fine_effect(rho, t, outcome))
        # These identities on the actual full Hermitian span establish the
        # branch-relative equalities, distinct from input-mass normalization.

    def test_fine_input_mass_normalized_optimum_is_not_the_relative_constant(self):
        for t in PARAMETERS:
            p = (1 + abs(t)) / 4
            device = m.optimal_instrument(t)
            optimum = p * (1 - p)
            self.assertEqual(m.fine_input_mass_floor(t), optimum)
            self.assertNotEqual(optimum, 1 - p)
            for outcome in CELLS:
                maximum_input = aligned_rho(t, outcome)
                output = device.branch(image(maximum_input, t), outcome)
                failure = raw_mass(output) - weights(output)[CELLS.index(outcome)]
                self.assertEqual(failure, optimum)
                deficit_effect = scale(1 - p, pulled_effect(t, outcome))
                self.assertTrue(m.is_psd(add(scale(optimum, eye(2)), scale(-1, deficit_effect))))

    def test_next_b_after_fine_and_aggregate_first_b_have_distinct_input_mass_bounds(self):
        for t in PARAMETERS:
            pf, pb = (1 + abs(t)) / 4, (1 + abs(t)) / 2
            self.assertEqual(m.b_after_fine_input_mass_floor(t), pf * (1 - pb))
            self.assertEqual(m.b_after_summed_b_input_mass_floor(t), pb * (1 - pb))
            device = m.optimal_instrument(t)
            for b in (0, 1):
                rho = aligned_rho(t, (0, b))
                raw = image(rho, t)
                fine_outputs = tuple(device.branch(raw, (a, b)) for a in (0, 1))
                for output in fine_outputs:
                    next_b = sum(
                        weight
                        for cell, weight in zip(CELLS, weights(output), strict=True)
                        if cell[1] == b
                    )
                    self.assertEqual(raw_mass(output) - next_b, pf * (1 - pb))
                    self.assertEqual(raw_mass(output) - next_b, (1 - t * t) / 8)
                aggregate = add(*fine_outputs)
                next_b = sum(
                    weight
                    for cell, weight in zip(CELLS, weights(aggregate), strict=True)
                    if cell[1] == b
                )
                self.assertEqual(raw_mass(aggregate) - next_b, pb * (1 - pb))
                self.assertEqual(raw_mass(aggregate) - next_b, (1 - t * t) / 4)

    def test_perfect_full_repeatability_has_no_normalized_same_image_target(self):
        for t in PARAMETERS:
            for outcome in CELLS:
                ceiling = (1 + abs(t)) / 4
                # I-E >= (1-ceiling)I >0, so a mass-one same-image target
                # cannot make the full (a,b) probability equal to one.
                failure_effect = add(eye(2), scale(-1, pulled_effect(t, outcome)))
                self.assertTrue(m.is_psd(add(failure_effect, scale(-(1 - ceiling), eye(2)))))
                self.assertGreater(1 - ceiling, 0)
                target = aligned_rho(t, outcome)
                self.assertEqual(fine_effect(target, t, outcome), ceiling)
                self.assertLess(fine_effect(target, t, outcome), 1)

    def test_t_zero_identity_scaled_branch_is_optimal_without_being_a_reset(self):
        t = F(0)
        device = m.optimal_instrument(t)
        images = tuple(scale(F(1, 4), image(rho, t)) for rho in RHO_BASIS)
        self.assertEqual(rank(tuple(flatten(output) for output in images)), 4)
        self.assertEqual(
            rank(tuple(flatten(device.branch_on_span(image(rho, t), (0, 0))) for rho in RHO_BASIS)),
            1,
        )
        source = image(RHO, t)
        output = scale(F(1, 4), source)
        self.assertNotEqual(output, device.branch(source, (0, 0)))
        self.assertEqual(raw_mass(output), F(1, 4))
        self.assertEqual(weights(output)[0], F(1, 16))
        self.assertEqual(raw_mass(output) - weights(output)[0], F(3, 16))
        self.assertEqual((raw_mass(output) - weights(output)[0]) / raw_mass(output), F(3, 4))
        self.assertEqual(sum(weights(output)[i] for i in (0, 2)) / raw_mass(output), F(1, 2))

    def test_absolute_minimax_does_not_imply_relative_optimal_reset_uniqueness(self):
        t, outcome = F(1, 2), (0, 0)
        high, low = F(3, 8), F(1, 8)

        def nonreset(rho):
            return matrix(((high * rho[0][0], 0), (0, low * rho[1][1])))

        for rho in (RHO, *RHO_BASIS[:2]):
            output = image(nonreset(rho), t)
            self.assertTrue(m.is_psd(output))
            self.assertEqual(raw_mass(output), fine_effect(rho, t, outcome))
            deficit = raw_mass(output) - weights(output)[0]
            self.assertLessEqual(deficit, high * (1 - high) * trace(rho)[0])
        high_output, low_output = (image(nonreset(rho), t) for rho in RHO_BASIS[:2])
        self.assertEqual(raw_mass(high_output) - weights(high_output)[0], F(15, 64))
        self.assertEqual(raw_mass(low_output) - weights(low_output)[0], F(7, 64))
        self.assertEqual(
            (raw_mass(low_output) - weights(low_output)[0]) / raw_mass(low_output), F(7, 8)
        )
        self.assertGreater(F(7, 8), F(5, 8))
        self.assertEqual(rank(tuple(flatten(image(nonreset(rho), t)) for rho in RHO_BASIS)), 2)

    def test_nonzero_t_relative_optimal_face_is_a_single_ray_not_a_general_uniqueness_claim(self):
        for t in (F(-1), F(-1, 2), F(1, 3), F(1)):
            for outcome in CELLS:
                target = aligned_rho(t, outcome)
                ceiling = (1 + abs(t)) / 4
                gap = add(scale(ceiling, eye(2)), scale(-1, pulled_effect(t, outcome)))
                self.assertEqual(mm(gap, target), zeros(2))
                self.assertEqual(trace(gap)[0], abs(t) / 2)
                opposite = add(eye(2), scale(-1, target))
                self.assertEqual(trace(mm(gap, opposite))[0], abs(t) / 2)
                self.assertEqual(
                    rank(
                        tuple(
                            flatten(m.optimal_instrument(t).branch_on_span(image(rho, t), outcome))
                            for rho in RHO_BASIS
                        )
                    ),
                    1,
                )
        # Positive outputs saturating the effect ceiling must lie in this
        # exposed ray. This does not characterize absolute-minimax optimizers.

    def test_preparation_retains_full_initial_context_without_replacing_native_image(self):
        state = prepared(F(-2, 3))
        context = state.context
        self.assertEqual(state.residual, image(RHO, F(-2, 3)))
        self.assertEqual(len(state.residual), 16)
        self.assertEqual(context.local.residual, local_from(RHO))
        self.assertEqual(
            context.reference.residual, local_from(scale(F(1, 2), add(eye(2), scale(F(-2, 3), Z))))
        )
        self.assertEqual(context.t, F(-2, 3))
        self.assertEqual(context.reference.orientation, "Z")
        self.assertEqual(context.coupler, "shared_CNOT_H2")
        self.assertEqual(context.frame, "fixed_shared_image")
        self.assertEqual(context.controller, "joint_return_controller")
        self.assertEqual(context.setting_id, "return-A")
        self.assertEqual(context.independence.origins, ("beam", "probe"))
        self.assertEqual(state.records, ())
        # Declared independent origins are retained premises, not a proof of independence.

    def test_positive_returns_preserve_all_input_labels_and_append_complete_fine_records(self):
        source = prepared()
        device = m.optimal_instrument(source.t, setting_id="return-A")
        for outcome in CELLS:
            probability, selected = m.commit(source, device, outcome)
            self.assertEqual(probability, fine_effect(RHO, source.t, outcome))
            self.assertEqual(selected.residual, image(aligned_rho(source.t, outcome), source.t))
            self.assertIs(selected.context, source.context)
            record = selected.records[0]
            self.assertEqual((record.event_id, record.outcome), (0, outcome))
            self.assertEqual(record.precursor, (("beam", 0), ("beam", 1), ("probe", 0)))
            self.assertEqual(record.local_records, source.context.local.records)
            self.assertEqual(record.reference_records, source.context.reference.records)
            self.assertEqual(record.local_records[0].settings, ("H", "P_inv"))
            self.assertEqual(record.local_records[1].precursor, (0,))
            self.assertEqual(record.reference_records[0].payload, (("sample", "R"),))
            self.assertEqual(record.origin, "joint-run")
            self.assertEqual(record.reference_t, source.t)
            self.assertEqual(record.reference_orientation, "Z")
            self.assertEqual(record.coupler, source.context.coupler)
            self.assertEqual(record.frame, source.context.frame)
            self.assertEqual(record.controller, source.context.controller)
            self.assertEqual(record.setting_id, source.context.setting_id)
            self.assertEqual(record.action, "same_image_joint_return")
        self.assertEqual(source.records, ())

    def test_stored_record_reread_is_not_next_fine_measurement_or_coarse_erasure(self):
        source = prepared(F(1), CENTER)
        device = m.optimal_instrument(1, setting_id="return-A")
        _, selected = m.commit(source, device, (0, 0))
        old_records = selected.records
        self.assertEqual(m.record_answer(old_records[0], "fine"), (0, 0))
        self.assertEqual(m.record_answer(old_records[0], "b"), 0)
        self.assertEqual(m.next_question_probability(selected, (0, 0), "fine"), F(1, 2))
        self.assertEqual(m.next_question_probability(selected, (0, 0), "b"), 1)
        self.assertEqual(m.next_question_probability(selected, (1, 0), "b"), 1)
        leaves = tuple(m.commit(selected, device, (a, 0)) for a in (0, 1))
        self.assertEqual(tuple(p for p, _ in leaves), (F(1, 2), F(1, 2)))
        self.assertNotEqual(leaves[0][1].records[-1], leaves[1][1].records[-1])
        for a, (_, leaf) in enumerate(leaves):
            self.assertEqual(tuple(record.outcome for record in leaf.records), ((0, 0), (a, 0)))
            self.assertEqual(m.record_answer(leaf.records[-1], "b"), 0)
            self.assertIs(leaf.records[0], old_records[0])
        self.assertIs(selected.records, old_records)

    def test_finite_return_tree_keeps_all_branch_histories_and_full_mass(self):
        source = prepared(F(1, 2), CENTER)
        device = m.optimal_instrument(source.t, setting_id="return-A")
        total_probability = F(0)
        histories = set()
        for first in CELLS:
            first_p, first_state = m.commit(source, device, first)
            second_total = F(0)
            for second in CELLS:
                second_p, leaf = m.commit(first_state, device, second)
                second_total += second_p
                total_probability += first_p * second_p
                histories.add(tuple(record.outcome for record in leaf.records))
                self.assertEqual(
                    leaf.records[-1].precursor,
                    (("beam", 0), ("beam", 1), ("probe", 0), ("joint-run", 0)),
                )
                self.assertEqual(first_state.records, leaf.records[:1])
                self.assertIs(leaf.context.reference, source.context.reference)
                self.assertEqual(leaf.residual, image(aligned_rho(source.t, second), source.t))
            self.assertEqual(second_total, 1)
        self.assertEqual(total_probability, 1)
        self.assertEqual(len(histories), 16)
        self.assertEqual(source.records, ())

    def test_zero_return_refuses_append_even_when_diagnostic_literal_cut_is_nonzero(self):
        source = prepared(F(1), RHO_BASIS[0])
        device = m.optimal_instrument(1, setting_id="return-A")
        outcome = (0, 1)
        cut = m.raw_cell_cut(source.residual, outcome)
        self.assertNotEqual(cut, zeros(16))
        self.assertTrue(m.is_psd(cut))
        self.assertEqual(raw_mass(cut), 0)
        self.assertEqual(device.branch(source.residual, outcome), zeros(16))
        prior_records = source.records
        with self.assertRaises(ValueError):
            m.commit(source, device, outcome)
        self.assertIs(source.records, prior_records)
        with self.assertRaises(ValueError):
            m.State(source.context, cut)

    def test_literal_terminal_cuts_cannot_be_reused_as_same_image_sources_or_targets(self):
        source = prepared()
        device = m.optimal_instrument(source.t, setting_id="return-A")
        raw = source.residual
        cut = m.raw_cell_cut(raw, (0, 0))
        indices = cell_indices((0, 0))
        expected = matrix(
            tuple(raw[i][j] if i in indices and j in indices else 0 for j in range(16))
            for i in range(16)
        )
        self.assertEqual(cut, expected)
        normalized = scale(1 / raw_mass(cut), cut)
        self.assertTrue(m.is_psd(normalized))
        self.assertEqual(raw_mass(normalized), 1)
        with self.assertRaises(ValueError):
            m.image_kernel(normalized, source.t, normalized=True)
        with self.assertRaises(ValueError):
            m.State(source.context, normalized)
        with self.assertRaises(ValueError):
            m.ReturnInstrument(source.t, (normalized,) * 4)
        for not_source in (normalized, source.context, source.context.local, object()):
            with self.assertRaises(TypeError):
                m.commit(not_source, device, (0, 0))

    def test_context_and_device_range_guards_do_not_borrow_a_missing_reference(self):
        source = prepared()
        context = source.context
        with self.assertRaises(TypeError):
            replace(context, reference=None)
        with self.assertRaises(TypeError):
            replace(context, independence=None)
        with self.assertRaises(ValueError):
            replace(context, independence=m.Independence(("beam", "someone-else")))
        with self.assertRaises(ValueError):
            replace(context, joint_origin="beam")
        for field, wrong in (("coupler", "identity"), ("frame", "local"), ("controller", "memory")):
            with self.assertRaises(ValueError):
                replace(context, **{field: wrong})
        with self.assertRaises(ValueError):
            replace(context.reference, orientation="X")
        for wrong_device in (
            m.optimal_instrument(-source.t, setting_id="return-A"),
            m.optimal_instrument(source.t, setting_id="return-B"),
        ):
            with self.assertRaises(ValueError):
                m.commit(source, wrong_device, (0, 0))
        with self.assertRaises(ValueError):
            m.State(
                replace(context, reference=replace(context.reference, t=-source.t)), source.residual
            )

    def test_local_c_is_rejected_not_silently_removed_including_at_zero_reference(self):
        local = local_from(CENTER, m.G(F(1, 10), F(1, 10)))
        self.assertTrue(m.is_psd(local))
        for t in (F(0), F(1, 2)):
            with self.assertRaises(ValueError):
                m.from_local(local, t)
            with self.assertRaises(ValueError):
                m.LocalInput(local)
        self.assertEqual(m.from_local(local_from(RHO), 0), image(RHO, 0))
        self.assertEqual(m.decompose_local(local)[1], m.G(F(1, 10), F(1, 10)))

    def test_one_shot_matrix_and_metadata_iterables_are_canonicalized_once(self):
        def rows(operator):
            return (iter(row) for row in operator)

        t = F(-1, 2)
        raw = image(RHO, t)
        device = m.optimal_instrument(t)
        self.assertEqual(m.image_span(rows(RHO), t), raw)
        self.assertEqual(m.inverse_span(rows(raw), t), RHO)
        self.assertEqual(m.image_kernel(rows(raw), t), raw)
        self.assertEqual(m.quotient_on_span(rows(raw), t), m.quotient_on_span(raw, t))
        self.assertEqual(m.effect_on_span(rows(raw), t, (0, 1)), fine_effect(RHO, t, (0, 1)))
        self.assertEqual(m.b_effect_on_span(rows(raw), t, 1), coarse_effect(RHO, t, 1))
        self.assertEqual(device.branch(rows(raw), (0, 1)), exact_optimal_branch(RHO, t, (0, 1)))
        signed = image(Y, t)
        self.assertEqual(device.branch_on_span(rows(signed), (0, 0)), zeros(16))
        rebuilt = m.ReturnInstrument(t, (rows(target) for target in device.targets))
        self.assertEqual(rebuilt.targets, device.targets)
        source = prepared(t)
        context = replace(source.context, permutation=iter(source.context.permutation))
        self.assertEqual(context.permutation, tuple(grouped(a, b, i, j) for a, i, b, j in BITS))
        local = replace(
            context.local,
            records=iter(context.local.records),
            residual=rows(context.local.residual),
        )
        self.assertEqual(local, context.local)
        initial = m.InputRecord(
            1,
            "calibrate",
            "pass",
            iter(("H", "P")),
            (iter(item) for item in (("phase", "full"),)),
            iter((0,)),
        )
        self.assertEqual(
            (initial.settings, initial.payload, initial.precursor),
            (("H", "P"), (("phase", "full"),), (0,)),
        )
        record = m.JointRecord(
            0, (1, 0), (iter(item) for item in (("beam", 0), ("beam", 1), ("probe", 0))), context
        )
        self.assertEqual(record.precursor, (("beam", 0), ("beam", 1), ("probe", 0)))
        state = m.State(context, rows(raw), iter((record,)))
        self.assertEqual(state.records, (record,))

    def test_record_ids_full_outcomes_and_precursors_are_strict_and_immutable(self):
        source = prepared()
        device = m.optimal_instrument(source.t, setting_id="return-A")
        _, selected = m.commit(source, device, (0, 0))
        record = selected.records[0]
        for bad_id in (False, 0.0, F(0), -1):
            with self.assertRaises(ValueError):
                replace(record, event_id=bad_id)
            with self.assertRaises(ValueError):
                m.InputRecord(bad_id, "a", "o")
        for outcome in ((False, 0), (0.0, 0), (F(0), 0), (0,), [0, 0], 0):
            with self.assertRaises(ValueError):
                replace(record, outcome=outcome)
        for precursor in (("beam", 0), (("beam", False),), record.precursor[:-1]):
            with self.assertRaises((TypeError, ValueError)):
                replace(record, precursor=precursor)
        for invalid_id in (False, 0.0, F(0)):
            permutation = (invalid_id,) + source.context.permutation[1:]
            with self.assertRaises(ValueError):
                replace(source.context, permutation=permutation)
        with self.assertRaises(FrozenInstanceError):
            record.outcome = (1, 1)
        with self.assertRaises(FrozenInstanceError):
            source.context.reference.t = F(0)
        with self.assertRaises(ValueError):
            m.State(
                source.context,
                source.residual,
                (replace(record, event_id=1, precursor=record.precursor + (("joint-run", 0),)),),
            )

    def test_nominal_labels_distinguish_settings_but_not_mathematical_provenance(self):
        source = prepared()
        device = m.optimal_instrument(source.t, setting_id="return-A")
        _, first = m.commit(source, device, (1, 0))
        _, same = m.commit(
            source, replace(device, provenance="independent algebraic witness"), (1, 0)
        )
        self.assertEqual(first, same)
        other_source = prepared(source.t, setting_id="return-B")
        _, other = m.commit(
            other_source, m.optimal_instrument(source.t, setting_id="return-B"), (1, 0)
        )
        self.assertEqual(first.residual, other.residual)
        self.assertNotEqual(first.records, other.records)
        with self.assertRaises(ValueError):
            m.State(other_source.context, first.residual, first.records)
        with self.assertRaises(ValueError):
            m.record_answer(first.records[0], "erase-a")
        with self.assertRaises(TypeError):
            m.record_answer((1, 0), "b")

    def test_malformed_matrix_reference_and_return_target_inputs_are_rejected(self):
        for t in (F(-3, 2), F(3, 2), False, 0.5):
            with self.assertRaises((TypeError, ValueError)):
                m.image_span(RHO, t)
        for rho in (matrix(((1, 1), (0, 0))), eye(3), matrix(((1, 2), (2, 1)))):
            with self.assertRaises(ValueError):
                m.image(rho, 0)
        for rho in (((True, 0), (0, 0)), ((1.0, 0), (0, 0))):
            with self.assertRaises(TypeError):
                m.image_span(rho, 0)
        raw = image(RHO, F(1, 2))
        with self.assertRaises(ValueError):
            m.ReturnInstrument(F(1, 2), (raw,) * 3)
        with self.assertRaises(ValueError):
            m.ReturnInstrument(F(1, 2), (scale(2, raw),) * 4)
        with self.assertRaises(ValueError):
            m.ReturnInstrument(F(-1, 2), (raw,) * 4)
        with self.assertRaises(ValueError):
            m.LocalInput(scale(2, local_from(RHO)))
        with self.assertRaises(ValueError):
            m.LocalInput(local_from(RHO), records=(m.InputRecord(1, "a", "o"),))


if __name__ == "__main__":
    unittest.main(verbosity=2)
