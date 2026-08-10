"""
Tests for MAM-Q: Quantum-Analogue Model.

Verifies all AGENTS.md M3 exit conditions.
"""

import math
from det8.models.mamq import (
    KrausOperator,
    MeasurementCommit,
    PointerRecord,
    POVMMeasurement,
    QubitActualizer,
    QubitState,
    TwoQubitState,
    interference_demo,
    make_bell_pair,
    make_x_measurement,
    make_z_measurement,
    no_signalling_test,
    run_measurement,
    verify_no_preexisting_outcome,
)


# ── Test 1: Qubit State ────────────────────────────────────────────────────


class TestQubitState:
    def test_normalized_state(self):
        s = QubitState(alpha=1, beta=0)
        p0, p1 = s.probabilities()
        assert abs(p0 - 1.0) < 1e-12
        assert abs(p1 - 0.0) < 1e-12

    def test_plus_state_equal_probs(self):
        inv2 = 1.0 / math.sqrt(2)
        s = QubitState(alpha=inv2, beta=inv2)
        p0, p1 = s.probabilities()
        assert abs(p0 - 0.5) < 1e-12
        assert abs(p1 - 0.5) < 1e-12

    def test_auto_normalize(self):
        s = QubitState(alpha=3, beta=4)
        p0, p1 = s.probabilities()
        assert abs(p0 - 9 / 25) < 1e-12
        assert abs(p1 - 16 / 25) < 1e-12

    def test_copy_independent(self):
        s1 = QubitState(alpha=1, beta=0)
        s2 = s1.copy()
        s2.alpha = 0
        s2.beta = 1
        assert abs(s1.alpha - 1.0) < 1e-12
        assert abs(s1.beta - 0.0) < 1e-12

    def test_no_hidden_outcome_field(self):
        """Qubit state stores only α, β — no hidden outcome selector."""
        s = QubitState(alpha=0.6, beta=0.8)
        assert not hasattr(s, "will_measure_0")
        assert not hasattr(s, "hidden_outcome")
        assert not hasattr(s, "pre_existing_value")


# ── Test 2: Kraus Operators / POVM ─────────────────────────────────────────


class TestKrausPOVM:
    def test_z_measurement_zero_state(self):
        s = QubitState(alpha=1, beta=0)
        z = make_z_measurement()
        poss = z.compute_possibility(s)

        assert len(poss.omega) == 1  # deterministic for |0⟩
        assert poss.omega[0][0] == 0  # outcome 0
        assert abs(poss.kernel[0] - 1.0) < 1e-12

    def test_z_measurement_one_state(self):
        s = QubitState(alpha=0, beta=1)
        z = make_z_measurement()
        poss = z.compute_possibility(s)

        assert len(poss.omega) == 1  # deterministic for |1⟩
        assert poss.omega[0][0] == 1

    def test_z_measurement_plus_state(self):
        inv2 = 1.0 / math.sqrt(2)
        s = QubitState(alpha=inv2, beta=inv2)
        z = make_z_measurement()
        poss = z.compute_possibility(s)

        assert len(poss.omega) == 2  # two outcomes
        assert set(label for label, _ in poss.omega) == {0, 1}
        # Both propensities ≈ 0.5.
        assert abs(poss.kernel[0] - 0.5) < 1e-12
        assert abs(poss.kernel[1] - 0.5) < 1e-12

    def test_x_measurement_plus_state_deterministic(self):
        inv2 = 1.0 / math.sqrt(2)
        s = QubitState(alpha=inv2, beta=inv2)
        x = make_x_measurement()
        poss = x.compute_possibility(s)

        assert len(poss.omega) == 1
        assert poss.omega[0][0] == 0

    def test_kernel_normalized(self):
        inv2 = 1.0 / math.sqrt(2)
        s = QubitState(alpha=inv2, beta=inv2)
        z = make_z_measurement()
        poss = z.compute_possibility(s)

        assert abs(sum(poss.kernel) - 1.0) < 1e-12
        assert all(k >= 0 for k in poss.kernel)


