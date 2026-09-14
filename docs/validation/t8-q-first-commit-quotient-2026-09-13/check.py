"""Independent exact checks for the finite first-commit/quotient witnesses.

Run with Python or Python -O. All decisions use integers/Fractions and unittest
assertions; no stochastic sampling, numerical tolerance, or external packages
are required. The finite certificates check the declared examples, not the
general compact-base theorem or any DET/physical selection of these maps.
"""

import unittest
from dataclasses import FrozenInstanceError
from fractions import Fraction as F
from itertools import product

import model as m

BASIS = tuple(tuple(F(int(i == j)) for i in range(4)) for j in range(4))
MIXED = (F(1, 10), F(1, 5), F(3, 10), F(2, 5))


def total(values):
    return sum(values, F(0))


def mv(operator, x):
    """Direct independent matrix/vector multiplication."""
    return tuple(total(row[j] * x[j] for j in range(len(x))) for row in operator)


def mm(left, right):
    """Direct independent matrix product, also for rectangular operators."""
    return tuple(
        tuple(
            total(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def add(left, right):
    return tuple(
        tuple(a + b for a, b in zip(x, y, strict=True)) for x, y in zip(left, right, strict=True)
    )


def scale(value, operator):
    return tuple(tuple(value * entry for entry in row) for row in operator)


def diag(values):
    return tuple(
        tuple(value if i == j else F(0) for j in range(len(values)))
        for i, value in enumerate(values)
    )


def induced_l1(operator):
    return max(total(abs(row[j]) for row in operator) for j in range(len(operator[0])))


def direct_silent(x):
    return (x[0] / 2, x[3], x[2] / 2, x[1])


def direct_commit(x, mode):
    return tuple(x[i] / 2 if i == 2 * mode else F(0) for i in range(4))


def direct_silent_power(x, count):
    bright = (x[0] / 2**count, x[2] / 2**count)
    dark = (x[1], x[3]) if count % 2 == 0 else (x[3], x[1])
    return (bright[0], dark[0], bright[1], dark[1])


def positive_entries(operator):
    return all(entry >= 0 for row in operator for entry in row)


class FirstCommitQuotientChecks(unittest.TestCase):
    def test_exact_input_and_positive_normalization_guards(self):
        for values in ((0.25,) * 4, (True, 0, 0, 0)):
            with self.assertRaises(TypeError):
                m.State(values)
        for values in ((1, 0, 0), (0, 0, 0, 0), (1, 1, 0, 0), (-1, 0, 2, 0)):
            with self.assertRaises(ValueError):
                m.State(values)
        for count in (-1, True, F(1, 2)):
            with self.assertRaises(ValueError):
                m.first_commit_prefix(count)
        for mode in (-1, 2, True, F(0)):
            with self.assertRaises(ValueError):
                m.apply_commit(m.State(BASIS[0]), mode)
        self.assertEqual(m.State(MIXED).residual, MIXED)

    def test_typed_branch_embedding_retains_full_labels_and_accounting(self):
        self.assertEqual(len(m.BRANCHES), 6)
        silent = tuple(branch for branch in m.BRANCHES if not branch.commits)
        commits = tuple(branch for branch in m.BRANCHES if branch.commits)
        self.assertEqual(m.aggregate_branches(silent), m.S)
        self.assertEqual(tuple(m.embed(branch) for branch in commits), (m.B0, m.B1))
        self.assertEqual(tuple(branch.label for branch in commits), m.LABELS)
        for mode in (0, 1):
            source = tuple(branch for branch in m.BRANCHES if branch.source == mode)
            expected = diag(tuple(F(int(i // 2 == mode)) for i in range(4)))
            embedded_sum = m.aggregate_branches(source)
            # Conservation is equality of the mass effects, not equality of
            # the summed map with an identity: dark mass changes controller.
            self.assertEqual(m.rowmat(m.UNIT, embedded_sum), m.rowmat(m.UNIT, expected))
        for branch in silent:
            self.assertEqual(branch.outcome, "epsilon")
            self.assertIsNone(branch.label)

    def test_aggregate_dynamics_and_complete_mass_on_positive_generators(self):
        for x in (*BASIS, MIXED, (2, 3, 5, 7)):
            silent = mv(m.S, x)
            commits = tuple(mv(operator, x) for operator in (m.B0, m.B1))
            self.assertEqual(silent, direct_silent(x))
            self.assertEqual(commits, tuple(direct_commit(x, mode) for mode in (0, 1)))
            self.assertTrue(all(value >= 0 for output in (silent, *commits) for value in output))
            self.assertEqual(total(silent) + total(total(output) for output in commits), total(x))
        self.assertEqual(m.rowmat(m.UNIT, add(add(m.S, m.B0), m.B1)), m.UNIT)

    def test_first_commit_each_depth_has_independent_geometric_formula(self):
        for count in range(10):
            operators = m.first_commit_at(count)
            for mode, operator in enumerate(operators):
                expected = diag(
                    tuple(F(1, 2 ** (count + 1)) if i == 2 * mode else F(0) for i in range(4))
                )
                self.assertEqual(operator, expected)
                for x in (*BASIS, MIXED):
                    self.assertEqual(total(mv(operator, x)), x[2 * mode] / 2 ** (count + 1))

    def test_prefix_formula_and_operator_norm_error_are_exact(self):
        for count in range(12):
            for mode, operator in enumerate(m.first_commit_prefix(count)):
                limit = (m.H0, m.H1)[mode]
                self.assertEqual(operator, scale(1 - F(1, 2**count), limit))
                error = add(limit, scale(-1, operator))
                self.assertEqual(induced_l1(error), F(1, 2**count))
                self.assertTrue(positive_entries(error))

    def test_mass_telescope_and_never_mass_for_all_generator_columns(self):
        for count in range(10):
            h0, h1 = m.first_commit_prefix(count)
            power = m.matpow(m.S, count)
            self.assertEqual(m.rowmat(m.UNIT, add(add(h0, h1), power)), m.UNIT)
            for x in (*BASIS, MIXED, (2, 3, 5, 7)):
                tail = mv(power, x)
                self.assertEqual(tail, direct_silent_power(x, count))
                self.assertEqual(total(tail), x[1] + x[3] + (x[0] + x[2]) / 2**count)
                self.assertEqual(m.never_mass(x), x[1] + x[3])
                self.assertEqual(total(mv(add(m.H0, m.H1), x)) + m.never_mass(x), total(x))

    def test_periodic_dark_residual_prevents_silent_convergence_and_inverse(self):
        dark = BASIS[1]
        for count in range(10):
            expected = BASIS[1] if count % 2 == 0 else BASIS[3]
            self.assertEqual(mv(m.matpow(m.S, count), dark), expected)
        self.assertEqual(total(abs(a - b) for a, b in zip(dark, mv(m.S, dark), strict=True)), 2)
        identity_minus_s = add(diag((1, 1, 1, 1)), scale(-1, m.S))
        dark_fixed_vector = (0, 1, 0, 1)
        self.assertEqual(mv(identity_minus_s, dark_fixed_vector), (0, 0, 0, 0))
        self.assertNotEqual(dark_fixed_vector, (0, 0, 0, 0))
        self.assertEqual(mv(add(m.H0, m.H1), dark), (0, 0, 0, 0))

    def test_positive_subnormalized_fixed_points_do_not_select_first_commit(self):
        extra = ((0, F(1, 3), 0, F(1, 3)), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
        alternative = add(m.H0, extra)
        self.assertEqual(m.H0, add(m.B0, mm(m.H0, m.S)))
        self.assertEqual(alternative, add(m.B0, mm(alternative, m.S)))
        self.assertTrue(positive_entries(alternative))
        self.assertTrue(all(value <= 1 for value in m.rowmat(m.UNIT, add(alternative, m.H1))))
        self.assertEqual(total(mv(alternative, BASIS[1])), F(1, 3))
        self.assertEqual(total(mv(m.H0, BASIS[1])), 0)
        for count in range(8):
            partial, _ = m.first_commit_prefix(count)
            self.assertTrue(positive_entries(add(alternative, scale(-1, partial))))
        # These identities exhibit nonuniqueness. Minimality for all positive
        # solutions is proved by iteration in the note, not by these samples.

    def test_quotient_has_positive_section_faithful_mass_and_closed_image(self):
        section = ((1, 0, 0), (0, 0, 1), (0, 1, 0), (0, 0, 0))
        self.assertEqual(mm(m.Q, section), diag((1, 1, 1)))
        self.assertTrue(positive_entries(section))
        self.assertTrue(positive_entries(m.Q))
        self.assertEqual(m.rowmat(m.QUOTIENT_UNIT, m.Q), m.UNIT)
        for y in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 3, 7)):
            lifted = mv(section, y)
            self.assertEqual(m.project(lifted), y)
            self.assertEqual(total(lifted), total(y))
        # The two nonnegative maps certify image(Q R_+^4)=R_+^3.

    def test_aggregate_maps_and_terminal_effects_descend_exactly(self):
        for operator, expected in ((m.S, m.S_BAR), (m.B0, m.B0_BAR), (m.B1, m.B1_BAR)):
            self.assertEqual(m.descend_map(operator), expected)
            self.assertEqual(mm(m.Q, operator), mm(expected, m.Q))
            self.assertTrue(positive_entries(expected))
        self.assertEqual(m.descend_effect(m.UNIT), m.QUOTIENT_UNIT)
        self.assertEqual(m.descend_effect((0, 1, 0, 1)), (0, 0, 1))
        for count in range(8):
            for operator in m.first_commit_prefix(count):
                induced = m.descend_map(operator)
                self.assertEqual(mm(m.Q, operator), mm(induced, m.Q))
        self.assertEqual(
            m.rowmat(m.QUOTIENT_UNIT, add(add(m.S_BAR, m.B0_BAR), m.B1_BAR)), m.QUOTIENT_UNIT
        )

    def test_declared_finite_words_preserve_probabilities_and_residual_projection(self):
        original = (m.S, m.B0, m.B1)
        quotient = (m.S_BAR, m.B0_BAR, m.B1_BAR)
        for length in range(5):
            for word in product(range(3), repeat=length):
                for initial in (MIXED, BASIS[1], BASIS[3]):
                    x, y = initial, m.project(initial)
                    for symbol in word:
                        x, y = mv(original[symbol], x), mv(quotient[symbol], y)
                    self.assertEqual(m.project(x), y)
                    self.assertEqual(total(x), total(y))
        # The proof uses invariance for every finite word. This enumeration
        # checks composition and does not add observations of internal edges.

    def test_hidden_edge_and_later_controller_read_block_the_same_quotient(self):
        left, right = BASIS[1], BASIS[3]
        self.assertEqual(m.project(left), m.project(right))
        edge = next(
            branch
            for branch in m.BRANCHES
            if not branch.commits and branch.source == 0 and branch.target == 1
        )
        edge_operator = m.embed(edge)
        self.assertNotEqual(m.project(mv(edge_operator, left)), m.project(mv(edge_operator, right)))
        with self.assertRaises(ValueError):
            m.descend_map(edge_operator)
        with self.assertRaises(ValueError):
            m.descend_effect((0, 1, 0, 0))
        controller_read = diag((1, 1, 0, 0))
        with self.assertRaises(ValueError):
            m.descend_map(controller_read)
        self.assertNotEqual(total(mv(controller_read, left)), total(mv(controller_read, right)))

    def test_commits_retain_labels_residuals_and_actual_full_precursors(self):
        initial = m.State(MIXED)
        for mode in (0, 1):
            probability, committed = m.apply_commit(initial, mode)
            self.assertEqual(probability, MIXED[2 * mode] / 2)
            self.assertEqual(committed.residual, BASIS[2 * mode])
            self.assertEqual(committed.records, (m.Record(0, m.LABELS[mode], ()),))
            next_probability, again = m.apply_commit(committed, mode)
            self.assertEqual(next_probability, F(1, 2))
            self.assertEqual(again.records[0], committed.records[0])
            self.assertEqual(again.records[1], m.Record(1, m.LABELS[mode], (0,)))
            with self.assertRaises(FrozenInstanceError):
                again.records[0].event_id = 99
        self.assertEqual(initial.records, ())

    def test_silent_steps_append_no_null_and_preserve_the_actual_history_tuple(self):
        _, committed = m.apply_commit(m.State(MIXED), 0)
        probability, silent = m.apply_silent(committed)
        self.assertEqual(probability, F(1, 2))
        self.assertIs(silent.records, committed.records)
        self.assertEqual(silent.records, (m.Record(0, m.LABELS[0], ()),))
        dark = m.State(BASIS[1], committed.records)
        probability, swapped = m.apply_silent(dark)
        self.assertEqual(probability, 1)
        self.assertEqual(swapped.residual, BASIS[3])
        self.assertIs(swapped.records, dark.records)

    def test_eliminated_selection_keeps_full_commit_and_refuses_never_modes(self):
        old_history = (m.Record(0, m.LABELS[1], ()),)
        state = m.State(MIXED, old_history)
        for mode in (0, 1):
            immediate_probability, immediate = m.apply_commit(state, mode)
            eventual_probability, eventual = m.apply_first_commit(state, mode)
            self.assertEqual(eventual_probability, MIXED[2 * mode])
            self.assertEqual(eventual_probability, 2 * immediate_probability)
            self.assertEqual(eventual, immediate)
            self.assertEqual(eventual.records[-1], m.Record(1, m.LABELS[mode], (0,)))
            self.assertEqual(eventual.records[0], old_history[0])
            for dark in (BASIS[1], BASIS[3]):
                with self.assertRaises(ValueError):
                    m.apply_first_commit(m.State(dark, old_history), mode)
        for function in (m.apply_silent, m.apply_commit, m.apply_first_commit):
            args = (MIXED,) if function is m.apply_silent else (MIXED, 0)
            with self.assertRaises(TypeError):
                function(*args)

    def test_zero_commits_refuse_normalization_without_changing_history(self):
        for index in range(4):
            state = m.State(BASIS[index])
            for mode in (0, 1):
                if index != 2 * mode:
                    with self.assertRaises(ValueError):
                        m.apply_commit(state, mode)
                    self.assertEqual(state.residual, BASIS[index])
                    self.assertEqual(state.records, ())

    def test_history_validation_is_structural_not_global_reachability(self):
        record = m.Record(0, m.LABELS[0], ())
        # The supplied process cannot reach bright 1 after recording bright 0,
        # but the constructor intentionally verifies structure, not a path.
        state = m.State(BASIS[2], (record,))
        self.assertEqual(state.records, (record,))
        self.assertEqual(state.residual, BASIS[2])
        with self.assertRaises(ValueError):
            m.State(BASIS[0], (m.Record(1, m.LABELS[0], ()),))
        with self.assertRaises(ValueError):
            m.State(BASIS[0], (record, m.Record(1, m.LABELS[0], ())))
        # append_record has no residual and cannot enforce a probability guard.
        self.assertEqual(m.append_record((), m.LABELS[0]), (record,))

    def test_nonfaithful_mass_can_hide_divergent_first_commit_residuals(self):
        silent = diag((F(1, 2), 2))
        commit = diag((F(1, 2), 1))
        unit = ((1, 0),)
        self.assertEqual(mm(unit, add(silent, commit)), unit)
        partial = diag((0, 0))
        power = diag((1, 1))
        for count in range(1, 10):
            partial = add(partial, mm(commit, power))
            power = mm(power, silent)
            self.assertEqual(partial, diag((1 - F(1, 2**count), 2**count - 1)))
            self.assertEqual(mm(unit, partial), ((1 - F(1, 2**count), 0),))
            self.assertEqual(induced_l1(partial), 2**count - 1)
        self.assertEqual(mv(silent, (0, 1)), (0, 2))
        # The zero-mass positive coordinate invalidates a compact-base bound.

    def test_predictive_quotient_lawfully_removes_invisible_divergence(self):
        q = ((1, 0),)
        silent = diag((F(1, 2), 2))
        commit = diag((F(1, 2), 1))
        for operator in (silent, commit):
            self.assertEqual(mm(q, operator), mm(((F(1, 2),),), q))
        for count in range(8):
            original = diag((1 - F(1, 2**count), 2**count - 1))
            reduced = ((1 - F(1, 2**count),),)
            self.assertEqual(mm(q, original), mm(reduced, q))
        # This probe identifies discarded algebraic information, but is not
        # a bounded probability effect on the full u=x normalized cone.
        # A later probabilistic readout would require a declared restricted
        # domain; the faithful dark-mode read test above needs no such change.
        distinguishing_linear_probe = ((0, 1),)
        self.assertNotEqual(
            mv(distinguishing_linear_probe, (1, 0)), mv(distinguishing_linear_probe, (1, 1))
        )
        self.assertEqual(mv(q, (1, 0)), mv(q, (1, 1)))

    def test_strict_mass_positivity_is_sufficient_not_necessary_for_convergence(self):
        silent = commit = diag((F(1, 2), F(1, 2)))
        nonfaithful_unit = ((1, 0),)
        self.assertEqual(mm(nonfaithful_unit, add(silent, commit)), nonfaithful_unit)
        for count in range(8):
            partial = scale(1 - F(1, 2**count), diag((1, 1)))
            self.assertEqual(induced_l1(add(diag((1, 1)), scale(-1, partial))), F(1, 2**count))
        self.assertEqual(mv(nonfaithful_unit, (0, 1)), (0,))

    def test_arbitrary_psd_projection_can_have_nonclosed_image_and_no_mass(self):
        # PSD2 is represented by (a,b,c) for [[a,b],[b,c]]. Its projection
        # (a,b) contains (1/n,1) using rank-one lifts, but not its limit (0,1):
        # every purported lift (0,1,c) has determinant -1 independently of c.
        for count in range(1, 10):
            a, b, c = F(1, count), F(1), F(count)
            self.assertGreater(a, 0)
            self.assertGreater(c, 0)
            self.assertEqual(a * c - b * b, 0)
            self.assertEqual(a, F(1, count))
        for c in (-5, 0, 1, 100):
            self.assertEqual(0 * c - 1, -1)
        first, second = (1, 0, 1), (1, 0, 2)
        self.assertEqual(first[:2], second[:2])
        self.assertNotEqual(first[0] + first[2], second[0] + second[2])
        # Thus trace cannot be defined from this arbitrary projected state.

    def test_equal_eliminated_outputs_do_not_make_primitive_maps_descend(self):
        silent = diag((F(1, 2), F(1, 3)))
        commit = ((F(1, 2), F(2, 3)),)
        q = ((1, 1),)
        self.assertEqual(add(mm(q, silent), commit), q)
        for count in range(1, 10):
            partial = ((1 - F(1, 2**count), 1 - F(1, 3**count)),)
            self.assertEqual(add(partial, ((F(1, 2**count), F(1, 3**count)),)), q)
        left, right = (1, 0), (0, 1)
        self.assertEqual(mv(q, left), mv(q, right))
        self.assertNotEqual(mv(commit, left), mv(commit, right))
        self.assertNotEqual(mv(q, mv(silent, left)), mv(q, mv(silent, right)))
        # Both eventual outputs have mass one, but their first-attempt laws
        # differ. No scalar map factors either primitive through q.

    def test_pointwise_convergence_has_no_unstated_uniform_family_rate(self):
        # For each fixed k, q_k^n tends to zero. Bernoulli's inequality gives
        # q_k^k >= 1-k/(2k)=1/2, so convergence over k is not uniform.
        for count in range(1, 25):
            q = 1 - F(1, 2 * count)
            self.assertGreaterEqual(q**count, F(1, 2))
            self.assertLess(q, 1)
            self.assertGreater(q, 0)
            self.assertEqual((1 - q) * total(q**n for n in range(count)), 1 - q**count)


if __name__ == "__main__":
    unittest.main(verbosity=2)
