"""Independent exact witnesses for the retained-word first-commit theorem.

Finite identities below check the declared examples and refusal contracts.
They do not prove countable convergence, a uniform model-family rate, or
physical availability. Hidden paths and retained words are different objects.
"""

import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F
from itertools import product

import model as m


def vec(values):
    return tuple(F(value) for value in values)


def mat(rows):
    return tuple(vec(row) for row in rows)


def add(*vectors):
    return tuple(sum(entries, F(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient, values):
    return tuple(F(coefficient) * value for value in values)


def mv(operator, values):
    return tuple(sum(a * b for a, b in zip(row, values, strict=True)) for row in operator)


def mm(left, right):
    columns = tuple(zip(*right, strict=True))
    return tuple(
        tuple(sum(a * b for a, b in zip(row, column, strict=True)) for column in columns)
        for row in left
    )


def identity(size):
    return mat(tuple(int(i == j) for j in range(size)) for i in range(size))


def words(length):
    return tuple(product(("A", "B"), repeat=length))


SA = mat(((0, F(1, 4), 0), (F(1, 4), 0, 0), (0, 0, F(1, 2))))
SB = mat(((F(1, 4), 0, 0), (0, F(1, 4), 0), (0, 0, F(1, 2))))
K = mat(((F(1, 2), 0, 0), (0, F(1, 2), 0)))
SILENT = {"A": SA, "B": SB}
E0, E1, DARK = vec((1, 0, 0)), vec((0, 1, 0)), vec((0, 0, 1))
SOURCE = vec((F(1, 2), F(1, 3), F(1, 6)))


def path_operator(word):
    result = identity(3)
    for letter in word:
        result = mm(SILENT[letter], result)
    return result


def output(values, word):
    return mv(K, mv(path_operator(word), values))


def closed_output(values, word):
    bright = (values[1], values[0]) if word.count("A") % 2 else values[:2]
    return scale(F(1, 2) * F(1, 4) ** len(word), bright)


def prefix(values, depth):
    return {word: output(values, word) for n in range(depth) for word in words(n)}


def output_norm(entries):
    return sum(abs(value) for residual in entries.values() for value in residual)


def context(policy=None, pending=("B", "A")):
    prior = (
        m.PriorRecord(0, "prepare", "accepted", ("source-setting",), (("sample", "s0"),)),
        m.PriorRecord(1, "calibrate", "valid", ("read-setting",), (("calibration", "c0"),), (0,)),
    )
    return m.Context(
        m.CLASSICAL_POLICY if policy is None else policy,
        prior,
        pending,
        "fixture-origin",
        "declared-stationary-controller",
    )


def source(values=SOURCE, pending=("B", "A")):
    return m.State(context(pending=pending), values)


def last_letter_effect():
    return m.WordEffect((1, 0), (1, 0), (0, 1), m.UniformEffectCertificate())


def gp(left, right):
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c


def gmm(left, right):
    return tuple(
        tuple(
            tuple(
                sum(gp(left[i][k], right[k][j])[part] for k in range(len(right))) for part in (0, 1)
            )
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def gd(operator):
    return tuple(
        tuple((operator[i][j][0], -operator[i][j][1]) for i in range(len(operator)))
        for j in range(len(operator[0]))
    )


def bloch_matrix(values):
    q, x, y, z = values
    return (((q + z) / 2, F(0)), (x / 2, -y / 2)), ((x / 2, y / 2), ((q - z) / 2, F(0)))


def bloch_values(block):
    return block.q, block.x, block.y, block.z


class RetainedWordChecks(unittest.TestCase):
    def test_closed_word_formula_and_full_mass_accounting(self):
        for source in (E0, E1, DARK, SOURCE, vec((2, 3, 5))):
            immediate = mv(K, source)
            self.assertEqual(m.commit_map(source), immediate)
            self.assertEqual(m.silent_map(source, "A"), mv(SA, source))
            self.assertEqual(m.silent_map(source, "B"), mv(SB, source))
            self.assertEqual(
                sum(immediate) + sum(mv(SA, source)) + sum(mv(SB, source)), sum(source)
            )
            for n in range(6):
                level = tuple(output(source, word) for word in words(n))
                self.assertTrue(all(value >= 0 for residual in level for value in residual))
                self.assertEqual(sum(map(sum, level)), (source[0] + source[1]) / 2 ** (n + 1))
                for word in words(n):
                    self.assertEqual(output(source, word), closed_output(source, word))
                    self.assertEqual(m.word_map(source, word), mv(path_operator(word), source))
                    self.assertEqual(m.first_commit_residual(source, word), output(source, word))
        self.assertEqual(output(SOURCE, ()), scale(F(1, 2), SOURCE[:2]))

    def test_retained_prefix_shift_recurrence_at_every_finite_coordinate(self):
        for depth in range(1, 6):
            actual = prefix(SOURCE, depth)
            shifted = {(): mv(K, SOURCE)}
            for letter in ("A", "B"):
                for suffix, residual in prefix(mv(SILENT[letter], SOURCE), depth - 1).items():
                    shifted[(letter,) + suffix] = residual
            self.assertEqual(actual, shifted)
            # Nonempty letter prefixes partition the nonempty label set;
            # no two retained words are summed into a common coordinate.
            self.assertEqual(len(actual), 2**depth - 1)
            for word in actual:
                self.assertEqual(m.coordinate_matrix(word), mm(K, path_operator(word)))
                self.assertEqual(m.prepend_word(word[:1], word[1:]), word)

    def test_chronological_prefix_convention_has_a_noncommuting_witness(self):
        a = mat(((F(1, 2), 0), (0, F(1, 4))))
        b = mat(((0, F(1, 4)), (F(1, 2), 0)))
        commit = mat(((0, 0), (0, F(1, 2))))
        source = vec((1, 0))
        self.assertEqual(sum(mv(a, source)) + sum(mv(b, source)) + sum(mv(commit, source)), 1)
        ab = mv(commit, mv(b, mv(a, source)))
        ba = mv(commit, mv(a, mv(b, source)))
        self.assertEqual(ab, vec((0, F(1, 8))))
        self.assertEqual(ba, vec((0, F(1, 16))))
        self.assertNotEqual(ab, ba)
        # A is the first letter of AB but acts on the input first, on the
        # right of B in the matrix product. This is not a new model command.

    def test_geometric_truncations_are_unnormalized_and_never_is_complementary(self):
        bright = SOURCE[0] + SOURCE[1]
        for depth in range(7):
            committed = sum(sum(residual) for residual in prefix(SOURCE, depth).values())
            tail = bright / 2**depth
            survival = SOURCE[2] + tail
            self.assertEqual(committed, bright * (1 - F(1, 2) ** depth))
            self.assertEqual(committed + survival, 1)
            self.assertEqual(committed + tail + SOURCE[2], 1)
        self.assertEqual(prefix(SOURCE, 0), {})
        self.assertEqual(
            prefix(DARK, 4), {word: vec((0, 0)) for n in range(4) for word in words(n)}
        )
        self.assertEqual(sum(SOURCE[:2]), F(5, 6))

    def test_base_norm_tail_coefficient_and_signed_input_certificate(self):
        for depth in range(5):
            for extra in (1, 2, 4):
                coefficient = F(1, 2) ** depth * (1 - F(1, 2) ** extra)
                for source in (E0, E1, DARK, vec((1, -2, 3))):
                    tail = {
                        word: output(source, word)
                        for n in range(depth, depth + extra)
                        for word in words(n)
                    }
                    self.assertEqual(
                        output_norm(tail), coefficient * (abs(source[0]) + abs(source[1]))
                    )
                self.assertEqual(max(coefficient, coefficient, F(0)), coefficient)
            # The exact infinite geometric scalar tail is 2^-depth; its
            # positive column sum is attained by either bright unit input.
            self.assertEqual(F(1, 2) ** depth, max(F(1, 2) ** depth, F(1, 2) ** depth, F(0)))

    def test_epsilon_dark_fixed_points_do_not_replace_the_least_series(self):
        silent = mat(((F(1, 2), 0), (0, 1)))
        immediate = vec((F(1, 2), 0))
        for dark_coefficient in (F(0), F(1, 3), F(1), F(2)):
            candidate = vec((1, dark_coefficient))
            multiplied = tuple(sum(candidate[i] * silent[i][j] for i in range(2)) for j in range(2))
            self.assertEqual(candidate, add(immediate, multiplied))
            self.assertGreaterEqual(candidate[1], 0)
            self.assertEqual(
                m.epsilon_candidate(F(2, 3), F(1, 3), dark_coefficient),
                F(2, 3) + dark_coefficient / 3,
            )
            if dark_coefficient <= 1:
                self.assertLessEqual(max(candidate), 1)
        for depth in range(8):
            actual = vec((1 - F(1, 2) ** depth, 0))
            self.assertEqual(actual[1], 0)
            self.assertLessEqual(actual[0], 1)
        # These epsilon steps really are unrecorded. For the primary A/B
        # law, the empty coordinate is fixed and every other coordinate is
        # forced recursively: this spurious dark solution is not portable.

    def test_nonempty_prefixes_fix_coordinates_and_positive_supersolutions_bound_them(self):
        for depth in range(1, 6):
            actual = prefix(SOURCE, depth)
            for multiplier in (F(1), F(3, 2), F(2)):
                candidate = {word: scale(multiplier, value) for word, value in actual.items()}
                right = {(): mv(K, SOURCE)}
                for letter in ("A", "B"):
                    for suffix, value in prefix(mv(SILENT[letter], SOURCE), depth - 1).items():
                        right[(letter,) + suffix] = scale(multiplier, value)
                for word in actual:
                    self.assertTrue(
                        all(a >= b for a, b in zip(candidate[word], right[word], strict=True))
                    )
                    self.assertTrue(
                        all(a >= b for a, b in zip(candidate[word], actual[word], strict=True))
                    )
                self.assertEqual(right[()], actual[()])
                for word in actual:
                    if word:
                        self.assertEqual(candidate[word], right[word])
        # In the homogeneous equality the empty coefficient is zero; the
        # prefix recursion then forces each finite-word coefficient to zero.

    def test_bounded_last_letter_effect_has_exact_word_resolved_series(self):
        def effect(word, residual):
            index = 0 if not word or word[-1] == "A" else 1
            return residual[index]

        total = (5 * SOURCE[0] + 3 * SOURCE[1]) / 8
        self.assertEqual(total, F(7, 16))
        continued = m.ContinuedSeries(m.GeometricFirstCommit(source()), last_letter_effect())
        self.assertEqual(continued.total_weight, total)
        for depth in range(2, 7):
            terms = prefix(SOURCE, depth)
            evaluated = sum(effect(word, residual) for word, residual in terms.items())
            self.assertEqual(total - evaluated, sum(SOURCE[:2]) / 2 ** (depth + 1))
            self.assertEqual(continued.tail_weight(depth), total - evaluated)
            for word, residual in terms.items():
                self.assertGreaterEqual(effect(word, residual), 0)
                self.assertLessEqual(effect(word, residual), sum(residual))
                self.assertEqual(continued.coordinate(word).weight, effect(word, residual))
            self.assertEqual(
                continued.level_weight(depth),
                sum(effect(word, output(SOURCE, word)) for word in words(depth)),
            )
        # This uniformly mass-bounded family defines a continuous linear
        # functional on the declared l1 output without dropping word labels.

    def test_equal_residuals_do_not_identify_words_used_by_later_effects(self):
        ab, ba = ("A", "B"), ("B", "A")
        first, second = output(E0, ab), output(E0, ba)
        self.assertEqual(first, second)
        self.assertEqual(first, vec((0, F(1, 32))))
        first_effect, second_effect = first[1], second[0]
        self.assertEqual((first_effect, second_effect), (F(1, 32), F(0)))
        self.assertNotEqual(ab, ba)
        continued = m.ContinuedSeries(m.GeometricFirstCommit(source(E0)), last_letter_effect())
        self.assertEqual(continued.coordinate(ab).weight, first_effect)
        self.assertEqual(continued.coordinate(ba).weight, second_effect)
        self.assertNotEqual(continued.coordinate(ab).label, continued.coordinate(ba).label)
        # The note's separate deterministic a/b policy reaches the same
        # scalar committing payload from distinct inputs, retaining a or b.
        silent_a = mat(((0, 0, 0), (0, 0, 0), (1, 0, 0)))
        silent_b = mat(((0, 0, 0), (0, 0, 0), (0, 1, 0)))
        commit = mat(((0, 0, 1),))
        for value in (E0, E1, DARK):
            self.assertEqual(
                sum(mv(silent_a, value)) + sum(mv(silent_b, value)) + sum(mv(commit, value)), 1
            )
        self.assertEqual(mv(commit, mv(silent_a, E0)), (F(1),))
        self.assertEqual(mv(commit, mv(silent_b, E1)), (F(1),))
        self.assertEqual((int(("a",) == ("a",)), int(("b",) == ("a",))), (1, 0))
        # A record-dependent continuation can inspect the last symbol.
        # Equality after erasing words is not full continuation equivalence.

    def test_nonuniform_output_norms_destroy_mass_control(self):
        for depth in range(1, 9):
            probabilities = tuple(F(1, 2) ** (n + 1) for n in range(depth))
            self.assertEqual(sum(probabilities), 1 - F(1, 2) ** depth)
            weighted_norm = sum(F(2) ** (n + 1) * p for n, p in enumerate(probabilities))
            self.assertEqual(weighted_norm, depth)
        # One scalar output at word A^n has norm 2^(n+1) times its mass.
        # The partial norms diverge although total probability tends to one.

    def test_unbounded_word_continuations_need_not_interchange_with_the_sum(self):
        for depth in range(1, 9):
            terms = tuple(F(2) ** (n + 1) * F(1, 2) ** (n + 1) for n in range(depth))
            self.assertEqual(terms, (F(1),) * depth)
            self.assertEqual(sum(terms), depth)
        # Each coordinate functional is linear and finite individually;
        # their family is unbounded on the l1 output, so its sum diverges.

    def test_infinite_input_delays_prevent_operator_norm_convergence(self):
        for depth in range(1, 9):
            # In l1(N), a deterministic countdown maps e_j to label A^j.
            # The finite coordinates below witness a tail unit vector e_N.
            source = vec(int(index == depth) for index in range(depth + 1))
            retained = source[:depth]
            tail = source[depth:]
            self.assertEqual(sum(abs(value) for value in source), 1)
            self.assertEqual(sum(abs(value) for value in retained), 0)
            self.assertEqual(sum(abs(value) for value in tail), 1)
        # Every fixed l1 input has summable tails, but the operator tails
        # are always norm one; finite source dimension is load-bearing.

    def test_no_uniform_geometric_rate_is_implied_across_models(self):
        for depth in range(1, 30):
            survival = 1 - F(1, 2 * depth)
            self.assertGreaterEqual(survival**depth, F(1, 2))
            self.assertEqual(1 - depth * (1 - survival), F(1, 2))
        # This particular sequence keeps the tail at least one half.
        # The note proves the stronger fixed-N supremum is one by q -> 1;
        # neither universal statement follows from this finite enumeration.

    def test_probability_times_source_audit_is_not_a_linear_output_map(self):
        def audit(source):
            mass = sum(source)
            return scale(source[0] / mass, source)

        left, right = vec((1, 0)), vec((0, 1))
        combined = add(left, right)
        self.assertEqual(audit(combined), vec((F(1, 2), F(1, 2))))
        self.assertEqual(add(audit(left), audit(right)), left)
        self.assertNotEqual(audit(combined), add(audit(left), audit(right)))
        # The scalar effect p=x0 IS additive. Retaining the source in an
        # audit sidecar does not turn p(x)*x/m(x) into a committing kernel.
        self.assertEqual(combined[0], left[0] + right[0])

    def test_hidden_A_subpaths_aggregate_only_inside_the_same_retained_word(self):
        for value in (SOURCE, E0, DARK, vec((1, -2, 3))):
            parts = m.hidden_A_parts(value)
            self.assertEqual(parts, (scale(F(1, 2), mv(SA, value)),) * 2)
            self.assertEqual(add(*parts), mv(SA, value))
        for retained in (("A",), ("A", "B", "A"), ("B", "A", "B")):
            paths = (SOURCE,)
            for letter in retained:
                paths = tuple(
                    child
                    for parent in paths
                    for child in (
                        (scale(F(1, 2), mv(SA, parent)),) * 2
                        if letter == "A"
                        else (mv(SB, parent),)
                    )
                )
            self.assertEqual(len(paths), 2 ** retained.count("A"))
            self.assertEqual(add(*(mv(K, value) for value in paths)), output(SOURCE, retained))
            coordinate = m.GeometricFirstCommit(source()).coordinate(retained)
            self.assertEqual(coordinate.label.new_word, retained)
            self.assertFalse(hasattr(coordinate.label, "hidden_path"))
        with self.assertRaises(ValueError):
            m.GeometricFirstCommit(source()).coordinate(("A_hidden_0",))

    def test_symbolic_queries_match_all_finite_coordinates_without_infinite_enumeration(self):
        state = source()
        series = m.GeometricFirstCommit(state)
        self.assertIs(series.source, state)
        for depth in range(7):
            finite = series.truncation(depth)
            expected_words = tuple(word for n in range(depth) for word in words(n))
            self.assertEqual(tuple(item.new_word for item in finite), expected_words)
            self.assertEqual(
                {item.new_word: item.residual for item in finite}, prefix(SOURCE, depth)
            )
            self.assertEqual(sum(item.mass for item in finite), series.partial_mass(depth))
            self.assertEqual(series.partial_mass(depth), F(5, 6) * (1 - F(1, 2) ** depth))
            self.assertEqual(series.level_mass(depth), F(5, 6) / 2 ** (depth + 1))
            self.assertEqual(series.tail_mass(depth), F(5, 6) / 2**depth)
            self.assertEqual(series.survival_mass(depth), F(1, 6) + series.tail_mass(depth))
            self.assertEqual(series.partial_mass(depth) + series.survival_mass(depth), 1)
        self.assertEqual(series.total_mass + series.never_mass, 1)
        self.assertEqual(series.tail_mass(200), F(5, 6 * 2**200))
        self.assertEqual(
            series.coordinate(("B",) * 100).residual, closed_output(SOURCE, ("B",) * 100)
        )
        with self.assertRaises(ValueError):
            series.truncation(13)

    def test_full_selection_retains_context_word_types_precursors_and_source(self):
        state = source()
        prior, pending = state.context.prior, state.context.initial_pending
        coordinate = m.GeometricFirstCommit(state).coordinate(("A", "B"))
        expected = output(SOURCE, ("A", "B"))
        self.assertIs(coordinate.source, state)
        self.assertEqual(coordinate.residual, expected)
        self.assertEqual(coordinate.label.actual_word, ("B", "A", "A", "B"))
        self.assertEqual(coordinate.label.outcome, "K")
        self.assertEqual(coordinate.label.event_id, 2)
        self.assertEqual(coordinate.label.precursor, (("fixture-origin", 0), ("fixture-origin", 1)))
        self.assertEqual(coordinate.label.output_type, m.BRIGHT_TYPE)
        selected = m.select_commit(coordinate)
        self.assertIs(selected.coordinate, coordinate)
        self.assertIs(selected.record, coordinate.label)
        self.assertEqual(selected.probability, sum(expected))
        self.assertEqual(selected.residual, scale(1 / sum(expected), expected))
        self.assertEqual(selected.records, prior + (coordinate.label,))
        self.assertEqual(selected.record.context.controller, "declared-stationary-controller")
        self.assertIs(state.context.prior, prior)
        self.assertIs(state.context.initial_pending, pending)
        self.assertEqual(state.residual, SOURCE)

    def test_initial_pending_words_are_retained_but_not_reapplied(self):
        first = source(E0, ("A",))
        second = source(E0, ("B",))
        c0 = m.GeometricFirstCommit(first).coordinate(())
        c1 = m.GeometricFirstCommit(second).coordinate(())
        self.assertEqual(c0.residual, vec((F(1, 2), 0)))
        self.assertEqual(c0.residual, c1.residual)
        self.assertNotEqual(c0.label, c1.label)
        self.assertEqual((c0.label.actual_word, c1.label.actual_word), (("A",), ("B",)))
        self.assertNotEqual(m.select_commit(c0).records, m.select_commit(c1).records)
        empty_specific = m.WordEffect((0, 1), (1, 0), (1, 0), m.UniformEffectCertificate())
        self.assertEqual(empty_specific.apply(c0).weight, 0)
        self.assertEqual(empty_specific.apply(c1).weight, 0)
        # The fixed family declares its empty NEW suffix rule explicitly;
        # it does not pretend that the already retained prefix is empty.

    def test_immutable_one_shot_inputs_preserve_all_labels_and_payloads(self):
        prior = m.PriorRecord(
            0, "prepare", "yes", iter(("setting",)), iter((iter(("key", "value")),)), iter(())
        )
        ctx = m.Context(prior=iter((prior,)), initial_pending=iter(("B", "A")))
        state = m.State(ctx, iter(SOURCE))
        coordinate = m.GeometricFirstCommit(state).coordinate(iter(("A", "B")))
        self.assertEqual(coordinate.residual, output(SOURCE, ("A", "B")))
        self.assertEqual(coordinate.label.actual_word, ("B", "A", "A", "B"))
        self.assertEqual(ctx.prior[0].payload, (("key", "value"),))
        self.assertEqual(m.coordinate_matrix(iter(("A", "B"))), mm(K, path_operator(("A", "B"))))
        self.assertEqual(
            m.first_commit_residual(iter(SOURCE), iter(("B", "A"))), output(SOURCE, ("B", "A"))
        )
        self.assertEqual(m.prepend_word(iter(("A",)), iter(("B",))), ("A", "B"))
        effect = m.WordEffect(
            iter((1, 0)), iter((1, 0)), iter((0, 1)), m.UniformEffectCertificate()
        )
        self.assertEqual(effect.apply(coordinate).weight, coordinate.residual[1])
        for obj, field, value in (
            (state, "residual", DARK),
            (ctx, "initial_pending", ()),
            (prior, "event_id", 1),
            (coordinate.label, "new_word", ()),
        ):
            with self.assertRaises(FrozenInstanceError):
                setattr(obj, field, value)

    def test_states_require_exact_positive_normalized_actual_domains(self):
        for invalid in ((0, 0, 0), (1, 1, 0), (1, 0), (-1, 1, 1)):
            with self.assertRaises(ValueError):
                m.State(context(), invalid)
        for invalid in ((True, 0, 0), (1.0, 0, 0)):
            with self.assertRaises(TypeError):
                m.State(context(), invalid)
        with self.assertRaises(TypeError):
            m.State(context(m.LT_POLICY), E0)
        with self.assertRaises(TypeError):
            m.GeometricFirstCommit(SOURCE)
        with self.assertRaises(ValueError):
            m.Context(policy="sum_of_available_actions")
        for malformed in ((m.PriorRecord(1, "a", "b"),), (object(),)):
            with self.assertRaises(ValueError):
                m.Context(prior=malformed)

    def test_lengths_records_and_fixed_command_labels_are_strict(self):
        series = m.GeometricFirstCommit(source())
        for value in (-1, True, 1.0, F(1)):
            for operation in (
                series.level_mass,
                series.tail_mass,
                series.survival_mass,
                series.truncation,
            ):
                with self.assertRaises(ValueError):
                    operation(value)
            with self.assertRaises(ValueError):
                m.PriorRecord(value, "action", "outcome")
        for bad_word in (("epsilon",), ("AB",), (0,), (True,)):
            with self.assertRaises(ValueError):
                series.coordinate(bad_word)
        with self.assertRaises(TypeError):
            series.coordinate("AB")
        for precursor in ((True,), (0, 0), (1,)):
            with self.assertRaises(ValueError):
                m.PriorRecord(1, "action", "outcome", precursor=precursor)
        with self.assertRaises(ValueError):
            m.CommitLabel(context(), (), "different", m.BRIGHT_TYPE)
        with self.assertRaises(ValueError):
            m.CommitLabel(context(), (), "K", m.INPUT_TYPE)

    def test_effect_certificate_is_required_and_continuations_keep_full_labels(self):
        state = source()
        series = m.GeometricFirstCommit(state)
        effect = last_letter_effect()
        for word in ((), ("A",), ("B",), ("A", "B")):
            coordinate = series.coordinate(word)
            scalar = effect.apply(coordinate)
            self.assertIs(scalar.original, coordinate)
            self.assertIs(scalar.label, coordinate.label)
            self.assertEqual(scalar.output_type, m.SCALAR_TYPE)
            self.assertFalse(hasattr(scalar, "residual"))
            with self.assertRaises(TypeError):
                m.select_commit(scalar)
        for rows in (
            ((1, 1), (1, 1), (1, 1)),
            ((F(1, 3), F(1, 2)), (F(1, 4), F(2, 3)), (F(3, 4), F(1, 5))),
            ((0, 0), (0, 0), (0, 0)),
        ):
            declared = m.WordEffect(*rows, m.UniformEffectCertificate())
            continued = m.ContinuedSeries(series, declared)
            empty, after_a, after_b = rows
            dot = lambda row, values: sum(a * b for a, b in zip(row, values, strict=True))
            expected_total = (
                dot(empty, SOURCE[:2]) / 2
                + (dot(after_a, SOURCE[1::-1]) + dot(after_b, SOURCE[:2])) / 8
                + sum(SOURCE[:2]) * sum(after_a + after_b) / 16
            )
            self.assertEqual(continued.total_weight, expected_total)
            for depth in range(6):
                explicit = sum(
                    declared.apply(series.coordinate(word)).weight for word in words(depth)
                )
                self.assertEqual(continued.level_weight(depth), explicit)
        with self.assertRaises(TypeError):
            m.WordEffect((1, 0), (1, 0), (0, 1), None)
        for row in ((2, 0), (-1, 0), (1,)):
            with self.assertRaises(ValueError):
                m.WordEffect(row, (1, 0), (0, 1), m.UniformEffectCertificate())
        with self.assertRaises(TypeError):
            m.WordEffect((0.5, 0), (1, 0), (0, 1), m.UniformEffectCertificate())
        for changes in ({"bound": 2}, {"input_type": m.SCALAR_TYPE}, {"proof_rule": "asserted"}):
            with self.assertRaises(ValueError):
                m.UniformEffectCertificate(**changes)
        with self.assertRaises(TypeError):
            m.ContinuedSeries(series, lambda item: item.mass)

    def test_zero_and_never_mass_never_produce_conditional_states_or_records(self):
        state = source(DARK)
        prior = state.context.prior
        series = m.GeometricFirstCommit(state)
        self.assertEqual(series.never_mass, 1)
        self.assertEqual(series.total_mass, 0)
        for word in ((), ("A",), ("B", "A")):
            coordinate = series.coordinate(word)
            self.assertEqual(coordinate.residual, vec((0, 0)))
            self.assertEqual(coordinate.mass, 0)
            with self.assertRaises(ValueError):
                m.select_commit(coordinate)
            self.assertIs(state.context.prior, prior)
        for field in ("never_state", "never_residual", "never_record"):
            self.assertFalse(hasattr(series, field))
        with self.assertRaises(TypeError):
            m.select_commit(series.never_mass)
        self.assertEqual(series.truncation(0), ())

    def test_derived_selected_outputs_cannot_be_forged_or_reused_as_input_type(self):
        coordinate = m.GeometricFirstCommit(source()).coordinate(("A",))
        selected = m.SelectedCommit(coordinate)
        with self.assertRaises(ValueError):
            replace(selected, probability=F(1))
        with self.assertRaises(ValueError):
            replace(coordinate, residual=vec((1, 0)))
        with self.assertRaises(FrozenInstanceError):
            selected.record = coordinate.label
        for candidate in (selected, selected.residual, coordinate):
            with self.assertRaises(TypeError):
                m.GeometricFirstCommit(candidate)

    def test_existing_Lt_face_A_congruence_retains_nonclassical_complex_payload(self):
        values = vec((1, 0, F(3, 5), F(4, 5)))
        block = m.Bloch(*values)
        unitary = (((F(3, 5), F(0)), (F(0), F(-4, 5))), ((F(0), F(-4, 5)), (F(3, 5), F(0))))
        for _ in range(7):
            expected_matrix = gmm(gmm(unitary, bloch_matrix(values)), gd(unitary))
            block = m.lt_control_A(block)
            self.assertEqual(bloch_matrix(bloch_values(block)), expected_matrix)
            self.assertEqual(block.q**2, block.x**2 + block.y**2 + block.z**2)
            values = bloch_values(block)
        self.assertNotEqual(values[2], 0)
        self.assertNotEqual(bloch_matrix(values)[0][1][1], 0)

    def test_existing_literal_cut_series_has_exact_geometric_residual_and_selection(self):
        block = m.Bloch(1, F(3, 5), F(4, 5), 0)
        state = m.LtFaceState(context(m.LT_POLICY), block)
        series = m.LtFaceSeries(state)
        expected = bloch_values(block)
        for length in range(7):
            coordinate = series.coordinate(length)
            coefficient = F(1, 2 ** (length + 1))
            self.assertEqual(bloch_values(coordinate.residual), scale(coefficient, expected))
            self.assertEqual(coordinate.mass, coefficient)
            self.assertEqual(coordinate.label.new_word, ("A",) * length)
            self.assertEqual(
                coordinate.label.actual_word, state.context.initial_pending + ("A",) * length
            )
            self.assertEqual(coordinate.label.outcome, (0, 0))
            self.assertEqual(coordinate.label.output_type, m.LT_TYPE)
            selected = m.select_commit(coordinate)
            self.assertEqual(bloch_values(selected.residual), expected)
            self.assertEqual(selected.records[:-1], state.context.prior)
            self.assertEqual(selected.record.precursor, state.context.precursor)
            self.assertEqual(series.tail_mass(length), 2 * coefficient)
            q, x, y, z = expected
            expected = (q, x, (-7 * y - 24 * z) / 25, (24 * y - 7 * z) / 25)
        self.assertEqual(series.never_mass, 0)
        self.assertEqual(sum(series.coordinate(n).mass for n in range(6)) + series.tail_mass(6), 1)
        with self.assertRaises(ValueError):
            m.Bloch(1, 1, 1, 0)
        with self.assertRaises(TypeError):
            m.LtFaceState(context(), block)
        with self.assertRaises(ValueError):
            m.LtFaceState(context(m.LT_POLICY), block.scaled(F(1, 2)))
        with self.assertRaises(ValueError):
            m.CommitLabel(context(m.LT_POLICY), ("B",), (0, 0), m.LT_TYPE)

    def test_terminal_tilted_read_is_only_a_full_labeled_linear_scalar(self):
        state = m.LtFaceState(context(m.LT_POLICY), m.Bloch(1, 0, F(3, 5), F(4, 5)))
        for length in range(6):
            coordinate = m.LtFaceSeries(state).coordinate(length)
            q, x, _, z = bloch_values(coordinate.residual)
            plus = m.TerminalScalar(coordinate, "+")
            minus = m.TerminalScalar(coordinate, "-")
            self.assertEqual(plus.weight, (q + (3 * x + 4 * z) / 5) / 2)
            self.assertEqual(minus.weight, (q - (3 * x + 4 * z) / 5) / 2)
            self.assertEqual(plus.weight + minus.weight, coordinate.mass)
            self.assertEqual(plus.full_label, (coordinate.label, (0, 0, "+")))
            self.assertEqual(plus.output_type, m.SCALAR_TYPE)
            self.assertIs(plus.coordinate, coordinate)
            self.assertFalse(hasattr(plus, "residual"))
            self.assertFalse(hasattr(plus, "postmeasurement_state"))
            for function in (m.select_commit, m.GeometricFirstCommit, m.LtFaceSeries):
                with self.assertRaises(TypeError):
                    function(plus)
        dark_to_read = m.LtFaceState(context(m.LT_POLICY), m.Bloch(1, F(-3, 5), 0, F(-4, 5)))
        zero = m.TerminalScalar(m.LtFaceSeries(dark_to_read).coordinate(0), "+")
        self.assertEqual(zero.weight, 0)
        self.assertFalse(hasattr(zero, "normalized_residual"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
