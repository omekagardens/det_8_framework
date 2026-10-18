"""Independent finite witnesses and the scope of experimental QM certificates.

Exact counterexamples test the mathematics. Metadata assertions keep imported
theorems and finite diagnostics from being emitted as a DET selection proof;
they do not purport to verify the imported NPA/Tsirelson theorems themselves.
"""

import itertools
import math
from fractions import Fraction as F

import pytest

from det8.models import (
    born_rule_uniqueness as born,
)
from det8.models import (
    correlation_class as correlations,
)
from det8.models import (
    correlation_frontier as frontier,
)
from det8.models import (
    grade2_justification as grade,
)
from det8.models import (
    quantum_deadlock as deadlock,
)
from det8.models import (
    record_extendability as records,
)
from det8.models import (
    u1_emergence as u1,
)
from det8.models import (
    why_complex as complex_forms,
)
from det8.models.pair_kernel import PairKernel


def product(a, b):
    return [[sum(x * y for x, y in zip(row, column)) for column in zip(*b)]
            for row in a]


def transpose(a):
    return list(map(list, zip(*a)))


def add(a, b, sign=1):
    return [[x + sign * y for x, y in zip(row_a, row_b)]
            for row_a, row_b in zip(a, b)]


def test_exact_positive_reversible_forms_do_not_force_complex_compatibility():
    # D has trace 1, determinant 3/16, hence positive eigenvalues 1/4 and 3/4.
    # G and Ω have exact rational entries; the rotation preserves both but
    # J=G^-1 Ω=J0/2 squares to -I/4, not -I.
    g = [[F(1, 2), 0], [0, F(1, 2)]]
    omega = [[0, F(1, 4)], [-F(1, 4), 0]]
    rotation = [[0, 1], [-1, 0]]
    j = [[2 * x for x in row] for row in omega]
    assert product(j, j) == [[-F(1, 4), 0], [0, -F(1, 4)]]
    for form in (g, omega):
        assert product(product(transpose(rotation), form), rotation) == form
    d = [[complex(g[i][k], omega[i][k]) for k in range(2)] for i in range(2)]
    assert sum(map(sum, d)) == 1
    assert g[0][0] * g[1][1] - omega[0][1] ** 2 == F(3, 16)
    result = complex_forms.reversible_form_counterexample()
    assert result["kernel"] == d
    assert result["eigenvalues"] == (0.25, 0.75)
    assert result["J_squared"] == product(j, j)
    assert result["rotation_preserves_both_forms"]
    assert not result["J_squared_equals_minus_I"]
    assert not result["complex_field_selected"]


@pytest.mark.parametrize("t", [0, 1, -0.5, float("nan"), float("inf"), True])
def test_reversible_counterexample_parameter_domain(t):
    with pytest.raises(ValueError):
        complex_forms.reversible_form_counterexample(t)


def test_compatible_generator_identity_has_nonzero_positive_and_negative_controls():
    j = [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]]
    zero = [[0] * 4 for _ in range(4)]
    identity = [[int(i == k) for k in range(4)] for i in range(4)]
    assert product(j, j) == [[-x for x in row] for row in identity]
    # A nonzero antisymmetric generator mixing one coordinate from each block
    # preserves G=I, but does not preserve J0. The positive control is X=J0.
    incompatible = [[0, 0, 1, 0], [0, 0, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 0]]
    for x, expected_preserves in ((j, True), (incompatible, False)):
        assert x != zero
        assert add(transpose(x), x) == zero
        symplectic_residual = add(product(transpose(x), j), product(j, x))
        commutator = add(product(j, x), product(x, j), sign=-1)
        assert symplectic_residual == commutator
        assert (symplectic_residual == zero) is expected_preserves
    for result in (complex_forms.complex_structure(),
                   complex_forms.reversible_dynamics_require_complex()):
        assert result["compatibility_assumed"]
        assert not result["complex_field_selected"]


def test_real_normalized_positive_kernel_has_interference_without_field_selection():
    d = [[F(1, 3), F(1, 6)], [F(1, 6), F(1, 3)]]
    assert sum(map(sum, d)) == 1
    assert d[0][0] * d[1][1] - d[0][1] ** 2 == F(1, 12)
    i2 = sum(map(sum, d)) - d[0][0] - d[1][1]
    assert i2 == F(1, 3)
    result = complex_forms.real_part_gives_real_qm()
    assert result["I2"] == pytest.approx(float(i2))
    assert result["real_QM_not_classical"]
    assert not result["scope"]["full_real_qm_reconstructed"]
    assert not result["scope"]["empirical_exclusion_performed"]
    assert not complex_forms.why_not_quaternions()["selects_complex_over_quaternionic"]


