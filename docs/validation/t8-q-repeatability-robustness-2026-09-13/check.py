"""Independent exact checks for conditional finite repeatability robustness.

Full local C and composite-compatible C0 are distinct domains. Rational pair
algebra, linear certificates and exact spectra check the specified witnesses;
finite protocols do not prove uniform all-domain bounds by sampling. No CP,
diamond norm, arbitrary ancilla, infinite horizon or physical availability is
assumed. Complete nominal records, not model-provenance tags, label leaves.
"""

import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F
from math import isqrt

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


def sqrt_exact(value):
    value = F(value)
    if value < 0:
        raise ValueError("An exact nonnegative square is required")
    numerator, denominator = isqrt(value.numerator), isqrt(value.denominator)
    if numerator**2 != value.numerator or denominator**2 != value.denominator:
        raise ValueError("This bounded certificate needs a rational square root")
    return F(numerator, denominator)


X = matrix(((0, 1), (1, 0)))
Y = matrix(((0, (0, -1)), ((0, 1), 0)))
Z = matrix(((1, 0), (0, -1)))
PAULI = {"X": X, "Y": Y, "Z": Z}
OUTCOMES = tuple((axis, outcome) for axis in PAULI for outcome in (0, 1))


def projector(axis, outcome):
    return scale(F(1, 2), add(eye(2), scale(1 if outcome == 0 else -1, PAULI[axis])))


def candidate(a, c=0):
    f, b = scale(c, Z), mm(mm(Z, a), Z)
    adjoint = dagger(f)
    return tuple(tuple(a[i]) + tuple(f[i]) for i in range(2)) + tuple(
        tuple(adjoint[i]) + tuple(b[i]) for i in range(2)
    )


def section(rho):
    return candidate(scale(F(1, 2), transpose(rho)))


def phi(operator):
    return scale(2, transpose(matrix(row[:2] for row in operator[:2])))


def effect(operator, axis, outcome):
    return trace(mm(phi(operator), projector(axis, outcome)))[0]


def raw_mass(operator):
    return total(entry for row in operator for entry in row)[0]


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
CENTER = section(scale(F(1, 2), eye(2)))
COMPLEX_A = matrix(((F(3, 10), (0, F(1, 20))), ((0, F(-1, 20)), F(1, 5))))
COMPLEX_C = m.G(F(3, 100), F(1, 25))
COMPLEX_D = candidate(COMPLEX_A, COMPLEX_C)
TILT_RHO = matrix(((F(16, 25), F(12, 25)), (F(12, 25), F(9, 25))))
TILT = section(TILT_RHO)
EPSILON = F(1, 100)


def raw_trace_norm_exact(operator):
    """Full signed D(Delta A,Delta c) spectrum: eigen(A) +/- |c|.

    Only rational-spectrum witnesses are passed here. Refuse irrational roots
    rather than silently round or substitute a quotient metric.
    """
    a, b, x, y, c, d = coordinates(operator)
    gap = sqrt_exact((a - b) ** 2 + 4 * (x * x + y * y))
    radius = sqrt_exact(c * c + d * d)
    eigenvalues = ((a + b + gap) / 2, (a + b - gap) / 2)
    return sum((abs(value + radius) + abs(value - radius) for value in eigenvalues), F(0))


def raw_distance_squared_to_ray(operator, axis, outcome):
    delta = add(operator, scale(-1, section(projector(axis, outcome))))
    a, b, x, y, c, d = coordinates(delta)
    if a + b != 0:
        raise ValueError("The compared source must be normalized")
    return 4 * max((a - b) ** 2 + 4 * (x * x + y * y), 4 * (c * c + d * d))


def instrument(axis, domain, epsilon=EPSILON, *, ideal=False, setting_id="shared-device"):
    if ideal:
        return m.ideal_instrument(axis, domain, setting_id=setting_id)
    targets = []
    for outcome in (0, 1):
        rho = add(
            scale(1 - epsilon, projector(axis, outcome)),
            scale(epsilon, projector(axis, 1 - outcome)),
        )
        c = m.G(0) if domain == m.COMPOSITE_C0 else m.G(3 * epsilon / 10, 2 * epsilon / 5)
        targets.append(candidate(scale(F(1, 2), transpose(rho)), c))
    return m.Instrument(
        axis, epsilon, tuple(targets), domain, "approximate target model", setting_id
    )


