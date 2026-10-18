"""Independent exact-arithmetic tests of the bounded comparator contract.

These are mathematical fixtures, not apparatus observations or sampled trials.
The test oracle checks every witness against the original measurement equations.
"""

import hashlib
import json
import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction

from contract import (
    Model,
    Record,
    Report,
    Request,
    assess,
    canonical_payload,
    compatible_parameters,
    verify_report,
)

F = Fraction


def make_request(model=None, records=None, selected_ids=None, **changes):
    """Declare a synthetic common context, without inferring its validity."""
    if model is None:
        model = Model("affine")
    if records is None:
        records = (
            Record("minus", "actual", -1, -1, F(1, 100)),
            Record("plus", "actual", 1, 1, F(1, 100)),
        )
    if selected_ids is None:
        selected_ids = ("minus", "plus")
    arguments = {
        "model": model,
        "records": records,
        "selected_ids": selected_ids,
        "tolerance": F(1, 20),
        "response_unit": "output_volt",
        "session_id": "synthetic-session",
        "calibration_id": "supplied-calibration",
        "model_basis": "Declared static polynomial on the three exact references",
        "error_basis": "Supplied deterministic bounds; no sampling law",
        "target": "mean_at_zero",
        "reference_unit": "normalized",
    }
    arguments.update(changes)
    return Request(**arguments)


def add_record(request, record, selected=False):
    selected_ids = request.selected_ids + ((record.record_id,) if selected else ())
    return replace(request, records=request.records + (record,), selected_ids=selected_ids)


class Assertions(unittest.TestCase):
    def assert_interval(self, request, lower, upper, identified, precision=None):
        report = assess(request)
        self.assertIsInstance(report, Report)
        self.assertEqual(report.status, "bounded")
        self.assertEqual((report.lower, report.upper), (F(lower), F(upper)))
        self.assertEqual(report.midpoint, (F(lower) + F(upper)) / 2)
        self.assertEqual(report.radius, (F(upper) - F(lower)) / 2)
        self.assertIs(report.structurally_identified, identified)
        expected = report.radius <= request.tolerance if precision is None else precision
        self.assertIs(report.precision_met, expected)
        for name in ("lower", "upper", "midpoint", "radius"):
            self.assertIs(type(getattr(report, name)), Fraction)
        self.assertTrue(report.reason)
        self.assertIs(verify_report(request, report), True)
        return report

    def assert_witness(self, request, target):
        parameters = compatible_parameters(request, F(target))
        self.assertIs(type(parameters), tuple)
        self.assertEqual(len(parameters), 3)
        self.assertTrue(all(type(item) is Fraction for item in parameters))
        gain, offset, curvature = parameters
        self.assertEqual(offset, target)
        if request.model.family == "affine":
            self.assertEqual(curvature, 0)
        elif request.model.family == "bounded_curvature":
            self.assertLessEqual(abs(curvature), request.model.curvature_bound)
        selected = set(request.selected_ids)
        for record in request.records:
            if record.record_id in selected:
                self.assertEqual(record.role, "actual")
                mean = gain * record.reference + offset + curvature * record.reference**2
                self.assertLessEqual(abs(record.value - mean), record.error)
        return parameters

    def assert_incompatible(self, request, identified):
        report = assess(request)
        self.assertEqual(report.status, "incompatible")
        self.assertIs(report.structurally_identified, identified)
        for name in ("lower", "upper", "midpoint", "radius", "precision_met"):
            self.assertIsNone(getattr(report, name))
        self.assertTrue(report.reason)
        self.assertIs(verify_report(request, report), True)
        with self.assertRaises(ValueError):
            compatible_parameters(request, 0)
        return report


