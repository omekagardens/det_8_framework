"""Independent exact certificates for one tilted terminal read.

Full per-cell joint weights, not conditionally renormalized probabilities,
enter reconstruction. Hypothetical exact tables do not supply preparations.
The terminal result retains audit provenance but no reusable output state.
Finite rank certificates supplement the universal finite-word span theorem.
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


def det3(a):
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


X = matrix(((0, 1), (1, 0)))
Y = matrix(((0, (0, -1)), ((0, 1), 0)))
Z = matrix(((1, 0), (0, -1)))
QP, QM = matrix(((1, 0), (0, 0))), matrix(((0, 0), (0, 1)))
CENTER = scale(F(1, 2), eye(2))
H0 = matrix(((1, 1), (1, -1)))
CNOT = matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)))
U0 = mm(tensor(eye(2), H0), CNOT)
UA = add(scale(F(3, 5), eye(2)), scale((0, F(-4, 5)), X))
T = F(3, 5)
CELLS = tuple(product((0, 1), repeat=2))
BITS = tuple(product((0, 1), repeat=4))
OUTCOMES = tuple((a, b, sign) for a, b in CELLS for sign in ("+", "-"))
WORDS = ((), ("A",), ("A", "A"))
AXES = (
    (F(3, 5), F(0), F(4, 5)),
    (F(3, 5), F(96, 125), F(-28, 125)),
    (F(3, 5), F(-1344, 3125), F(-2108, 3125)),
)
INVERSE = (
    (F(125, 192), F(70, 192), F(125, 192)),
    (F(-55, 192), F(180, 192), F(-125, 192)),
    (F(195, 256), F(-70, 256), F(-125, 256)),
)
QPLUS = scale(F(1, 10), matrix(((9, 3), (3, 1))))
QMINUS = add(eye(2), scale(-1, QPLUS))


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


def filt(cell):
    return matrix(((2, 0), (0, 1))) if cell[1] == 0 else matrix(((1, 0), (0, 2)))


def inv_filter(cell):
    return matrix(((F(1, 2), 0), (0, 1))) if cell[1] == 0 else matrix(((1, 0), (0, F(1, 2))))


def rhos_from_filtered(sigmas):
    return tuple(
        scale(10, mm(mm(inv_filter(cell), s), inv_filter(cell)))
        for cell, s in zip(CELLS, sigmas, strict=True)
    )


def retwist(operator):
    output = [[ZERO for _ in range(16)] for _ in range(16)]
    for a, i, b, j in BITS:
        for c, k, d, ell in BITS:
            native_left, native_right = 8 * a + 4 * i + 2 * b + j, 8 * c + 4 * k + 2 * d + ell
            group_left, group_right = 8 * a + 4 * b + 2 * i + j, 8 * c + 4 * d + 2 * k + ell
            output[native_left][native_right] = times(
                (-1) ** (a * i + b * j + c * k + d * ell), operator[group_left][group_right]
            )
    return matrix(output)


def image(rhos):
    reference = scale(F(1, 4), add(eye(2), scale(T, Z)))
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


def sparse_sigmas(index, s):
    return tuple(s if i == index else zeros(2) for i in range(4))


def values(sigmas, axis):
    output = []
    for s in sigmas:
        q, x, y, z = coords(s)
        difference = sum(a * b for a, b in zip(axis, (x, y, z), strict=True))
        output.extend(((q + difference) / 2, (q - difference) / 2))
    return tuple(output)


def exact_tables(sigmas):
    return tuple(
        m.ProbabilityTable(word, tuple(zip(OUTCOMES, values(sigmas, axis), strict=True)))
        for word, axis in zip(WORDS, AXES, strict=True)
    )


def local_from(rho):
    a = scale(F(1, 2), transpose(rho))
    b = mm(mm(Z, a), Z)
    return tuple(tuple(a[i]) + (m.G(), m.G()) for i in range(2)) + tuple(
        (m.G(), m.G()) + tuple(b[i]) for i in range(2)
    )


def snapshot(sigmas=SIGMAS, read_setting="read-A"):
    local_records = (
        m.InputRecord(0, "prepare", "beam-ready", ("H", "P_inv"), (("sample", "L"),)),
        m.InputRecord(1, "calibrate", "pass", ("Z",), (("phase", "full"),), (0,)),
    )
    reference_records = (m.InputRecord(0, "prepare", "probe-ready", ("Z",), (("sample", "R"),)),)
    context = m.Context(
        m.LocalInput(local_from(CENTER), "beam", local_records),
        m.ReferenceInput(T, "probe", reference_records),
        m.Independence(("beam", "probe")),
        m.TerminalReadPremise(setting_id=read_setting),
        joint_origin="joint-run",
        setting_id="cut-A",
    )
    # A declared conditional snapshot; provenance does not certify reachability.
    return m.State(m.INTERIOR_DOMAIN, context, raw(sigmas))


class TerminalReadObservabilityChecks(unittest.TestCase):
    def test_filtered_coordinates_reconstruct_every_native_entry_with_complex_transpose(self):
        rhos = rhos_from_filtered(SIGMAS)
        source = raw(SIGMAS)
        self.assertEqual(m.image_span(rhos, T), source)
        self.assertEqual(m.filtered_coordinates(source, T), SIGMAS)
        self.assertEqual(m.from_filtered_coordinates(SIGMAS, T, normalized=True), source)
        self.assertEqual(m.inverse_span(source, T), rhos)
        self.assertTrue(m.is_psd(source))
        self.assertEqual(mass(source), 1)
        self.assertNotEqual(source, image(tuple(transpose(rho) for rho in rhos)))

    def test_single_primary_tilted_read_is_complete_binary_with_full_cell_labels(self):
        self.assertEqual(m.READ_Q_PLUS, QPLUS)
        self.assertEqual(m.READ_Q_MINUS, QMINUS)
        self.assertEqual(mm(QPLUS, QPLUS), QPLUS)
        self.assertEqual(mm(QMINUS, QMINUS), QMINUS)
        self.assertEqual(mm(QPLUS, QMINUS), zeros(2))
        self.assertEqual(add(QPLUS, QMINUS), eye(2))
        self.assertEqual(m.TERMINAL_OUTCOMES, OUTCOMES)
        expected = values(SIGMAS, AXES[0])
        self.assertEqual(m.terminal_weights(raw(SIGMAS), T), expected)
        self.assertEqual(sum(expected), 1)
        self.assertEqual(
            tuple(expected[2 * i] + expected[2 * i + 1] for i in range(4)),
            tuple(coords(s)[0] for s in SIGMAS),
        )

    def test_backward_axes_and_determinant_follow_exact_conjugation(self):
        unitary = eye(2)
        for expected in AXES:
            backward = mm(mm(dagger(unitary), QPLUS), unitary)
            calculated = tuple(trace(mm(pauli, backward))[0] for pauli in (X, Y, Z))
            self.assertEqual(calculated, expected)
            self.assertEqual(sum(component * component for component in calculated), 1)
            unitary = mm(UA, unitary)
        self.assertEqual(det3(AXES), F(-73728, 78125))
        for i in range(3):
            for j in range(3):
                self.assertEqual(sum(INVERSE[i][k] * AXES[k][j] for k in range(3)), int(i == j))

    def test_named_three_setting_tables_equal_independent_full_probabilities(self):
        source = raw(SIGMAS)
        expected = exact_tables(SIGMAS)
        for word, table in zip(WORDS, expected, strict=True):
            self.assertEqual(m.probability_table(source, T, word), table)
            self.assertEqual(table.word, word)
            self.assertEqual(tuple(label for label, _ in table.probabilities), OUTCOMES)
            self.assertEqual(sum(p for _, p in table.probabilities), 1)
        # Tables are mathematical evaluations of a supplied snapshot. They do
        # not certify repeated physical preparation or previous-history weights.

    def test_general_axis_backward_rank_formula_has_exact_pauli_certificates(self):
        axes = (
            (F(1), F(0), F(0)),
            (F(0), F(1), F(0)),
            (F(0), F(0), F(1)),
            AXES[0],
            (F(2, 3), F(1, 3), F(2, 3)),
        )
        for axis in axes:
            initial_effect = sigma(1, *axis)
            backward = initial_effect
            rows = [(F(1), F(0), F(0), F(0))]
            for _ in range(3):
                rows.append(coords(backward))
                backward = mm(mm(dagger(UA), backward), UA)
            expected = 1 + int(axis[0] != 0) + 2 * int(axis[1] != 0 or axis[2] != 0)
            self.assertEqual(rank(rows), expected)
        # The general all-parameter classification belongs to the proof;
        # these exact ranks check its independent finite witnesses.

    def test_full_linear_ranks_and_normalized_affine_dimensions_are_distinct(self):
        for axis, expected in (((F(0), F(0), F(1)), 12), ((F(1), F(0), F(0)), 8), (AXES[0], 16)):
            qrows = []
            for cell in range(4):
                for coordinate in ((1, 0, 0, 0),):
                    qrows.append(
                        tuple(
                            F(value) if block == cell else F(0)
                            for block in range(4)
                            for value in coordinate
                        )
                    )
                backward = sigma(1, *axis)
                for _ in range(3):
                    local = coords(backward)
                    qrows.append(
                        tuple(
                            component if block == cell else F(0)
                            for block in range(4)
                            for component in local
                        )
                    )
                    backward = mm(mm(dagger(UA), backward), UA)
            self.assertEqual(rank(qrows), expected)
            # Restrict the row functionals to ker(total mass): three independent
            # intercell trace differences plus all twelve Bloch directions.
            tangent_basis = []
            for cell in range(1, 4):
                tangent_basis.append(
                    tuple(F(int(index == 4 * cell) - int(index == 0)) for index in range(16))
                )
            for cell in range(4):
                for direction in (1, 2, 3):
                    tangent_basis.append(
                        tuple(F(int(index == 4 * cell + direction)) for index in range(16))
                    )
            restricted = tuple(
                tuple(
                    sum(a * b for a, b in zip(row, tangent, strict=True))
                    for tangent in tangent_basis
                )
                for row in qrows
            )
            self.assertEqual(rank(restricted), expected - 1)

    def test_z_summary_has_a_positive_disk_cone_section_without_recovering_x(self):
        source = raw(SIGMAS)
        expected = tuple((q, y, z) for q, _, y, z in map(coords, SIGMAS))
        self.assertEqual(m.diagnostic_summary(source, T, "Z"), expected)
        section = m.diagnostic_section(expected, T, "Z")
        section_sigmas = tuple(sigma(q, 0, y, z) for q, y, z in expected)
        self.assertEqual(section, raw(section_sigmas))
        self.assertTrue(m.is_psd(section))
        self.assertEqual(m.diagnostic_summary(section, T, "Z"), expected)
        self.assertNotEqual(section, source)
        changed_summary = m.diagnostic_summary(m.command(source, T, "A"), T, "Z")
        self.assertEqual(m.command(section, T, "A"), m.diagnostic_section(changed_summary, T, "Z"))
        cut_summary = m.diagnostic_summary(m.branch(source, T, (0, 0)), T, "Z")
        self.assertEqual(m.branch(section, T, (0, 0)), m.diagnostic_section(cut_summary, T, "Z"))
        with self.assertRaises(ValueError):
            m.diagnostic_section(((F(1), F(1), F(1)),) + ((F(0), F(0), F(0)),) * 3, T, "Z")

    def test_x_summary_has_a_positive_interval_cone_section_without_yz(self):
        source = raw(SIGMAS)
        expected = tuple((q, x) for q, x, _, _ in map(coords, SIGMAS))
        self.assertEqual(m.diagnostic_summary(source, T, "X"), expected)
        section = m.diagnostic_section(expected, T, "X")
        self.assertEqual(section, raw(tuple(sigma(q, x) for q, x in expected)))
        self.assertTrue(m.is_psd(section))
        self.assertEqual(m.diagnostic_summary(section, T, "X"), expected)
        self.assertNotEqual(section, source)
        changed_summary = m.diagnostic_summary(m.command(source, T, "A"), T, "X")
        self.assertEqual(m.command(section, T, "A"), m.diagnostic_section(changed_summary, T, "X"))
        cut_summary = m.diagnostic_summary(m.branch(source, T, (0, 0)), T, "X")
        self.assertEqual(m.branch(section, T, (0, 0)), m.diagnostic_section(cut_summary, T, "X"))
        with self.assertRaises(ValueError):
            m.diagnostic_section(((F(1), F(2)),) + ((F(0), F(0)),) * 3, T, "X")

    def test_z_invisible_filtered_x_eigenstates_are_separated_by_the_tilted_read(self):
        states = tuple(raw(sparse_sigmas(0, sigma(1, sign, 0, 0))) for sign in (1, -1))
        self.assertEqual(
            m.diagnostic_summary(states[0], T, "Z"), m.diagnostic_summary(states[1], T, "Z")
        )
        self.assertNotEqual(states[0], states[1])
        for source in states:
            changed = m.command(m.command(source, T, "A"), T, "B")
            self.assertEqual(changed, source)
        self.assertEqual(m.terminal_weights(states[0], T), (F(4, 5), F(1, 5)) + (F(0),) * 6)
        self.assertEqual(m.terminal_weights(states[1], T), (F(1, 5), F(4, 5)) + (F(0),) * 6)

    def test_pi_z_countercontrol_does_not_make_a_z_read_fully_observable(self):
        for unitary in (UA, Z):
            conjugated_x = mm(mm(dagger(unitary), X), unitary)
            self.assertIn(conjugated_x, (X, scale(-1, X)))
            for effect_matrix in (Y, Z):
                backward = mm(mm(dagger(unitary), effect_matrix), unitary)
                self.assertEqual(trace(mm(X, backward))[0], 0)
        # Both generators preserve span(Y,Z); closure preserves that plane.
        # Nonparallel rotation axes alone are insufficient when the Z turn is pi.
        unitary = mm(mm(UA, Z), mm(UA, Z))
        self.assertEqual(trace(mm(X, mm(mm(dagger(unitary), Z), unitary)))[0], 0)

    def test_three_settings_invert_full_differences_without_conditioning_on_cell(self):
        tables = exact_tables(SIGMAS)
        for cell, s in enumerate(SIGMAS):
            differences = tuple(
                table.probabilities[2 * cell][1] - table.probabilities[2 * cell + 1][1]
                for table in tables
            )
            reconstructed = tuple(sum(row[k] * differences[k] for k in range(3)) for row in INVERSE)
            self.assertEqual(reconstructed, coords(s)[1:])
            self.assertNotEqual(coords(s)[0], 1)
        self.assertEqual(m.reconstruct_kernel(tables, T), raw(SIGMAS))
        self.assertEqual(
            m.inverse_span(m.reconstruct_kernel(tables, T), T), rhos_from_filtered(SIGMAS)
        )

    def test_zero_weight_cells_reconstruct_as_zero_without_division(self):
        sigmas = sparse_sigmas(2, sigma(1, F(3, 5), F(4, 5), 0))
        tables = exact_tables(sigmas)
        for table in tables:
            self.assertEqual(tuple(p for _, p in table.probabilities[:4]), (F(0),) * 4)
            self.assertEqual(tuple(p for _, p in table.probabilities[6:]), (F(0),) * 2)
        reconstructed = m.reconstruct_kernel(tables, T)
        self.assertEqual(reconstructed, raw(sigmas))
        self.assertEqual(m.filtered_coordinates(reconstructed, T), sigmas)

    def test_two_resolved_settings_have_a_remaining_exact_blind_direction(self):
        first, second = AXES[:2]
        null = (
            first[1] * second[2] - first[2] * second[1],
            first[2] * second[0] - first[0] * second[2],
            first[0] * second[1] - first[1] * second[0],
        )
        self.assertNotEqual(null, (0, 0, 0))
        self.assertEqual(sum(a * b for a, b in zip(first, null, strict=True)), 0)
        self.assertEqual(sum(a * b for a, b in zip(second, null, strict=True)), 0)
        left = sparse_sigmas(0, sigma(1, *(value / 2 for value in null)))
        right = sparse_sigmas(0, sigma(1, *(-value / 2 for value in null)))
        self.assertTrue(m.is_psd(left[0]) and m.is_psd(right[0]))
        self.assertEqual(exact_tables(left)[:2], exact_tables(right)[:2])
        self.assertNotEqual(exact_tables(left)[2], exact_tables(right)[2])
        # Exact rank/minimality witness, not a statistical finite-sample estimate.

    def test_nonnegative_tables_can_still_fail_the_bloch_compatibility_constraint(self):
        impossible_sigmas = sparse_sigmas(0, sigma(1, F(6, 5), 0, 0))
        tables = exact_tables(impossible_sigmas)
        self.assertTrue(all(p >= 0 for table in tables for _, p in table.probabilities))
        self.assertEqual(
            tuple(sum(p for _, p in table.probabilities) for table in tables), (F(1),) * 3
        )
        self.assertFalse(m.is_psd(impossible_sigmas[0]))
        with self.assertRaises(ValueError):
            m.reconstruct_kernel(tables, T)
        all_plus = tuple(
            m.ProbabilityTable(word, tuple(zip(OUTCOMES, (F(1),) + (F(0),) * 7, strict=True)))
            for word in WORDS
        )
        self.assertEqual(sum(INVERSE[0]), F(5, 3))
        with self.assertRaises(ValueError):
            m.reconstruct_kernel(all_plus, T)

    def test_reconstruction_rejects_shared_cell_mass_disagreement_even_with_unit_totals(self):
        tables = list(exact_tables(SIGMAS))
        changed = list(tables[1].probabilities)
        changed[0] = changed[0][0], changed[0][1] + F(1, 100)
        changed[2] = changed[2][0], changed[2][1] - F(1, 100)
        tables[1] = m.ProbabilityTable(WORDS[1], tuple(changed))
        self.assertEqual(sum(p for _, p in tables[1].probabilities), 1)
        with self.assertRaises(ValueError):
            m.reconstruct_kernel(tables, T)

    def test_native_signed_span_effect_certificates_have_rank_sixteen(self):
        basis = tuple(
            sparse_sigmas(cell, sigma(*coordinate))
            for cell in range(4)
            for coordinate in ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
        )
        columns = []
        for sigmas in basis:
            source = raw(sigmas)
            self.assertEqual(m.from_filtered_coordinates_on_span(sigmas, T), source)
            self.assertEqual(m.filtered_coordinates_on_span(source, T), sigmas)
            column = []
            changed = source
            for axis in AXES:
                actual = m.terminal_weights_on_span(changed, T)
                self.assertEqual(actual, values(sigmas, axis))
                column.extend(actual)
                changed = m.command_on_span(changed, T, "A")
            columns.append(tuple(column))
        self.assertEqual(rank(columns), 16)
        self.assertEqual(rank(tuple(flatten(raw(sigmas)) for sigmas in basis)), 16)

    def test_pulled_terminal_effects_are_exact_on_actual_rho_blocks(self):
        rhos = rhos_from_filtered(SIGMAS)
        for index, cell in enumerate(CELLS):
            effects = []
            for sign, projector in (("+", QPLUS), ("-", QMINUS)):
                effect = scale(F(1, 10), mm(mm(filt(cell), projector), filt(cell)))
                self.assertEqual(m.terminal_projector(sign), projector)
                self.assertEqual(m.terminal_effect_matrix((*cell, sign), T), effect)
                self.assertTrue(m.is_psd(effect))
                expected = values(SIGMAS, AXES[0])[2 * index + int(sign == "-")]
                self.assertEqual(trace(mm(effect, rhos[index]))[0], expected)
                effects.append(effect)
            self.assertEqual(add(*effects), scale(F(1, 10), mm(filt(cell), filt(cell))))

    def test_homogeneous_weights_and_sections_do_not_create_normalized_probability_tables(self):
        source = raw(SIGMAS)
        self.assertEqual(
            m.terminal_weights(scale(3, source), T), tuple(3 * p for p in values(SIGMAS, AXES[0]))
        )
        self.assertEqual(m.terminal_weights(zeros(16), T), (F(0),) * 8)
        for unnormalized in (scale(3, source), zeros(16)):
            with self.assertRaises(ValueError):
                m.probability_table(unnormalized, T)
        for axis, width in (("Z", 3), ("X", 2)):
            section = m.diagnostic_section(((F(0),) * width,) * 4, T, axis)
            self.assertEqual(section, zeros(16))
            with self.assertRaises(ValueError):
                m.diagnostic_section(((F(0),) * width,) * 4, T, axis, normalized=True)

    def test_probability_table_requires_complete_ordered_exact_labels_and_valid_values(self):
        table = exact_tables(SIGMAS)[0]
        for entries in (
            table.probabilities[:-1],
            table.probabilities[::-1],
            (table.probabilities[0],) * 8,
        ):
            with self.assertRaises(ValueError):
                m.ProbabilityTable((), entries)
        for value in (F(-1, 10), F(11, 10), False, 0.5):
            entries = list(table.probabilities)
            entries[0] = OUTCOMES[0], value
            with self.assertRaises((TypeError, ValueError)):
                m.ProbabilityTable((), entries)
        for label in (
            (False, 0, "+"),
            (0.0, 0, "+"),
            (F(0), 0, "+"),
            (0, 0, 1),
            (0, "+"),
            [0, 0, "+"],
        ):
            with self.assertRaises(ValueError):
                m.ProbabilityTable(
                    (), ((label, table.probabilities[0][1]),) + table.probabilities[1:]
                )
        with self.assertRaises(TypeError):
            m.ProbabilityTable("A", table.probabilities)
        with self.assertRaises(ValueError):
            m.ProbabilityTable(("B",), table.probabilities)

    def test_reconstruction_requires_three_resolved_settings_and_the_fixed_interior_frame(self):
        tables = exact_tables(SIGMAS)
        for wrong in (
            tables[:2],
            tables + tables[:1],
            tuple(table.probabilities for table in tables),
        ):
            with self.assertRaises(TypeError):
                m.reconstruct_kernel(wrong, T)
        for wrong in (tables[::-1], (tables[0], tables[0], tables[2])):
            with self.assertRaises(ValueError):
                m.reconstruct_kernel(wrong, T)
        for t in (F(-1), F(1), F(0), F(-3, 5)):
            with self.assertRaises(ValueError):
                m.reconstruct_kernel(tables, t)
        for word in (("B",), ("A", "A", "A")):
            with self.assertRaises(ValueError):
                m.probability_table(raw(SIGMAS), T, word)

    def test_additional_terminal_read_premise_is_explicit_not_inferred_from_old_context(self):
        source = snapshot()
        self.assertEqual(source.domain, "interior_filtered_L_t_with_terminal_read")
        self.assertEqual(source.context.terminal_read.calibration, "filtered_tilt_3_0_4_over_5")
        self.assertEqual(source.context.terminal_read.setting_id, "read-A")
        self.assertIs(source.context.terminal_read.available, True)
        with self.assertRaises(TypeError):
            replace(source.context, terminal_read=None)
        for available in (False, 1, "true"):
            with self.assertRaises(ValueError):
                m.TerminalReadPremise(available=available)
        with self.assertRaises(ValueError):
            m.TerminalReadPremise(calibration="uncalibrated")
        with self.assertRaises(TypeError):
            m.prepare_state(
                m.INTERIOR_DOMAIN,
                source.context.local,
                source.context.reference,
                source.context.independence,
            )
        seed = m.prepare_state(
            m.INTERIOR_DOMAIN,
            source.context.local,
            source.context.reference,
            source.context.independence,
            terminal_read=source.context.terminal_read,
        )
        self.assertEqual(mass(seed.residual), 1)

    def test_all_terminal_outcomes_preserve_the_exact_pre_read_source_without_fake_cell_commit(
        self,
    ):
        source = snapshot()
        old_records, old_pending, old_raw = source.records, source.pending, source.residual
        results = tuple(m.read_terminal(source, outcome) for outcome in OUTCOMES)
        self.assertEqual(tuple(result.probability for result in results), values(SIGMAS, AXES[0]))
        self.assertEqual(sum(result.probability for result in results), 1)
        for outcome, result in zip(OUTCOMES, results, strict=True):
            self.assertIs(result.source, source)
            self.assertEqual(result.record.event_id, 0)
            self.assertEqual(result.record.outcome, outcome)
            self.assertEqual(result.record.action, "terminal_tilted_read")
            self.assertEqual(result.record.precursor, (("beam", 0), ("beam", 1), ("probe", 0)))
            self.assertEqual(result.effect, m.terminal_effect_matrix(outcome, T))
            self.assertFalse(hasattr(result, "residual"))
            self.assertFalse(hasattr(result, "pending"))
        self.assertIs(source.records, old_records)
        self.assertIs(source.pending, old_pending)
        self.assertIs(source.residual, old_raw)

    def test_terminal_record_retains_actual_prefix_word_calibration_and_both_input_histories(self):
        source = snapshot()
        _, selected = m.commit(m.run_command(source, "A"), (0, 0))
        pre_read = m.run_word(selected, ("B_inv", "A"))
        result = m.read_terminal(pre_read, (0, 0, "+"))
        record = result.record
        self.assertIs(result.source, pre_read)
        self.assertEqual(record.event_id, 1)
        self.assertEqual(record.command_word, ("B_inv", "A"))
        self.assertEqual(
            record.precursor, (("beam", 0), ("beam", 1), ("probe", 0), ("joint-run", 0))
        )
        self.assertEqual(record.origin, "joint-run")
        self.assertEqual(record.setting_id, "read-A")
        self.assertEqual(record.calibration, source.context.terminal_read.calibration)
        self.assertIs(record.context, source.context)
        self.assertEqual(record.context.local.records[0].settings, ("H", "P_inv"))
        self.assertEqual(record.context.local.records[1].precursor, (0,))
        self.assertEqual(record.context.reference.records[0].payload, (("sample", "R"),))
        self.assertEqual(record.context.reference.t, T)
        self.assertEqual(record.context.reference.orientation, "Z")
        self.assertEqual(record.context.coupler, "shared_CNOT_H2")
        self.assertEqual(record.context.frame, "fixed_shared_image")
        self.assertEqual(record.context.setting_id, "cut-A")
        self.assertEqual(pre_read.records, selected.records)
        self.assertEqual(pre_read.pending, ("B_inv", "A"))

    def test_zero_terminal_outcome_and_counterfeit_result_are_rejected(self):
        source = snapshot(sparse_sigmas(0, QMINUS))
        self.assertEqual(m.terminal_weights(source.residual, T), (F(0), F(1)) + (F(0),) * 6)
        with self.assertRaises(ValueError):
            m.read_terminal(source, (0, 0, "+"))
        with self.assertRaises(ValueError):
            m.read_terminal(source, (1, 1, "-"))
        result = m.read_terminal(source, (0, 0, "-"))
        with self.assertRaises(ValueError):
            replace(result, probability=F(1, 2))
        with self.assertRaises(ValueError):
            replace(result, effect=eye(2))
        with self.assertRaises(ValueError):
            replace(result, source=m.run_command(source, "A"))
        zero_record = replace(result.record, outcome=(0, 0, "+"))
        with self.assertRaises(ValueError):
            m.TerminalResult(source, zero_record, m.terminal_effect_matrix((0, 0, "+"), T), F(0))
        self.assertEqual((source.records, source.pending), ((), ()))

    def test_terminal_result_is_not_an_input_to_any_primary_continuation(self):
        result = m.read_terminal(snapshot(), (0, 0, "+"))
        for action in (
            lambda: m.run_command(result, "A"),
            lambda: m.run_word(result, ("A",)),
            lambda: m.commit(result, (0, 0)),
            lambda: m.read_terminal(result, (0, 0, "+")),
        ):
            with self.assertRaises(TypeError):
                action()
        with self.assertRaises(TypeError):
            m.TerminalResult(result, result.record, result.effect, result.probability)
        self.assertFalse(hasattr(result, "output_state"))
        self.assertFalse(hasattr(result, "reset"))
        # Retained source is pre-read audit data, not a post-read operation.

    def test_same_raw_group_element_keeps_distinct_known_terminal_words_and_settings(self):
        source = snapshot()
        first = m.run_word(source, ("A", "B"))
        second = m.run_word(source, ("AB",))
        self.assertEqual(first.residual, second.residual)
        left, right = (m.read_terminal(state, (0, 0, "+")) for state in (first, second))
        self.assertEqual(left.probability, right.probability)
        self.assertEqual(left.effect, right.effect)
        self.assertNotEqual(left.record, right.record)
        self.assertEqual(left.record.command_word, ("A", "B"))
        self.assertEqual(right.record.command_word, ("AB",))
        other = snapshot(read_setting="read-B")
        other_result = m.read_terminal(other, (0, 0, "+"))
        same_raw_result = m.read_terminal(source, (0, 0, "+"))
        self.assertEqual(other_result.probability, same_raw_result.probability)
        self.assertNotEqual(other_result.record, same_raw_result.record)
        # A common policy may inspect the known initial word, but not raw
        # audit data: stop on ('AB',), otherwise perform the fixed terminal read.
        terminal_counts = []
        for initial in (first, second):
            if initial.pending == ("AB",):
                leaves = ((F(1), None),)
            else:
                results = tuple(m.read_terminal(initial, outcome) for outcome in OUTCOMES)
                leaves = tuple((result.probability, result) for result in results)
            self.assertEqual(sum(probability for probability, _ in leaves), 1)
            terminal_counts.append(sum(result is not None for _, result in leaves))
        self.assertEqual(terminal_counts, [8, 0])

    def test_one_shot_reconstruction_rows_tables_and_effects_are_consumed_once(self):
        def rows(operator):
            return (iter(row) for row in operator)

        source = raw(SIGMAS)
        self.assertEqual(m.filtered_coordinates(rows(source), T), SIGMAS)
        self.assertEqual(m.from_filtered_coordinates((rows(s) for s in SIGMAS), T), source)
        self.assertEqual(m.terminal_weights(rows(source), T), values(SIGMAS, AXES[0]))
        tables = exact_tables(SIGMAS)
        rebuilt = tuple(
            m.ProbabilityTable(iter(table.word), (iter(entry) for entry in table.probabilities))
            for table in tables
        )
        self.assertEqual(rebuilt, tables)
        self.assertEqual(m.reconstruct_kernel(iter(rebuilt), T), source)
        self.assertEqual(m.probability_table(rows(source), T, iter(("A",))), tables[1])
        summary = tuple((q, y, z) for q, _, y, z in map(coords, SIGMAS))
        self.assertEqual(
            m.diagnostic_section((iter(row) for row in summary), T, "Z"),
            raw(tuple(sigma(q, 0, y, z) for q, y, z in summary)),
        )
        result = m.read_terminal(snapshot(), (0, 0, "+"))
        self.assertEqual(replace(result, effect=rows(result.effect)), result)

    def test_terminal_records_tables_and_metadata_are_immutable_with_strict_ids(self):
        source = snapshot()
        context = replace(source.context, permutation=iter(source.context.permutation))
        record = m.TerminalRecord(
            m.INTERIOR_DOMAIN,
            0,
            (0, 0, "+"),
            (iter(item) for item in (("beam", 0), ("beam", 1), ("probe", 0))),
            context,
            iter(("A", "B")),
        )
        self.assertEqual(record.command_word, ("A", "B"))
        self.assertEqual(record.precursor, (("beam", 0), ("beam", 1), ("probe", 0)))
        for invalid in (False, F(0), 0.0, -1):
            with self.assertRaises(ValueError):
                replace(record, event_id=invalid)
        for outcome in ((False, 0, "+"), (0, 0, 1), (0, 0), [0, 0, "+"]):
            with self.assertRaises(ValueError):
                replace(record, outcome=outcome)
        for precursor in (("beam", 0), (("beam", False),), record.precursor[:-1]):
            with self.assertRaises((TypeError, ValueError)):
                replace(record, precursor=precursor)
        with self.assertRaises(TypeError):
            replace(record, command_word="AB")
        with self.assertRaises(ValueError):
            replace(record, action="literal_joint_cell_cut")
        with self.assertRaises(FrozenInstanceError):
            record.command_word = ("AB",)
        table = exact_tables(SIGMAS)[0]
        with self.assertRaises(FrozenInstanceError):
            table.word = ("A",)

    def test_new_read_does_not_admit_extra_axes_endpoints_or_context_changes(self):
        source = snapshot()
        for domain in ("interior_filtered_L_t", "cut_closed_L_t", "K_t"):
            with self.assertRaises(ValueError):
                m.State(domain, source.context, source.residual)
        for t in (F(-1), F(1), F(0), F(-3, 5)):
            with self.assertRaises(ValueError):
                replace(source.context, reference=replace(source.context.reference, t=t))
            with self.assertRaises(ValueError):
                m.terminal_weights(source.residual, t)
        for name in ("read_Z", "read_X", "pi_Z", "tilt_changed"):
            with self.assertRaises(ValueError):
                m.run_command(source, name)
        for field, wrong in (("coupler", "identity"), ("frame", "local"), ("joint_origin", "beam")):
            with self.assertRaises(ValueError):
                replace(source.context, **{field: wrong})
        with self.assertRaises(ValueError):
            replace(source.context.reference, orientation="X")
        with self.assertRaises(ValueError):
            m.diagnostic_summary(source.residual, T, "Y")

    def test_terminal_probability_is_conditional_on_the_supplied_snapshot_only(self):
        source = snapshot()
        global_probability = values(SIGMAS, AXES[0])[0]
        cell_probability, selected = m.commit(source, (0, 0))
        result = m.read_terminal(selected, (0, 0, "+"))
        self.assertEqual(cell_probability, F(3, 10))
        self.assertEqual(result.probability, F(11, 15))
        self.assertEqual(cell_probability * result.probability, global_probability)
        self.assertNotEqual(result.probability, global_probability)
        self.assertIs(result.source, selected)
        self.assertEqual(result.record.event_id, 1)
        self.assertEqual(len(source.records), 0)
        self.assertEqual(len(selected.records), 1)
        # These probabilities concern the displayed declared snapshots. No
        # selection weights for the earlier local/reference preparation are known.


if __name__ == "__main__":
    unittest.main(verbosity=2)
