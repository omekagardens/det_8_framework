"""Independent interchange checks against the two accepted, separately loaded APIs.

The launcher injects exact local_source/joint_source identities. These checks
compare scalar components, native tensor entries and literal cuts directly;
they do not infer preparation independence, prior history weights or new laws.
"""

import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F

import adapter as bridge
import joint_source as joint
import local_source as local


def components(matrix):
    return tuple(tuple((entry.real, entry.imag) for entry in row) for row in matrix)


def product_components(left, right):
    def multiply(a, b):
        return a.real * b.real - a.imag * b.imag, a.real * b.imag + a.imag * b.real

    return tuple(
        tuple(multiply(a, b) for a in left_row for b in right_row)
        for left_row in left
        for right_row in right
    )


def indices(outcome):
    a, b = outcome
    return tuple(8 * a + 4 * i + 2 * b + j for i in (0, 1) for j in (0, 1))


def cut_and_weight(raw, outcome):
    selected = indices(outcome)
    cut = tuple(
        tuple(
            entry if i in selected and j in selected else joint.G() for j, entry in enumerate(row)
        )
        for i, row in enumerate(raw)
    )
    return cut, sum((entry.real for row in cut for entry in row), F(0))


def source(c=0):
    a = local.matrix(
        ((F(3, 10), local.G(F(1, 20), F(1, 10))), (local.G(F(1, 20), F(-1, 10)), F(1, 5)))
    )
    return local.State(local.candidate_from(a, c, normalized=True))


def center_source(c=0):
    return local.State(local.candidate_from(local.scale(F(1, 4), local.identity(2)), c))


def recorded_source():
    state = local.run_word(center_source(), ("H", "P_inv"))
    _, state = local.commit_pauli(state, "Z", 0)
    state = local.run_control(state, "H")
    _, state = local.commit_pauli(state, "Y", 1)
    return local.run_word(state, ("H", "P_inv"))


PROVENANCE = (("preparation", "independent-reference"), ("selection_probability", "1/3"))


def prepared(state=None, t=F(1, 2), provenance=PROVENANCE):
    state = source() if state is None else state
    records = (joint.InputRecord(0, "prepare", "reference-ready", ("Z",), (("sample", "R"),)),)
    reference = joint.ReferenceState(t, "reference-run", records)
    independence = joint.Independence(("local-run", "reference-run"))
    return bridge.prepare(
        state,
        reference,
        independence,
        local_origin="local-run",
        joint_origin="joint-run",
        reference_provenance=provenance,
    )


def coupled(state=None, t=F(1, 2)):
    return bridge.promote(bridge.couple(bridge.promote(prepared(state, t))))


