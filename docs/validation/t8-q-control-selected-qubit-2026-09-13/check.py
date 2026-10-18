"""Independent exact checks of a supplied control-selected qubit candidate.

Gaussian pair arithmetic, real row reduction and closed signed-Pauli groups
are independent certificates. No bounded word-depth search is described as
all-word closure. These tests establish no DET selection or physical access
to the supplied preparations, controls, or additional terminal effects.
"""

import unittest
from dataclasses import FrozenInstanceError
from fractions import Fraction as F

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
    output = ZERO
    for value in values:
        output = plus(output, value)
    return output


def matrix(rows):
    return tuple(tuple(m.G(*pair(entry)) for entry in row) for row in rows)


def add(left, right):
    return matrix(
        tuple(plus(a, b) for a, b in zip(x, y, strict=True))
        for x, y in zip(left, right, strict=True)
    )


def scale(coefficient, operator):
    return matrix(tuple(times(coefficient, entry) for entry in row) for row in operator)


def dagger(operator):
    return matrix(
        tuple(conj(operator[i][j]) for i in range(len(operator))) for j in range(len(operator[0]))
    )


def transpose(operator):
    return matrix(
        tuple(operator[i][j] for i in range(len(operator))) for j in range(len(operator[0]))
    )


def mm(left, right):
    return matrix(
        tuple(
            total(times(left[i][k], right[k][j]) for k in range(len(right)))
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def outer(vector):
    return matrix(tuple(times(a, conj(b)) for b in vector) for a in vector)


def eye(size):
    return matrix(tuple(int(i == j) for j in range(size)) for i in range(size))


def zeros(size):
    return matrix((0,) * size for _ in range(size))


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


def hermitian_basis(size):
    result = []
    for i in range(size):
        result.append(matrix(tuple(int(r == c == i) for c in range(size)) for r in range(size)))
    for i in range(size):
        for j in range(i + 1, size):
            for coefficient in (1, (0, 1)):
                result.append(
                    matrix(
                        tuple(
                            coefficient
                            if (r, c) == (i, j)
                            else conj(coefficient)
                            if (r, c) == (j, i)
                            else 0
                            for c in range(size)
                        )
                        for r in range(size)
                    )
                )
    return tuple(result)


X = matrix(((0, 1), (1, 0)))
Y = matrix(((0, (0, -1)), ((0, 1), 0)))
Z = matrix(((1, 0), (0, -1)))
U = {
    "H": (matrix(((1, 1), (1, -1))), F(1, 2)),
    "P": (matrix(((1, 0), (0, (0, 1)))), F(1)),
    "P_inv": (matrix(((1, 0), (0, (0, -1)))), F(1)),
    "Z": (Z, F(1)),
}
PAULI_ACTIONS = {"H": (3, -2, 1), "P": (2, -1, 3), "P_inv": (-2, 1, 3), "Z": (-1, -2, 3)}


def assemble(a, f, b):
    adjoint = dagger(f)
    return tuple(tuple(a[i]) + tuple(f[i]) for i in range(2)) + tuple(
        tuple(adjoint[i]) + tuple(b[i]) for i in range(2)
    )


def candidate(a, c=0):
    return assemble(a, scale(c, Z), mm(mm(Z, a), Z))


def control(operator, name):
    numerator, factor = U[name]
    w = assemble(numerator, zeros(2), mm(mm(Z, numerator), Z))
    return scale(factor, mm(mm(w, operator), dagger(w)))


def word(operator, names):
    for name in names:
        operator = control(operator, name)
    return operator


def weights(operator):
    return tuple(total(operator[i][j] for i in cell for j in cell)[0] for cell in ((0, 1), (2, 3)))


def mass(operator):
    value = total(entry for row in operator for entry in row)
    if value[1]:
        raise ValueError("Expected a real Hermitian mass")
    return value[0]


def cross(operator):
    return total(operator[i][j] for i in (0, 1) for j in (2, 3))


def constraints(operator):
    output = (*cross(operator), *cross(control(operator, "Z")), *cross(control(operator, "H")))
    before, after = weights(operator), weights(control(operator, "Z"))
    return (
        output
        + (after[0] - before[1], after[1] - before[0])
        + tuple(mass(control(operator, name)) - mass(operator) for name in ("H", "P"))
    )


def compose(left, right):
    return tuple((1 if value > 0 else -1) * left[abs(value) - 1] for value in right)


def group(generators):
    """Exact finite closure, storing a witness word for every signed action."""
    found = {(1, 2, 3): ()}
    frontier = [(1, 2, 3)]
    while frontier:
        old = frontier.pop(0)
        for name in generators:
            new = compose(PAULI_ACTIONS[name], old)
            if new not in found:
                found[new] = found[old] + (name,)
                frontier.append(new)
    return found


FULL = group(tuple(U))
NO_H = group(("P", "P_inv", "Z"))
NO_P = group(("H", "Z"))
COMPLEX_A = matrix(((F(3, 10), (0, F(1, 20))), ((0, F(-1, 20)), F(1, 5))))
COMPLEX_C = m.G(F(3, 100), F(1, 25))
COMPLEX_D = candidate(COMPLEX_A, COMPLEX_C)


class ControlSelectedChecks(unittest.TestCase):
    def test_gaussian_arithmetic_and_exact_input_validation(self):
        a, b = m.G(F(2, 3), F(-1, 5)), m.G(F(1, 4), F(3, 7))
        self.assertEqual(pair(a + b), plus(a, b))
        self.assertEqual(pair(a * b), times(a, b))
        self.assertEqual(pair(a.conjugate()), conj(a))
        self.assertEqual((a / b) * b, a)
        for value in (0.25, True, complex(0, 1)):
            with self.assertRaises(TypeError):
                m.G(value)
        with self.assertRaises(ZeroDivisionError):
            a / 0

    def test_full_initial_psd_cone_is_not_assumed_block_diagonal_or_candidate(self):
        a = scale(F(1, 4), eye(2))
        f = matrix(((F(1, 16), F(-1, 16)), (0, 0)))
        d = assemble(a, f, a)
        self.assertTrue(m.is_psd(d))
        self.assertTrue(m.recordable(d))
        self.assertEqual(m.full_kernel(d, normalized=True), d)
        self.assertNotEqual(f, zeros(2))
        with self.assertRaises(ValueError):
            m.decompose_candidate(d)
        with self.assertRaises(ValueError):
            m.State(d)
        self.assertEqual(m.controls(d, "H"), control(d, "H"))

    def test_complex_residual_and_unequal_diagonal_survive_candidate_encoding(self):
        # |c|=1/20 exactly; A-|c|I has positive diagonals and determinant 7/200.
        self.assertEqual(COMPLEX_C.norm_squared(), F(1, 400))
        self.assertEqual(F(1, 4) * F(3, 20) - F(1, 20) ** 2, F(7, 200))
        self.assertEqual(m.candidate_from(COMPLEX_A, COMPLEX_C, normalized=True), COMPLEX_D)
        self.assertEqual(m.decompose_candidate(COMPLEX_D, normalized=True), (COMPLEX_A, COMPLEX_C))
        self.assertEqual(m.mass(COMPLEX_D), 1)
        self.assertNotEqual(m.blocks(COMPLEX_D)[1], zeros(2))
        self.assertNotEqual(COMPLEX_A[0][0], COMPLEX_A[1][1])

    def test_psd_boundary_depends_on_absolute_complex_c_not_just_real_part(self):
        a = matrix(((F(1, 10), 0), (0, F(2, 5))))
        for c in (F(1, 10), m.G(0, F(1, 10)), m.G(F(3, 50), F(2, 25))):
            self.assertEqual(pair(c)[0] ** 2 + pair(c)[1] ** 2, F(1, 100))
            self.assertTrue(m.is_psd(candidate(a, c)))
            self.assertEqual(m.decompose_candidate(candidate(a, c)), (a, c))
        for c in (F(3, 20), m.G(0, F(3, 20))):
            self.assertFalse(m.is_psd(candidate(a, c)))
            with self.assertRaises(ValueError):
                m.candidate_from(a, c)

    def test_candidate_real_span_retains_four_a_and_two_cross_block_coordinates(self):
        basis = tuple(candidate(a) for a in hermitian_basis(2)) + (
            candidate(zeros(2), 1),
            candidate(zeros(2), (0, 1)),
        )
        self.assertEqual(rank(tuple(flatten(d) for d in basis)), 6)
        self.assertTrue(all(constraints(d) == (0,) * 10 for d in basis))
        self.assertNotEqual(basis[-1], zeros(4))

    def test_full_hermitian_necessity_constraints_cut_span_fourteen_to_six(self):
        basis = hermitian_basis(4)
        self.assertEqual(rank(tuple(flatten(d) for d in basis)), 16)
        initial_rows = tuple(zip(*(cross(d) for d in basis), strict=True))
        all_rows = tuple(zip(*(constraints(d) for d in basis), strict=True))
        self.assertEqual(rank(initial_rows), 2)
        self.assertEqual(rank(all_rows), 10)
        self.assertEqual(16 - rank(initial_rows), 14)
        self.assertEqual(16 - rank(all_rows), 6)
        # Together with the explicit six-dimensional nullspace above, this
        # is a necessity certificate on the full Hermitian space, not PSD samples.

    def test_signed_pauli_groups_are_closed_not_depth_truncated(self):
        for generators, expected, found in (
            (tuple(U), 24, FULL),
            (("P", "P_inv", "Z"), 4, NO_H),
            (("H", "Z"), 8, NO_P),
        ):
            self.assertEqual(len(found), expected)
            for action, names in found.items():
                calculated = (1, 2, 3)
                for name in names:
                    calculated = compose(PAULI_ACTIONS[name], calculated)
                self.assertEqual(calculated, action)
                for name in generators:
                    self.assertIn(compose(PAULI_ACTIONS[name], action), found)

    def test_generator_pauli_actions_and_full_congruences_match_exact_matrices(self):
        paulis = (X, Y, Z)
        # I,X,Y,Z are a complex basis of all two-by-two matrices. Their
        # conjugation action therefore also determines arbitrary complex FZ,
        # not just Hermitian diagonal blocks or the selected candidate.
        complex_basis = (eye(2), *paulis)
        real_basis = complex_basis + tuple(scale((0, 1), d) for d in complex_basis)
        self.assertEqual(rank(tuple(flatten(d) for d in real_basis)), 8)
        for name, (numerator, factor) in U.items():
            self.assertEqual(scale(factor, mm(numerator, dagger(numerator))), eye(2))
            for index, pauli in enumerate(paulis):
                image = scale(factor, mm(mm(numerator, pauli), dagger(numerator)))
                target = PAULI_ACTIONS[name][index]
                expected = scale(1 if target > 0 else -1, paulis[abs(target) - 1])
                self.assertEqual(image, expected)
            expected_four = assemble(numerator, zeros(2), mm(mm(Z, numerator), Z))
            self.assertEqual(m.control_spec(name), (expected_four, factor))
            self.assertEqual(m.controls(COMPLEX_D, name), control(COMPLEX_D, name))

    def test_every_closed_catalogue_action_preserves_candidate_mass_and_calibration(self):
        for names in FULL.values():
            output = m.word(COMPLEX_D, names)
            self.assertEqual(output, word(COMPLEX_D, names))
            self.assertTrue(m.recordable(output))
            self.assertEqual(m.mass(output), 1)
            self.assertEqual(m.decompose_candidate(output)[1], COMPLEX_C)
            self.assertEqual(m.qcell(m.controls(output, "Z")), tuple(reversed(m.qcell(output))))
            for name in U:
                self.assertEqual(m.mass(m.controls(output, name)), 1)

    def test_quotient_transpose_psd_section_and_normalization_are_explicit(self):
        rho = scale(2, transpose(COMPLEX_A))
        self.assertEqual(m.q_quantum(COMPLEX_D), rho)
        self.assertTrue(m.is_psd(rho))
        self.assertEqual(rho[0][0].real + rho[1][1].real, 1)
        section = m.section(rho, normalized=True)
        self.assertEqual(m.q_quantum(section), rho)
        self.assertEqual(m.decompose_candidate(section)[1], 0)
        self.assertNotEqual(section, COMPLEX_D)
        for pure in (outer((1, 0)), scale(F(1, 2), outer((1, (0, 1))))):
            self.assertEqual(m.q_quantum(m.section(pure, normalized=True)), pure)

    def test_quotient_controls_use_conjugate_u_and_transpose_u(self):
        rho = m.q_quantum(COMPLEX_D)
        for names in FULL.values():
            expected = rho
            for name in names:
                numerator, factor = U[name]
                conjugated = matrix(tuple(conj(entry) for entry in row) for row in numerator)
                expected = scale(factor, mm(mm(conjugated, expected), transpose(numerator)))
            self.assertEqual(m.q_quantum(m.word(COMPLEX_D, names)), expected)

    def test_i_h_p_terminal_tomography_has_correct_y_transpose_sign(self):
        rx, ry, rz = F(1, 5), F(1, 3), F(1, 4)
        a = scale(F(1, 4), add(add(add(eye(2), scale(rx, X)), scale(ry, Y)), scale(rz, Z)))
        d = m.candidate_from(a, normalized=True)
        expected_rho = scale(
            F(1, 2), add(add(add(eye(2), scale(rx, X)), scale(-ry, Y)), scale(rz, Z))
        )
        self.assertEqual(m.q_quantum(d), expected_rho)
        self.assertEqual(m.qcell(d), ((1 + rx) / 2, (1 - rx) / 2))
        self.assertEqual(m.qcell(m.controls(d, "H")), ((1 + rz) / 2, (1 - rz) / 2))
        self.assertEqual(m.qcell(m.controls(d, "P")), ((1 - ry) / 2, (1 + ry) / 2))

    def test_tomographic_effect_rank_is_four_with_exactly_two_invisible_directions(self):
        basis = tuple(candidate(a) for a in hermitian_basis(2)) + (
            candidate(zeros(2), 1),
            candidate(zeros(2), (0, 1)),
        )
        effects = tuple(
            (mass(d), weights(d)[0], weights(control(d, "H"))[0], weights(control(d, "P"))[0])
            for d in basis
        )
        self.assertEqual(rank(tuple(zip(*effects, strict=True))), 4)
        self.assertEqual(effects[-2:], ((0, 0, 0, 0), (0, 0, 0, 0)))

    def test_hidden_complex_residual_is_catalogue_relative_not_all_effect_equivalence(self):
        a = scale(F(1, 4), eye(2))
        left, right = candidate(a, F(1, 8)), candidate(a, F(-1, 8))
        self.assertEqual(m.q_quantum(left), m.q_quantum(right))
        for names in FULL.values():
            self.assertEqual(m.qcell(m.word(left, names)), m.qcell(m.word(right, names)))
            left_source = m.run_word(m.State(left), names)
            right_source = m.run_word(m.State(right), names)
            for outcome in (0, 1):
                left_probability, left_terminal = m.commit_cell(left_source, outcome)
                right_probability, right_terminal = m.commit_cell(right_source, outcome)
                self.assertEqual(left_probability, right_probability)
                self.assertEqual(left_terminal.residual, right_terminal.residual)
                self.assertEqual(left_terminal.records, right_terminal.records)
                self.assertEqual(left_terminal, right_terminal)
        extra_left = m.mass(left) / 2 + m.decompose_candidate(left)[1].real
        extra_right = m.mass(right) / 2 + m.decompose_candidate(right)[1].real
        self.assertEqual((extra_left, extra_right), (F(5, 8), F(3, 8)))
        # This extra mathematical effect distinguishes source/pre-read states
        # outside the declared catalogue. The literal cuts delete c, so they
        # leave identical full terminal residuals, not merely equal weights.

    def test_uninformative_ray_also_satisfies_controls_without_full_preparation_access(self):
        d = candidate(scale(F(1, 4), eye(2)))
        for names in FULL.values():
            self.assertEqual(word(d, names), d)
            self.assertEqual(weights(word(d, names)), (F(1, 2), F(1, 2)))
        self.assertEqual(m.q_quantum(d), scale(F(1, 2), eye(2)))

    def test_deleting_h_admits_a_closed_subgroup_witness_rejected_by_h_mass(self):
        a = add(scale(F(1, 4), eye(2)), scale(F(1, 8), Z))
        c = add(scale(F(1, 4), eye(2)), scale(F(-1, 8), Z))
        d = assemble(a, zeros(2), mm(mm(Z, c), Z))
        self.assertTrue(m.is_psd(d))
        for names in NO_H.values():
            output = word(d, names)
            self.assertEqual(cross(output), ZERO)
            self.assertEqual(mass(output), 1)
            self.assertEqual(weights(control(output, "Z")), tuple(reversed(weights(output))))
        self.assertEqual(mass(control(d, "H")), F(3, 2))
        with self.assertRaises(ValueError):
            m.decompose_candidate(d)

    def test_deleting_p_and_inverse_admits_witness_rejected_by_quarter_phase_mass(self):
        a = add(scale(F(1, 4), eye(2)), scale(F(1, 8), Y))
        c = add(scale(F(1, 4), eye(2)), scale(F(-1, 8), Y))
        d = assemble(a, zeros(2), mm(mm(Z, c), Z))
        self.assertTrue(m.is_psd(d))
        for names in NO_P.values():
            output = word(d, names)
            self.assertEqual(cross(output), ZERO)
            self.assertEqual(mass(output), 1)
            self.assertEqual(weights(control(output, "Z")), tuple(reversed(weights(output))))
        self.assertEqual(mass(control(d, "P")), F(1, 2))
        with self.assertRaises(ValueError):
            m.decompose_candidate(d)

    def test_deleting_label_swap_calibration_admits_an_all_control_witness(self):
        a, c = scale(F(1, 8), eye(2)), scale(F(3, 8), eye(2))
        d = assemble(a, zeros(2), mm(mm(Z, c), Z))
        self.assertTrue(m.is_psd(d))
        for names in FULL.values():
            output = word(d, names)
            self.assertEqual(cross(output), ZERO)
            self.assertEqual(mass(output), 1)
        self.assertEqual(weights(d), (F(1, 4), F(3, 4)))
        self.assertEqual(weights(control(d, "Z")), weights(d))
        self.assertNotEqual(weights(control(d, "Z")), tuple(reversed(weights(d))))

    def test_literal_cell_cut_keeps_full_residual_but_exits_the_source_candidate(self):
        source = m.State(COMPLEX_D)
        for outcome in (0, 1):
            probability, terminal = m.commit_cell(source, outcome)
            projector = matrix(
                tuple(int(i == j and i // 2 == outcome) for j in range(4)) for i in range(4)
            )
            raw = mm(mm(projector, COMPLEX_D), projector)
            self.assertEqual(probability, mass(raw))
            self.assertEqual(terminal.residual, scale(1 / probability, raw))
            self.assertEqual(m.mass(terminal.residual), 1)
            with self.assertRaises(ValueError):
                m.decompose_candidate(terminal.residual)
            with self.assertRaises(TypeError):
                m.run_control(terminal, "H")
            with self.assertRaises(TypeError):
                m.run_word(terminal, ("P",))
            with self.assertRaises(TypeError):
                m.commit_cell(terminal, 0)

    def test_controls_preserve_history_and_commit_retains_full_actual_setting_word(self):
        old = m.Record(0, 1, ("P",), ())
        source = m.State(COMPLEX_D, (old,))
        names = ("P", "H", "P_inv", "Z")
        controlled = m.run_word(source, names)
        self.assertIs(controlled.records, source.records)
        self.assertEqual(controlled.settings, names)
        self.assertEqual(source.settings, ())
        _, terminal = m.commit_cell(controlled, 0)
        self.assertEqual(terminal.records[:-1], (old,))
        self.assertEqual(terminal.records[-1], m.Record(1, 0, names, (0,)))
        self.assertEqual(terminal.records[-1].action, "terminal_cell_read")
        self.assertEqual(terminal.records[-1].source_kind, "control_selected")
        with self.assertRaises(FrozenInstanceError):
            terminal.records[0].event_id = 9

    def test_nonzero_zero_mass_literal_cut_refuses_before_record_append(self):
        a = scale(F(1, 4), outer((1, -1)))
        d = m.candidate_from(a, normalized=True)
        source = m.State(d)
        projector = matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)))
        raw = mm(mm(projector, d), projector)
        self.assertNotEqual(raw, zeros(4))
        self.assertTrue(m.is_psd(raw))
        self.assertEqual(m.mass(raw), 0)
        self.assertEqual(m.qcell(d), (0, 1))
        with self.assertRaises(ValueError):
            m.commit_cell(source, 0)
        self.assertEqual(source.records, ())
        self.assertEqual(source.residual, d)

    def test_one_shot_control_words_are_retained_and_strings_are_rejected(self):
        source = m.State(COMPLEX_D)
        names = ("P", "H", "P_inv")
        controlled = m.run_word(source, (name for name in names))
        self.assertEqual(controlled.settings, names)
        self.assertEqual(controlled.residual, m.word(COMPLEX_D, names))
        for call in (lambda: m.word(COMPLEX_D, "H"), lambda: m.run_word(source, "P")):
            with self.assertRaises(TypeError):
                call()

    def test_history_checks_grammar_not_global_preparation_or_terminal_reuse(self):
        old = m.Record(0, 0, (), ())
        state = m.State(COMPLEX_D, (old,), ("H",))
        self.assertEqual(state.residual, COMPLEX_D)
        self.assertEqual(state.settings, ("H",))
        with self.assertRaises(ValueError):
            m.State(COMPLEX_D, (m.Record(1, 0, (), ()),))
        with self.assertRaises(ValueError):
            m.State(COMPLEX_D, (old, m.Record(1, 0, (), ())))
        with self.assertRaises(ValueError):
            m.TerminalState(COMPLEX_D, (old,))

    def test_malformed_unnormalized_or_unavailable_inputs_are_not_repaired(self):
        for d in (eye(2), matrix(((1, 2, 0, 0), (2, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)))):
            with self.assertRaises(ValueError):
                m.full_kernel(d)
        with self.assertRaises(ValueError):
            m.State(scale(2, COMPLEX_D))
        with self.assertRaises(ValueError):
            m.section(eye(2), normalized=True)
        with self.assertRaises(ValueError):
            m.run_control(m.State(COMPLEX_D), "unregistered")
        for outcome in (True, -1, 2, F(0)):
            with self.assertRaises(ValueError):
                m.commit_cell(m.State(COMPLEX_D), outcome)


if __name__ == "__main__":
    unittest.main(verbosity=2)
