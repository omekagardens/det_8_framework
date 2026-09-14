"""Exact certificates for the fixed-interior reversible-generator fixture.

Named rational group elements are commands, not additive clock readings.
Finite certificates check the formulas and counterexamples; continuity,
one-parameter classification, and physical availability are not inferred.
All native payloads and actual ordered command labels remain retained.
"""

import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F
from itertools import product

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


def eye(n):
    return matrix(tuple(int(i == j) for j in range(n)) for i in range(n))


def zeros(n):
    return matrix((0,) * n for _ in range(n))


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


def conjugate(operator):
    return matrix(tuple(conj(entry) for entry in row) for row in operator)


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


X = matrix(((0, 1), (1, 0)))
Y = matrix(((0, (0, -1)), ((0, 1), 0)))
Z = matrix(((1, 0), (0, -1)))
QP, QM = matrix(((1, 0), (0, 0))), matrix(((0, 0), (0, 1)))
H0 = matrix(((1, 1), (1, -1)))
CNOT = matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)))
U0 = mm(tensor(eye(2), H0), CNOT)
CENTER = scale(F(1, 2), eye(2))
RHO = matrix(((F(3, 5), (F(1, 10), F(1, 5))), ((F(1, 10), F(-1, 5)), F(2, 5))))
BLOCKS = (RHO, scale(3, CENTER), QP, scale(F(1, 2), add(eye(2), Y)))
HERMITIAN_BASIS = (QP, QM, X, Y)
CELLS = tuple(product((0, 1), repeat=2))
BITS = tuple(product((0, 1), repeat=4))
T = F(3, 5)
CIRCLE = {"A": (F(3, 5), F(4, 5)), "B": (F(5, 13), F(12, 13)), "AB": (F(-33, 65), F(56, 65))}
CIRCLE.update({name + "_inv": (c, -d) for name, (c, d) in tuple(CIRCLE.items())})


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