# ── Test 3: Born Rule as Provisional Calibration ────────────────────────────


class TestBornRule:
    def test_born_rule_in_omega(self):
        """The Born rule enters only through the kernel, not through
        any claim about its ontological status. It is labeled H/O."""
        inv2 = 1.0 / math.sqrt(2)
        s = QubitState(alpha=inv2, beta=inv2)
        z = make_z_measurement()
        poss = z.compute_possibility(s)

        # The kernel is computed from |α|², |β|².
        # But the formal status is provisional calibration, not derivation.
        assert abs(poss.kernel[0] - 0.5) < 1e-12
        assert abs(poss.kernel[1] - 0.5) < 1e-12


# ── Test 4: Pointer-Record Commit ───────────────────────────────────────────


class TestPointerRecordCommit:
    def test_pointer_starts_uncommitted(self):
        p = PointerRecord()
        assert not p.is_committed
        assert p.value is None

    def test_commit_writes_pointer(self):
        s = QubitState(alpha=0, beta=1)
        p = PointerRecord()
        MeasurementCommit.commit(s, p, (1, QubitState(alpha=0, beta=1)))

        assert p.is_committed
        assert p.value == 1

    def test_commit_collapses_state(self):
        inv2 = 1.0 / math.sqrt(2)
        s = QubitState(alpha=inv2, beta=inv2)
        p = PointerRecord()

        # Commit outcome 0.
        post_state_0 = QubitState(alpha=1, beta=0)
        MeasurementCommit.commit(s, p, (0, post_state_0))

        assert abs(s.alpha - 1.0) < 1e-12
        assert abs(s.beta - 0.0) < 1e-12


# ── Test 5: Interference / Two-Path Behavior ────────────────────────────────


class TestInterference:
    def test_interference_demo(self):
        result = interference_demo(n_samples=5000, seed=42)

        # Z on |+⟩: both outcomes appear (open).
        assert result["Z_is_open"]
        assert result["Z_on_plus"][0] > 0.4  # ~0.5
        assert result["Z_on_plus"][1] > 0.4  # ~0.5

        # X on |+⟩: only outcome 0 (deterministic).
        assert result["X_is_deterministic"]
        assert result["X_on_plus"][0] == 1.0
        assert result["X_on_plus"][1] == 0.0

    def test_basis_dependence(self):
        """The same state can be open in one basis and deterministic in another.
        This is the DET distinction between relational record (the state)
        and pointer record (the measurement outcome).
        """
        inv2 = 1.0 / math.sqrt(2)
        s = QubitState(alpha=inv2, beta=inv2)

        z_poss = make_z_measurement().compute_possibility(s)
        x_poss = make_x_measurement().compute_possibility(s)

        assert len(z_poss.omega) == 2  # open
        assert len(x_poss.omega) == 1  # deterministic


# ── Test 6: No Pre-Existing Outcome Storage ─────────────────────────────────


class TestNoPreselectedOutcome:
    def test_pre_measurement_pointer_is_none(self):
        inv2 = 1.0 / math.sqrt(2)
        s = QubitState(alpha=inv2, beta=inv2)
        pointer, event_log = run_measurement(
            s, make_z_measurement(), QubitActualizer(seed=42)
        )

        # After measurement, pointer is committed.
        assert pointer.is_committed
        # But the pre-measurement state had no predetermined outcome.
        assert verify_no_preexisting_outcome(event_log)

    def test_no_hidden_future_in_state(self):
        """The qubit state has no field that pre-selects a measurement outcome."""
        inv2 = 1.0 / math.sqrt(2)
        s = QubitState(alpha=inv2, beta=inv2)

        # All fields are in the dataclass __dataclass_fields__.
        field_names = set(s.__dataclass_fields__.keys())
        assert "alpha" in field_names
        assert "beta" in field_names
        assert "future_outcome" not in field_names
        assert "hidden_value" not in field_names

    def test_state_is_relational_not_outcome_warehouse(self):
        """A superposition is an actual relational record that constrains
        future outcomes without containing those outcomes as pre-existing facts.
        """
        inv2 = 1.0 / math.sqrt(2)
        s = QubitState(alpha=inv2, beta=inv2)
        poss = make_z_measurement().compute_possibility(s)

        # Both outcomes are possible but neither pre-exists.
        assert len(poss.omega) == 2
        # The state gives propensities, not hidden facts.
        assert abs(poss.kernel[0] - 0.5) < 1e-12


