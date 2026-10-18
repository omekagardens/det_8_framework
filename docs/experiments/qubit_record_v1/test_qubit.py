"""Focused exact ordinary-qubit/bridge checks; no accepted DET imports."""

import unittest
from dataclasses import FrozenInstanceError
from fractions import Fraction

import qubit as q

F = Fraction


class QubitTests(unittest.TestCase):
    def test_axes_are_exact_unit_vectors_and_immutable(self):
        self.assertEqual(tuple(q.AXES), ("X", "Y", "Z", "W"))
        self.assertEqual(q.AXES["W"], (F(0), F(3, 5), F(4, 5)))
        for axis in q.AXES.values():
            self.assertEqual(sum(v * v for v in axis), 1)
        with self.assertRaises(TypeError):
            q.AXES["other"] = (F(1), F(0), F(0))

    def test_bloch_canonical_exact_immutable_snapshot(self):
        state = q.Bloch(iter((0, F(3, 5), F(4, 5))))
        self.assertEqual(state.r, (F(0), F(3, 5), F(4, 5)))
        self.assertTrue(all(type(value) is F for value in state.r))
        with self.assertRaises(FrozenInstanceError):
            state.r = (F(0), F(0), F(0))

    def test_invalid_bloch_coordinates_are_refused(self):
        for values in ((), (0, 0), (0, 0, 0, 0), (1, 1, 0), (F(6, 5), 0, 0)):
            with self.subTest(values=values), self.assertRaises(ValueError):
                q.Bloch(values)
        for values in ((True, 0, 0), (0.0, 0, 0), (0j, 0, 0), ("0", 0, 0), "000"):
            with self.subTest(values=values), self.assertRaises(TypeError):
                q.Bloch(values)

    def test_plus_probability_matches_independent_exact_dot_product(self):
        state = q.Bloch((F(1, 5), F(-2, 5), F(1, 2)))
        expected = {"X": F(3, 5), "Y": F(3, 10), "Z": F(3, 4), "W": F(29, 50)}
        for setting, probability in expected.items():
            self.assertEqual(q.plus_probability(state, setting), probability)
            self.assertEqual(q.outcome_probability(state, setting, 1), probability)
            self.assertEqual(q.outcome_probability(state, setting, -1), 1 - probability)

    def test_opposite_phases_have_equal_z_and_opposite_y_laws(self):
        plus, minus = q.Bloch((0, 1, 0)), q.Bloch((0, -1, 0))
        self.assertEqual(q.plus_probability(plus, "Z"), F(1, 2))
        self.assertEqual(q.plus_probability(minus, "Z"), F(1, 2))
        self.assertEqual(q.plus_probability(plus, "Y"), 1)
        self.assertEqual(q.plus_probability(minus, "Y"), 0)
        self.assertEqual(q.plus_probability(plus, "W"), F(4, 5))
        self.assertEqual(q.plus_probability(minus, "W"), F(1, 5))

    def test_selective_same_axis_repeatability_for_all_settings(self):
        initial = q.Bloch((0, 0, 0))
        for setting, axis in q.AXES.items():
            for outcome in (-1, 1):
                with self.subTest(setting=setting, outcome=outcome):
                    output = q.selective_update(initial, setting, outcome)
                    self.assertEqual(output.r, tuple(outcome * value for value in axis))
                    self.assertEqual(q.outcome_probability(output, setting, outcome), 1)
                    self.assertEqual(q.selective_update(output, setting, outcome), output)
                    with self.assertRaises(q.ModelMismatch):
                        q.selective_update(output, setting, -outcome)

    def test_zero_observed_branch_refuses_without_mutating_source(self):
        source = q.Bloch((0, 0, 1))
        with self.assertRaisesRegex(q.ModelMismatch, "retain its record"):
            q.selective_update(source, "Z", -1)
        self.assertEqual(source.r, (0, 0, 1))

    def test_nonselective_z_erases_phase(self):
        plus, minus = q.Bloch((0, 1, 0)), q.Bloch((0, -1, 0))
        self.assertEqual(q.nonselective_update(plus, "Z"), q.Bloch((0, 0, 0)))
        self.assertEqual(q.nonselective_update(minus, "Z"), q.Bloch((0, 0, 0)))
        self.assertEqual(q.plus_probability(q.nonselective_update(plus, "Z"), "Y"), F(1, 2))

    def test_serial_z_then_y_no_longer_reads_initial_phase(self):
        for outcome in (-1, 1):
            plus = q.selective_update(q.Bloch((0, 1, 0)), "Z", outcome)
            minus = q.selective_update(q.Bloch((0, -1, 0)), "Z", outcome)
            self.assertEqual(plus, minus)
            self.assertEqual(q.plus_probability(plus, "Y"), F(1, 2))

    def test_nonselective_equals_probability_weighted_positive_branches(self):
        source = q.Bloch((F(1, 5), F(-2, 5), F(1, 2)))
        for setting in q.AXES:
            p = q.plus_probability(source, setting)
            plus = q.selective_update(source, setting, 1)
            minus = q.selective_update(source, setting, -1)
            expected = q.Bloch(tuple(p * a + (1 - p) * b for a, b in zip(plus.r, minus.r)))
            self.assertEqual(q.nonselective_update(source, setting), expected)

    def test_nonselective_oblique_preserves_only_axis_component(self):
        source = q.Bloch((F(1, 5), F(-2, 5), F(1, 2)))
        self.assertEqual(q.nonselective_update(source, "W"), q.Bloch((0, F(12, 125), F(16, 125))))

    def test_density_y_sign_and_hermiticity(self):
        rho = q.density(q.Bloch((0, 1, 0)))
        self.assertEqual(rho, ((q.G(F(1, 2)), q.G(0, F(-1, 2))), (q.G(0, F(1, 2)), q.G(F(1, 2)))))
        self.assertEqual(rho[1][0], rho[0][1].conjugate())

    def test_trace_one_density_is_not_total_entry_mass_one(self):
        state = q.Bloch((F(3, 5), 0, 0))
        rho = q.density(state)
        self.assertEqual(rho[0][0] + rho[1][1], q.G(1))
        self.assertEqual(sum((z for row in rho for z in row), q.G()), q.G(F(8, 5)))
        self.assertEqual(sum((z for row in q.J2(state) for z in row), q.G()), q.G(1))

    def test_complete_j2_bridge_and_phi_identity(self):
        states = [q.Bloch((0, 0, 0)), q.Bloch((F(1, 5), F(-2, 5), F(1, 2)))]
        states.extend(
            q.Bloch(tuple(sign * x for x in axis)) for axis in q.AXES.values() for sign in (-1, 1)
        )
        for state in states:
            raw, rho = q.J2(state), q.density(state)
            self.assertEqual(q.phi(raw), rho)
            self.assertEqual(sum((z for row in raw for z in row), q.G()), q.G(1))
            for i in range(4):
                for j in range(4):
                    if (i < 2) != (j < 2):
                        expected = q.G()
                    else:
                        a, b = i % 2, j % 2
                        sign = 1 if i < 2 else (-1) ** (a + b)
                        expected = F(sign, 2) * rho[b][a]
                    self.assertEqual(raw[i][j], expected)

    def test_j2_y_transpose_is_load_bearing(self):
        raw = q.J2(q.Bloch((0, 1, 0)))
        self.assertEqual(raw[0][1], q.G(0, F(1, 4)))
        self.assertEqual(raw[2][3], q.G(0, F(-1, 4)))
        self.assertEqual(q.phi(raw)[0][1], q.G(0, F(-1, 2)))

    def test_phi_refuses_out_of_image_payload_without_projection(self):
        raw = q.J2(q.Bloch((0, 0, 0)))
        for i, j in ((0, 2), (2, 3), (2, 2), (0, 0)):
            changed = [list(row) for row in raw]
            changed[i][j] += F(1, 10)
            with self.subTest(i=i, j=j), self.assertRaises(ValueError):
                q.phi(changed)
        with self.assertRaises(ValueError):
            q.phi(((0, 0), (0, 0)))

    def test_phi_refuses_nonpositive_trace_one_candidate(self):
        a, off, zero = q.G(F(1, 4)), q.G(F(1, 2)), q.G()
        raw = (
            (a, off, zero, zero),
            (off, a, zero, zero),
            (zero, zero, a, -off),
            (zero, zero, -off, a),
        )
        with self.assertRaises(ValueError):
            q.phi(raw)

    def test_phi_consumes_one_shot_rows_once(self):
        state = q.Bloch((F(1, 5), F(-2, 5), F(1, 2)))
        rows = (iter(row) for row in q.J2(state))
        self.assertEqual(q.phi(rows), q.density(state))

    def test_trace_distance_convention_and_exact_values(self):
        plus, minus, center = q.Bloch((0, 1, 0)), q.Bloch((0, -1, 0)), q.Bloch((0, 0, 0))
        self.assertEqual(q.trace_distance_squared(plus, plus), 0)
        self.assertEqual(q.trace_distance_squared(plus, minus), 1)
        self.assertEqual(q.trace_distance_squared(plus, center), F(1, 4))
        self.assertEqual(q.trace_distance_squared(q.Bloch((F(3, 5), 0, 0)), center), F(9, 100))

    def test_exact_gaussian_arithmetic_and_invalid_scalars(self):
        self.assertEqual(q.G(1, 2) * q.G(3, -4), q.G(11, 2))
        self.assertEqual(2 * q.G(1, -2) + F(1, 3), q.G(F(7, 3), -4))
        for value in (True, 0.5, 1j, "1"):
            with self.subTest(value=value), self.assertRaises(TypeError):
                q.G(value)

    def test_public_measurement_input_guards(self):
        state = q.Bloch((0, 0, 0))
        for setting in ("x", "UNKNOWN", "", None, True):
            with self.subTest(setting=setting), self.assertRaises((TypeError, ValueError)):
                q.plus_probability(state, setting)
        for outcome in (0, 2, True, F(1), 1.0, "+1"):
            with self.subTest(outcome=outcome), self.assertRaises((TypeError, ValueError)):
                q.selective_update(state, "Z", outcome)
        for function, args in (
            (q.plus_probability, (None, "Z")),
            (q.J2, (None,)),
            (q.density, (None,)),
            (q.trace_distance_squared, (state, None)),
        ):
            with self.subTest(function=function.__name__), self.assertRaises(TypeError):
                function(*args)


if __name__ == "__main__":
    unittest.main()
