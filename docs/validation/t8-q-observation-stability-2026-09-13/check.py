"""Independent exact stability and candidate-feasibility certificates.

All error budgets are deterministic mathematical assumptions, not confidence
levels or observed frequencies. A failed supplied candidate is inconclusive.
Rational square certificates avoid treating floating-point approximations as
proofs. Raw audit payloads and known histories are never inferred from errors.
"""

import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F
from itertools import product
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


X = matrix(((0, 1), (1, 0)))
Y = matrix(((0, (0, -1)), ((0, 1), 0)))
Z = matrix(((1, 0), (0, -1)))
QP, QM = matrix(((1, 0), (0, 0))), matrix(((0, 0), (0, 1)))
CENTER = scale(F(1, 2), eye(2))
H0 = matrix(((1, 1), (1, -1)))
CNOT = matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)))
U0 = mm(tensor(eye(2), H0), CNOT)
T = F(3, 5)
CELLS = tuple(product((0, 1), repeat=2))
BITS = tuple(product((0, 1), repeat=4))
OUTCOMES = tuple((a, b, sign) for a, b in CELLS for sign in ("+", "-"))
WORDS = ((), ("A",), ("A", "A"))
V = (
    (F(3, 5), F(0), F(4, 5)),
    (F(3, 5), F(96, 125), F(-28, 125)),
    (F(3, 5), F(-1344, 3125), F(-2108, 3125)),
)
B = (
    (F(125, 192), F(70, 192), F(125, 192)),
    (F(-55, 192), F(180, 192), F(-125, 192)),
    (F(195, 256), F(-70, 256), F(-125, 256)),
)
B_SQUARED = tuple(sum(B[i][j] * B[i][j] for i in range(3)) for j in range(3))
ROOT_UPPER = (F(640313, 100000), F(1000703, 12500))
COEFFICIENT_UPPER = (125 * ROOT_UPPER[0] / 768, 5 * ROOT_UPPER[1] / 384, 125 * ROOT_UPPER[0] / 768)


def sigma(q, x=0, y=0, z=0):
    return scale(F(1, 2), add(scale(q, eye(2)), scale(x, X), scale(y, Y), scale(z, Z)))


def coords(operator):
    return (
        trace(operator)[0],
        trace(mm(X, operator))[0],
        trace(mm(Y, operator))[0],
        trace(mm(Z, operator))[0],
    )


SIGMAS = (
    sigma(F(3, 10), F(1, 10), F(1, 10), F(1, 10)),
    sigma(F(1, 5), F(-1, 10), 0, F(1, 10)),
    sigma(F(2, 5), F(1, 10), F(-1, 5), F(1, 5)),
    sigma(F(1, 10), 0, 0, F(1, 10)),
)
CENTERS = (sigma(F(1, 4)),) * 4


def inv_filter(cell):
    return matrix(((F(1, 2), 0), (0, 1))) if cell[1] == 0 else matrix(((1, 0), (0, F(1, 2))))


def rhos_from_filtered(sigmas):
    return tuple(
        scale(10, mm(mm(inv_filter(cell), s), inv_filter(cell)))
        for cell, s in zip(CELLS, sigmas, strict=True)
    )


def retwist(operator):
    result = [[ZERO for _ in range(16)] for _ in range(16)]
    for a, i, b, j in BITS:
        for c, k, d, ell in BITS:
            result[8 * a + 4 * i + 2 * b + j][8 * c + 4 * k + 2 * d + ell] = times(
                (-1) ** (a * i + b * j + c * k + d * ell),
                operator[8 * a + 4 * b + 2 * i + j][8 * c + 4 * d + 2 * k + ell],
            )
    return matrix(result)


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


def raw(sigmas):
    return image(rhos_from_filtered(sigmas))


def mass(operator):
    return total(entry for row in operator for entry in row)[0]


def values(sigmas, axis):
    result = []
    for s in sigmas:
        q, x, y, z = coords(s)
        difference = sum(a * b for a, b in zip(axis, (x, y, z), strict=True))
        result.extend(((q + difference) / 2, (q - difference) / 2))
    return tuple(result)


def tables(sigmas):
    return tuple(
        m.ProbabilityTable(word, tuple(zip(OUTCOMES, values(sigmas, axis), strict=True)))
        for word, axis in zip(WORDS, V, strict=True)
    )


def tv(left, right):
    return sum(abs(a - b) for a, b in zip(left, right, strict=True)) / 2


def errors(left, right):
    return tuple(tv(values(left, axis), values(right, axis)) for axis in V)


