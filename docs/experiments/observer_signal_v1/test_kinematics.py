"""Independent exact arithmetic checks for the supplied kinematics model."""

import unittest
from dataclasses import FrozenInstanceError
from fractions import Fraction

import kinematics as k

F = Fraction


class KinematicsTests(unittest.TestCase):
    def test_static_half_distance(self):
        a = k.arrive(k.Geometry(H=0), k.StaticTime(0), F(1, 2))
        self.assertEqual(a.status, "finite")
        self.assertEqual(a.reception, k.StaticTime(F(1, 2)))
        self.assertEqual(a.delay, k.LogExpression(F(1, 2)))
        self.assertEqual((a.frequency_ratio, a.redshift), (1, 0))

    def test_expansion_half_distance(self):
        a = k.arrive(k.Geometry(H=1), k.QTime(1), F(1, 2))
        self.assertEqual(a.reception, k.QTime(F(1, 2)))
        self.assertEqual(a.delay, k.LogExpression(0, 1, 2))
        self.assertEqual((a.frequency_ratio, a.redshift), (F(1, 2), 1))
        self.assertEqual(a.delay_bounds, (F(1, 2), F(1)))

    def test_contraction_half_distance(self):
        a = k.arrive(k.Geometry(H=-1), k.QTime(1), F(1, 2))
        self.assertEqual(a.reception, k.QTime(F(3, 2)))
        self.assertEqual(a.delay, k.LogExpression(0, 1, F(3, 2)))
        self.assertEqual((a.frequency_ratio, a.redshift), (F(3, 2), F(-1, 3)))
        self.assertEqual(a.delay_bounds, (F(1, 3), F(1, 2)))

    def test_horizon_equality_is_not_finite(self):
        a = k.arrive(k.Geometry(H=1), k.QTime(1), 1)
        self.assertEqual((a.status, a.raw_reception_q), ("asymptotic_future_only", 0))
        for name in (
            "reception",
            "delay",
            "frequency_ratio",
            "redshift",
            "transfer_derivative",
            "delay_bounds",
        ):
            self.assertIsNone(getattr(a, name))
        self.assertFalse(k.received_by(a, k.QTime(F(1, 10**30))))

    def test_strict_horizon_sides_arbitrarily_close(self):
        step = F(1, 10**40)
        left = k.arrive(k.Geometry(H=1), k.QTime(1), 1 - step)
        right = k.arrive(k.Geometry(H=1), k.QTime(1), 1 + step)
        self.assertEqual((left.status, left.raw_reception_q), ("finite", step))
        self.assertEqual(right.status, "beyond_future_horizon")
        self.assertEqual(right.raw_reception_q, -step)
        self.assertIsNone(right.frequency_ratio)

    def test_contraction_has_no_finite_distance_future_horizon(self):
        for ell in (0, 1, 10**30):
            a = k.arrive(k.Geometry(H=-F(7, 3)), k.QTime(F(2, 5)), ell)
            self.assertEqual(a.status, "finite")
            self.assertEqual(a.reception.q, F(2, 5) + F(7, 3) * ell)

    def test_zero_distance_all_signs(self):
        for h, emission in ((0, k.StaticTime(-7)), (2, k.QTime(3)), (-2, k.QTime(3))):
            a = k.arrive(k.Geometry(H=h), emission, 0)
            self.assertIs(a.reception, emission)
            self.assertEqual(a.delay, k.LogExpression())
            self.assertEqual((a.frequency_ratio, a.redshift, a.delay_bounds), (1, 0, (0, 0)))
            self.assertTrue(k.received_by(a, emission))

    def test_expansion_cutoff_exact_and_inclusive(self):
        a = k.arrive(k.Geometry(H=1), k.QTime(1), F(1, 2))
        self.assertFalse(k.received_by(a, k.QTime(F(3, 4))))
        self.assertTrue(k.received_by(a, k.QTime(F(1, 2))))
        self.assertTrue(k.received_by(a, k.QTime(F(1, 4))))

    def test_contraction_cutoff_exact_and_inclusive(self):
        a = k.arrive(k.Geometry(H=-1), k.QTime(1), F(1, 2))
        self.assertFalse(k.received_by(a, k.QTime(F(5, 4))))
        self.assertTrue(k.received_by(a, k.QTime(F(3, 2))))
        self.assertTrue(k.received_by(a, k.QTime(2)))

    def test_static_cutoff_and_invalid_schedule(self):
        a = k.arrive(k.Geometry(), k.StaticTime(2), 1)
        self.assertFalse(k.received_by(a, k.StaticTime(F(5, 2))))
        self.assertTrue(k.received_by(a, k.StaticTime(3)))
        for h, emission, cutoff in (
            (0, k.StaticTime(2), k.StaticTime(1)),
            (1, k.QTime(1), k.QTime(2)),
            (-1, k.QTime(1), k.QTime(F(1, 2))),
        ):
            with self.assertRaises(ValueError):
                k.received_by(k.arrive(k.Geometry(H=h), emission, 1), cutoff)

    def test_time_order_is_h_sign_aware(self):
        for h, expected in ((1, 1), (-1, -1)):
            g = k.Geometry(H=h)
            self.assertEqual(g.compare_times(k.QTime(1), k.QTime(2)), expected)
            self.assertEqual(g.compare_times(k.QTime(2), k.QTime(1)), -expected)
            self.assertEqual(g.compare_times(k.QTime(1), k.QTime(1)), 0)
        self.assertEqual(k.Geometry().compare_times(k.StaticTime(-2), k.StaticTime(1)), -1)

    def test_time_and_scale_reference_normalization(self):
        for h in (F(2, 3), F(-2, 3)):
            g = k.Geometry(H=h, a_star=5, t_star=7)
            self.assertEqual(g.time(k.QTime(1)), k.LogExpression(7))
            self.assertEqual(g.scale_factor(k.QTime(1)), 5)
            self.assertEqual(g.time(k.QTime(2)), k.LogExpression(7, -1 / h, 2))
            self.assertEqual(g.scale_factor(k.QTime(2)), F(5, 2))
        g = k.Geometry(H=0, a_star=5, t_star=7)
        self.assertEqual(g.time(k.StaticTime(2)), k.LogExpression(2))
        self.assertEqual(g.scale_factor(k.StaticTime(2)), 5)

    def test_received_order_for_equal_distance(self):
        for h, earlier, later in (
            (1, k.QTime(2), k.QTime(F(3, 2))),
            (-1, k.QTime(1), k.QTime(2)),
            (0, k.StaticTime(-1), k.StaticTime(2)),
        ):
            g = k.Geometry(H=h)
            first, second = (k.arrive(g, e, F(1, 2)) for e in (earlier, later))
            self.assertEqual(g.compare_times(first.reception, second.reception), -1)

    def test_frequency_scale_conservation(self):
        for h, e in ((0, k.StaticTime(3)), (1, k.QTime(2)), (-1, k.QTime(2))):
            g = k.Geometry(H=h, a_star=F(5, 3), c=7)
            a = k.arrive(g, e, F(4, 5))
            nu_e = F(17, 3)
            self.assertEqual(
                g.scale_factor(e) * nu_e,
                g.scale_factor(a.reception) * a.frequency_ratio * nu_e,
            )

    def test_comoving_coordinate_rescaling(self):
        for h, e in ((0, k.StaticTime(3)), (1, k.QTime(2)), (-1, k.QTime(2))):
            g = k.Geometry(H=h, a_star=2, c=3, t_star=7)
            scale = F(7, 5)
            changed = k.Geometry(H=h, a_star=2 * scale, c=3, t_star=7)
            a = k.arrive(g, e, F(3, 4))
            b = k.arrive(changed, e, F(3, 4) / scale)
            for name in ("reception", "delay", "frequency_ratio", "redshift", "delay_bounds"):
                self.assertEqual(getattr(a, name), getattr(b, name))

    def test_static_limit_exact_rational_squeeze(self):
        tau = F(3, 7)
        for h in (F(1, 10), F(1, 100), F(-1, 10), F(-1, 100)):
            a = k.arrive(k.Geometry(H=h), k.QTime(1), tau)
            lo, hi = a.delay_bounds
            self.assertLessEqual(lo, tau)
            self.assertGreaterEqual(hi, tau)
            self.assertEqual(hi - lo, abs(h) * tau * tau / (1 - h * tau))
            self.assertEqual(a.frequency_ratio, 1 - h * tau)
        static = k.arrive(k.Geometry(), k.StaticTime(0), tau)
        self.assertEqual(static.delay_bounds, (tau, tau))

    def test_same_redshift_does_not_fix_flight_delay(self):
        a = k.arrive(k.Geometry(H=1), k.QTime(1), F(1, 2))
        b = k.arrive(k.Geometry(H=2), k.QTime(1), F(1, 4))
        self.assertEqual(a.redshift, b.redshift)
        self.assertEqual(a.delay, k.LogExpression(0, 1, 2))
        self.assertEqual(b.delay, k.LogExpression(0, F(1, 2), 2))
        self.assertNotEqual(a.delay, b.delay)

    def test_infinitesimal_derivative_is_inverse_frequency_ratio(self):
        for h in (1, -1):
            g = k.Geometry(H=h, a_star=2, c=3)
            a = k.arrive(g, k.QTime(2), F(1, 2))
            self.assertEqual(
                a.transfer_derivative, g.scale_factor(a.reception) / g.scale_factor(a.emission)
            )
            self.assertEqual(a.transfer_derivative * a.frequency_ratio, 1)

    def test_finite_pulse_secant_not_endpoint_derivative(self):
        g = k.Geometry(H=1)
        first = k.arrive(g, k.QTime(2), 1)
        second = k.arrive(g, k.QTime(F(3, 2)), 1)
        self.assertEqual(g.elapsed(first.emission, second.emission), k.LogExpression(0, 1, F(4, 3)))
        self.assertEqual(g.elapsed(first.reception, second.reception), k.LogExpression(0, 1, 2))
        self.assertEqual((first.transfer_derivative, second.transfer_derivative), (2, 3))
        # Monotonic ln gives 2 < ln(2)/ln(4/3) < 3, with no float evaluation.
        self.assertLess(F(4, 3) ** 2, 2)
        self.assertLess(2, F(4, 3) ** 3)

    def test_log_expression_canonicalization_and_signed_elapsed(self):
        self.assertEqual(k.LogExpression(3, -2, F(1, 5)), k.LogExpression(3, 2, 5))
        self.assertEqual(k.LogExpression(3, 0, 7), k.LogExpression(3))
        self.assertEqual(k.LogExpression(3, 7, 1), k.LogExpression(3))
        g = k.Geometry(H=1)
        self.assertEqual(g.elapsed(k.QTime(1), k.QTime(2)), k.LogExpression(0, -1, 2))

    def test_nonfinite_audit_and_exact_serialization(self):
        a = k.arrive(k.Geometry(H=1, t_star=F(1, 3)), k.QTime(1), F(3, 2))
        data = a.to_dict()
        self.assertEqual(data["raw_reception_q"], "-1/2")
        self.assertIsNone(data["reception"])
        self.assertIsNone(data["delay"])
        self.assertEqual(data["geometry"]["t_star"], "1/3")
        finite = k.arrive(k.Geometry(H=1), k.QTime(1), F(1, 2)).to_dict()
        self.assertEqual(finite["delay"], {"constant": "0", "coefficient": "1", "argument": "2"})
        self.assertEqual(finite["delay_bounds"], ["1/2", "1"])
        self.assertEqual(k.StaticTime(F(1, 3)).to_dict(), {"kind": "static_t", "t": "1/3"})

    def test_strict_exact_scalar_inputs(self):
        for invalid in (True, False, 1.0, "1", complex(1)):
            for constructor in (k.QTime, k.StaticTime, k.LogExpression):
                with self.assertRaises(TypeError):
                    constructor(invalid)
            with self.assertRaises(TypeError):
                k.Geometry(H=invalid)
            with self.assertRaises(TypeError):
                k.arrive(k.Geometry(), k.StaticTime(0), invalid)

    def test_positive_domain_and_nonnegative_distance(self):
        for value in (0, -1):
            with self.assertRaises(ValueError):
                k.QTime(value)
            with self.assertRaises(ValueError):
                k.LogExpression(argument=value)
            with self.assertRaises(ValueError):
                k.Geometry(a_star=value)
            with self.assertRaises(ValueError):
                k.Geometry(c=value)
        with self.assertRaises(ValueError):
            k.arrive(k.Geometry(), k.StaticTime(0), -1)

    def test_wrong_time_and_arrival_types_refused(self):
        for g, wrong in ((k.Geometry(), k.QTime(1)), (k.Geometry(H=1), k.StaticTime(1))):
            for operation in (g.time, g.scale_factor):
                with self.assertRaises(TypeError):
                    operation(wrong)
            with self.assertRaises(TypeError):
                k.arrive(g, wrong, 0)
        with self.assertRaises(TypeError):
            k.arrive({}, k.StaticTime(0), 0)
        with self.assertRaises(TypeError):
            k.received_by({}, k.StaticTime(0))
        with self.assertRaises(TypeError):
            k.received_by(k.arrive(k.Geometry(), k.StaticTime(0), 0), k.QTime(1))

    def test_frozen_inputs_and_derived_outputs(self):
        g = k.Geometry(H=1)
        moment = k.QTime(1)
        a = k.arrive(g, moment, F(1, 2))
        for obj, name in ((g, "H"), (moment, "q"), (a, "status"), (a.delay, "argument")):
            with self.assertRaises(FrozenInstanceError):
                setattr(obj, name, 999)
        with self.assertRaises(TypeError):
            k.Arrival(g, moment, F(1, 2), status="beyond_future_horizon")


if __name__ == "__main__":
    unittest.main()