def run_policy(state, maximum, *, ideal, early_stop=False):
    """A bounded known-record policy, returning full positive leaf records."""
    if type(maximum) is not int or maximum < 0:
        raise ValueError("A finite nonnegative commitment bound is required")
    initial_count = len(state.records)
    leaves = {}

    def visit(current, probability):
        depth = len(current.records) - initial_count
        if depth == maximum or (early_stop and depth == 1 and current.records[-1].outcome == 0):
            leaves[current.records] = (probability, current)
            return
        first_outcome = current.records[initial_count].outcome if depth else 0
        axis = ("Z", "X", "Y", "Z")[(depth + first_outcome) % 4]
        names = () if depth == 0 else (("H",) if first_outcome == 0 else ("P", "Z"))
        controlled = m.run_word(current, names)
        device = instrument(axis, current.domain, ideal=ideal)
        for outcome in (0, 1):
            branch_probability = device.effect(controlled.residual, outcome)
            if branch_probability:
                selected_probability, output = m.commit(controlled, device, outcome)
                if selected_probability != branch_probability:
                    raise ValueError("Branch selection disagrees with its calibrated effect")
                visit(output, probability * selected_probability)

    visit(state, F(1))
    return leaves


def leaf_metrics(left, right):
    raw_error, variation = F(0), F(0)
    for record in left.keys() | right.keys():
        p, left_state = left.get(record, (F(0), None))
        q, right_state = right.get(record, (F(0), None))
        a = zeros(4) if left_state is None else scale(p, left_state.residual)
        b = zeros(4) if right_state is None else scale(q, right_state.residual)
        raw_error += raw_trace_norm_exact(add(a, scale(-1, b)))
        variation += abs(p - q) / 2
    return raw_error, variation