class LocalJointInterchangeChecks(unittest.TestCase):
    def test_conversion_preserves_every_exact_complex_component_and_origin(self):
        state = source(local.G(F(1, 40), F(-1, 30)))
        converted = bridge.convert_local_state(state, origin="local-run")
        self.assertIs(type(converted), joint.LocalState)
        self.assertEqual(converted.origin, "local-run")
        self.assertEqual(components(converted.residual), components(state.residual))
        self.assertTrue(all(type(x) is joint.G for row in converted.residual for x in row))
        self.assertTrue(
            all(type(x.real) is F and type(x.imag) is F for row in converted.residual for x in row)
        )
        self.assertIsNot(type(converted.residual[0][0]), type(state.residual[0][0]))
        self.assertTrue(any(x.imag for row in converted.residual for x in row))

    def test_record_conversion_retains_all_fields_and_complete_precursors(self):
        state = recorded_source()
        converted = bridge.convert_local_state(state, origin="local-run")
        self.assertEqual(len(converted.records), 2)
        for old, new in zip(state.records, converted.records, strict=True):
            self.assertIs(type(new), joint.InputRecord)
            self.assertEqual(
                (new.event_id, new.action, new.outcome, new.settings, new.precursor),
                (old.event_id, old.action, str(old.outcome), old.settings, old.precursor),
            )
            self.assertEqual(
                new.payload,
                (
                    ("ri08c.axis", old.axis),
                    ("ri08c.controller", old.controller),
                    ("ri08c.source_kind", old.source_kind),
                    ("ri08c.frame", old.frame),
                ),
            )

    def test_empty_prefix_pending_word_is_retained_without_reapplication_or_fake_record(self):
        state = local.run_word(source(), ("H", "P_inv"))
        prospective = prepared(state)
        self.assertEqual(state.records, ())
        self.assertEqual(prospective.context.local_input.records, ())
        self.assertIs(prospective.context.local_source, state)
        self.assertEqual(prospective.context.local_source.settings, ("H", "P_inv"))
        self.assertEqual(
            components(prospective.context.local_input.residual), components(state.residual)
        )
        twice = local.run_word(state, state.settings)
        self.assertNotEqual(components(twice.residual), components(state.residual))
        self.assertEqual(
            components(prospective.target.residual),
            product_components(state.residual, prospective.context.reference.residual),
        )

    def test_prepare_retains_original_source_reference_and_explicit_provenance(self):
        state = recorded_source()
        prospective = prepared(state, F(-2, 3))
        context = prospective.context
        self.assertIs(context.local_source, state)
        self.assertEqual((context.local_origin, context.joint_origin), ("local-run", "joint-run"))
        self.assertEqual(context.reference_provenance, PROVENANCE)
        self.assertIs(prospective.target.local, context.local_input)
        self.assertIs(prospective.target.reference, context.reference)
        self.assertIs(prospective.target.independence, context.independence)
        self.assertEqual(
            prospective.target.local.records,
            bridge.convert_local_state(state, origin="local-run").records,
        )
        self.assertEqual(
            components(prospective.target.residual),
            product_components(state.residual, context.reference.residual),
        )

    def test_real_accepted_stages_keep_context_and_apply_only_the_one_shared_coupler(self):
        prospective = prepared(recorded_source())
        product = bridge.promote(prospective)
        after = bridge.couple(product)
        lawful = bridge.promote(after)
        self.assertIs(type(product.target), joint.CompositeState)
        self.assertIs(type(after.target), joint.ProspectiveState)
        self.assertEqual(after.target.residual, joint.shared_couple(product.target.residual))
        self.assertNotEqual(after.target.residual, product.target.residual)
        for stage in (product, after, lawful):
            self.assertIs(stage.context, prospective.context)
            self.assertEqual(stage.target.local.records, prospective.target.local.records)
        self.assertEqual(product.target.coupler, joint.IDENTITY_COUPLER)
        self.assertEqual(lawful.target.coupler, joint.SHARED_COUPLER)
        with self.assertRaises((TypeError, ValueError)):
            bridge.couple(lawful)

    def test_nonzero_imaginary_c_product_is_lawful_before_polarized_coupling(self):
        state = center_source(local.G(0, F(1, 8)))
        for t in (F(-1), F(-1, 2), F(1, 2), F(1)):
            product = bridge.promote(prepared(state, t))
            self.assertTrue(joint.joint_recordable(product.target.residual, normalized=True))
            after = bridge.couple(product)
            forms = joint.joint_crossforms(after.target.residual)
            self.assertTrue(any(x.imag != 0 for x in forms))
            self.assertTrue(all(x.real == 0 for x in forms))
            self.assertIn(joint.G(0, t / 8), forms)
            self.assertEqual(joint.joint_mass(after.target.residual), 1)
            with self.assertRaises((TypeError, ValueError)):
                bridge.promote(after)
            self.assertIs(after.context.local_source, state)

    def test_zero_polarization_retains_nonzero_c_through_successful_promotion(self):
        state = center_source(local.G(F(1, 10), F(1, 10)))
        lawful = coupled(state, 0)
        erased = coupled(center_source(), 0)
        self.assertNotEqual(lawful.target.residual, erased.target.residual)
        self.assertEqual(joint.joint_weights(lawful.target.residual), (F(1, 4),) * 4)
        self.assertEqual(
            components(lawful.context.local_input.residual), components(state.residual)
        )
        self.assertIs(lawful.context.local_source, state)

    def test_c_zero_source_survives_both_endpoints_and_interior(self):
        for t in (F(-1), F(-1, 2), F(0), F(1, 3), F(1)):
            lawful = coupled(source(), t)
            self.assertTrue(joint.joint_recordable(lawful.target.residual, normalized=True))
            self.assertEqual(joint.joint_mass(lawful.target.residual), 1)
            self.assertEqual(
                tuple(x.real for x in joint.joint_crossforms(lawful.target.residual)), (F(0),) * 6
            )

    def test_joint_probabilities_and_every_terminal_entry_match_independent_native_cuts(self):
        lawful = coupled(source(), F(1, 2))
        probabilities = []
        for a in (0, 1):
            for b in (0, 1):
                cut, expected = cut_and_weight(lawful.target.residual, (a, b))
                probability, terminal = bridge.commit(lawful, (a, b))
                probabilities.append(probability)
                self.assertEqual(expected, F(11, 40) if b == 0 else F(9, 40))
                self.assertEqual(probability, expected)
                self.assertEqual(
                    components(terminal.target.residual),
                    tuple(
                        tuple((x.real / expected, x.imag / expected) for x in row) for row in cut
                    ),
                )
                self.assertIs(terminal.context, lawful.context)
                self.assertEqual(terminal.target.source, lawful.target)
                self.assertEqual(terminal.target.record.outcome, (a, b))
        self.assertEqual(sum(probabilities, F(0)), F(1))

    def test_equal_residuals_preserve_distinct_complete_local_histories(self):
        _, plain = local.commit_pauli(center_source(), "Z", 0)
        _, controlled = local.commit_pauli(local.run_word(center_source(), ("H", "H")), "Z", 0)
        self.assertEqual(plain.residual, controlled.residual)
        self.assertEqual(plain.settings, controlled.settings)
        self.assertNotEqual(plain.records, controlled.records)
        self.assertEqual(plain.records[0].settings, ())
        self.assertEqual(controlled.records[0].settings, ("H", "H"))
        left, right = coupled(plain), coupled(controlled)
        self.assertEqual(left.target.residual, right.target.residual)
        self.assertNotEqual(left.context, right.context)
        self.assertNotEqual(left.target.local.records, right.target.local.records)
        with self.assertRaises((TypeError, ValueError)):
            replace(left, context=right.context)
        p_left, terminal_left = bridge.commit(left, (0, 0))
        p_right, terminal_right = bridge.commit(right, (0, 0))
        self.assertEqual(p_left, p_right)
        self.assertEqual(terminal_left.target.residual, terminal_right.target.residual)
        self.assertNotEqual(terminal_left.target.record, terminal_right.target.record)
        self.assertEqual(terminal_left.target.record.local_records, left.target.local.records)
        self.assertEqual(terminal_right.target.record.local_records, right.target.local.records)
        self.assertIs(terminal_left.context.local_source, plain)
        self.assertIs(terminal_right.context.local_source, controlled)

    def test_terminal_record_and_wrapper_retain_pending_metadata_and_both_input_origins(self):
        state = recorded_source()
        lawful = coupled(state)
        _, terminal = bridge.commit(lawful, (1, 0))
        record = terminal.target.record
        self.assertIs(terminal.context.local_source, state)
        self.assertEqual(terminal.context.local_source.settings, ("H", "P_inv"))
        self.assertEqual(terminal.context.reference_provenance, PROVENANCE)
        self.assertEqual(
            record.precursor, (("local-run", 0), ("local-run", 1), ("reference-run", 0))
        )
        self.assertEqual(record.local_records, lawful.context.local_input.records)
        self.assertEqual(record.reference_records, lawful.context.reference.records)
        self.assertEqual(record.permutation, joint.NATIVE_TO_GROUPED)
        self.assertEqual(record.input_origins, ("local-run", "reference-run"))
        self.assertEqual(
            (record.reference_t, record.reference_orientation, record.coupler),
            (F(1, 2), "Z", joint.SHARED_COUPLER),
        )

    def test_probability_is_conditional_not_an_invented_prior_history_or_reference_weight(self):
        prior_probability, state = local.commit_pauli(center_source(), "Z", 0)
        self.assertEqual(prior_probability, F(1, 2))
        probability, terminal = bridge.commit(coupled(state), (0, 0))
        self.assertEqual(probability, F(3, 8))
        self.assertEqual(terminal.conditional_probability, probability)
        self.assertNotEqual(probability, prior_probability * F(3, 8))
        self.assertNotEqual(probability, prior_probability * F(1, 3) * F(3, 8))
        self.assertEqual(terminal.context.reference_provenance, PROVENANCE)

    def test_nonzero_zero_weight_cut_refuses_commit_without_altering_source(self):
        _, state = local.commit_pauli(center_source(), "Z", 0)
        lawful = coupled(state, 1)
        raw_before = lawful.target.residual
        cut, probability = cut_and_weight(raw_before, (0, 1))
        self.assertEqual(probability, 0)
        self.assertTrue(any(x.real or x.imag for row in cut for x in row))
        with self.assertRaises((TypeError, ValueError)):
            bridge.commit(lawful, (0, 1))
        self.assertIs(lawful.target.residual, raw_before)

    def test_local_terminal_and_foreign_or_subclass_sources_are_rejected(self):
        state = source()
        _, terminal = local.literal_cut(state, 0)

        class ForeignState(local.State):
            pass

        for wrong in (
            terminal,
            ForeignState(state.residual),
            state.residual,
            joint.LocalState(joint.section(joint.scale(F(1, 2), joint.identity(2)))),
            object(),
        ):
            with self.assertRaises((TypeError, ValueError)):
                bridge.convert_local_state(wrong, origin="local-run")

    def test_wrong_stage_or_terminal_objects_cannot_continue_as_joint_sources(self):
        prospective = prepared()
        product = bridge.promote(prospective)
        _, terminal = bridge.commit(product, (0, 0))
        for wrong in (prospective, prospective.target, terminal, terminal.target, object()):
            with self.assertRaises((TypeError, ValueError)):
                bridge.couple(wrong)
            with self.assertRaises((TypeError, ValueError)):
                bridge.commit(wrong, (0, 0))
        for wrong in (product, product.target, terminal, terminal.target):
            with self.assertRaises((TypeError, ValueError)):
                bridge.promote(wrong)

    def test_prospective_wrapper_rejects_a_valid_psd_kernel_with_wrong_forward_provenance(self):
        prospective = prepared()
        other = prepared(center_source())
        bad_target = replace(prospective.target, residual=other.target.residual)
        self.assertTrue(joint.is_psd(bad_target.residual))
        with self.assertRaises((TypeError, ValueError)):
            replace(prospective, target=bad_target)

    def test_source_wrapper_rejects_a_recordable_but_wrong_forward_residual(self):
        lawful = coupled()
        other = coupled(center_source())
        bad_target = replace(lawful.target, residual=other.target.residual)
        self.assertTrue(joint.joint_recordable(bad_target.residual, normalized=True))
        with self.assertRaises((TypeError, ValueError)):
            replace(lawful, target=bad_target)

    def test_context_and_stage_metadata_cannot_disagree(self):
        prospective = prepared(recorded_source())
        bad_context = replace(prospective.context, local_source=source())
        with self.assertRaises((TypeError, ValueError)):
            replace(prospective, context=bad_context)
        wrong_target = replace(prospective.target, joint_origin="other-joint")
        with self.assertRaises((TypeError, ValueError)):
            replace(prospective, target=wrong_target)
        wrong_coupler = replace(prospective.target, coupler=joint.SHARED_COUPLER)
        with self.assertRaises((TypeError, ValueError)):
            replace(prospective, target=wrong_coupler)
        product = bridge.promote(prospective)
        outcome = next(
            (a, b)
            for a in (0, 1)
            for b in (0, 1)
            if cut_and_weight(product.target.residual, (a, b))[1] > 0
        )
        _, terminal = bridge.commit(product, outcome)
        other_context = prepared(recorded_source(), F(-1, 2)).context
        with self.assertRaises((TypeError, ValueError)):
            replace(terminal, context=other_context)

    def test_reference_provenance_is_explicit_canonical_and_detached(self):
        mutable = [["preparation", "independent"], ["selection", "declared"]]
        prospective = prepared(provenance=(iter(row) for row in mutable))
        mutable[0][1] = "changed"
        self.assertEqual(
            prospective.context.reference_provenance,
            (("preparation", "independent"), ("selection", "declared")),
        )
        for bad in (
            (),
            "claim",
            (("key", ""),),
            (("", "value"),),
            (("key", "value"), ("key", "other")),
            (("key", True),),
            (("key",),),
        ):
            with self.assertRaises((TypeError, ValueError)):
                prepared(provenance=bad)

    def test_wrappers_and_retained_source_are_immutable(self):
        prospective = prepared(recorded_source())
        with self.assertRaises(FrozenInstanceError):
            prospective.target = None
        with self.assertRaises(FrozenInstanceError):
            prospective.context.local_origin = "different"
        with self.assertRaises(FrozenInstanceError):
            prospective.context.local_source.settings = ()
        with self.assertRaises(FrozenInstanceError):
            prospective.context.reference.t = F(0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
