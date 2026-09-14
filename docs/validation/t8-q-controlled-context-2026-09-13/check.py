"""Independent exact checks for the explicitly chosen controlled-context model.

These tests verify a supplied finite classical cone in coherent pair-kernel
coordinates. They do not establish physical availability, a DET-selected law,
quantum reconstruction, or geometry. Run directly with Python or Python -O;
unittest assertions remain active under optimization. No numerical tolerance,
random sampling, or external dependency is used.
"""

import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F
from itertools import permutations, product

import model as m

PARTITIONS = {"P": ((0, 1), (2, 3)), "Q": ((0, 2), (1, 3))}
BASIS = tuple(tuple(F(int(i == j)) for i in range(4)) for j in range(4))
MIXED = (F(1, 10), F(1, 5), F(3, 10), F(2, 5))


def total(values):
    return sum(values, F(0))


def pair(kernel, left, right):
    return total(kernel[i][j] for i in left for j in right)


def kernel_total(kernel):
    return total(total(row) for row in kernel)


def expected_kernel(mode, x):
    """Direct generator assembly, independent of the model's encoding formula."""
    shapes = (
        ((F(1, 3), F(1, 6)), (F(1, 6), F(1, 3))),
        ((F(1), F(-1, 2)), (F(-1, 2), F(1))),
    )
    result = [[F(0) for _ in range(4)] for _ in range(4)]
    for r, block in enumerate(PARTITIONS[mode]):
        for s, shape in enumerate(shapes):
            for i, j in product(range(2), repeat=2):
                result[block[i]][block[j]] += x[2 * r + s] * shape[i][j]
    return tuple(tuple(row) for row in result)