class TargetContractTests(Assertions):
    def test_affine_endpoint_tolerance(self):
        request = make_request()
        self.assert_interval(request, F(-1, 100), F(1, 100), True, True)

    def test_model_enlargement_invalidates_the_affine_certificate(self):
        affine = make_request()
        changed = replace(affine, model=Model("bounded_curvature", F(1, 5)))
        old = assess(affine)
        current = self.assert_interval(changed, F(-21, 100), F(21, 100), False, False)
        self.assertNotEqual(current.input_digest, old.input_digest)
        self.assertIs(verify_report(changed, old), False)
        for target in (F(-21, 100), F(21, 100)):
            self.assert_witness(changed, target)

    def test_exact_laws_remain_ambiguous_with_positive_curvature_bound(self):
        request = make_request(
            Model("bounded_curvature", F(1, 100)),
            (
                Record("minus", "actual", -1, -1, 0),
                Record("plus", "actual", 1, 1, 0),
            ),
        )
        self.assert_interval(request, F(-1, 100), F(1, 100), False, True)
        # Explicit indistinguishable models, without using the witness producer.
        for offset, curvature in ((F(1, 100), F(-1, 100)), (F(-1, 100), F(1, 100))):
            for record in request.records:
                self.assertEqual(record.value, record.reference + offset + curvature)

    def test_zero_curvature_bound_recovers_affine_domain(self):
        affine = make_request()
        bounded = replace(affine, model=Model("bounded_curvature", 0))
        a, b = assess(affine), assess(bounded)
        self.assertEqual((a.lower, a.upper), (b.lower, b.upper))
        self.assertIs(b.structurally_identified, True)
        self.assertNotEqual(a.input_digest, b.input_digest)
        self.assert_witness(bounded, b.lower)

    def test_unbounded_curvature_without_zero(self):
        request = make_request(Model("unbounded_curvature"))
        report = assess(request)
        self.assertEqual(report.status, "unbounded")
        self.assertIs(report.precision_met, False)
        self.assertIs(report.structurally_identified, False)
        for name in ("lower", "upper", "midpoint", "radius"):
            self.assertIsNone(getattr(report, name))
        for target in (-(10**20), -3, 0, F(7, 3), 10**20):
            self.assert_witness(request, target)
        self.assertIs(verify_report(request, report), True)

    def test_empty_or_single_endpoint_information_leaves_target_unbounded(self):
        for model in (
            Model("affine"),
            Model("bounded_curvature", 0),
            Model("bounded_curvature", F(1, 5)),
            Model("unbounded_curvature"),
        ):
            for records, selection in (
                ((), ()),
                ((Record("minus", "actual", -1, -1, 0),), ("minus",)),
                ((Record("plus", "actual", 1, 1, F(1, 10)),), ("plus",)),
                (
                    (
                        Record("minus", "actual", -1, -1, 0),
                        Record("plus", "missing", 1, reason="lost"),
                    ),
                    ("minus",),
                ),
                (
                    (Record("minus", "actual", -1, -1, 0), Record("plus", "held_out", 1, 1, 0)),
                    ("minus",),
                ),
            ):
                with self.subTest(model=model, selection=selection):
                    request = make_request(model, records, selection)
                    report = assess(request)
                    self.assertEqual(report.status, "unbounded")
                    self.assertIs(report.structurally_identified, False)
                    self.assertIs(report.precision_met, False)
                    for name in ("lower", "upper", "midpoint", "radius"):
                        self.assertIsNone(getattr(report, name))
                    for target in (-1000, F(1, 3), 1000):
                        self.assert_witness(request, target)

    def test_no_selected_records_cannot_use_retained_actual_endpoints(self):
        request = make_request(selected_ids=())
        report = assess(request)
        self.assertEqual(report.status, "unbounded")
        self.assertIs(report.structurally_identified, False)
        self.assert_witness(request, 999)

    def test_zero_only_or_zero_with_one_endpoint_bounds_the_target(self):
        for model in (
            Model("affine"),
            Model("bounded_curvature", 0),
            Model("bounded_curvature", F(1, 5)),
            Model("unbounded_curvature"),
        ):
            for endpoint in (None, -1, 1):
                records = (Record("zero", "actual", 0, F(2, 3), F(1, 12)),)
                if endpoint is not None:
                    records += (Record("endpoint", "actual", endpoint, 17, 0),)
                request = make_request(model, records, tuple(r.record_id for r in records))
                self.assert_interval(request, F(7, 12), F(3, 4), True, False)
                self.assert_witness(request, F(7, 12))
                self.assert_witness(request, F(3, 4))

    def test_inconsistent_single_endpoint_is_incompatible_not_unbounded(self):
        records = (
            Record("minus", "actual", -1, -1, 0),
            Record("minus-2", "actual", -1, 1, 0),
        )
        request = make_request(records=records, selected_ids=("minus", "minus-2"))
        self.assert_incompatible(request, False)

    def test_actual_zero_restores_bounded_precision_not_affine_compatibility(self):
        zero = Record("zero", "actual", 0, F(1, 10), F(1, 100))
        bounded = add_record(make_request(Model("bounded_curvature", F(1, 5))), zero, True)
        self.assert_interval(bounded, F(9, 100), F(11, 100), True, True)
        self.assert_incompatible(replace(bounded, model=Model("affine")), True)

    def test_unbounded_curvature_with_selected_zero_is_bounded(self):
        request = add_record(
            make_request(Model("unbounded_curvature")),
            Record("zero", "actual", 0, 17, F(1, 7)),
            True,
        )
        self.assert_interval(request, F(118, 7), F(120, 7), True, False)
        self.assert_witness(request, F(118, 7))
        self.assert_witness(request, F(120, 7))

    def test_selected_zero_outside_model_interval_is_incompatible(self):
        request = add_record(
            make_request(Model("bounded_curvature", F(1, 5))),
            Record("zero", "actual", 0, F(3, 10), F(1, 100)),
            True,
        )
        self.assert_incompatible(request, True)

    def test_zero_reading_is_not_missing(self):
        request = add_record(make_request(), Record("zero", "actual", 0, 0, 0), True)
        self.assert_interval(request, 0, 0, True, True)
        missing = add_record(make_request(), Record("zero", "missing", 0, reason="lost"))
        self.assert_interval(missing, F(-1, 100), F(1, 100), True)

    def test_prospective_missing_held_out_and_unselected_actual_do_not_narrow(self):
        base = make_request(Model("bounded_curvature", F(1, 5)))
        for record in (
            Record("zero", "prospective", 0, error=0),
            Record("zero", "missing", 0, reason="not returned"),
            Record("zero", "held_out", 0, 10, 0),
            Record("zero", "actual", 0, 10, 0),
        ):
            with self.subTest(role=record.role):
                current = add_record(base, record)
                self.assert_interval(current, F(-21, 100), F(21, 100), False, False)
                self.assertNotEqual(assess(current).input_digest, assess(base).input_digest)

    def test_identical_repeated_errors_do_not_gain_independent_sample_precision(self):
        base = make_request(Model("bounded_curvature", F(1, 5)))
        repeated = add_record(base, Record("minus-2", "actual", -1, -1, F(1, 100)), True)
        repeated = add_record(repeated, Record("plus-2", "actual", 1, 1, F(1, 100)), True)
        self.assert_interval(repeated, F(-21, 100), F(21, 100), False, False)
        # Common signed errors attain both extremes even with repeated records.
        for target, curvature, common_error in (
            (F(21, 100), F(-1, 5), F(-1, 100)),
            (F(-21, 100), F(1, 5), F(1, 100)),
        ):
            for record in repeated.records:
                self.assertEqual(record.value, record.reference + target + curvature + common_error)

    def test_repeated_intervals_intersect_before_target_projection(self):
        records = (
            Record("minus", "actual", -1, -1, F(1, 5)),
            Record("minus-2", "actual", -1, F(-9, 10), F(1, 10)),
            Record("plus", "actual", 1, 1, F(1, 5)),
            Record("plus-2", "actual", 1, F(11, 10), F(1, 10)),
        )
        request = make_request(
            Model("bounded_curvature", F(1, 10)), records, tuple(r.record_id for r in records)
        )
        # Endpoint intervals are [-1,-4/5] and [1,6/5], so b spans [-1/10,3/10].
        self.assert_interval(request, F(-1, 10), F(3, 10), False, False)
        for target in (F(-1, 10), 0, F(3, 10)):
            self.assert_witness(request, target)

    def test_inconsistent_endpoint_repeats_cannot_be_repaired_by_curvature(self):
        for model in (
            Model("affine"),
            Model("bounded_curvature", 100),
            Model("unbounded_curvature"),
        ):
            request = add_record(make_request(model), Record("minus-2", "actual", -1, 2, 0), True)
            self.assert_incompatible(request, model.family == "affine")

    def test_precise_zero_does_not_hide_conflicting_endpoints_in_unbounded_model(self):
        request = add_record(
            make_request(Model("unbounded_curvature")),
            Record("zero", "actual", 0, 0, 0),
            True,
        )
        request = add_record(request, Record("minus-2", "actual", -1, 2, 0), True)
        self.assert_incompatible(request, True)

    def test_touching_endpoint_intervals_are_compatible(self):
        records = (
            Record("minus", "actual", -1, -2, 1),
            Record("minus-2", "actual", -1, 0, 1),
            Record("plus", "actual", 1, 1, 0),
        )
        request = make_request(
            records=records, selected_ids=("minus", "minus-2", "plus"), tolerance=0
        )
        self.assert_interval(request, 0, 0, True, True)
        self.assert_witness(request, 0)

    def test_zero_interval_only_partly_intersects_endpoint_projection(self):
        request = add_record(
            make_request(Model("bounded_curvature", F(1, 5))),
            Record("zero", "actual", 0, F(1, 5), F(1, 10)),
            True,
        )
        self.assert_interval(request, F(1, 10), F(21, 100), True, False)
        for target in (F(1, 10), F(31, 200), F(21, 100)):
            self.assert_witness(request, target)

    def test_touching_target_and_zero_intervals_give_singleton(self):
        request = add_record(
            make_request(Model("bounded_curvature", F(1, 5))),
            Record("zero", "actual", 0, F(31, 100), F(1, 10)),
            True,
        )
        self.assert_interval(request, F(21, 100), F(21, 100), True, True)
        self.assert_witness(request, F(21, 100))

    def test_repeated_zero_intervals_must_also_intersect(self):
        request = add_record(
            make_request(Model("unbounded_curvature")), Record("zero", "actual", 0, 0, 0), True
        )
        request = add_record(request, Record("zero-2", "actual", 0, 1, 0), True)
        self.assert_incompatible(request, True)

    def test_exact_precision_boundary_and_nearby_values(self):
        base = make_request(Model("bounded_curvature", F(1, 5)))
        for tolerance, expected in (
            (F(21, 100), True),
            (F(21, 100) - F(1, 10**12), False),
            (F(21, 100) + F(1, 10**12), True),
        ):
            request = replace(base, tolerance=tolerance)
            self.assert_interval(request, F(-21, 100), F(21, 100), False, expected)

    def test_precision_is_radius_not_absolute_target_size(self):
        request = make_request(
            records=(Record("minus", "actual", -1, 999, 0), Record("plus", "actual", 1, 1001, 0)),
            tolerance=0,
        )
        self.assert_interval(request, 1000, 1000, True, True)

    def test_unequal_endpoint_errors_and_shifted_response(self):
        request = make_request(
            Model("bounded_curvature", F(2, 7)),
            (
                Record("minus", "actual", -1, F(-7, 3), F(1, 8)),
                Record("plus", "actual", 1, F(5, 2), F(1, 12)),
            ),
        )
        center, radius = F(1, 12), F(5, 48) + F(2, 7)
        self.assert_interval(request, center - radius, center + radius, False)
        for fraction in (0, F(1, 7), F(1, 2), F(5, 6), 1):
            self.assert_witness(request, center - radius + 2 * radius * fraction)

    def test_witnesses_cover_a_rational_grid_of_endpoint_and_zero_cases(self):
        for em, ep, bound in (
            (0, 0, 0),
            (0, F(1, 3), F(1, 5)),
            (F(2, 9), 0, F(3, 7)),
            (F(1, 4), F(2, 5), F(1, 8)),
        ):
            base = make_request(
                Model("bounded_curvature", bound),
                (
                    Record("minus", "actual", -1, F(-4, 3), em),
                    Record("plus", "actual", 1, F(7, 5), ep),
                ),
            )
            center = (F(-4, 3) + F(7, 5)) / 2
            radius = (F(em) + F(ep)) / 2 + bound
            for use_zero in (False, True):
                request = base
                low, high = center - radius, center + radius
                if use_zero:
                    request = add_record(
                        base, Record("zero", "actual", 0, center, radius / 2), True
                    )
                    low, high = center - radius / 2, center + radius / 2
                with self.subTest(em=em, ep=ep, bound=bound, zero=use_zero):
                    self.assert_interval(request, low, high, use_zero or bound == 0)
                    for part in (0, F(1, 9), F(1, 2), F(8, 9), 1):
                        self.assert_witness(request, low + part * (high - low))
                    with self.assertRaises(ValueError):
                        compatible_parameters(request, low - F(1, 1000))
                    with self.assertRaises(ValueError):
                        compatible_parameters(request, high + F(1, 1000))

    def test_endpoint_witnesses_establish_the_minimax_radius(self):
        request = make_request(Model("bounded_curvature", F(1, 5)))
        report = assess(request)
        left = self.assert_witness(request, report.lower)[1]
        right = self.assert_witness(request, report.upper)[1]
        for answer in (
            left - 1,
            left,
            report.midpoint - F(1, 100),
            report.midpoint,
            right,
            right + 1,
        ):
            worst = max(abs(answer - left), abs(answer - right))
            self.assertGreaterEqual(worst, report.radius)
            self.assertEqual(worst == report.radius, answer == report.midpoint)


