"""
Confluence and Scheduler Analysis for DET 8

Implements proper confluence testing for MAM-0 event schedules.
Distinguishes three levels of scheduler robustness:

1. Invariant preservation: both schedules preserve conservation laws.
   (Already verified in MAM-0 tests.)

2. Distributional confluence: the probability distribution over final
   microstates is identical regardless of event ordering.

3. Strong confluence: Comm_{e1} ∘ Comm_{e2}(R) = Comm_{e2} ∘ Comm_{e1}(R)
   for spacelike events e1, e2. Requires commutativity of the commit
   maps. This is the strongest condition and the one DET needs for
   spacelike-separated events on entangled systems.

For MAM-0, events on overlapping domains generally do NOT satisfy
strong confluence. This is the open Confluence problem (P0.1 §5.5).
"""

from __future__ import annotations

import itertools
import random
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

from det8.models.mam0 import (
    Actualizer,
    CommitMap,
    EventScheduler,
    LawMap,
    Record,
    Regime,
)


# ── Confluence Test Harness ────────────────────────────────────────────────


@dataclass
class ConfluenceResult:
    """Results of a confluence test between two event schedules."""

    schedule_name: str
    final_state: tuple[int, ...]
    conservation_ok: bool
    event_log: list[dict] = field(default_factory=list)


def test_confluence_two_schedules(
    initial_values: dict[int, int],
    schedule_1_events: list[tuple[int, int]],  # (node_a, node_b) pairs
    schedule_2_events: list[tuple[int, int]],
    seed: int = 42,
    n_trials: int = 1,
) -> dict:
    """Test confluence between two event schedules.

    For each trial, generates fresh random outcomes and compares
    the final microstate distribution.

    Args:
        initial_values: {node_id: initial_value} for all nodes.
        schedule_1_events: List of (a,b) event pairs in order.
        schedule_2_events: List of (a,b) event pairs in different order.
        seed: Random seed for reproducibility.
        n_trials: Number of Monte Carlo trials for distribution comparison.

    Returns:
        Dictionary with confluence analysis.
    """
    rng = random.Random(seed)

    # For distributional analysis, collect final states over many trials.
    final_states_1: list[tuple[int, ...]] = []
    final_states_2: list[tuple[int, ...]] = []

    invariants_1: list[int] = []
    invariants_2: list[int] = []

    for trial in range(n_trials):
        trial_seed = seed + trial

        # Schedule 1
        records_1 = {k: Record(v) for k, v in initial_values.items()}
        act_1 = Actualizer(seed=trial_seed)
        sched_1 = EventScheduler(records_1)

        for a, b in schedule_1_events:
            sched_1.schedule_event(f"e_{a}_{b}", a, b, Regime.OPEN, act_1)

        total_1, cons_1 = sched_1.verify_conservation()
        invariants_1.append(total_1 if cons_1 else -1)
        state_1 = tuple(records_1[k].value for k in sorted(records_1.keys()))
        final_states_1.append(state_1)

        # Schedule 2
        records_2 = {k: Record(v) for k, v in initial_values.items()}
        act_2 = Actualizer(seed=trial_seed)
        sched_2 = EventScheduler(records_2)

        for a, b in schedule_2_events:
            sched_2.schedule_event(f"e_{a}_{b}", a, b, Regime.OPEN, act_2)

        total_2, cons_2 = sched_2.verify_conservation()
        invariants_2.append(total_2 if cons_2 else -1)
        state_2 = tuple(records_2[k].value for k in sorted(records_2.keys()))
        final_states_2.append(state_2)

    # Distribution comparison.
    counter_1 = Counter(final_states_1)
    counter_2 = Counter(final_states_2)

    all_states = set(counter_1.keys()) | set(counter_2.keys())

    # Compute total variation distance between distributions.
    tvd = 0.0
    for state in all_states:
        p1 = counter_1.get(state, 0) / n_trials
        p2 = counter_2.get(state, 0) / n_trials
        tvd += abs(p1 - p2)
    tvd /= 2.0  # Normalize to [0, 1].

    # Check for exact state match (strong confluence) in single trial.
    exact_match = (n_trials == 1 and final_states_1[0] == final_states_2[0])

    return {
        "initial_values": initial_values,
        "schedule_1": schedule_1_events,
        "schedule_2": schedule_2_events,
        "n_trials": n_trials,
        "conservation_all_same": (
            len(set(invariants_1)) == 1
            and len(set(invariants_2)) == 1
            and invariants_1[0] == invariants_2[0]
            and invariants_1[0] >= 0
        ),
        "conservation_values": {
            "schedule_1": invariants_1[0],
            "schedule_2": invariants_2[0],
        },
        "exact_state_match": exact_match,
        "total_variation_distance": tvd,
        "distributional_confluence": tvd < 1e-12,
        "state_counts_1": dict(counter_1.most_common(5)),
        "state_counts_2": dict(counter_2.most_common(5)),
        "interpretation": _interpret_confluence(tvd, exact_match),
    }


