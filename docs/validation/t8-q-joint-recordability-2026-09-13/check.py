"""Independent exact checks for the conditional joint-recordability test.

Native tensor order, full complex kernels and total-entry mass are retained.
The reference, independence and coupler are declared candidate premises, not
DET-derived preparations or arbitrary-ancilla quantum availability. Finite
linear certificates support the formulas; sample states are not substitutes
for the general structural proof.
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


def mass(operator):
    return total(entry for row in operator for entry in row)[0]


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
H0 = matrix(((1, 1), (1, -1)))
P = matrix(((1, 0), (0, (0, 1))))
CNOT = matrix(
    tuple(int(row == 2 * i + (j ^ i)) for row in range(4)) for i in range(2) for j in range(2)
)
U0 = mm(tensor(eye(2), H0), CNOT)
SWAP = matrix(tuple(int(row == 2 * j + i) for row in range(4)) for i in range(2) for j in range(2))
CELLS = tuple(product((0, 1), repeat=2))
CROSS_PAIRS = tuple(combinations(CELLS, 2))
BITS = tuple(product((0, 1), repeat=4))


def native(a, i, b, j):
    return 8 * a + 4 * i + 2 * b + j


def joint(a, b, i, j):
    return 8 * a + 4 * b + 2 * i + j


def untwist(operator):
    output = [[ZERO for _ in range(16)] for _ in range(16)]
    for a, i, b, j in BITS:
        for c, k, d, ell in BITS:
            sign = (-1) ** (a * i + b * j + c * k + d * ell)
            output[joint(a, b, i, j)][joint(c, d, k, ell)] = times(
                sign, operator[native(a, i, b, j)][native(c, k, d, ell)]
            )
    return matrix(output)


def retwist(operator):
    output = [[ZERO for _ in range(16)] for _ in range(16)]
    for a, i, b, j in BITS:
        for c, k, d, ell in BITS:
            sign = (-1) ** (a * i + b * j + c * k + d * ell)
            output[native(a, i, b, j)][native(c, k, d, ell)] = times(
                sign, operator[joint(a, b, i, j)][joint(c, d, k, ell)]
            )
    return matrix(output)


def block(operator, row, column):
    return matrix(operator[4 * row + i][4 * column : 4 * column + 4] for i in range(4))


def apply_shared(operator, numerator, factor=1):
    source = untwist(operator)
    output = [[ZERO for _ in range(16)] for _ in range(16)]
    for r, s in product(range(4), repeat=2):
        changed = scale(factor, mm(mm(numerator, block(source, r, s)), dagger(numerator)))
        for i, j in product(range(4), repeat=2):
            output[4 * r + i][4 * s + j] = changed[i][j]
    return retwist(matrix(output))


def cell_indices(cell):
    a, b = cell
    return tuple(native(a, i, b, j) for i, j in product((0, 1), repeat=2))


def cross(operator, left, right):
    return total(operator[i][j] for i in cell_indices(left) for j in cell_indices(right))


def weights(operator):
    return tuple(cross(operator, cell, cell)[0] for cell in CELLS)


def assemble(a, f, b):
    adjoint = dagger(f)
    return tuple(tuple(a[i]) + tuple(f[i]) for i in range(2)) + tuple(
        tuple(adjoint[i]) + tuple(b[i]) for i in range(2)
    )


def local(a, c=0):
    return assemble(a, scale(c, Z), mm(mm(Z, a), Z))


def reference(t):
    return local(scale(F(1, 4), add(eye(2), scale(t, Z))))


def from_coordinates(values):
    a, b, x, y, real_c, imag_c = values
    return local(matrix(((a, (x, y)), ((x, -y), b))), (real_c, imag_c))


LOCAL_SPAN = tuple(from_coordinates(tuple(F(int(i == j)) for i in range(6))) for j in range(6))
A = matrix(((F(3, 10), (0, F(1, 20))), ((0, F(-1, 20)), F(1, 5))))
C = m.G(F(3, 100), F(1, 25))
LOCAL = local(A, C)


def initial_source(c=0, t=F(1, 2), *, records=False, a=A):
    local_records = (
        (
            m.InputRecord(0, "prepare", "local-0", ("H",), (("sample", "left"),)),
            m.InputRecord(1, "read", "local-1", ("P",), (("retained", "yes"),), (0,)),
        )
        if records
        else ()
    )
    reference_records = (
        (
            m.InputRecord(
                0, "prepare_reference", "reference-0", ("polarize-Z",), (("sample", "right"),)
            ),
        )
        if records
        else ()
    )
    left = m.LocalState(local(a, c), origin="local-run", records=local_records)
    right = m.ReferenceState(t, origin="reference-run", records=reference_records)
    premise = m.Independence((left.origin, right.origin))
    prospective = m.prepare_joint(left, right, premise, joint_origin="joint-run")
    return m.promote_joint(prospective)


class JointRecordabilityChecks(unittest.TestCase):
    def test_native_and_joint_indices_are_distinct_exact_bijections(self):
        self.assertEqual({native(*bits) for bits in BITS}, set(range(16)))
        self.assertEqual({joint(a, b, i, j) for a, i, b, j in BITS}, set(range(16)))
        self.assertNotEqual(native(0, 1, 0, 0), joint(0, 0, 1, 0))
        for a, i, b, j in BITS:
            self.assertEqual(m.index_native(a, i, b, j), native(a, i, b, j))
            self.assertEqual(m.index_joint(a, b, i, j), joint(a, b, i, j))

    def test_full_complex_tensor_and_untwist_match_independent_entrywise_rules(self):
        source = tensor(LOCAL, reference(F(1, 2)))
        self.assertEqual(m.tensor(LOCAL, m.reference_kernel(F(1, 2))), source)
        self.assertEqual(m.to_untwisted(source), untwist(source))
        self.assertEqual(m.from_untwisted(untwist(source)), source)
        self.assertEqual(retwist(m.to_untwisted(source)), source)
        self.assertTrue(any(entry.imag for row in source for entry in row))

    def test_untwisted_blocks_keep_complex_c_and_reference_cell_zeros(self):
        t = F(1, 2)
        b = scale(F(1, 4), add(eye(2), scale(t, Z)))
        source = untwist(tensor(LOCAL, reference(t)))
        for r, (a, ref) in enumerate(CELLS):
            for s, (other_a, other_ref) in enumerate(CELLS):
                if ref != other_ref:
                    expected = zeros(4)
                elif a == other_a:
                    expected = tensor(A, b)
                else:
                    coefficient = C if a == 0 else m.G(*conj(C))
                    expected = scale(coefficient, tensor(eye(2), b))
                self.assertEqual(block(source, r, s), expected)

    def test_native_cell_forms_equal_untwisted_signed_read_vector_forms(self):
        source = tensor(LOCAL, reference(F(-1, 3)))
        untwisted = untwist(source)
        read_vectors = tuple(
            tuple(F((-1) ** (a * i + b * j)) for i, j in product((0, 1), repeat=2))
            for a, b in CELLS
        )
        resolution = zeros(4)
        for vector in read_vectors:
            resolution = add(resolution, matrix(tuple(a * b for b in vector) for a in vector))
        self.assertEqual(resolution, scale(4, eye(4)))
        for r, left in enumerate(CELLS):
            for s, right in enumerate(CELLS):
                chunk = block(untwisted, r, s)
                result = total(
                    times(read_vectors[r][i] * read_vectors[s][j], chunk[i][j])
                    for i, j in product(range(4), repeat=2)
                )
                self.assertEqual(cross(source, left, right), result)
                self.assertEqual(pair(m.joint_cross(source, left, right)), result)

    def test_independent_products_are_initially_joint_recordable_for_all_checked_c(self):
        for t in (F(-1), F(-1, 2), F(0), F(1, 2), F(1)):
            for c in (0, C, m.G(0, F(-1, 20))):
                source = tensor(local(A, c), reference(t))
                self.assertTrue(m.is_psd(source))
                self.assertTrue(m.joint_recordable(source, normalized=True))
                self.assertEqual(m.joint_mass(source), 1)
                self.assertEqual(m.joint_weights(source), weights(source))
                self.assertEqual(
                    tuple(pair(value) for value in m.joint_crossforms(source)), (ZERO,) * 6
                )

    def test_cnot_order_and_shared_unitarity_have_exact_certificates(self):
        for i, j in product((0, 1), repeat=2):
            column = 2 * i + j
            self.assertEqual(
                tuple(CNOT[row][column] for row in range(4)),
                tuple(m.G(int(row == 2 * i + (j ^ i))) for row in range(4)),
            )
        self.assertEqual(scale(F(1, 2), mm(U0, dagger(U0))), eye(4))
        for t in (F(-1), F(0), F(2, 3), F(1)):
            b = scale(F(1, 4), add(eye(2), scale(t, Z)))
            changed = scale(F(1, 2), mm(mm(U0, tensor(eye(2), b)), dagger(U0)))
            expected = scale(F(1, 4), add(eye(4), scale(t, tensor(Z, X))))
            self.assertEqual(changed, expected)

    def test_coupler_matches_independent_full_sixteen_atom_congruence(self):
        source = tensor(LOCAL, reference(F(1, 2)))
        coupled = m.shared_couple(source)
        self.assertEqual(coupled, apply_shared(source, U0, F(1, 2)))
        self.assertTrue(m.is_psd(coupled))
        self.assertEqual(trace(coupled), trace(source))

    def test_polarized_reference_exposes_both_real_and_imaginary_c_with_exact_signs(self):
        self.assertEqual(tuple(m.CROSS_PAIRS), CROSS_PAIRS)
        for t in (F(-1), F(1, 2), F(1)):
            for c in (F(1, 20), m.G(0, F(1, 20)), C):
                coupled = m.shared_couple(tensor(local(A, c), reference(t)))
                expected = (ZERO, times(t, c), ZERO, ZERO, times(-t, c), ZERO)
                self.assertEqual(
                    tuple(pair(value) for value in m.joint_crossforms(coupled)), expected
                )
                self.assertEqual(pair(m.joint_cross(coupled, (1, 0), (0, 0))), conj(times(t, c)))
                self.assertFalse(m.joint_recordable(coupled))

    def test_failed_joint_recordability_is_not_repaired_by_existing_unit_mass(self):
        source = tensor(LOCAL, reference(F(1, 2)))
        coupled = m.shared_couple(source)
        self.assertTrue(m.is_psd(coupled))
        self.assertEqual(m.joint_mass(coupled), 1)
        self.assertEqual(sum(m.joint_weights(coupled)), 1)
        self.assertTrue(all(weight >= 0 for weight in m.joint_weights(coupled)))
        self.assertFalse(m.joint_recordable(coupled, normalized=True))
        self.assertNotEqual(m.joint_cross(coupled, (0, 0), (1, 0)), 0)

    def test_joint_cross_constraints_leave_all_four_a_coordinates_and_exclude_two_c_coordinates(
        self,
    ):
        for t, expected_rank in ((F(1, 2), 2), (F(-1), 2), (F(0), 0)):
            columns = []
            for d in LOCAL_SPAN:
                output = apply_shared(tensor(d, reference(t)), U0, F(1, 2))
                columns.append(
                    tuple(
                        component
                        for left, right in CROSS_PAIRS
                        for component in cross(output, left, right)
                    )
                )
            self.assertEqual(rank(tuple(zip(*columns, strict=True))), expected_rank)
            self.assertEqual(tuple(columns[:4]), ((F(0),) * 12,) * 4)
        self.assertEqual(rank(tuple(flatten(d) for d in LOCAL_SPAN[:4])), 4)
        # A linear necessity certificate on the full local span, including
        # signed A and both complex-c directions; not just normalized examples.

    def test_zero_c_survives_with_psd_and_exact_total_mass(self):
        preparations = (
            A,
            scale(F(1, 4), eye(2)),
            matrix(((F(1, 2), 0), (0, 0))),
            scale(F(1, 4), matrix(((1, (0, 1)), ((0, -1), 1)))),
        )
        for a in preparations:
            for t in (F(-1), F(1, 2), F(1)):
                output = m.shared_couple(tensor(local(a), reference(t)))
                self.assertTrue(m.is_psd(output))
                self.assertTrue(m.joint_recordable(output, normalized=True))
                self.assertEqual(m.joint_mass(output), 1)
                self.assertEqual(m.joint_mass(output), 4 * trace(a)[0] * F(1, 2))
        b = scale(F(1, 4), add(eye(2), scale(F(1, 2), Z)))
        numerator = tensor(H0, P)
        conjugated = matrix(tuple(conj(entry) for entry in row) for row in numerator)
        for a in (zeros(2), A, scale(2, A)):
            output = apply_shared(tensor(local(a), reference(F(1, 2))), numerator, F(1, 2))
            self.assertTrue(m.is_psd(output))
            self.assertTrue(m.joint_recordable(output))
            self.assertEqual(m.joint_mass(output), 2 * trace(a)[0])
            grouped = untwist(output)
            common = block(grouped, 0, 0)
            for r, s in product(range(4), repeat=2):
                self.assertEqual(block(grouped, r, s), common if r == s else zeros(4))
            initial_quotient = tensor(scale(2, transpose(a)), scale(2, transpose(b)))
            expected_quotient = scale(
                F(1, 2), mm(mm(conjugated, initial_quotient), transpose(numerator))
            )
            self.assertEqual(scale(4, transpose(common)), expected_quotient)
        # This tests the general shared-congruence convention on supplied
        # matrices, not a new typed coupler or an availability assertion.

    def test_unpolarized_reference_cross_operator_is_central_for_every_shared_unitary(self):
        scalar = scale(F(1, 4), eye(4))
        units = tuple(
            matrix(tuple(int(i == r and j == s) for j in range(4)) for i in range(4))
            for r, s in product(range(4), repeat=2)
        )
        self.assertEqual(rank(tuple(flatten(d) for d in units)), 16)
        for unit in units:
            self.assertEqual(mm(unit, scalar), mm(scalar, unit))
        # Matrix units span all complex matrices; scalar centrality and
        # U U*=I give U scalar U*=scalar for every shared unitary.
        for numerator, factor in (
            (eye(4), F(1)),
            (U0, F(1, 2)),
            (SWAP, F(1)),
            (tensor(H0, P), F(1, 2)),
        ):
            self.assertEqual(scale(factor, mm(numerator, dagger(numerator))), eye(4))
            output = apply_shared(tensor(LOCAL, reference(0)), numerator, factor)
            self.assertTrue(m.joint_recordable(output, normalized=True))

    def test_raw_product_controls_and_cnot_alone_do_not_exclude_c(self):
        source = tensor(LOCAL, reference(F(1, 2)))
        for numerator, factor in (
            (tensor(H0, P), F(1, 2)),
            (tensor(P, H0), F(1, 2)),
            (tensor(Z, P), F(1)),
        ):
            output = apply_shared(source, numerator, factor)
            self.assertTrue(m.joint_recordable(output, normalized=True))
            off_diagonal = block(untwist(output), 0, 2)
            self.assertEqual(trace(off_diagonal), pair(C))
            self.assertNotEqual(off_diagonal, zeros(4))
        pure_b = scale(F(1, 4), add(eye(2), Z))
        cnot_only_reference = mm(mm(CNOT, tensor(eye(2), pure_b)), dagger(CNOT))
        self.assertEqual(cnot_only_reference, scale(F(1, 4), add(eye(4), tensor(Z, Z))))
        cnot_only = apply_shared(tensor(LOCAL, reference(1)), CNOT)
        self.assertTrue(m.joint_recordable(cnot_only, normalized=True))
        self.assertEqual(m.joint_mass(cnot_only), 1)
        self.assertEqual(tuple(pair(value) for value in m.joint_crossforms(cnot_only)), (ZERO,) * 6)
        self.assertEqual(trace(block(untwist(cnot_only), 0, 2)), pair(C))

    def test_arbitrary_shared_swap_need_not_preserve_total_entry_mass_off_domain(self):
        t = F(1, 2)
        source = tensor(LOCAL, reference(t))
        output = apply_shared(source, SWAP)
        self.assertTrue(m.is_psd(output))
        self.assertEqual(trace(output), (F(1), F(0)))
        self.assertEqual(cross(output, (0, 0), (1, 0)), times(t, C))
        self.assertEqual(cross(output, (0, 1), (1, 1)), times(t, C))
        self.assertEqual(m.joint_mass(output), 1 + 4 * t * C.real)
        self.assertNotEqual(m.joint_mass(output), 1)
        self.assertFalse(m.joint_recordable(output))

    def test_reference_parameter_and_orientation_are_explicit_not_inferred_purity(self):
        for t in (F(-1), F(0), F(1, 2), F(1)):
            state = m.ReferenceState(t)
            self.assertEqual(state.residual, reference(t))
            b, c = m.decompose_candidate(state.residual, normalized=True)
            self.assertEqual(c, 0)
            self.assertEqual(b, scale(F(1, 4), add(eye(2), scale(t, Z))))
            rho = m.q_quantum(state.residual)
            self.assertEqual(trace(mm(rho, rho))[0], (1 + t * t) / 2)
            self.assertEqual(state.orientation, "Z")
        # t=+/-1 makes the reference QUOTIENT pure; the full four-label
        # kernel still retains both local record cells.
        for t in (-1, 1):
            self.assertEqual(
                rank(tuple(tuple(entry.real for entry in row) for row in m.reference_kernel(t))), 2
            )

    def test_preparation_keeps_independence_as_a_declared_named_premise(self):
        source = initial_source(C, records=True)
        self.assertEqual(source.residual, tensor(source.local.residual, source.reference.residual))
        self.assertEqual(source.independence.origins, ("local-run", "reference-run"))
        self.assertEqual(source.joint_origin, "joint-run")
        self.assertEqual(source.coupler, m.IDENTITY_COUPLER)
        self.assertEqual(source.local.records[0].payload, (("sample", "left"),))
        self.assertEqual(source.reference.records[0].payload, (("sample", "right"),))
        self.assertEqual(source.local.records[0].event_id, source.reference.records[0].event_id)

    def test_full_joint_record_retains_reference_coupler_permutation_and_both_histories(self):
        initial = initial_source(records=True)
        source = m.promote_joint(m.couple_state(initial))
        _, terminal = m.commit_joint(source, (0, 0))
        record = terminal.record
        self.assertEqual(record.origin, "joint-run")
        self.assertEqual(record.event_id, 0)
        self.assertEqual(record.outcome, (0, 0))
        self.assertEqual(record.action, "terminal_joint_cell_cut")
        self.assertEqual(record.coupler, m.SHARED_COUPLER)
        self.assertEqual(record.reference_t, F(1, 2))
        self.assertEqual(record.reference_orientation, "Z")
        self.assertEqual(record.input_origins, ("local-run", "reference-run"))
        self.assertEqual(record.local_records, initial.local.records)
        self.assertEqual(record.reference_records, initial.reference.records)
        self.assertEqual(record.independence, initial.independence)
        self.assertEqual(record.permutation, m.NATIVE_TO_GROUPED)
        self.assertEqual(
            record.precursor, (("local-run", 0), ("local-run", 1), ("reference-run", 0))
        )
        self.assertEqual(terminal.records, (record,))
        self.assertIs(terminal.source, source)

    def test_all_positive_joint_branches_keep_full_native_literal_outputs_and_mass(self):
        source = m.promote_joint(m.couple_state(initial_source()))
        probabilities = []
        for outcome in CELLS:
            probability, terminal = m.commit_joint(source, outcome)
            indices = cell_indices(outcome)
            raw = matrix(
                tuple(
                    source.residual[i][j] if i in indices and j in indices else 0 for j in range(16)
                )
                for i in range(16)
            )
            self.assertGreater(probability, 0)
            self.assertEqual(probability, mass(raw))
            self.assertEqual(terminal.residual, scale(1 / probability, raw))
            self.assertEqual(len(terminal.residual), 16)
            self.assertEqual(m.joint_mass(terminal.residual), 1)
            self.assertTrue(m.is_psd(terminal.residual))
            self.assertEqual(
                m.joint_weights(terminal.residual), tuple(F(int(cell == outcome)) for cell in CELLS)
            )
            probabilities.append(probability)
        self.assertEqual(tuple(probabilities), m.joint_weights(source.residual))
        self.assertEqual(sum(probabilities), 1)

    def test_normalized_illegal_prospective_output_cannot_be_promoted_or_committed(self):
        initial = initial_source(C)
        prospective = m.couple_state(initial)
        self.assertEqual(m.joint_mass(prospective.residual), 1)
        self.assertEqual(prospective.coupler, m.SHARED_COUPLER)
        self.assertEqual(prospective.local, initial.local)
        self.assertEqual(prospective.reference, initial.reference)
        with self.assertRaises(ValueError):
            m.promote_joint(prospective)
        for outcome in CELLS:
            with self.assertRaises(TypeError):
                m.commit_joint(prospective, outcome)
        with self.assertRaises(TypeError):
            m.couple_state(prospective)
        self.assertEqual(prospective.residual, m.shared_couple(initial.residual))

    def test_unpolarized_typed_source_and_raw_product_countermodel_retain_c(self):
        initial = initial_source(C, 0)
        source = m.promote_joint(m.couple_state(initial))
        self.assertEqual(source.local.residual, local(A, C))
        self.assertEqual(source.coupler, m.SHARED_COUPLER)
        self.assertEqual(m.joint_mass(source.residual), 1)
        self.assertTrue(m.joint_recordable(source.residual, normalized=True))
        polarized = initial_source(C, F(1, 2))
        raw_product = m.couple(polarized.residual, m.PRODUCT_COUPLER)
        self.assertTrue(m.joint_recordable(raw_product, normalized=True))
        with self.assertRaises(ValueError):
            m.couple_state(polarized, m.PRODUCT_COUPLER)

    def test_terminal_outputs_have_no_registered_joint_source_or_coupler_reuse(self):
        source = m.promote_joint(m.couple_state(initial_source()))
        _, terminal = m.commit_joint(source, (0, 0))
        with self.assertRaises(TypeError):
            m.commit_joint(terminal, (0, 0))
        with self.assertRaises(TypeError):
            m.couple_state(terminal)
        with self.assertRaises(TypeError):
            m.promote_joint(terminal)
        with self.assertRaises(ValueError):
            m.couple_state(source)

    def test_zero_weight_nonzero_literal_cut_refuses_without_append_or_normalization(self):
        a = matrix(((F(1, 2), 0), (0, 0)))
        source = m.promote_joint(m.couple_state(initial_source(0, F(1), records=True, a=a)))
        self.assertEqual(m.joint_weights(source.residual), (F(1, 2), 0, F(1, 2), 0))
        raw = m.joint_cut(source.residual, (0, 1))
        self.assertNotEqual(raw, zeros(16))
        self.assertTrue(m.is_psd(raw))
        self.assertEqual(m.joint_mass(raw), 0)
        histories = source.local.records, source.reference.records
        with self.assertRaises(ValueError):
            m.commit_joint(source, (0, 1))
        self.assertEqual((source.local.records, source.reference.records), histories)
        self.assertEqual(m.joint_mass(source.residual), 1)

    def test_missing_mismatched_or_non_distinct_independence_origins_are_rejected(self):
        source = initial_source()
        with self.assertRaises(TypeError):
            m.prepare_joint(source.local, source.reference, None)
        with self.assertRaises(ValueError):
            m.prepare_joint(source.local, source.reference, m.Independence(("local-run", "other")))
        with self.assertRaises(ValueError):
            m.Independence(("same", "same"))
        with self.assertRaises(ValueError):
            m.prepare_joint(
                source.local, source.reference, source.independence, joint_origin="local-run"
            )

    def test_unavailable_couplers_reference_orientation_and_invalid_values_are_rejected(self):
        for t in (F(-2), F(2)):
            with self.assertRaises(ValueError):
                m.ReferenceState(t)
        for t in (True, 0.5):
            with self.assertRaises(TypeError):
                m.ReferenceState(t)
        with self.assertRaises(ValueError):
            m.ReferenceState(1, orientation="X")
        source = initial_source()
        for name in ("SWAP", "unknown", m.IDENTITY_COUPLER, m.PRODUCT_COUPLER):
            with self.assertRaises(ValueError):
                m.couple_state(source, name)
        for outcome in ((True, 0), (0, 2), [0, 0], (0,)):
            with self.assertRaises(ValueError):
                m.commit_joint(source, outcome)

    def test_one_shot_full_kernel_rows_are_canonicalized_once(self):
        source = tensor(LOCAL, reference(F(1, 2)))

        def rows():
            return ((entry for entry in row) for row in source)

        self.assertEqual(m.to_untwisted(rows()), m.to_untwisted(source))
        self.assertEqual(m.joint_crossforms(rows()), m.joint_crossforms(source))
        self.assertEqual(m.joint_weights(rows()), m.joint_weights(source))
        self.assertEqual(m.shared_couple(rows()), m.shared_couple(source))
        self.assertEqual(m.joint_recordable(rows()), m.joint_recordable(source))
        prospective = m.couple_state(initial_source())
        copied = replace(prospective, permutation=(value for value in m.NATIVE_TO_GROUPED))
        self.assertEqual(copied.permutation, m.NATIVE_TO_GROUPED)
        _, terminal = m.commit_joint(m.promote_joint(copied), (0, 0))
        record = replace(terminal.record, permutation=(value for value in m.NATIVE_TO_GROUPED))
        self.assertEqual(record.permutation, m.NATIVE_TO_GROUPED)
        self.assertEqual(replace(terminal, record=record), terminal)
        for equivalent in (
            tuple(float(value) for value in m.NATIVE_TO_GROUPED),
            tuple(bool(value) if value in (0, 1) else value for value in m.NATIVE_TO_GROUPED),
        ):
            # Numeric-equivalent metadata stays accepted, including one-shot
            # inputs, but both containers store only canonical built-in ints.
            snapshot = replace(prospective, permutation=iter(equivalent))
            record = replace(terminal.record, permutation=iter(equivalent))
            for stored in (snapshot.permutation, record.permutation):
                self.assertIs(stored, m.NATIVE_TO_GROUPED)
                self.assertTrue(all(type(value) is int for value in stored))
            self.assertEqual(replace(terminal, record=record), terminal)

    def test_independent_histories_remain_immutable_without_cross_origin_ordering(self):
        source = initial_source(records=True)
        precursor = m.full_precursor(source)
        self.assertEqual(len(precursor), 3)
        self.assertEqual(len(set(precursor)), 3)
        self.assertIn(("local-run", 0), precursor)
        self.assertIn(("reference-run", 0), precursor)
        self.assertEqual(source.local.records[1].precursor, (0,))
        self.assertEqual(source.reference.records[0].precursor, ())
        with self.assertRaises(FrozenInstanceError):
            source.local.records[0].outcome = "changed"
        _, terminal = m.commit_joint(source, (0, 0))
        with self.assertRaises(FrozenInstanceError):
            terminal.record.reference_t = 0
        self.assertEqual(terminal.record.local_records, source.local.records)
        self.assertEqual(terminal.record.reference_records, source.reference.records)

    def test_terminal_record_and_support_validation_rejects_changed_metadata(self):
        source = m.promote_joint(m.couple_state(initial_source(records=True)))
        _, terminal = m.commit_joint(source, (0, 0))
        with self.assertRaises(ValueError):
            replace(terminal, record=replace(terminal.record, reference_t=F(-1, 2)))
        with self.assertRaises(ValueError):
            replace(terminal.record, precursor=terminal.record.precursor[:-1])
        with self.assertRaises(ValueError):
            replace(terminal, residual=source.residual)
        with self.assertRaises(ValueError):
            replace(terminal.record, permutation=tuple(range(16)))
        alternative = matrix(tuple(int(i == j == 0) for j in range(16)) for i in range(16))
        self.assertEqual(m.joint_mass(alternative), 1)
        self.assertEqual(m.joint_cut(alternative, (0, 0)), alternative)
        self.assertNotEqual(alternative, terminal.residual)
        with self.assertRaises(ValueError):
            replace(terminal, residual=alternative)
        pure_a = matrix(((F(1, 2), 0), (0, 0)))
        zero_source = m.promote_joint(m.couple_state(initial_source(0, 1, a=pure_a)))
        _, genuine = m.commit_joint(zero_source, (0, 0))
        impossible_record = replace(genuine.record, outcome=(0, 1))
        supported_index = native(0, 0, 1, 0)
        impossible_residual = matrix(
            tuple(int(i == j == supported_index) for j in range(16)) for i in range(16)
        )
        self.assertEqual(m.joint_mass(impossible_residual), 1)
        self.assertEqual(m.joint_cut(impossible_residual, (0, 1)), impossible_residual)
        with self.assertRaises(ValueError):
            m.TerminalState(impossible_residual, zero_source, impossible_record)

    def test_metadata_validation_is_not_a_global_trajectory_or_independence_proof(self):
        initial = initial_source(C, records=True)
        # A separately supplied lawful snapshot need not equal the trajectory
        # generated by its retained input metadata. Constructors check grammar;
        # prepare_joint/couple_state are the actual forward transformation.
        other_residual = tensor(local(A), reference(F(1, 2)))
        snapshot = m.ProspectiveState(
            other_residual, initial.local, initial.reference, initial.independence
        )
        self.assertNotEqual(snapshot.residual, initial.residual)
        self.assertEqual(snapshot.local.residual, initial.local.residual)
        self.assertTrue(m.joint_recordable(snapshot.residual, normalized=True))
        with self.assertRaises(ValueError):
            m.LocalState(local(A), records=(m.InputRecord(1, "read", "outcome"),))
        with self.assertRaises(ValueError):
            m.InputRecord(1, "read", "outcome", precursor=(1,))
        with self.assertRaises(ValueError):
            replace(initial, permutation=tuple(range(16)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