class IdentityTests(Assertions):
    def test_canonical_digest_matches_independent_json_hash(self):
        request = make_request()
        payload = canonical_payload(request)
        expected = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(assess(request).input_digest, expected)
        self.assertEqual(len(expected), 64)
        self.assertEqual(payload["tolerance"], "1/20")
        self.assertEqual(payload["records"][0]["error"], "1/100")
        self.assertTrue(payload["contract_version"])

    def test_payload_is_fully_detached(self):
        request = make_request(Model("bounded_curvature", F(1, 5)))
        before = canonical_payload(request)
        changed = canonical_payload(request)
        changed["records"][0]["value"] = "999"
        changed["selected_ids"].append("invented")
        changed["model"]["family"] = "affine"
        self.assertEqual(canonical_payload(request), before)
        self.assertIs(verify_report(request, assess(request)), True)

    def test_equivalent_reduced_rationals_have_the_same_identity(self):
        original = make_request()
        equivalent = replace(
            original,
            tolerance=F(5, 100),
            records=(
                Record("minus", "actual", F(-2, 2), F(-3, 3), F(2, 200)),
                Record("plus", "actual", F(2, 2), F(3, 3), F(3, 300)),
            ),
        )
        self.assertEqual(canonical_payload(original), canonical_payload(equivalent))
        self.assertIs(verify_report(equivalent, assess(original)), True)

    def test_all_metadata_and_budget_changes_bind_identity(self):
        base = make_request()
        report = assess(base)
        variants = (
            replace(base, tolerance=F(1, 19)),
            replace(base, response_unit="different_output_unit"),
            replace(base, session_id="other-session"),
            replace(base, calibration_id="other-calibration"),
            replace(base, model_basis="Different supplied model evidence"),
            replace(base, error_basis="Different supplied error evidence"),
            replace(base, model=Model("bounded_curvature", 0)),
            replace(base, model=Model("bounded_curvature", F(1, 1000))),
            replace(base, records=(replace(base.records[0], error=F(1, 99)), base.records[1])),
            replace(base, records=(replace(base.records[0], value=F(-999, 1000)), base.records[1])),
        )
        for request in variants:
            with self.subTest(payload=canonical_payload(request)):
                self.assertNotEqual(assess(request).input_digest, report.input_digest)
                self.assertIs(verify_report(request, report), False)

    def test_retained_excluded_records_also_bind_identity(self):
        base = make_request()
        for old, new in (
            (Record("extra", "prospective", 0), Record("extra", "prospective", 0, error=F(1, 10))),
            (
                Record("extra", "missing", 0, reason="lost"),
                Record("extra", "missing", 0, reason="failed capture"),
            ),
            (Record("extra", "held_out", 0, 0, 0), Record("extra", "held_out", 0, 1, 0)),
            (Record("extra", "actual", 0, 0, 0), Record("extra", "actual", 0, 1, 0)),
        ):
            first, second = add_record(base, old), add_record(base, new)
            a, b = assess(first), assess(second)
            self.assertEqual((a.lower, a.upper), (b.lower, b.upper))
            self.assertNotEqual(a.input_digest, b.input_digest)
            self.assertIs(verify_report(second, a), False)

    def test_reference_record_identity_and_role_changes_bind_identity(self):
        base = make_request()
        original = assess(base)
        changed_reference = replace(
            base, records=(replace(base.records[0], reference=0), base.records[1])
        )
        renamed = replace(
            base,
            records=(replace(base.records[0], record_id="renamed-minus"), base.records[1]),
            selected_ids=("renamed-minus", "plus"),
        )
        for changed in (changed_reference, renamed):
            self.assertNotEqual(assess(changed).input_digest, original.input_digest)
            self.assertIs(verify_report(changed, original), False)
        self.assertEqual(
            (assess(renamed).lower, assess(renamed).upper),
            (original.lower, original.upper),
        )
        held_out = add_record(base, Record("extra", "held_out", 0, 1, F(1, 10)))
        unselected_actual = replace(
            held_out,
            records=held_out.records[:-1] + (replace(held_out.records[-1], role="actual"),),
        )
        first, second = assess(held_out), assess(unselected_actual)
        self.assertEqual((first.lower, first.upper), (second.lower, second.upper))
        self.assertNotEqual(first.input_digest, second.input_digest)
        self.assertIs(verify_report(unselected_actual, first), False)

    def test_selection_and_both_orders_bind_identity_without_changing_inference(self):
        base = add_record(make_request(), Record("plus-copy", "actual", 1, 1, F(1, 100)))
        variants = (
            replace(base, records=tuple(reversed(base.records))),
            replace(base, selected_ids=tuple(reversed(base.selected_ids))),
            replace(base, selected_ids=("minus", "plus-copy")),
        )
        original = assess(base)
        for request in variants:
            report = assess(request)
            self.assertEqual(
                (report.lower, report.upper, report.radius),
                (original.lower, original.upper, original.radius),
            )
            self.assertNotEqual(report.input_digest, original.input_digest)
            self.assertIs(verify_report(request, original), False)

    def test_reports_and_input_objects_are_frozen(self):
        request = make_request()
        for obj, name, value in (
            (request, "tolerance", 100),
            (request.model, "family", "unbounded_curvature"),
            (request.records[0], "value", 42),
            (assess(request), "precision_met", False),
        ):
            with self.assertRaises((FrozenInstanceError, AttributeError)):
                setattr(obj, name, value)

    def test_verification_recomputes_every_report_field(self):
        request = make_request()
        report = assess(request)
        for field, value in (
            ("input_digest", "0" * 64),
            ("status", "unbounded"),
            ("lower", F(-1)),
            ("upper", F(1)),
            ("midpoint", F(1)),
            ("radius", F(0)),
            ("precision_met", False),
            ("structurally_identified", False),
            ("reason", "Unsupported replacement reason"),
        ):
            changed = replace(report, **{field: value})
            with self.subTest(field=field):
                self.assertIs(verify_report(request, changed), False)
        for not_report in (None, {}, (), canonical_payload(request), "report"):
            self.assertIs(verify_report(request, not_report), False)

    def test_verification_rejects_equal_numeric_values_of_wrong_types(self):
        request = add_record(make_request(), Record("zero", "actual", 0, 0, 0), True)
        report = assess(request)
        for field in ("lower", "upper", "midpoint", "radius"):
            for value in (0, 0.0, False):
                with self.subTest(field=field, value=repr(value)):
                    changed = replace(report, **{field: value})
                    self.assertEqual(getattr(changed, field), getattr(report, field))
                    self.assertIs(verify_report(request, changed), False)
        for field in ("precision_met", "structurally_identified"):
            for value in (1, 1.0, F(1)):
                self.assertIs(verify_report(request, replace(report, **{field: value})), False)