def _interpret_confluence(tvd: float, exact_match: bool) -> str:
    if tvd < 1e-12:
        return "Distributional confluence: schedule order does not matter."
    elif tvd < 0.01 and not exact_match:
        return (
            "Near-confluence: distributions very close (TVD < 0.01). "
            "Microstates may differ occasionally but statistically equivalent."
        )
    else:
        return (
            "No confluence: schedule order matters. "
            "Events on overlapping domains are not commutative. "
            "This is the open Confluence problem (P0.1 §5.5)."
        )


# ── Specific Confluence Scenarios ───────────────────────────────────────────


def test_disjoint_domains() -> dict:
    """Test confluence for events on DISJOINT domains.

    Events on (0,1) and (2,3) have no shared nodes.
    Expected: strong confluence (commutative).
    """
    return test_confluence_two_schedules(
        initial_values={0: 5, 1: 5, 2: 5, 3: 5},
        schedule_1_events=[(0, 1), (2, 3)],
        schedule_2_events=[(2, 3), (0, 1)],
        seed=42,
        n_trials=100,
    )


def test_overlapping_domains() -> dict:
    """Test confluence for events on OVERLAPPING domains.

    Events on (0,1) and (1,2) share node 1.
    Expected: NO confluence (the Confluence problem).
    """
    return test_confluence_two_schedules(
        initial_values={0: 5, 1: 5, 2: 5},
        schedule_1_events=[(0, 1), (1, 2)],
        schedule_2_events=[(1, 2), (0, 1)],
        seed=42,
        n_trials=100,
    )


def test_single_node_multiple_events() -> dict:
    """Test confluence for multiple events on the SAME pair.

    Two events on (0,1) in different orders. But there's only one pair,
    so reordering is trivial.

    Expected: Yes, because the total transfer is the same regardless of
    whether we do event1 then event2 or event2 then event1... wait, no.
    The outcome of event1 changes the state, which changes the law map
    for event2. So the order DOES matter.

    But for MAM-0 transfers of ±1: the set of accessible states after
    two events may be the same regardless of order.
    """
    return test_confluence_two_schedules(
        initial_values={0: 5, 1: 5},
        schedule_1_events=[(0, 1), (0, 1)],
        schedule_2_events=[(0, 1), (0, 1)],  # Same schedule — trivially same.
        seed=42,
        n_trials=1,
    )


# ── Commutativity Check ─────────────────────────────────────────────────────


def check_commutativity(
    node_values: tuple[int, int],
    pair_1: tuple[int, int],
    pair_2: tuple[int, int],
) -> dict:
    """Check whether two events on given pairs commute for a specific state.

    For each possible outcome of event 1 and event 2, check whether
    the final state is the same regardless of order.

    Returns a commutativity matrix.
    """
    records = {
        pair_1[0]: Record(node_values[0]),
        pair_1[1]: Record(node_values[1]),
    }

    # Generate possibility objects.
    w1 = LawMap.generate(
        records[pair_1[0]], records[pair_1[1]], Regime.OPEN
    )
    w2 = LawMap.generate(
        records[pair_2[0]], records[pair_2[1]], Regime.OPEN
    )

    commutes_all = True
    failures = []

    for outcome_1 in w1.omega:
        for outcome_2 in w2.omega:
            # Order: 1 then 2.
            r_a = Record(node_values[0])
            r_b = Record(node_values[1])
            # Apply event 1.
            CommitMap.commit(r_a, r_b, outcome_1)
            # Generate fresh w2 from new state.
            w2_after_1 = LawMap.generate(r_a, r_b, Regime.OPEN)
            # Check if outcome_2 is still valid.
            if outcome_2 not in w2_after_1.omega:
                commutes_all = False
                failures.append(
                    {
                        "outcome_1": outcome_1,
                        "outcome_2": outcome_2,
                        "issue": "outcome_2 not valid after event 1",
                    }
                )
                continue
            CommitMap.commit(r_a, r_b, outcome_2)
            final_12 = (r_a.value, r_b.value)

            # Order: 2 then 1.
            r_a2 = Record(node_values[0])
            r_b2 = Record(node_values[1])
            CommitMap.commit(r_a2, r_b2, outcome_2)
            w1_after_2 = LawMap.generate(r_a2, r_b2, Regime.OPEN)
            if outcome_1 not in w1_after_2.omega:
                commutes_all = False
                failures.append(
                    {
                        "outcome_1": outcome_1,
                        "outcome_2": outcome_2,
                        "issue": "outcome_1 not valid after event 2",
                    }
                )
                continue
            CommitMap.commit(r_a2, r_b2, outcome_1)
            final_21 = (r_a2.value, r_b2.value)

            if final_12 != final_21:
                commutes_all = False
                failures.append(
                    {
                        "outcome_1": outcome_1,
                        "outcome_2": outcome_2,
                        "final_12": final_12,
                        "final_21": final_21,
                        "issue": "final states differ",
                    }
                )

    return {
        "node_values": node_values,
        "pair_1": pair_1,
        "pair_2": pair_2,
        "omega_1_size": len(w1.omega),
        "omega_2_size": len(w2.omega),
        "commutes": commutes_all,
        "n_outcome_pairs": len(w1.omega) * len(w2.omega),
        "failures": failures[:5],  # First 5 failures only.
    }
