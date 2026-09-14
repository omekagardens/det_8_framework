"""Independent exact certificates for the fixed finite composition contract.

The oracle uses Gaussian Fraction pairs and the full native sixteen-label
kernel. It does not call the accepted branch, coupling, cut, command or read
arithmetic. Finite witnesses supplement the conditional composition proof;
they do not establish physical availability or preparations.
"""

import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F
from itertools import product

import finite_protocol as m

ZERO = (F(0), F(0))
CELLS = tuple(product((0, 1), repeat=2))
BITS = tuple(product((0, 1), repeat=4))
READS = tuple((a, b, sign) for a, b in CELLS for sign in ("+", "-"))


def pair(value):
    if isinstance(value, tuple):
        return value
    if hasattr(value, "imag") and hasattr(value, "real"):
        return F(value.real), F(value.imag)
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


def mat(rows):
    return tuple(tuple(pair(value) for value in row) for row in rows)


def eye(n):
    return mat(tuple(int(i == j) for j in range(n)) for i in range(n))


def zero(n):
    return mat((0,) * n for _ in range(n))


def add(*operators):
    return mat(
        tuple(total(op[i][j] for op in operators) for j in range(len(operators[0][0])))
        for i in range(len(operators[0]))
    )


def scale(coefficient, operator):
    return mat(tuple(times(coefficient, entry) for entry in row) for row in operator)


def transpose(operator):
    return tuple(tuple(row[j] for row in operator) for j in range(len(operator[0])))


def dagger(operator):
    return mat(tuple(conj(row[j]) for row in operator) for j in range(len(operator[0])))


def mm(left, right):
    return mat(
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


def congruence(operator, residual):
    return mm(mm(operator, residual), dagger(operator))


def tensor(left, right):
    return mat(
        tuple(
            times(left[a][b], right[i][j])
            for b in range(len(left[0]))
            for j in range(len(right[0]))
        )
        for a in range(len(left))
        for i in range(len(right))
    )


def tr(operator):
    return total(operator[i][i] for i in range(len(operator)))


def to_api(operator, module):
    return tuple(tuple(module.G(*pair(entry)) for entry in row) for row in operator)


I2 = eye(2)
X = mat(((0, 1), (1, 0)))
Y = mat(((0, (0, -1)), ((0, 1), 0)))
Z = mat(((1, 0), (0, -1)))
H0 = mat(((1, 1), (1, -1)))
CNOT = mat(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)))
U0 = mm(tensor(I2, H0), CNOT)
UA = add(scale(F(3, 5), I2), scale((0, F(-4, 5)), X))
QP = scale(F(1, 10), mat(((9, 3), (3, 1))))
QM = add(I2, scale(-1, QP))
T = F(3, 5)
REF_A = scale(F(1, 4), add(I2, scale(T, Z)))