def direct_step(x, action, outcome):
    """Independent coordinate rule, without inspecting a branch matrix."""
    if action == "read":
        return tuple(value if str(i // 2) == outcome else F(0) for i, value in enumerate(x))
    if action == "switch":
        return (x[0], x[3], x[2], x[1])
    if outcome == "epsilon":
        return (x[0] / 2, x[1], x[2] / 2, x[3])
    index = 2 * int(outcome)
    return tuple(value / 2 if i == index else F(0) for i, value in enumerate(x))


def direct_word(x, word):
    for branch in word:
        x = direct_step(x, branch.action, branch.outcome)
    return total(x)


def determinant(rows):
    """Independent Leibniz determinant for the four-row closure certificate."""
    result = F(0)
    for permutation in permutations(range(4)):
        inversions = sum(permutation[i] > permutation[j] for i in range(4) for j in range(i + 1, 4))
        term = F((-1) ** inversions)
        for i in range(4):
            term *= rows[i][permutation[i]]
        result += term
    return result


def branch(mode, action, outcome="epsilon"):
    return next(item for item in m.branches(mode, action) if item.outcome == outcome)


def legal_words(mode, depth):
    yield ()
    if depth:
        for action in m.actions(mode):
            for first in m.branches(mode, action):
                for suffix in legal_words(first.target, depth - 1):
                    yield (first, *suffix)


class ControlledContextChecks(unittest.TestCase):
    def test_encoding_is_exact_linear_and_invertible_on_selected_cones(self):
        for mode, partition in PARTITIONS.items():
            for x in (*BASIS, MIXED, (0, 0, 0, 0), (2, 3, 4, 5)):
                with self.subTest(mode=mode, x=x):
                    kernel = m.encode(mode, x)
                    self.assertEqual(kernel, expected_kernel(mode, x))
                    self.assertEqual(m.decode(mode, kernel), x)
                    self.assertEqual(kernel_total(kernel), total(x))
                    self.assertEqual(pair(kernel, *partition), 0)
                    self.assertEqual(m.record_weights(mode, kernel), (x[0] + x[1], x[2] + x[3]))

    def test_shape_positivity_and_faithful_mass_have_exact_certificates(self):
        # Each 2x2 block has eigenvectors (1,1),(1,-1). The eigenvalues
        # below are strictly positive; every cone element is a positive sum.
        for x in BASIS:
            kernel = expected_kernel("P", x)
            nonzero_eigenvalues = []
            for i, j in PARTITIONS["P"]:
                nonzero_eigenvalues.extend(
                    (kernel[i][i] + kernel[i][j], kernel[i][i] - kernel[i][j])
                )
            self.assertTrue(all(value >= 0 for value in nonzero_eigenvalues))
            self.assertEqual(sum(value > 0 for value in nonzero_eigenvalues), 2)
            self.assertEqual(kernel_total(kernel), 1)
        for mode in PARTITIONS:
            self.assertEqual(m.decode(mode, m.encode(mode, (0, 0, 0, 0))), (0, 0, 0, 0))
            for x in (*BASIS, MIXED):
                kernel = m.encode(mode, x)
                # |g_ij| <= 1 for each normalized generator: an explicit
                # compact-base bound in the entrywise maximum norm.
                self.assertLessEqual(max(abs(value) for row in kernel for value in row), total(x))

    def test_decoder_rejects_larger_recordability_cones_without_repair(self):
        zero_mass_psd = ((1, -1, 0, 0), (-1, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
        unequal_diagonal_psd = ((1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
        rank_one_normalized = (
            (F(1, 4), F(1, 4), 0, 0),
            (F(1, 4), F(1, 4), 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
        )
        self.assertEqual(kernel_total(rank_one_normalized), 1)
        for kernel in (zero_mass_psd, unequal_diagonal_psd, rank_one_normalized):
            self.assertEqual(pair(kernel, *PARTITIONS["P"]), 0)
            with self.assertRaises(ValueError):
                m.decode("P", kernel)
        old_witness = expected_kernel("P", (F(3, 4), 0, 0, F(1, 4)))
        self.assertEqual(pair(old_witness, *PARTITIONS["Q"]), 0)
        with self.assertRaises(ValueError):
            m.decode("Q", old_witness)

    def test_exact_input_validation_and_normalization(self):
        for values in ((0.25,) * 4, (True, 0, 0, 0)):
            with self.assertRaises(TypeError):
                m.State("P", values)
        for values in ((1, 0, 0), (-1, 1, 1, 0), (0, 0, 0, 0), (1, 1, 0, 0)):
            with self.assertRaises(ValueError):
                m.State("P", values)
        with self.assertRaises(ValueError):
            m.State("absent", BASIS[0])
        self.assertEqual(m.State("P", (1, 0, 0, 0)).coordinates, BASIS[0])

    def test_available_actions_and_complete_branch_mass(self):
        self.assertEqual(m.actions("P"), ("read", "switch"))
        self.assertEqual(m.actions("Q"), ("read", "switch", "attempt"))
        for mode in PARTITIONS:
            for action in m.actions(mode):
                available = m.branches(mode, action)
                self.assertEqual(len(available), {"read": 2, "switch": 1, "attempt": 3}[action])
                for x in (*BASIS, MIXED):
                    probabilities = []
                    for item in available:
                        expected = direct_step(x, action, item.outcome)
                        actual = tuple(
                            total(row[j] * x[j] for j in range(4)) for row in item.matrix
                        )
                        self.assertEqual(actual, expected)
                        self.assertTrue(all(value >= 0 for value in actual))
                        probabilities.append(total(actual))
                    self.assertEqual(total(probabilities), 1)

    def test_every_positive_registered_branch_stays_in_target_domain(self):
        for mode in PARTITIONS:
            for action in m.actions(mode):
                for item in m.branches(mode, action):
                    for x in (*BASIS, MIXED):
                        expected = direct_step(x, action, item.outcome)
                        probability = total(expected)
                        if probability == 0:
                            with self.assertRaises(ValueError):
                                m.apply_branch(m.State(mode, x), item)
                            continue
                        result = m.apply_branch(m.State(mode, x), item)
                        conditional = tuple(value / probability for value in expected)
                        self.assertEqual(result.probability, probability)
                        self.assertEqual(result.state.coordinates, conditional)
                        self.assertEqual(result.state.mode, item.target)
                        kernel = m.encode(result.state.mode, result.state.coordinates)
                        self.assertEqual(m.decode(item.target, kernel), conditional)
                        self.assertEqual(kernel_total(kernel), 1)

    def test_old_naive_cut_then_other_context_obstruction_is_preserved(self):
        for c, x in ((F(1, 8), (F(3, 4), 0, 0, F(1, 4))), (F(-1, 8), (0, F(1, 4), F(3, 4), 0))):
            initial = m.encode("P", x)
            self.assertEqual(pair(initial, *PARTITIONS["P"]), 0)
            self.assertEqual(pair(initial, *PARTITIONS["Q"]), 0)
            result = m.apply_branch(m.State("P", x), branch("P", "read", "0"))
            self.assertEqual(result.probability, F(1, 2) + 2 * c)
            conditional = m.encode("P", result.state.coordinates)
            self.assertEqual(pair(conditional, *PARTITIONS["Q"]), c / result.probability)
            self.assertNotEqual(pair(conditional, *PARTITIONS["Q"]), 0)
            raw_sum = total(pair(conditional, cell, cell) for cell in PARTITIONS["Q"])
            self.assertEqual(raw_sum, F(2, 3) if c > 0 else F(2))
            with self.assertRaises(ValueError):
                m.decode("Q", conditional)
            with self.assertRaises(ValueError):
                m.apply_branch(result.state, branch("Q", "read", "0"))

    def test_switch_is_an_active_residual_transform_not_passive_relabeling(self):
        initial = m.State("P", BASIS[1])
        result = m.apply_branch(initial, branch("P", "switch"))
        self.assertEqual(result.probability, 1)
        self.assertEqual(result.state.mode, "Q")
        self.assertEqual(result.state.coordinates, BASIS[3])
        self.assertNotEqual(
            m.encode("Q", result.state.coordinates), m.encode("Q", initial.coordinates)
        )
        self.assertEqual(m.record_weights("Q", m.encode("Q", result.state.coordinates)), (0, 1))
        back = m.apply_branch(result.state, branch("Q", "switch"))
        self.assertEqual(back.state, initial)

    def test_selected_switch_has_no_positive_linear_extension_to_full_recordable_cone(self):
        # This normalized P-recordable kernel is PSD: its first block is
        # (1,-1)(1,-1)^T, and its second is the positive shape a. Its signed
        # expansion lies in the selected cone's linear span, not in that cone.
        signed_coordinates = (F(-3, 2), F(3, 2), F(1), F(0))
        kernel = expected_kernel("P", signed_coordinates)
        self.assertEqual(
            kernel,
            (
                (1, -1, 0, 0),
                (-1, 1, 0, 0),
                (0, 0, F(1, 3), F(1, 6)),
                (0, 0, F(1, 6), F(1, 3)),
            ),
        )
        self.assertEqual(
            tuple(
                value
                for i, j in PARTITIONS["P"]
                for value in (kernel[i][i] + kernel[i][j], kernel[i][i] - kernel[i][j])
            ),
            (0, 2, F(1, 2), F(1, 6)),
        )
        self.assertEqual(kernel_total(kernel), 1)
        self.assertEqual(pair(kernel, *PARTITIONS["P"]), 0)
        with self.assertRaises(ValueError):
            m.decode("P", kernel)
        with self.assertRaises(ValueError):
            m.encode("P", signed_coordinates)

        # Every linear extension agreeing on the four selected generators
        # must take this signed linear combination of their actual outputs.
        switched_generators = tuple(
            m.encode("Q", m.apply_branch(m.State("P", x), branch("P", "switch")).state.coordinates)
            for x in BASIS
        )
        forced_output = tuple(
            tuple(
                total(signed_coordinates[k] * switched_generators[k][i][j] for k in range(4))
                for j in range(4)
            )
            for i in range(4)
        )
        self.assertEqual(forced_output, expected_kernel("Q", (F(-3, 2), 0, 1, F(3, 2))))
        self.assertEqual(kernel_total(forced_output), 1)
        self.assertEqual(forced_output[0][0], F(-1, 2))
        self.assertLess(forced_output[0][0], 0)
        self.assertEqual(
            tuple(tuple(forced_output[i][j] for j in (0, 2)) for i in (0, 2)),
            ((F(-1, 2), F(-1, 4)), (F(-1, 4), F(-1, 2))),
        )
        with self.assertRaises(ValueError):
            m.decode("Q", forced_output)

    def test_illegal_and_unregistered_branches_are_rejected_even_after_zero_mass(self):
        with self.assertRaises(ValueError):
            m.branches("P", "attempt")
        with self.assertRaises(ValueError):
            m.branches("Q", "invented")
        forged = replace(branch("P", "read", "0"), matrix=((0, 0, 0, 0),) * 4)
        with self.assertRaises(ValueError):
            m.apply_branch(m.State("P", BASIS[0]), forged)
        with self.assertRaises(ValueError):
            m.word_probability("P", BASIS[0], (forged,))
        # The first branch has zero mass. That must not bypass validation of
        # the subsequent Q-only branch in this still-P controller state.
        illegal_word = (branch("P", "read", "1"), branch("Q", "attempt", "epsilon"))
        with self.assertRaises(ValueError):
            m.word_probability("P", BASIS[0], illegal_word)

    def test_commit_labels_precursors_and_silent_record_identity(self):
        initial = m.State("P", BASIS[1])
        first = m.apply_branch(initial, branch("P", "read", "0")).state
        switched = m.apply_branch(first, branch("P", "switch")).state
        self.assertIs(switched.records, first.records)
        second = m.apply_branch(switched, branch("Q", "read", "1")).state
        self.assertEqual(initial.records, ())
        self.assertEqual(len(first.records), 1)
        self.assertEqual(len(second.records), 2)
        self.assertIs(second.records[0], first.records[0])
        self.assertEqual(
            [(r.event_id, r.past, r.mode, r.action, r.outcome) for r in second.records],
            [(0, frozenset(), "P", "read", "0"), (1, frozenset({0}), "Q", "read", "1")],
        )
        third = m.apply_branch(second, branch("Q", "read", "1")).state
        self.assertEqual(third.records[2].past, frozenset({0, 1}))
        self.assertEqual(third.records[:2], second.records)

    def test_records_and_state_are_immutable_and_invalid_history_is_refused(self):
        state = m.apply_branch(m.State("P", BASIS[0]), branch("P", "read", "0")).state
        with self.assertRaises(FrozenInstanceError):
            state.mode = "Q"
        with self.assertRaises(FrozenInstanceError):
            state.records[0].outcome = "1"
        with self.assertRaises(TypeError):
            m.State("P", BASIS[0], list(state.records))
        with self.assertRaises(ValueError):
            m.State("P", BASIS[0], (replace(state.records[0], event_id=1),))
        with self.assertRaises(ValueError):
            m.State("P", BASIS[0], (replace(state.records[0], past=frozenset({0})),))
        with self.assertRaises(ValueError):
            m.append_record(state.records, branch("P", "switch"))

    def test_attempt_can_change_residual_without_committing_record(self):
        initial = m.State("Q", MIXED)
        silent = m.apply_branch(initial, branch("Q", "attempt", "epsilon"))
        self.assertEqual(silent.probability, F(4, 5))
        self.assertEqual(silent.state.coordinates, (F(1, 16), F(1, 4), F(3, 16), F(1, 2)))
        self.assertNotEqual(silent.state.coordinates, initial.coordinates)
        self.assertIs(silent.state.records, initial.records)
        committed = m.apply_branch(silent.state, branch("Q", "attempt", "1"))
        self.assertEqual(committed.probability, F(3, 32))
        self.assertEqual(committed.state.coordinates, BASIS[2])
        self.assertEqual(len(committed.state.records), 1)
        self.assertEqual(committed.state.records[0].action, "attempt")
        self.assertEqual(committed.state.records[0].outcome, "1")

    def test_zero_branch_cannot_create_a_record_or_conditional_state(self):
        initial = m.State("Q", BASIS[1])
        for outcome in ("0", "1"):
            item = branch("Q", "attempt", outcome)
            self.assertEqual(m.word_probability("Q", initial.coordinates, (item,)), 0)
            with self.assertRaises(ValueError):
                m.apply_branch(initial, item)
        self.assertEqual(initial.records, ())

    def test_future_effects_have_independent_full_rank_legal_word_certificates(self):
        effects = m.future_effects()
        self.assertEqual(set(effects), set(PARTITIONS))
        for mode, basis in effects.items():
            self.assertEqual(len(basis), 4)
            self.assertNotEqual(determinant(tuple(effect.row for effect in basis)), 0)
            self.assertEqual(basis[0].word, ())
            for effect in basis:
                current = mode
                for item in effect.word:
                    self.assertEqual(item.source, current)
                    self.assertIn(item, m.branches(current, item.action))
                    current = item.target
                independent_row = tuple(direct_word(x, effect.word) for x in BASIS)
                self.assertEqual(effect.row, independent_row)
                self.assertTrue(all(0 <= value <= 1 for value in effect.row))

    def test_distinguishing_word_exposes_equal_present_read_different_future(self):
        x, y = BASIS[0], BASIS[1]
        for outcome in ("0", "1"):
            read_word = (branch("P", "read", outcome),)
            self.assertEqual(
                m.word_probability("P", x, read_word), m.word_probability("P", y, read_word)
            )
        explicit = (branch("P", "switch"), branch("Q", "read", "0"))
        self.assertEqual(
            (m.word_probability("P", x, explicit), m.word_probability("P", y, explicit)), (1, 0)
        )
        result = m.equivalent("P", x, y)
        self.assertFalse(result.equivalent)
        self.assertIsNotNone(result.word)
        self.assertEqual(
            result.probabilities, (direct_word(x, result.word), direct_word(y, result.word))
        )
        self.assertNotEqual(*result.probabilities)

    def test_equivalence_detects_all_distinct_generators_and_exact_identity(self):
        for mode in PARTITIONS:
            for x, y in product((*BASIS, MIXED), repeat=2):
                result = m.equivalent(mode, x, y)
                self.assertEqual(result.equivalent, x == y)
                if x == y:
                    self.assertIsNone(result.word)
                    self.assertIsNone(result.probabilities)
                else:
                    self.assertEqual(
                        result.probabilities,
                        (direct_word(x, result.word), direct_word(y, result.word)),
                    )
                    self.assertNotEqual(*result.probabilities)

    def test_read_switch_read_provides_all_four_coordinate_effects(self):
        # This stronger explicit certificate needs neither attempt outcomes
        # nor any observation of a no-commit branch to distinguish shapes.
        for mode in PARTITIONS:
            other = "Q" if mode == "P" else "P"
            for r, s in product(range(2), repeat=2):
                word = (
                    branch(mode, "read", str(r)),
                    branch(mode, "switch"),
                    branch(other, "read", str(r ^ s)),
                )
                for x in (*BASIS, MIXED):
                    self.assertEqual(m.word_probability(mode, x, word), x[2 * r + s])

    def test_attempt_only_dark_equivalence_cannot_survive_added_read_action(self):
        x, y = BASIS[1], BASIS[3]
        silent = branch("Q", "attempt", "epsilon")
        for count in range(5):
            word = (silent,) * count
            self.assertEqual(m.word_probability("Q", x, word), 1)
            self.assertEqual(m.word_probability("Q", y, word), 1)
            for outcome in ("0", "1"):
                completed = (*word, branch("Q", "attempt", outcome))
                self.assertEqual(m.word_probability("Q", x, completed), 0)
                self.assertEqual(m.word_probability("Q", y, completed), 0)
        read = (branch("Q", "read", "0"),)
        self.assertEqual(
            (m.word_probability("Q", x, read), m.word_probability("Q", y, read)), (1, 0)
        )

    def test_declared_classical_product_local_maps_commute_and_preserve_mass(self):
        def local(operator, z, factor):
            if factor == 0:
                return tuple(
                    total(operator[i][k] * z[4 * k + j] for k in range(4))
                    for i, j in product(range(4), repeat=2)
                )
            return tuple(
                total(operator[j][k] * z[4 * i + k] for k in range(4))
                for i, j in product(range(4), repeat=2)
            )

        correlated = tuple(
            F(1, 3) if i == 0 else F(1, 6) if i == 7 else F(1, 2) if i == 10 else F(0)
            for i in range(16)
        )
        probes = (correlated, *(tuple(F(int(i == j)) for i in range(16)) for j in range(16)))
        for left_mode, right_mode in product(PARTITIONS, repeat=2):
            for left_action, right_action in product(m.actions(left_mode), m.actions(right_mode)):
                for z in probes:
                    total_probability = F(0)
                    for left, right in product(
                        m.branches(left_mode, left_action), m.branches(right_mode, right_action)
                    ):
                        left_first = local(right.matrix, local(left.matrix, z, 0), 1)
                        right_first = local(left.matrix, local(right.matrix, z, 1), 0)
                        self.assertEqual(left_first, right_first)
                        self.assertTrue(all(value >= 0 for value in left_first))
                        total_probability += total(left_first)
                    self.assertEqual(total_probability, 1)

    def test_declared_classical_product_kernel_is_product_recordable(self):
        z = tuple(
            F(1, 3) if i == 0 else F(1, 6) if i == 7 else F(1, 2) if i == 10 else F(0)
            for i in range(16)
        )
        for left_mode, right_mode in product(PARTITIONS, repeat=2):
            left_generators = tuple(expected_kernel(left_mode, x) for x in BASIS)
            right_generators = tuple(expected_kernel(right_mode, x) for x in BASIS)
            kernel = tuple(
                tuple(
                    total(
                        z[4 * i + j]
                        * left_generators[i][a // 4][b // 4]
                        * right_generators[j][a % 4][b % 4]
                        for i, j in product(range(4), repeat=2)
                    )
                    for b in range(16)
                )
                for a in range(16)
            )
            cells = tuple(
                tuple(4 * i + j for i, j in product(left, right))
                for left, right in product(PARTITIONS[left_mode], PARTITIONS[right_mode])
            )
            self.assertEqual(kernel_total(kernel), 1)
            for r, t in product(range(4), repeat=2):
                if r != t:
                    self.assertEqual(pair(kernel, cells[r], cells[t]), 0)
            expected_weights = tuple(
                total(
                    z[4 * i + j]
                    for i, j in product(range(4), repeat=2)
                    if i // 2 == r and j // 2 == t
                )
                for r, t in product(range(2), repeat=2)
            )
            self.assertEqual(tuple(pair(kernel, cell, cell) for cell in cells), expected_weights)

    def test_finite_legal_words_agree_with_direct_rule_not_conditional_renormalization(self):
        for mode in PARTITIONS:
            for word in legal_words(mode, 3):
                for x in (*BASIS, MIXED):
                    self.assertEqual(m.word_probability(mode, x, word), direct_word(x, word))
        total_probability = F(0)
        first = branch("P", "switch")
        for attempt, read in product(m.branches("Q", "attempt"), m.branches("Q", "read")):
            total_probability += m.word_probability("P", MIXED, (first, attempt, read))
        self.assertEqual(total_probability, 1)

    def test_repeated_attempt_first_commit_and_never_commit_are_separate(self):
        silent = branch("Q", "attempt", "epsilon")
        bright_mass, dark_mass = MIXED[0] + MIXED[2], MIXED[1] + MIXED[3]
        self.assertEqual((bright_mass, dark_mass), (F(2, 5), F(3, 5)))
        for count in range(9):
            survival = m.word_probability("Q", MIXED, (silent,) * count)
            self.assertEqual(survival, dark_mass + bright_mass / (2**count))
            committed = F(0)
            for n in range(count):
                for r in range(2):
                    probability = m.word_probability(
                        "Q", MIXED, (silent,) * n + (branch("Q", "attempt", str(r)),)
                    )
                    self.assertEqual(probability, MIXED[2 * r] / (2 ** (n + 1)))
                    committed += probability
            self.assertEqual(committed + survival, 1)
            self.assertEqual(committed, bright_mass * (1 - F(1, 2**count)))
            self.assertEqual(survival - dark_mass, bright_mass / (2**count))
        # These two invariant generators certify the nonzero limiting mass;
        # "never" is a probability of infinite survival, not a new record.
        for x in (BASIS[1], BASIS[3]):
            result = m.apply_branch(m.State("Q", x), silent)
            self.assertEqual(result.probability, 1)
            self.assertEqual(result.state.coordinates, x)
            self.assertEqual(result.state.records, ())


if __name__ == "__main__":
    unittest.main(verbosity=2)