def test_exact_nonnegative_grade_two_measure_has_no_positive_gram_representation():
    events = [frozenset(s) for n in range(4)
              for s in itertools.combinations(range(3), n)]
    mu = {a: F(len(a) * (len(a) - 1), 6) for a in events}
    assert mu[frozenset(range(3))] == 1
    assert all(value >= 0 for value in mu.values())
    assert all(mu[frozenset([i])] == 0 for i in range(3))
    i3 = sum((-1) ** (3 - len(a)) * value for a, value in mu.items())
    assert i3 == 0
    # The real part of any Hermitian representing D is fixed: diagonal 0,
    # off-diagonal 1/6. Imaginary parts cancel for the real vector (1,-1,0).
    real_part = [[0 if i == j else F(1, 6) for j in range(3)] for i in range(3)]
    v = [1, -1, 0]
    assert sum(v[i] * real_part[i][j] * v[j] for i in range(3) for j in range(3)) == -F(1, 3)
    result = grade.strong_positivity_counterexample()
    for event, value in mu.items():
        assert result["measure"].mu(event) == pytest.approx(float(value))
    assert result["normalized"] and result["eventwise_positive"]
    assert result["grade"] == 2
    assert not result["strong_positive_representation_exists"]


def test_squared_amplitude_positive_control_and_local_count_scope():
    amplitudes = (1, 2j, -1)
    def squared_norm(z):
        return z.real ** 2 + z.imag ** 2

    probabilities = {frozenset(s): squared_norm(sum(amplitudes[i] for i in s))
                     for n in range(1, 4) for s in itertools.combinations(range(3), n)}
    i3 = sum((-1) ** (3 - len(a)) * p for a, p in probabilities.items())
    assert i3 == 0
    assert deadlock.born_rule_is_grade2(amplitudes)["I3"] == pytest.approx(0, abs=1e-12)
    # This exact synthetic null still supplies no significance or universal law.
    result = grade.grade2_discriminator(probabilities)
    assert result["I3"] == 0
    assert result["grade2"]
    assert result["scope"] == {"tested_triple": (0, 1, 2), "significance_test": False,
                               "universal_grade2_established": False, "born_rule_selected": False}


@pytest.mark.parametrize("p", [1, 1.5, 2, 3, 4])
@pytest.mark.parametrize("n", [2, 3, 7])
def test_matching_lp_normalizations_all_conserve(p, n):
    amplitudes = [n ** (-1 / p)] * n
    assert sum(abs(c) ** p for c in amplitudes) == pytest.approx(1)
    assert born.lp_normalized_split_total_probability(p, n) == pytest.approx(1)
    expected_l2 = n ** (1 - p / 2)
    assert born.symmetric_split_total_probability(p, n) == pytest.approx(expected_l2)
    assert math.isclose(expected_l2, 1) is (p == 2)


def test_different_bare_tensor_extensions_have_the_same_old_marginal():
    original = PairKernel([[F(1, 2), 0], [0, F(1, 2)]])
    new_factors = [PairKernel([[1, 0], [0, 0]]), PairKernel([[0, 0], [0, 1]])]
    extensions = [original.compose(new) for new in new_factors]
    assert extensions[0].D != extensions[1].D
    for extension, new in zip(extensions, new_factors):
        assert records.marginal(extension, records.product_blocks(2, 2)).D == original.D
        # Sum the old coordinate instead: the newly supplied factor is free.
        assert records.marginal(extension, [frozenset([0, 2]), frozenset([1, 3])]).D == new.D
        assert records.trivial_extendability(original, new)["always_extends"]
    assert not records.resolution()["scope"]["bare_marginals_sufficient"]


def test_bell_word_fixture_is_one_finite_extension_with_a_distinct_q1ab_inventory():
    result = correlations.bell_state_npa_level1()
    expected = {"", "A0", "A1", "B0", "B1", "A0B0", "A0B1", "A1B0", "A1B1"}
    assert set(result["words"]) == expected
    assert len(result["words"]) == 9
    assert result["word_count"] == 9
    assert result["npa_level"] == "Q_1+AB"
    assert result["psd"] and result["constraints"]["all_constraints"]
    assert not result["general_membership_test"]
    extension = correlations.global_record_extendability()
    assert extension["level2_psd"] and extension["level1_is_principal_submatrix"]
    assert not extension["all_level_extension_established"]
    assert not extension["bare_marginal_equivalence_established"]
    operational = records.operator_algebra_consistency()
    assert operational["tested_levels"] == ("Q_1+AB", "Q_2")
    assert not operational["arbitrary_almost_quantum_rejection_established"]
    assert not operational["all_level_extension_tested"]