# ── Test 7: No-Signalling ───────────────────────────────────────────────────


class TestNoSignalling:
    def test_bell_pair_creation(self):
        bell = make_bell_pair()
        # Trace condition: reduced state of B should be maximally mixed.
        rho00, rho01, rho10, rho11 = bell.reduced_density_qubit_b()
        assert abs(rho00 - 0.5) < 1e-12
        assert abs(rho11 - 0.5) < 1e-12

    def test_no_signalling_holds(self):
        result = no_signalling_test(n_samples=5000, seed=42)
        assert result["no_signalling_holds"], (
            f"Delta = {result['delta']:.4f}, expected < 0.05"
        )
        assert abs(result["P(B=0 | A measured in Z)"] - 0.5) < 0.05
        assert abs(result["P(B=0 | A measured in X)"] - 0.5) < 0.05

    def test_no_signalling_is_causal_locality(self):
        """DET distinguishes causal locality (no controllable superluminal
        signalling) from Bell-local factorizability (which may be rejected).
        No-signalling is the former; it must hold."""
        result = no_signalling_test(n_samples=3000, seed=123)
        assert result["no_signalling_holds"]


# ── Integration: Full Measurement Cycle ─────────────────────────────────────


class TestFullCycle:
    def test_record_possibility_commit_cycle(self):
        """Verify the full DET cycle for a measurement event:
        |+⟩ state (relational record) → Z measurement possibility (law map)
        → actualize (select outcome) → commit (pointer record).
        """
        inv2 = 1.0 / math.sqrt(2)
        state = QubitState(alpha=inv2, beta=inv2)
        pointer, event_log = run_measurement(
            state, make_z_measurement(), QubitActualizer(seed=42)
        )

        # After measurement:
        # - Pointer record is committed.
        assert pointer.is_committed
        assert pointer.value in (0, 1)

        # - Qubit state collapsed to the outcome basis state.
        if pointer.value == 0:
            assert abs(state.alpha) > 0.99
            assert abs(state.beta) < 0.01
        else:
            assert abs(state.alpha) < 0.01
            assert abs(state.beta) > 0.99

        # - Event log preserved the chain of evidence.
        assert len(event_log.entries) == 1
        entry = event_log.entries[0]
        assert entry["outcome_label"] == entry["pointer_value"]


class TestTwoQubitState:
    def test_auto_normalize(self):
        s = TwoQubitState(amp00=1, amp01=1, amp10=1, amp11=1)
        # Should normalize to 1/2 for each amplitude.
        assert abs(abs(s.amp00) - 0.5) < 1e-12
        assert abs(abs(s.amp01) - 0.5) < 1e-12
        assert abs(abs(s.amp10) - 0.5) < 1e-12
        assert abs(abs(s.amp11) - 0.5) < 1e-12

    def test_product_state_probs(self):
        """|00⟩: prob of B=0 should be 1."""
        s = TwoQubitState(amp00=1, amp01=0, amp10=0, amp11=0)
        p0, p1 = s.prob_b_given_a_measurement(0, "Z")
        assert abs(p0 - 1.0) < 1e-12
        assert abs(p1 - 0.0) < 1e-12


class TestActualizer:
    def test_actualizer_samples_all_outcomes(self):
        inv2 = 1.0 / math.sqrt(2)
        state = QubitState(alpha=inv2, beta=inv2)
        z = make_z_measurement()
        actualizer = QubitActualizer(seed=42)

        outcomes_seen = set()
        for _ in range(1000):
            state_copy = state.copy()
            poss = z.compute_possibility(state_copy)
            outcome = actualizer.select(poss)
            outcomes_seen.add(outcome[0])

        assert outcomes_seen == {0, 1}
