"""Independent exact checks for the conditional repeatable-instrument result.

The source includes its full complex cross-block coordinate. Pair-valued
rational algebra and finite linear certificates below check the derived
branch formula, not DET selection or physical availability. Reachability statements
refer only to the declared preparation, control and randomization rules.
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


X = matrix(((0, 1), (1, 0)))
Y = matrix(((0, (0, -1)), ((0, 1), 0)))
Z = matrix(((1, 0), (0, -1)))
PAULI = {"X": X, "Y": Y, "Z": Z}
OUTCOMES = tuple((axis, outcome) for axis in PAULI for outcome in (0, 1))


def projector(axis, outcome):
    return scale(F(1, 2), add(eye(2), scale(1 if outcome == 0 else -1, PAULI[axis])))


def assemble(a, f, b):
    adjoint = dagger(f)
    return tuple(tuple(a[i]) + tuple(f[i]) for i in range(2)) + tuple(
        tuple(adjoint[i]) + tuple(b[i]) for i in range(2)
    )


def candidate(a, c=0):
    return assemble(a, scale(c, Z), mm(mm(Z, a), Z))


def section(rho):
    return candidate(scale(F(1, 2), transpose(rho)))


def phi(operator):
    return scale(2, transpose(matrix(row[:2] for row in operator[:2])))


def effect(operator, axis, outcome):
    value = trace(mm(phi(operator), projector(axis, outcome)))
    if value[1]:
        raise ValueError("A Hermitian effect must be real")
    return value[0]


def branch(operator, axis, outcome):
    return scale(effect(operator, axis, outcome), section(projector(axis, outcome)))


def coordinates(operator):
    return (
        operator[0][0].real,
        operator[1][1].real,
        operator[0][1].real,
        operator[0][1].imag,
        operator[0][2].real,
        operator[0][2].imag,
    )


def from_coordinates(values):
    a, b, x, y, real_c, imag_c = values
    return candidate(matrix(((a, (x, y)), ((x, -y), b))), (real_c, imag_c))


SPAN = tuple(from_coordinates(tuple(F(int(i == j)) for i in range(6))) for j in range(6))
CENTER_RHO = scale(F(1, 2), eye(2))
CENTER = section(CENTER_RHO)
VERTICES = tuple(section(projector(axis, outcome)) for axis, outcome in OUTCOMES)
COMPLEX_A = matrix(((F(3, 10), (0, F(1, 20))), ((0, F(-1, 20)), F(1, 5))))
COMPLEX_C = m.G(F(3, 100), F(1, 25))
COMPLEX_D = candidate(COMPLEX_A, COMPLEX_C)


def bloch(rho):
    return tuple(trace(mm(rho, pauli))[0] for pauli in PAULI.values())


class RepeatableInstrumentChecks(unittest.TestCase):
    def test_full_complex_source_and_signed_six_dimensional_span_are_retained(self):
        self.assertEqual(m.decompose_candidate(COMPLEX_D, normalized=True), (COMPLEX_A, COMPLEX_C))
        self.assertNotEqual(COMPLEX_C.imag, 0)
        self.assertEqual(m.phi(COMPLEX_D), phi(COMPLEX_D))
        self.assertEqual(rank(tuple(flatten(d) for d in SPAN)), 6)
        for index, d in enumerate(SPAN):
            self.assertEqual(coordinates(d), tuple(F(int(index == i)) for i in range(6)))
            self.assertEqual(m.phi_on_span(d), phi(d))

    def test_six_pauli_projectors_have_exact_rank_one_orthogonal_face_certificates(self):
        for axis, outcome in OUTCOMES:
            q = projector(axis, outcome)
            other = projector(axis, 1 - outcome)
            self.assertEqual(m.projector(axis, outcome), q)
            self.assertEqual(mm(q, q), q)
            self.assertEqual(mm(q, other), zeros(2))
            self.assertEqual(add(q, other), eye(2))
            self.assertEqual(trace(q), (F(1), F(0)))
            self.assertTrue(m.is_psd(q))
            self.assertEqual(times(q[0][0], q[1][1]), times(q[0][1], q[1][0]))

    def test_effects_match_independent_trace_and_complex_y_sign(self):
        for axis, outcome in OUTCOMES:
            self.assertEqual(m.effect(COMPLEX_D, axis, outcome), effect(COMPLEX_D, axis, outcome))
        self.assertEqual(m.effect(COMPLEX_D, "Y", 0), F(3, 5))
        self.assertEqual(m.effect(COMPLEX_D, "Y", 1), F(2, 5))
        self.assertEqual(m.effect(COMPLEX_D, "Z", 0), F(3, 5))
        self.assertEqual(m.effect(COMPLEX_D, "X", 0), F(1, 2))

    def test_each_branch_is_the_exact_rank_one_linear_map_on_the_full_span(self):
        for axis, outcome in OUTCOMES:
            images = tuple(m.branch_on_span(d, axis, outcome) for d in SPAN)
            expected = tuple(branch(d, axis, outcome) for d in SPAN)
            self.assertEqual(images, expected)
            self.assertEqual(rank(tuple(coordinates(d) for d in images)), 1)
            self.assertEqual(images[-2:], (zeros(4), zeros(4)))
            signed = from_coordinates((2, -3, F(1, 4), F(-2, 5), 3, -7))
            expanded = zeros(4)
            for coefficient, output in zip(coordinates(signed), images, strict=True):
                expanded = add(expanded, scale(coefficient, output))
            self.assertEqual(m.branch_on_span(signed, axis, outcome), expanded)

    def test_exposed_ray_and_mass_constraints_determine_all_thirty_six_map_coefficients(self):
        unit = (F(2), F(2), F(0), F(0), F(0), F(0))
        for axis, outcome in OUTCOMES:
            ray = coordinates(section(projector(axis, outcome)))
            pivot = next(i for i, value in enumerate(ray) if value)
            annihilators = []
            for i in range(6):
                if i != pivot:
                    row = [F(0)] * 6
                    row[i] = 1
                    row[pivot] = -ray[i] / ray[pivot]
                    annihilators.append(tuple(row))
            output_constraints = (*annihilators, unit)
            self.assertEqual(rank(output_constraints), 6)
            full_constraints = []
            for column in range(6):
                for row in output_constraints:
                    full_constraints.append(
                        tuple(row[i % 6] if i // 6 == column else F(0) for i in range(36))
                    )
            self.assertEqual(rank(full_constraints), 36)
            for d in SPAN:
                output = coordinates(m.branch_on_span(d, axis, outcome))
                for annihilator in annihilators:
                    self.assertEqual(
                        sum((a * b for a, b in zip(annihilator, output, strict=True)), F(0)), 0
                    )
                self.assertEqual(
                    sum((a * b for a, b in zip(unit, output, strict=True)), F(0)),
                    effect(d, axis, outcome),
                )
        # Positivity+repeatability first imply the exposed ray (proved in the
        # note); this exact linear system then certifies uniqueness, not its premise.
        # The declared domain is the whole six-dimensional source span; these
        # obligations are not inferred from the seven reachable c=0 states.

    def test_repeatable_output_face_forces_zero_c_without_truncating_source(self):
        for axis, outcome in OUTCOMES:
            rho = projector(axis, outcome)
            a = scale(F(1, 2), transpose(rho))
            self.assertEqual(m.candidate_from(a), section(rho))
            for c in (F(1, 100), m.G(0, F(1, 100))):
                self.assertFalse(m.is_psd(candidate(a, c)))
                with self.assertRaises(ValueError):
                    m.candidate_from(a, c)
        for cross in (F(1, 10), m.G(0, F(1, 10))):
            # In a basis exposing the zero opposite-outcome weight, a nonzero
            # off-diagonal has determinant -|cross|^2 and cannot be PSD.
            d = matrix(((1, cross), (conj(cross), 0)))
            self.assertFalse(m.is_psd(d))

    def test_complex_source_c_is_killed_by_branch_map_not_a_precondition(self):
        for c in (COMPLEX_C, -COMPLEX_C, m.G(0, F(1, 20))):
            d = m.candidate_from(COMPLEX_A, c, normalized=True)
            self.assertNotEqual(m.decompose_candidate(d)[1], 0)
            for axis, outcome in OUTCOMES:
                output = m.branch(d, axis, outcome)
                self.assertEqual(output, branch(COMPLEX_D, axis, outcome))
                self.assertEqual(m.decompose_candidate(output)[1], 0)

    def test_faithful_source_mass_and_zero_effect_give_full_zero_output(self):
        self.assertEqual(m.decompose_candidate(zeros(4)), (zeros(2), 0))
        for c in (1, m.I):
            with self.assertRaises(ValueError):
                m.candidate_from(zeros(2), c)
        for axis, outcome in OUTCOMES:
            source = section(projector(axis, 1 - outcome))
            self.assertEqual(m.effect(source, axis, outcome), 0)
            self.assertEqual(m.branch(source, axis, outcome), zeros(4))
            self.assertEqual(m.branch(zeros(4), axis, outcome), zeros(4))
        source = section(projector("X", 1))
        literal_projector = matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)))
        raw = mm(mm(literal_projector, source), literal_projector)
        self.assertNotEqual(raw, zeros(4))
        self.assertTrue(m.is_psd(raw))
        self.assertEqual(m.mass(raw), 0)
        self.assertEqual(m.branch(source, "X", 0), zeros(4))
        state = m.State(source)
        with self.assertRaises(ValueError):
            m.literal_cut(state, 0)
        self.assertEqual(state.records, ())

    def test_all_six_branch_outputs_are_positive_and_have_the_declared_mass(self):
        for d in (CENTER, COMPLEX_D, *VERTICES):
            for axis, outcome in OUTCOMES:
                output = m.branch(d, axis, outcome)
                probability = m.effect(d, axis, outcome)
                self.assertGreaterEqual(probability, 0)
                self.assertLessEqual(probability, 1)
                self.assertEqual(m.mass(output), probability)
                self.assertTrue(m.is_psd(output))
                self.assertEqual(output, branch(d, axis, outcome))

    def test_same_setting_repeatability_and_opposite_branch_annihilation(self):
        for axis, outcome in OUTCOMES:
            output = m.branch(COMPLEX_D, axis, outcome)
            self.assertEqual(m.branch(output, axis, outcome), output)
            self.assertEqual(m.branch(output, axis, 1 - outcome), zeros(4))
            probability = m.mass(output)
            normalized = scale(1 / probability, output)
            self.assertEqual(m.effect(normalized, axis, outcome), 1)
            self.assertEqual(m.effect(normalized, axis, 1 - outcome), 0)

    def test_each_complete_instrument_preserves_mass_but_not_generally_source(self):
        for d in (CENTER, COMPLEX_D, *VERTICES):
            for axis in PAULI:
                outputs = tuple(m.branch(d, axis, outcome) for outcome in (0, 1))
                summed = add(*outputs)
                self.assertEqual(m.mass(summed), m.mass(d))
                expected_rho = add(
                    mm(mm(projector(axis, 0), phi(d)), projector(axis, 0)),
                    mm(mm(projector(axis, 1), phi(d)), projector(axis, 1)),
                )
                self.assertEqual(phi(summed), expected_rho)
        self.assertNotEqual(
            add(m.branch(COMPLEX_D, "X", 0), m.branch(COMPLEX_D, "X", 1)), COMPLEX_D
        )

    def test_same_effect_mixed_reset_is_a_positive_nonrepeatable_countermodel(self):
        for axis, outcome in OUTCOMES:
            probability = effect(COMPLEX_D, axis, outcome)
            mixed_reset = scale(probability, CENTER)
            self.assertTrue(m.is_psd(mixed_reset))
            self.assertEqual(m.mass(mixed_reset), probability)
            self.assertEqual(effect(mixed_reset, axis, 1 - outcome), probability / 2)
            self.assertGreater(effect(mixed_reset, axis, 1 - outcome), 0)
            self.assertNotEqual(mixed_reset, m.branch(COMPLEX_D, axis, outcome))

    def test_literal_cut_countermodel_exits_candidate_and_cannot_continue(self):
        source = m.State(COMPLEX_D)
        for outcome in (0, 1):
            probability, terminal = m.literal_cut(source, outcome)
            projector4 = matrix(
                tuple(int(i == j and i // 2 == outcome) for j in range(4)) for i in range(4)
            )
            raw = mm(mm(projector4, COMPLEX_D), projector4)
            self.assertEqual(terminal.residual, scale(1 / probability, raw))
            self.assertEqual(probability, m.effect(COMPLEX_D, "X", outcome))
            self.assertEqual(
                m.qcell(terminal.residual), tuple(F(int(i == outcome)) for i in (0, 1))
            )
            self.assertEqual(mm(mm(projector4, terminal.residual), projector4), terminal.residual)
            with self.assertRaises(ValueError):
                m.decompose_candidate(terminal.residual)
            with self.assertRaises(ValueError):
                m.effect(terminal.residual, "X", outcome)
            for call in (
                lambda terminal=terminal: m.run_control(terminal, "H"),
                lambda terminal=terminal: m.commit_pauli(terminal, "X", 0),
            ):
                with self.assertRaises(TypeError):
                    call()

    def test_controls_actually_apply_before_fixed_frame_measurement(self):
        source = m.State(section(projector("X", 0)))
        controlled = m.run_control(source, "P")
        self.assertEqual(phi(controlled.residual), projector("Y", 1))
        self.assertEqual(controlled.settings, ("P",))
        self.assertEqual(m.effect(controlled.residual, "Y", 1), 1)
        probability, output = m.commit_pauli(controlled, "Y", 1)
        self.assertEqual(probability, 1)
        self.assertEqual(phi(output.residual), projector("Y", 1))
        self.assertEqual(output.records[-1].frame, "fixed_pauli")

    def test_repeat_does_not_reapply_the_previous_word_and_resets_only_pending_settings(self):
        controlled = m.run_control(m.State(section(projector("X", 0))), "P")
        _, first = m.commit_pauli(controlled, "Y", 1)
        probability, second = m.commit_pauli(first, "Y", 1)
        self.assertEqual(probability, 1)
        self.assertEqual(first.residual, second.residual)
        self.assertEqual(first.settings, ())
        self.assertEqual(second.settings, ())
        self.assertEqual(first.records[-1].settings, ("P",))
        self.assertEqual(second.records[-1].settings, ())
        self.assertEqual(second.records[0], first.records[0])

    def test_records_retain_axis_word_frame_controller_and_full_actual_precursor(self):
        source = m.State(COMPLEX_D)
        names = ("P", "H", "Z")
        controlled = m.run_word(source, names)
        self.assertIs(controlled.records, source.records)
        _, first = m.commit_pauli(controlled, "X", 0)
        _, second = m.commit_pauli(first, "X", 0)
        record = first.records[0]
        self.assertEqual((record.axis, record.outcome, record.settings), ("X", 0, names))
        self.assertEqual(record.action, "pauli_measure_prepare")
        self.assertEqual(record.controller, "pauli_controller")
        self.assertEqual(record.source_kind, "repeatable_selected")
        self.assertEqual(record.frame, "fixed_pauli")
        self.assertEqual(record.precursor, ())
        self.assertEqual(second.records[-1].precursor, (0,))
        self.assertEqual(second.records[-1].event_id, 1)
        self.assertEqual(second.records[0], record)
        with self.assertRaises(FrozenInstanceError):
            second.records[0].axis = "Z"

    def test_zero_branch_refusal_preserves_residual_word_and_history(self):
        source = m.run_control(m.State(section(projector("X", 0))), "P")
        with self.assertRaises(ValueError):
            m.commit_pauli(source, "Y", 0)
        self.assertEqual(source.settings, ("P",))
        self.assertEqual(source.records, ())
        self.assertEqual(phi(source.residual), projector("Y", 1))

    def test_known_record_feedback_tree_preserves_complete_mass_and_each_history(self):
        source = m.State(COMPLEX_D)
        leaves = []
        for first_outcome in (0, 1):
            first_probability, first = m.commit_pauli(source, "X", first_outcome)
            name, axis = ("H", "X") if first_outcome == 0 else ("P", "Z")
            controlled = m.run_control(first, name)
            conditional_sum = F(0)
            for second_outcome in (0, 1):
                conditional_probability, leaf = m.commit_pauli(controlled, axis, second_outcome)
                conditional_sum += conditional_probability
                self.assertEqual(conditional_probability, F(1, 2))
                self.assertEqual(leaf.records[0], first.records[0])
                self.assertEqual(leaf.records[-1].settings, (name,))
                self.assertEqual(leaf.records[-1].axis, axis)
                self.assertEqual(leaf.records[-1].precursor, (0,))
                self.assertEqual(m.mass(leaf.residual), 1)
                leaves.append((first_probability * conditional_probability, leaf))
            self.assertEqual(conditional_sum, 1)
        self.assertEqual(sum((weight for weight, _ in leaves), F(0)), 1)
        self.assertEqual(len({leaf.records for _, leaf in leaves}), 4)
        self.assertEqual(source.records, ())

    def test_source_controls_remain_lawful_after_each_positive_commit(self):
        for axis, outcome in OUTCOMES:
            _, source = m.commit_pauli(m.State(COMPLEX_D), axis, outcome)
            for name in m.CONTROLS:
                output = m.run_control(source, name)
                self.assertEqual(m.mass(output.residual), 1)
                self.assertEqual(m.decompose_candidate(output.residual)[1], 0)
                self.assertIs(output.records, source.records)

    def test_no_mixing_reachability_is_exact_finite_closure_of_center_and_six_vertices(self):
        found = {CENTER}
        frontier = [CENTER]
        while frontier:
            source = frontier.pop(0)
            candidates = [m.controls(source, name) for name in m.CONTROLS]
            for axis, outcome in OUTCOMES:
                probability = m.effect(source, axis, outcome)
                if probability:
                    candidates.append(scale(1 / probability, m.branch(source, axis, outcome)))
            for output in candidates:
                if output not in found:
                    found.add(output)
                    frontier.append(output)
        self.assertEqual(found, {CENTER, *VERTICES})
        self.assertEqual(len(found), 7)
        # Exhaustion of the finite frontier certifies closure, not merely a
        # search through an arbitrarily bounded collection of control words.

    def test_rational_mixtures_construct_exact_points_in_the_octahedron(self):
        # These are explicitly mixed preparations or record-blind ensemble
        # marginals. Retaining the selector and conditioning on all records
        # leaves the corresponding component among the seven states above.
        for vector in ((F(1, 5), F(-3, 10), F(1, 10)), (F(1, 2), F(1, 2), 0), (0, 0, 0)):
            weights = [1 - sum(abs(component) for component in vector)]
            residuals = [CENTER]
            for axis, component in zip(PAULI, vector, strict=True):
                weights.extend((max(component, 0), max(-component, 0)))
                residuals.extend((section(projector(axis, 0)), section(projector(axis, 1))))
            mixture = m.mix_residuals(weights, residuals)
            self.assertEqual(bloch(phi(mixture)), vector)
            self.assertEqual(m.decompose_candidate(mixture)[1], 0)
            self.assertLessEqual(sum(abs(component) for component in bloch(phi(mixture))), 1)
        prior = (F(1, 3), F(2, 3))
        components = (section(projector("X", 0)), CENTER)
        mixture = m.mix_residuals(prior, components)
        for outcome, expected_mass, expected_posterior in (
            (0, F(2, 3), (F(1, 2), F(1, 2))),
            (1, F(1, 3), (F(0), F(1))),
        ):
            probabilities = tuple(m.effect(d, "X", outcome) for d in components)
            branch_outputs = tuple(m.branch(d, "X", outcome) for d in components)
            aggregate = add(
                *(
                    scale(weight, output)
                    for weight, output in zip(prior, branch_outputs, strict=True)
                )
            )
            self.assertEqual(m.branch(mixture, "X", outcome), aggregate)
            total_probability = m.mass(aggregate)
            self.assertEqual(total_probability, expected_mass)
            posterior = tuple(
                weight * probability / total_probability
                for weight, probability in zip(prior, probabilities, strict=True)
            )
            self.assertEqual(posterior, expected_posterior)
            normalized_sum = zeros(4)
            for weight, probability, output in zip(
                posterior, probabilities, branch_outputs, strict=True
            ):
                if probability:
                    normalized_sum = add(normalized_sum, scale(weight / probability, output))
                else:
                    self.assertEqual(weight, 0)
                    self.assertEqual(output, zeros(4))
            self.assertEqual(normalized_sum, scale(1 / total_probability, aggregate))
            self.assertEqual(sum(posterior), 1)

    def test_nonstabilizer_is_in_the_mathematical_bloch_ball_but_outside_octahedron(self):
        vector = (F(3, 5), F(0), F(3, 5))
        rho = scale(F(1, 2), add(add(eye(2), scale(vector[0], X)), scale(vector[2], Z)))
        self.assertEqual(sum(component**2 for component in vector), F(18, 25))
        self.assertEqual(sum(abs(component) for component in vector), F(6, 5))
        self.assertTrue(m.is_psd(rho))
        self.assertEqual(m.phi(m.section(rho, normalized=True)), rho)
        self.assertNotIn(section(rho), {CENTER, *VERTICES})

    def test_nonzero_c_is_mathematically_allowed_but_cannot_be_generated_from_zero_c(self):
        self.assertEqual(m.decompose_candidate(COMPLEX_D)[1], COMPLEX_C)
        self.assertNotEqual(COMPLEX_C, 0)
        for d in (CENTER, *VERTICES):
            for name in m.CONTROLS:
                self.assertEqual(m.decompose_candidate(m.controls(d, name))[1], 0)
            for axis, outcome in OUTCOMES:
                self.assertEqual(m.decompose_candidate(m.branch(d, axis, outcome))[1], 0)
        mixture = m.mix_residuals((F(1, 2), F(1, 2)), (CENTER, VERTICES[0]))
        self.assertEqual(m.decompose_candidate(mixture)[1], 0)
        self.assertNotEqual(m.section(m.phi(COMPLEX_D)), COMPLEX_D)
        # Algebraic preservation of c=0 under every generator and convex sum
        # proves the exclusion; the candidate itself still permits c!=0.

    def test_averaging_residuals_does_not_erase_recordful_branches(self):
        source = m.State(COMPLEX_D)
        branches = tuple(m.commit_pauli(source, "X", outcome) for outcome in (0, 1))
        self.assertNotEqual(branches[0][1].records, branches[1][1].records)
        weighted = add(*(scale(probability, state.residual) for probability, state in branches))
        self.assertEqual(weighted, add(m.branch(COMPLEX_D, "X", 0), m.branch(COMPLEX_D, "X", 1)))
        with self.assertRaises((TypeError, ValueError)):
            m.mix_residuals(
                tuple(probability for probability, _ in branches),
                tuple(state for _, state in branches),
            )
        self.assertEqual(tuple(state.records[-1].outcome for _, state in branches), (0, 1))

    def test_one_shot_words_and_mixture_iterables_are_consumed_once(self):
        names = ("H", "P", "Z")
        controlled = m.run_word(m.State(COMPLEX_D), (name for name in names))
        self.assertEqual(controlled.settings, names)
        self.assertEqual(controlled.residual, m.word(COMPLEX_D, names))
        mixture = m.mix_residuals(
            (weight for weight in (F(1, 3), F(2, 3))), (d for d in (CENTER, VERTICES[0]))
        )
        self.assertEqual(mixture, add(scale(F(1, 3), CENTER), scale(F(2, 3), VERTICES[0])))
        for axis, outcome in OUTCOMES:
            self.assertEqual(
                m.effect(((entry for entry in row) for row in COMPLEX_D), axis, outcome),
                m.effect(COMPLEX_D, axis, outcome),
            )
            self.assertEqual(
                m.branch(((entry for entry in row) for row in COMPLEX_D), axis, outcome),
                m.branch(COMPLEX_D, axis, outcome),
            )

    def test_terminal_record_cannot_be_repackaged_as_a_lawful_source_history(self):
        _, terminal = m.literal_cut(m.State(COMPLEX_D), 0)
        with self.assertRaises(ValueError):
            m.State(CENTER, terminal.records)
        self.assertEqual(terminal.records[-1].action, "literal_cell_cut")
        self.assertEqual(terminal.records[-1].axis, "CELL")

    def test_record_validation_is_structural_and_not_global_reachability(self):
        old = m.Record(0, "X", 0, (), ())
        state = m.State(COMPLEX_D, (old,), ("H",))
        self.assertEqual(state.residual, COMPLEX_D)
        self.assertEqual(state.settings, ("H",))
        with self.assertRaises(ValueError):
            m.State(CENTER, (m.Record(1, "X", 0, (), ()),))
        with self.assertRaises(ValueError):
            m.State(CENTER, (old, m.Record(1, "X", 0, (), ())))

    def test_invalid_axes_controls_frames_mixtures_and_zero_sources_are_rejected(self):
        for axis in ("CELL", "x", "unknown"):
            with self.assertRaises(ValueError):
                m.commit_pauli(m.State(CENTER), axis, 0)
        for outcome in (True, 2, -1, F(0)):
            with self.assertRaises(ValueError):
                m.commit_pauli(m.State(CENTER), "X", outcome)
        with self.assertRaises(ValueError):
            m.State(zeros(4))
        with self.assertRaises(ValueError):
            m.State(CENTER, frame="moving")
        with self.assertRaises(ValueError):
            m.run_control(m.State(CENTER), "unknown")
        for weights in ((F(1, 2), F(1, 3)), (-1, 2), (True, 0)):
            with self.assertRaises((ValueError, TypeError)):
                m.mix_residuals(weights, (CENTER, VERTICES[0]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