class RefusalTests(unittest.TestCase):
    def test_model_family_and_bound_contract(self):
        bad = (
            lambda: Model("other"),
            lambda: Model("bounded_curvature", -1),
            lambda: Model("affine", 0),
            lambda: Model("unbounded_curvature", 0),
        )
        for construct in bad:
            with self.assertRaises(ValueError):
                construct()
        with self.assertRaises(TypeError):
            Model("bounded_curvature")

    def test_numeric_types_are_exact_and_not_subclasses(self):
        class IntSubclass(int):
            pass

        class FractionSubclass(Fraction):
            pass

        for value in (True, False, 0.0, "0", IntSubclass(0), FractionSubclass(0), complex(0)):
            for construct in (
                lambda value=value: Model("bounded_curvature", value),
                lambda value=value: Record("r", "actual", value, 0, 0),
                lambda value=value: Record("r", "actual", 0, value, 0),
                lambda value=value: Record("r", "actual", 0, 0, value),
                lambda value=value: make_request(tolerance=value),
                lambda value=value: compatible_parameters(make_request(), value),
            ):
                with (
                    self.subTest(value=repr(value), constructor=construct),
                    self.assertRaises(TypeError),
                ):
                    construct()

    def test_reduced_input_bit_limits_and_unbounded_derived_outputs(self):
        legal = 1 << 255
        illegal = 1 << 256
        Model("bounded_curvature", legal)
        Model("bounded_curvature", F(1, legal))
        for value in (illegal, -illegal, F(1, illegal)):
            with self.assertRaises(ValueError):
                Record("r", "actual", 0, value, 0)
        request = make_request(
            Model("bounded_curvature", legal),
            (Record("minus", "actual", -1, legal, 0), Record("plus", "actual", 1, legal, 0)),
        )
        self.assertEqual(assess(request).upper, 1 << 256)
        self.assertEqual(assess(request).lower, 0)

    def test_reference_catalogue_only(self):
        for reference in (-2, 2, F(1, 2)):
            for role, kwargs in (
                ("actual", {"value": 0, "error": 0}),
                ("prospective", {}),
                ("missing", {"reason": "lost"}),
                ("held_out", {"value": 0, "error": 0}),
            ):
                with self.assertRaises(ValueError):
                    Record("r", role, reference, **kwargs)

    def test_record_roles_and_payload_refusals(self):
        bad = (
            lambda: Record("r", "unknown", 0),
            lambda: Record("r", "actual", 0),
            lambda: Record("r", "actual", 0, 0),
            lambda: Record("r", "actual", 0, 0, -1),
            lambda: Record("r", "actual", 0, 0, 0, "unexpected"),
            lambda: Record("r", "held_out", 0),
            lambda: Record("r", "held_out", 0, 0, 0, "unexpected"),
            lambda: Record("r", "prospective", 0, 0),
            lambda: Record("r", "prospective", 0, error=-1),
            lambda: Record("r", "prospective", 0, reason="unexpected"),
            lambda: Record("r", "missing", 0),
            lambda: Record("r", "missing", 0, reason=""),
            lambda: Record("r", "missing", 0, 0, reason="lost"),
            lambda: Record("r", "missing", 0, error=0, reason="lost"),
        )
        for construct in bad:
            with self.assertRaises((TypeError, ValueError)):
                construct()

    def test_tuple_only_containers_and_record_types(self):
        base = make_request()
        for records in (
            list(base.records),
            iter(base.records),
            {"minus": base.records[0]},
            "records",
        ):
            with self.assertRaises(TypeError):
                replace(base, records=records)
        for selection in (list(base.selected_ids), iter(base.selected_ids), "minus"):
            with self.assertRaises(TypeError):
                replace(base, selected_ids=selection)
        with self.assertRaises(TypeError):
            replace(base, records=base.records + ({},))
        with self.assertRaises(TypeError):
            replace(base, model="affine")

    def test_container_count_bound(self):
        base = make_request()
        records = base.records + tuple(
            Record("p" + str(index), "prospective", 0) for index in range(62)
        )
        make_request(records=records)
        with self.assertRaises(ValueError):
            make_request(records=records + (Record("extra", "prospective", 0),))

    def test_duplicate_unknown_and_ineligible_selection_refused(self):
        base = make_request()
        with self.assertRaises(ValueError):
            replace(base, records=base.records + (base.records[0],))
        for selected in (("minus", "plus", "plus"), ("minus", "plus", "unknown")):
            with self.assertRaises(ValueError):
                replace(base, selected_ids=selected)
        for record in (
            Record("extra", "prospective", 0),
            Record("extra", "missing", 0, reason="lost"),
            Record("extra", "held_out", 0, 0, 0),
        ):
            with self.assertRaises(ValueError):
                add_record(base, record, True)

    def test_constructor_replacement_cannot_make_an_invalid_unselected_record(self):
        base = make_request()
        unselected = Record("unselected", "actual", 0, 0, 0)
        with self.assertRaises(ValueError):
            replace(base, records=base.records + (replace(unselected, error=-1),))

    def test_context_text_boundaries_and_unsupported_targets(self):
        for text in ("", " ", " edge", "edge ", "new\nline", "tab\ttext", "control\x00"):
            for construct in (
                lambda text=text: Record(text, "prospective", 0),
                lambda text=text: make_request(session_id=text),
                lambda text=text: make_request(model_basis=text),
            ):
                with self.assertRaises(ValueError):
                    construct()
        Record("r" * 96, "prospective", 0)
        make_request(session_id="s" * 128, model_basis="b" * 512)
        for construct in (
            lambda: Record("r" * 97, "prospective", 0),
            lambda: make_request(session_id="s" * 129),
            lambda: make_request(error_basis="b" * 513),
            lambda: make_request(target="gain"),
            lambda: make_request(reference_unit="volt"),
            lambda: make_request(tolerance=-1),
        ):
            with self.assertRaises(ValueError):
                construct()

    def test_invalid_request_type_raises_instead_of_report_mismatch(self):
        for invalid in (None, {}, (), "request"):
            for operation in (
                lambda invalid=invalid: assess(invalid),
                lambda invalid=invalid: canonical_payload(invalid),
                lambda invalid=invalid: compatible_parameters(invalid, 0),
                lambda invalid=invalid: verify_report(invalid, assess(make_request())),
            ):
                with self.assertRaises(TypeError):
                    operation()
        with self.assertRaises(ValueError):
            replace(make_request(), tolerance=-1)


if __name__ == "__main__":
    unittest.main()
