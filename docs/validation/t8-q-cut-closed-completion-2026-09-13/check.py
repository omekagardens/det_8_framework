"""Exact independent certificates for the fixed-t cut-closed completion.

The enlarged cone, not a physical enlargement or an available preparation law,
is tested. Full native kernels remain distinct from their four cut weights.
At polarized endpoints positive zero-mass cuts must not be silently deleted
from raw completeness, even though they cannot produce a selected record.
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


def zeros(n):
    return matrix((0,) * n for _ in range(n))


def eye(n):
    return matrix(tuple(int(i == j) for j in range(n)) for i in range(n))


def add(*operators):
    return matrix(
        tuple(total(operator[i][j] for operator in operators) for j in range(len(operators[0][0])))
        for i in range(len(operators[0]))
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


def trace(operator):
    return total(operator[i][i] for i in range(len(operator)))


def flatten(operator):
    return tuple(component for row in operator for entry in row for component in pair(entry))


def rank(rows):
    rows = [list(map(F, row)) for row in rows]
    pivot_row = 0
    if not rows:
        return 0
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
QP, QM = matrix(((1, 0), (0, 0))), matrix(((0, 0), (0, 1)))
CENTER = scale(F(1, 2), eye(2))
HERMITIAN_BASIS = (QP, QM, X, Y)
RHO = matrix(((F(3, 5), (F(1, 10), F(1, 5))), ((F(1, 10), F(-1, 5)), F(2, 5))))
BLOCKS = (RHO, scale(3, CENTER), QP, scale(F(1, 2), add(eye(2), Y)))
CELLS = tuple(product((0, 1), repeat=2))
BITS = tuple(product((0, 1), repeat=4))
PARAMETERS = (F(-1), F(-1, 2), F(0), F(1, 3), F(1))


def native(a, i, b, j):
    return 8 * a + 4 * i + 2 * b + j


def grouped(a, b, i, j):
    return 8 * a + 4 * b + 2 * i + j


def retwist(operator):
    output = [[ZERO for _ in range(16)] for _ in range(16)]
    for a, i, b, j in BITS:
        for c, k, d, ell in BITS:
            output[native(a, i, b, j)][native(c, k, d, ell)] = times(
                (-1) ** (a * i + b * j + c * k + d * ell),
                operator[grouped(a, b, i, j)][grouped(c, d, k, ell)],
            )
    return matrix(output)


def untwist(operator):
    output = [[ZERO for _ in range(16)] for _ in range(16)]
    for a, i, b, j in BITS:
        for c, k, d, ell in BITS:
            output[grouped(a, b, i, j)][grouped(c, d, k, ell)] = times(
                (-1) ** (a * i + b * j + c * k + d * ell),
                operator[native(a, i, b, j)][native(c, k, d, ell)],
            )
    return matrix(output)


def image(rhos, t):
    reference = scale(F(1, 4), add(eye(2), scale(t, Z)))
    blocks = tuple(
        scale(F(1, 2), mm(mm(U0, tensor(scale(F(1, 2), transpose(rho)), reference)), dagger(U0)))
        for rho in rhos
    )
    grouped_kernel = matrix(
        tuple(blocks[i // 4][i % 4][j % 4] if i // 4 == j // 4 else 0 for j in range(16))
        for i in range(16)
    )
    return retwist(grouped_kernel)


def independent_inverse(operator):
    grouped_kernel = untwist(operator)
    output = []
    for cell in range(4):
        block = matrix(grouped_kernel[4 * cell + i][4 * cell : 4 * cell + 4] for i in range(4))
        before = scale(F(1, 2), mm(mm(dagger(U0), block), U0))
        reduced = matrix(
            tuple(total(before[2 * i + j][2 * k + j] for j in range(2)) for k in range(2))
            for i in range(2)
        )
        output.append(scale(4, transpose(reduced)))
    return tuple(output)


def cell_indices(cell):
    a, b = cell
    return tuple(native(a, i, b, j) for i, j in product((0, 1), repeat=2))


def cell_form(operator, left, right):
    return total(operator[i][j] for i in cell_indices(left) for j in cell_indices(right))


def cut(operator, cell):
    indices = cell_indices(cell)
    return matrix(
        tuple(operator[i][j] if i in indices and j in indices else 0 for j in range(16))
        for i in range(16)
    )


def weights(operator):
    return tuple(cell_form(operator, cell, cell)[0] for cell in CELLS)


def mass(operator):
    return total(entry for row in operator for entry in row)[0]


def effect(t, cell):
    return scale(F(1, 4), add(eye(2), scale((-1) ** cell[1] * t, Z)))


def sparse_blocks(index, rho):
    return tuple(rho if i == index else zeros(2) for i in range(4))


def normalize_blocks(rhos, t):
    denominator = sum(
        trace(mm(effect(t, cell), rho))[0] for cell, rho in zip(CELLS, rhos, strict=True)
    )
    return tuple(scale(1 / denominator, rho) for rho in rhos)


def local_from(rho, c=0):
    a = scale(F(1, 2), transpose(rho))
    off_diagonal = scale(c, Z)
    adjoint = dagger(off_diagonal)
    b = mm(mm(Z, a), Z)
    return tuple(tuple(a[i]) + tuple(off_diagonal[i]) for i in range(2)) + tuple(
        tuple(adjoint[i]) + tuple(b[i]) for i in range(2)
    )


def prepared(t=F(1, 2), rho=RHO, setting_id="cut-A"):
    local_records = (
        m.InputRecord(0, "prepare", "beam-ready", ("H", "P_inv"), (("sample", "L"),)),
        m.InputRecord(1, "calibrate", "pass", ("Z",), (("phase", "full"),), (0,)),
    )
    reference_records = (m.InputRecord(0, "prepare", "probe-ready", ("Z",), (("sample", "R"),)),)
    local = m.LocalInput(local_from(rho), "beam", local_records)
    reference = m.ReferenceInput(t, "probe", reference_records)
    return m.prepare_state(
        m.L_DOMAIN,
        local,
        reference,
        m.Independence(("beam", "probe")),
        joint_origin="joint-run",
        setting_id=setting_id,
    )


class CutClosedCompletionChecks(unittest.TestCase):
    def test_four_independent_complex_blocks_match_the_full_native_construction(self):
        for t in PARAMETERS:
            raw = image(BLOCKS, t)
            self.assertEqual(m.image_span(BLOCKS, t), raw)
            self.assertEqual(m.inverse_span(raw, t), BLOCKS)
            self.assertEqual(independent_inverse(raw), BLOCKS)
            self.assertEqual(m.to_untwisted(raw), untwist(raw))
            self.assertEqual(m.from_untwisted(untwist(raw)), raw)
            self.assertNotEqual(BLOCKS[0], BLOCKS[1])
            self.assertTrue(any(entry.imag for row in raw for entry in row))

    def test_signed_span_has_sixteen_independent_native_directions_at_every_endpoint(self):
        for t in (F(-1), F(0), F(1, 3), F(1)):
            generators = []
            for cell in range(4):
                for rho in HERMITIAN_BASIS:
                    blocks = sparse_blocks(cell, rho)
                    raw = image(blocks, t)
                    self.assertEqual(m.inverse_span(raw, t), blocks)
                    generators.append(flatten(raw))
            self.assertEqual(rank(generators), 16)
        # An exact real-basis certificate, not a sampled PSD dimension estimate.

    def test_mass_and_raw_trace_are_different_exact_linear_functionals(self):
        for t in PARAMETERS:
            raw = image(BLOCKS, t)
            expected_weights = tuple(
                trace(mm(effect(t, cell), rho))[0] for cell, rho in zip(CELLS, BLOCKS, strict=True)
            )
            self.assertEqual(weights(raw), expected_weights)
            self.assertEqual(m.quotient_on_span(raw, t), expected_weights)
            self.assertEqual(m.raw_mass(raw), sum(expected_weights))
            self.assertEqual(trace(raw)[0], sum(trace(rho)[0] for rho in BLOCKS) / 4)
            self.assertEqual(m.raw_cell_weights(raw), expected_weights)
            for cell in CELLS:
                self.assertEqual(m.pulled_effect(t, cell), effect(t, cell))
            for left, right in combinations(CELLS, 2):
                self.assertEqual(cell_form(raw, left, right), ZERO)
            self.assertEqual(tuple(pair(value) for value in m.raw_crossforms(raw)), (ZERO,) * 6)
        raw = image(sparse_blocks(0, QP), 1)
        self.assertEqual(mass(raw), F(1, 2))
        self.assertEqual(trace(raw)[0], F(1, 4))

    def test_positive_image_and_normalization_use_native_mass_not_trace(self):
        for t in PARAMETERS:
            normalized = normalize_blocks(BLOCKS, t)
            raw = image(normalized, t)
            self.assertEqual(m.image(normalized, t, normalized=True), raw)
            self.assertEqual(m.inverse_image(raw, t, normalized=True), normalized)
            self.assertTrue(m.is_psd(raw))
            self.assertEqual(mass(raw), 1)
        raw = image(sparse_blocks(0, scale(2, QP)), 1)
        self.assertEqual(mass(raw), 1)
        self.assertEqual(trace(raw)[0], F(1, 2))
        self.assertEqual(m.image_kernel(raw, 1, normalized=True), raw)

    def test_old_same_block_image_embeds_but_does_not_exhaust_completion(self):
        for t in PARAMETERS:
            old = image((RHO,) * 4, t)
            self.assertEqual(m.k_image_span(RHO, t), old)
            self.assertEqual(m.k_image(RHO, t, normalized=True), old)
            self.assertEqual(m.inverse_span(old, t), (RHO,) * 4)
            self.assertEqual(mass(old), trace(RHO)[0])
            enlarged = image(sparse_blocks(0, RHO), t)
            self.assertNotEqual(enlarged, old)
            self.assertEqual(m.inverse_span(enlarged, t), sparse_blocks(0, RHO))

    def test_cuts_of_embedded_generators_span_the_entire_cut_closed_completion(self):
        t = F(1, 3)
        generators = []
        for cell_index, cell in enumerate(CELLS):
            for rho in HERMITIAN_BASIS:
                old = image((rho,) * 4, t)
                expected = image(sparse_blocks(cell_index, rho), t)
                self.assertEqual(cut(old, cell), expected)
                self.assertEqual(m.branch_on_span(old, t, cell), expected)
                generators.append(flatten(expected))
        self.assertEqual(rank(generators), 16)

    def test_raw_cuts_are_positive_complete_orthogonal_and_idempotent(self):
        for t in PARAMETERS:
            raw = image(BLOCKS, t)
            branches = tuple(m.branch(raw, t, cell) for cell in CELLS)
            self.assertEqual(add(*branches), raw)
            for cell, output in zip(CELLS, branches, strict=True):
                self.assertEqual(output, cut(raw, cell))
                self.assertTrue(m.is_psd(output))
                self.assertEqual(mass(output), weights(raw)[CELLS.index(cell)])
                self.assertEqual(m.image_span(m.inverse_span(output, t), t), output)
                for next_cell in CELLS:
                    expected = output if next_cell == cell else zeros(16)
                    self.assertEqual(cut(output, next_cell), expected)

    def test_positive_selected_cuts_have_perfect_full_outcome_repeatability(self):
        for t in PARAMETERS:
            raw = image(normalize_blocks(BLOCKS, t), t)
            for cell, probability in zip(CELLS, weights(raw), strict=True):
                if probability == 0:
                    continue
                selected = scale(1 / probability, cut(raw, cell))
                self.assertEqual(mass(selected), 1)
                self.assertEqual(weights(selected), tuple(F(int(other == cell)) for other in CELLS))
                self.assertEqual(cut(selected, cell), selected)
                self.assertEqual(m.image_kernel(selected, t, normalized=True), selected)

    def test_interior_positive_mass_is_faithful_with_explicit_spectral_lower_bound(self):
        for t in (F(-3, 4), F(0), F(2, 3)):
            minimum = (1 - abs(t)) / 4
            self.assertGreater(minimum, 0)
            for cell in CELLS:
                self.assertTrue(m.is_psd(add(effect(t, cell), scale(-minimum, eye(2)))))
            raw = image(BLOCKS, t)
            self.assertGreaterEqual(mass(raw), minimum * sum(trace(rho)[0] for rho in BLOCKS))
            self.assertEqual(mass(zeros(16)), 0)
        # Strictly positive E_ab makes a positive block with zero weight zero.

    def test_endpoint_positive_zero_mass_cone_has_four_independent_ray_generators(self):
        for t in (F(-1), F(1)):
            generators = []
            for index, cell in enumerate(CELLS):
                dark = QM if (-1) ** cell[1] * t > 0 else QP
                raw = image(sparse_blocks(index, dark), t)
                self.assertTrue(m.is_psd(raw))
                self.assertNotEqual(raw, zeros(16))
                self.assertEqual(mass(raw), 0)
                self.assertEqual(weights(raw), (F(0),) * 4)
                self.assertEqual(m.image_kernel(raw, t), raw)
                with self.assertRaises(ValueError):
                    m.image_kernel(raw, t, normalized=True)
                generators.append(flatten(raw))
            self.assertEqual(rank(generators), 4)
            dark_sum = add(
                *(
                    image(sparse_blocks(i, QM if (-1) ** cell[1] * t > 0 else QP), t)
                    for i, cell in enumerate(CELLS)
                )
            )
            self.assertEqual(mass(dark_sum), 0)
            self.assertEqual(trace(dark_sum)[0], 1)
            # Ordinary trace is a bounded ambient linear probe, but it is not
            # bounded by the native mass on this positive endpoint cone.
            trace_effects = (scale(F(1, 4), eye(2)),) * 4
            self.assertEqual(
                sum(
                    trace(mm(f, rho))[0]
                    for f, rho in zip(trace_effects, independent_inverse(dark_sum), strict=True)
                ),
                1,
            )
            with self.assertRaises(ValueError):
                m.dominated_effect_matrices(trace_effects, t)

    def test_weight_rank_four_common_kernel_twelve_and_mass_kernel_fifteen(self):
        for t in PARAMETERS:
            basis = tuple(
                image(sparse_blocks(i, rho), t) for i in range(4) for rho in HERMITIAN_BASIS
            )
            functionals = tuple(tuple(weights(raw)[i] for raw in basis) for i in range(4))
            self.assertEqual(rank(functionals), 4)
            self.assertEqual(rank((tuple(mass(raw) for raw in basis),)), 1)
            kernel = []
            for i, cell in enumerate(CELLS):
                e = effect(t, cell)
                diagonal = add(scale(e[1][1].real, QP), scale(-e[0][0].real, QM))
                for rho in (X, Y, diagonal):
                    raw = image(sparse_blocks(i, rho), t)
                    self.assertEqual(weights(raw), (F(0),) * 4)
                    kernel.append(raw)
            self.assertEqual(rank(tuple(flatten(raw) for raw in kernel)), 12)
            section = tuple(
                m.weight_section(tuple(F(int(i == j)) for i in range(4)), t) for j in range(4)
            )
            mass_kernel = kernel + [add(section[j], scale(-1, section[0])) for j in range(1, 4)]
            self.assertTrue(all(mass(raw) == 0 for raw in mass_kernel))
            self.assertEqual(rank(tuple(flatten(raw) for raw in mass_kernel)), 15)

    def test_weight_section_is_positive_surjective_not_an_inverse_for_raw_kernels(self):
        for t in PARAMETERS:
            for target in ((F(0),) * 4, (F(1, 7), F(2, 7), F(3, 7), F(1, 7))):
                raw = m.weight_section(target, t)
                self.assertTrue(m.is_psd(raw))
                self.assertEqual(weights(raw), target)
                self.assertEqual(m.quotient(raw, t), target)
                self.assertEqual(m.image_kernel(raw, t), raw)
            original = image(normalize_blocks(BLOCKS, t), t)
            representative = m.weight_section(weights(original), t)
            self.assertEqual(weights(representative), weights(original))
            self.assertNotEqual(representative, original)

    def test_equal_cut_weights_do_not_identify_interior_coherence_or_raw_payload(self):
        t = F(1, 2)
        plus_rho = add(CENTER, scale(F(1, 4), X))
        minus_rho = add(CENTER, scale(F(-1, 4), X))
        plus_raw = image(normalize_blocks(sparse_blocks(0, plus_rho), t), t)
        minus_raw = image(normalize_blocks(sparse_blocks(0, minus_rho), t), t)
        self.assertTrue(m.is_psd(plus_raw) and m.is_psd(minus_raw))
        self.assertEqual(weights(plus_raw), weights(minus_raw))
        self.assertNotEqual(plus_raw, minus_raw)
        self.assertNotEqual(cut(plus_raw, (0, 0)), cut(minus_raw, (0, 0)))

    def test_endpoint_weight_equivalence_also_hides_nonzero_coherence(self):
        t = F(1)
        first = matrix(((2, (0, F(1, 2))), ((0, F(-1, 2)), 1)))
        second = matrix(((2, 0), (0, 1)))
        first_raw, second_raw = (image(sparse_blocks(0, rho), t) for rho in (first, second))
        self.assertTrue(m.is_psd(first_raw) and m.is_psd(second_raw))
        self.assertEqual(weights(first_raw), (F(1), F(0), F(0), F(0)))
        self.assertEqual(weights(first_raw), weights(second_raw))
        self.assertNotEqual(first_raw, second_raw)
        self.assertEqual(trace(first_raw)[0], F(3, 4))
        for coefficient in (F(0), F(1, 3), F(1)):
            dominated = scale(coefficient, effect(t, (0, 0)))
            self.assertEqual(trace(mm(dominated, first)), trace(mm(dominated, second)))

    def test_endpoint_mass_dominated_effects_are_scalar_on_the_visible_ray(self):
        for t in (F(-1), F(1)):
            for cell in CELLS:
                e = effect(t, cell)
                visible = QP if (-1) ** cell[1] * t > 0 else QM
                dark = add(eye(2), scale(-1, visible))
                self.assertEqual(e, scale(F(1, 2), visible))
                for coefficient in (F(0), F(1, 3), F(1)):
                    f = scale(coefficient, e)
                    self.assertTrue(m.is_psd(f) and m.is_psd(add(e, scale(-1, f))))
                    self.assertEqual(mm(f, dark), zeros(2))
                    self.assertEqual(mm(visible, mm(f, visible)), f)
                # A nonzero coherence with a zero dark diagonal violates PSD.
                proposed = add(scale(F(1, 2), e), scale(F(1, 10), X))
                determinant = plus(
                    times(proposed[0][0], proposed[1][1]),
                    times(-1, times(proposed[0][1], proposed[1][0])),
                )
                self.assertEqual(determinant, (F(-1, 100), F(0)))
                self.assertFalse(m.is_psd(proposed))

    def test_interior_dominated_effect_can_detect_a_coherence_hidden_from_cut_weights(self):
        t = F(1, 2)
        e = effect(t, (0, 0))
        f = add(scale(F(1, 2), e), scale(F(1, 32), X))
        self.assertTrue(m.is_psd(f))
        self.assertTrue(m.is_psd(add(e, scale(-1, f))))
        first = add(CENTER, scale(F(1, 4), X))
        second = add(CENTER, scale(F(-1, 4), X))
        self.assertEqual(trace(mm(e, first)), trace(mm(e, second)))
        self.assertEqual(trace(mm(f, first))[0] - trace(mm(f, second))[0], F(1, 32))
        effects = sparse_blocks(0, f)
        self.assertEqual(m.dominated_effect_matrices(effects, t), effects)
        first_raw, second_raw = (image(sparse_blocks(0, rho), t) for rho in (first, second))
        self.assertEqual(
            m.dominated_effect(first_raw, t, effects) - m.dominated_effect(second_raw, t, effects),
            F(1, 32),
        )
        dual_generators = []
        for index, cell in enumerate(CELLS):
            middle = scale(F(1, 2), effect(t, cell))
            for perturbation in (zeros(2), X, Y, Z):
                f_cell = add(middle, scale(F(1, 32), perturbation))
                self.assertTrue(m.is_psd(f_cell))
                self.assertTrue(m.is_psd(add(effect(t, cell), scale(-1, f_cell))))
                family = sparse_blocks(index, f_cell)
                self.assertEqual(m.dominated_effect_matrices(family, t), family)
                dual_generators.append(
                    tuple(component for f_block in family for component in flatten(f_block))
                )
        self.assertEqual(rank(dual_generators), 16)
        # Algebraically allowed domination does not assert this effect is available.

    def test_dominated_effect_evaluation_is_exact_on_the_full_signed_span(self):
        for t in PARAMETERS:
            coefficients = (F(0), F(1, 3), F(2, 3), F(1))
            effects = tuple(
                scale(c, effect(t, cell)) for c, cell in zip(coefficients, CELLS, strict=True)
            )
            self.assertEqual(m.dominated_effect_matrices(effects, t), effects)
            for index in range(4):
                for rho in HERMITIAN_BASIS:
                    rhos = sparse_blocks(index, rho)
                    raw = image(rhos, t)
                    expected = trace(mm(effects[index], rho))[0]
                    self.assertEqual(m.dominated_effect_on_span(raw, t, effects), expected)
                    self.assertEqual(
                        expected,
                        sum(c * p for c, p in zip(coefficients, weights(raw), strict=True)),
                    )
            positive = image(BLOCKS, t)
            value = m.dominated_effect(positive, t, effects)
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, mass(positive))

    def test_cut_only_word_laws_depend_on_exactly_the_four_weights(self):
        for t in PARAMETERS:
            left = image(normalize_blocks((add(CENTER, scale(F(1, 4), X)),) * 4, t), t)
            right = image(normalize_blocks((add(CENTER, scale(F(-1, 4), X)),) * 4, t), t)
            self.assertNotEqual(left, right)
            self.assertEqual(weights(left), weights(right))
            for word in product(CELLS, repeat=3):
                left_output, right_output = left, right
                for cell in word:
                    left_output, right_output = cut(left_output, cell), cut(right_output, cell)
                expected = weights(left)[CELLS.index(word[0])] if len(set(word)) == 1 else F(0)
                self.assertEqual(mass(left_output), expected)
                self.assertEqual(mass(right_output), expected)
            for cell in CELLS:
                self.assertEqual(m.weight_cut(weights(left), cell), weights(cut(left, cell)))
                self.assertEqual(m.quotient(m.branch(left, t, cell), t), weights(cut(left, cell)))
        # A finite certificate of C_s C_r=delta_sr C_r, not a new history theorem.
        # The first full read recovers all four weights; it does not recover raw data.

    def test_opposite_ray_normalization_diverges_toward_both_polarized_endpoints(self):
        for sign in (-1, 1):
            for n in (2, 3, 5, 11):
                t = sign * (1 - F(1, n))
                small = (1 - abs(t)) / 4
                opposite = QM if sign > 0 else QP
                rhos = sparse_blocks(0, scale(1 / small, opposite))
                raw = image(rhos, t)
                self.assertEqual(mass(raw), 1)
                self.assertEqual(trace(raw)[0], n)
                self.assertEqual(trace(raw)[0], 1 / (1 - abs(t)))
                self.assertEqual(m.image(rhos, t, normalized=True), raw)
            endpoint_raw = image(sparse_blocks(0, opposite), sign)
            self.assertNotEqual(endpoint_raw, zeros(16))
            self.assertEqual(mass(endpoint_raw), 0)

    def test_raw_completeness_keeps_endpoint_terms_lost_by_zero_weight_normalized_ensembles(self):
        t = F(1)
        rhos = (scale(2, QP), QP, zeros(2), zeros(2))
        source = image(rhos, t)
        branches = tuple(cut(source, cell) for cell in CELLS)
        self.assertEqual(mass(source), 1)
        self.assertEqual(weights(source), (F(1), F(0), F(0), F(0)))
        self.assertEqual(add(*branches), source)
        self.assertNotEqual(branches[1], zeros(16))
        selected_ensemble = add(
            *(
                scale(probability, scale(1 / probability, branch))
                for probability, branch in zip(weights(source), branches, strict=True)
                if probability > 0
            )
        )
        self.assertNotEqual(selected_ensemble, source)
        self.assertEqual(add(selected_ensemble, branches[1]), source)
        self.assertEqual(weights(selected_ensemble), weights(source))
        self.assertEqual(trace(source)[0] - trace(selected_ensemble)[0], F(1, 4))

    def test_preparation_requires_the_changed_domain_and_retains_full_initial_context(self):
        source = prepared(F(-1, 2))
        context = source.context
        self.assertEqual(source.domain, "cut_closed_L_t")
        self.assertEqual(source.residual, image((RHO,) * 4, source.t))
        self.assertEqual(context.local.residual, local_from(RHO))
        self.assertEqual(context.t, F(-1, 2))
        self.assertEqual(context.reference.orientation, "Z")
        self.assertEqual(context.coupler, "shared_CNOT_H2")
        self.assertEqual(context.frame, "fixed_shared_image")
        self.assertEqual(context.controller, "joint_literal_cut_controller")
        self.assertEqual(context.setting_id, "cut-A")
        self.assertEqual(context.independence.origins, ("beam", "probe"))
        self.assertEqual(source.records, ())
        for wrong in ("K_t", "same_image_return", None):
            with self.assertRaises(ValueError):
                m.prepare_state(wrong, context.local, context.reference, context.independence)
        complex_local = local_from(CENTER, m.G(F(1, 10), F(1, 10)))
        self.assertTrue(m.is_psd(complex_local))
        with self.assertRaises(ValueError):
            m.LocalInput(complex_local)
        with self.assertRaises(ValueError):
            m.k_from_local(complex_local, 0)

    def test_selected_cut_retains_actual_raw_output_full_labels_and_tagged_precursors(self):
        base = prepared()
        source = m.State(m.L_DOMAIN, base.context, image(normalize_blocks(BLOCKS, base.t), base.t))
        for cell, probability in zip(CELLS, weights(source.residual), strict=True):
            actual_p, selected = m.commit(source, cell)
            self.assertEqual(actual_p, probability)
            self.assertEqual(selected.residual, scale(1 / probability, cut(source.residual, cell)))
            self.assertIs(selected.context, source.context)
            self.assertEqual(selected.domain, source.domain)
            record = selected.records[0]
            self.assertEqual(
                (record.domain, record.event_id, record.outcome), (m.L_DOMAIN, 0, cell)
            )
            self.assertEqual(record.precursor, (("beam", 0), ("beam", 1), ("probe", 0)))
            self.assertEqual(record.local_records, source.context.local.records)
            self.assertEqual(record.reference_records, source.context.reference.records)
            self.assertEqual(record.local_records[0].settings, ("H", "P_inv"))
            self.assertEqual(record.local_records[1].precursor, (0,))
            self.assertEqual(record.reference_records[0].payload, (("sample", "R"),))
            self.assertEqual(record.reference_t, source.t)
            self.assertEqual(record.reference_orientation, "Z")
            self.assertEqual(record.origin, "joint-run")
            self.assertEqual(record.action, "literal_joint_cell_cut")
            self.assertEqual(
                (record.coupler, record.frame, record.controller, record.setting_id),
                (source.context.coupler, source.context.frame, source.context.controller, "cut-A"),
            )
            with self.assertRaises(ValueError):
                m.inverse_k_span(selected.residual, source.t)
        self.assertEqual(source.records, ())

    def test_finite_adaptive_stopping_preserves_repeated_fine_records_and_probability(self):
        source = prepared(F(1, 3))
        source_records = source.records
        leaves = []
        for cell, expected in zip(CELLS, weights(source.residual), strict=True):
            probability, selected = m.commit(source, cell)
            first_residual = selected.residual
            stop_depth = 1 + 2 * cell[0] + cell[1]
            for depth in range(1, stop_depth):
                repeat_probability, selected = m.commit(selected, cell)
                probability *= repeat_probability
                self.assertEqual(repeat_probability, 1)
                self.assertEqual(selected.residual, first_residual)
                self.assertEqual(
                    selected.records[-1].precursor,
                    (("beam", 0), ("beam", 1), ("probe", 0))
                    + tuple(("joint-run", i) for i in range(depth)),
                )
            self.assertEqual(probability, expected)
            self.assertEqual(
                tuple(record.outcome for record in selected.records), (cell,) * stop_depth
            )
            self.assertEqual(m.next_question_probability(selected, cell, "fine"), 1)
            self.assertEqual(m.next_question_probability(selected, cell, "b"), 1)
            self.assertEqual(m.record_answer(selected.records[-1], "fine"), cell)
            self.assertEqual(m.record_answer(selected.records[-1], "b"), cell[1])
            leaves.append((f"stop-after-{stop_depth}", probability, selected))
        self.assertEqual(sum(probability for _, probability, _ in leaves), 1)
        self.assertEqual(len({label for label, _, _ in leaves}), 4)
        self.assertIs(source.records, source_records)
        # An immediate stop is the unchanged source with probability one;
        # these policy stop labels are bookkeeping, not fabricated cut records.
        immediate_stop = ("stop-now", F(1), source)
        self.assertIs(immediate_stop[2], source)
        self.assertEqual(immediate_stop[2].records, ())

    def test_equal_weight_sources_keep_equal_finite_record_laws_but_distinct_residuals(self):
        for t in PARAMETERS:
            base = prepared(t)
            left_rho = add(CENTER, scale(F(1, 4), Y))
            right_rho = add(CENTER, scale(F(-1, 4), Y))
            left = m.State(m.L_DOMAIN, base.context, image((left_rho,) * 4, t))
            right = m.State(m.L_DOMAIN, base.context, image((right_rho,) * 4, t))
            self.assertEqual(weights(left.residual), weights(right.residual))
            for cell in CELLS:
                p_left, selected_left = m.commit(left, cell)
                p_right, selected_right = m.commit(right, cell)
                self.assertEqual(p_left, p_right)
                self.assertEqual(selected_left.records, selected_right.records)
                self.assertNotEqual(selected_left.residual, selected_right.residual)
                repeat_left, final_left = m.commit(selected_left, cell)
                repeat_right, final_right = m.commit(selected_right, cell)
                self.assertEqual((repeat_left, repeat_right), (F(1), F(1)))
                self.assertEqual(final_left.records, final_right.records)
                self.assertNotEqual(final_left.residual, final_right.residual)

    def test_nonzero_zero_mass_endpoint_cut_is_inspectable_but_cannot_append(self):
        base = prepared(F(1))
        raw = image((scale(2, QP), QP, zeros(2), zeros(2)), 1)
        source = m.State(m.L_DOMAIN, base.context, raw)
        impossible = m.branch(raw, 1, (0, 1))
        self.assertNotEqual(impossible, zeros(16))
        self.assertEqual(impossible, cut(raw, (0, 1)))
        self.assertEqual(mass(impossible), 0)
        self.assertGreater(trace(impossible)[0], 0)
        prior = source.records
        with self.assertRaises(ValueError):
            m.commit(source, (0, 1))
        with self.assertRaises(ValueError):
            m.State(m.L_DOMAIN, source.context, impossible)
        self.assertIs(source.records, prior)
        probability, selected = m.commit(source, (0, 0))
        self.assertEqual(probability, 1)
        self.assertNotEqual(selected.residual, source.residual)
        self.assertEqual(add(selected.residual, impossible), source.residual)

    def test_endpoint_normalized_snapshots_and_selected_same_cell_keep_arbitrary_dark_payload(self):
        base = prepared(F(1))
        for amount in (F(0), F(3), F(100)):
            rhos = sparse_blocks(0, add(scale(2, QP), scale(amount, QM)))
            raw = image(rhos, 1)
            self.assertEqual(mass(raw), 1)
            self.assertEqual(trace(raw)[0], F(1, 2) + amount / 4)
            source = m.State(m.L_DOMAIN, base.context, raw)
            probability, selected = m.commit(source, (0, 0))
            self.assertEqual(probability, 1)
            self.assertEqual(selected.residual, raw)
            self.assertEqual(m.inverse_image(selected.residual, 1), rhos)
        # Valid snapshots are not a claim that a physical preparation reaches them.

    def test_old_domain_raw_objects_and_reset_actions_are_not_silent_adapters(self):
        source = prepared()
        for domain in ("K_t", "fixed_shared_image", "", None):
            with self.assertRaises(ValueError):
                m.State(domain, source.context, source.residual)
        for not_source in (source.residual, source.context, source.context.local, object()):
            with self.assertRaises(TypeError):
                m.commit(not_source, (0, 0))
        _, selected = m.commit(source, (0, 0))
        with self.assertRaises(ValueError):
            replace(selected.records[0], action="same_image_joint_return")
        with self.assertRaises(ValueError):
            replace(selected.records[0], domain="K_t")
        self.assertEqual(selected.records[0].domain, m.L_DOMAIN)
        # The raw cut is now in L_t; this does not rewrite the old K_t contract.

    def test_full_image_membership_rejects_wrong_reference_and_unreconstructed_raw_entries(self):
        raw = image(BLOCKS, F(1, 2))
        with self.assertRaises(ValueError):
            m.inverse_span(raw, F(-1, 2))
        grouped_raw = [list(row) for row in untwist(raw)]
        grouped_raw[0][4] = m.G(F(1, 100))
        grouped_raw[4][0] = m.G(F(1, 100))
        off_cell = retwist(matrix(grouped_raw))
        with self.assertRaises(ValueError):
            m.inverse_span(off_cell, F(1, 2))
        diagonal = [list(row) for row in untwist(raw)]
        diagonal[0][0] += F(1, 100)
        wrong_block = retwist(matrix(diagonal))
        self.assertTrue(m.is_psd(wrong_block))
        with self.assertRaises(ValueError):
            m.inverse_span(wrong_block, F(1, 2))
        self.assertEqual(m.inverse_span(zeros(16), -1), (zeros(2),) * 4)
        self.assertEqual(m.inverse_span(zeros(16), 1), (zeros(2),) * 4)

    def test_context_reference_frame_and_setting_history_cannot_be_silently_changed(self):
        source = prepared()
        with self.assertRaises(TypeError):
            replace(source.context, reference=None)
        with self.assertRaises(TypeError):
            replace(source.context, independence=None)
        with self.assertRaises(ValueError):
            replace(source.context, independence=m.Independence(("beam", "other")))
        with self.assertRaises(ValueError):
            replace(source.context.reference, orientation="X")
        for field, value in (
            ("coupler", "identity"),
            ("frame", "local"),
            ("controller", "joint_return_controller"),
            ("joint_origin", "beam"),
        ):
            with self.assertRaises(ValueError):
                replace(source.context, **{field: value})
        changed_t = replace(
            source.context, reference=replace(source.context.reference, t=-source.t)
        )
        with self.assertRaises(ValueError):
            m.State(m.L_DOMAIN, changed_t, source.residual)
        _, selected = m.commit(source, (0, 0))
        changed_setting = replace(source.context, setting_id="cut-B")
        with self.assertRaises(ValueError):
            m.State(m.L_DOMAIN, changed_setting, selected.residual, selected.records)
        other = prepared(setting_id="cut-B")
        _, other_selected = m.commit(other, (0, 0))
        self.assertEqual(other_selected.residual, selected.residual)
        self.assertNotEqual(other_selected.records, selected.records)

    def test_one_shot_matrices_effects_sections_and_metadata_are_consumed_once(self):
        def rows(operator):
            return (iter(row) for row in operator)

        t = F(-1, 2)
        raw = image(BLOCKS, t)
        self.assertEqual(m.image_span((rows(rho) for rho in BLOCKS), t), raw)
        self.assertEqual(m.inverse_span(rows(raw), t), BLOCKS)
        self.assertEqual(m.inverse_image(rows(raw), t), BLOCKS)
        self.assertEqual(m.image_kernel(rows(raw), t), raw)
        self.assertEqual(m.quotient(rows(raw), t), weights(raw))
        self.assertEqual(m.branch(rows(raw), t, (1, 0)), cut(raw, (1, 0)))
        self.assertEqual(m.fine_effect_on_span(rows(raw), t, (1, 0)), weights(raw)[2])
        self.assertEqual(m.b_effect_on_span(rows(raw), t, 0), weights(raw)[0] + weights(raw)[2])
        effects = tuple(scale(F(1, 2), effect(t, cell)) for cell in CELLS)
        self.assertEqual(
            m.dominated_effect(rows(raw), t, (rows(f) for f in effects)), mass(raw) / 2
        )
        self.assertEqual(m.dominated_effect_matrices((rows(f) for f in effects), t), effects)
        self.assertEqual(weights(m.weight_section(iter((F(1, 4),) * 4), t)), (F(1, 4),) * 4)
        source = prepared(t)
        context = replace(source.context, permutation=iter(source.context.permutation))
        self.assertEqual(context.permutation, tuple(grouped(a, b, i, j) for a, i, b, j in BITS))
        record = m.JointRecord(
            m.L_DOMAIN,
            0,
            (1, 0),
            (iter(item) for item in (("beam", 0), ("beam", 1), ("probe", 0))),
            context,
        )
        state = m.State(m.L_DOMAIN, context, rows(source.residual), iter((record,)))
        self.assertEqual(state.records, (record,))
        local_record = m.InputRecord(
            1,
            "calibrate",
            "pass",
            iter(("H", "P_inv")),
            (iter(item) for item in (("sample", "full"),)),
            iter((0,)),
        )
        self.assertEqual(
            (local_record.settings, local_record.payload, local_record.precursor),
            (("H", "P_inv"), (("sample", "full"),), (0,)),
        )
        self.assertEqual(
            replace(
                context.local,
                records=iter(context.local.records),
                residual=rows(context.local.residual),
            ),
            context.local,
        )

    def test_full_record_ids_precursors_and_payloads_are_strict_and_immutable(self):
        source = prepared()
        _, selected = m.commit(source, (0, 0))
        record = selected.records[0]
        for invalid in (False, 0.0, F(0), -1):
            with self.assertRaises(ValueError):
                replace(record, event_id=invalid)
            with self.assertRaises(ValueError):
                m.InputRecord(invalid, "a", "o")
        for outcome in ((False, 0), (0.0, 0), (F(0), 0), (0,), [0, 0], 0):
            with self.assertRaises(ValueError):
                replace(record, outcome=outcome)
        for precursor in (("beam", 0), (("beam", False),), record.precursor[:-1]):
            with self.assertRaises((TypeError, ValueError)):
                replace(record, precursor=precursor)
        for invalid in (False, 0.0, F(0)):
            with self.assertRaises(ValueError):
                replace(source.context, permutation=(invalid,) + source.context.permutation[1:])
        with self.assertRaises(FrozenInstanceError):
            record.outcome = (1, 1)
        with self.assertRaises(FrozenInstanceError):
            source.context.reference.t = F(0)
        with self.assertRaises(ValueError):
            m.record_answer(record, "erase-a")
        with self.assertRaises(TypeError):
            m.record_answer(record.outcome, "b")
        with self.assertRaises(ValueError):
            m.State(
                m.L_DOMAIN,
                source.context,
                source.residual,
                (replace(record, event_id=1, precursor=record.precursor + (("joint-run", 0),)),),
            )

    def test_signed_extensions_and_malformed_positive_inputs_effects_are_separated(self):
        signed_blocks = sparse_blocks(0, add(QP, scale(-2, QM)))
        signed = image(signed_blocks, F(1, 2))
        self.assertEqual(m.inverse_span(signed, F(1, 2)), signed_blocks)
        self.assertEqual(m.branch_on_span(signed, F(1, 2), (0, 0)), signed)
        with self.assertRaises(ValueError):
            m.image(signed_blocks, F(1, 2))
        with self.assertRaises(ValueError):
            m.inverse_image(signed, F(1, 2))
        for t in (False, 0.5, F(-3, 2), F(3, 2)):
            with self.assertRaises((TypeError, ValueError)):
                m.image_span(BLOCKS, t)
        for blocks in ((RHO,) * 3, (eye(3),) * 4, (matrix(((1, 1), (0, 0))),) * 4):
            with self.assertRaises(ValueError):
                m.image_span(blocks, 0)
        with self.assertRaises(TypeError):
            m.image_span((((True, 0), (0, 0)),) * 4, 0)
        with self.assertRaises(ValueError):
            m.dominated_effect_matrices((eye(2),) * 4, 0)
        with self.assertRaises(ValueError):
            m.dominated_effect_matrices((scale(-1, eye(2)),) * 4, 0)
        with self.assertRaises(ValueError):
            m.dominated_effect_matrices((eye(2),) * 3, 0)
        signed_weights = (F(2), F(-1), F(0), F(0))
        self.assertEqual(weights(m.weight_section_span(iter(signed_weights), 0)), signed_weights)
        with self.assertRaises(ValueError):
            m.weight_section(signed_weights, 0)
        with self.assertRaises(ValueError):
            m.weight_section((F(1),) * 4, 0, normalized=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
