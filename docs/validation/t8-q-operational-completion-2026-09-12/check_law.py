"""Bounded exact checks of the chosen two-port X/Y/Z renewal protocol.

This checks a protocol within a conditionally reconstructed finite quantum
framework. It does not verify reconstruction axioms, purification, physical
observations or universal control. No old mathematical module is imported;
there is no growth census, sampling, parameter search or capture.
"""

import itertools
import unittest
from fractions import Fraction as F

ZERO = (F(0), F(0))
ONE = (F(1), F(0))
IMAGINARY = (F(0), F(1))


def scalar(value):
    return value if type(value) is tuple else (F(value), F(0))


def plus(a, b):
    return (a[0] + b[0], a[1] + b[1])


def times(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def conjugate(a):
    return (a[0], -a[1])


def matrix(rows):
    return [[scalar(value) for value in row] for row in rows]


def zeros(n=4):
    return [[ZERO for _ in range(n)] for _ in range(n)]


def identity(n=4):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def scale(value, a):
    value = scalar(value)
    return [[times(value, entry) for entry in row] for row in a]


def add(a, b):
    return [
        [plus(x, y) for x, y in zip(arow, brow, strict=True)]
        for arow, brow in zip(a, b, strict=True)
    ]


def multiply(a, b):
    result = zeros(len(a))
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                if a[i][k] != ZERO and b[k][j] != ZERO:
                    result[i][j] = plus(result[i][j], times(a[i][k], b[k][j]))
    return result


def adjoint(a):
    return [[conjugate(a[j][i]) for j in range(len(a))] for i in range(len(a))]


def tensor(a, b):
    return [
        [times(a[i][j], b[k][l]) for j in range(len(a)) for l in range(len(b))]
        for i in range(len(a))
        for k in range(len(b))
    ]


def trace(a):
    result = ZERO
    for i, row in enumerate(a):
        result = plus(result, row[i])
    return result


def normalize(a):
    real, imaginary = trace(a)
    if imaginary or real <= 0:
        raise ValueError("conditional state requires strictly positive real branch mass")
    return scale(1 / real, a)


def unit(i, j):
    result = zeros()
    result[i][j] = ONE
    return result


def dense_involution(action, context):
    """First route: explicit local matrices, tensoring and dense products."""
    local = (
        matrix([[0, 1], [1, 0]]),
        matrix([[0, (F(0), F(-1))], [IMAGINARY, 0]]),
        matrix([[1, 0], [0, -1]]),
    )[context]
    if action == "a":
        return tensor(local, identity(2))
    if action == "b":
        return tensor(identity(2), local)
    if action == "ab":
        return tensor(local, local)
    raise ValueError("unknown action")


def dense_projector(action, context, outcome):
    return scale(
        F(1, 2), add(identity(), scale((-1) ** outcome, dense_involution(action, context)))
    )


def dense_branch(a, action, context, outcome):
    if outcome is None:
        return zeros()
    projection = dense_projector(action, context, outcome)
    return scale(F(1, 3), multiply(multiply(projection, a), projection))


def basis_action(action, context, index):
    """Independent route: bit flips and phases, with no dense matrix lookup."""
    bits = [index // 2, index % 2]
    phase = ONE
    for name, position in (("a", 0), ("b", 1)):
        if name not in action:
            continue
        old_bit = bits[position]
        if context == 0:
            bits[position] = 1 - old_bit
        elif context == 1:
            phase = times(phase, (F(0), F(1 if old_bit == 0 else -1)))
            bits[position] = 1 - old_bit
        elif context == 2:
            phase = times(phase, (F(1 if old_bit == 0 else -1), F(0)))
        else:
            raise ValueError("unknown context")
    return 2 * bits[0] + bits[1], phase


def formula_unit(i, j, action, context, outcome):
    """(Eij + s T Eij + s Eij T + T Eij T)/12, by basis action."""
    result = zeros()
    if outcome is None:
        return result
    target_i, phase_i = basis_action(action, context, i)
    target_j, phase_j = basis_action(action, context, j)
    sign = scalar((-1) ** outcome)
    terms = (
        (i, j, ONE),
        (target_i, j, times(sign, phase_i)),
        (i, target_j, times(sign, conjugate(phase_j))),
        (target_i, target_j, times(phase_i, conjugate(phase_j))),
    )
    for row, column, coefficient in terms:
        result[row][column] = plus(result[row][column], times(scalar(F(1, 12)), coefficient))
    return result


def formula_branch(a, action, context, outcome):
    result = zeros()
    for i in range(4):
        for j in range(4):
            if a[i][j] != ZERO:
                result = add(result, scale(a[i][j], formula_unit(i, j, action, context, outcome)))
    return result


def context_at(history, action):
    """Committed-head ideal and sum of its binary outcomes modulo three."""
    heads, pasts, outcomes = {}, {}, {}
    records = []
    for event, ports, outcome in history:
        past = set()
        for port in ports:
            if port in heads:
                head = heads[port]
                past |= pasts[head] | {head}
        context = sum(outcomes[ancestor] for ancestor in past) % 3
        records.append([event, ports, outcome, context])
        pasts[event], outcomes[event] = past, outcome
        for port in ports:
            heads[port] = event
    past = set()
    for port in action:
        if port in heads:
            head = heads[port]
            past |= pasts[head] | {head}
    return {
        "past": sorted(past),
        "context": sum(outcomes[ancestor] for ancestor in past) % 3,
        "records": sorted(records),
        "order": sorted(
            [ancestor, event] for event, ancestors in pasts.items() for ancestor in ancestors
        ),
    }


class ChosenLawChecks(unittest.TestCase):
    def test_1_involution_and_projection_identities(self):
        for action, context in itertools.product(("a", "b", "ab"), range(3)):
            involution = dense_involution(action, context)
            self.assertEqual(adjoint(involution), involution)
            self.assertEqual(multiply(involution, involution), identity())
            p, q = (dense_projector(action, context, outcome) for outcome in (0, 1))
            self.assertEqual(add(p, q), identity())
            self.assertEqual(multiply(p, q), zeros())
            self.assertEqual(multiply(q, p), zeros())
            for projection in (p, q):
                self.assertEqual(adjoint(projection), projection)
                self.assertEqual(multiply(projection, projection), projection)
        # These identities support the conditional positivity proof P rho P >= 0;
        # a finite test does not enumerate all positive preparations.

    def test_2_all_288_complete_matrix_unit_map_comparisons(self):
        count = 0
        for action, context, outcome, i, j in itertools.product(
            ("a", "b", "ab"), range(3), (0, 1), range(4), range(4)
        ):
            self.assertEqual(
                dense_branch(unit(i, j), action, context, outcome),
                formula_unit(i, j, action, context, outcome),
            )
            count += 1
        self.assertEqual(count, 18 * 16)

    def test_3_all_576_complete_disjoint_basis_compositions(self):
        count = 0
        for ca, cb, xa, xb, i, j in itertools.product(
            range(3), range(3), (0, 1), (0, 1), range(4), range(4)
        ):
            source = unit(i, j)
            ab = dense_branch(dense_branch(source, "a", ca, xa), "b", cb, xb)
            ba = dense_branch(dense_branch(source, "b", cb, xb), "a", ca, xa)
            independent_ab = formula_branch(formula_unit(i, j, "a", ca, xa), "b", cb, xb)
            independent_ba = formula_branch(formula_unit(i, j, "b", cb, xb), "a", ca, xa)
            self.assertEqual(ab, ba)
            self.assertEqual(ab, independent_ab)
            self.assertEqual(ba, independent_ba)
            count += 1
        self.assertEqual(count, 576)

    def test_4_normalization_is_not_nondisturbance(self):
        for context, i, j in itertools.product(range(3), range(4), range(4)):
            source = unit(i, j)
            combined = zeros()
            for action in ("a", "b", "ab"):
                partial = add(
                    dense_branch(source, action, context, 0),
                    dense_branch(source, action, context, 1),
                )
                self.assertEqual(trace(partial), times(scalar(F(1, 3)), trace(source)))
                combined = add(combined, partial)
            self.assertEqual(trace(combined), trace(source))
        prepared = unit(0, 0)
        discarded_x = scale(
            3, add(dense_branch(prepared, "a", 0, 0), dense_branch(prepared, "a", 0, 1))
        )
        self.assertEqual(trace(discarded_x), ONE)
        self.assertNotEqual(discarded_x, prepared)
        self.assertEqual(discarded_x, scale(F(1, 2), add(unit(0, 0), unit(2, 2))))

    def test_5_actual_and_formal_zero_branches_are_not_normalized(self):
        prepared = tensor(matrix([[1, 0], [0, 0]]), scale(F(1, 2), identity(2)))
        actual = dense_branch(prepared, "a", 2, 1)
        self.assertEqual(actual, zeros())
        self.assertEqual(actual, formula_branch(prepared, "a", 2, 1))
        with self.assertRaises(ValueError):
            normalize(actual)
        for action, context in itertools.product(("a", "b", "ab"), range(3)):
            formal = dense_branch(prepared, action, context, None)
            self.assertEqual(formal, zeros())
            self.assertEqual(formal, formula_branch(prepared, action, context, None))
            with self.assertRaises(ValueError):
                normalize(formal)
        self.assertEqual(trace(dense_branch(prepared, "a", 2, 0)), scalar(F(1, 3)))

    def test_6_mixture_conditioning_uses_branch_probability_weights(self):
        first = unit(0, 0)
        second = scale(F(1, 2), add(unit(1, 1), unit(3, 3)))
        weight = F(1, 3)
        mixture = add(scale(weight, first), scale(1 - weight, second))
        out_first = dense_branch(first, "a", 2, 0)
        out_second = dense_branch(second, "a", 2, 0)
        out_mix = dense_branch(mixture, "a", 2, 0)
        self.assertEqual(out_mix, add(scale(weight, out_first), scale(1 - weight, out_second)))
        self.assertEqual(trace(out_first), scalar(F(1, 3)))
        self.assertEqual(trace(out_second), scalar(F(1, 6)))
        self.assertEqual(trace(out_mix), scalar(F(2, 9)))
        posterior = normalize(out_mix)
        self.assertEqual(
            posterior,
            add(scale(F(1, 2), normalize(out_first)), scale(F(1, 2), normalize(out_second))),
        )
        incorrect = add(
            scale(weight, normalize(out_first)), scale(1 - weight, normalize(out_second))
        )
        self.assertNotEqual(posterior, incorrect)

    def test_7_imaginary_coherence_readout_after_a_genuinely_reachable_prefix(self):
        history = [[0, "b", 1], [1, "ab", 0]]
        context = context_at(history, "a")
        self.assertEqual(context["records"], [[0, "b", 1, 0], [1, "ab", 0, 1]])
        self.assertEqual(context["past"], [0, 1])
        self.assertEqual(context["context"], 1)
        states = []
        weights = []
        whole_history_weights = []
        for sign in (1, -1):
            local = matrix([[F(1, 2), (F(0), F(-sign, 4))], [(F(0), F(sign, 4)), F(1, 2)]])
            # Exact eigenvalues 1/4 and 3/4 certify this local preparation.
            determinant = F(1, 4) - F(1, 16)
            self.assertEqual(determinant, F(3, 16))
            self.assertEqual(F(1, 4) * F(3, 4), determinant)
            prepared = tensor(local, scale(F(1, 2), identity(2)))
            self.assertEqual(adjoint(prepared), prepared)
            self.assertEqual(trace(prepared), ONE)
            first = dense_branch(prepared, "b", 0, 1)
            self.assertEqual(trace(first), scalar(F(1, 6)))
            raw_prefix = dense_branch(first, "ab", 1, 0)
            self.assertEqual(trace(raw_prefix), scalar(F(1, 36)))
            independent_prefix = formula_branch(formula_branch(prepared, "b", 0, 1), "ab", 1, 0)
            self.assertEqual(raw_prefix, independent_prefix)
            residual = normalize(raw_prefix)
            output = dense_branch(residual, "a", context["context"], 0)
            self.assertEqual(output, formula_branch(residual, "a", 1, 0))
            whole_history = dense_branch(raw_prefix, "a", 1, 0)
            self.assertEqual(trace(whole_history), times(trace(raw_prefix), trace(output)))
            weights.append(trace(output))
            whole_history_weights.append(trace(whole_history))
            states.append(prepared)
        self.assertEqual([states[0][i][i] for i in range(4)], [states[1][i][i] for i in range(4)])
        self.assertNotEqual(states[0], states[1])
        self.assertEqual(weights, [scalar(F(1, 4)), scalar(F(1, 12))])
        self.assertEqual(
            [times(scalar(3), value) for value in weights], [scalar(F(3, 4)), scalar(F(1, 4))]
        )
        self.assertEqual(whole_history_weights, [scalar(F(1, 144)), scalar(F(1, 432))])
        self.assertIn([2, "a", 0, 1], context_at(history + [[2, "a", 0]], "a")["records"])

    def test_8_three_fixed_contexts_preserve_the_full_swapped_marked_order(self):
        prefixes = (
            [[0, "ab", 0]],
            [[0, "ab", 1]],
            [[0, "ab", 1], [1, "ab", 1]],
        )
        for expected_context, prefix in enumerate(prefixes):
            before_a = context_at(prefix, "a")
            before_b = context_at(prefix, "b")
            self.assertEqual(before_a["context"], expected_context)
            self.assertEqual(before_b["context"], expected_context)
            a, b = [10, "a", 1], [11, "b", 0]
            self.assertEqual(context_at(prefix + [a], "b")["past"], before_b["past"])
            self.assertEqual(context_at(prefix + [a], "b")["context"], expected_context)
            self.assertEqual(context_at(prefix + [b], "a")["past"], before_a["past"])
            self.assertEqual(context_at(prefix + [b], "a")["context"], expected_context)
            self.assertEqual(context_at(prefix + [a, b], "ab"), context_at(prefix + [b, a], "ab"))
            terminal = context_at(prefix + [a, b], "ab")
            self.assertIn([10, "a", 1, expected_context], terminal["records"])
            self.assertIn([11, "b", 0, expected_context], terminal["records"])
            self.assertNotIn([10, 11], terminal["order"])
            self.assertNotIn([11, 10], terminal["order"])

    def test_9_same_port_noncommutation_and_y_sign_controls(self):
        x_then_y = dense_branch(dense_branch(unit(0, 0), "a", 0, 0), "a", 1, 0)
        y_then_x = dense_branch(dense_branch(unit(0, 0), "a", 1, 0), "a", 0, 0)
        self.assertNotEqual(x_then_y, y_then_x)
        self.assertEqual(trace(x_then_y), trace(y_then_x))
        self.assertEqual(basis_action("a", 1, 0), (2, IMAGINARY))
        self.assertEqual(basis_action("a", 1, 2), (0, (F(0), F(-1))))
        self.assertEqual(basis_action("ab", 1, 0), (3, scalar(-1)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