def local_kernel(rho, c=0):
    a = scale(F(1, 2), transpose(rho))
    blocks = ((a, scale(c, Z)), (scale(conj(c), Z), congruence(Z, a)))
    return mat(tuple(blocks[i // 2][j // 2][i % 2][j % 2] for j in range(4)) for i in range(4))


def local_rho(kernel):
    return scale(2, transpose(tuple(tuple(kernel[i][j] for j in range(2)) for i in range(2))))


def native_index(a, i, b, j):
    return 8 * a + 4 * i + 2 * b + j


def grouped_blocks(native):
    return tuple(
        tuple(
            mat(
                tuple(
                    times(
                        (-1) ** (a * i + b * j + c * k + d * ell),
                        native[native_index(a, i, b, j)][native_index(c, k, d, ell)],
                    )
                    for k, ell in CELLS
                )
                for i, j in CELLS
            )
            for c, d in CELLS
        )
        for a, b in CELLS
    )


def native_from_blocks(blocks):
    result = [[ZERO for _ in range(16)] for _ in range(16)]
    for a, i, b, j in BITS:
        for c, k, d, ell in BITS:
            result[native_index(a, i, b, j)][native_index(c, k, d, ell)] = times(
                (-1) ** (a * i + b * j + c * k + d * ell),
                blocks[2 * a + b][2 * c + d][2 * i + j][2 * k + ell],
            )
    return mat(result)


def coupled_native(local):
    reference = local_kernel(scale(2, REF_A))
    blocks = grouped_blocks(tensor(local, reference))
    return native_from_blocks(
        tuple(tuple(scale(F(1, 2), congruence(U0, block)) for block in row) for row in blocks)
    )


def cut_native(native, cell):
    retained = {native_index(cell[0], i, cell[1], j) for i, j in CELLS}
    return mat(
        tuple(native[i][j] if i in retained and j in retained else ZERO for j in range(16))
        for i in range(16)
    )


def native_mass(native):
    return total(entry for row in native for entry in row)[0]


def recovered_cell_rho(native, cell):
    block = grouped_blocks(native)[2 * cell[0] + cell[1]][2 * cell[0] + cell[1]]
    uncoupled = scale(F(1, 2), congruence(dagger(U0), block))
    partial = mat(
        tuple(total(uncoupled[2 * i + j][2 * k + j] for j in (0, 1)) for k in (0, 1))
        for i in (0, 1)
    )
    return scale(4, transpose(partial))


def image_one(rho, cell):
    blocks = [[zero(4) for _ in CELLS] for _ in CELLS]
    block = scale(F(1, 4), congruence(U0, tensor(transpose(rho), REF_A)))
    blocks[2 * cell[0] + cell[1]][2 * cell[0] + cell[1]] = block
    return native_from_blocks(blocks)


def filter_for(cell, inverse=False):
    entries = (2, 1) if cell[1] == 0 else (1, 2)
    if inverse:
        entries = tuple(F(1, value) for value in entries)
    return mat(((entries[0], 0), (0, entries[1])))


def command_native(native, cell):
    if cell[0] == 0:
        return native
    rho = recovered_cell_rho(native, cell)
    operator = mm(mm(filter_for(cell, inverse=True), UA), filter_for(cell))
    return image_one(congruence(operator, rho), cell)


def terminal_weight(native, outcome):
    cell, sign = outcome[:2], outcome[2]
    rho = recovered_cell_rho(native, cell)
    filtered = scale(F(1, 10), congruence(filter_for(cell), rho))
    return tr(mm(QP if sign == "+" else QM, filtered))[0]


def independent_law(initial, beta):
    """Return unnormalized native stages and all 66 separate scalar labels."""
    rho = local_rho(initial)
    result = {}
    stages = {}
    for r in (0, 1):
        projector = scale(F(1, 2), add(I2, scale((-1) ** r, Y)))
        p = tr(mm(rho, projector))[0]
        branch = scale(p, local_kernel(projector))
        controlled = local_kernel(scale(p, congruence(Z, projector)))
        joint = coupled_native(controlled)
        stages[r] = (p, branch, controlled, joint)
        result[(r, "unavailable")] = (1 - beta) * p
        for cell in CELLS:
            cut = cut_native(joint, cell)
            commanded = command_native(cut, cell)
            stages[r, cell] = (cut, commanded)
            for outcome in READS:
                result[(r, "ready", cell, outcome)] = beta * terminal_weight(commanded, outcome)
    return result, stages


def coordinate_key(label):
    if label.reference_outcome == "unavailable":
        return label.local_outcome, "unavailable"
    return label.local_outcome, "ready", label.cut_outcome, label.terminal_outcome


class FiniteCompositionChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.boundary = m.primary_boundary()
        cls.law = m.primary_law()
        cls.read = m.i.TerminalReadPremise()
        cls.protocol = m.run_protocol(cls.boundary, cls.law, cls.read)
        cls.initial = mat(cls.boundary.source.residual)
        cls.expected, cls.stages = independent_law(cls.initial, F(2, 3))
        cls.terminals = {
            coordinate_key(leaf.label): leaf
            for leaf in cls.protocol.leaves
            if type(leaf) is m.WeightedTerminal
        }
        cls.lts = {
            r: cls.terminals[r, "ready", (0, 0), (0, 0, "+")].commands.cut.source for r in (0, 1)
        }

    def test_original_full_complex_input_is_retained_without_projection(self):
        rho = scale(F(1, 2), add(I2, scale(F(3, 5), Y)))
        self.assertEqual(self.initial, local_kernel(rho, F(1, 20)))
        self.assertNotEqual(self.initial, local_kernel(rho))
        self.assertEqual(tr(rho), pair(1))
        self.assertEqual(self.initial[0][3], ZERO)
        self.assertEqual(self.initial[0][2], pair(F(1, 20)))
        self.assertEqual(self.initial[0][1], pair((0, F(3, 20))))
        self.assertEqual(self.boundary.source.records, ())
        self.assertEqual(self.boundary.source.settings, ())
        self.assertEqual(self.boundary.root_weight, 1)

    def test_all_66_full_coordinates_equal_independent_unnormalized_native_law(self):
        observed = {
            coordinate_key(entry.label): entry.weight for entry in self.protocol.coordinates
        }
        self.assertEqual(len(self.protocol.coordinates), 66)
        self.assertEqual(len(observed), 66)
        self.assertEqual(observed, self.expected)
        self.assertEqual(sum(observed.values()), 1)
        self.assertEqual(self.protocol.total, 1)
        self.assertEqual(
            self.protocol.probabilities,
            tuple((entry.label, entry.weight) for entry in self.protocol.coordinates),
        )

    def test_sixteen_positive_reads_two_stops_and_48_unselected_zero_coordinates(self):
        reads = [
            entry for entry in self.protocol.coordinates if entry.label.reference_outcome == "ready"
        ]
        stops = [
            entry
            for entry in self.protocol.coordinates
            if entry.label.reference_outcome == "unavailable"
        ]
        self.assertEqual(sum(entry.weight > 0 for entry in reads), 16)
        self.assertEqual(sum(entry.weight == 0 for entry in reads), 48)
        self.assertEqual([entry.weight for entry in stops], [F(4, 15), F(1, 15)])
        self.assertEqual(sum(entry.weight for entry in reads), F(2, 3))
        self.assertEqual(len(self.protocol.leaves), 18)
        for entry in self.protocol.coordinates:
            self.assertEqual(entry.selected is None, entry.weight == 0)
        self.assertEqual(
            tuple(entry.selected for entry in self.protocol.coordinates if entry.weight > 0),
            self.protocol.leaves,
        )

    def test_exact_conditional_table_including_complex_y_orientation(self):
        plus_probabilities = (
            (F(37, 50), F(13, 50), F(157, 1250), F(13, 50)),
            (F(37, 50), F(13, 50), F(37, 50), F(1093, 1250)),
        )
        for r, p in enumerate((F(4, 5), F(1, 5))):
            for cell, probability in zip(CELLS, plus_probabilities[r], strict=True):
                with self.subTest(local=r, cell=cell):
                    positive = self.expected[r, "ready", cell, (*cell, "+")]
                    negative = self.expected[r, "ready", cell, (*cell, "-")]
                    self.assertEqual(positive, p * probability / 6)
                    self.assertEqual(negative, p * (1 - probability) / 6)
        self.assertEqual(
            sum(
                value for key, value in self.expected.items() if len(key) == 4 and key[3][2] == "+"
            ),
            F(2549, 9375),
        )

    def test_native_cut_completeness_and_record_dependent_command_mass(self):
        for r in (0, 1):
            p, _, _, joint = self.stages[r]
            cuts = []
            for cell in CELLS:
                cut, commanded = self.stages[r, cell]
                cuts.append(cut)
                self.assertEqual(native_mass(cut), p / 4)
                self.assertEqual(native_mass(commanded), p / 4)
                self.assertEqual(
                    sum(terminal_weight(commanded, outcome) for outcome in READS), p / 4
                )
                self.assertEqual(commanded == cut, cell[0] == 0)
            self.assertEqual(add(*cuts), joint)
            self.assertEqual(native_mass(joint), p)

    def test_native_index_conversion_and_inverse_keep_every_complex_component(self):
        for r in (0, 1):
            p, _, controlled, joint = self.stages[r]
            self.assertEqual(native_from_blocks(grouped_blocks(joint)), joint)
            self.assertEqual(len(joint), 16)
            self.assertTrue(all(len(row) == 16 for row in joint))
            self.assertTrue(any(imag for row in joint for _, imag in row))
            for cell in CELLS:
                self.assertEqual(recovered_cell_rho(joint, cell), local_rho(controlled))
                expected = scale(p / 2, add(I2, scale(-((-1) ** r), Y)))
                self.assertEqual(recovered_cell_rho(joint, cell), expected)

    def test_unnormalized_native_effects_are_linear_and_mass_complete(self):
        # A finite exact witness of the proof's homogeneous extension, not a
        # claim that the normalized executable boundary accepts unnormalized x.
        center = local_kernel(scale(F(1, 2), I2), (F(1, 8), F(1, 16)))
        small = scale(F(2, 7), center)
        law_center, _ = independent_law(center, F(2, 3))
        law_small, _ = independent_law(small, F(2, 3))
        law_sum, _ = independent_law(add(self.initial, small), F(2, 3))
        for key in self.expected:
            self.assertEqual(law_small[key], F(2, 7) * law_center[key])
            self.assertEqual(law_sum[key], self.expected[key] + law_small[key])
        self.assertEqual(sum(law_sum.values()), F(9, 7))

    def test_zero_local_branch_keeps_scalar_coordinates_without_selected_history(self):
        boundary = m.zero_local_boundary()
        run = m.run_protocol(boundary, self.law, self.read)
        expected, stages = independent_law(mat(boundary.source.residual), F(2, 3))
        self.assertEqual(
            {coordinate_key(entry.label): entry.weight for entry in run.coordinates}, expected
        )
        self.assertEqual(len(run.coordinates), 66)
        self.assertEqual(run.total, 1)
        zero_outcome = next(r for r in (0, 1) if stages[r][0] == 0)
        self.assertEqual(stages[zero_outcome][1], zero(4))
        self.assertEqual(sum(entry.selected is not None for entry in run.coordinates), 9)
        for entry in run.coordinates:
            if entry.label.local_outcome == zero_outcome:
                self.assertEqual(entry.weight, 0)
                self.assertIsNone(entry.selected)
        with self.assertRaises(ValueError):
            m.WeightedLocal(boundary, zero_outcome)

    def test_complete_reference_law_endpoints_do_not_fabricate_zero_selections(self):
        for ready in (F(0), F(1)):
            law = replace(self.law, ready=ready, unavailable=1 - ready)
            run = m.run_protocol(self.boundary, law, self.read)
            expected, _ = independent_law(self.initial, ready)
            self.assertEqual(
                {coordinate_key(entry.label): entry.weight for entry in run.coordinates}, expected
            )
            self.assertEqual(len(run.coordinates), 66)
            self.assertEqual(run.total, 1)
            self.assertEqual(len(run.leaves), 2 if ready == 0 else 16)
            absent = "ready" if ready == 0 else "unavailable"
            with self.assertRaises(ValueError):
                m.ReferenceDecision(law, absent)

    def test_module_aliases_bind_the_same_original_instances_and_distinct_classes(self):
        self.assertIs(m.bridge.c, m.c)
        self.assertIs(m.bridge.d, m.d)
        self.assertIsNot(m.c.G, m.d.G)
        self.assertIsNot(m.d.G, m.i.G)
        self.assertIsNot(m.c.State, m.i.State)
        self.assertEqual(m.c.__name__, "local_source")
        self.assertEqual(m.d.__name__, "joint_source")
        self.assertEqual(m.bridge.__name__, "local_joint_adapter")
        self.assertEqual(m.i.__name__, "terminal_read_source")

    def test_boundary_requires_normalized_empty_fixed_snapshot_and_root_one(self):
        for weight in (F(0), F(2, 3), 2, True, 1.0, "1"):
            with self.subTest(weight=weight), self.assertRaises((TypeError, ValueError)):
                m.Boundary(self.boundary.source, weight)
        _, selected = m.c.commit_pauli(self.boundary.source, "Y", 0)
        pending = m.c.run_control(self.boundary.source, "Z")
        for state in (selected, pending):
            with self.assertRaises(ValueError):
                m.Boundary(state)
        forged = replace(self.boundary.source)
        object.__setattr__(forged, "residual", to_api(scale(2, self.initial), m.c))
        with self.assertRaises(ValueError):
            m.Boundary(forged)
        for field, value in (("controller", "other"), ("frame", "other"), ("source_kind", "other")):
            forged = replace(self.boundary.source)
            object.__setattr__(forged, field, value)
            with self.subTest(field=field), self.assertRaises(ValueError):
                m.Boundary(forged)

    def test_reference_law_requires_both_exact_complete_independent_weights(self):
        for ready, unavailable in ((F(2, 3), F(1, 2)), (-1, 2), (2, -1), (0, 0)):
            with self.subTest(ready=ready, unavailable=unavailable), self.assertRaises(ValueError):
                replace(self.law, ready=ready, unavailable=unavailable)
        for invalid in (True, 0.5, "2/3", None):
            with self.subTest(invalid=invalid), self.assertRaises((TypeError, ValueError)):
                replace(self.law, ready=invalid)
        for field, value in (
            ("preparation_id", ""),
            ("law_id", " bad"),
            ("preparation_available", False),
            ("preparation_available", 1),
            ("independence", m.d.Independence(("reference", "signal"))),
            ("independence", ("signal", "reference")),
        ):
            with self.subTest(field=field, value=value), self.assertRaises((TypeError, ValueError)):
                replace(self.law, **{field: value})
        with self.assertRaises(TypeError):
            m.ReferenceLaw(ready=F(2, 3))

    def test_positive_reference_decisions_retain_one_actual_independent_record(self):
        for outcome, probability in (("ready", F(2, 3)), ("unavailable", F(1, 3))):
            decision = m.ReferenceDecision(self.law, outcome)
            self.assertEqual(decision.probability, probability)
            self.assertEqual(decision.record.event_id, 0)
            self.assertEqual(decision.record.action, "reference_select_prepare")
            self.assertEqual(decision.record.outcome, outcome)
            self.assertEqual(decision.record.precursor, ())
            if outcome == "ready":
                self.assertEqual(decision.reference.t, F(3, 5))
                self.assertEqual(decision.reference.orientation, "Z")
                self.assertEqual(decision.reference.origin, "reference")
                self.assertEqual(decision.reference.records, (decision.record,))
            else:
                self.assertIsNone(decision.reference)
        for outcome in ("missing", " ready", 0, True):
            with self.assertRaises((TypeError, ValueError)):
                m.ReferenceDecision(self.law, outcome)

    def test_fixed_terminal_read_premise_required_even_when_ready_weight_is_zero(self):
        law = replace(self.law, ready=F(0), unavailable=F(1))
        for supplied in (None, True, "calibrated", self.boundary.source):
            with self.assertRaises((TypeError, ValueError)):
                m.run_protocol(self.boundary, law, supplied)
        for field, value in (("available", False), ("calibration", "unknown"), ("setting_id", "")):
            forged = replace(self.read)
            object.__setattr__(forged, field, value)
            with self.subTest(field=field), self.assertRaises((TypeError, ValueError)):
                m.run_protocol(self.boundary, law, forged)

    def test_strict_outcome_types_and_whole_labels_are_not_probability_aliases(self):
        sample = self.protocol.coordinates[0].label
        for outcome in (True, 0.0, F(0), -1, 2, "0"):
            with self.subTest(outcome=outcome), self.assertRaises((TypeError, ValueError)):
                replace(sample, local_outcome=outcome)
        for cell in ((True, 0), (0, F(0)), (0,), "00"):
            with self.subTest(cell=cell), self.assertRaises((TypeError, ValueError)):
                replace(sample, cut_outcome=cell)
        for outcome in ((0, 0), (0, 0, 1), (0, 0, "+", "extra"), (0, True, "+")):
            with self.assertRaises((TypeError, ValueError)):
                replace(sample, terminal_outcome=outcome)
        with self.assertRaises((TypeError, ValueError)):
            replace(sample, command_word=("B",))
        identical_weights = [
            entry.label for entry in self.protocol.coordinates if entry.weight == F(13, 375)
        ]
        self.assertGreater(len(identical_weights), 1)
        self.assertEqual(len(set(identical_weights)), len(identical_weights))

    def test_exact_initial_rows_can_be_one_shot_without_losing_complex_entries(self):
        generated = (iter(row) for row in self.boundary.source.residual)
        state = m.c.State(generated)
        boundary = m.Boundary(state)
        self.assertEqual(mat(boundary.source.residual), self.initial)
        self.assertIs(boundary.source, state)
        self.assertEqual(boundary.source.records, ())
        self.assertEqual(boundary.source.settings, ())

    def test_actual_api_factors_and_full_raw_payloads_match_each_native_stage(self):
        for r in (0, 1):
            lt = self.lts[r]
            joint, local = lt.joint, lt.joint.local
            p, raw_branch, controlled, raw_joint = self.stages[r]
            self.assertIs(local.boundary, self.boundary)
            self.assertEqual(local.probability, p)
            self.assertEqual(local.weight, p)
            self.assertEqual(scale(p, mat(local.committed.residual)), raw_branch)
            self.assertEqual(scale(p, mat(local.state.residual)), controlled)
            self.assertEqual(mat(local.unnormalized), controlled)
            self.assertEqual(scale(p, mat(joint.source.target.residual)), raw_joint)
            self.assertEqual(mat(lt.state.residual), mat(joint.source.target.residual))
            self.assertEqual(joint.weight, p * F(2, 3))
            self.assertEqual(lt.weight, joint.weight)
            self.assertIs(joint.source.context.local_source, local.state)
            self.assertEqual(
                m.i.inverse_k_span(lt.state.residual, T),
                to_api(local_rho(controlled), m.i)
                if p == 1
                else to_api(scale(1 / p, local_rho(controlled)), m.i),
            )
            for cell in CELLS:
                leaf = self.terminals[r, "ready", cell, (*cell, "+")]
                commands, cut = leaf.commands, leaf.commands.cut
                raw_cut, raw_command = self.stages[r, cell]
                self.assertIs(cut.source, lt)
                self.assertEqual(cut.probability, F(1, 4))
                self.assertEqual(scale(p, mat(cut.unnormalized)), raw_cut)
                self.assertEqual(scale(p / 4, mat(cut.state.residual)), raw_cut)
                self.assertEqual(scale(p / 4, mat(commands.state.residual)), raw_command)
                self.assertEqual(commands.weight, p / 6)
                self.assertEqual(
                    leaf.probability, terminal_weight(raw_command, leaf.outcome) / (p / 4)
                )
                self.assertEqual(leaf.weight, p * F(2, 3) * cut.probability * leaf.probability)

    def test_lossless_conversion_retains_all_origins_inputs_and_original_local_word(self):
        expected_permutation = tuple(8 * a + 4 * b + 2 * i + j for a, i, b, j in BITS)
        for r, lt in self.lts.items():
            joint, context = lt.joint, lt.state.context
            local = joint.local
            original = joint.source.context
            self.assertEqual(local.state.settings, ("Z",))
            self.assertEqual(local.committed.settings, ())
            self.assertIs(local.state.records, local.committed.records)
            self.assertEqual(lt.state.pending, ())
            self.assertEqual(lt.state.records, ())
            self.assertEqual(context.local.origin, "signal")
            self.assertEqual(context.reference.origin, "reference")
            self.assertEqual(context.joint_origin, "joint")
            self.assertEqual(context.independence.origins, ("signal", "reference"))
            self.assertEqual(context.permutation, expected_permutation)
            self.assertEqual(context.coupler, "shared_CNOT_H2")
            self.assertEqual(context.frame, m.i.FRAME)
            self.assertEqual(context.controller, m.i.CONTROLLER)
            self.assertEqual(context.setting_id, m.i.NOMINAL_CUT)
            self.assertIs(context.terminal_read, self.read)
            self.assertEqual(mat(context.local.residual), mat(original.local_input.residual))
            self.assertEqual(mat(context.reference.residual), mat(original.reference.residual))
            for old, new in zip(original.local_input.records, context.local.records, strict=True):
                self.assertEqual(
                    (
                        new.event_id,
                        new.action,
                        new.outcome,
                        new.settings,
                        new.payload,
                        new.precursor,
                    ),
                    (
                        old.event_id,
                        old.action,
                        old.outcome,
                        old.settings,
                        old.payload,
                        old.precursor,
                    ),
                )
            self.assertEqual(
                context.local.records[0].payload,
                (
                    ("ri08c.axis", "Y"),
                    ("ri08c.controller", m.c.CONTROLLER),
                    ("ri08c.source_kind", m.c.SOURCE_KIND),
                    ("ri08c.frame", m.c.FRAME),
                ),
            )
            self.assertEqual(context.local.records[0].outcome, str(r))
            self.assertEqual(context.local.records[0].precursor, ())
            self.assertEqual(context.reference.records[0].precursor, ())
            self.assertEqual(original.local_source.settings, ("Z",))
            self.assertIs(original.local_source, local.state)
            self.assertIs(local.boundary.source, self.boundary.source)

    def test_full_cut_and_terminal_records_have_precursors_without_extra_conversion_event(self):
        for leaf in self.terminals.values():
            commands, cut = leaf.commands, leaf.commands.cut
            cut_record = cut.state.records[0]
            terminal_record = leaf.result.record
            self.assertEqual(len(cut.state.records), 1)
            self.assertEqual(cut_record.event_id, 0)
            self.assertEqual(cut_record.outcome, cut.outcome)
            self.assertEqual(cut_record.command_word, ())
            self.assertEqual(cut_record.precursor, (("signal", 0), ("reference", 0)))
            self.assertIs(commands.state.records, cut.state.records)
            self.assertEqual(commands.state.pending, () if cut.outcome[0] == 0 else ("A",))
            self.assertEqual(terminal_record.event_id, 1)
            self.assertEqual(terminal_record.outcome, leaf.outcome)
            self.assertEqual(terminal_record.command_word, commands.word)
            self.assertEqual(
                terminal_record.precursor, (("signal", 0), ("reference", 0), ("joint", 0))
            )
            self.assertIs(leaf.result.source, commands.state)
            self.assertEqual(terminal_record.context, commands.state.context)
            self.assertEqual(terminal_record.action, "terminal_tilted_read")
            self.assertEqual(leaf.label.command_word, commands.word)
            self.assertEqual(leaf.label.cut_outcome, cut.outcome)
            self.assertEqual(leaf.label.terminal_outcome, leaf.outcome)

    def test_stops_retain_both_independent_prefixes_without_failed_reference_kernel(self):
        stops = [leaf for leaf in self.protocol.leaves if type(leaf) is m.StoppedBranch]
        for stop in stops:
            self.assertIsNone(stop.decision.reference)
            self.assertEqual(stop.decision.record.outcome, "unavailable")
            self.assertEqual(stop.decision.record.precursor, ())
            self.assertEqual(stop.local.state.settings, ("Z",))
            self.assertEqual(stop.weight, stop.local.probability / 3)
            self.assertEqual(stop.report.origin, "protocol-stop")
            self.assertEqual(stop.report.event_id, 0)
            self.assertEqual(stop.report.action, "protocol_stop")
            self.assertEqual(stop.report.outcome, "reference_unavailable")
            self.assertEqual(stop.report.policy_id, m.POLICY_ID)
            self.assertEqual(stop.report.precursor, (("signal", 0), ("reference", 0)))
            self.assertIs(stop.report.local, stop.local)
            self.assertIs(stop.report.decision, stop.decision)
            self.assertIsNone(stop.label.cut_outcome)
            self.assertIsNone(stop.label.terminal_outcome)
            self.assertEqual(stop.label.command_word, ())
            for forbidden in ("residual", "result", "state"):
                self.assertFalse(hasattr(stop, forbidden))
            with self.assertRaises(ValueError):
                m.WeightedJoint(stop.local, stop.decision)
        with self.assertRaises(ValueError):
            m.StoppedBranch(self.lts[0].joint.local, self.lts[0].joint.decision, self.read)

    def test_command_decision_receives_only_validated_outcome_bits(self):
        self.assertEqual(m.WORD_BY_A, ((), ("A",)))
        observed = []
        original = m.policy_word

        def observe(outcome):
            observed.append(outcome)
            self.assertIs(type(outcome), tuple)
            self.assertTrue(all(type(bit) is int for bit in outcome))
            return original(outcome)

        try:
            m.policy_word = observe
            for cell in CELLS:
                cut = self.terminals[0, "ready", cell, (*cell, "+")].commands.cut
                commanded = m.CommandEnvelope(cut)
                self.assertEqual(commanded.word, () if cell[0] == 0 else ("A",))
        finally:
            m.policy_word = original
        self.assertEqual(observed, list(CELLS))
        leaf = self.terminals[0, "ready", (0, 0), (0, 0, "+")]
        for forbidden in (
            leaf.commands.cut.state.records[0],
            leaf.result.source.context,
            leaf.result.source,
            self.boundary.source.residual,
            lambda _: (),
        ):
            with self.assertRaises((TypeError, ValueError)):
                m.policy_word(forbidden)
        with self.assertRaises(TypeError):
            m.CommandEnvelope(leaf.commands.cut, word=("B",))

    def test_terminal_results_are_scalar_only_and_cannot_continue_any_stage(self):
        leaf = self.terminals[0, "ready", (1, 0), (1, 0, "+")]
        stop = next(value for value in self.protocol.leaves if type(value) is m.StoppedBranch)
        for terminal in (leaf, leaf.result, stop):
            self.assertFalse(hasattr(terminal, "residual"))
            for operation in (
                lambda value: m.Boundary(value),
                lambda value: m.WeightedLocal(value, 0),
                lambda value: m.LtEnvelope(value, self.read),
                lambda value: m.CutEnvelope(value, (0, 0)),
                lambda value: m.CommandEnvelope(value),
                lambda value: m.WeightedTerminal(value, (0, 0, "+")),
                lambda value: m.i.run_word(value, ("A",)),
                lambda value: m.i.commit(value, (0, 0)),
            ):
                with self.assertRaises((TypeError, ValueError)):
                    operation(terminal)
        self.assertIs(leaf.result.source, leaf.commands.state)
        self.assertEqual(leaf.result.source.pending, ("A",))
        self.assertEqual(len(leaf.result.source.records), 1)
        with self.assertRaises(TypeError):
            m.i.TerminalResult(
                leaf.result.source,
                leaf.result.record,
                leaf.result.effect,
                leaf.result.probability,
                residual=leaf.result.source.residual,
            )

    def test_preterminal_adapter_refuses_product_prospective_raw_and_old_terminal_sources(self):
        anchor = self.lts[0].joint
        context = anchor.source.context
        prospective = m.bridge.prepare(
            context.local_source,
            context.reference,
            context.independence,
            local_origin=context.local_origin,
            joint_origin=context.joint_origin,
            reference_provenance=context.reference_provenance,
        )
        product_source = m.bridge.promote(prospective)
        _, terminal = m.bridge.commit(anchor.source, (0, 0))
        local_terminal = m.c.literal_cut(anchor.local.state, 0)[1]
        for forbidden in (
            prospective,
            product_source,
            terminal,
            terminal.target,
            local_terminal,
            anchor.source.target,
            anchor.source.target.residual,
            self.lts[0].state,
        ):
            with (
                self.subTest(source=type(forbidden).__name__),
                self.assertRaises((TypeError, ValueError)),
            ):
                m.convert_preterminal(forbidden, anchor, self.read)
        converted = m.convert_preterminal(anchor.source, anchor, self.read)
        self.assertEqual(converted.state, self.lts[0].state)
        self.assertIs(converted.joint, anchor)
        self.assertEqual(converted.weight, anchor.weight)

    def test_preterminal_adapter_rejects_wrong_anchor_and_full_native_target_forgery(self):
        anchor = self.lts[0].joint
        source = anchor.source
        with self.assertRaises(ValueError):
            m.convert_preterminal(self.lts[1].joint.source, anchor, self.read)
        for signal, reference in (
            (anchor.local.state, replace(source.context.reference, t=F(1, 2))),
            (replace(anchor.local.state, settings=()), source.context.reference),
        ):
            prospective = m.bridge.prepare(
                signal,
                reference,
                self.law.independence,
                local_origin="signal",
                joint_origin="joint",
                reference_provenance=self.law.provenance,
            )
            wrong_context_source = m.bridge.promote(m.bridge.couple(m.bridge.promote(prospective)))
            with self.assertRaises(ValueError):
                m.convert_preterminal(wrong_context_source, anchor, self.read)
        for field, value in (
            ("residual", self.lts[1].joint.source.target.residual),
            ("permutation", tuple(reversed(source.target.permutation))),
            ("coupler", m.d.PRODUCT_COUPLER),
            ("joint_origin", "other-joint"),
        ):
            target = object.__new__(m.d.CompositeState)
            for name, old in vars(source.target).items():
                object.__setattr__(target, name, old)
            object.__setattr__(target, field, value)
            forged = object.__new__(m.bridge.JointSource)
            object.__setattr__(forged, "context", source.context)
            object.__setattr__(forged, "target", target)
            with self.subTest(field=field), self.assertRaises((TypeError, ValueError)):
                m.convert_preterminal(forged, anchor, self.read)

    def test_ineligible_direct_nonzero_c_is_not_repaired_into_the_joint_domain(self):
        local = m.bridge.convert_local_state(self.boundary.source, origin="signal")
        decision = self.lts[0].joint.decision
        prospective = m.d.prepare_joint(
            local, decision.reference, self.law.independence, joint_origin="joint"
        )
        coupled = m.d.couple_state(m.d.promote_joint(prospective))
        self.assertEqual(m.d.joint_mass(coupled.residual), 1)
        self.assertFalse(m.d.joint_recordable(coupled.residual))
        with self.assertRaises(ValueError):
            m.d.promote_joint(coupled)
        with self.assertRaises(ValueError):
            m.i.LocalInput(to_api(self.initial, m.i), "signal")
        self.assertNotEqual(self.initial, local_kernel(local_rho(self.initial)))

    def test_zero_read_and_zero_recut_refuse_normalization_or_appended_records(self):
        leaf = self.terminals[0, "ready", (0, 0), (0, 0, "+")]
        cut, commands = leaf.commands.cut, leaf.commands
        before = cut.state.records
        self.assertEqual(m.i.branch(cut.state.residual, T, (1, 1)), to_api(zero(16), m.i))
        with self.assertRaises(ValueError):
            m.i.commit(cut.state, (1, 1))
        self.assertIs(cut.state.records, before)
        for outcome in READS:
            if outcome[:2] != cut.outcome:
                self.assertEqual(
                    m.i.terminal_weights(commands.state.residual, T)[READS.index(outcome)], 0
                )
                with self.assertRaises(ValueError):
                    m.WeightedTerminal(commands, outcome)
        self.assertIs(commands.state.records, before)

    def test_exact_bound_classes_and_module_instance_mismatch_are_rejected(self):
        class ForeignState(m.c.State):
            pass

        with self.assertRaises(TypeError):
            m.Boundary(ForeignState(self.boundary.source.residual))
        forged = replace(self.boundary.source)
        object.__setattr__(forged, "residual", to_api(self.initial, m.d))
        with self.assertRaises(TypeError):
            m.Boundary(forged)
        original = m.c
        try:
            m.c = m.d
            with self.assertRaises(ValueError):
                m.validate_aliases()
            with self.assertRaises(ValueError):
                m.Boundary(self.boundary.source)
        finally:
            m.c = original
        m.validate_aliases()

    def test_derived_outputs_and_numeric_weights_cannot_be_supplied_or_rewritten(self):
        lt = self.lts[0]
        local = lt.joint.local
        leaf = self.terminals[0, "ready", (0, 0), (0, 0, "+")]
        for constructor in (
            lambda: m.WeightedLocal(self.boundary, 0, weight=F(1)),
            lambda: m.ReferenceDecision(self.law, "ready", probability=F(1)),
            lambda: m.WeightedJoint(local, lt.joint.decision, weight=F(1)),
            lambda: m.LtEnvelope(lt.joint, self.read, state=lt.state),
            lambda: m.CutEnvelope(lt, (0, 0), probability=F(1)),
            lambda: m.CommandEnvelope(leaf.commands.cut, state=leaf.commands.state),
            lambda: m.WeightedTerminal(leaf.commands, leaf.outcome, probability=F(1)),
            lambda: m.ProtocolRun(self.boundary, self.law, self.read, coordinates=()),
        ):
            with self.assertRaises(TypeError):
                constructor()
        for item, field, value in (
            (local, "weight", F(1)),
            (lt.state, "pending", ("A",)),
            (leaf.result.record, "event_id", 9),
            (leaf.label, "local_outcome", 1),
            (self.law, "ready", F(1)),
        ):
            with self.assertRaises(FrozenInstanceError):
                setattr(item, field, value)
        entry = next(entry for entry in self.protocol.coordinates if entry.weight > 0)
        for weight, selected in (
            (entry.weight * 2, entry.selected),
            (F(0), entry.selected),
            (F(1), None),
            (F(-1), None),
        ):
            with self.assertRaises((TypeError, ValueError)):
                m.LawEntry(entry.label, weight, selected)
        with self.assertRaises(ValueError):
            m.LawEntry(replace(entry.label, local_outcome=1), entry.weight, entry.selected)

    def test_iterable_labels_canonicalize_once_and_keep_full_immutable_identity(self):
        sample = self.protocol.coordinates[8].label
        label = replace(
            sample,
            cut_outcome=iter(sample.cut_outcome),
            command_word=iter(sample.command_word),
            terminal_outcome=iter(sample.terminal_outcome),
        )
        self.assertEqual(label, sample)
        self.assertIs(type(label.cut_outcome), tuple)
        self.assertIs(type(label.command_word), tuple)
        self.assertIs(type(label.terminal_outcome), tuple)
        boundary = m.Boundary(self.boundary.source, availability=iter(m.AVAILABILITY))
        self.assertEqual(boundary.availability, m.AVAILABILITY)
        self.assertEqual(m.policy_word(iter((1, 0))), ("A",))
        for labels in ((), m.AVAILABILITY[:-1], (*m.AVAILABILITY, "unknown")):
            with self.assertRaises(ValueError):
                m.Boundary(self.boundary.source, availability=labels)

    def test_named_reference_identity_survives_equal_kernels_and_unequal_history_labels(self):
        alternate_law = replace(self.law, preparation_id="another_declared_ready_preparation")
        alternate = m.ReferenceDecision(alternate_law, "ready")
        original = self.lts[0].joint.decision
        self.assertEqual(mat(alternate.reference.residual), mat(original.reference.residual))
        self.assertEqual(alternate.probability, original.probability)
        self.assertNotEqual(alternate.record, original.record)
        label = self.protocol.coordinates[0].label
        self.assertNotEqual(label, replace(label, preparation_id=alternate_law.preparation_id))
        self.assertEqual(self.protocol.boundary.root_weight, 1)
        self.assertEqual(self.protocol.law, self.law)
        self.assertIs(self.protocol.terminal_read, self.read)
        other_read = replace(self.read, setting_id="second_nominal_tilted_read")
        other = m.run_protocol(self.boundary, self.law, other_read)
        self.assertEqual(
            tuple(entry.weight for entry in other.coordinates),
            tuple(entry.weight for entry in self.protocol.coordinates),
        )
        self.assertNotEqual(other.probabilities, self.protocol.probabilities)
        for original_entry, other_entry in zip(
            self.protocol.coordinates, other.coordinates, strict=True
        ):
            self.assertEqual(original_entry.label.terminal_setting_id, self.read.setting_id)
            self.assertEqual(other_entry.label.terminal_setting_id, other_read.setting_id)
            if original_entry.weight:
                with self.assertRaises(ValueError):
                    m.LawEntry(other_entry.label, original_entry.weight, original_entry.selected)
            if type(other_entry.selected) is m.StoppedBranch:
                self.assertIs(other_entry.selected.terminal_read, other_read)
                self.assertIs(other_entry.selected.report.terminal_read, other_read)
                self.assertFalse(hasattr(other_entry.selected, "result"))

    def test_same_y_distinct_x_and_hidden_c_give_same_law_not_same_audit_source(self):
        starts = (
            local_kernel(scale(F(1, 2), add(I2, scale(F(1, 2), X))), F(1, 20)),
            local_kernel(scale(F(1, 2), add(I2, scale(F(-1, 2), X))), (0, F(1, 20))),
        )
        boundaries = tuple(m.Boundary(m.c.State(to_api(raw, m.c))) for raw in starts)
        self.assertNotEqual(starts[0], starts[1])
        self.assertNotEqual(local_rho(starts[0]), local_rho(starts[1]))
        direct = tuple(independent_law(raw, F(2, 3))[0] for raw in starts)
        self.assertEqual(direct[0], direct[1])
        local_outputs = tuple(
            tuple(m.WeightedLocal(boundary, r) for r in (0, 1)) for boundary in boundaries
        )
        for r in (0, 1):
            left, right = local_outputs[0][r], local_outputs[1][r]
            self.assertEqual(left.probability, F(1, 2))
            self.assertEqual(left.probability, right.probability)
            self.assertEqual(left.committed, right.committed)
            self.assertEqual(left.state, right.state)
            self.assertIs(left.boundary.source, boundaries[0].source)
            self.assertIs(right.boundary.source, boundaries[1].source)
            self.assertNotEqual(left.boundary.source, right.boundary.source)
        # One full executable replay suffices here: both actual local branches
        # and every later fixed input are identical, while the anchors are not.
        protocol = m.run_protocol(boundaries[0], self.law, self.read)
        self.assertEqual(
            {coordinate_key(entry.label): entry.weight for entry in protocol.coordinates}, direct[0]
        )
        for leaf in protocol.leaves:
            local = (
                leaf.commands.cut.source.joint.local
                if type(leaf) is m.WeightedTerminal
                else leaf.local
            )
            self.assertIs(local.boundary.source, boundaries[0].source)


if __name__ == "__main__":
    unittest.main()