class RepeatabilityRobustnessChecks(unittest.TestCase):
    def test_primary_c0_and_broader_local_c_are_not_silently_identified(self):
        self.assertEqual(m.domain_kernel(COMPLEX_D, m.LOCAL_ONLY, normalized=True), COMPLEX_D)
        with self.assertRaises(ValueError):
            m.domain_kernel(COMPLEX_D, m.COMPOSITE_C0)
        self.assertEqual(m.domain_kernel(CENTER, m.COMPOSITE_C0, normalized=True), CENTER)
        self.assertEqual(rank(tuple(flatten(d) for d in SPAN[:4])), 4)
        self.assertEqual(rank(tuple(flatten(d) for d in SPAN)), 6)

    def test_c0_rank_one_effect_families_have_constant_weight_for_all_real_parameters(self):
        for axis, outcome in OUTCOMES:
            q, opposite = projector(axis, outcome), projector(axis, 1 - outcome)
            for other_axis, off_diagonal in PAULI.items():
                if other_axis == axis:
                    continue
                for t in (F(-3), F(-1, 2), F(0), F(2, 3)):
                    rho = add(add(q, scale(t, off_diagonal)), scale(t * t, opposite))
                    self.assertTrue(m.is_psd(rho))
                    source = section(rho)
                    self.assertEqual(effect(source, axis, outcome), 1)
                    device = instrument(axis, m.COMPOSITE_C0)
                    self.assertEqual(device.branch(source, outcome), device.targets[outcome])
        # Positivity and constant mass on this unbounded family force the two
        # off-diagonal images to vanish; the general cone argument is in the note.

    def test_zero_effect_and_mass_faithfulness_force_full_zero_branch(self):
        for domain in m.DOMAINS:
            for axis, outcome in OUTCOMES:
                device = instrument(axis, domain)
                source = section(projector(axis, 1 - outcome))
                self.assertEqual(device.effect(source, outcome), 0)
                self.assertEqual(device.branch(source, outcome), zeros(4))
                self.assertEqual(device.branch(zeros(4), outcome), zeros(4))
        for c in (1, m.I):
            with self.assertRaises(ValueError):
                m.candidate_from(zeros(2), c)

    def test_c0_factorization_is_fixed_by_sixteen_independent_linear_coefficients(self):
        for axis, outcome in OUTCOMES:
            others = tuple(pauli for name, pauli in PAULI.items() if name != axis)
            basis = tuple(
                section(rho)
                for rho in (projector(axis, outcome), projector(axis, 1 - outcome), *others)
            )
            source_rows = tuple(coordinates(d)[:4] for d in basis)
            self.assertEqual(rank(source_rows), 4)
            constraints = []
            for row in source_rows:
                for output_index in range(4):
                    constraints.append(
                        tuple(row[i % 4] if i // 4 == output_index else F(0) for i in range(16))
                    )
            self.assertEqual(rank(constraints), 16)
            device = instrument(axis, m.COMPOSITE_C0)
            self.assertEqual(device.branch_on_span(basis[0], outcome), device.targets[outcome])
            self.assertEqual(
                tuple(device.branch_on_span(d, outcome) for d in basis[1:]), (zeros(4),) * 3
            )
        # No Kraus representation was used: after the positive rank-one-effect
        # argument, these full-Hermitian-span equations determine the map.

    def test_c0_branch_linearity_and_rank_one_range_hold_on_signed_span(self):
        for axis, outcome in OUTCOMES:
            device = instrument(axis, m.COMPOSITE_C0)
            images = tuple(device.branch_on_span(d, outcome) for d in SPAN[:4])
            self.assertEqual(rank(tuple(flatten(d) for d in images)), 1)
            signed = from_coordinates((2, -3, F(1, 4), F(-2, 5), 0, 0))
            expected = zeros(4)
            for coefficient, output in zip(coordinates(signed)[:4], images, strict=True):
                expected = add(expected, scale(coefficient, output))
            self.assertEqual(device.branch_on_span(signed, outcome), expected)

    def test_uniform_defect_for_the_chosen_ray_maps_is_an_exact_linear_identity(self):
        for domain in m.DOMAINS:
            basis = SPAN if domain == m.LOCAL_ONLY else SPAN[:4]
            for axis, outcome in OUTCOMES:
                device = instrument(axis, domain)
                self.assertEqual(1 - effect(device.targets[outcome], axis, outcome), EPSILON)
                for d in basis:
                    output = device.branch_on_span(d, outcome)
                    self.assertEqual(
                        effect(output, axis, 1 - outcome), EPSILON * effect(d, axis, outcome)
                    )
        # Equality on a real basis establishes this implementation's uniform
        # identity by linearity, not by testing finitely many preparations.

    def test_target_validation_checks_defect_range_and_same_domain(self):
        bad = (section(projector("Z", 1)), section(projector("Z", 0)))
        with self.assertRaises(ValueError):
            m.Instrument("Z", F(1, 5), bad)
        full_targets = instrument("Z", m.LOCAL_ONLY).targets
        with self.assertRaises(ValueError):
            m.Instrument("Z", EPSILON, full_targets, m.COMPOSITE_C0)
        for epsilon in (F(-1, 10), F(3, 5), True, 0.1):
            with self.assertRaises((ValueError, TypeError)):
                m.Instrument("Z", epsilon, (section(projector("Z", 0)), section(projector("Z", 1))))

    def test_pure_tilt_attains_the_exact_six_fifths_raw_distance_bound(self):
        self.assertTrue(m.is_psd(TILT_RHO))
        self.assertEqual(
            times(TILT_RHO[0][0], TILT_RHO[1][1]), times(TILT_RHO[0][1], TILT_RHO[1][0])
        )
        self.assertEqual(effect(TILT, "Z", 1), F(9, 25))
        delta = add(TILT, scale(-1, section(projector("Z", 0))))
        self.assertEqual(raw_trace_norm_exact(delta), F(6, 5))
        self.assertEqual(raw_distance_squared_to_ray(TILT, "Z", 0), F(36, 25))
        self.assertEqual(m.quotient_trace_distance_squared_to_ray(TILT, "Z", 0), F(9, 25))
        self.assertEqual(m.quotient_trace_norm_squared_to_ray(TILT, "Z", 0), F(36, 25))

    def test_complex_coherent_tilt_has_the_same_exact_sharp_distance(self):
        rho = matrix(((F(16, 25), (0, F(12, 25))), ((0, F(-12, 25)), F(9, 25))))
        source = section(rho)
        self.assertTrue(m.is_psd(rho))
        self.assertEqual(effect(source, "Z", 1), F(9, 25))
        self.assertEqual(
            raw_trace_norm_exact(add(source, scale(-1, section(projector("Z", 0))))), F(6, 5)
        )

    def test_maximum_output_c_bound_is_separately_sharp_at_epsilon_one_fifth(self):
        epsilon = F(1, 5)
        a = matrix(((F(2, 5), 0), (0, F(1, 10))))
        for c in (F(1, 10), m.G(0, F(1, 10)), m.G(F(3, 50), F(2, 25))):
            source = candidate(a, c)
            self.assertEqual(m.domain_kernel(source, m.LOCAL_ONLY, normalized=True), source)
            self.assertEqual(sqrt_exact(pair(c)[0] ** 2 + pair(c)[1] ** 2), epsilon / 2)
            self.assertEqual(effect(source, "Z", 1), epsilon)
            self.assertEqual(
                raw_trace_norm_exact(add(source, scale(-1, section(projector("Z", 0))))), F(2, 5)
            )
        with self.assertRaises(ValueError):
            m.candidate_from(a, F(11, 100))

    def test_full_raw_ray_distance_uses_shifted_eigenvalues_and_matches_visible_bound(self):
        sources = (
            TILT,
            section(TILT_RHO),
            candidate(matrix(((F(2, 5), 0), (0, F(1, 10)))), m.G(F(3, 50), F(2, 25))),
        )
        for source in sources:
            deficit = effect(source, "Z", 1)
            distance_squared = raw_distance_squared_to_ray(source, "Z", 0)
            self.assertEqual(distance_squared, m.quotient_trace_norm_squared_to_ray(source, "Z", 0))
            self.assertLessEqual(distance_squared, 4 * deficit)
            self.assertEqual(
                raw_trace_norm_exact(add(source, scale(-1, section(projector("Z", 0))))) ** 2,
                distance_squared,
            )
        signed = candidate(scale(F(1, 10), eye(2)), F(1, 5))
        self.assertEqual(raw_trace_norm_exact(signed), F(4, 5))
        with self.assertRaises(ValueError):
            sqrt_exact(F(1, 5))

    def test_nearby_c0_reset_is_not_ideal_but_preserves_calibrated_first_effects(self):
        device = m.noisy_pauli_instrument("Z", F(1, 5))
        ideal = m.ideal_instrument("Z")
        for source in (CENTER, section(projector("Z", 0)), section(projector("Y", 0))):
            for outcome in (0, 1):
                self.assertEqual(device.effect(source, outcome), ideal.effect(source, outcome))
                self.assertEqual(
                    raw_mass(device.branch(source, outcome)), ideal.effect(source, outcome)
                )
        self.assertNotEqual(device.branch(CENTER, 0), ideal.branch(CENTER, 0))

    def test_broader_c_counter_has_same_quotient_inputs_but_different_quotient_outputs(self):
        device = m.LocalCounterInstrument()
        sources = tuple(candidate(scale(F(1, 4), eye(2)), c) for c in (F(1, 4), F(-1, 4)))
        self.assertEqual(phi(sources[0]), phi(sources[1]))
        for source, sign in zip(sources, (1, -1), strict=True):
            self.assertEqual(device.effect(source, 0), F(1, 2))
            output = device.branch(source, 0)
            a, c = m.decompose_candidate(output)
            self.assertEqual(a[0][1], sign * F(1, 10))
            self.assertEqual(c, 0)
            normalized = scale(2, output)
            self.assertEqual(phi(normalized)[0][1], sign * F(2, 5))
            self.assertEqual(effect(normalized, "X", 0), F(1, 2) + sign * F(2, 5))
        self.assertNotEqual(phi(device.branch(sources[0], 0)), phi(device.branch(sources[1], 0)))

    def test_local_counter_positivity_and_defect_identity_retain_complex_input_c(self):
        device = m.LocalCounterInstrument()
        self.assertEqual(device.k**2, device.epsilon * (1 - device.epsilon))
        for source in (CENTER, COMPLEX_D, candidate(scale(F(1, 4), eye(2)), m.G(0, F(1, 4)))):
            p = device.effect(source, 0)
            _, c = m.decompose_candidate(source)
            self.assertLessEqual(c.norm_squared(), p * p / 4)
            output = device.branch(source, 0)
            self.assertTrue(m.is_psd(output))
            self.assertEqual(effect(output, "Z", 1), device.epsilon * p)
            self.assertEqual(raw_mass(output), p)
            self.assertEqual(raw_mass(add(output, device.branch(source, 1))), raw_mass(source))
        for d in SPAN:
            self.assertEqual(
                effect(device.branch_on_span(d, 0), "Z", 1), F(1, 5) * effect(d, "Z", 0)
            )
        imaginary_source = candidate(scale(F(1, 4), eye(2)), m.G(0, F(1, 4)))
        imaginary_output = device.branch(imaginary_source, 0)
        self.assertEqual(imaginary_output[0][1], m.G(0, F(1, 10)))
        normalized = scale(2, imaginary_output)
        self.assertEqual(phi(normalized)[0][1], m.G(0, F(-2, 5)))
        self.assertEqual(effect(normalized, "Y", 0), F(9, 10))

    def test_local_counter_is_not_misrepresented_as_a_c0_instrument(self):
        with self.assertRaises(ValueError):
            m.LocalCounterInstrument(domain=m.COMPOSITE_C0)
        with self.assertRaises(ValueError):
            m.commit(m.State(m.COMPOSITE_C0, CENTER), m.LocalCounterInstrument(), 0)
        with self.assertRaises(ValueError):
            m.State(m.COMPOSITE_C0, COMPLEX_D)
        self.assertEqual(m.LocalCounterInstrument().branch(zeros(4), 0), zeros(4))

    def test_zero_horizon_keeps_full_residual_and_record_prefix_exactly(self):
        for domain, source in ((m.COMPOSITE_C0, CENTER), (m.LOCAL_ONLY, COMPLEX_D)):
            state = m.State(domain, source)
            approximate = run_policy(state, 0, ideal=False)
            ideal = run_policy(state, 0, ideal=True)
            self.assertEqual(approximate, {(): (F(1), state)})
            self.assertEqual(leaf_metrics(approximate, ideal), (0, 0))

    def test_first_committed_record_law_is_identical_even_with_nonzero_raw_error(self):
        for domain, source in ((m.COMPOSITE_C0, CENTER), (m.LOCAL_ONLY, COMPLEX_D)):
            state = m.State(domain, source)
            approximate, ideal = run_policy(state, 1, ideal=False), run_policy(state, 1, ideal=True)
            self.assertEqual(set(approximate), set(ideal))
            self.assertEqual(
                {key: value[0] for key, value in approximate.items()},
                {key: value[0] for key, value in ideal.items()},
            )
            raw_error, variation = leaf_metrics(approximate, ideal)
            self.assertGreater(raw_error, 0)
            self.assertLessEqual(raw_error, 2 * sqrt_exact(EPSILON))
            self.assertEqual(variation, 0)

    def test_second_same_axis_record_can_diverge_although_the_first_does_not(self):
        state = m.State(m.COMPOSITE_C0, section(projector("Z", 0)))
        approximate = instrument("Z", state.domain)
        ideal = instrument("Z", state.domain, ideal=True)
        p, a = m.commit(state, approximate, 0)
        q, b = m.commit(state, ideal, 0)
        self.assertEqual((p, q), (1, 1))
        self.assertEqual(a.records, b.records)
        self.assertEqual(approximate.effect(a.residual, 1), EPSILON)
        self.assertEqual(ideal.effect(b.residual, 1), 0)
        self.assertEqual(
            sum(
                abs(approximate.effect(a.residual, r) - ideal.effect(b.residual, r)) for r in (0, 1)
            )
            / 2,
            EPSILON,
        )

    def test_finite_adaptive_complete_record_policies_obey_raw_and_tv_bounds(self):
        for domain, source in ((m.COMPOSITE_C0, CENTER), (m.LOCAL_ONLY, COMPLEX_D)):
            for maximum in (1, 2, 3, 4):
                state = m.State(domain, source)
                approximate = run_policy(state, maximum, ideal=False)
                ideal = run_policy(state, maximum, ideal=True)
                self.assertEqual(sum(p for p, _ in approximate.values()), 1)
                self.assertEqual(sum(p for p, _ in ideal.values()), 1)
                raw_error, variation = leaf_metrics(approximate, ideal)
                self.assertLessEqual(raw_error, min(F(2), 2 * maximum * sqrt_exact(EPSILON)))
                self.assertLessEqual(variation, min(F(1), (maximum - 1) * sqrt_exact(EPSILON)))
                for records, (_, leaf) in approximate.items():
                    self.assertEqual(len(records), maximum)
                    self.assertEqual(leaf.records, records)
                    self.assertEqual(m.mass(leaf.residual), 1)

    def test_early_stopping_preserves_variable_length_records_and_complete_mass(self):
        for domain, source in ((m.COMPOSITE_C0, CENTER), (m.LOCAL_ONLY, COMPLEX_D)):
            state = m.State(domain, source)
            approximate = run_policy(state, 4, ideal=False, early_stop=True)
            ideal = run_policy(state, 4, ideal=True, early_stop=True)
            self.assertEqual({len(records) for records in approximate}, {1, 4})
            self.assertEqual(sum(p for p, _ in approximate.values()), 1)
            self.assertEqual(sum(p for p, _ in ideal.values()), 1)
            raw_error, variation = leaf_metrics(approximate, ideal)
            self.assertLessEqual(raw_error, F(4, 5))
            self.assertLessEqual(variation, F(3, 10))

    def test_finite_policy_preserves_prior_prefix_full_words_and_precursors(self):
        domain = m.LOCAL_ONLY
        prior = m.Record(0, "Y", 1, ("P",), (), domain, setting_id="earlier-device")
        state = m.State(domain, COMPLEX_D, (prior,))
        leaves = run_policy(state, 3, ideal=False)
        for records, (_, leaf) in leaves.items():
            self.assertEqual(records[0], prior)
            self.assertEqual(len(records), 4)
            for i, record in enumerate(records):
                self.assertEqual(record.event_id, i)
                self.assertEqual(record.precursor, tuple(range(i)))
                self.assertEqual(record.domain, domain)
            self.assertEqual(records[1].settings, ())
            self.assertEqual(records[2].settings, ("H",) if records[1].outcome == 0 else ("P", "Z"))
            self.assertEqual(leaf.settings, ())
        self.assertEqual(state.records, (prior,))

    def test_controls_are_applied_once_in_the_fixed_frame_and_pending_word_resets(self):
        domain = m.COMPOSITE_C0
        initial = m.State(domain, section(projector("X", 0)))
        controlled = m.run_control(initial, "P")
        self.assertEqual(phi(controlled.residual), projector("Y", 1))
        device = instrument("Y", domain)
        probability, first = m.commit(controlled, device, 1)
        self.assertEqual(probability, 1)
        again_probability, second = m.commit(first, device, 1)
        self.assertEqual(again_probability, 1 - EPSILON)
        self.assertEqual(first.records[-1].settings, ("P",))
        self.assertEqual(second.records[-1].settings, ())
        self.assertEqual(first.residual, second.residual)

    def test_model_provenance_is_not_an_extra_record_label_but_nominal_setting_is(self):
        domain = m.COMPOSITE_C0
        source = m.State(domain, CENTER)
        approximate = instrument("Z", domain)
        ideal = instrument("Z", domain, ideal=True)
        self.assertNotEqual(approximate.provenance, ideal.provenance)
        _, a = m.commit(source, approximate, 0)
        _, b = m.commit(source, ideal, 0)
        self.assertEqual(a.records, b.records)
        self.assertNotEqual(a.residual, b.residual)
        for name in ("provenance", "epsilon", "targets"):
            self.assertNotIn(name, m.Record.__dataclass_fields__)
        _, changed = m.commit(source, replace(approximate, setting_id="different-device"), 0)
        self.assertNotEqual(changed.records, a.records)

    def test_sharp_second_read_total_variation_is_twelve_twenty_fifths(self):
        domain = m.COMPOSITE_C0
        source = m.State(domain, section(projector("Z", 0)))
        approximate = m.Instrument(
            "Z",
            F(9, 25),
            (TILT, section(projector("Z", 1))),
            domain,
            "coherent tilt",
            "shared-device",
        )
        ideal = instrument("Z", domain, ideal=True)
        p, a = m.commit(source, approximate, 0)
        q, b = m.commit(source, ideal, 0)
        self.assertEqual((p, q), (1, 1))
        self.assertEqual(a.records, b.records)
        reader = instrument("X", domain, ideal=True)
        approximate_law = tuple(reader.effect(a.residual, r) for r in (0, 1))
        ideal_law = tuple(reader.effect(b.residual, r) for r in (0, 1))
        self.assertEqual(approximate_law, (F(49, 50), F(1, 50)))
        self.assertEqual(ideal_law, (F(1, 2), F(1, 2)))
        variation = sum(abs(p - q) for p, q in zip(approximate_law, ideal_law, strict=True)) / 2
        self.assertEqual(variation, F(12, 25))
        self.assertEqual(variation**2, F(9, 25) * F(16, 25))
        approximate_leaves, ideal_leaves = {}, {}
        for outcome in (0, 1):
            pa, after_a = m.commit(a, reader, outcome)
            pb, after_b = m.commit(b, reader, outcome)
            approximate_leaves[after_a.records] = (pa, after_a)
            ideal_leaves[after_b.records] = (pb, after_b)
        raw_error, recorded_variation = leaf_metrics(approximate_leaves, ideal_leaves)
        self.assertEqual(raw_error, F(24, 25))
        self.assertEqual(recorded_variation, variation)
        self.assertLessEqual(raw_error, min(F(2), 4 * F(3, 5)))
        self.assertLessEqual(recorded_variation, min(F(1), F(3, 5)))

    def test_zero_branch_guard_does_not_append_or_modify_full_source(self):
        domain = m.LOCAL_ONLY
        source = m.run_control(m.State(domain, section(projector("X", 0))), "P")
        device = instrument("Y", domain)
        with self.assertRaises(ValueError):
            m.commit(source, device, 0)
        self.assertEqual(source.settings, ("P",))
        self.assertEqual(source.records, ())
        self.assertEqual(phi(source.residual), projector("Y", 1))

    def test_declared_domains_and_unavailable_frames_are_enforced(self):
        with self.assertRaises(ValueError):
            m.commit(m.State(m.COMPOSITE_C0, CENTER), instrument("Z", m.LOCAL_ONLY), 0)
        with self.assertRaises(ValueError):
            m.State(m.LOCAL_ONLY, CENTER, frame="moving")
        with self.assertRaises(ValueError):
            m.run_control(m.State(m.LOCAL_ONLY, CENTER), "unregistered")
        with self.assertRaises(TypeError):
            m.commit(CENTER, instrument("Z", m.LOCAL_ONLY), 0)

    def test_one_shot_source_rows_targets_and_actual_words_are_consumed_once(self):
        for domain, source in ((m.COMPOSITE_C0, CENTER), (m.LOCAL_ONLY, COMPLEX_D)):
            device = instrument("Y", domain)
            copied = m.Instrument("Y", EPSILON, (target for target in device.targets), domain)
            self.assertEqual(copied.targets, device.targets)
            self.assertEqual(
                m.domain_span(((entry for entry in row) for row in source), domain), source
            )
            self.assertEqual(
                m.domain_kernel(((entry for entry in row) for row in source), domain), source
            )
            for outcome in (0, 1):
                self.assertEqual(
                    device.effect(((entry for entry in row) for row in source), outcome),
                    device.effect(source, outcome),
                )
                self.assertEqual(
                    device.branch(((entry for entry in row) for row in source), outcome),
                    device.branch(source, outcome),
                )
            state = m.run_word(m.State(domain, source), (name for name in ("H", "P")))
            self.assertEqual(state.settings, ("H", "P"))
        counter = m.LocalCounterInstrument()
        for outcome in (0, 1):
            self.assertEqual(
                counter.effect(((entry for entry in row) for row in COMPLEX_D), outcome),
                counter.effect(COMPLEX_D, outcome),
            )
            self.assertEqual(
                counter.branch(((entry for entry in row) for row in COMPLEX_D), outcome),
                counter.branch(COMPLEX_D, outcome),
            )

    def test_record_constructor_checks_grammar_not_unstated_global_reachability(self):
        domain = m.LOCAL_ONLY
        record = m.Record(0, "Z", 0, (), (), domain)
        state = m.State(domain, COMPLEX_D, (record,), ("H",))
        self.assertEqual(state.residual, COMPLEX_D)
        self.assertEqual(state.settings, ("H",))
        with self.assertRaises(FrozenInstanceError):
            record.outcome = 1
        with self.assertRaises(ValueError):
            m.Record(1, "Z", 0, (), (), domain)
        with self.assertRaises(ValueError):
            m.State(m.COMPOSITE_C0, CENTER, (record,))

    def test_finite_policy_bounds_do_not_accept_negative_or_infinite_horizons(self):
        state = m.State(m.COMPOSITE_C0, CENTER)
        for maximum in (-1, F(1, 2), True, float("inf")):
            with self.assertRaises(ValueError):
                run_policy(state, maximum, ideal=False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