def differences(left, right):
    return tuple(
        tuple(a - b for a, b in zip(coords(s), coords(t), strict=True))
        for s, t in zip(left, right, strict=True)
    )


def radical_interval(value, denominator=10**12):
    lower_integer = isqrt(value.numerator * denominator * denominator // value.denominator)
    lower = F(lower_integer, denominator)
    upper = lower if lower * lower == value else lower + F(1, denominator)
    if not lower * lower <= value <= upper * upper:
        raise ArithmeticError("Invalid exact rational square certificate")
    return lower, upper


def filtered_interval(left, right):
    lower, upper = F(0), F(0)
    for dq, dx, dy, dz in differences(left, right):
        lo, hi = radical_interval(dx * dx + dy * dy + dz * dz)
        lower += max(abs(dq), lo) / 2
        upper += max(abs(dq), hi) / 2
    return lower, upper


def raw_interval(left_rhos, right_rhos):
    lower, upper = F(0), F(0)
    for left, right in zip(left_rhos, right_rhos, strict=True):
        q, x, y, z = coords(add(left, scale(-1, right)))
        lo, hi = radical_interval(x * x + y * y + z * z)
        lower += max(abs(q), lo) / 8
        upper += max(abs(q), hi) / 8
    return lower, upper


def local_from(rho):
    a = scale(F(1, 2), transpose(rho))
    b = mm(mm(Z, a), Z)
    return tuple(tuple(a[i]) + (m.G(), m.G()) for i in range(2)) + tuple(
        (m.G(), m.G()) + tuple(b[i]) for i in range(2)
    )


def snapshot(sigmas=SIGMAS):
    local_records = (m.InputRecord(0, "prepare", "L", ("H", "P_inv"), (("sample", "local"),)),)
    reference_records = (m.InputRecord(0, "prepare", "R", ("Z",), (("sample", "reference"),)),)
    context = m.Context(
        m.LocalInput(local_from(CENTER), "beam", local_records),
        m.ReferenceInput(T, "probe", reference_records),
        m.Independence(("beam", "probe")),
        m.TerminalReadPremise(setting_id="read-A"),
        joint_origin="joint-run",
        setting_id="cut-A",
    )
    return m.State(m.INTERIOR_DOMAIN, context, raw(sigmas))


class ObservationStabilityChecks(unittest.TestCase):
    def test_inverse_and_column_norm_constants_have_exact_square_certificates(self):
        for i in range(3):
            for j in range(3):
                self.assertEqual(sum(B[i][k] * V[k][j] for k in range(3)), int(i == j))
        self.assertEqual(B_SQUARED[0], F(125 * 125 * 41, 768 * 768))
        self.assertEqual(B_SQUARED[2], B_SQUARED[0])
        self.assertEqual(B_SQUARED[1], F(25 * 6409, 384 * 384))
        self.assertEqual(ROOT_UPPER[0] ** 2 - 41, F(737969, 10**10))
        self.assertEqual(ROOT_UPPER[1] ** 2 - 6409, F(244209, 156250000))
        self.assertEqual(m.B_UPPER, COEFFICIENT_UPPER)
        self.assertEqual(m.coefficient_upper_bounds(), COEFFICIENT_UPPER)
        self.assertEqual(m.B_NORM_SQUARED, B_SQUARED)
        for squared, upper in zip(B_SQUARED, COEFFICIENT_UPPER, strict=True):
            self.assertGreater(upper, 0)
            self.assertGreater(upper * upper, squared)

    def test_full_native_difference_data_retains_q_and_squared_bloch_radius(self):
        first, second = raw(SIGMAS), raw(CENTERS)
        expected = tuple(
            (abs(dq), dx * dx + dy * dy + dz * dz)
            for dq, dx, dy, dz in differences(SIGMAS, CENTERS)
        )
        self.assertEqual(m.filtered_difference_data(first, second), expected)
        self.assertEqual(m.from_filtered_coordinates(SIGMAS, T), first)
        self.assertEqual(m.inverse_span(first, T), rhos_from_filtered(SIGMAS))
        self.assertEqual(mass(first), 1)
        self.assertTrue(any(entry.imag for row in first for entry in row))

    def test_binary_pair_tv_uses_maximum_not_sum_of_q_and_internal_differences(self):
        for dq, dd in ((F(2), F(1)), (F(-2), F(1)), (F(1), F(3)), (F(-1), F(-3)), (F(0), F(2))):
            pair_l1 = abs((dq + dd) / 2) + abs((dq - dd) / 2)
            self.assertEqual(pair_l1, max(abs(dq), abs(dd)))
        for axis in V:
            expected = (
                sum(
                    max(abs(dq), abs(sum(a * b for a, b in zip(axis, (dx, dy, dz), strict=True))))
                    for dq, dx, dy, dz in differences(SIGMAS, CENTERS)
                )
                / 2
            )
            self.assertEqual(tv(values(SIGMAS, axis), values(CENTERS, axis)), expected)

    def test_cell_trace_norm_formula_has_exact_rational_eigenvalue_witnesses(self):
        for dq, dr in (
            (F(3), (F(1), F(2), F(2))),
            (F(-4), (F(3), F(0), F(0))),
            (F(1), (F(0), F(0), F(2))),
            (F(0), (F(3, 5), F(4, 5), F(0))),
        ):
            squared = sum(value * value for value in dr)
            lo, hi = radical_interval(squared)
            self.assertEqual(lo, hi)
            eigenvalues = ((dq + lo) / 2, (dq - lo) / 2)
            self.assertEqual(sum(abs(value) for value in eigenvalues), max(abs(dq), lo))
            operator = sigma(dq, *dr)
            self.assertEqual(trace(operator)[0], dq)
            self.assertEqual(trace(mm(operator, operator))[0], (dq * dq + squared) / 2)

    def test_stability_inequalities_are_checked_with_rational_radical_intervals(self):
        first = SIGMAS
        for second in (
            CENTERS,
            tuple(scale(F(1, 2), add(s, t)) for s, t in zip(SIGMAS, CENTERS, strict=True)),
        ):
            eps = errors(first, second)
            lower, upper = filtered_interval(first, second)
            self.assertLessEqual(max(eps), lower)
            certified = sum(b * error for b, error in zip(COEFFICIENT_UPPER, eps, strict=True))
            self.assertLessEqual(upper, certified)
            self.assertLessEqual(certified, sum(COEFFICIENT_UPPER) * max(eps))
            self.assertEqual(
                m.filtered_difference_data(raw(first), raw(second)),
                tuple(
                    (abs(dq), dx * dx + dy * dy + dz * dz)
                    for dq, dx, dy, dz in differences(first, second)
                ),
            )
        transfer = F(1, 10)
        shifted = (sigma(F(1, 4) + transfer), sigma(F(1, 4) - transfer), *CENTERS[2:])
        self.assertEqual(errors(shifted, CENTERS), (transfer,) * 3)
        self.assertEqual(filtered_interval(shifted, CENTERS), (transfer, transfer))

    def test_three_separate_cells_saturate_the_sharp_symbolic_column_norm_sum(self):
        epsilon = F(1, 100)
        left, right = [], []
        for column in range(3):
            direction = tuple(epsilon * B[row][column] for row in range(3))
            left.append(sigma(F(1, 4), *direction))
            right.append(sigma(F(1, 4), *(-value for value in direction)))
        left.append(sigma(F(1, 4)))
        right.append(sigma(F(1, 4)))
        self.assertTrue(all(m.is_psd(s) for s in (*left, *right)))
        self.assertEqual(errors(left, right), (epsilon,) * 3)
        data = m.filtered_difference_data(raw(left), raw(right))
        for k in range(3):
            self.assertEqual(data[k], (F(0), 4 * epsilon * epsilon * B_SQUARED[k]))
        self.assertEqual(data[3], (F(0), F(0)))
        # Each cell contributes epsilon*sqrt(B_SQUARED[k]) to d_F exactly;
        # hence d_F=epsilon*(b0+b1+b2), the sharp symbolic equality.
        self.assertEqual(mass(raw(left)), 1)
        self.assertEqual(mass(raw(right)), 1)

    def test_one_column_sharpness_has_only_its_own_setting_error(self):
        epsilon = F(1, 100)
        for column in range(3):
            direction = tuple(epsilon * B[row][column] for row in range(3))
            left = (sigma(F(1, 4), *direction),) + CENTERS[1:]
            right = (sigma(F(1, 4), *(-value for value in direction)),) + CENTERS[1:]
            self.assertEqual(
                errors(left, right), tuple(epsilon if k == column else F(0) for k in range(3))
            )
            self.assertEqual(
                m.filtered_difference_data(raw(left), raw(right))[0],
                (F(0), 4 * epsilon * epsilon * B_SQUARED[column]),
            )

    def test_native_filter_comparison_has_both_sharp_extreme_ray_ratios(self):
        for projector, ratio in ((QP, F(5, 8)), (QM, F(5, 2))):
            weight = F(1, 4)
            first = (scale(weight, projector), scale(1 - weight, CENTER), zeros(2), zeros(2))
            second = (zeros(2), scale(1 - weight, CENTER), scale(weight, projector), zeros(2))
            filtered = filtered_interval(first, second)
            native = raw_interval(rhos_from_filtered(first), rhos_from_filtered(second))
            self.assertEqual(filtered, (weight, weight))
            self.assertEqual(native, (ratio * weight, ratio * weight))
            self.assertTrue(m.is_psd(raw(first)) and m.is_psd(raw(second)))
            self.assertEqual((mass(raw(first)), mass(raw(second))), (F(1), F(1)))
        self.assertEqual(F(5, 8), 1 / (1 + T))
        self.assertEqual(F(5, 2), 1 / (1 - T))

    def test_bounded_native_endpoint_family_has_vanishing_full_read_errors(self):
        for t in (F(0), F(1, 2), T, F(9, 10), F(99, 100), F(1)):
            small = (1 - t) / 4
            fill = (3 + t) / (1 + t)
            first_rhos = (QM, scale(fill, QM), zeros(2), zeros(2))
            second_rhos = (zeros(2), scale(fill, QM), QM, zeros(2))
            first, second = image(first_rhos, t), image(second_rhos, t)
            self.assertTrue(m.is_psd(first) and m.is_psd(second))
            self.assertEqual((mass(first), mass(second)), (F(1), F(1)))
            self.assertEqual(raw_interval(first_rhos, second_rhos), (F(1, 4), F(1, 4)))
            self.assertLessEqual(trace(first)[0], 1)
            sigmas_first = (scale(small, QM), scale(1 - small, QM), zeros(2), zeros(2))
            sigmas_second = (zeros(2), scale(1 - small, QM), scale(small, QM), zeros(2))
            self.assertEqual(errors(sigmas_first, sigmas_second), (small,) * 3)
            if t == 1:
                self.assertNotEqual(first, second)
                self.assertEqual(errors(sigmas_first, sigmas_second), (F(0),) * 3)
                with self.assertRaises(ValueError):
                    m.terminal_weights(first, t)
        # Fixed-t endpoint diagnostics are not a primary inverse-filter extension.

    def test_rare_cell_conditioning_can_hide_unit_internal_distance_in_small_full_laws(self):
        for q in (F(1, 10), F(1, 100), F(1, 1000)):
            left = (scale(q, sigma(1, 1)), scale(1 - q, CENTER), zeros(2), zeros(2))
            right = (scale(q, sigma(1, -1)), scale(1 - q, CENTER), zeros(2), zeros(2))
            self.assertEqual(errors(left, right), (3 * q / 5,) * 3)
            self.assertEqual(filtered_interval(left, right), (q, q))
            conditional = filtered_interval((scale(1 / q, left[0]),), (scale(1 / q, right[0]),))
            self.assertEqual(conditional, (F(1), F(1)))
        # A lower bound on q is needed for conditional-state stability; no
        # division or fabricated conditional state is made at q=0.

    def test_rational_near_blind_axes_have_no_uniform_observability_constant(self):
        x_pair = (
            (sigma(1, 1), zeros(2), zeros(2), zeros(2)),
            (sigma(1, -1), zeros(2), zeros(2), zeros(2)),
        )
        y_pair = (
            (sigma(1, 0, 1), zeros(2), zeros(2), zeros(2)),
            (sigma(1, 0, -1), zeros(2), zeros(2), zeros(2)),
        )
        for n in (5, 10, 100):
            small, large = F(2 * n, n * n + 1), F(n * n - 1, n * n + 1)
            self.assertEqual(small * small + large * large, 1)
            for axis, pair_states, bound in (
                ((small, F(0), large), x_pair, small),
                ((large, F(0), small), y_pair, small),
            ):
                axes = [axis]
                for _ in range(2):
                    x, y, z = axes[-1]
                    axes.append((x, F(-7, 25) * y + F(24, 25) * z, F(-24, 25) * y + F(-7, 25) * z))
                eps = tuple(
                    tv(values(pair_states[0], direction), values(pair_states[1], direction))
                    for direction in axes
                )
                self.assertLessEqual(max(eps), bound)
                self.assertEqual(filtered_interval(*pair_states), (F(1), F(1)))
            self.assertEqual(
                tuple(tv(values(x_pair[0], axis), values(x_pair[1], axis)) for axis in axes),
                (large,) * 3,
            )
        # These are exact rational diagnostics for the written near-blind
        # formula, not extra primary reads or an enumeration proof of a limit.

    def test_exact_positive_candidate_certifies_nonempty_zero_diameter_set(self):
        source = raw(SIGMAS)
        observed = tables(SIGMAS)
        witness = m.candidate_witness(source, observed, m.ErrorBudget((0, 0, 0)))
        self.assertIsInstance(witness, m.FeasibleWitness)
        self.assertIs(witness.feasible_nonempty, True)
        self.assertEqual(witness.kernel, source)
        self.assertEqual(witness.candidate, source)
        self.assertEqual(witness.predicted_tables, observed)
        self.assertEqual(witness.actual_tv, (F(0),) * 3)
        self.assertEqual(witness.filtered_diameter_upper, 0)
        self.assertEqual(witness.native_diameter_upper, 0)
        self.assertEqual(m.reconstruct_kernel(observed, T), source)
        self.assertIsNone(witness.data.metadata)

    def test_unknown_paired_calibration_can_hide_a_unit_state_frame_difference(self):
        left = (QP, zeros(2), zeros(2), zeros(2))
        right = (QM, zeros(2), zeros(2), zeros(2))
        self.assertEqual(mm(mm(X, QP), X), QM)
        self.assertEqual(filtered_interval(left, right), (F(1), F(1)))
        self.assertNotEqual(raw(left), raw(right))
        read = sigma(1, *V[0])
        paired_read = mm(mm(X, read), X)
        self.assertEqual(coords(paired_read), (F(1), V[0][0], -V[0][1], -V[0][2]))
        for name in m.COMMANDS:
            unitary = m.command_unitary(name)
            self.assertEqual(mm(X, unitary), mm(unitary, X))
        for word, axis in zip(WORDS, V, strict=True):
            unitary = eye(2)
            for name in word:
                unitary = mm(m.command_unitary(name), unitary)
            evolved_left = mm(mm(unitary, QP), dagger(unitary))
            evolved_right = mm(mm(unitary, QM), dagger(unitary))
            self.assertEqual(evolved_right, mm(mm(X, evolved_left), X))
            probability = trace(mm(read, evolved_left))
            self.assertEqual(probability, trace(mm(paired_read, evolved_right)))
            self.assertEqual(probability, (values(left, axis)[0], F(0)))
            paired_axis = (axis[0], -axis[1], -axis[2])
            self.assertEqual(
                tuple(zip(OUTCOMES, values(left, axis), strict=True)),
                tuple(zip(OUTCOMES, values(right, paired_axis), strict=True)),
            )
        # This paired unknown state/read frame is an ambiguity diagnostic.
        # It does not add an admitted terminal read or change its calibration.

    def test_inconsistent_exact_cell_masses_can_still_admit_a_budgeted_positive_witness(self):
        candidate = raw(CENTERS)
        observed = list(tables(CENTERS))
        eta = F(1, 100)
        altered = list(observed[1].probabilities)
        altered[0] = OUTCOMES[0], altered[0][1] + eta
        altered[4] = OUTCOMES[4], altered[4][1] - eta
        observed[1] = m.ProbabilityTable(WORDS[1], altered)
        with self.assertRaises(ValueError):
            m.reconstruct_kernel(observed, T)
        budget = m.ErrorBudget((0, eta, 0))
        witness = m.candidate_witness(candidate, observed, budget)
        self.assertIsInstance(witness, m.FeasibleWitness)
        self.assertEqual(witness.actual_tv, (F(0), eta, F(0)))
        self.assertEqual(witness.data.tables, tuple(observed))
        self.assertIs(witness.data.budget, budget)
        self.assertEqual(witness.kernel, candidate)

    def test_failed_candidate_is_inconclusive_even_when_another_exact_candidate_exists(self):
        observed = tables(SIGMAS)
        budget = m.ErrorBudget((0, 0, 0))
        failure = m.candidate_witness(raw(CENTERS), observed, budget)
        self.assertIsInstance(failure, m.CandidateFailure)
        self.assertEqual(failure.conclusion, "inconclusive")
        self.assertEqual(failure.actual_tv, errors(CENTERS, SIGMAS))
        self.assertEqual(failure.failed_settings, WORDS)
        good = m.candidate_witness(raw(SIGMAS), observed, budget)
        self.assertIsInstance(good, m.FeasibleWitness)
        self.assertIs(good.feasible_nonempty, True)
        self.assertFalse(hasattr(failure, "infeasible"))
        self.assertFalse(hasattr(failure, "filtered_diameter_upper"))

    def test_exact_tv_thresholds_and_event_difference_factor_are_not_rounded_or_clipped(self):
        eta = F(1, 100)
        sigmas = (CENTER, zeros(2), zeros(2), zeros(2))
        observed = list(tables(sigmas))
        entries = list(observed[1].probabilities)
        entries[0] = OUTCOMES[0], F(1, 2) + eta
        entries[1] = OUTCOMES[1], F(1, 2) - eta
        observed[1] = m.ProbabilityTable(WORDS[1], entries)
        self.assertEqual(m.total_variation(observed[1], tables(sigmas)[1]), eta)
        self.assertEqual(observed[1].weights[0] - F(1, 2), eta)
        self.assertEqual(observed[1].weights[0] - observed[1].weights[1], 2 * eta)
        candidate = raw(sigmas)
        exact = m.candidate_witness(candidate, observed, m.ErrorBudget((0, eta, 0)))
        self.assertIsInstance(exact, m.FeasibleWitness)
        too_small = m.candidate_witness(
            candidate, observed, m.ErrorBudget((0, eta - F(1, 10**12), 0))
        )
        self.assertIsInstance(too_small, m.CandidateFailure)
        self.assertEqual(too_small.failed_settings, (("A",),))
        large_budget = m.ErrorBudget((2, F(3, 2), 4))
        loose = m.candidate_witness(candidate, observed, large_budget)
        self.assertEqual(loose.data.budget.etas, (F(2), F(3, 2), F(4)))
        self.assertGreater(loose.filtered_diameter_upper, 1)

    def test_two_feasible_candidates_obey_the_certified_set_diameter_bounds(self):
        epsilon = F(1, 100)
        left, right = [], []
        for k in range(3):
            direction = tuple(epsilon * B[row][k] for row in range(3))
            left.append(sigma(F(1, 4), *direction))
            right.append(sigma(F(1, 4), *(-value for value in direction)))
        left.append(CENTERS[3])
        right.append(CENTERS[3])
        observed = tables(CENTERS)
        budget = m.ErrorBudget((epsilon / 2,) * 3)
        witnesses = tuple(
            m.candidate_witness(raw(sigmas), observed, budget) for sigmas in (left, right)
        )
        expected = 2 * sum(b * eta for b, eta in zip(COEFFICIENT_UPPER, budget.etas, strict=True))
        for witness in witnesses:
            self.assertIsInstance(witness, m.FeasibleWitness)
            self.assertEqual(witness.actual_tv, (epsilon / 2,) * 3)
            self.assertEqual(witness.filtered_diameter_upper, expected)
            self.assertEqual(witness.native_diameter_upper, expected / (1 - T))
            self.assertEqual(witness.coefficient_upper, COEFFICIENT_UPPER)
        self.assertLessEqual(filtered_interval(left, right)[1], expected)
        self.assertLessEqual(
            raw_interval(rhos_from_filtered(left), rhos_from_filtered(right))[1], expected / (1 - T)
        )

    def test_typed_candidate_retains_full_source_identity_prefix_and_pending_word(self):
        initial = snapshot()
        _, selected = m.commit(initial, (0, 0))
        source = m.run_word(selected, ("A", "B"))
        metadata = m.metadata_from_state(source)
        observed = tuple(m.probability_table(source.residual, T, word) for word in WORDS)
        records, pending = source.records, source.pending
        witness = m.candidate_witness(source, observed, m.ErrorBudget((0, 0, 0)), metadata=metadata)
        self.assertIs(witness.candidate, source)
        self.assertIs(witness.kernel, source.residual)
        self.assertIs(witness.data.metadata, metadata)
        self.assertEqual(metadata.records, source.records)
        self.assertEqual(metadata.pending, ("A", "B"))
        self.assertEqual(metadata.context.local.records[0].settings, ("H", "P_inv"))
        self.assertEqual(metadata.context.reference.records[0].payload, (("sample", "reference"),))
        self.assertEqual(metadata.records[0].precursor, (("beam", 0), ("probe", 0)))
        self.assertIs(source.records, records)
        self.assertIs(source.pending, pending)
        self.assertEqual(witness.actual_tv, (F(0),) * 3)
        # Pure hypothetical tables caused no terminal read, cut, new word or reset.

    def test_numerically_equal_candidates_do_not_erase_foreign_known_metadata(self):
        base = snapshot()
        first = m.run_word(base, ("A", "B"))
        second = m.run_word(base, ("AB",))
        self.assertEqual(first.residual, second.residual)
        observed = tuple(m.probability_table(first.residual, T, word) for word in WORDS)
        budget = m.ErrorBudget((0, 0, 0))
        with self.assertRaises(ValueError):
            m.candidate_witness(first, observed, budget)
        with self.assertRaises(ValueError):
            m.candidate_witness(first, observed, budget, metadata=m.metadata_from_state(second))
        metadata = m.metadata_from_state(first)
        for changed in (
            replace(metadata, pending=()),
            replace(metadata, context=replace(metadata.context, setting_id="different-cut")),
        ):
            with self.assertRaises(ValueError):
                m.candidate_witness(first, observed, budget, metadata=changed)
        good = m.candidate_witness(first, observed, budget, metadata=metadata)
        self.assertIsInstance(good, m.FeasibleWitness)

    def test_raw_candidate_audit_makes_no_automatic_operational_prefix_claim(self):
        source = snapshot()
        observed = tables(SIGMAS)
        witness = m.candidate_witness(source.residual, observed, m.ErrorBudget((0, 0, 0)))
        self.assertIsNone(witness.data.metadata)
        self.assertEqual(witness.candidate, source.residual)
        self.assertNotIsInstance(witness.candidate, m.State)
        self.assertFalse(hasattr(witness, "records"))
        self.assertFalse(hasattr(witness, "pending"))
        self.assertFalse(hasattr(witness, "confidence"))
        self.assertFalse(hasattr(witness, "preparation_probability"))

    def test_only_matched_typed_candidates_can_bind_snapshot_metadata(self):
        source = snapshot()
        metadata = m.metadata_from_state(source)
        foreign = replace(metadata, pending=("A",))
        budget = m.ErrorBudget((0, 0, 0))
        for observed, audit_type, expected_errors in (
            (tables(SIGMAS), m.FeasibleWitness, (F(0),) * 3),
            (tables(CENTERS), m.CandidateFailure, errors(SIGMAS, CENTERS)),
        ):
            raw_data = m.ObservationData(observed, budget)
            bound_data = m.ObservationData(observed, budget, metadata)
            foreign_data = m.ObservationData(observed, budget, foreign)
            raw_helper = m.candidate_witness(source.residual, observed, budget)
            raw_direct = audit_type(source.residual, raw_data)
            for audit in (raw_helper, raw_direct):
                self.assertIsInstance(audit, audit_type)
                self.assertIsNone(audit.data.metadata)
                self.assertEqual(audit.actual_tv, expected_errors)
            # Even metadata copied from the source cannot bind its untyped
            # residual: the raw mathematical path has no source identity.
            with self.assertRaises(ValueError):
                m.candidate_witness(source.residual, observed, budget, metadata=metadata)
            with self.assertRaises(ValueError):
                audit_type(source.residual, bound_data)
            typed_helper = m.candidate_witness(source, observed, budget, metadata=metadata)
            typed_direct = audit_type(source, bound_data)
            for audit in (typed_helper, typed_direct):
                self.assertIsInstance(audit, audit_type)
                self.assertIs(audit.candidate, source)
                self.assertIs(audit.data.metadata, metadata)
                self.assertEqual(audit.actual_tv, expected_errors)
            with self.assertRaises(ValueError):
                m.candidate_witness(source, observed, budget, metadata=foreign)
            with self.assertRaises(ValueError):
                audit_type(source, foreign_data)

    def test_audit_results_and_terminal_results_cannot_be_used_as_continuation_sources(self):
        source = snapshot()
        observed = tables(SIGMAS)
        budget = m.ErrorBudget((0, 0, 0))
        success = m.candidate_witness(source.residual, observed, budget)
        failure = m.candidate_witness(raw(CENTERS), observed, budget)
        for audit in (success, failure):
            for action in (
                lambda audit=audit: m.run_command(audit, "A"),
                lambda audit=audit: m.commit(audit, (0, 0)),
                lambda audit=audit: m.read_terminal(audit, (0, 0, "+")),
            ):
                with self.assertRaises(TypeError):
                    action()
        terminal = m.read_terminal(source, (0, 0, "+"))
        with self.assertRaises(TypeError):
            m.candidate_witness(terminal, observed, budget)
        with self.assertRaises(TypeError):
            m.metadata_from_state(terminal)

    def test_direct_audit_constructors_revalidate_instead_of_accepting_forged_conclusions(self):
        data = m.ObservationData(tables(SIGMAS), m.ErrorBudget((0, 0, 0)))
        with self.assertRaises(ValueError):
            m.FeasibleWitness(raw(CENTERS), data)
        with self.assertRaises(ValueError):
            m.CandidateFailure(raw(SIGMAS), data)
        witness = m.FeasibleWitness(raw(SIGMAS), data)
        with self.assertRaises(FrozenInstanceError):
            witness.filtered_diameter_upper = F(100)
        with self.assertRaises(ValueError):
            replace(witness, actual_tv=(F(1),) * 3)
        with self.assertRaises(FrozenInstanceError):
            data.budget.etas = (F(1),) * 3
        with self.assertRaises(TypeError):
            m.FeasibleWitness(raw(SIGMAS), data.tables)

    def test_error_budgets_reject_nonexact_negative_and_wrong_sized_values(self):
        for etas in ((0, 0), (0, 0, 0, 0), (F(-1, 100), 0, 0), (True, 0, 0), (0.1, 0, 0)):
            with self.assertRaises((TypeError, ValueError)):
                m.ErrorBudget(etas)
        exact = m.ErrorBudget((F(1, 10**30), 0, 2))
        self.assertEqual(exact.etas, (F(1, 10**30), F(0), F(2)))
        with self.assertRaises(TypeError):
            m.ObservationData(tables(SIGMAS), (0, 0, 0))

    def test_observation_data_preserves_resolved_order_and_typed_table_validation(self):
        observed = tables(SIGMAS)
        budget = m.ErrorBudget((0, 0, 0))
        for malformed in (
            observed[:2],
            observed + observed[:1],
            tuple(table.weights for table in observed),
        ):
            with self.assertRaises(TypeError):
                m.ObservationData(malformed, budget)
        for reordered in (observed[::-1], (observed[0], observed[0], observed[2])):
            with self.assertRaises(ValueError):
                m.ObservationData(reordered, budget)
        with self.assertRaises(ValueError):
            m.total_variation(observed[0], observed[1])
        with self.assertRaises(TypeError):
            m.total_variation(observed[0].weights, observed[0])
        with self.assertRaises(TypeError):
            m.ObservationData(observed, budget, metadata=snapshot())
        with self.assertRaises(ValueError):
            m.ProbabilityTable((), observed[0].probabilities[::-1])

    def test_one_shot_candidates_tables_budget_and_metadata_are_materialized_once(self):
        def rows(operator):
            return (iter(row) for row in operator)

        observed = tables(SIGMAS)
        budget = m.ErrorBudget(iter((0, 0, 0)))
        witness = m.candidate_witness(rows(raw(SIGMAS)), iter(observed), budget)
        self.assertIsInstance(witness, m.FeasibleWitness)
        self.assertEqual(witness.kernel, raw(SIGMAS))
        self.assertEqual(witness.data.tables, observed)
        self.assertEqual(
            m.filtered_difference_data(rows(raw(SIGMAS)), rows(raw(CENTERS))),
            m.filtered_difference_data(raw(SIGMAS), raw(CENTERS)),
        )
        source = m.run_word(snapshot(), ("A", "B"))
        metadata = m.SnapshotMetadata(
            source.context, iter(source.records), iter(source.pending), source.domain
        )
        self.assertEqual(metadata, m.metadata_from_state(source))
        typed_tables = tuple(m.probability_table(source.residual, T, word) for word in WORDS)
        typed = m.candidate_witness(source, iter(typed_tables), budget, metadata=metadata)
        self.assertIs(typed.candidate, source)

    def test_metadata_grammar_and_frozen_ids_do_not_admit_terminal_or_foreign_prefixes(self):
        source = snapshot()
        _, selected = m.commit(source, (0, 0))
        metadata = m.metadata_from_state(selected)
        with self.assertRaises(ValueError):
            replace(metadata, domain="K_t")
        with self.assertRaises(ValueError):
            replace(metadata, pending=("unavailable",))
        with self.assertRaises(TypeError):
            replace(metadata, pending="AB")
        terminal = m.read_terminal(source, (0, 0, "+"))
        with self.assertRaises(ValueError):
            replace(metadata, records=(terminal.record,))
        for invalid in (False, 0.0, F(0)):
            with self.assertRaises(ValueError):
                replace(metadata.records[0], event_id=invalid)
        with self.assertRaises(FrozenInstanceError):
            metadata.pending = ("A",)
        with self.assertRaises(ValueError):
            replace(metadata.context, reference=replace(metadata.context.reference, t=1))

    def test_invalid_candidate_kernels_are_rejected_not_clipped_projected_or_fitted(self):
        observed = tables(SIGMAS)
        budget = m.ErrorBudget((1, 1, 1))
        candidates = (
            zeros(16),
            scale(2, raw(SIGMAS)),
            raw((sigma(F(1, 4), 1),) + CENTERS[1:]),
            image(rhos_from_filtered(SIGMAS), F(-3, 5)),
        )
        for candidate in candidates:
            with self.assertRaises(ValueError):
                m.candidate_witness(candidate, observed, budget)
        with self.assertRaises(TypeError):
            m.candidate_witness(object(), observed, budget)
        with self.assertRaises(ValueError):
            m.filtered_difference_data(raw(SIGMAS), scale(2, raw(SIGMAS)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
