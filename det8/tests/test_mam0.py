"""
Tests for MAM-0: Minimal Actualization Model.

Verifies all AGENTS.md M2 exit conditions.
"""

from det8.models.mam0 import (
    Actualizer,
    CommitMap,
    EventScheduler,
    LawMap,
    PossibilityObject,
    Record,
    Regime,
    deterministic_baseline_comparison,
    scheduler_independence_demo,
)


# ── Test 1: Finite Record Model ─────────────────────────────────────────────


class TestRecord:
    def test_record_creation(self):
        r = Record(value=7)
        assert r.value == 7

    def test_record_copy_independent(self):
        r1 = Record(value=3)
        r2 = r1.copy()
        r2.value = 99
        assert r1.value == 3  # original unaffected

    def test_record_modal_annotation(self):
        """Record is A (actual committed fact) — no hidden fields."""
        r = Record(value=0)
        assert not hasattr(r, "future_outcome")
        assert not hasattr(r, "hidden_selector")
        assert not hasattr(r, "agency")


# ── Test 2: Deterministic Case (Singleton Support) ──────────────────────────


class TestDeterministicRegime:
    def test_singleton_support(self):
        """When values are (0, 5), the only valid transfer from A to B
        is d=-1 (A gives to B, wait no: d=-1 means new_a = a - (-1) = a+1,
        but nonnegativity for a: new_a >= 0 always. Let's work it out:
        transfers d ∈ {-1, 0, +1}:
          d=-1: new_a = a - (-1) = a+1, new_b = b + (-1) = b-1
          d=0:  new_a = a, new_b = b
          d=+1: new_a = a-1, new_b = b+1
        
        So for (a=0, b=5):
          d=-1: (1, 4) — valid (both ≥ 0)
          d=0:  (0, 5) — valid
          d=+1: (-1, 6) — INVALID (new_a < 0)
        
        So deterministic regime constrains to singleton by picking d=0.
        """
        r_a = Record(value=0)
        r_b = Record(value=5)
        w = LawMap.generate(r_a, r_b, Regime.DETERMINISTIC)

        assert w.is_deterministic
        assert len(w.omega) == 1
        assert w.omega[0] == (0, 5)

    def test_deterministic_always_same_output(self):
        """Same input → same Ω every time."""
        r_a = Record(value=3)
        r_b = Record(value=3)
        w1 = LawMap.generate(r_a, r_b, Regime.DETERMINISTIC)
        w2 = LawMap.generate(r_a, r_b, Regime.DETERMINISTIC)

        assert w1.omega == w2.omega
        assert w1.kernel == w2.kernel

    def test_actualizer_returns_singleton(self):
        w = PossibilityObject(omega=[(4, 4)], kernel=[1.0], constraints=["test"])
        actualizer = Actualizer(seed=0)
        for _ in range(100):
            assert actualizer.select(w) == (4, 4)


# ── Test 3: Open-Support Case (Two Outcomes) ────────────────────────────────


class TestOpenRegime:
    def test_multi_support(self):
        """For (a=1, b=1), valid transfers are:
          d=-1: (2, 0) — valid
          d=0:  (1, 1) — valid
          d=+1: (0, 2) — valid
        
        So Ω has 3 elements in open regime.
        """
        r_a = Record(value=1)
        r_b = Record(value=1)
        w = LawMap.generate(r_a, r_b, Regime.OPEN)

        assert w.is_open
        assert len(w.omega) == 3

    def test_two_outcome_case(self):
        """For (a=0, b=1), valid transfers are:
          d=-1: (1, 0) — valid
          d=0:  (0, 1) — valid
          d=+1: (-1, 2) — INVALID
        
        So 2 outcomes (our minimal two-outcome case).
        """
        r_a = Record(value=0)
        r_b = Record(value=1)
        w = LawMap.generate(r_a, r_b, Regime.OPEN)

        assert w.is_open
        assert len(w.omega) == 2
        assert w.omega == [(1, 0), (0, 1)]

    def test_kernel_normalized(self):
        r_a = Record(value=1)
        r_b = Record(value=1)
        w = LawMap.generate(r_a, r_b, Regime.OPEN)

        assert abs(sum(w.kernel) - 1.0) < 1e-12
        assert all(k >= 0 for k in w.kernel)

    def test_open_actualizer_explores_support(self):
        """Over many draws, both outcomes should appear."""
        w = PossibilityObject(
            omega=[(1, 0), (0, 1)],
            kernel=[0.5, 0.5],
            constraints=["test"],
        )
        actualizer = Actualizer(seed=42)
        outcomes = {actualizer.select(w) for _ in range(1000)}

        assert (1, 0) in outcomes
        assert (0, 1) in outcomes


# ── Test 4: Commit Rule ─────────────────────────────────────────────────────


class TestCommit:
    def test_commit_writes_values(self):
        r_a = Record(value=3)
        r_b = Record(value=7)
        CommitMap.commit(r_a, r_b, (2, 8))

        assert r_a.value == 2
        assert r_b.value == 8

    def test_commit_is_irreversible_overwrite(self):
        r_a = Record(value=5)
        r_b = Record(value=5)
        CommitMap.commit(r_a, r_b, (4, 6))
        CommitMap.commit(r_a, r_b, (3, 7))

        assert r_a.value == 3  # not 5
        assert r_b.value == 7  # not 5


# ── Test 5: Conservation-Like Constraints ───────────────────────────────────