def behavior_with_marginals(e, alice, bob):
    return correlations.NoSignallingCorrelation([
        [(1 + (-1) ** a * alice[x] + (-1) ** b * bob[y]
          + (-1) ** (a + b) * e[2 * x + y]) / 4
         for a in (0, 1) for b in (0, 1)]
        for x in (0, 1) for y in (0, 1)])


def test_tlm_projection_does_not_read_valid_behavior_marginal_biases():
    # Both tables are nonnegative, normalized and no-signalling; their distinct
    # marginal data is invisible to the four-correlator predicate. We make no
    # unsupported full quantum-membership claim about the biased table.
    s = 1 / math.sqrt(2)
    e = (s, s, s, -s)
    uniform = behavior_with_marginals(e, (0, 0), (0, 0))
    biased = behavior_with_marginals(e, (0.1, 0.1), (0.1, 0.1))
    assert uniform.M != biased.M
    assert uniform.marginal_alice(0, 0) != biased.marginal_alice(0, 0)
    for behavior in (uniform, biased):
        assert all(p >= 0 for row in behavior.M for p in row)
        assert behavior.validate()["valid"]
        assert behavior.correlations() == pytest.approx(e)
        assert frontier.correlators_satisfy_tlm(behavior)
        assert frontier.is_quantum_masanes(behavior)
    assert frontier.tlm_sums(uniform) == pytest.approx(frontier.tlm_sums(biased))
    assert not frontier.correlators_satisfy_tlm(correlations.pr_box())
    assert not frontier.derivation_certificate()["scope"]["tlm_full_behavior_membership_test"]


@pytest.mark.parametrize("row", [[0.6, 0.6, -0.1, -0.1], [-0.1, 0.1, 0.1, 0.9]])
def test_signed_normalized_no_signalling_tables_do_not_pass_membership(row):
    behavior = correlations.NoSignallingCorrelation([row] * 4)
    assert behavior.is_normalized() and behavior.is_no_signalling()
    report = behavior.validate()
    assert report["finite"] and not report["nonnegative"] and not report["valid"]
    assert not behavior.is_classical()
    assert not frontier.is_quantum_masanes(behavior)
    with pytest.raises(ValueError, match="valid finite nonnegative"):
        frontier.tlm_sums(behavior)
    assert behavior.M == [row] * 4  # No clipping or hidden repair.


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), -float("inf"),
                                     1 + 0j, True, "0.25"])
def test_nonfinite_or_nonreal_probability_entries_are_invalid_diagnostics(invalid):
    behavior = correlations.NoSignallingCorrelation([[invalid, 0.25, 0.25, 0.25]] * 4)
    assert not behavior.has_finite_probabilities()
    assert not behavior.validate()["valid"]
    assert not behavior.is_classical()
    assert not frontier.correlators_satisfy_tlm(behavior)
    with pytest.raises(ValueError):
        frontier.tlm_sums(behavior)


def test_tlm_does_not_clip_correlators_even_inside_normalization_tolerance():
    behavior = correlations.NoSignallingCorrelation([[1 + 5e-10, 0, 0, 0]] * 4)
    assert behavior.validate()["valid"]  # Stated 1e-9 equality tolerance.
    assert all(e > 1 for e in behavior.correlations())
    assert not frontier.correlators_satisfy_tlm(behavior)
    with pytest.raises(ValueError, match="correlators must lie"):
        frontier.tlm_sums(behavior)


@pytest.mark.parametrize("matrix", [
    [[0.2] * 4] * 4,  # Unnormalized even though finite and nonnegative.
    [[1, 0, 0, 0], [0.25] * 4, [0.25] * 4, [0.25] * 4],  # Signalling.
])
def test_invalid_normalization_or_signalling_rejects_membership(matrix):
    behavior = correlations.NoSignallingCorrelation(matrix)
    assert not behavior.validate()["valid"]
    assert not behavior.is_classical()
    assert not frontier.correlators_satisfy_tlm(behavior)