def image(rhos, t=T):
    reference = scale(F(1, 4), add(eye(2), scale(t, Z)))
    blocks = tuple(
        scale(F(1, 2), mm(mm(U0, tensor(scale(F(1, 2), transpose(rho)), reference)), dagger(U0)))
        for rho in rhos
    )
    return retwist(
        matrix(
            tuple(blocks[i // 4][i % 4][j % 4] if i // 4 == j // 4 else 0 for j in range(16))
            for i in range(16)
        )
    )


def cell_indices(cell):
    a, b = cell
    return tuple(native(a, i, b, j) for i, j in product((0, 1), repeat=2))


def cut(operator, cell):
    indices = cell_indices(cell)
    return matrix(
        tuple(operator[i][j] if i in indices and j in indices else 0 for j in range(16))
        for i in range(16)
    )


def weights(operator):
    return tuple(
        total(operator[i][j] for i in cell_indices(cell) for j in cell_indices(cell))[0]
        for cell in CELLS
    )


def mass(operator):
    return total(entry for row in operator for entry in row)[0]


def effect(cell, t=T):
    return scale(F(1, 4), add(eye(2), scale((-1) ** cell[1] * t, Z)))


def filt(cell):
    return matrix(((2, 0), (0, 1))) if cell[1] == 0 else matrix(((1, 0), (0, 2)))


def inv_filter(cell):
    return matrix(((F(1, 2), 0), (0, 1))) if cell[1] == 0 else matrix(((1, 0), (0, F(1, 2))))


def circle(c, d):
    return add(scale(c, eye(2)), scale((0, -d), X))


def weighted(unitary, cell):
    return mm(mm(inv_filter(cell), unitary), filt(cell))


def act(rhos, unitaries):
    return tuple(
        mm(mm(weighted(unitary, cell), rho), dagger(weighted(unitary, cell)))
        for cell, rho, unitary in zip(CELLS, rhos, unitaries, strict=True)
    )


def generator(hamiltonian, cell):
    return scale((0, -1), mm(mm(inv_filter(cell), hamiltonian), filt(cell)))


def derivative(rhos, hamiltonians):
    return tuple(
        add(mm(generator(h, cell), rho), mm(rho, dagger(generator(h, cell))))
        for cell, rho, h in zip(CELLS, rhos, hamiltonians, strict=True)
    )


def sparse_blocks(index, rho):
    return tuple(rho if i == index else zeros(2) for i in range(4))


def local_from(rho, c=0):
    a = scale(F(1, 2), transpose(rho))
    off_diagonal = scale(c, Z)
    adjoint = dagger(off_diagonal)
    b = mm(mm(Z, a), Z)
    return tuple(tuple(a[i]) + tuple(off_diagonal[i]) for i in range(2)) + tuple(
        tuple(adjoint[i]) + tuple(b[i]) for i in range(2)
    )


def prepared(rho=RHO, setting_id="cut-A"):
    local_records = (
        m.InputRecord(0, "prepare", "beam-ready", ("H", "P_inv"), (("sample", "L"),)),
        m.InputRecord(1, "calibrate", "pass", ("Z",), (("phase", "full"),), (0,)),
    )
    reference_records = (m.InputRecord(0, "prepare", "probe-ready", ("Z",), (("sample", "R"),)),)
    local = m.LocalInput(local_from(rho), "beam", local_records)
    reference = m.ReferenceInput(T, "probe", reference_records)
    return m.prepare_state(
        m.INTERIOR_DOMAIN,
        local,
        reference,
        m.Independence(("beam", "probe")),
        joint_origin="joint-run",
        setting_id=setting_id,
    )


class ReversibleGeneratorChecks(unittest.TestCase):
    def test_fixture_native_map_keeps_four_independent_complex_blocks(self):
        raw = image(BLOCKS)
        self.assertEqual(m.image_span(BLOCKS, T), raw)
        self.assertEqual(m.inverse_span(raw, T), BLOCKS)
        self.assertEqual(m.to_untwisted(raw), untwist(raw))
        self.assertEqual(m.from_untwisted(untwist(raw)), raw)
        self.assertEqual(
            weights(raw),
            tuple(trace(mm(effect(cell), rho))[0] for cell, rho in zip(CELLS, BLOCKS, strict=True)),
        )
        self.assertEqual(mass(raw), sum(weights(raw)))
        self.assertEqual(trace(raw)[0], sum(trace(rho)[0] for rho in BLOCKS) / 4)

    def test_rational_filters_factor_the_actual_cell_effects(self):
        self.assertEqual(m.FIXED_T, T)
        for cell in CELLS:
            d, inverse = filt(cell), inv_filter(cell)
            self.assertEqual(m.block_filter(cell, T), d)
            self.assertEqual(m.inverse_filter(cell, T), inverse)
            self.assertEqual(mm(d, inverse), eye(2))
            self.assertEqual(scale(F(1, 10), mm(d, d)), effect(cell))
            self.assertEqual(m.pulled_effect(T, cell), effect(cell))

    def test_named_rational_group_elements_have_exact_products_and_inverses(self):
        self.assertEqual(set(m.COMMANDS), set(CIRCLE))
        for name, (c, d) in CIRCLE.items():
            self.assertEqual(c * c + d * d, 1)
            unitary = circle(c, d)
            self.assertEqual(m.command_unitary(name), unitary)
            self.assertEqual(mm(dagger(unitary), unitary), eye(2))
        a, b, ab = (circle(*CIRCLE[name]) for name in ("A", "B", "AB"))
        self.assertEqual(mm(b, a), ab)
        self.assertEqual(mm(a, b), ab)
        for name in ("A", "B", "AB"):
            self.assertEqual(mm(m.command_unitary(name + "_inv"), m.command_unitary(name)), eye(2))
        # These are element identities. The names carry no additive time coordinate.

    def test_weighted_congruences_preserve_effects_without_being_ordinary_unitaries(self):
        for name, parameters in CIRCLE.items():
            unitary = circle(*parameters)
            for cell in CELLS:
                transform = weighted(unitary, cell)
                self.assertEqual(m.weighted_unitary(unitary, cell, T), transform)
                self.assertEqual(mm(mm(dagger(transform), effect(cell)), transform), effect(cell))
                self.assertNotEqual(mm(dagger(transform), transform), eye(2))
                inverse = weighted(dagger(unitary), cell)
                self.assertEqual(mm(inverse, transform), eye(2))
            self.assertNotEqual(name, "elapsed_time")

    def test_full_raw_action_matches_independent_filtered_complex_congruence(self):
        raw = image(BLOCKS)
        unitaries = (circle(*CIRCLE["A"]), circle(*CIRCLE["B"]), Y, Z)
        expected = image(act(BLOCKS, unitaries))
        self.assertEqual(m.weighted_action_on_span(raw, T, unitaries), expected)
        self.assertEqual(m.weighted_action(raw, T, unitaries), expected)
        self.assertTrue(m.is_psd(expected))
        self.assertEqual(weights(expected), weights(raw))
        self.assertNotEqual(expected, raw)

    def test_command_inverse_and_products_hold_on_the_entire_signed_span(self):
        for index in range(4):
            for rho in HERMITIAN_BASIS:
                raw = image(sparse_blocks(index, rho))
                first = m.command_on_span(raw, T, "A")
                self.assertEqual(
                    first, image(act(sparse_blocks(index, rho), (circle(*CIRCLE["A"]),) * 4))
                )
                self.assertEqual(m.command_on_span(first, T, "A_inv"), raw)
                self.assertEqual(m.command_on_span(first, T, "B"), m.command_on_span(raw, T, "AB"))

    def test_all_weights_and_mass_are_invariant_while_raw_trace_can_change(self):
        raw = image(BLOCKS)
        changed_trace = False
        for name, parameters in CIRCLE.items():
            expected = image(act(BLOCKS, (circle(*parameters),) * 4))
            actual = m.command(raw, T, name)
            self.assertEqual(actual, expected)
            self.assertEqual(weights(actual), weights(raw))
            self.assertEqual(mass(actual), mass(raw))
            self.assertEqual(sum(weights(actual)), mass(raw))
            changed_trace |= trace(actual) != trace(raw)
        self.assertTrue(changed_trace)

    def test_reversible_actions_commute_with_each_literal_cut(self):
        raw = image(BLOCKS)
        for name in ("A", "B", "AB_inv"):
            changed = m.command(raw, T, name)
            for cell in CELLS:
                self.assertEqual(m.command(cut(raw, cell), T, name), cut(changed, cell))
            self.assertEqual(add(*(cut(changed, cell) for cell in CELLS)), changed)

    def test_scalar_unitary_phase_is_an_exact_action_gauge(self):
        raw = image(BLOCKS)
        for phase in (m.G(0, 1), -1, m.G(F(3, 5), F(4, 5))):
            unitary = scale(phase, eye(2))
            self.assertEqual(mm(dagger(unitary), unitary), eye(2))
            self.assertEqual(m.weighted_action(raw, T, (unitary,) * 4), raw)
        self.assertNotEqual(scale((0, 1), eye(2)), eye(2))

    def test_filtered_generators_obey_the_weighted_skew_identity(self):
        for cell in CELLS:
            for h in (eye(2), X, Y, Z, add(X, scale(F(2, 3), Y), Z)):
                g = generator(h, cell)
                self.assertEqual(m.weighted_generator(h, cell, T), g)
                self.assertEqual(add(mm(dagger(g), effect(cell)), mm(effect(cell), g)), zeros(2))
                self.assertEqual(m.weighted_skew_residual(g, cell, T), zeros(2))

    def test_generator_action_matches_full_signed_span_and_block_preservation(self):
        hamiltonians = (X, Y, Z, add(X, Y, Z))
        for index in range(4):
            for rho in HERMITIAN_BASIS:
                rhos = sparse_blocks(index, rho)
                expected_rhos = derivative(rhos, hamiltonians)
                expected = image(expected_rhos)
                self.assertEqual(m.generator_action_on_span(image(rhos), T, hamiltonians), expected)
                self.assertTrue(m.is_hermitian(expected))
                self.assertEqual(cut(expected, CELLS[index]), expected)

    def test_action_generators_have_twelve_directions_and_four_scalar_gauges(self):
        rhos_basis = tuple(
            sparse_blocks(index, rho) for index in range(4) for rho in HERMITIAN_BASIS
        )
        action_columns = []
        for index in range(4):
            for h in (X, Y, Z):
                hs = sparse_blocks(index, h)
                action_columns.append(
                    tuple(
                        component
                        for rhos in rhos_basis
                        for output in derivative(rhos, hs)
                        for component in flatten(output)
                    )
                )
            scalar = sparse_blocks(index, eye(2))
            for rhos in rhos_basis:
                self.assertEqual(derivative(rhos, scalar), (zeros(2),) * 4)
            self.assertEqual(m.generator_action_on_span(image(BLOCKS), T, scalar), zeros(16))
        self.assertEqual(rank(action_columns), 12)
        # A rank certificate on the actual direct-sum Hermitian span. No
        # finite list proves continuity or an unrestricted group classification.

    def test_generator_tangent_preserves_each_weight_not_the_raw_trace(self):
        hamiltonians = (Y, X, Z, Y)
        tangent = image(derivative(BLOCKS, hamiltonians))
        self.assertEqual(m.generator_action_on_span(image(BLOCKS), T, hamiltonians), tangent)
        self.assertEqual(weights(tangent), (F(0),) * 4)
        self.assertEqual(mass(tangent), 0)
        self.assertNotEqual(trace(tangent)[0], 0)

    def test_raw_tangent_uses_conjugated_generator_and_transposed_complex_input(self):
        raw = image(BLOCKS)
        grouped_raw = untwist(raw)
        hamiltonians = (X, Y, X, Y)
        derivatives = []
        for index, (cell, h) in enumerate(zip(CELLS, hamiltonians, strict=True)):
            common = matrix(grouped_raw[4 * index + i][4 * index : 4 * index + 4] for i in range(4))
            g = generator(h, cell)
            lifted = scale(F(1, 2), mm(mm(U0, tensor(conjugate(g), eye(2))), dagger(U0)))
            derivatives.append(add(mm(lifted, common), mm(common, dagger(lifted))))
        direct = retwist(
            matrix(
                tuple(
                    derivatives[i // 4][i % 4][j % 4] if i // 4 == j // 4 else 0 for j in range(16)
                )
                for i in range(16)
            )
        )
        self.assertEqual(direct, image(derivative(BLOCKS, hamiltonians)))
        self.assertEqual(m.generator_action_on_span(raw, T, hamiltonians), direct)
        self.assertEqual(transpose(Y), scale(-1, Y))
        self.assertNotEqual(image((transpose(RHO),) + BLOCKS[1:]), raw)

    def test_commutator_of_generator_actions_has_the_expected_lie_sign(self):
        for cell in CELLS:
            gx, gy, gz = (generator(h, cell) for h in (X, Y, Z))
            self.assertEqual(add(mm(gx, gy), scale(-1, mm(gy, gx))), scale(2, gz))
        hx, hy, hz = (tuple(h for _ in CELLS) for h in (X, Y, Z))
        commutator = tuple(
            add(left, scale(-1, right))
            for left, right in zip(
                derivative(derivative(BLOCKS, hy), hx),
                derivative(derivative(BLOCKS, hx), hy),
                strict=True,
            )
        )
        self.assertEqual(commutator, tuple(scale(2, output) for output in derivative(BLOCKS, hz)))

    def test_endpoint_dark_scaling_is_mass_preserving_positive_and_noncompact(self):
        for t in (F(-1), F(1)):
            for index, cell in enumerate(CELLS):
                bright = QP if (-1) ** cell[1] * t > 0 else QM
                dark = add(eye(2), scale(-1, bright))
                source_rho = add(scale(2, bright), dark)
                for ratio in (F(2), F(1, 2), F(4)):
                    transform = add(bright, scale(ratio, dark))
                    inverse = add(bright, scale(1 / ratio, dark))
                    self.assertEqual(m.endpoint_scale_operator(cell, t, ratio), transform)
                    output_rho = mm(mm(transform, source_rho), dagger(transform))
                    self.assertEqual(mm(inverse, transform), eye(2))
                    self.assertEqual(
                        mm(mm(dagger(transform), effect(cell, t)), transform), effect(cell, t)
                    )
                    output = image(sparse_blocks(index, output_rho), t)
                    source = image(sparse_blocks(index, source_rho), t)
                    self.assertEqual(m.endpoint_scale(source, t, ratio), output)
                    self.assertEqual(m.endpoint_scale(output, t, 1 / ratio), source)
                    self.assertTrue(m.is_psd(output))
                    self.assertEqual(mass(output), 1)
                    self.assertEqual(trace(output)[0], F(1, 2) + ratio * ratio / 4)
            with self.assertRaises(ValueError):
                m.block_filter((0, 0), t)
        # Finite exact members illustrate the separately proved endpoint family;
        # they do not make the interior filter invertible at an endpoint.

    def test_static_transpose_is_positive_but_flips_one_pauli_orientation(self):
        transposed = tuple(transpose(rho) for rho in BLOCKS)
        output = image(transposed)
        self.assertEqual(m.transpose_blocks(image(BLOCKS), T), output)
        self.assertTrue(m.is_psd(output))
        self.assertEqual(weights(output), weights(image(BLOCKS)))
        self.assertNotEqual(output, image(BLOCKS))
        self.assertEqual(tuple(transpose(rho) for rho in transposed), BLOCKS)
        self.assertEqual(transpose(X), X)
        self.assertEqual(transpose(Y), scale(-1, Y))
        self.assertEqual(transpose(Z), Z)
        self.assertEqual(1 * -1 * 1, -1)
        # This static orientation reversal is not a witness for a continuous
        # one-parameter group connected to the identity.

    def test_dephasing_is_forward_positive_but_its_linear_inverse_need_not_be_positive(self):
        rho = scale(F(1, 2), add(eye(2), X))
        for parameter in (F(0), F(1, 3), F(3, 5), F(1)):
            output = add(
                scale((1 + parameter) / 2, rho), scale((1 - parameter) / 2, mm(mm(Z, rho), Z))
            )
            expected = matrix(((F(1, 2), parameter / 2), (parameter / 2, F(1, 2))))
            self.assertEqual(output, expected)
            self.assertEqual(
                m.filtered_dephasing(image((rho,) * 4), T, parameter), image((expected,) * 4)
            )
            self.assertTrue(m.is_psd(output))
            for cell in CELLS:
                self.assertEqual(trace(mm(effect(cell), output)), trace(mm(effect(cell), rho)))
        for parameter in (F(1, 3), F(3, 5)):
            inverse_candidate = matrix(
                ((F(1, 2), 1 / (2 * parameter)), (1 / (2 * parameter), F(1, 2)))
            )
            eigenvalue = (1 - 1 / parameter) / 2
            self.assertLess(eigenvalue, 0)
            raw_inverse = m.inverse_dephasing_diagnostic(image((rho,) * 4), T, parameter)
            self.assertEqual(raw_inverse, image((inverse_candidate,) * 4))
            self.assertEqual(
                m.filtered_dephasing_on_span(raw_inverse, T, parameter), image((rho,) * 4)
            )
            self.assertFalse(m.is_psd(inverse_candidate))
            self.assertEqual(
                mm(inverse_candidate, matrix(((1,), (-1,)))),
                scale(eigenvalue, matrix(((1,), (-1,)))),
            )

    def test_preparation_retains_the_fixed_interior_domain_and_known_context(self):
        state = prepared()
        self.assertEqual(state.domain, "interior_filtered_L_t")
        self.assertEqual(state.t, T)
        self.assertEqual(state.residual, image((RHO,) * 4))
        self.assertEqual(state.context.local.residual, local_from(RHO))
        self.assertEqual(state.context.reference.orientation, "Z")
        self.assertEqual(state.context.coupler, "shared_CNOT_H2")
        self.assertEqual(state.context.frame, "fixed_shared_image")
        self.assertEqual(state.context.controller, "weighted_command_cut_controller")
        self.assertEqual(state.context.setting_id, "cut-A")
        self.assertEqual(state.context.independence.origins, ("beam", "probe"))
        self.assertEqual((state.records, state.pending), ((), ()))
        nonzero_c = local_from(CENTER, m.G(F(1, 10), F(1, 10)))
        self.assertTrue(m.is_psd(nonzero_c))
        with self.assertRaises(ValueError):
            m.LocalInput(nonzero_c)

    def test_silent_commands_act_on_raw_state_and_preserve_the_record_tuple(self):
        source = prepared()
        old_records = source.records
        after_a = m.run_command(source, "A")
        expected_a = image(act((RHO,) * 4, (circle(*CIRCLE["A"]),) * 4))
        self.assertEqual(after_a.residual, expected_a)
        self.assertNotEqual(after_a.residual, source.residual)
        self.assertIs(after_a.records, old_records)
        self.assertEqual(after_a.pending, ("A",))
        after_b = m.run_command(after_a, "B")
        self.assertEqual(after_b.residual, image(act((RHO,) * 4, (circle(*CIRCLE["AB"]),) * 4)))
        self.assertEqual(after_b.pending, ("A", "B"))
        self.assertIs(after_b.records, old_records)
        self.assertIs(after_b.context, source.context)
        self.assertEqual(source.pending, ())
        self.assertEqual(weights(after_b.residual), weights(source.residual))

    def test_commit_uses_already_applied_word_then_clears_it_without_reapplying(self):
        source = prepared()
        changed = m.run_word(source, ("A", "B"))
        expected_p = weights(source.residual)[0]
        probability, selected = m.commit(changed, (0, 0))
        self.assertEqual(probability, expected_p)
        self.assertEqual(selected.residual, scale(1 / expected_p, cut(changed.residual, (0, 0))))
        self.assertEqual(selected.records[-1].command_word, ("A", "B"))
        self.assertEqual(selected.pending, ())
        self.assertNotEqual(m.command(selected.residual, T, "AB"), selected.residual)
        again_p, again = m.commit(selected, (0, 0))
        self.assertEqual(again_p, 1)
        self.assertEqual(again.residual, selected.residual)
        self.assertEqual(again.records[-1].command_word, ())
        self.assertIs(again.records[0], selected.records[0])
        self.assertEqual(changed.pending, ("A", "B"))

    def test_equal_group_elements_never_identify_distinct_nominal_command_records(self):
        source = prepared()
        product_word = m.run_word(source, ("A", "B"))
        single_name = m.run_word(source, ("AB",))
        self.assertEqual(product_word.residual, single_name.residual)
        self.assertNotEqual(product_word.pending, single_name.pending)
        left_p, left = m.commit(product_word, (1, 1))
        right_p, right = m.commit(single_name, (1, 1))
        self.assertEqual(left_p, right_p)
        self.assertEqual(left.residual, right.residual)
        self.assertNotEqual(left.records, right.records)
        identity_word = m.run_word(source, ("A", "A_inv"))
        self.assertEqual(identity_word.residual, source.residual)
        self.assertEqual(identity_word.pending, ("A", "A_inv"))
        _, with_word = m.commit(identity_word, (0, 1))
        _, without_word = m.commit(source, (0, 1))
        self.assertEqual(with_word.residual, without_word.residual)
        self.assertNotEqual(with_word.records, without_word.records)
        # One common known-history policy can stop on the single-name word
        # and otherwise request a cut. Equal raw states/weights alone do not
        # equate these laws when the initial pending words already differ.
        policy_leaves = []
        for initial in (product_word, single_name):
            if initial.pending == ("AB",):
                leaves = ((F(1), initial),)
            else:
                leaves = tuple(m.commit(initial, cell) for cell in CELLS)
            self.assertEqual(sum(probability for probability, _ in leaves), 1)
            policy_leaves.append(tuple(len(leaf.records) for _, leaf in leaves))
        self.assertEqual(policy_leaves, [(1, 1, 1, 1), (0,)])

    def test_same_finite_nominal_policy_has_equal_outcome_laws_without_erasing_commands(self):
        base = prepared()
        rho_left, rho_right = (add(CENTER, scale(sign * F(1, 4), Y)) for sign in (1, -1))
        sources = tuple(
            m.State(m.INTERIOR_DOMAIN, base.context, image((rho,) * 4))
            for rho in (rho_left, rho_right)
        )
        prior_totals = [F(0), F(0)]
        for cell in CELLS:
            outputs = []
            for index, source in enumerate(sources):
                first = m.run_command(source, "A")
                probability, selected = m.commit(first, cell)
                policy_word = ("B",) if cell[0] == 0 else ("A_inv", "AB")
                continued = m.run_word(selected, policy_word)
                second_p, leaf = m.commit(continued, cell)
                self.assertEqual(second_p, 1)
                self.assertEqual(
                    tuple(record.command_word for record in leaf.records), (("A",), policy_word)
                )
                self.assertEqual(tuple(record.outcome for record in leaf.records), (cell, cell))
                self.assertEqual(
                    leaf.records[-1].precursor,
                    (("beam", 0), ("beam", 1), ("probe", 0), ("joint-run", 0)),
                )
                prior_totals[index] += probability * second_p
                outputs.append((probability, leaf))
            self.assertEqual(outputs[0][0], outputs[1][0])
            self.assertEqual(outputs[0][1].records, outputs[1][1].records)
            self.assertNotEqual(outputs[0][1].residual, outputs[1][1].residual)
        self.assertEqual(prior_totals, [F(1), F(1)])
        # Equality is conditional on this same nominal history policy, not a
        # claim that different known command words denote the same records.

    def test_committed_history_preserves_both_input_origins_payloads_and_actual_settings(self):
        source = prepared()
        changed = m.run_word(source, ("B_inv", "A"))
        _, selected = m.commit(changed, (1, 0))
        record = selected.records[0]
        self.assertEqual(
            (record.event_id, record.outcome, record.domain), (0, (1, 0), m.INTERIOR_DOMAIN)
        )
        self.assertEqual(record.precursor, (("beam", 0), ("beam", 1), ("probe", 0)))
        self.assertEqual(record.local_records, source.context.local.records)
        self.assertEqual(record.reference_records, source.context.reference.records)
        self.assertEqual(record.local_records[0].settings, ("H", "P_inv"))
        self.assertEqual(record.local_records[1].precursor, (0,))
        self.assertEqual(record.reference_records[0].payload, (("sample", "R"),))
        self.assertEqual(record.command_word, ("B_inv", "A"))
        self.assertEqual(record.reference_t, T)
        self.assertEqual(record.reference_orientation, "Z")
        self.assertEqual(record.origin, "joint-run")
        self.assertEqual(
            (record.coupler, record.frame, record.controller, record.setting_id),
            (source.context.coupler, source.context.frame, source.context.controller, "cut-A"),
        )
        old_records = selected.records
        controlled = m.run_command(selected, "AB_inv")
        self.assertIs(controlled.records, old_records)
        self.assertEqual(m.record_answer(record, "fine"), (1, 0))
        self.assertEqual(m.record_answer(record, "b"), 0)
        self.assertEqual(m.next_question_probability(controlled, (1, 0), "fine"), 1)
        self.assertEqual(m.next_question_probability(controlled, (0, 0), "fine"), 0)
        self.assertIs(controlled.records, old_records)

    def test_zero_branches_refuse_normalization_without_losing_pending_words(self):
        _, selected = m.commit(prepared(), (0, 0))
        changed = m.run_word(selected, ("B", "A_inv"))
        impossible = (1, 1)
        self.assertEqual(m.branch(changed.residual, T, impossible), zeros(16))
        self.assertEqual(m.next_question_probability(changed, impossible), 0)
        prior_records, prior_pending = changed.records, changed.pending
        with self.assertRaises(ValueError):
            m.commit(changed, impossible)
        self.assertIs(changed.records, prior_records)
        self.assertIs(changed.pending, prior_pending)
        self.assertEqual(prior_pending, ("B", "A_inv"))
        with self.assertRaises(ValueError):
            m.State(m.INTERIOR_DOMAIN, changed.context, zeros(16))

    def test_primary_domain_and_context_reject_endpoints_and_unrecorded_frame_changes(self):
        source = prepared()
        for wrong in ("cut_closed_L_t", "K_t", "", None):
            with self.assertRaises(ValueError):
                m.State(wrong, source.context, source.residual)
        for t in (F(-1), F(1), F(0), F(-3, 5)):
            with self.assertRaises(ValueError):
                replace(source.context, reference=replace(source.context.reference, t=t))
            with self.assertRaises(ValueError):
                m.command_on_span(image((RHO,) * 4, t), t, "A")
        with self.assertRaises(TypeError):
            replace(source.context, reference=None)
        with self.assertRaises(TypeError):
            replace(source.context, independence=None)
        with self.assertRaises(ValueError):
            replace(source.context.reference, orientation="X")
        with self.assertRaises(ValueError):
            replace(source.context, independence=m.Independence(("beam", "other")))
        for field, value in (
            ("coupler", "identity"),
            ("frame", "local"),
            ("controller", "joint_literal_cut_controller"),
            ("joint_origin", "beam"),
        ):
            with self.assertRaises(ValueError):
                replace(source.context, **{field: value})
        _, selected = m.commit(source, (0, 0))
        with self.assertRaises(ValueError):
            m.State(
                m.INTERIOR_DOMAIN,
                replace(source.context, setting_id="cut-B"),
                selected.residual,
                selected.records,
            )

    def test_diagnostics_and_numerical_time_values_are_not_available_primary_commands(self):
        source = prepared()
        for name in (
            "transpose",
            "dephasing",
            "endpoint_scale",
            "Hamiltonian",
            "H",
            "A+B",
            "A(0.6)",
            1,
            F(3, 5),
            None,
        ):
            with self.assertRaises(ValueError):
                m.run_command(source, name)
        with self.assertRaises(TypeError):
            m.run_word(source, "AB")
        for not_source in (source.residual, source.context, source.context.local, object()):
            with self.assertRaises(TypeError):
                m.run_command(not_source, "A")
            with self.assertRaises(TypeError):
                m.commit(not_source, (0, 0))
        with self.assertRaises(ValueError):
            replace(source, pending=("transpose",))
        self.assertIs(m.run_word(source, ()), source)
        self.assertEqual((source.records, source.pending), ((), ()))

    def test_one_shot_inputs_and_command_words_are_materialized_exactly_once(self):
        def rows(operator):
            return (iter(row) for row in operator)

        raw = image(BLOCKS)
        unitaries = (circle(*CIRCLE["A"]), Y, Z, eye(2))
        hamiltonians = (X, Y, Z, eye(2))
        self.assertEqual(
            m.weighted_action(rows(raw), T, (rows(unitary) for unitary in unitaries)),
            image(act(BLOCKS, unitaries)),
        )
        self.assertEqual(
            m.generator_action_on_span(rows(raw), T, (rows(h) for h in hamiltonians)),
            image(derivative(BLOCKS, hamiltonians)),
        )
        self.assertEqual(m.weighted_generator(rows(Y), (0, 1), T), generator(Y, (0, 1)))
        self.assertEqual(
            m.command(rows(raw), T, "A"), image(act(BLOCKS, (circle(*CIRCLE["A"]),) * 4))
        )
        self.assertEqual(
            m.transpose_blocks(rows(raw), T), image(tuple(transpose(rho) for rho in BLOCKS))
        )
        dephased = m.filtered_dephasing(rows(raw), T, F(3, 5))
        self.assertEqual(m.inverse_dephasing_diagnostic(rows(dephased), T, F(3, 5)), raw)
        source = prepared()
        context = replace(source.context, permutation=iter(source.context.permutation))
        self.assertEqual(context.permutation, tuple(grouped(a, b, i, j) for a, i, b, j in BITS))
        changed = m.run_word(source, iter(("A", "B")))
        self.assertEqual(changed.pending, ("A", "B"))
        record = m.JointRecord(
            m.INTERIOR_DOMAIN,
            0,
            (0, 0),
            (iter(item) for item in (("beam", 0), ("beam", 1), ("probe", 0))),
            context,
            iter(("A", "B")),
        )
        state = m.State(
            m.INTERIOR_DOMAIN, context, rows(source.residual), iter((record,)), iter(("A_inv",))
        )
        self.assertEqual((state.records, state.pending), ((record,), ("A_inv",)))
        self.assertEqual(record.command_word, ("A", "B"))
        input_record = m.InputRecord(
            1,
            "calibrate",
            "pass",
            iter(("H",)),
            (iter(item) for item in (("sample", "full"),)),
            iter((0,)),
        )
        self.assertEqual(
            (input_record.settings, input_record.payload, input_record.precursor),
            (("H",), (("sample", "full"),), (0,)),
        )

    def test_record_ids_full_words_and_precursors_are_strict_and_immutable(self):
        source = prepared()
        _, selected = m.commit(m.run_word(source, ("A", "B")), (0, 0))
        record = selected.records[0]
        for invalid in (False, 0.0, F(0), -1):
            with self.assertRaises(ValueError):
                replace(record, event_id=invalid)
            with self.assertRaises(ValueError):
                m.InputRecord(invalid, "a", "o")
        for outcome in ((False, 0), (F(0), 0), (0.0, 0), (0,), [0, 0]):
            with self.assertRaises(ValueError):
                replace(record, outcome=outcome)
        for precursor in (("beam", 0), (("beam", False),), record.precursor[:-1]):
            with self.assertRaises((TypeError, ValueError)):
                replace(record, precursor=precursor)
        for invalid in (False, F(0), 0.0):
            with self.assertRaises(ValueError):
                replace(source.context, permutation=(invalid,) + source.context.permutation[1:])
        with self.assertRaises(TypeError):
            replace(record, command_word="AB")
        with self.assertRaises(ValueError):
            replace(record, command_word=("unavailable",))
        with self.assertRaises(FrozenInstanceError):
            record.command_word = ("AB",)
        with self.assertRaises(FrozenInstanceError):
            source.context.reference.t = F(0)
        with self.assertRaises(ValueError):
            m.State(
                m.INTERIOR_DOMAIN,
                source.context,
                source.residual,
                (replace(record, event_id=1, precursor=record.precursor + (("joint-run", 0),)),),
            )

    def test_algebraic_diagnostics_reject_bad_domains_matrices_and_unproved_positive_inverses(self):
        raw = image(BLOCKS)
        signed_blocks = sparse_blocks(0, Y)
        signed = image(signed_blocks)
        expected = image(act(signed_blocks, (circle(*CIRCLE["A"]),) * 4))
        self.assertEqual(m.command_on_span(signed, T, "A"), expected)
        with self.assertRaises(ValueError):
            m.command(signed, T, "A")
        self.assertEqual(m.command(zeros(16), T, "A"), zeros(16))
        for bad_unitary in (scale(2, eye(2)), zeros(2), eye(3)):
            with self.assertRaises(ValueError):
                m.weighted_unitary(bad_unitary, (0, 0), T)
        with self.assertRaises(ValueError):
            m.weighted_action(raw, T, (eye(2),) * 3)
        with self.assertRaises(ValueError):
            m.weighted_generator(matrix(((1, 1), (0, 0))), (0, 0), T)
        with self.assertRaises(ValueError):
            m.generator_action_on_span(raw, T, (X,) * 3)
        with self.assertRaises(ValueError):
            m.inverse_span(image(BLOCKS, F(-3, 5)), T)
        for rate in (F(-1), F(2)):
            with self.assertRaises(ValueError):
                m.filtered_dephasing(raw, T, rate)
        with self.assertRaises(ValueError):
            m.inverse_dephasing_diagnostic(raw, T, 0)
        for rate in (0, -1):
            with self.assertRaises(ValueError):
                m.endpoint_scale_operator((0, 0), 1, rate)
        with self.assertRaises(ValueError):
            m.endpoint_scale(raw, T, 2)
        for t in (True, 0.6):
            with self.assertRaises(TypeError):
                m.block_filter((0, 0), t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