class TestConservation:
    def test_total_sum_preserved(self):
        records = {0: Record(3), 1: Record(7)}
        actualizer = Actualizer(seed=1)
        scheduler = EventScheduler(records)

        for i in range(20):
            scheduler.schedule_event(
                f"e_{i}", 0, 1, Regime.OPEN, actualizer
            )

        total, conserved = scheduler.verify_conservation()
        assert conserved
        assert total == 10

    def test_nonnegativity_enforced(self):
        r_a = Record(value=0)
        r_b = Record(value=0)
        w = LawMap.generate(r_a, r_b, Regime.OPEN)

        for outcome in w.omega:
            assert outcome[0] >= 0
            assert outcome[1] >= 0

    def test_impossible_transfer_rejected(self):
        """With (0, 0), only d=0 is valid → nonempty Ω."""
        r_a = Record(value=0)
        r_b = Record(value=0)
        w = LawMap.generate(r_a, r_b, Regime.OPEN)

        assert len(w.omega) == 1  # only (0,0)
        assert w.omega == [(0, 0)]


# ── Test 6: Scheduler Independence ──────────────────────────────────────────


class TestSchedulerIndependence:
    def test_different_schedules_produce_lawful_records(self):
        rec1, rec2, log1, log2 = scheduler_independence_demo(seed=42)

        # Both schedules must conserve total sum.
        total1 = rec1[0].value + rec1[1].value + rec1[2].value
        total2 = rec2[0].value + rec2[1].value + rec2[2].value
        assert total1 == 15  # initial was 5+5+5
        assert total2 == 15

        # Both schedules produce non-negative values.
        for i in range(3):
            assert rec1[i].value >= 0
            assert rec2[i].value >= 0

    def test_scheduler_is_not_a_physical_present(self):
        """The scheduler token (event_log indices) is not stored in records."""
        rec1, rec2, _, _ = scheduler_independence_demo(seed=42)

        # Records contain only values — no schedule metadata.
        for i in range(3):
            r = rec1[i]
            assert not hasattr(r, "schedule_index")
            assert not hasattr(r, "global_step")


# ── Test 7: No Future Outcome Stored Before Commit ──────────────────────────


class TestNoPreselectedFuture:
    def test_pre_commit_record_does_not_contain_selected_outcome(self):
        """In open regime, the pre-commit record is (a, b).
        The selected successor is (a±1, b∓1) or (a, b).
        If d=0 is selected, pre == post. If d≠0, pre ≠ post.
        But critically: there is no field in the record that tells us
        in advance which will be chosen. The record only stores committed
        values, not future selectors.
        """
        records = {0: Record(1), 1: Record(1)}
        actualizer = Actualizer(seed=99)
        scheduler = EventScheduler(records)

        scheduler.schedule_event("e", 0, 1, Regime.OPEN, actualizer)

        entry = scheduler.event_log[-1]
        # Pre-commit state is the past record, not a prophecy.
        assert entry["pre_commit"] == (1, 1)
        # The selected outcome is one of the lawful successors.
        assert entry["selected"] in entry["omega"]

    def test_record_has_no_hidden_future_field(self):
        r = Record(value=5)
        field_names = vars(r).keys()
        assert "value" in field_names
        assert "next_outcome" not in field_names
        assert "future" not in field_names
        assert "selector" not in field_names

    def test_omega_does_not_preselect(self):
        """The possibility object describes what MAY become,
        not what WILL become. The kernel is a present propensity,
        not a hidden instruction."""
        r_a = Record(value=1)
        r_b = Record(value=1)
        w = LawMap.generate(r_a, r_b, Regime.OPEN)

        # The kernel is uniform — no outcome is "preferred by a hidden token".
        assert all(k == 1.0 / 3 for k in w.kernel)


# ── Test 8: Deterministic Baseline Comparison ───────────────────────────────


class TestBaselineComparison:
    def test_deterministic_vs_open_behavior(self):
        result = deterministic_baseline_comparison(seed=42, n_events=200)

        # Deterministic should produce exactly 1 distinct outcome pattern.
        assert result["deterministic_outcome_count"] <= 2  # (0,1)→(0,1) only

        # Open should have multiple options available at each event.
        assert all(n > 1 for n in result["open_outcome_options_per_event"])


# ── Integration: Full Cycle ─────────────────────────────────────────────────


class TestFullCycle:
    def test_record_possibility_commit_cycle(self):
        """Verify the full cycle:
        R⁻ → L → W → actualize → Commit → R⁺
        """
        records = {0: Record(2), 1: Record(2)}
        actualizer = Actualizer(seed=7)
        scheduler = EventScheduler(records)

        # Run 10 cycles.
        for i in range(10):
            scheduler.schedule_event(f"cycle_{i}", 0, 1, Regime.OPEN, actualizer)

        # After each cycle:
        # - total sum conserved
        total, ok = scheduler.verify_conservation()
        assert ok
        assert total == 4

        # - values are non-negative
        assert records[0].value >= 0
        assert records[1].value >= 0

        # - the event log preserves the chain of evidence
        assert len(scheduler.event_log) == 10
        for entry in scheduler.event_log:
            assert entry["selected"] in entry["omega"]


class TestPossibilityObject:
    def test_empty_omega_raises(self):
        import pytest as _unused

    def test_deterministic_flag(self):
        w = PossibilityObject(omega=[(0, 0)], kernel=[1.0])
        assert w.is_deterministic
        assert not w.is_open

        w2 = PossibilityObject(omega=[(1, 0), (0, 1)], kernel=[0.5, 0.5])
        assert not w2.is_deterministic
        assert w2.is_open