@pytest.mark.parametrize("tol", [-1, float("nan"), float("inf")])
def test_invalid_tolerances_cannot_bypass_behavior_or_tlm_checks(tol):
    behavior = correlations.pr_box()
    for check in (behavior.validate, behavior.is_classical):
        with pytest.raises(ValueError):
            check(tol=tol)
    with pytest.raises(ValueError):
        frontier.correlators_satisfy_tlm(behavior, tol=tol)


def test_exact_behavior_boundary_and_canonical_positive_controls():
    local = correlations.local_deterministic_correlation()
    assert local.validate(tol=0)["valid"]
    assert local.is_classical(tol=0)
    assert frontier.correlators_satisfy_tlm(local, tol=0)
    assert correlations.bell_state_correlation().validate()["valid"]
    assert correlations.pr_box().validate(tol=0)["valid"]
    report = correlations.run_t6()
    metadata = report["membership_scope"]
    assert metadata["legacy_key_levels"]["Bell ∈ Q̃ (level-1 PSD + constraints)"] == "Q_1+AB"
    assert metadata["bell_constraints_are_partial_diagnostics"]
    assert not metadata["general_behavior_membership_test"]


def test_imported_hierarchy_endpoint_scope_is_consistent_across_certificates():
    reports = [correlations.derivation_certificate(), frontier.derivation_certificate(),
               frontier.npa_convergence_statement(), records.derivation_certificate(),
               records.resolution()]
    for report in reports:
        scope = report["scope"]
        assert scope["npa_limit"] == "C_qc"
        assert scope["tensor_product_closure"] == "C_qa"
        assert scope["almost_quantum_level"] == "Q_1+AB"
        assert scope["requires_operator_word_relations"]
        assert not scope["bare_marginals_sufficient"]
        assert not scope["tensor_closure_equals_commuting_in_general"]
        assert not scope["det_correlation_class_selected"]
        assert scope["ordinary_level_one_word_count"] == 5
        assert scope["selected_word_count"] == 9


def test_grade_and_field_certificates_do_not_promote_unproved_premises():
    grade_scope = grade.derivation_certificate()["scope"]
    assert not grade_scope["grade2_implies_strong_positivity"]
    assert grade_scope["gram_requires_strong_positivity"]
    assert not grade_scope["composition_closure_established"]
    assert not grade_scope["empirical_born_selection"]
    assert not born.grade2_born_connection()["scope"]["three_slit_null_selects_born"]
    assert not born.grade2_born_connection()["scope"]["grade2_implies_strong_positivity"]
    assert born.born_rule_uniqueness_theorem()["scope"]["l2_normalization_assumed"]
    assert not born.born_rule_uniqueness_theorem()["scope"]["born_rule_derived"]
    assert not complex_forms.derivation_certificate()["scope"]["complex_field_selected"]
    observations = complex_forms.connection_to_observation()["scope"]
    assert not observations["empirical_data_analyzed"]
    assert not observations["real_correlators_equal_almost_quantum"]


def test_uniform_preserving_channel_is_exactly_noninjective():
    channel = [[F(1, 2)] * 2 for _ in range(2)]
    assert all(sum(column) == 1 for column in zip(*channel))
    assert product(channel, [[F(1, 2)], [F(1, 2)]]) == [[F(1, 2)], [F(1, 2)]]
    assert product(channel, [[1], [0]]) == product(channel, [[0], [1]])
    assert channel[0][0] * channel[1][1] - channel[0][1] * channel[1][0] == 0
    result = u1.irreversible_record_reversible_possibility()
    assert result["counterexample"]["uniform_preserving_channel"] == channel
    assert result["counterexample"]["distinct_input_outputs"] == [[0.5, 0.5]] * 2
    assert not result["counterexample"]["injective"]
    assert not result["reversibility_derived"]
    assert not u1.one_arrow_implies_one_phase()["causal_order_implies_one_phase"]
    assert not u1.u1_emergence_resolution()["scope"]["u1_emergence_proved"]


def test_direct_consumer_coherence_is_algebraic_and_not_ontology_validation():
    result = deadlock.quantum_resolution()
    assert result["coherence"]["coherent"]
    assert result["coherence"]["scope"]["algebraic_examples_only"]
    assert not result["coherence"]["scope"]["ontology_validated"]
    assert not result["coherence"]["static_level_is_real"]
    assert not result["coherence"]["complex_is_dynamical"]
    assert not result["full_qm_derived"]
    assert not result["almost_quantum"]["real_correlators_equal_almost_quantum"]
